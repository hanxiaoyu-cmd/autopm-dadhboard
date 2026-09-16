# AutoPM 本地体验网站

这是用于讨论真实操作方式的可交互原型，覆盖个人工作、项目、项目组合、状态报告、支持与经验、部门六个中心。

入口：http://127.0.0.1:4177

后续重新打开，双击本目录的 **Open AutoPM.cmd**。网页界面全部使用英文。

## 推荐这样试一遍

1. **My Work**：默认显示当前人员需要处理的工作。右上角点击姓名可搜索同事（姓名、邮箱、部门）。打开任务填写Latest update，必要时勾选My part is complete，再Save update。日期、Owner和计划设置默认收起。
2. **Project Center**：打开项目，依次看Overview、Plan & Assessments、SKUs、Issues、Team、Documents、History。在评估Task的Follow-up work里点Save & plan follow-up，会先保存当前评估结果，再准备独立执行Task，确认创建后保留评估来源。
3. **Portfolio**：打开Program，查看所有关联项目与SKU。点SKU可以查看它在具体项目中的状态和日期例外，不覆盖另一个项目的同一SKU。
4. **Status Reports**：选择一个/多个项目，也可以叠加Program、部门、Health筛选。Export CSV导出当前范围；Save snapshot保存固定版本。
5. **Support & Knowledge**：新增Issue，增加独立Recovery Action。措施逐项完成或取消，问题负责人点Resolve issue提交结果，项目负责人点Review resolution确认关闭或退回；Save as a lesson沉淀经验；Use in a project生成预防Task。
6. **Departments**：选择部门，查看该工作方向的评估、任务、问题、支持的项目及人员工作分布。计数是任务数量，不冒充工时或人员利用率。

可以新建项目并自动生成跨部门评估任务，也可以编辑团队、添加项目资料引用、打开和下载示例文件。

## 数据是真实的还是示例？

- 原始场景：6个Program、14个Project、224条Tasks等。当前追加规模场景后，初始参考合计1,062名人员、134个Project、4,064条Tasks、68条Issues、204条措施。用户新增记录会使当前数量增加。
- 两个Program及部分Project/SKU身份和关系来自此前本地Airtable导出；其他Program名称来自用户提供的参考。
- **负责人分配、状态、日期、问题、解决结果和文件内容是演示场景，不是当前正式项目事实。** 虚构项目用DEMO开头，页面顶端持续显示Design sandbox。
- 场景日期固定为2026-09-14，使“今天、逾期、本周”能稳定演示，不冒充电脑当前日期。
- 不连接或写回Airtable、Microsoft、ECN，不发送邮件。

## 本轮字段微调落实在哪里？

只调整本地原型的数据模型；没有更改生产Airtable字段。

| 对象 | 本地原型中的补充 | 业务用途 |
|---|---|---|
| Project | 整体Stage、Health、项目Lead、Scope与最新Summary分开 | 看清项目在哪一阶段、谁统筹、此次改什么、目前有什么变化 |
| Task | Workstream、Kind、Brief、Outcome、Assessment Decision | 部门评估要留下结论，不能只剩完成标记 |
| Task | 实际Predecessors、Source Assessments、预估Duration及单位 | 说明先后关系，以及执行工作来自哪次评估 |
| Task | Test Result、外部Approval Status与Decision Date | 测试完成不等于通过；提交ECN不等于批准 |
| Issue | Details、Impact、Resolution、Actual Closed Date、Prevention、Occurrence Phase | 从登记走到解决，并留下可复用经验 |
| Issue Actions | 每项措施独立Owner、Due、Status、Result | 解决一段Recovery文字无法分别追踪多项措施的问题 |
| ProjectSKU | 项目内执行状态、日期例外和原因 | 同一SKU跨项目互不覆盖 |
| Report snapshot | 保存当时筛选范围和数据 | 后续修改项目不改写既有报告 |

Task的多Owner完成确认保留，独立于技术结果；不把Issue普通措施自动加入项目Tasks。不在本轮重新定义正式项目进度算法，页面展示的是“Tasks confirmed”计数。

