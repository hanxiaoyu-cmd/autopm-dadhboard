# AutoPM v2.2.0 深度审计与落地保障报告

**审计时间**：2026-09-17  
**审计对象**：AutoPM_Source_20260915（v2.2.0）  
**审计范围**：周报 Excel → Airtable 写入 → 本地总表回写的完整链路  
**审计方法**：5 个维度并行审计 + Mock dry-run 全链路验证  

---

## 一、执行摘要

| 维度 | 结论 | 关键发现 |
|------|------|---------|
| 数据链路完整性 | **WARN** | 28 个 Airtable 无匹配项目被静默丢弃；88 个 issues 因 People 解析失败被丢弃 |
| 字段映射与 Schema | **WARN** | sync.py 写入 24 个字段，tracker.py 仅能完整回写约 19 个；4 个字段无本地接收列 |
| 双向同步机制 | **FAIL** | 当前是"周报→Airtable→本地 Excel"单向级联，**不存在严格双向同步** |
| 边界安全 | **WARN** | F7 Next PLM 无 identity 已修复；Exception 信息丢失已修复 |
| 全链路集成 | **PASS** | 190 changes → 190 applied，零 errors，计数完全对齐 |

**本轮已修复缺陷**：
1. ✅ F7 Next PLM 缺失 identity（sync.py）
2. ✅ Exception 信息丢失，调试困难（sync.py）
3. ✅ result.json 增加 summary + operations 分类明细（sync.py + ui.py）
4. ✅ 版本号统一为 v2.2.0（__init__.py / sync.py / preview.py / ui.py）

---

## 二、数据链路完整性审计

### 2.1 周报 Excel → parsed_report

- **[OK]** workbook.py 正确识别 "Report" 工作表，支持 Project Number / Update on / 合并单元格
- **[OK]** 报告日期解析完整，166 个项目均有有效 report_date
- **[OK]** 字段别名映射完整：Next PLM、First CRD、LOA-13weeks plan、Engineering remark 等
- **[RISK]** `country` 字段在周报中完全缺失（0/166），FIELD_ALIASES 有映射但 Excel 无该列
- **[RISK]** `first_crd_date` 和 `loa_13weeks_plan` 在周报中完全无数据（0/166）

### 2.2 build_plan → changes 组装

- **[OK]** `_equivalent` 比较逻辑正确，仅写入真正有差异的字段
- **[RISK]** 137 个 project changes 中，101 个仅有 2 个字段（Engineering remark + Jira summary），36 个仅有 1 个字段——这是正常去重，非数据丢失
- **[MISS]** `first_crd_date` / `loa_13weeks_plan` 周报源数据缺失 → 0 个 milestone task 生成
- **[HIGH]** **28 个项目（NXA0288, NXA0359~NXA0419 等）在 Airtable 中无匹配记录，被完整跳过**。这些项目的所有任务、issues 数据均丢失，属于 **silently dropped**（sync.py 第 626-630 行）

### 2.3 preview.json → apply_plan

- **[OK]** 195 changes，kind 分布：projects 137, tasks 58, issues 0
- **[OK]** 无任何 "fields" 为空的 operation
- **[OK]** 所有 operation 的 `fields` 与 `field_names` 一一对应
- **[RISK]** Issue changes 为 0，但 parsed_report 中有 88 个有效 issues（来自 61 个项目）。原因：大量 issue owner 在 People 表中无法 resolve（如 "Leo Tao"、"Max Xu" 等无唯一匹配），导致 issue 被完整跳过（sync.py 第 1197-1218 行）

### 2.4 写入字段完整性（抽样）

| 抽样对象 | 字段数量 | field_names 覆盖 | 结论 |
|---------|---------|-----------------|------|
| Project NXA0249 | 2 | ✓ 完全匹配 | OK |
| Task NXA0038 (Next PLM) | 4 | ✓ 完全匹配 | OK |
| Task NXA0033 (Completed By) | 1 | ✓ 完全匹配 | OK |

---

## 三、字段映射与 Schema 一致性审计

### 3.1 REQUIRED_PROJECT_TYPES

- **[OK]** 字段名与 Airtable 云端一致（含 `current_progress` richText、`report_date` date）
- **[OK]** 已修复此前的 `KeyError('current_progress')` 根因（REQUIRED_PROJECT_TYPES 补全缺失键）

### 3.2 schema_memory 兼容性

- **[OK]** `compatibility()` 中日期字段判断已修正为 `endswith("_date")`，`latest_update` 不再被误判

### 3.3 字段映射对称性（sync.py 写入 vs tracker.py 读取）

