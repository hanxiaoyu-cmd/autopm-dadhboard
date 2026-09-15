# qoder 固定入口

先读 [根规则](../../../AGENTS.md)、[当前决定](../../README.md)、[分工指南](../../使用分工指南.md)，再读原Issue和inbox任务。根规则优先于历史任务包。

每天启动时检查自己的任务，先列计划等用户确认，随后在Issue记录确认范围、执行身份和版本再执行。已提交结果不重复执行，重试沿用task_id并增加attempt。

独立分支提交PR；基准分支读取总协调Issue。

inbox由Codex维护；work存获准的过程文件；outbox/<任务ID>/result.md存结果、确认、变更、验证与回退。采用 [DELIVERY](../../planning/templates/DELIVERY.md)，最终验收由Codex完成。

用户已向辅助AI传达协作要求；实际产品身份、私有访问、交付和调度能力须分别验证。不得把文件存在或用户设置API当作已经运行。各自使用获准认证，不读取他人凭据。

## Power Apps 长期任务（2026-09-15）

从 [迁移 inbox](inbox/POWERAPPS-MIGRATION.md) 开始，阅读原Issue及最新评论。已确认范围不重复询问；每轮结束或阻塞必须在原Issue提交检查点、提交/PR、验证和下一步，outbox 使用 DELIVERY。具体范围及依赖以正式任务书为准。
