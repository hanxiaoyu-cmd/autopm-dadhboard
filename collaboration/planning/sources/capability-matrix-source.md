# AutoPM_Function_Capability_Matrix_2026-08-30_v1.0

> 状态：持续修订的工作资料，非最终规格、非开发授权。历史状态和日期须结合最新审计复核。


来源：`AutoPM_Function_Capability_Matrix_2026-08-30_v1.0.xlsx`。逐工作表、逐非空行保留内容；列字母和行号对应原Excel。公式单元格同时记录公式和已有缓存值，未重新计算。图片、版式、条件格式不包含在文本提取中。

## Executive Overview

### Row 1

**A1**

AutoPM Core Problem, Goal & Capability Map

### Row 2

**A2**

用于管理层对齐、开发规划和团队任务分配；功能存在不等于真实业务价值已经验证。版本 v1.0 | 2026-08-30

### Row 4

**A4**

ONE-LINE POSITIONING

### Row 5

**A5**

AutoPM把项目数据、任务执行、问题决策和组织经验连接成一个持续运行的企业执行系统，并在此基础上让AI真正看见业务、理解问题和辅助行动。

### Row 8

**A8**

核心问题

**B8**

当前表现

**C8**

AutoPM目标

**D8**

可验证价值

**F8**

VALUE CREATION CHAIN

### Row 9

**A9**

事实分散

**B9**

Project/SKU/日期/Owner分散在Excel、邮件、Teams和专业系统

**C9**

建立统一执行数据模型与Source of Truth

**D9**

信息可查、可关联、可追溯

**F9**

1 CONNECT

**I9**

连接事实

### Row 10

**A10**

人工追踪

**B10**

状态依赖会议、邮件和PM反复催办

**C10**

用任务、提醒、依赖和证据驱动执行

**D10**

减少等待和重复沟通

**F10**

2 SEE

**I10**

看清状态

### Row 11

**A11**

问题不闭环

**B11**

Issue被汇报，但原因、行动、结果和验证没有连起来

**C11**

建立Exception & Decision Loop

**D11**

问题从发现走到验证关闭

**F11**

3 DRIVE

**I11**

推动执行

### Row 12

**A12**

经验流失

**B12**

项目结束或人员离开后，解决方案无法复用

**C12**

形成Execution Knowledge System

**D12**

经验成为可检索的企业资产

**F12**

4 CLOSE

**I12**

关闭异常

### Row 13

**A13**

汇报噪音

**B13**

大量时间用于收集、整理和解释状态

**C13**

自动生成共同Review视图

**D13**

减少周报、会议和邮件负担

**F13**

5 LEARN

**I13**

沉淀经验

### Row 14

**A14**

AI看不见业务

**B14**

数据、关系和结果未连接，AI只能做单点内容生成

**C14**

先连接数据，再训练智能能力

**D14**

AI能够识别风险并辅助行动

**F14**

6 ALIGN

**I14**

共同Review

### Row 15

**F15**

7 THINK

**I15**

AI辅助行动

### Row 17

**A17**

PHASE CONFIGURATION

### Row 18

**A18**

Phase 1 | XPT Pilot Validation

**C18**

Phase 2 | NPI Scale-up

**F18**

Phase 3 | Cross-functional Execution

**I18**

Phase 4 | Enterprise AI Intelligence

### Row 19

**A19**

可信数据＋单项目闭环

**C19**

标准模板＋团队运营＋PMO对齐

**F19**

跨部门流程＋Portfolio＋系统集成

**I19**

知识图谱＋预测＋Copilot/Agent

### Row 21

**A21**

证明一套真实项目可以持续运行

**C21**

证明能力可以复制而非依赖个人

**F21**

证明能够发现和改善系统性瓶颈

**I21**

证明AI能够可靠辅助判断和行动

### Row 24

**A24**

STOP LINE | 在Phase 1证据成立前，不进入AI预测、AI Agent、企业级大规模集成和与当前闭环无关的新功能。

## Function Matrix

### Row 1

**A1**

AutoPM Function & Capability Matrix

### Row 2

**A2**

横向为Phase，纵向为能力模块；每个Phase均拆成具体交付物和验收标准。数值门槛为建议值，必须经Sponsor确认后才成为承诺。

### Row 4

**A4**

能力分类

**B4**

功能模块

**C4**

要解决的问题

**D4**

Phase 1 | XPT Pilot Validation

**G4**

Phase 2 | NPI Scale-up

**I4**

Phase 3 | Cross-functional

**K4**

Phase 4 | Enterprise AI

**M4**

当前判断

**N4**

Owner / Evidence

### Row 5

**D5**

交付物

**E5**

验收标准

**F5**

Comment 8/31

**G5**

交付物

**H5**

验收标准

**I5**

交付物

**J5**

验收标准

**K5**

交付物

**L5**

验收标准

### Row 6

**A6**

1 数据基础

**B6**

业务对象模型

**C6**

项目、SKU、任务和Issue缺少统一关系

**D6**

建立Program→Project→SKU→Task→Issue→Action关系

**E6**

核心对象均有唯一ID；父子关系可追踪；抽查无孤立核心记录

**F6**

1.尝试把data部分的数据打通，建立清晰的者三个部分的关系

**G6**

统一NPI项目类型、Gate、字段词典和对象Owner

**H6**

新项目按同一模板创建；字段定义、Owner和更新频率获确认

**I6**

加入Function、Supplier、Resource、Dependency对象

**J6**

至少2条跨部门流程能从项目下钻到责任对象和依赖

**K6**

形成企业统一执行语义模型

**L6**

模型可供企业数据平台和AI服务调用，版本及变更可审计

**M6**

Partial / To Validate

### Row 7

**A7**

1 数据基础

**B7**

主数据与身份

**C7**

同一项目、SKU、人员存在多种名称和编码

**D7**

锁定Project ID、SKU、People、Factory主键及匹配规则

**E7**

导入重复项可识别；关键记录都能匹配到唯一主键

**F7**

