# MS-00 部署前置条件

版本：attempt 1｜执行者：Qoder｜日期：2026-09-16 Asia/Shanghai

## 概述

本文档记录 MS-00 环境就绪性核实结果。由于 Qoder 无法登录或访问任何 Microsoft 租户、Dataverse 实例或 Power Platform 环境，所有核实项均标记为 **Unknown**。本文档不构成部署授权。

## 核实结果

| 前置条件 | 状态 | 证据 | 说明 |
|---------|------|------|------|
| Dev 环境已创建并可用 | Unknown | 无可核验证据 | 未登录；无环境 ID |
| Test 环境已创建并可用 | Unknown | 无可核验证据 | 未登录；无环境 ID |
| Prod 环境已规划 | Unknown | 无可核验证据 | 未登录；无环境 ID |
| Dataverse 表创建权限 | Unknown | 无可核验证据 | 无 API 访问 |
| Solution 发布权限 | Unknown | 无可核验证据 | 无 API 访问 |
| 插件注册权限 | Unknown | 无可核验证据 | 无 API 访问 |
| 用户许可（Power Apps per user/per app） | Unknown | 无可核验证据 | 未查看许可中心 |
| 服务身份/应用注册 | Unknown | 无可核验证据 | 未登录 Azure AD |
| 连接引用（Airtable、SharePoint） | Unknown | 无可核验证据 | 未配置 |
| 环境变量与凭据托管 | Unknown | 无可核验证据 | 未登录 Key Vault |
| Power Automate 流部署 | Unknown | 无可核验证据 | 未登录 |
| Azure Functions 运行时 | Unknown | 无可核验证据 | 未登录 |

## 阻塞项

1. **无环境访问**：Qoder 未被授予任何 Microsoft 租户登录权限，无法执行任何在线核实。
2. **无 IT 批准证据**：任务规格书指出 Dataverse 用户"最后反馈仍未批准"；本轮无新信息。
3. **无服务身份凭据**：不索取密码/令牌；无法验证连接引用或环境变量配置。

## TC-25 离线子结果

**TC-25 — 部署、配置与故障交接**

| 子项 | 状态 | 说明 |
|------|------|------|
| 测试环境部署版本记录 | Not Run | 无环境 |
| 断开后台连接后恢复 | Not Run | 无环境 |
| 故障后保留合法新修改 | Not Run | 无环境 |
| 连接/规则版本可定位 | Not Run | 无环境 |
| 另一维护者按手册恢复 | Not Run | 无环境/无手册 |
| 无个人凭据依赖 | Pass（设计层面） | 本包不存储任何凭据 |

## TC-32 离线子结果

**TC-32 — 数据模型生成与平台约束**

| 子项 | 状态 | 说明 |
|------|------|------|
| 离线生成两次相同元数据 | Not Run | 本轮未执行元数据生成；依赖 MS-01 Bridge 分析 |
| 无重复逻辑字段 | Not Run | 依赖 MS-01 |
| SourceRecordMap source_id 不重复 | Not Run | 依赖 MS-01 |
| Dataverse 关系类型/唯一键 | Not Run | 无 Dataverse 环境 |
| 不宣称正式 Solution/插件已部署 | Pass（声明层面） | 本文明确声明未部署 |

## 恢复与回退

本包为纯文档交付，无配置变更、无代码部署、无环境修改。回退方式：忽略或删除本提交。

## 依赖

- 需要 Microsoft 租户管理员提供环境 ID 和许可证据
- 需要 IT 部门确认 Dataverse 批准状态
- 需要 Codex 审核离线子结果并决定是否推进
