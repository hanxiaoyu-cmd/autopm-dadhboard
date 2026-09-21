# ALL Tracker → Airtable 同步方案

**版本**：v1｜日期：2026-09-18｜Base：`appOMWiK4CTOH7iQu`

---

## 一、现状总览

| 对象 | Excel ALL Tracker | Airtable ALL Tracker 表 | Airtable Projects 表 |
|---|---|---|---|
| 数据粒度 | SKU 级（一行一个 SKU） | SKU 级（无 Link，纯文本） | 项目级（聚合多 SKU） |
| 字段数 | 50 列 | 49 个字段（全 multilineText） | 100 个字段（多类型） |
| 当前状态 | 主数据源 | 已有数据（从 Excel 导入的副本） | 核心业务表，部分字段已同步 |
| 同步方向建议 | 源 → 目标 | — | Excel → Projects（主） |

---

## 二、已同步字段（✅ 已完成）

| Excel 列 | Excel 字段名 | Projects 表字段 | 类型 | 状态 |
|---|---|---|---|---|
| C3 | Project Type | `Project Type (Manual)` | singleSelect | ✅ |
| C5 | Category | `Category` (via PMO SKU Link lookup) | lookup | ✅ |
| C6 | Sub Category | `Sub_Category` (via PMO SKU Link lookup) | lookup | ✅ |
| C7 | Project Name | `Project name (Manual)` | singleLineText | ✅ |
| C8 | Base Model | `BaseModel` (via PMO SKU Link lookup) | lookup | ✅ 或需直连 |
| C12 | Development Factory | `Factory (Manual)` (Link to Factories) | multipleRecordLinks | ✅ |
| C13 | Manufacturing Factory | `Factory (Manual)` (Link to Factories) | multipleRecordLinks | ✅ |
| C17 | NPI LEADER | `NPI Owner (Manual)` (Link to People) | multipleRecordLinks | ✅ |
| C22–31 | 里程碑日期 | Tasks 表（已导入为 Task 记录） | date (in Tasks) | ✅ |
| C32 | MP START | `MP Start Date (Manual)` | date | ✅ |
| C34 | Engineering Remarks | `Engineering remark(Manual)` | richText | ✅ (weekly_remark.py) |
| C35 | Eng Status | `Project Status (Manual)` | singleSelect | ✅ |

---

## 三、建议同步字段（按优先级分组）

### 🔴 P0 — 核心信息缺失（建议立即同步）

| Excel 列 | Excel 字段名 | 建议 Projects 字段 | 现有字段？ | 类型建议 | 处理说明 |
|---|---|---|---|---|---|
| C1 | PROJECT NUMBER | `Project Number (Manual)` | ❌ 缺失 | singleLineText | 唯一标识，必须补建 |
| C2 | Date Added | `Date Added (Manual)` | ❌ 缺失 | date | 项目创建日期 |
| C4 | Brand | `Brand (Manual)` | ✅ 已存在 | singleSelect | 直接映射更新 |
| C9 | SKUs Kicked Off | `SKU Count (Manual)` 或 `SKUs Kicked Off` | ❌ 缺失 | number | 统计用，可 formula 计算 |
| C10 | Target Launch Year | `Target Launch Year (Manual)` | ❌ 缺失 | singleLineText | 如 "2026" |
| C11 | Launch Timing | `Launch Timing (Manual)` | ❌ 缺失 | singleSelect | Spring/Fall/Holiday 等 |
| C14 | Country | `Country (Manual)` 或复用 `Manufacture Country` | ✅ `Manufacture Country` | singleSelect | 注意：Excel Country vs Airtable Manufacture Country |
| C15 | Eng/OEM Kick Off | `Kick Off Date (Manual)` | ✅ 已存在 | date | 直接更新 |
| C16 | Original TRA [at KO] | `Original TRA (Manual)` | ❌ 缺失 | date | 初始 TRA 基准日期 |
| C33 | Previous MP Start Date | `Previous MP Start (Manual)` | ❌ 缺失 | date | 历史 MP 日期 |

