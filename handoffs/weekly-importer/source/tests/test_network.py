import errno
import json
import os
import socket
import ssl
import unittest
import urllib.error
from dataclasses import FrozenInstanceError
from unittest.mock import patch

from autopm.network import NetworkDiagnosis, diagnose_network_error, verified_tls_context

try:
    import httpx
    import httpcore
except ImportError:
    httpx = httpcore = None


def caused_by(error, cause):
    error.__cause__ = cause
    return error


class NetworkDiagnosisTests(unittest.TestCase):
    def test_default_tls_loads_system_trust_without_disabling_verification(self):
        with patch.dict(os.environ, {"SSL_CERT_FILE": "", "SSL_CERT_DIR": ""}), patch.object(ssl.SSLContext, 'load_default_certs', autospec=True) as loader:
            context = verified_tls_context()
        loader.assert_called_once()
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_invalid_explicit_ca_never_falls_back_to_unverified_connection(self):
        with patch.dict(os.environ, {"SSL_CERT_FILE": "invalid-ca-fixture.pem", "SSL_CERT_DIR": ""}), patch('ssl.create_default_context', side_effect=ssl.SSLError('invalid configured CA')) as create:
            with self.assertRaises(ssl.SSLError):
                verified_tls_context()
        create.assert_called_once_with(cafile='invalid-ca-fixture.pem', capath=None)

    def test_report_is_frozen_and_serializable(self):
        result = diagnose_network_error(socket.gaierror(socket.EAI_AGAIN, "private-host"))
        self.assertIsInstance(result, NetworkDiagnosis)
        self.assertEqual(result.code, "dns")
        self.assertEqual(result.error_type, "gaierror")
        self.assertEqual(json.loads(json.dumps(result.as_dict()))["code"], "dns")
        with self.assertRaises(FrozenInstanceError):
            result.title = "changed"

    def test_urllib_reason_and_context_are_unwrapped(self):
        outer = urllib.error.URLError(urllib.error.URLError(socket.gaierror(socket.EAI_AGAIN, "secret")))
        self.assertEqual(diagnose_network_error(outer).code, "dns")
        outer = RuntimeError("private-token")
        outer.__context__ = OSError(errno.ECONNREFUSED, "private-proxy")
        self.assertEqual(diagnose_network_error(outer).code, "connection_refused")

    def test_urllib_exception_reason_takes_priority_over_unrelated_context(self):
        old_certificate = ssl.SSLCertVerificationError(1, "old failure")
        old_certificate.verify_code = 10
        outer = urllib.error.URLError(socket.gaierror(socket.EAI_AGAIN, "current failure"))
        outer.__context__ = old_certificate
        result = diagnose_network_error(outer)
        self.assertEqual(result.code, "dns")
        self.assertTrue(result.retryable)

    def test_explicit_cause_takes_priority_over_urllib_reason(self):
        old_certificate = ssl.SSLCertVerificationError(1, "old failure")
        old_certificate.verify_code = 10
        outer = caused_by(urllib.error.URLError(old_certificate), socket.gaierror(socket.EAI_AGAIN, "current failure"))
        result = diagnose_network_error(outer)
        self.assertEqual(result.code, "dns")
        self.assertTrue(result.retryable)

    def test_context_is_available_when_suppressed_without_an_explicit_cause(self):
        outer = RuntimeError("wrapper")
        outer.__context__ = socket.gaierror(socket.EAI_AGAIN, "current failure")
        outer.__suppress_context__ = True
        self.assertEqual(diagnose_network_error(outer).code, "dns")

    def test_cyclic_and_long_chains_are_bounded(self):
        outer = urllib.error.URLError("secret")
        inner = socket.gaierror(socket.EAI_AGAIN, "secret")
        outer.reason = outer
        outer.__cause__ = inner
        inner.__context__ = outer
        self.assertEqual(diagnose_network_error(outer).code, "dns")
        unknown = RuntimeError("secret")
        unknown.__cause__ = unknown
        self.assertEqual(diagnose_network_error(unknown).code, "network_error")
        for _ in range(100):
            unknown = caused_by(RuntimeError("secret"), unknown)
        self.assertEqual(diagnose_network_error(unknown).code, "network_error")

    def test_socket_and_windows_numeric_errors(self):
        cases = [(errno.ECONNREFUSED, "connection_refused"), (errno.ENETUNREACH, "network_unreachable"),
                 (errno.EHOSTUNREACH, "network_unreachable"), (errno.ECONNRESET, "connection_reset"),
                 (errno.EPIPE, "connection_reset"), (errno.ETIMEDOUT, "timeout"),
                 (errno.EACCES, "network_permission"), (10061, "connection_refused"),
                 (10051, "network_unreachable"), (10054, "connection_reset"), (10060, "timeout")]
        for number, code in cases:
            with self.subTest(number=number):
                self.assertEqual(diagnose_network_error(OSError(number, "private endpoint")).code, code)
        wrapped = OSError("private endpoint")
        wrapped.winerror = 10061
        self.assertEqual(diagnose_network_error(wrapped).code, "connection_refused")
        self.assertEqual(diagnose_network_error(ConnectionRefusedError()).code, "connection_refused")
        self.assertEqual(diagnose_network_error(ConnectionResetError()).code, "connection_reset")

    def test_certificate_verification_codes_are_specific_and_never_retried(self):
        cases = [(9, "tls_certificate_not_yet_valid"), (10, "tls_certificate_expired"),
                 (18, "tls_certificate_untrusted"), (19, "tls_certificate_untrusted"),
                 (20, "tls_certificate_untrusted"), (21, "tls_certificate_untrusted"),
                 (23, "tls_certificate_revoked"), (62, "tls_hostname_mismatch"),
                 (999, "tls_certificate_invalid")]
        for number, code in cases:
            with self.subTest(number=number):
                certificate = ssl.SSLCertVerificationError(1, "private-token")
                certificate.verify_code = number
                result = diagnose_network_error(urllib.error.URLError(certificate))
                self.assertEqual(result.code, code)
                self.assertFalse(result.retryable)
                self.assertEqual(result.error_type, "SSLCertVerificationError")

    def test_tls_reason_is_structured_and_raw_text_does_not_establish_cause(self):
        failure = ssl.SSLError(1, "private-proxy: CERTIFICATE_VERIFY_FAILED")
        self.assertEqual(diagnose_network_error(failure).code, "tls_handshake")
        failure.reason = "CERTIFICATE_VERIFY_FAILED"
        self.assertEqual(diagnose_network_error(failure).code, "tls_certificate_invalid")
        failure.reason = "WRONG_VERSION_NUMBER"
        result = diagnose_network_error(failure)
        self.assertEqual(result.code, "tls_configuration_error")
        self.assertFalse(result.retryable)

    def test_arbitrary_messages_urls_and_type_names_are_never_returned(self):
        private = "http://proxy-user:proxy-password@proxy.invalid:7897/?token=pat-secret"
        secret_class = type("secret_token_as_class_name", (RuntimeError,), {})
        for error in (urllib.error.URLError(private), OSError(errno.ECONNREFUSED, private),
                      ssl.SSLCertVerificationError(1, private), secret_class(private)):
            with self.subTest(error=type(error)):
                report = json.dumps(diagnose_network_error(error).as_dict())
                for secret in ("proxy-user", "proxy-password", "proxy.invalid", "pat-secret", "secret_token_as_class_name"):
                    self.assertNotIn(secret, report)
        self.assertEqual(diagnose_network_error(secret_class(private)).error_type, "UnknownError")

    def test_network_type_name_in_urllib_string_is_not_trusted_as_evidence(self):
        result = diagnose_network_error(urllib.error.URLError("ConnectError"))
        self.assertEqual(result.code, "network_error")


