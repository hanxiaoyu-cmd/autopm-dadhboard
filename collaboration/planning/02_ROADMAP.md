# 双平台路线图与任务台账

版本：v1.1｜33工作包＝15 Airtable＋14 Microsoft＋4共用治理；27 P0、6 P1。P0/依赖是业务顺序，非虚构日期或进度百分比。

## 1. 现在可以交出的首批任务

- Airtable：AT-00，完成受影响对象基线和隔离测试准备。通过后才能按依赖开始AT-01/02/03。
- Microsoft：MS-01，离线拆分Bridge公共逻辑、样例和适配器契约；无需等待Dataverse。MS-00由IT/平台角色补开通证据。
- 共用：GOV-01/02/03可分别整理规则、权限与试用准备；GOV-04贯穿后续提交审核。

首发提示词：[Airtable](dispatch/START_AIRTABLE.md) / [Microsoft](dispatch/START_MICROSOFT.md)。本轮未实际派发。

## 2. 依赖波次

| 波次 | Airtable | Microsoft | 退出条件 |
|---|---|---|---|
| W0 | AT-00 | MS-01；MS-00环境准备 | 对象基线、隔离、公共契约和可部署条件各有明确证据 |
| W1 | AT-01/02/03 | MS-02/03 | 身份、关系、统计、完成与写入约束稳定 |
| W2 | AT-04/05/06 | MS-04/05/06/07 | 主执行功能和数据处理规则通过组件测试 |
| W3 | AT-07/08/09/10 | MS-08/09 | 团队统一入口、报告、提醒、案例与恢复可操作 |
| W4 | AT-11 | MS-10 | 真实角色、全链路、切换与两个周度周期 |
| W5 | AT-12/13/14 | MS-11/12/13 | 基于实际使用证据增强效率与AI能力 |

波次内不代表所有包能同时开始；以每包dependencies为准。MS-04包含基础Hub，Plan/Issues等由后继包接入。GOV-01/02是关键业务/权限依赖，GOV-03不阻止离线开发但限制正式运行验收。GOV-04按提交持续审核，不能把整体审核完成设为所有任务开始前提。

## 3. 全部任务

