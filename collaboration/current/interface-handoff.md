# AutoPM Interface 实施交接 — 2026-09-14

## 范围与监督

用户授权：完成市场上市清单，直接优化 Portfolio，继续建设 Status Reports、Department management、Support & Knowledge。允许分批交付；难点记录后继续，不长期卡住。scope_supervisor 已参与监督与纠偏，不操作浏览器。

执行约束：一处 UI 问题两种方法失败或约10分钟无进展就记录并切换；不重复全量读取；验收依据为保存后读回/实际预览，不以点击成功代替完成。品牌 Shark 与部门 NPI 分开；人员筛选不能冒充部门筛选。只维护原始业务数据一次。

## 交付状态

| 工作 | 状态 | 证据/限制 |
|---|---|---|
| Market Launch Schedule | 已发布现有 Program 清单 | 152 Programs × 5 = 760 行；3040 日期值对账零差异；Lily 实际发布页验证 |
| 新 Program 自动补五行 | 未完成 | 不能声称全生命周期自动化完成 |
| Portfolio 后续优化 | 已保存草稿 | 删除独立 EU 日期页面组件；市场清单改小尺寸，隐藏行高控制；未二次发布 |
| Status Reports | 隐藏、未发布草稿 | 复用旧 Project report，不是新建重复入口；品牌筛选有效；尚未完成部门与周度报告 |
| Project Status Report | 详情草稿 | 项目ID标题，新增状态解释、Owner、日期、Next Action、Issues；删除失效组件，关闭分组内编辑 |
| Department management | 未实施 | 尚未查看 localhost4177 部门参考页面 |
| Support & Knowledge | 未实施 | 已识别可复用数据表，尚未配置用户入口 |

## 定位

- Base: appOMWiK4CTOH7iQu
- Portfolio: pagWxoZ87HOM12Lmh；Program detail: pagabNDVGYw7XklpA；Lily: recjY5HLyEGhsPm91。
- Program Markets: tblVXMjT7vWeJwthB；Program: fldkjCFcOei2JeqYN；逆向关联 fldnYmBmrPrx5cKTM。
- Market fldjM7TfaYvPteNFf；Market Order fldXL2tSqISHFqtKX；组合键 fldM2nTtnpPvBRIzT。
- 显示公式：DTC fldL6XFGCdlNshzcA；Amazon fldEOeJ1Q5AYWLCs9；Rcom fldkN6KpDonbPtRTI；In Store fldpcZX7uNPaut7mj。
- Status Reports: pagh9nWCD3zQcni8v；Project Status Report detail: pag72ID5HVgRrsfNW。
- 用户的 Portfolio copy 是备份，不删除。

## Status Reports 实际改动与检查

- 复用 Projects 数据；增加 Brand、NPI Owner 筛选；保留 Project Status、搜索和自定义 Filter。
- 删除多余饼图和 Factory 图；剩余 Projects by Status 图原来错误按 Project Type 分类，已改 Project Status、横向。
- Project Updates 显示 Project ID、Planned MP、NPI Owner、Project name、Engineering remark、Next Action；状态前缀保留；列表只读，可进入详情。
- Shark 预览已验证：总项目从2997变为1348，On track 215、At risk 5、Delay 6；明细显示 SXA 项目。此为当前筛选显示值，不代表全量指标口径已审计。
- 单项目详情：Project ID 作标题，全屏；保留 Start/Planned MP，增加名称、品牌、最新进展、更新时间、Issues、Owner、MP Start、Next Action。

### 发布前必须处理

1. 旧报告底部独立 Issues 数据区域可能不跟随 Projects 的 Brand 筛选：验证关联筛选或移除此重复区域，不能展示跨品牌问题却标作品牌报告。
2. 顶部说明编辑不完整，当前开头为 `n status grid...`，需要修正。
3. 多个显示标签仍含 Manual/技术命名；详情 Latest Update 标签是否保存需要读回。
4. NPI Owner 是人员，不是 Department。Projects 没有明确 Department 字段，不根据历史有污染的 Project People 直接推导。
5. 尚未配置异常项目优先展示、No Demand 汇总、报告周期/快照。当前只是实时状态报告草稿。
6. 验证详情实际用户模式只读、品牌/状态筛选对所有汇总和明细一致，再决定发布。不要为发布 Portfolio 草稿顺带开放未验收报告。

## 后续实施顺序

1. 补市场清单自动化：按 Program record ID + Market 查重，只补缺；新增 Program 自动建五行；测试重复执行。再做隔离日期变更/清空及第二 Program 页面切换。
2. 完成 Status Reports 的上述发布检查；用明确品牌与部门归属实现筛选，不虚构新事实。普通用户无需复制维护报告内容。
3. Department management：先看 localhost4177 参考，复用 People/Projects/Tasks；把部门负责的项目与部门参与项目的口径区分清楚，再连接报告。
4. Support & Knowledge：知识候选 System Knowledge & Progress (tblYpSrdHi84mJ8rO)，产品反馈候选 Issue Summary (tblE10VAfX0JZKAye)。不要与业务 Issues 混用，不把内部开发记录无差别展示给普通用户。

