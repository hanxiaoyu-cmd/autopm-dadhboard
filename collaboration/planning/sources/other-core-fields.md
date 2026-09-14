# AutoPM 其他核心表字段架构与显示规划

更新日期：2026-09-06  
检查范围：Airtable 线上 schema、PMO Roadmap Programs / PMO SKUs / Tasks / Issues 导出 CSV，以及已经建立的 Project SKUs / SKU Milestone Plans 样本。  
配套文件：`Projects_Field_Architecture_Plan.md`。本文件不重复规划 Projects。

## 一、核心结论

目前的其他核心表已经具备 AutoPM 所需的大部分业务信息，不需要再大规模增加字段。真正要解决的是：

1. `PMO SKUs` 同时承担产品主数据和 Project 执行信息，职责混杂；
2. `People` 有大量历史反向关系和重复关系，日常维护入口不清楚；
3. `Tasks` 同时承担普通行动项和 Project 主计划里程碑，需要靠分类和 View 分开；
4. `Issues` 已有问题闭环骨架，但缺少“影响说明、最新进展、是否升级”三个高价值字段；
5. `Project SKUs` 与 `SKU Milestone Plans` 的方向正确，它们是解决“一款 SKU 多个供应商 Project、主计划继承、单 SKU 独立调整”的关键；
6. Program、Project、SKU 的重复产品信息不应在每层重复显示；下层只表达相对上层新增的信息或例外。

第一阶段原则：不急着删除；先划分模块、确定权威字段、建立 Views、隐藏后台字段。所有删除必须先检查 Formula、Lookup、Rollup、Automation、Interface、导入工具和 All Tracker 导出工具。

## 二、统一关系与权威来源

```text
PMO Roadmap Programs（PMO定义的产品平台）
  └── Projects（一次具体项目执行）
        ├── Project SKUs（一个Project × 一个SKU的执行实例）
        │     ├── PMO SKUs（PMO/PLM定义的SKU主数据）
        │     ├── SKU Milestone Plans（该执行实例的里程碑日期）
        │     │     └── Master Task（继承Project主计划）
        │     └── Issues（只影响该Project SKU的问题）
        ├── Tasks（行动项 + Project主计划里程碑）
        ├── Issues（Project级问题）
        ├── People（负责人和项目成员）
        └── Factories（Project默认工厂）
```

权威位置：

| 业务事实 | 权威表 |
|---|---|
| Program名称、代码、品牌、品类、上市规划 | PMO Roadmap Programs |
| SKU编码、市场、认证、PLM属性 | PMO SKUs |
| Project整体状态、Gate、主计划、本周更新 | Projects + Tasks |
| 某SKU在某Project/供应商下的状态 | Project SKUs |
| SKU继承或独立调整后的里程碑日期 | SKU Milestone Plans |
| 任务责任、时间和完成情况 | Tasks |
| 问题、根因、恢复动作和关闭结果 | Issues |
| 人名、邮箱、部门、协作者身份 | People |
| 工厂名称、代码、国家和状态 | Factories |

字段治理标签统一使用：

- `KEEP-CORE`：员工维护的权威业务字段；
- `KEEP-RELATION`：正式关联关系；
- `KEEP-SYSTEM`：公式、Lookup、Rollup或系统生成；
- `HIDE-ADMIN`：保留，但只在后台View显示；
- `REVIEW-MERGE`：与其他字段重叠，迁移后合并；
- `REVIEW-DELETE`：依赖检查后可删除；
- `ADD-LATER`：有明确价值，但不在未确认需求前创建。

---

## 三、PMO Roadmap Programs

### 3.1 职责边界

Program 是 PMO 定义的稳定产品平台，不是日常 Project 周报。它回答：这是什么产品平台、由谁负责、计划在哪些市场上市、下面有多少 Project/SKU、整体是否需要关注。

Program 不应保存：单个 Project 的详细时间表、单个 SKU 的执行状态、Issue 长文本、Task 明细。

