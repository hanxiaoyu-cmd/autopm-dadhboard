# ALL Tracker 与 Airtable 匹配关系核对

核对日期：2026-09-15。依据：当前业务源码、当前本地设置与映射记忆、刚读取的 Airtable 实时结构，以及本地 `All Projects Tracker 0603.xlsx` 的真实表头。此轮只核对，未修改业务代码、Excel 或 Airtable 数据。

## 1. 结论

**目前是“部分字段可用、信息覆盖不足”，不能视为 ALL Tracker 与 Airtable 的完整同步。**

- 项目编号唯一匹配、稳定字段 ID、人员/工厂唯一解析、日期与公式保护：总体合理。
- 本地总表 50 个表头中，现有规则识别 23 个；其中包含项目编号，且 Category/Sub Category 并未启用云端来源。23/50 只是表头覆盖，不代表 46% 的业务内容已导入。
- Engineering Remarks、Manufacturing Factory、Country、P1/P2/P3 等列存在未接通的路径。
- 本地 Excel ALL Tracker 和 Airtable `ALL Tracker` 是两个对象。当前脚本不读写后者来同步业务数据。
- 当前 Excel 还存在独立读取阻断：范围为 `A1:PK19872`，按源码计算为 8,485,344 个单元格，超过 2,000,000 上限，`read_tracker()` 实测报“总表范围过大”。本文表头清单随后以只读 XML 提取完成；这不代表程序已经能够正常生成该文件的更新预览。

**因此，上轮“周报导入阻断已修复”成立，但不能延伸为“本地总表全部字段已经同步完备”。**

## 2. 实际数据流

| 方向 | 当前支持情况 | 实际来源/目标 |
|---|---|---|
| 周报 Excel → Airtable | 支持 | 写 Projects、Tasks、Issues；读 People、Factories 解析关联 |
| 周报 Excel → 本地 ALL Tracker | 支持独立离线路径 | 按表头更新已有项目，导出新 Excel 副本 |
| Airtable → 本地 ALL Tracker | 支持 | 重新读 Projects、Tasks、Issues、People、Factories，再生成总表副本 |
| 本地 ALL Tracker → Airtable | 当前没有该导入路径 | 总表在此程序中是更新目标，不是云端主数据导入源 |
| Airtable 的 ALL Tracker 表 ↔ Projects/本地 Excel | 当前没有该同步路径 | 未在表映射及读写业务中接入 |

自动衔接只针对本次有确认变更的项目，且需要先选本地总表。当前设置中的 `local_tracker_path` 为空；开启“同步后生成本地总表预览”并不等于已经生成/保存总表。若周报同步零变更，自动衔接也不会修复一个落后的本地总表；需要单独选择“Airtable → 本地总表”全库匹配。

## 3. 关键匹配规则是否合理

| 规则 | 现状 | 判断 |
|---|---|---|
| 项目识别 | Project Number/Project ID 去空白、不区分大小写、统一部分破折号；保留连字符差异。只接受唯一现有项目/行 | 合理。AB-12 不会被猜成 AB12；不自动新建未匹配项目 |
| 字段识别 | Airtable 按 Base 记住字段 ID，再核对类型；本地 Excel 按预设表头别名匹配，不依赖固定列号 | Airtable 改名适应较好；本地别名表仍写在源码，业务人员不能仅靠云端“映射记忆”改变 Excel 别名 |
| 失效映射 | 非关键字段跳过并提示，保留旧 ID；项目身份及周报版本等关键保护仍可阻断 | 合理，既隔离不确定项又防止写错对象 |
| 新旧版本 | 云端从备注中的周报日期判断；本地用更新日期列或 `.autopm.json` | 合理但依赖有效版本记录；当前模板没有可匹配的周报日期列，Date Added 不能替代 |
| 空值与公式 | 空白不清除旧值；本地公式不覆盖；源报告同日冲突跳过 | 合理，但“空白不清除”意味着不能用清空来源来删除旧值 |
| 地区/重复任务 | 同一里程碑多个任务、带地区范围、项目日期与任务日期冲突时，保留本地日期 | 对单一日期列合理；否则会把 CN/VN 等时间表混成一个日期 |
| 未知里程碑 | 当前 `require_milestone=true`，无批准选项的任务跳过 | 安全但过于保守。代码已有普通任务路径，可按业务政策改配置；不能只凭近似名称猜里程碑 |
| 新任务负责人 | 默认沿用项目 NPI Owner | 对 NPI 统筹任务可用；对质量/合规/采购任务未必合理，宜支持任务类型对应责任角色 |