## 不改动的业务规则

- 保留当前任务完成与项目进度规则，用户已要求暂不修复。
- Task 是项目计划工作；Issue 是意外障碍，两者分别直接关联 Project。
- 一个 Issue 默认一个措施，措施不自动成为正式 Task。
- 页面全英文、尽量少选择；不新增未经定义的 Market Owner。
- 此次未发送邮件、未修改原始业务日期、未开启部门或知识模块。

## 浏览器续接

站内浏览器 id 1，Airtable tab 10，localhost tab 8。原生发现偶有失败但 agent.browsers API 可控制。部分 UI 调用耗时21—33秒，应每次最多1—2个动作、60秒超时；超时后先读回，避免重复修改。

当前为 Status Reports 创作者预览，Brand=Shark；页面有未发布修改。不要把创作者预览当已发布用户入口。

## 续作检查点：2026-09-14（覆盖上述旧页面状态）

本轮新增内容均保留草稿，未发布。市场清单此前发布状态不变。

### Department Workspace
- 复用 Department intelligent 的 pagwksnqWdjoEqMYc，命名 Department Workspace。
- People & Assigned Tasks 只读表：姓名、部门、任务、Primary Function、Issues；按部门分组。
- Choose a Department 筛选已连接表格。实测 NPI 163 人，清空筛选恢复 1696 人；89 人部门为空。
- People Detail 标题改姓名、关闭编辑、增加任务和问题关联。关联任务详情跳转仍需验收；原 Project member summary 不能直接作为可靠的部门项目归属。
- 尚缺部门项目汇总和周报联动，不算完整部门管理交付。

### Support & Knowledge
- 原 Knowledge Center 重命名；旧无效 Project Info 页面已隐藏，最新预览确认导航不再出现。
- 新建 Knowledge Library：pagMMevxrxMQCO5yI，源表 System Knowledge & Progress。
- 新增 Employee Visible checkbox flddJhA3xUXewj3GZ；页面只显示勾选项，内部开发记录保持不勾选。
- 新增三篇真实英文指南 HELP-001/002/003，分别介绍市场日期、Task 与 Issue 区别、反馈 AutoPM 问题。
- 记录 ID：recvDllWPp5YwLmLo、recDcYDpWTFeSuflt、recbO82CfQczrH4c4。标记 AI-inferred，不声称已正式批准。
- 知识页只读，Knowledge Article 详情标题为 Title。预览确认只有三篇指南；文章完整阅读链路尚未验收。
- Support 产品反馈表单尚未创建，拟复用 Issue Summary，不能与业务 Issues 混用。

### Status Reports
- 简化描述；Project Status Overview 标题；项目更新改 Tall 行高、换行标题、按 Project Status 分组并默认收起。
- Shark 预览汇总 1348、On Track 215、At Risk 5、Delayed 6 已观察。
- 独立 Issues 区域仍出现 450 条且未随品牌筛选；尝试删除没有持久生效，因此保持草稿，禁止误称已修复。
- 尚缺部门筛选和周报时间定义等验收。

### 下次优先项
1. 知识文章阅读验收、支持反馈入口；单独发布合格界面，勿连带发布报告草稿。
2. 部门人员至任务详情的跳转验收，再补项目与报告联动。
3. 用原生 UI 正确移除或过滤报告独立 Issues 区域。
4. 新 Program 自动生成五个市场的自动化仍未完成。

### 中断
最后打开知识文章时 UI 调用 60 秒超时并重置；随后 cua.getState 返回浏览器发现连接失败。此时未继续点击发布。临时 viewport override 未能恢复，因浏览器连接失败；恢复后应 reset，并保留工作标签页。
未发送邮件，未改变源日期、任务完成公式或生产业务状态。

## 继续任务：跳过阻塞项（2026-09-14）
- 浏览器发现再次失败，按用户要求不再反复排查。
- Airtable MCP 数据读可用。页面列表仅返回已发布的 Project Portfolio / AutoPM Workspace，未返回 Support 草稿 ID，未建立重复界面。
- 已核对 Market 实际为文本、Program 为多记录关联。
- 已完成 ensure-program-markets.js、test-ensure-program-markets.cjs、AUTOMATION-SETUP.md，均在 outputs/program-markets。
- 九类离线模拟测试通过，含部分写入恢复。未部署/启用自动化；不称为线上完成。
- Support 表单和报告页面操作等待浏览器恢复，原草稿保持。
