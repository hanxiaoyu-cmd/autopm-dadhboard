# 29项功能需求：目标—现状—差距—任务

版本：v1.1。现状与证据栏保留第二轮审计原文及时点；Bridge/Closure的本轮补充以蓝图和来源登记为准。审计里的“未读”不等于本轮仍完全未读，也不等于功能不存在。原Done不能替代本轮验收。


## REQ-001 — 业务对象模型

**目标：** 业务对象模型；建立Program→Project→SKU→Task→Issue→Action关系

**设计依据／历史批注：** Matrix Function Matrix D6/E6/F6；批注：1.尝试把data部分的数据打通，建立清晰的者三个部分的关系

**审计现状：** 部分实现；Program／PMO SKU同步，19–22、Projects／Tasks／Issues、两详情

**证据：** R2：E-A12–19、同步源及两详情取证；R1：跨项目SKU样本

**差距类型：** 数据问题／配置错误。历史依赖：确认上游权威、Closure Action

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-00](../tasks/AT-00.md), [AT-03](../tasks/AT-03.md), [MS-02](../tasks/MS-02.md), [MS-06](../tasks/MS-06.md), [GOV-01](../tasks/GOV-01.md)。

**原始验收目标：** 核心对象均有唯一ID；父子关系可追踪；抽查无孤立核心记录

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-002 — 主数据与身份

**目标：** 主数据与身份；锁定Project ID、SKU、People、Factory主键及匹配规则

**设计依据／历史批注：** Matrix Function Matrix D7/E7/F7；批注：需要检查现有的数据完整性，；比如工厂和工厂ID；人员信息的完整性和准确性；SKU与project ，program的关系

**审计现状：** 部分实现；DEV_SKU／Program_Code／People.Email／Factory链接；04／05编号

**证据：** R2：schema字段ID／类型无差异；R1：F10编码匹配样本及A04/A05

**差距类型：** 数据问题／规则待定。历史依赖：主数据Owner／别名／编码规范

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-03](../tasks/AT-03.md), [MS-02](../tasks/MS-02.md), [MS-10](../tasks/MS-10.md), [GOV-01](../tasks/GOV-01.md)。

**原始验收目标：** 导入重复项可识别；关键记录都能匹配到唯一主键

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-003 — 数据输入与系统连接

**目标：** 数据输入与系统连接；建立输入/输出矩阵；支持Excel/MPP导入和原系统链接

**设计依据／历史批注：** Matrix Function Matrix D8/E8/F8；批注：需要系统整理出来数据的输入和输出的关系表

**审计现状：** 部分实现；计划附件→16已追一批；Bridge输入输出两链未读；专业系统链接

**证据：** R2：E-A10、C1历史日志与9条当前Task；C2/C3无法检查

**差距类型：** 仅待验证／配置错误。历史依赖：C-01至C-04资料、接口Owner

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-06](../tasks/AT-06.md), [AT-07](../tasks/AT-07.md), [MS-01](../tasks/MS-01.md), [MS-08](../tasks/MS-08.md), [MS-13](../tasks/MS-13.md)。

**原始验收目标：** 每类数据标明Read/Write/Link/Import/TBD及系统Owner；导入可重复执行

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-004 — 数据质量与治理

**目标：** 数据质量与治理；定义核心必填字段、Source、Owner、Last Updated和质量例外

**设计依据／历史批注：** Matrix Function Matrix D9/E9/F9；批注：ok

**审计现状：** 部分实现；Audit Note／Last Modified；Relationship Check仅非空；样本孤立Issue

**证据：** R2：Relationship Check公式；R1：F11/F12具体异常记录

**差距类型：** 数据问题／规则待定。历史依赖：必填／及时性门槛需确认

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-00](../tasks/AT-00.md), [AT-03](../tasks/AT-03.md), [AT-06](../tasks/AT-06.md), [MS-01](../tasks/MS-01.md), [MS-02](../tasks/MS-02.md), [MS-03](../tasks/MS-03.md), [MS-08](../tasks/MS-08.md), [GOV-01](../tasks/GOV-01.md), [GOV-04](../tasks/GOV-04.md)。

**原始验收目标：** 建议门槛：核心字段完整度≥95%；所有例外可定位到记录和Owner

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-005 — Project Hub

**目标：** Project Hub；单页展示项目、SKU、阶段、日期、Owner、Task、Issue和Action

