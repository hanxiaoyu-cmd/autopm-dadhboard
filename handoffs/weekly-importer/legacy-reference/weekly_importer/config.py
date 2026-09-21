"""Configuration management for Weekly Report Importer.

Supports loading from:
- Environment variables (prefixed with AIRTABLE_)
- JSON config file
- Direct dictionary

Priority: env vars > config file > defaults
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATHS = [
    "weekly_importer.json",
    "config/weekly_importer.json",
    "~/.weekly_importer.json",
]

DEFAULT_CONFIG = {
    "api_version": "v0",
    "batch_size": 10,
    "request_timeout": 30,
    "max_retries": 3,
    "retry_delay": 1.0,
}


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load configuration from file and environment variables.

    Args:
        config_path: Optional explicit path to JSON config file.

    Returns:
        Merged configuration dictionary.

    Raises:
        FileNotFoundError: If explicit config_path is given but does not exist.
        ValueError: If required credentials are missing.
    """
    config = dict(DEFAULT_CONFIG)

    # Load from file if available
    loaded = _load_from_file(config_path)
    config.update(loaded)

    # Override with environment variables
    env = _load_from_env()
    config.update(env)

    # Validate required fields
    if not config.get("api_token"):
        raise ValueError(
            "Missing Airtable API token. Set AIRTABLE_API_TOKEN environment variable "
            "or add 'api_token' to your config file."
        )
    if not config.get("base_id"):
        raise ValueError(
            "Missing Airtable base ID. Set AIRTABLE_BASE_ID environment variable "
            "or add 'base_id' to your config file."
        )

    return config


def _load_from_file(config_path: str | None) -> dict[str, Any]:
    """Attempt to load configuration from JSON file."""
    if config_path:
        path = Path(config_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    for candidate in DEFAULT_CONFIG_PATHS:
        path = Path(candidate).expanduser()
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

    return {}


def _load_from_env() -> dict[str, Any]:
    """Load configuration from environment variables."""
    env = {}
    mappings = {
        "AIRTABLE_API_TOKEN": "api_token",
        "AIRTABLE_BASE_ID": "base_id",
        "AIRTABLE_TABLE_ID": "table_id",
        "AIRTABLE_PROJECTS_TABLE": "projects_table_id",
        "AIRTABLE_TASKS_TABLE": "tasks_table_id",
        "AIRTABLE_API_VERSION": "api_version",
        "AIRTABLE_BATCH_SIZE": "batch_size",
    }

    for env_var, config_key in mappings.items():
        value = os.environ.get(env_var)
        if value:
            if config_key in ("batch_size", "max_retries"):
                value = int(value)
            elif config_key == "retry_delay":
                value = float(value)
            env[config_key] = value

    return env
