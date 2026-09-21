import io
import json
import ssl
import unittest
import urllib.error
from unittest.mock import patch

from autopm.airtable import AirtableClient, AirtableError, UncertainWriteError, _HttpxOpener, resolve_tables

try:
    import httpx
except ImportError:
    httpx = None


class Clock:
    def __init__(self):
        self.now = 0
        self.waits = []

    def clock(self):
        return self.now

    def sleep(self, seconds):
        self.waits.append(seconds)
        self.now += seconds


class Transport:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, request, timeout):
        self.calls.append(request)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return io.BytesIO(json.dumps(response).encode())


class AirtableTests(unittest.TestCase):
    def test_base_discovery_paginates_without_base_id(self):
        transport = Transport({"bases": [{"id": "appOne"}], "offset": "more"},
                              {"bases": [{"id": "appTwo"}]})
        with AirtableClient("test-token", opener=transport) as client:
            self.assertEqual([b["id"] for b in client.list_bases()], ["appOne", "appTwo"])
            self.assertIn("offset=more", transport.calls[1].full_url)
            with self.assertRaises(AirtableError):
                client.get_schema()
            with self.assertRaises(AirtableError):
                client.get_record("tblAny", "recAny")

    def test_token_id_cannot_be_used_as_base_id(self):
        with self.assertRaisesRegex(AirtableError, "Token ID"):
            AirtableClient("test-token", "patWrong")

    def client(self, transport, **kwargs):
        clock = Clock()
        return AirtableClient("private-test-token", "appTest", opener=transport,
                              sleep=clock.sleep, clock=clock.clock, **kwargs), clock

    def test_pagination_and_throttle(self):
        transport = Transport({"records": [{"id": "rec1", "fields": {}}], "offset": "next"},
                              {"records": [{"id": "rec2", "fields": {}}]})
        client, clock = self.client(transport)
        self.assertEqual([r["id"] for r in client.list_records("tblTest")], ["rec1", "rec2"])
        self.assertIn("returnFieldsByFieldId=true", transport.calls[0].full_url)
        self.assertIn("offset=next", transport.calls[1].full_url)
        self.assertGreaterEqual(clock.now, .25)

    def test_429_waits_at_least_thirty_seconds(self):
        error = urllib.error.HTTPError("https://api.airtable.com", 429, "rate", {"Retry-After": "1"}, None)
        transport = Transport(error, {"id": "rec1", "fields": {}})
        client, clock = self.client(transport)
        client.get_record("tbl1", "rec1")
        self.assertTrue(any(wait >= 30 for wait in clock.waits))

    def test_create_timeout_is_never_retried(self):
        transport = Transport(TimeoutError("connection lost"), {"id": "rec2"})
        client, _ = self.client(transport)
        with self.assertRaises(UncertainWriteError):
            client.create_record("tbl1", {"fldName": "value"})
        self.assertEqual(len(transport.calls), 1)

    def test_create_server_error_is_uncertain(self):
        error = urllib.error.HTTPError("https://api.airtable.com", 503, "error", {}, None)
        transport = Transport(error)
        client, _ = self.client(transport)
        with self.assertRaises(UncertainWriteError):
            client.create_record("tbl1", {"fldName": "value"})
        self.assertEqual(len(transport.calls), 1)

    def test_patch_retries_same_values_no_typecast(self):
        transport = Transport(TimeoutError(), {"id": "rec1", "fields": {"fldName": "new"}})
        client, _ = self.client(transport)
        client.update_record("tbl1", "rec1", {"fldName": "new"})
        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(transport.calls[0].data, transport.calls[1].data)
        self.assertIs(json.loads(transport.calls[0].data)["typecast"], False)

    def test_error_does_not_expose_token(self):
        transport = Transport(urllib.error.URLError("private-test-token"))
        client, _ = self.client(transport, max_retries=0)
        with self.assertRaises(AirtableError) as caught:
            client.get_record("tbl1", "rec1")
        self.assertNotIn("private-test-token", str(caught.exception))

    def test_table_names_are_normalized_and_ambiguities_rejected(self):
        schema = {"tables": [{"id": "tbl" + str(i), "name": name} for i, name in enumerate(
            [" Pro jects ", "TASKS", "Issues", "PeoPle", "Factories"])]}
        self.assertEqual(resolve_tables(schema)["projects"], "tbl0")
        schema["tables"].append({"id": "tblOther", "name": "Projects"})
        with self.assertRaises(AirtableError):
            resolve_tables(schema)

    def test_snapshot_progress_reports_each_table_and_page_without_data(self):
        schema = {"tables": [{"id": "tbl" + str(i), "name": name, "fields": []} for i, name in enumerate(
            ["Projects", "Tasks", "Issues", "People", "Factories"])]}
        transport = Transport(schema,
                              {"records": [{"id": "rec1", "fields": {"private": "not-for-progress"}}], "offset": "second"},
                              {"records": [{"id": "rec2", "fields": {}}]},
                              {"records": []}, {"records": []}, {"records": []}, {"records": []})
        client, _ = self.client(transport)
        events = []
        snapshot = client.snapshot(progress=events.append)
        self.assertEqual(len(snapshot["records"]["tbl0"]), 2)
        self.assertEqual(events[0]["stage"], "schema")
        self.assertEqual(events[-1]["stage"], "done")
        self.assertEqual(events[-1]["records"], 2)
        self.assertEqual(len([event for event in events if event["stage"] == "table_start"]), 5)
        pages = [event for event in events if event["stage"] == "page" and event["table"] == "projects"]
        self.assertEqual([(page["page"], page["records"]) for page in pages], [(1, 1), (2, 2)])
        self.assertNotIn("not-for-progress", json.dumps(events))
        self.assertNotIn("private-test-token", json.dumps(events))


