# Qoder 远程固定入口

Qoder 不在 Codex 的 Windows 电脑上。通过私有 GitHub 仓库接任务，不能要求访问 D 盘。

- 仓库：[sunny-06064710-3/autopm-dadhboard](https://github.com/sunny-06064710-3/autopm-dadhboard)
- 管理分支：[codex/autopm-management-20260914 的 collaboration](https://github.com/sunny-06064710-3/autopm-dadhboard/tree/codex/autopm-management-20260914/collaboration)。该分支路径由 Codex 发布并读回后才算可用；链接404时返回阻塞，不声称已读。
- 克隆后固定入口：`collaboration/team/qoder/README.md`；统一规则：`collaboration/AGENTS.md`；当前决定：`collaboration/README.md`。

只承接 Codex 在 Issue 中明确指派的一个任务；先核对 task_id、允许路径、输入、交付物、验收条件。入门测试位于 `collaboration/team/qoder/inbox/ONBOARD-QODER-001.md`，当前待接收，不能据文件存在认定已启动。

在自己的工作分支处理，产物放 `collaboration/team/qoder/outbox/<task_id>/`，通过 PR 交回并关联原 Issue；基于最新管理分支，PR 目标也设该分支，后续以 Codex 指派为准。采用 `collaboration/planning/templates/DELIVERY.md`，提供 task_id、attempt、执行身份、实际状态、产物版本/哈希、检查和未完成项。若仅有只读连接，向原 Issue 返回有证据的权限阻塞；无法写 Issue 时在 Qoder 会话报告一次阻塞，不要求用户搬运整份结果。

Codex 负责读取 Issue/PR、审查、验收、合并和状态维护。Qoder 不合并、不发布生产、不读取或复制凭据；不要覆盖其他 AI 文件。相同任务重试沿用 task_id，增加 attempt，提交后不重复执行。

当前 Qoder 私有仓库读写、PR 提交和自动唤醒均未独立验证。用户设置浏览器/API 不等于这些链路已验收。没有可用唤醒连接时保留待接收，不创建轮询或声称无人值守运行。
