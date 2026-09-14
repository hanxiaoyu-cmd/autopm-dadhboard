# ONBOARD-QODER-001：远程 GitHub 接入测试

状态：Prepared / 待接收；attempt：1；真实执行会话待回执。没有声称已启动或验收。

目标：证明 Qoder 能从私有仓库读取指定资料，通过独立分支及 PR 交回结果。此测试不证明生产系统访问或自动唤醒。

仓库 `sunny-06064710-3/autopm-dadhboard`，基准分支 `codex/autopm-management-20260914`。在线入口：https://github.com/sunny-06064710-3/autopm-dadhboard/tree/codex/autopm-management-20260914/collaboration 。分支未发布时报告阻塞，不猜测文件内容。

只读输入：`collaboration/team/qoder/README.md`、`collaboration/AGENTS.md`、`collaboration/README.md`、`collaboration/planning/templates/DELIVERY.md`。不得读取本机 D 盘或凭据。

允许写入：独立工作分支中的 `collaboration/team/qoder/outbox/ONBOARD-QODER-001/result.md`。内容含任务 ID、attempt、真实执行身份、时间、读取分支与提交、实际读取文件、三条当前业务约束、状态、产物哈希（无法计算注明）。不修改其他文件。

提交：创建 PR 指向上述管理分支，关联 Codex 指定的原 Issue。Codex 读回 PR、核对内容和范围后验收；Qoder 不合并。没有写权限时明确报告 Blocked，不尝试复制认证材料或绕过授权。

验收：私有读取成功、源提交可追踪、三条约束与输入一致、变更只有允许文件、PR 可由 Codex 读取。没有自动触发证据则自动唤醒仍未验证。失败不要自动循环重试。