**设计依据／历史批注：** Matrix Function Matrix D10/E10/F10；批注：ok

**审计现状：** 部分实现；两套Project Detail；列表入口缺执行SKU，Program入口缺完整问题操作

**证据：** R2：两详情当前绑定、R2-12；R1：F05/F17

**差距类型：** 体验问题。历史依赖：页面保留策略；用户任务验收

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-08](../tasks/AT-08.md), [MS-04](../tasks/MS-04.md)。

**原始验收目标：** 真实用户无需解释可在30秒内回答状态、原因、Owner和下一步

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-006 — 项目健康与状态

**目标：** 项目健康与状态；用日期、逾期Task、开放Issue和下一Action支撑健康判断

**设计依据／历史批注：** Matrix Function Matrix D11/E11/F11；批注：还需要详细定义At risk 的标准，最好能创建成自动化

**审计现状：** 部分实现；Project Status手工；Task日期／Open Issue／MP差分开

**证据：** R2：Project状态／日期字段、三项目样本；R1：健康判断规则缺口

**差距类型：** 规则待定。历史依赖：F11明确At Risk标准待定义

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-01](../tasks/AT-01.md), [AT-08](../tasks/AT-08.md), [MS-04](../tasks/MS-04.md), [GOV-01](../tasks/GOV-01.md)。

**原始验收目标：** 每个At Risk/Delayed状态均可下钻到事实与Owner

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-007 — Portfolio视图

**目标：** Portfolio视图；展示试点项目状态、关键日期、Issue和Owner分布

**设计依据／历史批注：** Matrix Function Matrix D12/E12/F12；批注：还需要结合SKU, Project 以及program 这个方式显示项目状态

**审计现状：** 部分实现；Program画廊、Weekly Summary、多个保留报告页

**证据：** R2：E-F14–16/18、E-C09–25、R2-06/07/09

**差距类型：** 配置错误／规则待定。历史依赖：统计集合／主数据范围

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-03](../tasks/AT-03.md), [AT-08](../tasks/AT-08.md), [MS-04](../tasks/MS-04.md)。

**原始验收目标：** 试点范围内项目总数与明细一致；筛选后可下钻到记录

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-008 — Task & Action

**目标：** Task & Action；建立Task/Action、Owner、Due、Status、Priority、Dependency、Evidence

**设计依据／历史批注：** Matrix Function Matrix D13/E13/F13；批注：从周报导入的任务和状态还需要检查和确认

**审计现状：** 部分实现；Tasks Owner／Due／Status／Dependency／Deliverables；完成仅人数

**证据：** R2：E-F01/02、E-A11、三项目Task汇总；R1：交付证据字段

**差距类型：** 配置错误／规则待定。历史依赖：代理完成和关键任务证据标准

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-01](../tasks/AT-01.md), [AT-02](../tasks/AT-02.md), [AT-05](../tasks/AT-05.md), [MS-03](../tasks/MS-03.md), [MS-05](../tasks/MS-05.md), [MS-07](../tasks/MS-07.md)。

**原始验收目标：** 关键工作100%具备Owner和Due；完成项有状态和证据

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-009 — Milestone与模板

**目标：** Milestone与模板；锁定XPT/NPI基础Milestone和关键交付物

**设计依据／历史批注：** Matrix Function Matrix D14/E14/F14；批注：需要再次检查导入的项目数据是否正确，需要再次检查自动创建的任务计划是否合理

**审计现状：** 部分实现；01实际CPM模板、Tasks Milestone；另有Task Template

**证据：** R2：E-A01、Master/Effective公式、日期依赖；R1：CPM与Task Template样本

**差距类型：** 规则待定／配置错误。历史依赖：业务专家批准模板；不直接合并两表

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-04](../tasks/AT-04.md), [AT-12](../tasks/AT-12.md), [MS-05](../tasks/MS-05.md), [MS-06](../tasks/MS-06.md), [MS-11](../tasks/MS-11.md), [GOV-01](../tasks/GOV-01.md)。

**原始验收目标：** 每个试点项目有批准的里程碑、计划日期和Owner

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-010 — 提醒、催办与升级

**目标：** 提醒、催办与升级；上线个人待办、逾期提醒和每周检查

**设计依据／历史批注：** Matrix Function Matrix D15/E15/F15；批注：缺少自动提醒

