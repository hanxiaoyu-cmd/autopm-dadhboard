# AutoPM 第二轮补查记录

**状态：已完成当前可访问范围的补查；整体完成标准尚未全部满足。** Closure Plan、两个字段架构文件及 Windows Data Bridge 文件和历史输出当前不可访问；周报写入与新 Tracker 文件输出尚未贯通。不能把这份结果称为整套系统已完成验收。

原报告 `AutoPM_System_Audit_2026-09-10.md` 保留不改。本报告补充、修正其证据；整合蓝图见同批交付的 `AutoPM_Traceable_Blueprint_2026-09-11.md`。原报告问题始终称“原报告问题 Fxx”，本轮新增观察用 R2-xx，需求用 REQ-xxx。

## 1. 本轮基线与方法

- 检查时间：2026-09-10 23:47 至 2026-09-11 00:22 左右，UTC；逐项 UTC 时间见证据索引。浏览器取证时钟与执行环境 UTC 已交叉核对。
- Base：AutoPM V2（Pilot），`appOMWiK4CTOH7iQu`，登录账户 Sun Sun。实际操作浏览器、展开配置、读取代码及既有日志；Airtable 连接器用于字段配置差异和具体记录核对。
- 本轮重开当前目录全部 13 个业务页面；8 个在导航显示、5 个隐藏但仍可达。另有 Knowledge Center、Department intelligent 两个空的 Unpublished 分组。连接器只列出 11 个顶层页面，不能用其数量替代浏览器目录。
- 顶层 Project Portfolio 显示 Last published Sep 10, 2026／No changes；列表嵌套详情 `pagRChzyUg9wthYhB` 显示 Aug 29；Program 嵌套详情 `pagabNDVGYw7XklpA` 显示 Sep 7；Program 路线项目详情 `pag13iJZweBRoXJTB` 显示 Sep 10。可见日期没有小时和发布版本号，不能称为同一脚本或页面版本。
- 18 表共 498 字段的 ID、名称、类型及连接器返回的配置与上轮比较无差异。这不证明连接器未返回的聚合表达式、视图、权限或数据没有变化。
- 本轮展开 18 项关键字段配置、27 个统计卡片条件，检查详情绑定、原生日期依赖、3 张同步表来源；重读 19 条关键脚本全文，均与上轮留存文本匹配。其余脚本沿用上轮代码证据，32 条启停状态本轮重核仍为 29 ON／3 OFF。
- 没有修改或保存记录、字段、关联、脚本、自动化、权限、发布或同步配置；未测试、重跑、手动同步、发送通知，也未运行生产 EXE 或写入脚本。

## 2. 新证据及原结论修正

