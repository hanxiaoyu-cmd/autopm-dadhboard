import os
import unittest
import runpy
import sys
from pathlib import Path
from unittest.mock import patch
import autopm.config as config
from autopm.config import _protect, redact


class ConfigTests(unittest.TestCase):
    def test_shipped_base_defaults_are_scoped_and_preserve_saved_choices(self):
        from autopm.weekly_remark import uses_weekly_remark
        other = {"base_id": "appOther"}
        self.assertEqual(config.with_base_defaults(other), other)
        known = {"base_id": "appOMWiK4CTOH7iQu"}
        result = config.with_base_defaults(known)
        self.assertTrue(uses_weekly_remark(result))
        self.assertNotIn("field_mapping", known)
        saved = {**known, "project_report_storage_by_base": {known["base_id"]: "normal"},
                 "field_mapping": {"tasks": {"project": None}}}
        result = config.with_base_defaults(saved)
        self.assertFalse(uses_weekly_remark(result))
        self.assertIsNone(result["field_mapping"]["tasks"]["project"])
        self.assertNotIn("report_date", result["field_mapping"].get("projects", {}))

    def test_packaged_data_uses_user_directory_not_executable_directory(self):
        with patch.object(sys, "frozen", True, create=True), patch.object(sys, "executable", "C:/Program Files/AutoPM/AutoPM.exe"), patch.dict(os.environ, {"LOCALAPPDATA": "C:/Users/Example/AppData/Local"}):
            loaded = runpy.run_path(config.__file__)
        self.assertEqual(loaded["ROOT"], Path("C:/Users/Example/AppData/Local/AutoPM-Preview"))
        self.assertEqual(loaded["SETTINGS"], loaded["ROOT"] / ".local/settings.json")

    @unittest.skipUnless(os.name == "nt", "Windows DPAPI")
    def test_dpapi_roundtrip(self):
        value = b"test-secret-no-real-key"
        encrypted = _protect(value)
        self.assertNotIn(value, encrypted)
        self.assertEqual(_protect(encrypted, decrypt=True), value)

    def test_redaction(self):
        self.assertNotIn("secret-value", redact("error secret-value", {"deepseek_api_key": "secret-value"}))
