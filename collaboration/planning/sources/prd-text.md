AutoPM
Master PRD
专业基线、Phase 1执行控制与视觉导读版
一句话定义  AutoPM是连接项目主数据、执行流程、任务、问题、责任、行动、决策、报告和知识的项目执行平台。真实项目运行产生可信数据，可信数据再支撑自动化、管理输出和AI。

项目
内容
版本
v3.4
状态
顶层业务关系确认与Phase 1执行基线整合版
Owner
Sun Sun / AutoPM
日期
2026-09-01
范围
当前以NPI/XPT试点为起点，长期支持跨职能项目执行
事实纪律
真实业务；结构化且MECE；不编造；未确认事项标记TBD

本版更新重点
保留AutoPM双重定位和Phase 1至Phase 4唯一主路线。
将Phase 1从概念范围更新为M1至M6的执行控制结构。
明确Target、Current Implementation、Implementation Check、Evidence和Gate Decision之间的关系。
把正文、执行Blueprint和Implementation Check分层，避免PRD成为重复任务清单。
统一排版、标题层级、表格、状态标签、页眉页脚和导航。

目录
锁定Programme、Base Model、Product、SKU、Project、Factory和Market的顶层定义、关系、继承规则与角色视图边界，作为后续设计不再反复确认的基线。
在Word中右键目录并选择“更新域”
Contents
0. 执行摘要3
0.1 价值主线3
0.2 本版核心结论3
0.3 读者导航4
1. AutoPM定位5
1.1 双重定位5
1.2 两层定位的关系5
1.3 产品原则5
2. 核心问题与目标结果6
2.1 非目标6
3. 管理对象、关系与数据纪律7
3.1 统一业务对象7
3.2 统一执行链7
3.3 数据治理8
3.4 状态纪律8
4. 核心运行机制10
4.1 项目进入与计划10
4.2 日常执行10
4.3 异常与恢复10
4.4 周度管理11
4.5 持续改进11
5. 范围、系统边界与Phase演进12
5.1 系统边界12
5.2 Phase 1至Phase 412
5.3 Phase Gate原则13
6. 产品能力与角色工作空间14
6.1 项目执行核心能力14
6.2 角色工作空间15
6.3 共同原则15
7. 平台、集成、自动化与AI治理17
7.1 平台架构17
7.2 Airtable角色17
7.3 集成治理18
7.4 Automation治理18
7.5 AI治理18
8. Phase 1实施、验收与Gate 120
8.1 Phase 1目标20
8.2 M1至M6执行结构20
8.3 执行控制体系21
8.4 完成判定22
8.5 Gate 1证据22
8.6 Gate 1输出23
8.7 主要待决策事项23
附录A. 术语与定义24
附录B. Phase 1能力包Blueprint25
附录C. Action与验收治理27
附录D. 责任与人工Decision矩阵28
附录E. Current Baseline与指标控制29
附录F. 系统集成工作矩阵30
附录G. 版本更新记录31
v3.2审阅结论31



0. 执行摘要
核心业务问题  AutoPM要解决的不是缺少更多Tracker或页面，而是项目事实分散、责任和行动不清、问题未闭环、报告难下钻，以及真实执行数据无法持续沉淀。

问题
当前表现
AutoPM改变
信息分散
Project、SKU、日期、Issue和Action分布在不同系统、Excel和协作渠道
连接对象、来源和责任，形成一次维护、多处使用
人工推动
状态、Owner、Due、周报和关闭依赖追问
用规则、队列、提醒和例外管理推动执行
问题未闭环
Issue、Root Cause、Action、Decision和Result断开
建立从异常到验证关闭的完整链条
管理难下钻
汇总数字与具体Task、Issue、Owner脱节
所有上层视图可回到执行事实和证据
知识不可复用
结果散落在会议、邮件和个人文件
把原因、行动、结果和Lesson形成结构化历史

0.1 价值主线
关系 / 层级使用关系图或分层图
流程 / 闭环使用步骤流或循环图
角色 / 界面使用工作空间卡片
定义 / 边界使用对照表
状态 / 范围使用标签矩阵
验收 / Gate使用检查清单
图0｜PRD视觉表达方法
读图结论｜不同信息使用不同表达方式，不把所有内容都画成复杂大图。每个图只回答一个核心问题。
价值主线  透明 → 执行加速 → 数据驱动 → 智能辅助。顺序不可倒置，AI必须建立在真实使用、可信数据和人工责任之上。

0.2 本版核心结论
AutoPM首先是项目执行平台，同时也是数字化与AI转型试点。
管理不是目的，持续收集真实细颗粒度数据、发现问题并验证结果才是目的。
Phase 1目标不是单纯证明技术可行，而是证明可信数据、执行闭环、真实采用、稳定运行和业务价值。
Phase 1由M1至M6六个模块组成，所有状态必须从Action级Implementation Check汇总。
当前实现不反向定义Target；已开发不自动等于已完成；无证据不标记完成。
0.3 读者导航
深蓝稳定定义 / 核心结构
绿色已连接 / 运行链路
蓝色目标能力 / 设计
橙色风险 / 需确认 / Decision
紫色治理 / AI / Gate
灰色边界 / TBD / 外部来源
图例｜颜色含义
读图结论｜同一颜色在全篇保持同一语义，帮助读者快速区分核心结构、运行链路、目标设计、风险、治理和TBD。
读者
重点章节
主要收获
Sponsor / Leadership
0、1、5、8
价值、范围、证据和Gate决定
PM / NPI
3、4、6、8
对象、执行闭环、日常与周度运行
跨职能Owner
3、4、6
更新什么、何时升级、如何验证关闭
开发与平台伙伴
3、4、6、7、附录
对象、规则、功能、接口和验收
PMO / Data / IT
3、5、7、8、附录
来源、边界、责任、集成和运营

1. AutoPM定位
1.1 双重定位
项目执行平台连接事实、任务、问题、责任、行动与结果
数字化与AI试点验证连接数据、规则、自动化和AI的转型路径
图1｜AutoPM双重定位
读图结论｜项目执行平台是业务落点，数字化与AI试点是验证目的。没有真实执行数据，转型价值无法证明。
定位
目的
不能退化为
数字化与AI转型试点
验证集中并连接数据、定义对象与规则、自动化推动执行、AI基于可信上下文辅助管理的路径
只做演示、概念验证或AI包装
自动化项目执行平台
连接Project、SKU、Milestone、Task、Issue、Recovery Action、Decision、Result和Owner，推动真实执行
只做任务列表、周报或另一个Tracker