### 3.2 当前覆盖评价

当前 50 个字段已充分覆盖 Program 身份、分类、负责人、阶段目标、区域/渠道上市日期和下属 Project。151 条导出记录中，核心身份、状态、目标、PMO/PD Lead、数量字段基本都有值；Program Image 覆盖约74%，Projects Link约62%。主要问题不是缺字段，而是负责人均为文本、三类目标为文本、20个上市日期平铺，以及数量Rollup需要验证口径。

### 3.3 建议模块

#### 01 Program身份与产品分类

`KEEP-CORE`：

- Program_Name
- Program_Code
- ALE_ID
- Program_Aliases
- Brand
- Category
- Sub_Category
- Launch_Year_Projection
- Program_Image

规则：Program_Code 与 ALE_ID分别保留业务代码和系统/PMO标识；不得用名称做唯一匹配。Program Image作为 Program Gallery 的默认封面。

#### 02 状态与战略时间

`KEEP-CORE`：

- Program_Status
- Milestone_Status
- TRA_Target
- MP_Target
- Launch_Target

建议：明确这些字段是 PMO Source，普通 Project 成员只读。若源数据能够稳定提供真实日期，再逐步把文本目标标准化为日期；不要在不确定格式时强制转换。

Program Status 是人工/PMO判断，不由下属Project状态自动覆盖；系统只计算风险提示。

#### 03 正式关系与组合统计

`KEEP-RELATION`：

- Projects ID (Link)

`KEEP-SYSTEM`：

- Project quantity
- SKU Models
- SKU Quantity

需要修正：

- Project quantity 应统计正式 Projects Link；
- SKU Quantity 最终应通过 `Projects → Project SKUs` 统计执行SKU，而不是拼接多个Project中的数字；
- SKU Models 与 SKU Quantity 必须区分“唯一产品型号数”和“Project SKU执行实例数”；
- 新增 Risk Project Count 只有在 Interface 无法直接按关联Project状态统计时才考虑。

#### 04 Program负责人

当前字段：PMO_Lead、PD_Lead、Comm_Lead、Eng_Lead、ID_Lead、CMF_Lead、TPMO_Lead、CI_Lead、Compliance_Lead、Supply_Planning_Lead、Supply_Chain_Lead、NPI_Lead。

短期：全部保留为 PMO 导入文本，在详情页按职能分组，不在Gallery Card展开。  
中期：People清理完成后，只为需要通知、权限或“My Work”的Lead增加People Link；不要一次创建12个新的链接字段。

#### 05 上市日历

当前20个日期字段覆盖 US / CA / MX / UK / EU × DTC / Amazon / Rcom / InStore。

建议：

- 全部保留在 `Launch Calendar` 后台View；
- Program详情只显示有值且未来最近的市场日期；
- 不在Program Card显示20个日期；
- MX_Rcom、MX_Amazon、MX_InStore、EU_Amazon目前覆盖率低，但低覆盖不等于无价值；
- 只有当市场/渠道继续扩展且需要跨Program分析时，才考虑拆成 `Program Launch Events` 子表。本轮不新建。

### 3.4 推荐Views与Interface

- `01 Program Core`：Name、Code、Brand、Category、Sub Category、Status、Launch Target、Image。
- `02 Portfolio Status`：Program、Status、Project Count、SKU Models、SKU Execution Count、风险提示。
- `03 Program Owners`：所有Lead文本/链接。
- `04 Launch Calendar`：20个区域渠道日期。
- `90 Relations & Rollups`：Project Link、数量及校验。

Program Card只显示：图片、Program Name、Brand、Category、Launch Target、Program Status、Project数、SKU执行数、需关注Project数。

---

## 四、PMO SKUs

### 4.1 职责边界

PMO SKUs 是 PMO/PLM 定义的产品主数据。它回答：这是哪个SKU、属于哪个Program、面向哪个市场、认证SKU是什么、主型号和供应商主数据是什么。