需要检查现有的数据完整性，
比如工厂和工厂ID
人员信息的完整性和准确性
SKU与project ，program的关系

**G7**

与PMO主数据对齐Program、SKU、Owner和关键日期

**H7**

对账差异有清单、责任人和处理状态；不再复制同一主数据

**I7**

与批准的PLM/质量/供应链主数据建立映射

**J7**

跨系统对象可通过统一ID关联，差异自动暴露

**K7**

接入企业Master Data服务

**L7**

主数据变更自动同步且保留来源、时间和版本

**M7**

Partial / To Validate

### Row 8

**A8**

1 数据基础

**B8**

数据输入与系统连接

**C8**

现有数据需要人工搬运，且来源边界不清楚

**D8**

建立输入/输出矩阵；支持Excel/MPP导入和原系统链接

**E8**

每类数据标明Read/Write/Link/Import/TBD及系统Owner；导入可重复执行

**F8**

需要系统整理出来数据的输入和输出的关系表

**G8**

建立标准导入模板、批量更新和PMO同步流程

**H8**

导入失败有日志；重复导入不产生重复记录；同步频率明确

**I8**

按架构评审结果连接PLM、Jira、Power BI或Snowflake

**J8**

每个集成都有业务Owner、技术Owner、接口、频率和异常处理

**K8**

形成事件驱动的数据服务

**L8**

关键状态变化可自动进入统一数据层并触发下游流程

**M8**

Manual / Partial

### Row 9

**A9**

1 数据基础

**B9**

数据质量与治理

**C9**

字段多、重复、空值和更新时间不一致

**D9**

定义核心必填字段、Source、Owner、Last Updated和质量例外

**E9**

建议门槛：核心字段完整度≥95%；所有例外可定位到记录和Owner

**F9**

ok

**G9**

上线完整度、及时性、一致性和重复项巡检

**H9**

每周生成质量报告；问题有责任人、截止日和关闭状态

**I9**

增加跨系统对账、数据血缘和变更审计

**J9**

关键指标能追溯到原系统和字段；差异有处理闭环

**K9**

AI辅助发现和修复质量异常

**L9**

AI建议可解释、可回退；修复前需通过授权规则

**M9**

Partial

### Row 10

**A10**

2 项目控制塔

**B10**

Project Hub

**C10**

管理者难以快速找到项目事实和下一步

**D10**

单页展示项目、SKU、阶段、日期、Owner、Task、Issue和Action

**E10**

真实用户无需解释可在30秒内回答状态、原因、Owner和下一步

**F10**

ok

**G10**

形成标准NPI Project Hub和角色化视图

**H10**

同一数据支持PM、工程、质量和管理者视图，不重复维护

**I10**

加入跨部门依赖、供应商和资源视图

**J10**

项目页面可直接看到主要外部依赖及等待时长

**K10**

形成企业项目数字视图

**L10**

企业指标可下钻到项目、任务、Issue和原始证据

**M10**

Built / To Validate

### Row 11

**A11**

2 项目控制塔

**B11**

项目健康与状态

**C11**

项目状态依赖主观汇报，缺少事实支撑

**D11**

用日期、逾期Task、开放Issue和下一Action支撑健康判断

**E11**

每个At Risk/Delayed状态均可下钻到事实与Owner

**F11**

还需要详细定义At risk 的标准，最好能创建成自动化

**G11**

建立统一健康规则和趋势记录

**H11**

状态变化保留原因、时间和责任人；同类项目使用同一规则

**I11**

分析跨部门等待、资源和依赖对健康的影响

**J11**

健康视图能区分项目内部问题与系统性瓶颈

**K11**

AI预测健康变化

**L11**

预测显示证据、置信度和时间窗口，并经过人工验证

**M11**

Partial / To Validate

### Row 12

**A12**

2 项目控制塔

**B12**

Portfolio视图

**C12**

单项目可见，但无法发现组合层风险和冲突

**D12**

展示试点项目状态、关键日期、Issue和Owner分布

**E12**

试点范围内项目总数与明细一致；筛选后可下钻到记录

**F12**

还需要结合SKU, Project 以及program 这个方式显示项目状态

**G12**

形成NPI项目组合视图

**H12**

按Program、类型、Gate、Owner、月份查看并导出同一口径

**I12**

形成部门和跨部门Portfolio及瓶颈视图

**J12**

至少识别并验证1个跨项目重复瓶颈

**K12**

企业Portfolio Intelligence

**L12**

组合风险、资源和价值指标可预测并支持情景分析

**M12**

Built / To Validate

### Row 13

**A13**

3 工作流协调

**B13**

Task & Action

**C13**

任务依赖邮件和个人记忆，责任与证据不完整

**D13**

建立Task/Action、Owner、Due、Status、Priority、Dependency、Evidence

**E13**

关键工作100%具备Owner和Due；完成项有状态和证据

**F13**

从周报导入的任务和状态还需要检查和确认

**G13**

按项目类型生成标准任务并支持批量维护

**H13**

建议门槛：≥80%新试点项目从批准模板生成核心任务

**I13**

支持跨部门任务、交接和依赖

**J13**

至少2条跨部门流程可以追踪等待方、等待时间和下一动作

**K13**

AI辅助安排、拆分和协调任务

**L13**

AI生成任务须人工确认；执行结果可追踪和撤销

**M13**

Built / To Validate

### Row 14

**A14**

3 工作流协调

**B14**

Milestone与模板

**C14**

不同项目计划颗粒度不一致，启动时反复重建

**D14**

锁定XPT/NPI基础Milestone和关键交付物

**E14**

每个试点项目有批准的里程碑、计划日期和Owner

**F14**

需要再次检查导入的项目数据是否正确，需要再次检查自动创建的任务计划是否合理

**G14**

建立项目类型/Level对应的标准模板

**H14**

模板由业务专家确认；版本、适用范围和变更记录完整

**I14**

跨部门Milestone联动及关键路径

**J14**

依赖变化能反映到相关里程碑和责任团队

**K14**

