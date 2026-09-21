"""Conservative normalization shared by extraction and record matching."""

from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime


def clean_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (date, datetime)):
        return (
            value.date().isoformat()
            if isinstance(value, datetime)
            else value.isoformat()
        )
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    text = unicodedata.normalize("NFKC", str(value))
    text = re.sub(r"[\u200b-\u200d\ufeff]", "", text)
    return "\n".join(
        re.sub(r"[^\S\n]+", " ", line).strip() for line in text.splitlines()
    ).strip()


def normalize_key(value) -> str:
    return re.sub(r"\s+", "", clean_text(value)).casefold()


def normalize_project_id(value) -> str:
    # Preserve punctuation: AB-12 and AB12 are distinct projects.
    text = clean_text(value).translate(str.maketrans({"–": "-", "—": "-", "−": "-"}))
    return normalize_key(text).upper()


def normalize_header(value) -> str:
    return re.sub(r"[^\w]", "", normalize_key(value), flags=re.UNICODE).replace("_", "")


def normalize_task_title(value: str) -> str:
    """Remove regional suffixes and normalize for title matching.

    Strips trailing region codes like (CN), (VN), (TH) etc. and collapses
    whitespace so the same milestone with different regional variants maps
    to one canonical title.
    """
    text = clean_text(value)
    text = re.sub(
        r"\s*\(\s*(?:CN|VN|TH|ID|IDN|MY|KH|US|UK|EU)\s*\)\s*$",
        "",
        text,
        flags=re.I,
    )
    return normalize_key(text)


def parse_date(value, report_date=None, *, date_order="AUTO") -> str | None:
    """AUTO accepts only unambiguous numeric dates; MDY/DMY are explicit policies.

    Yearless dates more than half a year from the report need an explicit year.
    This avoids silently putting a next-January milestone in the preceding year.
    """
    if date_order not in {"AUTO", "MDY", "DMY"}:
        raise ValueError("日期顺序须为 AUTO、MDY 或 DMY。")
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if not isinstance(value, str):
        return None  # Numeric Excel dates must be decoded using workbook date styles/epoch.
    text = clean_text(value).strip()
    if not text:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        try:
            return date.fromisoformat(text).isoformat()
        except ValueError:
            return None
    if "T" in text:
        try:
            return datetime.fromisoformat(text).date().isoformat()
        except ValueError:
            return None
    numeric = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})(?:/(\d{4}))?", text)
    if numeric:
        first, second = int(numeric[1]), int(numeric[2])
        if date_order == "AUTO" and first != second and first <= 12 and second <= 12:
            return None
        day_first = date_order == "DMY" or (date_order == "AUTO" and first > 12)
        month, day = (second, first) if day_first else (first, second)
        context = parse_date(report_date) if report_date else None
        year = numeric[3] or (context[:4] if context else None)
        if not year:
            return None
        try:
            result = date(int(year), month, day)
            if (
                not numeric[3]
                and context
                and abs((result - date.fromisoformat(context)).days) > 183
            ):
                return None
            return result.isoformat()
        except ValueError:
            return None
    for fmt in (
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%Y年%m月%d日",
        "%Y%m%d",
        "%d-%b-%Y",
        "%d-%b-%y",
        "%d %b %Y",
        "%b %d, %Y",
        "%Y-%m-%d %H:%M:%S",
    ):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    if report_date:
        year = parse_date(report_date)
        if year:
            for fmt in ("%d-%b", "%d %b", "%b %d"):
                try:
                    result = datetime.strptime(f"{text} {year[:4]}", fmt + " %Y").date()
                    if abs((result - date.fromisoformat(year)).days) > 183:
                        return None
                    return result.isoformat()
                except ValueError:
                    pass
    return None


# === Stage classification for singleSelect fields ===
_STAGE_PATTERNS = {
    "PB": [
        "p1",
        "p2",
        "p3",
        "pre-build",
        "prebuild",
        "pre-build review",
        "pilot",
        "pilot run",
        "first sample",
        "initial sample",
    ],
    "EB": [
        "eb1",
        "eb2",
        "eb3",
        "engineering build",
        "engineering pilot",
        "engineering validation",
        "ev build",
        "dv build",
    ],
    "MP": [
        "mp",
        "mass production",
        "mass-prod",
        "ramp up",
        "ramp-up",
        "volume production",
        "production",
        "milestone release",
        "go live",
    ],
    "Delay": [
        "delay",
        "delayed",
        "postpone",
        "postponed",
        "hold",
        "on hold",
        "suspend",
        "suspended",
        "wait",
        "waiting",
    ],
}


def normalize_stage(text) -> str | None:
    """Classify weekly progress text into a canonical project stage.

    Only returns a stage when the evidence is unambiguous.
    Falls back to None so callers can retain the existing field value.
    """
    if not text or not isinstance(text, str):
        return None
    lowered = clean_text(text).casefold()
    for stage, keywords in _STAGE_PATTERNS.items():
        for kw in keywords:
            if kw in lowered:
                return stage
    return None