它不应回答：该SKU在某一个供应商Project中的状态是什么、某Project的24个日期是什么。一个产品SKU可以出现在多个供应商/Project中，这些执行差异必须放在 Project SKUs 和 SKU Milestone Plans。

### 4.2 当前覆盖评价

当前41个字段足以描述SKU主数据，但结构明显失衡：9937条导出记录中，约一半以上字段是从Projects直接Lookup的日期。由于同一个SKU可能关联多个Project，这些Lookup会产生多值、顺序不稳定和语义不明确。`SKU Status (Manual)`放在PMO SKU也无法表达同一个SKU在不同供应商Project中的不同状态。

### 4.3 建议模块

#### 01 SKU身份

`KEEP-CORE`：

- DEV_SKU（主显示名称）
- Auth_SKU
- Master_Item
- SKU_ID (from SKU From PLM 2)
- Is_Authenticated
- Market
- Color(Manual)（有明确使用场景才维护）

建议新增：`PMO Program (Link)` → PMO Roadmap Programs。当前只有Program_Code文本，不足以形成稳定的Program→SKU关系。

#### 02 PMO / PLM来源

`KEEP-RELATION`：SKU From PLM 2。  
`KEEP-SYSTEM`：BaseModel、Supplier等PLM Lookup。  
`KEEP-CORE / IMPORT RAW`：Program_Code、ALE_ID。

Program Link建立后：Brand、PMO_Category、Sub_Category改为从Program读取或仅作为导入核对字段，不再由员工重复维护。

#### 03 Project执行关系

正式关系：

- Project SKUs：`KEEP-RELATION`，长期权威关系；
- Projects ID：`REVIEW-MERGE`，迁移期交叉核对；不能继续作为“SKU只属于一个Project”的假设。

`SKU Status (Manual)`：停止新维护，状态迁移到 `Project SKUs.SKU Status (Manual)`。当前字段暂不删除，先从日常View隐藏。

#### 04 Project日期副本

以下从Projects Lookup的字段统一归入 `Legacy Project Date Lookups`：

- Region、Start、MP Start、Planned MP、Original TRA
- P1/P2/P3 BUILD、Last P BUILD
- TRA、Cut Steel、FOT、EB1/EB2/EB3
- Tooling Transfer Load/Arrival、Pilot、Date Added、MPRA、Previous MP、Last P

治理结论：

- 不在SKU详情页继续展示这些多值Lookup；
- 页面需要显示日期时，从 `Project SKU → SKU Milestone Plans.Effective Date` 展示；
- 只有与某一Project执行实例明确绑定后，日期才有意义；
- 等Project SKUs全量迁移、Interface和导入导出工具切换后，再批量退役这些Lookup。

### 4.4 推荐Views与Interface

- `01 SKU Master`：DEV_SKU、Auth_SKU、Master Item、Market、Program、Authenticated。
- `02 PLM Reconciliation`：PLM Link、SKU ID、BaseModel、Supplier、ALE ID、Program Code。
- `03 Project Assignments`：SKU、Project SKUs、旧Projects ID核对。
- `90 Legacy Project Date Lookups`：所有旧日期Lookup，仅管理员。
- `99 Cleanup Candidates`：旧SKU Status、人工Brand/Category、日期副本。

SKU Master Detail只显示产品主数据和关联Project SKUs；不重复Program图片、Brand、Category，也不直接铺Project日期。

---

## 五、Project SKUs

### 5.1 职责边界

Project SKUs 是执行关系表，一条记录代表“某一个Project中的某一个SKU”。它不是新的SKU主数据表。

它解决：

- 同一个产品SKU可参与不同供应商Project；
- 同一个Project可包含多个SKU；
- 每个执行实例可以拥有独立Status、Factory、Issue和日期例外。

### 5.2 当前覆盖评价