| 编号／关联旧问题 | 实际观察与证据 | 业务影响／范围 | 判断与后续建议 |
|---|---|---|---|
| R2-01；原报告问题 F03 | Projects.Total Task Count (Auto) 聚合是 `SUM(1)`；Total Task Count (Rollup) 才是对 Task Count Helper 求和。NXA0010 分别为 1／7；NXA0245、NXA0229 为 1／6 | 旧总数无法反映任务量；只按这三个样本确认数值 | 已验证配置问题。修复现有字段或统一消费者来源，先不删除字段 |
| R2-02；原报告问题 F03 | Open Task Count (Auto) 使用 COUNTALL，条件是 Task Completion＝🟢 Complete **且** Priority＝High | 名为开放任务，实际计已完成高优先级任务；三样本均0 | 已验证配置问题。先统一开放口径，再对记录明细验算 |
| R2-03；原报告问题 F08 | My daily work 的 Task／Issue 默认用 Collaborators＝Current user；不是 Owner。Tasks.Owner Count 与 Completed Count 都对 People.Person Name 使用 COUNTA | 同一名字字段空值会影响人数；完成者人数达到负责人数量不证明成员相同。协作者全局 NPI 写入规则直接影响“我的工作” | 配置已核对；没有宣称已发生权限泄露或全库误判。完成、代理、参与者规则需分别决定 |
| R2-04 | My daily work.Overdue Issues 使用 Closed Date＝Yesterday 且非Closed；Issue due this week 使用 Closed Date＜一周后且非Closed | 未关闭问题通常没有关闭日期，可能被漏掉；本轮核实的是配置，不估算漏掉全库数量 | 已验证界面规则问题。以批准的 Target Date／逾期定义修复，并保留无日期例外 |
| R2-05 | Task this week 只有 Start Date≤一周后且非Complete；Completed Task 用 Due Date＜一月后，Completed Issue 用 Closed Date＜一月后，均无下限 | 累积历史与滚动窗口混在“本周／完成”标题中 | 条件已验证；窗口口径和标签需明确。不能说它们已经是“本周新增／本月完成” |
| R2-06；原报告问题 F16 | Weekly Summary 的 Active Projects in Selected Window 无基础／卡片过滤；MP Time Window (Select) 默认Not set。Review的Active排除Cancelled，Overview的Active只取On Track／At Risk／Delayed | 三个Active标题口径不一致，默认数量不可横向比较 | 已验证配置差异；业务口径待决，不能擅自认定一种为权威 |
| R2-07；原报告问题 F16 | Review.Open Critical Issues 是对 Open Critical Issue＞0 的 **Projects 行数**计数；Overview.Projects with Open Issues 仅要求 Issues链接非空；Overdue Tasks仍计全部Projects；Review仍有Field deleted | 项目数冒充Issue数，关闭问题也可能进入所谓Open；仅这些保留隐藏页的样本组件 | 已验证问题。只对产品负责人决定保留的页面修复，不扩大停用页范围 |
| R2-08 | Projects.Open Critical Issue包含High及Critical；Key issue各列按Impact MP勾选后分别ARRAYUNIQUE，不排除Closed，不按Issue成组 | 关键问题可保留已关闭记录；分别去重的原因／行动／Owner不能保证一一对齐。NXA0176详情可见Closed关键问题 | 已验证计算规则及具体显示。建议按Issue记录展示原因、行动、Owner、Target，或明确“历史MP影响”标签 |
| R2-09 | Program.SKU Quantity＝SUM(各Project.SKU quantity)，后者Count PMO SKU链接；SKU Models汇总的是Projects.SKU List Lookup并ARRAYUNIQUE | 数的是项目关联SKU次数，不是Program唯一SKU数，也不是Project SKUs执行记录数 | 已验证粒度。是否展示独立SKU数或执行次数由产品口径决定；没有推断具体Program发生重复 |
| R2-10；原报告问题 F01 | Tasks原生Date dependencies已开启：Start、Due、Duration；Predecessor未选，Flexible，未排除周末节假日。Duration类型为Duration、精度Days；与脚本Est. Duration (days)不同 | 日期处理除了02／03还有原生机制；02／03缺mode仍成立，但不能推断所有日期计算均不存在 | 修正架构遗漏。跨任务依赖目前没有原生Predecessor绑定；实际日期写入行为仍待授权测试 |
| R2-11；原报告问题 F20 | Program和PMO SKU来自`appyuYEyXI3Q03VK2`，主页名称PDPMO (Demo only)；ALL Tracker来自`appuQi6xxc5EVhPdF` All Projects Tracker。三者均自动同步、源端编辑Off、源记录删除或隐藏时删除目标 | 原报告“文本快照／来源未知”不足。同步可能改变关联与数量，不能忽略源视图隐藏／删除事件；Demo名称不等于已证明数据不可用 | 修正来源描述；上游维护责任、源视图规则和权威性待确认。Airtable同步表不是Data Bridge生成的新Tracker文件 |
| R2-12；原报告问题 F05／F17 | 两套详情均绑定当前Project的关系字段。列表详情的Critical issue无Severity／Open筛选，Tasks按Task Completion分组、Due升序；Program详情含Project SKUs和Master Milestone | 没有证据支持“列表All records串到全库”的推断；两入口功能差异仍在 | 已核对绑定正常；“Critical issue”标题误导，旧详情隐藏已有周更新及执行SKU字段问题仍成立 |
| R2-13；原报告问题 F04／F20 | 找到XSXA80455现有CSV、8/18 20:19显示时间的历史运行、recordId、解析16条、完成字段缺失警告。当前9条Open来源任务的名称和日期可逐行对上 | 首条计划导入链不再只有状态。当前附件身份可核对，但不能证明文件字节与当时完全相同，也不能把少7条直接判成当时丢失 | 历史运行与当前结果部分核对；批次脚本版本、旧快照、创建记录清单及后续修改仍欠缺 |
| R2-14；原报告问题 F15／F20 | 8b当前代码仍含`pagsanXHyAY3PZfj7`，实际打开返回“We can’t open this interface／page not found” | 邮件中旧链接仍是当前脚本依赖，即使不在目录也属于当前修复候选 | 已验证链接不可达；不能据此声称邮件未发送或未送达 |
| R2-15 | NXA0176的SharePoint Folder链接返回“This link has been removed”；Issue既有Jira AFOPT-53跳转登录 | 这两条外部证据尚不能支持交付物验收／Issue验证关闭 | SharePoint具体链接已验证问题；Jira内容无法检查，需要用户登录 |
| R2-16 | Issues Overview.All issue record无筛选，但副标题说Recovery State＝In Recovery；页面说明提Closure Ready等，而当前Issues无这些字段 | 文案声称的关闭工作流不能视为已实现 | 已验证文案与配置不一致；和Matrix F20“Done”并列记录，不替历史批注背书 |

