# Project、Task、Issue：执行 AI 工作清单

2026-09-11｜FD-14 修订｜关联 AT-01/02/05/08/09/10、MS-02/03/04/05/07/08/09。

状态：设计与交接文件已形成；未分派执行者，未修改生产表、自动化或页面，未完成平台验收。先读[简明业务说明](PROJECT-TASK-ISSUE.md)。本单不独立授权生产发布。

## 1. 不得改错的业务边界

- Tasks 只承载项目正式计划工作，包括PM明确批准加入计划的额外工作。
- Issues 直接属于项目，记录实际发生的意外障碍；关联受影响Task是可选项。
- Issue Actions 承载问题处理措施，不作为 Tasks 的 Work Type，不计入计划完成率。
- 日常操作、批量导入和自动化都遵守上述归属；不能靠页面隐藏掩盖重复维护。
- 只有 PM 的明确操作可以将措施纳入项目计划；操作必须留来源、操作者、理由、时间与防重复记录。
- 旧PRD、初始语义JSON和历史审计保留原文；其中“恢复行动进入Tasks”的目标建议已被本次用户决定替代。历史配置事实不能改写成新设计。

## 2. 数据关系与现有字段处理

以下ID来自已保存的2026-09-11结构证据。接手时按ID复核受影响配置；名称可能已经变化。不要重新创建同义关联。

| 关系 | 当前可定位字段 | 目标行为 |
| --- | --- | --- |
| Project → Tasks | Projects `fldXFvT45GnPHz77v` ↔ Tasks `fldZmIf1cjO1baWz9` | 每Task一个Project；开案时独立生成计划，不需要Issue |
| Project → Issues | Projects `fldYYP7Ww11XEEvFc` ↔ Issues `fldbZYuFwTSkfRTw6` | 每Issue一个Project；从项目页新建时自动带入 |
| Issue → Affected Tasks | Issues `fldqyrQz6KDJHiBoh` ↔ Tasks `fldqNfP0yQgKcDgca` | 同项目可选多对多；只表达受影响工作，不表示恢复任务或自动阻塞 |
| Issue → Issue Actions | 新增目标关系，尚无Field ID | 一个Issue有多条措施；每条措施只归属一个Issue |
| Issue Action → Plan Task | 新增可选 `Linked Plan Task` | 只有PM纳入计划时建立；一条措施最多指向一个Task，可复用同项目已有Task |

Issues `fldmC0PnEEOsRUxCR`、`fld45Tk40HT000paP` 是历史文本字段，不能代替Project关联。存在新同义关联时，先记录ID、数据和消费者差异，再归并入口；不直接删除或盲目双写。

关联选择器按同Project筛选，后台导入/脚本也校验。Issue不关联Task时仍可完整运行；不得从任意第一条Task静默覆盖Issue.Project。改变Project归属属于管理员纠错，先检查受影响Task/SKU/措施及已入计划任务的上下文，再留下变更记录。

## 3. 字段怎样分工

### Issues：问题本身

| 字段或事实 | 现有来源／目标处理 | 用户维护要求 |
| --- | --- | --- |
| Project | 复用 `fldbZYuFwTSkfRTw6` | 创建时带入；普通详情只读 |
| Issue ID | 复用 `fldH7wExRQPOHVW35`，补稳定编号规则 | 系统生成，不要求员工手填；导入另保留来源ID |
| Title | 复用 `fld6TUPutbZeb0OXH` | 简短描述实际问题 |
| Description | 新增长文本 | 现象与背景；不能用Root Cause代替事实 |
| Issue Owner | 新增单一People关联 | 推进负责人；不把多位Recovery Owners直接当成单一负责人 |
| Severity / Category | 复用 `fldPXDw07OQgAc1hN` / `fldzQGqKtfgv59d6R` | 分别表示严重程度和问题类别；不随意新造选项 |
| Status | 复用 `fldwzeQr9Ue4RUnBw` | Open → In Recovery → Pending Verification → Closed；拒绝返回处理，重开留历史 |
| Target Date | 复用 `fldiSAxlci41MJWYt` | 问题关闭目标，不等于每条措施的Due |
| Impact MP / Impacted Gate | 复用 `fld3GzRRInVIIuzDJ` / `fld4m4y4WgBNnviww` | 说明关键日期或阶段影响；补Impact Description解释影响 |
| Affected Tasks / Project SKUs | 复用上文Task关联和 `fldaqXuZOlR4QAUx5` | 可选；只选真实受影响范围 |
| Root Cause | 复用 `fld08VbL17q7bjliX` | 保留原因文字；新增Root Cause Status区分Unknown / Hypothesis / Confirmed |
| Resolution Result / Evidence | 新增结果、证据引用；保留Jira `fld2WQYHhW6wKmyF5` | 实际结果，不复用处理计划冒充结果 |
| Prevention / Cause Category | 新增预防建议和受控原因分类 | 分类由业务管理员维护；尚未明确的原因保留Unclassified |
| Record Date / Closed Date | 复用 `fldwUmgjS8KPRiFFf` / `fldXITohd0AFbEHjy` | 发生日期保留来源；关闭日期由验证操作填写 |
| Verifier / Verified At / History | 新增验证身份、时间，接入Execution History | 每次提交、拒绝、关闭、重开保留事件 |
| Context at Occurrence | 新增发生时背景快照：阶段、工厂ID/名称、供应商（如适用） | 已知时保存来源与时间，不能日后用最新工厂覆盖历史；未知不猜 |

