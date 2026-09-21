import { PRESETS, compareScopes, baseId } from './core.js';
const $ = id => document.getElementById(id);
let catalog = [], current = null, running = false, revealTimer;
const selected = () => [...document.querySelectorAll('[data-scope]:checked')].map(e => e.dataset.scope).sort();
const mode = () => document.querySelector('[name=mode]:checked').value;
const tables = () => Object.fromEntries(['projects', 'tasks', 'issues'].map(k => [k, $(k + 'Table').value.trim()]));
function notice(text, error = false) { $('notice').textContent = text; $('notice').classList.toggle('error', error); $('notice').hidden = false; }
async function send(type, extra = {}) {
  const response = await chrome.runtime.sendMessage({ type, ...extra });
  if (!response?.ok) throw new Error(response?.error || '插件后台暂不可用，请重新打开插件。');
  return response.data;
}
function scopeSummary() {
  $('scopeCount').textContent = `已选择 ${selected().length} 项权限`;
  $('scopeList').textContent = selected().join('\n') || '尚未选择权限';
  document.querySelectorAll('[data-preset]').forEach(b => b.classList.toggle('selected', JSON.stringify([...PRESETS[b.dataset.preset]].sort()) === JSON.stringify(selected())));
  if (current) renderCredential();
}
function renderMode() { $('patPanel').hidden = mode() !== 'pat'; $('oauthPanel').hidden = mode() !== 'oauth'; }
function renderCredential() {
  const c = current?.credential;
  $('credentialPanel').hidden = !c;
  $('connectionBadge').textContent = c ? '已获取 Token' : '尚未连接';
  $('connectionBadge').classList.toggle('connected', !!c);
  if (!c) { $('savedToken').value = ''; return; }
  $('credentialKind').textContent = c.kind === 'oauth' ? 'OAuth 访问令牌' : 'Personal Access Token';
  $('savedToken').type = 'password'; $('savedToken').value = c.mask; $('showToken').textContent = '显示';
  $('oauthActions').hidden = c.kind !== 'oauth';
  const comparison = compareScopes(selected(), c.grantedScopes);
  $('credentialStatus').textContent = c.refreshPending ? '刷新结果不确定，请重新授权。' : !comparison.known ? '身份验证通过；Airtable 未返回此 PAT 的完整 scopes，不能据此确认写入权限。' : comparison.exact ? 'Airtable 返回的 scopes 与所选权限完全一致。' : `实际授权与当前选择不同。缺少 ${comparison.missing.length} 项，多出 ${comparison.extra.length} 项。${c.kind === 'oauth' ? '请应用所选权限。' : '请在官方页面修改 PAT。'}`;
  $('grantedScopes').textContent = comparison.known ? c.grantedScopes.join('\n') || '空权限集合' : '未知：此 PAT 的完整 scopes 未通过公开接口返回。读取成功仅证明对应读取请求可用。';
  $('expiry').textContent = c.kind === 'oauth' ? `访问令牌有效至 ${new Date(c.expiresAt).toLocaleString()}。插件使用时会按需刷新；已导出的配置不会随之更新。` : '本机仅在当前浏览器会话保存 Token，关闭浏览器后需重新粘贴。';
  $('exportHint').textContent = c.kind === 'oauth' ? '导出的是临时 OAuth 连接。AutoPM 当前不会自动刷新；到期后需重新导出。JSON 不包含刷新令牌。' : 'JSON 包含完整 PAT。AutoPM：连接设置 → 导入已有 sync_config.json → 保存连接设置。';
}
async function savePreferences() {
  return send('savePreferences', { value: { mode: mode(), clientId: $('clientId').value,
    selectedScopes: selected(), baseId: $('baseId').value ? baseId($('baseId').value) : '' } });
}
async function action(fn, persist = true) {
  if (running) return;
  running = true; document.body.classList.add('working');
  document.querySelectorAll('button,input,select').forEach(e => e.disabled = true);
  try { if (persist) await savePreferences(); await fn(); }
  catch (error) { notice(error.message || '操作失败，请重试。', true); }
  finally {
    try { current = await send('state'); renderCredential(); } catch { /* Keep the actionable error already shown. */ }
    running = false; document.body.classList.remove('working');
    document.querySelectorAll('button,input,select').forEach(e => e.disabled = false);
  }
}
async function copy(text) { await navigator.clipboard.writeText(text); notice('已复制。'); }
function download(value) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2)], { type: 'application/json' }));
  const a = document.createElement('a'); a.href = url; a.download = 'sync_config.json'; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function addScopes() {
  for (const item of catalog) {
    const label = document.createElement('label'); label.className = 'scope'; label.title = item.description;
    const box = document.createElement('input'); box.type = 'checkbox'; box.dataset.scope = item.id; box.checked = current.preferences.selectedScopes.includes(item.id);
    const text = document.createElement('span'), name = document.createElement('strong'), code = document.createElement('code');
    name.textContent = item.label; code.textContent = item.id; text.append(name, code); label.append(box, text);
    $(item.basic ? 'scopes' : 'enterpriseScopes').append(label); box.addEventListener('change', scopeSummary);
  }
}
async function init() {
  if (!globalThis.chrome?.runtime?.id) throw new Error('请先在 Chrome / Edge 中加载此扩展，再点击扩展图标打开。');
  catalog = await (await fetch(chrome.runtime.getURL('scopes.json'))).json(); current = await send('state');
  $('clientId').value = current.preferences.clientId; $('baseId').value = current.preferences.baseId; $('redirectUri').value = current.redirectUri;
  document.querySelector(`[name=mode][value=${current.preferences.mode}]`).checked = true;
  addScopes(); renderMode(); scopeSummary();
  document.querySelectorAll('[name=mode]').forEach(e => e.addEventListener('change', renderMode));
  document.querySelectorAll('[data-preset]').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('[data-scope]').forEach(e => e.checked = PRESETS[b.dataset.preset].includes(e.dataset.scope)); scopeSummary();
  }));
  $('copyScopes').onclick = () => action(() => copy(selected().join('\n')));
  $('copyRedirect').onclick = () => action(() => copy(current.redirectUri), false);
  $('importPat').onclick = () => action(async () => { await send('importPat', { token: $('patToken').value }); $('patToken').value = ''; notice('PAT 身份验证成功。接下来获取 Base 列表，验证目标连接。'); });
  $('authorize').onclick = () => action(async () => { await send('authorize'); notice('OAuth 授权已完成，实际 scopes 已核对。请获取 Base 列表。'); });
  $('applyScopes').onclick = () => action(async () => { await send('applyScopes'); notice('OAuth 权限已应用并核对。请重新导出需要使用的连接配置。'); });
  $('refreshToken').onclick = () => action(async () => { await send('refresh'); notice('Token 已刷新。之前导出的 OAuth 配置不会自动更新，请重新导出。'); });
  $('inspect').onclick = () => action(async () => { await send('inspect'); notice('已重新读取 Airtable 身份与可查询的权限信息。'); });
  $('forget').onclick = () => action(async () => { await send('forget'); clearTimeout(revealTimer); $('patToken').value = ''; $('savedToken').value = ''; $('bases').replaceChildren(new Option('先获取 Base 列表', '')); notice('本机令牌已清除。Airtable 上的授权仍由官方管理页控制。'); }, false);
  $('copyToken').onclick = () => action(async () => copy((await send('reveal')).token));
  $('showToken').onclick = async () => {
    if ($('savedToken').type === 'text') { renderCredential(); return; }
    try {
      await savePreferences(); const { token } = await send('reveal');
      $('savedToken').value = token; $('savedToken').type = 'text'; $('showToken').textContent = '隐藏';
      clearTimeout(revealTimer); revealTimer = setTimeout(renderCredential, 30000);
    } catch (e) { notice(e.message, true); }
  };
  $('loadBases').onclick = () => action(async () => {
    const rows = await send('listBases'); $('bases').replaceChildren(new Option('请选择一个已授权 Base', ''));
    for (const row of rows) $('bases').add(new Option(`${row.name} · ${row.id} · ${row.permissionLevel}`, row.id));
    $('bases').value = $('baseId').value;
    notice(`读取到 ${rows.length} 个可访问 Base。此列表只包含当前授权可见的资源。`);
  });
  const clearTables = () => { for (const k of ['projects', 'tasks', 'issues']) $(k + 'Table').value = ''; $('tableOptions').replaceChildren(); $('baseStatus').textContent = 'Base 已变更，请重新读取表结构或填写表 ID。'; };
  $('baseId').addEventListener('input', () => { clearTables(); $('bases').value = ''; });
  $('bases').onchange = () => { if ($('bases').value) { $('baseId').value = $('bases').value; clearTables(); } };
  $('loadSchema').onclick = () => action(async () => {
    const rows = await send('getSchema', { baseId: $('baseId').value }); $('tableOptions').replaceChildren();
    for (const row of rows) { const option = document.createElement('option'); option.value = row.id; option.label = row.name; $('tableOptions').append(option); }
    for (const kind of ['projects', 'tasks', 'issues']) {
      const hits = rows.filter(r => r.name.normalize('NFKC').replace(/\s+/g, '').toLowerCase() === kind);
      $(kind + 'Table').value = hits.length === 1 ? hits[0].id : '';
    }
    $('baseStatus').textContent = `已读取 ${rows.length} 张表。只有名称唯一匹配的表会自动填入，其余请从列表选择。`;
    notice('Base 与表结构读取成功。还可以验证 Projects 记录读取。');
  });
  $('testRecords').onclick = () => action(async () => {
    const result = await send('testRecords', { baseId: $('baseId').value, tableId: $('projectsTable').value.trim() });
    notice(`记录读取成功（返回 ${result.recordsReturned} 条）。未执行新增、修改或删除操作；写入权限不能仅靠读取成功判断。`);
  });
  $('export').onclick = () => action(async () => { const value = await send('export', { baseId: $('baseId').value, tables: tables() }); download(value); notice('已导出 sync_config.json，文件包含完整 Token。'); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) renderCredential(); });
}
init().catch(error => notice(error.message, true));