字段和组件的准确名称、ID、计算式、UTC取证时间及页面链接在整合蓝图和证据包中，可据此直接分派修复。

## 3. 原报告问题的处理结果

- **补强根因**：F03、F04、F05、F08、F10、F13、F16、F17。
- **需修正范围或补充机制**：F01补原生日期依赖；F20明确3条输入输出链和3张同步表上游；Weekly Summary当前组件来源全部是Projects，不能沿用“本页同时直接展示Tasks／Issues”的泛称。
- **仍有代码／字段证据支撑，但未进行写入验证**：F02、F06、F07、F14、F15；F09原生PLM条件本轮未重新展开，保留上轮证据标签。
- **保留样本和风险范围**：F11、F12、F18、F19，不升级为整库结论。已隐藏／移除页面不因历史存在就成为当前修复任务，8b仍引用的失效页例外。
- Matrix中F20、F33的“Done”属于用户历史批注；本轮没有取得对应验证关闭／持续采用证据，不能转成“已核对可用”。

## 4. 本轮未完成的证据与影响

已知本地根目录 `D:\个人资料\AI学习圈\SN Auto PM`。当前为Linux云端工作区，没有D盘挂载；根路径检查不可访问，`/mnt`和`/media`未发现挂载。准确路径和影响见蓝图“资料访问清单”。本轮没有把这些文件称为“用户未提供”，也没有用Airtable配置猜测Bridge代码。

Closure Plan的“开发计划_工程主导”“Blueprint Detail”“Task Execution”“Implementation Check”“RACI与验收”均未读取。因此REQ编号尚未与Closure Action ID建立映射，RACI和历史关闭证据不能确认。外部周报写入及新All Tracker文件输出均缺代码、映射、日志、当时快照和输出文件；这两条链未达到完整追踪标准。

授权范围不允许保存／重跑／发邮件／多角色写入；其成功、并发、循环、失败重试、实际收件与权限效果都保留为后续测试，不是本轮要突破的边界。

## 5. 可以独立验收的最小候选任务（暂不执行）

**让 Projects.Total Task Count (Auto) 显示实际关联任务数。** 仅修改这个已有Rollup的来源与聚合：沿Tasks关联取既有Task Count Helper (System)，使用SUM(values)；不增加表、不删除旧字段、不改其他进度口径。先列出消费者，避免改变页面含义。

验收：在获准修改的环境中，NXA0010应为7，NXA0245与NXA0229应为6，并逐一对照Tasks关联；零任务记录为0。新增／移除关联后同步变化的写入测试另行授权。验收同时确认所有引用该字段的卡片／脚本显示同样总数。此任务不能被包装成“整个进度问题已修复”。
