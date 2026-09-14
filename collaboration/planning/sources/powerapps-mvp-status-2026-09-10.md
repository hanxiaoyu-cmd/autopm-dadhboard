# AutoPM Power Apps MVP — implementation status

Verified on 2026-09-10 through the company's signed-in browser UI.

## Published application

- App: AutoPM test
- App ID: fff66275-da9f-41f8-8df2-6fd4d7bf543b
- Environment: Default-276bce15-bc90-4de5-8559-6c504d8b6cf8
- Player: https://apps.powerapps.com/play/e/Default-276bce15-bc90-4de5-8559-6c504d8b6cf8/a/fff66275-da9f-41f8-8df2-6fd4d7bf543b?tenantId=276bce15-bc90-4de5-8559-6c504d8b6cf8
- Published player verified to open Screen2 (Program Portfolio), displaying 151 PROGRAMS and 151 matching programs with no filters.
- Screen3 is Program Details. Screen1 and MainScreen1 are older test screens, retained for rollback, not linked from the new user flow.
- Fixed landscape 16:9 layout, proportional scaling enabled. Visual checks performed in the in-app browser; mobile redesign and accessibility remediation are not complete.

## Current data location

Site: https://europro365.sharepoint.com/teams/Autopm

| List | Imported rows | Purpose |
| --- | ---: | --- |
| APM_Programs | 151 | All Programs from source export |
| APM_Projects | 480 | Distinct projects linked to those Programs |
| APM_SKUs | 2128 | Direct Program SKUs plus SKUs linked through those projects |
| APM_ProgramProjects | 481 | Program/project junction |
| APM_ProjectSKUs | 1045 | Project/SKU junction |

All five lists were created via SharePoint CSV import and connected to the app. Program count verified in player; project and SKU subset counts verified through sample Program views. These are all Programs, not all 2997 unfiltered source projects or 9926 unfiltered source SKUs.

Previous AutoPM_Programs, AutoPM_Projects, AutoPM_SKUs, AutoPM_ProgramProjects and AutoPM_ProjectSKUs contain the two-Program pilot only. Original AutoPM_Project contains Test-001. Do not confuse them with current APM_ lists.

## User experience

- English application labels and description. Microsoft shell language remains account-dependent.
- Portfolio: three-column cards; name/code search; brand and category dropdowns; colored Program status labels.
- Details: project/attention/In MP/Program SKU metrics; Projects, Program SKUs and Project SKUs tabs; name/ID/SKU search; project status-group filter.
- Project colors: On Track green, At Risk amber, Delayed red, In MP blue, On Hold purple, Cancelled gray. Labels accompany colors.
- Project edits: ProjectStatus and ProgressSummary. StatusGroup updated in the same save action.
- SKU edits: SKUStatus and Market.
- Program editing and relationship editing are not implemented in the app; current administrative access is through SharePoint lists.
- Saves are disabled without a selected record and show English result notifications.

## Query strategy

- Programs total 151; local/filter operations fit within the current 500-row setting.
- Opening Program: filter APM_ProgramProjects by ProgramKey, then ForAll / LookUp matching project keys into cProgramProjects. Fetch direct SKUs using Filter(APM_SKUs, ProgramKey=vProgram.ProgramKey) into cProgramSKUs.
- Selecting project: filter APM_ProjectSKUs by ProjectKey, then LookUp each SkuKey into cProjectSKUs. Avoid nondelegable global IN against the 2128-row SKU table.
- Status and search filtering operate on the selected Program's collections.
- Largest direct Program SKU count in current source is 212; per-parent collections are below 500. This is not a guarantee for arbitrary future growth.
- Progress percentage and dates remain imported source snapshots; task dependency calculations are not recreated.
- App checker before final publishing showed warnings only: 11 delegation warnings, 9 in old screens and 2 for the new portfolio counters. No formula errors were shown. Full accessibility review not complete.

## Verified tests

- All-program portfolio: 151 records displayed; CrushBoss name search returned one card.
- CrushBoss: 15 projects, 1 Needs attention, 8 In MP, 66 direct Program SKUs.
- Needs attention filter: exactly NXA0303 / LB201UKPKBRN / Delayed.
- NXA0303 project SKU lookup: LB201EUPKBRN and LB201UKPKBRN, two records.
- New SKU save: temporarily wrote MVP-VERIFY to LB201EUPKBRN; directly verified in APM_SKUs via SharePoint; restored original blank and verified again.
- New project save: appended [MVP verification 2026-09-10] to NXA0303 summary; verified SharePoint row retained Delayed and Needs attention and new summary; restored exact original summary and verified no marker remained.
- Earlier pilot tests likewise restored XSXA80925 summary and DB351GY1 status.

## Airtable synchronization — not configured

User asked whether recurring synchronization is possible. Recommended: scheduled Power Automate/API reader -> SharePoint -> Power Apps. Need verify approved API connection, applicable Premium licensing, and Airtable Base read authorization.

CSV-based SKU IDs are deterministic internal UUIDs derived from source snapshot row keys. Before live API sync, align records with actual Airtable record IDs. Never match SKUs or Programs by name alone. Decide field ownership and conflict handling before overwriting user edits; two-way sync requires write authorization and explicit conflict policy. No scheduled flow, credentials, permission expansion, notifications or two-way sync were created.

## Browser execution notes

- Working control: in-app browser ID 1, through mcp__cua_repl. Global cua.getState can fail due external-browser inventory; direct known tab works.
- Power Apps editor tab 2; SharePoint tab 3; published player created and marked deliverable.
- Many calls take about 21 seconds. Two calls can exceed 60 seconds and reset the kernel; prefer single UI operations near navigation changes.
- Power Apps iframe: iframe[name="EmbeddedStudio"]. Player iframe: iframe[name="fullscreen-app-host"].
- UI YAML paste works via cua tab.paste. Control versions: Label@2.5.1, Classic/Button@2.2.0, Classic/TextInput@2.3.2, Classic/DropDown@2.3.1, Gallery@2.15.0 Variant Vertical.
- Do not use locator.fill to replace Monaco formulas: it concatenated content. Use editor press Control+a, then cua tab.paste, then blur.
- Empty fill on regular Power Apps inputs sometimes failed to trigger state updates. Use keyboard Control+a / Backspace on actual populated input; verify persisted blank in SharePoint.
- SharePoint UI list filter can use Title. Displayed custom column names from CSV may differ from internal names; URL FilterField1=ProjectKey failed. Do not infer internal schema names.