创建Issue只强制当前Project和Title；Severity、Owner、Target缺失时进入Needs Triage。开始正式处理前必须确定Owner、Severity和Target。未知严重度不能当Low；Needs Triage在项目及PM队列中可见。Root Cause和完整方案不作为发现阶段的前置条件。

旧Closed保持历史事实，不伪造验证。旧风险、空状态、旧Overdue状态单列映射异常，不自动改变其业务含义。Root Cause旧文本保留，初始标Unknown，不能自动升级为Confirmed。

### Issue Actions：问题内逐条维护的措施

新增独立后台表，建议英文名 `Issue Actions`，普通用户只在Issue详情及My Issue Actions看到它。

| 字段 | 用途 |
| --- | --- |
| Action ID / Issue | 稳定身份及唯一所属Issue |
| Action | 一项明确措施 |
| Owner / Due Date | 该措施执行人和承诺时间 |
| Status | Not Started / In Progress / Done / Cancelled |
| Result / Evidence | 实际结果与证据；Done需结果，Cancelled需理由 |
| Execution Location | Issue / Project Plan，默认Issue |
| Linked Plan Task | 可选的同项目计划Task；PM纳入计划后填写 |
| Promotion Event / Request ID | 纳入计划的操作者、理由、时间及防重复依据 |

Project从所属Issue读取，不再由用户填写一遍。Issue Target和Action Due分别维护；措施晚于问题关闭目标时提示冲突，不自动覆盖日期。删除有执行历史的措施改用Cancelled并留原因。

现有Recovery Action `fldTcwJCg6OdpoGaO`、Recovery Owners `fldboKxfGDcOgpaNw`保留原始导入/历史值。拆分前预览“原文→措施→Owner→Due”；不按人数、行数或标点猜配人员和日期。拆分完成后，旧字段退出普通编辑入口，新摘要只读生成；不再让人同时维护两份行动。

### Tasks：项目计划保持独立

复用项目、名称、Owners、Start/Due、依赖、Phase/Gate、完成确认及交付物。Baseline/Forecast/Actual继续按既有日期治理工作包细化，本单不另造进度算法或按问题数量改写计划。

不新增用于混装恢复行动的Work Type。`Issues`反向关联展示名改为Affecting Issues；由措施纳入计划的来源另用上述Linked Plan Task关系，不混用受影响关联。

### PM把措施纳入正式计划

1. PM从Issue Action选择Add to Project Plan，查看理由、日期、Owner及计划影响；可以选择同项目已有Task，避免重复建工作。
2. 明确确认后才创建或关联Task，记录操作身份、请求ID和来源Action；相同请求重复提交返回已有关联。
3. 纳入后，执行Owner、日期、状态和结果以Task为准；Issue Action页只读引用这些字段并提供Open Plan Task。原措施执行字段作为转入前快照，不继续双向同步。
4. Issue自己的关闭结果继续由Issue维护。Task完成不自动关闭Issue。Task取消也不关闭Issue；显示需要重新安排措施。
5. 新Task进入当前正式计划统计；原Baseline不变，页面明确说明计划新增。普通Issue Action增删、完成、取消都不影响计划任务数和完成率。

## 4. Interface执行要求

| 位置 | 内容和操作 |
| --- | --- |
| Project / Plan Progress | 计划阶段、下一节点、任务与负责人、到期/逾期；只统计Tasks |
| Project / Needs Attention | 未关闭且Critical/High、Impact MP、逾期的Issue；Needs Triage单独可见；显示负责人和目标日期 |
| Project / Issues | 逐条问题：ID、Title、Severity、Status、Owner、Target、Impact；All/Open/In Recovery/Pending Verification/Closed筛选；另有Overdue/Needs Triage |
| Issue Detail | Summary、Impact、Analysis、Actions、Resolution、History；新建时自动带入Project；Actions可逐条编辑 |
| Task Detail | 正式工作及结果；Affected Issues为上下文；同一Task在所有入口复用详情 |
| My Work | My Tasks / My Issues / My Issue Actions分开展示，分别读取源记录，不复制待办 |
| Issue Lessons | 已解决案例按类别、发生阶段、背景、确认原因和有效措施检索；可回到原Issue/验证记录 |