AI根据项目特征推荐和优化模板

**L14**

推荐基于历史结果，显示依据并接受专家批准

**M14**

Partial

### Row 15

**A15**

3 工作流协调

**B15**

提醒、催办与升级

**C15**

PM花费大量时间追踪状态和催促Owner

**D15**

上线个人待办、逾期提醒和每周检查

**E15**

提醒指向正确Owner和记录；发送结果有日志；可关闭重复提醒

**F15**

缺少自动提醒

**G15**

定义分级催办和升级规则

**H15**

每条规则包含触发条件、接收人、响应时限和停止条件

**I15**

跨部门升级路径和SLA

**J15**

跨部门阻塞可自动进入正确Review或决策层级

**K15**

AI按风险动态选择提醒和升级

**L15**

AI不得越权；所有自动动作保留理由和审计日志

**M15**

Prototype / To Validate

### Row 16

**A16**

3 工作流协调

**B16**

完成证据与审计

**C16**

任务标记完成，但交付物和结果不可验证

**D16**

为关键Task定义Completion Evidence

**E16**

关键交付物可通过附件、链接或结果字段验证

**F16**

这个是当前的难点，无法创建合适的审批方式来确保交付物的准确性

**G16**

按任务类型定义证据标准和Reopen规则

**H16**

抽查完成项可复核；证据不足的任务不能进入最终关闭

**I16**

连接专业系统中的交付记录

**J16**

完成状态可追溯到批准记录或源系统对象

**K16**

AI检查证据完整性

**L16**

AI只提示异常，不在未授权情况下替代业务验收

**M16**

Needed

### Row 17

**A17**

4 异常与决策

**B17**

Issue识别与影响

**C17**

Issue描述不统一，业务影响难以比较

**D17**

记录Issue、Category、Severity、MP/Launch Impact、Owner和Target

**E17**

每个关键Issue均关联项目并说明影响、Owner和目标日期

**F17**

目前导入的这些issue 无法和autoPM里定义的完全匹配，需要和主管部门确认最终的标准格式

**G17**

统一Issue分类和影响口径

**H17**

同类Issue使用同一分类；高影响Issue自动进入Review

**I17**

跨项目、部门、工厂和供应商Issue关联

**J17**

可以统计重复Issue及影响范围，并验证至少1个系统性模式

**K17**

AI自动识别潜在Issue

**L17**

信号有来源、阈值和置信度；由业务Owner确认是否立项

**M17**

Built / To Validate

### Row 18

**A18**

4 异常与决策

**B18**

Root Cause与Recovery

**C18**

问题被描述，但根因和恢复行动没有形成闭环

**D18**

连接Root Cause、Recovery Action、Owner和Target Date

**E18**

关闭前必须有原因、行动和责任人；Action Done不等于Issue Closed

**F18**

还需要深度思考如何构把issue 构建成一个闭环的知识库

**G18**

建立根因分类和标准Recovery模板

**H18**

高频原因可统计；Recovery模板由业务专家验证

**I18**

分析重复根因和组织约束

**J18**

至少识别1个跨项目根因并形成管理行动

**K18**

AI推荐历史Recovery方案

**L18**

推荐显示类似案例、适用条件和历史结果

**M18**

Built / To Validate

### Row 19

**A19**

4 异常与决策

**B19**

Decision管理

**C19**

会议决定与后续执行脱节，无法追踪谁决定了什么

**D19**

记录Decision Needed、Decision Owner、Due和Decision Result

**E19**

每个待决事项有唯一责任人和日期；决定后自动生成Action

**F19**

TBD 无限制的增加功能会导致系统复杂，需要思考更好的方案

**G19**

建立Review决策清单和升级路径

**H19**

超时事项按规则升级；决定、理由和影响留痕

**I19**

跨部门决策和权限边界

**J19**

事项可路由到具备权限的角色并记录响应时间

**K19**

AI提供决策情景分析

**L19**

AI说明数据、假设和不确定性；最终责任仍属于Decision Owner

**M19**

Needed

### Row 20

**A20**

4 异常与决策

**B20**

验证关闭

**C20**

问题关闭缺少结果验证，容易重新发生

**D20**

增加Result、Verification、Verified By、Closed Date和Reopen

**E20**

至少一个真实Issue完成从发现到验证关闭的全链路证据

**F20**

Done

**G20**

定义不同Issue类型的关闭标准

**H20**

关闭项可抽查；不符合标准的记录自动回到Open/Rework

**I20**

跟踪Recovery对周期、质量和成本的实际影响

**J20**

关闭结果可以与原始影响基线比较

**K20**

AI监控复发和关闭有效性

**L20**

复发信号自动关联原Issue并提示人工复核

**M20**

Needed

### Row 21

**A21**

5 执行知识

**B21**

Lesson Learned

**C21**

问题解决后没有形成可复用经验

**D21**

Issue关闭时记录Lesson、适用条件和证据

**E21**

已验证关闭的关键Issue均有Lesson或明确Not Reusable原因

**F21**

还需要深度思考如何构把issue 构建成一个闭环的知识库

**G21**

建立标签、审核人和发布状态

**H21**

知识条目可检索；高影响Lesson由业务专家审核

**I21**

形成跨项目、工厂和供应商知识库

**J21**

新项目Review中实际引用历史经验并记录使用结果

**K21**

形成企业执行知识图谱

**L21**

知识与对象、时间、结果和证据关系可供AI查询

**M21**

Partial

### Row 22

**A22**

5 执行知识

**B22**

案例检索与复用

**C22**

新人和其他项目无法快速找到相似案例

**D22**

支持按Category、Project Type和关键词检索Issue

**E22**

用户可在限定步骤内找到并打开历史记录和证据

**F22**

issue 库还需要不断改善

**G22**

按场景推荐相似案例和模板

**H22**

推荐由用户确认相关性并记录是否采用

**I22**

跨部门复用案例并统计采用效果

**J22**

可量化被复用次数和复用后的结果

**K22**

AI自动匹配并解释相似案例

