export const API_ORIGIN = 'https://api.airtable.com';
export const AUTH_ORIGIN = 'https://airtable.com';
export const PRESETS = {
  read: ['data.records:read', 'schema.bases:read'],
  sync: ['data.records:read', 'data.records:write', 'schema.bases:read'],
  structure: ['data.records:read', 'data.records:write', 'schema.bases:read', 'schema.bases:write'],
};

export class UserError extends Error {}

export function normalizeScopes(scopes, catalog) {
  if (!Array.isArray(scopes) || !scopes.length) throw new UserError('请至少选择一项权限。');
  const allowed = new Set(catalog.map(s => s.id));
  if (scopes.some(s => typeof s !== 'string' || !allowed.has(s))) throw new UserError('包含未支持的权限，请重新选择。');
  return [...new Set(scopes)].sort();
}

export function compareScopes(requested, granted) {
  if (!Array.isArray(granted)) return { known: false, exact: false, missing: [], extra: [] };
  const a = new Set(requested), b = new Set(granted);
  const missing = [...a].filter(s => !b.has(s));
  const extra = [...b].filter(s => !a.has(s));
  return { known: true, exact: !missing.length && !extra.length, missing, extra };
}

export function tokenInput(value) {
  const token = String(value || '').trim().replace(/^Bearer\s+/i, '');
  if (!token || token.length > 16384 || /\s/.test(token)) throw new UserError('请输入完整 Token，不能包含空格或换行。');
  if (/^(?:pat|app|tbl)[a-zA-Z0-9]{14}$/.test(token)) throw new UserError('这是 Token ID、Base ID 或表 ID；需要完整的 Token 密钥。');
  if (token.startsWith('apat')) throw new UserError('Token 开头疑似多了一个 a，请核对 Airtable 显示的原始密钥。');
  return token;
}

export function baseId(value) {
  let result = String(value || '').trim();
  if (result.startsWith('https://')) {
    let url;
    try { url = new URL(result); } catch { throw new UserError('Base 链接无效。'); }
    if (url.hostname !== 'airtable.com') throw new UserError('请输入 Airtable 的 Base 链接。');
    result = url.pathname.split('/').find(p => /^app[a-zA-Z0-9]{14}$/.test(p)) || '';
  }
  if (!/^app[a-zA-Z0-9]{14}$/.test(result)) throw new UserError('Base ID 应为 app 开头的 17 位标识，不能填写 pat 开头的 Token ID。');
  return result;
}

export function tableId(value) {
  if (!/^tbl[a-zA-Z0-9]{14}$/.test(String(value))) throw new UserError('表 ID 应为 tbl 开头的 17 位标识。');
  return value;
}

export function clientId(value) {
  const id = String(value || '').trim();
  if (!id || id.length > 200 || /\s/.test(id)) throw new UserError('请先完成首次配置，填写 OAuth Client ID。');
  return id;
}

function base64url(bytes) {
  return btoa(String.fromCharCode(...bytes)).replaceAll('+', '-').replaceAll('/', '_').replace(/=+$/, '');
}
export async function createAuthorization(id, redirectUri, scopes, cryptoImpl = globalThis.crypto, now = Date.now()) {
  const verifier = base64url(cryptoImpl.getRandomValues(new Uint8Array(48)));
  const state = base64url(cryptoImpl.getRandomValues(new Uint8Array(32)));
  const challenge = base64url(new Uint8Array(await cryptoImpl.subtle.digest('SHA-256', new TextEncoder().encode(verifier))));
  const pending = { clientId: clientId(id), redirectUri, scopes, verifier, state, challenge, createdAt: now };
  const url = new URL('/oauth2/v1/authorize', AUTH_ORIGIN);
  for (const [k, v] of Object.entries({ client_id: pending.clientId, redirect_uri: redirectUri, response_type: 'code',
    scope: scopes.join(' '), state, code_challenge: challenge, code_challenge_method: 'S256' })) url.searchParams.set(k, v);
  return { url: url.href, pending };
}

export function authorizationCode(callback, pending, now = Date.now()) {
  if (!pending || now - pending.createdAt > 10 * 60 * 1000 || now < pending.createdAt) throw new UserError('授权已过期，请重新授权。');
  let url;
  try { url = new URL(callback); } catch { throw new UserError('授权回调无效，请重试。'); }
  const target = new URL(pending.redirectUri);
  if (url.origin !== target.origin || url.pathname !== target.pathname || url.hash || url.username || url.password) throw new UserError('授权回调地址不匹配。');
  for (const k of ['state', 'code', 'error', 'code_challenge', 'code_challenge_method']) {
    if (url.searchParams.getAll(k).length > 1) throw new UserError('授权回调包含重复参数。');
  }
  if (url.searchParams.get('state') !== pending.state) throw new UserError('授权状态校验失败，请重新授权。');
  if (url.searchParams.has('error')) throw new UserError('Airtable 未完成授权。请检查权限、集成配置，或重新发起授权。');
  if (url.searchParams.has('code_challenge') && url.searchParams.get('code_challenge') !== pending.challenge) throw new UserError('授权校验码不匹配。');
  if (url.searchParams.has('code_challenge_method') && url.searchParams.get('code_challenge_method') !== 'S256') throw new UserError('授权校验方式不匹配。');
  const code = url.searchParams.get('code');
  if (!code || code.length > 8192) throw new UserError('Airtable 没有返回有效授权码。');
  return code;
}

