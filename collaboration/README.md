# AutoPM 管理入口

Codex 负责主维护、计划、Issue 发布、分派、审核和集成。执行 AI 按指定任务工作。

- [使用分工指南](使用分工指南.md)
- [协作总 Issue #1](https://github.com/sunny-06064710-3/autopm-dadhboard/issues/1)
- [全部开发任务](https://github.com/sunny-06064710-3/autopm-dadhboard/issues)
- [任务编号与 GitHub 链接](issue-map.json)
- [DuMate 入口](team/dumate/README.md) / [Qoder 入口](team/qoder/README.md)
- [AI-03](team/ai-03/README.md) / [AI-04](team/ai-04/README.md)：产品身份待明确，浏览器/API 为用户报告已配置，尚未独立验收。

## 当前业务决定

1. 9/13评估覆盖16表424字段，是历史快照；9/11的18表499字段也是历史范围，不能表示当前线上实测。
2. 保留现有Task完成机制，暂停项目进度改造。AT-01等旧任务标为Deferred，不能直接实施。
3. Task承载项目计划；业务Issue及其措施承载异常处理；GitHub Issues承载AutoPM开发工作。
4. 根据保存的交接证据，现有Program市场清单已发布；报告、部门和知识库有未验收草稿；新增Program补市场脚本有离线测试但尚未线上启用。
5. Power Apps保留既有MVP与双路线规划；本次管理设置不授权全面迁移、停用Airtable或生产发布。

## 资料与状态

`planning/`保留33个历史工作包、蓝图、验收用例和模板。`review-2026-09-13/`保留业务适用性评估及证据；`current/`保留后续界面交接和市场脚本。冲突以用户最新决定和协调方Issue中的明确范围为准。

Issues用Backlog、Ready、Blocked、Deferred、In progress、In review、Accepted标签表示状态。没有明确执行者与派工评论，Ready也不代表AI已经启动。执行者在Issue中接收并提交结果，Codex检查后更新状态。

现有PAT已通过仓库访问；创建GitHub Projects返回`Resource not accessible by personal access token`。当前使用Issues和标签管理，看板单独列为权限阻塞，不阻塞执行。

DuMate本地文件交接产物已核验。Qoder在另一台机器，必须使用GitHub。没有已验证的自动唤醒连接，不声称各AI持续后台运行。
