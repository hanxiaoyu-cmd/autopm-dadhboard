#!/usr/bin/env python3
"""Entry point for Weekly Report Importer.

No arguments: launches GUI.
With arguments: uses command-line interface.

Usage:
    weekly_importer.exe                    # Launch GUI (no arguments)
    weekly_importer.exe --help             # Show CLI help
    weekly_importer.exe --init-config     # Generate config template (CLI)
    weekly_importer.exe --excel "file.xlsx" --dry-run  # CLI import

See README.md for full documentation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def init_config(path: str) -> None:
    """Generate a template configuration file."""
    template = {
        "api_token": "your_airtable_api_token_here",
        "base_id": "your_base_id_here",
        "projects_table_id": "Projects",
        "remark_field": "Engineering remark(Manual)",
        "project_name_field": "Project name (Manual)",
        "batch_size": 10,
        "request_timeout": 30,
        "max_retries": 3,
        "retry_delay": 1.0,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    print(f"Template config written to: {path}")
    print("Please edit the file and add your Airtable API token and base ID.")


def run_cli() -> int:
    """Run command-line interface."""
    from weekly_importer import (
        AirtableClient,
        WeeklyImporter,
        RemarkCleaner,
        load_config,
    )

    parser = argparse.ArgumentParser(
        description="Import weekly progress reports from Excel to Airtable"
    )
    parser.add_argument(
        "--config",
        "-c",
        default="weekly_importer.json",
        help="Path to JSON configuration file (default: weekly_importer.json)",
    )
    parser.add_argument(
        "--excel",
        "-e",
        help="Path to Excel ALL Tracker file",
    )
    parser.add_argument(
        "--sheet",
        default="ALL PROJECTS",
        help="Excel sheet name (default: ALL PROJECTS)",
    )
    parser.add_argument(
        "--date",
        help="Report date override (YYYY-MM-DD). If omitted, uses Excel date column",
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Preview changes without writing to Airtable",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean legacy AutoPM weekly blocks from Engineering remark",
    )
    parser.add_argument(
        "--init-config",
        action="store_true",
        help="Generate a template configuration file and exit",
    )
    parser.add_argument(
        "--save-mappings",
        help="Save Excel-to-Airtable match preview to JSON file (dry-run only)",
    )

    args = parser.parse_args()

    if args.init_config:
        init_config(args.config)
        return 0

    # Load configuration
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"Error: Config file not found: {args.config}")
        print("Run with --init-config to generate a template.")
        return 1
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1

    # Initialize API client
    client = AirtableClient(
        api_token=config["api_token"],
        base_id=config["base_id"],
        request_timeout=config.get("request_timeout", 30),
        max_retries=config.get("max_retries", 3),
        retry_delay=config.get("retry_delay", 1.0),
    )

    if args.clean:
        print("Starting remark cleanup...")
        cleaner = RemarkCleaner(
            client=client,
            table_id=config.get("projects_table_id", "Projects"),
            field_name=config.get("remark_field", "Engineering remark(Manual)"),
            batch_size=config.get("batch_size", 10),
        )
        stats = cleaner.clean_all()
        print(f"\nCleanup complete:")
        print(f"  Total records: {stats['total']}")
        print(f"  Cleaned: {stats['cleaned']}")
        print(f"  Skipped: {stats['skipped']}")
        print(f"  Errors: {stats['errors']}")
        return 0 if stats["errors"] == 0 else 1

    if not args.excel:
        print("Error: --excel is required (unless using --clean or --init-config)")
        return 1

    excel_path = Path(args.excel)
    if not excel_path.exists():
        print(f"Error: Excel file not found: {excel_path}")
        return 1

    # Initialize importer
    importer = WeeklyImporter(
        client=client,
        projects_table_id=config.get("projects_table_id", "Projects"),
        remark_field=config.get("remark_field", "Engineering remark(Manual)"),
        project_name_field=config.get("project_name_field", "Project name (Manual)"),
        batch_size=config.get("batch_size", 10),
    )

    print(f"Importing from: {excel_path}")
    print(f"Sheet: {args.sheet}")
    print(f"Mode: {'DRY-RUN (no changes)' if args.dry_run else 'LIVE'}")
    if args.date:
        print(f"Report date override: {args.date}")

    # Execute import
    result = importer.import_from_excel(
        excel_path=excel_path,
        sheet_name=args.sheet,
        report_date=args.date,
        dry_run=args.dry_run,
    )

    print(f"\nImport complete:")
    print(f"  Status: {result['status']}")
    print(f"  Total Excel rows: {result['total']}")
    print(f"  Applied: {result['applied']}")
    print(f"  Skipped: {result['skipped']}")
    print(f"  Failed: {result['failed']}")

    if args.save_mappings and args.dry_run:
        importer.save_mappings(
            excel_path, args.save_mappings, sheet_name=args.sheet, report_date=args.date
        )
        print(f"  Preview saved to: {args.save_mappings}")

    return 0


def run_gui() -> None:
    """Run graphical user interface."""
    # Ensure package is importable when frozen by PyInstaller
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        import os

        exe_dir = os.path.dirname(sys.executable)
        if exe_dir not in sys.path:
            sys.path.insert(0, exe_dir)

    from weekly_importer.gui import main as gui_main

    gui_main()


def main() -> int:
    """Entry point: auto-detect CLI vs GUI mode."""
    # If any arguments provided (other than the script name), use CLI
    if len(sys.argv) > 1:
        return run_cli()
    else:
        # No arguments: launch GUI
        run_gui()
        return 0


if __name__ == "__main__":
    sys.exit(main())
