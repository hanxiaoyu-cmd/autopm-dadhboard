"""Network diagnostics, retry boundaries, and write replay protection."""
import io
import json
import socket
import ssl
import unittest
import urllib.error
from unittest.mock import patch

import httpx

from autopm.airtable import AirtableClient, AirtableError, UncertainWriteError, _HttpxOpener
from autopm.connection import discover_connection
from test_airtable import Clock, Transport


class NetworkRetryTests(unittest.TestCase):
    def make_client(self, transport, **kwargs):
        clock, events = Clock(), []
        client = AirtableClient("private-test-token", "appPrivate", opener=transport,
                               sleep=clock.sleep, clock=clock.clock, on_event=events.append, **kwargs)
        return client, clock, events

    def test_get_retries_three_times_with_backoff_and_reports_recovery(self):
        transport = Transport(TimeoutError(), TimeoutError(), TimeoutError(), {"tables": []})
        client, clock, events = self.make_client(transport)
        self.assertEqual(client.get_schema(), {"tables": []})
        self.assertEqual(len(transport.calls), 4)
        self.assertEqual(clock.waits, [1, 2, 4])
        self.assertEqual([e["attempt"] for e in events if e["stage"] == "request"], [1, 2, 3, 4])
        self.assertEqual([e["retry_in"] for e in events if e["stage"] == "retry"], [1, 2, 4])
        self.assertEqual(events[-1]["stage"], "recovered")
        self.assertIn("第 4 次", events[-1]["message"])

    def test_exhaustion_exposes_structured_report_without_raw_details(self):
        transport = Transport(*(urllib.error.URLError("http://user:proxy-secret@proxy.local/private-test-token") for _ in range(4)))
        client, _, events = self.make_client(transport)
        with self.assertRaises(AirtableError) as caught:
            client.get_schema()
        self.assertEqual(len(transport.calls), 4)
        report = caught.exception.report
        self.assertEqual(report["attempt"], 4)
        self.assertEqual(report["stage"], "failed")
        self.assertIn("用完", report["stop_reason"])
        self.assertIn("api.airtable.com", report["report"])
        for secret in ("private-test-token", "proxy-secret", "proxy.local", "appPrivate"):
            self.assertNotIn(secret, json.dumps(events) + str(caught.exception))

    def test_http_auth_permission_and_invalid_request_fail_without_retries(self):
        for status in (400, 401, 403, 404, 407, 422):
            with self.subTest(status=status):
                transport = Transport(urllib.error.HTTPError("https://api.airtable.com/private", status,
                                                            "private-test-token", {}, None))
                client, _, events = self.make_client(transport)
                with self.assertRaises(AirtableError) as caught:
                    client.get_schema()
                self.assertEqual(len(transport.calls), 1)
                self.assertEqual(events[-1]["diagnosis"]["code"], f"http_{status}")
                self.assertNotIn("private-test-token", str(caught.exception))
                self.assertFalse(any(e["stage"] == "retry" for e in events))

    def test_post_429_retries_rejected_request_with_same_payload(self):
        transport = Transport(urllib.error.HTTPError("https://api.airtable.com", 429, "rate", {}, None),
                              {"id": "recNew", "fields": {}})
        client, clock, events = self.make_client(transport)
        client.create_record("tblPrivate", {"fldPrivate": "private-record-value"})
        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(transport.calls[0].data, transport.calls[1].data)
        self.assertEqual(clock.waits, [30])
        self.assertNotIn("private-record-value", json.dumps(events))

    def test_post_408_and_5xx_never_replay(self):
        for status in (408, 500, 502, 503, 504):
            with self.subTest(status=status):
                transport = Transport(urllib.error.HTTPError("https://api.airtable.com", status, "error", {}, None))
                client, _, events = self.make_client(transport)
                with self.assertRaises(UncertainWriteError) as caught:
                    client.create_record("tbl1", {"fldName": "value"})
                self.assertEqual(len(transport.calls), 1)
                self.assertIn("结果未知", caught.exception.report["stop_reason"])
                self.assertFalse(any(e["stage"] == "retry" for e in events))

    def test_post_unreadable_json_never_replay(self):
        calls = []
        def invalid(request, timeout):
            calls.append(request)
            return io.BytesIO(b"proxy-secret not json")
        client, _, events = self.make_client(invalid)
        with self.assertRaises(UncertainWriteError) as caught:
            client.create_record("tbl1", {"fldName": "value"})
        self.assertEqual(len(calls), 1)
        self.assertEqual(events[-1]["diagnosis"]["code"], "invalid_json")
        self.assertNotIn("proxy-secret", str(caught.exception) + json.dumps(events))

    def test_observer_failure_cannot_replay_successful_create(self):
        transport = Transport({"id": "recNew", "fields": {}})
        client, _, _ = self.make_client(transport)
        def broken_observer(event):
            raise OSError("observer unavailable")
        client._on_event = broken_observer
        self.assertEqual(client.create_record("tbl1", {})["id"], "recNew")
        self.assertEqual(len(transport.calls), 1)

    def test_retry_after_invalid_headers_are_bounded_and_large_delays_stop(self):
        for headers in (None, {}, {"Retry-After": "nan"}, {"Retry-After": "inf"},
                        {"Retry-After": "invalid"}, {"Retry-After": "-1"}):
            with self.subTest(headers=headers):
                self.assertEqual(AirtableClient._rate_limit_wait(headers), 30)
        transport = Transport(urllib.error.HTTPError("https://api.airtable.com", 429, "rate", {"Retry-After": "86400"}, None))
        client, clock, events = self.make_client(transport)
        with self.assertRaises(AirtableError):
            client.get_schema()
        self.assertEqual(len(transport.calls), 1)
        self.assertEqual(clock.waits, [])
        self.assertIn("超过 5 分钟", events[-1]["stop_reason"])

    def test_discovery_uses_four_attempts_and_passes_event_observer(self):
        events = []
        with patch("autopm.connection.AirtableClient") as factory:
            client = factory.return_value.__enter__.return_value
            client.list_bases.return_value = [{"id": "appOne"}, {"id": "appTwo"}]
            discover_connection("patExample.secret", on_event=events.append)
            self.assertEqual(factory.call_args.kwargs["max_retries"], 3)
            self.assertEqual(factory.call_args.kwargs["timeout"], 15)
            self.assertEqual(factory.call_args.kwargs["on_event"], events.append)


