"""Main weekly report importer orchestrating Excel to Airtable sync.

Workflow:
1. Read Excel ALL Tracker file
2. Map Project Name to Airtable Projects records
3. Merge weekly progress into Engineering remark field
4. Batch update Airtable
"""

from __future__ import annotations

import json
import re
from datetime import date as _date
from pathlib import Path
from typing import Any

import openpyxl

from .api_client import AirtableClient
from .remark_engine import merge_weekly_remark


def _valid_date(value: str) -> bool:
    """Return True if value is a valid YYYY-MM-DD date string."""
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value
    ):
        return False
    try:
        _date.fromisoformat(value)
        return True
    except ValueError:
        return False


class WeeklyImporter:
    """Import weekly progress reports from Excel to Airtable."""

    def __init__(
        self,
        client: AirtableClient,
        projects_table_id: str,
        remark_field: str = "Engineering remark(Manual)",
        project_name_field: str = "Project name (Manual)",
        batch_size: int = 10,
    ) -> None:
        self.client = client
        self.projects_table_id = projects_table_id
        self.remark_field = remark_field
        self.project_name_field = project_name_field
        self.batch_size = batch_size

    def import_from_excel(
        self,
        excel_path: str | Path,
        *,
        sheet_name: str = "ALL PROJECTS",
        date_column: str = "Date Added",
        progress_column: str = "Engineering Remarks",
        project_name_column: str = "Project Name , Description",
        report_date: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Import weekly reports from Excel file.

        Args:
            excel_path: Path to ALL Tracker Excel file.
            sheet_name: Worksheet name to read.
            date_column: Column header for report date (used if report_date not given).
            progress_column: Column header for progress content.
            project_name_column: Column header for project name.
            report_date: Override date (YYYY-MM-DD). If None, uses date_column value.
            dry_run: If True, only preview changes without writing to Airtable.

        Returns:
            Statistics dict with applied, skipped, failed, total counts.
        """
        # Load Excel data
        wb = openpyxl.load_workbook(str(excel_path), data_only=True)
        sheet = wb[sheet_name]

        # Map headers to column indices
        headers = {}
        for col in range(1, sheet.max_column + 1):
            val = sheet.cell(row=2, column=col).value
            if val:
                headers[str(val).strip()] = col

        # Extract weekly data
        weekly_data = []
        for row in range(3, sheet.max_row + 1):
            name = sheet.cell(row=row, column=headers.get(project_name_column, 0)).value
            progress = sheet.cell(row=row, column=headers.get(progress_column, 0)).value
            date_val = sheet.cell(row=row, column=headers.get(date_column, 0)).value

            if name and progress:
                weekly_data.append(
                    {
                        "project_name": str(name).strip(),
                        "progress": str(progress).strip(),
                        "date": str(date_val)[:10] if date_val else report_date,
                    }
                )

        if not weekly_data:
            return {
                "status": "no_data",
                "applied": 0,
                "skipped": 0,
                "failed": 0,
                "total": 0,
            }

        # Fetch Airtable projects
        projects = self.client.get_records(
            self.projects_table_id,
            fields=[self.project_name_field, self.remark_field],
        )

        # Build name -> record mapping
        project_map = {}
        for rec in projects:
            name = rec.get("fields", {}).get(self.project_name_field, "")
            if name:
                project_map[str(name).strip()] = rec

        # Prepare updates
        updates = []
        stats = {"applied": 0, "skipped": 0, "failed": 0, "total": len(weekly_data)}

        for item in weekly_data:
            rec = project_map.get(item["project_name"])
            if not rec:
                stats["failed"] += 1
                continue

            current_remark = rec.get("fields", {}).get(self.remark_field, "") or ""
            target_date = report_date or item["date"]

            if not target_date or not _valid_date(target_date):
                stats["skipped"] += 1
                continue

            new_remark = merge_weekly_remark(
                current_remark,
                target_date,
                {"current_progress": item["progress"]},
            )

            if new_remark == current_remark:
                stats["skipped"] += 1
                continue

            updates.append(
                {
                    "id": rec["id"],
                    "fields": {self.remark_field: new_remark},
                }
            )

        if dry_run:
            return {
                "status": "dry_run",
                "applied": 0,
                "skipped": stats["skipped"],
                "failed": stats["failed"],
                "total": stats["total"],
                "preview_count": len(updates),
            }

        # Execute batch updates
        for i in range(0, len(updates), self.batch_size):
            batch = updates[i : i + self.batch_size]
            try:
                self.client.patch_records(self.projects_table_id, batch)
                stats["applied"] += len(batch)
            except Exception:
                # Fallback to individual updates
                for update in batch:
                    try:
                        self.client.patch_records(self.projects_table_id, [update])
                        stats["applied"] += 1
                    except Exception:
                        stats["failed"] += 1

        return stats

    def save_mappings(
        self,
        excel_path: str | Path,
        output_path: str | Path,
        **kwargs: Any,
    ) -> None:
        """Save Excel to Airtable mappings to JSON for inspection."""
        result = self.import_from_excel(excel_path, dry_run=True, **kwargs)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