**审计现状：** 部分实现；My daily work；09→Controls→09b；历史部分失败

**证据：** R2：E-C01–08、E-A06；R1：A13(09b)运行与发送动作

**差距类型：** 配置错误／仅待验证。历史依赖：提醒频率／停止／升级阈值；收件测试授权

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-02](../tasks/AT-02.md), [AT-09](../tasks/AT-09.md), [MS-07](../tasks/MS-07.md), [MS-09](../tasks/MS-09.md)。

**原始验收目标：** 提醒指向正确Owner和记录；发送结果有日志；可关闭重复提醒

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-011 — 完成证据与审计

**目标：** 完成证据与审计；为关键Task定义Completion Evidence

**设计依据／历史批注：** Matrix Function Matrix D16/E16/F16；批注：这个是当前的难点，无法创建合适的审批方式来确保交付物的准确性

**审计现状：** 部分实现；Tasks.Deliverables URL存在；完成公式不看证据

**证据：** R2：Task完成公式；R1：Deliverables URL字段；保存核验未验证

**差距类型：** 缺功能／规则待定。历史依赖：F16审批方式未定；链接可达性

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-01](../tasks/AT-01.md), [AT-05](../tasks/AT-05.md), [AT-06](../tasks/AT-06.md), [MS-01](../tasks/MS-01.md), [MS-03](../tasks/MS-03.md), [MS-07](../tasks/MS-07.md)。

**原始验收目标：** 关键交付物可通过附件、链接或结果字段验证

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-012 — Issue识别与影响

**目标：** Issue识别与影响；记录Issue、Category、Severity、MP/Launch Impact、Owner和Target

**设计依据／历史批注：** Matrix Function Matrix D17/E17/F17；批注：目前导入的这些issue 无法和autoPM里定义的完全匹配，需要和主管部门确认最终的标准格式

**审计现状：** 部分实现；Issues Severity／Impact MP／Owner／Target与Project／SKU关联

**证据：** R2：Issues字段配置无差异；R1：18条Closed样本中4条缺Project

**差距类型：** 数据问题／规则待定。历史依赖：F17需主管部门确认标准格式；Bridge未读

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-05](../tasks/AT-05.md), [MS-07](../tasks/MS-07.md)。

**原始验收目标：** 每个关键Issue均关联项目并说明影响、Owner和目标日期

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-013 — Root Cause与Recovery

**目标：** Root Cause与Recovery；连接Root Cause、Recovery Action、Owner和Target Date

**设计依据／历史批注：** Matrix Function Matrix D18/E18/F18；批注：还需要深度思考如何构把issue 构建成一个闭环的知识库

**审计现状：** 部分实现；Issues Root Cause／Recovery Action／Owners／Target；摘要分列去重

**证据：** R2：E-F09–13、旧详情Issue列表；R1：Issue Recovery字段

**差距类型：** 体验问题／缺功能。历史依赖：行动粒度、责任人、Jira权威

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-05](../tasks/AT-05.md), [MS-07](../tasks/MS-07.md)。

**原始验收目标：** 关闭前必须有原因、行动和责任人；Action Done不等于Issue Closed

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-014 — Decision管理

**目标：** Decision管理；记录Decision Needed、Decision Owner、Due和Decision Result

**设计依据／历史批注：** Matrix Function Matrix D19/E19/F19；批注：TBD 无限制的增加功能会导致系统复杂，需要思考更好的方案

**审计现状：** 未发现实现；Airtable未发现已核对的Decision闭环；历史知识／反馈不是决策执行

**证据：** R2：当前字段／页面目录；Decision正式闭环未发现；外部范围未读

**差距类型：** 规则待定。历史依赖：Matrix F19认为无限加功能会复杂化

**本轮优先级：** P1；发现已有日常依赖能力时按对等迁移变更纳入P0

**落地包：** [AT-13](../tasks/AT-13.md), [MS-12](../tasks/MS-12.md)。

**原始验收目标：** 每个待决事项有唯一责任人和日期；决定后自动生成Action

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-015 — 验证关闭

**目标：** 验证关闭；增加Result、Verification、Verified By、Closed Date和Reopen

**设计依据／历史批注：** Matrix Function Matrix D20/E20/F20；批注：Done

