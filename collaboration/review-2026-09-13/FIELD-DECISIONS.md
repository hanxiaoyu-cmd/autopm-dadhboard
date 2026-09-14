# AutoPM最小字段补充：先决定存什么，再设计页面

**2026-09-13｜候选设计，不是建表指令**

本页只列本轮业务评估得出的处理建议，不包含旧评审的全部新增项。主结论见 [评估报告](README.md)。

“需要补”指当前数据库没有明确位置保存该事实；最终英文名称和选择项可以在逐项讨论时调整。Task完成方式、Completed By和项目进度计算保持原样。

## 先复用，不新增

| 需要的信息 | 当前放在哪里 | 使用规则 |
|---|---|---|
| 项目范围、为什么开案 | Projects.Project Description (Manual) | 保存相对稳定的项目范围；最新进展另放Engineering remark |
| 变更方向、项目类型 | Projects.Change Types / Project Type | 分类筛选；不代替变更PPT中的具体内容 |
| 美国输入、Change PPT、设计文件 | Projects.SharePoint Folder URL；具体Task说明中指向资料版本 | 文件继续有一个正式存放处；不拿Import File附件字段混装全部业务文档 |
| 部门负责人与项目团队 | Projects各职能Owner、People、Tasks Owners | 项目职能负责人和具体工作执行人可不同，不让同一人员事实维护两份 |
| 包装矩阵、评估结论文件、测试报告 | Tasks.Deliverables (Manual) | 一个成果目录可容纳多文件；需要保留历史时文件必须有版本，不能一直覆盖同一文件 |
| 当前进展 | Projects.Engineering remark及其AI摘要 | 原文由人或正式输入维护，AI辅助阅读；不是稳定需求说明或历史报告快照 |
| 外部正式审批入口 | Projects.ECN URL | 项目级入口；各审批Task用Deliverables指到对应审批记录 |
| 问题关联和原因 | Issues.Projects、Related Tasks、Root Cause | 原因不再另建一个同义字段；Task关联可为空，不要求先有Task才能有Issue |
| 日期例外 | SKU Milestone Plans.Master Task、Override Date、Adjustment Reason | 保留；日期取值锚点另讨论，不在本次批量改公式 |

## Tasks建议补什么

项目层面另有一个应先明确的信息：**Project Stage**。建议在Projects用单选保存项目整体阶段，例如Assessment & Planning / ECN DD Review / Execution & Testing / ECN IMP Review / MP，由项目负责人根据实际推进情况维护。实际阶段名称沿用团队口径再整理；它不由任务完成比例自动推导，不替代现有Project Status，也不触发本轮暂停的进度重算。

如果NPI和NPD同时负责，现有角色字段不能明确谁统筹时，再补Project Lead。若既有业务规则已经能唯一确定，则直接复用；不让团队为同一个负责人维护多个重复字段。

先保留19个现有字段。以下候选字段按用途显示，不要求每个Task都填全部列。

### 一、各类工作共用的内容

| 候选字段 | 类型 | 存什么、谁维护 | 为什么当前字段不能替代 |
|---|---|---|---|
| Workstream | 单选 | 工作方向，如Packaging、CMF/ID/UI、DQTP、EE、Compliance、Tooling、NPD、ME、SC、Factory；模板带入，PM可调整 | People.Department表示人属于哪里；跨部门任务的工作方向不能随Owner变更而改变。模板已有Department，实际Task没有 |
| Work Brief | 长文本 | 具体要做的事、变更范围、所依据资料与版本；PM发起、部门补充 | Task Name只是一行名称；Deliverables存输出链接，不能说明输入依据与要求 |
| Outcome | 长文本 | 评估结论、工作实际结果、关键限制与简短说明；执行人员维护 | Completed By只记录完成操作；Deliverables有文件但不能让项目负责人快速读懂结果 |
| Predecessors | 关联Tasks，多选 | 当前项目中必须先完成的工作；PM维护，执行人员提出变更 | Task Template的Predecessor是模板规则；当前Tasks并没有项目实际前置关系 |
| Source Assessments | 关联Tasks，多选 | 一项执行工作来自哪些评估Task；由建计划时带入/PM维护 | 它表达“为什么有这项工作”，与“必须等哪项完成”不同；不能拿同一个前置字段兼任 |

Predecessors不是增加字段就获得自动排期。需要检查同项目、不能关联自己、不能形成循环；自动排期和影响提示另行实现。先支持明确的完成后开始关系，确实存在并行启动等需求时再扩展关系类型，不能把所有工程关系假装成一种关系。