1.2 两层定位的关系
核心关系  真实项目持续运行产生可信执行数据；可信执行数据验证数字化、自动化和AI治理方法。没有真实使用，转型价值无法证明。

1.3 产品原则
真实业务优先于页面数量。
共享数据优先于重复复制。
业务对象和关系优先于报表外观。
Action、Owner、Due和Result优先于模糊状态描述。
人工确认保留在Root Cause、正式Decision、Gate批准和Issue关闭等关键节点。
未确认事项保持TBD，不用Target代替Baseline或Actual。
2. 核心问题与目标结果
结构性问题
根因
目标结果
流程不畅
前置条件、交接和跨团队依赖不透明
依赖、等待、Blocker和影响可见并可处理
信息分散
同一事实多处保存且版本不一致
每项关键事实有来源、责任和唯一维护位置
管理依赖人工
更新、追问、升级和报告靠个人推动
系统队列与规则推动，PM处理例外
问题未闭环
异常、行动、决定和结果没有稳定连接
Issue能够追溯到Action、Decision、Result和Evidence
知识不能复用
结果没有形成结构化历史
Lesson能够反馈到模板、规则和流程
双系统阻力
旧工具与AutoPM同时维护
过渡期有唯一编辑位置、同步和退出条件

2.1 非目标
复杂项目与分散数据
→
等待 / 查找 / 追问 / 返工
→
执行慢与问题晚
→
统一事实与闭环行动
图2｜核心问题因果链
读图结论｜AutoPM要解决的是项目执行效率和问题闭环，不是增加更多页面或Tracker。
不替代完整PLM、ERP、ECN、Jira或专业文件库。
不创建第二套产品或BOM主数据。
不让AI未经授权修改Actual、确认Root Cause、作正式Decision、批准Gate或关闭Issue。
不以页面数、Automation数、记录数或演示效果单独证明价值。
3. 管理对象、关系与数据纪律
3.1 统一业务对象
类别
对象
回答的问题
项目结构
Programme、Project、SKU
这是什么项目，包含哪些可独立跟踪的SKU
计划执行
Stage、Milestone、Gate、Task、Deliverable
准备如何完成，当前执行到哪里
异常
Risk、Issue、Delay、Blocker
发生或可能发生什么偏差，影响什么
处置
Recovery Action、Decision、Escalation
谁在何时采取什么行动，需要谁决定
结果
Result、Evidence、Verification、Lesson
实际结果是什么，是否真正解决，如何复用
责任
Owner、Contributor、Confirmer、Approver
谁执行、谁确认、谁决策

3.1.1 顶层产品与项目对象的确认定义
本节固化已通过真实业务案例确认的顶层定义。除非正式数据或业务规则发生变化，后续设计、实施和评审不应再次从零确认这些基本含义。
对象
确认定义
粒度与边界
Programme
PMO基于Subcategory拆分出的产品族管理单元；不是一次Project开案。
不是一次开案，也不是Project文件夹；用于稳定识别产品族及其正式归属。
Base Model
产品的参考型号或基础型号。
一个Programme可包含多个Base Model；一个Base Model只能属于一个Programme。
Product
Base Model下具有独立记录和编号的产品对象，包括US/Canada与International产品。
Product不是SKU的别名；具体正式字段与来源仍由主数据映射确认。
SKU
具有独立SKU ID的正式产品单元，也是Project中需要保留独立执行差异的追踪粒度。
一个Project可含一个或多个SKU；同一SKU可参与多个Project。
Project
在特定时间启动的一次真实开案，具有独立业务目的、范围、Factory和主时间表。
Project Type说明为什么开案，不是另一个项目层级。
Project Type
Extension、Upsell、Cost Saving、Dual Source、Transfer等开案类型。
一个Project只有一个主要Project Type。
Project-SKU
一个SKU在某次Project中的执行关系。
保存范围变化、SKU日期例外和该Project上下文中的执行状态。
Project Group
当前业务中不存在的正式对象。
不得因视觉分组或方便理解而建立正式Project Group层级。
确认主线｜产品结构回答“这是什么产品”；项目结构回答“这次开案要做什么”。两者通过SKU及Project-SKU关系连接。
3.1.2 顶层对象关系与基数规则
以下关系是当前顶层架构的业务基线。关系用于规范数据连接，不代表每个业务概念都必须拆成独立数据库表。
关系
确认规则
设计影响
Subcategory → Programme
Programme属于Subcategory，是PMO视角的产品族管理单元。
Programme保留正式Subcategory归属。
Programme → Base Model
一对多；同一Base Model不得属于多个Programme。
避免Programme归属冲突。
Base Model → Product → SKU
Product有独立编号；SKU有独立SKU ID。
正式产品信息来自主数据源，AutoPM保存映射与执行所需信息。
Project ↔ SKU
多对多；一个Project可含一个或多个SKU，同一SKU可进入多个Project。
必须通过Project-SKU表达执行关系。
Project → Factory
一个Project严格对应一个Factory。
Factory属于具体开案上下文；同一SKU可在多个Factory对应不同Project。
Project → Market
原则上一个Project对应一个Market，允许少量多Market例外。
Market提出的产品和配置需求在Project层表达。
Project → Base Model
Project不直接限制Base Model，由Project所含SKU决定。
Base Model通过SKU关联或汇总，不重复手工维护。
重要纪律｜业务对象、实际数据库表和页面展示是三件不同的事。是否独立建表必须根据独立维护、生命周期、历史和关系需要决定。
3.2 统一执行链

图3｜核心业务对象关系
读图结论｜Project连接多个SKU；执行事实沿Milestone、Task、Issue、Action、Decision、Result和Learning沉淀，并支持从汇总反向下钻。
示例编号仅用于解释关系，不代表真实项目数据。
主链  Programme → Project → SKU → Milestone / Gate → Task / Deliverable → Issue / Risk / Delay → Recovery Action / Decision → Result / Evidence / Learning。