**L22**

匹配说明相似字段、差异和适用风险

**M22**

Needed

### Row 23

**A23**

5 执行知识

**B23**

模板资产

**C23**

每个项目都从零开始设计任务和流程

**D23**

建立基础Task Template并标注版本

**E23**

模板任务有Owner Function、Duration、Dependency和适用范围

**F23**

已经创建，还需要仔细检查并确保其正确

**G23**

形成经验证的项目类型模板库

**H23**

模板通过真实项目复盘；变更有版本和批准人

**I23**

建立跨部门流程模板

**J23**

模板覆盖交接、输入、输出和异常路径

**K23**

AI根据历史结果优化模板

**L23**

优化建议可比较新旧版本的实际结果

**M23**

Partial

### Row 24

**A24**

6 Review与沟通

**B24**

Weekly Summary

**C24**

周报依赖重复收集和人工拼接

**D24**

自动汇总状态变化、Top Issue、Overdue、Decision和Next Action

**E24**

试点项目周报从系统数据生成；不再二次录入核心状态

**F24**

进一步完善生成周报的格式和内容，确保内容准确，格式合理

**G24**

形成团队标准周报和角色化摘要

**H24**

同一数据生成PM、Function和Leadership版本，口径一致

**I24**

形成跨部门和Portfolio Review

**J24**

Review可以下钻到事实并把决定写回Action

**K24**

AI生成实时、个性化管理简报

**L24**

摘要引用来源；关键数字和结论经过自动校验

**M24**

Built / To Validate

### Row 25

**A25**

6 Review与沟通

**B25**

Management Review

**C25**

管理会议讨论状态多，形成决策和行动少

**D25**

建立变化、例外、待决事项和行动四区Review

**E25**

会议输出的Decision和Action在会后进入系统并有Owner/Due

**F25**

TBC 暂时不纳入到考虑范围内

**G25**

建立NPI组合Review节奏

**H25**

Review只聚焦例外和决策；会议前无需人工重建状态

**I25**

部门瓶颈和资源Review

**J25**

至少1个Portfolio问题形成跨部门管理行动

**K25**

企业执行驾驶舱

**L25**

领导指标可下钻、可解释并连接到行动结果

**M25**

Partial

### Row 26

**A26**

6 Review与沟通

**B26**

通知与行动回写

**C26**

邮件发送后不能确认是否形成行动

**D26**

状态邮件包含记录链接、Owner和Next Action

**E26**

发送有成功/失败日志；行动可直接回到对应记录

**F26**

TBC 暂时不纳入到考虑范围内

**G26**

按角色订阅并减少重复通知

**H26**

用户可配置频率；相同事项不会被多渠道重复推送

**I26**

跨系统通知与Action同步

**J26**

批准集成范围内状态变化和行动保持一致

**K26**

AI选择信息重点和接收人

**L26**

推荐遵守权限和订阅规则，用户可解释和调整

**M26**

Prototype

### Row 27

**A27**

7 执行智能

**B27**

AI Summary

**C27**

管理信息很多，但人工总结耗时且口径不稳定

**D27**

仅对可信字段生成项目/Issue摘要并人工确认

**E27**

摘要引用数据来源；事实错误可记录和纠正

**F27**

太模糊，看不董

**G27**

自动生成项目、周报和风险摘要

**H27**

建立准确性和人工采用率基线；低置信度内容不自动发布

**I27**

生成跨项目趋势和部门摘要

**J27**

AI结论可下钻到项目和字段证据

**K27**

企业级实时智能简报

**L27**

不同角色在权限范围内获得一致、可解释的信息

**M27**

Prototype

### Row 28

**A28**

7 执行智能

**B28**

风险与瓶颈分析

**C28**

风险往往在延期后才被发现

**D28**

用规则暴露逾期、空Owner、临近节点和开放高风险Issue

**E28**

规则、阈值和命中记录透明；误报可记录

**F28**

需要思考如何用自动化的方式来构建自动提醒

**G28**

分析风险信号与结果的关联

**H28**

形成可验证的命中率、提前量和误报基线

**I28**

识别跨项目等待、重复Issue和资源约束

**J28**

AI/分析结果至少支持1项经验证的管理改善

**K28**

预测延期、质量、资源和供应风险

**L28**

模型监控漂移；预测不直接替代业务决策

**M28**

Planned

### Row 29

**A29**

7 执行智能

**B29**

建议与Copilot

**C29**

历史数据存在，但难以转化为下一步建议

**D29**

不进入核心范围，仅保留需求和数据准备

**E29**

未通过数据与知识Gate前不发布业务建议

**G29**

完善案例检索、权限和评估数据，不上线Copilot

**H29**

形成经审核的知识集、测试问题和准确性评估方法

**I29**

受控试用项目问答、案例比较和决策准备

**J29**

答案引用来源，权限正确，用户反馈可追踪；低置信度拒答

**K29**

企业Execution Copilot

**L29**

能够跨对象分析、解释建议并记录最终决定

**M29**

Later Phase

### Row 30

**A30**

7 执行智能

**B30**

AI Agent

**C30**

标准动作仍需人工跨系统执行

**D30**

明确不开发自主执行

**E30**

仅记录候选场景、风险和授权需求

**F30**

需要研究下airtable的AI能力和边界

**G30**

定义候选场景、权限、风险和停止条件，不执行生产动作

**H30**

形成批准的场景清单和控制要求；不连接生产写权限

**I30**

在受控沙盒中验证提醒、建任务和信息同步

**J30**

动作需人工批准、可回退、有日志，并达到批准的安全门槛

**K30**

在治理边界内自主执行

**L30**

具备权限、监控、审计、人工接管和停止机制

**M30**

Later Phase

### Row 31

**A31**

8 支撑能力

**B31**

权限、安全与审计

**C31**

不同角色不应看到或修改全部数据

**D31**

定义试点角色、查看/编辑范围和关键变更日志

**E31**

权限测试通过；敏感字段不向无权限用户开放

