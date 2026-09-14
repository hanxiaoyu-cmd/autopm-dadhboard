# Projects 字段架构与显示规划

更新日期：2026-09-06  
检查范围：Projects CSV（2,998条、124个导出字段）与 Airtable 线上 schema（125个字段，新增 Project SKUs 关联）。

配套规划：`Other_Core_Tables_Field_Architecture_Plan.md`（Programs、PMO SKUs、Project SKUs、SKU Milestone Plans、Tasks、Issues、People、Factories）。

## 一、结论

Projects 已经覆盖项目管理需要表达的主要内容：项目身份、范围、状态、负责人、主计划、SKU、任务、问题、周报、资料入口、进度和数据质量。当前问题不是缺字段，而是五类信息混在一起：

1. 员工需要维护的业务事实；
2. 其他表的关联和自动汇总；
3. Weekly Report／All Tracker 使用的里程碑缓存；
4. 导入、审计、通知控制字段；
5. 多代方案遗留的重复字段。

因此第一阶段不建议继续增加普通字段。先建立分类 Views、统一权威字段、隐藏后台字段，再迁移或删除重复项。

目标不是让一个 Grid 显示125列，而是：

- Project List 显示8–10个字段；
- Project Detail 按模块显示约25个高价值字段和关联列表；
- Data 表通过多个 Views 分工；
- 系统、导入和审计字段只在 Admin Views 中显示。

## 二、Projects 的职责边界

Projects 回答五个问题：

1. 这是哪个项目，属于哪个 Program，包含哪些 Project SKU 执行实例？
2. 项目整体状态和当前阶段是什么？
3. 谁负责，哪个工厂／供应商执行？
4. 主计划、任务和问题现在如何？
5. 本周发生了什么，下一步需要关注什么？

Projects 不应重复保存：SKU自己的状态、SKU独立日期、完整Issue正文、完整Task内容、Program产品主数据，以及导入运行的全过程。

## 三、建议的八个字段模块

### 01 基础信息与范围

员工维护并在详情页顶部显示：

- Project ID (Manual)：唯一业务编号，必须保留；用于匹配，但脚本内部仍应使用 record ID。
- Project name (Manual)：项目名称。
- Project Description (Manual)：稳定的项目范围和目标，不用于写周报。
- Project Type (Manual)：项目类型。
- Region (Manual)：项目覆盖区域。
- Model / Family (Manual)：当无法完全由Program或SKU获得时保留。
- Factory （Manual)：关联Factories，项目执行工厂／供应商。
- Manufacture Country (Manual)：仅在Factory不能稳定给出国家时保留；长期应改为Factory Lookup。
- Capacity / Forecast (Manual)：先确认粒度；若同一Project不同SKU不同，应迁移到Project SKUs。
- Change Types (Manual)：项目变更范围。
- Project Level (Auto)：由Change Types自动判定，后台计算，详情可显示。

条件保留、默认不显示：

- Product Photo (Manual)：CSV仅12/2,998有值。优先使用Program或SKU图片，完成迁移后再删除。
- Brand (Manual)、Sub Category (Manual)、Launch_Target (Manual)：当前属于产品／Program属性。PMO Program覆盖完整后改为Lookup，人工字段转为导入兼容字段。
- Project SKU (Manual)：保留为导入原文，建议改名 Project SKU (Import Raw)，不作为正式关系。

### 02 正式关系

系统或管理员维护，是后续页面和自动化的骨架：

- PMO Program (Link)：Project → Program。
- Project SKUs：Project → Project SKUs，新关系表；作为Project与PMO SKU、供应商和SKU Status的正式执行关系。
- PMO SKU (Link)：迁移期保留，用于与Project SKUs交叉核对；不能再代表唯一Project归属。
- Tasks (system manage)：Project → Tasks。
- Issues (system manage)：Project → Issues。
- Project People(System)：项目团队汇总关系。
- CPM Template References (system manage)：模板引用，隐藏；未查清Automation前不能删除。
- Schedule Import 2：关联导入记录，隐藏。

