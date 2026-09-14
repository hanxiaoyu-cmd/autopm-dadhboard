# AutoPM Microsoft migration engineering

## Status as of 2026-09-10

Implementation has started, but the approved plan is **not fully implemented**.
This directory contains executable offline migration preparation, not a deployed
Dataverse solution or a replacement local web application.

The user confirmed IT approval and Dataverse access are still pending. Live UI
verification in the default environment showed the insufficient-privilege banner,
disabled table creation commands and `使用 Dataverse 生成应用(0)` in the environment
selector. Existing Power Apps/SharePoint production data was not changed.

## Implemented

- `tools/prepare_migration.py`: preserves every normalized source row, validates
  unique identities and orphan links, derives distinct Program/Project relations,
  retains historical relations, produces a discrepancy CSV and integrity manifest.
- `tools/preview_weekly.py`: reuses the existing Bridge parser in read-only mode;
  does not load sync_config.json, instantiate Airtable, or call cloud services.
- `tests/test_migration.py`: eight tests for many-to-many relations, duplicate
  identities, orphan links, unassigned projects, status isolation and determinism.
- `functional-parity.csv`: twelve feature groups with source evidence, target,
  actual progress and acceptance criteria. This is not an exhaustive live
  automation/field inventory; R0 remains open until those dependencies are checked.

## First snapshot audit

Source: `outputs/program-mvp/normalized-data.json` in the workspace.
151 Programs, 2,997 Projects, 9,926 SKUs, 2,923 Project/SKU source links retained.
481 historical Program/Project links versus 371 derived links; 122 discrepancies.
2,628 projects have no Program derived from available SKU links. This is a finding
about the exported snapshot, not proof that these projects lack a Program in the
live source. Do not remove these projects or automatically replace historical links.

There were no duplicate/orphan identity errors in the checked normalized snapshot.
That does not establish full data quality: fields and history omitted by the
normalization, permanent source SKU IDs, execution statuses and current SharePoint
edits still require reconciliation. Candidate execution statuses intentionally
remain unset rather than copying the SKU master status.

The manifest always reports `production_ready: false`. No deploy/apply command
exists in this preparation tool. Output directories must be new, preserving prior
review results and fingerprints. Artifacts contain company data; retain locally.

## Run

Use the bundled Codex Python runtime, from the workspace root:

```powershell
$py = 'C:/Users/40734/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py -m unittest discover -s '10-AutoPM Microsoft/tests' -v
& $py '10-AutoPM Microsoft/tools/prepare_migration.py' --source 'outputs/program-mvp/normalized-data.json' --output '10-AutoPM Microsoft/artifacts/new-review'
& $py '10-AutoPM Microsoft/tools/preview_weekly.py' --source '<weekly-report.xlsx>' --output '10-AutoPM Microsoft/artifacts/weekly-preview.json'
```

Legacy regression suite: run `python -m unittest test_bridge -v` from
`07-脚本与数据治理 Scripts & data ops/sync_bridge`, using the bundled runtime.
All 12 existing tests passed on 2026-09-10; this is an offline regression result,
not Dataverse integration or Azure deployment evidence.

Two real workbook parser smoke checks also completed:

| Source workbook | Project blocks | Issue rows | Duplicate Project IDs | Unmapped fields / warnings |
| --- | ---: | ---: | --- | --- |
| Ninja XPT Projects Weekly Report-20260807.xlsx | 190 | 145 | NXA0244, NXA0243, NXA0235, NXA0194, NXA0224 (each twice) | 1 / 1 |
| APAC Shark XPT Project Weekly Report V2 (3).xlsx | 197 | 61 | None | 0 / 0 |

These are parsed source blocks, not unique migrated projects or verified Issue
records. Duplicate handling and target mapping must occur before writes. Output
JSON files in `artifacts` retain the parser's source cells and warnings for review.

## Remaining work and next boundary

1. Resolve 122 relationship discrepancies using permanent Airtable IDs and
   ProjectSKU source records; keep current SharePoint edits in the reconciliation.
2. Complete individual automation/template/field parity inventory (not just the
   twelve feature headings), then add repeatable source/target contract tests.
3. Build and deploy Dataverse tables, server rules, Custom APIs, roles and Solution
   in the company-approved development environment after access is available.
4. Adapt Bridge writes/Tracker source reads to Dataverse; deploy file processing,
   import jobs and Canvas screens. No Azure Functions runtime is deployed yet.
5. Implement and validate remaining task, issue, reminder, reporting and AI flows.
6. Validate real multi-user operations and cutover/recovery before stopping old
   writes. Do not claim the whole plan is done based on these preparation tests.

IT input needed: approved environment name/URL, Dataverse customization/Solution
and plug-in deployment privileges, approved service identity/API access, runtime
hosting and licensing. Credentials must not be pasted into this README or chat.