当前总表识别到 304 个不同项目编号，其中 3 个编号对应多行。现有规则会跳过这些重复编号，不能按表格行序任选一行。

## 4. 50 个实际总表列的逐项关系

说明：下表“Airtable 来源”只描述当前程序的读取规则。写入本地之前还受版本、重复行、地区、日期冲突和公式保护限制；“候选”只代表建议，尚未接入。

| 列 | 本地实际表头 | 当前 Airtable → 本地关系 | 合理性/缺口 |
|---:|---|---|---|
| 1 | PROJECT NUMBER | .Project ID (Manual) → 唯一匹配行 | 合理；不覆盖身份，不新增项目行 |
| 2 | Date Added | 不回填 | 合理；创建日期不等于周报日期 |
| 3 | Project Type | Projects.Project Type (Manual) | 合理；周报入云时必须匹配既有单选项 |
| 4 | Brand | Projects.Brand (Manual) | 合理 |
| 5 | Category | 本地表头已识别，云端映射未配置 | 覆盖缺口；Projects 现有类别来源是 lookup，不能反向直接写；读取也被当前统一类型校验排除 |
| 6 | Sub Category | 本地表头已识别，云端映射为 null | 同上；应区分只读导出与可写导入的规则 |
| 7 | Project Name , Description | Projects.Project name (Manual) | 有语义风险：云端另有 Project Description (Manual)，且当前名称字段描述允许周报中的 SKU；可能用短型号覆盖本地长描述 |
| 8 | Base Model | 未匹配 | 覆盖缺口；云端 ALL Tracker 有 BASE_MODEL，但当前路径不读取该表 |
| 9 | SKUs Kicked Off | Projects.Project SKU (Manual) | 可用，但属于项目级 SKU 文本，不是逐 SKU 关联同步 |
| 10 | Target Launch Year | 未匹配 | 保留原值；尚无当前映射来源 |
| 11 | Launch Timing | 未匹配 | 保留原值；不能简单视为 MP 日期 |
| 12 | Development Factory | 未匹配 | 需先区分开发工厂和量产工厂，不能都填同一 Factory |
| 13 | Manufacturing Factory | 未匹配；源码只接受 Factory / Factory (Manual) 等别名 | 明确遗漏。候选为 Projects.Factory （Manual) → Factories 名称，但需确认该关联代表量产工厂 |
| 14 | Country | 未匹配 | 候选为 Manufacture Country (Manual)；不能把周报销售 Region 自动当作制造国家 |
| 15 | Eng , OEM Kick Off | Projects.Kick Off Date (Manual)，并核对 Tasks 的 Kick off/Due Date | 合理；项目与任务候选不一致则跳过 |
| 16 | Original TRA [at KO] | 未匹配 | 保留基线合理，不应被本周当前计划覆盖 |
| 17 | Original MP Ready [at KO] | 未匹配 | 保留基线合理；云端有 Original MP ready (Manual)，尚未作为独立受保护基线接入 |
| 18 | P1 CAD DROP | 未匹配 | 明确遗漏；云端 Projects 有 P1 CAD DROP，Tasks 也有该里程碑选项 |
| 19 | P2 CAD DROP | 未匹配 | 同上，不能与 P2 BUILD DATE 混用 |
| 20 | P3 CAD DROP | 未匹配 | 同上，不能与 P3 BUILD DATE 混用 |
| 21 | Last P | 未匹配 | 有 Last P Date、Last P BUILD DATE 和任务选项；应先明确本列指原型节点还是 BUILD 节点 |
| 22 | TRA | Tasks：TRA / ECN DD → Due Date (Manual) | 可用；Projects.TRA Date 未配置，当前不会直接读取该项目字段 |
| 23 | Cut Steel | Tasks：Cut Steel → Due Date (Manual) | 可用；Projects 同名日期未接入 |
| 24 | FOT | Tasks：FOT → Due Date (Manual) | 同上 |
| 25 | EB1 | Tasks：EB1 → Due Date (Manual) | 可用；地区任务不压成一列 |
| 26 | EB2 | Tasks：EB2 → Due Date (Manual) | 同上 |
| 27 | Tooling Transfer Load | Tasks：Tooling Transfer Load → Due Date (Manual) | 可用；保留已有公式 |
| 28 | Tooling Transfer Arrival | Tasks：Tooling Transfer Arrival → Due Date (Manual) | 同上 |
| 29 | EB3 | Tasks：EB3 → Due Date (Manual) | 可用 |
| 30 | Pilot | Tasks：Pilot → Due Date (Manual) | 可用 |
| 31 | MPRA , ECN | Tasks：MPRA / ECN → Due Date (Manual) | 可用，但本列当前有 371 个公式单元格，它们不会被覆盖 |
| 32 | MP START | Projects.MP Start Date (Manual) + Tasks.MP Start/Due Date 核对 | 合理；冲突时保留本地，不取最大/最小值猜测 |
| 33 | Previous MP Start Date | Tasks：Previous MP Date → Due Date (Manual) | 有条件合理；不能自动当作 Original MP Ready 基线 |
| 34 | Engineering Remarks [INITIAL MM,DD: Comment] | 未匹配；源码只接受 Current Progress / Update This Week 等表头 | 最明显遗漏：云端备注已有完整周报，本地实际备注列却接不到；修复时应按日期合并并保留人工历史 |
| 35 | Eng Status | Projects.Project Status (Manual) | 大体可用，但必须确认“工程状态”和项目健康状态相同；不等于 PB/EB/MB/MP 阶段 |
| 36 | SC Leader | 未匹配 | 云端有 SC Owner (Manual)，但 Leader 与 Owner 的职责含义需确认 |
| 37 | NPI LEADER | 未匹配 | 保留组织角色合理，不应直接套用项目负责人 |
| 38 | NPI Cat Lead | 未匹配 | 同上 |
| 39 | NPI Project Lead | Projects.NPI Owner (Manual) → People 名称 | 合理；多个关联人员用分号合并 |
| 40 | NPD LEADER | 未匹配 | 不应等同 NPD Project Lead |
| 41 | NPD Cat Lead | 未匹配 | 同上 |
| 42 | NPD Project Lead | Projects.NPD Owner(Manual) → People 名称 | 合理 |
| 43 | TRA Month | 未匹配，保留公式 | 合理，应从基础日期计算 |
| 44 | MP Month | 未匹配，保留公式 | 合理 |
| 45 | MP Week | 未匹配，保留公式 | 合理 |
| 46 | Delta from MP vs Origil MP [weeks] | 未匹配，保留公式 | 合理，应保持当前日期与原始基线的差值 |
| 47 | Kick off to TRA Leadtime [Weeks] | 未匹配，保留公式 | 合理 |
| 48 | TRA to MP Leadtime [Weeks] | 未匹配，保留公式 | 合理 |
| 49 | 13wk Plan Release Date | 未匹配，当前有大量公式 | 不能映射到数字类型 LOA-13weeks plan(Manual)；若要同步，应另明确日期语义及公式优先级 |
| 50 | FPO Release Date | 未匹配，当前有大量公式 | 云端 Tasks 有 FPO Release 选项，但本地没有接通；先确认是否继续由公式推算 |

