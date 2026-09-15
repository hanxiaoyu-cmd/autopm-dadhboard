# AutoPM

AutoPM 项目资料、应用代码和多 AI 协作仓库。Codex 负责主维护、任务统筹、审核和集成；执行 AI 按用户确认的范围交付。

## 从这里开始

1. 所有 AI 必读 [AGENTS.md](AGENTS.md)。
2. 查看 [当前业务决定与团队入口](collaboration/README.md)、[使用分工指南](collaboration/使用分工指南.md)。
3. 从 [总协调 Issue #1](https://github.com/sunny-06064710-3/autopm-dadhboard/issues/1) 获取有效分支和任务；未确认前只整理计划。

过渡期：本规范位于 `codex/autopm-management-20260914`，通过 [PR #44](https://github.com/sunny-06064710-3/autopm-dadhboard/pull/44) 集成。合并前不能假定 main 已包含这些文件；后续基准分支以总协调 Issue 为准。

## 目录与事实来源

| 位置 | 用途 |
|---|---|
| `backend/` | 当前服务代码；部署配置见 `render.yaml` |
| `backend/frontend/` | 当前服务实际挂载的前端目录 |
| `frontend/`、`backend/static/` | 历史/其他候选前端，未确认用途前不要作为当前修改入口 |
| [docs](docs/README.md) | 文档索引、来源边界、历史归档 |
| [collaboration](collaboration/README.md) | 当前决定、分工和交付模板 |
| `collaboration/team/<角色>/outbox/<任务ID>/` | 一项任务的确认记录、结果、测试与变更日志 |
| GitHub Issues / PRs | 当前任务状态 / 实际变更和审查证据 |

`backend/main.py` 使用 `backend/frontend/`；`render.yaml` 从 backend 启动服务。这里是代码配置判断，不代表线上部署已验收。历史页面、bak及辅助脚本暂留原位，改动前须检查消费者。

根目录不存临时文件、个人记忆或重复任务台账。历史资料不构成执行授权，入口见 [归档说明](docs/archive/README.md)。