当前9个字段已经具备最小可用骨架：Project、SKU、Status、唯一键、Issues、Factory文本、Notes、Plans反向关系。结构方向正确，但只完成了SXA0061的3条样本，尚未全量推广。

### 5.3 建议模块

#### 01 唯一身份与正式关系

- Assignment Name：系统生成显示名，例如 `SXA0061 · FW575PK1`；员工不维护。
- Project：正式单记录链接，`KEEP-RELATION`。
- SKU：正式单记录链接，`KEEP-RELATION`。
- Unique Key：`Project record ID + SKU record ID`，`KEEP-SYSTEM`。

字段层和脚本层都应强制 Project / SKU 为单记录链接。

#### 02 SKU执行状态

- SKU Status (Manual)：`KEEP-CORE`；只表示该SKU在该Project下的人工判断。
- Notes：改名或明确为 `SKU Execution Note (Manual)`，只写稳定说明。

建议仅在确有需要时新增：

- `Status Reason / Latest Update (Manual)`：当Status为At Risk/Delayed时写一句当前原因；
- `Execution Owner` → People：只有SKU确实有独立负责人时增加，不复制Project默认Owner。

#### 03 工厂/供应商

当前 `Factory / Supplier (Manual)` 是文本。建议在Factory主数据清理完成后改为或新增 `Factory / Supplier (Link)` → Factories；文本字段保留为导入原文，完成迁移后退役。

规则：Project.Factory是默认值；Project SKU只有与Project不同或需要明确供应商执行实例时才单独维护。

#### 04 Issues与里程碑

- Related Issues：只关联影响该执行SKU的问题；Project公共问题直接留在Project级。
- SKU Milestone Plans：系统生成的反向关系；员工不在此字段手动增删。

可选系统指标，仅在Interface需要时添加：

- Independent Milestone Count
- Missing Milestone Count
- Open Issue Count
- Next Effective Milestone / Date

不要为了“可能会显示”一次性创建这些字段。

### 5.4 推荐Views与Interface

- `01 Active Assignments`：Assignment、Project、SKU、Status、Factory、Open Issues。
- `02 Status Update`：只显示员工要维护的Status、Status Reason、Owner。
- `03 Milestone Exceptions`：独立日期数、缺日期数、关联Plans。
- `90 Relationship Audit`：Unique Key、Project、SKU、计划数、数据质量。

Project页面的SKU列表只显示：SKU、Market、Factory/Supplier、SKU Status、独立日期数、需关注Issue数。点击后打开侧边详情，不跳离Project页面。

---

## 六、SKU Milestone Plans

### 6.1 职责边界

一条记录代表“一个Project SKU执行实例 × 一个Project主计划里程碑”。它只保存继承关系和例外，不复制一套新的主计划。

### 6.2 当前覆盖评价

当前13个字段已基本完整，三层机制清楚：Master Task / Master Date → Override Date → Effective Date。现有33条样本全部通过关系验证。主要需要收口的是旧SKU直链、Relationship Check命名，以及人工修改入口。

### 6.3 建议模块

#### 01 身份与来源

- Plan Name：系统生成，员工不维护。
- Project SKU：正式单记录链接。
- Master Task：正式单记录链接，只能选择同一Project的里程碑Task。
- Unique Key：`Project SKU record ID + Master Task record ID`。
- Milestone：从Master Task Lookup，只读。

旧 `SKU` Link：迁移核对字段。全量迁移并验证后退役，避免Project SKU和SKU两条关系不一致。

#### 02 日期继承与覆盖

- Master Date：Lookup `Tasks.Start Date (Manual)`；定义为Project主计划里程碑日期。
- Override Date：员工只在该SKU日期不同于主计划时填写。
- Effective Date：`IF(Override Date, Override Date, Master Date)`。
- Plan Source：Inherited / Independent / Unscheduled。
- Adjustment Reason：只要填写Override Date，就必须填写原因。