## 5. 周报写入 Airtable 的重要补充

### 周报正文、阶段和日期

- `current_progress`、`update_this_week`、Jira 五类计数及周报日期都通过现有结构化周报块保存到 `Engineering remark(Manual)`。这里 `update_this_week` / `report_date` 独立映射为 null 是有意的，并不代表这两项完全没入云。
- **不要把 Eng Update This Week 全文直接映射到 Current stage。**实际测试周报中存在物流、测试、下一步计划等长段文字，不是四个阶段枚举。合理做法是保留全文；有明确当前阶段证据时，单独产生阶段候选。
- 当前 `Current stage` 是 singleSelect，选项为 PB stage、EB stage、MB stage、MP stage；`Current Stage (Auto)` 也是 singleSelect，但选项是 Kick Off、Design、Engineering Build、Tooling、Pre-MP、Mass Production、Complete。两者不是同一个字段，也不是同一套阶段定义。是否有自动化管理后者，本轮未核验。
- `Last Modified` 的真实类型为 lastModifiedTime，不能用来存来源周报日期。把版本放在备注中可防旧报告覆盖，但不利于直接按日期筛选；如需筛选，可增加独立可配置日期字段，与备注同次更新。

### 日期与任务

- 周报时间轴写 `Tasks.Due Date (Manual)`，不凭空推算 Start Date 或持续天数，合理。
- Award 当前会转为 Projects.Start Date (Manual)，需确认项目启动是否定义为 Award；两者不是天然相等。
- Kick off、DQTP、Compliance、MP AW、MP Start 等部分项目日期会同时与任务日期参与核对。TRA、FOT、EB1 等 Projects 字段虽然存在，却没有当前映射；其总表回填主要依赖 Tasks。应明确“项目级日期与任务级日期谁是主来源”，不能因为字段都存在就双向盲写。
- 首个 CRD 与 LOA 不在当前明确字段映射内；不能承诺自动维护 CRD date / LOA 字段。现有 LOA 字段为 number，无法无损承接一段文字或一个日期。

