# AutoPM · Airtable 授权助手

Chrome / Edge 浏览器扩展，版本 1.0.0。独立于 AutoPM 桌面程序运行，不需要安装 Node 或 Python。

## 安装

1. 使用本源码包中的 `browser-extension/airtable-token-helper` 目录。
2. Chrome 打开 `chrome://extensions`；Edge 打开 `edge://extensions`。
3. 开启“开发者模式”，点击“加载已解压的扩展程序”，选择包含 `manifest.json` 的目录。
4. 点击浏览器工具栏中的扩展图标，打开授权助手。支持 Chrome / Edge 116 及以上版本。

## 没有 Client ID：先用 PAT

1. 保持“PAT 创建 / 导入”模式。选择“AutoPM 周报同步”预设。
2. 点击“打开官方 Token 管理”，登录 Airtable，在创建或编辑 Token 时加入清单中的 scopes：`data.records:read`、`data.records:write`、`schema.bases:read`。
3. 在官方页面添加需要访问的 Base 或工作区，保存并复制完整 Token。
4. 粘贴到插件，点击“验证并使用 PAT”→“获取列表”→选择 Base →“读取表结构”。
5. 检查 Projects / Tasks / Issues 表 ID，验证记录读取，导出 `sync_config.json`。
6. 在 AutoPM 的“连接设置”中导入该 JSON，并保存连接设置。

PAT 权限必须在 Airtable 官方页面保存。插件不会通过网页脚本操作账户，也不会把勾选动作当作远程 PAT 权限修改。官方 whoami 接口对 PAT 不一定返回 scopes；插件将这种情况显示为“未知”，读取成功不代表已验证写入权限。PAT 的 Token ID 不是 Token 密钥。

## 首次配置 OAuth：让勾选权限直接用于授权

1. 在插件切换为“OAuth 自动授权”。
2. 打开 <https://airtable.com/create/oauth>，选择 **Register new OAuth integration**，填写集成名称。
3. 将插件显示的回调地址填到 **OAuth redirect URI**。此包使用固定公开标识，地址应为：

   `https://jembllofamdmnklofgmdnbemhjfmknep.chromiumapp.org/airtable`

4. 在集成的 **Permission scopes** 中启用你可能申请的权限，然后保存。实际授权仍只申请插件当前勾选的权限。企业权限还需要账户与角色支持。
5. 此扩展是公开客户端：**不要为该集成生成 Client Secret**。已经生成 Secret 的集成请另建公开客户端集成；不要把 Secret 填进插件或源代码。
6. 复制 **Client ID** 到插件，点击“按所选权限打开 Airtable 授权”。登录后，在 Airtable 的授权页选择允许的 Base / 工作区并确认。
7. 插件使用 PKCE 和 state 校验回调、获取 Token，并核对服务端返回的 scopes 是否与选择完全一致。

自己账号测试可从基础配置开始。供其他账户使用时，需要在 Airtable 集成中填写支持邮箱、公开隐私政策网址和服务条款网址。本包的 PRIVACY.md 可作为隐私说明参考，但它不是已经发布的网站。扩展上架商店后若扩展 ID 改变，必须在 Airtable 更新回调地址；以运行中的插件显示值为准。

## 如何改变权限

- OAuth：修改勾选后点击“应用所选权限”。缩小权限通过刷新请求应用；扩大权限需要重新进入 Airtable 授权。勾选本身不改变已获取 Token。
- PAT：打开官方 Token 管理页，修改 scopes / 资源并保存，之后在插件重新验证。插件没有使用 PAT 创建或修改的非公开接口。
- Airtable 的 `data.records:write` 包含新增、修改和删除，不能把三者拆成不同的 Token 权限。
- 所选 scopes、授权资源范围、用户自身角色共同限制实际操作。扩大 scope 不能绕过 Base / 表 / 字段的访问限制。

## Token 保存、刷新与导出

- 完整 Token、刷新令牌和授权流程临时数据只放在 `chrome.storage.session`，不写入同步存储或持久设置。浏览器会话结束、扩展重新加载或禁用后需要重新连接。
- Client ID、权限选择、Base ID 等非密钥配置保存在本机。Client ID 和 manifest.key 均为公开标识。
- OAuth 访问令牌使用时按需刷新，刷新令牌轮换不自动重试；如果刷新结果不确定，必须重新授权，避免重复消费旧令牌。
- OAuth 刷新会使旧 Token 失效，之前导出的 JSON 也可能提前失效。**AutoPM 目前不会自动刷新 OAuth Token**；每次刷新后需要重新导出、导入。长期 AutoPM 连接建议使用 PAT。
- JSON 含完整访问令牌，但不含 OAuth 刷新令牌。只在用户点击时导出、显示或复制。不要公开分享导出的 JSON。
- “清除本机令牌”只清除插件会话数据，不撤销 Airtable 端授权。撤销、删除 PAT 或管理 OAuth 授权需在 Airtable 官方页面操作。
- 验证仅调用身份、Base 列表、表结构和最多一条记录的读取接口；不会通过新增、修改或删除业务数据来猜测写入权限。记录内容不会传到插件页面。

## 开发与验证

源码目录包含 `tests`，可使用 Node 22+ 运行 `node --test tests/*.test.mjs`。发行 ZIP 不含测试代码、任何用户密钥或依赖目录。真实 OAuth 授权需要你先注册 Client ID；协议模拟测试不能替代 Airtable 真实登录与授权测试。

官方参考：[OAuth 集成配置](https://airtable.com/developers/web/guides/oauth-integrations)、[OAuth 协议与刷新](https://airtable.com/developers/web/api/oauth-reference)、[权限定义](https://airtable.com/developers/web/api/scopes)、[身份与 scopes](https://airtable.com/developers/web/api/get-user-id-scopes)、[PAT 管理](https://support.airtable.com/articles/9934989703-creating-personal-access-tokens)。