export function oauthCredential(data, id, now = Date.now()) {
  if (!data || typeof data.access_token !== 'string' || !data.access_token || typeof data.refresh_token !== 'string' || !data.refresh_token ||
    typeof data.scope !== 'string' || !Number.isFinite(data.expires_in) || data.expires_in <= 0 ||
    !Number.isFinite(data.refresh_expires_in) || data.refresh_expires_in <= 0 || String(data.token_type).trim().toLowerCase() !== 'bearer') {
    throw new UserError('Airtable 的令牌响应不完整，请重新授权。');
  }
  return { kind: 'oauth', accessToken: data.access_token, refreshToken: data.refresh_token, clientId: id,
    expiresAt: now + data.expires_in * 1000, refreshExpiresAt: now + data.refresh_expires_in * 1000,
    grantedScopes: [...new Set(data.scope.split(/\s+/).filter(Boolean))].sort(), scopeSource: 'oauth_response', refreshPending: false };
}

function statusError(status) {
  return ({ 401: '认证失败：Token 无效、已撤销或已过期。', 403: '访问被拒绝：请核对 Token 权限、授权的 Base，以及账户在该 Base 的权限。',
    404: '目标不存在或不可访问，请核对 Base ID / 表 ID。', 429: 'Airtable 请求过于频繁，请稍后重试。' })[status] || `Airtable 请求失败（HTTP ${status}）。`;
}

export function createApi(fetchImpl = globalThis.fetch) {
  async function request(url, options) {
    let response;
    try {
      response = await fetchImpl(url, { ...options, credentials: 'omit', redirect: 'error', cache: 'no-store', signal: AbortSignal.timeout(25000) });
    } catch { throw new UserError('连接 Airtable 失败或超时，请检查网络。授权码或刷新请求不会自动重发。'); }
    let data;
    try { data = await response.json(); } catch { throw new UserError(`Airtable 返回了无法读取的响应（HTTP ${response.status}）。`); }
    if (!response.ok) {
      const oauthErrors = { invalid_client: 'OAuth Client ID 不正确，或集成已设置 Client Secret。本插件需要不含 Client Secret 的公开客户端集成。',
        invalid_grant: '授权码或刷新令牌已失效，请重新授权。', invalid_scope: '请求的权限未在 OAuth 集成中启用，请检查首次配置。' };
      throw new UserError(typeof data?.error === 'string' && Object.hasOwn(oauthErrors, data.error) ? oauthErrors[data.error] : statusError(response.status));
    }
    return data;
  }
  const get = (token, path) => request(API_ORIGIN + path, { headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' } });
  const exchange = body => request(AUTH_ORIGIN + '/oauth2/v1/token', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(body).toString() });
  return {
    async whoami(token) {
      const data = await get(token, '/v0/meta/whoami');
      if (!data || typeof data.id !== 'string' || (data.scopes !== undefined && (!Array.isArray(data.scopes) || data.scopes.some(s => typeof s !== 'string')))) throw new UserError('Airtable 未返回有效用户身份或权限信息。');
      return { id: data.id, scopes: Array.isArray(data.scopes) ? [...new Set(data.scopes)].sort() : null };
    },
    async bases(token) {
      const result = [], seen = new Set(); let offset;
      do {
        const query = new URLSearchParams();
        if (offset) query.set('offset', offset);
        const data = await get(token, '/v0/meta/bases' + (query.size ? '?' + query : ''));
        if (!Array.isArray(data.bases)) throw new UserError('Airtable 未返回 Base 列表。');
        result.push(...data.bases.map(b => ({ id: b.id, name: b.name, permissionLevel: b.permissionLevel })));
        offset = data.offset;
        if (offset && (seen.has(offset) || seen.size > 1000)) throw new UserError('Base 列表分页异常，请稍后重试。');
        if (offset) seen.add(offset);
      } while (offset);
      return result;
    },
    async schema(token, id) {
      const data = await get(token, `/v0/meta/bases/${baseId(id)}/tables`);
      if (!Array.isArray(data.tables)) throw new UserError('Airtable 未返回表结构。');
      return data.tables.map(t => ({ id: t.id, name: t.name }));
    },
    async probe(token, base, table) {
      const data = await get(token, `/v0/${baseId(base)}/${tableId(table)}?pageSize=1`);
      if (!Array.isArray(data.records)) throw new UserError('Airtable 未返回记录列表。');
      return { ok: true, recordsReturned: data.records.length };
    },
    exchange(pending, code) {
      return exchange({ grant_type: 'authorization_code', code, client_id: pending.clientId, redirect_uri: pending.redirectUri, code_verifier: pending.verifier });
    },
    refresh(credential, scopes) {
      const body = { grant_type: 'refresh_token', client_id: credential.clientId, refresh_token: credential.refreshToken };
      if (scopes) body.scope = scopes.join(' ');
      return exchange(body);
    },
  };
}

export function exportConfig(credential, base, tables, requestedScopes, now = Date.now()) {
  if (!credential?.accessToken) throw new UserError('请先完成授权或验证 PAT。');
  if (credential.kind === 'oauth' && credential.expiresAt <= now) throw new UserError('访问令牌已过期，请先刷新。');
  const credentials = { token: credential.accessToken, base_id: baseId(base) };
  for (const kind of ['projects', 'tasks', 'issues']) credentials[kind + '_table_id'] = tables[kind] ? tableId(tables[kind]) : '';
  return { airtable_credentials: credentials, authorization_info: { type: credential.kind,
    requested_scopes: requestedScopes, granted_scopes: credential.grantedScopes ?? null,
    scopes_verified: Array.isArray(credential.grantedScopes), expires_at: credential.expiresAt ? new Date(credential.expiresAt).toISOString() : null,
    note: credential.kind === 'oauth' ? '临时访问令牌。AutoPM 当前不会自动刷新；过期后请在插件重新导出。' : 'PAT 的完整 scopes 可能无法通过公开 API 查询；选择的权限不等于实际授权。' } };
}