所有汇总必须能够回到原始执行事实。多SKU项目既要表达共同计划，也要保留SKU独立日期、状态、Issue和MP影响。
3.3 数据治理
IdentityRecord ID、Name、Type、Version
RelationshipParent、Project、SKU、Milestone、Task、Issue
ResponsibilityOwner、Collaborator、Verifier、Approver、Decision Maker
DatesBaseline、Target、Forecast、Actual、Last Updated
StatusLifecycle、Health、Execution、Confirmation
Source & EvidenceSource System、Method、Document、Change Log
图4｜核心记录字段分组
读图结论｜字段不是一张扁平清单。每条记录都要同时回答“是谁、关联谁、谁负责、什么时候、什么状态、依据是什么”。
治理项
要求
唯一性
核心对象使用稳定ID；名称变化不改变身份；重复导入不得静默新建
来源
每个关键字段明确正式来源、人工、同步、计算或AI候选
责任
明确业务定义Owner、数据质量Owner、维护人和批准人
时间
Target、Baseline、Forecast、Actual、更新时间和确认时间分开
质量
检查完整、一致、唯一、准确、及时和可追溯
审计
关键修改保留修改人、时间、原因、前后值和影响范围

3.4 状态纪律
TBD
→
PLANNED
→
PILOT
→
CURRENT
→
ACTUAL EVIDENCE
图5｜从未确认到真实证据
读图结论｜Target和计划状态不能代替Actual。只有能够回查的真实证据，才能支撑完成判断和Gate决策。
状态
含义
控制
CURRENT
当前存在或使用
必须有可查看证据
PILOT
真实试点
不等于规模化
PLANNED
已计划未完成
不得写成现有能力
VISION
长期方向
不作为当前承诺
TBD
未确认
公开保留，不编造
Baseline
确认的实际起点
注明范围、日期和来源
Target
验证目标
不等于Actual
Actual
真实结果
可以追溯原始数据

3.5 可视化页面体系与使用边界

为支持不同受众理解 Programme、Project 与 SKU 三层关系，避免同一份关系图同时承载治理目标、当前实现和字段细节，建立以下三个互补的可视化页面。
PMO_Data_Model_Slide.html：目标治理模型。面向架构设计者和业务方，回答“应该是什么”。以 Programme → Project → SKU 的层级瀑布形式，说明每张表的功能、模块和继承关系。
PMO_Table_Relationship.html：当前 Airtable 落地实现。面向 AutoPM 配置和开发团队，回答“系统里数据怎么流”。聚焦字段维护方、触发方向和当前 SKU-based 自动关联链路。
PMO_Field_Inheritance.html：字段级清单。面向字段配置和视图设计者，回答“具体字段从哪来”。列出每张表应展示哪些字段、哪些字段来自本表、哪些来自关联表。
三者关系：Data Model 描述目标结构，Table Relationship 描述当前实现的数据流，Field Inheritance 描述当前实现的字段来源。三者覆盖不同问题，不重复、不冲突；后续设计变更应先更新 Data Model，再同步 Table Relationship 和 Field Inheritance。
4. 核心运行机制
总体闭环  业务数据进入 → 标准化与关联 → 计划和任务运行 → 规则识别异常 → Recovery与Decision → Result与Verification → 报告与学习。

4.1 项目进入与计划
项目进入
→
结构与来源确认
→
Milestone / Task
→
Owner / Due / Dependency
→
执行更新
图6｜项目从进入到执行
读图结论｜先确认项目身份、关系和来源，再建立计划、责任和依赖，最后进入持续更新。
项目进入前检查重复，确认Project ID、Programme、SKU、Owner、范围、阶段和模板。
将目标分解为Milestone、Task、Deliverable、Owner、日期和依赖。
保留原始计划、当前Forecast和Actual，不互相覆盖。
4.1.1 Project主计划、SKU继承与例外
Project维护共同主时间表。Project中的SKU在启动时默认继承该计划；项目推进过程中，仅对发生差异的少数关键日期进行SKU级调整，避免复制和维护完整SKU时间表。
情形
系统规则
必须保留的信息
无SKU例外
SKU有效日期使用Project主时间表日期。
Project日期与来源。
存在SKU例外
SKU有效日期使用已确认的SKU例外日期。
Project原日期、SKU例外日期、原因、修改人、修改时间。
Project日期变化
未覆盖SKU随Project更新；已有Override的SKU进入冲突复核。
变更前后值、受影响SKU、复核结果。
新增SKU
按当前有效Project主计划建立继承关系。
加入日期、来源与确认人。
SKU移出
不得删除Project-SKU关系。
移出日期、原因、操作者或确认人。
SKU重新加入
保留旧历史并建立当前有效状态。
历史状态、重新加入日期和适用计划。
有效SKU日期 = 已确认的SKU例外日期（如有）；否则 = Project主时间表日期。具体关键日期清单、批准权限和冲突处理仍为TBD。
4.2 日常执行
Owner通过Today、Upcoming、Overdue、Blocked和Pending队列处理工作。
Task完成必须记录实际结果和必要证据，不只选择Completed。
长期未更新、缺Owner、缺Due和状态冲突进入例外队列。
4.3 异常与恢复

图7｜问题从发现到验证关闭
读图结论｜Action完成不等于Issue关闭。必须记录Result、完成Verification并确认影响已解决或正式接受，否则Reopen或新增Action。
升级阈值、批准角色和关闭权限仍以TBD及正式规则为准。
处置链  异常候选 → 业务确认 → Issue / Risk / Delay / Blocker → Impact与Root Cause → Recovery Action → Owner与Due → Escalation / Decision → Result → Verification → Close或Reopen。

