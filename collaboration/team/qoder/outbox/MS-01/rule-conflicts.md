# MS-01 Rule Conflicts

版本：attempt 1｜执行者：Qoder｜日期：2026-09-16 Asia/Shanghai

## 概述

记录 legacy_bridge 与 candidate_bridge 之间的业务规则冲突，以及需要 Codex 裁决的事项。

## 规则冲突清单

### RC-01：日期语义（TC-04 相关）

| 维度 | Legacy | Candidate | 冲突影响 |
|------|--------|-----------|---------|
| 规则 | 单日期 + 7 天默认偏移 | 显式 start/due；无默认 | 相同输入产生不同日期范围 |
| 示例 | 输入 2026-09-18 → Start=09-18, Due=09-25 | 输入 2026-09-18 → Start=Due=09-18（里程碑）或 skip（非里程碑无映射） |
| TC-04 验证 | "Baseline仍为09-18" — 通过 | "点状节点 Start=Due" — 通过；"含义不明日期报映射异常，不统一加7天" — 通过 |
| 裁决需要 | 是否接受"无映射则跳过"替代"默认7天"？ |

**建议**：采用 candidate 规则。TC-04 明确要求"含义不明日期报映射异常，不统一加7天"，candidate 行为与验收标准一致。

### RC-02：绿色完成处理（TC-18 相关）

| 维度 | Legacy | Candidate | 冲突影响 |
|------|--------|-----------|---------|
| 规则 | green + owners → completed_by = owners | green → reported_completion（需确认） | 相同绿色标记产生不同完成状态 |
| TC-18 验证 | "源周报绿色但无Owner确认" — legacy 自动设 completed_by | "记录 SourceReportedComplete 及出处；不伪造 CompletedBy/核验" — candidate 行为匹配 |
| 裁决需要 | 是否接受"报告而非自动确认"？ |

**建议**：采用 candidate 规则。TC-18 明确要求"不伪造 CompletedBy/核验"，candidate 行为与验收标准一致。Legacy 自动设置 completed_by 违反了"源声称完成不等于正式确认"的业务规则。

### RC-03：写入安全模型（TC-17 相关）

| 维度 | Legacy | Candidate | 冲突影响 |
|------|--------|-----------|---------|
| 规则 | 批量写入，结束时保存 journal | 逐条原子写入，每步保存 journal | 中断后恢复能力不同 |
| TC-17 验证 | "第2个创建已落地但响应超时" — legacy 无特殊处理 | "先查询身份/回执确认未知结果" — candidate 检测 uncertain POST |
| 裁决需要 | 是否接受 verified_writer 作为唯一写入路径？ |

**建议**：采用 candidate 的 verified_writer。TC-17 要求"创建更新均读回，差异不标 verified"，verified_writer 的 post-write readback 和 ReconciliationRequired 机制满足此要求。

## 非冲突差异

| ID | 差异 | 性质 | 影响 |
|----|------|------|------|
| NC-01 | rule_version 字段 | 增强 | 无破坏性；提供可追溯性 |
| NC-02 | reported_completion 列表 | 增强 | 新增输出字段，不影响既有消费者 |
| NC-03 | 单写者锁 | 增强 | 防并发；不影响单实例部署 |
| NC-04 | identity 去重 | 增强 | 防重复创建；不影响正常流程 |

## 待 Codex 裁决

1. **RC-01**：确认日期规则采用 candidate 版本（消除 7 天默认值）
2. **RC-02**：确认绿色完成采用 candidate 版本（报告而非自动确认）
3. **RC-03**：确认 verified_writer 作为唯一写入路径
4. 确认 `rule_version: 'BR-2026-09-11'` 为正式规则版本号
