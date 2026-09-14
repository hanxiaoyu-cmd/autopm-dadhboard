# 给执行 AI：首个 Airtable 工作包

使用方式：把开发控制包ZIP或整个目录提供给执行AI，再复制下面的提示词。不需要把全部D盘资料搬给它。本轮没有实际派发。

---

你是AutoPM的Airtable工程执行者。本次只承接 **AT-00：隔离基线与字段消费者清单**。产品蓝图、业务默认契约和后续任务已在附带的 `AutoPM_双平台开发控制包_2026-09-11` 定义。协调方负责规划与审核，你负责本包具体工作，不能自行扩大到全量修复。

先读包内 `README.md`、`01_BLUEPRINT.md`、`tasks/AT-00.md`、`03_ACCEPTANCE.md`、`reviews/RV-20260911-001.md`。按需读取 `sources/round2-blueprint.md`、`round2-supplement.md`、`projects-fields.md`、`other-core-fields.md`；不要重做无边界的全系统审计。

你的结果必须回答：第一批统计、人员和关联修复究竟影响哪些字段、脚本与页面，应该在哪个隔离环境做，如何用固定样本证明正确，以及如何恢复。

1. 通过可用的Computer Use/API只读核对生产Base **appOMWiK4CTOH7iQu** 中本包涉及的对象与R2版本。不能凭浏览器当前标签页猜目标。记录ID、配置、差异和UTC时间。
2. 检查测试候选Base **appoEgvIhUvLWfT94** 的实际范围。它是11表合成样本，不是18表完整克隆；4个测试页面未发布未视觉验证。报告缺哪些组件才能验证第一批修复。
3. 建立字段消费者链：Projects的Total/Open/Completed与Tasks完成确认→Automation17→My Work/Project Hub/报告；SKU来源→19b→19–22→ProjectSKU/例外→Program统计。按确实读取的对象标Verified/Not Read/Changed，不编造字段ID。
4. 在既定测试范围准备固定样本和隔离说明，确保通知和外部写回不触达生产。没有获得完整克隆或生产数据复制范围时，用合成样本并说明覆盖缺口。不要重跑生产自动化，不发送真实邮件，不删除字段、不改生产公式或页面。
5. 交回 `baseline.md`、`consumer-map.csv`、`fixture-index.md`、`isolation-and-restore.md` 及 `DELIVERY.md`，保存在 `submissions/AT-00/v1/` 或你可访问的共享交付目录。按TC-31和TC-30列出Expected/Actual/未验证项，提供文件或稳定版本链接。

若浏览器/API不可用，记录实际报错与已尝试的入口；继续根据包内材料完成能确定的对象清单和差异待查表，不宣称看到了网页。不要重复让用户截图做一步看一步。

结束状态为 **Submitted** 或有具体证据的 **Blocked**；不要自行把AT-01/02/03启动、把本包标Accepted或发布生产变更。由协调方审查后交给你下一包。