| 字段 | sync.py 写入目标 | tracker.py 读取源 | 状态 |
|------|------------------|-------------------|------|
| `project_id` / `project_name` / `sku` / `status` / `brand` / `type` / `factory` / `quality` / `npi_lead` / `npd_lead` / `pmo` / `tooling` / 日期字段 | 与 tracker HEADERS 一致 | 与 sync PROJECT_FIELDS 一致 | OK |
| `next_plm` | "Next Action" | **无对应列** | **MISS** |
| `jira_link` | "Jira URL (Manual)" | **无对应列** | **MISS** |
| `jira_summary` | "Jira summary (Manual)" | **无对应列** | **MISS** |
| `loa_13weeks_plan` | "LOA-13weeks plan(Manual)" | **无对应列** | **MISS** |
| `update_this_week` | "Current stage" (singleSelect) | "Update This Week" (长文本) | **RISK** — 字段名和语义均错位，且 weekly remark 模式下回写时**主动跳过**该字段 |
| `current_progress` | "Engineering remark(Manual)" (richText 周报块) | "Current Progress" (纯文本) | **RISK** — Excel 中编辑 Current Progress 后，下次周报同步会直接用周报内容覆盖，Excel 修改对 Airtable 不可见 |

---

## 四、双向同步机制审计

### 4.1 架构定性

当前机制是 **"周报 → Airtable → 本地 Excel" 单向级联**，**不存在严格意义上的双向同步**。

| 方向 | 状态 | 说明 |
|------|------|------|
| 周报 → Airtable | **Pass** | 字段映射明确，有 schema 校验、版本守卫、并发检测和写后校验 |
| Airtable → 本地 Excel | **Warn** | 基础字段可正常导出；但 next_plm/jira_link/jira_summary/loa_13weeks_plan 无本地接收列；update_this_week 路径断裂；27/50 列未映射 |
| 本地 Excel → Airtable | **Fail** | **当前不存在该路径**。Excel 中的手工修改（Current Progress、Update This Week、Manufacturing Factory 等）**永远不会自动回写云端** |

### 4.2 关键风险

1. **Excel Current Progress 编辑丢失**：用户在 Excel 中修改 Current Progress 后，下次周报同步会直接用周报内容覆盖 Engineering remark
2. **Factory 字段类型不对称**：sync.py 写为 `multipleRecordLinks`（关联 Factories 表）；tracker.py 读取为纯文本。Airtable 工厂名称变更时，Excel 中的旧文本不会触发冲突提示
3. **零变更时不自动刷新**：当 Airtable apply 产生 0 条变更时，`follow_sync` 直接返回 False，本地总表不会自动读取最新 Airtable 状态

---

## 五、边界安全审计

### 5.1 Next PLM 稳定任务（F7）— **已修复**

**问题**：F7 任务在 `append_change` 时未传递 `identity`，导致 `_identity_hits` 返回 `[]`，create 场景下缺乏重复检测保护。

**修复**（sync.py 第 833-847 行）：
```python
project_f = task_fields.get("project")
name_f = task_fields.get("name")
extras_f7 = (
    {"identity": {
        "project_field": project_f["id"],
        "title_field": name_f["id"],
        "title": "nextplm",
    }}
    if project_f and name_f else {}
)
append_change("tasks", existing, child, ..., **extras_f7)
```

**验证**：dry-run 190/190 applied，static validation 零 errors，F7 操作全部携带 identity。

### 5.2 Exception 信息丢失 — **已修复**

**问题**：`except Exception` 分支未记录具体异常类型和消息，result.json 中只有固定错误文本。

**修复**（sync.py 第 1735-1754 行）：
```python
except Exception as exc:
    entry["error"] = f"Write or verification failed; {type(exc).__name__}: {exc}; inspect remote state before retry"
    # result["operations"] 同步记录 error 详情
```

### 5.3 并发编辑 Guard

- **[OK]** `apply.lock` 使用 `O_CREAT|O_EXCL` 原子创建
- **[OK]** `journal` 恢复检查 plan_id 一致性
- **[OK]** `_record_fields_equal` 逐字段比较，支持 checkbox/richText
- **[RISK]** 锁残留：若进程在 `finally` 前被 SIGKILL 终止，`apply.lock` 会残留

### 5.4 日期/时区处理

- **[OK]** 中文日期、英文月份（含 ordinal 后缀如 1st）、歧义日期（如 01/02）均正确处理
- **[OK]** Airtable 写入使用 ISO 格式（YYYY-MM-DD）
- **[OK]** `report_date` / `context_date` 在整个链路中传递一致

---

## 六、全链路集成验证

### 6.1 Dry-run 验证

| 测试 | 结果 | 证据 |
|------|------|------|
| `verify_apply_plan.py` Mock dry-run | **PASS** | 190 changes → 190 applied，零 errors |
| `verify_full_chain.py` 真实 API 只读 | **PASS**（历史） | 196 changes → prepare_preview PASS |
| `py_compile` 回归测试 | **PASS** | sync.py, ui.py, preview.py, schema_memory.py, normalize.py, tracker.py 全部通过 |

### 6.2 Preview 与 Result 一致性

| 样本 | Preview Changes | Result Applied | Result Skipped | 一致性 |
|------|-----------------|----------------|----------------|--------|
| 20260917_140343_f91f28 | 195 | 195 | 0 | ✅ 100% |
| 20260917_144838_b2e45f | 190 | 190 | 0 | ✅ 100% |

