"""Command line read/preview entry points. Remote writes are available in the UI."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import uuid

from .config import ROOT, load_settings, import_legacy, redact
from .preview import enrich_display, save_preview
from .workbook import parse_local, read_workbook


def main():
    parser = argparse.ArgumentParser(description="AutoPM 周报离线检查 / AI 同步预览")
    parser.add_argument("mode", choices=("inspect", "preview", "local-preview"))
    parser.add_argument("file")
    parser.add_argument("--report-date", help="YYYY-MM-DD，仅补充缺失项目日期")
    parser.add_argument("--date-order", choices=("AUTO", "MDY", "DMY"), help="文本日期顺序；AUTO 拒绝月/日歧义")
    parser.add_argument("--legacy-config", help="读取既有 sync_config.json 的 Airtable 连接")
    parser.add_argument("--output", help="本次预览输出目录")
    args = parser.parse_args()
    config = load_settings()
    if args.legacy_config:
        config.update(import_legacy(args.legacy_config))
    try:
        evidence = read_workbook(args.file, report_date=args.report_date, date_order=args.date_order or config.get("date_order", "AUTO"))
        if args.mode == "inspect":
            report, plan = parse_local(evidence), None
        else:
            from .airtable import AirtableClient
            from .deepseek import DeepSeekClient
            from .workflow import prepare_preview
            from .schema_memory import SchemaMemoryStore
            if args.mode == "preview" and not config.get("deepseek_api_key"):
                raise ValueError("请在桌面程序保存 DeepSeek API Key 或设置 DEEPSEEK_API_KEY 环境变量。")
            report = (DeepSeekClient(config["deepseek_api_key"], base_url=config["deepseek_base_url"], model=config["deepseek_model"], cache_dir=ROOT / ".local" / "model-cache").parse(evidence, progress=print)
                      if args.mode == "preview" else parse_local(evidence))
            with AirtableClient(config["airtable_token"], config["base_id"]) as client:
                plan, _ = prepare_preview(client, report, config, SchemaMemoryStore(ROOT / ".local/schema-memory"))
        directory = Path(args.output) if args.output else ROOT / "Run Logs" / (datetime.now().strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6])
        save_preview(report, plan, directory)
        print(json.dumps({"projects": len(report["projects"]), "tasks": sum(len(p.get("tasks", [])) for p in report["projects"]),
                          "issues": sum(len(p.get("issues", [])) for p in report["projects"]), "warnings": len(report.get("warnings", [])),
                          "changes": len((plan or {}).get("changes", [])), "blockers": len((plan or {}).get("blockers", [])),
                          "output": str(directory.resolve())}, ensure_ascii=False, indent=2))
    except Exception as exc:
        parser.exit(1, redact(exc, config) + "\n")


if __name__ == "__main__":
    main()
