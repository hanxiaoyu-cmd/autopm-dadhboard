# AutoPM_Phase1_Engineering_Closure_Plan_2026-08-29 1

> 状态：持续修订的工作资料，非最终规格、非开发授权。历史状态和日期须结合最新审计复核。


来源：`AutoPM_Phase1_Engineering_Closure_Plan_2026-08-29 1.xlsx`。逐工作表、逐非空行保留内容；列字母和行号对应原Excel。公式单元格同时记录公式和已有缓存值，未重新计算。图片、版式、条件格式不包含在文本提取中。

## 分析与规划_0829

### Row 1

**A1**

AutoPM Phase 1｜线性分析 → 收尾规划 → 工程执行输入

### Row 2

**A2**

更新日期：2026-08-29｜目标：聚焦开发收尾，不重复泛化功能清单；工程负责实现、稳定性与上线证据，业务负责规则确认与验收。

单元格批注：文件依据已附资料与企业搜索结果更新。建议日期是收尾规划，不代表已承诺日期；所有当前值保持TBD，避免把目标误写成成果。

### Row 4

**A4**

分析层

**B4**

已确认事实 / 约束

**C4**

影响

**D4**

必须做的决定

**E4**

工程主导输出

**F4**

业务/领导输入

**G4**

完成判定

**H4**

证据来源

**I4**

置信度

**J4**

备注

### Row 5

**A5**

1 目标

**B5**

Phase 1的下一证明点是约20个XPT项目完成Project→Task→Issue→Recovery Action→Owner→Weekly Summary端到端运行。

**C5**

不能继续以“页面已建成”代替“流程已成功”。

**D5**

把Phase 1定义为可运行、可验收、可回退的闭环。

**E5**

端到端数据链路、状态规则、自动化日志和UAT证据。

**F5**

锁定20个项目、试点用户及每周更新节奏。

**G5**

20个项目均有真实任务/问题/行动/Owner，并能生成周报草稿。

**H5**

AutoPM Phase1 Status Update；AutoPM reporting

**I5**

高

**J5**

目标为已确认；实际项目数需在系统中复核。

### Row 6

**A6**

2 数据

**B6**

已存在核心表、界面和自动化，但字段仍杂乱，PMO链接未完成，仅少数项目含详细真实数据。

**C6**

自动化和报表会放大脏数据，先做功能会重复返工。

**D6**

先冻结最小数据字典和唯一键，再改自动化。

**E6**

Project/SKU/Task/Issue唯一标识；必填字段；Owner规则；数据质量检查。

**F6**

确认Programme/Project/SKU业务边界以及官方系统归属。

**G6**

关键字段完整率达到验收阈值；无关键重复；引用关系可追溯。

**H6**

Phase1 Status Update；PMO Integration meeting

**I6**

高

**J6**

阈值在验收表中作为目标，不冒充当前结果。

### Row 7

**A7**

3 执行闭环

**B7**

当前痛点集中在任务责任、截止日期、问题根因、恢复行动和关闭标准不完整。

**C7**

任务能创建但不能闭环，系统仍是另一张表。

**D7**

P0建设Task和Issue的最小强制字段及升级逻辑。

**E7**

Task Owner/Due Date/Status；Issue Severity/MP Impact/Root Cause/Recovery/Owner/Target Date/Closure Evidence。

**F7**

确认责任分配规则和关闭条件。

**G7**

每个开放问题都有恢复行动与责任人；关闭项有证据。

**H7**

Airtable MVP Roadmap；Pilot meeting

**I7**

高

**J7**

AI预测推迟，先做可解释规则。

### Row 8

**A8**

4 报告与集成

**B8**

领导方向是PMO Dashboard用于组合总览，AutoPM用于项目执行细节；重复维护Weekly Report、All Projects Tracker和AutoPM阻碍采用。

**C8**

不解决同步与周报，真实使用不会发生。

**D8**

按阶段先做单向、可审计同步，暂不强行重构所有上游系统。

**E8**

字段映射、增量同步、异常队列、重跑和对账；Weekly Summary 2.0。

**F8**

确认源系统、发布节奏、周报格式和审批人。

**G8**

同一项目关键状态在AutoPM与Tracker对账一致；周报可复制发送。

**H8**

AutoPM reporting；PMO Integration meeting

**I8**

高

**J8**

双向同步不是Phase 1必需条件。

### Row 9

**A9**

5 稳定性与权限

**B9**

中国团队存在登录、刷新和加载问题；权限、自动化维护及支持能力尚未完善。

**C9**

即便功能正确，访问不稳定也会导致试点失败。

**D9**

把可用性、权限和故障处理列为P0上线门槛。

**E9**

账号测试矩阵、最小权限、失败日志、重试/降级、支持Runbook。

**F9**

提供试点账号名单、网络场景和问题样本。

**G9**

试点账号可执行所需动作；关键自动化失败可见、可重跑。

**H9**

Airtable support email；Airtable meeting

**I9**

高

**J9**

外部平台根因仍需供应商确认。

### Row 10

**A10**

6 范围控制

**B10**

已确认MVP包括项目摘要、周报草稿、Issue分类、Follow-up草稿；自动风险预测、自动改状态、自动审批/关闭延后。

**C10**

若把黑箱AI和跨系统知识检索塞进收尾阶段，会增加风险。

**D10**

Phase 1只完成可解释、可人工确认的AI辅助。

**E10**

AI输出草稿、来源字段、人工确认、错误反馈入口。

**F10**

确认允许的AI模型与数据合规范围。

**G10**

AI输出不自动覆盖权威字段；全部可人工确认和追溯。

**H10**

Kickoff Agenda；Airtable meeting

**I10**

高

**J10**

严格遵守中国环境合规限制。

### Row 11

**A11**

7 上线策略

**B11**

当前处于技术验证末期，周使用尚不稳定；用户仍管理两个系统。

**C11**

不能直接宣布全量切换。

**D11**

采用“工程收尾→UAT→20项目运行→Gate决定”的线性Gate。

**E11**

发布候选版本、数据备份、回退方案、缺陷分级、上线日志。

**F11**

领导确认Gate、试点用户承诺和切换规则。

**G11**

P0=0；P1有明确处置；关键流程通过；回退演练完成。

**H11**

Phase1 Status Update；AutoPM reporting

**I11**

高

**J11**

日期为建议计划，不代表承诺。

### Row 14

**A14**

线性收尾路径（禁止并行发散）

### Row 15

**A15**

Gate

**B15**

阶段

**C15**

建议开始

**D15**

建议完成

**E15**

主导

**F15**

退出条件

### Row 16

**A16**

Gate 0

**B16**

范围与数据规则冻结

**C16**

2026-08-31

**D16**

2026-09-02

**E16**

工程 + 产品Owner

**F16**

P0范围、数据字典、唯一键、验收阈值签字

### Row 17

**A17**

Gate 1

**B17**

数据与核心闭环修复

**C17**

2026-09-03

**D17**

2026-09-09

**E17**

工程主导

**F17**

Project/Task/Issue数据质量与闭环规则通过单元测试

### Row 18

**A18**

Gate 2

**B18**

自动化、周报与同步稳定

**C18**

2026-09-10

**D18**

2026-09-16

**E18**

工程主导

**F18**

关键自动化可监控可重跑；周报与Tracker对账

### Row 19

**A19**

Gate 3

**B19**

20项目UAT与缺陷收口

**C19**

2026-09-17

**D19**

2026-09-23

**E19**

工程 + 试点用户

**F19**

20项目端到端运行；P0清零；P1有处置

### Row 20

**A20**

Gate 4

**B20**

上线/回退与Phase 1评审

**C20**

2026-09-24

**D20**

2026-09-25

**E20**

工程 + 领导Gate

**F20**

发布证据、回退方案、价值基线和下一阶段决策

## 开发计划_工程主导

### Row 1

**A1**

AutoPM Phase 1｜工程主导开发收尾计划

### Row 2

**A2**

排序原则：先数据，再闭环，再自动化/集成，再体验，最后UAT与发布。日期为建议计划，未确认Owner保留“TBD”，不虚构责任人。

### Row 3

**A3**

P0总数

**B3**

=COUNTIF(B6:B23,"P0")

缓存值：16

**D3**

已完成

**E3**

=COUNTIF(N6:N23,"已完成")

缓存值：0

**G3**

进行中

**H3**

=COUNTIF(N6:N23,"进行中")

缓存值：0

**J3**

受阻

**K3**

=COUNTIF(N6:N23,"受阻")

缓存值：0

**M3**

总体完成率

**N3**

=IFERROR(AVERAGE(O6:O23),0)

缓存值：0

### Row 5

**A5**

序号

**B5**

优先级

**C5**

工作流

**D5**

功能/工作包

**E5**

问题与目的

**F5**

工程范围（详细）

**G5**

明确不做

**H5**

前置依赖

**I5**

工程主导角色

**J5**

业务验收角色

**K5**

建议开始

**L5**

建议完成

**M5**

工期(工作日)

**N5**

状态

**O5**

完成率

**P5**

退出/验收标准

**Q5**

验证方法

**R5**

交付物

**S5**

风险

**T5**

缓解措施

**U5**

来源/依据

**V5**

Gate

**W5**

阻塞项

**X5**

备注

### Row 6

**A6**

1

**B6**

P0

**C6**

治理

**D6**

冻结Phase 1范围与DoD

**E6**

防止收尾阶段继续加功能，确保每项工作可验收。

**F6**

建立P0/P1清单；定义Definition of Done、缺陷分级、Gate退出条件；将未确认需求放入P2 Backlog。

**G6**

预测性风险、自动审批、跨系统知识检索、全组织资源优化。

**H6**

领导确认Phase 1目标；20项目名单。

**I6**

Engineering Lead

**J6**

Product Owner / Leadership

**K6**

2026-08-31

**L6**

2026-09-01

**M6**

2

**N6**

未开始

**O6**

0

**P6**

范围、DoD、Gate、变更流程均有书面版本并签字。

**Q6**

评审纪要；变更请求抽样。

**R6**

Scope baseline；DoD；Backlog

**S6**

持续插单

**T6**

只有P0阻断可进入；其他转P2。

**U6**

Kickoff Agenda；Phase1 Status Update

**V6**

G0

### Row 7

**A7**

2

**B7**

P0

**C7**

数据

**D7**

数据字典与系统归属冻结

**E7**

Programme/Project/SKU/Task/Issue混用将导致同步、自动化和报表错误。

**F7**

定义对象、字段、类型、枚举、必填、Owner、权威来源、更新权限；Project中心关联Task/Milestone/Risk/Issue；SharePoint保存文档，AutoPM保存链接。

**G7**

重新设计所有企业主数据。

**H7**

PMO/PLM字段清单；业务对象确认。

**I7**

Data Engineer / Airtable Builder

**J7**

APAC Product Owner + PMO

**K7**

2026-08-31

**L7**

2026-09-02

**M7**

3

**N7**

未开始

**O7**

0

**P7**

关键字段无同义重复；每字段有Owner和Source of Truth。

**Q7**

字段审计；样例项目走查；schema diff。

**R7**

Data Dictionary v1；Mapping

**S7**

上游口径不一致

**T7**

保留映射层，不修改上游字段。

**U7**

Kickoff Agenda；PMO Integration meeting

**V7**

G0

### Row 8

**A8**

3

**B8**

P0

**C8**

数据

**D8**

唯一ID与关联完整性

**E8**

无稳定ID会导致重复项目、孤立Issue和错误同步。

**F8**

实现稳定Project ID；定义SKU-Factory粒度；Task/Issue关联Project；建立孤儿记录、重复键和空键检查。

**G8**

一次性解决所有历史主数据问题。

**H8**

数据字典冻结。

**I8**

Data Engineer

**J8**

Product Owner + PMO

**K8**

2026-09-03

**L8**

2026-09-05

**M8**

3

**N8**

未开始

**O8**

0

**P8**

新增记录ID唯一；关键关系无孤儿；历史异常进入清单。

**Q8**

唯一性查询；关联完整性脚本；抽样10项目。

**R8**

ID规则；修复脚本；异常清单

**S8**

历史数据缺失

**T8**

不猜测补值；标为待业务确认。

**U8**

Phase1 Status Update；PMO Integration meeting

**V8**

G1

### Row 9

**A9**

4

**B9**

P0

**C9**

数据

**D9**

关键字段质量门禁

**E9**

真实项目详细数据不足，周报与AI输出不可信。

**F9**

为Project、Task、Issue设置最小必填；数据质量评分；导入前校验；缺失项队列；禁止不完整记录进入周报。

**G9**

对非关键字段强制100%完整。

**H9**

唯一ID完成。

**I9**

Data Engineer / QA

**J9**

Pilot Leads

**K9**

2026-09-04

**L9**

2026-09-08

**M9**

3

**N9**

未开始

**O9**

0

**P9**

关键字段完整率达到验收表目标；缺失记录可定位到Owner。

**Q9**

质量检查脚本；20项目基线报告。

**R9**

DQ规则；质量报告；修复队列

**S9**

规则过严阻碍录入

**T9**

仅关键字段阻断，次要字段预警。

**U9**

Airtable MVP Roadmap；Phase1 Status Update

**V9**

G1

### Row 10

**A10**

5

**B10**

P0

**C10**

任务

**D10**

任务模板与默认Owner规则

**E10**

模板名称不一致、Owner手工选择会增加工作而非减少工作。

**F10**

按Project Type建立模板版本；字段名规范；根据部门/任务类型映射默认Owner；允许人工覆盖并记录原因；支持导入映射。

**G10**

复杂子任务层级全面重构。

**H10**

数据字典；业务模板确认。

**I10**

Automation Engineer

**J10**

NPI/XPT Process Expert

**K10**

2026-09-05

**L10**

2026-09-09

**M10**

3

**N10**

未开始

**O10**

0

**P10**

测试项目生成准确任务；无重复；默认Owner可解释；覆盖可审计。

**Q10**

至少3种项目类型自动生成测试；重复检测。

**R10**

Template v1；Owner Matrix；测试日志

**S10**

不同项目差异大

**T10**

首批只覆盖试点项目类型。

**U10**

AutoPM introduction meeting；Phase1 Status Update

**V10**

G1

### Row 11

**A11**

6

**B11**

P0

**C11**

问题

**D11**

Issue Closure Board闭环

**E11**

Issue记录若无根因、恢复行动、Owner、Target Date，无法推动关闭。

**F11**

标准化Severity、MP Impact、Root Cause、Recovery Action、Owner、Target Date、Status、Closure Evidence；状态转换校验；关闭前检查。

**G11**

AI自动关闭或自动改权威状态。

**H11**

数据字典；关闭规则确认。

**I11**

Backend/Automation Engineer

**J11**

Pilot Lead / Quality

**K11**

2026-09-03

**L11**

2026-09-08

**M11**

4

**N11**

未开始

**O11**

0

**P11**

所有开放问题均有Owner与恢复行动或明确例外；关闭项有证据。

**Q11**

开放/关闭/重开/延期场景测试。

**R11**

Issue board；状态机；关闭校验

**S11**

用户跳过字段

**T11**

在状态转换时阻断并给出提示。

**U11**

Airtable MVP Roadmap；Phase1 Status Update

**V11**

G1

### Row 12

**A12**

7

**B12**

P0

**C12**

自动化

**D12**

核心自动化逐条审计

**E12**

现有自动化已能运行，但尚未逐条复核，失败可能静默发生。

**F12**

建立自动化清单、触发器、输入输出、Owner、失败处理、运行日志；对模板生成、进度同步、里程碑提醒、周报草稿做回归测试。

**G12**

一次性优化所有低频自动化。

**H12**

P0流程规则冻结。

**I12**

Automation Engineer

**J12**

Product Owner

**K12**

2026-09-06

**L12**

2026-09-10

**M12**

3

**N12**

未开始

**O12**

0

**P12**

P0自动化均有测试、日志、Owner、重跑方法；无静默失败。

**Q12**

正向、空值、重复触发、权限失败测试。

**R12**

Automation Register；Test Pack；Runbook

**S12**

重复触发/循环

**T12**

幂等键、触发条件和去重锁。

**U12**

Phase1 Status Update

**V12**

G2

### Row 13

**A13**

8

**B13**

P0

**C13**

提醒

**D13**

Task/Risk分级提醒与升级

**E13**

任务和风险提醒不完整，PM仍需手动追问。

**F13**

定义到期前、到期、逾期、MP Impact四级规则；合并通知避免邮件轰炸；支持直接链接更新；记录发送与确认状态。

**G13**

向所有人高频发送单条邮件。

**H13**

Owner/Due Date规则；权限测试。

**I13**

Automation Engineer

**J13**

Pilot Users

**K13**

2026-09-09

**L13**

2026-09-12

**M13**

3

**N13**

未开始

**O13**

0

**P13**

提醒准确到人；无重复轰炸；逾期未处理按规则升级。

**Q13**

模拟日期；收件人矩阵；邮件/链接实测。

**R13**

Reminder rules；Template；Log

**S13**

通知疲劳

**T13**

摘要式批量提醒；可配置频次。

**U13**

Airtable meeting；Phase1 Status Update

**V13**

G2

### Row 14

**A14**

9

**B14**

P0

**C14**

报告

**D14**

Weekly Summary 2.0

**E14**

当前周报只是草稿，格式粗糙，不能替代手工报告。

**F14**

按项目、Owner、风险和MP Impact聚合；明确本周变化、关键问题、恢复行动、决策请求；数据缺失需标红；支持人工确认后发送。

**G14**

无人审核自动对外发送。

**H14**

数据质量门禁；Issue闭环。

**I14**

Reporting Engineer

**J14**

Leadership Reviewers

**K14**

2026-09-09

**L14**

2026-09-14

**M14**

4

**N14**

未开始

**O14**

0

**P14**

周报可直接复制/发送；关键数据可追溯；缺失不被隐藏。

**Q14**

与现有周报并排对比3期；字段追溯。

**R14**

Weekly Summary 2.0；对比报告

**S14**

格式偏好反复

**T14**

先锁定唯一模板，变更走Backlog。

**U14**

Phase1 Status Update；AutoPM reporting

**V14**

G2

### Row 15

**A15**

10

**B15**

P0

**C15**

集成

**D15**

AutoPM→All Projects Tracker单向同步

**E15**

重复维护是当前采用最大障碍。

**F15**

建立字段映射；增量同步；创建/更新/删除策略；异常队列；重跑；对账；保留源记录链接和时间戳。

**G15**

直接删除All Projects Tracker；未经验证的双向同步。

**H15**

数据字典；唯一ID；Tracker接口/文件权限。

**I15**

Integration Engineer

**J15**

PMO Data Owner

**K15**

2026-09-08

**L15**

2026-09-15

**M15**

6

**N15**

未开始

**O15**

0

**P15**

试点项目关键字段同步成功且可对账；失败可见、可重跑、不重复。

**Q15**

金样本；新增/更新/冲突/空值/断网测试。

**R15**

Mapping；Sync job；Reconciliation report

**S15**

上游列结构不能修改

**T15**

适配现有结构；写入前schema检查。

**U15**

AutoPM reporting；PMO Integration meeting

**V15**

G2

### Row 16

**A16**

11

**B16**

P0

**C16**

可靠性

**D16**

登录、刷新、加载与平台限制处置

**E16**

中国用户存在登录和数据刷新问题，影响真实采用。

**F16**

收集3–4用户环境矩阵；浏览器控制台/时间/网络信息；定义重试、刷新、降级和故障公告；与Airtable support跟踪。

**G16**

声称已找到供应商根因。

**H16**

试点用户配合；供应商支持。

**I16**

Platform Engineer

**J16**

China Pilot Lead

**K16**

2026-08-31

**L16**

2026-09-16

**M16**

13

**N16**

未开始

**O16**

0

**P16**

关键场景可复现或明确不可复现；有缓解方案、支持入口和用户说明。

**Q16**

多账号/浏览器/VPN与非VPN矩阵测试。

**R16**

Incident log；Support case；Mitigation guide

**S16**

外部平台不可控

**T16**

准备导出/缓存/人工回退流程。

**U16**

Airtable support email

**V16**

G2

### Row 17

**A17**

12

**B17**

P0

**C17**

权限

**D17**

最小权限与外部参与链接

**E17**

关键Owner不在系统内时，任务分配和更新中断。

**F17**

定义Creator/Editor/Commenter/Viewer矩阵；试点账号批量验证；链接更新最小字段；禁止越权访问。

**G17**

Phase 1一次覆盖全部跨职能用户。

**H17**

账号名单；Airtable许可。

**I17**

Platform Engineer / Security

**J17**

Product Owner + Security

**K17**

2026-09-03

**L17**

2026-09-10

**M17**

6

**N17**

未开始

**O17**

0

**P17**

所有试点用户可完成其动作且看不到不应访问的数据。

**Q17**

角色矩阵场景测试；负向访问测试。

**R17**

Access Matrix；Provisioning list；Test record

**S17**

许可不足

**T17**

优先轻量参与，核心用户完整许可。

**U17**

Kickoff Agenda；Phase1 Status Update

**V17**

G2

### Row 18

**A18**

13

**B18**

P1

**C18**

界面

**D18**

PM Daily Work与Owner Action List收口

**E18**

界面已存在但需按真实使用反馈减少点击与遗漏。

**F18**

统一Today/Overdue/Risk Action/Pending Confirmation；个性化过滤；快速更新；移动/低速网络可用性。

**G18**

新建大量漂亮页面。

**H18**

任务、提醒、权限稳定。

**I18**

Frontend/Airtable Builder

**J18**

Pilot Users

**K18**

2026-09-12

**L18**

2026-09-16

**M18**

3

**N18**

未开始

**O18**

0

**P18**

核心动作在3次点击内完成；用户无需全表搜索。

**Q18**

5名用户任务测试；点击路径记录。

**R18**

Daily Cockpit v1；Usability notes

**S18**

个性偏好冲突

**T18**

根据角色统一最小入口。

**U18**

Airtable MVP Roadmap；Phase1 Status Update

**V18**

G2

### Row 19

**A19**

14

**B19**

P1

**C19**

AI

**D19**

AI项目摘要与Follow-up草稿

**E19**

需要AI辅助但不能在数据不全时给出错误结论。

**F19**

只使用结构化权威字段；标注更新时间与缺失；生成状态/风险/下一步；人工确认后复制或发送；记录反馈。

**G19**

预测性风险、自动状态修改、自动审批。

**H19**

数据质量；合规模型可用。

**I19**

AI/Automation Engineer

**J19**

Product Owner + Compliance

**K19**

2026-09-13

**L19**

2026-09-18

**M19**

4

**N19**

未开始

**O19**

0

**P19**

输出可追溯、可人工修改；不覆盖权威字段；错误反馈可记录。

**Q19**

20项目摘要抽样；事实一致性检查。

**R19**

Prompt/Agent config；Evaluation set

**S19**

幻觉/上下文不足

**T19**

缺失即提示，不推断；人工确认。

**U19**

Kickoff Agenda；Airtable meeting

**V19**

G3

### Row 20

**A20**

15

**B20**

P0

**C20**

测试

**D20**

端到端UAT测试包

**E20**

没有统一测试，无法证明Phase 1完成。

**F20**

覆盖Project创建、模板任务、Owner分配、Issue闭环、提醒、周报、Tracker同步、权限、失败恢复；定义证据格式。

**G20**

只做演示截图。

**H20**

P0功能完成。

**I20**

QA Lead

**J20**

20项目Pilot Users

**K20**

2026-09-16

**L20**

2026-09-22

**M20**

5

**N20**

未开始

**O20**

0

**P20**

所有P0场景通过；失败均有缺陷ID、Owner、计划。

**Q20**

UAT脚本；实际项目执行；证据链接。

**R20**

UAT pack；Defect log；Sign-off

**S20**

测试数据不真实

**T20**

每个场景绑定真实试点项目。

**U20**

Phase1 Status Update；Kickoff Agenda

**V20**

G3

### Row 21

**A21**

16

**B21**

P0

**C21**

发布

**D21**

监控、回退与支持Runbook

**E21**

试点期间一个人维护不可扩展，发布后问题无法快速定位。

**F21**

关键自动化和同步监控；失败告警；备份/导出；回退步骤；支持分级；值守Owner；已知问题清单。

**G21**

建立完整企业SRE体系。

**H21**

自动化/集成完成。

**I21**

Engineering Lead / Platform Engineer

**J21**

Product Owner

**K21**

2026-09-18

**L21**

2026-09-23

**M21**

4

**N21**

未开始

**O21**

0

**P21**

一次回退演练成功；P0故障有明确处理路径；关键数据可恢复。

**Q21**

故障注入；关闭连接；错误字段；回退演练。

**R21**

Runbook；Rollback plan；Monitoring list

**S21**

单人依赖

**T21**

至少1名备份工程支持。

**U21**

Phase1 Status Update

**V21**

G3

### Row 22

**A22**

17

**B22**

P0

**C22**

采用

**D22**

20项目运行切换

**E22**

真实使用而非临时测试是Phase 1核心。

**F22**

迁移20项目；校验Owner、Due Date、Issue、链接；设定周二更新/周五周报；冻结重复维护方式；收集使用日志。

**G22**

立即迁移全部XPT项目。

**H22**

UAT通过；用户名单；培训。

**I22**

Engineering Support Lead

**J22**

Pilot Team Lead

**K22**

2026-09-17

**L22**

2026-09-23

**M22**

5

**N22**

未开始

**O22**

0

**P22**

20项目每周有真实更新；闭环链路可见；重复维护规则明确。

**Q22**

活跃记录；更新日志；周报对账。

**R22**

Migration log；Adoption dashboard

**S22**

用户忙、双系统

**T22**

试点团队整组切换；明确单一更新入口。

**U22**

Phase1 Status Update；AutoPM reporting

**V22**

G3

### Row 23

**A23**

18

**B23**

P0

**C23**

Gate

**D23**

Phase 1证据包与决策评审

**E23**

需要用业务结果而非页面数量决定是否扩大。

**F23**

汇总真实项目数、活跃用户、数据质量、问题闭环、周报效率基线、风险提前暴露案例、已知限制；提出Go/Fix/Stop建议。

**G23**

把目标值表述成已实现结果。

**H23**

20项目运行；UAT结果。

**I23**

Engineering Lead + Product Owner

**J23**

Leadership Gate

**K23**

2026-09-24

**L23**

2026-09-25

**M23**

2

**N23**

未开始

**O23**

0

**P23**

所有结论均有证据链接；未达到项明确Gap/Owner/日期；Gate决定记录。

**Q23**

证据抽样；指标重算；评审签字。

**R23**

Phase1 Evidence Pack；Gate decision

**S23**

指标定义变化

**T23**

评审前冻结指标口径。

**U23**

Peter/Jen meeting；Airtable MVP Roadmap

**V23**

G4

## RACI与验收

### Row 1

**A1**

AutoPM Phase 1｜RACI与验收基线

### Row 2

**A2**

原则：工程对“实现正确、稳定、可监控、可回退”负责；业务对“规则正确、数据真实、流程可用”负责；领导对Gate与范围取舍负责。

### Row 4

**A4**

工作域

**B4**

工程(A/R)

**C4**

产品Owner(A/R)

**D4**

试点用户(R/C)

**E4**

PMO/数据Owner(C)

**F4**

领导(I/A)

**G4**

主要输入

**H4**

主要输出

**I4**

验收指标

**J4**

目标值

**K4**

当前值

**L4**

证据链接

**M4**

结论

### Row 5

**A5**

范围与Gate

**B5**

R

**C5**

R

**D5**

C

**E5**

C

**F5**

A

**G5**

目标、约束、优先级

**H5**

Scope/DoD/Gate

**I5**

P0范围冻结

**J5**

100%

**K5**

TBD

### Row 6

**A6**

数据标准与ID

**B6**

A/R

**C6**

A

**D6**

C

**E6**

C

**F6**

I

**G6**

官方字段与样例

**H6**

字典、唯一键、质量规则

**I6**

关键字段完整率

**J6**

≥95%

**K6**

TBD

### Row 7

**A7**

任务与Issue闭环

**B7**

A/R

**C7**

A

**D7**

R

**E7**

C

**F7**

I

**G7**

流程规则与真实案例

**H7**

状态机、Owner、Recovery

**I7**

Open Issue有Recovery

**J7**

≥80%

**K7**

TBD

### Row 8

**A8**

MP影响可见性

**B8**

R

**C8**

A

**D8**

R

**E8**

C

**F8**

I

**G8**

MP影响判定

**H8**

Issue/Report标识

**I8**

MP-impact Issue可见率

**J8**

100%

**K8**

TBD

### Row 9

**A9**

自动化可靠性

**B9**

A/R

**C9**

C

**D9**

C

**E9**

I

**F9**

触发器与异常案例

**G9**

日志、重跑、Runbook

**H9**

P0自动化测试通过率

**I9**

100%

**J9**

TBD

### Row 10

**A10**

Tracker同步

**B10**

A/R

**C10**

C

**D10**

I

**E10**

A/R

**F10**

I

**G10**

字段映射、写入权限

**H10**

同步、异常队列、对账

**I10**

关键字段对账通过

**J10**

100%

**K10**

TBD

### Row 11

**A11**

周报输出

**B11**

R

**C11**

A

**D11**

C

**E11**

C

**F11**

A

**G11**

领导模板与判断

**H11**

Weekly Summary 2.0

**I11**

周报准备时间降低

**J11**

20–30%目标

**K11**

TBD

### Row 12

**A12**

真实采用

**B12**

C

**C12**

A

**D12**

R

**E12**

C

**F12**

A

**G12**

20项目与用户承诺

**H12**

运行日志、反馈

**I12**

每周活跃用户

**J12**

≥10目标

**K12**

TBD

### Row 13

**A13**

权限与可用性

**B13**

A/R

**C13**

C

**D13**

R

**E13**

I

**F13**

账号/环境矩阵

**G13**

权限矩阵、故障指南

**H13**

试点关键动作可执行

**I13**

100%

**J13**

TBD

### Row 14

**A14**

Phase 1 Gate

**B14**

R

**C14**

R

**D14**

C

**E14**

C

**F14**

A

**G14**

全部证据

**H14**

Go/Fix/Stop决策

**I14**

P0缺陷

**J14**

0

**K14**

TBD

## Phase 1 Map

### Row 1

**B1**

AutoPM Phase 1 | Target Map

### Row 3

**B3**

独立目标地图：只依据已确认的Phase 1目标、业务问题、边界和成功标准，不依据当前已开发页面反推。

### Row 5

**D5**

PHASE 1 目标
让真实 XPT / NPI 项目持续运行，验证可信执行数据、执行闭环、真实采用和业务价值

### Row 9

**B9**

产品主链：可信事实  →  有效执行  →  用户行动

### Row 10

**B10**

="M1  执行数据基础 | 可信事实"&CHAR(10)&COUNTIF('Task Execution'!$B$8:$B$1000,"M1")&"项｜执行完成"&COUNTIFS('Task Execution'!$B$8:$B$1000,"M1",'Task Execution'!$O$8:$O$1000,"已完成")&"｜检查完成"&COUNTIFS('Implementation Check'!$A$8:$A$1000,"M1",'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：M1  执行数据基础 | 可信事实
25项｜执行完成0｜检查完成0

**F10**

="M2  项目执行与问题闭环 | 有效执行"&CHAR(10)&COUNTIF('Task Execution'!$B$8:$B$1000,"M2")&"项｜执行完成"&COUNTIFS('Task Execution'!$B$8:$B$1000,"M2",'Task Execution'!$O$8:$O$1000,"已完成")&"｜检查完成"&COUNTIFS('Implementation Check'!$A$8:$A$1000,"M2",'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：M2  项目执行与问题闭环 | 有效执行
33项｜执行完成0｜检查完成0

**J10**

="M3  工作与管理入口 | 用户行动"&CHAR(10)&COUNTIF('Task Execution'!$B$8:$B$1000,"M3")&"项｜执行完成"&COUNTIFS('Task Execution'!$B$8:$B$1000,"M3",'Task Execution'!$O$8:$O$1000,"已完成")&"｜检查完成"&COUNTIFS('Implementation Check'!$A$8:$A$1000,"M3",'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：M3  工作与管理入口 | 用户行动
16项｜执行完成0｜检查完成0

### Row 11

**B11**

M1.1  业务对象定义
M1.2  对象关系模型
M1.3  唯一标识与映射
M1.4  字段与状态标准
M1.5  数据来源与责任
M1.6  真实项目数据初始化
M1.7  数据质量与审计

**F11**

M2.1  项目进入与初始化
M2.2  计划与任务建立
M2.3  日常执行与更新
M2.4  异常识别与记录
M2.5  恢复行动与升级
M2.6  管理决策
M2.7  结果确认与验证关闭
M2.8  历史与经验沉淀

**J11**

M3.1  个人执行入口
M3.2  项目管理入口
M3.3  异常处理入口
M3.4  周度管理入口
M3.5  领导审查与下钻
M3.6  用户体验与动作效率

### Row 21

**B21**

横向保障：稳定运行  +  真实采用  +  证据验证

### Row 22

**B22**

="M4  自动化、集成与运行保障 | 稳定运行"&CHAR(10)&COUNTIF('Task Execution'!$B$8:$B$1000,"M4")&"项｜执行完成"&COUNTIFS('Task Execution'!$B$8:$B$1000,"M4",'Task Execution'!$O$8:$O$1000,"已完成")&"｜检查完成"&COUNTIFS('Implementation Check'!$A$8:$A$1000,"M4",'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：M4  自动化、集成与运行保障 | 稳定运行
29项｜执行完成1｜检查完成1

**F22**

="M5  Pilot运行与采用 | 真实采用"&CHAR(10)&COUNTIF('Task Execution'!$B$8:$B$1000,"M5")&"项｜执行完成"&COUNTIFS('Task Execution'!$B$8:$B$1000,"M5",'Task Execution'!$O$8:$O$1000,"已完成")&"｜检查完成"&COUNTIFS('Implementation Check'!$A$8:$A$1000,"M5",'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：M5  Pilot运行与采用 | 真实采用
18项｜执行完成1｜检查完成1

**J22**

="M6  价值证据与Gate决策 | 证据验证"&CHAR(10)&COUNTIF('Task Execution'!$B$8:$B$1000,"M6")&"项｜执行完成"&COUNTIFS('Task Execution'!$B$8:$B$1000,"M6",'Task Execution'!$O$8:$O$1000,"已完成")&"｜检查完成"&COUNTIFS('Implementation Check'!$A$8:$A$1000,"M6",'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：M6  价值证据与Gate决策 | 证据验证
14项｜执行完成0｜检查完成0

### Row 23

**B23**

M4.1  数据导入与初始化自动化
M4.2  状态与异常计算
M4.3  提醒与升级
M4.4  报告生成
M4.5  PMO主数据连接
M4.6  权限与审计
M4.7  运行监控与失败恢复

**F23**

M5.1  Pilot范围确认
M5.2  角色与责任
M5.3  使用规则
M5.4  双系统过渡
M5.5  角色上手
M5.6  周度运行节奏
M5.7  用户支持与问题处理

**J23**

M6.1  基线定义
M6.2  使用与采用证据
M6.3  数据质量证据
M6.4  执行闭环证据
M6.5  效率与业务结果
M6.6  平台能力评估
M6.7  Gate 1决策

### Row 33

**E33**

↓  展开为可执行任务  ↓
Task Execution：Action ID、简单解释、产出、验收、Owner、日期、状态和证据

超链接：'Task Execution'!A7

### Row 38

**D38**

IMPLEMENTATION CHECK
目标任务确定后，再对比当前开发成果；当前实现不改变Target Map。

超链接：'Implementation Check'!A7

### Row 43

**B43**

PHASE 1 统计与导航

### Row 44

**B44**

实时关联 Task Execution 与 Implementation Check：更新任务状态后，KPI、模块进度和地图模块标题会自动变化。

### Row 46

**B46**

任务总数

**E46**

模块总数

**H46**

任务执行完成率

**K46**

实施检查完成率

### Row 47

**B47**

=COUNTIF('Task Execution'!$F$8:$F$1000,"?*")

缓存值：135

**E47**

<openpyxl.worksheet.formula.ArrayFormula object at 0x0000017D7FD6DEE0>

缓存值：6

**H47**

=IFERROR(COUNTIF('Task Execution'!$O$8:$O$1000,"已完成")/COUNTIF('Task Execution'!$F$8:$F$1000,"?*"),0)

缓存值：0.014814814814814815

**K47**

=IFERROR(COUNTIF('Implementation Check'!$P$8:$P$1000,"已完成")/COUNTIF('Implementation Check'!$C$8:$C$1000,"?*"),0)

缓存值：0.014814814814814815

### Row 49

**B49**

任务清单实时总数

**E49**

来自任务模块列

**H49**

=COUNTIF('Task Execution'!$O$8:$O$1000,"已完成")&" / "&COUNTIF('Task Execution'!$F$8:$F$1000,"?*")&" 项已完成"

缓存值：2 / 135 项已完成

**K49**

=COUNTIF('Implementation Check'!$P$8:$P$1000,"已完成")&" / "&COUNTIF('Implementation Check'!$C$8:$C$1000,"?*")&" 项已完成"

缓存值：2 / 135 项已完成

### Row 51

**B51**

模块进度总览

### Row 53

**B53**

模块

**C53**

模块名称

**E53**

任务数

**F53**

执行完成

**G53**

执行率

**H53**

检查完成

**I53**

检查率

**J53**

剩余任务

**K53**

地图位置

### Row 54

**B54**

M1

**C54**

执行数据基础

**E54**

=COUNTIF('Task Execution'!$B$8:$B$1000,B54)

缓存值：25

**F54**

=COUNTIFS('Task Execution'!$B$8:$B$1000,B54,'Task Execution'!$O$8:$O$1000,"已完成")

缓存值：0

**G54**

=IFERROR(F54/E54,0)

缓存值：0

**H54**

=COUNTIFS('Implementation Check'!$A$8:$A$1000,B54,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**I54**

=IFERROR(H54/E54,0)

缓存值：0

**J54**

=E54-F54

缓存值：25

**K54**

上排左侧 B10:E18

### Row 55

**B55**

M2

**C55**

项目执行与问题闭环

**E55**

=COUNTIF('Task Execution'!$B$8:$B$1000,B55)

缓存值：33

**F55**

=COUNTIFS('Task Execution'!$B$8:$B$1000,B55,'Task Execution'!$O$8:$O$1000,"已完成")

缓存值：0

**G55**

=IFERROR(F55/E55,0)

缓存值：0

**H55**

=COUNTIFS('Implementation Check'!$A$8:$A$1000,B55,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**I55**

=IFERROR(H55/E55,0)

缓存值：0

**J55**

=E55-F55

缓存值：33

**K55**

上排中部 F10:I18

### Row 56

**B56**

M3

**C56**

工作与管理入口

**E56**

=COUNTIF('Task Execution'!$B$8:$B$1000,B56)

缓存值：16

**F56**

=COUNTIFS('Task Execution'!$B$8:$B$1000,B56,'Task Execution'!$O$8:$O$1000,"已完成")

缓存值：0

**G56**

=IFERROR(F56/E56,0)

缓存值：0

**H56**

=COUNTIFS('Implementation Check'!$A$8:$A$1000,B56,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**I56**

=IFERROR(H56/E56,0)

缓存值：0

**J56**

=E56-F56

缓存值：16

**K56**

上排右侧 J10:M18

### Row 57

**B57**

M4

**C57**

自动化、集成与运行保障

**E57**

=COUNTIF('Task Execution'!$B$8:$B$1000,B57)

缓存值：29

**F57**

=COUNTIFS('Task Execution'!$B$8:$B$1000,B57,'Task Execution'!$O$8:$O$1000,"已完成")

缓存值：1

**G57**

=IFERROR(F57/E57,0)

缓存值：0.034482758620689655

**H57**

=COUNTIFS('Implementation Check'!$A$8:$A$1000,B57,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：1

**I57**

=IFERROR(H57/E57,0)

缓存值：0.034482758620689655

**J57**

=E57-F57

缓存值：28

**K57**

下排左侧 B22:E30

### Row 58

**B58**

M5

**C58**

Pilot运行与采用

**E58**

=COUNTIF('Task Execution'!$B$8:$B$1000,B58)

缓存值：18

**F58**

=COUNTIFS('Task Execution'!$B$8:$B$1000,B58,'Task Execution'!$O$8:$O$1000,"已完成")

缓存值：1

**G58**

=IFERROR(F58/E58,0)

缓存值：0.05555555555555555

**H58**

=COUNTIFS('Implementation Check'!$A$8:$A$1000,B58,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：1

**I58**

=IFERROR(H58/E58,0)

缓存值：0.05555555555555555

**J58**

=E58-F58

缓存值：17

**K58**

下排中部 F22:I30

### Row 59

**B59**

M6

**C59**

价值证据与Gate决策

**E59**

=COUNTIF('Task Execution'!$B$8:$B$1000,B59)

缓存值：14

**F59**

=COUNTIFS('Task Execution'!$B$8:$B$1000,B59,'Task Execution'!$O$8:$O$1000,"已完成")

缓存值：0

**G59**

=IFERROR(F59/E59,0)

缓存值：0

**H59**

=COUNTIFS('Implementation Check'!$A$8:$A$1000,B59,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**I59**

=IFERROR(H59/E59,0)

缓存值：0

**J59**

=E59-F59

缓存值：14

**K59**

下排右侧 J22:M30

### Row 60

**B60**

总计

**C60**

Phase 1

**E60**

=SUM(E54:E59)

缓存值：135

**F60**

=SUM(F54:F59)

缓存值：2

**G60**

=IFERROR(F60/E60,0)

缓存值：0.014814814814814815

**H60**

=SUM(H54:H59)

缓存值：2

**I60**

=IFERROR(H60/E60,0)

缓存值：0.014814814814814815

**J60**

=SUM(J54:J59)

缓存值：133

**K60**

覆盖全部 6 个模块

### Row 62

**B62**

工作表导航

### Row 63

**B63**

Phase 1 Map

**E63**

查看目标地图、实时 KPI、模块任务量与进度。

### Row 64

**B64**

Task Execution

**E64**

日常维护执行状态；将 O 列“执行状态”更新为“已完成”后，地图执行数字自动变化。

### Row 65

**B65**

Implementation Check

**E65**

记录当前实现与证据；将 P 列“状态”更新为“已完成”后，地图检查数字自动变化。

## Blueprint

### Row 1

**A1**

AutoPM Phase 1 | Blueprint

### Row 3

**A3**

精简总览：每个能力包一行。任务详细解释在 Blueprint Detail；状态、差距、行动、Owner和日期均通过公式读取 Implementation Check。

### Row 5

**A5**

主线：M1可信数据 → M2执行闭环 → M3工作入口 → M4稳定保障 → M5真实采用 → M6证据与Gate决策

### Row 7

**A7**

模块

**B7**

能力包

**C7**

能力包名称

**D7**

核心问题

**E7**

任务数

**F7**

已完成

**G7**

进行中

**H7**

受阻/调整

**I7**

未开始

**J7**

完成率

**K7**

进入明细

### Row 8

**A8**

M1

**B8**

M1.1

**C8**

业务对象定义

**D8**

说清楚AutoPM管理哪些业务对象，以及每个对象分别代表什么，避免Programme、Project、SKU、Task、Issue等概念混用。

**E8**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B8)

缓存值：6

**F8**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B8,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G8**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B8,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：5

**H8**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B8,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B8,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：1

**I8**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B8,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：0

**J8**

=IFERROR(F8/E8,0)

缓存值：0

**K8**

查看任务

超链接：'Blueprint Detail'!A8

### Row 9

**A9**

M1

**B9**

M1.2

**C9**

对象关系模型

**D9**

把M1.1定义的对象正确连接起来，确保项目状态、问题、行动、责任和结果能够相互追溯。

**E9**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B9)

缓存值：3

**F9**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B9,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G9**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B9,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H9**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B9,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B9,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I9**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B9,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J9**

=IFERROR(F9/E9,0)

缓存值：0

**K9**

查看任务

超链接：'Blueprint Detail'!A14

### Row 10

**A10**

M1

**B10**

M1.3

**C10**

唯一标识与映射

**D10**

确保每条核心记录都有唯一、稳定的身份，并能与PMO、Excel等上游数据正确对应。

**E10**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B10)

缓存值：2

**F10**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B10,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G10**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B10,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：2

**H10**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B10,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B10,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I10**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B10,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：0

**J10**

=IFERROR(F10/E10,0)

缓存值：0

**K10**

查看任务

超链接：'Blueprint Detail'!A17

### Row 11

**A11**

M1

**B11**

M1.4

**C11**

字段与状态标准

**D11**

统一每类对象需要哪些字段、每个字段表达什么，以及状态如何变化，避免日期、健康状态和执行状态混用。

**E11**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B11)

缓存值：2

**F11**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B11,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G11**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B11,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H11**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B11,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B11,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I11**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B11,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J11**

=IFERROR(F11/E11,0)

缓存值：0

**K11**

查看任务

超链接：'Blueprint Detail'!A19

### Row 12

**A12**

M1

**B12**

M1.5

**C12**

数据来源与责任

**D12**

明确每个关键数据从哪里来、由谁负责、AutoPM可以怎样使用，以及多个系统发生冲突时如何处理。

**E12**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B12)

缓存值：4

**F12**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B12,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G12**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B12,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H12**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B12,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B12,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I12**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B12,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：3

**J12**

=IFERROR(F12/E12,0)

缓存值：0

**K12**

查看任务

超链接：'Blueprint Detail'!A21

### Row 13

**A13**

M1

**B13**

M1.6

**C13**

真实项目数据初始化

**D13**

选择真实试点项目，清理并建立完整项目数据，用实际业务验证对象、关系、字段与状态规则。

**E13**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B13)

缓存值：5

**F13**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B13,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G13**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B13,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：2

**H13**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B13,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B13,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：1

**I13**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B13,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J13**

=IFERROR(F13/E13,0)

缓存值：0

**K13**

查看任务

超链接：'Blueprint Detail'!A25

### Row 14

**A14**

M1

**B14**

M1.7

**C14**

数据质量与审计

**D14**

持续发现数据中的缺失、重复、冲突和长期未更新问题，并确保关键变化能够追溯和关闭。

**E14**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B14)

缓存值：3

**F14**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B14,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G14**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B14,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H14**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B14,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B14,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I14**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B14,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J14**

=IFERROR(F14/E14,0)

缓存值：0

**K14**

查看任务

超链接：'Blueprint Detail'!A30

### Row 15

**A15**

M2

**B15**

M2.1

**C15**

项目进入与初始化

**D15**

确保真实项目以正确、完整且不重复的方式进入AutoPM，并具备建立计划和开始执行的条件。

**E15**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B15)

缓存值：2

**F15**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B15,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G15**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B15,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H15**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B15,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B15,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I15**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B15,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J15**

=IFERROR(F15/E15,0)

缓存值：0

**K15**

查看任务

超链接：'Blueprint Detail'!A33

### Row 16

**A16**

M2

**B16**

M2.2

**C16**

计划与任务建立

**D16**

把项目目标转化为可以执行的Milestone和Task，明确做什么、谁负责、何时完成及前后依赖。

**E16**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B16)

缓存值：6

**F16**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B16,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G16**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B16,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：4

**H16**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B16,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B16,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I16**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B16,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J16**

=IFERROR(F16/E16,0)

缓存值：0

**K16**

查看任务

超链接：'Blueprint Detail'!A35

### Row 17

**A17**

M2

**B17**

M2.3

**C17**

日常执行与更新

**D17**

让项目成员持续更新真实执行情况，使AutoPM反映当前实际状态，而不是只保存最初计划。

**E17**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B17)

缓存值：4

**F17**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B17,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G17**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B17,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H17**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B17,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B17,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I17**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B17,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：3

**J17**

=IFERROR(F17/E17,0)

缓存值：0

**K17**

查看任务

超链接：'Blueprint Detail'!A41

### Row 18

**A18**

M2

**B18**

M2.4

**C18**

异常识别与记录

**D18**

及时发现并结构化记录Risk、Issue、Delay和Blocker，明确异常影响、责任和下一步。

**E18**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B18)

缓存值：3

**F18**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B18,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G18**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B18,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H18**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B18,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B18,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I18**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B18,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：3

**J18**

=IFERROR(F18/E18,0)

缓存值：0

**K18**

查看任务

超链接：'Blueprint Detail'!A45

### Row 19

**A19**

M2

**B19**

M2.5

**C19**

恢复行动与升级

**D19**

异常发生后，明确谁在什么时候采取什么行动恢复项目，并在处理不了时及时升级。

**E19**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B19)

缓存值：5

**F19**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B19,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G19**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B19,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H19**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B19,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B19,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I19**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B19,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：5

**J19**

=IFERROR(F19/E19,0)

缓存值：0

**K19**

查看任务

超链接：'Blueprint Detail'!A48

### Row 20

**A20**

M2

**B20**

M2.6

**C20**

管理决策

**D20**

对超出执行权限、涉及日期、范围、资源、成本或风险选择的事项，明确由谁何时作出决定并推动落实。

**E20**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B20)

缓存值：5

**F20**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B20,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G20**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B20,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H20**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B20,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B20,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I20**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B20,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：5

**J20**

=IFERROR(F20/E20,0)

缓存值：0

**K20**

查看任务

超链接：'Blueprint Detail'!A53

### Row 21

**A21**

M2

**B21**

M2.7

**C21**

结果确认与验证关闭

**D21**

确认Recovery Action完成后原问题是否真正解决，避免把Action完成错误地当成Issue关闭。

**E21**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B21)

缓存值：6

**F21**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B21,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G21**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B21,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H21**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B21,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B21,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I21**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B21,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：6

**J21**

=IFERROR(F21/E21,0)

缓存值：0

**K21**

查看任务

超链接：'Blueprint Detail'!A58

### Row 22

**A22**

M2

**B22**

M2.8

**C22**

历史与经验沉淀

**D22**

把项目问题、行动和结果保存为可复用经验，减少相同问题在不同项目中反复发生。

**E22**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B22)

缓存值：2

**F22**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B22,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G22**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B22,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H22**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B22,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B22,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I22**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B22,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J22**

=IFERROR(F22/E22,0)

缓存值：0

**K22**

查看任务

超链接：'Blueprint Detail'!A64

### Row 23

**A23**

M3

**B23**

M3.1

**C23**

个人执行入口

**D23**

让每个用户在一个入口看到本人需要处理的任务、异常、行动和待确认事项，并能直接完成更新。

**E23**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B23)

缓存值：2

**F23**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B23,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G23**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B23,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：2

**H23**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B23,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B23,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I23**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B23,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：0

**J23**

=IFERROR(F23/E23,0)

缓存值：0

**K23**

查看任务

超链接：'Blueprint Detail'!A66

### Row 24

**A24**

M3

**B24**

M3.2

**C24**

项目管理入口

**D24**

为项目负责人提供一个可信的项目工作空间，集中查看和维护项目结构、计划、执行、异常和决定。

**E24**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B24)

缓存值：2

**F24**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B24,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G24**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B24,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H24**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B24,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B24,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I24**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B24,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J24**

=IFERROR(F24/E24,0)

缓存值：0

**K24**

查看任务

超链接：'Blueprint Detail'!A68

### Row 25

**A25**

M3

**B25**

M3.3

**C25**

异常处理入口

**D25**

把需要处理的异常集中成工作队列，让负责人快速找到缺Owner、缺Action、逾期和待关闭事项并直接处理。

**E25**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B25)

缓存值：2

**F25**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B25,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G25**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B25,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H25**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B25,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B25,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I25**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B25,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J25**

=IFERROR(F25/E25,0)

缓存值：0

**K25**

查看任务

超链接：'Blueprint Detail'!A70

### Row 26

**A26**

M3

**B26**

M3.4

**C26**

周度管理入口

**D26**

让周度审查直接基于AutoPM事实进行，集中确认变化、偏差、风险、行动和决策，并将会议结果写回系统。

**E26**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B26)

缓存值：2

**F26**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B26,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G26**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B26,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H26**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B26,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B26,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I26**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B26,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J26**

=IFERROR(F26/E26,0)

缓存值：0

**K26**

查看任务

超链接：'Blueprint Detail'!A72

### Row 27

**A27**

M3

**B27**

M3.5

**C27**

领导审查与下钻

**D27**

让领导看到组合层面的健康、重大风险、延误和待决策事项，同时能逐层找到事实、责任和结果。

**E27**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B27)

缓存值：2

**F27**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B27,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G27**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B27,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H27**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B27,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B27,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I27**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B27,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J27**

=IFERROR(F27/E27,0)

缓存值：0

**K27**

查看任务

超链接：'Blueprint Detail'!A74

### Row 28

**A28**

M3

**B28**

M3.6

**C28**

用户体验与动作效率

**D28**

减少不必要字段、重复录入和页面切换，让关键动作简单清楚，并把用户反馈转为可验收改进。

**E28**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B28)

缓存值：6

**F28**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B28,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G28**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B28,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H28**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B28,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B28,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I28**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B28,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：5

**J28**

=IFERROR(F28/E28,0)

缓存值：0

**K28**

查看任务

超链接：'Blueprint Detail'!A76

### Row 29

**A29**

M4

**B29**

M4.1

**C29**

数据导入与初始化自动化

**D29**

让项目和计划数据可重复、安全地进入AutoPM，避免格式错误、重复记录和错误覆盖。

**E29**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B29)

缓存值：6

**F29**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B29,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G29**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B29,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：5

**H29**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B29,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B29,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I29**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B29,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J29**

=IFERROR(F29/E29,0)

缓存值：0

**K29**

查看任务

超链接：'Blueprint Detail'!A82

### Row 30

**A30**

M4

**B30**

M4.2

**C30**

状态与异常计算

**D30**

根据已确认规则自动计算到期、逾期、Next Milestone和偏差，并识别缺失与冲突，同时展示计算依据。

**E30**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B30)

缓存值：3

**F30**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B30,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G30**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B30,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H30**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B30,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B30,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I30**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B30,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J30**

=IFERROR(F30/E30,0)

缓存值：0

**K30**

查看任务

超链接：'Blueprint Detail'!A88

### Row 31

**A31**

M4

**B31**

M4.3

**C31**

提醒与升级

**D31**

把到期、逾期、缺失和关键Delay及时通知正确人员，同时控制重复提醒并记录响应和升级。

**E31**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B31)

缓存值：2

**F31**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B31,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G31**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B31,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H31**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B31,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B31,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I31**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B31,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J31**

=IFERROR(F31/E31,0)

缓存值：0

**K31**

查看任务

超链接：'Blueprint Detail'!A91

### Row 32

**A32**

M4

**B32**

M4.4

**C32**

报告生成

**D32**

从统一数据生成可确认、可追溯的周报和管理报告，缺失信息透明，发布前保留人工确认。

**E32**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B32)

缓存值：4

**F32**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B32,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：1

**G32**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B32,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H32**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B32,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B32,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I32**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B32,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J32**

=IFERROR(F32/E32,0)

缓存值：0.25

**K32**

查看任务

超链接：'Blueprint Detail'!A93

### Row 33

**A33**

M4

**B33**

M4.5

**C33**

PMO主数据连接

**D33**

让AutoPM稳定读取并匹配Programme、Project、SKU和目标日期等必要主数据，冲突和同步失败能够被发现。

**E33**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B33)

缓存值：5

**F33**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B33,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G33**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B33,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H33**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B33,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B33,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I33**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B33,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：4

**J33**

=IFERROR(F33/E33,0)

缓存值：0

**K33**

查看任务

超链接：'Blueprint Detail'!A97

### Row 34

**A34**

M4

**B34**

M4.6

**C34**

权限与审计

**D34**

控制不同角色可以查看、修改、确认、审批和导出的内容，并记录关键操作。

**E34**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B34)

缓存值：3

**F34**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B34,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G34**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B34,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H34**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B34,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B34,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I34**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B34,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：3

**J34**

=IFERROR(F34/E34,0)

缓存值：0

**K34**

查看任务

超链接：'Blueprint Detail'!A102

### Row 35

**A35**

M4

**B35**

M4.7

**C35**

运行监控与失败恢复

**D35**

持续监控自动化和同步运行，失败时及时告警、分配责任、安全重试并能够回退。

**E35**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B35)

缓存值：6

**F35**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B35,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G35**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B35,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H35**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B35,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B35,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I35**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B35,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：5

**J35**

=IFERROR(F35/E35,0)

缓存值：0

**K35**

查看任务

超链接：'Blueprint Detail'!A105

### Row 36

**A36**

M5

**B36**

M5.1

**C36**

Pilot范围确认

**D36**

明确试点为了证明什么、由谁参与、使用哪些项目，以及何时启动、暂停或退出。

**E36**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B36)

缓存值：1

**F36**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B36,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G36**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B36,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H36**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B36,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B36,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I36**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B36,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J36**

=IFERROR(F36/E36,0)

缓存值：0

**K36**

查看任务

超链接：'Blueprint Detail'!A111

### Row 37

**A37**

M5

**B37**

M5.2

**C37**

角色与责任

**D37**

明确Pilot运行中谁负责数据更新、项目推进、职能确认、管理决定、数据规则和平台支持。

**E37**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B37)

缓存值：1

**F37**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B37,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G37**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B37,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H37**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B37,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B37,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I37**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B37,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J37**

=IFERROR(F37/E37,0)

缓存值：0

**K37**

查看任务

超链接：'Blueprint Detail'!A112

### Row 38

**A38**

M5

**B38**

M5.3

**C38**

使用规则

**D38**

规定Pilot用户在什么情况下、在哪里、更新哪些信息，以及异常、行动、升级和关闭的最低要求。

**E38**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B38)

缓存值：1

**F38**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B38,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G38**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B38,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H38**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B38,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B38,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I38**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B38,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J38**

=IFERROR(F38/E38,0)

缓存值：0

**K38**

查看任务

超链接：'Blueprint Detail'!A113

### Row 39

**A39**

M5

**B39**

M5.4

**C39**

双系统过渡

**D39**

明确AutoPM与旧工具并存期间每项数据的唯一维护位置、同步方向、冲突处理和退出方式。

**E39**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B39)

缓存值：1

**F39**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B39,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G39**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B39,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H39**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B39,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B39,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I39**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B39,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：0

**J39**

=IFERROR(F39/E39,0)

缓存值：0

**K39**

查看任务

超链接：'Blueprint Detail'!A114

### Row 40

**A40**

M5

**B40**

M5.5

**C40**

角色上手

**D40**

让关键角色在真实项目中完成自己的核心操作，并记录理解偏差和使用问题。

**E40**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B40)

缓存值：2

**F40**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B40,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G40**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B40,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H40**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B40,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B40,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I40**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B40,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J40**

=IFERROR(F40/E40,0)

缓存值：0

**K40**

查看任务

超链接：'Blueprint Detail'!A115

### Row 41

**A41**

M5

**B41**

M5.6

**C41**

周度运行节奏

**D41**

建立可重复的每周更新、检查、审查、决定、行动和结果验证循环。

**E41**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B41)

缓存值：6

**F41**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B41,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：1

**G41**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B41,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H41**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B41,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B41,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I41**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B41,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：4

**J41**

=IFERROR(F41/E41,0)

缓存值：0.16666666666666666

**K41**

查看任务

超链接：'Blueprint Detail'!A117

### Row 42

**A42**

M5

**B42**

M5.7

**C42**

用户支持与问题处理

**D42**

持续收集、分类、排序、修复和验证Pilot用户问题，并把重复反馈转成系统性改进。

**E42**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B42)

缓存值：6

**F42**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B42,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G42**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B42,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H42**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B42,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B42,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I42**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B42,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：6

**J42**

=IFERROR(F42/E42,0)

缓存值：0

**K42**

查看任务

超链接：'Blueprint Detail'!A123

### Row 43

**A43**

M6

**B43**

M6.1

**C43**

基线定义

**D43**

在Pilot前记录当前工作方式和指标，确保后续价值比较有真实起点。

**E43**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B43)

缓存值：2

**F43**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B43,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G43**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B43,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H43**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B43,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B43,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I43**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B43,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：2

**J43**

=IFERROR(F43/E43,0)

缓存值：0

**K43**

查看任务

超链接：'Blueprint Detail'!A129

### Row 44

**A44**

M6

**B44**

M6.2

**C44**

使用与采用证据

**D44**

证明真实用户是否在真实项目中持续使用AutoPM，而不是只登录或一次性录入。

**E44**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B44)

缓存值：1

**F44**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B44,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G44**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B44,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H44**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B44,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B44,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I44**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B44,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J44**

=IFERROR(F44/E44,0)

缓存值：0

**K44**

查看任务

超链接：'Blueprint Detail'!A131

### Row 45

**A45**

M6

**B45**

M6.3

**C45**

数据质量证据

**D45**

用可重复指标证明AutoPM中的数据是否完整、关联正确、可用于项目管理。

**E45**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B45)

缓存值：1

**F45**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B45,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G45**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B45,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：1

**H45**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B45,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B45,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I45**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B45,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：0

**J45**

=IFERROR(F45/E45,0)

缓存值：0

**K45**

查看任务

超链接：'Blueprint Detail'!A132

### Row 46

**A46**

M6

**B46**

M6.4

**C46**

执行闭环证据

**D46**

证明任务、异常、行动、决定和验证关闭是否真正形成闭环，并识别最常中断的环节。

**E46**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B46)

缓存值：1

**F46**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B46,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G46**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B46,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H46**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B46,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B46,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I46**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B46,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J46**

=IFERROR(F46/E46,0)

缓存值：0

**K46**

查看任务

超链接：'Blueprint Detail'!A133

### Row 47

**A47**

M6

**B47**

M6.5

**C47**

效率与业务结果

**D47**

比较Pilot前后查找、追问、周报、重复维护和问题处理的变化，同时记录新增工作和负面影响。

**E47**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B47)

缓存值：3

**F47**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B47,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G47**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B47,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H47**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B47,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B47,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I47**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B47,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：3

**J47**

=IFERROR(F47/E47,0)

缓存值：0

**K47**

查看任务

超链接：'Blueprint Detail'!A134

### Row 48

**A48**

M6

**B48**

M6.6

**C48**

平台能力评估

**D48**

评估当前平台是否能支持后续规模，包括性能、访问、权限、集成、迁移、支持和成本。

**E48**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B48)

缓存值：1

**F48**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B48,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G48**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B48,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H48**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B48,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B48,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I48**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B48,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：1

**J48**

=IFERROR(F48/E48,0)

缓存值：0

**K48**

查看任务

超链接：'Blueprint Detail'!A137

### Row 49

**A49**

M6

**B49**

M6.7

**C49**

Gate 1决策

**D49**

汇总Phase 1证据，判断是否满足成功条件，并正式决定继续、调整、延长、迁移或停止。

**E49**

=COUNTIF('Implementation Check'!$B$8:$B$1000,B49)

缓存值：5

**F49**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B49,'Implementation Check'!$P$8:$P$1000,"已完成")

缓存值：0

**G49**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B49,'Implementation Check'!$P$8:$P$1000,"进行中")

缓存值：0

**H49**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B49,'Implementation Check'!$P$8:$P$1000,"受阻")+COUNTIFS('Implementation Check'!$B$8:$B$1000,B49,'Implementation Check'!$P$8:$P$1000,"需要调整")

缓存值：0

**I49**

=COUNTIFS('Implementation Check'!$B$8:$B$1000,B49,'Implementation Check'!$P$8:$P$1000,"未开始")

缓存值：5

**J49**

=IFERROR(F49/E49,0)

缓存值：0

**K49**

查看任务

超链接：'Blueprint Detail'!A138

## Blueprint Detail

### Row 1

**A1**

AutoPM Phase 1 | Blueprint Detail

### Row 3

**A3**

每个Action仅占一行；目标解释、验收和交付物完整保留。执行状态与管理信息通过公式从 Implementation Check 读取。可筛选模块、能力包和状态。

### Row 5

**A5**

蓝色列为定义内容；绿色/黄色列为联动结果。请只在 Implementation Check 维护当前证据、判断、差距、行动、Owner、日期和状态。

### Row 7

**A7**

模块

**B7**

能力包

**C7**

Action ID

**D7**

任务

**E7**

明确内容

**F7**

简单理解

**G7**

能力包验收标准

**H7**

能力包交付物

**I7**

状态

**J7**

主要差距

**K7**

修改行动

**L7**

Owner / 日期

### Row 8

**A8**

M1

**B8**

M1.1

超链接：'Blueprint'!A8

**C8**

M1.1-A01

**D8**

项目结构对象

**E8**

Programme、Project、SKU分别是什么，三者各自管理什么。

**F8**

先说清楚一个项目由哪些层级组成。

**G8**

1. 不同人员对核心对象的理解基本一致。
2. 同一业务事实不会被重复记录成不同对象。
3. 可以用一个真实项目完整说明所有核心对象。
4. 每个对象的业务边界和系统归属清楚。

**H8**

1 业务对象定义表｜2 项目、计划、异常、行动和责任对象清单｜3 对象系统归属表｜4 真实项目示例

**I8**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C8,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J8**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C8,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Programme未独立成表；SKU无明确表或明确定义；对象边界未文档化；缺少统一的业务对象定义文档。

**K8**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C8,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：编写业务对象定义文档；确认SKU表归属；Programme层级定义明确化。

**L8**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C8,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C8,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 9

**A9**

M1

**B9**

M1.1

**C9**

M1.1-A02

**D9**

计划执行对象

**E9**

Stage表示项目所处过程；Milestone表示关键节点；Task表示具体工作；Deliverable表示完成后留下的结果。

**F9**

说清楚项目怎样计划、怎样执行、怎样证明完成。

**G9**

1. 不同人员对核心对象的理解基本一致。
2. 同一业务事实不会被重复记录成不同对象。
3. 可以用一个真实项目完整说明所有核心对象。
4. 每个对象的业务边界和系统归属清楚。

**H9**

1 业务对象定义表｜2 项目、计划、异常、行动和责任对象清单｜3 对象系统归属表｜4 真实项目示例

**I9**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C9,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J9**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C9,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Stage、Deliverable概念未定义；计划→执行→完成的对象链不完整。

**K9**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C9,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义Stage/Deliverable对象；明确与Milestone/Task的关系。

**L9**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C9,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C9,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 10

**A10**

M1

**B10**

M1.1

**C10**

M1.1-A03

**D10**

异常对象

**E10**

Risk是潜在风险；Issue是已发生问题；Delay是日期偏差；Blocker是工作目前无法继续。

**F10**

说清楚不同异常分别应该怎样记录。

**G10**

1. 不同人员对核心对象的理解基本一致。
2. 同一业务事实不会被重复记录成不同对象。
3. 可以用一个真实项目完整说明所有核心对象。
4. 每个对象的业务边界和系统归属清楚。

**H10**

1 业务对象定义表｜2 项目、计划、异常、行动和责任对象清单｜3 对象系统归属表｜4 真实项目示例

**I10**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C10,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J10**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C10,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Risk、Delay、Blocker未独立定义；Issue与Delay/Blocker边界不清。

**K10**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C10,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义Risk/Delay/Blocker对象；明确与Issue的区分规则。

**L10**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C10,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C10,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 11

**A11**

M1

**B11**

M1.1

**C11**

M1.1-A04

**D11**

恢复与决策对象

**E11**

记录Recovery Action、责任人、管理决定、实际结果、验证人，以及关闭或重新处理结论。

**F11**

说清楚问题发生后，如何从行动一直管理到真正关闭。

**G11**

1. 不同人员对核心对象的理解基本一致。
2. 同一业务事实不会被重复记录成不同对象。
3. 可以用一个真实项目完整说明所有核心对象。
4. 每个对象的业务边界和系统归属清楚。

**H11**

1 业务对象定义表｜2 项目、计划、异常、行动和责任对象清单｜3 对象系统归属表｜4 真实项目示例

**I11**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C11,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：受阻

**J11**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C11,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Recovery Action和Decision完全缺失；无验证关闭机制。

**K11**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C11,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：设计Recovery Action表结构；定义验证关闭流程。

**L11**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C11,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C11,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 12

**A12**

M1

**B12**

M1.1

**C12**

M1.1-A05

**D12**

组织责任对象

**E12**

明确参与人、Project/Task/Issue/Action Owner、协作者、确认人和决策人。

**F12**

说清楚谁负责做、谁负责确认、谁负责决定。

**G12**

1. 不同人员对核心对象的理解基本一致。
2. 同一业务事实不会被重复记录成不同对象。
3. 可以用一个真实项目完整说明所有核心对象。
4. 每个对象的业务边界和系统归属清楚。

**H12**

1 业务对象定义表｜2 项目、计划、异常、行动和责任对象清单｜3 对象系统归属表｜4 真实项目示例

**I12**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C12,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J12**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C12,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：缺少确认人、决策人角色定义；Owner与Collaborator边界不清。

**K12**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C12,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：明确各角色定义和权限边界。

**L12**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C12,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C12,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 13

**A13**

M1

**B13**

M1.1

**C13**

M1.1-A06

**D13**

对象系统归属

**E13**

明确数据创建系统、维护位置、准确性责任，以及AutoPM是读取、写入、计算还是仅保存链接。

**F13**

说清楚每类数据从哪里来、在哪里维护、以哪套数据为准。

**G13**

1. 不同人员对核心对象的理解基本一致。
2. 同一业务事实不会被重复记录成不同对象。
3. 可以用一个真实项目完整说明所有核心对象。
4. 每个对象的业务边界和系统归属清楚。

**H13**

1 业务对象定义表｜2 项目、计划、异常、行动和责任对象清单｜3 对象系统归属表｜4 真实项目示例

**I13**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C13,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J13**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C13,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：缺少正式的数据来源矩阵文档；AutoPM读写计算边界未文档化。

**K13**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C13,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：编写数据来源与系统归属文档。

**L13**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C13,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C13,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 14

**A14**

M1

**B14**

M1.2

超链接：'Blueprint'!A9

**C14**

M1.2-A01

**D14**

建立完整对象关系

**E14**

建立Programme→Project→SKU→Milestone→Task→Issue→Recovery Action→Result的业务链，并关联各类Owner、决策人和验证人。

**F14**

把所有项目数据连接成一条完整业务链。

**G14**

1. 关键记录不存在无法关联的孤立数据。
2. 从Project可以下钻到SKU、Milestone、Task、Issue和Action。
3. 从Issue可以追溯Owner、Action、结果和验证记录。
4. 多SKU项目能够表达共同计划和SKU独立差异。

**H14**

1 业务对象关系图｜2 对象关系规则表｜3 汇总与下钻规则｜4 多SKU和跨项目处理规则｜5 真实项目关系验证记录

**I14**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C14,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J14**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C14,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：完整业务链(Project→SKU→Milestone→Task→Issue→Recovery→Result)未贯通；Programme未链接。

**K14**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C14,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立完整对象关系链；Programme改为Linked Record。

**L14**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C14,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C14,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 15

**A15**

M1

**B15**

M1.2

**C15**

M1.2-A02

**D15**

建立汇总下钻规则

**E15**

明确SKU状态如何汇总到Project，Task、Milestone、Issue和Delay如何影响上层状态，以及如何下钻到具体原因。

**F15**

上层能看整体，下层能找到具体问题和责任人。

**G15**

1. 关键记录不存在无法关联的孤立数据。
2. 从Project可以下钻到SKU、Milestone、Task、Issue和Action。
3. 从Issue可以追溯Owner、Action、结果和验证记录。
4. 多SKU项目能够表达共同计划和SKU独立差异。

**H15**

1 业务对象关系图｜2 对象关系规则表｜3 汇总与下钻规则｜4 多SKU和跨项目处理规则｜5 真实项目关系验证记录

**I15**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C15,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J15**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C15,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：汇总下钻规则未定义；SKU状态汇总到Project不存在。

**K15**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C15,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义汇总下钻规则；实现状态向上聚合。

**L15**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C15,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C15,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 16

**A16**

M1

**B16**

M1.2

**C16**

M1.2-A03

**D16**

处理跨项目和多SKU关系

**E16**

明确多SKU管理、共同信息传递、SKU独立日期与状态，以及一个Issue影响多个对象时的记录方式。

**F16**

正确管理共同信息和不同SKU之间的真实差异。

**G16**

1. 关键记录不存在无法关联的孤立数据。
2. 从Project可以下钻到SKU、Milestone、Task、Issue和Action。
3. 从Issue可以追溯Owner、Action、结果和验证记录。
4. 多SKU项目能够表达共同计划和SKU独立差异。

**H16**

1 业务对象关系图｜2 对象关系规则表｜3 汇总与下钻规则｜4 多SKU和跨项目处理规则｜5 真实项目关系验证记录

**I16**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C16,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J16**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C16,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：多SKU关系管理完全缺失；共同信息传递规则不存在。

**K16**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C16,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：设计SKU表或SKU关联机制；定义跨项目管理规则。

**L16**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C16,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C16,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 17

**A17**

M1

**B17**

M1.3

超链接：'Blueprint'!A10

**C17**

M1.3-A01

**D17**

定义核心对象标识

**E17**

为Project、SKU、Milestone、Task、Issue、Action和Decision建立唯一编号。

**F17**

每条记录都有自己的身份证，名称改变也不会认错。

**G17**

1. 每个核心对象都有唯一编号。
2. 名称、Owner和状态变化时编号不变。
3. 重复导入不会产生重复Project或SKU。
4. 历史无ID数据按统一规则处理。

**H17**

1 核心对象编号规则｜2 上下游映射与去重规则｜3 历史无ID补号与例外处理记录

**I17**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C17,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J17**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C17,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：仅22.2%项目有Project ID；SKU/Milestone/Action/Decision无唯一编号。

**K17**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C17,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：补全Project ID覆盖率；为其他对象建立编号规则。

**L17**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C17,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C17,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 18

**A18**

M1

**B18**

M1.3

**C18**

M1.3-A02

**D18**

建立映射、去重和历史无ID规则

**E18**

明确上游记录如何对应AutoPM、重复导入如何防重、历史无ID如何补号，以及无法确认的数据如何处理。

**F18**

解决旧数据和外部数据进入AutoPM时的匹配与清理问题。

**G18**

1. 每个核心对象都有唯一编号。
2. 名称、Owner和状态变化时编号不变。
3. 重复导入不会产生重复Project或SKU。
4. 历史无ID数据按统一规则处理。

**H18**

1 核心对象编号规则｜2 上下游映射与去重规则｜3 历史无ID补号与例外处理记录

**I18**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C18,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J18**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C18,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：历史无ID记录无补号规则；无法确认数据的处理规则不存在。

**K18**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C18,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义历史ID补号规则和例外处理流程。

**L18**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C18,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C18,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 19

**A19**

M1

**B19**

M1.4

超链接：'Blueprint'!A11

**C19**

M1.4-A01

**D19**

定义核心字段

**E19**

统一身份、责任、日期、生命周期、健康、执行和数据确认字段，并明确字段适用于哪个业务对象。

**F19**

说清楚每张记录需要填写什么，以及每个字段是什么意思。

**G19**

1. 每个核心字段只有一个明确含义。
2. 原计划、预测和实际日期不会互相覆盖。
3. 生命周期、健康、执行和确认状态不混用。
4. 状态变化有明确条件，Action完成不会自动关闭Issue。

**H19**

1 字段字典｜2 状态字典｜3 状态转换与重开规则｜4 日期与状态使用示例

**I19**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C19,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J19**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C19,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无正式字段字典；原计划/预测/实际日期字段混合（如Due Date同时承担计划和实际）。

**K19**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C19,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：编写字段字典；分离计划日期、预测日期和实际日期。

**L19**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C19,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C19,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 20

**A20**

M1

**B20**

M1.4

**C20**

M1.4-A02

**D20**

定义状态转换、重开和关闭规则

**E20**

明确Task、Issue、Action、Risk和Blocker等对象何时改变状态、何时关闭、何时重开，以及系统计算与人工确认边界。

**F20**

说清楚状态什么时候可以改变，避免用户随意选择状态。

**G20**

1. 每个核心字段只有一个明确含义。
2. 原计划、预测和实际日期不会互相覆盖。
3. 生命周期、健康、执行和确认状态不混用。
4. 状态变化有明确条件，Action完成不会自动关闭Issue。

**H20**

1 字段字典｜2 状态字典｜3 状态转换与重开规则｜4 日期与状态使用示例

**I20**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C20,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J20**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C20,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：状态转换条件未文档化；Action完成不自动关闭Issue(需人工)。

**K20**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C20,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义状态转换规则和重开条件。

**L20**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C20,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C20,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 21

**A21**

M1

**B21**

M1.5

超链接：'Blueprint'!A12

**C21**

M1.5-A01

**D21**

确认关键字段正式来源

**E21**

确认Programme、Project、SKU、目标日期、人员、Task、Issue、Action及原始文件的正式来源。

**F21**

为每项重要数据确定正式来源。

**G21**

1. 每个关键字段有正式来源。
2. 每类数据有明确Owner。
3. AutoPM的读写计算边界清楚。
4. 数据冲突和同步失败有处理方法。

**H21**

1 字段来源矩阵｜2 系统读写边界表｜3 业务Owner与数据Owner责任表｜4 数据冲突处理规则｜5 双系统维护和退出规则

**I21**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C21,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J21**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C21,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无正式字段来源矩阵；部分字段来源不明确。

**K21**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C21,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：编写字段来源矩阵文档。

**L21**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C21,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C21,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 22

**A22**

M1

**B22**

M1.5

**C22**

M1.5-A02

**D22**

明确读写计算引用边界

**E22**

明确AutoPM对每项数据是读取、写入、自动计算、保存链接还是只做展示。

**F22**

说清楚AutoPM对每项数据能做什么、不能做什么。

**G22**

1. 每个关键字段有正式来源。
2. 每类数据有明确Owner。
3. AutoPM的读写计算边界清楚。
4. 数据冲突和同步失败有处理方法。

**H22**

1 字段来源矩阵｜2 系统读写边界表｜3 业务Owner与数据Owner责任表｜4 数据冲突处理规则｜5 双系统维护和退出规则

**I22**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C22,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J22**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C22,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：未形成完整的读写计算引用边界文档。

**K22**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C22,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：编写系统读写边界表。

**L22**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C22,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C22,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 23

**A23**

M1

**B23**

M1.5

**C23**

M1.5-A03

**D23**

指定业务与数据Owner

**E23**

明确谁决定业务含义、谁负责准确性、谁维护、谁解决问题、谁批准规则变化。

**F23**

数据出现问题时，明确应该由谁处理和决定。

**G23**

1. 每个关键字段有正式来源。
2. 每类数据有明确Owner。
3. AutoPM的读写计算边界清楚。
4. 数据冲突和同步失败有处理方法。

**H23**

1 字段来源矩阵｜2 系统读写边界表｜3 业务Owner与数据Owner责任表｜4 数据冲突处理规则｜5 双系统维护和退出规则

**I23**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C23,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J23**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C23,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无正式的业务Owner与数据Owner责任分离定义。

**K23**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C23,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义业务Owner和数据Owner责任矩阵。

**L23**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C23,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C23,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 24

**A24**

M1

**B24**

M1.5

**C24**

M1.5-A04

**D24**

定义冲突失败与双维护规则

**E24**

明确系统数据不一致、同步失败、过渡期维护位置及结束双系统维护的规则。

**F24**

防止数据冲突、同步失败和重复维护。

**G24**

1. 每个关键字段有正式来源。
2. 每类数据有明确Owner。
3. AutoPM的读写计算边界清楚。
4. 数据冲突和同步失败有处理方法。

**H24**

1 字段来源矩阵｜2 系统读写边界表｜3 业务Owner与数据Owner责任表｜4 数据冲突处理规则｜5 双系统维护和退出规则

**I24**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C24,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J24**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C24,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无正式的冲突失败处理规则；双系统退出条件未定义。

**K24**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C24,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：编写冲突处理和双系统退出规则。

**L24**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C24,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C24,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 25

**A25**

M1

**B25**

M1.6

超链接：'Blueprint'!A13

**C25**

M1.6-A01

**D25**

确认试点项目

**E25**

确定具有代表性的试点项目、SKU范围、业务负责人和验证人员。

**F25**

先选一个能代表真实复杂度的项目。

**G25**

1. 试点项目具有真实项目、SKU、计划、成员、异常和行动数据。
2. 关键关系完整。
3. 日期、状态、责任和来源符合统一规则。
4. 抽样问题进入修复清单。

**H25**

1 试点项目与范围确认｜2 清理后的基础数据｜3 完整项目关系与执行数据｜4 业务抽样及修复清单

**I25**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C25,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：受阻

**J25**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C25,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：未选择代表性试点项目；无试点范围确认文档。

**K25**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C25,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：选择2-3个代表性试点项目并确认范围。

**L25**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C25,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C25,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-04

### Row 26

**A26**

M1

**B26**

M1.6

**C26**

M1.6-A02

**D26**

清理记录

**E26**

清理重复、缺失、冲突和历史格式不一致的基础记录，并保留处理结果。

**F26**

先把旧数据整理到可用。

**G26**

1. 试点项目具有真实项目、SKU、计划、成员、异常和行动数据。
2. 关键关系完整。
3. 日期、状态、责任和来源符合统一规则。
4. 抽样问题进入修复清单。

**H26**

1 试点项目与范围确认｜2 清理后的基础数据｜3 完整项目关系与执行数据｜4 业务抽样及修复清单

**I26**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C26,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J26**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C26,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：1125个项目无对应里程碑日期(项目无数据)；重复/冲突清理不完整。

**K26**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C26,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：清理试点项目数据；补全缺失里程碑日期。

**L26**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C26,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C26,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 27

**A27**

M1

**B27**

M1.6

**C27**

M1.6-A03

**D27**

建立Project与SKU关系

**E27**

按已定义模型建立项目与一个或多个SKU的关系及独立差异。

**F27**

把项目和产品正确连起来。

**G27**

1. 试点项目具有真实项目、SKU、计划、成员、异常和行动数据。
2. 关键关系完整。
3. 日期、状态、责任和来源符合统一规则。
4. 抽样问题进入修复清单。

**H27**

1 试点项目与范围确认｜2 清理后的基础数据｜3 完整项目关系与执行数据｜4 业务抽样及修复清单

**I27**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C27,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J27**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C27,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Project与SKU关系未建立。

**K27**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C27,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立Project-SKU关系；导入试点项目SKU数据。

**L27**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C27,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C27,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 28

**A28**

M1

**B28**

M1.6

**C28**

M1.6-A04

**D28**

导入计划成员异常和Action

**E28**

导入Milestone、Task、成员、Issue、Risk、Delay、Blocker与Recovery Action。

**F28**

建立可运行的完整项目数据。

**G28**

1. 试点项目具有真实项目、SKU、计划、成员、异常和行动数据。
2. 关键关系完整。
3. 日期、状态、责任和来源符合统一规则。
4. 抽样问题进入修复清单。

**H28**

1 试点项目与范围确认｜2 清理后的基础数据｜3 完整项目关系与执行数据｜4 业务抽样及修复清单

**I28**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C28,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J28**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C28,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Recovery Action不存在；Risk/Delay/Blocker未导入；成员关联有限。

**K28**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C28,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：补全异常和行动数据导入。

**L28**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C28,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C28,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 29

**A29**

M1

**B29**

M1.6

**C29**

M1.6-A05

**D29**

完成业务抽样

**E29**

由业务人员按样本核对结构、日期、状态、责任、关系和可追溯结果。

**F29**

让业务人员证明数据真的正确。

**G29**

1. 试点项目具有真实项目、SKU、计划、成员、异常和行动数据。
2. 关键关系完整。
3. 日期、状态、责任和来源符合统一规则。
4. 抽样问题进入修复清单。

**H29**

1 试点项目与范围确认｜2 清理后的基础数据｜3 完整项目关系与执行数据｜4 业务抽样及修复清单

**I29**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C29,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J29**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C29,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无业务人员抽样确认记录。

**K29**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C29,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：对试点项目进行业务抽样验证。

**L29**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C29,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C29,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 30

**A30**

M1

**B30**

M1.7

超链接：'Blueprint'!A14

**C30**

M1.7-A01

**D30**

建立数据质量检查

**E30**

检查必填缺失、关系断开、重复、冲突、长期未更新以及日期和状态逻辑。

**F30**

自动或定期找出不完整、不一致和不合理的数据。

**G30**

1. 关键数据问题可以被识别。
2. 每个重要问题有Owner和状态。
3. 修正后经过重新检查。
4. 关键字段变化可以追溯。

**H30**

1 数据质量检查规则｜2 数据质量问题清单｜3 关键变更记录｜4 数据产生方式说明｜5 问题分配、修复和关闭记录

**I30**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C30,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J30**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C30,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：缺少必填缺失、关系断开、重复、冲突检查；无定期检查机制。

**K30**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C30,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立系统性数据质量检查规则和定期运行机制。

**L30**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C30,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C30,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 31

**A31**

M1

**B31**

M1.7

**C31**

M1.7-A02

**D31**

记录关键变更和数据产生方式

**E31**

记录谁在何时修改了什么，以及数据由人工、计算还是同步产生。

**F31**

让关键数据变化可以追溯。

**G31**

1. 关键数据问题可以被识别。
2. 每个重要问题有Owner和状态。
3. 修正后经过重新检查。
4. 关键字段变化可以追溯。

**H31**

1 数据质量检查规则｜2 数据质量问题清单｜3 关键变更记录｜4 数据产生方式说明｜5 问题分配、修复和关闭记录

**I31**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C31,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J31**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C31,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无关键变更审计记录；数据产生方式(人工/计算/同步)未标记。

**K31**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C31,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立关键变更记录和数据产生方式标记。

**L31**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C31,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C31,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 32

**A32**

M1

**B32**

M1.7

**C32**

M1.7-A03

**D32**

修复、验证并关闭质量问题

**E32**

为数据问题分配Owner和日期，修正后重新验证并关闭，重复问题转为规则或自动化改进。

**F32**

发现数据问题后必须有人处理，并确认是否真正修好。

**G32**

1. 关键数据问题可以被识别。
2. 每个重要问题有Owner和状态。
3. 修正后经过重新检查。
4. 关键字段变化可以追溯。

**H32**

1 数据质量检查规则｜2 数据质量问题清单｜3 关键变更记录｜4 数据产生方式说明｜5 问题分配、修复和关闭记录

**I32**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C32,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J32**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C32,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无Owner分配和状态跟踪；修复后无重新验证机制。

**K32**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C32,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立质量问题分配、修复、验证和关闭流程。

**L32**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C32,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C32,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 33

**A33**

M2

**B33**

M2.1

超链接：'Blueprint'!A15

**C33**

M2.1-A01

**D33**

识别新增与重复项目

**E33**

先搜索项目是否存在；存在时关联原项目，不存在时再新建；无法确认的信息标记待确认。

**F33**

先查有没有，再决定关联还是新建。

**G33**

1. 项目进入前完成重复检查。
2. Project ID和SKU关系正确。
3. 类型、Owner、关键日期和阶段明确。
4. 真实项目完整跑通一次进入流程。

**H33**

1 项目进入检查清单｜2 项目创建与确认记录｜3 Programme、Project和SKU关联结果｜4 重复或待确认问题清单｜5 真实项目进入验证记录

**I33**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C33,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J33**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C33,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：项目进入前无自动重复检查流程；待确认标记不存在。

**K33**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C33,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加项目进入前的重复检查步骤。

**L33**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C33,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C33,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 34

**A34**

M2

**B34**

M2.1

**C34**

M2.1-A02

**D34**

确认项目结构、责任与模板

**E34**

确认Project ID、项目类型、Programme、SKU、Owner、成员、关键日期、当前阶段和适用模板。

**F34**

把项目身份、结构、责任和执行入口一次确认清楚。

**G34**

1. 项目进入前完成重复检查。
2. Project ID和SKU关系正确。
3. 类型、Owner、关键日期和阶段明确。
4. 真实项目完整跑通一次进入流程。

**H34**

1 项目进入检查清单｜2 项目创建与确认记录｜3 Programme、Project和SKU关联结果｜4 重复或待确认问题清单｜5 真实项目进入验证记录

**I34**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C34,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J34**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C34,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无项目模板选择机制；SKU/成员/关键日期确认不完整。

**K34**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C34,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：设计项目模板和进入确认流程。

**L34**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C34,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C34,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 35

**A35**

M2

**B35**

M2.2

超链接：'Blueprint'!A16

**C35**

M2.2-A01

**D35**

建立阶段和Milestone

**E35**

根据项目类型选择适用模板，建立并确认关键Stage和Milestone。

**F35**

先明确项目要经过哪些阶段、达到哪些关键节点。

**G35**

1. 项目有清楚的关键Milestone。
2. 每个必要Task都有Owner、Due和状态。
3. 依赖关系能够表达。
4. 项目负责人确认计划可执行。

**H35**

1 项目Milestone清单｜2 项目Task计划｜3 Owner与日期分配结果｜4 关键依赖关系清单｜5 计划确认及变更记录

**I35**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C35,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J35**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C35,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Stage未定义；Milestone模板不存在（依赖周报格式）。

**K35**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C35,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义Stage模型；建立Milestone模板选择机制。

**L35**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C35,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C35,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 36

**A36**

M2

**B36**

M2.2

**C36**

M2.2-A02

**D36**

导入或生成Task

**E36**

将Milestone拆成Task，删除不适用任务并补充项目特有任务。

**F36**

把目标拆成真正需要执行的工作。

**G36**

1. 项目有清楚的关键Milestone。
2. 每个必要Task都有Owner、Due和状态。
3. 依赖关系能够表达。
4. 项目负责人确认计划可执行。

**H36**

1 项目Milestone清单｜2 项目Task计划｜3 Owner与日期分配结果｜4 关键依赖关系清单｜5 计划确认及变更记录

**I36**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C36,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J36**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C36,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Task生成后无法删除不适用任务；项目特有任务补充机制不完善。

**K36**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C36,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加Task筛选和补充机制。

**L36**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C36,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C36,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 37

**A37**

M2

**B37**

M2.2

**C37**

M2.2-A03

**D37**

明确交付物和依赖

**E37**

明确Task前后依赖、完成后需要留下的Deliverable，以及关联的Project、SKU或Milestone。

**F37**

说清楚任务前后关系和完成结果。

**G37**

1. 项目有清楚的关键Milestone。
2. 每个必要Task都有Owner、Due和状态。
3. 依赖关系能够表达。
4. 项目负责人确认计划可执行。

**H37**

1 项目Milestone清单｜2 项目Task计划｜3 Owner与日期分配结果｜4 关键依赖关系清单｜5 计划确认及变更记录

**I37**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C37,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J37**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C37,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Deliverable未定义；依赖关系表达能力有限。

**K37**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C37,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强依赖关系；定义Deliverable概念。

**L37**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C37,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C37,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 38

**A38**

M2

**B38**

M2.2

**C38**

M2.2-A04

**D38**

分配Owner

**E38**

为每项必要Task指定一个主要Owner。

**F38**

每项工作都必须有人明确负责。

**G38**

1. 项目有清楚的关键Milestone。
2. 每个必要Task都有Owner、Due和状态。
3. 依赖关系能够表达。
4. 项目负责人确认计划可执行。

**H38**

1 项目Milestone清单｜2 项目Task计划｜3 Owner与日期分配结果｜4 关键依赖关系清单｜5 计划确认及变更记录

**I38**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C38,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J38**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C38,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：部分Task缺少Owner分配。

**K38**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C38,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：确保所有Task有Owner。（原始评级：大部分覆盖）

**L38**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C38,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C38,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 39

**A39**

M2

**B39**

M2.2

**C39**

M2.2-A05

**D39**

设置Baseline与Due

**E39**

记录原始计划、当前目标日期、优先级和初始状态。

**F39**

把时间要求设置成可执行计划。

**G39**

1. 项目有清楚的关键Milestone。
2. 每个必要Task都有Owner、Due和状态。
3. 依赖关系能够表达。
4. 项目负责人确认计划可执行。

**H39**

1 项目Milestone清单｜2 项目Task计划｜3 Owner与日期分配结果｜4 关键依赖关系清单｜5 计划确认及变更记录

**I39**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C39,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J39**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C39,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无Baseline日期(原计划日期)；无优先级字段。

**K39**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C39,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加Baseline和优先级字段。

**L39**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C39,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C39,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 40

**A40**

M2

**B40**

M2.2

**C40**

M2.2-A06

**D40**

确认计划并记录变更

**E40**

由项目负责人确认任务、日期、Owner和依赖，后续变化保留记录。

**F40**

计划必须经过业务确认。

**G40**

1. 项目有清楚的关键Milestone。
2. 每个必要Task都有Owner、Due和状态。
3. 依赖关系能够表达。
4. 项目负责人确认计划可执行。

**H40**

1 项目Milestone清单｜2 项目Task计划｜3 Owner与日期分配结果｜4 关键依赖关系清单｜5 计划确认及变更记录

**I40**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C40,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J40**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C40,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：计划未经业务确认；变更无记录。

**K40**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C40,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立计划确认和变更记录流程。

**L40**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C40,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C40,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 41

**A41**

M2

**B41**

M2.3

超链接：'Blueprint'!A17

**C41**

M2.3-A01

**D41**

查看待办

**E41**

查看本人负责的今日、即将到期、逾期、等待、受阻和待确认事项。

**F41**

先看清楚自己现在要做什么。

**G41**

1. 成员能更新本人Task。
2. 更新反映真实进度。
3. 计划、预测和实际日期可区分。
4. 等待、阻塞和延期可记录。
5. 真实项目连续运行后可了解当前状态。

**H41**

1 日常更新规则｜2 Task更新记录｜3 日期和状态变化记录｜4 未更新及待确认事项清单｜5 真实项目连续运行记录

**I41**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C41,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J41**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C41,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：待办视图不完整(缺少等待/受阻/待确认分类)；更新入口分散。

**K41**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C41,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：完善个人待办视图分类。

**L41**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C41,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C41,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 42

**A42**

M2

**B42**

M2.3

**C42**

M2.3-A02

**D42**

更新Task和Forecast

**E42**

更新Task状态、真实进度和Forecast Date，区分原计划、预测和实际。

**F42**

用真实进度和日期变化更新任务。

**G42**

1. 成员能更新本人Task。
2. 更新反映真实进度。
3. 计划、预测和实际日期可区分。
4. 等待、阻塞和延期可记录。
5. 真实项目连续运行后可了解当前状态。

**H42**

1 日常更新规则｜2 Task更新记录｜3 日期和状态变化记录｜4 未更新及待确认事项清单｜5 真实项目连续运行记录

**I42**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C42,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J42**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C42,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无Forecast Date字段；原计划/预测/实际日期未分离。

**K42**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C42,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加Forecast Date字段；分离日期类型。

**L42**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C42,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C42,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 43

**A43**

M2

**B43**

M2.3

**C43**

M2.3-A03

**D43**

提交交付物或证据

**E43**

Task完成或取得结果时提交Deliverable、附件、链接或验证证据。

**F43**

完成任务时留下能够检查的结果。

**G43**

1. 成员能更新本人Task。
2. 更新反映真实进度。
3. 计划、预测和实际日期可区分。
4. 等待、阻塞和延期可记录。
5. 真实项目连续运行后可了解当前状态。

**H43**

1 日常更新规则｜2 Task更新记录｜3 日期和状态变化记录｜4 未更新及待确认事项清单｜5 真实项目连续运行记录

**I43**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C43,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J43**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C43,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无百分比进度字段；更新频率不固定。

**K43**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C43,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：考虑增加进度表达方式。

**L43**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C43,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C43,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 44

**A44**

M2

**B44**

M2.3

**C44**

M2.3-A04

**D44**

记录下一步、等待、阻塞与变化

**E44**

记录等待对象、Blocker、Milestone或MP影响、下一步、更新时间和更新人。

**F44**

说明卡在哪里、下一步做什么。

**G44**

1. 成员能更新本人Task。
2. 更新反映真实进度。
3. 计划、预测和实际日期可区分。
4. 等待、阻塞和延期可记录。
5. 真实项目连续运行后可了解当前状态。

**H44**

1 日常更新规则｜2 Task更新记录｜3 日期和状态变化记录｜4 未更新及待确认事项清单｜5 真实项目连续运行记录

**I44**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C44,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J44**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C44,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无法记录等待、阻塞状态。

**K44**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C44,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：扩展Task状态选项。

**L44**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C44,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C44,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 45

**A45**

M2

**B45**

M2.4

超链接：'Blueprint'!A18

**C45**

M2.4-A01

**D45**

识别并分类异常

**E45**

从Task、日期和依赖中识别异常，并按Risk、Issue、Delay或Blocker分类。

**F45**

把模糊偏差转化为明确异常类型。

**G45**

1. 异常分类一致。
2. 每个关键异常关联具体业务对象。
3. 事实、影响、Owner和状态明确。
4. 重复异常被识别。
5. 候选异常经确认后生效。

**H45**

1 异常识别规则｜2 异常确认流程｜3 真实异常记录｜4 重复异常处理结果｜5 异常业务验证记录

**I45**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C45,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J45**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C45,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Risk/Delay/Blocker未独立；影响评估缺失。

**K45**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C45,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：扩展异常类型。

**L45**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C45,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C45,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 46

**A46**

M2

**B46**

M2.4

**C46**

M2.4-A02

**D46**

关联影响对象

**E46**

关联受影响的Project、SKU、Milestone或Task，并明确是否影响MP或Launch。

**F46**

说清楚异常具体影响哪里。

**G46**

1. 异常分类一致。
2. 每个关键异常关联具体业务对象。
3. 事实、影响、Owner和状态明确。
4. 重复异常被识别。
5. 候选异常经确认后生效。

**H46**

1 异常识别规则｜2 异常确认流程｜3 真实异常记录｜4 重复异常处理结果｜5 异常业务验证记录

**I46**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C46,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J46**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C46,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：影响范围和严重程度未结构化。

**K46**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C46,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加影响评估字段。

**L46**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C46,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C46,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 47

**A47**

M2

**B47**

M2.4

**C47**

M2.4-A03

**D47**

记录影响、原因、Owner与确认

**E47**

记录事实、原因、影响、严重度、状态和Owner；合并重复异常；候选异常经业务确认后生效。

**F47**

异常必须有事实、影响、责任和确认。

**G47**

1. 异常分类一致。
2. 每个关键异常关联具体业务对象。
3. 事实、影响、Owner和状态明确。
4. 重复异常被识别。
5. 候选异常经确认后生效。

**H47**

1 异常识别规则｜2 异常确认流程｜3 真实异常记录｜4 重复异常处理结果｜5 异常业务验证记录

**I47**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C47,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J47**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C47,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：异常与Owner/Action关联不完整。

**K47**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C47,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：完善异常关联关系。

**L47**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C47,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C47,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 48

**A48**

M2

**B48**

M2.5

超链接：'Blueprint'!A19

**C48**

M2.5-A01

**D48**

创建Recovery Action

**E48**

针对关键异常建立具体行动，并关联来源异常和受影响对象。

**F48**

把问题转化为可执行行动。

**G48**

1. 关键异常有Action或处置结论。
2. Action有单一Owner、Due和预期结果。
3. 行动可追溯来源异常。
4. 逾期或无效行动可升级。
5. 升级有实际处理结果。

**H48**

1 Recovery Action清单｜2 Action Owner和Due记录｜3 恢复目标和结果记录｜4 升级条件与路径｜5 升级事项及处理结果

**I48**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C48,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J48**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C48,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Recovery Action完全缺失。

**K48**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C48,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立Recovery Action表。

**L48**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C48,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C48,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 49

**A49**

M2

**B49**

M2.5

**C49**

M2.5-A02

**D49**

指定Owner

**E49**

每项Recovery Action指定一个主要Owner及必要协作者。

**F49**

每项恢复行动只有一个主要负责人。

**G49**

1. 关键异常有Action或处置结论。
2. Action有单一Owner、Due和预期结果。
3. 行动可追溯来源异常。
4. 逾期或无效行动可升级。
5. 升级有实际处理结果。

**H49**

1 Recovery Action清单｜2 Action Owner和Due记录｜3 恢复目标和结果记录｜4 升级条件与路径｜5 升级事项及处理结果

**I49**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C49,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J49**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C49,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无升级流程和规则。

**K49**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C49,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：设计升级机制。

**L49**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C49,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C49,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 50

**A50**

M2

**B50**

M2.5

**C50**

M2.5-A03

**D50**

设置Due和恢复目标

**E50**

设置Due Date、预期恢复结果和判断成功的条件。

**F50**

明确何时完成、恢复到什么程度。

**G50**

1. 关键异常有Action或处置结论。
2. Action有单一Owner、Due和预期结果。
3. 行动可追溯来源异常。
4. 逾期或无效行动可升级。
5. 升级有实际处理结果。

**H50**

1 Recovery Action清单｜2 Action Owner和Due记录｜3 恢复目标和结果记录｜4 升级条件与路径｜5 升级事项及处理结果

**I50**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C50,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J50**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C50,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无行动分配和跟踪系统。

**K50**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C50,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立行动跟踪。

**L50**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C50,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C50,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 51

**A51**

M2

**B51**

M2.5

**C51**

M2.5-A04

**D51**

更新优先级、状态、进展和结果

**E51**

持续更新行动进度、优先级和实际结果，完成后进入验证。

**F51**

持续跟踪行动是否真正有效。

**G51**

1. 关键异常有Action或处置结论。
2. Action有单一Owner、Due和预期结果。
3. 行动可追溯来源异常。
4. 逾期或无效行动可升级。
5. 升级有实际处理结果。

**H51**

1 Recovery Action清单｜2 Action Owner和Due记录｜3 恢复目标和结果记录｜4 升级条件与路径｜5 升级事项及处理结果

**I51**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C51,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J51**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C51,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：升级未记录。

**K51**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C51,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：记录升级。

**L51**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C51,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C51,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 52

**A52**

M2

**B52**

M2.5

**C52**

M2.5-A05

**D52**

识别逾期无效行动并升级

**E52**

行动超期、无效或Owner无法解决时，记录升级原因、对象、所需支持和结果。

**F52**

处理不了时按明确路径获得支持。

**G52**

1. 关键异常有Action或处置结论。
2. Action有单一Owner、Due和预期结果。
3. 行动可追溯来源异常。
4. 逾期或无效行动可升级。
5. 升级有实际处理结果。

**H52**

1 Recovery Action清单｜2 Action Owner和Due记录｜3 恢复目标和结果记录｜4 升级条件与路径｜5 升级事项及处理结果

**I52**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C52,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J52**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C52,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：完全缺失。

**K52**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C52,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：设计恢复行动管理。

**L52**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C52,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C52,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 53

**A53**

M2

**B53**

M2.6

超链接：'Blueprint'!A20

**C53**

M2.6-A01

**D53**

识别待决策事项

**E53**

识别必须由管理者判断的问题，并说明不决定的影响。

**F53**

把需要权限选择的问题单独识别。

**G53**

1. 待决策事项可单独识别。
2. Decision有决策人和Due。
3. 背景、影响和选项清楚。
4. 决定和理由被记录。
5. 后续Action可追踪。

**H53**

1 待决策事项清单｜2 Decision Log｜3 决定及理由记录｜4 Decision Follow-up Action清单｜5 真实决策闭环记录

**I53**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C53,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J53**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C53,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：管理决策完全缺失。

**K53**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C53,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立Decision表。

**L53**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C53,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C53,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 54

**A54**

M2

**B54**

M2.6

**C54**

M2.6-A02

**D54**

记录背景、影响、时限、方案和建议

**E54**

准备决策背景、影响、最晚时间、选项、事实和建议。

**F54**

把决策需要的信息准备完整。

**G54**

1. 待决策事项可单独识别。
2. Decision有决策人和Due。
3. 背景、影响和选项清楚。
4. 决定和理由被记录。
5. 后续Action可追踪。

**H54**

1 待决策事项清单｜2 Decision Log｜3 决定及理由记录｜4 Decision Follow-up Action清单｜5 真实决策闭环记录

**I54**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C54,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J54**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C54,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：决策触发未定义。

**K54**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C54,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义决策触发条件。

**L54**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C54,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C54,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 55

**A55**

M2

**B55**

M2.6

**C55**

M2.6-A03

**D55**

指定决策人

**E55**

明确有权作出最终选择的Decision Maker。

**F55**

明确谁有权决定。

**G55**

1. 待决策事项可单独识别。
2. Decision有决策人和Due。
3. 背景、影响和选项清楚。
4. 决定和理由被记录。
5. 后续Action可追踪。

**H55**

1 待决策事项清单｜2 Decision Log｜3 决定及理由记录｜4 Decision Follow-up Action清单｜5 真实决策闭环记录

**I55**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C55,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J55**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C55,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：决策记录缺失。

**K55**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C55,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立决策记录。

**L55**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C55,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C55,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 56

**A56**

M2

**B56**

M2.6

**C56**

M2.6-A04

**D56**

记录决定理由

**E56**

记录最终决定、日期、理由和依据。

**F56**

留下决定了什么以及为什么。

**G56**

1. 待决策事项可单独识别。
2. Decision有决策人和Due。
3. 背景、影响和选项清楚。
4. 决定和理由被记录。
5. 后续Action可追踪。

**H56**

1 待决策事项清单｜2 Decision Log｜3 决定及理由记录｜4 Decision Follow-up Action清单｜5 真实决策闭环记录

**I56**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C56,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J56**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C56,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：决策跟踪缺失。

**K56**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C56,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立决策跟踪。

**L56**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C56,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C56,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 57

**A57**

M2

**B57**

M2.6

**C57**

M2.6-A05

**D57**

转化Action并跟踪结果

**E57**

将决定转成Follow-up Action，指定Owner和Due并跟踪结果。

**F57**

让决定落到行动和结果。

**G57**

1. 待决策事项可单独识别。
2. Decision有决策人和Due。
3. 背景、影响和选项清楚。
4. 决定和理由被记录。
5. 后续Action可追踪。

**H57**

1 待决策事项清单｜2 Decision Log｜3 决定及理由记录｜4 Decision Follow-up Action清单｜5 真实决策闭环记录

**I57**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C57,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J57**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C57,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：决策落实缺失。

**K57**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C57,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立决策落实机制。

**L57**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C57,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C57,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 58

**A58**

M2

**B58**

M2.7

超链接：'Blueprint'!A21

**C58**

M2.7-A01

**D58**

检查Action

**E58**

核对Action是否按要求完成以及Owner、Due和来源异常。

**F58**

先确认行动确实做了。

**G58**

1. Action完成后有实际Result。
2. 关键Result有证据。
3. Issue关闭前经过验证。
4. 失败时可重开或增加Action。
5. 关闭后仍可完整追溯。

**H58**

1 Action Result记录｜2 结果证据或文件链接｜3 Verification记录｜4 Issue关闭或重开记录｜5 端到端异常闭环验证报告

**I58**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C58,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J58**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C58,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：结果确认缺失。

**K58**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C58,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立结果确认流程。

**L58**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C58,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C58,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 59

**A59**

M2

**B59**

M2.7

**C59**

M2.7-A02

**D59**

记录结果

**E59**

记录Action实际产生的Result及与预期目标的差异。

**F59**

不仅写Completed，还要写实际结果。

**G59**

1. Action完成后有实际Result。
2. 关键Result有证据。
3. Issue关闭前经过验证。
4. 失败时可重开或增加Action。
5. 关闭后仍可完整追溯。

**H59**

1 Action Result记录｜2 结果证据或文件链接｜3 Verification记录｜4 Issue关闭或重开记录｜5 端到端异常闭环验证报告

**I59**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C59,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J59**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C59,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：验证关闭缺失。

**K59**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C59,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立验证关闭。

**L59**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C59,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C59,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 60

**A60**

M2

**B60**

M2.7

**C60**

M2.7-A03

**D60**

确认影响是否消除或接受

**E60**

判断原问题影响是否消除、恢复或被正式接受，并识别剩余Risk。

**F60**

确认原来的问题到底解决没有。

**G60**

1. Action完成后有实际Result。
2. 关键Result有证据。
3. Issue关闭前经过验证。
4. 失败时可重开或增加Action。
5. 关闭后仍可完整追溯。

**H60**

1 Action Result记录｜2 结果证据或文件链接｜3 Verification记录｜4 Issue关闭或重开记录｜5 端到端异常闭环验证报告

**I60**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C60,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J60**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C60,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：重开机制缺失。

**K60**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C60,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立重开机制。

**L60**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C60,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C60,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 61

**A61**

M2

**B61**

M2.7

**C61**

M2.7-A04

**D61**

指定验证人

**E61**

由合适人员独立确认结果是否满足关闭条件。

**F61**

不能只由Action Owner自己宣布关闭。

**G61**

1. Action完成后有实际Result。
2. 关键Result有证据。
3. Issue关闭前经过验证。
4. 失败时可重开或增加Action。
5. 关闭后仍可完整追溯。

**H61**

1 Action Result记录｜2 结果证据或文件链接｜3 Verification记录｜4 Issue关闭或重开记录｜5 端到端异常闭环验证报告

**I61**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C61,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J61**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C61,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：关闭记录缺失。

**K61**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C61,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立关闭记录。

**L61**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C61,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C61,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 62

**A62**

M2

**B62**

M2.7

**C62**

M2.7-A05

**D62**

提交证据

**E62**

提交支持Result和Verification的证据、附件或正式链接。

**F62**

用可检查的证据证明结果。

**G62**

1. Action完成后有实际Result。
2. 关键Result有证据。
3. Issue关闭前经过验证。
4. 失败时可重开或增加Action。
5. 关闭后仍可完整追溯。

**H62**

1 Action Result记录｜2 结果证据或文件链接｜3 Verification记录｜4 Issue关闭或重开记录｜5 端到端异常闭环验证报告

**I62**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C62,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J62**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C62,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：关闭确认缺失。

**K62**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C62,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立关闭确认。

**L62**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C62,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C62,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 63

**A63**

M2

**B63**

M2.7

**C63**

M2.7-A06

**D63**

正式关闭或重开

**E63**

验证通过后关闭；未通过时补充Action或重新打开Issue。

**F63**

真正解决才关闭。

**G63**

1. Action完成后有实际Result。
2. 关键Result有证据。
3. Issue关闭前经过验证。
4. 失败时可重开或增加Action。
5. 关闭后仍可完整追溯。

**H63**

1 Action Result记录｜2 结果证据或文件链接｜3 Verification记录｜4 Issue关闭或重开记录｜5 端到端异常闭环验证报告

**I63**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C63,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J63**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C63,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：结果归档缺失。

**K63**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C63,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立结果归档。

**L63**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C63,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C63,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 64

**A64**

M2

**B64**

M2.8

超链接：'Blueprint'!A22

**C64**

M2.8-A01

**D64**

保留计划和状态变化

**E64**

保留关键计划、Forecast、Actual、状态、Owner和影响变化。

**F64**

保存真实时间线供复盘。

**G64**

1. 关键变化可追溯。
2. 重要关闭Issue形成经验记录。
3. 经验可追溯真实Project和结果。
4. 可查找重复问题。
5. 经验能够转化为规则或模板改进。

**H64**

1 项目执行变化记录｜2 Lesson Learned记录｜3 真实问题案例库｜4 重复问题清单｜5 模板、规则或流程改进建议

**I64**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C64,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J64**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C64,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：经验沉淀缺失。

**K64**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C64,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立经验沉淀机制。

**L64**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C64,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C64,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 65

**A65**

M2

**B65**

M2.8

**C65**

M2.8-A02

**D65**

记录经验并形成可检索案例

**E65**

记录Root Cause、有效与无效Action、关键Decision、最终Result和预防建议，并反馈到模板和规则。

**F65**

把真实问题转成可搜索、可复用的案例。

**G65**

1. 关键变化可追溯。
2. 重要关闭Issue形成经验记录。
3. 经验可追溯真实Project和结果。
4. 可查找重复问题。
5. 经验能够转化为规则或模板改进。

**H65**

1 项目执行变化记录｜2 Lesson Learned记录｜3 真实问题案例库｜4 重复问题清单｜5 模板、规则或流程改进建议

**I65**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C65,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J65**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C65,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：经验复用缺失。

**K65**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C65,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立经验复用。

**L65**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C65,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C65,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-20

### Row 66

**A66**

M3

**B66**

M3.1

超链接：'Blueprint'!A23

**C66**

M3.1-A01

**D66**

展示个人工作队列

**E66**

展示今日、即将到期、逾期、待更新、待确认，以及本人负责的异常和Action。

**F66**

打开一个页面就知道自己要做什么。

**G66**

1. 个人工作项完整且属于当前用户。
2. 到期、逾期、异常和待确认分类准确。
3. 用户能直接更新并提交结果。
4. 能从个人事项进入完整项目背景。

**H66**

1 My Daily Work页面｜2 个人工作分类规则｜3 直接更新与结果提交功能｜4 真实用户操作验证记录

**I66**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C66,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J66**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C66,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：缺少异常、行动和待确认事项聚合。

**K66**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C66,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强个人入口功能。

**L66**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C66,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C66,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 67

**A67**

M3

**B67**

M3.1

**C67**

M3.1-A02

**D67**

支持执行与查看背景

**E67**

支持直接更新状态、提交结果，并进入所属Project、SKU或Issue查看完整背景。

**F67**

不仅能看待办，还能直接处理并知道为什么做。

**G67**

1. 个人工作项完整且属于当前用户。
2. 到期、逾期、异常和待确认分类准确。
3. 用户能直接更新并提交结果。
4. 能从个人事项进入完整项目背景。

**H67**

1 My Daily Work页面｜2 个人工作分类规则｜3 直接更新与结果提交功能｜4 真实用户操作验证记录

**I67**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C67,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J67**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C67,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：更新动作分散；无一键完成。

**K67**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C67,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：优化更新动作。

**L67**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C67,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C67,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 68

**A68**

M3

**B68**

M3.2

超链接：'Blueprint'!A24

**C68**

M3.2-A01

**D68**

展示完整项目情况

**E68**

展示Project、SKU、Stage、健康、Milestone、Task、异常、Action、待决策及缺失信息。

**F68**

一个页面看清项目整体和关键问题。

**G68**

1. 项目信息完整且来源一致。
2. 异常状态可下钻到具体原因。
3. 项目负责人可直接维护必要信息。
4. 真实项目审查无需另做解释性报告。

**H68**

1 Project Workspace｜2 项目展示和下钻规则｜3 项目更新与审查功能｜4 真实项目管理验证记录

**I68**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C68,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J68**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C68,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：缺少项目工作空间(结构+计划+异常+决定集中)。

**K68**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C68,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立项目工作空间。

**L68**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C68,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C68,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 69

**A69**

M3

**B69**

M3.2

**C69**

M3.2-A02

**D69**

支持更新、审查和下钻

**E69**

支持更新关键事实、审查异常与行动，并下钻到具体SKU、Task、Issue、Owner和Result。

**F69**

项目负责人能在同一入口发现原因并推动处理。

**G69**

1. 项目信息完整且来源一致。
2. 异常状态可下钻到具体原因。
3. 项目负责人可直接维护必要信息。
4. 真实项目审查无需另做解释性报告。

**H69**

1 Project Workspace｜2 项目展示和下钻规则｜3 项目更新与审查功能｜4 真实项目管理验证记录

**I69**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C69,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J69**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C69,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：项目集中维护能力不足。

**K69**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C69,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强项目管理视图。

**L69**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C69,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C69,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 70

**A70**

M3

**B70**

M3.3

超链接：'Blueprint'!A25

**C70**

M3.3-A01

**D70**

展示异常处理队列

**E70**

展示开放、缺Owner、缺Action、缺Due、逾期和待验证关闭的异常。

**F70**

集中看到哪些问题还没有被正确处理。

**G70**

1. 异常分类和筛选准确。
2. 每条异常可直接进入处理动作。
3. 缺失和逾期事项清楚可见。
4. 真实异常能在入口中完成端到端操作。

**H70**

1 异常处理工作台｜2 异常队列和筛选规则｜3 异常处理动作清单｜4 真实异常操作验证记录

**I70**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C70,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J70**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C70,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：缺少工作队列(缺Owner/缺Action/逾期/待关闭)。

**K70**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C70,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立异常工作队列。

**L70**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C70,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C70,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 71

**A71**

M3

**B71**

M3.3

**C71**

M3.3-A02

**D71**

支持异常全流程处理

**E71**

支持分配Owner、创建Action、更新、升级、发起Decision、提交验证和关闭。

**F71**

在同一入口把问题从发现一路处理到关闭。

**G71**

1. 异常分类和筛选准确。
2. 每条异常可直接进入处理动作。
3. 缺失和逾期事项清楚可见。
4. 真实异常能在入口中完成端到端操作。

**H71**

1 异常处理工作台｜2 异常队列和筛选规则｜3 异常处理动作清单｜4 真实异常操作验证记录

**I71**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C71,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J71**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C71,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：处理动作不完整。

**K71**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C71,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强异常处理能力。

**L71**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C71,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C71,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 72

**A72**

M3

**B72**

M3.4

超链接：'Blueprint'!A26

**C72**

M3.4-A01

**D72**

展示周度审查内容

**E72**

展示健康、变化、偏差、Top Risk、逾期、缺失、待决策和上周Action结果。

**F72**

周会先看真正需要讨论和决定的事项。

**G72**

1. 周会所需关键事实来自统一数据。
2. 上周Action结果可见。
3. 会议决定和新Action写回系统。
4. 下周期能够验证结果。

**H72**

1 周度管理视图｜2 周度审查清单｜3 Decision与Action回写记录｜4 连续周度运行验证记录

**I72**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C72,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J72**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C72,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：周报基于数据生成，但周度审查流程未结构化。

**K72**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C72,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立周度审查流程。

**L72**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C72,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C72,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 73

**A73**

M3

**B73**

M3.4

**C73**

M3.4-A02

**D73**

支持确认、决定和行动回写

**E73**

在审查中确认状态、记录决定、创建或更新Action，并保留下周期验证要求。

**F73**

周会结论直接变成系统里的决定和行动。

**G73**

1. 周会所需关键事实来自统一数据。
2. 上周Action结果可见。
3. 会议决定和新Action写回系统。
4. 下周期能够验证结果。

**H73**

1 周度管理视图｜2 周度审查清单｜3 Decision与Action回写记录｜4 连续周度运行验证记录

**I73**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C73,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J73**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C73,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：会议结果无法写回系统。

**K73**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C73,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：设计会议结果写回。

**L73**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C73,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C73,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 74

**A74**

M3

**B74**

M3.5

超链接：'Blueprint'!A27

**C74**

M3.5-A01

**D74**

展示领导关注事项

**E74**

展示组合健康、关键风险与延误、受影响Milestone和需要领导决定的事项。

**F74**

先看哪些项目需要管理关注。

**G74**

1. 组合结论由底层事实支持。
2. 重大异常和待决策事项没有被汇总掩盖。
3. 可下钻到Owner、Action和Result。
4. 领导决定可继续追踪落实。

**H74**

1 Leadership View｜2 组合健康与筛选规则｜3 完整下钻路径｜4 领导审查验证记录

**I74**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C74,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J74**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C74,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：组合健康、重大风险视图缺失。

**K74**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C74,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立领导审查看板。

**L74**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C74,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C74,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-20

### Row 75

**A75**

M3

**B75**

M3.5

**C75**

M3.5-A02

**D75**

逐层下钻到事实和责任

**E75**

从组合下钻到Project、SKU、异常、Action、Owner、Due和Result。

**F75**

每个红色结论都能找到具体原因和责任。

**G75**

1. 组合结论由底层事实支持。
2. 重大异常和待决策事项没有被汇总掩盖。
3. 可下钻到Owner、Action和Result。
4. 领导决定可继续追踪落实。

**H75**

1 Leadership View｜2 组合健康与筛选规则｜3 完整下钻路径｜4 领导审查验证记录

**I75**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C75,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J75**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C75,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：逐层下钻到事实/责任/结果缺失。

**K75**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C75,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立下钻能力。

**L75**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C75,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C75,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-20

### Row 76

**A76**

M3

**B76**

M3.6

超链接：'Blueprint'!A28

**C76**

M3.6-A01

**D76**

删除无用字段

**E76**

识别不支持决策、执行或追溯的字段，并删除、隐藏或移出核心页面。

**F76**

只保留真正需要使用的信息。

**G76**

1. 核心动作能够快速完成。
2. 同一事实不需要无规则重复维护。
3. 用户知道下一步和责任。
4. 用户问题转成有Owner和验收的改进任务。

**H76**

1 字段和页面精简清单｜2 核心动作流程｜3 使用说明｜4 用户问题与优先级清单｜5 改进验证记录

**I76**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C76,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J76**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C76,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：字段冗余和重复录入问题存在。

**K76**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C76,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：优化UI减少冗余。

**L76**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C76,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C76,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 77

**A77**

M3

**B77**

M3.6

**C77**

M3.6-A02

**D77**

减少重复录入和页面切换

**E77**

同一事实尽量一次维护、多处使用，减少在多个页面或系统重复填写。

**F77**

让用户少填、少找、少切换。

**G77**

1. 核心动作能够快速完成。
2. 同一事实不需要无规则重复维护。
3. 用户知道下一步和责任。
4. 用户问题转成有Owner和验收的改进任务。

**H77**

1 字段和页面精简清单｜2 核心动作流程｜3 使用说明｜4 用户问题与优先级清单｜5 改进验证记录

**I77**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C77,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J77**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C77,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：页面切换频繁。

**K77**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C77,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：减少页面切换。

**L77**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C77,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C77,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 78

**A78**

M3

**B78**

M3.6

**C78**

M3.6-A03

**D78**

突出下一步

**E78**

在页面中明确显示下一步、Owner、Due和需要确认或决定的事项。

**F78**

用户一眼知道接下来做什么。

**G78**

1. 核心动作能够快速完成。
2. 同一事实不需要无规则重复维护。
3. 用户知道下一步和责任。
4. 用户问题转成有Owner和验收的改进任务。

**H78**

1 字段和页面精简清单｜2 核心动作流程｜3 使用说明｜4 用户问题与优先级清单｜5 改进验证记录

**I78**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C78,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J78**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C78,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：用户反馈收集缺失。

**K78**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C78,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立反馈收集。

**L78**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C78,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C78,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 79

**A79**

M3

**B79**

M3.6

**C79**

M3.6-A04

**D79**

简化更新

**E79**

缩短日常更新步骤，减少不必要必填项和复杂操作。

**F79**

让真实用户愿意持续更新。

**G79**

1. 核心动作能够快速完成。
2. 同一事实不需要无规则重复维护。
3. 用户知道下一步和责任。
4. 用户问题转成有Owner和验收的改进任务。

**H79**

1 字段和页面精简清单｜2 核心动作流程｜3 使用说明｜4 用户问题与优先级清单｜5 改进验证记录

**I79**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C79,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J79**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C79,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：反馈分类排序缺失。

**K79**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C79,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立反馈管理。

**L79**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C79,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C79,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 80

**A80**

M3

**B80**

M3.6

**C80**

M3.6-A05

**D80**

提供说明

**E80**

为容易误解的字段、状态和操作提供简单说明或示例。

**F80**

避免用户靠猜测使用系统。

**G80**

1. 核心动作能够快速完成。
2. 同一事实不需要无规则重复维护。
3. 用户知道下一步和责任。
4. 用户问题转成有Owner和验收的改进任务。

**H80**

1 字段和页面精简清单｜2 核心动作流程｜3 使用说明｜4 用户问题与优先级清单｜5 改进验证记录

**I80**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C80,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J80**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C80,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：改进验收缺失。

**K80**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C80,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立改进验收。

**L80**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C80,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C80,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 81

**A81**

M3

**B81**

M3.6

**C81**

M3.6-A06

**D81**

收集并排序用户问题

**E81**

收集真实用户问题，按影响和频率排序，并转成明确修复任务。

**F81**

用真实使用问题持续改进页面。

**G81**

1. 核心动作能够快速完成。
2. 同一事实不需要无规则重复维护。
3. 用户知道下一步和责任。
4. 用户问题转成有Owner和验收的改进任务。

**H81**

1 字段和页面精简清单｜2 核心动作流程｜3 使用说明｜4 用户问题与优先级清单｜5 改进验证记录

**I81**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C81,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J81**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C81,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：体验度量缺失。

**K81**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C81,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立体验度量。

**L81**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C81,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C81,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 82

**A82**

M4

**B82**

M4.1

超链接：'Blueprint'!A29

**C82**

M4.1-A01

**D82**

建立导入模板

**E82**

定义项目、SKU、计划和任务导入所需字段、格式和示例。

**F82**

先给用户一个统一可用的导入格式。

**G82**

1. 正确数据可成功导入。
2. 错误记录被拦截并说明原因。
3. 重复记录不被再次创建。
4. 错误导入可以修正或回退。

**H82**

1 导入模板｜2 导入校验规则｜3 ID与Owner匹配规则｜4 错误报告｜5 重试与回退验证记录

**I82**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C82,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J82**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C82,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：格式错误检测和防护可增强。

**K82**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C82,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强格式校验。（原始评级：大部分覆盖）

**L82**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C82,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C82,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 83

**A83**

M4

**B83**

M4.1

**C83**

M4.1-A02

**D83**

校验格式

**E83**

导入前检查必填字段、日期、编号和字段格式。

**F83**

错误数据先拦住，不直接进入系统。

**G83**

1. 正确数据可成功导入。
2. 错误记录被拦截并说明原因。
3. 重复记录不被再次创建。
4. 错误导入可以修正或回退。

**H83**

1 导入模板｜2 导入校验规则｜3 ID与Owner匹配规则｜4 错误报告｜5 重试与回退验证记录

**I83**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C83,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J83**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C83,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：极少数无法匹配的项目需人工处理。

**K83**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C83,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强无法匹配项处理。（原始评级：大部分覆盖）

**L83**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C83,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C83,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 84

**A84**

M4

**B84**

M4.1

**C84**

M4.1-A03

**D84**

匹配ID和Owner

**E84**

将导入记录匹配到正确的Project、SKU和人员。

**F84**

确保数据进到正确项目并找到正确责任人。

**G84**

1. 正确数据可成功导入。
2. 错误记录被拦截并说明原因。
3. 重复记录不被再次创建。
4. 错误导入可以修正或回退。

**H84**

1 导入模板｜2 导入校验规则｜3 ID与Owner匹配规则｜4 错误报告｜5 重试与回退验证记录

**I84**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C84,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J84**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C84,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：错误覆盖保护(空白保护)已实现。

**K84**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C84,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：持续优化。（原始评级：大部分覆盖）

**L84**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C84,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C84,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 85

**A85**

M4

**B85**

M4.1

**C85**

M4.1-A04

**D85**

防重复和静默覆盖

**E85**

识别已有记录，禁止未提示的重复创建和覆盖。

**F85**

不让导入悄悄制造重复或改坏真实数据。

**G85**

1. 正确数据可成功导入。
2. 错误记录被拦截并说明原因。
3. 重复记录不被再次创建。
4. 错误导入可以修正或回退。

**H85**

1 导入模板｜2 导入校验规则｜3 ID与Owner匹配规则｜4 错误报告｜5 重试与回退验证记录

**I85**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C85,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J85**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C85,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增量导入机制未建立。

**K85**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C85,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：考虑增量导入。（原始评级：大部分覆盖）

**L85**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C85,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C85,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 86

**A86**

M4

**B86**

M4.1

**C86**

M4.1-A05

**D86**

显示错误

**E86**

清楚显示失败记录、错误原因和需要修正的位置。

**F86**

让用户知道哪里错、怎么修。

**G86**

1. 正确数据可成功导入。
2. 错误记录被拦截并说明原因。
3. 重复记录不被再次创建。
4. 错误导入可以修正或回退。

**H86**

1 导入模板｜2 导入校验规则｜3 ID与Owner匹配规则｜4 错误报告｜5 重试与回退验证记录

**I86**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C86,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J86**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C86,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：日志和回退能力有限。

**K86**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C86,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强日志和回退。（原始评级：大部分覆盖）

**L86**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C86,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C86,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 87

**A87**

M4

**B87**

M4.1

**C87**

M4.1-A06

**D87**

支持修正和回退

**E87**

允许修正后重新导入，并在错误导入时安全撤销。

**F87**

导入失败或出错后能够恢复。

**G87**

1. 正确数据可成功导入。
2. 错误记录被拦截并说明原因。
3. 重复记录不被再次创建。
4. 错误导入可以修正或回退。

**H87**

1 导入模板｜2 导入校验规则｜3 ID与Owner匹配规则｜4 错误报告｜5 重试与回退验证记录

**I87**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C87,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J87**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C87,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：CSV格式校验有限。

**K87**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C87,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强CSV校验。

**L87**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C87,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C87,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 88

**A88**

M4

**B88**

M4.2

超链接：'Blueprint'!A30

**C88**

M4.2-A01

**D88**

计算到期、逾期、Next Milestone和偏差

**E88**

按统一日期和状态规则生成执行结果。

**F88**

让系统自动发现时间和计划偏差。

**G88**

1. 计算结果与规则一致。
2. 边界场景通过测试。
3. 每个结果能看到依据。
4. 人工调整有权限和记录。

**H88**

1 计算规则表｜2 异常和冲突规则｜3 计算依据展示｜4 边界测试记录｜5 授权确认规则

**I88**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C88,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J88**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C88,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Next Milestone/偏差计算不存在；计算依据未展示。

**K88**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C88,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加自动计算字段。

**L88**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C88,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C88,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 89

**A89**

M4

**B89**

M4.2

**C89**

M4.2-A02

**D89**

识别缺失与冲突

**E89**

识别缺Owner、缺日期、状态冲突、Project与SKU日期冲突等情况。

**F89**

自动找出数据和业务逻辑问题。

**G89**

1. 计算结果与规则一致。
2. 边界场景通过测试。
3. 每个结果能看到依据。
4. 人工调整有权限和记录。

**H89**

1 计算规则表｜2 异常和冲突规则｜3 计算依据展示｜4 边界测试记录｜5 授权确认规则

**I89**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C89,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J89**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C89,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：未自动化为系统字段；仅脚本临时检查。

**K89**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C89,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立系统级自动检测。

**L89**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C89,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C89,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 90

**A90**

M4

**B90**

M4.2

**C90**

M4.2-A03

**D90**

展示依据并支持授权确认

**E90**

显示计算使用的日期、状态和规则，并允许授权人员确认或处理例外。

**F90**

系统结论必须能解释，例外必须受控。

**G90**

1. 计算结果与规则一致。
2. 边界场景通过测试。
3. 每个结果能看到依据。
4. 人工调整有权限和记录。

**H90**

1 计算规则表｜2 异常和冲突规则｜3 计算依据展示｜4 边界测试记录｜5 授权确认规则

**I90**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C90,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J90**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C90,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：偏差计算缺失。

**K90**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C90,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立偏差计算。

**L90**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C90,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C90,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 91

**A91**

M4

**B91**

M4.3

超链接：'Blueprint'!A31

**C91**

M4.3-A01

**D91**

建立关键提醒

**E91**

建立Task和Action到期、逾期、缺失信息及关键Delay提醒。

**F91**

在需要行动时提醒正确的人。

**G91**

1. 提醒对象和内容准确。
2. 已完成事项停止提醒。
3. 重复提醒受控。
4. 长期无响应事项可升级。
5. 提醒和响应可追溯。

**H91**

1 提醒规则｜2 提醒模板｜3 去重与停止规则｜4 升级规则｜5 提醒与响应验证记录

**I91**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C91,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J91**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C91,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：重复提醒控制缺失；响应和升级记录不存在。

**K91**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C91,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强提醒控制。

**L91**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C91,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C91,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 92

**A92**

M4

**B92**

M4.3

**C92**

M4.3-A02

**D92**

建立去重、停止、升级及响应记录

**E92**

控制重复提醒，事项完成后停止，长期无响应时升级，并记录处理结果。

**F92**

提醒不能骚扰，也不能发完就不管。

**G92**

1. 提醒对象和内容准确。
2. 已完成事项停止提醒。
3. 重复提醒受控。
4. 长期无响应事项可升级。
5. 提醒和响应可追溯。

**H92**

1 提醒规则｜2 提醒模板｜3 去重与停止规则｜4 升级规则｜5 提醒与响应验证记录

**I92**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C92,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J92**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C92,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：升级流程完全缺失。

**K92**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C92,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立升级流程。

**L92**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C92,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C92,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 93

**A93**

M4

**B93**

M4.4

超链接：'Blueprint'!A32

**C93**

M4.4-A01

**D93**

汇总状态、变化、风险、延误、行动和决定

**E93**

从项目执行数据形成报告所需内容。

**F93**

报告内容来自统一事实，不重新收集一遍。

**G93**

1. 报告来自统一数据。
2. 关键缺失和冲突清楚标记。
3. 内容可下钻到来源。
4. 发布前有人工确认。

**H93**

1 报告字段映射｜2 周报模板与草稿｜3 缺失待确认规则｜4 来源与下钻路径｜5 报告确认记录

**I93**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C93,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J93**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C93,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：周报内容有限；缺少管理报告。

**K93**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C93,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强报告内容。

**L93**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C93,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C93,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 94

**A94**

M4

**B94**

M4.4

**C94**

M4.4-A02

**D94**

生成周报

**E94**

按已确认模板自动形成项目或SKU周报草稿。

**F94**

系统自动准备周报初稿。

**G94**

1. 报告来自统一数据。
2. 关键缺失和冲突清楚标记。
3. 内容可下钻到来源。
4. 发布前有人工确认。

**H94**

1 报告字段映射｜2 周报模板与草稿｜3 缺失待确认规则｜4 来源与下钻路径｜5 报告确认记录

**I94**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C94,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：已完成

**J94**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C94,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：管理报告缺失。

**K94**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C94,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立管理报告。

**L94**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C94,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C94,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-04

### Row 95

**A95**

M4

**B95**

M4.4

**C95**

M4.4-A03

**D95**

标记缺失待确认

**E95**

对缺数据、冲突或无法确认的内容明确标记。

**F95**

不知道的内容不编造，直接提示待确认。

**G95**

1. 报告来自统一数据。
2. 关键缺失和冲突清楚标记。
3. 内容可下钻到来源。
4. 发布前有人工确认。

**H95**

1 报告字段映射｜2 周报模板与草稿｜3 缺失待确认规则｜4 来源与下钻路径｜5 报告确认记录

**I95**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C95,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J95**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C95,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：缺失信息不透明。

**K95**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C95,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加缺失信息展示。

**L95**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C95,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C95,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 96

**A96**

M4

**B96**

M4.4

**C96**

M4.4-A04

**D96**

保留来源、下钻、确认和导出

**E96**

报告内容可追溯来源、下钻到记录、人工确认并按需要导出。

**F96**

每项结论都能找到依据并在发布前确认。

**G96**

1. 报告来自统一数据。
2. 关键缺失和冲突清楚标记。
3. 内容可下钻到来源。
4. 发布前有人工确认。

**H96**

1 报告字段映射｜2 周报模板与草稿｜3 缺失待确认规则｜4 来源与下钻路径｜5 报告确认记录

**I96**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C96,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J96**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C96,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：发布前确认缺失。

**K96**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C96,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增加发布前确认。

**L96**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C96,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C96,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 97

**A97**

M4

**B97**

M4.5

超链接：'Blueprint'!A33

**C97**

M4.5-A01

**D97**

确认必要数据范围

**E97**

明确Phase 1必须从PMO读取哪些对象和字段。

**F97**

只连接试点真正需要的数据。

**G97**

1. 必要主数据可稳定读取。
2. 对象和日期匹配正确。
3. 冲突与失败不被静默忽略。
4. 同步结果可追溯和对账。

**H97**

1 必要数据范围清单｜2 字段与对象映射｜3 读取验证记录｜4 冲突清单｜5 同步日志与对账结果

**I97**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C97,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J97**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C97,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Programme匹配通过文本(非linked record)。

**K97**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C97,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强匹配方式。（原始评级：大部分覆盖）

**L97**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C97,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C97,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 98

**A98**

M4

**B98**

M4.5

**C98**

M4.5-A02

**D98**

建立对象和日期映射

**E98**

建立Programme、Project、SKU及目标日期的对应关系。

**F98**

让两边的同一对象正确对应。

**G98**

1. 必要主数据可稳定读取。
2. 对象和日期匹配正确。
3. 冲突与失败不被静默忽略。
4. 同步结果可追溯和对账。

**H98**

1 必要数据范围清单｜2 字段与对象映射｜3 读取验证记录｜4 冲突清单｜5 同步日志与对账结果

**I98**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C98,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J98**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C98,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：SKU匹配完全缺失。

**K98**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C98,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立SKU匹配。

**L98**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C98,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C98,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 99

**A99**

M4

**B99**

M4.5

**C99**

M4.5-A03

**D99**

验证读取

**E99**

用真实数据验证读取结果的完整性和准确性。

**F99**

确认连接真的拿到了正确数据。

**G99**

1. 必要主数据可稳定读取。
2. 对象和日期匹配正确。
3. 冲突与失败不被静默忽略。
4. 同步结果可追溯和对账。

**H99**

1 必要数据范围清单｜2 字段与对象映射｜3 读取验证记录｜4 冲突清单｜5 同步日志与对账结果

**I99**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C99,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J99**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C99,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：部分里程碑日期为空。

**K99**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C99,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：补全日期数据。

**L99**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C99,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C99,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 100

**A100**

M4

**B100**

M4.5

**C100**

M4.5-A04

**D100**

识别变化冲突

**E100**

识别上游变化、AutoPM本地变化及二者冲突。

**F100**

数据变化时不能悄悄覆盖。

**G100**

1. 必要主数据可稳定读取。
2. 对象和日期匹配正确。
3. 冲突与失败不被静默忽略。
4. 同步结果可追溯和对账。

**H100**

1 必要数据范围清单｜2 字段与对象映射｜3 读取验证记录｜4 冲突清单｜5 同步日志与对账结果

**I100**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C100,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J100**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C100,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：冲突检测有限；无自动告警。

**K100**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C100,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强冲突检测。

**L100**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C100,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C100,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 101

**A101**

M4

**B101**

M4.5

**C101**

M4.5-A05

**D101**

记录同步并对账

**E101**

记录同步时间、结果、失败和差异，并定期与正式来源核对。

**F101**

知道同步是否成功，数据是否一致。

**G101**

1. 必要主数据可稳定读取。
2. 对象和日期匹配正确。
3. 冲突与失败不被静默忽略。
4. 同步结果可追溯和对账。

**H101**

1 必要数据范围清单｜2 字段与对象映射｜3 读取验证记录｜4 冲突清单｜5 同步日志与对账结果

**I101**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C101,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J101**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C101,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：同步失败恢复机制不完善。

**K101**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C101,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：增强失败恢复。

**L101**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C101,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C101,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 102

**A102**

M4

**B102**

M4.6

超链接：'Blueprint'!A34

**C102**

M4.6-A01

**D102**

定义权限模型

**E102**

定义角色、项目范围、查看、编辑、确认、审批、导出和敏感字段权限。

**F102**

让正确的人只能做被允许的操作。

**G102**

1. 角色权限清楚。
2. 关键操作可追溯。
3. 越权测试被阻止并记录。
4. 真实试点用户获得正确访问范围。

**H102**

1 权限矩阵｜2 审计字段和日志要求｜3 测试账号与场景｜4 越权测试记录

**I102**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C102,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J102**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C102,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：字段级权限控制不存在(Airtable限制)。

**K102**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C102,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：评估权限需求。

**L102**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C102,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C102,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 103

**A103**

M4

**B103**

M4.6

**C103**

M4.6-A02

**D103**

记录关键操作

**E103**

记录关键数据和权限的创建、修改、确认、审批和导出。

**F103**

重要操作留下可追溯记录。

**G103**

1. 角色权限清楚。
2. 关键操作可追溯。
3. 越权测试被阻止并记录。
4. 真实试点用户获得正确访问范围。

**H103**

1 权限矩阵｜2 审计字段和日志要求｜3 测试账号与场景｜4 越权测试记录

**I103**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C103,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J103**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C103,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：自定义审计记录不存在。

**K103**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C103,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立自定义审计。

**L103**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C103,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C103,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 104

**A104**

M4

**B104**

M4.6

**C104**

M4.6-A03

**D104**

测试越权

**E104**

用不同角色测试不能访问或修改的场景。

**F104**

证明权限不只是写在文档里。

**G104**

1. 角色权限清楚。
2. 关键操作可追溯。
3. 越权测试被阻止并记录。
4. 真实试点用户获得正确访问范围。

**H104**

1 权限矩阵｜2 审计字段和日志要求｜3 测试账号与场景｜4 越权测试记录

**I104**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C104,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J104**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C104,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：导出控制缺失。

**K104**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C104,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：评估导出控制。

**L104**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C104,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C104,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 105

**A105**

M4

**B105**

M4.7

超链接：'Blueprint'!A35

**C105**

M4.7-A01

**D105**

记录自动化和同步结果

**E105**

记录每次运行的时间、对象、结果和处理数量。

**F105**

先知道系统做了什么、是否成功。

**G105**

1. 失败及时发现。
2. 故障有Owner和状态。
3. 重试不产生重复。
4. 错误数据不污染正式记录。
5. 关键流程有回退方案。

**H105**

1 运行日志｜2 监控和告警规则｜3 故障处理清单｜4 安全重试验证｜5 数据保护和回退记录

**I105**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C105,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J105**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C105,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无持久化监控；无告警。

**K105**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C105,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立持久化监控。

**L105**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C105,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C105,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 106

**A106**

M4

**B106**

M4.7

**C106**

M4.7-A02

**D106**

监控异常

**E106**

识别失败、超时、重复、异常数量和数据差异。

**F106**

自动发现运行故障。

**G106**

1. 失败及时发现。
2. 故障有Owner和状态。
3. 重试不产生重复。
4. 错误数据不污染正式记录。
5. 关键流程有回退方案。

**H106**

1 运行日志｜2 监控和告警规则｜3 故障处理清单｜4 安全重试验证｜5 数据保护和回退记录

**I106**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C106,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J106**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C106,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：失败告警缺失。

**K106**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C106,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立告警机制。

**L106**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C106,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C106,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 107

**A107**

M4

**B107**

M4.7

**C107**

M4.7-A03

**D107**

告警并分配Owner

**E107**

重大失败及时通知并指定处理人。

**F107**

故障必须有人负责。

**G107**

1. 失败及时发现。
2. 故障有Owner和状态。
3. 重试不产生重复。
4. 错误数据不污染正式记录。
5. 关键流程有回退方案。

**H107**

1 运行日志｜2 监控和告警规则｜3 故障处理清单｜4 安全重试验证｜5 数据保护和回退记录

**I107**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C107,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J107**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C107,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：责任分配缺失。

**K107**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C107,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立责任分配。

**L107**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C107,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C107,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 108

**A108**

M4

**B108**

M4.7

**C108**

M4.7-A04

**D108**

支持安全重试

**E108**

重试不会重复创建或重复执行已成功部分。

**F108**

失败后再运行也不能造成重复。

**G108**

1. 失败及时发现。
2. 故障有Owner和状态。
3. 重试不产生重复。
4. 错误数据不污染正式记录。
5. 关键流程有回退方案。

**H108**

1 运行日志｜2 监控和告警规则｜3 故障处理清单｜4 安全重试验证｜5 数据保护和回退记录

**I108**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C108,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J108**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C108,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：重试机制缺失。

**K108**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C108,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立重试机制。

**L108**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C108,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C108,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 109

**A109**

M4

**B109**

M4.7

**C109**

M4.7-A05

**D109**

防数据污染

**E109**

失败时阻止不完整或错误数据进入正式记录。

**F109**

先保护真实数据。

**G109**

1. 失败及时发现。
2. 故障有Owner和状态。
3. 重试不产生重复。
4. 错误数据不污染正式记录。
5. 关键流程有回退方案。

**H109**

1 运行日志｜2 监控和告警规则｜3 故障处理清单｜4 安全重试验证｜5 数据保护和回退记录

**I109**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C109,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J109**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C109,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：回退能力缺失。

**K109**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C109,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立回退能力。

**L109**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C109,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C109,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 110

**A110**

M4

**B110**

M4.7

**C110**

M4.7-A06

**D110**

建立回退

**E110**

严重错误时能够恢复到运行前状态。

**F110**

出大问题时能够撤回。

**G110**

1. 失败及时发现。
2. 故障有Owner和状态。
3. 重试不产生重复。
4. 错误数据不污染正式记录。
5. 关键流程有回退方案。

**H110**

1 运行日志｜2 监控和告警规则｜3 故障处理清单｜4 安全重试验证｜5 数据保护和回退记录

**I110**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C110,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J110**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C110,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：运行报告缺失。

**K110**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C110,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立运行报告。

**L110**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C110,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C110,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 111

**A111**

M5

**B111**

M5.1

超链接：'Blueprint'!A36

**C111**

M5.1-A01

**D111**

确认Pilot范围

**E111**

确认试点目标、团队、负责人、项目清单、选择标准、参与角色、使用承诺及启动、暂停、退出条件。

**F111**

先把谁用、用什么项目、要证明什么说清楚。

**G111**

1. 目标、项目、团队和角色确认。
2. 项目选择有代表性。
3. 启动和退出条件清楚。
4. 未确认数量和周期保持TBD。

**H111**

1 Pilot范围说明｜2 试点项目清单｜3 参与角色和负责人｜4 启动暂停退出条件

**I111**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C111,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J111**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C111,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：无试点范围确认文档。

**K111**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C111,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义试点范围和启动条件。

**L111**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C111,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C111,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-04

### Row 112

**A112**

M5

**B112**

M5.2

超链接：'Blueprint'!A37

**C112**

M5.2-A01

**D112**

定义Pilot角色责任

**E112**

定义执行人员、项目负责人、职能Owner、管理者、Data Owner和平台支持责任。

**F112**

每类数据和行动都知道谁负责，PM不代替所有人维护。

**G112**

1. 每类关键数据有维护责任。
2. 每类行动有执行和确认责任。
3. 管理决定和平台问题有明确Owner。

**H112**

1 Pilot角色责任矩阵｜2 数据与行动责任清单｜3 平台支持责任清单

**I112**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C112,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J112**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C112,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：角色与责任未正式定义。

**K112**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C112,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义Pilot角色和责任。

**L112**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C112,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C112,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 113

**A113**

M5

**B113**

M5.3

超链接：'Blueprint'!A38

**C113**

M5.3-A01

**D113**

定义Pilot使用规则

**E113**

定义必须维护的信息、更新频率、异常与Action规则、升级关闭条件、人工确认和最低证据。

**F113**

让所有试点项目按同一基本方法使用。

**G113**

1. 用户知道何时更新什么。
2. 关键异常和Action按统一规则处理。
3. 关键事实保留人工确认。
4. 最低证据要求明确。

**H113**

1 Pilot使用规则｜2 更新时间和责任要求｜3 异常Action升级关闭规则｜4 最低证据清单

**I113**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C113,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J113**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C113,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：使用规则完全缺失。

**K113**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C113,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：编写使用规则。

**L113**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C113,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C113,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-18

### Row 114

**A114**

M5

**B114**

M5.4

超链接：'Blueprint'!A39

**C114**

M5.4-A01

**D114**

建立过渡方案

**E114**

明确唯一维护位置、旧工具范围、读取写入和链接方向、冲突失败、停止条件及回退方案。

**F114**

避免用户长期重复维护两套相同数据。

**G114**

1. 同一事实有唯一维护位置。
2. 同步和冲突规则清楚。
3. 切换和回退不丢数据。
4. 结束双维护条件明确。

**H114**

1 双系统过渡方案｜2 数据唯一维护矩阵｜3 同步与冲突规则｜4 停止与回退条件

**I114**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C114,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J114**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C114,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：唯一维护位置/冲突处理/退出方式未定义。

**K114**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C114,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义双系统过渡规则。

**L114**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C114,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C114,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 115

**A115**

M5

**B115**

M5.5

超链接：'Blueprint'!A40

**C115**

M5.5-A01

**D115**

完成真实角色操作

**E115**

使用真实项目完成Task更新、异常维护、Action确认、管理审查和Decision。

**F115**

是否上手看真实操作，不看是否参加过培训。

**G115**

1. 关键角色完成真实核心动作。
2. 操作结果正确。
3. 理解偏差被记录并处理。
4. 不能只以登录或培训作为完成。

**H115**

1 角色上手清单｜2 真实操作记录｜3 问题与理解偏差清单｜4 首轮改进任务

**I115**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C115,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J115**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C115,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：其他关键角色未上手；理解偏差未记录。

**K115**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C115,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：扩展到更多角色。

**L115**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C115,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C115,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 116

**A116**

M5

**B116**

M5.5

**C116**

M5.5-A02

**D116**

记录问题和理解偏差

**E116**

记录用户不会做、做错、理解不一致或流程不清的地方。

**F116**

把上手困难转成具体改进问题。

**G116**

1. 关键角色完成真实核心动作。
2. 操作结果正确。
3. 理解偏差被记录并处理。
4. 不能只以登录或培训作为完成。

**H116**

1 角色上手清单｜2 真实操作记录｜3 问题与理解偏差清单｜4 首轮改进任务

**I116**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C116,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J116**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C116,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：使用问题记录缺失。

**K116**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C116,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立问题记录。

**L116**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C116,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C116,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 117

**A117**

M5

**B117**

M5.6

超链接：'Blueprint'!A41

**C117**

M5.6-A01

**D117**

按规则更新

**E117**

用户在规定时间前更新Task、异常、Action和Forecast。

**F117**

会前先把真实状态更新好。

**G117**

1. 真实项目持续更新。
2. 周会直接使用AutoPM数据。
3. 决定和Action及时回写。
4. 下周期验证结果。

**H117**

1 周度运行日历｜2 会前更新与检查清单｜3 周报和异常清单｜4 周会决定与Action记录｜5 下周期验证记录

**I117**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C117,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：已完成

**J117**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C117,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：周度审查循环未结构化。

**K117**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C117,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：结构化周度审查。

**L117**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C117,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C117,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 118

**A118**

M5

**B118**

M5.6

**C118**

M5.6-A02

**D118**

检查数据

**E118**

检查缺失、冲突、未更新和异常闭环问题。

**F118**

先确保周会使用的数据可信。

**G118**

1. 真实项目持续更新。
2. 周会直接使用AutoPM数据。
3. 决定和Action及时回写。
4. 下周期验证结果。

**H118**

1 周度运行日历｜2 会前更新与检查清单｜3 周报和异常清单｜4 周会决定与Action记录｜5 下周期验证记录

**I118**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C118,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J118**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C118,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：检查/审查/决定/行动循环缺失。

**K118**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C118,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立周度循环。

**L118**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C118,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C118,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-30

### Row 119

**A119**

M5

**B119**

M5.6

**C119**

M5.6-A03

**D119**

生成异常和周报

**E119**

形成异常清单和周报草稿。

**F119**

把需要讨论的重点准备出来。

**G119**

1. 真实项目持续更新。
2. 周会直接使用AutoPM数据。
3. 决定和Action及时回写。
4. 下周期验证结果。

**H119**

1 周度运行日历｜2 会前更新与检查清单｜3 周报和异常清单｜4 周会决定与Action记录｜5 下周期验证记录

**I119**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C119,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J119**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C119,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：结果验证循环缺失。

**K119**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C119,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立验证循环。

**L119**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C119,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C119,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 120

**A120**

M5

**B120**

M5.6

**C120**

M5.6-A04

**D120**

开展周度审查

**E120**

围绕偏差、Risk、Delay、Action和Decision开展管理审查。

**F120**

周会重点推动问题和决定。

**G120**

1. 真实项目持续更新。
2. 周会直接使用AutoPM数据。
3. 决定和Action及时回写。
4. 下周期验证结果。

**H120**

1 周度运行日历｜2 会前更新与检查清单｜3 周报和异常清单｜4 周会决定与Action记录｜5 下周期验证记录

**I120**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C120,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J120**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C120,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：行动跟踪缺失。

**K120**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C120,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立行动跟踪。

**L120**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C120,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C120,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 121

**A121**

M5

**B121**

M5.6

**C121**

M5.6-A05

**D121**

回写决定和Action

**E121**

把会议决定和新Action写回AutoPM。

**F121**

会议结果直接变成可追踪记录。

**G121**

1. 真实项目持续更新。
2. 周会直接使用AutoPM数据。
3. 决定和Action及时回写。
4. 下周期验证结果。

**H121**

1 周度运行日历｜2 会前更新与检查清单｜3 周报和异常清单｜4 周会决定与Action记录｜5 下周期验证记录

**I121**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C121,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J121**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C121,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：决策记录缺失。

**K121**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C121,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立决策记录。

**L121**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C121,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C121,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 122

**A122**

M5

**B122**

M5.6

**C122**

M5.6-A06

**D122**

下周期验证结果

**E122**

下周检查上周Action和Decision是否产生结果。

**F122**

每周验证上一轮承诺有没有落地。

**G122**

1. 真实项目持续更新。
2. 周会直接使用AutoPM数据。
3. 决定和Action及时回写。
4. 下周期验证结果。

**H122**

1 周度运行日历｜2 会前更新与检查清单｜3 周报和异常清单｜4 周会决定与Action记录｜5 下周期验证记录

**I122**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C122,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J122**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C122,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：循环记录缺失。

**K122**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C122,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立循环记录。

**L122**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C122,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C122,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-23

### Row 123

**A123**

M5

**B123**

M5.7

超链接：'Blueprint'!A42

**C123**

M5.7-A01

**D123**

建立反馈入口

**E123**

提供统一的问题和建议提交位置。

**F123**

用户知道遇到问题去哪里反馈。

**G123**

1. 关键问题有分类、影响、Owner和状态。
2. 高优先级问题及时处理。
3. 修复经真实用户验证。
4. 重复问题形成系统性改进。

**H123**

1 反馈入口｜2 用户问题清单｜3 优先级和Owner｜4 修复与用户验证记录｜5 重复反馈改进清单

**I123**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C123,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J123**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C123,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：问题收集未系统化。

**K123**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C123,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：系统化问题收集。

**L123**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C123,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C123,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 124

**A124**

M5

**B124**

M5.7

**C124**

M5.7-A02

**D124**

分类问题

**E124**

区分数据、规则、流程、功能、自动化和培训问题。

**F124**

先判断问题属于哪一类。

**G124**

1. 关键问题有分类、影响、Owner和状态。
2. 高优先级问题及时处理。
3. 修复经真实用户验证。
4. 重复问题形成系统性改进。

**H124**

1 反馈入口｜2 用户问题清单｜3 优先级和Owner｜4 修复与用户验证记录｜5 重复反馈改进清单

**I124**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C124,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J124**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C124,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：问题分类排序缺失。

**K124**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C124,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立问题分类。

**L124**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C124,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C124,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 125

**A125**

M5

**B125**

M5.7

**C125**

M5.7-A03

**D125**

评估影响优先级

**E125**

按影响范围、业务阻塞和出现频率排序。

**F125**

先修最影响Pilot运行的问题。

**G125**

1. 关键问题有分类、影响、Owner和状态。
2. 高优先级问题及时处理。
3. 修复经真实用户验证。
4. 重复问题形成系统性改进。

**H125**

1 反馈入口｜2 用户问题清单｜3 优先级和Owner｜4 修复与用户验证记录｜5 重复反馈改进清单

**I125**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C125,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J125**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C125,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：优先级排序缺失。

**K125**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C125,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立优先级。

**L125**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C125,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C125,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 126

**A126**

M5

**B126**

M5.7

**C126**

M5.7-A04

**D126**

分配Owner

**E126**

为每个重要问题指定处理人和目标日期。

**F126**

每个问题都有人负责。

**G126**

1. 关键问题有分类、影响、Owner和状态。
2. 高优先级问题及时处理。
3. 修复经真实用户验证。
4. 重复问题形成系统性改进。

**H126**

1 反馈入口｜2 用户问题清单｜3 优先级和Owner｜4 修复与用户验证记录｜5 重复反馈改进清单

**I126**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C126,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J126**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C126,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：修复流程不系统。

**K126**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C126,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：系统化修复流程。

**L126**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C126,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C126,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 127

**A127**

M5

**B127**

M5.7

**C127**

M5.7-A05

**D127**

验证修复

**E127**

由实际用户确认问题是否解决。

**F127**

修复完成后必须由使用者验证。

**G127**

1. 关键问题有分类、影响、Owner和状态。
2. 高优先级问题及时处理。
3. 修复经真实用户验证。
4. 重复问题形成系统性改进。

**H127**

1 反馈入口｜2 用户问题清单｜3 优先级和Owner｜4 修复与用户验证记录｜5 重复反馈改进清单

**I127**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C127,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J127**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C127,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：验证缺失。

**K127**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C127,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立验证。

**L127**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C127,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C127,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-16

### Row 128

**A128**

M5

**B128**

M5.7

**C128**

M5.7-A06

**D128**

转化重复反馈

**E128**

将反复出现的问题转成规则、模板、设计或培训改进。

**F128**

不要每次单独救火，要解决根因。

**G128**

1. 关键问题有分类、影响、Owner和状态。
2. 高优先级问题及时处理。
3. 修复经真实用户验证。
4. 重复问题形成系统性改进。

**H128**

1 反馈入口｜2 用户问题清单｜3 优先级和Owner｜4 修复与用户验证记录｜5 重复反馈改进清单

**I128**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C128,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J128**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C128,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：系统性改进缺失。

**K128**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C128,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立系统性改进。

**L128**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C128,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C128,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 129

**A129**

M6

**B129**

M6.1

超链接：'Blueprint'!A43

**C129**

M6.1-A01

**D129**

定义业务基线

**E129**

定义人工追踪、周报汇总、数据质量、Task、Issue、Action和Delay等基线指标。

**F129**

先记录现在是什么水平，后面才知道有没有改善。

**G129**

1. 指标定义清楚。
2. 来源和Owner明确。
3. Pilot前完成记录。
4. 无基线不宣称改善。

**H129**

1 基线指标字典｜2 数据来源和计算方法｜3 Pilot前基线记录｜4 基线确认记录

**I129**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C129,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J129**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C129,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：基线定义完全缺失。

**K129**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C129,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：记录当前工作方式基线。

**L129**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C129,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C129,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 130

**A130**

M6

**B130**

M6.1

**C130**

M6.1-A02

**D130**

锁定口径并记录基线

**E130**

明确计算方法、来源、Owner和采集周期，并在Pilot前保存基线。

**F130**

基线必须能重复计算，不靠感觉。

**G130**

1. 指标定义清楚。
2. 来源和Owner明确。
3. Pilot前完成记录。
4. 无基线不宣称改善。

**H130**

1 基线指标字典｜2 数据来源和计算方法｜3 Pilot前基线记录｜4 基线确认记录

**I130**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C130,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J130**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C130,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：基线指标缺失。

**K130**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C130,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义基线指标。

**L130**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C130,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C130,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 131

**A131**

M6

**B131**

M6.2

超链接：'Blueprint'!A44

**C131**

M6.2-A01

**D131**

记录真实采用情况

**E131**

记录活跃项目和用户、更新频率及时性、周度审查、关键动作、中断退出及双系统维护。

**F131**

区分真正持续使用和只试了一次。

**G131**

1. 采用证据来自真实项目行为。
2. 能够区分登录、录入和持续使用。
3. 中断、退出和额外负担如实记录。

**H131**

1 Pilot使用证据包｜2 活跃项目与用户记录｜3 关键动作和周度审查记录｜4 中断退出与双维护记录

**I131**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C131,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J131**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C131,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：持续使用证据未收集。

**K131**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C131,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：收集使用证据。

**L131**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C131,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C131,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 132

**A132**

M6

**B132**

M6.3

超链接：'Blueprint'!A45

**C132**

M6.3-A01

**D132**

记录数据质量结果

**E132**

记录字段、关系、Owner、Due和状态完整性，以及重复、冲突、同步失败、修正和关闭。

**F132**

用数据证明AutoPM里的信息是否可信。

**G132**

1. 指标可重复计算。
2. 问题可追溯到记录。
3. 修正和关闭有证据。
4. 能够形成管理可用性结论。

**H132**

1 数据质量指标结果｜2 问题与修复记录｜3 同步和冲突记录｜4 数据可用性结论

**I132**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C132,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：进行中

**J132**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C132,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：可重复指标未定义。

**K132**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C132,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：定义数据质量指标。

**L132**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C132,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C132,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-09

### Row 133

**A133**

M6

**B133**

M6.4

超链接：'Blueprint'!A46

**C133**

M6.4-A01

**D133**

记录执行闭环结果

**E133**

记录Task按期逾期、异常Action覆盖、责任日期、Delay恢复、Issue验证关闭和Decision转Action。

**F133**

用真实记录证明问题是否从发现走到结果。

**G133**

1. Action完成和Issue关闭被区分。
2. 闭环中断点可识别。
3. 关键异常有结果和验证。
4. Decision能够转成并完成Action。

**H133**

1 执行闭环指标｜2 中断点清单｜3 真实异常闭环案例｜4 Decision执行记录

**I133**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C133,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J133**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C133,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：闭环证据完全缺失。

**K133**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C133,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：建立闭环证据收集。

**L133**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C133,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C133,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-06

### Row 134

**A134**

M6

**B134**

M6.5

超链接：'Blueprint'!A47

**C134**

M6.5-A01

**D134**

比较效率与处理结果

**E134**

比较信息查找、周报汇总、人工追问、重复维护，以及问题发现、升级和关闭。

**F134**

比较Pilot前后工作方式是否真的改善。

**G134**

1. 比较基于已确认基线。
2. 改善和负面影响同时呈现。
3. 结论与证据一致。
4. 数据不足处明确标记。

**H134**

1 Pilot前后比较｜2 新增工作与负面影响记录｜3 业务结果案例｜4 价值结论

**I134**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C134,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J134**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C134,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：效率对比缺失。

**K134**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C134,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：设计效率对比。

**L134**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C134,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C134,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 135

**A135**

M6

**B135**

M6.5

**C135**

M6.5-A02

**D135**

记录新增工作和负面影响

**E135**

记录AutoPM带来的新维护成本、重复操作、使用阻碍及管理决定的实际结果。

**F135**

价值评估不能只看好处。

**G135**

1. 比较基于已确认基线。
2. 改善和负面影响同时呈现。
3. 结论与证据一致。
4. 数据不足处明确标记。

**H135**

1 Pilot前后比较｜2 新增工作与负面影响记录｜3 业务结果案例｜4 价值结论

**I135**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C135,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J135**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C135,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：新增工作评估缺失。

**K135**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C135,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：评估新增工作。

**L135**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C135,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C135,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-13

### Row 136

**A136**

M6

**B136**

M6.5

**C136**

M6.5-A03

**D136**

形成证据结论

**E136**

综合基线和Pilot结果，说明改善、未改善、负面影响和证据不足。

**F136**

给出真实结论，不为了证明成功而挑数据。

**G136**

1. 比较基于已确认基线。
2. 改善和负面影响同时呈现。
3. 结论与证据一致。
4. 数据不足处明确标记。

**H136**

1 Pilot前后比较｜2 新增工作与负面影响记录｜3 业务结果案例｜4 价值结论

**I136**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C136,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J136**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C136,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：业务结果衡量缺失。

**K136**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C136,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：衡量业务结果。

**L136**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C136,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C136,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 137

**A137**

M6

**B137**

M6.6

超链接：'Blueprint'!A48

**C137**

M6.6-A01

**D137**

评估平台能力和技术路线

**E137**

评估性能容量、中国访问、权限审计、自动化集成、导出迁移回退、支持、许可成本及Phase 2技术路线。

**F137**

判断当前平台能否继续支撑，哪些限制必须解决。

**G137**

1. 评估基于真实Pilot使用。
2. 事实、限制和建议分开。
3. 迁移与回退能力明确。
4. 不预设当前平台一定是最终方案。

**H137**

1 平台能力评估｜2 限制与风险清单｜3 许可和支持评估｜4 Phase 2技术路线建议

**I137**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C137,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J137**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C137,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：性能/集成/迁移/成本评估未做。

**K137**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C137,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：评估平台能力。

**L137**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C137,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C137,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-10-30

### Row 138

**A138**

M6

**B138**

M6.7

超链接：'Blueprint'!A49

**C138**

M6.7-A01

**D138**

汇总证据

**E138**

汇总数据质量、执行闭环、采用、效率、业务结果和平台证据。

**F138**

把所有决定所需事实放在一起。

**G138**

1. 全部结论有证据支持。
2. 成功条件逐项评估。
3. 缺口和风险透明。
4. 正式决定、理由和条件被记录。

**H138**

1 Gate 1证据包｜2 成功条件评估｜3 缺口与风险清单｜4 下一步建议｜5 正式Decision及Phase 2进入条件

**I138**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C138,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J138**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C138,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：Gate决策完全缺失。

**K138**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C138,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：准备Gate决策。

**L138**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C138,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C138,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-11-27

### Row 139

**A139**

M6

**B139**

M6.7

**C139**

M6.7-A02

**D139**

评估成功条件

**E139**

逐项判断Phase 1成功标准是否满足。

**F139**

不是看做了多少功能，而是看是否达到目标。

**G139**

1. 全部结论有证据支持。
2. 成功条件逐项评估。
3. 缺口和风险透明。
4. 正式决定、理由和条件被记录。

**H139**

1 Gate 1证据包｜2 成功条件评估｜3 缺口与风险清单｜4 下一步建议｜5 正式Decision及Phase 2进入条件

**I139**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C139,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J139**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C139,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：证据汇总缺失。

**K139**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C139,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：汇总Phase 1证据。

**L139**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C139,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C139,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-11

### Row 140

**A140**

M6

**B140**

M6.7

**C140**

M6.7-A03

**D140**

识别缺口风险

**E140**

列出未完成能力、证据不足和扩大使用风险。

**F140**

把不能进入下一阶段的原因说清楚。

**G140**

1. 全部结论有证据支持。
2. 成功条件逐项评估。
3. 缺口和风险透明。
4. 正式决定、理由和条件被记录。

**H140**

1 Gate 1证据包｜2 成功条件评估｜3 缺口与风险清单｜4 下一步建议｜5 正式Decision及Phase 2进入条件

**I140**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C140,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J140**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C140,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：成功条件评估缺失。

**K140**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C140,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：评估成功条件。

**L140**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C140,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C140,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 141

**A141**

M6

**B141**

M6.7

**C141**

M6.7-A04

**D141**

提出下一步建议

**E141**

基于证据提出继续、调整、延长、迁移或停止建议。

**F141**

给决策人清楚的可选方向。

**G141**

1. 全部结论有证据支持。
2. 成功条件逐项评估。
3. 缺口和风险透明。
4. 正式决定、理由和条件被记录。

**H141**

1 Gate 1证据包｜2 成功条件评估｜3 缺口与风险清单｜4 下一步建议｜5 正式Decision及Phase 2进入条件

**I141**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C141,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J141**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C141,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：决策选项缺失。

**K141**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C141,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：准备决策选项。

**L141**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C141,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C141,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun / 2026-09-25

### Row 142

**A142**

M6

**B142**

M6.7

**C142**

M6.7-A05

**D142**

明确Phase 2条件和正式决定

**E142**

记录正式Decision、理由、条件、Owner和后续行动。

**F142**

只有正式决定并满足条件后才进入Phase 2。

**G142**

1. 全部结论有证据支持。
2. 成功条件逐项评估。
3. 缺口和风险透明。
4. 正式决定、理由和条件被记录。

**H142**

1 Gate 1证据包｜2 成功条件评估｜3 缺口与风险清单｜4 下一步建议｜5 正式Decision及Phase 2进入条件

**I142**

=IFERROR(INDEX('Implementation Check'!$P$8:$P$1000,MATCH($C142,'Implementation Check'!$C$8:$C$1000,0)),"未开始")

缓存值：未开始

**J142**

=IFERROR(INDEX('Implementation Check'!$L$8:$L$1000,MATCH($C142,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：正式决策缺失。

**K142**

=IFERROR(INDEX('Implementation Check'!$M$8:$M$1000,MATCH($C142,'Implementation Check'!$C$8:$C$1000,0)),"")

缓存值：进行正式决策。

**L142**

=IFERROR(INDEX('Implementation Check'!$N$8:$N$1000,MATCH($C142,'Implementation Check'!$C$8:$C$1000,0))&" / "&TEXT(INDEX('Implementation Check'!$O$8:$O$1000,MATCH($C142,'Implementation Check'!$C$8:$C$1000,0)),"yyyy-mm-dd"),"")

缓存值：Sun Sun+主管 / 2026-11-27

## Task Execution

### Row 1

**A1**

AutoPM Phase 1 | Task Execution

### Row 3

**A3**

目标任务执行表：每项任务都包含简单解释、预期产出和验收标准。蓝色字段用于维护；未确认内容保持TBD。

### Row 5

**A5**

规则：TARGET表示从Phase 1目标独立推导的任务；已开发不等于正确，当前实现必须在Implementation Check中单独审查。

### Row 7

**A7**

Phase

**B7**

模块

**C7**

模块名称

**D7**

能力包

**E7**

能力包名称

**F7**

Action ID

**G7**

具体任务

**H7**

简单解释

**I7**

预期产出

**J7**

验收标准

**K7**

依据状态

**L7**

前置依赖

**M7**

Owner

**N7**

目标日期

**O7**

执行状态

**P7**

成熟度

**Q7**

验收证据

### Row 8

**A8**

Phase 1

**B8**

M1

**C8**

执行数据基础

**D8**

M1.1

**E8**

业务对象定义

**F8**

M1.1-A01

**G8**

定义项目结构对象

**H8**

明确Programme、Project、SKU等层级分别代表什么，以及一个Project如何包含多个SKU。

**I8**

对象清单、定义及系统归属表

**J8**

对象定义唯一清晰，边界和系统归属明确

**K8**

TARGET

**L8**

TBD

**M8**

TBD

**N8**

TBD

**O8**

进行中

**P8**

已定义

### Row 9

**A9**

Phase 1

**B9**

M1

**C9**

执行数据基础

**D9**

M1.1

**E9**

业务对象定义

**F9**

M1.1-A02

**G9**

定义计划执行对象

**H9**

明确阶段、里程碑、任务和交付物分别表达什么，避免日期和状态混用。

**I9**

对象清单、定义及系统归属表

**J9**

对象定义唯一清晰，边界和系统归属明确

**K9**

TARGET

**L9**

TBD

**M9**

TBD

**N9**

TBD

**O9**

未开始

**P9**

已定义

### Row 10

**A10**

Phase 1

**B10**

M1

**C10**

执行数据基础

**D10**

M1.1

**E10**

业务对象定义

**F10**

M1.1-A03

**G10**

定义异常对象

**H10**

明确Risk、Issue、Delay和Blocker如何区分，以及异常应该关联到哪个业务对象。

**I10**

对象清单、定义及系统归属表

**J10**

对象定义唯一清晰，边界和系统归属明确

**K10**

TARGET

**L10**

TBD

**M10**

TBD

**N10**

TBD

**O10**

未开始

**P10**

已定义

### Row 11

**A11**

Phase 1

**B11**

M1

**C11**

执行数据基础

**D11**

M1.1

**E11**

业务对象定义

**F11**

M1.1-A04

**G11**

定义恢复与决策对象

**H11**

明确问题发生后如何记录恢复行动、责任人、管理决定、实际结果和验证关闭。

**I11**

对象清单、定义及系统归属表

**J11**

对象定义唯一清晰，边界和系统归属明确

**K11**

TARGET

**L11**

TBD

**M11**

TBD

**N11**

TBD

**O11**

未开始

**P11**

已定义

### Row 12

**A12**

Phase 1

**B12**

M1

**C12**

执行数据基础

**D12**

M1.1

**E12**

业务对象定义

**F12**

M1.1-A05

**G12**

定义组织责任对象

**H12**

明确人员、团队、角色、执行责任、确认责任和决策责任如何区分。

**I12**

对象清单、定义及系统归属表

**J12**

对象定义唯一清晰，边界和系统归属明确

**K12**

TARGET

**L12**

TBD

**M12**

TBD

**N12**

TBD

**O12**

未开始

**P12**

已定义

### Row 13

**A13**

Phase 1

**B13**

M1

**C13**

执行数据基础

**D13**

M1.1

**E13**

业务对象定义

**F13**

M1.1-A06

**G13**

确认对象系统归属

**H13**

明确每类数据在哪里创建、在哪里维护、谁负责，以及AutoPM是读取、引用、计算还是写入。

**I13**

对象清单、定义及系统归属表

**J13**

对象定义唯一清晰，边界和系统归属明确

**K13**

TARGET

**L13**

TBD

**M13**

TBD

**N13**

TBD

**O13**

进行中

**P13**

已定义

### Row 14

**A14**

Phase 1

**B14**

M1

**C14**

执行数据基础

**D14**

M1.2

**E14**

对象关系模型

**F14**

M1.2-A01

**G14**

建立项目层级、计划、责任、异常和恢复结果关系

**H14**

完成“建立项目层级、计划、责任、异常和恢复结果关系”，使“对象关系模型”能够按统一规则执行、检查并留下可验证结果。

**I14**

业务对象关系图及关系规则

**J14**

任务、异常和行动可追溯，汇总可下钻，无孤立核心记录

**K14**

TARGET

**L14**

TBD

**M14**

TBD

**N14**

TBD

**O14**

未开始

**P14**

已定义

### Row 15

**A15**

Phase 1

**B15**

M1

**C15**

执行数据基础

**D15**

M1.2

**E15**

对象关系模型

**F15**

M1.2-A02

**G15**

建立汇总下钻规则

**H15**

完成“建立汇总下钻规则”，使“对象关系模型”能够按统一规则执行、检查并留下可验证结果。

**I15**

业务对象关系图及关系规则

**J15**

任务、异常和行动可追溯，汇总可下钻，无孤立核心记录

**K15**

TARGET

**L15**

TBD

**M15**

TBD

**N15**

TBD

**O15**

未开始

**P15**

已定义

### Row 16

**A16**

Phase 1

**B16**

M1

**C16**

执行数据基础

**D16**

M1.2

**E16**

对象关系模型

**F16**

M1.2-A03

**G16**

处理跨项目和多SKU关系

**H16**

完成“处理跨项目和多SKU关系”，使“对象关系模型”能够按统一规则执行、检查并留下可验证结果。

**I16**

业务对象关系图及关系规则

**J16**

任务、异常和行动可追溯，汇总可下钻，无孤立核心记录

**K16**

TARGET

**L16**

TBD

**M16**

TBD

**N16**

TBD

**O16**

未开始

**P16**

已定义

### Row 17

**A17**

Phase 1

**B17**

M1

**C17**

执行数据基础

**D17**

M1.3

**E17**

唯一标识与映射

**F17**

M1.3-A01

**G17**

定义Project、SKU、Milestone、Task、Issue、Action和Decision标识

**H17**

完成“定义Project、SKU、Milestone、Task、Issue、Action和Decision标识”，使“唯一标识与映射”能够按统一规则执行、检查并留下可验证结果。

**I17**

唯一标识、映射和去重规则

**J17**

同一对象不重复，上下游稳定匹配，历史记录可处理

**K17**

TARGET

**L17**

TBD

**M17**

TBD

**N17**

TBD

**O17**

进行中

**P17**

已定义

### Row 18

**A18**

Phase 1

**B18**

M1

**C18**

执行数据基础

**D18**

M1.3

**E18**

唯一标识与映射

**F18**

M1.3-A02

**G18**

建立上游映射、去重和历史无ID处理规则

**H18**

完成“建立上游映射、去重和历史无ID处理规则”，使“唯一标识与映射”能够按统一规则执行、检查并留下可验证结果。

**I18**

唯一标识、映射和去重规则

**J18**

同一对象不重复，上下游稳定匹配，历史记录可处理

**K18**

TARGET

**L18**

TBD

**M18**

TBD

**N18**

TBD

**O18**

进行中

**P18**

已定义

### Row 19

**A19**

Phase 1

**B19**

M1

**C19**

执行数据基础

**D19**

M1.4

**E19**

字段与状态标准

**F19**

M1.4-A01

**G19**

定义身份、责任、日期、生命周期、健康、执行和数据确认字段

**H19**

完成“定义身份、责任、日期、生命周期、健康、执行和数据确认字段”，使“字段与状态标准”能够按统一规则执行、检查并留下可验证结果。

**I19**

字段字典、状态字典和转换规则

**J19**

日期和状态不混用，状态条件明确，自动结果可解释

**K19**

TARGET

**L19**

TBD

**M19**

TBD

**N19**

TBD

**O19**

进行中

**P19**

已定义

### Row 20

**A20**

Phase 1

**B20**

M1

**C20**

执行数据基础

**D20**

M1.4

**E20**

字段与状态标准

**F20**

M1.4-A02

**G20**

定义状态转换、重开和关闭规则

**H20**

完成“定义状态转换、重开和关闭规则”，使“字段与状态标准”能够按统一规则执行、检查并留下可验证结果。

**I20**

字段字典、状态字典和转换规则

**J20**

日期和状态不混用，状态条件明确，自动结果可解释

**K20**

TARGET

**L20**

TBD

**M20**

TBD

**N20**

TBD

**O20**

未开始

**P20**

已定义

### Row 21

**A21**

Phase 1

**B21**

M1

**C21**

执行数据基础

**D21**

M1.5

**E21**

数据来源与责任

**F21**

M1.5-A01

**G21**

确认关键字段正式来源

**H21**

完成“确认关键字段正式来源”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**I21**

数据来源矩阵、责任矩阵和读写规则

**J21**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**K21**

TARGET

**L21**

TBD

**M21**

TBD

**N21**

TBD

**O21**

进行中

**P21**

已定义

### Row 22

**A22**

Phase 1

**B22**

M1

**C22**

执行数据基础

**D22**

M1.5

**E22**

数据来源与责任

**F22**

M1.5-A02

**G22**

明确读写计算引用边界

**H22**

完成“明确读写计算引用边界”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**I22**

数据来源矩阵、责任矩阵和读写规则

**J22**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**K22**

TARGET

**L22**

TBD

**M22**

TBD

**N22**

TBD

**O22**

未开始

**P22**

已定义

### Row 23

**A23**

Phase 1

**B23**

M1

**C23**

执行数据基础

**D23**

M1.5

**E23**

数据来源与责任

**F23**

M1.5-A03

**G23**

指定业务与数据Owner

**H23**

完成“指定业务与数据Owner”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**I23**

数据来源矩阵、责任矩阵和读写规则

**J23**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**K23**

TARGET

**L23**

TBD

**M23**

TBD

**N23**

TBD

**O23**

未开始

**P23**

已定义

### Row 24

**A24**

Phase 1

**B24**

M1

**C24**

执行数据基础

**D24**

M1.5

**E24**

数据来源与责任

**F24**

M1.5-A04

**G24**

定义冲突、失败和双系统维护规则

**H24**

完成“定义冲突、失败和双系统维护规则”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**I24**

数据来源矩阵、责任矩阵和读写规则

**J24**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**K24**

TARGET

**L24**

TBD

**M24**

TBD

**N24**

TBD

**O24**

未开始

**P24**

已定义

### Row 25

**A25**

Phase 1

**B25**

M1

**C25**

执行数据基础

**D25**

M1.6

**E25**

真实项目数据初始化

**F25**

M1.6-A01

**G25**

确认试点项目

**H25**

完成“确认试点项目”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**I25**

可运行试点数据及修复清单

**J25**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**K25**

TARGET

**L25**

TBD

**M25**

TBD

**N25**

TBD

**O25**

未开始

**P25**

已定义

### Row 26

**A26**

Phase 1

**B26**

M1

**C26**

执行数据基础

**D26**

M1.6

**E26**

真实项目数据初始化

**F26**

M1.6-A02

**G26**

清理记录

**H26**

完成“清理记录”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**I26**

可运行试点数据及修复清单

**J26**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**K26**

TARGET

**L26**

TBD

**M26**

TBD

**N26**

TBD

**O26**

进行中

**P26**

已定义

### Row 27

**A27**

Phase 1

**B27**

M1

**C27**

执行数据基础

**D27**

M1.6

**E27**

真实项目数据初始化

**F27**

M1.6-A03

**G27**

建立Project与SKU关系

**H27**

完成“建立Project与SKU关系”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**I27**

可运行试点数据及修复清单

**J27**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**K27**

TARGET

**L27**

TBD

**M27**

TBD

**N27**

TBD

**O27**

未开始

**P27**

已定义

### Row 28

**A28**

Phase 1

**B28**

M1

**C28**

执行数据基础

**D28**

M1.6

**E28**

真实项目数据初始化

**F28**

M1.6-A04

**G28**

导入Milestone、Task、成员、异常和Action

**H28**

完成“导入Milestone、Task、成员、异常和Action”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**I28**

可运行试点数据及修复清单

**J28**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**K28**

TARGET

**L28**

TBD

**M28**

TBD

**N28**

TBD

**O28**

进行中

**P28**

已定义

### Row 29

**A29**

Phase 1

**B29**

M1

**C29**

执行数据基础

**D29**

M1.6

**E29**

真实项目数据初始化

**F29**

M1.6-A05

**G29**

完成业务抽样

**H29**

完成“完成业务抽样”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**I29**

可运行试点数据及修复清单

**J29**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**K29**

TARGET

**L29**

TBD

**M29**

TBD

**N29**

TBD

**O29**

未开始

**P29**

已定义

### Row 30

**A30**

Phase 1

**B30**

M1

**C30**

执行数据基础

**D30**

M1.7

**E30**

数据质量与审计

**F30**

M1.7-A01

**G30**

建立必填、关系、重复、冲突、未更新和业务逻辑检查

**H30**

完成“建立必填、关系、重复、冲突、未更新和业务逻辑检查”，使“数据质量与审计”能够按统一规则执行、检查并留下可验证结果。

**I30**

质量规则、问题清单和审计记录

**J30**

问题可识别、分配和关闭，关键变化可追溯

**K30**

TARGET

**L30**

TBD

**M30**

TBD

**N30**

TBD

**O30**

进行中

**P30**

已定义

### Row 31

**A31**

Phase 1

**B31**

M1

**C31**

执行数据基础

**D31**

M1.7

**E31**

数据质量与审计

**F31**

M1.7-A02

**G31**

记录关键变更和数据产生方式

**H31**

完成“记录关键变更和数据产生方式”，使“数据质量与审计”能够按统一规则执行、检查并留下可验证结果。

**I31**

质量规则、问题清单和审计记录

**J31**

问题可识别、分配和关闭，关键变化可追溯

**K31**

TARGET

**L31**

TBD

**M31**

TBD

**N31**

TBD

**O31**

未开始

**P31**

已定义

### Row 32

**A32**

Phase 1

**B32**

M1

**C32**

执行数据基础

**D32**

M1.7

**E32**

数据质量与审计

**F32**

M1.7-A03

**G32**

关闭质量问题

**H32**

完成“关闭质量问题”，使“数据质量与审计”能够按统一规则执行、检查并留下可验证结果。

**I32**

质量规则、问题清单和审计记录

**J32**

问题可识别、分配和关闭，关键变化可追溯

**K32**

TARGET

**L32**

TBD

**M32**

TBD

**N32**

TBD

**O32**

未开始

**P32**

已定义

### Row 33

**A33**

Phase 1

**B33**

M2

**C33**

项目执行与问题闭环

**D33**

M2.1

**E33**

项目进入与初始化

**F33**

M2.1-A01

**G33**

识别新增与重复项目

**H33**

完成“识别新增与重复项目”，使“项目进入与初始化”能够按统一规则执行、检查并留下可验证结果。

**I33**

已初始化项目及范围责任记录

**J33**

项目身份唯一，结构、责任和模板明确

**K33**

TARGET

**L33**

TBD

**M33**

TBD

**N33**

TBD

**O33**

进行中

**P33**

已定义

### Row 34

**A34**

Phase 1

**B34**

M2

**C34**

项目执行与问题闭环

**D34**

M2.1

**E34**

项目进入与初始化

**F34**

M2.1-A02

**G34**

确认Programme、Project Group、SKU、类型、阶段、范围、负责人、成员和模板

**H34**

完成“确认Programme、Project Group、SKU、类型、阶段、范围、负责人、成员和模板”，使“项目进入与初始化”能够按统一规则执行、检查并留下可验证结果。

**I34**

已初始化项目及范围责任记录

**J34**

项目身份唯一，结构、责任和模板明确

**K34**

TARGET

**L34**

TBD

**M34**

TBD

**N34**

TBD

**O34**

未开始

**P34**

已定义

### Row 35

**A35**

Phase 1

**B35**

M2

**C35**

项目执行与问题闭环

**D35**

M2.2

**E35**

计划与任务建立

**F35**

M2.2-A01

**G35**

建立阶段和Milestone

**H35**

完成“建立阶段和Milestone”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**I35**

项目基线计划及任务责任清单

**J35**

关键里程碑和任务有日期、责任、依赖并可执行

**K35**

TARGET

**L35**

TBD

**M35**

TBD

**N35**

TBD

**O35**

进行中

**P35**

已定义

### Row 36

**A36**

Phase 1

**B36**

M2

**C36**

项目执行与问题闭环

**D36**

M2.2

**E36**

计划与任务建立

**F36**

M2.2-A02

**G36**

导入或生成Task

**H36**

完成“导入或生成Task”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**I36**

项目基线计划及任务责任清单

**J36**

关键里程碑和任务有日期、责任、依赖并可执行

**K36**

TARGET

**L36**

TBD

**M36**

TBD

**N36**

TBD

**O36**

进行中

**P36**

已定义

### Row 37

**A37**

Phase 1

**B37**

M2

**C37**

项目执行与问题闭环

**D37**

M2.2

**E37**

计划与任务建立

**F37**

M2.2-A03

**G37**

明确交付物和依赖

**H37**

完成“明确交付物和依赖”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**I37**

项目基线计划及任务责任清单

**J37**

关键里程碑和任务有日期、责任、依赖并可执行

**K37**

TARGET

**L37**

TBD

**M37**

TBD

**N37**

TBD

**O37**

未开始

**P37**

已定义

### Row 38

**A38**

Phase 1

**B38**

M2

**C38**

项目执行与问题闭环

**D38**

M2.2

**E38**

计划与任务建立

**F38**

M2.2-A04

**G38**

分配Owner

**H38**

完成“分配Owner”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**I38**

项目基线计划及任务责任清单

**J38**

关键里程碑和任务有日期、责任、依赖并可执行

**K38**

TARGET

**L38**

TBD

**M38**

TBD

**N38**

TBD

**O38**

进行中

**P38**

已定义

### Row 39

**A39**

Phase 1

**B39**

M2

**C39**

项目执行与问题闭环

**D39**

M2.2

**E39**

计划与任务建立

**F39**

M2.2-A05

**G39**

设置Baseline与Due

**H39**

完成“设置Baseline与Due”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**I39**

项目基线计划及任务责任清单

**J39**

关键里程碑和任务有日期、责任、依赖并可执行

**K39**

TARGET

**L39**

TBD

**M39**

TBD

**N39**

TBD

**O39**

进行中

**P39**

已定义

### Row 40

**A40**

Phase 1

**B40**

M2

**C40**

项目执行与问题闭环

**D40**

M2.2

**E40**

计划与任务建立

**F40**

M2.2-A06

**G40**

确认计划并记录变更

**H40**

完成“确认计划并记录变更”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**I40**

项目基线计划及任务责任清单

**J40**

关键里程碑和任务有日期、责任、依赖并可执行

**K40**

TARGET

**L40**

TBD

**M40**

TBD

**N40**

TBD

**O40**

未开始

**P40**

已定义

### Row 41

**A41**

Phase 1

**B41**

M2

**C41**

项目执行与问题闭环

**D41**

M2.3

**E41**

日常执行与更新

**F41**

M2.3-A01

**G41**

查看待办

**H41**

完成“查看待办”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**I41**

持续更新的执行状态及承诺结果记录

**J41**

状态真实，计划预测实际可比较，长期未更新可识别

**K41**

TARGET

**L41**

TBD

**M41**

TBD

**N41**

TBD

**O41**

进行中

**P41**

已定义

### Row 42

**A42**

Phase 1

**B42**

M2

**C42**

项目执行与问题闭环

**D42**

M2.3

**E42**

日常执行与更新

**F42**

M2.3-A02

**G42**

更新Task和Forecast

**H42**

完成“更新Task和Forecast”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**I42**

持续更新的执行状态及承诺结果记录

**J42**

状态真实，计划预测实际可比较，长期未更新可识别

**K42**

TARGET

**L42**

TBD

**M42**

TBD

**N42**

TBD

**O42**

未开始

**P42**

已定义

### Row 43

**A43**

Phase 1

**B43**

M2

**C43**

项目执行与问题闭环

**D43**

M2.3

**E43**

日常执行与更新

**F43**

M2.3-A03

**G43**

提交交付物或证据

**H43**

完成“提交交付物或证据”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**I43**

持续更新的执行状态及承诺结果记录

**J43**

状态真实，计划预测实际可比较，长期未更新可识别

**K43**

TARGET

**L43**

TBD

**M43**

TBD

**N43**

TBD

**O43**

未开始

**P43**

已定义

### Row 44

**A44**

Phase 1

**B44**

M2

**C44**

项目执行与问题闭环

**D44**

M2.3

**E44**

日常执行与更新

**F44**

M2.3-A04

**G44**

记录下一步、等待、阻塞、变化、更新时间和更新人

**H44**

完成“记录下一步、等待、阻塞、变化、更新时间和更新人”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**I44**

持续更新的执行状态及承诺结果记录

**J44**

状态真实，计划预测实际可比较，长期未更新可识别

**K44**

TARGET

**L44**

TBD

**M44**

TBD

**N44**

TBD

**O44**

未开始

**P44**

已定义

### Row 45

**A45**

Phase 1

**B45**

M2

**C45**

项目执行与问题闭环

**D45**

M2.4

**E45**

异常识别与记录

**F45**

M2.4-A01

**G45**

识别并分类Issue、Risk、Delay和Blocker

**H45**

完成“识别并分类Issue、Risk、Delay和Blocker”，使“异常识别与记录”能够按统一规则执行、检查并留下可验证结果。

**I45**

结构化异常记录及影响责任

**J45**

分类一致，影响对象、Owner、状态和下一步明确

**K45**

TARGET

**L45**

TBD

**M45**

TBD

**N45**

TBD

**O45**

未开始

**P45**

已定义

### Row 46

**A46**

Phase 1

**B46**

M2

**C46**

项目执行与问题闭环

**D46**

M2.4

**E46**

异常识别与记录

**F46**

M2.4-A02

**G46**

关联影响对象

**H46**

完成“关联影响对象”，使“异常识别与记录”能够按统一规则执行、检查并留下可验证结果。

**I46**

结构化异常记录及影响责任

**J46**

分类一致，影响对象、Owner、状态和下一步明确

**K46**

TARGET

**L46**

TBD

**M46**

TBD

**N46**

TBD

**O46**

未开始

**P46**

已定义

### Row 47

**A47**

Phase 1

**B47**

M2

**C47**

项目执行与问题闭环

**D47**

M2.4

**E47**

异常识别与记录

**F47**

M2.4-A03

**G47**

记录影响、严重度、原因、Owner、升级需求和重复异常

**H47**

完成“记录影响、严重度、原因、Owner、升级需求和重复异常”，使“异常识别与记录”能够按统一规则执行、检查并留下可验证结果。

**I47**

结构化异常记录及影响责任

**J47**

分类一致，影响对象、Owner、状态和下一步明确

**K47**

TARGET

**L47**

TBD

**M47**

TBD

**N47**

TBD

**O47**

未开始

**P47**

已定义

### Row 48

**A48**

Phase 1

**B48**

M2

**C48**

项目执行与问题闭环

**D48**

M2.5

**E48**

恢复行动与升级

**F48**

M2.5-A01

**G48**

创建Recovery Action

**H48**

完成“创建Recovery Action”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**I48**

恢复行动计划及责任日期结果

**J48**

关键异常有行动或处置结论，逾期无效行动可升级

**K48**

TARGET

**L48**

TBD

**M48**

TBD

**N48**

TBD

**O48**

未开始

**P48**

已定义

### Row 49

**A49**

Phase 1

**B49**

M2

**C49**

项目执行与问题闭环

**D49**

M2.5

**E49**

恢复行动与升级

**F49**

M2.5-A02

**G49**

指定Owner

**H49**

完成“指定Owner”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**I49**

恢复行动计划及责任日期结果

**J49**

关键异常有行动或处置结论，逾期无效行动可升级

**K49**

TARGET

**L49**

TBD

**M49**

TBD

**N49**

TBD

**O49**

未开始

**P49**

已定义

### Row 50

**A50**

Phase 1

**B50**

M2

**C50**

项目执行与问题闭环

**D50**

M2.5

**E50**

恢复行动与升级

**F50**

M2.5-A03

**G50**

设置Due和恢复目标

**H50**

完成“设置Due和恢复目标”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**I50**

恢复行动计划及责任日期结果

**J50**

关键异常有行动或处置结论，逾期无效行动可升级

**K50**

TARGET

**L50**

TBD

**M50**

TBD

**N50**

TBD

**O50**

未开始

**P50**

已定义

### Row 51

**A51**

Phase 1

**B51**

M2

**C51**

项目执行与问题闭环

**D51**

M2.5

**E51**

恢复行动与升级

**F51**

M2.5-A04

**G51**

更新优先级、状态、进展和结果

**H51**

完成“更新优先级、状态、进展和结果”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**I51**

恢复行动计划及责任日期结果

**J51**

关键异常有行动或处置结论，逾期无效行动可升级

**K51**

TARGET

**L51**

TBD

**M51**

TBD

**N51**

TBD

**O51**

未开始

**P51**

已定义

### Row 52

**A52**

Phase 1

**B52**

M2

**C52**

项目执行与问题闭环

**D52**

M2.5

**E52**

恢复行动与升级

**F52**

M2.5-A05

**G52**

识别逾期无效行动并升级

**H52**

完成“识别逾期无效行动并升级”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**I52**

恢复行动计划及责任日期结果

**J52**

关键异常有行动或处置结论，逾期无效行动可升级

**K52**

TARGET

**L52**

TBD

**M52**

TBD

**N52**

TBD

**O52**

未开始

**P52**

已定义

### Row 53

**A53**

Phase 1

**B53**

M2

**C53**

项目执行与问题闭环

**D53**

M2.6

**E53**

管理决策

**F53**

M2.6-A01

**G53**

识别待决策事项

**H53**

完成“识别待决策事项”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**I53**

待决策清单、决策记录和后续行动

**J53**

决策事项、人员、期限、理由和结果可追踪

**K53**

TARGET

**L53**

TBD

**M53**

TBD

**N53**

TBD

**O53**

未开始

**P53**

已定义

### Row 54

**A54**

Phase 1

**B54**

M2

**C54**

项目执行与问题闭环

**D54**

M2.6

**E54**

管理决策

**F54**

M2.6-A02

**G54**

记录背景、影响、时限、方案和建议

**H54**

完成“记录背景、影响、时限、方案和建议”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**I54**

待决策清单、决策记录和后续行动

**J54**

决策事项、人员、期限、理由和结果可追踪

**K54**

TARGET

**L54**

TBD

**M54**

TBD

**N54**

TBD

**O54**

未开始

**P54**

已定义

### Row 55

**A55**

Phase 1

**B55**

M2

**C55**

项目执行与问题闭环

**D55**

M2.6

**E55**

管理决策

**F55**

M2.6-A03

**G55**

指定决策人

**H55**

完成“指定决策人”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**I55**

待决策清单、决策记录和后续行动

**J55**

决策事项、人员、期限、理由和结果可追踪

**K55**

TARGET

**L55**

TBD

**M55**

TBD

**N55**

TBD

**O55**

未开始

**P55**

已定义

### Row 56

**A56**

Phase 1

**B56**

M2

**C56**

项目执行与问题闭环

**D56**

M2.6

**E56**

管理决策

**F56**

M2.6-A04

**G56**

记录决定理由

**H56**

完成“记录决定理由”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**I56**

待决策清单、决策记录和后续行动

**J56**

决策事项、人员、期限、理由和结果可追踪

**K56**

TARGET

**L56**

TBD

**M56**

TBD

**N56**

TBD

**O56**

未开始

**P56**

已定义

### Row 57

**A57**

Phase 1

**B57**

M2

**C57**

项目执行与问题闭环

**D57**

M2.6

**E57**

管理决策

**F57**

M2.6-A05

**G57**

转化Action并跟踪结果

**H57**

完成“转化Action并跟踪结果”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**I57**

待决策清单、决策记录和后续行动

**J57**

决策事项、人员、期限、理由和结果可追踪

**K57**

TARGET

**L57**

TBD

**M57**

TBD

**N57**

TBD

**O57**

未开始

**P57**

已定义

### Row 58

**A58**

Phase 1

**B58**

M2

**C58**

项目执行与问题闭环

**D58**

M2.7

**E58**

结果确认与验证关闭

**F58**

M2.7-A01

**G58**

检查Action

**H58**

完成“检查Action”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**I58**

验证关闭记录及结果证据

**J58**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**K58**

TARGET

**L58**

TBD

**M58**

TBD

**N58**

TBD

**O58**

未开始

**P58**

已定义

### Row 59

**A59**

Phase 1

**B59**

M2

**C59**

项目执行与问题闭环

**D59**

M2.7

**E59**

结果确认与验证关闭

**F59**

M2.7-A02

**G59**

记录结果

**H59**

完成“记录结果”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**I59**

验证关闭记录及结果证据

**J59**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**K59**

TARGET

**L59**

TBD

**M59**

TBD

**N59**

TBD

**O59**

未开始

**P59**

已定义

### Row 60

**A60**

Phase 1

**B60**

M2

**C60**

项目执行与问题闭环

**D60**

M2.7

**E60**

结果确认与验证关闭

**F60**

M2.7-A03

**G60**

确认影响是否消除或接受

**H60**

完成“确认影响是否消除或接受”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**I60**

验证关闭记录及结果证据

**J60**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**K60**

TARGET

**L60**

TBD

**M60**

TBD

**N60**

TBD

**O60**

未开始

**P60**

已定义

### Row 61

**A61**

Phase 1

**B61**

M2

**C61**

项目执行与问题闭环

**D61**

M2.7

**E61**

结果确认与验证关闭

**F61**

M2.7-A04

**G61**

指定验证人

**H61**

完成“指定验证人”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**I61**

验证关闭记录及结果证据

**J61**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**K61**

TARGET

**L61**

TBD

**M61**

TBD

**N61**

TBD

**O61**

未开始

**P61**

已定义

### Row 62

**A62**

Phase 1

**B62**

M2

**C62**

项目执行与问题闭环

**D62**

M2.7

**E62**

结果确认与验证关闭

**F62**

M2.7-A05

**G62**

提交证据

**H62**

完成“提交证据”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**I62**

验证关闭记录及结果证据

**J62**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**K62**

TARGET

**L62**

TBD

**M62**

TBD

**N62**

TBD

**O62**

未开始

**P62**

已定义

### Row 63

**A63**

Phase 1

**B63**

M2

**C63**

项目执行与问题闭环

**D63**

M2.7

**E63**

结果确认与验证关闭

**F63**

M2.7-A06

**G63**

正式关闭或重开

**H63**

完成“正式关闭或重开”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**I63**

验证关闭记录及结果证据

**J63**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**K63**

TARGET

**L63**

TBD

**M63**

TBD

**N63**

TBD

**O63**

未开始

**P63**

已定义

### Row 64

**A64**

Phase 1

**B64**

M2

**C64**

项目执行与问题闭环

**D64**

M2.8

**E64**

历史与经验沉淀

**F64**

M2.8-A01

**G64**

保留计划和状态变化

**H64**

完成“保留计划和状态变化”，使“历史与经验沉淀”能够按统一规则执行、检查并留下可验证结果。

**I64**

结构化执行历史及问题处理案例

**J64**

原因、行动、决定和结果可关联，案例来自真实关闭记录

**K64**

TARGET

**L64**

TBD

**M64**

TBD

**N64**

TBD

**O64**

未开始

**P64**

已定义

### Row 65

**A65**

Phase 1

**B65**

M2

**C65**

项目执行与问题闭环

**D65**

M2.8

**E65**

历史与经验沉淀

**F65**

M2.8-A02

**G65**

记录Root Cause、有效无效Action、关键Decision、最终Result和可检索案例

**H65**

完成“记录Root Cause、有效无效Action、关键Decision、最终Result和可检索案例”，使“历史与经验沉淀”能够按统一规则执行、检查并留下可验证结果。

**I65**

结构化执行历史及问题处理案例

**J65**

原因、行动、决定和结果可关联，案例来自真实关闭记录

**K65**

TARGET

**L65**

TBD

**M65**

TBD

**N65**

TBD

**O65**

未开始

**P65**

已定义

### Row 66

**A66**

Phase 1

**B66**

M3

**C66**

工作与管理入口

**D66**

M3.1

**E66**

个人执行入口

**F66**

M3.1-A01

**G66**

展示今日、即将到期、逾期、待更新、待确认、本人异常和Action

**H66**

完成“展示今日、即将到期、逾期、待更新、待确认、本人异常和Action”，使“个人执行入口”能够按统一规则执行、检查并留下可验证结果。

**I66**

My Daily Work入口

**J66**

一个入口找到并完成核心工作，可返回项目背景，减少重复维护

**K66**

TARGET

**L66**

TBD

**M66**

TBD

**N66**

TBD

**O66**

进行中

**P66**

已定义

### Row 67

**A67**

Phase 1

**B67**

M3

**C67**

工作与管理入口

**D67**

M3.1

**E67**

个人执行入口

**F67**

M3.1-A02

**G67**

支持更新、提交结果并进入项目背景

**H67**

完成“支持更新、提交结果并进入项目背景”，使“个人执行入口”能够按统一规则执行、检查并留下可验证结果。

**I67**

My Daily Work入口

**J67**

一个入口找到并完成核心工作，可返回项目背景，减少重复维护

**K67**

TARGET

**L67**

TBD

**M67**

TBD

**N67**

TBD

**O67**

进行中

**P67**

已定义

### Row 68

**A68**

Phase 1

**B68**

M3

**C68**

工作与管理入口

**D68**

M3.2

**E68**

项目管理入口

**F68**

M3.2-A01

**G68**

展示项目、SKU、阶段、健康、Milestone、Task、异常、Action、待决策和缺失项

**H68**

完成“展示项目、SKU、阶段、健康、Milestone、Task、异常、Action、待决策和缺失项”，使“项目管理入口”能够按统一规则执行、检查并留下可验证结果。

**I68**

Project Workspace及可信项目视图

**J68**

偏差、影响、Owner和下一步清楚，无需另做解释报告

**K68**

TARGET

**L68**

TBD

**M68**

TBD

**N68**

TBD

**O68**

未开始

**P68**

已定义

### Row 69

**A69**

Phase 1

**B69**

M3

**C69**

工作与管理入口

**D69**

M3.2

**E69**

项目管理入口

**F69**

M3.2-A02

**G69**

支持更新、审查和下钻

**H69**

完成“支持更新、审查和下钻”，使“项目管理入口”能够按统一规则执行、检查并留下可验证结果。

**I69**

Project Workspace及可信项目视图

**J69**

偏差、影响、Owner和下一步清楚，无需另做解释报告

**K69**

TARGET

**L69**

TBD

**M69**

TBD

**N69**

TBD

**O69**

未开始

**P69**

已定义

### Row 70

**A70**

Phase 1

**B70**

M3

**C70**

工作与管理入口

**D70**

M3.3

**E70**

异常处理入口

**F70**

M3.3-A01

**G70**

展示开放、缺失Owner/Action/Due、逾期和待关闭异常

**H70**

完成“展示开放、缺失Owner/Action/Due、逾期和待关闭异常”，使“异常处理入口”能够按统一规则执行、检查并留下可验证结果。

**I70**

统一异常处理入口

**J70**

异常集中可见，可直接分配、行动、升级和关闭

**K70**

TARGET

**L70**

TBD

**M70**

TBD

**N70**

TBD

**O70**

未开始

**P70**

已定义

### Row 71

**A71**

Phase 1

**B71**

M3

**C71**

工作与管理入口

**D71**

M3.3

**E71**

异常处理入口

**F71**

M3.3-A02

**G71**

支持分配、行动、更新、升级、决策和关闭

**H71**

完成“支持分配、行动、更新、升级、决策和关闭”，使“异常处理入口”能够按统一规则执行、检查并留下可验证结果。

**I71**

统一异常处理入口

**J71**

异常集中可见，可直接分配、行动、升级和关闭

**K71**

TARGET

**L71**

TBD

**M71**

TBD

**N71**

TBD

**O71**

未开始

**P71**

已定义

### Row 72

**A72**

Phase 1

**B72**

M3

**C72**

工作与管理入口

**D72**

M3.4

**E72**

周度管理入口

**F72**

M3.4-A01

**G72**

展示健康、变化、偏差、Top Risk、逾期、缺失、待决策和上周结果

**H72**

完成“展示健康、变化、偏差、Top Risk、逾期、缺失、待决策和上周结果”，使“周度管理入口”能够按统一规则执行、检查并留下可验证结果。

**I72**

周度管理视图及决定行动记录

**J72**

周会直接使用AutoPM，决定回写，下周期验证结果

**K72**

TARGET

**L72**

TBD

**M72**

TBD

**N72**

TBD

**O72**

进行中

**P72**

已定义

### Row 73

**A73**

Phase 1

**B73**

M3

**C73**

工作与管理入口

**D73**

M3.4

**E73**

周度管理入口

**F73**

M3.4-A02

**G73**

支持确认、决定和行动回写

**H73**

完成“支持确认、决定和行动回写”，使“周度管理入口”能够按统一规则执行、检查并留下可验证结果。

**I73**

周度管理视图及决定行动记录

**J73**

周会直接使用AutoPM，决定回写，下周期验证结果

**K73**

TARGET

**L73**

TBD

**M73**

TBD

**N73**

TBD

**O73**

未开始

**P73**

已定义

### Row 74

**A74**

Phase 1

**B74**

M3

**C74**

工作与管理入口

**D74**

M3.5

**E74**

领导审查与下钻

**F74**

M3.5-A01

**G74**

展示组合健康、关键风险延误、受影响Milestone和待决策项

**H74**

完成“展示组合健康、关键风险延误、受影响Milestone和待决策项”，使“领导审查与下钻”能够按统一规则执行、检查并留下可验证结果。

**I74**

Leadership View及下钻路径

**J74**

汇总结论可下钻，管理决定和后续行动可追踪

**K74**

TARGET

**L74**

TBD

**M74**

TBD

**N74**

TBD

**O74**

未开始

**P74**

已定义

### Row 75

**A75**

Phase 1

**B75**

M3

**C75**

工作与管理入口

**D75**

M3.5

**E75**

领导审查与下钻

**F75**

M3.5-A02

**G75**

逐层下钻至Project、SKU、异常、Action、Owner和Result

**H75**

完成“逐层下钻至Project、SKU、异常、Action、Owner和Result”，使“领导审查与下钻”能够按统一规则执行、检查并留下可验证结果。

**I75**

Leadership View及下钻路径

**J75**

汇总结论可下钻，管理决定和后续行动可追踪

**K75**

TARGET

**L75**

TBD

**M75**

TBD

**N75**

TBD

**O75**

未开始

**P75**

已定义

### Row 76

**A76**

Phase 1

**B76**

M3

**C76**

工作与管理入口

**D76**

M3.6

**E76**

用户体验与动作效率

**F76**

M3.6-A01

**G76**

删除无用字段

**H76**

完成“删除无用字段”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**I76**

用户问题清单及界面修复任务

**J76**

核心动作易完成，信息一次维护，反馈转为可验收任务

**K76**

TARGET

**L76**

TBD

**M76**

TBD

**N76**

TBD

**O76**

未开始

**P76**

已定义

### Row 77

**A77**

Phase 1

**B77**

M3

**C77**

工作与管理入口

**D77**

M3.6

**E77**

用户体验与动作效率

**F77**

M3.6-A02

**G77**

减少重复录入和页面切换

**H77**

完成“减少重复录入和页面切换”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**I77**

用户问题清单及界面修复任务

**J77**

核心动作易完成，信息一次维护，反馈转为可验收任务

**K77**

TARGET

**L77**

TBD

**M77**

TBD

**N77**

TBD

**O77**

进行中

**P77**

已定义

### Row 78

**A78**

Phase 1

**B78**

M3

**C78**

工作与管理入口

**D78**

M3.6

**E78**

用户体验与动作效率

**F78**

M3.6-A03

**G78**

突出下一步

**H78**

完成“突出下一步”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**I78**

用户问题清单及界面修复任务

**J78**

核心动作易完成，信息一次维护，反馈转为可验收任务

**K78**

TARGET

**L78**

TBD

**M78**

TBD

**N78**

TBD

**O78**

未开始

**P78**

已定义

### Row 79

**A79**

Phase 1

**B79**

M3

**C79**

工作与管理入口

**D79**

M3.6

**E79**

用户体验与动作效率

**F79**

M3.6-A04

**G79**

简化更新

**H79**

完成“简化更新”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**I79**

用户问题清单及界面修复任务

**J79**

核心动作易完成，信息一次维护，反馈转为可验收任务

**K79**

TARGET

**L79**

TBD

**M79**

TBD

**N79**

TBD

**O79**

未开始

**P79**

已定义

### Row 80

**A80**

Phase 1

**B80**

M3

**C80**

工作与管理入口

**D80**

M3.6

**E80**

用户体验与动作效率

**F80**

M3.6-A05

**G80**

提供说明

**H80**

完成“提供说明”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**I80**

用户问题清单及界面修复任务

**J80**

核心动作易完成，信息一次维护，反馈转为可验收任务

**K80**

TARGET

**L80**

TBD

**M80**

TBD

**N80**

TBD

**O80**

未开始

**P80**

已定义

### Row 81

**A81**

Phase 1

**B81**

M3

**C81**

工作与管理入口

**D81**

M3.6

**E81**

用户体验与动作效率

**F81**

M3.6-A06

**G81**

收集并排序用户问题

**H81**

完成“收集并排序用户问题”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**I81**

用户问题清单及界面修复任务

**J81**

核心动作易完成，信息一次维护，反馈转为可验收任务

**K81**

TARGET

**L81**

TBD

**M81**

TBD

**N81**

TBD

**O81**

未开始

**P81**

已定义

### Row 82

**A82**

Phase 1

**B82**

M4

**C82**

自动化、集成与运行保障

**D82**

M4.1

**E82**

数据导入与初始化自动化

**F82**

M4.1-A01

**G82**

建立导入模板

**H82**

完成“建立导入模板”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**I82**

稳定导入流程及错误报告

**J82**

不重复，错误可定位，不静默覆盖真实数据

**K82**

TARGET

**L82**

TBD

**M82**

TBD

**N82**

TBD

**O82**

进行中

**P82**

已定义

### Row 83

**A83**

Phase 1

**B83**

M4

**C83**

自动化、集成与运行保障

**D83**

M4.1

**E83**

数据导入与初始化自动化

**F83**

M4.1-A02

**G83**

校验格式

**H83**

完成“校验格式”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**I83**

稳定导入流程及错误报告

**J83**

不重复，错误可定位，不静默覆盖真实数据

**K83**

TARGET

**L83**

TBD

**M83**

TBD

**N83**

TBD

**O83**

进行中

**P83**

已定义

### Row 84

**A84**

Phase 1

**B84**

M4

**C84**

自动化、集成与运行保障

**D84**

M4.1

**E84**

数据导入与初始化自动化

**F84**

M4.1-A03

**G84**

匹配ID和Owner

**H84**

完成“匹配ID和Owner”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**I84**

稳定导入流程及错误报告

**J84**

不重复，错误可定位，不静默覆盖真实数据

**K84**

TARGET

**L84**

TBD

**M84**

TBD

**N84**

TBD

**O84**

进行中

**P84**

已定义

### Row 85

**A85**

Phase 1

**B85**

M4

**C85**

自动化、集成与运行保障

**D85**

M4.1

**E85**

数据导入与初始化自动化

**F85**

M4.1-A04

**G85**

防重复和静默覆盖

**H85**

完成“防重复和静默覆盖”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**I85**

稳定导入流程及错误报告

**J85**

不重复，错误可定位，不静默覆盖真实数据

**K85**

TARGET

**L85**

TBD

**M85**

TBD

**N85**

TBD

**O85**

进行中

**P85**

已定义

### Row 86

**A86**

Phase 1

**B86**

M4

**C86**

自动化、集成与运行保障

**D86**

M4.1

**E86**

数据导入与初始化自动化

**F86**

M4.1-A05

**G86**

显示错误

**H86**

完成“显示错误”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**I86**

稳定导入流程及错误报告

**J86**

不重复，错误可定位，不静默覆盖真实数据

**K86**

TARGET

**L86**

TBD

**M86**

TBD

**N86**

TBD

**O86**

进行中

**P86**

已定义

### Row 87

**A87**

Phase 1

**B87**

M4

**C87**

自动化、集成与运行保障

**D87**

M4.1

**E87**

数据导入与初始化自动化

**F87**

M4.1-A06

**G87**

支持修正和回退

**H87**

完成“支持修正和回退”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**I87**

稳定导入流程及错误报告

**J87**

不重复，错误可定位，不静默覆盖真实数据

**K87**

TARGET

**L87**

TBD

**M87**

TBD

**N87**

TBD

**O87**

未开始

**P87**

已定义

### Row 88

**A88**

Phase 1

**B88**

M4

**C88**

自动化、集成与运行保障

**D88**

M4.2

**E88**

状态与异常计算

**F88**

M4.2-A01

**G88**

计算到期、逾期、Next Milestone和偏差

**H88**

完成“计算到期、逾期、Next Milestone和偏差”，使“状态与异常计算”能够按统一规则执行、检查并留下可验证结果。

**I88**

计算规则及可解释结果

**J88**

规则与业务定义一致，异常边界通过测试，不无依据覆盖

**K88**

TARGET

**L88**

TBD

**M88**

TBD

**N88**

TBD

**O88**

进行中

**P88**

已定义

### Row 89

**A89**

Phase 1

**B89**

M4

**C89**

自动化、集成与运行保障

**D89**

M4.2

**E89**

状态与异常计算

**F89**

M4.2-A02

**G89**

识别缺失与冲突

**H89**

完成“识别缺失与冲突”，使“状态与异常计算”能够按统一规则执行、检查并留下可验证结果。

**I89**

计算规则及可解释结果

**J89**

规则与业务定义一致，异常边界通过测试，不无依据覆盖

**K89**

TARGET

**L89**

TBD

**M89**

TBD

**N89**

TBD

**O89**

未开始

**P89**

已定义

### Row 90

**A90**

Phase 1

**B90**

M4

**C90**

自动化、集成与运行保障

**D90**

M4.2

**E90**

状态与异常计算

**F90**

M4.2-A03

**G90**

展示依据并支持授权确认

**H90**

完成“展示依据并支持授权确认”，使“状态与异常计算”能够按统一规则执行、检查并留下可验证结果。

**I90**

计算规则及可解释结果

**J90**

规则与业务定义一致，异常边界通过测试，不无依据覆盖

**K90**

TARGET

**L90**

TBD

**M90**

TBD

**N90**

TBD

**O90**

未开始

**P90**

已定义

### Row 91

**A91**

Phase 1

**B91**

M4

**C91**

自动化、集成与运行保障

**D91**

M4.3

**E91**

提醒与升级

**F91**

M4.3-A01

**G91**

建立到期、逾期、缺失和关键Delay提醒

**H91**

完成“建立到期、逾期、缺失和关键Delay提醒”，使“提醒与升级”能够按统一规则执行、检查并留下可验证结果。

**I91**

分级提醒和升级机制

**J91**

对象正确，已完成停止，重复受控，关键事项升级

**K91**

TARGET

**L91**

TBD

**M91**

TBD

**N91**

TBD

**O91**

进行中

**P91**

已定义

### Row 92

**A92**

Phase 1

**B92**

M4

**C92**

自动化、集成与运行保障

**D92**

M4.3

**E92**

提醒与升级

**F92**

M4.3-A02

**G92**

建立去重、停止、升级及响应记录

**H92**

完成“建立去重、停止、升级及响应记录”，使“提醒与升级”能够按统一规则执行、检查并留下可验证结果。

**I92**

分级提醒和升级机制

**J92**

对象正确，已完成停止，重复受控，关键事项升级

**K92**

TARGET

**L92**

TBD

**M92**

TBD

**N92**

TBD

**O92**

未开始

**P92**

已定义

### Row 93

**A93**

Phase 1

**B93**

M4

**C93**

自动化、集成与运行保障

**D93**

M4.4

**E93**

报告生成

**F93**

M4.4-A01

**G93**

汇总状态、变化、风险、延误、行动和决定

**H93**

完成“汇总状态、变化、风险、延误、行动和决定”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**I93**

可确认、可追溯的周报草稿

**J93**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**K93**

TARGET

**L93**

TBD

**M93**

TBD

**N93**

TBD

**O93**

进行中

**P93**

已定义

### Row 94

**A94**

Phase 1

**B94**

M4

**C94**

自动化、集成与运行保障

**D94**

M4.4

**E94**

报告生成

**F94**

M4.4-A02

**G94**

生成周报

**H94**

完成“生成周报”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**I94**

可确认、可追溯的周报草稿

**J94**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**K94**

TARGET

**L94**

TBD

**M94**

TBD

**N94**

TBD

**O94**

已完成

**P94**

已定义

### Row 95

**A95**

Phase 1

**B95**

M4

**C95**

自动化、集成与运行保障

**D95**

M4.4

**E95**

报告生成

**F95**

M4.4-A03

**G95**

标记缺失待确认

**H95**

完成“标记缺失待确认”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**I95**

可确认、可追溯的周报草稿

**J95**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**K95**

TARGET

**L95**

TBD

**M95**

TBD

**N95**

TBD

**O95**

未开始

**P95**

已定义

### Row 96

**A96**

Phase 1

**B96**

M4

**C96**

自动化、集成与运行保障

**D96**

M4.4

**E96**

报告生成

**F96**

M4.4-A04

**G96**

保留来源、下钻、确认和导出

**H96**

完成“保留来源、下钻、确认和导出”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**I96**

可确认、可追溯的周报草稿

**J96**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**K96**

TARGET

**L96**

TBD

**M96**

TBD

**N96**

TBD

**O96**

未开始

**P96**

已定义

### Row 97

**A97**

Phase 1

**B97**

M4

**C97**

自动化、集成与运行保障

**D97**

M4.5

**E97**

PMO主数据连接

**F97**

M4.5-A01

**G97**

确认必要数据范围

**H97**

完成“确认必要数据范围”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**I97**

PMO读取验证及映射对账结果

**J97**

必要主数据稳定匹配，冲突和失败不静默处理

**K97**

TARGET

**L97**

TBD

**M97**

TBD

**N97**

TBD

**O97**

进行中

**P97**

已定义

### Row 98

**A98**

Phase 1

**B98**

M4

**C98**

自动化、集成与运行保障

**D98**

M4.5

**E98**

PMO主数据连接

**F98**

M4.5-A02

**G98**

建立Programme、Project、SKU和目标日期映射

**H98**

完成“建立Programme、Project、SKU和目标日期映射”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**I98**

PMO读取验证及映射对账结果

**J98**

必要主数据稳定匹配，冲突和失败不静默处理

**K98**

TARGET

**L98**

TBD

**M98**

TBD

**N98**

TBD

**O98**

未开始

**P98**

已定义

### Row 99

**A99**

Phase 1

**B99**

M4

**C99**

自动化、集成与运行保障

**D99**

M4.5

**E99**

PMO主数据连接

**F99**

M4.5-A03

**G99**

验证读取

**H99**

完成“验证读取”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**I99**

PMO读取验证及映射对账结果

**J99**

必要主数据稳定匹配，冲突和失败不静默处理

**K99**

TARGET

**L99**

TBD

**M99**

TBD

**N99**

TBD

**O99**

未开始

**P99**

已定义

### Row 100

**A100**

Phase 1

**B100**

M4

**C100**

自动化、集成与运行保障

**D100**

M4.5

**E100**

PMO主数据连接

**F100**

M4.5-A04

**G100**

识别变化冲突

**H100**

完成“识别变化冲突”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**I100**

PMO读取验证及映射对账结果

**J100**

必要主数据稳定匹配，冲突和失败不静默处理

**K100**

TARGET

**L100**

TBD

**M100**

TBD

**N100**

TBD

**O100**

未开始

**P100**

已定义

### Row 101

**A101**

Phase 1

**B101**

M4

**C101**

自动化、集成与运行保障

**D101**

M4.5

**E101**

PMO主数据连接

**F101**

M4.5-A05

**G101**

记录同步并对账

**H101**

完成“记录同步并对账”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**I101**

PMO读取验证及映射对账结果

**J101**

必要主数据稳定匹配，冲突和失败不静默处理

**K101**

TARGET

**L101**

TBD

**M101**

TBD

**N101**

TBD

**O101**

未开始

**P101**

已定义

### Row 102

**A102**

Phase 1

**B102**

M4

**C102**

自动化、集成与运行保障

**D102**

M4.6

**E102**

权限与审计

**F102**

M4.6-A01

**G102**

定义角色、项目、查看、编辑、确认、审批、导出和敏感字段权限

**H102**

完成“定义角色、项目、查看、编辑、确认、审批、导出和敏感字段权限”，使“权限与审计”能够按统一规则执行、检查并留下可验证结果。

**I102**

Phase 1权限模型及审计记录

**J102**

访问和关键操作受控，越权经过测试，操作可追溯

**K102**

TARGET

**L102**

TBD

**M102**

TBD

**N102**

TBD

**O102**

未开始

**P102**

已定义

### Row 103

**A103**

Phase 1

**B103**

M4

**C103**

自动化、集成与运行保障

**D103**

M4.6

**E103**

权限与审计

**F103**

M4.6-A02

**G103**

记录变更

**H103**

完成“记录变更”，使“权限与审计”能够按统一规则执行、检查并留下可验证结果。

**I103**

Phase 1权限模型及审计记录

**J103**

访问和关键操作受控，越权经过测试，操作可追溯

**K103**

TARGET

**L103**

TBD

**M103**

TBD

**N103**

TBD

**O103**

未开始

**P103**

已定义

### Row 104

**A104**

Phase 1

**B104**

M4

**C104**

自动化、集成与运行保障

**D104**

M4.6

**E104**

权限与审计

**F104**

M4.6-A03

**G104**

测试越权

**H104**

完成“测试越权”，使“权限与审计”能够按统一规则执行、检查并留下可验证结果。

**I104**

Phase 1权限模型及审计记录

**J104**

访问和关键操作受控，越权经过测试，操作可追溯

**K104**

TARGET

**L104**

TBD

**M104**

TBD

**N104**

TBD

**O104**

未开始

**P104**

已定义

### Row 105

**A105**

Phase 1

**B105**

M4

**C105**

自动化、集成与运行保障

**D105**

M4.7

**E105**

运行监控与失败恢复

**F105**

M4.7-A01

**G105**

记录自动化和同步结果

**H105**

完成“记录自动化和同步结果”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**I105**

运行监控及失败处理机制

**J105**

失败及时发现，重试安全，故障有责任和回退

**K105**

TARGET

**L105**

TBD

**M105**

TBD

**N105**

TBD

**O105**

未开始

**P105**

已定义

### Row 106

**A106**

Phase 1

**B106**

M4

**C106**

自动化、集成与运行保障

**D106**

M4.7

**E106**

运行监控与失败恢复

**F106**

M4.7-A02

**G106**

监控异常

**H106**

完成“监控异常”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**I106**

运行监控及失败处理机制

**J106**

失败及时发现，重试安全，故障有责任和回退

**K106**

TARGET

**L106**

TBD

**M106**

TBD

**N106**

TBD

**O106**

未开始

**P106**

已定义

### Row 107

**A107**

Phase 1

**B107**

M4

**C107**

自动化、集成与运行保障

**D107**

M4.7

**E107**

运行监控与失败恢复

**F107**

M4.7-A03

**G107**

告警并分配Owner

**H107**

完成“告警并分配Owner”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**I107**

运行监控及失败处理机制

**J107**

失败及时发现，重试安全，故障有责任和回退

**K107**

TARGET

**L107**

TBD

**M107**

TBD

**N107**

TBD

**O107**

未开始

**P107**

已定义

### Row 108

**A108**

Phase 1

**B108**

M4

**C108**

自动化、集成与运行保障

**D108**

M4.7

**E108**

运行监控与失败恢复

**F108**

M4.7-A04

**G108**

支持幂等重试

**H108**

完成“支持幂等重试”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**I108**

运行监控及失败处理机制

**J108**

失败及时发现，重试安全，故障有责任和回退

**K108**

TARGET

**L108**

TBD

**M108**

TBD

**N108**

TBD

**O108**

进行中

**P108**

已定义

### Row 109

**A109**

Phase 1

**B109**

M4

**C109**

自动化、集成与运行保障

**D109**

M4.7

**E109**

运行监控与失败恢复

**F109**

M4.7-A05

**G109**

防数据污染

**H109**

完成“防数据污染”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**I109**

运行监控及失败处理机制

**J109**

失败及时发现，重试安全，故障有责任和回退

**K109**

TARGET

**L109**

TBD

**M109**

TBD

**N109**

TBD

**O109**

未开始

**P109**

已定义

### Row 110

**A110**

Phase 1

**B110**

M4

**C110**

自动化、集成与运行保障

**D110**

M4.7

**E110**

运行监控与失败恢复

**F110**

M4.7-A06

**G110**

建立回退

**H110**

完成“建立回退”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**I110**

运行监控及失败处理机制

**J110**

失败及时发现，重试安全，故障有责任和回退

**K110**

TARGET

**L110**

TBD

**M110**

TBD

**N110**

TBD

**O110**

未开始

**P110**

已定义

### Row 111

**A111**

Phase 1

**B111**

M5

**C111**

Pilot运行与采用

**D111**

M5.1

**E111**

Pilot范围确认

**F111**

M5.1-A01

**G111**

确认试点目标、团队、负责人、项目清单、选择标准、参与角色、使用承诺及启动暂停退出条件

**H111**

完成“确认试点目标、团队、负责人、项目清单、选择标准、参与角色、使用承诺及启动暂停退出条件”，使“Pilot范围确认”能够按统一规则执行、检查并留下可验证结果。

**I111**

Pilot范围说明及团队项目清单

**J111**

团队、项目、角色和目标确认，未确认数量周期保持TBD

**K111**

TARGET

**L111**

TBD

**M111**

TBD

**N111**

TBD

**O111**

未开始

**P111**

已定义

### Row 112

**A112**

Phase 1

**B112**

M5

**C112**

Pilot运行与采用

**D112**

M5.2

**E112**

角色与责任

**F112**

M5.2-A01

**G112**

定义执行、项目、职能、管理、Data Owner和平台支持责任

**H112**

完成“定义执行、项目、职能、管理、Data Owner和平台支持责任”，使“角色与责任”能够按统一规则执行、检查并留下可验证结果。

**I112**

Pilot角色责任矩阵

**J112**

每类数据和行动有责任，PM不代替所有人维护

**K112**

TARGET

**L112**

TBD

**M112**

TBD

**N112**

TBD

**O112**

未开始

**P112**

已定义

### Row 113

**A113**

Phase 1

**B113**

M5

**C113**

Pilot运行与采用

**D113**

M5.3

**E113**

使用规则

**F113**

M5.3-A01

**G113**

定义必须维护的信息、更新频率、异常Action升级关闭规则、人工确认和最低证据

**H113**

完成“定义必须维护的信息、更新频率、异常Action升级关闭规则、人工确认和最低证据”，使“使用规则”能够按统一规则执行、检查并留下可验证结果。

**I113**

Pilot使用规则

**J113**

何时在哪里更新什么清楚，关键事实保留人工责任

**K113**

TARGET

**L113**

TBD

**M113**

TBD

**N113**

TBD

**O113**

未开始

**P113**

已定义

### Row 114

**A114**

Phase 1

**B114**

M5

**C114**

Pilot运行与采用

**D114**

M5.4

**E114**

双系统过渡

**F114**

M5.4-A01

**G114**

明确唯一维护位置、旧工具范围、读取写入链接同步方向、冲突失败、停止条件和回退方案

**H114**

完成“明确唯一维护位置、旧工具范围、读取写入链接同步方向、冲突失败、停止条件和回退方案”，使“双系统过渡”能够按统一规则执行、检查并留下可验证结果。

**I114**

双系统过渡方案

**J114**

无规则重复维护被消除，切换和回退不丢数据

**K114**

TARGET

**L114**

TBD

**M114**

TBD

**N114**

TBD

**O114**

进行中

**P114**

已定义

### Row 115

**A115**

Phase 1

**B115**

M5

**C115**

Pilot运行与采用

**D115**

M5.5

**E115**

角色上手

**F115**

M5.5-A01

**G115**

使用真实项目完成任务更新、状态异常维护、Action确认、管理审查和Decision

**H115**

完成“使用真实项目完成任务更新、状态异常维护、Action确认、管理审查和Decision”，使“角色上手”能够按统一规则执行、检查并留下可验证结果。

**I115**

角色上手记录及首轮问题清单

**J115**

关键角色在真实项目完成核心动作，不以登录培训作为完成

**K115**

TARGET

**L115**

TBD

**M115**

TBD

**N115**

TBD

**O115**

未开始

**P115**

已定义

### Row 116

**A116**

Phase 1

**B116**

M5

**C116**

Pilot运行与采用

**D116**

M5.5

**E116**

角色上手

**F116**

M5.5-A02

**G116**

记录问题和理解偏差

**H116**

完成“记录问题和理解偏差”，使“角色上手”能够按统一规则执行、检查并留下可验证结果。

**I116**

角色上手记录及首轮问题清单

**J116**

关键角色在真实项目完成核心动作，不以登录培训作为完成

**K116**

TARGET

**L116**

TBD

**M116**

TBD

**N116**

TBD

**O116**

未开始

**P116**

已定义

### Row 117

**A117**

Phase 1

**B117**

M5

**C117**

Pilot运行与采用

**D117**

M5.6

**E117**

周度运行节奏

**F117**

M5.6-A01

**G117**

按规则更新

**H117**

完成“按规则更新”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**I117**

可重复周度运行机制

**J117**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**K117**

TARGET

**L117**

TBD

**M117**

TBD

**N117**

TBD

**O117**

已完成

**P117**

已定义

### Row 118

**A118**

Phase 1

**B118**

M5

**C118**

Pilot运行与采用

**D118**

M5.6

**E118**

周度运行节奏

**F118**

M5.6-A02

**G118**

检查数据

**H118**

完成“检查数据”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**I118**

可重复周度运行机制

**J118**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**K118**

TARGET

**L118**

TBD

**M118**

TBD

**N118**

TBD

**O118**

未开始

**P118**

已定义

### Row 119

**A119**

Phase 1

**B119**

M5

**C119**

Pilot运行与采用

**D119**

M5.6

**E119**

周度运行节奏

**F119**

M5.6-A03

**G119**

生成异常和周报

**H119**

完成“生成异常和周报”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**I119**

可重复周度运行机制

**J119**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**K119**

TARGET

**L119**

TBD

**M119**

TBD

**N119**

TBD

**O119**

进行中

**P119**

已定义

### Row 120

**A120**

Phase 1

**B120**

M5

**C120**

Pilot运行与采用

**D120**

M5.6

**E120**

周度运行节奏

**F120**

M5.6-A04

**G120**

开展周度审查

**H120**

完成“开展周度审查”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**I120**

可重复周度运行机制

**J120**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**K120**

TARGET

**L120**

TBD

**M120**

TBD

**N120**

TBD

**O120**

未开始

**P120**

已定义

### Row 121

**A121**

Phase 1

**B121**

M5

**C121**

Pilot运行与采用

**D121**

M5.6

**E121**

周度运行节奏

**F121**

M5.6-A05

**G121**

回写决定和Action

**H121**

完成“回写决定和Action”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**I121**

可重复周度运行机制

**J121**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**K121**

TARGET

**L121**

TBD

**M121**

TBD

**N121**

TBD

**O121**

未开始

**P121**

已定义

### Row 122

**A122**

Phase 1

**B122**

M5

**C122**

Pilot运行与采用

**D122**

M5.6

**E122**

周度运行节奏

**F122**

M5.6-A06

**G122**

下周期验证结果

**H122**

完成“下周期验证结果”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**I122**

可重复周度运行机制

**J122**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**K122**

TARGET

**L122**

TBD

**M122**

TBD

**N122**

TBD

**O122**

未开始

**P122**

已定义

### Row 123

**A123**

Phase 1

**B123**

M5

**C123**

Pilot运行与采用

**D123**

M5.7

**E123**

用户支持与问题处理

**F123**

M5.7-A01

**G123**

建立反馈入口

**H123**

完成“建立反馈入口”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**I123**

问题改进清单及支持修复节奏

**J123**

关键问题有分类、影响、责任和状态，修复经用户验证

**K123**

TARGET

**L123**

TBD

**M123**

TBD

**N123**

TBD

**O123**

未开始

**P123**

已定义

### Row 124

**A124**

Phase 1

**B124**

M5

**C124**

Pilot运行与采用

**D124**

M5.7

**E124**

用户支持与问题处理

**F124**

M5.7-A02

**G124**

分类问题

**H124**

完成“分类问题”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**I124**

问题改进清单及支持修复节奏

**J124**

关键问题有分类、影响、责任和状态，修复经用户验证

**K124**

TARGET

**L124**

TBD

**M124**

TBD

**N124**

TBD

**O124**

未开始

**P124**

已定义

### Row 125

**A125**

Phase 1

**B125**

M5

**C125**

Pilot运行与采用

**D125**

M5.7

**E125**

用户支持与问题处理

**F125**

M5.7-A03

**G125**

评估影响优先级

**H125**

完成“评估影响优先级”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**I125**

问题改进清单及支持修复节奏

**J125**

关键问题有分类、影响、责任和状态，修复经用户验证

**K125**

TARGET

**L125**

TBD

**M125**

TBD

**N125**

TBD

**O125**

未开始

**P125**

已定义

### Row 126

**A126**

Phase 1

**B126**

M5

**C126**

Pilot运行与采用

**D126**

M5.7

**E126**

用户支持与问题处理

**F126**

M5.7-A04

**G126**

分配Owner

**H126**

完成“分配Owner”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**I126**

问题改进清单及支持修复节奏

**J126**

关键问题有分类、影响、责任和状态，修复经用户验证

**K126**

TARGET

**L126**

TBD

**M126**

TBD

**N126**

TBD

**O126**

未开始

**P126**

已定义

### Row 127

**A127**

Phase 1

**B127**

M5

**C127**

Pilot运行与采用

**D127**

M5.7

**E127**

用户支持与问题处理

**F127**

M5.7-A05

**G127**

验证修复

**H127**

完成“验证修复”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**I127**

问题改进清单及支持修复节奏

**J127**

关键问题有分类、影响、责任和状态，修复经用户验证

**K127**

TARGET

**L127**

TBD

**M127**

TBD

**N127**

TBD

**O127**

未开始

**P127**

已定义

### Row 128

**A128**

Phase 1

**B128**

M5

**C128**

Pilot运行与采用

**D128**

M5.7

**E128**

用户支持与问题处理

**F128**

M5.7-A06

**G128**

转化重复反馈

**H128**

完成“转化重复反馈”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**I128**

问题改进清单及支持修复节奏

**J128**

关键问题有分类、影响、责任和状态，修复经用户验证

**K128**

TARGET

**L128**

TBD

**M128**

TBD

**N128**

TBD

**O128**

未开始

**P128**

已定义

### Row 129

**A129**

Phase 1

**B129**

M6

**C129**

价值证据与Gate决策

**D129**

M6.1

**E129**

基线定义

**F129**

M6.1-A01

**G129**

定义人工追踪、周报汇总、数据质量、Task/Issue/Action/Delay基线

**H129**

完成“定义人工追踪、周报汇总、数据质量、Task/Issue/Action/Delay基线”，使“基线定义”能够按统一规则执行、检查并留下可验证结果。

**I129**

指标定义及Pilot前基线

**J129**

定义和证据清楚，无基线不宣称改善

**K129**

TARGET

**L129**

TBD

**M129**

TBD

**N129**

TBD

**O129**

未开始

**P129**

已定义

### Row 130

**A130**

Phase 1

**B130**

M6

**C130**

价值证据与Gate决策

**D130**

M6.1

**E130**

基线定义

**F130**

M6.1-A02

**G130**

定义算法来源Owner周期并在Pilot前记录

**H130**

完成“定义算法来源Owner周期并在Pilot前记录”，使“基线定义”能够按统一规则执行、检查并留下可验证结果。

**I130**

指标定义及Pilot前基线

**J130**

定义和证据清楚，无基线不宣称改善

**K130**

TARGET

**L130**

TBD

**M130**

TBD

**N130**

TBD

**O130**

未开始

**P130**

已定义

### Row 131

**A131**

Phase 1

**B131**

M6

**C131**

价值证据与Gate决策

**D131**

M6.2

**E131**

使用与采用证据

**F131**

M6.2-A01

**G131**

记录活跃项目用户、频率及时性、周度审查、关键动作、中断退出和双系统维护

**H131**

完成“记录活跃项目用户、频率及时性、周度审查、关键动作、中断退出和双系统维护”，使“使用与采用证据”能够按统一规则执行、检查并留下可验证结果。

**I131**

Pilot使用证据包

**J131**

区分登录、一次录入和持续使用，负担和中断如实记录

**K131**

TARGET

**L131**

TBD

**M131**

TBD

**N131**

TBD

**O131**

未开始

**P131**

已定义

### Row 132

**A132**

Phase 1

**B132**

M6

**C132**

价值证据与Gate决策

**D132**

M6.3

**E132**

数据质量证据

**F132**

M6.3-A01

**G132**

记录字段、关系、Owner、Due、状态完整性，以及重复、冲突、同步失败、修正和关闭

**H132**

完成“记录字段、关系、Owner、Due、状态完整性，以及重复、冲突、同步失败、修正和关闭”，使“数据质量证据”能够按统一规则执行、检查并留下可验证结果。

**I132**

数据质量证据包

**J132**

指标可重复计算，问题可追溯，管理可用性有结论

**K132**

TARGET

**L132**

TBD

**M132**

TBD

**N132**

TBD

**O132**

进行中

**P132**

已定义

### Row 133

**A133**

Phase 1

**B133**

M6

**C133**

价值证据与Gate决策

**D133**

M6.4

**E133**

执行闭环证据

**F133**

M6.4-A01

**G133**

记录Task按期逾期、异常Action覆盖、责任日期关闭、Delay影响恢复、Issue验证关闭和Decision转Action

**H133**

完成“记录Task按期逾期、异常Action覆盖、责任日期关闭、Delay影响恢复、Issue验证关闭和Decision转Action”，使“执行闭环证据”能够按统一规则执行、检查并留下可验证结果。

**I133**

执行闭环证据包

**J133**

能识别闭环中断，区分Action完成和Issue关闭

**K133**

TARGET

**L133**

TBD

**M133**

TBD

**N133**

TBD

**O133**

未开始

**P133**

已定义

### Row 134

**A134**

Phase 1

**B134**

M6

**C134**

价值证据与Gate决策

**D134**

M6.5

**E134**

效率与业务结果

**F134**

M6.5-A01

**G134**

比较查找、周报、追问、重复维护、问题发现升级关闭

**H134**

完成“比较查找、周报、追问、重复维护、问题发现升级关闭”，使“效率与业务结果”能够按统一规则执行、检查并留下可验证结果。

**I134**

Pilot前后比较及价值结论

**J134**

基于基线，同时呈现改善、未改善、负面影响和数据不足

**K134**

TARGET

**L134**

TBD

**M134**

TBD

**N134**

TBD

**O134**

未开始

**P134**

已定义

### Row 135

**A135**

Phase 1

**B135**

M6

**C135**

价值证据与Gate决策

**D135**

M6.5

**E135**

效率与业务结果

**F135**

M6.5-A02

**G135**

记录决定结果、新增工作和负面影响

**H135**

完成“记录决定结果、新增工作和负面影响”，使“效率与业务结果”能够按统一规则执行、检查并留下可验证结果。

**I135**

Pilot前后比较及价值结论

**J135**

基于基线，同时呈现改善、未改善、负面影响和数据不足

**K135**

TARGET

**L135**

TBD

**M135**

TBD

**N135**

TBD

**O135**

未开始

**P135**

已定义

### Row 136

**A136**

Phase 1

**B136**

M6

**C136**

价值证据与Gate决策

**D136**

M6.5

**E136**

效率与业务结果

**F136**

M6.5-A03

**G136**

形成结论

**H136**

完成“形成结论”，使“效率与业务结果”能够按统一规则执行、检查并留下可验证结果。

**I136**

Pilot前后比较及价值结论

**J136**

基于基线，同时呈现改善、未改善、负面影响和数据不足

**K136**

TARGET

**L136**

TBD

**M136**

TBD

**N136**

TBD

**O136**

未开始

**P136**

已定义

### Row 137

**A137**

Phase 1

**B137**

M6

**C137**

价值证据与Gate决策

**D137**

M6.6

**E137**

平台能力评估

**F137**

M6.6-A01

**G137**

评估性能容量、中国访问、权限审计、自动化集成、导出迁移回退、支持许可成本及技术路线

**H137**

完成“评估性能容量、中国访问、权限审计、自动化集成、导出迁移回退、支持许可成本及技术路线”，使“平台能力评估”能够按统一规则执行、检查并留下可验证结果。

**I137**

平台评估及Phase 2技术路线建议

**J137**

基于真实使用，事实限制建议分开，不预设最终平台

**K137**

TARGET

**L137**

TBD

**M137**

TBD

**N137**

TBD

**O137**

未开始

**P137**

已定义

### Row 138

**A138**

Phase 1

**B138**

M6

**C138**

价值证据与Gate决策

**D138**

M6.7

**E138**

Gate 1决策

**F138**

M6.7-A01

**G138**

汇总证据

**H138**

完成“汇总证据”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**I138**

Gate 1评审包、决策记录及Phase 2条件

**J138**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**K138**

TARGET

**L138**

TBD

**M138**

TBD

**N138**

TBD

**O138**

未开始

**P138**

已定义

### Row 139

**A139**

Phase 1

**B139**

M6

**C139**

价值证据与Gate决策

**D139**

M6.7

**E139**

Gate 1决策

**F139**

M6.7-A02

**G139**

评估成功条件

**H139**

完成“评估成功条件”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**I139**

Gate 1评审包、决策记录及Phase 2条件

**J139**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**K139**

TARGET

**L139**

TBD

**M139**

TBD

**N139**

TBD

**O139**

未开始

**P139**

已定义

### Row 140

**A140**

Phase 1

**B140**

M6

**C140**

价值证据与Gate决策

**D140**

M6.7

**E140**

Gate 1决策

**F140**

M6.7-A03

**G140**

识别缺口风险

**H140**

完成“识别缺口风险”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**I140**

Gate 1评审包、决策记录及Phase 2条件

**J140**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**K140**

TARGET

**L140**

TBD

**M140**

TBD

**N140**

TBD

**O140**

未开始

**P140**

已定义

### Row 141

**A141**

Phase 1

**B141**

M6

**C141**

价值证据与Gate决策

**D141**

M6.7

**E141**

Gate 1决策

**F141**

M6.7-A04

**G141**

提出继续调整延长迁移停止建议

**H141**

完成“提出继续调整延长迁移停止建议”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**I141**

Gate 1评审包、决策记录及Phase 2条件

**J141**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**K141**

TARGET

**L141**

TBD

**M141**

TBD

**N141**

TBD

**O141**

未开始

**P141**

已定义

### Row 142

**A142**

Phase 1

**B142**

M6

**C142**

价值证据与Gate决策

**D142**

M6.7

**E142**

Gate 1决策

**F142**

M6.7-A05

**G142**

明确Phase 2条件和正式决定

**H142**

完成“明确Phase 2条件和正式决定”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**I142**

Gate 1评审包、决策记录及Phase 2条件

**J142**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**K142**

TARGET

**L142**

TBD

**M142**

TBD

**N142**

TBD

**O142**

未开始

**P142**

已定义

## Implementation Check

### Row 1

**A1**

AutoPM Phase 1 | Implementation Check

### Row 3

**A3**

本表只评价当前开发成果，不用于定义Target Map。先锁定目标任务，再填写当前实现和证据。

### Row 5

**A5**

判断顺序：目标要求 → 当前实现 → 覆盖程度 → 正确性判断 → 差距 → 修改行动 → 验证结果。

### Row 7

**A7**

模块

**B7**

能力包

**C7**

Action ID

**D7**

目标任务

**E7**

目标解释

**F7**

目标产出

**G7**

目标验收

**H7**

当前实现

**I7**

当前证据

**J7**

覆盖程度

**K7**

正确性判断

**L7**

主要差距

**M7**

修改行动

**N7**

Owner

**O7**

目标日期

**P7**

状态

### Row 8

**A8**

M1

**B8**

M1.1

**C8**

M1.1-A01

**D8**

定义项目结构对象

**E8**

明确Programme、Project、SKU等层级分别代表什么，以及一个Project如何包含多个SKU。

**F8**

对象清单、定义及系统归属表

**G8**

对象定义唯一清晰，边界和系统归属明确

**H8**

Projects表(3008条)、Tasks表、Issues表、People表已存在；Programme通过Projects表的Programme字段关联；SKU无独立表，分散在各业务表中。

**I8**

Airtable API验证：Projects 3008条，Tasks含Milestone/Task/Due Date/Completed By等字段，Issues表存在。

**J8**

部分覆盖

**K8**

需要修正

**L8**

Programme未独立成表；SKU无明确表或明确定义；对象边界未文档化；缺少统一的业务对象定义文档。

**M8**

编写业务对象定义文档；确认SKU表归属；Programme层级定义明确化。

**N8**

Sun Sun

**O8**

2026-09-18T00:00:00

**P8**

进行中

### Row 9

**A9**

M1

**B9**

M1.1

**C9**

M1.1-A02

**D9**

定义计划执行对象

**E9**

明确阶段、里程碑、任务和交付物分别表达什么，避免日期和状态混用。

**F9**

对象清单、定义及系统归属表

**G9**

对象定义唯一清晰，边界和系统归属明确

**H9**

Tasks表含Milestone(Manual)和Stage概念，但Stage未显式定义；Deliverable概念不存在。

**I9**

Tasks表schema含Milestone(Manual)(singleSelect)字段；无Deliverable字段。

**J9**

部分覆盖

**K9**

需要修正

**L9**

Stage、Deliverable概念未定义；计划→执行→完成的对象链不完整。

**M9**

定义Stage/Deliverable对象；明确与Milestone/Task的关系。

**N9**

Sun Sun

**O9**

2026-09-25T00:00:00

**P9**

进行中

### Row 10

**A10**

M1

**B10**

M1.1

**C10**

M1.1-A03

**D10**

定义异常对象

**E10**

明确Risk、Issue、Delay和Blocker如何区分，以及异常应该关联到哪个业务对象。

**F10**

对象清单、定义及系统归属表

**G10**

对象定义唯一清晰，边界和系统归属明确

**H10**

Issues表存在，含Key Issue/Delay Root Cause/Recovery/Solution/Current Impact字段；Risk/Delay/Blocker无独立对象。

**I10**

Issues表API验证：252条Key Issue, 18条Delay Root Cause。

**J10**

部分覆盖

**K10**

需要修正

**L10**

Risk、Delay、Blocker未独立定义；Issue与Delay/Blocker边界不清。

**M10**

定义Risk/Delay/Blocker对象；明确与Issue的区分规则。

**N10**

Sun Sun

**O10**

2026-09-30T00:00:00

**P10**

进行中

### Row 11

**A11**

M1

**B11**

M1.1

**C11**

M1.1-A04

**D11**

定义恢复与决策对象

**E11**

明确问题发生后如何记录恢复行动、责任人、管理决定、实际结果和验证关闭。

**F11**

对象清单、定义及系统归属表

**G11**

对象定义唯一清晰，边界和系统归属明确

**H11**

无Recovery Action独立表；Decision表不存在；Issue关闭逻辑未明确。

**I11**

Airtable 8表中无Recovery Actions或Decisions表。

**J11**

未覆盖

**K11**

资料不足

**L11**

Recovery Action和Decision完全缺失；无验证关闭机制。

**M11**

设计Recovery Action表结构；定义验证关闭流程。

**N11**

Sun Sun

**O11**

2026-10-16T00:00:00

**P11**

受阻

### Row 12

**A12**

M1

**B12**

M1.1

**C12**

M1.1-A05

**D12**

定义组织责任对象

**E12**

明确人员、团队、角色、执行责任、确认责任和决策责任如何区分。

**F12**

对象清单、定义及系统归属表

**G12**

对象定义唯一清晰，边界和系统归属明确

**H12**

Tasks表含Tasks Owners(Manual)(multipleRecordLinks)和Collaborators(multipleCollaborators)；People表存在。

**I12**

API验证：Tasks Owners链接到People；Collaborators含用户如Sun Sun(usr6l4kP2uAf5UhZK)。

**J12**

部分覆盖

**K12**

需要修正

**L12**

缺少确认人、决策人角色定义；Owner与Collaborator边界不清。

**M12**

明确各角色定义和权限边界。

**N12**

Sun Sun

**O12**

2026-10-09T00:00:00

**P12**

进行中

### Row 13

**A13**

M1

**B13**

M1.1

**C13**

M1.1-A06

**D13**

确认对象系统归属

**E13**

明确每类数据在哪里创建、在哪里维护、谁负责，以及AutoPM是读取、引用、计算还是写入。

**F13**

对象清单、定义及系统归属表

**G13**

对象定义唯一清晰，边界和系统归属明确

**H13**

SyncAutoPM v10支持三个方向同步（Airtable→Tracker、周报→Tracker、周报→Airtable）；数据来源部分明确。

**I13**

sync_tool.py v10三标签GUI；PMO Excel Tracker为主数据源。

**J13**

部分覆盖

**K13**

需要修正

**L13**

缺少正式的数据来源矩阵文档；AutoPM读写计算边界未文档化。

**M13**

编写数据来源与系统归属文档。

**N13**

Sun Sun

**O13**

2026-09-11T00:00:00

**P13**

进行中

### Row 14

**A14**

M1

**B14**

M1.2

**C14**

M1.2-A01

**D14**

建立项目层级、计划、责任、异常和恢复结果关系

**E14**

完成“建立项目层级、计划、责任、异常和恢复结果关系”，使“对象关系模型”能够按统一规则执行、检查并留下可验证结果。

**F14**

业务对象关系图及关系规则

**G14**

任务、异常和行动可追溯，汇总可下钻，无孤立核心记录

**H14**

Projects→Tasks通过Projects(system manage)链接；Projects→Issues通过linked record；Programme→Project通过文本字段。

**I14**

API验证：Tasks表含Projects(system manage)字段链接到Projects表。

**J14**

部分覆盖

**K14**

需要修正

**L14**

完整业务链(Project→SKU→Milestone→Task→Issue→Recovery→Result)未贯通；Programme未链接。

**M14**

建立完整对象关系链；Programme改为Linked Record。

**N14**

Sun Sun

**O14**

2026-10-23T00:00:00

**P14**

进行中

### Row 15

**A15**

M1

**B15**

M1.2

**C15**

M1.2-A02

**D15**

建立汇总下钻规则

**E15**

完成“建立汇总下钻规则”，使“对象关系模型”能够按统一规则执行、检查并留下可验证结果。

**F15**

业务对象关系图及关系规则

**G15**

任务、异常和行动可追溯，汇总可下钻，无孤立核心记录

**H15**

Projects表含Project ID；Task汇总到Project通过lookup；Issue汇总有限。

**I15**

Project ID(Manual)(from Project ID) lookup字段存在。

**J15**

部分覆盖

**K15**

需要修正

**L15**

汇总下钻规则未定义；SKU状态汇总到Project不存在。

**M15**

定义汇总下钻规则；实现状态向上聚合。

**N15**

Sun Sun

**O15**

2026-10-30T00:00:00

**P15**

未开始

### Row 16

**A16**

M1

**B16**

M1.2

**C16**

M1.2-A03

**D16**

处理跨项目和多SKU关系

**E16**

完成“处理跨项目和多SKU关系”，使“对象关系模型”能够按统一规则执行、检查并留下可验证结果。

**F16**

业务对象关系图及关系规则

**G16**

任务、异常和行动可追溯，汇总可下钻，无孤立核心记录

**H16**

多SKU项目管理通过文本字段分散记录；无正式的跨项目管理规则。

**I16**

Projects表无SKU linked record字段。

**J16**

未覆盖

**K16**

资料不足

**L16**

多SKU关系管理完全缺失；共同信息传递规则不存在。

**M16**

设计SKU表或SKU关联机制；定义跨项目管理规则。

**N16**

Sun Sun

**O16**

2026-11-06T00:00:00

**P16**

未开始

### Row 17

**A17**

M1

**B17**

M1.3

**C17**

M1.3-A01

**D17**

定义Project、SKU、Milestone、Task、Issue、Action和Decision标识

**E17**

完成“定义Project、SKU、Milestone、Task、Issue、Action和Decision标识”，使“唯一标识与映射”能够按统一规则执行、检查并留下可验证结果。

**F17**

唯一标识、映射和去重规则

**G17**

同一对象不重复，上下游稳定匹配，历史记录可处理

**H17**

Project ID字段存在(668条有值，占22.2%)；Task ID通过Automation AutoPM-04自动生成(ProjectID-T-001)；Issue ID通过AutoPM-05自动生成。

**I17**

Automation清单：AutoPM-04(Task ID)、AutoPM-05(Issue ID)均已上线(ON)。

**J17**

部分覆盖

**K17**

需要修正

**L17**

仅22.2%项目有Project ID；SKU/Milestone/Action/Decision无唯一编号。

**M17**

补全Project ID覆盖率；为其他对象建立编号规则。

**N17**

Sun Sun

**O17**

2026-09-11T00:00:00

**P17**

进行中

### Row 18

**A18**

M1

**B18**

M1.3

**C18**

M1.3-A02

**D18**

建立上游映射、去重和历史无ID处理规则

**E18**

完成“建立上游映射、去重和历史无ID处理规则”，使“唯一标识与映射”能够按统一规则执行、检查并留下可验证结果。

**F18**

唯一标识、映射和去重规则

**G18**

同一对象不重复，上下游稳定匹配，历史记录可处理

**H18**

SyncAutoPM v3.0支持模糊匹配(3-pass精确→0.9→0.85)和去重；历史ID补号规则不存在。

**I18**

sync_tool.py 3-pass匹配；sync_config.json别名配置。

**J18**

部分覆盖

**K18**

需要修正

**L18**

历史无ID记录无补号规则；无法确认数据的处理规则不存在。

**M18**

定义历史ID补号规则和例外处理流程。

**N18**

Sun Sun

**O18**

2026-09-18T00:00:00

**P18**

进行中

### Row 19

**A19**

M1

**B19**

M1.4

**C19**

M1.4-A01

**D19**

定义身份、责任、日期、生命周期、健康、执行和数据确认字段

**E19**

完成“定义身份、责任、日期、生命周期、健康、执行和数据确认字段”，使“字段与状态标准”能够按统一规则执行、检查并留下可验证结果。

**F19**

字段字典、状态字典和转换规则

**G19**

日期和状态不混用，状态条件明确，自动结果可解释

**H19**

Projects表130+字段；Tasks表含Task Name/Milestone/Due Date/Completed By/Status等核心字段；无统一字段字典。

**I19**

API schema读取确认字段存在；字段命名含(Manual)后缀区分手工/Auto字段。

**J19**

部分覆盖

**K19**

需要修正

**L19**

无正式字段字典；原计划/预测/实际日期字段混合（如Due Date同时承担计划和实际）。

**M19**

编写字段字典；分离计划日期、预测日期和实际日期。

**N19**

Sun Sun

**O19**

2026-09-25T00:00:00

**P19**

进行中

### Row 20

**A20**

M1

**B20**

M1.4

**C20**

M1.4-A02

**D20**

定义状态转换、重开和关闭规则

**E20**

完成“定义状态转换、重开和关闭规则”，使“字段与状态标准”能够按统一规则执行、检查并留下可验证结果。

**F20**

字段字典、状态字典和转换规则

**G20**

日期和状态不混用，状态条件明确，自动结果可解释

**H20**

Task状态通过singleSelect；Completed By(Manual)标记完成；Issue状态存在但转换规则未明确。

**I20**

Tasks表schema含Status字段；Completed By触发公式自动标记完成。

**J20**

部分覆盖

**K20**

需要修正

**L20**

状态转换条件未文档化；Action完成不自动关闭Issue(需人工)。

**M20**

定义状态转换规则和重开条件。

**N20**

Sun Sun

**O20**

2026-10-09T00:00:00

**P20**

未开始

### Row 21

**A21**

M1

**B21**

M1.5

**C21**

M1.5-A01

**D21**

确认关键字段正式来源

**E21**

完成“确认关键字段正式来源”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**F21**

数据来源矩阵、责任矩阵和读写规则

**G21**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**H21**

PMO Excel Tracker为主数据源；周报为里程碑日期来源；People数据来自HR系统手动导入。

**I21**

SyncAutoPM v10三方向同步；PMO Tracker作为权威源。

**J21**

部分覆盖

**K21**

需要修正

**L21**

无正式字段来源矩阵；部分字段来源不明确。

**M21**

编写字段来源矩阵文档。

**N21**

Sun Sun

**O21**

2026-09-25T00:00:00

**P21**

进行中

### Row 22

**A22**

M1

**B22**

M1.5

**C22**

M1.5-A02

**D22**

明确读写计算引用边界

**E22**

完成“明确读写计算引用边界”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**F22**

数据来源矩阵、责任矩阵和读写规则

**G22**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**H22**

SyncAutoPM明确了读取(Pull from Airtable)和写入(Push to Tracker/Airtable)方向；计算字段(公式)不可API写入。

**I22**

SyncAutoPM v10实现；Airtable API限制formula/rollup字段不可写。

**J22**

部分覆盖

**K22**

需要修正

**L22**

未形成完整的读写计算引用边界文档。

**M22**

编写系统读写边界表。

**N22**

Sun Sun

**O22**

2026-10-16T00:00:00

**P22**

未开始

### Row 23

**A23**

M1

**B23**

M1.5

**C23**

M1.5-A03

**D23**

指定业务与数据Owner

**E23**

完成“指定业务与数据Owner”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**F23**

数据来源矩阵、责任矩阵和读写规则

**G23**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**H23**

Sun Sun为主要Owner和维护者；业务Owner和数据Owner未分离。

**I23**

实际操作中Sun Sun负责全部维护。

**J23**

部分覆盖

**K23**

需要修正

**L23**

无正式的业务Owner与数据Owner责任分离定义。

**M23**

定义业务Owner和数据Owner责任矩阵。

**N23**

Sun Sun

**O23**

2026-09-18T00:00:00

**P23**

未开始

### Row 24

**A24**

M1

**B24**

M1.5

**C24**

M1.5-A04

**D24**

定义冲突、失败和双系统维护规则

**E24**

完成“定义冲突、失败和双系统维护规则”，使“数据来源与责任”能够按统一规则执行、检查并留下可验证结果。

**F24**

数据来源矩阵、责任矩阵和读写规则

**G24**

关键字段有来源和责任，无规则双维护被消除，冲突可处理

**H24**

双系统维护(Tracker+Airtable)通过SyncAutoPM同步；冲突处理依赖人工判断。

**I24**

SyncAutoPM v3.0空白保护(CSV空值不覆盖Tracker已有数据)。

**J24**

部分覆盖

**K24**

需要修正

**L24**

无正式的冲突失败处理规则；双系统退出条件未定义。

**M24**

编写冲突处理和双系统退出规则。

**N24**

Sun Sun

**O24**

2026-10-16T00:00:00

**P24**

未开始

### Row 25

**A25**

M1

**B25**

M1.6

**C25**

M1.6-A01

**D25**

确认试点项目

**E25**

完成“确认试点项目”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**F25**

可运行试点数据及修复清单

**G25**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**H25**

试点项目未正式确认；当前使用全部3008个项目(非选择性试点)。

**I25**

Projects表3008条记录全部导入。

**J25**

未覆盖

**K25**

资料不足

**L25**

未选择代表性试点项目；无试点范围确认文档。

**M25**

选择2-3个代表性试点项目并确认范围。

**N25**

Sun Sun

**O25**

2026-09-04T00:00:00

**P25**

受阻

### Row 26

**A26**

M1

**B26**

M1.6

**C26**

M1.6-A02

**D26**

清理记录

**E26**

完成“清理记录”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**F26**

可运行试点数据及修复清单

**G26**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**H26**

SyncAutoPM v10实现了全量导入(绿色+白色里程碑日期)；batch去重已修复。

**I26**

v10 Tab3更新为全部导入；1515 Overdue Tasks诊断完成。

**J26**

部分覆盖

**K26**

需要修正

**L26**

1125个项目无对应里程碑日期(项目无数据)；重复/冲突清理不完整。

**M26**

清理试点项目数据；补全缺失里程碑日期。

**N26**

Sun Sun

**O26**

2026-09-11T00:00:00

**P26**

进行中

### Row 27

**A27**

M1

**B27**

M1.6

**C27**

M1.6-A03

**D27**

建立Project与SKU关系

**E27**

完成“建立Project与SKU关系”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**F27**

可运行试点数据及修复清单

**G27**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**H27**

Projects表含项目信息但无SKU关联；SKU数据分散在外部系统。

**I27**

Projects表schema无SKU linked record字段。

**J27**

未覆盖

**K27**

资料不足

**L27**

Project与SKU关系未建立。

**M27**

建立Project-SKU关系；导入试点项目SKU数据。

**N27**

Sun Sun

**O27**

2026-10-23T00:00:00

**P27**

未开始

### Row 28

**A28**

M1

**B28**

M1.6

**C28**

M1.6-A04

**D28**

导入Milestone、Task、成员、异常和Action

**E28**

完成“导入Milestone、Task、成员、异常和Action”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**F28**

可运行试点数据及修复清单

**G28**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**H28**

Tasks已通过Automation(AutoPM-01)生成；Milestone通过周报导入；Issue手动创建；Recovery Action不存在。

**I28**

AutoPM-01 Project Task Generator(ON)；SyncAutoPM周报导入。

**J28**

部分覆盖

**K28**

需要修正

**L28**

Recovery Action不存在；Risk/Delay/Blocker未导入；成员关联有限。

**M28**

补全异常和行动数据导入。

**N28**

Sun Sun

**O28**

2026-10-09T00:00:00

**P28**

进行中

### Row 29

**A29**

M1

**B29**

M1.6

**C29**

M1.6-A05

**D29**

完成业务抽样

**E29**

完成“完成业务抽样”，使“真实项目数据初始化”能够按统一规则执行、检查并留下可验证结果。

**F29**

可运行试点数据及修复清单

**G29**

项目具有真实结构和执行数据，关系完整，业务抽样一致

**H29**

未进行正式业务抽样验证。

**I29**

无抽样验证记录。

**J29**

未覆盖

**K29**

资料不足

**L29**

无业务人员抽样确认记录。

**M29**

对试点项目进行业务抽样验证。

**N29**

Sun Sun

**O29**

2026-10-23T00:00:00

**P29**

未开始

### Row 30

**A30**

M1

**B30**

M1.7

**C30**

M1.7-A01

**D30**

建立必填、关系、重复、冲突、未更新和业务逻辑检查

**E30**

完成“建立必填、关系、重复、冲突、未更新和业务逻辑检查”，使“数据质量与审计”能够按统一规则执行、检查并留下可验证结果。

**F30**

质量规则、问题清单和审计记录

**G30**

问题可识别、分配和关闭，关键变化可追溯

**H30**

Overdue诊断脚本(diagnose_overdue.py)可检查日期异常；无系统性数据质量检查。

**I30**

diagnose_overdue.py/diagnose_sun_sun_tasks.py可运行。

**J30**

部分覆盖

**K30**

需要修正

**L30**

缺少必填缺失、关系断开、重复、冲突检查；无定期检查机制。

**M30**

建立系统性数据质量检查规则和定期运行机制。

**N30**

Sun Sun

**O30**

2026-09-30T00:00:00

**P30**

进行中

### Row 31

**A31**

M1

**B31**

M1.7

**C31**

M1.7-A02

**D31**

记录关键变更和数据产生方式

**E31**

完成“记录关键变更和数据产生方式”，使“数据质量与审计”能够按统一规则执行、检查并留下可验证结果。

**F31**

质量规则、问题清单和审计记录

**G31**

问题可识别、分配和关闭，关键变化可追溯

**H31**

Airtable原生记录Last Modified/Created By；无自定义变更记录。

**I31**

Airtable字段含Last Modified By/Created By(系统字段)。

**J31**

部分覆盖

**K31**

需要修正

**L31**

无关键变更审计记录；数据产生方式(人工/计算/同步)未标记。

**M31**

建立关键变更记录和数据产生方式标记。

**N31**

Sun Sun

**O31**

2026-10-30T00:00:00

**P31**

未开始

### Row 32

**A32**

M1

**B32**

M1.7

**C32**

M1.7-A03

**D32**

关闭质量问题

**E32**

完成“关闭质量问题”，使“数据质量与审计”能够按统一规则执行、检查并留下可验证结果。

**F32**

质量规则、问题清单和审计记录

**G32**

问题可识别、分配和关闭，关键变化可追溯

**H32**

问题发现后手动修复；无系统化的问题分配-修复-关闭流程。

**I32**

Overdue诊断后手动处理同步滞后任务。

**J32**

部分覆盖

**K32**

超出Phase 1

**L32**

无Owner分配和状态跟踪；修复后无重新验证机制。

**M32**

建立质量问题分配、修复、验证和关闭流程。

**N32**

Sun Sun

**O32**

2026-10-09T00:00:00

**P32**

未开始

### Row 33

**A33**

M2

**B33**

M2.1

**C33**

M2.1-A01

**D33**

识别新增与重复项目

**E33**

完成“识别新增与重复项目”，使“项目进入与初始化”能够按统一规则执行、检查并留下可验证结果。

**F33**

已初始化项目及范围责任记录

**G33**

项目身份唯一，结构、责任和模板明确

**H33**

SyncAutoPM v10支持PID匹配导入(97.5%+匹配率)；去重通过batch去重机制。

**I33**

SyncAutoPM v3.0模糊匹配；v10 GUI集成。

**J33**

部分覆盖

**K33**

需要修正

**L33**

项目进入前无自动重复检查流程；待确认标记不存在。

**M33**

增加项目进入前的重复检查步骤。

**N33**

Sun Sun

**O33**

2026-09-18T00:00:00

**P33**

进行中

### Row 34

**A34**

M2

**B34**

M2.1

**C34**

M2.1-A02

**D34**

确认Programme、Project Group、SKU、类型、阶段、范围、负责人、成员和模板

**E34**

完成“确认Programme、Project Group、SKU、类型、阶段、范围、负责人、成员和模板”，使“项目进入与初始化”能够按统一规则执行、检查并留下可验证结果。

**F34**

已初始化项目及范围责任记录

**G34**

项目身份唯一，结构、责任和模板明确

**H34**

项目导入时携带Type/Brand/Status/Owner等字段；模板概念不存在。

**I34**

PMO Tracker含项目元数据字段。

**J34**

部分覆盖

**K34**

需要修正

**L34**

无项目模板选择机制；SKU/成员/关键日期确认不完整。

**M34**

设计项目模板和进入确认流程。

**N34**

Sun Sun

**O34**

2026-10-09T00:00:00

**P34**

未开始

### Row 35

**A35**

M2

**B35**

M2.2

**C35**

M2.2-A01

**D35**

建立阶段和Milestone

**E35**

完成“建立阶段和Milestone”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**F35**

项目基线计划及任务责任清单

**G35**

关键里程碑和任务有日期、责任、依赖并可执行

**H35**

Milestone通过周报导入到Projects表(20+日期字段)；Stage未显式定义。

**I35**

Projects表含Start Date/TRA Date/Cut Steel Date/FOT Date/EB1-EB3 Date等20+里程碑字段。

**J35**

部分覆盖

**K35**

需要修正

**L35**

Stage未定义；Milestone模板不存在（依赖周报格式）。

**M35**

定义Stage模型；建立Milestone模板选择机制。

**N35**

Sun Sun

**O35**

2026-10-16T00:00:00

**P35**

进行中

### Row 36

**A36**

M2

**B36**

M2.2

**C36**

M2.2-A02

**D36**

导入或生成Task

**E36**

完成“导入或生成Task”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**F36**

项目基线计划及任务责任清单

**G36**

关键里程碑和任务有日期、责任、依赖并可执行

**H36**

AutoPM-01 Project Task Generator自动从Milestone生成Task；Task含Milestone(Manual)字段。

**I36**

Automation AutoPM-01(ON)生成Task。

**J36**

部分覆盖

**K36**

需要修正

**L36**

Task生成后无法删除不适用任务；项目特有任务补充机制不完善。

**M36**

增加Task筛选和补充机制。

**N36**

Sun Sun

**O36**

2026-10-16T00:00:00

**P36**

进行中

### Row 37

**A37**

M2

**B37**

M2.2

**C37**

M2.2-A03

**D37**

明确交付物和依赖

**E37**

完成“明确交付物和依赖”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**F37**

项目基线计划及任务责任清单

**G37**

关键里程碑和任务有日期、责任、依赖并可执行

**H37**

Task含前置依赖字段(通过lookup)；Deliverable概念不存在。

**I37**

Tasks表schema有限依赖字段。

**J37**

部分覆盖

**K37**

需要修正

**L37**

Deliverable未定义；依赖关系表达能力有限。

**M37**

增强依赖关系；定义Deliverable概念。

**N37**

Sun Sun

**O37**

2026-11-13T00:00:00

**P37**

未开始

### Row 38

**A38**

M2

**B38**

M2.2

**C38**

M2.2-A04

**D38**

分配Owner

**E38**

完成“分配Owner”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**F38**

项目基线计划及任务责任清单

**G38**

关键里程碑和任务有日期、责任、依赖并可执行

**H38**

Tasks Owners(Manual)字段支持分配Owner；Collaborators字段支持多人协作。

**I38**

API验证字段存在并有数据。

**J38**

部分覆盖

**K38**

正确

**L38**

部分Task缺少Owner分配。

**M38**

确保所有Task有Owner。（原始评级：大部分覆盖）

**N38**

Sun Sun

**O38**

2026-09-30T00:00:00

**P38**

进行中

### Row 39

**A39**

M2

**B39**

M2.2

**C39**

M2.2-A05

**D39**

设置Baseline与Due

**E39**

完成“设置Baseline与Due”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**F39**

项目基线计划及任务责任清单

**G39**

关键里程碑和任务有日期、责任、依赖并可执行

**H39**

Due Date(Manual)从Milestone日期同步；Baseline概念不存在；优先级未定义。

**I39**

SyncAutoPM里程碑→Due Date映射。

**J39**

部分覆盖

**K39**

需要修正

**L39**

无Baseline日期(原计划日期)；无优先级字段。

**M39**

增加Baseline和优先级字段。

**N39**

Sun Sun

**O39**

2026-09-18T00:00:00

**P39**

进行中

### Row 40

**A40**

M2

**B40**

M2.2

**C40**

M2.2-A06

**D40**

确认计划并记录变更

**E40**

完成“确认计划并记录变更”，使“计划与任务建立”能够按统一规则执行、检查并留下可验证结果。

**F40**

项目基线计划及任务责任清单

**G40**

关键里程碑和任务有日期、责任、依赖并可执行

**H40**

无计划确认流程；变更无记录。

**I40**

无确认记录。

**J40**

未覆盖

**K40**

资料不足

**L40**

计划未经业务确认；变更无记录。

**M40**

建立计划确认和变更记录流程。

**N40**

Sun Sun

**O40**

2026-10-23T00:00:00

**P40**

未开始

### Row 41

**A41**

M2

**B41**

M2.3

**C41**

M2.3-A01

**D41**

查看待办

**E41**

完成“查看待办”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**F41**

持续更新的执行状态及承诺结果记录

**G41**

状态真实，计划预测实际可比较，长期未更新可识别

**H41**

My Tasks视图存在；Collaborators过滤可用；Overdue/Due today可查看。

**I41**

Airtable Interface含My Tasks视图。

**J41**

部分覆盖

**K41**

需要修正

**L41**

待办视图不完整(缺少等待/受阻/待确认分类)；更新入口分散。

**M41**

完善个人待办视图分类。

**N41**

Sun Sun

**O41**

2026-09-11T00:00:00

**P41**

进行中

### Row 42

**A42**

M2

**B42**

M2.3

**C42**

M2.3-A02

**D42**

更新Task和Forecast

**E42**

完成“更新Task和Forecast”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**F42**

持续更新的执行状态及承诺结果记录

**G42**

状态真实，计划预测实际可比较，长期未更新可识别

**H42**

Task状态可手动更新；Completed By标记完成；Forecast Date不存在。

**I42**

Tasks表Status字段可编辑。

**J42**

部分覆盖

**K42**

需要修正

**L42**

无Forecast Date字段；原计划/预测/实际日期未分离。

**M42**

增加Forecast Date字段；分离日期类型。

**N42**

Sun Sun

**O42**

2026-10-16T00:00:00

**P42**

未开始

### Row 43

**A43**

M2

**B43**

M2.3

**C43**

M2.3-A03

**D43**

提交交付物或证据

**E43**

完成“提交交付物或证据”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**F43**

持续更新的执行状态及承诺结果记录

**G43**

状态真实，计划预测实际可比较，长期未更新可识别

**H43**

Task%Complete字段不存在；进度通过状态(Status)表达。

**I43**

Tasks表schema无%Complete字段。

**J43**

部分覆盖

**K43**

需要修正

**L43**

无百分比进度字段；更新频率不固定。

**M43**

考虑增加进度表达方式。

**N43**

Sun Sun

**O43**

2026-11-13T00:00:00

**P43**

未开始

### Row 44

**A44**

M2

**B44**

M2.3

**C44**

M2.3-A04

**D44**

记录下一步、等待、阻塞、变化、更新时间和更新人

**E44**

完成“记录下一步、等待、阻塞、变化、更新时间和更新人”，使“日常执行与更新”能够按统一规则执行、检查并留下可验证结果。

**F44**

持续更新的执行状态及承诺结果记录

**G44**

状态真实，计划预测实际可比较，长期未更新可识别

**H44**

Blocker/Waiting状态不存在于Task状态选项中。

**I44**

Tasks表Status字段选项有限。

**J44**

未覆盖

**K44**

资料不足

**L44**

无法记录等待、阻塞状态。

**M44**

扩展Task状态选项。

**N44**

Sun Sun

**O44**

2026-10-16T00:00:00

**P44**

未开始

### Row 45

**A45**

M2

**B45**

M2.4

**C45**

M2.4-A01

**D45**

识别并分类Issue、Risk、Delay和Blocker

**E45**

完成“识别并分类Issue、Risk、Delay和Blocker”，使“异常识别与记录”能够按统一规则执行、检查并留下可验证结果。

**F45**

结构化异常记录及影响责任

**G45**

分类一致，影响对象、Owner、状态和下一步明确

**H45**

Issues表存在含Key Issue字段。

**I45**

API验证252条Issue。

**J45**

部分覆盖

**K45**

需要修正

**L45**

Risk/Delay/Blocker未独立；影响评估缺失。

**M45**

扩展异常类型。

**N45**

Sun Sun

**O45**

2026-09-30T00:00:00

**P45**

未开始

### Row 46

**A46**

M2

**B46**

M2.4

**C46**

M2.4-A02

**D46**

关联影响对象

**E46**

完成“关联影响对象”，使“异常识别与记录”能够按统一规则执行、检查并留下可验证结果。

**F46**

结构化异常记录及影响责任

**G46**

分类一致，影响对象、Owner、状态和下一步明确

**H46**

Issue含Delay Root Cause字段。

**I46**

API验证18条。

**J46**

部分覆盖

**K46**

需要修正

**L46**

影响范围和严重程度未结构化。

**M46**

增加影响评估字段。

**N46**

Sun Sun

**O46**

2026-10-30T00:00:00

**P46**

未开始

### Row 47

**A47**

M2

**B47**

M2.4

**C47**

M2.4-A03

**D47**

记录影响、严重度、原因、Owner、升级需求和重复异常

**E47**

完成“记录影响、严重度、原因、Owner、升级需求和重复异常”，使“异常识别与记录”能够按统一规则执行、检查并留下可验证结果。

**F47**

结构化异常记录及影响责任

**G47**

分类一致，影响对象、Owner、状态和下一步明确

**H47**

Issue可链接到Project和Task。

**I47**

linked record字段存在。

**J47**

部分覆盖

**K47**

需要修正

**L47**

异常与Owner/Action关联不完整。

**M47**

完善异常关联关系。

**N47**

Sun Sun

**O47**

2026-10-30T00:00:00

**P47**

未开始

### Row 48

**A48**

M2

**B48**

M2.5

**C48**

M2.5-A01

**D48**

创建Recovery Action

**E48**

完成“创建Recovery Action”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**F48**

恢复行动计划及责任日期结果

**G48**

关键异常有行动或处置结论，逾期无效行动可升级

**H48**

Recovery Action不存在独立表。

**I48**

8表中无Recovery Actions。

**J48**

未覆盖

**K48**

资料不足

**L48**

Recovery Action完全缺失。

**M48**

建立Recovery Action表。

**N48**

Sun Sun

**O48**

2026-10-23T00:00:00

**P48**

未开始

### Row 49

**A49**

M2

**B49**

M2.5

**C49**

M2.5-A02

**D49**

指定Owner

**E49**

完成“指定Owner”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**F49**

恢复行动计划及责任日期结果

**G49**

关键异常有行动或处置结论，逾期无效行动可升级

**H49**

升级机制不存在。

**I49**

无升级记录。

**J49**

未覆盖

**K49**

资料不足

**L49**

无升级流程和规则。

**M49**

设计升级机制。

**N49**

Sun Sun

**O49**

2026-10-23T00:00:00

**P49**

未开始

### Row 50

**A50**

M2

**B50**

M2.5

**C50**

M2.5-A03

**D50**

设置Due和恢复目标

**E50**

完成“设置Due和恢复目标”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**F50**

恢复行动计划及责任日期结果

**G50**

关键异常有行动或处置结论，逾期无效行动可升级

**H50**

无行动跟踪。

**I50**

无Action表。

**J50**

未覆盖

**K50**

资料不足

**L50**

无行动分配和跟踪系统。

**M50**

建立行动跟踪。

**N50**

Sun Sun

**O50**

2026-10-23T00:00:00

**P50**

未开始

### Row 51

**A51**

M2

**B51**

M2.5

**C51**

M2.5-A04

**D51**

更新优先级、状态、进展和结果

**E51**

完成“更新优先级、状态、进展和结果”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**F51**

恢复行动计划及责任日期结果

**G51**

关键异常有行动或处置结论，逾期无效行动可升级

**H51**

无升级记录。

**I51**

无。

**J51**

未覆盖

**K51**

资料不足

**L51**

升级未记录。

**M51**

记录升级。

**N51**

Sun Sun

**O51**

2026-10-30T00:00:00

**P51**

未开始

### Row 52

**A52**

M2

**B52**

M2.5

**C52**

M2.5-A05

**D52**

识别逾期无效行动并升级

**E52**

完成“识别逾期无效行动并升级”，使“恢复行动与升级”能够按统一规则执行、检查并留下可验证结果。

**F52**

恢复行动计划及责任日期结果

**G52**

关键异常有行动或处置结论，逾期无效行动可升级

**H52**

无。

**I52**

无。

**J52**

未覆盖

**K52**

资料不足

**L52**

完全缺失。

**M52**

设计恢复行动管理。

**N52**

Sun Sun

**O52**

2026-11-06T00:00:00

**P52**

未开始

### Row 53

**A53**

M2

**B53**

M2.6

**C53**

M2.6-A01

**D53**

识别待决策事项

**E53**

完成“识别待决策事项”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**F53**

待决策清单、决策记录和后续行动

**G53**

决策事项、人员、期限、理由和结果可追踪

**H53**

无决策表。

**I53**

无。

**J53**

未覆盖

**K53**

资料不足

**L53**

管理决策完全缺失。

**M53**

建立Decision表。

**N53**

Sun Sun

**O53**

2026-10-23T00:00:00

**P53**

未开始

### Row 54

**A54**

M2

**B54**

M2.6

**C54**

M2.6-A02

**D54**

记录背景、影响、时限、方案和建议

**E54**

完成“记录背景、影响、时限、方案和建议”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**F54**

待决策清单、决策记录和后续行动

**G54**

决策事项、人员、期限、理由和结果可追踪

**H54**

无。

**I54**

无。

**J54**

未覆盖

**K54**

资料不足

**L54**

决策触发未定义。

**M54**

定义决策触发条件。

**N54**

Sun Sun

**O54**

2026-10-23T00:00:00

**P54**

未开始

### Row 55

**A55**

M2

**B55**

M2.6

**C55**

M2.6-A03

**D55**

指定决策人

**E55**

完成“指定决策人”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**F55**

待决策清单、决策记录和后续行动

**G55**

决策事项、人员、期限、理由和结果可追踪

**H55**

无。

**I55**

无。

**J55**

未覆盖

**K55**

资料不足

**L55**

决策记录缺失。

**M55**

建立决策记录。

**N55**

Sun Sun

**O55**

2026-10-30T00:00:00

**P55**

未开始

### Row 56

**A56**

M2

**B56**

M2.6

**C56**

M2.6-A04

**D56**

记录决定理由

**E56**

完成“记录决定理由”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**F56**

待决策清单、决策记录和后续行动

**G56**

决策事项、人员、期限、理由和结果可追踪

**H56**

无。

**I56**

无。

**J56**

未覆盖

**K56**

资料不足

**L56**

决策跟踪缺失。

**M56**

建立决策跟踪。

**N56**

Sun Sun

**O56**

2026-10-30T00:00:00

**P56**

未开始

### Row 57

**A57**

M2

**B57**

M2.6

**C57**

M2.6-A05

**D57**

转化Action并跟踪结果

**E57**

完成“转化Action并跟踪结果”，使“管理决策”能够按统一规则执行、检查并留下可验证结果。

**F57**

待决策清单、决策记录和后续行动

**G57**

决策事项、人员、期限、理由和结果可追踪

**H57**

无。

**I57**

无。

**J57**

未覆盖

**K57**

资料不足

**L57**

决策落实缺失。

**M57**

建立决策落实机制。

**N57**

Sun Sun

**O57**

2026-11-06T00:00:00

**P57**

未开始

### Row 58

**A58**

M2

**B58**

M2.7

**C58**

M2.7-A01

**D58**

检查Action

**E58**

完成“检查Action”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**F58**

验证关闭记录及结果证据

**G58**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**H58**

无。

**I58**

无。

**J58**

未覆盖

**K58**

资料不足

**L58**

结果确认缺失。

**M58**

建立结果确认流程。

**N58**

Sun Sun

**O58**

2026-11-06T00:00:00

**P58**

未开始

### Row 59

**A59**

M2

**B59**

M2.7

**C59**

M2.7-A02

**D59**

记录结果

**E59**

完成“记录结果”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**F59**

验证关闭记录及结果证据

**G59**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**H59**

无。

**I59**

无。

**J59**

未覆盖

**K59**

资料不足

**L59**

验证关闭缺失。

**M59**

建立验证关闭。

**N59**

Sun Sun

**O59**

2026-11-06T00:00:00

**P59**

未开始

### Row 60

**A60**

M2

**B60**

M2.7

**C60**

M2.7-A03

**D60**

确认影响是否消除或接受

**E60**

完成“确认影响是否消除或接受”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**F60**

验证关闭记录及结果证据

**G60**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**H60**

无。

**I60**

无。

**J60**

未覆盖

**K60**

资料不足

**L60**

重开机制缺失。

**M60**

建立重开机制。

**N60**

Sun Sun

**O60**

2026-11-13T00:00:00

**P60**

未开始

### Row 61

**A61**

M2

**B61**

M2.7

**C61**

M2.7-A04

**D61**

指定验证人

**E61**

完成“指定验证人”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**F61**

验证关闭记录及结果证据

**G61**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**H61**

无。

**I61**

无。

**J61**

未覆盖

**K61**

资料不足

**L61**

关闭记录缺失。

**M61**

建立关闭记录。

**N61**

Sun Sun

**O61**

2026-11-06T00:00:00

**P61**

未开始

### Row 62

**A62**

M2

**B62**

M2.7

**C62**

M2.7-A05

**D62**

提交证据

**E62**

完成“提交证据”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**F62**

验证关闭记录及结果证据

**G62**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**H62**

无。

**I62**

无。

**J62**

未覆盖

**K62**

资料不足

**L62**

关闭确认缺失。

**M62**

建立关闭确认。

**N62**

Sun Sun

**O62**

2026-11-13T00:00:00

**P62**

未开始

### Row 63

**A63**

M2

**B63**

M2.7

**C63**

M2.7-A06

**D63**

正式关闭或重开

**E63**

完成“正式关闭或重开”，使“结果确认与验证关闭”能够按统一规则执行、检查并留下可验证结果。

**F63**

验证关闭记录及结果证据

**G63**

Action完成不等于Issue关闭，关闭有结果、证据和验证人

**H63**

无。

**I63**

无。

**J63**

未覆盖

**K63**

资料不足

**L63**

结果归档缺失。

**M63**

建立结果归档。

**N63**

Sun Sun

**O63**

2026-11-13T00:00:00

**P63**

未开始

### Row 64

**A64**

M2

**B64**

M2.8

**C64**

M2.8-A01

**D64**

保留计划和状态变化

**E64**

完成“保留计划和状态变化”，使“历史与经验沉淀”能够按统一规则执行、检查并留下可验证结果。

**F64**

结构化执行历史及问题处理案例

**G64**

原因、行动、决定和结果可关联，案例来自真实关闭记录

**H64**

无。

**I64**

无。

**J64**

未覆盖

**K64**

资料不足

**L64**

经验沉淀缺失。

**M64**

建立经验沉淀机制。

**N64**

Sun Sun

**O64**

2026-11-13T00:00:00

**P64**

未开始

### Row 65

**A65**

M2

**B65**

M2.8

**C65**

M2.8-A02

**D65**

记录Root Cause、有效无效Action、关键Decision、最终Result和可检索案例

**E65**

完成“记录Root Cause、有效无效Action、关键Decision、最终Result和可检索案例”，使“历史与经验沉淀”能够按统一规则执行、检查并留下可验证结果。

**F65**

结构化执行历史及问题处理案例

**G65**

原因、行动、决定和结果可关联，案例来自真实关闭记录

**H65**

无。

**I65**

无。

**J65**

未覆盖

**K65**

资料不足

**L65**

经验复用缺失。

**M65**

建立经验复用。

**N65**

Sun Sun

**O65**

2026-11-20T00:00:00

**P65**

未开始

### Row 66

**A66**

M3

**B66**

M3.1

**C66**

M3.1-A01

**D66**

展示今日、即将到期、逾期、待更新、待确认、本人异常和Action

**E66**

完成“展示今日、即将到期、逾期、待更新、待确认、本人异常和Action”，使“个人执行入口”能够按统一规则执行、检查并留下可验证结果。

**F66**

My Daily Work入口

**G66**

一个入口找到并完成核心工作，可返回项目背景，减少重复维护

**H66**

My Tasks视图可用(Collaborators过滤)。

**I66**

Airtable Interface截图验证。

**J66**

部分覆盖

**K66**

需要修正

**L66**

缺少异常、行动和待确认事项聚合。

**M66**

增强个人入口功能。

**N66**

Sun Sun

**O66**

2026-09-18T00:00:00

**P66**

进行中

### Row 67

**A67**

M3

**B67**

M3.1

**C67**

M3.1-A02

**D67**

支持更新、提交结果并进入项目背景

**E67**

完成“支持更新、提交结果并进入项目背景”，使“个人执行入口”能够按统一规则执行、检查并留下可验证结果。

**F67**

My Daily Work入口

**G67**

一个入口找到并完成核心工作，可返回项目背景，减少重复维护

**H67**

可直接在Airtable编辑Task状态。

**I67**

Interface支持直接编辑。

**J67**

部分覆盖

**K67**

需要修正

**L67**

更新动作分散；无一键完成。

**M67**

优化更新动作。

**N67**

Sun Sun

**O67**

2026-10-23T00:00:00

**P67**

进行中

### Row 68

**A68**

M3

**B68**

M3.2

**C68**

M3.2-A01

**D68**

展示项目、SKU、阶段、健康、Milestone、Task、异常、Action、待决策和缺失项

**E68**

完成“展示项目、SKU、阶段、健康、Milestone、Task、异常、Action、待决策和缺失项”，使“项目管理入口”能够按统一规则执行、检查并留下可验证结果。

**F68**

Project Workspace及可信项目视图

**G68**

偏差、影响、Owner和下一步清楚，无需另做解释报告

**H68**

Projects表可按项目查看。

**I68**

Projects表含多视图。

**J68**

部分覆盖

**K68**

需要修正

**L68**

缺少项目工作空间(结构+计划+异常+决定集中)。

**M68**

建立项目工作空间。

**N68**

Sun Sun

**O68**

2026-10-30T00:00:00

**P68**

未开始

### Row 69

**A69**

M3

**B69**

M3.2

**C69**

M3.2-A02

**D69**

支持更新、审查和下钻

**E69**

完成“支持更新、审查和下钻”，使“项目管理入口”能够按统一规则执行、检查并留下可验证结果。

**F69**

Project Workspace及可信项目视图

**G69**

偏差、影响、Owner和下一步清楚，无需另做解释报告

**H69**

Project详情页有限。

**I69**

Airtable record expand。

**J69**

部分覆盖

**K69**

需要修正

**L69**

项目集中维护能力不足。

**M69**

增强项目管理视图。

**N69**

Sun Sun

**O69**

2026-11-06T00:00:00

**P69**

未开始

### Row 70

**A70**

M3

**B70**

M3.3

**C70**

M3.3-A01

**D70**

展示开放、缺失Owner/Action/Due、逾期和待关闭异常

**E70**

完成“展示开放、缺失Owner/Action/Due、逾期和待关闭异常”，使“异常处理入口”能够按统一规则执行、检查并留下可验证结果。

**F70**

统一异常处理入口

**G70**

异常集中可见，可直接分配、行动、升级和关闭

**H70**

Issues表可按状态过滤。

**I70**

Issues表含Status字段。

**J70**

部分覆盖

**K70**

需要修正

**L70**

缺少工作队列(缺Owner/缺Action/逾期/待关闭)。

**M70**

建立异常工作队列。

**N70**

Sun Sun

**O70**

2026-10-30T00:00:00

**P70**

未开始

### Row 71

**A71**

M3

**B71**

M3.3

**C71**

M3.3-A02

**D71**

支持分配、行动、更新、升级、决策和关闭

**E71**

完成“支持分配、行动、更新、升级、决策和关闭”，使“异常处理入口”能够按统一规则执行、检查并留下可验证结果。

**F71**

统一异常处理入口

**G71**

异常集中可见，可直接分配、行动、升级和关闭

**H71**

可直接编辑Issue。

**I71**

Interface支持。

**J71**

部分覆盖

**K71**

需要修正

**L71**

处理动作不完整。

**M71**

增强异常处理能力。

**N71**

Sun Sun

**O71**

2026-11-13T00:00:00

**P71**

未开始

### Row 72

**A72**

M3

**B72**

M3.4

**C72**

M3.4-A01

**D72**

展示健康、变化、偏差、Top Risk、逾期、缺失、待决策和上周结果

**E72**

完成“展示健康、变化、偏差、Top Risk、逾期、缺失、待决策和上周结果”，使“周度管理入口”能够按统一规则执行、检查并留下可验证结果。

**F72**

周度管理视图及决定行动记录

**G72**

周会直接使用AutoPM，决定回写，下周期验证结果

**H72**

AutoPM-08 Weekly Report Automation每周五9:30触发。

**I72**

Automation清单(ON)。

**J72**

部分覆盖

**K72**

需要修正

**L72**

周报基于数据生成，但周度审查流程未结构化。

**M72**

建立周度审查流程。

**N72**

Sun Sun

**O72**

2026-10-09T00:00:00

**P72**

进行中

### Row 73

**A73**

M3

**B73**

M3.4

**C73**

M3.4-A02

**D73**

支持确认、决定和行动回写

**E73**

完成“支持确认、决定和行动回写”，使“周度管理入口”能够按统一规则执行、检查并留下可验证结果。

**F73**

周度管理视图及决定行动记录

**G73**

周会直接使用AutoPM，决定回写，下周期验证结果

**H73**

无会议结果写回机制。

**I73**

无。

**J73**

未覆盖

**K73**

资料不足

**L73**

会议结果无法写回系统。

**M73**

设计会议结果写回。

**N73**

Sun Sun

**O73**

2026-11-13T00:00:00

**P73**

未开始

### Row 74

**A74**

M3

**B74**

M3.5

**C74**

M3.5-A01

**D74**

展示组合健康、关键风险延误、受影响Milestone和待决策项

**E74**

完成“展示组合健康、关键风险延误、受影响Milestone和待决策项”，使“领导审查与下钻”能够按统一规则执行、检查并留下可验证结果。

**F74**

Leadership View及下钻路径

**G74**

汇总结论可下钻，管理决定和后续行动可追踪

**H74**

无领导审查看板。

**I74**

无。

**J74**

未覆盖

**K74**

资料不足

**L74**

组合健康、重大风险视图缺失。

**M74**

建立领导审查看板。

**N74**

Sun Sun

**O74**

2026-11-20T00:00:00

**P74**

未开始

### Row 75

**A75**

M3

**B75**

M3.5

**C75**

M3.5-A02

**D75**

逐层下钻至Project、SKU、异常、Action、Owner和Result

**E75**

完成“逐层下钻至Project、SKU、异常、Action、Owner和Result”，使“领导审查与下钻”能够按统一规则执行、检查并留下可验证结果。

**F75**

Leadership View及下钻路径

**G75**

汇总结论可下钻，管理决定和后续行动可追踪

**H75**

无下钻功能。

**I75**

无。

**J75**

未覆盖

**K75**

资料不足

**L75**

逐层下钻到事实/责任/结果缺失。

**M75**

建立下钻能力。

**N75**

Sun Sun

**O75**

2026-11-20T00:00:00

**P75**

未开始

### Row 76

**A76**

M3

**B76**

M3.6

**C76**

M3.6-A01

**D76**

删除无用字段

**E76**

完成“删除无用字段”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**F76**

用户问题清单及界面修复任务

**G76**

核心动作易完成，信息一次维护，反馈转为可验收任务

**H76**

Interface已有基础UI。

**I76**

Airtable Interface存在。

**J76**

部分覆盖

**K76**

需要修正

**L76**

字段冗余和重复录入问题存在。

**M76**

优化UI减少冗余。

**N76**

Sun Sun

**O76**

2026-09-30T00:00:00

**P76**

未开始

### Row 77

**A77**

M3

**B77**

M3.6

**C77**

M3.6-A02

**D77**

减少重复录入和页面切换

**E77**

完成“减少重复录入和页面切换”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**F77**

用户问题清单及界面修复任务

**G77**

核心动作易完成，信息一次维护，反馈转为可验收任务

**H77**

部分。

**I77**

Interface。

**J77**

部分覆盖

**K77**

需要修正

**L77**

页面切换频繁。

**M77**

减少页面切换。

**N77**

Sun Sun

**O77**

2026-11-06T00:00:00

**P77**

进行中

### Row 78

**A78**

M3

**B78**

M3.6

**C78**

M3.6-A03

**D78**

突出下一步

**E78**

完成“突出下一步”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**F78**

用户问题清单及界面修复任务

**G78**

核心动作易完成，信息一次维护，反馈转为可验收任务

**H78**

无。

**I78**

无。

**J78**

未覆盖

**K78**

资料不足

**L78**

用户反馈收集缺失。

**M78**

建立反馈收集。

**N78**

Sun Sun

**O78**

2026-09-25T00:00:00

**P78**

未开始

### Row 79

**A79**

M3

**B79**

M3.6

**C79**

M3.6-A04

**D79**

简化更新

**E79**

完成“简化更新”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**F79**

用户问题清单及界面修复任务

**G79**

核心动作易完成，信息一次维护，反馈转为可验收任务

**H79**

无。

**I79**

无。

**J79**

未覆盖

**K79**

资料不足

**L79**

反馈分类排序缺失。

**M79**

建立反馈管理。

**N79**

Sun Sun

**O79**

2026-10-16T00:00:00

**P79**

未开始

### Row 80

**A80**

M3

**B80**

M3.6

**C80**

M3.6-A05

**D80**

提供说明

**E80**

完成“提供说明”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**F80**

用户问题清单及界面修复任务

**G80**

核心动作易完成，信息一次维护，反馈转为可验收任务

**H80**

无。

**I80**

无。

**J80**

未覆盖

**K80**

资料不足

**L80**

改进验收缺失。

**M80**

建立改进验收。

**N80**

Sun Sun

**O80**

2026-10-09T00:00:00

**P80**

未开始

### Row 81

**A81**

M3

**B81**

M3.6

**C81**

M3.6-A06

**D81**

收集并排序用户问题

**E81**

完成“收集并排序用户问题”，使“用户体验与动作效率”能够按统一规则执行、检查并留下可验证结果。

**F81**

用户问题清单及界面修复任务

**G81**

核心动作易完成，信息一次维护，反馈转为可验收任务

**H81**

无。

**I81**

无。

**J81**

未覆盖

**K81**

资料不足

**L81**

体验度量缺失。

**M81**

建立体验度量。

**N81**

Sun Sun

**O81**

2026-09-25T00:00:00

**P81**

未开始

### Row 82

**A82**

M4

**B82**

M4.1

**C82**

M4.1-A01

**D82**

建立导入模板

**E82**

完成“建立导入模板”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**F82**

稳定导入流程及错误报告

**G82**

不重复，错误可定位，不静默覆盖真实数据

**H82**

SyncAutoPM v10 Tab3实现周报→Airtable导入。

**I82**

sync_tool.py v10 GUI。

**J82**

部分覆盖

**K82**

正确

**L82**

格式错误检测和防护可增强。

**M82**

增强格式校验。（原始评级：大部分覆盖）

**N82**

Sun Sun

**O82**

2026-09-18T00:00:00

**P82**

进行中

### Row 83

**A83**

M4

**B83**

M4.1

**C83**

M4.1-A02

**D83**

校验格式

**E83**

完成“校验格式”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**F83**

稳定导入流程及错误报告

**G83**

不重复，错误可定位，不静默覆盖真实数据

**H83**

batch去重已修复；PID匹配去重(97.5%+)。

**I83**

SyncAutoPM v3.0匹配。

**J83**

部分覆盖

**K83**

正确

**L83**

极少数无法匹配的项目需人工处理。

**M83**

增强无法匹配项处理。（原始评级：大部分覆盖）

**N83**

Sun Sun

**O83**

2026-09-30T00:00:00

**P83**

进行中

### Row 84

**A84**

M4

**B84**

M4.1

**C84**

M4.1-A03

**D84**

匹配ID和Owner

**E84**

完成“匹配ID和Owner”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**F84**

稳定导入流程及错误报告

**G84**

不重复，错误可定位，不静默覆盖真实数据

**H84**

SyncAutoPM v10 Tab1实现Airtable→Tracker导出。

**I84**

sync_tool.py Tab1。

**J84**

部分覆盖

**K84**

正确

**L84**

错误覆盖保护(空白保护)已实现。

**M84**

持续优化。（原始评级：大部分覆盖）

**N84**

Sun Sun

**O84**

2026-10-09T00:00:00

**P84**

进行中

### Row 85

**A85**

M4

**B85**

M4.1

**C85**

M4.1-A04

**D85**

防重复和静默覆盖

**E85**

完成“防重复和静默覆盖”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**F85**

稳定导入流程及错误报告

**G85**

不重复，错误可定位，不静默覆盖真实数据

**H85**

Projects表全量导入(绿色+白色里程碑)已实现。

**I85**

v10 Tab3更新。

**J85**

部分覆盖

**K85**

正确

**L85**

增量导入机制未建立。

**M85**

考虑增量导入。（原始评级：大部分覆盖）

**N85**

Sun Sun

**O85**

2026-10-16T00:00:00

**P85**

进行中

### Row 86

**A86**

M4

**B86**

M4.1

**C86**

M4.1-A05

**D86**

显示错误

**E86**

完成“显示错误”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**F86**

稳定导入流程及错误报告

**G86**

不重复，错误可定位，不静默覆盖真实数据

**H86**

SyncAutoPM支持多次运行(幂等性)。

**I86**

batch去重+PID匹配。

**J86**

部分覆盖

**K86**

正确

**L86**

日志和回退能力有限。

**M86**

增强日志和回退。（原始评级：大部分覆盖）

**N86**

Sun Sun

**O86**

2026-10-16T00:00:00

**P86**

进行中

### Row 87

**A87**

M4

**B87**

M4.1

**C87**

M4.1-A06

**D87**

支持修正和回退

**E87**

完成“支持修正和回退”，使“数据导入与初始化自动化”能够按统一规则执行、检查并留下可验证结果。

**F87**

稳定导入流程及错误报告

**G87**

不重复，错误可定位，不静默覆盖真实数据

**H87**

CSV导入通过AutoPM-13 Schedule Import。

**I87**

Automation AutoPM-13(ON)。

**J87**

部分覆盖

**K87**

需要修正

**L87**

CSV格式校验有限。

**M87**

增强CSV校验。

**N87**

Sun Sun

**O87**

2026-10-23T00:00:00

**P87**

未开始

### Row 88

**A88**

M4

**B88**

M4.2

**C88**

M4.2-A01

**D88**

计算到期、逾期、Next Milestone和偏差

**E88**

完成“计算到期、逾期、Next Milestone和偏差”，使“状态与异常计算”能够按统一规则执行、检查并留下可验证结果。

**F88**

计算规则及可解释结果

**G88**

规则与业务定义一致，异常边界通过测试，不无依据覆盖

**H88**

Overdue公式(IS_BEFORE(Due Date, TODAY()) AND Completed By = BLANK))已在诊断中使用。

**I88**

diagnose_overdue.py公式。

**J88**

部分覆盖

**K88**

需要修正

**L88**

Next Milestone/偏差计算不存在；计算依据未展示。

**M88**

增加自动计算字段。

**N88**

Sun Sun

**O88**

2026-09-25T00:00:00

**P88**

进行中

### Row 89

**A89**

M4

**B89**

M4.2

**C89**

M4.2-A02

**D89**

识别缺失与冲突

**E89**

完成“识别缺失与冲突”，使“状态与异常计算”能够按统一规则执行、检查并留下可验证结果。

**F89**

计算规则及可解释结果

**G89**

规则与业务定义一致，异常边界通过测试，不无依据覆盖

**H89**

缺失和冲突在诊断脚本中可检测。

**I89**

diagnose脚本。

**J89**

部分覆盖

**K89**

需要修正

**L89**

未自动化为系统字段；仅脚本临时检查。

**M89**

建立系统级自动检测。

**N89**

Sun Sun

**O89**

2026-10-09T00:00:00

**P89**

未开始

### Row 90

**A90**

M4

**B90**

M4.2

**C90**

M4.2-A03

**D90**

展示依据并支持授权确认

**E90**

完成“展示依据并支持授权确认”，使“状态与异常计算”能够按统一规则执行、检查并留下可验证结果。

**F90**

计算规则及可解释结果

**G90**

规则与业务定义一致，异常边界通过测试，不无依据覆盖

**H90**

无。

**I90**

无。

**J90**

未覆盖

**K90**

资料不足

**L90**

偏差计算缺失。

**M90**

建立偏差计算。

**N90**

Sun Sun

**O90**

2026-10-23T00:00:00

**P90**

未开始

### Row 91

**A91**

M4

**B91**

M4.3

**C91**

M4.3-A01

**D91**

建立到期、逾期、缺失和关键Delay提醒

**E91**

完成“建立到期、逾期、缺失和关键Delay提醒”，使“提醒与升级”能够按统一规则执行、检查并留下可验证结果。

**F91**

分级提醒和升级机制

**G91**

对象正确，已完成停止，重复受控，关键事项升级

**H91**

AutoPM-09 Daily Task Reminder(ON)。

**I91**

Automation清单。

**J91**

部分覆盖

**K91**

需要修正

**L91**

重复提醒控制缺失；响应和升级记录不存在。

**M91**

增强提醒控制。

**N91**

Sun Sun

**O91**

2026-09-25T00:00:00

**P91**

进行中

### Row 92

**A92**

M4

**B92**

M4.3

**C92**

M4.3-A02

**D92**

建立去重、停止、升级及响应记录

**E92**

完成“建立去重、停止、升级及响应记录”，使“提醒与升级”能够按统一规则执行、检查并留下可验证结果。

**F92**

分级提醒和升级机制

**G92**

对象正确，已完成停止，重复受控，关键事项升级

**H92**

无升级机制。

**I92**

无。

**J92**

未覆盖

**K92**

资料不足

**L92**

升级流程完全缺失。

**M92**

建立升级流程。

**N92**

Sun Sun

**O92**

2026-10-09T00:00:00

**P92**

未开始

### Row 93

**A93**

M4

**B93**

M4.4

**C93**

M4.4-A01

**D93**

汇总状态、变化、风险、延误、行动和决定

**E93**

完成“汇总状态、变化、风险、延误、行动和决定”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**F93**

可确认、可追溯的周报草稿

**G93**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**H93**

AutoPM-08 Weekly Report(ON)生成周报。

**I93**

Automation清单。

**J93**

部分覆盖

**K93**

需要修正

**L93**

周报内容有限；缺少管理报告。

**M93**

增强报告内容。

**N93**

Sun Sun

**O93**

2026-10-09T00:00:00

**P93**

进行中

### Row 94

**A94**

M4

**B94**

M4.4

**C94**

M4.4-A02

**D94**

生成周报

**E94**

完成“生成周报”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**F94**

可确认、可追溯的周报草稿

**G94**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**H94**

无管理报告。

**I94**

无。

**J94**

未覆盖

**K94**

资料不足

**L94**

管理报告缺失。

**M94**

建立管理报告。

**N94**

Sun Sun

**O94**

2026-09-04T00:00:00

**P94**

已完成

### Row 95

**A95**

M4

**B95**

M4.4

**C95**

M4.4-A03

**D95**

标记缺失待确认

**E95**

完成“标记缺失待确认”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**F95**

可确认、可追溯的周报草稿

**G95**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**H95**

无缺失信息透明展示。

**I95**

无。

**J95**

未覆盖

**K95**

资料不足

**L95**

缺失信息不透明。

**M95**

增加缺失信息展示。

**N95**

Sun Sun

**O95**

2026-10-16T00:00:00

**P95**

未开始

### Row 96

**A96**

M4

**B96**

M4.4

**C96**

M4.4-A04

**D96**

保留来源、下钻、确认和导出

**E96**

完成“保留来源、下钻、确认和导出”，使“报告生成”能够按统一规则执行、检查并留下可验证结果。

**F96**

可确认、可追溯的周报草稿

**G96**

报告来自统一数据，缺失透明，可下钻，发布前人工确认

**H96**

报告发布前无确认步骤。

**I96**

无。

**J96**

未覆盖

**K96**

资料不足

**L96**

发布前确认缺失。

**M96**

增加发布前确认。

**N96**

Sun Sun

**O96**

2026-10-23T00:00:00

**P96**

未开始

### Row 97

**A97**

M4

**B97**

M4.5

**C97**

M4.5-A01

**D97**

确认必要数据范围

**E97**

完成“确认必要数据范围”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**F97**

PMO读取验证及映射对账结果

**G97**

必要主数据稳定匹配，冲突和失败不静默处理

**H97**

PMO Tracker通过SyncAutoPM读取(3008条Projects)。

**I97**

SyncAutoPM v10。

**J97**

部分覆盖

**K97**

正确

**L97**

Programme匹配通过文本(非linked record)。

**M97**

增强匹配方式。（原始评级：大部分覆盖）

**N97**

Sun Sun

**O97**

2026-09-18T00:00:00

**P97**

进行中

### Row 98

**A98**

M4

**B98**

M4.5

**C98**

M4.5-A02

**D98**

建立Programme、Project、SKU和目标日期映射

**E98**

完成“建立Programme、Project、SKU和目标日期映射”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**F98**

PMO读取验证及映射对账结果

**G98**

必要主数据稳定匹配，冲突和失败不静默处理

**H98**

SKU匹配不在AutoPM中。

**I98**

无SKU表。

**J98**

未覆盖

**K98**

资料不足

**L98**

SKU匹配完全缺失。

**M98**

建立SKU匹配。

**N98**

Sun Sun

**O98**

2026-11-06T00:00:00

**P98**

未开始

### Row 99

**A99**

M4

**B99**

M4.5

**C99**

M4.5-A03

**D99**

验证读取

**E99**

完成“验证读取”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**F99**

PMO读取验证及映射对账结果

**G99**

必要主数据稳定匹配，冲突和失败不静默处理

**H99**

目标日期通过里程碑字段读取。

**I99**

Projects表20+日期字段。

**J99**

部分覆盖

**K99**

需要修正

**L99**

部分里程碑日期为空。

**M99**

补全日期数据。

**N99**

Sun Sun

**O99**

2026-10-09T00:00:00

**P99**

未开始

### Row 100

**A100**

M4

**B100**

M4.5

**C100**

M4.5-A04

**D100**

识别变化冲突

**E100**

完成“识别变化冲突”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**F100**

PMO读取验证及映射对账结果

**G100**

必要主数据稳定匹配，冲突和失败不静默处理

**H100**

同步失败通过日志发现。

**I100**

SyncAutoPM日志输出。

**J100**

部分覆盖

**K100**

需要修正

**L100**

冲突检测有限；无自动告警。

**M100**

增强冲突检测。

**N100**

Sun Sun

**O100**

2026-10-23T00:00:00

**P100**

未开始

### Row 101

**A101**

M4

**B101**

M4.5

**C101**

M4.5-A05

**D101**

记录同步并对账

**E101**

完成“记录同步并对账”，使“PMO主数据连接”能够按统一规则执行、检查并留下可验证结果。

**F101**

PMO读取验证及映射对账结果

**G101**

必要主数据稳定匹配，冲突和失败不静默处理

**H101**

部分。

**I101**

SyncAutoPM。

**J101**

部分覆盖

**K101**

需要修正

**L101**

同步失败恢复机制不完善。

**M101**

增强失败恢复。

**N101**

Sun Sun

**O101**

2026-09-25T00:00:00

**P101**

未开始

### Row 102

**A102**

M4

**B102**

M4.6

**C102**

M4.6-A01

**D102**

定义角色、项目、查看、编辑、确认、审批、导出和敏感字段权限

**E102**

完成“定义角色、项目、查看、编辑、确认、审批、导出和敏感字段权限”，使“权限与审计”能够按统一规则执行、检查并留下可验证结果。

**F102**

Phase 1权限模型及审计记录

**G102**

访问和关键操作受控，越权经过测试，操作可追溯

**H102**

Airtable原生权限(Workspace级别)。

**I102**

Airtable权限模型。

**J102**

部分覆盖

**K102**

需要修正

**L102**

字段级权限控制不存在(Airtable限制)。

**M102**

评估权限需求。

**N102**

Sun Sun

**O102**

2026-10-30T00:00:00

**P102**

未开始

### Row 103

**A103**

M4

**B103**

M4.6

**C103**

M4.6-A02

**D103**

记录变更

**E103**

完成“记录变更”，使“权限与审计”能够按统一规则执行、检查并留下可验证结果。

**F103**

Phase 1权限模型及审计记录

**G103**

访问和关键操作受控，越权经过测试，操作可追溯

**H103**

Airtable审计日志(平台级)。

**I103**

Airtable Enterprise功能。

**J103**

部分覆盖

**K103**

需要修正

**L103**

自定义审计记录不存在。

**M103**

建立自定义审计。

**N103**

Sun Sun

**O103**

2026-10-30T00:00:00

**P103**

未开始

### Row 104

**A104**

M4

**B104**

M4.6

**C104**

M4.6-A03

**D104**

测试越权

**E104**

完成“测试越权”，使“权限与审计”能够按统一规则执行、检查并留下可验证结果。

**F104**

Phase 1权限模型及审计记录

**G104**

访问和关键操作受控，越权经过测试，操作可追溯

**H104**

无。

**I104**

无。

**J104**

未覆盖

**K104**

资料不足

**L104**

导出控制缺失。

**M104**

评估导出控制。

**N104**

Sun Sun

**O104**

2026-11-13T00:00:00

**P104**

未开始

### Row 105

**A105**

M4

**B105**

M4.7

**C105**

M4.7-A01

**D105**

记录自动化和同步结果

**E105**

完成“记录自动化和同步结果”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**F105**

运行监控及失败处理机制

**G105**

失败及时发现，重试安全，故障有责任和回退

**H105**

SyncAutoPM运行时输出日志。

**I105**

控制台输出。

**J105**

部分覆盖

**K105**

需要修正

**L105**

无持久化监控；无告警。

**M105**

建立持久化监控。

**N105**

Sun Sun

**O105**

2026-10-09T00:00:00

**P105**

未开始

### Row 106

**A106**

M4

**B106**

M4.7

**C106**

M4.7-A02

**D106**

监控异常

**E106**

完成“监控异常”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**F106**

运行监控及失败处理机制

**G106**

失败及时发现，重试安全，故障有责任和回退

**H106**

无自动告警。

**I106**

无。

**J106**

未覆盖

**K106**

资料不足

**L106**

失败告警缺失。

**M106**

建立告警机制。

**N106**

Sun Sun

**O106**

2026-10-16T00:00:00

**P106**

未开始

### Row 107

**A107**

M4

**B107**

M4.7

**C107**

M4.7-A03

**D107**

告警并分配Owner

**E107**

完成“告警并分配Owner”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**F107**

运行监控及失败处理机制

**G107**

失败及时发现，重试安全，故障有责任和回退

**H107**

无。

**I107**

无。

**J107**

未覆盖

**K107**

资料不足

**L107**

责任分配缺失。

**M107**

建立责任分配。

**N107**

Sun Sun

**O107**

2026-10-16T00:00:00

**P107**

未开始

### Row 108

**A108**

M4

**B108**

M4.7

**C108**

M4.7-A04

**D108**

支持幂等重试

**E108**

完成“支持幂等重试”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**F108**

运行监控及失败处理机制

**G108**

失败及时发现，重试安全，故障有责任和回退

**H108**

无安全重试。

**I108**

无。

**J108**

未覆盖

**K108**

资料不足

**L108**

重试机制缺失。

**M108**

建立重试机制。

**N108**

Sun Sun

**O108**

2026-09-25T00:00:00

**P108**

进行中

### Row 109

**A109**

M4

**B109**

M4.7

**C109**

M4.7-A05

**D109**

防数据污染

**E109**

完成“防数据污染”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**F109**

运行监控及失败处理机制

**G109**

失败及时发现，重试安全，故障有责任和回退

**H109**

无回退。

**I109**

无。

**J109**

未覆盖

**K109**

资料不足

**L109**

回退能力缺失。

**M109**

建立回退能力。

**N109**

Sun Sun

**O109**

2026-10-16T00:00:00

**P109**

未开始

### Row 110

**A110**

M4

**B110**

M4.7

**C110**

M4.7-A06

**D110**

建立回退

**E110**

完成“建立回退”，使“运行监控与失败恢复”能够按统一规则执行、检查并留下可验证结果。

**F110**

运行监控及失败处理机制

**G110**

失败及时发现，重试安全，故障有责任和回退

**H110**

无。

**I110**

无。

**J110**

未覆盖

**K110**

资料不足

**L110**

运行报告缺失。

**M110**

建立运行报告。

**N110**

Sun Sun

**O110**

2026-10-23T00:00:00

**P110**

未开始

### Row 111

**A111**

M5

**B111**

M5.1

**C111**

M5.1-A01

**D111**

确认试点目标、团队、负责人、项目清单、选择标准、参与角色、使用承诺及启动暂停退出条件

**E111**

完成“确认试点目标、团队、负责人、项目清单、选择标准、参与角色、使用承诺及启动暂停退出条件”，使“Pilot范围确认”能够按统一规则执行、检查并留下可验证结果。

**F111**

Pilot范围说明及团队项目清单

**G111**

团队、项目、角色和目标确认，未确认数量周期保持TBD

**H111**

Pilot未正式启动；全部项目已导入但非试点模式。

**I111**

3008条全量导入。

**J111**

未覆盖

**K111**

资料不足

**L111**

无试点范围确认文档。

**M111**

定义试点范围和启动条件。

**N111**

Sun Sun

**O111**

2026-09-04T00:00:00

**P111**

未开始

### Row 112

**A112**

M5

**B112**

M5.2

**C112**

M5.2-A01

**D112**

定义执行、项目、职能、管理、Data Owner和平台支持责任

**E112**

完成“定义执行、项目、职能、管理、Data Owner和平台支持责任”，使“角色与责任”能够按统一规则执行、检查并留下可验证结果。

**F112**

Pilot角色责任矩阵

**G112**

每类数据和行动有责任，PM不代替所有人维护

**H112**

Sun Sun为唯一实际维护者；角色分工未定义。

**I112**

实际操作观察。

**J112**

未覆盖

**K112**

资料不足

**L112**

角色与责任未正式定义。

**M112**

定义Pilot角色和责任。

**N112**

Sun Sun

**O112**

2026-09-11T00:00:00

**P112**

未开始

### Row 113

**A113**

M5

**B113**

M5.3

**C113**

M5.3-A01

**D113**

定义必须维护的信息、更新频率、异常Action升级关闭规则、人工确认和最低证据

**E113**

完成“定义必须维护的信息、更新频率、异常Action升级关闭规则、人工确认和最低证据”，使“使用规则”能够按统一规则执行、检查并留下可验证结果。

**F113**

Pilot使用规则

**G113**

何时在哪里更新什么清楚，关键事实保留人工责任

**H113**

无使用规则文档。

**I113**

无。

**J113**

未覆盖

**K113**

资料不足

**L113**

使用规则完全缺失。

**M113**

编写使用规则。

**N113**

Sun Sun

**O113**

2026-09-18T00:00:00

**P113**

未开始

### Row 114

**A114**

M5

**B114**

M5.4

**C114**

M5.4-A01

**D114**

明确唯一维护位置、旧工具范围、读取写入链接同步方向、冲突失败、停止条件和回退方案

**E114**

完成“明确唯一维护位置、旧工具范围、读取写入链接同步方向、冲突失败、停止条件和回退方案”，使“双系统过渡”能够按统一规则执行、检查并留下可验证结果。

**F114**

双系统过渡方案

**G114**

无规则重复维护被消除，切换和回退不丢数据

**H114**

Tracker+Airtable双系统运行中；同步通过SyncAutoPM。

**I114**

SyncAutoPM v10。

**J114**

部分覆盖

**K114**

需要修正

**L114**

唯一维护位置/冲突处理/退出方式未定义。

**M114**

定义双系统过渡规则。

**N114**

Sun Sun

**O114**

2026-09-25T00:00:00

**P114**

进行中

### Row 115

**A115**

M5

**B115**

M5.5

**C115**

M5.5-A01

**D115**

使用真实项目完成任务更新、状态异常维护、Action确认、管理审查和Decision

**E115**

完成“使用真实项目完成任务更新、状态异常维护、Action确认、管理审查和Decision”，使“角色上手”能够按统一规则执行、检查并留下可验证结果。

**F115**

角色上手记录及首轮问题清单

**G115**

关键角色在真实项目完成核心动作，不以登录培训作为完成

**H115**

Sun Sun已在真实项目中使用。

**I115**

日常操作。

**J115**

部分覆盖

**K115**

需要修正

**L115**

其他关键角色未上手；理解偏差未记录。

**M115**

扩展到更多角色。

**N115**

Sun Sun

**O115**

2026-09-30T00:00:00

**P115**

未开始

### Row 116

**A116**

M5

**B116**

M5.5

**C116**

M5.5-A02

**D116**

记录问题和理解偏差

**E116**

完成“记录问题和理解偏差”，使“角色上手”能够按统一规则执行、检查并留下可验证结果。

**F116**

角色上手记录及首轮问题清单

**G116**

关键角色在真实项目完成核心动作，不以登录培训作为完成

**H116**

无。

**I116**

无。

**J116**

未覆盖

**K116**

资料不足

**L116**

使用问题记录缺失。

**M116**

建立问题记录。

**N116**

Sun Sun

**O116**

2026-10-09T00:00:00

**P116**

未开始

### Row 117

**A117**

M5

**B117**

M5.6

**C117**

M5.6-A01

**D117**

按规则更新

**E117**

完成“按规则更新”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**F117**

可重复周度运行机制

**G117**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**H117**

周报每周五自动发送(AutoPM-08)。

**I117**

Automation清单。

**J117**

部分覆盖

**K117**

需要修正

**L117**

周度审查循环未结构化。

**M117**

结构化周度审查。

**N117**

Sun Sun

**O117**

2026-10-09T00:00:00

**P117**

已完成

### Row 118

**A118**

M5

**B118**

M5.6

**C118**

M5.6-A02

**D118**

检查数据

**E118**

完成“检查数据”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**F118**

可重复周度运行机制

**G118**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**H118**

无。

**I118**

无。

**J118**

未覆盖

**K118**

资料不足

**L118**

检查/审查/决定/行动循环缺失。

**M118**

建立周度循环。

**N118**

Sun Sun

**O118**

2026-09-30T00:00:00

**P118**

未开始

### Row 119

**A119**

M5

**B119**

M5.6

**C119**

M5.6-A03

**D119**

生成异常和周报

**E119**

完成“生成异常和周报”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**F119**

可重复周度运行机制

**G119**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**H119**

无。

**I119**

无。

**J119**

未覆盖

**K119**

资料不足

**L119**

结果验证循环缺失。

**M119**

建立验证循环。

**N119**

Sun Sun

**O119**

2026-10-30T00:00:00

**P119**

进行中

### Row 120

**A120**

M5

**B120**

M5.6

**C120**

M5.6-A04

**D120**

开展周度审查

**E120**

完成“开展周度审查”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**F120**

可重复周度运行机制

**G120**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**H120**

无。

**I120**

无。

**J120**

未覆盖

**K120**

资料不足

**L120**

行动跟踪缺失。

**M120**

建立行动跟踪。

**N120**

Sun Sun

**O120**

2026-10-16T00:00:00

**P120**

未开始

### Row 121

**A121**

M5

**B121**

M5.6

**C121**

M5.6-A05

**D121**

回写决定和Action

**E121**

完成“回写决定和Action”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**F121**

可重复周度运行机制

**G121**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**H121**

无。

**I121**

无。

**J121**

未覆盖

**K121**

资料不足

**L121**

决策记录缺失。

**M121**

建立决策记录。

**N121**

Sun Sun

**O121**

2026-10-23T00:00:00

**P121**

未开始

### Row 122

**A122**

M5

**B122**

M5.6

**C122**

M5.6-A06

**D122**

下周期验证结果

**E122**

完成“下周期验证结果”，使“周度运行节奏”能够按统一规则执行、检查并留下可验证结果。

**F122**

可重复周度运行机制

**G122**

真实项目持续更新，周会使用AutoPM，行动下周期验证

**H122**

无。

**I122**

无。

**J122**

未覆盖

**K122**

资料不足

**L122**

循环记录缺失。

**M122**

建立循环记录。

**N122**

Sun Sun

**O122**

2026-10-23T00:00:00

**P122**

未开始

### Row 123

**A123**

M5

**B123**

M5.7

**C123**

M5.7-A01

**D123**

建立反馈入口

**E123**

完成“建立反馈入口”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**F123**

问题改进清单及支持修复节奏

**G123**

关键问题有分类、影响、责任和状态，修复经用户验证

**H123**

问题通过对话方式处理(非系统化)。

**I123**

日常沟通。

**J123**

部分覆盖

**K123**

需要修正

**L123**

问题收集未系统化。

**M123**

系统化问题收集。

**N123**

Sun Sun

**O123**

2026-09-25T00:00:00

**P123**

未开始

### Row 124

**A124**

M5

**B124**

M5.7

**C124**

M5.7-A02

**D124**

分类问题

**E124**

完成“分类问题”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**F124**

问题改进清单及支持修复节奏

**G124**

关键问题有分类、影响、责任和状态，修复经用户验证

**H124**

无。

**I124**

无。

**J124**

未覆盖

**K124**

资料不足

**L124**

问题分类排序缺失。

**M124**

建立问题分类。

**N124**

Sun Sun

**O124**

2026-10-09T00:00:00

**P124**

未开始

### Row 125

**A125**

M5

**B125**

M5.7

**C125**

M5.7-A03

**D125**

评估影响优先级

**E125**

完成“评估影响优先级”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**F125**

问题改进清单及支持修复节奏

**G125**

关键问题有分类、影响、责任和状态，修复经用户验证

**H125**

无。

**I125**

无。

**J125**

未覆盖

**K125**

资料不足

**L125**

优先级排序缺失。

**M125**

建立优先级。

**N125**

Sun Sun

**O125**

2026-10-09T00:00:00

**P125**

未开始

### Row 126

**A126**

M5

**B126**

M5.7

**C126**

M5.7-A04

**D126**

分配Owner

**E126**

完成“分配Owner”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**F126**

问题改进清单及支持修复节奏

**G126**

关键问题有分类、影响、责任和状态，修复经用户验证

**H126**

问题修复通过脚本和手动方式。

**I126**

diagnose脚本。

**J126**

部分覆盖

**K126**

需要修正

**L126**

修复流程不系统。

**M126**

系统化修复流程。

**N126**

Sun Sun

**O126**

2026-10-16T00:00:00

**P126**

未开始

### Row 127

**A127**

M5

**B127**

M5.7

**C127**

M5.7-A05

**D127**

验证修复

**E127**

完成“验证修复”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**F127**

问题改进清单及支持修复节奏

**G127**

关键问题有分类、影响、责任和状态，修复经用户验证

**H127**

无。

**I127**

无。

**J127**

未覆盖

**K127**

资料不足

**L127**

验证缺失。

**M127**

建立验证。

**N127**

Sun Sun

**O127**

2026-10-16T00:00:00

**P127**

未开始

### Row 128

**A128**

M5

**B128**

M5.7

**C128**

M5.7-A06

**D128**

转化重复反馈

**E128**

完成“转化重复反馈”，使“用户支持与问题处理”能够按统一规则执行、检查并留下可验证结果。

**F128**

问题改进清单及支持修复节奏

**G128**

关键问题有分类、影响、责任和状态，修复经用户验证

**H128**

无。

**I128**

无。

**J128**

未覆盖

**K128**

资料不足

**L128**

系统性改进缺失。

**M128**

建立系统性改进。

**N128**

Sun Sun

**O128**

2026-11-13T00:00:00

**P128**

未开始

### Row 129

**A129**

M6

**B129**

M6.1

**C129**

M6.1-A01

**D129**

定义人工追踪、周报汇总、数据质量、Task/Issue/Action/Delay基线

**E129**

完成“定义人工追踪、周报汇总、数据质量、Task/Issue/Action/Delay基线”，使“基线定义”能够按统一规则执行、检查并留下可验证结果。

**F129**

指标定义及Pilot前基线

**G129**

定义和证据清楚，无基线不宣称改善

**H129**

无正式基线记录。

**I129**

无。

**J129**

未覆盖

**K129**

资料不足

**L129**

基线定义完全缺失。

**M129**

记录当前工作方式基线。

**N129**

Sun Sun

**O129**

2026-09-11T00:00:00

**P129**

未开始

### Row 130

**A130**

M6

**B130**

M6.1

**C130**

M6.1-A02

**D130**

定义算法来源Owner周期并在Pilot前记录

**E130**

完成“定义算法来源Owner周期并在Pilot前记录”，使“基线定义”能够按统一规则执行、检查并留下可验证结果。

**F130**

指标定义及Pilot前基线

**G130**

定义和证据清楚，无基线不宣称改善

**H130**

无。

**I130**

无。

**J130**

未覆盖

**K130**

资料不足

**L130**

基线指标缺失。

**M130**

定义基线指标。

**N130**

Sun Sun

**O130**

2026-09-11T00:00:00

**P130**

未开始

### Row 131

**A131**

M6

**B131**

M6.2

**C131**

M6.2-A01

**D131**

记录活跃项目用户、频率及时性、周度审查、关键动作、中断退出和双系统维护

**E131**

完成“记录活跃项目用户、频率及时性、周度审查、关键动作、中断退出和双系统维护”，使“使用与采用证据”能够按统一规则执行、检查并留下可验证结果。

**F131**

Pilot使用证据包

**G131**

区分登录、一次录入和持续使用，负担和中断如实记录

**H131**

Airtable可记录登录和操作。

**I131**

Airtable平台功能。

**J131**

部分覆盖

**K131**

需要修正

**L131**

持续使用证据未收集。

**M131**

收集使用证据。

**N131**

Sun Sun

**O131**

2026-10-09T00:00:00

**P131**

未开始

### Row 132

**A132**

M6

**B132**

M6.3

**C132**

M6.3-A01

**D132**

记录字段、关系、Owner、Due、状态完整性，以及重复、冲突、同步失败、修正和关闭

**E132**

完成“记录字段、关系、Owner、Due、状态完整性，以及重复、冲突、同步失败、修正和关闭”，使“数据质量证据”能够按统一规则执行、检查并留下可验证结果。

**F132**

数据质量证据包

**G132**

指标可重复计算，问题可追溯，管理可用性有结论

**H132**

数据质量诊断脚本可运行。

**I132**

diagnose脚本。

**J132**

部分覆盖

**K132**

需要修正

**L132**

可重复指标未定义。

**M132**

定义数据质量指标。

**N132**

Sun Sun

**O132**

2026-10-09T00:00:00

**P132**

进行中

### Row 133

**A133**

M6

**B133**

M6.4

**C133**

M6.4-A01

**D133**

记录Task按期逾期、异常Action覆盖、责任日期关闭、Delay影响恢复、Issue验证关闭和Decision转Action

**E133**

完成“记录Task按期逾期、异常Action覆盖、责任日期关闭、Delay影响恢复、Issue验证关闭和Decision转Action”，使“执行闭环证据”能够按统一规则执行、检查并留下可验证结果。

**F133**

执行闭环证据包

**G133**

能识别闭环中断，区分Action完成和Issue关闭

**H133**

无闭环证据。

**I133**

无。

**J133**

未覆盖

**K133**

资料不足

**L133**

闭环证据完全缺失。

**M133**

建立闭环证据收集。

**N133**

Sun Sun

**O133**

2026-11-06T00:00:00

**P133**

未开始

### Row 134

**A134**

M6

**B134**

M6.5

**C134**

M6.5-A01

**D134**

比较查找、周报、追问、重复维护、问题发现升级关闭

**E134**

完成“比较查找、周报、追问、重复维护、问题发现升级关闭”，使“效率与业务结果”能够按统一规则执行、检查并留下可验证结果。

**F134**

Pilot前后比较及价值结论

**G134**

基于基线，同时呈现改善、未改善、负面影响和数据不足

**H134**

无。

**I134**

无。

**J134**

未覆盖

**K134**

资料不足

**L134**

效率对比缺失。

**M134**

设计效率对比。

**N134**

Sun Sun

**O134**

2026-11-13T00:00:00

**P134**

未开始

### Row 135

**A135**

M6

**B135**

M6.5

**C135**

M6.5-A02

**D135**

记录决定结果、新增工作和负面影响

**E135**

完成“记录决定结果、新增工作和负面影响”，使“效率与业务结果”能够按统一规则执行、检查并留下可验证结果。

**F135**

Pilot前后比较及价值结论

**G135**

基于基线，同时呈现改善、未改善、负面影响和数据不足

**H135**

无。

**I135**

无。

**J135**

未覆盖

**K135**

资料不足

**L135**

新增工作评估缺失。

**M135**

评估新增工作。

**N135**

Sun Sun

**O135**

2026-11-13T00:00:00

**P135**

未开始

### Row 136

**A136**

M6

**B136**

M6.5

**C136**

M6.5-A03

**D136**

形成结论

**E136**

完成“形成结论”，使“效率与业务结果”能够按统一规则执行、检查并留下可验证结果。

**F136**

Pilot前后比较及价值结论

**G136**

基于基线，同时呈现改善、未改善、负面影响和数据不足

**H136**

无。

**I136**

无。

**J136**

未覆盖

**K136**

资料不足

**L136**

业务结果衡量缺失。

**M136**

衡量业务结果。

**N136**

Sun Sun

**O136**

2026-09-25T00:00:00

**P136**

未开始

### Row 137

**A137**

M6

**B137**

M6.6

**C137**

M6.6-A01

**D137**

评估性能容量、中国访问、权限审计、自动化集成、导出迁移回退、支持许可成本及技术路线

**E137**

完成“评估性能容量、中国访问、权限审计、自动化集成、导出迁移回退、支持许可成本及技术路线”，使“平台能力评估”能够按统一规则执行、检查并留下可验证结果。

**F137**

平台评估及Phase 2技术路线建议

**G137**

基于真实使用，事实限制建议分开，不预设最终平台

**H137**

Airtable当前可支持3008+记录。

**I137**

API验证。

**J137**

部分覆盖

**K137**

需要修正

**L137**

性能/集成/迁移/成本评估未做。

**M137**

评估平台能力。

**N137**

Sun Sun

**O137**

2026-10-30T00:00:00

**P137**

未开始

### Row 138

**A138**

M6

**B138**

M6.7

**C138**

M6.7-A01

**D138**

汇总证据

**E138**

完成“汇总证据”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**F138**

Gate 1评审包、决策记录及Phase 2条件

**G138**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**H138**

无。

**I138**

无。

**J138**

未覆盖

**K138**

资料不足

**L138**

Gate决策完全缺失。

**M138**

准备Gate决策。

**N138**

Sun Sun

**O138**

2026-11-27T00:00:00

**P138**

未开始

### Row 139

**A139**

M6

**B139**

M6.7

**C139**

M6.7-A02

**D139**

评估成功条件

**E139**

完成“评估成功条件”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**F139**

Gate 1评审包、决策记录及Phase 2条件

**G139**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**H139**

无。

**I139**

无。

**J139**

未覆盖

**K139**

资料不足

**L139**

证据汇总缺失。

**M139**

汇总Phase 1证据。

**N139**

Sun Sun

**O139**

2026-09-11T00:00:00

**P139**

未开始

### Row 140

**A140**

M6

**B140**

M6.7

**C140**

M6.7-A03

**D140**

识别缺口风险

**E140**

完成“识别缺口风险”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**F140**

Gate 1评审包、决策记录及Phase 2条件

**G140**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**H140**

无。

**I140**

无。

**J140**

未覆盖

**K140**

资料不足

**L140**

成功条件评估缺失。

**M140**

评估成功条件。

**N140**

Sun Sun

**O140**

2026-09-25T00:00:00

**P140**

未开始

### Row 141

**A141**

M6

**B141**

M6.7

**C141**

M6.7-A04

**D141**

提出继续调整延长迁移停止建议

**E141**

完成“提出继续调整延长迁移停止建议”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**F141**

Gate 1评审包、决策记录及Phase 2条件

**G141**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**H141**

无。

**I141**

无。

**J141**

未覆盖

**K141**

资料不足

**L141**

决策选项缺失。

**M141**

准备决策选项。

**N141**

Sun Sun

**O141**

2026-09-25T00:00:00

**P141**

未开始

### Row 142

**A142**

M6

**B142**

M6.7

**C142**

M6.7-A05

**D142**

明确Phase 2条件和正式决定

**E142**

完成“明确Phase 2条件和正式决定”，使“Gate 1决策”能够按统一规则执行、检查并留下可验证结果。

**F142**

Gate 1评审包、决策记录及Phase 2条件

**G142**

决策由证据支持，未确认不转承诺，通过后才进入Phase 2

**H142**

无。

**I142**

无。

**J142**

未覆盖

**K142**

资料不足

**L142**

正式决策缺失。

**M142**

进行正式决策。

**N142**

Sun Sun+主管

**O142**

2026-11-27T00:00:00

**P142**

未开始