原型中SKU的演示日期锚点明确采用Project Target MP；这不是对线上Airtable全部里程碑Start/Due映射的批准或迁移。

## 不重复维护的规则

- 同一Task被My Work、Project、Department与Report查询，不复制一份新任务。
- 一个Issue直接归属Project，可选关联受影响Task及ProjectSKU。
- Issue措施独立保存；关闭问题需要实际Resolution，尚未处理的措施需先完成或取消。
- Lesson引用原Issue，再由用户决定是否把预防工作放进另一个项目计划。
- 外部审批仍在ECN，网页只跟踪其结果；示例文件明确写明不是正式工程放行资料。

## 本地保存与启动

- 当前内容：data/state.json；每次成功写入保留上一次data/state.json.bak。
- 初始场景：data/seed.json。启动时只有不存在state.json才复制种子，不会覆盖你的体验修改。
- 导出的CSV和示例资料副本保存在data/exports，页面提供Open file和Download copy；即使浏览器下载受限，已生成的本地副本仍保留。
- 后端：server.mjs，仅监听127.0.0.1:4177。网页静态资源只从dist提供，不暴露整个Workspace。
- 写入有版本检查，拒绝旧版本覆盖新状态。不是公司生产权限系统；角色体验开关已移入Demo settings，切换人员仍是本地模拟身份。
- API：GET /api/state；POST /api/operation。所有页面使用相同业务处理器dist/model.js。
- qa与test在隔离副本中验证。规模模拟数据由tools/scale-sample.mjs一次性追加到本地体验数据，原有记录不覆盖；state.before-simplification-20260913.json保留追加前备份。

## 开发者接手

- 业务和字段：dist/model.js、tools/make_seed.py。
- 六个中心与交互：dist/app.js；简化工作台：dist/simple-ui.js；默认规则：dist/workflow-rules.js；样式：dist/style.css。
- 单元与界面处理器测试：test/domain.test.mjs、test/workspace.test.mjs。
- 运行测试：node --test test/*.test.mjs。DOM测试依赖保存在qa/package-lock.json中；全新电脑需在qa目录npm install。
- 可选WebMCP：列出当前人员工作、打开项目、保存Task Outcome；普通浏览器不支持时不影响网页使用。

正式迁移到Airtable Interface或Power Apps前，仍需完成权限、自动化消费者、真实文件访问、导入/Tracker、字段映射与规模验证。此网站交付的是可尝试的设计和业务交互，不把这些后台生产能力假装成已经部署。

## GitHub 源码与部署边界

- 此目录是可复现的本地演示源码：先运行 `npm test`，再运行 `npm start`。
- 当前服务刻意只监听 `127.0.0.1`，并将体验过程写入本地 `data/state.json`；GitHub Pages 只能托管静态文件，不能完整运行这个版本。
- 需要公开演示网址时，请按仓库根目录的 `DEMO-DEPLOYMENT-TASK.md` 执行。部署人员必须先明确演示数据的保存与访问策略，再提交独立 PR。

## 2026-09-13 简化版

- 日常新增任务只需项目、任务名、截止日期；有项目上下文时自动带入项目，负责人优先来自项目成员。任务类型、工作领域由明确的标题规则和模板上下文预设，未知任务保留普通执行类型；不推断完成或审批结果。
- 有1000多人时不展开整个名册；一次显示最多25个搜索结果，可按邮箱定位同名人员。任务Owner优先显示当前项目团队，额外人员通过搜索查找。
- 任务列表先显示10项，可继续展开；按任务名、项目编号或项目名称搜索全量本人范围。已关闭项目有遗留任务时仍显示。
- 任务的类型、日期、人员、工期及关联仍可在收起的设置中维护。普通更新不需要选择这些值。
- ECN直接使用ECN status和Decision date，不附加业务解释。
- Issue入口按当前职责显示动作；关闭保留操作者、时间、结果及事件历史。不同模拟身份的操作检查不代表公司生产认证已经实现。
- 数据与场景仍然保存在本机，不写回Airtable或Microsoft。新增模拟人员邮箱使用example.invalid。

本轮验收：[简化与规模测试记录](qa/simplification/REVIEW.md)。