多个日期发生变化时，每个里程碑各有一条Plan记录，因此分别填写各自Override Date和原因，不把多个日期塞进一个字段。

#### 03 问题关联与校验

- Related Issues：只链接造成该里程碑例外的问题。
- Relationship Check：当前只检查字段是否填充，建议改名 `Link Presence Check (System)`，避免把POPULATED误解为“关联正确”。
- 真正的Project/SKU/Task一致性由初始化/审计脚本按record ID检查。

建议新增规则而非字段：Override Date有值但Adjustment Reason为空时，标红并禁止进入正式周报。

### 6.4 推荐Views与Interface

- `01 Effective Plan`：Project SKU、Milestone、Master Date、Override Date、Effective Date、Source。
- `02 Independent Adjustments`：只显示Source=Independent。
- `03 Missing Dates`：Source=Unscheduled。
- `04 Adjustment Review`：Override、Reason、Related Issues。
- `90 Relationship Audit`：Unique Key、旧SKU Link、Project SKU、Master Task、Link Presence。

员工默认只看到：Milestone、主计划日期、独立日期、生效日期、来源、原因、恢复继承按钮。

---

## 七、Tasks

### 7.1 职责边界

Tasks回答：“谁在什么时间完成什么”。同一张表可同时存普通行动项和Project主计划节点，但必须通过Milestone标签和Views分离。

Task不保存Issue完整分析，不直接自动修改Project Status，也不保存SKU独立日期。

### 7.2 当前覆盖评价

当前37个字段已覆盖任务身份、Project、Owner、起止日期、完成度、优先级、里程碑、Gate、Issue、依赖和CPM。5004条导出任务中，Project、Due Date和Owner覆盖约99%以上，Milestone覆盖约84%。不足是缺少明确的人工异常状态，完成度算法对多Owner任务较复杂，CPM和依赖字段仅少量使用。

### 7.3 建议模块

#### 01 任务身份与范围

- Task Name (Manual)：`KEEP-CORE`。
- Task ID (Auto)：稳定系统ID，用于导入和去重。
- Projects (system manage)：正式单Project链接。
- Project ID Lookup：只读显示。
- Issues (system manage)：相关Issue，可选。
- Deliverables (Manual)：有值才显示。

#### 02 时间与责任

- Start Date (Manual)
- Due Date (Manual)
- Tasks Owners (Manual)
- Completed By (Manual)
- Department (Auto)
- Priority (Manual)
- Last Modified

规则：Owner与Completed By都使用People关系；Collaborators只用于Airtable账号协作，不作为业务Owner的第二套来源。

#### 03 状态与完成

现有系统字段：Task Completion、% Complete、Completion Status、Owner Count、Completed Count、Is Completed。

治理建议：

- `Task Completion (Auto)`作为日期/责任信号；
- `Is Completed (System)`作为统一完成布尔值；
- `% Complete`仅在“每个Owner分别确认完成”这一业务规则成立时保留；
- Completion Status与Is Completed含义重复，依赖检查后合并；
- 增加 `Task State (Manual)` 仅用于 Blocked / Cancelled / Not Applicable 等公式无法判断的例外；不要用Automation自动改它。

#### 04 计划分类

- Milestone (Manual)：固定选项，只有已批准的标准里程碑才填写。
- Phase (Manual)
- Gate (Manual)
- Is Delivery (Auto)
- Is Critical Path (Auto)

普通日期任务可以导入Tasks但不标Milestone。Milestone Task的Start Date是SKU计划继承的权威日期。

#### 05 依赖与CPM

- Depends On、反向Depends On
- Est. Duration、CPM Source、CPM ES/EF/Float
- Duration for Start Date

当前覆盖率不足1%，全部放在 `CPM / Advanced Planning` 后台View。不能因使用率低直接删除，但不进入普通员工页面。

#### 06 后台与审计

