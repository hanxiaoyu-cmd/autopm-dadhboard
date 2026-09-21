"""Airtable API client with retry and batch support."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.parse import quote

import requests


class AirtableClient:
    """Low-level Airtable API client with automatic retry logic."""

    BASE_URL = "https://api.airtable.com"

    def __init__(self, api_token: str, base_id: str, **options: Any) -> None:
        self.api_token = api_token
        self.base_id = base_id
        self.timeout = options.get("request_timeout", 30)
        self.max_retries = options.get("max_retries", 3)
        self.retry_delay = options.get("retry_delay", 1.0)
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute HTTP request with exponential backoff retry."""
        url = f"{self.BASE_URL}/{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method, url, headers=self.headers, timeout=self.timeout, **kwargs
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as exc:
                status = exc.response.status_code if exc.response else 0
                if status in (429, 500, 502, 503, 504):
                    last_error = exc
                    wait = self.retry_delay * (2**attempt)
                    time.sleep(wait)
                    continue
                raise
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ) as exc:
                last_error = exc
                wait = self.retry_delay * (2**attempt)
                time.sleep(wait)
                continue

        raise last_error or RuntimeError("Request failed after all retries")

    def get_records(
        self,
        table_id: str,
        fields: list[str] | None = None,
        filter_formula: str | None = None,
        page_size: int = 100,
    ) -> list[dict[str, Any]]:
        """Fetch all records from a table with automatic pagination."""
        params: dict[str, Any] = {"pageSize": page_size}
        if fields:
            for f in fields:
                params.setdefault("fields[]", []).append(f)
        if filter_formula:
            params["filterByFormula"] = filter_formula

        records: list[dict[str, Any]] = []
        offset = None

        while True:
            if offset:
                params["offset"] = offset

            query_parts: list[str] = []
            for k, v in params.items():
                if isinstance(v, list):
                    for item in v:
                        query_parts.append(f"{k}={quote(str(item))}")
                else:
                    query_parts.append(f"{k}={quote(str(v))}")
            query = "&".join(query_parts)

            data: dict[str, Any] = self._request(
                "GET", f"v0/{self.base_id}/{table_id}?{query}"
            )
            batch = data.get("records", [])
            records.extend(batch)
            offset = data.get("offset")
            if not offset:
                break

        return records

    def patch_records(
        self,
        table_id: str,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Batch update records (max 10 per Airtable API)."""
        return self._request(
            "PATCH",
            f"v0/{self.base_id}/{table_id}",
            json={"records": records},
        )

    def get_table_meta(self) -> dict[str, Any]:
        """Fetch base metadata including table schemas."""
        return self._request("GET", f"v0/meta/bases/{self.base_id}/tables")

    def list_bases(self) -> list[dict[str, Any]]:
        """List all bases accessible with the current token.

        Returns:
            List of base dicts with 'id', 'name' and 'permissionLevel' keys.
        """
        data: dict[str, Any] = self._request("GET", "v0/meta/bases")
        return data.get("bases", [])