Source Assessments不是通用历史库；如果RKO/变更范围有重大版本变化，任务说明要保留旧依据，复评保留独立记录或可追溯版本，不覆盖全部旧结论。

### 二、部门评估与形成计划

| 候选字段 | 类型 | 具体含义 | 维护位置 |
|---|---|---|---|
| Assessment Decision | 单选 | Needs Information / Further Work Required / No Further Work；只表示是否需要后续工作，不是Task完成状态 | 评估Task |
| Estimated Duration | 数字 | 这项执行工作预计持续多久；模板给初值，由实际评估调整 | 对应的执行Task |
| Duration Basis | 单选 | Working Days / Calendar Days；必须说明工作日采用的日历 | 与Estimated Duration一起使用 |

初步评估可能只有周期估计、还排不出具体Start/Due，因此不能简单用起止日期相减代替预估。专业评估里同时出现等待期、实际操作时间时，先在Outcome说清，并将确实需要独立排期的工作分成实际Task。

**不新增“评估是否完成”字段。** 评估Task继续使用原完成机制。Assessment Decision里的No Further Work指不需要额外执行工作，不是跳过部门评估，也不是修改任务统计分母。

评估工作与执行工作可先利用现有Phase加模板约定识别；如果同一Phase中必须机器区分评估/测试/审批，再加入Work Kind（Assessment / Execution / Test / Approval）。不能长期依靠任务名称关键词控制自动化。它是自动化和按类型显示字段的条件项，不能与Phase混为同一含义。

### 三、测试和外部审批

| 候选字段 | 类型 | 存什么 | 与现有字段的区别 |
|---|---|---|---|
| Test Result | 单选 | Not Reported / Pass / Fail / Conditional；仅测试Task使用 | 测试工作完成后仍可能Fail。记录真实结论，不重新定义Task Completion |
| Approval Status | 单选 | Not Submitted / In Review / Returned / Approved；仅外部ECN审批跟踪Task使用 | 提交资料、审查中、已批准不同；项目ECN URL和日期无法表达这些区别 |
| Approval Decision Date | 日期 | 外部ECN当前结论发生日期；有新结论才更新 | 不是Task的计划到期日，也不是页面最近编辑时间 |

Test Result为Conditional时，限制、授权或待完成事项写Outcome并链接正式来源，不自动等于可以量产。

两个ECN阶段分别是一条审批跟踪Task。审批记录仍以ECN为准；Airtable记录最新结果，历史细节回到ECN。若将来需要AutoPM自己统计每轮审批耗时，再建逐轮记录，不在首轮重复建设。

复测不能用新Pass覆盖原Fail。用不同轮次的Task及对应报告保留事实；需要频繁多轮且大批样机追踪时，再评估独立测试明细表。

## Issues建议补什么

保留原Issue ID、项目、相关任务、Severity、Category、Impact MP plan、Root Cause、Recovery Owners和计划关闭日。

| 候选调整 | 类型 | 员工填写什么 | 处理建议 |
|---|---|---|---|
| Issue Details | 长文本 | 实际现象、发现条件、相关背景 | 现有Issue description是单行，可继续作简短标题；增加正文，不把所有细节塞标题 |
| Impact Details | 长文本 | 哪个交付受影响、预计怎样影响、依据是什么 | 现有Impact MP plan勾选只保留快速标记；不能取代具体解释 |
| Resolution | 长文本 | 最终怎样解决，实际效果是什么 | 与Root Cause和准备采取的Recovery Action分开 |
| Actual Closed Date | 日期 | 实际确认解决并关闭的日期 | 不能拿Planned close Date或Last Modified代替 |
| Prevention / Lesson | 长文本 | 下次什么检查或计划安排能防止重演 | 可先在已解决Issue中检索，不立即复制到另一套知识表 |
| Occurrence Phase | 单选 | 发现问题时处于哪个项目阶段 | 用于以后分析问题常在哪个阶段出现；记录发生时事实，不随项目进入MP而改变 |

这些信息分开在登记、处理中、解决时补充，不要求发现问题的员工当场写根因和预防方案。谁负责关闭及是否需要额外验证流程另讨论，本次不设强制新制度。

### 新增Issue Actions：仅为解决“一条Issue有多项措施”

一条记录代表一个措施，不代表一个项目计划Task。

| 字段 | 类型 | 用途 |
|---|---|---|
| Action ID | 自动编号/稳定标识 | 定位一项措施 |
| Issue | 关联Issues，单个 | 所属问题；项目从Issue读取 |
| Action | 长文本 | 具体措施 |
| Owner | 关联People | 此措施的牵头执行人；不要把几项措施的多人混成一个无法对应的名单 |
| Due Date | 日期 | 这项措施承诺完成时间 |
| Action Status | 单选 | Open / In Progress / Done / Cancelled，记录该措施进展 |
| Result | 长文本 | 实际做了什么、有没有效果 |
| Evidence URL | URL | 相关结果或材料 |
| Formal Task | 可选关联Tasks，单个 | 措施经PM决定纳入正式计划时，指向那条Task |

