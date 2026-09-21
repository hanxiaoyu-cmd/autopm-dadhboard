"""Describe the bundled local source files without network or credential access."""
from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE_DIRECTORY = "All Projects Tracker SUNNY (1)"

# Verified from the workbooks' per-project Update / Update on cells on 2026-09-07.
# File names and filesystem timestamps are deliberately not used as report dates.
KNOWN_REPORT_DATES = {
    "bcc78f6af67246c94f7d097bfd5bf85228e264adfbef4192508e68f6096aae07":
        "内容最新：2026-09-03（各项目 2026-07-17 至 2026-09-03）",
    "797fdb737f593e46eed3b03461bb34b6ad7a54e449d01bea3ff79e25bdbf8685":
        "内容最新：2026-09-04（各项目 2026-06-25 至 2026-09-04）",
}

_FILES = (
    ("APAC Shark XPT Project Weekly Report V2 (1).xlsx", "Shark 周报", "weekly",
     "可选择为 AI 解析输入；每个项目保留自己的更新日期。"),
    ("Ninja XPT Projects Weekly Report-20260518 (3).xlsx", "Ninja 周报", "weekly",
     "可选择为 AI 解析输入；文件名中的日期不代表内容更新时间。"),
    ("All Projects Tracker SUNNY (1).xlsx", "原总项目表", "tracker",
     "原有项目汇总与字段参考；程序直接更新 Airtable，不改写这份 Excel。"),
    ("weekly report rule.pptx", "周报规则说明", "rules",
     "说明周报各区域及其与 Projects、Tasks、Issues 的对应关系。"),
    ("AutoPM_Bridge_v5.exe", "旧版同步程序", "legacy",
     "原资料附带的旧程序；日常请使用 dist/AutoPM_AI_latest.exe。"),
)


def workspace_root(executable_root) -> Path:
    """Resolve a source ROOT or the usual workspace/dist executable ROOT.

    A source folder that itself contains the original materials takes precedence,
    including when that source folder happens to be named ``dist``.
    """
    root = Path(executable_root).expanduser().resolve()
    if (root / SOURCE_DIRECTORY).is_dir():
        return root
    return root.parent if root.name.casefold() == "dist" else root


def _size_text(size: int) -> str:
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} B"


def _report_date(path: Path) -> str:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return KNOWN_REPORT_DATES.get(digest.hexdigest(), "日期待检查")
    except OSError:
        return "日期待检查"


def scan_local_files(workspace) -> list[dict[str, str]]:
    """List only existing, explicitly named materials in the source directory.

    This never recursively searches other folders or reads connection settings,
    API keys, or executable contents. It does not interpret document text. Only
    weekly workbooks are streamed to calculate their content hashes; no timestamp
    is treated as a date.
    """
    source = Path(workspace).expanduser().resolve() / SOURCE_DIRECTORY
    result = []
    for filename, label, kind, description in _FILES:
        path = source / filename
        try:
            if not path.is_file():
                continue
            size = path.stat().st_size
        except OSError:
            continue
        if kind == "weekly":
            date_label = _report_date(path)
        elif kind == "tracker":
            date_label = "导出日期未确认（项目日期不代表文件导出时间）"
        else:
            date_label = ""
        result.append({
            "path": str(path), "label": label, "filename": filename,
            "kind": kind, "description": description, "date_label": date_label,
            "size_text": _size_text(size),
        })
    return result