自动显示／汇总：

- SKU quantity：应逐步改为统计Project SKUs，而不是直接PMO SKU链接。
- SKU List：迁移期使用；最终从Project SKUs Lookup。
- ALE ID (PMO)、Program Code (PMO)：Lookup，后台或详情次要区域显示。
- PMO Program Match Note：匹配审计信息，仅Admin显示。

### 03 项目状态与阶段

员工维护：

- Project Status (Manual)：项目整体业务判断，唯一正式Project Status。
- Current Gate (Manual)：当前阶段／Gate。
- MP Time Window (Select)：保留为Interface筛选缓存，但应由系统同步，建议改名 MP Time Window (Filter Cache)，员工不维护。

系统计算：

- MP Time Window (Auto)：权威计算结果。
- MP Month (Auto)：用于分组和筛选。
- Project duration(Auto)：项目周期。
- MP Gap Analysis(Auto)：计划MP与当前MP的差异提示。

规则：日期和公式只能提示风险，不能自动修改Project Status。

### 04 责任人与团队

Project列表／详情顶部优先显示：

- NPI Owner (Manual)
- PMO Owner (Manual)
- NPD Owner(Manual)
- SC Owner (Manual)

按需在“Project Team”区域显示，不在主Grid全部展开：

- EE Owner (Manual)
- DQTP Owner (Manual)
- Compliance Owner (Manual)
- CMF Owner (Manual)
- Quality Owner (Manual)
- PD Owner (Manual)
- ENG Owner (Manual)
- Package Owner (Manual)
- Planning Owner (Manual)
- ID Owner(Manual)
- ME Owner(Manual)
- VAVE Owner(Manual)
- Tooling Owner (Manual)
- On-side Quality Owner(Manual)

CSV显示：NPI约79%、SC约71%、NPD约24%、PMO约15%有值；其余职能Owner多数不足1%。这些字段不是立即删除对象，但继续横向增加会让Projects失控。

中期建议建立 Project Team Assignments：Project、Person、Role、Function、Primary、Active。完成迁移前保留现有Owner字段，迁移后仅保留四个核心Owner作为快捷显示。

### 05 计划与里程碑

Project顶部保留的关键日期：

- Start Date (Manual)：项目启动／Award口径。
- Kick Off Date (Manual)：正式Kickoff，与Start Date含义不同。
- Planned MP Date (Manual)：批准／基准MP日期。
- MP Start Date (Manual)：当前预计或实际MP日期，需在业务定义中明确“forecast还是actual”。
- Previous MP Start Date：历史已使用字段；迁移后与Previous MP Date只保留一个明确口径。
- DQTP Finish Date (Manual)
- Compliance Complete Date (Manual)
- MP AW Date (Manual)

详细里程碑缓存，仅在 Milestone Cache / Integration View 显示：

- Original TRA Date
- P1 CAD DROP、P1 BUILD DATE
- P2 CAD DROP、P2 BUILD DATE
- P3 CAD DROP、P3 BUILD DATE
- Last P BUILD DATE、Last P Date
- TRA Date
- Cut Steel Date
- FOT Date
- EB1 Date、EB2 Date、EB3 Date
- Tooling Transfer Load Date
- Tooling Transfer Arrival Date
- Pilot Date
- MPRA Date

这些详细日期正在与Tasks主计划、Weekly Report导入和All Tracker导出重叠。短期不能删除。目标口径应是：

- Tasks.Start Date = Project主计划节点的权威日期；
- SKU Milestone Plans = Project SKU的继承／独立日期；
- Projects详细日期列 = 仅作为兼容缓存，明确由系统同步，员工不再双重维护；
- 等导入和导出工具全部改为读取Tasks／SKU Milestone Plans后，再决定删除缓存列。

需要澄清后合并：

- Previous MP Start Date 与 Previous MP Date；后者当前为空，不能在未查导入脚本前直接删。
- Original TRA Date 与 TRA Date：如分别表示baseline/current则都保留；否则合并。
- Date Added：当前为空，确认无导入依赖后移到Import Runs或删除。

