"""Weekly progress tracking with delta-only updates in Engineering remark.

Existing notes and history are preserved verbatim. Only changed progress text
is appended; an empty dated block advances the version without repeating text.

New plain-text format (no headers, no end markers, no AUTOPM wrappers):
  --- 2026-09-14 ---
  1. MP AW just released...
  2. ...
  --- 2026-09-15 ---
  1. New content

Legacy format (read-only backward compatibility):
  [[AUTOPM_WEEKLY_REPORT:v1]]
  周报日期: 2026-09-14
  工程进展:
  ...
  [[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]
  [[/AUTOPM_WEEKLY_REPORT]]
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date
import re


MAX_REMARK_LENGTH = 100_000

# ------------------------------------------------------------------
# Legacy marker constants (read-only, for backward compatibility)
# ------------------------------------------------------------------
_LEGACY_RESERVED = "AUTOPM_WEEKLY"
_LEGACY_RESERVED_PATTERN = re.compile(r"AUTOPM\\?_WEEKLY")
_LEGACY_START = "[[AUTOPM_WEEKLY_REPORT:v1]]"
_LEGACY_END = "[[/AUTOPM_WEEKLY_REPORT]]"
_LEGACY_SECTIONS = {
    "current_progress": ("工程进展:", "[[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]"),
    "update_this_week": ("本周更新:", "[[AUTOPM_WEEKLY_REPORT:END_UPDATE]]"),
    "jira_total": ("Jira Total:", "[[AUTOPM_WEEKLY_REPORT:END_JIRA_TOTAL]]"),
    "jira_open": ("Jira Open:", "[[AUTOPM_WEEKLY_REPORT:END_JIRA_OPEN]]"),
    "jira_verify": ("Jira Verify:", "[[AUTOPM_WEEKLY_REPORT:END_JIRA_VERIFY]]"),
    "jira_ready_to_close": ("Jira Ready to close:", "[[AUTOPM_WEEKLY_REPORT:END_JIRA_READY]]"),
    "jira_closed": ("Jira Closed:", "[[AUTOPM_WEEKLY_REPORT:END_JIRA_CLOSED]]"),
}
JIRA_COUNT_FIELDS = frozenset(k for k in _LEGACY_SECTIONS if k.startswith("jira_"))
_LEGACY_MARKERS = frozenset(
    (_LEGACY_START, _LEGACY_END, *(footer for _, footer in _LEGACY_SECTIONS.values()))
)
_LEGACY_DATE_LABEL = "周报日期: "

# ------------------------------------------------------------------
# New plain-text format (write path)
# ------------------------------------------------------------------
_DATE_RE = re.compile(r"^---\s+(\d{4}-\d{2}-\d{2})\s+---$")
REMARK_FIELDS = frozenset({"current_progress"})


def _marker_line(value):
    canonical = value.replace(r"\_", "_")
    return canonical if canonical in _LEGACY_MARKERS else value


def remark_comparison_value(value):
    """Compare rich-text storage framing without altering the stored prose.

    Airtable escapes marker underscores and appends a newline to the closing
    report marker. Only those exact marker lines and LF/CRLF are equivalent;
    changed dates, report text, history and manual notes remain different.
    """
    text = _text(value, allow_none=True)
    lines = [_marker_line(line) for line in text.replace("\r\n", "\n").split("\n")]
    starts = [i for i, line in enumerate(lines) if line == _LEGACY_START]
    report_legacy = len(lines) >= 2 and lines[-2] == _LEGACY_END
    fenced_legacy = (
        len(lines) >= 3
        and lines[-3] == _LEGACY_END
        and re.fullmatch(r"`{3,}", lines[-2]) is not None
        and starts
        and starts[-1] > 0
        and lines[starts[-1] - 1] == lines[-2]
    )
    if lines[-1] == "" and (report_legacy or fenced_legacy):
        lines.pop()
    elif lines[-1] == '' and any(_DATE_RE.fullmatch(line) for line in lines):
        lines.pop()  # Airtable rich text can add one terminal LF.
    # Airtable restarts Markdown ordered lists at 1. Compare marker formatting,
    # never numbers inside item text, escaped literal numbers, or fenced code.
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token, rest = marker.groups()
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not rest.strip():
                fence = None
        elif fence is None:
            lines[index] = re.sub(r"^( {0,3})[0-9]{1,9}\.([ \t]+)", r"\g<1>1.\2", line)
    return "\n".join(lines)


def uses_weekly_remark(config) -> bool:
    """Use an explicit base profile before the legacy, scope-guarded setting.

    An exact profile can opt a base in or out. Missing profiles retain legacy
    behavior; malformed profiles never enable remark storage by fallback.
    """
    if not isinstance(config, Mapping):
        raise ValueError("周报存储配置必须是字典。")
    if "project_report_storage_by_base" in config:
        profiles = config["project_report_storage_by_base"]
        if not isinstance(profiles, Mapping):
            return False
        base = config.get("base_id")
        if base is not None and not isinstance(base, str):
            return False
        if base and base in profiles:
            return profiles[base] == "engineering_remark"
    scope = config.get("project_report_storage_base_id")
    return config.get("project_report_storage") == "engineering_remark" and (
        not scope or scope == config.get("base_id")
    )


def _text(value, *, allow_none=False) -> str:
    if value is None and allow_none:
        return ""
    if not isinstance(value, str):
        raise ValueError("Engineering remark 和周报文本必须是字符串。")
    try:
        too_long = (
            len(value) > MAX_REMARK_LENGTH
            or len(value.encode("utf-16-le")) // 2 > MAX_REMARK_LENGTH
        )
    except UnicodeEncodeError as exc:
        raise ValueError("周报文本含有无效 Unicode 字符。") from exc
    if too_long:
        raise ValueError("Engineering remark 超过 100000 字符，不能安全保存周报。")
    return value


def _report_date(value) -> str:
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value
    ):
        raise ValueError("周报日期必须是有效的 YYYY-MM-DD 日期。")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("周报日期必须是有效的 YYYY-MM-DD 日期。") from exc
    return value


def _line(text, cursor):
    """Read a metadata line while accepting both LF and CRLF framing."""
    end = text.find("\n", cursor)
    if end < 0:
        return text[cursor:], len(text), ""
    if end > cursor and text[end - 1] == "\r":
        return text[cursor : end - 1], end + 1, "\r\n"
    return text[cursor:end], end + 1, "\n"


def _broken():
    return ValueError("Engineering remark 中的 AutoPM 周报标记损坏，请先修复原备注。")


def _read_legacy_blocks(text):
    """Read legacy AUTOPM_WEEKLY_REPORT delimited blocks from text."""
    blocks = []
    cursor = 0
    while True:
        match = _LEGACY_RESERVED_PATTERN.search(text, cursor)
        if match is None:
            break
        token = match.start()
        start = token - 2  # The only valid top-level token starts with [[.
        if start < cursor or (start and text[start - 1] != "\n"):
            raise _broken()
        header, pos, framing = _line(text, start)
        if _marker_line(header) != _LEGACY_START or not framing:
            raise _broken()
        date_line, pos, newline = _line(text, pos)
        if not date_line.startswith(_LEGACY_DATE_LABEL) or not newline:
            raise _broken()
        block = {
            "report_date": _report_date(date_line[len(_LEGACY_DATE_LABEL) :]),
            "fields": {},
        }
        previous_section = -1
        while True:
            label, next_pos, newline = _line(text, pos)
            if _marker_line(label) == _LEGACY_END:
                cursor = next_pos
                break
            keys = list(_LEGACY_SECTIONS)
            key = next(
                (k for k, (heading, _) in _LEGACY_SECTIONS.items() if label == heading),
                None,
            )
            if key is None or not newline or keys.index(key) <= previous_section:
                raise _broken()
            previous_section = keys.index(key)
            footer = _LEGACY_SECTIONS[key][1]
            match = _LEGACY_RESERVED_PATTERN.search(text, next_pos)
            token = match.start() if match is not None else -1
            footer_start = token - 2
            if token < 0 or footer_start < next_pos:
                raise _broken()
            footer_line, after_footer, footer_newline = _line(text, footer_start)
            content = text[next_pos:footer_start]
            if (
                _marker_line(footer_line) != footer
                or not footer_newline
                or not content.endswith(framing)
            ):
                raise _broken()
            content = content[: -len(framing)]
            if content.strip():
                block["fields"][key] = content
            pos = after_footer
        blocks.append(block)
    return blocks


def _read_new_blocks(text):
    """Read new plain-text format blocks: --- YYYY-MM-DD --- ... (content lines) ..."""
    blocks = []
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        match = _DATE_RE.match(lines[i])
        if not match:
            i += 1
            continue
        report_date = match.group(1)
        i += 1
        content_lines = []
        while i < len(lines) and not _DATE_RE.match(lines[i]):
            content_lines.append(lines[i])
            i += 1
        content = "\n".join(content_lines).rstrip("\n")
        blocks.append({"report_date": _report_date(report_date),
                       "fields": {"current_progress": content} if content else {}})
    return blocks


def _blocks(text):
    """Read all weekly report blocks from text, supporting both legacy and new formats."""
    legacy_blocks = _read_legacy_blocks(text)
    new_blocks = _read_new_blocks(text)
    return legacy_blocks + new_blocks


def _latest(blocks):
    if not blocks:
        return {"report_date": None, "fields": {}}
    fields = {}
    ordered = sorted(blocks, key=lambda block: block["report_date"])
    for block in ordered:
        fields.update(block["fields"])
    return {"report_date": ordered[-1]["report_date"], "fields": fields}


def read_weekly_remark(value) -> dict:
    """Read the newest report; reject damaged blocks rather than losing its date.

    None and ordinary undelimited notes have no known report date or fields.
    Historical blocks are ordered by date, with the last block winning ties.
    """
    return _latest(_blocks(_text(value, allow_none=True)))


def merge_weekly_remark(existing, report_date, fields, *, rich_text=False) -> str:
    """Append a report snapshot, preserving notes and historical revisions.

    Empty or absent weekly values inherit existing values. Other project keys
    are ignored. Repeating the latest content for a date does not append a block;
    returning to an earlier same-day value after a revision creates a revision.

    New format: writes clean plain text without section headers, end markers,
    AUTOPM wrappers, or markdown code fences.
    Legacy blocks in existing text are preserved but new blocks use the new format.
    The rich_text parameter is accepted for API compatibility but ignored.
    """
    text = _text(existing, allow_none=True)
    report_date = _report_date(report_date)
    if not isinstance(fields, Mapping):
        raise ValueError("周报字段必须是字典。")
    blocks = _blocks(text)
    combined = dict(_latest(blocks)["fields"])
    for key in REMARK_FIELDS:
        if key not in fields or fields[key] is None:
            continue
        value = _text(fields[key])
        if _LEGACY_RESERVED_PATTERN.search(value):
            raise ValueError("周报内容包含保留的 AutoPM 周报标记，不能安全保存。")
        if any(_DATE_RE.fullmatch(line) for line in value.splitlines()):
            raise ValueError("进展正文包含周报日期分隔行，请勿把整段历史作为本周进展再次导入。")
        if value.strip():
            combined[key] = value
    # Delta-only: skip if current_progress is unchanged from latest stored value
    latest = _latest(blocks)
    if latest["report_date"] and report_date < latest["report_date"]:
        raise ValueError("来源周报早于已存版本，不能追加旧报告。")
    def comparable(value):
        if rich_text and isinstance(value, str):
            return remark_comparison_value(value)
        return value.replace("\r\n", "\n").rstrip("\n") if isinstance(value, str) else value
    if comparable(latest["fields"].get("current_progress")) == comparable(combined.get("current_progress")):
        if latest['report_date'] == report_date:
            return text
        # Advance the version even when only status/tasks/issues changed.
        # An empty dated block inherits progress without duplicating its prose.
        block = f"--- {report_date} ---"
    else:
        block = f"--- {report_date} ---\n{combined['current_progress']}"
    return _text(text + ("\n\n" if text else "") + block)