4.4 周度管理
更新事实
→
检查缺失 / 冲突
→
审查异常 / 决策
→
回写Action
→
下周验证
图8｜周度运行闭环
读图结论｜周会不是重新收集状态，而是基于已更新事实处理例外、形成决定并在下周期验证结果。
会前更新Task、Issue、Action和Forecast。
系统检查缺失、冲突、逾期、未更新和闭环中断。
周会聚焦变化、偏差、Top Risk、逾期Action和Decision Needed。
决定和新Action直接写回系统，下周期验证结果。
4.5 持续改进
关闭的问题形成Root Cause、有效与无效Action、Decision、Result和Lesson，并反馈到项目分类、模板、标准工期、依赖、Owner映射、提醒、关闭规则和报告结构。
5. 范围、系统边界与Phase演进
5.1 系统边界
正式记录层保存主数据、专业记录和原始文件
AutoPM执行层连接执行影响并管理Task、Issue、Action、Decision和Result
分析与AI层使用已确认数据形成报告、分析和建议
图9｜三层系统边界
读图结论｜AutoPM连接正式系统，但不替代专业记录；分析和AI只能消费经过确认且可追溯的数据。
系统层
主要责任
正式记录层
PMO/Tracker、PLM、ECN、Jira、SharePoint及人员目录保存正式主数据、专业记录和原始文件
项目执行层
AutoPM连接影响执行的关键状态，管理Project/SKU、Task、Issue、Action、Decision、Result、提醒和关闭
分析与智能层
Power BI、Snowflake和AI使用确认后的结构化数据进行分析、报告和建议

5.2 Phase 1至Phase 4
Phase 1XPT Pilot ValidationM1 Data → M6 Evidence
Phase 2NPI Scale-up标准化与规模化
Phase 3Cross-functional跨团队与跨系统执行
Phase 4AI Intelligence分析、预测、建议与治理
图10｜唯一Phase演进路线
读图结论｜Phase 1至Phase 4是唯一主路线；M1至M6是Phase 1内部实施模块，不新增或重命名Phase。
Phase
目标
完成方向
Phase 1：XPT Pilot Validation
让真实XPT/NPI项目持续运行，验证可信数据、执行闭环、真实采用、稳定运行与业务价值
完成M1至M6并形成Gate 1证据
Phase 2：NPI Scale-up
成为NPI日常项目执行工具
扩展标准模板、依赖、报告自动化、治理和支持
Phase 3：Cross-functional
扩展为跨团队执行平台
连接跨系统状态、业务模块、Gate、跨部门Issue与资源瓶颈
Phase 4：AI Intelligence
让AI参与分析、预测、建议和治理
建立可信上下文、相似案例、风险和Portfolio智能

5.3 Phase Gate原则
真实项目和真实用户持续使用。
数据达到本Phase要求的完整性、稳定性和可追溯性。
工作流能够暴露并推动解决实际问题。
用户使用方式和管理节奏已经形成。
扩大范围不会增加不可接受的重复维护。
支持、权限、Data Owner和平台能力能够承接下一阶段。
6. 产品能力与角色工作空间
6.1 项目执行核心能力
Project / SKU
→
Plan / Task
→
Deliverable / Gate
→
Issue / Recovery
→
Decision / Change
→
Report / Learning
图11｜核心功能链
读图结论｜功能不是独立页面集合，而是围绕同一数据链推动项目从计划、执行、异常、决定走到报告和经验。
能力
业务目的
关键输出
项目与SKU
建立统一入口并保留SKU真实差异
Project Profile、SKU Exception、Change History
计划与Task
把目标分解为可执行工作
Schedule、Milestone、Dependency、Overdue、Blocked
Deliverable与Gate
连接专业交付状态而不复制完整文件
Checklist、Gate Readiness、Exception、Approval
Issue与Recovery
把异常转化为有责任、有行动、有结果的闭环
Issue Board、Recovery、Escalation、Closure
Decision与Change
记录背景、选项、决定、影响和后续行动
Decision Queue、Impacted Objects、Follow-up Action
报告与Knowledge
从确认数据生成输出并沉淀经验
Weekly Summary、Leadership Pack、Lessons

6.2 角色工作空间

图12｜角色工作空间
读图结论｜个人、项目、异常、周度、领导和系统管理入口共享同一数据中心，只改变查看范围和允许动作。
界面、项目编号、状态和统计数字均为概念示例，不代表真实数据或当前已实现页面。
工作空间
回答的问题
主要动作
My Daily Work
本人今天做什么，什么逾期、阻塞或待确认
更新Task/Action、提交Issue、补充Result
PM Daily Cockpit
项目怎样，谁未更新，什么需要Decision
维护计划、Review、提醒、升级和关闭
Project Detail
一个Project的完整可下钻全景
下钻至SKU、Task、Issue、Owner和Action
异常工作台
哪些异常缺Owner、Action、Due或验证
分配、恢复、升级、Decision、验证和关闭
Weekly Review
本周变化、风险、行动和决定是什么
确认状态，回写Decision和Action
Leadership / Portfolio
哪些项目偏离，什么影响MP/Launch
协调资源、Decision并下钻到Recovery
System Admin
系统是否稳定，数据是否可信
权限、模板、规则、同步、Automation和审计

6.2.1 Programme与Project的角色视图边界
底层关系模型负责连接数据；角色工作空间只提取对当前使用者和决策有价值的信息。存在关系不等于必须在上层页面默认展开。
维度
Programme视图
Project视图
主要使用者
PMO、产品组合管理、管理层
Project Manager、Project Engineer、功能团队
核心目的
识别产品族、确认归属和正式主数据，并进入相关Project。
把Market需求转化为可执行范围并推动交付。
默认信息
Programme Code、Name、ALE ID、Alias、Brand、Category、Subcategory、Lifecycle、相关Project入口。
Project ID、Name、Type、Market需求、Factory、Owner、Kickoff、主时间表、SKU范围和执行关注。
轻量汇总
相关Project数量或入口，以及必要的关注提示。
Active SKU、范围变化、日期例外和下一个关键节点。
不默认展示
完整Base Model/Product/SKU清单、Market配置、Factory、详细计划、SKU日期例外、Issue和Action明细。
Programme产品族主数据、完整SKU主数据，以及全部下层明细的横向复制。
主要动作
查找、定位、筛选和下钻。
更新、推进、调整、确认和关闭。
页面原则｜Programme是产品族定位与组合入口；Project是一次真实开案的执行控制中心。主线保持统一，视图按角色变化。
6.3 共同原则
共享数据  所有工作空间共享同一套Project、SKU、Task、Issue、Action、Decision和Result数据，只按角色显示不同范围与动作，不形成新的数据孤岛。

7. 平台、集成、自动化与AI治理
7.1 平台架构