### 06 执行、问题与进度

正式关系：

- Tasks (system manage)
- Issues (system manage)

Project级高价值汇总：

- Open Task Count (Auto)
- Open Issue Count (Auto)
- Open Critical Issue (Auto)
- Total Task Count (Rollup)
- Completed Task Count (Rollup)
- Completion % (Formula)

需要修复或收缩：

- Open Critical Tasks（Auto）：线上Rollup无效，不能显示为可靠指标。修复正确来源；若与重要任务视图重复则删除。
- Project Progress Bar (Auto)、Total Task Count (Auto)、Completed Task Count (Auto)、Project Completion % (Auto)、Progress Bar (Formula)：与现有Rollup／Formula重复。统一使用三个权威字段：Total Task Count (Rollup)、Completed Task Count (Rollup)、Completion % (Formula)。其余先隐藏，完成依赖审计后删除。
- Key Issue (Manual)：与Issues表重复。停止新写，迁移有效内容到Issues后删除。
- Milestones (system manage)：普通文本、CSV完全为空，与Tasks.Milestone和SKU Milestone Plans重复，列为高优先级删除候选。
- Key issue impact MP(Auto)、Key issue Recovery action(Auto)、Root cause(Auto)、Key issue status(Auto)、Key issue owner(Auto)：这些是Issues内容的重复展开，且覆盖率低。Project页面应显示关联Issues列表，不应把五个多值Rollup长期铺在Projects主表。先从用户Views隐藏，确认无公式／Automation依赖后删除。

### 07 周报、沟通与资料入口

员工／导入工具维护：

- Update This Week (Manual)：本周关键变化和结论。
- Current Progress (Manual)：当前工作进展；与Update This Week分开，因为原周报本身就是两个区块。
- Tooling (Manual)：稳定的Tooling说明。
- Weekly Report Update Date (System)：本周内容的来源日期，作为正式周报版本日期。

系统时间：

- Last Modified：任何字段发生变更的系统时间。

待收缩：