**F31**

需要和数据层，功能层，界面层等结合起来，一起定义一份权限指南，参考PLM

**G31**

形成角色权限矩阵和定期复核

**H31**

新增/离职/调岗权限有流程和Owner

**I31**

跨部门数据分类、保留和审计

**J31**

集成数据满足IT/Security要求并可追踪访问

**K31**

企业AI授权和安全治理

**L31**

模型、工具、数据和Agent权限统一管理

**M31**

Partial

### Row 32

**A32**

8 支撑能力

**B32**

平台运营

**C32**

系统维护、修复、支持和迭代依赖一个人

**D32**

建立问题清单、优先级、响应规则和备份

**E32**

关键故障有Owner和恢复步骤；系统知识不只存在于个人电脑

**F32**

系统知识库的功能还非常不完善，可以说还没起步，需要下一步思考如何构建，

**G32**

形成最小核心团队和服务节奏

**H32**

产品、系统构建、用户支持和试点运营均有明确责任人

**I32**

Business、IT/Data、Security联合运营

**J32**

集成、版本、变更和支持流程正式运行

**K32**

企业平台运营模式

**L32**

具备持续预算、SLA、容量和灾备能力

**M32**

One-person / Needs Design

### Row 33

**A33**

8 支撑能力

**B33**

采纳与用户支持

**C33**

双系统、习惯和响应能力限制真实使用

**D33**

确定Committed Pilot Team、使用节奏、反馈和退出条件

**E33**

真实团队持续使用；每周记录活跃、完整度、问题和价值证据

**F33**

Done

**G33**

建立培训、Champion和支持渠道

**H33**

问题有响应时限；关键流程由团队而非Sunny单独维护

**I33**

跨部门Change Network

**J33**

每个参与部门有业务Owner和采用指标

**K33**

企业AI能力与工作方式转型

**L33**

培训、角色变化和价值指标进入正式运营机制

**M33**

Pilot / Needs Design

### Row 34

**A34**

8 支撑能力

**B34**

平台架构与边界

**C34**

Airtable适合试点，但企业级扩展边界尚未验证

**D34**

记录容量、权限、性能、集成和治理Gap

**E34**

形成Airtable Fit/Gap清单及每个Gap的风险、Owner和决策日期

**F34**

需要调查并明确airtable 的运行机理和特征，并且和autoPM的功能进行比较和匹配，生成报告

**G34**

完成继续/集成/重构/迁移架构评审

**H34**

Business、IT/Data、Security共同签署决策和过渡方案

**I34**

实施批准的集成或平台演进

**J34**

迁移/集成不破坏核心对象、历史和审计链

**K34**

形成可扩展企业技术架构

**L34**

满足企业容量、安全、可靠性和AI服务要求

**M34**

Needs Evaluation

## Phase Gates

### Row 1

**A1**

Phase Gates & Decision Criteria

### Row 2

**A2**

Gate的作用是防止“开发了下一阶段功能”被误认为“已经进入下一阶段”。所有建议门槛需在启动阶段由Sponsor确认。

### Row 4

**A4**

Phase

**B4**

阶段名称

**C4**

唯一目标

**D4**

强制交付范围

**E4**

怎样算完成

**F4**

必须保留的证据

**G4**

Gate决策

**H4**

明确不做

### Row 5

**A5**

Phase 1

**B5**

XPT Pilot Validation

**C5**

证明可信数据能支撑项目查看、任务执行、Issue闭环和Weekly Review

**D5**

Data Foundation；Project Hub；Task & Action；Issue & Recovery；Weekly Review；Pilot Operating Model

**E5**

建议门槛：核心字段完整度≥95%；关键Task具备Owner/Due；周报无需重复录入；至少1个真实Issue完成验证闭环；采纳和节省时间建立Baseline

**F5**

项目数据抽查；使用日志；Issue闭环样本；周报样本；用户反馈；平台Fit/Gap

**G5**

Continue / Rework / Integrate / Handover / Stop

**H5**

AI预测、Agent、企业级大规模集成

### Row 6

**A6**

Phase 2

**B6**

NPI Scale-up

**C6**

把已验证闭环标准化并复制到NPI团队

**D6**

标准项目模板；PMO数据对齐；团队运营；数据质量巡检；角色化Review；AI Summary

**E6**

建议门槛：≥80%新试点从批准模板启动；质量报告每周运行；核心支持责任明确；不同角色使用同一事实源

**F6**

模板版本；数据对账；活跃项目；支持记录；摘要准确性基线

**G6**

Scale / Rework / Platform Review / Stop

**H6**

未经批准的跨部门强制推广和自主AI执行

### Row 7

**A7**

Phase 3

**B7**

Cross-functional Execution

**C7**

让跨部门对象、依赖和Portfolio瓶颈可见并形成管理行动

**D7**

跨部门流程；批准系统集成；Portfolio；瓶颈分析；跨项目知识复用

**E7**

至少2条跨部门流程跑通；至少1个系统性瓶颈被验证并形成行动；集成有双Owner和异常处理

**F7**

跨部门流程证据；瓶颈案例；集成运行日志；管理决策记录

**G7**

Expand / Reprioritize / Redesign / Stop

**H7**

没有数据、权限和Owner支撑的全企业铺开

### Row 8

**A8**

Phase 4

**B8**

Enterprise AI Intelligence

**C8**

在可信数据、知识和治理基础上形成预测、建议和有限自主执行

**D8**

知识图谱；风险预测；Execution Copilot；Agent；企业AI治理

**E8**

模型和建议可解释、可审计；准确率/采用率达到批准门槛；Agent可回退、有限权、可人工接管

**F8**

模型评估；审计日志；安全评审；业务价值；人工接管测试

**G8**

Scale / Limit / Retrain / Suspend

**H8**

黑盒决策、无授权Agent和无法追踪的数据使用

## Feature Catalog

### Row 1

**A1**

Feature Catalog & Development Assignment

### Row 2

**A2**