图13｜AutoPM目标平台架构
读图结论｜Source of Truth、AutoPM执行层、分析与AI层职责分开；权限、质量、审计和变更治理贯穿所有层。
具体接口、同步方向、频率和成熟度以集成矩阵的CURRENT、PILOT、PLANNED或TBD状态为准。
层
责任
数据来源层
正式主数据、专业状态、原始文件和人工执行更新
数据接入层
表单、导入、链接、读取、写入、同步和AI候选提取
统一业务数据层
统一ID、对象关系、状态、来源、版本和历史
规则与自动化层
生成、计算、校验、提醒、升级、报告、同步和失败处理
工作空间层
个人、项目、异常、周度、领导和管理入口
分析与AI层
基于确认数据形成可追溯的分析、总结和建议

7.2 Airtable角色
平台纪律  AutoPM是产品，Airtable是当前用于验证业务模型和运行闭环的承载平台。平台选择不能反向定义业务目标、对象和规则。

7.3 集成治理
LINK只保存正式系统链接
IMPORT批量进入并校验
READ读取正式来源
WRITE受控写回
SYNC双向同步与冲突管理
图14｜五种集成方式
读图结论｜能打开链接不等于已经集成。每个对象必须明确采用哪种方式、哪个系统为准、失败和冲突如何处理。
管理项
要求
对象与正式来源
明确取得或写回什么，以及哪个系统为准
方式
严格区分Link、Import、Read、Write和双向同步
匹配
使用稳定ID；记录匹配失败、冲突、裁决和修复
责任与安全
明确Business Owner、Data Owner、权限和审计
成熟度
按CURRENT、PILOT、PLANNED、VISION或TBD标记

7.4 Automation治理
每项Automation记录ID、目的、Trigger、Input、Rule、Output、Owner、Version、成功条件、失败处理、测试、回退和Run Log。重复事件不得重复创建，失败必须可定位、可重试、可补救。
7.4.1 当前 Automation 清单与匹配策略

当前已部署的 Automation 围绕 Project、PMO SKU 和 Programme 三层对象的自动关联展开，同时包含人员协作和进度计算辅助。
AutoPM-19（Project 触发）：当 Project 新建或其 Project SKU (Manual) 字段更新时，按 SKU 文本匹配 PMO SKUs.DEV_SKU，回写 Projects.PMO SKU (Link) 和 Projects.PMO Program (Link)。
AutoPM-20（PMO SKU 触发）：当 PMO SKU 新建或更新时，反写相关 Projects 的 SKU Link 和 Program Link。
AutoPM-21（Programme 触发）：当 Programme 新建或其 Program_Code 更新时，反写相关 Projects 的 SKU Link 和 Program Link。
AutoPM-07c（Task 人员同步）：新 Task 创建时，将所属 Project 的 NPI Owner 按邮箱匹配为 Collaborator。
AutoPM-07d（Issue 人员同步）：新 Issue 创建时，将所属 Project 的 NPI Owner 按邮箱匹配为 Collaborator。
AutoPM-17（Project 进度计算）：Task 的 Completed By 更新时，自动计算所属 Project 的完成进度条。
三层匹配策略：Projects.Project SKU (Manual) 文本 → PMO SKUs.DEV_SKU → PMO SKUs.Program_Code → Programs.Program_Code。SKU 是 Project 与 Programme 之间的精确匹配锚点；Programme 通过 SKU 间接与 Project 关联，而不是通过独立的人工层级链路。
7.5 AI治理
Extract
→
Summarize
→
Identify
→
Suggest
→
Human Decision
图15｜AI参与层级
读图结论｜AI可以提取、总结、识别和建议，但正式Decision、Root Cause、Gate批准、Actual修改和Issue关闭保留人工责任。
AI用途
允许内容
控制
Extract
提取候选Issue、Action、Owner、Due和Decision
保留来源并由业务确认
Summarize
总结已记录事实
仅使用授权数据并支持回查
Identify
识别缺失、冲突、异常和风险候选
提供依据，不直接修改正式事实
Suggest
提出优先级、Recovery、相似案例和流程建议
记录接受、修改、拒绝和最终结果

禁止越权  AI未经授权不得修改Actual、确认Root Cause、作出正式Decision、批准Gate、关闭Issue、修改规则或写回正式系统。

8. Phase 1实施、验收与Gate 1
8.1 Phase 1目标
更新后的目标  让真实XPT/NPI项目在AutoPM中持续运行，验证可信执行数据、项目执行闭环、真实用户采用、运行稳定性和可证明的业务价值，为是否进入Phase 2提供证据。

8.2 M1至M6执行结构
M1 数据基础对象、关系、字段、来源、质量
M2 执行闭环进入、计划、异常、Recovery、验证
M3 工作入口个人、项目、异常、周度、领导
M4 运行保障导入、计算、提醒、报告、权限、恢复
M5 Pilot采用范围、责任、使用规则、节奏、支持
M6 证据与GateBaseline、采用、质量、价值、平台、Gate 1
图16｜Phase 1六个实施模块
读图结论｜M1至M6按因果顺序连接：先建立可信数据，再运行闭环、提供入口、保障稳定、推动采用，最后形成证据和Gate决定。
模块
名称
核心问题
能力包范围
M1
执行数据基础
建立可信、关联、可追溯的数据基础
对象、关系、ID、字段、来源、真实数据、质量审计
M2
项目执行与问题闭环
让真实项目从进入运行到问题验证关闭
进入、计划、更新、异常、Recovery、Decision、Verification、Learning
M3
工作与管理入口
让不同角色在合适入口完成工作
个人、项目、异常、周度、领导和用户体验
M4
自动化、集成与运行保障
确保导入、计算、提醒、报告和连接稳定
导入、计算、提醒、报告、PMO连接、权限、失败恢复
M5
Pilot运行与采用
推动真实团队和项目持续使用
范围、责任、使用规则、双系统、上手、周度节奏、支持
M6
价值证据与Gate决策
用真实证据决定是否进入Phase 2
Baseline、采用、质量、闭环、效率、平台和Gate 1

8.3 执行控制体系