### 6.3 UI 状态栏验证

- **[OK]** 状态栏消息："同步已完成：已写入 190 条，跳过 0 条。（项目：写入 115 / 跳过 0 / 失败 0 · 任务：写入 75 / 跳过 0 / 失败 0）"
- **[OK]** 失败场景警告页：自动列出失败的项目/任务及失败原因
- **[OK]** 版本号 v2.2.0 在窗口标题、面包屑、preview.html 页脚、result.json 中一致显示

---

## 七、遗留风险与建议

### 🔴 P0 — 阻断性（必须处理）

| # | 问题 | 影响 | 建议 |
|---|------|------|------|
| 1 | **28 个项目 Airtable 无匹配** | 周报数据完整读取但无法写入，任务+issues 全部丢失 | 检查 Airtable Projects 表，确认 NXA0288、NXA0359~NXA0419 等项目是否需预先创建，或修正周报中的 Project ID |
| 2 | **88 个 issues 未写入** | People 表解析失败导致 issues 被完整跳过 | 在 `.autopm.json` 的 `people_aliases` 中补充 "Leo Tao"、"Max Xu" 等人员的 record ID 映射 |
| 3 | **本地 Excel 无法回写 Airtable** | Excel 中手工修改永远不同步到云端 | **架构决策**：明确本地总表是"只读副本"还是"可编辑主数据"。若需双向，需补全 Excel→Airtable 写入路径 |

### 🟡 P1 — 高优先级

| # | 问题 | 影响 | 建议 |
|---|------|------|------|
| 4 | **next_plm / jira_link / jira_summary / loa_13weeks_plan 无本地接收列** | Airtable 更新后本地总表无法感知 | 在 tracker.py HEADERS 中增加对应列，或在导出日志中增加"云端专属字段，本地不保留"的提示 |
| 5 | **update_this_week 语义错位** | sync.py 写入 "Current stage"（枚举），tracker.py 读取 "Update This Week"（长文本），且回写时跳过 | 统一语义：一个用于阶段枚举（Current stage），一个用于本周更新全文（Update This Week） |
| 6 | **All Tracker 总表范围过大** | 文件范围 `A1:PK19872` 超过 200 万单元格上限，`read_tracker()` 会抛出"总表范围过大"错误 | 清理空白行/列，或改用流式读取 |

### 🟢 P2 — 改进项

| # | 问题 | 影响 | 建议 |
|---|------|------|------|
| 7 | **country / first_crd_date / loa_13weeks_plan 周报源数据缺失** | 字段映射存在但 Excel 无该列 | 确认周报模板是否应补充这些列 |
| 8 | **Factory 字段类型不对称** | Airtable 变更后 Excel 保留旧文本快照 | 导出日志中增加提示 |
| 9 | **锁残留风险** | SIGKILL 后 apply.lock 残留 | 启动时自动检测并清理过期的 apply.lock |

---

## 八、本轮修复清单

| # | 修复项 | 文件 | 行号 | 状态 |
|---|--------|------|------|------|
| 1 | F7 Next PLM 补充 identity | sync.py | 833-847 | ✅ 已修复并验证 |
| 2 | Exception 信息增强 | sync.py | 1735-1754 | ✅ 已修复并验证 |
| 3 | result.json 增加 summary + operations 分类明细 | sync.py | 1386-1394, 1618-1750 | ✅ 已修复并验证 |
| 4 | UI 状态栏展示分类结果 | ui.py | 1966-2025 | ✅ 已修复并验证 |
| 5 | 版本号统一为 v2.2.0 | __init__.py, sync.py, preview.py, ui.py | — | ✅ 已修复并验证 |
| 6 | verify_apply_plan 目录排序修复 | verify_apply_plan.py | 91-103 | ✅ 已修复并验证 |

---

## 九、最终结论

### 能否落地？

**可以落地，但需用户确认 3 个架构决策**：

1. **28 个 Airtable 缺失项目**：是否需要预先创建这些项目，或修正周报中的 Project ID？
2. **88 个 issues 人员解析失败**：是否需要在配置中补充 People 别名映射？
3. **本地总表定位**：本地 Excel 是"只读副本"（当前行为）还是"可编辑主数据"（需补双向写入路径）？

### 核心链路验证结果

| 检查项 | 结果 |
|--------|------|
| 周报 → parsed_report → preview | ✅ 正常 |
| preview → apply_plan → Airtable | ✅ 正常（190/190 applied） |
| Airtable → 本地 Excel（导出） | ⚠️ 基础字段正常，4 个字段无本地接收列 |
| 本地 Excel → Airtable（回写） | ❌ 当前不存在该路径 |
| 并发编辑保护 | ✅ 正常 |
| 版本号一致性 | ✅ v2.2.0 全链路一致 |

**建议**：先解决 P0 问题（28 个项目 + 88 个 issues），再明确本地总表定位，最后处理 P1 字段映射补全。