把功能矩阵转化为可分配任务：先确认用户问题和输入，再开发逻辑与输出；没有验收指标的功能不得标记Done。

### Row 4

**A4**

能力分类

**B4**

功能模块

**C4**

当前判断

**D4**

核心用户问题

**E4**

最小输入

**F4**

核心处理逻辑

**G4**

明确输出

**H4**

成功指标

**I4**

主要依赖

**J4**

首次进入Phase

### Row 5

**A5**

1 数据基础

**B5**

业务对象模型

**C5**

Partial / To Validate

**D5**

项目、SKU、任务和Issue缺少统一关系

**E5**

对象ID、来源字段、更新规则

**F5**

建立Program→Project→SKU→Task→Issue→Action关系

**G5**

对象关系图、字段词典和唯一ID规则

**H5**

核心对象均有唯一ID；父子关系可追踪；抽查无孤立核心记录

**I5**

前序数据模型、业务Owner和验收人

**J5**

Phase 1

### Row 6

**A6**

1 数据基础

**B6**

主数据与身份

**C6**

Partial / To Validate

**D6**

同一项目、SKU、人员存在多种名称和编码

**E6**

对象ID、来源字段、更新规则

**F6**

锁定Project ID、SKU、People、Factory主键及匹配规则

**G6**

主数据匹配表、重复项和差异清单

**H6**

导入重复项可识别；关键记录都能匹配到唯一主键

**I6**

前序数据模型、业务Owner和验收人

**J6**

Phase 1

### Row 7

**A7**

1 数据基础

**B7**

数据输入与系统连接

**C7**

Manual / Partial

**D7**

现有数据需要人工搬运，且来源边界不清楚

**E7**

对象ID、来源字段、更新规则

**F7**

建立输入/输出矩阵；支持Excel/MPP导入和原系统链接

**G7**

输入输出矩阵、导入结果和接口日志

**H7**

每类数据标明Read/Write/Link/Import/TBD及系统Owner；导入可重复执行

**I7**

前序数据模型、业务Owner和验收人

**J7**

Phase 1

### Row 8

**A8**

1 数据基础

**B8**

数据质量与治理

**C8**

Partial

**D8**

字段多、重复、空值和更新时间不一致

**E8**

对象ID、来源字段、更新规则

**F8**

定义核心必填字段、Source、Owner、Last Updated和质量例外

**G8**

质量报告、例外清单和责任矩阵

**H8**

建议门槛：核心字段完整度≥95%；所有例外可定位到记录和Owner

**I8**

前序数据模型、业务Owner和验收人

**J8**

Phase 1

### Row 9

**A9**

2 项目控制塔

**B9**

Project Hub

**C9**

Built / To Validate

**D9**

管理者难以快速找到项目事实和下一步

**E9**

Project/SKU/日期/Owner/Task/Issue

**F9**

单页展示项目、SKU、阶段、日期、Owner、Task、Issue和Action

**G9**

可下钻的单项目页面

**H9**

真实用户无需解释可在30秒内回答状态、原因、Owner和下一步

**I9**

前序数据模型、业务Owner和验收人

**J9**

Phase 1

### Row 10

**A10**

2 项目控制塔

**B10**

项目健康与状态

**C10**

Partial / To Validate

**D10**

项目状态依赖主观汇报，缺少事实支撑

**E10**

Project/SKU/日期/Owner/Task/Issue

**F10**

用日期、逾期Task、开放Issue和下一Action支撑健康判断

**G10**

有事实支撑的健康状态和变化记录

**H10**

每个At Risk/Delayed状态均可下钻到事实与Owner

**I10**

前序数据模型、业务Owner和验收人

**J10**

Phase 1

### Row 11

**A11**

2 项目控制塔

**B11**

Portfolio视图

**C11**

Built / To Validate

**D11**

单项目可见，但无法发现组合层风险和冲突

**E11**

Project/SKU/日期/Owner/Task/Issue

**F11**

展示试点项目状态、关键日期、Issue和Owner分布

**G11**

可筛选、可下钻的组合视图

**H11**

试点范围内项目总数与明细一致；筛选后可下钻到记录

**I11**

前序数据模型、业务Owner和验收人

**J11**

Phase 1

### Row 12

**A12**

3 工作流协调

**B12**

Task & Action

**C12**

Built / To Validate

**D12**

任务依赖邮件和个人记忆，责任与证据不完整

**E12**

Task、Owner、Due、Dependency、Evidence

**F12**

建立Task/Action、Owner、Due、Status、Priority、Dependency、Evidence

**G12**

个人/项目工作队列和执行日志

**H12**

关键工作100%具备Owner和Due；完成项有状态和证据

**I12**

前序数据模型、业务Owner和验收人

**J12**

Phase 1

### Row 13

**A13**

3 工作流协调

**B13**

Milestone与模板

**C13**

Partial

**D13**

不同项目计划颗粒度不一致，启动时反复重建

**E13**

Task、Owner、Due、Dependency、Evidence

**F13**

锁定XPT/NPI基础Milestone和关键交付物

**G13**

有版本的项目/任务模板

**H13**

每个试点项目有批准的里程碑、计划日期和Owner

**I13**

前序数据模型、业务Owner和验收人

**J13**

Phase 1

### Row 14

**A14**

3 工作流协调

**B14**

提醒、催办与升级

**C14**

Prototype / To Validate

**D14**

PM花费大量时间追踪状态和催促Owner

**E14**

Task、Owner、Due、Dependency、Evidence

**F14**

上线个人待办、逾期提醒和每周检查

**G14**

提醒规则、发送日志和升级记录

**H14**

提醒指向正确Owner和记录；发送结果有日志；可关闭重复提醒

**I14**

前序数据模型、业务Owner和验收人

**J14**

Phase 1

### Row 15

**A15**

3 工作流协调

**B15**

完成证据与审计

**C15**

Needed

**D15**

任务标记完成，但交付物和结果不可验证

**E15**

Task、Owner、Due、Dependency、Evidence

**F15**

为关键Task定义Completion Evidence

