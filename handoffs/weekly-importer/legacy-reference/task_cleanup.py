#!/usr/bin/env python3
"""Cleanup FPO and 13wk tasks without owners from Airtable Tasks table.

Usage:
    python task_cleanup.py --dry-run    # Preview only
    python task_cleanup.py --execute   # Delete after confirmation

Requires Airtable API token via interactive prompt or environment variable.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests


# --- Configuration ---
BASE_ID = "appOMWiK4CTOH7iQu"
TASKS_TABLE_ID = "tblS2my1r93KothyZ"  # AutoPM Tasks
TARGET_NAMES = ["FPO Release Date", "13wk Plan Release Date"]
OWNER_FIELD = "Tasks Owners (Manual)"
NAME_FIELD = "Task Name (Manual)"

LOG_DIR = Path("D:/个人资料/AI学习圈/SN Auto PM/weekly_importer/logs")


class AirtableClient:
    """Reusable Airtable client with pagination."""

    BASE_URL = "https://api.airtable.com"

    def __init__(self, api_token: str, base_id: str) -> None:
        self.api_token = api_token
        self.base_id = base_id
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(3):
            try:
                response = requests.request(
                    method, url, headers=self.headers, timeout=30, **kwargs
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as exc:
                status = exc.response.status_code if exc.response else 0
                if status in (429, 500, 502, 503, 504):
                    time.sleep(2**attempt)
                    continue
                raise
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                time.sleep(2**attempt)
                continue
        raise RuntimeError("Request failed after all retries")

    def get_records_by_name(
        self,
        table_id: str,
        task_name: str,
        page_size: int = 100,
    ) -> list[dict[str, Any]]:
        """Fetch records matching a specific task name via filter formula."""
        formula = f"{{{NAME_FIELD}}}='{task_name}'"
        params = f"pageSize={page_size}&filterByFormula={quote(formula)}"
        data = self._request("GET", f"v0/{self.base_id}/{table_id}?{params}")
        return data.get("records", [])

    def delete_record(self, table_id: str, record_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"v0/{self.base_id}/{table_id}/{record_id}")


def get_token() -> str:
    token = os.environ.get("AIRTABLE_API_TOKEN", "")
    if token:
        return token
    token = input("Enter Airtable API token: ").strip()
    if not token:
        print("Error: Token is required.", file=sys.stderr)
        sys.exit(1)
    return token


def fetch_candidates(client: AirtableClient) -> list[dict[str, Any]]:
    """Fetch tasks by name via formula, then filter locally for empty owner."""
    all_matched: list[dict[str, Any]] = []
    seen_ids = set()

    for task_name in TARGET_NAMES:
        print(f"Querying '{task_name}'...")
        records = client.get_records_by_name(TASKS_TABLE_ID, task_name)
        print(f"  Found {len(records)} records with this name.")

        for rec in records:
            rid = rec["id"]
            if rid in seen_ids:
                continue
            seen_ids.add(rid)

            fields = rec.get("fields", {})
            owner = fields.get(OWNER_FIELD)
            if not owner:
                all_matched.append(rec)

    print(f"\nTotal with empty owner: {len(all_matched)}")
    return all_matched


def preview(records: list[dict[str, Any]]) -> None:
    if not records:
        print("\nNo records match the criteria. Nothing to delete.")
        return
    print(f"\n=== PREVIEW: {len(records)} records to DELETE ===\n")
    print(f"{'#':<5} {'Record ID':<20} {'Name':<30} {'Owner':<15}")
    print("-" * 70)
    for i, rec in enumerate(records, 1):
        rid = rec.get("id", "")
        fields = rec.get("fields", {})
        name = str(fields.get(NAME_FIELD, ""))[:28]
        owner = str(fields.get(OWNER_FIELD, "(empty)"))[:13]
        print(f"{i:<5} {rid:<20} {name:<30} {owner:<15}")
    print("-" * 70)
    print(f"\nTotal: {len(records)} records will be DELETED if you run with --execute.")


def execute_deletions(
    client: AirtableClient, records: list[dict[str, Any]]
) -> tuple[dict[str, int], list[dict[str, Any]]]:
    stats: dict[str, int] = {"deleted": 0, "failed": 0, "total": len(records)}
    failed_records: list[dict[str, Any]] = []

    print(f"\nStarting deletion of {len(records)} records...")
    for i, rec in enumerate(records, 1):
        rid = rec["id"]
        name = rec.get("fields", {}).get(NAME_FIELD, "")
        print(f"  [{i}/{len(records)}] Deleting {rid} ({name})...", end=" ")
        try:
            client.delete_record(TASKS_TABLE_ID, rid)
            stats["deleted"] += 1
            print("OK")
        except Exception as exc:
            stats["failed"] += 1
            failed_records.append({"id": rid, "name": name, "error": str(exc)})
            print(f"FAILED: {exc}")
        time.sleep(0.15)  # rate limit courtesy

    return stats, failed_records


def write_log(
    records: list[dict[str, Any]],
    stats: dict[str, int],
    failed: list[dict[str, Any]],
    executed: bool,
) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = "EXECUTED" if executed else "DRYRUN"
    log_path = LOG_DIR / f"task_cleanup_{mode}_{timestamp}.json"

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "base_id": BASE_ID,
        "table_id": TASKS_TABLE_ID,
        "criteria": {
            "name_in": TARGET_NAMES,
            "owner_empty": True,
        },
        "total_candidates": len(records),
        "deleted": stats.get("deleted", 0),
        "failed": stats.get("failed", 0),
        "records": [
            {
                "id": r["id"],
                "name": r.get("fields", {}).get(NAME_FIELD, ""),
                "owner": r.get("fields", {}).get(OWNER_FIELD, ""),
            }
            for r in records
        ],
        "failed_records": failed,
    }

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    print(f"\nLog saved to: {log_path}")
    return log_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean up orphaned FPO/13wk tasks")
    parser.add_argument("--dry-run", action="store_true", help="Preview only (default)")
    parser.add_argument(
        "--execute", action="store_true", help="Actually delete records"
    )
    args = parser.parse_args()

    if args.execute:
        confirm = input(
            "\n⚠️  This will PERMANENTLY DELETE records. Type 'DELETE' to confirm: "
        )
        if confirm.strip() != "DELETE":
            print("Aborted.")
            sys.exit(0)

    token = get_token()
    client = AirtableClient(token, BASE_ID)

    records = fetch_candidates(client)
    preview(records)

    if not records:
        write_log(records, {}, [], executed=False)
        return

    if args.execute:
        stats, failed = execute_deletions(client, records)
        write_log(records, stats, failed, executed=True)
        print(f"\n=== RESULT ===")
        print(f"Deleted: {stats['deleted']}")
        print(f"Failed:  {stats['failed']}")
    else:
        print("\nThis was a DRY RUN. No records were deleted.")
        write_log(records, {}, [], executed=False)
        print("\nTo actually delete, run: python task_cleanup.py --execute")


if __name__ == "__main__":
    main()
