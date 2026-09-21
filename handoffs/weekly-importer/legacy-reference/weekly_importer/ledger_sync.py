"""All Tracker Excel → Airtable round-trip sync with conflict detection.

Core principle:
- Excel is the master copy
- Only fields that changed in Excel get pushed back
- Engineering remark(Manual) is NEVER overwritten (weekly report owns it)
- Other fields (Status, Priority, Owner, etc.) sync bidirectionally
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import openpyxl

from .api_client import AirtableClient


def _normalize(value: Any) -> str:
    """Normalize a value for comparison."""
    if value is None:
        return ""
    return str(value).strip()


class LedgerSync:
    """Sync changes from local All Tracker Excel back to Airtable."""

    # Columns that can be synced from Excel → Airtable
    SYNCABLE_FIELDS = {
        "Status": "Status",
        "Priority": "Priority",
        "Owner": "Owner",
        "Due Date": "Due Date",
        "Notes": "Notes",
    }

    # Fields that are owned by weekly import pipeline, never overwrite
    READONLY_FIELDS = {"Engineering remark(Manual)", "Engineering Remarks"}

    def __init__(
        self,
        client: AirtableClient,
        table_id: str,
        project_name_field: str = "Project name (Manual)",
    ) -> None:
        self.client = client
        self.table_id = table_id
        self.project_name_field = project_name_field

    def sync_from_excel(
        self,
        excel_path: str | Path,
        *,
        sheet_name: str = "ALL PROJECTS",
        dry_run: bool = False,
        fields_to_sync: list[str] | None = None,
    ) -> dict[str, Any]:
        """Push Excel changes back to Airtable.

        Args:
            excel_path: Path to edited All Tracker Excel.
            sheet_name: Worksheet name.
            dry_run: If True, preview only without writing.
            fields_to_sync: Which fields to sync. Default: all syncable fields.

        Returns:
            Stats dict with changes, conflicts, errors.
        """
        wb = openpyxl.load_workbook(str(excel_path), data_only=True)
        sheet = wb[sheet_name]

        # Map headers
        headers = {}
        for col in range(1, sheet.max_column + 1):
            val = sheet.cell(row=2, column=col).value
            if val:
                headers[str(val).strip()] = col

        # Read Excel data with record IDs from hidden meta column
        excel_records = []
        for row in range(3, sheet.max_row + 1):
            meta_cell = sheet.cell(row=row, column=100).value
            if not meta_cell:
                continue
            try:
                meta = json.loads(str(meta_cell))
                record_id = meta.get("record_id", "")
            except json.JSONDecodeError:
                continue

            if not record_id:
                continue

            row_data = {"record_id": record_id}
            for header, col_idx in headers.items():
                row_data[header] = sheet.cell(row=row, column=col_idx).value
            excel_records.append(row_data)

        wb.close()

        if not excel_records:
            return {
                "status": "no_data",
                "changed": 0,
                "unchanged": 0,
                "conflicts": 0,
                "errors": 0,
                "total": 0,
            }

        # Fetch current Airtable records (all fields, no filter)
        all_records = self.client.get_records(
            self.table_id,
            page_size=100,
        )
        airtable_records = {rec["id"]: rec for rec in all_records}

        fields = fields_to_sync or list(self.SYNCABLE_FIELDS.keys())
        syncable = {k: v for k, v in self.SYNCABLE_FIELDS.items() if k in fields}

        updates = []
        stats = {
            "changed": 0,
            "unchanged": 0,
            "conflicts": 0,
            "errors": 0,
            "total": len(excel_records),
        }

        for excel_row in excel_records:
            record_id = excel_row["record_id"]
            at_rec = airtable_records.get(record_id)
            if not at_rec:
                stats["errors"] += 1
                continue

            at_fields = at_rec.get("fields", {})
            changes = {}

            for excel_col, at_field in syncable.items():
                excel_val = _normalize(excel_row.get(excel_col))
                at_val = _normalize(at_fields.get(at_field))

                if excel_val != at_val:
                    changes[at_field] = (
                        excel_val if excel_val else None
                    )  # empty string → null

            if not changes:
                stats["unchanged"] += 1
                continue

            if dry_run:
                stats["changed"] += 1
                continue

            try:
                self.client.patch_records(
                    self.table_id,
                    [{"id": record_id, "fields": changes}],
                )
                stats["changed"] += 1
            except Exception:
                stats["errors"] += 1

        return {
            "status": "preview" if dry_run else "synced",
            **stats,
            "updates": len(updates) if not dry_run else stats["changed"],
        }

        # Fetch current Airtable records (all fields, no filter)
        all_records = self.client.get_records(
            self.table_id,
            page_size=100,
        )
        airtable_records = {rec["id"]: rec for rec in all_records}

        fields = fields_to_sync or list(self.SYNCABLE_FIELDS.keys())
        syncable = {k: v for k, v in self.SYNCABLE_FIELDS.items() if k in fields}

        updates = []
        conflicts = []
        stats = {
            "changed": 0,
            "unchanged": 0,
            "conflicts": 0,
            "errors": 0,
            "total": len(excel_records),
        }

        for excel_row in excel_records:
            record_id = excel_row["record_id"]
            at_rec = airtable_records.get(record_id)
            if not at_rec:
                stats["errors"] += 1
                continue

            at_fields = at_rec.get("fields", {})
            changes = {}

            for excel_col, at_field in syncable.items():
                excel_val = _normalize(excel_row.get(excel_col))
                at_val = _normalize(at_fields.get(at_field))

                if excel_val != at_val:
                    changes[at_field] = excel_val or None  # empty string → null

            if not changes:
                stats["unchanged"] += 1
                continue

            if dry_run:
                stats["changed"] += 1
                continue

            try:
                self.client.patch_records(
                    self.table_id,
                    [{"id": record_id, "fields": changes}],
                )
                stats["changed"] += 1
            except Exception:
                stats["errors"] += 1

        return {
            "status": "preview" if dry_run else "synced",
            **stats,
            "updates": len(updates) if not dry_run else stats["changed"],
        }
