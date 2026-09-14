# UX-MS-01｜Power Apps 项目详情面板设计与实现任务

版本：v1.0｜2026-09-11｜交给网页操作 AI 的独立任务书

这是现有 SharePoint MVP 的设计验证工作单，对应正式计划 MS-04 的界面准备，不代表 Dataverse 版 MS-04 已实施或验收。本文件本身尚未派发；由用户转交后，执行 AI 在下述边界内开展工作。

---

## 1. 你要完成什么

你是 AutoPM 的 Power Apps 界面设计与实现人员。请通过已经登录的浏览器，直接在 Power Apps Canvas Studio 中完成一个具体改进：

**在现有 Program Details 的 Projects 视图中，建立“项目列表＋项目详情面板”。用户选中一个项目，就能在同一窗口看清它的状态、进度、MP日期、最新进展和所属SKU，并修改保存项目进展。**

这是一次可操作的产品设计交付。请做出原生 Power Apps 页面、绑定已有真实数据并验证操作。不要只写建议，也不要另建 HTML 网站或Dataverse提供静态图片替代应用。

任务价值：保留用户正在查看的 Program 和筛选条件，让查看多个项目、核对SKU、更新进展在一个稳定上下文中完成。首个工作包聚焦这一条旅程，不建设完整的Plan、Issue、Data Center或新的导航系统。

## 2. 已知环境与已有成果

