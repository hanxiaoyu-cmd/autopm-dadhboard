> 2026-09-15流程更新：先向用户提交本任务计划并取得范围确认，再执行。沿用本地outbox交付，由Codex读取、同步GitHub并验收；此前#32评论中的PR要求对此任务取消。实时状态以#32为准。

# GOV-01：最新业务规则与冲突清单

执行角色：DuMate。状态：Ready / 待接收。Codex已分派文件任务；未取得本次执行回执前不标执行中。

## 目标

整理9/13字段评估与9/14最新界面交接中的业务决定，给Codex一份有来源的冲突清单，供协调方收敛后续任务。只读分析，不改变线上平台。

## 输入与范围

先读本团队入口和根README。输入限本工作区 `review-2026-09-13/README.md`、`FIELD-DECISIONS.md`、`FOLLOWUP-REVIEW.md`，`current/interface-handoff.md`、`planning/design/PROJECT-TASK-ISSUE.md`、`team/codex/outbox/TRIAGE-20260914.md`。

允许写入 `team/dumate/work/GOV-01/` 与 `team/dumate/outbox/GOV-01/`。不修改输入、其他AI目录或业务系统。不读取凭据。不触发自动化、发邮件或创建周期调度。

## 交付

1. `receipt.md`：真实身份、时间、任务ID、实际能读取的输入与缺失项。
2. `result.md`：逐项列出规则、两边来源路径/章节、是否冲突、已明确用户决定、建议给Codex的处理，不自行替用户作新业务决定。
3. 聚焦：Task完成机制/项目进度暂停；Issue默认单措施与多措施建议；部门归属；日期来源；已发布与草稿差别。

## 验收

每条判断必须能定位来源；保留快照日期；不得把未实现建议当现状。特别不得建议恢复暂停的改造。Codex读回原文验证后验收，先提交再等待，不重复执行。

对应GitHub Issue链接由Codex在 `issue-map.json` 的 GOV-01 项维护。文件派工与Issue是同一个任务，不另建平行任务。
