# 给 Qoder：AutoPM → Power Apps 业务功能等效迁移

修订：2026-09-15。总协调 [#1](https://github.com/sunny-06064710-3/autopm-dadhboard/issues/1)。仅使用 autopm-dadhboard。
资料基准：`codex/autopm-management-20260914`；PR #44 合并前不要从 main 猜测缺失文件。实际状态读取原 Issue。

## 用户授权与目标

用户于2026-09-15（Asia/Shanghai）在本次 Codex 会话明确要求实施本修订计划：由 Qoder 执行，复刻业务功能和结果，允许界面适配 Power Apps；每轮交回 GitHub。当前轮授权为 #18 的只读核实与 #19 的离线实现、测试、分支、PR和回报。已有范围不重复询问；扩大范围另行确认。
不得把租户访问、发布许可、环境批准或自动唤醒当作已验证。

## 必须先读

- [根规则](../../../AGENTS.md)、[当前决定](../../README.md)、[Qoder入口](../../team/qoder/README.md)。
- [MS-00](../tasks/MS-00.md)、[MS-01](../tasks/MS-01.md)、[蓝图](../01_BLUEPRINT.md)、[验收](../03_ACCEPTANCE.md)、[用例](../acceptance/TEST_CATALOG.md)。
- [可运行源码、合成样例与指纹](../../current/microsoft/README.md)、[缺失资料](../../../docs/DEPENDENCIES.md)。不依赖协调方本机路径，不读取历史认证截图、账号配置或个人归档。

## 当前轮：先接收，再推进两个独立任务

1. 在 #18、#19 回执真实执行身份、读取提交、允许修改范围、检查计划及授权出处。Ready 不等于已启动。
2. #18 / MS-00：只读核实本人获准的 Microsoft 环境URL/ID、Dataverse、许可证、开发/Solution权限、运行身份及证据时间；无入口写 Unknown 和最小需求。核实子任务可交付，部署门槛仍未通过时不得把整个 MS-00 标 Accepted。
3. #19 / MS-01：比较 legacy/candidate Bridge，复现测试，输出复用图与规则冲突；从历史12组对照细化功能矩阵（功能ID、源证据/日期、输入操作、规则、预期结果、目标组件、验收用例、证据缺口）。当前线上未知项标待核实。
4. 在最少必要修改下分离解析与目标写入，交付目标无关变更计划和 Dataverse 适配契约；覆盖 TC-04/15/16/17/18/19/30，包含稳定身份、空值、重复导入、预览过期/并发、写入响应丢失、创建/更新读回、Tracker公式/Baseline/原文件保护。平台测试无法运行则明确 Not Run。
5. 先补正接入 PR #45 的任务编号、源提交、确认、时间和文件哈希说明。该文档补正不阻塞已授权的 #18/#19 离线工作，但不代表 #42 完整验收通过。

## 写入范围与后续阶段

- 一任务一工作分支，PR指向管理分支。#18 写 `collaboration/team/qoder/outbox/MS-00/`；#19 代码/合成样例写 `collaboration/team/qoder/work/MS-01/`，结果写 `collaboration/team/qoder/outbox/MS-01/`。源码快照只读；其他必要修改先在 Issue 明确范围。
- #20–#28 沿用各原任务依赖及验收编号：模型/身份 → 公共规则 → Hub/模板/SKU/Issue → 导入/周报 → 迁移验收。环境和前置验收通过后由 Codex 激活具体任务，不同时将所有任务设为执行中。
- #29–#31 为后续增强，保持 Deferred；#37 作为界面适配设计候选，保留已撤回布局约束，不替代正式 Dataverse 验收。
- 保留现有Task完成机制，暂停项目进度改造；不更改现有SharePoint MVP、不写生产、不停用Airtable、不发送真实通知、不扩展权限或新建未批准服务。

## 每轮交回 GitHub

每次启动读原Issue及最新评论，按上次检查点继续。每次结束（包括部分完成、阻塞）在原Issue评论：任务ID/attempt、执行身份、时间/时区、起始/结束提交、完成内容、PR、测试Actual与证据、未验证项、阻塞、下一步。
使用 [DELIVERY](../templates/DELIVERY.md) 记录 outbox 结果，保留每次日志；不以新结果覆盖历史检查点。代码须推送，只有本地文件不算已交付。
结束标 Submitted/In review 或 Blocked；不得自行合并、关闭任务或部署。写回失败保存待补报内容，下一次先补报；不要重复执行已成功写入。
Codex负责独立验收；GitHub评论不证明Codex已获通知，定时检查的实际配置与运行证据另行核实。