**审计现状：** 部分实现；Issue Closed／Closed Date存在；Result／Verification等未发现；Jira要求登录

**证据：** R2：Issues Overview文案与字段不符、Jira登录阻塞；R1：Closed样本

**差距类型：** 缺功能／仅待验证。历史依赖：Matrix F20写Done但无对应证据；关闭角色待定

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-05](../tasks/AT-05.md), [MS-03](../tasks/MS-03.md), [MS-07](../tasks/MS-07.md)。

**原始验收目标：** 至少一个真实Issue完成从发现到验证关闭的全链路证据

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-016 — Lesson Learned

**目标：** Lesson Learned；Issue关闭时记录Lesson、适用条件和证据

**设计依据／历史批注：** Matrix Function Matrix D21/E21/F21；批注：还需要深度思考如何构把issue 构建成一个闭环的知识库

**审计现状：** 部分实现；System Knowledge & Progress／历史Issue；未见由验证关闭生成可复用Lesson链

**证据：** R1：System Knowledge与Issue历史；R2：未发现关闭→Lesson自动链

**差距类型：** 缺功能／规则待定。历史依赖：F21知识库设计待定；依赖验证关闭

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-10](../tasks/AT-10.md), [MS-09](../tasks/MS-09.md)。

**原始验收目标：** 已验证关闭的关键Issue均有Lesson或明确Not Reusable原因

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-017 — 案例检索与复用

**目标：** 案例检索与复用；支持按Category、Project Type和关键词检索Issue

**设计依据／历史批注：** Matrix Function Matrix D22/E22/F22；批注：issue 库还需要不断改善

**审计现状：** 部分实现；Issues搜索筛选、知识记录存在；采用反馈未核对

**证据：** R2：Issues Overview入口；R1：Knowledge记录；采用结果未核对

**差距类型：** 体验问题／仅待验证。历史依赖：已验证知识范围

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-10](../tasks/AT-10.md), [AT-14](../tasks/AT-14.md), [MS-09](../tasks/MS-09.md), [MS-12](../tasks/MS-12.md)。

**原始验收目标：** 用户可在限定步骤内找到并打开历史记录和证据

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-018 — 模板资产

**目标：** 模板资产；建立基础Task Template并标注版本

**设计依据／历史批注：** Matrix Function Matrix D23/E23/F23；批注：已经创建，还需要仔细检查并确保其正确

**审计现状：** 仅有配置待验证；Task Template111／CPM56；01仅使用CPM

**证据：** R2：E-A01；R1：CPM56／Task Template111及模板字段

**差距类型：** 规则待定／仅待验证。历史依赖：F23“已创建、需仔细检查”；模板Owner

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-04](../tasks/AT-04.md), [AT-12](../tasks/AT-12.md), [MS-05](../tasks/MS-05.md), [MS-11](../tasks/MS-11.md), [GOV-01](../tasks/GOV-01.md)。

**原始验收目标：** 模板任务有Owner Function、Duration、Dependency和适用范围

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-019 — Weekly Summary

**目标：** Weekly Summary；自动汇总状态变化、Top Issue、Overdue、Decision和Next Action

**设计依据／历史批注：** Matrix Function Matrix D24/E24/F24；批注：进一步完善生成周报的格式和内容，确保内容准确，格式合理

**审计现状：** 部分实现；Weekly Summary页面、08／8b邮件，Bridge输出未读

**证据：** R2：E-C09–12、Weekly Summary筛选、E-A04/05、旧链接；C3无法检查

**差距类型：** 配置错误／仅待验证。历史依赖：收件人／窗口／关键问题规则；外部映射

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-09](../tasks/AT-09.md), [MS-01](../tasks/MS-01.md), [MS-09](../tasks/MS-09.md)。

**原始验收目标：** 试点项目周报从系统数据生成；不再二次录入核心状态

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-020 — Management Review

**目标：** Management Review；建立变化、例外、待决事项和行动四区Review

**设计依据／历史批注：** Matrix Function Matrix D25/E25/F25；批注：TBC 暂时不纳入到考虑范围内

**审计现状：** 部分实现；保留Review页面及反馈记录；会后Decision／Action回写未核对

**证据：** R2：E-C13–15、Review Field deleted；R1：反馈记录；会后回写未验证

**差距类型：** 规则待定。历史依赖：Matrix F25“暂时不纳入考虑”

