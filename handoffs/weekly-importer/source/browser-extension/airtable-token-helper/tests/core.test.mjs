import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { PRESETS, normalizeScopes, compareScopes, tokenInput, baseId, tableId, createAuthorization, authorizationCode, oauthCredential, createApi, exportConfig } from '../core.js';
import { createController } from '../controller.js';

const catalog = JSON.parse(await readFile(new URL('../scopes.json', import.meta.url)));
const base = 'app12345678901234', table = 'tbl12345678901234', redirect = 'https://test.chromiumapp.org/airtable';
const grant = (scopes = PRESETS.sync, suffix = '') => ({ access_token: 'opaque-access' + suffix, refresh_token: 'opaque-refresh' + suffix,
  token_type: 'Bearer ', scope: scopes.join(' '), expires_in: 3600, refresh_expires_in: 5184000 });
function bucket() {
  const data = {};
  return { data, async get(k) { return structuredClone({ [k]: data[k] }); }, async set(v) { Object.assign(data, structuredClone(v)); },
    async remove(keys) { for (const k of Array.isArray(keys) ? keys : [keys]) delete data[k]; } };
}
function fixture(overrides = {}) {
  const storage = { local: bucket(), session: bucket() }, calls = [];
  const api = { whoami: async () => ({ id: 'usr-test', scopes: null }), bases: async () => [{ id: base }],
    schema: async () => [{ id: table, name: 'Projects' }], probe: async () => ({ ok: true, recordsReturned: 0 }),
    exchange: async (p, code) => { calls.push({ kind: 'exchange', p, code }); return grant(p.scopes); },
    refresh: async (c, scopes) => { calls.push({ kind: 'refresh', c, scopes }); return grant(scopes || c.grantedScopes, '-new'); }, ...overrides };
  const identity = { getRedirectURL: () => redirect, launchWebAuthFlow: async ({ url }) => {
    calls.push({ kind: 'authorize', url }); return redirect + '?code=once&state=' + new URL(url).searchParams.get('state'); } };
  const options = { storage, api, identity, catalog, now: () => 1000000 };
  const c = createController(options);
  const prefs = (scopes = PRESETS.sync) => c.handle({ type: 'savePreferences', value: { mode: 'oauth', clientId: 'integration-public', selectedScopes: scopes } });
  return { c, storage, api, identity, calls, prefs, options };
}

