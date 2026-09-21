import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from autopm import local_files


class LocalFilesTests(unittest.TestCase):
    def test_source_and_dist_roots_and_empty_library(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.assertEqual(local_files.workspace_root(root), root)
            self.assertEqual(local_files.workspace_root(root / "dist"), root)
            self.assertEqual(local_files.scan_local_files(root), [])
            # A source directory may itself be named dist.
            (root / "dist" / local_files.SOURCE_DIRECTORY).mkdir(parents=True)
            self.assertEqual(local_files.workspace_root(root / "dist"), root / "dist")

    def test_only_known_existing_materials_are_classified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / local_files.SOURCE_DIRECTORY
            source.mkdir()
            filenames = {
                "APAC Shark XPT Project Weekly Report V2 (1).xlsx": "weekly",
                "Ninja XPT Projects Weekly Report-20260518 (3).xlsx": "weekly",
                "All Projects Tracker SUNNY (1).xlsx": "tracker",
                "weekly report rule.pptx": "rules",
                "AutoPM_Bridge_v5.exe": "legacy",
            }
            for filename in filenames:
                (source / filename).write_bytes(b"local test material")
            (source / "sync_config.json").write_bytes(b"do not inspect")
            (source / "another-report.xlsx").write_bytes(b"not in the fixed library")
            rows = local_files.scan_local_files(root)
            self.assertEqual({row["filename"]: row["kind"] for row in rows}, filenames)
            self.assertTrue(all(Path(row["path"]).is_absolute() for row in rows))
            tracker = next(row for row in rows if row["kind"] == "tracker")
            self.assertIn("导出日期未确认", tracker["date_label"])
            self.assertTrue(all(row["size_text"] for row in rows))

    def test_verified_date_expires_when_workbook_content_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / local_files.SOURCE_DIRECTORY
            source.mkdir()
            path = source / "Ninja XPT Projects Weekly Report-20260518 (3).xlsx"
            original = b"verified workbook content"
            path.write_bytes(original)
            digest = hashlib.sha256(original).hexdigest()
            with patch.dict(local_files.KNOWN_REPORT_DATES, {digest: "已验证日期范围"}):
                self.assertEqual(local_files.scan_local_files(root)[0]["date_label"], "已验证日期范围")
                path.write_bytes(b"different workbook content")
                self.assertEqual(local_files.scan_local_files(root)[0]["date_label"], "日期待检查")


if __name__ == "__main__":
    unittest.main()