@unittest.skipIf(httpx is None, "httpx is installed by requirements.txt")
class PersistentTransportTests(unittest.TestCase):
    def make_client(self, handler):
        session = httpx.Client(transport=httpx.MockTransport(handler))
        adapter = _HttpxOpener(client=session)
        clock = Clock()
        client = AirtableClient("private-test-token", "appTest", opener=adapter,
                               sleep=clock.sleep, clock=clock.clock)
        self.addCleanup(adapter.close)
        return client, clock, session

    def test_default_reuses_client_verifies_tls_respects_env_and_closes(self):
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(200, json={"id": "rec1", "fields": {}})

        session = httpx.Client(transport=httpx.MockTransport(handler))
        clock = Clock()
        with patch("httpx.Client", return_value=session) as factory:
            with AirtableClient("private-test-token", "appTest", sleep=clock.sleep, clock=clock.clock) as client:
                client.get_record("tbl1", "rec1")
                client.get_record("tbl1", "rec1")
            self.assertEqual(factory.call_count, 1)
            context = factory.call_args.kwargs["verify"]
            self.assertIsInstance(context, ssl.SSLContext)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(context.check_hostname)
            self.assertIs(factory.call_args.kwargs["trust_env"], True)
            self.assertIs(factory.call_args.kwargs["follow_redirects"], False)
        self.assertEqual(len(calls), 2)
        self.assertTrue(session.is_closed)

    def test_httpx_read_error_retries_get_but_never_post(self):
        calls = []

        def handler(request):
            calls.append(request)
            if len(calls) == 1:
                raise httpx.ReadError("sensitive error detail", request=request)
            return httpx.Response(200, json={"id": "rec1", "fields": {}})

        client, _, _ = self.make_client(handler)
        client.get_record("tbl1", "rec1")
        self.assertEqual(len(calls), 2)
        calls.clear()
        with self.assertRaises(UncertainWriteError) as caught:
            client.create_record("tbl1", {"fldName": "value"})
        self.assertEqual(len(calls), 1)
        self.assertNotIn("sensitive error detail", str(caught.exception))

    def test_pool_timeout_diagnostic_keeps_type_without_sensitive_detail(self):
        def handler(request):
            raise httpx.PoolTimeout("sensitive error detail", request=request)
        client, _, _ = self.make_client(handler)
        with self.assertRaises(AirtableError) as caught:
            client.get_record("tbl1", "rec1")
        self.assertIn("PoolTimeout", str(caught.exception))
        self.assertNotIn("sensitive error detail", str(caught.exception))

    def test_httpx_429_reuses_existing_retry_policy(self):
        calls = []

        def handler(request):
            calls.append(request)
            if len(calls) == 1:
                return httpx.Response(429, headers={"Retry-After": "2"})
            return httpx.Response(200, json={"id": "rec1", "fields": {}})

        client, clock, _ = self.make_client(handler)
        client.get_record("tbl1", "rec1")
        self.assertEqual(len(calls), 2)
        self.assertTrue(any(wait >= 30 for wait in clock.waits))

    def test_redirect_is_not_followed_or_forwarded(self):
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(302, headers={"Location": "https://other.example/collect"})

        client, _, _ = self.make_client(handler)
        with self.assertRaisesRegex(AirtableError, "HTTP 302"):
            client.get_record("tbl1", "rec1")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].url.host, "api.airtable.com")

    def test_httpx_post_server_failure_is_uncertain(self):
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(503)

        client, _, _ = self.make_client(handler)
        with self.assertRaises(UncertainWriteError):
            client.create_record("tbl1", {"fldName": "value"})
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