@unittest.skipIf(httpx is None, "httpx is installed by requirements.txt")
class HttpxNetworkDiagnosisTests(unittest.TestCase):
    def test_explicit_httpx_cause_excludes_unrelated_prior_certificate_context(self):
        old_certificate = ssl.SSLCertVerificationError(1, "old failure")
        old_certificate.verify_code = 10
        error = caused_by(httpx.ConnectError("wrapper"), socket.gaierror(socket.EAI_AGAIN, "current failure"))
        error.__context__ = old_certificate
        result = diagnose_network_error(error)
        self.assertEqual(result.code, "dns")
        self.assertTrue(result.retryable)
        self.assertEqual(result.error_type, "gaierror")

    def test_real_httpx_transport_maps_socket_failure_without_losing_diagnosis(self):
        # Exercise httpx/httpcore's real exception mapping without using the network.
        failure = socket.gaierror(socket.EAI_AGAIN, "private-dns-message")
        with httpx.Client(trust_env=False) as client:
            with patch("httpcore._backends.sync.socket.create_connection", side_effect=failure):
                with self.assertRaises(httpx.ConnectError) as caught:
                    client.get("https://example.invalid")
        result = diagnose_network_error(caught.exception)
        self.assertEqual(result.code, "dns")
        self.assertEqual(result.error_type, "gaierror")
        self.assertNotIn("private-dns-message", json.dumps(result.as_dict()))

    def test_httpx_httpcore_os_cause_chain_preserves_specific_cause(self):
        dns = socket.gaierror(socket.EAI_AGAIN, "private-host")
        core = caused_by(httpcore.ConnectError("private-proxy"), dns)
        error = caused_by(httpx.ConnectError("private-token"), core)
        result = diagnose_network_error(urllib.error.URLError(error))
        self.assertEqual(result.code, "dns")
        self.assertTrue(result.retryable)
        self.assertEqual(result.error_type, "gaierror")

    def test_httpx_certificate_chain_does_not_retry(self):
        certificate = ssl.SSLCertVerificationError(1, "private certificate")
        certificate.verify_code = 10
        error = caused_by(httpx.ConnectError("secret"), caused_by(httpcore.ConnectError("secret"), certificate))
        result = diagnose_network_error(error)
        self.assertEqual(result.code, "tls_certificate_expired")
        self.assertFalse(result.retryable)

    def test_timeout_phase_is_preserved_despite_generic_timeout_cause(self):
        for name, code in (("ConnectTimeout", "connect_timeout"), ("ReadTimeout", "read_timeout"),
                           ("WriteTimeout", "write_timeout"), ("PoolTimeout", "pool_timeout")):
            with self.subTest(name=name):
                error = caused_by(getattr(httpx, name)("private-token"), TimeoutError("secret"))
                result = diagnose_network_error(error)
                self.assertEqual(result.code, code)
                self.assertTrue(result.retryable)
                self.assertEqual(result.error_type, name)

    def test_httpx_transport_families_and_retry_policy(self):
        for name, code, retryable in (("ProxyError", "proxy", True), ("ReadError", "read_error", True),
                ("WriteError", "write_error", True), ("RemoteProtocolError", "protocol_error", True),
                ("LocalProtocolError", "local_protocol_error", False),
                ("UnsupportedProtocol", "unsupported_protocol", False)):
            with self.subTest(name=name):
                result = diagnose_network_error(getattr(httpx, name)("secret"))
                self.assertEqual(result.code, code)
                self.assertIs(result.retryable, retryable)

    def test_httpcore_connect_407_is_not_retried_and_reason_phrase_is_private(self):
        private = "http://proxy-user:proxy-password@proxy.invalid/?token=pat-secret"
        core = httpcore.ProxyError("407 " + private)
        error = caused_by(httpx.ProxyError("private wrapper"), core)
        result = diagnose_network_error(error)
        self.assertEqual(result.code, "proxy_authentication")
        self.assertFalse(result.retryable)
        self.assertIn("407", result.detail)
        report = json.dumps(result.as_dict())
        for secret in ("proxy-user", "proxy-password", "proxy.invalid", "pat-secret", "private wrapper"):
            self.assertNotIn(secret, report)

    def test_407_in_arbitrary_error_text_does_not_prove_proxy_authentication_failure(self):
        for error in (httpx.ProxyError("407 private"), httpcore.ProxyError("failure: 407 private"),
                      httpcore.ProxyError("4070 private"), httpcore.ProxyError("502 mentions 407"),
                      urllib.error.URLError("407 private"), httpx.ConnectError("407 private")):
            with self.subTest(error=type(error)):
                result = diagnose_network_error(error)
                self.assertNotEqual(result.code, "proxy_authentication")
                self.assertTrue(result.retryable)

    def test_unknown_connect_error_does_not_guess_from_sensitive_message(self):
        error = httpx.ConnectError("https://user:password@proxy.invalid:7897?token=pat-secret CERTIFICATE_VERIFY_FAILED")
        result = diagnose_network_error(error)
        self.assertEqual(result.code, "connect_error")
        self.assertIn("底层原因未确认", result.detail)
        self.assertTrue(result.retryable)
        report = json.dumps(result.as_dict())
        for secret in ("user:password", "proxy.invalid", "pat-secret", "CERTIFICATE_VERIFY_FAILED"):
            self.assertNotIn(secret, report)


if __name__ == "__main__":
    unittest.main()
