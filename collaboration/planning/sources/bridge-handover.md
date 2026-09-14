# AutoPM Data Bridge — maintenance handover

**Handover date:** 2026-09-07  
**Production version:** **AutoPM Bridge v5.1**  
**Scope:** Weekly Report → Airtable → All Tracker

## 1. What this tool does

AutoPM Data Bridge replaces the manual weekly-report conversion path. Its intended data flow is:

```text
Weekly Report (Shark / Ninja)
        ↓  reviewable import plan
Airtable Projects + Tasks + Issues + People + Factories
        ↓  reviewable export plan
New All Tracker copy
```

The tool is deliberately conservative. It uses a normalized **Project ID** as the only cross-system key. If a Project ID is missing, duplicated, or does not match exactly once, it skips the record rather than guessing.

It has two operating modes:

1. **Weekly Report → Airtable**: reads a weekly report, creates a preview, then writes only after the user reviews and confirms it.
2. **Airtable → All Tracker**: reads Airtable and creates a **new** All Tracker workbook. It never overwrites the input workbook.

## 2. The one production entry point

Use only the following executable for normal business operation:

| Purpose | Canonical file |
|---|---|
| Production application | [AutoPM_Bridge_v5.1.exe](交付工具/AutoPM_Bridge_v5.1.exe) |
| Required configuration, kept beside the executable | [sync_config.json](交付工具/sync_config.json) |
| Operator instructions | [README.txt](交付工具/README.txt) |
| Run-by-run output | [Run Logs](交付工具/Run Logs) |

`AutoPM_Bridge.exe` and `AutoPM_Bridge_v2.exe` through `AutoPM_Bridge_v5.exe` are historical builds. **Do not use them for production.** v5.1 includes the Excel-style fix needed to preserve namespace prefixes and to add the temporary green fill reliably.

## 3. Source code and engineering materials

All maintenance source is under this folder:

`D:\个人资料\AI学习圈\SN Auto PM\07-脚本与数据治理 Scripts & data ops\sync_bridge`

| File / folder | Role | Maintain? |
|---|---|---|
| [app.py](app.py) | English desktop UI; file selection, preview/apply workflow, progress bar, blocker display | Yes |
| [bridge.py](bridge.py) | Core engine: Excel parsing, field mapping, Airtable API, Task/Issue creation, All Tracker export, validation and green formatting | Yes — highest risk |
| [report.py](report.py) | HTML preview report generator | Yes |
| [test_bridge.py](test_bridge.py) | Automated regression tests for parsing, mappings, export and Excel style handling | Run before every release |
| [validate_release.py](validate_release.py) | Release-level validation against source examples and a clean All Tracker copy | Run before every release |
| [validate_styles_fix.py](validate_styles_fix.py) | Regression validation for the v5.1 Excel green-fill/style fix | Run when export formatting changes |
| [AutoPM_Bridge.spec](AutoPM_Bridge.spec) | Packaging definition used to build the executable | Use when rebuilding the EXE |
| [add_project_sync_fields.py](add_project_sync_fields.py) | Adds the required Project fields if missing | Schema-changing: run only after approval |
| [audit_inputs.py](audit_inputs.py), [run_audit.py](run_audit.py) | Input/schema diagnostics | Safe read-only diagnostics |
| [inspect_corruption.py](inspect_corruption.py), [recover_tracker.py](recover_tracker.py), [repair_tracker_excel.ps1](repair_tracker_excel.ps1) | Investigation tools for damaged All Tracker files | Diagnostic/recovery only; do not treat as normal workflow |
| [evidence](evidence) | Prior release evidence, live snapshots, test outputs and corruption investigation | Retain as evidence |
| [build](build), [dist](dist) | Packaging artifacts | Rebuildable; not the source of truth |

## 4. Business rules implemented in v5.1

### Matching and ownership

- **Primary key:** `Weekly Report Project Number` → `Airtable Project ID (Manual)` → `All Tracker Project Number`.
- **People:** resolve within the expected department first, then use exact name or a single unambiguous abbreviation. Ambiguous names are skipped and reported.
- **Factory:** resolve to a unique Factory record using its known name/code/legacy alias. The UI shows the actual Factory name, not Airtable record IDs.
- **Freshness guard:** if Airtable is newer than the weekly-report update date, the Project is not overwritten by an older report.