- Data Quality Note (Audit)
- Task Count Helper
- System Knowledge & Progress
- SKU Milestone Plans（反向关系）

全部隐藏在Admin View。

### 7.4 推荐Views与Interface

- `01 My Open Tasks`：Task、Project、Owner、Start、Due、Priority、Health。
- `02 Due This Week`
- `03 Overdue / Blocked`
- `04 Project Master Milestones`：只显示Milestone非空。
- `05 Issue Recovery Tasks`
- `90 CPM & Dependencies`
- `91 System & Audit`

Task Detail只让员工维护：Task Name、Project、Owner、Start/Due、Priority、例外状态、完成确认、相关Issue。

---

## 八、Issues

### 8.1 职责边界

Issues是一处维护、多处显示的问题中心。它回答：发生了什么、影响什么、为什么、谁采取什么动作、何时完成、是否关闭。

同一Issue可以影响一个Project中的多个Project SKU，不应为每个SKU复制一条Issue。

### 8.2 当前覆盖评价

当前25个字段已覆盖问题闭环主干。400条导出记录中，Issue、Status、Recovery Action和Project覆盖率高，Severity约79%、Owner约67%、Target Date约54%。缺口集中在业务影响说明、最新进展和升级标记；同时存在两个完全为空的Projects文本字段。

### 8.3 建议模块

#### 01 问题身份与影响范围

- Issue ID (Auto)
- Issue Record (Manual)：一句话问题标题，不写整篇分析。
- Projects (system manage)：正式Project链接。
- Project SKUs：需要精确到执行SKU时关联，可多选。
- Related Tasks：恢复行动拆成任务时关联。
- SKU Milestone Plans：问题直接影响某个里程碑例外时关联。
- Record Date (Manual)

`Project SKU (Auto)` Lookup只用于显示旧关系；正式范围应使用Project SKUs直接链接。

#### 02 分类与影响

- Issue Status (Manual)
- Severity (Manual)
- Category (Manual)
- Impact MP date (Manual)
- Impacted Gate (Manual)

建议新增：`Business Impact (Manual)`（Long text），描述对MP、质量、成本、产能或市场的实际影响。不要只靠Impact MP checkbox表达全部影响。

#### 03 分析与恢复

- Root Cause (Manual)
- Recovery Action (Manual)
- Recovery Owners (Manual)
- Target Date (Manual)：统一定义为当前Recovery承诺日期。
- Related Tasks：复杂Recovery应拆成多个Task，Issue内保留结论。

#### 04 进展、升级与关闭

建议新增：

- `Latest Update (Manual)`：本周最新进展，只保存当前结论；
- `Escalation Needed (Manual)`：人工勾选，需要管理层/跨部门推动时使用。

保留：Closed Date、Last Modified。  
规则：关闭Issue必须有Closed Date；关闭后不自动修改Project Status。

#### 05 资料与后台

- Jira link：有值才显示。
- Data Quality Note (Audit)、System Knowledge & Progress：后台。
- Projects、Projects 2：CSV为0值的文本遗留字段，列为第一批 `REVIEW-DELETE`；依赖检查通过后删除。

### 8.4 推荐Views与Interface

- `01 Open Issues`
- `02 Critical / MP Impact`
- `03 My Recovery Actions`
- `04 Escalation Needed`
- `05 Closed This Month`
- `90 Missing Owner / Action / Date`
- `99 Cleanup Candidates`

Project页面直接显示关联Issue列表：标题、Severity、Status、Owner、Target Date、Latest Update；点击侧边详情再看Root Cause和完整Recovery。

---

## 九、People

### 9.1 职责边界

People是人员主数据和所有Owner、邮件提醒、部门筛选、My Work的基础。它只维护“一名真实人员的一份身份”，不把每个Owner角色复制成新的人员记录。

### 9.2 当前覆盖评价

当前44个字段中，真正需要员工/管理员维护的核心身份字段不到10个，其余大部分是Projects/Tasks/Issues的反向链接或历史重复关系。信息覆盖足够，但结构最需要治理。

