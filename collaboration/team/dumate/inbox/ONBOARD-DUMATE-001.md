# ONBOARD-DUMATE-001：只读接入测试

状态：Prepared / 待接收。执行者角色：dumate；实际会话身份待回执。attempt：1。尚未启动、尚未验收。

目标：证明该 AI 能读取固定入口和指定资料，并把结果交回共享目录。本测试不证明 GitHub、浏览器、API 或自动唤醒能力。

输入仅限：本 AI README、根 AGENTS.md、根 README.md，以及 planning/templates/DELIVERY.md。允许读取这些文件；允许写入本 AI work/ONBOARD-DUMATE-001/ 与 outbox/ONBOARD-DUMATE-001/。其他路径和业务平台不得修改；不得读取凭据或联网发布。

执行：阅读四个输入，写一份 result.md，列出 task_id、attempt、真实执行者与会话标识（若可得）、时间、实际读取文件、三条当前业务约束、产物路径及 SHA256（无法计算则注明）。保留根 README 中的历史快照日期，不能报告成今日实测。先形成回执再交结果亦可。

验收：Codex 独立读回 result.md，核对三条约束与输入一致、任务 ID 正确、输出在允许路径内；核算哈希。文件读写失败则提交 Blocked/needs_input 和错误，不能声称接入成功。

提交采用 DELIVERY 模板的适用项目；未执行项标 Not Run。结果只写本 AI outbox，不由用户复制报告。不得为本测试创建周期任务或自动重试。
