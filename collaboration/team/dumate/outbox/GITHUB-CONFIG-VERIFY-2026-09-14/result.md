# GitHub 配置验证报告（dumate 实测）

任务ID：GITHUB-CONFIG-VERIFY-2026-09-14（用户直接指令，非 Codex inbox 派单）　提交版本：attempt 1　执行者：dumate　开始／结束时间：2026-09-14 22:30 / 22:40 (UTC+8)

目标环境／App：GitHub 私有仓库 `sunny-06064710-3/autopm-dadhboard`（协作管理仓库）　代码分支与提交或文件哈希：无代码提交，临时分支已删除　授权范围：仅验证与测试；测试数据全部自建自删，未修改任何既有 Issue / 分支 / 文件。

## 业务结果

GitHub CLI 环境已从"未安装／未认证"配置为**可用的完整读写环境**：gh CLI 已就位并以 `sunny-06064710-3` 身份完成设备授权登录；私有仓库可读（管理员权限）；Issue 创建/读取/关闭/删除全链路实测通过；git over https 推送实测通过。测试遗留数据为零，仓库回到验证前状态（Issue 仅 `#1 [COORD-001] OPEN`，无多余分支）。

## 环境与认证

| 项 | 实测结果 |
|---|---|
| git | 2.54.0.windows.1；全局 user.name=Sunny，user.email=sunny@autopm.dev |
| gh CLI | v2.100.0，位于 `C:\Program Files\GitHub CLI\gh.exe`（winget 安装；此前不在 PATH 中，已用绝对路径调用） |
| 认证方式 | GitHub 设备授权（Device flow），浏览器内账号已登录 `sunny-06064710-3` 完成授权 |
| 认证结果 | `gh auth status`：✓ Logged in to github.com account sunny-06064710-3；令牌存储于系统凭据库（keyring）；Token scopes：`gist`、`read:org`、`repo` |
| 令牌处理 | 全程未输出、未写入任何任务正文/日志/交付文件；gh 输出自动打码 |

## 验收用例（实测记录）

| 用例 | 操作 | Expected | Actual | Pass/Fail | 备注 |
|---|---|---|---|---|---|
| 仓库可读 | `gh repo view sunny-06064710-3/autopm-dadhboard` | 返回仓库 README | 返回完整部署指南 README | Pass | 私有仓库可见 |
| 仓库属性 | repo view --json 查询 | PRIVATE + 管理员权限 | isPrivate=true, visibility=PRIVATE, viewerPermission=**ADMIN**, hasIssuesEnabled=true, defaultBranch=main | Pass | |
| Issue 列表 | `gh issue list --state all` | 可读 | `#1 OPEN [COORD-001] AutoPM 多 AI 协作管理与接入` | Pass | 与 README 记录一致 |
| Issue 创建 | create 测试 Issue | 创建成功 | 创建 `#2`，返回 URL | Pass | 标题含测试标识 |
| Issue 读取 | `gh issue view #2` | 读取字段正确 | {number:2, state:OPEN, author:sunny-06064710-3, title 正确} | Pass | |
| Issue 关闭 | `gh issue close #2` | 关闭成功 | `✓ Closed issue ...#2` | Pass | |
| Issue 删除 | `gh issue delete #2 --yes` | 删除成功 | 退出码 0；终态列表无 #2 | Pass | 零残留 |
| git 推送 | 临时分支 `gh-test-temp` push over https | 推送成功 | `* [new branch] gh-test-temp`，远端确认分支存在 | Pass | 使用了 gh 凭据助手 |
| 分支清理 | 删除临时远端分支 | 远端无残留 | 经 gh API DELETE 成功，再查 404 | Pass | 见"剩余问题" |

## 数据与后台结果

- 创建：Issue 1 个（#2）、git 临时分支 1 个（gh-test-temp）→ 已全部删除。
- 修改：0（未触碰 #1 及任何既有内容）。
- 冲突 0、失败 0、结果未知 0。
- 通知/推送类：Not Run（无此需求）。
- 线上发布/生产：Not Run（未涉及）。

## 剩余问题与交接

| 问题 | 严重程度／影响 | 复现与证据 | 所需动作／依赖 | 建议负责角色 |
|---|---|---|---|---|
| `git push origin --delete` 在本环境挂起（120s 超时） | 中／分支清理便利性 | 推送成功后执行删除时挂起；改用 `gh api -X DELETE repos/{o}/{r}/git/refs/heads/{b}` 成功 | 后续删除远端分支建议直接用 gh API 或 `gh api` 封装命令；也可复查 git 凭据助手配置 | Codex |
| `gh issue create` 本版不支持 `--json` 标志 | 低／脚本化时需解析 URL | `--json` 报 unknown flag | 脚本内用返回 URL 提取编号 | Codex |
| 仓库 README 中含默认管理员凭据明文 | 中／凭据泄露风险（仓库私有，风险受控） | repo view 输出可见 | 建议改为环境变量方式部署并移除 README 明文；是否处理由用户决定 | Codex／用户 |
| 自动唤醒／定时任务能力 | 未验证 | 本次未涉及 | 按分工指南由 Codex 另行安排连接验证 | Codex |
| 站内浏览器授权按钮 disabled（README 记录） | 不适用 | 本次设备授权经内置浏览器完成，未依赖站内按钮 | 无需动作 | — |

## 未验证项（如实声明）

- 代码推送至 `main` 分支（按协作规则不得测试推主分支，未执行）。
- GitHub 线上部署、Pages、Webhook、API 深度能力（不在本次范围）。
- 自动唤醒／无人值守（README 明确未验证，本次保持不变）。

执行状态：Submitted（用户直派任务，无 Codex 验收环；报告留档供 Codex 读取核验）。验收状态留给协调方。