### 9.3 建议模块

#### 01 人员身份

- Person Name (Manual)
- Email (Manual)：建议作为去重和通知的主要业务键。
- Department (Manual)
- Primary Function (Manual)
- Title (Manual)
- Location (Manual)
- Status (Manual)：Active / Inactive。
- Line Manager (Manual)：中期从文本改为People Link。

建议新增系统字段：`Normalized Email / Person Key`，用于大小写、空格规范化和去重；不向普通用户显示。

#### 02 Airtable账号与通知

- Collaborator (Manual)
- Receive Daily Reminder (Manual)

规则：People记录可以没有Airtable账号，但只要Email有效，就应能通过外部邮件动作收到任务通知。Collaborator不等于业务Owner。

#### 03 正式业务关系

- Project(Manual)：统一项目成员浏览关系。
- Tasks Owner、Issues Owner：正式反向关系。
- NPI/PMO/EE/DQTP/Compliance/CMF/SC/Quality/PD/ENG/Package/Planning Owner Projects：角色字段的反向链接，`KEEP-BACKEND`，不在People日常Grid横向展开。

#### 04 工作量汇总

- Project count (Auto)
- Open Tasks (Auto)
- Overdue Tasks (Auto)

需要校验：Project count必须基于统一项目关系，不应只统计某一个Owner角色。

#### 05 历史重复关系

以下字段统一进入 `People Legacy Relations`：

- Person Name selection (Manual)及copy/From field版本
- Project Members (system manage)文本
- Projects、Projects 2、Projects 3、Projects 4、Projects 5、Projects 6、Projects 7、Projects 8
- Schedule Import

处理原则：先确定每一列的来源、记录数和被哪些Automation/Interface引用；把有效链接合并到统一Project关系后再删除。禁止按字段名相似直接合并人员。

#### 06 数据质量

- Data Quality Note (Audit)

必须检查：空名字、重复姓名、重复邮箱、非法邮箱、部门缺失、Inactive仍有开放任务、Collaborator与Email不一致、部门名或角色名被误建成人员。

### 9.4 推荐Views与Interface

- `01 Active People`：Name、Email、Department、Function、Title、Location、Manager。
- `02 Reminder & Access`：Email、Collaborator、Receive Reminder、Status。
- `03 Workload`：Project Count、Open Tasks、Overdue Tasks、Open Issues。
- `04 Project Membership`
- `90 Role Reverse Links`
- `91 Data Quality`
- `99 Legacy Relations`

People Detail只显示：身份、部门/职能、联系方式、当前Project、开放Task/Issue和提醒设置。

---

## 十、Factories

### 10.1 职责边界

Factories是工厂/供应商主数据，避免Projects和Project SKUs反复写不同拼法。

### 10.2 建议模块

#### 01 工厂身份

- Factory Full Name (Manual)：正式名称。
- Factory ID (Manual)：外部系统ID；如没有独立来源，不与Factory code重复维护。
- Factory code：短代码。
- Country (Manual)
- Status (Manual)

可选：Supplier Group，只有集团与工厂层级确实不同且需要分析时增加。

#### 02 联系方式

- Contact Person (Manual)
- Contact Email (Manual)

外部供应商联系人不必强行进入内部People表。

#### 03 项目关系

- Projects (system manage)：Project默认工厂反向关系。
- 建议Project SKUs增加正式Factory Link后，由Airtable自动生成执行实例反向关系。

`Factory name (Old)`：迁移到正式名称后列为 `REVIEW-DELETE`。

### 10.3 推荐Views

- `01 Active Factories`
- `02 Factory Projects`
- `03 Contacts`
- `90 Duplicate Name / Code Audit`
- `99 Legacy Fields`

---

## 十一、跨表字段分工：员工维护与系统维护

