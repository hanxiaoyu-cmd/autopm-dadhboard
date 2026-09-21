"""Safe, structured network diagnostics without exposing exception messages."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import errno
import os
import socket
import ssl
import urllib.error


def verified_tls_context():
    """Use Windows ROOT/CA stores, or an explicitly configured CA bundle.

    Keep hostname and certificate validation enabled in source and frozen builds.
    """
    return ssl.create_default_context(
        cafile=os.environ.get("SSL_CERT_FILE") or None,
        capath=os.environ.get("SSL_CERT_DIR") or None,
    )

try:
    import httpx
except ImportError:  # The diagnostics also support injected urllib transports.
    httpx = None

try:
    import httpcore
except ImportError:
    httpcore = None


@dataclass(frozen=True)
class NetworkDiagnosis:
    code: str
    title: str
    detail: str
    advice: str
    retryable: bool
    error_type: str

    def as_dict(self):
        return asdict(self)


_MESSAGES = {
    "dns": ("DNS 解析失败", "系统未能把目标主机名解析为网络地址。失败可能发生在服务域名或代理域名的解析阶段。",
            "检查网络和 DNS 设置，以及代理是否能够解析目标域名。", True),
    "connection_refused": ("连接被拒绝", "目标端点拒绝建立连接；端点可能是 Airtable 服务，也可能是当前使用的代理。",
                           "确认代理程序已启动、端口设置正确，并检查防火墙规则。", True),
    "network_unreachable": ("网络不可达", "系统报告目标网络或主机不可达，尚未建立可用连接。",
                            "检查网络、VPN、代理和路由设置。", True),
    "connection_reset": ("网络连接中断", "连接被重置、终止或关闭，未能完成网络请求。",
                         "检查网络或代理稳定性，稍后重试。", True),
    "network_permission": ("系统阻止网络连接", "系统拒绝了网络访问操作。",
                           "检查防火墙、安全软件及当前应用的网络访问权限。", False),
    "tls_certificate_expired": ("TLS 证书已过期", "证书校验器报告服务器或证书链中的证书已过期。",
                                "检查系统日期和时间，并检查服务端或 HTTPS 代理的证书有效期。", False),
    "tls_certificate_not_yet_valid": ("TLS 证书尚未生效", "证书校验器报告证书还未到生效时间。",
                                      "检查系统日期和时间，以及服务端或 HTTPS 代理的证书有效期。", False),
    "tls_hostname_mismatch": ("TLS 证书域名不匹配", "证书校验器报告证书中的域名与连接的主机名不匹配。",
                              "检查代理、DNS 和服务端证书配置，保持证书校验开启。", False),
    "tls_certificate_untrusted": ("TLS 证书不受信任", "证书校验器报告自签名证书，或无法建立可信的证书链。",
                                   "检查服务端证书链；如使用企业 HTTPS 代理，检查其受信任证书配置。", False),
    "tls_certificate_revoked": ("TLS 证书已被吊销", "证书校验器报告证书已经被吊销。",
                                "检查服务端或 HTTPS 代理的证书，并联系对应管理员更换证书。", False),
    "tls_certificate_invalid": ("TLS 证书校验失败", "无法验证连接证书；当前异常未提供可确认的具体证书原因。",
                                "检查系统时间、服务端证书链及 HTTPS 代理的受信任证书配置。", False),
    "tls_configuration_error": ("TLS 协议配置不兼容", "TLS 库报告协议版本或加密配置不可用或不兼容。",
                                 "检查代理的 HTTP/HTTPS 协议设置和 TLS 配置。", False),
    "tls_handshake": ("TLS 安全连接失败", "TLS 库报告安全连接错误，具体握手或传输原因尚未确认。",
                       "检查网络和 HTTPS 代理设置，确认代理能够正常建立 TLS 连接。", True),
    "proxy": ("代理连接失败", "HTTP 客户端报告代理连接或代理握手失败，尚未确认具体原因。",
              "检查代理是否运行、代理协议和端口是否正确，以及是否需要代理认证。", True),
    "proxy_authentication": ("代理需要身份认证", "HTTP 代理在建立 CONNECT 隧道时返回 407（需要代理身份认证）。",
                             "检查代理的用户名、密码和认证配置，确认当前应用获准使用该代理。", False),
    "connect_timeout": ("建立连接超时", "未能在规定时间内完成连接建立，可能涉及 TCP 或 TLS 阶段。",
                         "检查网络、代理和防火墙，稍后重试。", True),
    "read_timeout": ("读取响应超时", "等待服务端响应数据超过了本次请求的读取时限。",
                      "检查网络或代理稳定性；服务端繁忙时可稍后重试。", True),
    "write_timeout": ("发送请求超时", "发送请求数据超过了本次请求的写入时限。",
                       "检查上传网络或代理稳定性，稍后重试。", True),
    "pool_timeout": ("等待连接池超时", "未能在规定时间内取得空闲的 HTTP 连接。",
                      "等待正在执行的请求结束，减少同时发起的操作后重试。", True),
    "timeout": ("网络请求超时", "网络操作超过时限，当前异常未区分连接、读取或写入阶段。",
                 "检查网络或代理稳定性，稍后重试。", True),
    "read_error": ("读取网络响应失败", "HTTP 客户端在接收响应数据时遇到网络错误。",
                    "检查网络或代理稳定性，稍后重试。", True),
    "write_error": ("发送网络请求失败", "HTTP 客户端在发送请求数据时遇到网络错误。",
                     "检查网络或代理稳定性，稍后重试。", True),
    "local_protocol_error": ("本地请求协议错误", "HTTP 客户端报告本地请求不符合协议要求。",
                              "检查程序的请求构造和代理协议配置；重复请求通常无法解决此问题。", False),
    "unsupported_protocol": ("不支持的网络协议", "HTTP 客户端不支持当前请求使用的协议。",
                              "检查请求地址及代理协议配置。", False),
    "protocol_error": ("远端响应协议错误", "HTTP 客户端收到不完整或不符合协议要求的响应。",
                        "检查网络或代理稳定性，持续出现时检查代理和服务端。", True),
    "connect_error": ("无法建立网络连接", "HTTP 客户端报告 ConnectError，但底层原因未确认；无法据此确定是 DNS、代理还是 TLS 问题。",
                       "检查网络和代理连接；如问题持续，请保留本诊断报告供排查。", True),
    "network_error": ("网络请求失败", "发生网络异常，当前异常链中没有可确认的更具体原因。",
                       "检查网络和代理连接；如问题持续，请保留本诊断报告供排查。", True),
}

_TRANSPORT_NAMES = (
    "ConnectTimeout", "ReadTimeout", "WriteTimeout", "PoolTimeout", "TimeoutException",
    "ProxyError", "LocalProtocolError", "RemoteProtocolError", "UnsupportedProtocol",
    "ConnectError", "ReadError", "WriteError", "CloseError", "NetworkError",
    "ProtocolError", "RequestError", "TransportError",
)
_TRANSPORT_TYPES = {
    name: tuple(cls for module in (httpx, httpcore)
                if isinstance(cls := getattr(module, name, None), type))
    for name in _TRANSPORT_NAMES
}
_SAFE_TYPES = (
    (ssl.SSLCertVerificationError, "SSLCertVerificationError"),
    (ssl.SSLError, "SSLError"), (socket.gaierror, "gaierror"),
    (ConnectionRefusedError, "ConnectionRefusedError"),
    (ConnectionResetError, "ConnectionResetError"),
    (ConnectionAbortedError, "ConnectionAbortedError"),
    (BrokenPipeError, "BrokenPipeError"), (TimeoutError, "TimeoutError"),
    (PermissionError, "PermissionError"), (urllib.error.URLError, "URLError"),
    (OSError, "OSError"),
)


def _exception_chain(exc):
    """Follow one causal path so unrelated handled errors cannot change the diagnosis.

    Explicit causes take priority, followed by urllib's wrapped reason. Context is
    only a fallback, including suppressed context used by some transport wrappers.
    """
    current, seen, result = exc, set(), []
    while isinstance(current, BaseException) and id(current) not in seen and len(result) < 32:
        seen.add(id(current))
        result.append(current)
        if isinstance(current.__cause__, BaseException):
            current = current.__cause__
        elif isinstance(current, urllib.error.URLError) and isinstance(current.reason, BaseException):
            current = current.reason
        else:
            current = current.__context__
    return result


def _safe_type(exc):
    for name, classes in _TRANSPORT_TYPES.items():
        if isinstance(exc, classes):
            return name
    for cls, name in _SAFE_TYPES:
        if isinstance(exc, cls):
            return name
    return "UnknownError"


def _diagnosis(code, exc):
    title, detail, advice, retryable = _MESSAGES[code]
    return NetworkDiagnosis(code, title, detail, advice, retryable, _safe_type(exc))


def diagnose_network_error(exc: BaseException) -> NetworkDiagnosis:
    """Use structured types/codes only; never return raw messages, URLs or class names.

    ``retryable`` describes the failure, not whether replaying an operation is safe.
    Callers must separately prevent replay of a possibly completed non-idempotent write.
    """
    chain = _exception_chain(exc)
    for item in chain:
        if isinstance(item, ssl.SSLCertVerificationError):
            # OpenSSL X509 verification result codes, also used by Python's ssl.
            code = {9: "tls_certificate_not_yet_valid", 10: "tls_certificate_expired",
                    18: "tls_certificate_untrusted", 19: "tls_certificate_untrusted",
                    20: "tls_certificate_untrusted", 21: "tls_certificate_untrusted",
                    23: "tls_certificate_revoked", 62: "tls_hostname_mismatch"}.get(
                        getattr(item, "verify_code", None), "tls_certificate_invalid")
            return _diagnosis(code, item)
    for item in chain:
        if isinstance(item, ssl.SSLError):
            reason = getattr(item, "reason", None)
            if reason == "CERTIFICATE_VERIFY_FAILED":
                return _diagnosis("tls_certificate_invalid", item)
            if reason in ("WRONG_VERSION_NUMBER", "UNSUPPORTED_PROTOCOL", "NO_PROTOCOLS_AVAILABLE",
                          "NO_CIPHERS_AVAILABLE", "VERSION_TOO_LOW"):
                return _diagnosis("tls_configuration_error", item)
            return _diagnosis("tls_handshake", item)
    for name, code in (("LocalProtocolError", "local_protocol_error"),
                       ("UnsupportedProtocol", "unsupported_protocol")):
        for item in chain:
            if isinstance(item, _TRANSPORT_TYPES[name]):
                return _diagnosis(code, item)
    for item in chain:
        if isinstance(item, socket.gaierror):
            return _diagnosis("dns", item)
        if not isinstance(item, OSError):
            continue
        numbers = (item.errno, getattr(item, "winerror", None))
        for code, codes in (
            ("connection_refused", (errno.ECONNREFUSED, 10061)),
            ("network_unreachable", (errno.ENETUNREACH, errno.EHOSTUNREACH, errno.ENETDOWN, 10050, 10051, 10064, 10065)),
            ("connection_reset", (errno.ECONNRESET, errno.ECONNABORTED, errno.EPIPE, 10052, 10053, 10054, 10058)),
            ("network_permission", (errno.EACCES, errno.EPERM, 10013)),
        ):
            if any(number in codes for number in numbers if isinstance(number, int)):
                return _diagnosis(code, item)
        if isinstance(item, (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError, BrokenPipeError)):
            return _diagnosis("connection_refused" if isinstance(item, ConnectionRefusedError) else "connection_reset", item)
    for item in chain:
        # httpcore's CONNECT handler creates ProxyError("%d %s" % (status, reason)).
        # Recognize only its exact exception type and fixed leading status; the
        # server-controlled reason phrase must never be returned or searched.
        if (type(item) is getattr(httpcore, "ProxyError", None) and len(item.args) == 1 and
                isinstance(item.args[0], str) and item.args[0].startswith("407 ")):
            return _diagnosis("proxy_authentication", item)
    for name, code in (("ProxyError", "proxy"), ("ConnectTimeout", "connect_timeout"),
                       ("ReadTimeout", "read_timeout"), ("WriteTimeout", "write_timeout"),
                       ("PoolTimeout", "pool_timeout"), ("TimeoutException", "timeout")):
        for item in chain:
            if isinstance(item, _TRANSPORT_TYPES[name]):
                return _diagnosis(code, item)
    for item in chain:
        if isinstance(item, TimeoutError) or (isinstance(item, OSError) and
                (item.errno in (errno.ETIMEDOUT, 10060) or getattr(item, "winerror", None) == 10060)):
            return _diagnosis("timeout", item)
    for name, code in (("ReadError", "read_error"), ("WriteError", "write_error"),
                       ("RemoteProtocolError", "protocol_error"), ("ProtocolError", "protocol_error"),
                       ("ConnectError", "connect_error")):
        for item in chain:
            if isinstance(item, _TRANSPORT_TYPES[name]):
                return _diagnosis(code, item)
    return _diagnosis("network_error", exc)
