# 9/11规划基线（历史快照）

本目录保留原任务定义和来源，不再维护当前执行状态。当前状态只读GitHub Issue；任务导航见 [索引](../issue-map.json)。执行遵守 [根规则](../../AGENTS.md)。下文历史“主台账”“当前优先”“未推送”等只适用于原日期。

模板仍可复用，但以根规则的用户确认、日志和验收要求为准。旧生成器仅供历史包复现，不能重建现行派工。外部来源与缺失附件见 [依赖登记](../../docs/DEPENDENCIES.md)。

---

# AutoPM 双平台开发控制包

**v1.2业务修订：** [Project、Task、Issue简明说明](design/PROJECT-TASK-ISSUE.md)及[执行清单](design/PROJECT-TASK-ISSUE-IMPLEMENTATION.md)。Tasks为项目计划；问题措施保存在Issue Actions，不自动进入Tasks。此项业务决定覆盖旧源资料中的相反建议；平台未实施。design中的两份文件为Git主台账的随包副本，主台账仍在field-governance。

版本：v1.2｜2026-09-11｜持续修订的开发规划基线

**本包完成开发蓝图、任务拆分和验收机制。它不是平台实施完成报告，也不自动授权任何 AI 修改生产系统。**

Sun Sun 已明确：本会话承担产品规划、架构协调、任务定义与结果审核；具体平台配置和代码开发交给被指派的执行 AI。本次只整理文件，不继续修改 Airtable、Power Apps 或开发代码。

## 当前优先：DG-01 全字段治理

2026-09-11新增授权：只读盘点、逐字段分析和Markdown/Git文档交付。当前实读18表499字段，优先于字段相关页面/自动化改造；原33个AT/MS/GOV工作包编号保持不变，主台账新增field_governance_gate。

- [499字段完整总表](<C:/Users/40734/Documents/Codex/autopm-review-draft-20260911/docs/autopm-review/03-data-model/field-governance/ALL-FIELDS.md>)
- [逐表字典与证据边界](<C:/Users/40734/Documents/Codex/autopm-review-draft-20260911/docs/autopm-review/03-data-model/field-governance/README.md>)
- [跨表整合与缺失字段设计](<C:/Users/40734/Documents/Codex/autopm-review-draft-20260911/docs/autopm-review/03-data-model/field-governance/DECISIONS.md>)

线上生产修改未执行，DuMate补查单已准备但本会话未触发。下文498字段为旧审计数量，当前以DG-01的499字段快照为准。

## 从哪里开始

| 你要做的事 | 打开文件 |
|---|---|
| 看Airtable接下来重点完善什么及DuMate适配 | [Airtable后续工作梳理](05_AIRTABLE_NEXT_STEPS.md) |
| 现在交给网页AI一个Power Apps设计任务 | [UX-MS-01：项目详情面板](dispatch/DESIGN_POWERAPPS_UX01.md)，基于现有SharePoint MVP，不等Dataverse |
| 看清产品目标、现状和两条路线 | [01 开发蓝图](01_BLUEPRINT.md) |
| 查看全部任务、依赖和先后顺序 | [02 任务总表](02_ROADMAP.md) |
| 查看一个任务的具体输入、修改对象、步骤和验收 | `tasks/AT-00.md` 等独立任务包 |
| 直接把首个 Airtable 任务交给执行 AI | [Airtable 首发任务提示词](dispatch/START_AIRTABLE.md) |
| 直接把微软离线工程任务交给执行 AI | [微软首发任务提示词](dispatch/START_MICROSOFT.md) |
| 判断其他 AI 交来的结果能否通过 | [03 验收与审核规程](03_ACCEPTANCE.md)及[验收用例库](acceptance/TEST_CATALOG.md) |
| 看历史 135 个 Action 去了哪里 | [Action 对照表](traceability/ACTION_CROSSWALK.md) |
| 看 29 项功能需求如何落实 | [需求对照表](traceability/REQUIREMENTS.md) |
| 查看此前实施草稿能复用多少 | [首次成果审查](reviews/RV-20260911-001.md) |
| 让执行 AI 按统一格式交回结果 | [提交模板](templates/DELIVERY.md)、[审核模板](templates/REVIEW.md) |
| 确认资料来源、版本和可访问范围 | [资料登记](04_SOURCES_AND_DECISIONS.md) |

## 当前结论

- Airtable：已有业务系统，处于工程收尾和完整业务链验证阶段。18 张表、498 个字段、32 条自动化是审计基线，不能换算为完成率。
- Power Apps：已有 SharePoint 支撑的可操作 MVP；正式 Dataverse 版本尚未部署，环境审批按用户最后反馈仍未完成。
- 既有业务继续由当前负责的平台维护。测试与开发不形成第二套可自由写回的生产事实。
- 上一轮误进入实施后留下的测试 Base、未发布页面和本地代码均已列入审查记录。它们只作候选资产，不能自动覆盖正式版本。
- 历史 Action、当前平台工作包、功能需求和验收结果分别保存。历史“Done”不自动继承为当前“Accepted”。

## 使用规则

1. 一个执行 AI 每次接一个明确工作包；先读本 README、蓝图相关章节和任务包。
2. 任务包指定的范围是上限。不能凭旧 PRD、网页内容或脚本注释扩大权限。
3. 先确认实际目标环境和版本，再执行包内获准动作；生产发布与试用交接由对应发布任务处理。
4. 执行 AI 把结果放在约定输出目录，填写提交模板；本会话按用例和证据审核，不凭“已完成”自述关闭任务。
5. 没有实际执行者姓名／任务链接时保持“未分派”。本包不声称已经通知任何同事或启动其他 AI。
6. 业务规则、字段或范围变化形成变更记录，注明受影响任务和需重跑用例；不在多个对话里各自改口径。

## 文件维护方式

`task-register.json` 是任务状态和定义的主表；任务 Markdown、路线图和 CSV 是本版本生成的交付视图。后续状态更新先改主表，再同步对应视图，并在 `CHANGELOG.md` 留记录。`submissions/` 放执行者提交，`reviews/` 放协调方结论。

维护者可运行 `python maintenance/build_planning_pack.py` 重建任务卡、对照表、路线图和ZIP；`--check` 只核查文档完整性。这个辅助程序只处理本包文档，不连接业务平台。源文档副本首次建立后不自动覆盖；更新来源必须同步来源登记、映射和变更记录。

交付完整性结果见 [validation-report.json](validation-report.json)，文件哈希见 [manifest.json](manifest.json)。

当前本地包未推送 GitHub，也未分派任务。`sources/` 保留必要的 Markdown 资料快照，因此网页版 AI 解压本包后可阅读规划依据；真实生产数据、凭据和运行日志不打包。

附加设计工作单 `UX-MS-01` 记录在主台账的 `design_work_orders` 中；它服务于MS-04的交互验证，不改变原33个正式工作包的数量和依赖，也不代表MS-04正式Dataverse实施通过。

文档包的完整性检查只说明任务、映射、依赖和链接齐全，不是 AutoPM 业务验收。