**G15**

可复核的交付物和审计链

**H15**

关键交付物可通过附件、链接或结果字段验证

**I15**

前序数据模型、业务Owner和验收人

**J15**

Phase 1

### Row 16

**A16**

4 异常与决策

**B16**

Issue识别与影响

**C16**

Built / To Validate

**D16**

Issue描述不统一，业务影响难以比较

**E16**

Issue、Impact、Cause、Decision、Action、Result

**F16**

记录Issue、Category、Severity、MP/Launch Impact、Owner和Target

**G16**

关联项目和业务影响的Issue记录

**H16**

每个关键Issue均关联项目并说明影响、Owner和目标日期

**I16**

前序数据模型、业务Owner和验收人

**J16**

Phase 1

### Row 17

**A17**

4 异常与决策

**B17**

Root Cause与Recovery

**C17**

Built / To Validate

**D17**

问题被描述，但根因和恢复行动没有形成闭环

**E17**

Issue、Impact、Cause、Decision、Action、Result

**F17**

连接Root Cause、Recovery Action、Owner和Target Date

**G17**

根因记录和Recovery Plan

**H17**

关闭前必须有原因、行动和责任人；Action Done不等于Issue Closed

**I17**

前序数据模型、业务Owner和验收人

**J17**

Phase 1

### Row 18

**A18**

4 异常与决策

**B18**

Decision管理

**C18**

Needed

**D18**

会议决定与后续执行脱节，无法追踪谁决定了什么

**E18**

Issue、Impact、Cause、Decision、Action、Result

**F18**

记录Decision Needed、Decision Owner、Due和Decision Result

**G18**

Decision Log及自动生成的Action

**H18**

每个待决事项有唯一责任人和日期；决定后自动生成Action

**I18**

前序数据模型、业务Owner和验收人

**J18**

Phase 1

### Row 19

**A19**

4 异常与决策

**B19**

验证关闭

**C19**

Needed

**D19**

问题关闭缺少结果验证，容易重新发生

**E19**

Issue、Impact、Cause、Decision、Action、Result

**F19**

增加Result、Verification、Verified By、Closed Date和Reopen

**G19**

Result、Verification和Reopen记录

**H19**

至少一个真实Issue完成从发现到验证关闭的全链路证据

**I19**

前序数据模型、业务Owner和验收人

**J19**

Phase 1

### Row 20

**A20**

5 执行知识

**B20**

Lesson Learned

**C20**

Partial

**D20**

问题解决后没有形成可复用经验

**E20**

已验证Issue、Solution、Lesson、Evidence

**F20**

Issue关闭时记录Lesson、适用条件和证据

**G20**

经审核的知识条目

**H20**

已验证关闭的关键Issue均有Lesson或明确Not Reusable原因

**I20**

前序数据模型、业务Owner和验收人

**J20**

Phase 1

### Row 21

**A21**

5 执行知识

**B21**

案例检索与复用

**C21**

Needed

**D21**

新人和其他项目无法快速找到相似案例

**E21**

已验证Issue、Solution、Lesson、Evidence

**F21**

支持按Category、Project Type和关键词检索Issue

**G21**

历史案例检索结果和采用反馈

**H21**

用户可在限定步骤内找到并打开历史记录和证据

**I21**

前序数据模型、业务Owner和验收人

**J21**

Phase 1

### Row 22

**A22**

5 执行知识

**B22**

模板资产

**C22**

Partial

**D22**

每个项目都从零开始设计任务和流程

**E22**

已验证Issue、Solution、Lesson、Evidence

**F22**

建立基础Task Template并标注版本

**G22**

经验证、可复用的模板库

**H22**

模板任务有Owner Function、Duration、Dependency和适用范围

**I22**

前序数据模型、业务Owner和验收人

**J22**

Phase 1

### Row 23

**A23**

6 Review与沟通

**B23**

Weekly Summary

**C23**

Built / To Validate

**D23**

周报依赖重复收集和人工拼接

**E23**

状态变化、例外、Decision、Action

**F23**

自动汇总状态变化、Top Issue、Overdue、Decision和Next Action

**G23**

自动周报和角色化摘要

**H23**

试点项目周报从系统数据生成；不再二次录入核心状态

**I23**

前序数据模型、业务Owner和验收人

**J23**

Phase 1

### Row 24

**A24**

6 Review与沟通

**B24**

Management Review

**C24**

Partial

**D24**

管理会议讨论状态多，形成决策和行动少

**E24**

状态变化、例外、Decision、Action

**F24**

建立变化、例外、待决事项和行动四区Review

**G24**

例外/决策Review及行动清单

**H24**

会议输出的Decision和Action在会后进入系统并有Owner/Due

**I24**

前序数据模型、业务Owner和验收人

**J24**

Phase 1

### Row 25

**A25**

6 Review与沟通

**B25**

通知与行动回写

**C25**

Prototype

**D25**

邮件发送后不能确认是否形成行动

**E25**

状态变化、例外、Decision、Action

**F25**

状态邮件包含记录链接、Owner和Next Action

**G25**

通知日志和写回原记录的Action

**H25**

发送有成功/失败日志；行动可直接回到对应记录

**I25**

前序数据模型、业务Owner和验收人

**J25**

Phase 1

### Row 26

**A26**

7 执行智能

**B26**

AI Summary

**C26**

Prototype

**D26**

管理信息很多，但人工总结耗时且口径不稳定

**E26**

可信数据、历史结果、权限、反馈

**F26**

仅对可信字段生成项目/Issue摘要并人工确认

**G26**

带来源引用的项目/Issue摘要

**H26**

摘要引用数据来源；事实错误可记录和纠正

**I26**

前序数据模型、业务Owner和验收人

**J26**

Phase 1

### Row 27

**A27**

7 执行智能

**B27**

风险与瓶颈分析

**C27**

Planned

**D27**

风险往往在延期后才被发现

**E27**

可信数据、历史结果、权限、反馈

**F27**

用规则暴露逾期、空Owner、临近节点和开放高风险Issue