### 🟡 P1 — 人员链路完善（需 People 表匹配）

| Excel 列 | Excel 字段名 | 建议 Projects 字段 | 现有字段？ | 类型建议 | 处理说明 |
|---|---|---|---|---|---|
| C36 | SC Leader | `SC Owner (Manual)` | ✅ 已存在 | multipleRecordLinks → People | 需通过 People 表反查 record ID |
| C37 | NPI LEADER | `NPI Owner (Manual)` | ✅ 已存在 | multipleRecordLinks → People | ✅ 已完成 |
| C38 | NPI Cat Lead | `NPI Category Lead (Manual)` | ❌ 缺失 | multipleRecordLinks → People | 新增字段 |
| C39 | NPI Project Lead | `NPI Project Lead (Manual)` | ❌ 缺失 | multipleRecordLinks → People | 新增字段 |
| — | (Excel 隐含) | `NPD Owner (Manual)` | ✅ 已存在 | multipleRecordLinks → People | 如 Excel 有对应列则映射 |
| — | (Excel 隐含) | `PD Owner (Manual)` / `EE Owner` 等 | ✅ 已存在 | multipleRecordLinks → People | 视 Excel 是否有数据 |

### 🟢 P2 — 扩展字段（可选增强）

| Excel 列 | Excel 字段名 | 建议 Projects 字段 | 类型建议 | 备注 |
|---|---|---|---|---|
| C9 | SKUs Kicked Off | `Project SKU (Manual)` 或 `SKU Count` | singleLineText / number | 当前 Projects 表有 `Project SKU (Manual)` 和 `SKU count(Auto)` (rollup) |
| C18–21 | P1/P2/P3 CAD DROP, Last P | `P1 CAD DROP` 等 | date | Projects 表已有 P1–P3 CAD DROP 和 Last P Date 字段，可直接更新 |
| C43–49 | (隐含人员列) | `Compliance Owner` / `DQTP Owner` / `CMF Owner` 等 | multipleRecordLinks → People | 如 Excel 后续版本加入这些列，可直接扩展映射 |

---

## 四、需新建字段清单（Projects 表）

以下字段在 Projects 表**目前不存在**，如需同步必须先创建：

| # | 字段名 | 类型 | 用途 | 优先级 |
|---|---|---|---|---|
| 1 | `Project Number (Manual)` | singleLineText | Excel 项目编号，唯一标识 | 🔴 P0 |
| 2 | `Date Added (Manual)` | date | 项目创建日期 | 🔴 P0 |
| 3 | `Target Launch Year (Manual)` | singleLineText | 目标上市年份 | 🔴 P0 |
| 4 | `Launch Timing (Manual)` | singleSelect | 上市窗口（Spring/Fall/Holiday） | 🔴 P0 |
| 5 | `Original TRA (Manual)` | date | 初始 TRA 基准日期 | 🔴 P0 |
| 6 | `Previous MP Start (Manual)` | date | 历史 MP 日期 | 🔴 P0 |
| 7 | `NPI Category Lead (Manual)` | multipleRecordLinks → People | NPI 品类负责人 | 🟡 P1 |
| 8 | `NPI Project Lead (Manual)` | multipleRecordLinks → People | NPI 项目负责人 | 🟡 P1 |

---

## 五、Link 字段特殊处理（People / Factories）

Excel 中人员/工厂是**纯文本名称**，Airtable Link 字段需要**record ID**。处理方式：

1. **People 表反查**：读取 People 表（`People` / `Person Name (Manual)`），建立 `姓名 → record ID` 映射字典
2. **模糊匹配**：处理大小写、空格、拼写差异（历史经验：已处理过 "Samantha Stratton" vs "Samathan" 等）
3. **未匹配处理**：记录为 `Data Quality Note`，不阻塞同步，人工后续补录
4. **Factory 同理**：已验证过 Development/Manufacturing Factory → `Factory (Manual)` 的匹配逻辑

