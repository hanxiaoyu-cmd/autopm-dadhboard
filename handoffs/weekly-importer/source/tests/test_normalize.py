from datetime import date, datetime
import unittest

from autopm.normalize import clean_text, normalize_header, normalize_key, normalize_project_id, parse_date


class NormalizeTests(unittest.TestCase):
    def test_keys_ignore_unicode_spacing_and_case(self):
        self.assertEqual(normalize_key(" Current\u00a0Progress （Manual） "), normalize_key("current progress (Manual)"))
        self.assertEqual(normalize_header(" Project \n Number："), "projectnumber")
        self.assertEqual(normalize_project_id(" ｎｘａ ０２４３\u200b "), "NXA0243")
        self.assertNotEqual(normalize_project_id("AB-12"), normalize_project_id("AB12"))

    def test_date_types_and_ambiguity(self):
        self.assertEqual(parse_date(datetime(2026, 9, 7)), "2026-09-07")
        self.assertEqual(parse_date(date(2026, 9, 7)), "2026-09-07")
        self.assertIsNone(parse_date("9/7", "2026-09-01"))
        self.assertEqual(parse_date("9/7", "2026-09-01", date_order="MDY"), "2026-09-07")
        self.assertIsNone(parse_date("9/7"))
        self.assertIsNone(parse_date("2026-02-30"))
        self.assertIsNone(parse_date("2026-09-01 -> 2026-10-01"))
        self.assertIsNone(parse_date(45555))

    def test_clean_text_preserves_paragraphs(self):
        self.assertEqual(clean_text("  A\t B\r\n C  "), "A B\nC")


if __name__ == "__main__":
    unittest.main()