### 完成状态

**当前实现与真实 Airtable 模型不匹配。**程序只支持将绿色完成标记写进 checkbox；但真实 Tasks 使用 `Completed By (Manual)`（关联 People），`Task Completion (Auto)` 根据 Owner Count / Completed Count 等计算。

现状是完成信息留在预览，不会真正让任务在云端变成完成。本地总表也不改变完成颜色。合理的后续规则应回答“由谁完成”，只有有明确人员证据才更新 Completed By；不能把一格绿色直接解释成所有负责人均已完成。

### Issues

周报问题写到 Issues，不合并成 Excel 单个问题列。当前真实字段是 `Issue description (Manual)`、`Recovery Action (Manual)`、`Severity (Manual)`、`Recovery Owners (Manual)`、`Planned close Date (Manual)` 和 `Record Date (Auto)`。最后一项虽然名字带 Auto，实际 API 类型是可写 date；判断可写性应看结构类型，不能只看名字。

本地总表没有对应问题明细列，问题只保留在导出同步记录。规则解析模式用项目+问题文本匹配；只有来源标记为 DeepSeek 时才启用额外的问题修订匹配。因此问题文字改写后，在规则模式下仍可能形成另一条问题，应明确使用预期。

## 6. Airtable 云端 ALL Tracker 表：适合什么，不适合什么

当前实时结构中：

- 主键字段名为 `PROJECT_TRACKER_SKU_KEY`，不是 `Project ID (Manual)`。抽读 5 条记录，键为类似哈希的值，并分别带 SKU、BASE_MODEL 和项目描述。**不能直接拿本地 SXA/NXA 项目编号与这个键相等匹配。**
- 存在 SKU、BASE_MODEL、PROJECT_NAME_DESCRIPTION、MANUFACTURING_FACTORY、工程里程碑、备注和各级负责人列；结构更像 SKU 展开的原始 Tracker 数据。完整粒度及键生成规则仍需核对原导入器，5 条样本不足以证明全表唯一性。
- 大多数日期列实际是 multilineText；MANUFACTURING_FACTORY 是 singleSelect，而 Projects.Factory 是关联 Factories。若未来接入，需要专门的日期解析、选项到关联记录转换，不能只靠同名复制。
- 现有代码没有维护该表。它与业务表是否通过其他自动化/导入器同步，本轮没有验证，不能据此认定它完全独立或没有被其他系统更新。

