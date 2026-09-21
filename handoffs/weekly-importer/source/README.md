# AutoPM 源码版

当前为 **2026-09-19 / 2.4.0-rc3 测试版**，已提供 Windows x64 单文件 EXE。正常业务主线为：周报 → Airtable → All Tracker；All Tracker 回写用于复验与查漏。

最新确认：周报内容归属 Project，SKU 维度从 Airtable 开始维护。该业务调整尚未完成代码落地，本次 EXE 仅用于解析与预览测试，不代表业务验收通过。

## 单文件测试版

发送 `dist/AutoPM_2.4.0-rc3_Test_Windows_x64.exe` 一个文件即可，接收电脑无需安装 Python。首次连接需自行配置 Airtable 凭证；AI 解析另需 DeepSeek 凭证。程序不包含本机密钥、周报或数据库快照。

打包版配置、日志和缓存保存在 `%LOCALAPPDATA%\AutoPM-Preview`，不要求 EXE 所在文件夹可写。该 EXE 尚未签名，公司设备是否允许运行取决于 IT 策略。

rc2 修复 Airtable 与 DeepSeek 的证书信任来源：无显式 CA 配置时，使用系统信任库（Windows ROOT/CA）；保留 `SSL_CERT_FILE` / `SSL_CERT_DIR` 配置、域名验证、证书验证与代理支持。没有关闭 TLS 校验或安装证书。

rc3 修复新电脑缺少本机已保存配置的问题：只对已确认的 AutoPM 主库补充工程备注日期存储规则、Tasks/Issues 的项目关联、工厂代码等非敏感默认映射；每次仍核对实际 schema，保留用户明确设置及已保存的映射记忆。其他 Base 不套用这些字段 ID，不新增 Airtable 字段。

封装验证：424 项测试通过；在独立目录、空白配置和不含 Python 的 PATH 下成功启动，读取真实 Shark 周报 183 个项目区块，并使用本次只读获取的真实 schema 验证首次映射：0 阻断、0 映射警告。EXE 无凭据访问 Airtable 返回 HTTP 401，证明当前机器的 TLS 验证通过，不代表 Token 权限或公司电脑已验证。验证记录在 `.local/rc3_fix_20260919/package-verification.json`。真实报告仍有数据匹配等提示；未执行生产云端写入。

请先阅读 [匹配规则、真实验证与最终审核清单](../docs/reference/先看这里.md)。该页记录 2026-09-19 的审核依据；本交接包的最新入口是 [交接 README](../README.md)。旧目录、旧交接文档和旧 EXE 不代表当前实现。

## 启动

1. 将整个 ZIP 解压到固定目录，不能直接在压缩包里运行。
2. 安装 Windows Python 3.11 或更新版本（本次现有环境验证为 Python 3.14），保留 Python Launcher 和 Tcl/Tk 组件。
3. 双击 **启动源码版.cmd**。首次会创建 `.venv` 并联网安装 `requirements.txt` 中的依赖，然后打开桌面界面。
4. 在“连接设置”填写自己的 Airtable Token，检测并选择数据库；DeepSeek Key 按需填写。
5. 选择周报。规则模式使用“离线检查”再“本地结果 → Airtable 预览”；核对后才确认写入。

也可以在解压目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\start.ps1
```

已有 Python 环境时：

```powershell
python -m pip install -r requirements.txt
python app.py
```

## 首次复用当前主库映射（可选）

`config.main-base.example.json` 保存当前 AutoPM V2（Pilot）的 Base、表、字段映射及周报合并规则，不含密钥或业务记录。仅在首次配置、尚无本地设置时使用：

```powershell
New-Item -ItemType Directory -Path .local -Force
Copy-Item config.main-base.example.json .local/settings.json
```

然后启动界面填写 Token 并重新检测数据库。切换其他 Base 时，需要核对其结构映射。不要将此示例覆盖到已有个性化设置上。

## 目录

| 位置 | 内容 |
|---|---|
| `app.py`、`autopm/` | 桌面入口和完整业务源码 |
| `tests/` | 全部自动测试 |
| `benchmarks/` | 测试需要的评分和故障矩阵辅助代码；历史评测语料未附带 |
| `assets/` | 品牌图标、界面字体和字体许可 |
| `browser-extension/airtable-token-helper/` | 可选的 Chrome/Edge 授权助手源码及测试 |
| `start.ps1` | 源码启动及首次依赖安装 |
| `build.ps1` | 后续需要时自行构建 EXE；不影响源码运行 |
| `SOURCE_MANIFEST.json` | 包内文件哈希及来源源码校验 |

原始周报和本地总表没有放入源码包，可在界面自行选择文件。首次运行会按需生成 `.local` 和 `Run Logs`。

## 验证与开发

安装依赖后运行全部测试：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

可选扩展直接加载 `browser-extension/airtable-token-helper` 目录。安装 Node 后可测试扩展：

```powershell
Set-Location browser-extension/airtable-token-helper
npm test
```

本包不包含真实 Token/API Key、加密凭据、用户缓存、Airtable 数据快照、原始业务 Excel、虚拟环境、构建缓存、已封装 EXE 或历史运行日志。

## 本版修复

### 2026-09-15 字段容错修复

- 非关键字段缺失、类型不兼容或旧映射失效时，仅跳过该字段，在“提示与检查”和运行日志中保留原因；其他有效字段继续导入。
- 单个项目编号重复、日期无效、备注无法合并时，仅跳过该项目；任务/问题必要字段有问题时，仅跳过对应任务/问题。
- 项目 ID、当前使用的周报版本字段、表身份和映射冲突仍受保护，避免错项目写入或旧周报覆盖新周报。
- 映射按 Base 保存稳定字段 ID，字段改名可继续使用；删除重建或类型变化的字段保留旧映射，进入“映射记忆”重新指定目标后恢复导入。也可用“DS 建议缺失映射”辅助选择。
- 当前主库的有效映射和备注合并方式已写入本地设置。其他 Base 需根据实际结构配置；业务源码没有新增本库专用字段 ID。

无法匹配的内容保留在原周报和 `Run Logs`，不会往日期、选项或人员字段写入虚假的占位值。表结构变化或并发修改发生在预览之后时，仍需重新预览。以上容错针对周报导入；本地总表回填仍使用严格结构核对。

- 按 Base 隔离周报合并规则，并校验预览的客户端、配置和读取结果一致。
- 兼容富文本对周报标记的转义及有效闭合标记后的单个换行。
- 对新周报块增加动态代码围栏，避免富文本自动重排原文编号；保留原备注和历史，同文件重复导入不追加。
- 保留 NPI/XPT Lead、Jira 数值与显式 URL、Next PLM 以及本地总表功能。

仅隐藏在 Excel 超链接目标中的 URL 仍属未支持范围；未匹配项目、含糊日期与主数据仍按原规则提示和跳过。