- Last updated(Manual）：旧人工更新时间，改由Weekly Report Update Date (System)承担后退役。
- Weekly Report Update Date (Manual)：当前为空；如果没有明确人工Override场景，确认依赖后删除。

资料链接按需显示，有值才出现在Interface：

- ECN URL (Manual)
- Jira URL (Manual)
- Teams Channel URL (Manual)
- SharePoint Folder URL (Manual)
- PIS(Manual)
- DQTP URL(Manual)
- Sample plan URL (Manual)：只有1条数据，优先合并到统一资料入口或退役。

### 08 自动化、导入与审计

全部隐藏在Admin Views，不进入员工Project页面：

- Tasks Generated (system manage)
- Schedule Import
- Schedule Import 2
- Import File (System)
- Import Status (system)
- Import Note (system)
- Import Result Count(system)
- Data Quality Note (Audit)
- Generate Weekly Email
- Email Recipients

长期建议：Import File、Status、Note、Result Count放在独立Import Runs记录中，Projects只关联“Last Import Run”和保留Weekly Report Update Date。通知对象应从People／Project Team关系生成，避免手填Email Recipients。

## 四、需要新增什么

Projects当前不缺新的普通业务字段。优先完成现有关系迁移：

1. Project SKUs：已新增，用来表达一个Project × 一个SKU的执行实例。
2. Project Team Assignments：中期新增，用来收敛十几个职能Owner字段；本轮不急着创建。
3. Last Import Run：只有在Import Runs表完成后再增加一个Link，不先建空字段。

Next Milestone、Next Milestone Date、At Risk SKU Count 等可作为Interface需要的派生字段，但必须等Interface确认无法直接汇总时再增加，不能为了“也许要显示”继续堆字段。

## 五、删除／合并优先级

### 第一批：先隐藏并做依赖检查

- Milestones (system manage)
- Key Issue (Manual)
- Open Critical Tasks（Auto，无效）
- Project Progress Bar (Auto)
- Total Task Count (Auto)
- Completed Task Count (Auto)
- Project Completion % (Auto)
- Progress Bar (Formula)
- 五个Key issue Rollup字段
- Weekly Report Update Date (Manual)
- Last updated(Manual）
- Sample plan URL (Manual)
- Schedule Import（文本版）

### 第二批：完成迁移后再退役

- Project SKU (Manual)
- PMO SKU (Link)（待Project SKUs成为正式关系后）
- Brand、Sub Category、Launch Target等人工产品属性
- 详细Project里程碑缓存列
- 十几个低使用率职能Owner字段
- Import File／Status／Note／Result Count

任何删除前必须检查：Formula、Lookup、Rollup、Automation、Interface、导入工具、All Tracker导出工具和API脚本。字段为空不等于可以删除。

## 六、推荐的Data Views

### 01 Project Core

Project ID、Project name、Project Status、Current Gate、Project Type、PMO Program、Project SKUs、Region、Factory、NPI Owner、PMO Owner、Planned MP Date、MP Start Date。

### 02 Weekly Update

Project ID、Project Status、Update This Week、Current Progress、Weekly Report Update Date (System)、NPI Owner、PMO Owner、Open Critical Issue、Open Task Count、Issues、Tasks。

### 03 Project Team

Project ID、NPI、PMO、NPD、SC，以及其他职能Owner、Project People。

### 04 Milestone Cache

Project ID、Start、Kick Off、Planned MP、MP Start、Previous MP、DQTP、Compliance、MP AW以及全部详细里程碑缓存。该View供导入、核对和导出，不作为日常项目页面。

### 05 Links and Documents

Project ID、ECN、Jira、Teams、SharePoint、PIS、DQTP、Sample plan。

### 90 System Relations

Project ID、所有Link、Lookup、Rollup、模板关系、Tasks Generated。

### 91 Import and Audit

Project ID、Schedule Import、Import File、Status、Note、Result Count、Data Quality Note、Last Modified。

### 99 Cleanup Candidates

集中显示所有准备合并／退役字段，方便迁移和依赖审计。禁止员工在该View继续填写。

## 七、Project Interface 的显示顺序

### Project List

只显示：Project ID／Name、Status、Current Gate、Program、NPI Owner、Factory、SKU数量、MP Start、需关注Issue数。

### Project Detail

1. 顶部：Project ID／Name、Status、Gate、Program、Project Type。
2. 责任人：NPI、PMO、NPD、SC、Factory；其他角色折叠。
3. 主计划：从Tasks展示关键里程碑，不直接铺全部Project日期列。
4. Project SKU：SKU、Supplier／Factory、SKU Status、独立日期数。
5. Issues与Important Tasks：直接显示关联列表。
6. Weekly Update：Update This Week、Current Progress、来源日期。
7. 资料入口：只显示有值的链接。
8. Admin区域：导入、审计和系统字段，不向普通员工展示。

## 八、维护责任

| 内容 | 权威位置 | 维护者 |
|---|---|---|
| Project Status、Gate、Weekly Update | Projects | Project Owner／NPI |
| Project主计划里程碑 | Tasks | Project计划负责人 |
| SKU在某Project下的Status | Project SKUs | 对应项目／SKU负责人 |
| SKU独立日期与原因 | SKU Milestone Plans | 对应SKU负责人 |
| Issue和Recovery Action | Issues | Issue Owner |
| Program产品信息 | PMO Roadmap Programs | PMO |
| SKU产品主数据 | PMO SKUs | PMO／PLM来源 |
| 进度、数量、差异、日期来源 | Formula／Lookup／Rollup | 系统 |
| 导入结果和数据质量 | Import Runs／Audit字段 | 导入工具／管理员 |

最终原则：员工只维护判断、承诺和事实；关系、汇总、提醒和显示由系统完成。同一事实不得在Projects、Tasks、Issues、SKU和周报字段中重复人工维护。
