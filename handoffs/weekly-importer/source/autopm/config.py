"""Local settings. Secrets use Windows DPAPI and are never written in clear text."""
from __future__ import annotations

import base64
from copy import deepcopy
import ctypes
import json
import os
from pathlib import Path
import sys

ROOT = (
    Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "AutoPM-Preview"
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent.parent
)
LOCAL = ROOT / ".local"
SETTINGS = LOCAL / "settings.json"
SECRET_KEYS = ("deepseek_api_key", "airtable_token")
DEFAULTS = {
    "project_identity_mode": "number_sku_factory",
    "require_milestone": False,
    "date_order": "AUTO",
    "deepseek_base_url": "https://api.deepseek.com",
    "deepseek_model": "deepseek-v4-flash",
    "base_id": "", "projects_table_id": "", "tasks_table_id": "", "issues_table_id": "",
}


def with_base_defaults(settings):
    """Ship confirmed, non-secret bindings; validate them against live schema.

    Saved choices override these defaults. Other bases receive no such bindings.
    """
    config = deepcopy(settings)
    base = "appOMWiK4CTOH7iQu"
    if config.get("base_id") != base:
        return config
    config.setdefault("project_report_storage", "engineering_remark")
    config.setdefault("project_report_storage_base_id", base)
    defaults = {
        "tasks": {"project": "fldZmIf1cjO1baWz9", "duration": None},
        "issues": {"project": "fldbZYuFwTSkfRTw6"},
        "factories": {"factory_id": "fldHTj7koS2Ke4UdW", "code": "fldAwh01Lzi3zdmHc", "old_name": None},
    }
    from .weekly_remark import uses_weekly_remark
    if uses_weekly_remark(config):
        defaults["projects"] = {"report_date": None}
    mappings = config.setdefault("field_mapping", {})
    for kind, fields in defaults.items():
        configured = mappings.setdefault(kind, {})
        for key, value in fields.items():
            configured.setdefault(key, value)
    return config


def _protect(value: bytes, decrypt=False) -> bytes:
    if os.name != "nt":
        raise RuntimeError("密钥本地保存仅支持 Windows。其他系统请使用环境变量。")
    class Blob(ctypes.Structure):
        _fields_ = [("size", ctypes.c_ulong), ("data", ctypes.POINTER(ctypes.c_ubyte))]
    buf = ctypes.create_string_buffer(value)
    incoming = Blob(len(value), ctypes.cast(buf, ctypes.POINTER(ctypes.c_ubyte)))
    outgoing = Blob()
    fn = ctypes.windll.crypt32.CryptUnprotectData if decrypt else ctypes.windll.crypt32.CryptProtectData
    if not fn(ctypes.byref(incoming), None, None, None, None, 1, ctypes.byref(outgoing)):
        raise ctypes.WinError()
    try:
        return ctypes.string_at(outgoing.data, outgoing.size)
    finally:
        ctypes.windll.kernel32.LocalFree(outgoing.data)


def load_settings() -> dict:
    settings = dict(DEFAULTS)
    if SETTINGS.exists():
        saved = json.loads(SETTINGS.read_text(encoding="utf-8"))
        settings.update({k: v for k, v in saved.items() if k not in SECRET_KEYS and k != "encrypted_secrets"})
        for key, value in saved.get("encrypted_secrets", {}).items():
            if key in SECRET_KEYS:
                settings[key] = _protect(base64.b64decode(value), decrypt=True).decode("utf-8")
    settings["deepseek_api_key"] = os.getenv("DEEPSEEK_API_KEY") or settings.get("deepseek_api_key", "")
    settings["airtable_token"] = os.getenv("AIRTABLE_TOKEN") or settings.get("airtable_token", "")
    settings["base_id"] = os.getenv("AIRTABLE_BASE_ID") or settings.get("base_id", "")
    return settings


def save_settings(settings: dict):
    LOCAL.mkdir(parents=True, exist_ok=True)
    saved = {k: v for k, v in settings.items() if k not in SECRET_KEYS}
    saved["encrypted_secrets"] = {
        k: base64.b64encode(_protect(settings[k].encode("utf-8"))).decode("ascii")
        for k in SECRET_KEYS if settings.get(k)
    }
    temp = SETTINGS.with_suffix(".tmp")
    temp.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(SETTINGS)


def import_legacy(path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    creds = data.get("airtable_credentials", {})
    return {"airtable_token": creds.get("token", ""), **{
        k: creds.get(k, "") for k in ("base_id", "projects_table_id", "tasks_table_id", "issues_table_id")
    }}


def redact(message, settings):
    text = str(message)
    for key in SECRET_KEYS:
        if settings.get(key):
            text = text.replace(settings[key], "[已隐藏密钥]")
    return text
