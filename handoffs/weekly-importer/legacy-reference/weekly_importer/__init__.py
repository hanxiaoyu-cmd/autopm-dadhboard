"""Weekly Report Importer for Airtable.

This package imports weekly progress reports from Excel files into Airtable
Projects table, merging them into the Engineering remark field with
delta-only updates and legacy format cleanup support.

New capabilities (v1.2):
- Export Airtable → local Excel (All Tracker format)
- Sync local Excel changes back to Airtable (with conflict detection)
"""

__version__ = "1.2.0"
__author__ = "AutoPM Team"

from .config import load_config
from .api_client import AirtableClient
from .remark_engine import read_weekly_remark, merge_weekly_remark
from .cleaner import RemarkCleaner
from .importer import WeeklyImporter
from .exporter import AllTrackerExporter
from .ledger_sync import LedgerSync

__all__ = [
    "load_config",
    "AirtableClient",
    "read_weekly_remark",
    "merge_weekly_remark",
    "RemarkCleaner",
    "WeeklyImporter",
    "AllTrackerExporter",
    "LedgerSync",
]