普通措施在这里维护。如果已经纳入正式Task，Owner、日期和执行状态以该Task为维护位置，措施行只展示引用和相关处理结果，不要求员工双写。不能直接用脚本把历史段落拆成看似有确定Owner和结果的记录；无法明确对应的旧措施保留原文待整理。

现有Recovery Action保留为历史原文或过渡摘要；新措施逐项维护后，摘要应自动读取或明确只读。不能两处都继续编辑同一措施。

## 尚不足，但不应借机全部扩表的地方

| 能力 | 现有办法 | 本轮推荐与边界 |
|---|---|---|
| 判断项目是否紧急 | 当前Projects没有专门紧急程度；Project Level是复杂度 | 若要分类或排序，补Project Priority。理由可用Project Description/Work Brief；不先建设复杂评分模型 |
| 详细变更清单、版本 | Change Types、Description、Change PPT文件 | 先明确本次评估采用哪个版本；需要按每项变更追踪影响时再建Change Items，不能宣称现在已支持逐条变更追踪 |
| 样机规格、数量、分配和借用 | Sample plan URL、测试计划及Task | 当前可协调文件交付，不能系统合计机器或分配。若要求在AutoPM内维护，新增Sample Requirements明细：Project、Build/Round、SKU/规格、请求部门/测试Task、数量、需要日期、分配状态；不能只加Project.Sample Count |
| 工时与资源容量 | 部门估计和外部计划 | 预计周期先用于排期；实际工时填报、产能负荷是另一项能力。工时、周期、机器数量不能混用 |
| 原批准计划与后来变化 | 已有计划文件和多种日期，但当前Tasks没有完整计划版本事实 | 先保留批准版文件及明确来源。自动比较Baseline/Forecast、SKU日期继承属于后续单独日期设计；本轮不先搬日期 |
| Template来源和版本 | 模板ID、两套模板字段和CPM规则 | 确定生成器使用哪一套，已生成Task记录来源模板/版本；需按模板升级追溯时增加Source Template关联和生成时版本快照，不按任务名称猜 |
| SKU受影响范围 | 现有背景SKU文字、项目全部Issue及SKU节点关联 | 如果要准确筛选受影响SKU，增加Affected Project SKUs关联及范围说明。没有选择不能被解释为影响全部 |
| ProjectSKU退出和重加 | 现有执行关系和状态 | 页面支持该操作前补Active/Removed及范围变更记录；业务执行状态与是否属于项目分开 |
| 周报历史、导入批次、逐条失败 | 最新备注/摘要、Schedule Import基础状态 | 另行设计快照与作业明细；本次没有把这些功能判为已足够 |

这些条件项不是被删除或降级。它们说明“当前可以做到什么，要求再往前一步需要什么”。未来开发范围包含该能力时，就必须补齐，不能在页面上用静态展示冒充。

## 决定字段前，用这组情况检验

| 情况 | 数据应如何保存 |
|---|---|
| 包装评估后确认无需变更 | 评估Task保留，Decision=No Further Work；Outcome有理由；不新增不需要的包材执行任务 |
| Compliance因缺美国资料还不能判断 | Decision=Needs Information；Work Brief/Outcome记录缺什么；跟进美国资料用独立计划Task；若造成异常障碍再登记Issue |
| DQTP要10台、Compliance要4台，但有复用可能 | 不直接相加当生产需求；先在正式Sample Plan确认规格、批次、复用条件；要系统计算就需样机需求明细 |
| 测试做完但未通过 | Task照原规则完成，Test Result=Fail，Outcome和报告记录结果；异常进入Issue |
| 一个Issue有三项措施，仅第一项做完 | 三条Issue Actions分别维护；Issue不因其中一条Done自动被解释为已解决 |
| ECN资料已提交但被退回 | 审批Task状态记录Returned；Outcome给退回原因，来源指向外部审批；不能展示成Approved |
| 美国变更导致已完成评估要重做 | 保留原依据和结论；复评有明确版本或新记录；新增计划工作指向新的评估来源 |
| 想看某员工现在要做什么 | 读取其Task和Issue Actions，不为My Work再建重复业务记录 |

**上述场景能被不重填、不丢结果地表达，就可以进入对应Interface讨论。字段存在之后，还需要页面和保存链路验收，不能把建字段等同于功能完成。**
