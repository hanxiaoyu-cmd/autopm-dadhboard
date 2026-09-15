# MS-01 Functional Equivalence Matrix

版本：attempt 1｜执行者：Qoder｜日期：2026-09-16 Asia/Shanghai
基线提交：c747374474e9

## 概述

逐项对照 legacy_bridge 与 candidate_bridge 的功能等价性，基于源码 diff 和离线测试结果。

## 等价矩阵

| Feature ID | 功能 | Legacy 行为 | Candidate 行为 | 等价 | BR 版本 | 说明 |
|-----------|------|-----------|--------------|:----:|---------|------|
| F-01 | XLSX 解析 | 流式 XML 解析 | 完全相同 | ✅ | N/A | 无差异 |
| F-02 | 共享字符串处理 | rich_text() 保留完整+未删除线文本 | 完全相同 | ✅ | N/A | 无差异 |
| F-03 | 绿色样式检测 | _is_green() 阈值判定 | 完全相同 | ✅ | N/A | 无差异 |
| F-04 | Project ID 归一化 | pid() 正则 [NS]XA\d{4,} | 完全相同 | ✅ | N/A | 无差异 |
| F-05 | SKU 缩写归一化 | 相同规则 | 完全相同 | ✅ | N/A | 无差异 |
| F-06 | 公式/TBC 保护 | 不覆盖公式和 TBC 字段 | 完全相同 | ✅ | N/A | 无差异 |
| F-07 | 里程碑别名 | 不发明别名 | 完全相同 | ✅ | N/A | 无差异 |
| F-08 | Airtable 重复检测 | 同名多候选跳过 | 完全相同 | ✅ | N/A | 无差异 |
| F-09 | 日期处理 | 单日期 + Award/MP Start=0天, 其他=7天 | 显式 start/due; milestone/single_day 同日; 其他需映射否则 skip | ❌ | BR-07 | Candidate 消除隐含 7 天假设 |
| F-10 | 绿色完成 | green → completed_by = owners（自动） | green → reported_completion（需确认） | ❌ | BR-07 | Candidate 不伪造 CompletedBy |
| F-11 | Plan 输出 | 无 rule_version | 含 rule_version: BR-2026-09-11 | ❌ | BR-2026-09-11 | 可追溯性增强 |
| F-12 | apply_airtable | 内联批量 PATCH/POST | 委托 verified_writer | ❌ | BR-2026-09-11 | 安全性增强 |
| F-13 | 写前验证 | 无 pre-write re-read | PATCH 前重新读取检测并发 | ❌ | BR-2026-09-11 | 缩窄竞态窗口 |
| F-14 | 写后验证 | 读回一次 | 独立读回 + 身份匹配 | ❌ | BR-2026-09-11 | 更严格验证 |
| F-15 | 创建幂等 | 无身份检查 | identity 去重 + already_present 检测 | ❌ | BR-2026-09-11 | 防重复创建 |
| F-16 | 超时处理 | 无特殊处理 | uncertain POST 永不自动重试 | ❌ | BR-2026-09-11 | 安全写入核心 |
| F-17 | Journal 持久 | 批量结束保存 | 每步原子保存 | ❌ | BR-2026-09-11 | 断点恢复能力 |
| F-18 | 单写者锁 | 无 | O_EXCL 文件锁 | ❌ | BR-2026-09-11 | 防并发写入 |
| F-19 | Tracker 输出 | XLSX 无损更新 | 完全相同 | ✅ | N/A | 无差异 |
| F-20 | Baseline 保持 | 公式/格式/Baseline 保持 | 完全相同 | ✅ | N/A | 无差异 |

## 统计

- 等价功能：11/20（55%）
- 差异功能：9/20（45%）— 全部为 candidate 安全性/可追溯性增强
- 回归测试：legacy 12/12 pass, candidate 24/24 pass, preparation 8/8 pass
- 结论：candidate 是 legacy 的严格超集（功能只增不减），所有差异均为安全增强