**本轮优先级：** P1；发现已有日常依赖能力时按对等迁移变更纳入P0

**落地包：** [AT-13](../tasks/AT-13.md), [MS-12](../tasks/MS-12.md)。

**原始验收目标：** 会议输出的Decision和Action在会后进入系统并有Owner/Due

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-021 — 通知与行动回写

**目标：** 通知与行动回写；状态邮件包含记录链接、Owner和Next Action

**设计依据／历史批注：** Matrix Function Matrix D26/E26/F26；批注：TBC 暂时不纳入到考虑范围内

**审计现状：** 部分实现；8b／09b发送动作有历史；8b旧链接失效；送达未验

**证据：** R2：E-A05/06、8b失效入口；R1：09b发送历史；实际送达未验证

**差距类型：** 配置错误／仅待验证。历史依赖：Matrix F26暂缓扩展；邮件测试另授权

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-09](../tasks/AT-09.md), [MS-09](../tasks/MS-09.md)。

**原始验收目标：** 发送有成功/失败日志；行动可直接回到对应记录

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-022 — AI Summary

**目标：** AI Summary；仅对可信字段生成项目/Issue摘要并人工确认

**设计依据／历史批注：** Matrix Function Matrix D27/E27/F27；批注：太模糊，看不董

**审计现状：** 无法检查；未找到当前已核对的带来源AI Summary端到端证据；外部可能存在

**证据：** R2：未取得当前AI Summary端到端证据；Bridge无法检查

**差距类型：** 规则待定／仅待验证。历史依赖：Matrix F27批注“太模糊”；知识与数据Gate

**本轮优先级：** P1；发现已有日常依赖能力时按对等迁移变更纳入P0

**落地包：** [AT-14](../tasks/AT-14.md), [MS-12](../tasks/MS-12.md)。

**原始验收目标：** 摘要引用数据来源；事实错误可记录和纠正

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-023 — 风险与瓶颈分析

**目标：** 风险与瓶颈分析；用规则暴露逾期、空Owner、临近节点和开放高风险Issue

**设计依据／历史批注：** Matrix Function Matrix D28/E28/F28；批注：需要思考如何用自动化的方式来构建自动提醒

**审计现状：** 部分实现；Task缺失／逾期公式、MP差、开放High/Critical Issue

**证据：** R2：Task公式、E-F07/08、E-C01–08；风险阈值待决

**差距类型：** 规则待定／配置错误。历史依赖：阈值与风险定义

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-01](../tasks/AT-01.md), [AT-14](../tasks/AT-14.md), [MS-04](../tasks/MS-04.md), [MS-12](../tasks/MS-12.md)。

**原始验收目标：** 规则、阈值和命中记录透明；误报可记录

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-024 — 建议与Copilot

**目标：** 建议与Copilot；不进入核心范围，仅保留需求和数据准备

**设计依据／历史批注：** Matrix Function Matrix D29/E29/F29；批注：无

**审计现状：** 未发现实现；本轮未核对到Copilot执行链；目标本身非Phase1核心

**证据：** R2：未发现已核对Copilot链；非全系统不存在的证明

**差距类型：** 规则待定。历史依赖：Matrix Phase3及Gate

**本轮优先级：** Future：仅保留需求，不实施自主行为

**落地包：** [GOV-04](../tasks/GOV-04.md)。

**原始验收目标：** 未通过数据与知识Gate前不发布业务建议

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-025 — AI Agent

**目标：** AI Agent；明确不开发自主执行

**设计依据／历史批注：** Matrix Function Matrix D30/E30/F30；批注：需要研究下airtable的AI能力和边界

**审计现状：** 未发现实现；未核对到自主Agent工作流；PRD保留人工Decision责任

**证据：** R2：未发现已核对自主Agent链；外部未读

**差距类型：** 规则待定。历史依赖：Matrix F30研究需求不覆盖Phase1禁区

**本轮优先级：** Future：仅保留需求，不实施自主行为

**落地包：** [GOV-04](../tasks/GOV-04.md)。

**原始验收目标：** 仅记录候选场景、风险和授权需求

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-026 — 权限、安全与审计

**目标：** 权限、安全与审计；定义试点角色、查看/编辑范围和关键变更日志

**设计依据／历史批注：** Matrix Function Matrix D31/E31/F31；批注：需要和数据层，功能层，界面层等结合起来，一起定义一份权限指南，参考PLM