test('scope catalog is unique; presets request only documented scopes; unknown and empty rejected', () => {
  assert.equal(catalog.length, 25); assert.equal(new Set(catalog.map(s => s.id)).size, 25);
  for (const scopes of Object.values(PRESETS)) assert.deepEqual(normalizeScopes([...scopes, scopes[0]], catalog), [...scopes].sort());
  assert.throws(() => normalizeScopes([], catalog)); assert.throws(() => normalizeScopes(['data.records:delete'], catalog));
  assert.equal(compareScopes(PRESETS.sync, null).known, false);
  assert.equal(compareScopes(PRESETS.sync, []).known, true);
  assert.deepEqual(compareScopes(['a'], ['b']).missing, ['a']);
});
test('token input preserves opaque strings and rejects ID confusion', () => {
  assert.equal(tokenInput(' Bearer opaque-secret '), 'opaque-secret');
  for (const v of ['', 'has space', 'pat12345678901234', base, table, 'apat-typo']) assert.throws(() => tokenInput(v));
});
test('resource IDs and official Base links validated before URL construction', () => {
  assert.equal(baseId(`https://airtable.com/${base}/${table}?x=1`), base);
  for (const v of ['pat12345678901234', `https://evil.test/${base}`, `${base}/../other`]) assert.throws(() => baseId(v));
  assert.equal(tableId(table), table); assert.throws(() => tableId(base));
});
test('PKCE uses S256 and random state; exact requested scopes in authorization URL', async () => {
  const { url, pending } = await createAuthorization('public', redirect, PRESETS.sync);
  assert.equal(pending.verifier.length, 64); assert.equal(pending.state.length, 43);
  assert.equal(pending.challenge, createHash('sha256').update(pending.verifier).digest('base64url'));
  assert.equal(new URL(url).searchParams.get('scope'), PRESETS.sync.join(' '));
  assert.equal(new URL(url).searchParams.get('code_challenge_method'), 'S256');
  assert.notEqual((await createAuthorization('public', redirect, PRESETS.sync)).pending.state, pending.state);
});
test('callback rejects state, origin, path, duplicate values, expiry and OAuth denial', async () => {
  const { pending: p } = await createAuthorization('public', redirect, PRESETS.sync, crypto, 1000);
  const good = `${redirect}?state=${p.state}&code=abc`;
  assert.equal(authorizationCode(good, p, 1001), 'abc');
  for (const bad of [good.replace(p.state, 'wrong'), good.replace('test.chromiumapp.org', 'evil.test'), good.replace('/airtable?', '/other?'), good + '&code=twice', good + '&state=twice', good + '#fragment', good + '&error=denied', good + '&code_challenge=bad', good + '&code_challenge_method=plain']) assert.throws(() => authorizationCode(bad, p, 1001));
  assert.throws(() => authorizationCode(good, p, 601001)); assert.throws(() => authorizationCode(good, p, 999));
});
test('OAuth tokens are opaque; expiry, refresh, type and scopes required', () => {
  const c = oauthCredential(grant(), 'public', 1000);
  assert.equal(c.expiresAt, 3601000); assert.equal(c.refreshToken, 'opaque-refresh');
  for (const patch of [{ refresh_token: '' }, { expires_in: -1 }, { refresh_expires_in: null }, { token_type: 'basic' }, { scope: null }]) assert.throws(() => oauthCredential({ ...grant(), ...patch }, 'public'));
});
test('PAT whoami without scopes remains unknown; malformed scopes rejected', async () => {
  const api = createApi(async () => Response.json({ id: 'usr' })); assert.equal((await api.whoami('secret')).scopes, null);
  await assert.rejects(createApi(async () => Response.json({ id: 'usr', scopes: [1] })).whoami('secret'));
});
test('API uses fixed official origins; no credentials in URL; redirects blocked; PKCE POST has no Basic header', async () => {
  const requests = []; const api = createApi(async (url, opts) => { requests.push({ url, opts }); return Response.json({ id: 'usr' }); });
  await api.whoami('test-secret'); await api.exchange({ clientId: 'public', redirectUri: redirect, verifier: 'verifier' }, 'one-code');
  const [read, post] = requests;
  assert.equal(new URL(read.url).origin, 'https://api.airtable.com'); assert.ok(!read.url.includes('test-secret'));
  assert.equal(read.opts.headers.Authorization, 'Bearer test-secret'); assert.equal(read.opts.credentials, 'omit'); assert.equal(read.opts.redirect, 'error');
  assert.equal(new URL(post.url).origin, 'https://airtable.com'); assert.equal(post.opts.headers.Authorization, undefined);
  assert.equal(new URLSearchParams(post.opts.body).get('code_verifier'), 'verifier');
});
test('Base pagination gathers all pages and repeated offsets fail', async () => {
  let n = 0; const api = createApi(async (url) => {
    assert.equal(new URL(url).searchParams.has('pageSize'), false);
    assert.equal(new URL(url).searchParams.get('offset'), n === 0 ? null : 'next');
    return Response.json(++n === 1 ? { bases: [{ id: 'first' }], offset: 'next' } : { bases: [{ id: 'second' }] });
  });
  assert.equal((await api.bases('secret')).length, 2);
  await assert.rejects(createApi(async () => Response.json({ bases: [], offset: 'loop' })).bases('secret'), /分页/);
});
for (const status of [401, 403, 404, 429, 500]) test(`HTTP ${status} errors sanitized and no automatic retry`, async () => {
  let n = 0; const api = createApi(async () => { n++; return Response.json({ error: { message: 'secret-should-not-leak' } }, { status }); });
  await assert.rejects(api.whoami('secret'), e => !e.message.includes('secret-should-not-leak'));
  assert.equal(n, 1);
});
test('network exception details not exposed and token exchange not retried', async () => {
  let n = 0; const api = createApi(async () => { n++; throw new Error('raw-credential'); });
  await assert.rejects(api.exchange({ clientId: 'public', redirectUri: redirect, verifier: 'v' }, 'c'), e => !e.message.includes('raw-credential'));
  assert.equal(n, 1);
});
test('record probe discards data and empty table is success', async () => {
  for (const records of [[], [{ id: 'rec', fields: { sensitive: 'value' } }]]) {
    const result = await createApi(async () => Response.json({ records })).probe('secret', base, table);
    assert.deepEqual(result, { ok: true, recordsReturned: records.length });
  }
});
test('PAT is kept in session only; state masks credentials; unverified grants remain unverified in export', async () => {
  const f = fixture(); await f.prefs(); await f.c.handle({ type: 'importPat', token: 'pat-fixture-secret' });
  const state = await f.c.state(); assert.equal(state.credential.grantedScopes, null);
  assert.ok(!JSON.stringify(state).includes('pat-fixture-secret')); assert.ok(!JSON.stringify(f.storage.local.data).includes('pat-fixture-secret'));
  const config = await f.c.handle({ type: 'export', baseId: base, tables: { projects: table } });
  assert.equal(config.authorization_info.scopes_verified, false); assert.equal(config.airtable_credentials.projects_table_id, table);
  await f.c.handle({ type: 'forget' }); assert.equal((await f.c.state()).credential, null);
});
test('failed PAT replacement preserves previously verified credential', async () => {
  const f = fixture(); await f.c.handle({ type: 'importPat', token: 'first-secret' });
  f.api.whoami = async () => { throw new Error('denied'); };
  await assert.rejects(f.c.handle({ type: 'importPat', token: 'second-secret' }));
  assert.equal(f.storage.session.data.credential.accessToken, 'first-secret');
});
test('authorization exchange is once and pending code removed before exchange', async () => {
  const f = fixture(); await f.prefs(); f.api.exchange = async () => {
    assert.equal(f.storage.session.data.pendingAuthorization, undefined); throw new Error('network'); };
  await assert.rejects(f.c.handle({ type: 'authorize' })); assert.equal(f.storage.session.data.pendingAuthorization, undefined);
  assert.equal(f.storage.session.data.credential, undefined);
});
test('authorization rejects service returned extra scopes', async () => {
  const f = fixture({ exchange: async () => grant([...PRESETS.sync, 'schema.bases:write']) }); await f.prefs();
  await assert.rejects(f.c.handle({ type: 'authorize' }), /不一致/); assert.equal(f.storage.session.data.credential, undefined);
});
test('scope selection does not silently change grant; un-applied selection blocks OAuth export', async () => {
  const f = fixture(); await f.prefs(); await f.c.handle({ type: 'authorize' }); await f.prefs(PRESETS.read);
  assert.equal(f.storage.session.data.credential.grantedScopes.length, 3);
  await assert.rejects(f.c.handle({ type: 'export', baseId: base }), /尚未应用/);
  await assert.rejects(f.c.handle({ type: 'reveal' }), /尚未应用/);
});
test('narrowing sends exact subset in refresh; rotated tokens saved; export excludes refresh token', async () => {
  const f = fixture(); await f.prefs(); await f.c.handle({ type: 'authorize' }); await f.prefs(PRESETS.read);
  await f.c.handle({ type: 'applyScopes' }); const last = f.calls.at(-1);
  assert.equal(last.kind, 'refresh'); assert.deepEqual(last.scopes, [...PRESETS.read].sort());
  assert.equal(f.storage.session.data.credential.accessToken, 'opaque-access-new');
  const config = await f.c.handle({ type: 'export', baseId: base });
  assert.ok(!JSON.stringify(config).includes('opaque-refresh')); assert.equal(config.authorization_info.scopes_verified, true);
});
test('increasing scope opens new authorization rather than refreshing broader scope', async () => {
  const f = fixture(); await f.prefs(PRESETS.read); await f.c.handle({ type: 'authorize' }); await f.prefs(PRESETS.structure);
  await f.c.handle({ type: 'applyScopes' }); assert.equal(f.calls.filter(c => c.kind === 'authorize').length, 2);
  assert.equal(f.calls.filter(c => c.kind === 'refresh').length, 0);
});
test('failed refresh blocks retries including after worker recreation', async () => {
  let n = 0; const f = fixture({ refresh: async () => { n++; throw new Error('network'); } });
  await f.prefs(); await f.c.handle({ type: 'authorize' });
  await assert.rejects(f.c.handle({ type: 'refresh' })); assert.equal(f.storage.session.data.credential.refreshPending, true);
  const restarted = createController(f.options);
  await assert.rejects(restarted.handle({ type: 'refresh' }), /不确定/);
  await assert.rejects(restarted.handle({ type: 'listBases' }), /不确定/); assert.equal(n, 1);
});
test('refresh in progress cannot run concurrently; near expiry refreshes once', async () => {
  const f = fixture(); await f.prefs(); await f.c.handle({ type: 'authorize' });
  let release, entered; const started = new Promise(r => entered = r);
  f.api.refresh = async () => { entered(); await new Promise(r => release = r); return grant(PRESETS.sync, '-rotated'); };
  f.storage.session.data.credential.expiresAt = 1000001;
  const first = f.c.handle({ type: 'listBases' }); await started;
  await assert.rejects(f.c.handle({ type: 'refresh' }), /正在进行/); release(); await first;
  assert.equal(f.storage.session.data.credential.accessToken, 'opaque-access-rotated');
});
test('expired refresh token does not send request; expired access token cannot export directly', async () => {
  const f = fixture(); await f.prefs(); await f.c.handle({ type: 'authorize' }); f.storage.session.data.credential.refreshExpiresAt = 1;
  await assert.rejects(f.c.handle({ type: 'refresh' }), /已过期/);
  assert.equal(f.calls.filter(c => c.kind === 'refresh').length, 0);
  assert.throws(() => exportConfig({ ...oauthCredential(grant(), 'public'), expiresAt: 1 }, base, {}, PRESETS.sync), /已过期/);
});
test('PAT scope change never calls OAuth or claims to remotely modify PAT', async () => {
  const f = fixture(); await f.c.handle({ type: 'importPat', token: 'fixture-pat' });
  await assert.rejects(f.c.handle({ type: 'applyScopes' }), /官方页面/); assert.equal(f.calls.length, 0);
});
