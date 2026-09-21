"""Weekly remark parser and merger with delta-only updates.

Supports two formats:
- New plain-text: --- YYYY-MM-DD ---\ncontent lines
- Legacy: [[AUTOPM_WEEKLY_REPORT:v1]] with delimited blocks
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import date
from typing import Any

MAX_REMARK_LENGTH = 100_000

# Legacy marker constants (read-only backward compatibility)
_LEGACY_RESERVED = "AUTOPM_WEEKLY"
_LEGACY_RESERVED_PATTERN = re.compile(r"AUTOPM\?_WEEKLY")
_LEGACY_START = "[[AUTOPM_WEEKLY_REPORT:v1]]"
_LEGACY_END = "[[/AUTOPM_WEEKLY_REPORT]]"
_LEGACY_SECTIONS = {
    "current_progress": (
        "Engineering Progress:",
        "[[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]",
    ),
}
_LEGACY_MARKERS = frozenset(
    (_LEGACY_START, _LEGACY_END, *(footer for _, footer in _LEGACY_SECTIONS.values()))
)
_LEGACY_DATE_LABEL = "Report Date: "

# New plain-text format
_DATE_RE = re.compile(r"^---\s+(\d{4}-\d{2}-\d{2})\s+---$")
REMARK_FIELDS = frozenset({"current_progress"})


def _text(value: Any, *, allow_none: bool = False) -> str:
    """Validate and normalize text value."""
    if value is None and allow_none:
        return ""
    if not isinstance(value, str):
        raise ValueError("Engineering remark must be a string.")
    try:
        too_long = (
            len(value) > MAX_REMARK_LENGTH
            or len(value.encode("utf-16-le")) // 2 > MAX_REMARK_LENGTH
        )
    except UnicodeEncodeError as exc:
        raise ValueError("Invalid Unicode characters in remark text.") from exc
    if too_long:
        raise ValueError("Engineering remark exceeds 100,000 character limit.")
    return value


def _report_date(value: str) -> str:
    """Validate YYYY-MM-DD date string."""
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value
    ):
        raise ValueError("Report date must be valid YYYY-MM-DD.")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Report date must be valid YYYY-MM-DD.") from exc
    return value


def _marker_line(value: str) -> str:
    """Normalize marker line for comparison."""
    canonical = value.replace(r"\_", "_")
    return canonical if canonical in _LEGACY_MARKERS else value


def _line(text: str, cursor: int) -> tuple[str, int, str]:
    """Read a line handling both LF and CRLF."""
    end = text.find("\n", cursor)
    if end < 0:
        return text[cursor:], len(text), ""
    if end > cursor and text[end - 1] == "\r":
        return text[cursor : end - 1], end + 1, "\r\n"
    return text[cursor:end], end + 1, "\n"


def _broken() -> ValueError:
    return ValueError(
        "Damaged weekly report markers detected. Please fix the remark first."
    )


def _read_legacy_blocks(text: str) -> list[dict[str, Any]]:
    """Extract legacy AUTOPM_WEEKLY_REPORT delimited blocks."""
    blocks = []
    cursor = 0
    while True:
        match = _LEGACY_RESERVED_PATTERN.search(text, cursor)
        if match is None:
            break
        token = match.start()
        start = token - 2
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


def _read_new_blocks(text: str) -> list[dict[str, Any]]:
    """Extract new plain-text format blocks."""
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
        if content:
            blocks.append(
                {
                    "report_date": _report_date(report_date),
                    "fields": {"current_progress": content},
                }
            )
    return blocks


def _blocks(text: str) -> list[dict[str, Any]]:
    """Read all weekly report blocks from text."""
    legacy_blocks = _read_legacy_blocks(text)
    new_blocks = _read_new_blocks(text)
    return legacy_blocks + new_blocks


def _latest(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    """Get the latest report with merged fields."""
    if not blocks:
        return {"report_date": None, "fields": {}}
    fields = {}
    ordered = sorted(blocks, key=lambda block: block["report_date"])
    for block in ordered:
        fields.update(block["fields"])
    return {"report_date": ordered[-1]["report_date"], "fields": fields}


def read_weekly_remark(value: Any) -> dict[str, Any]:
    """Read the newest weekly report from remark text.

    Returns dict with keys:
        - report_date: str or None
        - fields: dict of field_name -> content
    """
    return _latest(_blocks(_text(value, allow_none=True)))


def merge_weekly_remark(
    existing: Any,
    report_date: str,
    fields: Mapping[str, Any],
    *,
    rich_text: bool = False,
) -> str:
    """Append a new report snapshot, preserving existing notes and history.

    Uses delta-only updates: if current_progress is unchanged from the
    latest stored value, returns existing text without modification.

    Args:
        existing: Current Engineering remark text (str or None).
        report_date: YYYY-MM-DD date string.
        fields: Dictionary with at least "current_progress" key.
        rich_text: Accepted for API compatibility but ignored (always plain text).

    Returns:
        Updated remark text with new block appended.
    """
    text = _text(existing, allow_none=True)
    report_date = _report_date(report_date)
    if not isinstance(fields, Mapping):
        raise ValueError("Fields must be a dictionary.")

    blocks = _blocks(text)
    combined = dict(_latest(blocks)["fields"])

    for key in REMARK_FIELDS:
        if key not in fields or fields[key] is None:
            continue
        value = _text(fields[key])
        if _LEGACY_RESERVED_PATTERN.search(value):
            raise ValueError("Weekly report content contains reserved AutoPM markers.")
        if value.strip():
            combined[key] = value

    # Delta-only: skip if unchanged
    latest = _latest(blocks)
    if latest["fields"].get("current_progress") == combined.get("current_progress"):
        return text

    block = f"--- {report_date} ---\n{combined['current_progress']}"
    return _text(text + ("\n\n" if text else "") + block)