**审计现状：** 无法检查；当前Sun Sun账号可读配置／编辑入口；未做多角色行为验证

**证据：** R2：Sun Sun可访问配置与编辑入口；多角色行为未验证

**差距类型：** 仅待验证／平台限制待核实。历史依赖：多角色账号／租户策略／测试授权

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-00](../tasks/AT-00.md), [AT-02](../tasks/AT-02.md), [AT-11](../tasks/AT-11.md), [MS-00](../tasks/MS-00.md), [MS-02](../tasks/MS-02.md), [MS-03](../tasks/MS-03.md), [MS-10](../tasks/MS-10.md), [GOV-02](../tasks/GOV-02.md), [GOV-04](../tasks/GOV-04.md)。

**原始验收目标：** 权限测试通过；敏感字段不向无权限用户开放

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-027 — 平台运营

**目标：** 平台运营；建立问题清单、优先级、响应规则和备份

**设计依据／历史批注：** Matrix Function Matrix D32/E32/F32；批注：系统知识库的功能还非常不完善，可以说还没起步，需要下一步思考如何构建，

**审计现状：** 部分实现；Issue Summary、知识记录、运行历史；Windows交接资料已知不可访问

**证据：** R1：Knowledge／运行历史；R2：同步维护配置；Windows交接无法检查

**差距类型：** 仅待验证。历史依赖：Bridge交接／Closure RACI

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-00](../tasks/AT-00.md), [AT-07](../tasks/AT-07.md), [AT-10](../tasks/AT-10.md), [AT-11](../tasks/AT-11.md), [MS-00](../tasks/MS-00.md), [MS-08](../tasks/MS-08.md), [MS-10](../tasks/MS-10.md), [GOV-02](../tasks/GOV-02.md), [GOV-04](../tasks/GOV-04.md)。

**原始验收目标：** 关键故障有Owner和恢复步骤；系统知识不只存在于个人电脑

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-028 — 采纳与用户支持

**目标：** 采纳与用户支持；确定Committed Pilot Team、使用节奏、反馈和退出条件

**设计依据／历史批注：** Matrix Function Matrix D33/E33/F33；批注：Done

**审计现状：** 无法检查；有反馈126条和真实项目；持续使用／效率对照证据未取得

**证据：** R2：Comment现有记录；持续采用／效率历史未核对

**差距类型：** 仅待验证。历史依赖：Matrix F33写Done；Pilot Charter／基线缺口

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-02](../tasks/AT-02.md), [AT-07](../tasks/AT-07.md), [AT-08](../tasks/AT-08.md), [AT-10](../tasks/AT-10.md), [AT-11](../tasks/AT-11.md), [MS-08](../tasks/MS-08.md), [MS-10](../tasks/MS-10.md), [GOV-02](../tasks/GOV-02.md), [GOV-03](../tasks/GOV-03.md), [GOV-04](../tasks/GOV-04.md)。

**原始验收目标：** 真实团队持续使用；每周记录活跃、完整度、问题和价值证据

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。


## REQ-029 — 平台架构与边界

**目标：** 平台架构与边界；记录容量、权限、性能、集成和治理Gap

**设计依据／历史批注：** Matrix Function Matrix D34/E34/F34；批注：需要调查并明确airtable 的运行机理和特征，并且和autoPM的功能进行比较和匹配，生成报告

**审计现状：** 部分实现；本轮字段／脚本／UI／同步Fit-Gap；Power Apps租户未检查

**证据：** R2：本蓝图字段、脚本、页面与官方平台文档；Power Apps租户未检查

**差距类型：** 平台限制待核实。历史依赖：PO平台评审；Closure／Bridge边界

**本轮优先级：** P0基础；P1增强以任务卡为准

**落地包：** [AT-11](../tasks/AT-11.md), [MS-00](../tasks/MS-00.md), [MS-10](../tasks/MS-10.md), [MS-13](../tasks/MS-13.md), [GOV-01](../tasks/GOV-01.md), [GOV-02](../tasks/GOV-02.md), [GOV-03](../tasks/GOV-03.md), [GOV-04](../tasks/GOV-04.md)。

**原始验收目标：** 形成Airtable Fit/Gap清单及每个Gap的风险、Owner和决策日期

**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。