### Weekly Report → Airtable

- Project attributes update the existing Project only when their fields are valid and mapped.
- Dated red-section items create or update **Tasks**. Only approved fixed values populate `Milestone (Manual)`; unmatched dated headers become ordinary Tasks with no milestone label.
- Award and MP Start use Start Date = Due Date; other dated Tasks use Due Date = Start Date + 7 days.
- Green date cells represent completed work. A date that has simply passed does **not** prove completion.
- Weekly Issues and Actions are handled in the **Issues** table, not as free text in Projects.
- `Current Progress (Manual)` and `Update This Week (Manual)` retain the current weekly text only, with `Weekly Report Update Date (System)` identifying the version.
- SKU input is normalized and written only to `Project SKU (Manual)`; PMO SKU linkage is maintained by a separate process.

### Airtable → All Tracker

- Writes to a new workbook copy only.
- Never overwrites Excel formula cells, original baseline dates, or unsupported ambiguous text.
- Factory maps to `Manufacturing Factory`; the legacy `Development Factory` header is supported.
- Exported changed cells are given a temporary green fill so the recipient can identify this run's updates.
- Project ID must be an exact 1:1 match. Non-matching records are skipped and included in the report.

## 5. Required Airtable schema

The following fields must exist with the stated type. If they are renamed, removed, or their type changes, the UI will show **Required Setup** and disable import.

| Table | Field | Required type |
|---|---|---|
| Projects | Kick Off Date (Manual) | Date |
| Projects | DQTP Finish Date (Manual) | Date |
| Projects | MP AW Date (Manual) | Date |
| Projects | Compliance Complete Date (Manual) | Date |
| Projects | Update This Week (Manual) | Long text |
| Projects | Weekly Report Update Date (System) | Date |
| Projects | Current Progress (Manual) | Long text |
| Projects | Tooling (Manual) | Single line text |

The Bridge also relies on the live Projects, Tasks, Issues, People and Factories tables. It reads their schema at run time, so field IDs — not display names — are used internally for stable writes.

## 6. Configuration and access control

### Configuration file

The executable reads `交付工具\sync_config.json`. It contains:

- Airtable Base, Projects, Tasks and Issues table settings.
- Airtable credential settings.
- All Tracker filename/sheet aliases and search locations.
- Optional aliases for source headings and target headers.

**Important:** the current configuration includes an Airtable credential. Do not send it by email, Teams, public links, or source control.

Before handing the tool to a new maintainer:

1. Create a new, scoped Airtable PAT for the new owner; do not pass along the existing PAT.
2. Give the PAT only the necessary Base access and read/write scopes.
3. Put the new credential in that maintainer's local `sync_config.json`.
4. Revoke the former credential after the new setup passes a preview test.

## 7. Normal operating procedure

### Weekly Report → Airtable

1. Copy the newest Shark or Ninja weekly workbook into the agreed source folder.
2. Open `AutoPM_Bridge_v5.1.exe`.
3. Select `Weekly Report → Airtable`, the local `sync_config.json`, and the weekly workbook.
4. Select **Generate Preview**.
5. Review all three areas: Proposed Changes, Required Setup, and Skipped / Notes.
6. Do not apply if Required Setup is non-zero, if the wrong source date is detected, or if any unexpected Project is present.
7. Select **Import to Airtable** only after review.
8. Retain the generated Run Logs folder for audit.

### Airtable → All Tracker

1. Obtain a clean, current All Tracker source workbook from SharePoint/OneDrive.
2. Select `Airtable → All Tracker` and choose that source workbook.
3. Generate and review the preview.
4. Select **Create All Tracker Copy** and choose a new output filename.
5. Open the output in Excel and confirm the workbook opens without repair, the expected cells are green, and the source workbook is unchanged.

## 8. Logs, evidence and input locations