**G27**

可解释的风险信号和瓶颈清单

**H27**

规则、阈值和命中记录透明；误报可记录

**I27**

前序数据模型、业务Owner和验收人

**J27**

Phase 1

### Row 28

**A28**

7 执行智能

**B28**

建议与Copilot

**C28**

Later Phase

**D28**

历史数据存在，但难以转化为下一步建议

**E28**

可信数据、历史结果、权限、反馈

**F28**

不进入核心范围，仅保留需求和数据准备

**G28**

带证据的问答、比较和建议

**H28**

未通过数据与知识Gate前不发布业务建议

**I28**

前序数据模型、业务Owner和验收人

**J28**

Phase 3

### Row 29

**A29**

7 执行智能

**B29**

AI Agent

**C29**

Later Phase

**D29**

标准动作仍需人工跨系统执行

**E29**

可信数据、历史结果、权限、反馈

**F29**

明确不开发自主执行

**G29**

可回退、有限权的动作与审计日志

**H29**

仅记录候选场景、风险和授权需求

**I29**

前序数据模型、业务Owner和验收人

**J29**

Phase 3

### Row 30

**A30**

8 支撑能力

**B30**

权限、安全与审计

**C30**

Partial

**D30**

不同角色不应看到或修改全部数据

**E30**

角色、权限、流程、平台运行数据

**F30**

定义试点角色、查看/编辑范围和关键变更日志

**G30**

角色权限矩阵和访问审计

**H30**

权限测试通过；敏感字段不向无权限用户开放

**I30**

前序数据模型、业务Owner和验收人

**J30**

Phase 1

### Row 31

**A31**

8 支撑能力

**B31**

平台运营

**C31**

One-person / Needs Design

**D31**

系统维护、修复、支持和迭代依赖一个人

**E31**

角色、权限、流程、平台运行数据

**F31**

建立问题清单、优先级、响应规则和备份

**G31**

Runbook、支持队列和服务责任

**H31**

关键故障有Owner和恢复步骤；系统知识不只存在于个人电脑

**I31**

前序数据模型、业务Owner和验收人

**J31**

Phase 1

### Row 32

**A32**

8 支撑能力

**B32**

采纳与用户支持

**C32**

Pilot / Needs Design

**D32**

双系统、习惯和响应能力限制真实使用

**E32**

角色、权限、流程、平台运行数据

**F32**

确定Committed Pilot Team、使用节奏、反馈和退出条件

**G32**

Pilot Charter、使用和支持证据

**H32**

真实团队持续使用；每周记录活跃、完整度、问题和价值证据

**I32**

前序数据模型、业务Owner和验收人

**J32**

Phase 1

### Row 33

**A33**

8 支撑能力

**B33**

平台架构与边界

**C33**

Needs Evaluation

**D33**

Airtable适合试点，但企业级扩展边界尚未验证

**E33**

角色、权限、流程、平台运行数据

**F33**

记录容量、权限、性能、集成和治理Gap

**G33**

Airtable Fit/Gap、架构决定和过渡方案

**H33**

形成Airtable Fit/Gap清单及每个Gap的风险、Owner和决策日期

**I33**

前序数据模型、业务Owner和验收人

**J33**

Phase 1

## Guide & Status

### Row 1

**A1**

Guide, Status Definitions & Working Rules

### Row 2

**A2**

这份工作簿是产品能力地图，不是“功能愿望清单”。每个功能必须回答：解决什么问题、需要什么数据、交付什么、怎样验收。

### Row 4

**A4**

状态

**B4**

含义

**C4**

允许的表述

**D4**

不允许的误解

**E4**

RECOMMENDED WEEKLY USE

### Row 5

**A5**

Validated

**B5**

已经在真实项目和真实用户中形成证据

**C5**

已验证，可用于Gate判断

**D5**

不能因为一次Demo就标记Validated

**E5**

Monday

**F5**

更新Feature Catalog中的当前状态、Owner和证据链接

### Row 6

**A6**

Built / To Validate

**B6**

功能或字段已经存在，但价值和运行尚未验证

**C6**

已构建，待真实验证

**D6**

不等于已完成

**E6**

Wednesday

**F6**

检查Phase 1功能是否被非主线需求打断

### Row 7

**A7**

Partial / Prototype

**B7**

只有部分流程、数据或自动化可用

**C7**

部分可用/原型

**D7**

不能称为Operating Model

**E7**

Friday

**F7**

按Gate证据复盘：完成/未完成/原因/需要支持/下一步

### Row 8

**A8**

Needed / Planned

**B8**

已确认有必要，但尚未开发或锁定

**C8**

需要开发/计划中

**D8**

不能写成Current Capability

**E8**

Monthly

**F8**

与Sponsor确认范围、数字门槛和资源是否变化

### Row 9

**A9**

Later Phase

**B9**

明确不进入当前Phase

**C9**

后续阶段

**D9**

不能挤占Phase 1主线

### Row 12

**A12**

DEVELOPMENT WORKING RULES

### Row 13

**A13**

01

**B13**

先证明用户问题

**C13**

每个功能必须对应一个明确问题；只因为“看起来有用”不能进入开发。

### Row 14

**A14**

02

**B14**

先定义数据再做页面

**C14**

先明确对象、来源、Owner和更新规则，再设计界面和自动化。

### Row 15

**A15**

03

**B15**

交付物与验收分开

**C15**

Built只表示功能存在；Validated必须有真实项目、真实用户和证据。

### Row 16

**A16**

04

**B16**

数字门槛先获批准

**C16**

本文件中的百分比为建议值；经Peter/Jen/Sponsor确认后才成为正式承诺。

### Row 17

**A17**

05

**B17**

Gate决定下一阶段

**C17**

提前做出Phase 2功能不等于进入Phase 2；必须满足Phase 1 Gate。

### Row 18

**A18**

06

**B18**

AI必须基于可信事实

**C18**

没有数据、知识、权限和反馈闭环，不开发AI预测或Agent。