- 应用：**AutoPM test**。
- App ID：`fff66275-da9f-41f8-8df2-6fd4d7bf543b`。
- 环境：`Default-276bce15-bc90-4de5-8559-6c504d8b6cf8`。
- [原应用编辑入口](https://make.powerapps.com/e/Default-276bce15-bc90-4de5-8559-6c504d8b6cf8/canvas/?action=edit&app-id=%2Fproviders%2FMicrosoft.PowerApps%2Fapps%2Ffff66275-da9f-41f8-8df2-6fd4d7bf543b)。
- [SharePoint站点](https://europro365.sharepoint.com/teams/Autopm)。
- Dataverse 尚未取得。这次继续使用已有 SharePoint 数据源，不等待IT，也不改变正式Dataverse路线。

2026-09-10的实施记录显示：Screen2为Program Portfolio，Screen3为Program Details；已经有英文页面、分类和状态颜色、项目与SKU查看以及保存。先核实当前真实版本，不把旧记录当成今日网页检查结果。

当时数据范围：151 Programs、480 Projects、2,128 SKUs、481 Program–Project关系、1,045 Project–SKU关系。这是已导入的Program相关范围，不是全部2,997源Projects和9,926源SKUs。本任务不重新导入数据，不重建已经完成的Program列表。

当前使用的是 **APM_** 五张列表；旧 **AutoPM_** 列表只有早期两个Program测试数据，不能误接。

## 3. 必须遵守的数据关系与写入范围

以下名称来自历史CSV和实施记录，接手时检查Power Apps实际字段类型与内部名称：

| 列表 | 关键字段 | 页面用途 |
|---|---|---|
| APM_Programs | Title、ProgramKey、ProgramCode、Brand、Category | 当前Program身份与标题 |
| APM_ProgramProjects | ProgramKey、ProjectKey | 当前Program包含哪些Project |
| APM_Projects | Title、ProjectKey、ProjectStatus、StatusGroup、ProgressSummary、MPStartSource、ProgressSource | 项目列表和详情 |
| APM_ProjectSKUs | ProjectKey、SkuKey | 当前Project包含哪些SKU |
| APM_SKUs | Title、SkuKey、ProgramKey、Market、SKUStatus | 关联SKU身份及产品主数据 |

查询方向：

`Selected Program.ProgramKey → APM_ProgramProjects → ProjectKey → APM_Projects`

`Selected Project.ProjectKey → APM_ProjectSKUs → SkuKey → APM_SKUs`

必须使用经核对的稳定键匹配，不按名称猜关联。保留当前MVP的Program–Project映射；本次不切换为未来Dataverse的派生关系，也不清洗全部历史关系。

- **Project SKUs**表示选中项目的SKU；**Program SKUs**表示Program产品范围。两者不能混为一张列表或同一个数量。
- `APM_SKUs.SKUStatus`是现有SKU主数据状态，不应展示为“该SKU在当前Project中的执行状态”。这次默认在项目SKU面板中只展示SKU名称/编码和Market。
- 本次只开放项目 **ProgressSummary** 的编辑。ProjectStatus、StatusGroup、SKU字段保持只读，避免设计任务改变状态业务规则。
- 进度和MP日期是已有来源快照；显示来源/更新时间信息仅使用真实存在字段，不编造实时计算或最近更新时间。
- 原有状态组合仍按实际数据展示，不凭“In MP”推断项目健康。正式Stage/Health拆分留给后续数据规则任务。

## 4. 目标界面

保留现有Program Portfolio与其筛选。仅改善Program Details中的Projects工作区，并复用当前Program SKUs入口。

### 布局

```text
Back to Programs   /   Current Program name                 Program code
Current Program information and existing summary metrics

Projects                         Program SKUs
Search projects...    Status group [All]    Clear filters

Project list (~40%)              Selected project details (~60%)
--------------------------------+--------------------------------------
Project name / Project ID       | Project name / Project ID     Status
Status / imported progress      | Overview                 Project SKUs
                                |
Selected row clearly marked     | Imported progress | MP date | SKU count
                                | Latest progress
                                | [existing summary text]
                                | [Edit update]
                                |
                                | Edit mode: multiline input
                                | [Cancel]                 [Save update]
```

设计重点：

1. Program标题始终可见；切换项目时列表和筛选不丢失。选中行有蓝色标记，详情标题与选中行一致。
2. 项目列表展示Name、Project ID、Status；进度有有效值时可显示紧凑进度条。不要把内部UUID当成用户认识的项目编号，无法确定业务编号时只显示真实名称并记录映射缺口。
3. 详情只做 **Overview / Project SKUs** 两个有效标签。不创建尚无数据与功能的Plan、Issues或History空标签。
4. Overview突出Status、Imported progress、MP date和Latest progress；长文本完整可读。缺值显示`Not provided`，不显示假的0%、日期或责任人。
5. Project SKUs显示该Project真实关联记录及去重数量。空集显示`No SKUs linked to this project`，不能用Program全部SKU补满。
6. `Edit update`进入编辑；`Save update`作为主按钮，`Cancel`作为次按钮；未修改或正在保存时禁止重复提交。

### 视觉规范

- AutoPM自建页面的文字、按钮、帮助、空状态和错误提示全部英文；Microsoft外壳语言由账号设置决定，本次不用改账号语言。
- 复用当前应用主题；在改造区域采用浅灰背景、白色内容区、清楚的标题层级和16–24px内容间距。正文建议14–16px，不靠缩小字号塞满信息。
- 主按钮和选中态使用Blue，例如`#2563EB`配白字；保存处理中保持可辨识。
- 现有状态按含义呈现：On Track绿色、At Risk琥珀色、Delayed红色、In MP蓝色、On Hold紫色、Cancelled灰色。优先浅色徽标配深色文字；状态名一直可见，不能只靠颜色。
- 桌面至少检查1366×768及一个较窄视口。较窄时上下排列，或在同一应用内打开详情并提供返回；不得让保存按钮被裁掉。此次不要求全应用手机重做。
- 页面字段标题用`Latest progress`、`MP date`等用户语言，不直接显示`ProgressSummary`或`MPStartSource`。

## 5. 操作流程与异常行为

正常旅程：打开Program → 搜索/筛选项目 → 选择项目 → 看Overview → 看Project SKUs → Edit update → Save update → 重开该项目，仍读到保存后的内容。

同时实现这些必要行为：

- 初次未选择项目：显示`Select a project to view details`。
- 搜索无结果：显示`No projects match your filters`及清除筛选入口；清除后数据回到当前Program范围。
- 项目不再符合筛选或切换Program：清除已失效的选择与旧SKU列表，不能继续展示上一个项目的数据。
- 有未保存编辑时切项目/Program：应用内提示保留编辑或放弃；不能把A的草稿写入B。编辑和保存绑定开始编辑时的ProjectKey。
- Cancel只丢弃草稿，不写SharePoint。保存失败保留输入，显示英文错误；成功必须在后台写入确认之后显示。
- 保存前刷新/核对当前ProgressSummary与编辑时原值。如果已有他人修改，则提示冲突、保留草稿，不静默覆盖。该前置检测不能被宣称为SharePoint原子并发保证。
- 保存后刷新当前记录和展示数据；不能仅更新本地Collection就宣称保存成功。

## 6. 网页执行步骤和授权边界

1. **只核对相关页面。** 确认App ID、当前入口、数据源和保存公式；记录设计前截图。已经符合本任务的控件直接复用，不为证明做过工作而全部重建。
2. **建立设计副本。** 通过Power Apps当前可用的复制/另存操作，建立`AutoPM UX – Project Workspace v1`。记录副本App ID，在副本内实施，不覆盖原已发布版本。若无法复制，不自行修改原App，提交具体阻塞及已完成设计说明。
3. **完成布局与绑定。** 按第3–5节实现列表、选择、Overview/SKUs标签、摘要编辑及反馈。可通过Studio界面编辑Power Fx或粘贴平台支持的控件定义；绑定后必须实际预览，不把成功粘贴当作成功设计。
4. **完成验证。** 检查下面的验收清单。原应用9月10日有历史委派警告，逐条区分本次新增和原有；不通过调高500/2000上限掩盖数据截断。若本Program读取量达到限制，明确范围不完整并修复本次查询，不隐藏记录。
5. **保存与交付。** 保存设计副本及结果文件，提供编辑链接、页面名、修改对象和用例证据。原App的发布、覆盖和向同事分享不属于本次任务；不用等待这些操作才能交付设计副本。

**数据测试特别说明：** 复制App不会复制SharePoint数据。设计副本仍可能指向同一批列表，不能因此随意编辑业务项目。

转交本任务时，允许执行者在既有APM列表中使用明确隔离的专用QA记录做一次真实保存验证：优先使用已确认专用测试Project；没有专用记录时，可通过网页创建一个唯一标识为`UX-QA-<时间戳>`的测试Project，以及一条测试Program–Project关联和一条测试Project–SKU关联。关联已有Program/SKU只读引用，不改它们的主记录；测试Project的业务键需按实际字段类型生成，不与现有记录碰撞。

测试仅修改该QA项目的ProgressSummary。完成后核对并删除本任务新建的、仍保持测试状态的两条关联与测试Project，按关联→Project顺序清理；不得删除或覆盖任何既有业务记录。如果测试记录已被他人改变或无法确认唯一身份，停止清理并交回具体记录ID。不能创建测试记录时，将保存验收写`Blocked`，保留其他已完成成果，不拿真实项目冒充测试记录。

本任务不授权：全量导入、改表结构、改关系规则、改SKU主数据、部署Dataverse、建立Power Automate、发送邮件、配置同步、修改原App发布版本。普通画布编辑和本节范围内测试不需要让用户逐步代操作。

## 7. 验收清单

| 编号 | 必须证明 |
|---|---|
| UX01-01 | 当前Program的项目列表/筛选仍可用；原Portfolio记录范围未被缩成两个示例Program |
| UX01-02 | 选中A、切B、再切Program，标题、摘要和Project SKUs始终属于当前有效选中项目，无残留数据 |
| UX01-03 | Project SKUs通过ProjectKey→SkuKey关联并去重；Program SKUs入口保持原有语义 |
| UX01-04 | QA项目修改摘要，后台SharePoint独立读取确认，再关闭/重开详情仍显示新值；业务项目未被试写 |
| UX01-05 | Cancel不写入；无改动/保存中不可重复提交；未保存切换有应用内处理；检测到目标已更新时不静默覆盖 |
| UX01-06 | 英文标题/按钮/提示、状态颜色加文字、空值不伪造；长摘要和窄视口可读且操作不被裁掉 |
| UX01-07 | 本次无新增公式错误；查询范围与计数可核对，已有警告/未来规模限制如实列出 |
| UX01-08 | 设计副本已保存；原发布App保持原版本；测试新建记录已准确清理或列出待清理ID |

历史样例仅作定位参考：CrushBoss曾有15Projects，NXA0303曾关联LB201EUPKBRN、LB201UKPKBRN两SKU。先核对当前数据；发生变化时按真实明细解释，不为了匹配旧数字修改记录。

## 8. 交回结果

请提交一份`UX-MS-01_Result.md`，内容包括：

1. 副本App名称、App ID、编辑链接、保存状态、修改页面；未覆盖原发布App的证据。
2. 设计前后截图，至少包含项目列表＋详情、Project SKUs、摘要编辑、窄视口。
3. 字段与控件对应表，以及选中Project、查询SKU、保存摘要的实际逻辑；现有保存/状态规则有无变化。
4. 八项验收逐项写Expected、Actual、Pass/Fail/Not Run/Blocked及证据；不要只写“已完成”。
5. 测试记录ID、实际写入和独立读回、清理结果；未验证的权限、并发、规模或发布事项单独列出。

这个任务通过的标准是：现有MVP的一个关键工作区变得清晰、顺畅且有真实数据交互。它不代表完整AutoPM、数据治理或Dataverse版本已经完成。