| Material | Current location | Notes |
|---|---|---|
| Latest user-run previews and write journals | [Run Logs](交付工具/Run Logs) | Each run contains `preview.json`, `snapshot.json`, `preview_report.html`; an applied run also contains `result.json` and `write_journal.json` |
| Release evidence | [evidence](evidence) | Includes style-fix, release-validation and tracker-integrity evidence |
| Current weekly-report working folder | `D:\个人资料\AI学习圈\SN Auto PM\05-真实项目数据 Real data\Weekly report` | Contains input weekly reports, clean source candidates and generated output copies |
| Older weekly reports / tracker files | `D:\个人资料\AI学习圈\SN Auto PM\05-真实项目数据 Real data\Archive` | Historical reference only |
| Original functional requirements | [AutoPM_Sync_Requirements_Draft_v2.md](AutoPM_Sync_Requirements_Draft_v2.md) | Product/design reference; not the final runtime truth |
| Historical mapping audit | [AutoPM_End_to_End_Field_Mapping_2026-09-05.md](AutoPM_End_to_End_Field_Mapping_2026-09-05.md) | Historical investigation; see warning below |
| Historical release/audit conclusion | [AutoPM_Sync_Audit_and_Usage_2026-09-05.md](AutoPM_Sync_Audit_and_Usage_2026-09-05.md) | Useful evidence and safety rationale |

## 9. Important known constraints and maintenance backlog

1. **Do not use the damaged legacy All Tracker workbook.** The 162 MB file `All Projects Tracker to Sunny Sun 2026 08 13.xlsx` was found to have Excel XML/CRC damage. Obtain a clean current source from SharePoint/OneDrive instead of attempting production repair.
2. **Unknown milestone headings require review.** The Bridge will safely import a dated item as a normal Task where possible, but will not invent a new milestone option. Add a mapping only after the PMO confirms it belongs to the fixed milestone list.
3. **People and Factory completeness remains dependent on Airtable master data.** The tool does not guess when a name/abbreviation is ambiguous. Maintain an approved alias list in configuration or clean the People/Factories master data.
4. **Structured Issues require a stable identity rule.** The Bridge matches an Issue within a Project using normalized issue text. If the business wants robust history across wording changes, define and add an explicit Issue ID / deduplication key.
5. **Historical documents may conflict with current code.** The v5.1 source code and `交付工具\README.txt` are the current operating authority. `AutoPM_End_to_End_Field_Mapping_2026-09-05.md` is earlier audit material and contains older assumptions that no longer fully reflect v5.1, including some Issue and weekly-text handling.
6. **All Tracker mapping must be revalidated when its template changes.** New columns, renamed headers, formula changes or new sheet layouts require a preview and release validation before production use.

## 10. Release and change-control checklist for the new maintainer

Before changing code, mapping, configuration, or Excel formatting:

1. Create a versioned copy of the current production executable and configuration.
2. Make the change in source, not by patching the EXE.
3. Run `python -m unittest test_bridge.py` — current baseline: **12 tests passed** on 2026-09-07.
4. Run `validate_release.py` against at least one Shark report, one Ninja report and a clean All Tracker sample.
5. Check that a preview is generated; no unexpected Project IDs, schema blockers or unmapped required fields may exist.
6. For Airtable writes, apply only a small reviewed sample first, then inspect `write_journal.json` and live records.
7. For All Tracker exports, open the generated workbook in Excel, verify no repair dialog appears, and verify temporary green fills on changed cells.
8. Rebuild the EXE with `AutoPM_Bridge.spec`, publish it with an explicit version suffix, and update `交付工具\README.txt`.
9. Keep the prior EXE for rollback, but do not overwrite it.

## 11. Handover acceptance checklist

The new maintainer has accepted the work only when they can independently:

- [ ] Start `AutoPM_Bridge_v5.1.exe` with a locally configured PAT.
- [ ] Generate a preview from a current weekly report without changing Airtable.
- [ ] Explain every item in Required Setup and Skipped / Notes.
- [ ] Apply a reviewed small test import and locate its Run Logs folder.
- [ ] Generate a new All Tracker copy from Airtable.
- [ ] Verify the exported workbook opens cleanly and the green-fill marker is visible.
- [ ] Run the automated regression tests.
- [ ] Rotate the credential so the former maintainer no longer has write access.

## 12. Decision authority

The maintainer owns technical operation, diagnostics, configuration updates, release testing and safe rollback.

PMO / business ownership must approve: new milestone definitions, field-semantic changes, status mapping changes, issue de-duplication policy, new automatic writes, and changes that alter the All Tracker business template.
