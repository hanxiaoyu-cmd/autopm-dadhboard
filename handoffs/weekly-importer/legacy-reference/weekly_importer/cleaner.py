"""Engineering remark cleaner to remove legacy AutoPM weekly blocks.

Preserves manual notes outside the automated blocks.
"""

from __future__ import annotations

import re
from typing import Any

from .api_client import AirtableClient

# Pattern to match legacy AUTOPM weekly report blocks
BLOCK_PATTERN = re.compile(
    r"\[\[AUTOPM_?WEEKLY_REPORT:v1\]\].*?\[\[/AUTOPM_?WEEKLY_REPORT\]\]",
    re.DOTALL,
)


def clean_remark(
    text: str,
    *,
    collapse_lines: bool = True,
) -> str:
    """Remove AutoPM weekly report blocks from remark text.

    Args:
        text: Original Engineering remark text.
        collapse_lines: Whether to collapse multiple blank lines to two.

    Returns:
        Cleaned text with manual notes preserved.
    """
    if not text:
        return text

    cleaned = BLOCK_PATTERN.sub("", text).strip()

    if collapse_lines:
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned


class RemarkCleaner:
    """Batch cleaner for Airtable Engineering remark fields."""

    def __init__(
        self,
        client: AirtableClient,
        table_id: str,
        field_name: str = "Engineering remark(Manual)",
        batch_size: int = 10,
    ) -> None:
        self.client = client
        self.table_id = table_id
        self.field_name = field_name
        self.batch_size = batch_size

    def clean_all(self) -> dict[str, int]:
        """Clean legacy blocks from all records in the table.

        Returns:
            Statistics dict with keys: cleaned, skipped, errors, total.
        """
        records = self.client.get_records(
            self.table_id,
            fields=[self.field_name],
            page_size=100,
        )

        stats = {"cleaned": 0, "skipped": 0, "errors": 0, "total": len(records)}
        updates = []

        for rec in records:
            rid = rec["id"]
            raw = rec.get("fields", {}).get(self.field_name, "") or ""

            if not raw:
                stats["skipped"] += 1
                continue

            cleaned = clean_remark(raw)

            if cleaned == raw.strip():
                stats["skipped"] += 1
                continue

            updates.append(
                {
                    "id": rid,
                    "fields": {self.field_name: cleaned},
                }
            )

            if len(updates) >= self.batch_size:
                stats["cleaned"] += self._batch_update(updates)
                updates = []

        if updates:
            stats["cleaned"] += self._batch_update(updates)

        return stats

    def _batch_update(self, updates: list[dict[str, Any]]) -> int:
        """Send batch update and return count of successful updates."""
        try:
            self.client.patch_records(self.table_id, updates)
            return len(updates)
        except Exception:
            # Fall back to individual updates on batch failure
            success = 0
            for update in updates:
                try:
                    self.client.patch_records(self.table_id, [update])
                    success += 1
                except Exception:
                    pass
            return success
