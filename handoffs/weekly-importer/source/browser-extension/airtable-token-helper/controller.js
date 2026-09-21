import { UserError, PRESETS, normalizeScopes, compareScopes, tokenInput, clientId, baseId, tableId,
  createAuthorization, authorizationCode, oauthCredential, exportConfig } from './core.js';

export function createController({ api, storage, identity, catalog, now = Date.now }) {
  let busy = false;
  const defaults = { mode: 'pat', clientId: '', selectedScopes: PRESETS.sync, baseId: '' };
  const preferences = async () => ({ ...defaults, ...(await storage.local.get('preferences')).preferences });
  const credential = async () => (await storage.session.get('credential')).credential;
  async function state() {
    const c = await credential();
    return { preferences: await preferences(), redirectUri: identity.getRedirectURL('airtable'), busy,
      credential: c ? { kind: c.kind, userId: c.userId || null, grantedScopes: c.grantedScopes ?? null,
        expiresAt: c.expiresAt || null, refreshExpiresAt: c.refreshExpiresAt || null,
        refreshPending: !!c.refreshPending, mask: '••••••••' + c.accessToken.slice(-6), scopeSource: c.scopeSource } : null };
  }
  async function storeGrant(data, id, requested) {
    const next = oauthCredential(data, id, now());
    if (!compareScopes(requested, next.grantedScopes).exact) throw new UserError('Airtable 返回的权限与申请不一致，未接受此令牌，请重新授权。');
    await storage.session.set({ credential: next });
    return next;
  }
  async function refresh(c, scopes) {
    if (!c || c.kind !== 'oauth') throw new UserError('只有 OAuth 令牌需要刷新；PAT 请在 Airtable 管理。');
    if (c.refreshPending) throw new UserError('上次刷新结果不确定。为避免重复使用刷新令牌，请重新授权。');
    if (c.refreshExpiresAt <= now()) throw new UserError('刷新令牌已过期，请重新授权。');
    if (scopes?.some(s => !c.grantedScopes.includes(s))) throw new UserError('扩大权限需要重新授权，不能通过刷新增加权限。');
    // Persist before sending: a restarted service worker must not replay a rotated token.
    await storage.session.set({ credential: { ...c, refreshPending: true } });
    const data = await api.refresh(c, scopes);
    return storeGrant(data, c.clientId, scopes || c.grantedScopes);
  }
  async function active() {
    let c = await credential();
    if (!c) throw new UserError('请先授权或验证 PAT。');
    if (c.refreshPending) throw new UserError('刷新结果不确定，请重新授权。');
    if (c.kind === 'oauth' && c.expiresAt <= now() + 60000) c = await refresh(c);
    return c;
  }
  async function authorize(p) {
    const scopes = normalizeScopes(p.selectedScopes, catalog);
    const { url, pending } = await createAuthorization(clientId(p.clientId), identity.getRedirectURL('airtable'), scopes, globalThis.crypto, now());
    await storage.session.set({ pendingAuthorization: pending });
    try {
      let callback;
      try { callback = await identity.launchWebAuthFlow({ url, interactive: true }); }
      catch { throw new UserError('授权窗口已关闭，或未收到回调。请核对首次配置中的 Client ID 和回调地址。'); }
      const stored = (await storage.session.get('pendingAuthorization')).pendingAuthorization;
      const code = authorizationCode(callback, stored, now());
      // An authorization code can only be consumed once, including failed exchanges.
      await storage.session.remove('pendingAuthorization');
      const data = await api.exchange(stored, code);
      await storeGrant(data, stored.clientId, scopes);
    } finally { await storage.session.remove('pendingAuthorization'); }
  }
  async function run(message) {
    const p = await preferences();
    switch (message.type) {
      case 'savePreferences': {
        const v = message.value || {};
        const selectedScopes = normalizeScopes(v.selectedScopes, catalog);
        const id = String(v.clientId || '').trim();
        if (id) clientId(id);
        const next = { mode: v.mode === 'oauth' ? 'oauth' : 'pat', clientId: id, selectedScopes,
          baseId: v.baseId ? baseId(v.baseId) : '' };
        await storage.local.set({ preferences: next });
        return state();
      }
      case 'importPat': {
        const token = tokenInput(message.token);
        const identityInfo = await api.whoami(token);
        await storage.session.set({ credential: { kind: 'pat', accessToken: token, userId: identityInfo.id,
          grantedScopes: identityInfo.scopes, scopeSource: identityInfo.scopes ? 'whoami' : 'not_returned' } });
        return state();
      }
      case 'authorize': await authorize(p); return state();
      case 'applyScopes': {
        const c = await credential();
        if (!c || c.kind !== 'oauth') throw new UserError('PAT 权限需在 Airtable 官方页面修改。插件中的选择只生成权限指引。');
        const scopes = normalizeScopes(p.selectedScopes, catalog);
        if (c.clientId !== p.clientId || scopes.some(s => !c.grantedScopes.includes(s))) await authorize(p);
        else if (!compareScopes(scopes, c.grantedScopes).exact) await refresh(c, scopes);
        return state();
      }
      case 'refresh': await refresh(await credential()); return state();
      case 'inspect': {
        const c = await active();
        const info = await api.whoami(c.accessToken);
        const next = { ...c, userId: info.id };
        if (Array.isArray(info.scopes)) { next.grantedScopes = info.scopes; next.scopeSource = 'whoami'; }
        // PATs do not expose their complete scopes in the documented whoami response.
        else if (c.kind === 'pat') { next.grantedScopes = null; next.scopeSource = 'not_returned'; }
        await storage.session.set({ credential: next });
        return state();
      }
      case 'listBases': return api.bases((await active()).accessToken);
      case 'getSchema': return api.schema((await active()).accessToken, baseId(message.baseId));
      case 'testRecords': return api.probe((await active()).accessToken, baseId(message.baseId), tableId(message.tableId));
      case 'export':
      case 'reveal': {
        const c = await active();
        if (c.kind === 'oauth' && !compareScopes(p.selectedScopes, c.grantedScopes).exact) throw new UserError('所选权限尚未应用，或实际授权已变化。请先应用权限或重新授权。');
        return message.type === 'reveal' ? { token: c.accessToken } : exportConfig(c, message.baseId, message.tables || {}, p.selectedScopes, now());
      }
      case 'forget': await storage.session.remove(['credential', 'pendingAuthorization']); return state();
      default: throw new UserError('不支持的操作。');
    }
  }
  return {
    state,
    async handle(message) {
      if (message?.type === 'state') return state();
      if (busy) throw new UserError('另一项授权或令牌操作正在进行，请稍候。');
      busy = true;
      try { return await run(message || {}); } finally { busy = false; }
    },
  };
}
