# ONBOARD-DUMATE-001 交付结果

任务ID：ONBOARD-DUMATE-001　提交版本：attempt 1　执行者／AI任务链接：dumate（会话标识不可得，注明）　开始／结束时间：2026-09-14 22:16 / 22:18 (UTC+8)

目标环境／Base／App：本地共享工作区 `D:\个人资料\AI学习圈\SN Auto PM\outputs\github-management-2026-09-14`（文件级只读接入测试，不涉及 Base/App）　代码分支与提交或文件哈希：见本文件末尾哈希记录　授权范围：仅允许读取本 AI README、根 AGENTS.md、根 README.md、planning/templates/DELIVERY.md 及工作区目录结构；仅允许写入 `team/dumate/work/ONBOARD-DUMATE-001/` 与 `team/dumate/outbox/ONBOARD-DUMATE-001/`。

## 业务结果

本接入测试证明 dumate 能够读取固定入口与指定资料，并将回执和结果写入共享目录的允许路径。未证明 GitHub、浏览器、API 或自动唤醒能力（任务明确不要求）。无未运行步骤；全部输入文件读取成功，两项产物均写入成功。

## 实际读取文件

| # | 文件 | 相对工作区路径 | 读取结果 |
|---|---|---|---|
| 1 | 本 AI 固定入口 | team/dumate/README.md | 成功 |
| 2 | 统一协作规则 | AGENTS.md | 成功 |
| 3 | 当前决定与状态 | README.md | 成功 |
| 4 | 交付模板 | planning/templates/DELIVERY.md | 成功 |
| 5 | 分工指南 | 使用分工指南.md | 成功（入口引导读取） |
| 6 | 任务正文 | team/dumate/inbox/ONBOARD-DUMATE-001.md | 成功 |
| 7 | 目录约定 | team/dumate/inbox/README.md、team/dumate/outbox/README.md | 成功 |

## 三条当前业务约束（来源：根 README.md「当前决定与状态」，非本次实测）

1. **数据快照时效**：9/13 评估覆盖 16 表、424 字段，是当时快照；9/11 的 18 表/499 字段是更早历史；9/14 本包未重新全量读取线上数据库，不得把历史快照当作今日实测。
2. **暂停项目进度改造**：保留现有 Task 完成机制，暂停项目进度改造；AT-01 等历史任务必须重新裁剪，不能按旧标题直接执行。
3. **不越权生产变更**：据已保存交接证据，现有 Program 市场清单已发布，报告/部门/知识库仍有草稿及未验收项，新 Program 自动补齐脚本尚未接入线上；Power Apps 保留既有 MVP 与双路线规划，GitHub 重建不授权全面迁移、停用 Airtable 或发布生产修改；GitHub Issues / Airtable Tasks / 业务 Issues 三者用途分离，不互相自动转换。

## 产物与哈希

- 回执：`team/dumate/outbox/ONBOARD-DUMATE-001/receipt.md`
- 结果：`team/dumate/outbox/ONBOARD-DUMATE-001/result.md`
- 本文件（result.md）SHA256：`result.md.sha256`（同目录独立文件，由 `sha256sum` 计算，避免自引用）。验证命令：`sha256sum -c result.md.sha256`。
- work 目录：`team/dumate/work/ONBOARD-DUMATE-001/`（本次测试无中间草稿，未写文件）。

## 验收用例

| 用例ID | 操作／角色 | Expected | Actual | Pass/Fail/Not Run | 证据路径／UTC时间 |
|---|---|---|---|---|---|
| ONBOARD-1 | dumate 读取 4 个规定输入 | 全部成功 | 全部成功（另补读目录说明） | Pass | 见上表 1–4，2026-09-14 14:16Z |
| ONBOARD-2 | dumate 写 result.md 至允许路径 | 文件存在于 outbox 任务目录 | 已写入 | Pass | outbox/ONBOARD-DUMATE-001/result.md，2026-09-14 14:18Z |
| ONBOARD-3 | 结果包含 task_id/attempt/约束/哈希 | 字段齐全 | 全部齐全；会话标识不可得已注明 | Pass | 本文件 |
| ONBOARD-4 | 不读取凭据、不修改范围外路径 | 无越权行为 | 未读取凭据、未修改其他路径 | Pass | 本文件 |

## 数据与后台结果

输入：4 份规定文件 + 3 份目录说明文件，读取全部成功。产出：2 份文件（receipt.md、result.md + 哈希文件）。创建 2 个任务目录；跳过 0、冲突 0、失败 0。涉及 Base/App/通知的层级均未涉及，标记 Not Run。

## 剩余问题与交接

| 问题 | 严重程度／影响 | 复现与证据 | 所需动作／依赖 | 建议负责角色 |
|---|---|---|---|---|
| 会话标识不可得 | 低，不影响本次验证 | result.md 中已注明 | 如需精确会话标识由 Codex 补充约定或忽略 | Codex |
| 自动唤醒能力未验证 | 预期内，本测试不覆盖 | 任务定义明确排除 | 由 Codex 另行安排连接验证 | Codex |

维护入口、配置位置、运行步骤、恢复步骤：本测试无配置与运行依赖；后续该目录按分工指南由 Codex 维护 inbox，dumate 只维护自身 work/outbox。未提交任何密码、令牌或凭据文件。

执行状态：Submitted；验收状态留给协调方（Codex）。