class TransportCauseTests(unittest.TestCase):
    def run_error(self, root_cause):
        calls, events, clock = [], [], Clock()
        def handler(request):
            calls.append(request)
            try:
                raise root_cause
            except Exception as cause:
                raise httpx.ConnectError("proxy http://user:proxy-secret@proxy.local/private-test-token", request=request) from cause
        with httpx.Client(transport=httpx.MockTransport(handler)) as session:
            adapter = _HttpxOpener(client=session)
            with AirtableClient("private-test-token", opener=adapter, sleep=clock.sleep,
                               clock=clock.clock, on_event=events.append) as client:
                with self.assertRaises(AirtableError) as caught:
                    client.list_bases()
        return calls, events, caught.exception

    def test_dns_chain_is_visible_in_safe_report_and_retried(self):
        calls, events, error = self.run_error(socket.gaierror(socket.EAI_NONAME, "private DNS detail"))
        self.assertEqual(len(calls), 4)
        self.assertEqual(error.report["diagnosis"]["code"], "dns")
        for secret in ("private DNS detail", "proxy-secret", "proxy.local", "private-test-token"):
            self.assertNotIn(secret, str(error) + json.dumps(events))

    def test_certificate_failure_is_reported_without_pointless_retries(self):
        calls, events, error = self.run_error(ssl.SSLCertVerificationError(1, "certificate verify failed"))
        self.assertEqual(len(calls), 1)
        self.assertTrue(error.report["diagnosis"]["code"].startswith("tls_certificate"))
        self.assertFalse(error.report["diagnosis"]["retryable"])
        self.assertEqual([e["stage"] for e in events], ["request", "failed"])


if __name__ == "__main__":
    unittest.main()