全英文UI，设计说明用中文。重要性使用颜色+文字+原因。未关闭且Target早于今天才算Overdue，今天到期不算，沿用Asia/Shanghai。空日期显示未安排，不当成未逾期的正常绿灯。

所有Issue入口共用一套详情，所有Task入口共用一套详情。Project不复制可编辑的根因、措施、负责人文本。保存后重新读取记录检查结果；异步汇总显示更新时间。关闭后留在历史，不清空Project关联。

## 5. 自动化、导入和知识的改动边界

- 现有05项目关联自动化：仅在Project缺失且受影响Tasks有唯一一致Project时给出可追溯补全；多项目或已有Project冲突进入异常，不覆盖。
- 项目模板、排期、任务导入：继续只生成正式Tasks，不要求Issue；完成/进度自动化17不纳入Issue Actions。
- 周报：计划栏目写Tasks，问题栏目写Issues，措施写Issue Actions；旧长文本先保留来源，经预览匹配后再结构化。旧周报不得覆盖新的执行结果，重复文件不得重复创建措施。
- 提醒：Task按任务Due，Issue按关闭Target，Action按措施Due。纳入计划的措施只发送Task执行提醒，避免相同工作重复提醒；Issue责任提醒仍按其独立关闭目标判断。
- 报告：分别输出计划进展和问题/措施；按同一个Issue组织原因、措施、人员、日期，避免平行Rollup文本错配。
- 经验：保留问题事实、原因确认状态、措施效果和发生时背景。关闭不强制编造根因；缺证据/原因保留Incomplete标识。归因统计只使用Confirmed原因，Unknown单列。
- 规律分析：计数按唯一Issue而不是Action数量；相同项目、类别、阶段和背景可以比较，但样本数量不等于原因已被证明。预防建议经PM/模板管理员采纳后生成新模板版本，不自动重排运行项目。
- Dataverse采用同样的Project→Task、Project→Issue、Issue→IssueAction模型；跨表约束通过服务端实施。环境未就绪只交付设计，不扩大SharePoint MVP关系作为正式版本。

## 6. 实施顺序与交回证据

1. 按表/字段ID核对这三张表、相关页面、05/17和周报消费者，提交差异；保持原始快照。
2. 在获准开发副本建立Issue Actions、补缺字段和校验；先用合成样例，不批量搬迁真实措施。
3. 完成Project两类区域、共用详情、My Work及PM纳入计划操作。
4. 预览历史关联、长文本和Owner/Due映射；有歧义的记录保留待整理，不猜测、不删除。
5. 通过下表场景后提交配置差异、截图、读回结果、导入对账和恢复步骤。由协调侧验收，状态才可从设计转到实现/验证。

| 验收 | 输入与必须看到的结果 |
| --- | --- |
| PIT-01 正常项目 | 项目有10条计划Task、0条Issue；计划正常展示/执行 |
| PIT-02 独立问题 | 新建Issue不选Task；Project问题列表可见；Task数量不变 |
| PIT-03 多项措施 | 一个Issue有3条措施、不同Owner/Due；逐条维护，计划仍10条 |
| PIT-04 问题完成不改计划 | 完成/取消措施、关闭/重开Issue，计划进度保持不变 |
| PIT-05 纳入计划 | PM新增一条正式Task：当前计划11条，Baseline仍原版；重复点击不产生第12条 |
| PIT-06 复用已有任务 | PM选择已有Task，Task总数不变；Issue页只读引用执行结果，无第二份可编辑Owner/Due/Status |
| PIT-07 多入口 | 从Project、My Work、Issues修改同一对象，重开详情读取相同值 |
| PIT-08 多个问题 | Project有多个Issue，重点问题可见；同Issue关联多个Task只计1个问题 |
| PIT-09 跨项目 | 选择或导入另一个项目Task时被识别；Issue原Project不被悄悄改写 |
| PIT-10 实际关闭 | 措施Done但问题仍存在，Issue不能自动Closed；通过/拒绝/重开有事件 |
| PIT-11 经验与背景 | 项目Factory后来修改，旧Issue发生时背景仍可查；Hypothesis不进入Confirmed原因统计 |
| PIT-12 导入与缺失 | 重复周报不重复建措施；缺Owner/日期/状态显示待整理；旧报告不覆盖新结果 |
| PIT-13 到期与提醒 | 任务逾期不自动建Issue；纳入计划的措施不会再发重复执行提醒 |
| PIT-14 模板改进 | 采纳案例生成新模板版本，新项目可用；旧项目计划不自动变化 |

验收定义不等于用例已经通过。既有TC-13补充PIT-01～13的业务关系检查，TC-25补充PIT-11/14；平台安全、完成判定和导入通用用例继续有效。