图17｜Action ID连接五类执行载体
读图结论｜Task Execution定义Target，Blueprint解释标准，Implementation Check维护事实和证据，Map汇总状态，Gate 1 Evidence Pack支持正式决定。
Action数量和显示内容以当前受控Excel为准。
载体
唯一责任
禁止事项
Phase 1 Map
展示Phase 1整体方向及M1至M6汇总状态
不得手工维护与明细不一致的完成状态
Task Execution
定义Target Action、解释、预期产出和目标验收
不得用当前实现反向修改Target
Implementation Check
记录Current Implementation、Evidence、判断、Gap、修改Action、Owner、Due和Status
无证据不得标记完成
Blueprint
解释能力包核心问题、Action含义、验收标准和交付物
不得成为第二套状态维护表
Gate 1 Evidence Pack
汇总采用、质量、闭环、效率、平台和风险证据
页面数和演示效果不得单独作为价值证据

关联规则  Action ID是跨表唯一关联键。定义只维护一次，执行状态只维护一次，Map和Blueprint通过公式或受控关联读取明细状态。

8.4 完成判定
存在功能、规则或流程真实存在
关联连接正确业务对象
运行可在真实项目使用
证据结果可检查并回查
责任Owner、Due和状态明确
独立理解不依赖额外口头解释
图18｜Action完成的六项判断
读图结论｜页面存在或字段建立只是“存在”。只有关联、运行、证据和责任同时成立，才能判断Target完成。
真实功能、规则或流程存在。
与正确业务对象和上下游记录关联。
在真实项目中可以运行。
输出结果可以检查并留下证据。
责任、日期和状态清楚。
不依赖额外人工解释才能证明完成。
8.5 Gate 1证据
采用真实项目与真实用户持续使用
数据质量完整、一致、唯一、及时、可追溯
执行闭环Issue到Result与Verification
效率与结果与Baseline比较并记录负面影响
平台能力访问、性能、权限、恢复与支持
治理Owner、Source of Truth、Decision权
图19｜Gate 1六类证据
读图结论｜Gate 1不能由单一指标或演示效果决定，必须同时审查采用、数据、闭环、效率、平台和治理证据。
证据域
最低需要证明
真实采用
真实用户和项目持续更新并使用AutoPM开展日常和周度管理
数据质量
核心对象、关系、Owner、Due和状态完整，重复与冲突可处理
执行闭环
Issue能够形成Action、Decision、Result和Verification，失败时可Reopen
效率与结果
与Baseline比较查找、追问、报告和重复维护的变化，并记录负面影响
平台能力
访问、性能、权限、自动化、集成、导出、回退和支持可承接下一阶段
治理
关键角色、Source of Truth、Decision权和Phase 2进入条件明确

8.6 Gate 1输出
决定
适用判断
输出
Continue
方向成立，但部分质量或稳定性需要修复
限定范围继续，设Owner和Due
Scale
采用、质量、闭环、效率、稳定性和支持达到门槛
进入Phase 2并扩大范围
Integrate
业务模型有效，整合可减少重复或提高可信度
批准具体Link、Import、Read或Write范围
Rework
真实案例证明模型、规则或体验不适用
重设计并重新验证
Handover
文档、权限、监控、支持和替代Owner就绪
正式交接运营责任
Stop
无采用或价值、重复工作增加、平台条件不满足
停止投入，保护数据并记录原因

8.7 主要待决策事项
Programme、Base Model、Product、SKU、Project、Factory和Market的顶层定义与核心关系已确认；后续只需验证正式字段映射和真实数据例外。
Project主时间表、SKU默认继承和仅保存关键日期例外的原则已确认；关键日期清单、批准权限、冲突复核和恢复规则仍为TBD。
关键字段正式来源、Data Owner和冲突裁决。
Tracker与Weekly Report的唯一维护位置及退出双系统条件。
Airtable许可、容量、性能和长期角色。
权限、批准、Decision和Issue关闭责任。
提醒升级与降噪阈值。
Phase指标、Gate标准和批准人。
8.8 Phase 1最小产品范围与当前优先级
Phase 1不是同时建设所有设想能力，而是先用同一套可信数据跑通四个用户可见功能，并以真实试点证明它们能够共同形成项目执行闭环。
优先级
Phase 1核心能力
必须解决的问题
最低可验收结果
P0
Data Foundation & Governance
统一Project、SKU、Milestone、Task、Issue、Action、Owner、日期、状态和来源。
核心对象可追溯、可关联、可去重；关键字段有来源、Owner和更新时间。
P1
Project Hub / Project Detail
把判断项目所需的核心事实集中到一个可下钻入口，而不是复制全部专业系统和文件。
用户在30秒内找到当前状态、SKU差异、主要问题、责任人和下一步行动，并可回到正式来源。
P1
Task & Action Management
管理影响交付的Milestone、跨部门Task和Recovery Action，不扩展为个人琐事管理工具。
每项关键工作有Owner、Due、Status、关联对象和完成证据；逾期、阻塞和缺失可识别。
P1
Issue & Recovery Loop
把流程、资源、责任和跨部门问题从记录推进到解决与验证。
Issue可连接Root Cause、Recovery Action、Decision、Result、Verification和Lesson；Action Done不自动等于Issue Closed。
P1
Weekly Review & Reporting
用同一套执行数据形成周度管理输出，停止再次收集和重做状态。
周报可自动生成、突出变化与例外，并下钻到Project、SKU、Issue、Action和Owner。
Gate
Pilot Operation & Evidence
证明系统被真实团队持续使用，并产生可信的效率、闭环、数据质量和平台能力证据。
形成连续运行记录、Baseline对比、问题闭环样本、平台评估和Gate 1决定。
8.9 当前开发顺序与停止线
Release 1｜数据与业务结构：锁定Program → Project → SKU、核心对象、ID、Source of Truth及输入输出关系。
Release 2｜Project Hub：建立30秒项目判断入口，并完成Project/SKU下钻和正式来源链接。
Release 3｜Task & Action：让影响交付的任务、责任、日期、依赖、逾期和完成证据可运行。
Release 4｜Issue & Recovery：跑通Issue → Action → Result → Verification → Lesson。
Release 5｜Weekly Review：从同一套数据生成可下钻周报，并形成周度更新、审查、决定和验证节奏。
Release 6｜Phase 1 Gate：基于采用、质量、闭环、效率、平台和治理证据决定继续、扩展、集成、返工或停止。
Phase 1停止线｜AI预测、企业级Portfolio Intelligence、大规模双向集成、个人待办管理、非关键Dashboard和不影响当前闭环的新功能，不进入当前开发主线。
8.10 Peter会议后的强制交付
交付物
必须回答的问题
完成标准
Problem Statement
AutoPM到底解决什么，为什么不是另一个Tracker或Power BI？
问题、业务影响、AutoPM边界和Phase 1假设在一页内讲清楚。
Success Beacon
Phase 1结束时，什么证据证明方向成立？
采用、数据质量、执行闭环、效率、管理价值和平台能力均有可核查证据。
Old State → Future State
工作方式具体改变了什么？
展示多系统查找和人工追问如何变为一次更新、例外管理、下钻和闭环。
Functional & Data Architecture
哪些数据进来、出去、由谁维护，哪些接口仍缺失？
明确Source、Link/Import/Read/Write/Sync、方向、Owner、频率、成熟度和Gap。
Program → Project → SKU
业务层级和汇总/下钻规则是什么？
定义层级、唯一ID、继承/Override、状态汇总和SKU独立差异。
附录A. 术语与定义
术语
定义
Programme
PMO基于Subcategory拆分出的产品族管理单元；不是一次Project开案。
Project
在特定时间启动的一次真实开案，具有独立业务目的、范围、Factory和主时间表。
SKU
具有独立SKU ID的正式产品单元，也是Project中需要保留独立执行差异的追踪粒度。
Milestone
关键时间节点或阶段结果
Task
需要由Owner在明确日期前完成的工作
Issue
已经发生并需要处理的问题
Risk
尚未发生但可能影响目标的不确定事项
Delay
计划、Forecast或Actual之间的日期偏差
Blocker
导致当前工作无法继续的条件
Recovery Action
用于消除影响或恢复计划的具体行动
Decision
由有权限人员作出的正式选择
Result
Action或Decision产生的实际业务结果
Verification
由适当人员确认结果是否满足关闭条件
Lesson
从真实问题、行动和结果中形成的可复用经验