| ID／任务 | 优先级 | 依赖 | 执行状态 | 验收状态 |
|---|---|---|---|---|
| [AT-00 隔离基线与字段消费者清单](tasks/AT-00.md) | P0 | 可开始准备 | Unassigned | Not Submitted |
| [AT-01 统一任务完成和统计口径](tasks/AT-01.md) | P0 | AT-00, GOV-01 | Waiting Dependencies | Not Submitted |
| [AT-02 My Work与人员责任维护](tasks/AT-02.md) | P0 | AT-00, GOV-01, GOV-02 | Waiting Dependencies | Not Submitted |
| [AT-03 Program、Project与SKU关系生命周期](tasks/AT-03.md) | P0 | AT-00, GOV-01 | Waiting Dependencies | Not Submitted |
| [AT-04 模板与统一排期处理](tasks/AT-04.md) | P0 | AT-01, AT-03, GOV-01 | Waiting Dependencies | Not Submitted |
| [AT-05 Issue结果、验证关闭与重开](tasks/AT-05.md) | P0 | AT-01, AT-02, GOV-01 | Waiting Dependencies | Not Submitted |
| [AT-06 计划导入与Bridge可靠写入](tasks/AT-06.md) | P0 | AT-01, AT-03, GOV-01 | Waiting Dependencies | Not Submitted |
| [AT-07 团队Data Center与托管处理](tasks/AT-07.md) | P0 | AT-06, GOV-02 | Waiting Dependencies | Not Submitted |
| [AT-08 统一Project Hub与组合界面](tasks/AT-08.md) | P0 | AT-01, AT-03, AT-04, AT-05 | Waiting Dependencies | Not Submitted |
| [AT-09 周报、提醒与Tracker结果](tasks/AT-09.md) | P0 | AT-01, AT-02, AT-06, AT-07, AT-08 | Waiting Dependencies | Not Submitted |
| [AT-10 最小案例复用与运行维护](tasks/AT-10.md) | P0 | AT-05, AT-07, GOV-02 | Waiting Dependencies | Not Submitted |
| [AT-11 角色、完整链路与生产发布验收](tasks/AT-11.md) | P0 | AT-00, AT-01, AT-02, AT-03, AT-04, AT-05, AT-06, AT-07, AT-08, AT-09, AT-10, GOV-02, GOV-03 | Waiting Dependencies | Not Submitted |
| [AT-12 计划交互与模板升级增强](tasks/AT-12.md) | P1 | AT-04, AT-11 | Deferred | Not Submitted |
| [AT-13 管理Review与轻量待决事项](tasks/AT-13.md) | P1 | AT-05, AT-09, AT-11 | Deferred | Not Submitted |
| [AT-14 有来源的AI摘要与案例推荐](tasks/AT-14.md) | P1 | AT-09, AT-10, AT-11, GOV-02 | Deferred | Not Submitted |
| [MS-00 微软环境、许可和运行身份](tasks/MS-00.md) | P0 | 可开始准备 | Blocked Environment | Not Submitted |
| [MS-01 复用Bridge并分离公共规则](tasks/MS-01.md) | P0 | 可开始准备 | Unassigned | Not Submitted |
| [MS-02 Dataverse模型、身份和权限](tasks/MS-02.md) | P0 | MS-00, GOV-01, GOV-02 | Waiting Dependencies | Not Submitted |
| [MS-03 公共API与服务端规则](tasks/MS-03.md) | P0 | MS-01, MS-02 | Waiting Dependencies | Not Submitted |
| [MS-04 Canvas统一Program与Project Hub](tasks/MS-04.md) | P0 | MS-02, MS-03 | Waiting Dependencies | Not Submitted |
| [MS-05 建案模板与计划维护](tasks/MS-05.md) | P0 | MS-03, MS-04 | Waiting Dependencies | Not Submitted |
| [MS-06 ProjectSKU范围与里程碑例外](tasks/MS-06.md) | P0 | MS-03, MS-05 | Waiting Dependencies | Not Submitted |
| [MS-07 My Work与Issue验证闭环](tasks/MS-07.md) | P0 | MS-03, MS-04 | Waiting Dependencies | Not Submitted |
| [MS-08 应用内导入、预览与批量维护](tasks/MS-08.md) | P0 | MS-01, MS-03, MS-04, GOV-02 | Waiting Dependencies | Not Submitted |
| [MS-09 周报、提醒、Tracker与Lesson](tasks/MS-09.md) | P0 | MS-05, MS-06, MS-07, MS-08 | Waiting Dependencies | Not Submitted |
| [MS-10 迁移、发布与运行交接](tasks/MS-10.md) | P0 | MS-00, MS-01, MS-02, MS-03, MS-04, MS-05, MS-06, MS-07, MS-08, MS-09, GOV-02, GOV-03 | Waiting Dependencies | Not Submitted |
| [MS-11 计划与管理效率增强](tasks/MS-11.md) | P1 | MS-05, MS-06, MS-10 | Deferred | Not Submitted |
| [MS-12 Review、知识与有来源AI](tasks/MS-12.md) | P1 | MS-09, MS-10, GOV-02 | Deferred | Not Submitted |
| [MS-13 更多正式系统接入](tasks/MS-13.md) | P1 | MS-10, GOV-01, GOV-02 | Deferred | Not Submitted |
| [GOV-01 业务字典、归属和规则决策](tasks/GOV-01.md) | P0 | 可开始准备 | Unassigned | Not Submitted |
| [GOV-02 权限、发布与运行责任](tasks/GOV-02.md) | P0 | 可开始准备 | Unassigned | Not Submitted |
| [GOV-03 试用、采纳和价值基线](tasks/GOV-03.md) | P0 | 可开始准备 | Unassigned | Not Submitted |
| [GOV-04 成果审核、变更与双平台Gate](tasks/GOV-04.md) | P0 | 可开始准备 | Unassigned | Not Submitted |

## 4. 任务排期与状态使用

执行AI接手后，基于本包对象数量、实际权限、可复用版本和首批用例给出工作量区间，并分开执行投入、环境等待、业务观察周期。本轮不承诺未知工期。用户先前拒绝无依据的4–8周估计，不应换成另一个无依据短工期。

所有assignee为空表示未分派；没有替任何同事接受任务。执行方交回后由协调方审核、更新主表并解除具体后继依赖。历史已完成行和本地候选代码均不能自动解锁依赖。

规则／数据结构有变更先更新[决策登记](04_SOURCES_AND_DECISIONS.md)，再同步受影响AT/MS包与用例。同一轮不要让多个AI同时修改相同字段、脚本或主规则文件；可按互不重叠的任务和开发分支分工。

