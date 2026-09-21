# -*- coding: utf-8 -*-
"""Full-chain read-only simulation for the 'current_progress' KeyError fix.

Simulates the exact worker paths the UI runs:
  1. prepare_preview:  parse weekly xlsx -> reconcile(schema) -> build_plan -> enrich
  2. prepare_airtable_tracker: cloud snapshot -> build_airtable_tracker_plan
Reads Airtable schema + records (read-only). NEVER writes anything to Airtable.
"""

import sys
import json
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from autopm.config import load_settings, ROOT as CFG_ROOT
from autopm.airtable import AirtableClient
from autopm.schema_memory import SchemaMemoryStore
from autopm.workflow import prepare_preview, prepare_airtable_tracker
from autopm.workbook import read_workbook, parse_local

WEEKLY = ROOT / "weekly report data" / "Ninja XPT Projects Weekly Report-20260914.xlsx"
TRACKER = ROOT / "weekly report data" / "All Projects Tracker 0603.xlsx"

results = []


def step(name, ok, extra=""):
    results.append((name, ok, extra))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {extra}")


def main():
    settings = load_settings()
    token = settings.get("airtable_token")
    base_id = settings.get("base_id")
    if not token or not base_id:
        print("NO-CRED: 缺少 airtable_token / base_id，跳过在线链路")
        return 1

    # ---- Path 1: prepare_preview (weekly report -> cloud preview) ----
    if not WEEKLY.exists():
        step("prepare_preview", False, f"周报文件不存在: {WEEKLY}")
    else:
        try:
            evidence = read_workbook(
                str(WEEKLY),
                report_date=None,
                date_order=settings.get("date_order", "AUTO"),
            )
            report = parse_local(evidence)
            report.setdefault("extraction_mode", "local")
            with AirtableClient(token, base_id) as client:
                store = SchemaMemoryStore(CFG_ROOT / ".local/schema-memory")
                plan, effective = prepare_preview(client, report, settings, store)
            blockers = plan.get("blockers") or []
            n_changes = len(plan.get("changes") or [])
            n_warn = len(plan.get("warnings") or [])
            if blockers:
                step("prepare_preview", False, f"blockers={blockers[:3]}")
            else:
                step(
                    "prepare_preview",
                    True,
                    f"changes={n_changes} warnings={n_warn} base={effective.get('base_id')}",
                )
        except Exception as exc:
            step("prepare_preview", False, f"{type(exc).__name__}: {exc}")
            traceback.print_exc()

    # ---- Path 2: prepare_airtable_tracker (local tracker workbook) ----
    if not TRACKER.exists():
        step("prepare_airtable_tracker", False, f"本地总表不存在: {TRACKER}")
    else:
        try:
            from autopm.config import ROOT as R2

            with AirtableClient(token, base_id) as client:
                store = SchemaMemoryStore(R2 / ".local/schema-memory")
                plan = prepare_airtable_tracker(
                    client,
                    str(TRACKER),
                    settings,
                    store,
                    project_ids=None,
                )
            blockers = plan.get("blockers") or []
            n_changes = len(plan.get("changes") or [])
            n_warn = len(plan.get("warnings") or [])
            if blockers:
                step("prepare_airtable_tracker", False, f"blockers={blockers[:3]}")
            else:
                step(
                    "prepare_airtable_tracker",
                    True,
                    f"changes={n_changes} warnings={n_warn}",
                )
        except Exception as exc:
            step("prepare_airtable_tracker", False, f"{type(exc).__name__}: {exc}")
            traceback.print_exc()

    failed = [r for r in results if not r[1]]
    print("\n==== 汇总 ====")
    print(
        f"{'全部通过' if not failed else f'失败 {len(failed)} 项'}: {len(results)} 条链路"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