附录A.1 顶层关系不可反复确认基线
本表用于保留本轮深度业务确认结果。后续评审应先引用本基线，只有出现正式规则变化或真实数据反证时才重新打开相应问题。
基线ID
已确认结论
允许重新打开的条件
BL-01
Programme属于Subcategory；一个Programme可含多个Base Model；一个Base Model只能属于一个Programme。
正式PMO规则发生变化或发现可验证反例。
BL-02
US/Canada与International Product是具有独立记录和编号的Product对象。
正式产品主数据证明定义不同。
BL-03
Project是一次真实开案；Project Type是开案分类；不存在正式Project Group对象。
PMO发布正式层级规则。
BL-04
一个Project可含一个或多个SKU；同一SKU可参与多个Project。
真实业务规则发生变化。
BL-05
一个Project严格对应一个Factory；同一SKU可对应多个Factory。
供应商与Factory正式数据模型证明需要拆分。
BL-06
Project原则上对应一个Market，允许少量多Market例外。
正式Market开案规则改变。
BL-07
Project不直接限制Base Model，由Project中的SKU决定。
真实数据验证出必须独立保存的业务约束。
BL-08
Project维护主计划；SKU默认继承；仅差异关键日期保存Override。
Pilot证明该机制不可运行或维护成本不可接受。
BL-09
SKU加入或移出Project必须保留历史，不得直接删除。
正式数据保留政策另有要求。
BL-10
新Project Business ID全公司唯一；历史无ID项目通过Name加Kickoff Date或Year辅助识别，并使用AutoPM内部ID。
正式历史编号或主数据匹配规则提供更稳定标识。
治理要求｜任何基线变更必须记录变更原因、依据、批准人、影响范围和生效版本，不得静默修改。
附录B. Phase 1能力包Blueprint
能力包
名称
核心问题
M1.1
业务对象定义
统一项目、计划、异常、恢复和责任对象
M1.2
对象关系模型
建立层级、汇总、下钻与多SKU关系
M1.3
唯一标识与映射
确保对象稳定匹配、去重和历史处理
M1.4
字段与状态标准
统一字段含义、日期和状态转换
M1.5
数据来源与责任
明确Source of Truth、读写边界与Owner
M1.6
真实项目数据初始化
用真实项目验证结构和数据
M1.7
数据质量与审计
发现、修复并追溯数据问题
M2.1
项目进入与初始化
正确、不重复地建立真实项目
M2.2
计划与任务建立
建立Milestone、Task、Owner、Due和依赖
M2.3
日常执行与更新
持续记录真实进度、Forecast和证据
M2.4
异常识别与记录
分类并关联Risk、Issue、Delay和Blocker
M2.5
恢复行动与升级
建立Recovery Action并在需要时升级
M2.6
管理决策
记录Decision背景、选项、决定和跟踪
M2.7
结果确认与验证关闭
区分Action Done和Issue Closed
M2.8
历史与经验沉淀
形成可检索案例并改进规则与模板
M3.1
个人执行入口
集中个人Task、Action和待确认事项
M3.2
项目管理入口
查看和维护完整项目执行情况
M3.3
异常处理入口
集中处理缺Owner、Action、Due和验证的异常
M3.4
周度管理入口
基于同一事实完成Review和回写
M3.5
领导审查与下钻
从组合状态下钻到事实、责任和结果
M3.6
用户体验与动作效率
减少无用字段、重复录入和页面切换
M4.1
数据导入与初始化自动化
安全导入、校验、去重、修正和回退
M4.2
状态与异常计算
自动计算逾期和偏差并展示依据
M4.3
提醒与升级
提醒正确人员并控制去重、停止和升级
M4.4
报告生成
从确认数据生成可下钻报告草稿
M4.5
PMO主数据连接
读取、匹配并对账必要主数据
M4.6
权限与审计
控制访问、修改、确认、批准和导出
M4.7
运行监控与失败恢复
监控失败、安全重试、防污染和回退
M5.1
Pilot范围确认
明确目标、项目、角色、启动和退出条件
M5.2
角色与责任
明确执行、业务、数据、平台和管理责任
M5.3
使用规则
统一更新、异常、升级、关闭和证据要求
M5.4
双系统过渡
明确唯一维护位置、同步和退出条件
M5.5
角色上手
用真实操作证明角色能够使用
M5.6
周度运行节奏
建立更新、检查、审查、决定和验证循环
M5.7
用户支持与问题处理
收集、排序、修复并验证用户问题
M6.1
基线定义
在Pilot前锁定可重复计算的实际起点
M6.2
使用与采用证据
证明持续使用而不是一次登录
M6.3
数据质量证据
证明数据完整、关联正确和可管理
M6.4
执行闭环证据
证明问题从发现走到结果和验证
M6.5
效率与业务结果
比较前后变化并记录负面影响
M6.6
平台能力评估
评价容量、访问、集成、迁移、支持和成本
M6.7
Gate 1决策
基于证据正式决定下一步