**建议**：先明确该表是原始导入档案还是要持续维护的 SKU 总表。如果要持续同步，先定义 Project↔SKU 的桥接和唯一键，再设计导入；不要在当前项目级写入器里增加一个未经定义的目标表。

## 7. 建议调整顺序

| 优先级 | 调整 | 完成标准 |
|---|---|---|
| P0 | 修复总表因格式范围膨胀而无法读取的问题 | 使用实际有值区域核对，或安全清理无用格式；不通过盲目提高上限解决 |
| P1 | 接通真实备注列、制造工厂及制造国家 | 明确语义；备注按日期合并并保留人工记录；不把 Region 当 Country |
| P1 | 定义绿色完成标记 → Completed By 的规则 | 人员明确才写，不伪造完成者；完成后的云端计算结果可核验 |
| P1 | 补 P1/P2/P3 CAD、Last P 等缺失里程碑 | CAD 与 BUILD 分开；公式与原始基线保护不变 |
| P1 | 本地表头别名移到可维护配置 | 当前表头、别名、目标字段、数据类型、覆盖方式和跳过原因可查看；不靠每换模板就改源码 |
| P2 | 分开云端读取映射与写入映射 | lookup 可用于本地导出，但仍不能成为周报写入目标 |
| P2 | 定义阶段、Award/Start、日期主来源和任务责任角色 | 有明确业务定义和冲突优先级；不靠含糊相似度自动决定 |
| P2 | 改善零变更后的总表补同步入口 | 云端零变更不应被用户误解为本地也已一致 |

## 8. 源码与证据定位

- 本地总表表头及日期列规则：`autopm/tracker.py:13`、`:35`。
- 当前范围阻断：`autopm/tracker.py:79`；本地公式保护：`:176`；仅导出新副本：`:195`。
- 云端项目/任务/问题默认映射：`autopm/sync.py:24`、`:41`、`:45`；当前有效映射必须结合 `.local/settings.json` 和 `.local/schema-memory/`。
- 云端回填总表：`autopm/airtable_tracker.py:54`；版本入口：`:90`；地区/重复里程碑冲突：`:217`、`:229`。
- 里程碑严格模式：`autopm/sync.py:561`；新任务默认 NPI Owner：`:570`；完成标记限制：`:581`。
- Award → Start Date：`autopm/workbook.py:667`；未知业务字段受源解析词表约束：`:29`。
- 零变更与未选择总表的自动衔接限制：`autopm/tracker_ui.py:128`、`:131`。
- 本轮机器核对明细：`.local/mapping_audit.json`；实时结构：`.local/live_schema.json`；云端 Tracker 五条样本：`.local/cloud_tracker_sample.json`。

字段名称/类型为本轮实时验证；“合理性”和未来调整为基于这些证据的判断，不代表已修改或已验证外部自动化。

## 附录：当前有效 Airtable 映射全表

这是当前配置与实时字段 ID 核对后的结果，优先于源码中的默认字段名。People/Factories 用于只读解析关联；其他各行是否产生写入仍取决于来源值和业务规则。

