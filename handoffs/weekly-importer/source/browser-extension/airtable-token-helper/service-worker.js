import { createApi, UserError } from './core.js';
import { createController } from './controller.js';

const ready = (async () => {
  await chrome.storage.session.setAccessLevel({ accessLevel: 'TRUSTED_CONTEXTS' });
  const catalog = await (await fetch(chrome.runtime.getURL('scopes.json'))).json();
  return createController({ api: createApi(), storage: chrome.storage, identity: chrome.identity, catalog });
})();

chrome.action.onClicked.addListener(() => chrome.tabs.create({ url: chrome.runtime.getURL('index.html') }));
chrome.runtime.onMessage.addListener((message, sender, reply) => {
  if (sender.id !== chrome.runtime.id || sender.url !== chrome.runtime.getURL('index.html')) {
    reply({ ok: false, error: '仅允许插件自身的页面发起请求。' }); return false;
  }
  ready.then(c => c.handle(message)).then(data => reply({ ok: true, data })).catch(error => {
    // Never forward a network response body, token, callback URL, or stack trace.
    reply({ ok: false, error: error instanceof UserError ? error.message : '操作未完成，请重试；授权或刷新失败时请重新授权。' });
  });
  return true;
});
