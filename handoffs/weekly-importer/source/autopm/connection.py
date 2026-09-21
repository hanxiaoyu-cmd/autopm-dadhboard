"""Read-only onboarding from a complete PAT to verified base/table identities."""
from .airtable import AirtableClient, AirtableError, resolve_tables


def discover_connection(token, base_id=None, *, on_event=None):
    token = token.strip()
    if not token.startswith("pat") or "." not in token or not token.split(".", 1)[1]:
        raise AirtableError("请粘贴完整 Token（pat…后面包含句点和密钥）。截图中的 Token ID 不能用于连接，无需单独填写。")
    with AirtableClient(token, timeout=15, max_retries=3, on_event=on_event) as client:
        bases = client.list_bases()
        if not bases:
            raise AirtableError("Token 已验证，但未找到可访问的数据库。请在 Airtable 的 Access 中授权目标数据库。")
        if base_id is None and len(bases) != 1:
            return {"bases": bases}
        selected = [b for b in bases if b["id"] == base_id] if base_id else bases
        if len(selected) != 1:
            raise AirtableError("所选数据库不在此 Token 的授权列表中，请重新检测。")
        base = selected[0]
        client.base_id = base["id"]
        tables = resolve_tables(client.get_schema())
        return {"bases": bases, "base": base, "tables": tables}