| 表 | 内部业务字段 | 实际 Airtable 字段 | API 类型 | 说明 |
|---|---|---|---|---|
| projects | project_id | Project ID (Manual) | singleLineText | 用于身份匹配，不改项目编号 |
| projects | project_name | Project name (Manual) | singleLineText | 按有效来源值更新 |
| projects | sku | Project SKU (Manual) | singleLineText | 按有效来源值更新 |
| projects | region | 未启用/未匹配 | — | 来源值存在时提示并跳过 |
| projects | sub_category | 未启用/未匹配 | — | 来源值存在时提示并跳过 |
| projects | status | Project Status (Manual) | singleSelect | 按有效来源值更新 |
| projects | brand | Brand (Manual) | singleSelect | 按有效来源值更新 |
| projects | type | Project Type (Manual) | singleSelect | 按有效来源值更新 |
| projects | capacity | 未启用/未匹配 | — | 来源值存在时提示并跳过 |
| projects | factory | Factory （Manual) | multipleRecordLinks | 按有效来源值更新 |
| projects | quality | Quality Owner (Manual) | multipleRecordLinks | 按有效来源值更新 |
| projects | npi_lead | NPI Owner (Manual) | multipleRecordLinks | 按有效来源值更新 |
| projects | npd_lead | NPD Owner(Manual) | multipleRecordLinks | 按有效来源值更新 |
| projects | pmo | PMO Owner (Manual) | multipleRecordLinks | 按有效来源值更新 |
| projects | current_progress | Engineering remark(Manual) | richText | 保留人工备注及周报历史 |
| projects | update_this_week | Engineering remark(Manual) 中的周报块 | — | 没有独立列，合并存储 |
| projects | tooling | Tooling (Manual) | singleLineText | 按有效来源值更新 |
| projects | kick_off_date | Kick Off Date (Manual) | date | 按有效来源值更新 |
| projects | dqtp_finish_date | DQTP Finish Date (Manual) | date | 按有效来源值更新 |
| projects | mp_aw_date | MP AW Date (Manual) | date | 按有效来源值更新 |
| projects | compliance_complete_date | Compliance Complete Date (Manual) | date | 按有效来源值更新 |
| projects | start_date | Start Date (Manual) | date | 按有效来源值更新 |
| projects | mp_start_date | MP Start Date (Manual) | date | 按有效来源值更新 |
| projects | report_date | Engineering remark(Manual) 中的周报块 | — | 没有独立列，合并存储 |
| projects | next_plm | Next Action | multilineText | 按有效来源值更新 |
| projects | jira_link | Jira URL (Manual) | url | 按有效来源值更新 |
| tasks | name | Task Name (Manual) | singleLineText | 按有效来源值更新 |
| tasks | project | Projects（Link） | multipleRecordLinks | 按有效来源值更新 |
| tasks | start_date | Start Date (Manual) | date | 配置存在；当前周报时间轴不写此列 |
| tasks | due_date | Due Date (Manual) | date | 按有效来源值更新 |
| tasks | milestone | Milestone (Manual) | singleSelect | 按有效来源值更新 |
| tasks | owners | Tasks Owners (Manual) | multipleRecordLinks | 按有效来源值更新 |
| tasks | duration | 未启用/未匹配 | — | 来源值存在时提示并跳过 |
| issues | text | Issue description (Manual) | singleLineText | 按有效来源值更新 |
| issues | project | Projects（Link） | multipleRecordLinks | 按有效来源值更新 |
| issues | action | Recovery Action (Manual) | multilineText | 按有效来源值更新 |
| issues | record_date | Record Date (Auto) | date | 按有效来源值更新 |
| issues | risk | Severity (Manual) | singleSelect | 按有效来源值更新 |
| issues | owner | Recovery Owners (Manual) | multipleRecordLinks | 按有效来源值更新 |
| issues | due_date | Planned close Date (Manual) | date | 按有效来源值更新 |
| people | name | Person Name (Manual) | singleLineText | 只读解析人员/工厂 |
| people | department | Department (Manual) | singleSelect | 只读解析人员/工厂 |
| factories | name | Factory Full Name (Manual) | singleLineText | 只读解析人员/工厂 |
| factories | factory_id | Factory ID (Auto) | singleLineText | 只读解析人员/工厂 |
| factories | code | Factory code (Manual) | singleLineText | 只读解析人员/工厂 |
| factories | old_name | 未启用/未匹配 | — | 只读解析人员/工厂 |
