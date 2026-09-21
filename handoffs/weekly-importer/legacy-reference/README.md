# Weekly Report Importer for Airtable

A standalone Python package to import weekly progress reports from Excel **ALL Tracker** files into Airtable **Projects** table, with delta-only updates and legacy format cleanup.

## Features

- **Delta-only updates**: Appends new weekly progress only when content changes, avoiding repetition
- **Plain-text format**: Writes clean `--- YYYY-MM-DD ---` blocks without AUTOPM wrappers
- **Legacy cleanup**: Removes old `[[AUTOPM_WEEKLY_REPORT]]` blocks while preserving manual notes
- **Batch updates**: Handles large bases with automatic pagination and retry logic
- **Dry-run mode**: Preview all changes before writing to Airtable

## Installation

### Option 1: Install from source

```bash
git clone https://github.com/your-repo/weekly-importer.git
cd weekly-importer
pip install -r requirements.txt
```

### Option 2: Copy folder directly

1. Copy the `weekly_importer/` folder to your project
2. Run `pip install -r requirements.txt`

## Quick Start

### 1. Generate config template

```bash
python -m weekly_importer --init-config
```

This creates `weekly_importer.json`. Edit it with your credentials:

```json
{
  "api_token": "patXXXXXXXXXXXXXXXX",
  "base_id": "appXXXXXXXXXXXXXXXX",
  "projects_table_id": "tbllvOHZdwfBRWGM0",
  "remark_field": "Engineering remark(Manual)",
  "project_name_field": "Project name (Manual)"
}
```

**Security note**: Never commit your API token. Use environment variables instead:

```bash
export AIRTABLE_API_TOKEN="patXXXXXXXXXXXXXXXX"
export AIRTABLE_BASE_ID="appXXXXXXXXXXXXXXXX"
```

### 2. Preview changes (dry-run)

```bash
python -m weekly_importer --excel "All Projects Tracker.xlsx" --dry-run
```

### 3. Execute import

```bash
python -m weekly_importer --excel "All Projects Tracker.xlsx"
```

### 4. Clean legacy blocks

```bash
python -m weekly_importer --clean
```

## Usage as Library

```python
from weekly_importer import load_config, AirtableClient, WeeklyImporter

config = load_config("weekly_importer.json")
client = AirtableClient(api_token=config["api_token"], base_id=config["base_id"])

importer = WeeklyImporter(
    client=client,
    projects_table_id=config["projects_table_id"],
)

result = importer.import_from_excel(
    excel_path="All Projects Tracker.xlsx",
    dry_run=True,  # Set False to apply
)

print(f"Applied: {result['applied']}, Skipped: {result['skipped']}, Failed: {result['failed']}")
```

## Excel Format Expected

| Column | Header | Description |
|--------|--------|-------------|
| C7 | `Project Name , Description` | Project name (matched to Airtable) |
| C34 | `Engineering Remarks` | Weekly progress content |
| C2 | `Date Added` | Report date (used if `--date` not specified) |

## Architecture

```
weekly_importer/
├── __init__.py        # Package exports
├── __main__.py        # CLI entry point
├── config.py          # Configuration loader (env + JSON)
├── api_client.py      # Airtable API client with retry
├── remark_engine.py   # Remark parser/merger (delta-only)
├── cleaner.py         # Legacy block cleaner
└── importer.py        # Main import orchestrator
```

## Configuration Options

| Key | Default | Description |
|-----|---------|-------------|
| `api_token` | *required* | Airtable personal access token |
| `base_id` | *required* | Airtable base ID |
| `projects_table_id` | `Projects` | Projects table name or ID |
| `remark_field` | `Engineering remark(Manual)` | Target field for weekly reports |
| `project_name_field` | `Project name (Manual)` | Matching key field |
| `batch_size` | `10` | Records per API request (Airtable limit) |
| `request_timeout` | `30` | HTTP timeout in seconds |
| `max_retries` | `3` | Retry count for failed requests |
| `retry_delay` | `1.0` | Initial retry delay in seconds |

## Troubleshooting

### "Config file not found"
Run `python -m weekly_importer --init-config` to create a template.

### "Missing Airtable API token"
Set `AIRTABLE_API_TOKEN` environment variable or add `api_token` to config file.

### Connection errors
Increase `retry_delay` and `max_retries` in config for unstable networks.

### Partial failures
Check `result["failed"]` count. Failed records usually mean Project Name mismatch between Excel and Airtable. Ensure names match exactly (case-sensitive, but leading/trailing spaces are trimmed).

## License

Internal use only — AutoPM Team
