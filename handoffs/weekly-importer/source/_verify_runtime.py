"""
Runtime simulation check for all modified files.
Tests: syntax, importability, critical function existence,
       None-input robustness on key paths.
"""

import sys
import traceback
import py_compile
from pathlib import Path
import os

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

FILES = [
    "autopm/sync.py",
    "autopm/normalize.py",
    "autopm/tracker.py",
    "autopm/ui.py",
    "autopm/deepseek.py",
    "autopm/schema_memory.py",
    "autopm/workbook.py",
    "autopm/weekly_remark.py",
]

results = {}

# 1. Syntax check
for rel in FILES:
    path = ROOT / rel
    try:
        py_compile.compile(str(path), doraise=True)
        results[rel] = {"syntax": "OK"}
    except Exception as e:
        results[rel] = {"syntax": f"FAIL: {e}"}

# 2. Import check (with isolation to avoid side effects)
for rel in FILES:
    mod_name = rel.replace("/", ".").replace("\\", ".").replace(".py", "")
    try:
        # force reimport if cached
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        __import__(mod_name)
        results[rel]["import"] = "OK"
    except Exception as e:
        tb = traceback.format_exc()
        results[rel]["import"] = f"FAIL: {e}\n{tb}"

# 3. Specific function robustness tests
print("=== AutoPM Runtime Verification ===\n")

# 3a. normalize_task_title with None / regional suffixes
from autopm.normalize import normalize_task_title

for inp, expected in [
    ("EB1 (CN)", "eb1"),
    ("P1 CAD DROP (VN)", "p1caddrop"),
    ("", ""),
    ("Normal Title", "normaltitle"),
]:
    out = normalize_task_title(inp)
    ok = out == expected
    results["autopm/normalize.py"][f"normalize_task_title({inp!r})"] = (
        f"{'OK' if ok else 'FAIL'}: got {out!r}, expected {expected!r}"
    )

# 3b. _extract_narrative_date simulation
# Exercise the production helper instead of maintaining a stale local copy.
from autopm.sync import _extract_narrative_date


for inp, ctx, has_result in [
    ("Next PLM by Oct 15", "2026-09-16", True),
    ("Ship by Dec 1st", "2026-09-16", True),
    ("Nothing here", "2026-09-16", False),
    ("", "2026-09-16", False),
    ("N/A", "2026-09-16", False),
]:
    out = _extract_narrative_date(inp, ctx)
    ok = (out is not None) == has_result
    results["autopm/sync.py"][f"_extract_narrative_date({inp!r})"] = (
        f"{'OK' if ok else 'FAIL'}: got {out!r}"
    )

# 3c. weekly_remark merge robustness: None version_field path
from autopm.weekly_remark import merge_weekly_remark

# This should NOT raise when text is empty but blocks are present
try:
    # Simulate calling merge_weekly_remark with empty text
    result = merge_weekly_remark("", "2026-09-16", {"current_progress": "test"})
    results["autopm/weekly_remark.py"]["merge_weekly_remark(empty_text)"] = (
        f"OK: returned {type(result).__name__}"
    )
except Exception as e:
    results["autopm/weekly_remark.py"]["merge_weekly_remark(empty_text)"] = f"FAIL: {e}"

# 3d. Check sync.py key globals exist after import
from autopm import sync

for name in ["PROJECT_FIELDS", "TASK_FIELDS", "ISSUE_FIELDS", "WRITABLE"]:
    ok = hasattr(sync, name)
    results["autopm/sync.py"][f"hasattr({name})"] = "OK" if ok else "FAIL: missing"

# 3e. Verify TASK_FIELDS contains required keys
for key in ["latest_update", "completed_by"]:
    ok = key in sync.TASK_FIELDS
    results["autopm/sync.py"][f"TASK_FIELDS[{key!r}]"] = (
        f"{'OK' if ok else 'FAIL'}: value={sync.TASK_FIELDS.get(key, 'MISSING')!r}"
    )

# 3f. Verify _milestone_target handles None aliases gracefully
try:
    out = sync._milestone_target("EB1 (CN)", {})
    results["autopm/sync.py"]["_milestone_target(EB1 (CN), {})"] = f"OK: {out!r}"
except Exception as e:
    results["autopm/sync.py"]["_milestone_target(EB1 (CN), {})"] = f"FAIL: {e}"

# 4. Print summary
failures = []
for rel, checks in results.items():
    print(f"--- {rel} ---")
    for check, status in checks.items():
        marker = (
            "[PASS]"
            if status.startswith("OK")
            else "[WARN/INFO]"
            if "FAIL" not in status
            else "[FAIL]"
        )
        print(f"  {marker} {check}: {status}")
        if "FAIL" in status:
            failures.append((rel, check, status))
    print()

if failures:
    print(f"!!! {len(failures)} FAILURE(S) FOUND !!!")
    for rel, check, status in failures:
        print(f"  {rel} -> {check}: {status}")
    sys.exit(1)
else:
    print("All checks passed.")
    sys.exit(0)
