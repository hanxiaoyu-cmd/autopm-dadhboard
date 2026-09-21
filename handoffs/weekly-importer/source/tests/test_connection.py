import unittest
from unittest.mock import MagicMock, patch

from autopm.connection import discover_connection
from autopm.airtable import AirtableError


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.patch = patch("autopm.connection.AirtableClient")
        self.factory = self.patch.start()
        self.addCleanup(self.patch.stop)
        self.client = self.factory.return_value.__enter__.return_value
        self.client.list_bases.return_value = [{"id": "appOne", "name": "Copy"}]
        self.client.get_schema.return_value = {"tables": [
            {"id": "tbl" + n, "name": n} for n in ("Projects", "Tasks", "Issues", "People", "Factories")]}

    def test_token_id_rejected_before_network(self):
        for token in ("", "patOnlyId", "patOnlyId."):
            with self.assertRaisesRegex(AirtableError, "完整 Token"):
                discover_connection(token)
        self.factory.assert_not_called()

    def test_single_base_auto_resolves_tables(self):
        result = discover_connection(" patExample.secret ")
        self.assertEqual(result["base"]["id"], "appOne")
        self.assertEqual(result["tables"]["projects"], "tblProjects")
        self.assertEqual(self.client.base_id, "appOne")

    def test_multiple_same_name_bases_require_id_selection(self):
        self.client.list_bases.return_value.append({"id": "appTwo", "name": "Copy"})
        result = discover_connection("patExample.secret")
        self.assertNotIn("base", result)
        self.client.get_schema.assert_not_called()
        selected = discover_connection("patExample.secret", "appTwo")
        self.assertEqual(selected["base"]["id"], "appTwo")

    def test_unavailable_selection_is_not_used(self):
        with self.assertRaisesRegex(AirtableError, "授权列表"):
            discover_connection("patExample.secret", "appStale")
        self.client.get_schema.assert_not_called()

    def test_no_accessible_base(self):
        self.client.list_bases.return_value = []
        with self.assertRaisesRegex(AirtableError, "未找到"):
            discover_connection("patExample.secret")

    def test_missing_or_ambiguous_tables_never_guess(self):
        self.client.get_schema.return_value["tables"].append({"id": "tblDuplicate", "name": " projects "})
        with self.assertRaises(AirtableError):
            discover_connection("patExample.secret")