| 表 | 员工/业务维护 | PMO/管理员维护 | 系统自动维护 |
|---|---|---|---|
| Programs | 不建议普通员工维护 | 身份、分类、状态、目标、Lead、上市日历 | Project/SKU数量、风险提示 |
| PMO SKUs | 原则上只读 | SKU/PLM主数据、Program映射 | Lookup、Project SKU反向关系 |
| Project SKUs | SKU Status、例外说明、必要的执行Owner/Factory | 创建/校验Project×SKU关系 | Unique Key、计划数、风险汇总 |
| SKU Milestone Plans | Override Date、Adjustment Reason | 处理歧义和数据质量 | Master Date、Effective Date、Source |
| Tasks | Task、Owner、日期、优先级、完成确认、例外状态 | Milestone/Gate标准 | Health、完成信号、数量、CPM |
| Issues | 问题、影响、根因、Recovery、Owner、日期、进展、关闭 | 分类标准、升级规则 | ID、缺失项提示、汇总 |
| People | 个人提醒偏好 | 身份、邮箱、部门、状态、账号映射 | 工作量和反向关系 |
| Factories | 少量联系人更新 | 名称、代码、国家、状态 | Project/Project SKU反向关系 |

统一原则：员工维护判断、承诺、原因和完成事实；系统维护关系、继承、计算、提醒和显示。任何事实只允许一个人工权威入口。

## 十二、建议的实施顺序

### Phase 1：先整理Views，不删除

1. 为上述各表建立01/02/90/99分类Views；
2. 主View只放员工真正需要的字段；
3. 系统、反向链接、审计、旧字段全部移动到后台Views；
4. 给字段Description写明Source、Maintainer和Do Not Write规则。

### Phase 2：建立正式关系

1. PMO SKUs增加Program Link并校验Program Code；
2. Project SKUs从SXA0061样本逐Project dry-run推广；
3. Project SKUs的Factory从文本迁移为Factories Link；
4. Project/SKU/Master Task等单记录链接在字段层关闭多选。

### Phase 3：迁移重复事实

1. SKU Status迁移到Project SKUs；
2. SKU独立日期迁移到SKU Milestone Plans；
3. Issues增加Business Impact、Latest Update、Escalation Needed；
4. People有效Project关系合并到统一关系；
5. Tasks统一完成状态口径。

### Phase 4：切换Interface和Automation

1. Program页面读取Program+Projects；
2. Project页面读取Project SKUs、Tasks、Issues；
3. SKU执行详情读取SKU Milestone Plans；
4. My Work读取People→Tasks/Issues；
5. 更新导入/All Tracker工具读取新的权威关系；
6. 完成依赖测试后才隐藏或退役旧字段。

### Phase 5：删除候选

优先审计：

- Issues：Projects、Projects 2文本字段；
- People：Projects 2–8、self-link/copy字段、旧文本关系；
- PMO SKUs：旧SKU Status和Project日期Lookup；
- Factories：Factory name (Old)；
- SKU Milestone Plans：旧SKU直链和误导性的Relationship Check命名；
- Tasks：重复完成状态字段。

删除闸门：必须同时满足“数据已迁移、Interface已切换、Automation无依赖、导入/导出工具已切换、备份完成”。

## 十三、最终目标

整理完成后，每张表只回答一种核心问题：

- Program：公司准备推进哪些产品平台；
- Project：一次项目整体怎么推进；
- PMO SKU：产品主数据是什么；
- Project SKU：这个SKU在这个Project/供应商下表现怎样；
- SKU Milestone Plan：它沿用主计划，还是有独立日期；
- Task：谁在什么时候完成什么；
- Issue：什么问题阻碍执行，如何关闭；
- People：谁负责、属于哪里、如何联系；
- Factory：在哪里生产、对应哪个供应商实体。

最终不是把所有字段摆在一个Grid里，而是让每个角色只看到需要判断和维护的内容，让Interface、Automation和AI都使用同一套权威关系。