详细Action  每个能力包的Action级定义、简单解释、验收标准和交付物保存在Phase 1 Blueprint；正文不重复复制，避免PRD和执行表形成两套定义。

附录C. Action与验收治理
字段
定义
维护位置
Action ID
跨Map、Task Execution、Blueprint和Implementation Check的唯一键
锁定后不随任务名称改变
Target Task
为实现Phase 1目标必须完成的任务
Task Execution
明确内容 / 简单理解
专业定义和业务人员可理解的解释
Blueprint
Target Deliverable
完成任务必须留下的结果
Task Execution / Blueprint
Target Acceptance
判断Target是否完成的标准
Task Execution / Blueprint
Current Implementation
当前真实存在的页面、字段、规则或流程
Implementation Check
Evidence
支持判断的真实记录、文件、截图或测试结果
Implementation Check
Gap
当前实现相对Target的差距
Implementation Check
Modification Action
为关闭Gap需要采取的行动
Implementation Check
Owner / Due / Status
执行责任、日期和进度
Implementation Check

附录D. 责任与人工Decision矩阵
事项
执行负责
最终批准
状态
产品范围与优先级
Product Owner
Sponsor
具体人员TBD
项目范围与计划
Project Manager
Project Approver
批准权TBD
业务规则
Business Owner
业务批准人
人员TBD
数据冲突
Data Owner
正式系统Owner
人员TBD
Root Cause
Issue Business Owner
授权确认人
阈值TBD
Gate / Exception
Gate Owner
Gate Approver
规则TBD
Issue关闭
Issue Owner
授权关闭人
规则TBD
Phase下一步
Product Owner准备
Phase Gate Approver
批准人TBD

附录E. Current Baseline与指标控制
事实纪律  现有材料不足以得出精确Actual。未知值保持TBD，不使用Target代替Baseline。

指标
Baseline
来源
用途
真实运行项目数
TBD
Project清单与更新历史
采用和扩大判断
周活跃目标用户
TBD
活动日志
采用
Task Owner/Due完整率
TBD
字段检查
执行可用性
Issue Recovery完整率
TBD
Issue和Action关系
闭环
周报准备时间
TBD
统一测时
效率
人工追问次数
TBD
PM统一记录
效率
风险提前暴露时间
TBD
首次可见与影响时间
管理价值
Automation成功率
TBD
Run Log
稳定性
v3.4
2026-09-01
补充Phase 1最小产品范围、Release优先顺序、停止线及Peter会议后的五项强制交付。


每个指标必须定义业务目的、公式、范围、数据来源、Baseline、Target、Actual、频率、Owner、确认人和异常解释。不同日期、范围或口径不得合并为一个“最新数字”。
附录F. 系统集成工作矩阵
系统
数据 / 用途
目标关系
成熟度
PMO / Tracker
Programme、Project、SKU、目标与Lead
正式来源；可能接收执行偏差
PILOT / TBD
MS Project
Schedule、Milestone、Task
导入或连接计划
PLANNED / TBD
PLM / BOM
产品、物料和文件
引用标识、链接和关键状态
LINK / TBD
ECN
变更、状态和影响
连接Decision、Action和受影响对象
LINK / TBD
Jira
专业工作项
读取或链接相关状态
LINK / TBD
SharePoint / Teams
文件、会议和协作
保留链接，候选提取需确认
CURRENT LINK / PLANNED
People Directory
人员、部门和角色
Owner、权限、通知和交接
TBD
Snowflake / Power BI
分析与报告
接收确认后的结构化数据
PLANNED / TBD

附录G. 版本更新记录
版本
日期
更新内容
v1.0
2026-08-27
完成第1至第8章及附录框架，并进行全篇审阅
v2.0
2026-08-27
补充跨角色导航、Baseline、责任、开发规格、集成矩阵与Gate决策
v3.4
2026-09-01
系统整合Phase 1 M1至M6执行结构、Action控制关系、完成判定和Gate 1证据；整体重构排版与视觉层级
v3.4
2026-09-01
固化顶层对象定义、基数关系、Project主计划与SKU继承/Override、范围历史、Programme与Project角色视图边界，并新增不可反复确认基线。

v3.5 更新记录
2026-09-01
新增 3.5 可视化页面体系与使用边界，明确 PMO_Data_Model_Slide.html、PMO_Table_Relationship.html、PMO_Field_Inheritance.html 三页面向的不同受众与问题。
新增 7.4.1 当前 Automation 清单与匹配策略，补充 AutoPM-07c、AutoPM-07d、AutoPM-17 的人员同步与进度计算职责。
梳理并新增 AutoPM-19、AutoPM-20、AutoPM-21 的触发逻辑与回写规则；明确 SKU-only 匹配策略为 Projects.Project SKU (Manual) → PMO SKUs.DEV_SKU → Programs.Program_Code。
v3.4审阅结论
检查维度
结果
定位
双重定位保留，项目执行平台为业务落点
MECE
正文按定位、问题、对象、运行、边界、产品、平台、实施组织
Phase一致性
仅使用既定Phase 1至Phase 4
执行可落地性
Phase 1通过M1至M6、Action ID、Evidence和Gate 1连接
准确性
Target、Current、Baseline、Actual和TBD分开
可维护性
PRD保留稳定原则；Action级细节放在Blueprint与Implementation Check
版式
统一封面、目录、标题层级、表格、Callout、页眉页脚和留白

最终结论  本版本可作为AutoPM Master PRD的当前专业基线。未确认的人员、阈值、系统接口、字段值和平台长期选择继续保持TBD，并通过真实Pilot证据逐项锁定。