---

## 六、同步策略建议

### 方案 A：全量字段同步（推荐）
- **范围**：P0 + P1 全部字段
- **步骤**：
  1. 在 Projects 表新建 8 个缺失字段（§四）
  2. 读取 People 表构建姓名→ID 映射
  3. 逐行读取 ALL Tracker Excel，按 Project Name / Base Model 匹配 Projects 记录
  4. 批量 PATCH 更新（每批 10 条，Airtable API 限制）
  5. 生成同步报告：更新数/跳过数/错误数/未匹配人员清单

### 方案 B：渐进式同步（保守）
- **第一阶段**：仅同步 P0 核心字段（Project Number, Date Added, Brand, Launch Year/Timing, Country, KO Date, Original TRA, Previous MP）
- **第二阶段**：人员链路（SC Leader, NPI Cat/Project Lead）
- **第三阶段**：日期细节（P1–P3 CAD DROP, Last P）

### 关键决策点
- **匹配键**：用 `Project Name` + `Base Model` 组合匹配 Projects 记录（因为 Projects 表是项目级聚合，ALL Tracker 是 SKU 级，同一项目多 SKU 时首行匹配）
- **重复处理**：同一 Project 多 SKU 时，日期类字段取最早/最新（需确认业务规则）
- **Brand 字段**：Projects 表已有 `Brand (Manual)`（singleSelect：Shark/Ninja），直接更新值域
- **Country 字段**：Projects 表已有 `Manufacture Country (Manual)`（singleSelect），Excel `Country`（VN/CN/US 等）可直接映射

---

## 七、技术风险与踩坑点

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| **Projects 表 100 字段已达上限附近** | 无法新建字段 | Airtable 单表上限 500 字段，当前 100 个安全；但 Link 字段过多可能影响性能 |
| **Link 字段 PATCH 需 record ID** | 人员名称无法直接写入 | 必须先读 People 表全量，本地构建映射字典 |
| **Excel 空值/格式异常** | 写入失败或脏数据 | 标准化处理：空值跳过、日期取第一个（Planned MP Date 历史问题）、文本 strip |
| **逐条 PATCH 超时** | 大批量同步中断 | 必须用批量 API（每批 10 条），加 checkpoint 断点续传 |
| **SKU 级 → 项目级聚合** | 同一项目多 SKU 数据冲突 | 明确聚合规则：日期取 min/max、文本取首行、计数取 sum |
| **字段类型不匹配** | API 返回 422 | 日期必须 `YYYY-MM-DD`、singleSelect 值必须在选项列表内 |

---

## 八、ALL Tracker 表（tbl6BKcL7qnsfsXrT）的定位

当前 ALL Tracker 表在 Airtable 中的角色：
- **已有 49 个 multilineText 字段**：全是文本副本，无 Link 关系，无公式，无自动化
- **建议**：ALL Tracker 表可作为 Excel 的"镜像副本"保留（只读参考），**主同步链路应是 Excel → Projects 表**（业务核心）
- 如需要 ALL Tracker 表也同步更新，可额外建立 Projects → ALL Tracker 的反向映射，但优先级低于 Projects 表

---

## 九、下一步（待用户确认）

1. **确认同步字段范围**：P0 全部？P0+P1？还是全部 50 列？
2. **确认新建字段**：是否在 Projects 表新建 §四 中的 8 个字段？
3. **确认匹配规则**：SKU 级 → 项目级的聚合规则（日期取 earliest/latest？文本取 first？）
4. **确认同步方向**：单向（Excel → Airtable）还是双向？
5. **提供最新 Excel**：确认使用 `All Projects Tracker 0603_更新_20260917_161052.xlsx` 作为同步源

---

*本方案基于 2026-09-18 的 Airtable Meta API 查询结果和 ALL Tracker Excel 结构分析生成。*
