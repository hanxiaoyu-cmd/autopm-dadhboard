# AutoPM 资源需求与落地路线图

> **版本**: v1.0 | **日期**: 2026-05-17 | **作者**: Sunny Sun
> **原则**: 不诉苦、不空谈，每个数字都有来源，每条路径都可执行

---

## 第一部分：我到底要什么资源（一页纸版）

### 🔴 必须有（没有做不了）

| # | 资源类型 | 具体要什么 | 为什么需要 | 没有会怎样 | 费用/周期 |
|---|---------|-----------|-----------|-----------|----------|
| 1 | 服务器 | Azure中国区 B2as v2（2 vCPU / 8GB RAM）+ Premium SSD P6（64GB） | 当前部署在Render免费层（国外），GitHub仓库已暴露过，数据安全无保障，免费层随时停服 | 数据泄露 + 服务中断 + 无法通过IT安全审计 | 按需￥298+81≈￥379/月（≈$52/月）；1年预留≈$70/月；审批2-4周 [¹](#数据来源) |
| 2 | 内网域名+SSO | `autopm.internal.sharkninja.com` + 接入公司Azure AD SSO | 不做SSO无法推广——没人愿意记新密码，IT不允许独立账号体系 | 死在"又一个新系统"的抵触上，5人试点后无法扩展 | $0（IT内部配置）；需Corey/IT部门配合，审批1-2周 |
| 3 | 1个兼职后端 | 现有IT/工程团队借1人，每周投入2天，持续12周 | 数据管道（E3/PLM→CSV→数据库）和API接口需要后端开发，Sunny不是开发 | 只能靠手动录入，系统永远是"手工填表的网页"，不是自动化平台 | 内部借调$0；外聘合同工按苏州标准≈15-25k RMB/月×3月≈$6k-10k [²](#数据来源) |
| 4 | Copilot许可证 | 10个M365 Copilot Enterprise附加许可证（$30/用户/月） | AI分析能力是AutoPM核心卖点，没有Copilot就无法做AI Insights、风险预警、智能摘要 | AutoPM降级为"项目看板"，失去AI驱动这个最大差异化 | $30/用户/月×10=$300/月=$3,600/年 [³](#数据来源) |

**🔴 必须有 小计：$300/月（SaaS）+ $52/月（服务器）≈ $352/月 ≈ $4,224/年**（不含人力）

### 🟡 最好有（有了快3倍）

| # | 资源类型 | 具体要什么 | 为什么需要 | 没有会怎样 | 费用/周期 |
|---|---------|-----------|-----------|-----------|----------|
| 5 | 1个全栈开发 | 每周3-4天，持续12周 | 前端（交互优化、移动端适配）+ 后端（API、数据库）同步推进 | Sunny手动管理所有技术细节，90天只能做到半自动，无法达到全自动 | 内部借调$0；外聘合同工≈20-30k RMB/月×3月≈$8k-12k [²](#数据来源) |
| 6 | Power Automate Premium | 5个Premium许可证（$15/用户/月） | 免费版只有标准连接器，无法接E3/PLM的HTTP API和自定义连接器 | 自动化流程只能做Teams/邮件级通知，无法做数据自动同步 | $15/用户/月×5=$75/月=$900/年 [⁴](#数据来源) |
| 7 | E3/PLM API权限 | 只读API访问权限 | 实现数据自动同步，取代手动导CSV | 每天靠人手动导出CSV上传，数据延迟1天，且容易遗忘 | $0（权限开放）；需E3管理员配合，审批2-4周 |
| 8 | 试点PM（兼职） | 其他部门1个NPI PM，每周投入1天 | Sunny自己管OF102是"自证"，需要其他项目的PM也用才能证明通用性 | 试点数据只来自1个项目1个部门，说服力不足 | $0（内部借调） |

**🟡 最好有 小计：$75/月（SaaS）+ 人力（内部借调$0 / 外聘$8k-12k）**

### 🟢 锦上添花

| # | 资源类型 | 具体要什么 | 为什么需要 | 没有会怎样 | 费用/周期 |
|---|---------|-----------|-----------|-----------|----------|
| 9 | Copilot Studio | 1个Copilot Studio许可证 | 构建AutoPM专属AI Agent，用户在Teams里直接@AutoPM提问 | 用户需打开浏览器访问AutoPM，不能在Teams里即问即答 | ~$200/月（25,000 messages）[³](#数据来源) |
| 10 | Azure Monitor | 基础监控+Log Analytics | 5人试点不需要，30+用户时需要监控性能和错误 | 出问题只能手动查日志，响应慢 | ~$50/月 |
| 11 | 正式Headcount | 1个AutoPM产品经理正式岗位 | Sunny当前是NPI PM身份做AutoPM，没有正式编制，优先级永远被项目挤占 | AutoPM永远是"兼职项目"，无法长期持续 | 苏州外企PM年薪≈200k-350k RMB（≈$28k-48k）[²](#数据来源) |

**🟢 锦上添花 小计：$250/月 + 1个HC ≈ $28k-48k/年**

---

### 💰 总计费用汇总

| 场景 | SaaS年费（不含HC） | 含1个正式HC |
|------|-------------------|------------|
| 最小可行（🔴必须有） | $4,224 | $32,224-52,224 |
| 推荐配置（🔴+🟡，内部借调） | $5,124 | $33,124-53,124 |
| 推荐配置（🔴+🟡，外聘合同工） | $13,124-17,124 | $41,124-65,124 |
| 完整配置（🔴+🟡+🟢，内部借调） | $8,124 | $36,124-56,124 |

> 💡 **对比参照**：SharkNinja 2026 Q1现金储备$511.8M，年营收增速15.6%。AutoPM最小可行年费$4,224 ≈ 1个苏州工程师3周工资。

---

### 数据来源

- ¹ Azure中国区（世纪互联）官方定价页 azure.cn/pricing，B2as v2按需￥298/月，P6 SSD￥81/月，汇率按7.2折算
- ² SharkNinja苏州（尚科宁家）猎聘招聘数据：工程师15-25k/月·13薪，高级工程师18-35k/月·13薪；苏州工业园区薪酬报告（2025）：本科工程师年薪中位数11.7万元
- ³ Microsoft官方定价：M365 Copilot Enterprise $30/用户/月（2026年5月验证）；Copilot Studio ~$200/月
- ⁴ Microsoft官方定价：Power Automate Premium $15/用户/月（2026年5月验证）

---

## 第二部分：资源获取的三个路径

### 路径A：正式申请（通过建→Ross→审批）

**适用资源**：服务器、SSO、Copilot许可证、正式HC

**流程**：
```
Sunny写资源申请单 → 建审批签字 → 建递交Ross → Ross/CDO办公室审批 → IT执行
                                                    ↓（如果Ross不批）
                                              CEO月度Review时呈报
```

**每个资源的具体操作**：

| 资源 | 申请方式 | 审批层级 | 预估周期 | 成功概率 |
|------|---------|---------|---------|---------|
| Azure VM（中国区） | IT资源申请表，说明用途和安全需求 | 建→IT经理→Ross | 2-4周 | 70%（费用极低，主要卡流程） |
| SSO/Azure AD接入 | 安全审查+IT配置 | 建→Corey/IT团队 | 1-2周 | 80%（CEO已背书，IT有义务配合） |
| 10个Copilot许可证 | M365管理员添加 | 建→IT管理员 | 1-2周 | 90%（只是加许可证，不是买新产品） |
| 1个正式HC | 需要编制审批，走HR | 建→Ross→HR→预算委员会 | 6-12周 | 30%（最难的资源，需要ROI数据支撑） |

**关键策略**：
- 🔑 先拿容易的（Copilot许可证、SSO），再拿难的（HC）
- 🔑 每拿到一个资源，立刻产出成果，用成果换下一个资源
- 🔑 给建准备好"1分钟汇报稿"——他只需要在Ross面前说"这个项目已经跑出数据了，需要X资源继续"

---

### 路径B：借力不借人（不占HC，用公司现有工具和兼职人力）

**适用资源**：开发人力、自动化工具、试点用户

**核心逻辑**：不申请编制，用现有工具链+借调时间把事做了

**具体操作**：

| 做法 | 怎么操作 | 拿到什么 | 花多少钱 |
|------|---------|---------|---------|
| 用SharePoint做数据库 | 创建`AutoPM_Data`站点，Excel Online存储项目数据 | 数据层（零审批，全员可用） | $0 |
| 用Power Automate做自动化 | M365免费版搭3个流：邮件→Excel、Excel→Teams通知、每日摘要 | 自动通知+自动录入 | $0（M365含基础Power Automate） |
| 用Teams做通知中心 | 创建"AutoPM"频道，Power Automate推送状态变更 | 推送层 | $0 |
| 用Copilot Chat做AI | Copilot Chat对M365用户免费，可读Teams消息和SharePoint文件 | 基础AI问答 | $0 |
| 借1个IT工程师2天/周 | 找Corey/IT团队直接说"CEO要求7高管配合AutoPM，我需要1人帮忙搭服务器和API" | DevOps+后端 | $0（借调） |
| 借1个NPI PM半天/周 | 找Tom/PD部门PM，说"我用AutoPM管OF102省了很多时间，帮你管你的项目试试" | 试点用户+口碑 | $0（借调） |

**⚠️ 注意：Power Automate免费版的限制**
- M365包含的Power Automate只能用**标准连接器**（Teams、SharePoint、Excel Online、Outlook等）
- 接E3/PLM的HTTP API需要**Premium连接器**，即需Premium许可证（$15/用户/月）
- 5人试点阶段：标准连接器够用（Excel Online→Teams通知→邮件提醒）
- 30人扩展阶段：必须升级Premium才能接E3/PLM

**关键策略**：
- 🔑 **谁痛谁帮忙**：不找"开发者"，找"受益者"——OF102的NPI最痛，最可能投入时间
- 🔑 **做出来再审批**：先用免费工具跑起来，再拿数据去走正式流程
- 🔑 **Power Automate免费版够5人试点**：5人以下不需要Premium，先跑再说

---

### 路径C：外部合作（华师大CTO学院、开源社区）

**适用资源**：技术指导、架构咨询、开源工具

**具体操作**：

| 合作方 | 怎么对接 | 能拿到什么 | 限制 |
|--------|---------|-----------|------|
| 华东师大CTO学院（5位导师） | Sunny是该校MEM研究生，王振源教授是导师 | 架构评审、技术方案咨询、学术论文背书、产学研合作项目 | 不能做具体开发；导师时间有限 |
| 开源社区 | AutoPM非核心代码开源，吸引贡献者 | 代码贡献、Bug修复、功能建议 | 公司安全审查；可能不允许代码外泄 |
| Microsoft Tech Community | 参加Power Automate/Copilot社区 | 模板、脚本、排错经验 | 无直接人力支持 |
| 苏州本地高校 | 通过CTO学院联系苏大/西交利物浦大学计算机系 | 实习生（3-6个月），成本低 | 需HR审批实习岗位；产出不稳定 |

**关键策略**：
- 🔑 **华师大是最大的外部杠杆**：5位导师的专业建议值$5,000+/次咨询，对Sunny免费
- 🔑 **把AutoPM做成MEM毕业论文课题**：学术+实践双赢，论文本身就是"第三方背书"
- 🔑 **实习生方案要慎重**：审批流程长、产出不确定，作为补充不是主力

---

### 🎯 三路径优先级排序

```
第1周-第4周：路径B为主（用免费工具先跑起来）
第5周-第8周：路径A为主（拿试点数据去申请正式资源）
第9周-第12周：路径C为辅（学术背书+论文框架）
```

---

## 第三部分：90天落地路线图

### Phase 1：证明有人用（Day 1-30）

**目标**：5-10个真实用户在AutoPM上管理至少2个项目，产出可量化的使用数据

| 事项 | 时间 | 需要的资源 | 路径 | 不依赖资源也能做？ | 交付物 | 验收标准 |
|------|------|-----------|------|-------------------|--------|---------|
| 手动MVP上线 | Day 1-3 | Sunny 1人 | B | ✅ 可以 | OF102真实数据填入AutoPM v14.5 | 5人打开链接可看项目状态 |
| 3个Power Automate流程 | Day 4-10 | Power Automate免费版 | B | ✅ 可以 | 邮件→Excel→Teams通知自动流转 | 状态更新从邮件到Teams < 30秒 |
| Excel Online数据源 | Day 4-7 | SharePoint | B | ✅ 可以 | OF102_Project_Tracker.xlsx | 多人可同时编辑 |
| Copilot Chat接入 | Day 8-14 | Copilot Chat（免费） | B | ✅ 可以 | Teams里@Copilot能回答OF102项目问题 | 3个问题正确回答 |
| 用户Onboarding | Day 7-14 | 3-5个试点用户 | B | ✅ 可以 | 用户追踪表+NPS评分 | NPS ≥ 7/10 |
| 试点扩展到第2个项目 | Day 15-21 | 1个NPI PM（兼职半天/周） | B | ⚠️ 需人配合 | 第2个项目在AutoPM上运行 | 数据每日更新 |
| Week 1-2效果报告 | Day 14 | — | — | ✅ 可以 | 1页纸英文Brief | 3个量化指标有改善 |
| Week 3-4效果报告 | Day 28 | — | — | ✅ 可以 | 1页纸Brief + ≥3份用户endorsement | 书面好评已收集 |

**Phase 1 关键**：✅ 所有事项都不依赖路径A资源，路径B全部可做

---

### Phase 2：证明有价值（Day 31-60）

**目标**：用Phase 1数据争取正式资源，将AutoPM从"手动流水线"升级为"半自动系统"

| 事项 | 时间 | 需要的资源 | 路径 | 不依赖资源也能做？ | 交付物 | 验收标准 |
|------|------|-----------|------|-------------------|--------|---------|
| 向建正式汇报 | Day 31-35 | Week 1-4数据 | — | ✅ 可以 | 汇报PPT（3页） | 建同意向Ross引荐 |
| 争取Ross 15分钟 | Day 35-42 | 建的支持 | A | ⚠️ 需建配合 | 与Ross的会议 | Ross认可方向 |
| 服务器申请 | Day 35-49 | Azure VM中国区 | A | ❌ 必须走审批 | 服务器到位+环境搭建 | SSH可登录 |
| SSO接入 | Day 42-56 | IT部门配合 | A | ❌ 必须IT执行 | Azure AD SSO可用 | 公司账号直接登录 |
| CSV导入模块开发 | Day 42-56 | 1个兼职后端（2天/周） | A/B | ⚠️ 没后端只能手动 | csv_parser.py + csv_importer.py | 每日自动导入 |
| 数据库搭建 | Day 42-49 | PostgreSQL on 服务器 | A | ❌ 需服务器 | 5张核心表已创建 | `\dt` 看到5张表 |
| Copilot许可证申请 | Day 35-42 | 10个Copilot Enterprise | A | ❌ 需要付费 | AI Insights功能可用 | Copilot可分析项目数据 |
| 试点扩展到5个项目 | Day 42-60 | 更多PM加入 | B | ✅ 可以（口碑推荐） | 5个项目在AutoPM上运行 | 活跃用户 ≥ 8人 |
| 60天成果报告 | Day 58-60 | — | — | ✅ 可以 | 3页报告+预算对比表 | 呈报给建/Ross |

**Phase 2 关键**：前2周不依赖路径A（继续汇报+扩大试点），后2周路径A资源需要到位

---

### Phase 3：规模化准备（Day 61-90）

**目标**：系统达到30人可用的稳定状态，锁定正式资源承诺

| 事项 | 时间 | 需要的资源 | 路径 | 不依赖资源也能做？ | 交付物 | 验收标准 |
|------|------|-----------|------|-------------------|--------|---------|
| E3/PLM API调研 | Day 61-67 | IT+后端 | A | ⚠️ 需IT配合 | API可行性报告 | 明确API可用/不可用 |
| API直连开发（如可行） | Day 67-84 | 1个后端（全职或3天/周） | A | ❌ 需开发资源 | E3/PLM数据自动同步 | 每日自动同步 |
| Power Automate Premium | Day 61-67 | 5个Premium许可证 | A | ❌ 需要付费 | 高级连接器可用 | E3 HTTP请求自动触发 |
| 移动端适配 | Day 67-84 | 1个前端（2天/周） | A/B | ⚠️ 没前端可用响应式CSS | 手机可正常使用 | 5个用户手机验证通过 |
| 用户培训+文档 | Day 75-84 | — | — | ✅ 可以 | Quick Start Guide + FAQ | 新用户15分钟内上手 |
| 正式资源谈判 | Day 80-90 | 60天数据+ROI | A | ✅ 可以 | 书面承诺（邮件确认） | 至少1个HC+工具预算 |
| 90天总结呈报CEO办公室 | Day 88-90 | — | — | ✅ 可以 | 1页纸Memo | CEO办公室收到 |
| 华师大论文框架 | Day 70-90 | 导师时间 | C | ✅ 可以 | 论文大纲+导师签字 | 论文开题通过 |

**Phase 3 关键**：路径A资源必须在Phase 2到位，Phase 3才能做开发；否则降级为"如果只给我1个人"方案

---

### 📊 资源依赖关系图

```
                    Phase 1 (Day 1-30)
                    ┌─────────────┐
                    │  全部路径B   │ ← 不需要任何审批和预算
                    │  0美元/月    │
                    └──────┬──────┘
                           │ 拿到试点数据
                           ↓
                    Phase 2 (Day 31-60)
                    ┌─────────────┐
                    │ 路径A+B混合  │ ← 服务器+SSO+Copilot需审批
                    │ ~$352/月     │
                    └──────┬──────┘
                           │ 拿到正式资源承诺
                           ↓
                    Phase 3 (Day 61-90)
                    ┌─────────────┐
                    │ 路径A+B+C   │ ← 开发资源+API权限+学术背书
                    │ ~$427/月     │
                    └─────────────┘
```

---

## 第四部分：如果只给我1个人

**现实场景**：1个人（Sunny）+ 1个帮手（兼职半天/周），90天，零额外预算，只用公司现有工具链。

### 90天能做到什么

| 阶段 | 时间 | 目标 | 做法 | 交付物 |
|------|------|------|------|--------|
| 手动MVP | Day 1-14 | 5人看到OF102真实状态 | 手动把数据填进AutoPM HTML → 放SharePoint → 发链接 | 5人可看+反馈收集 |
| 半自动流水线 | Day 15-42 | 状态更新不再靠人追 | SharePoint Excel + Power Automate免费版 + Teams通知 + Copilot Chat | 3个自动化流程在跑 |
| 扩大试点 | Day 43-60 | 3个项目在AutoPM上管理 | 用OF102成功案例说服其他PM | 8个活跃用户 |
| 争取资源 | Day 61-90 | 拿到下一阶段正式资源 | 60天数据+用户endorsement → 建→Ross | 至少1个HC承诺 |

### 哪些功能保留，哪些放弃

| 功能 | 保留/放弃 | 理由 | 替代方案 |
|------|----------|------|---------|
| 项目可见性（看板+列表） | ✅ 保留 | 核心价值 | AutoPM HTML v14.5 |
| 甘特图 | ✅ 保留 | 已有 | 现有Gantt Chart模块 |
| 自动通知 | ✅ 保留 | Power Automate免费版能做 | Teams推送+邮件 |
| AI Insights | ⚠️ 简化版 | 没有Copilot许可证，只能用免费Copilot Chat | @Copilot in Teams（基础问答） |
| E3/PLM自动同步 | ❌ 放弃 | 没有后端开发，无法做API对接 | 每天手动导CSV，15分钟 |
| 移动端适配 | ❌ 放弃 | 没有前端开发 | 用Teams移动端查看通知 |
| 多项目甘特联动 | ❌ 放弃 | 数据量超出手动管理能力 | 单项目甘特图够用 |
| 风险自动预警 | ⚠️ 简化版 | 没有AI模型 | Power Automate定时检查逾期milestone+Teams告警 |
| 文件附件管理 | ❌ 放弃 | 需要后端+存储 | SharePoint文件夹替代 |
| SSO登录 | ❌ 放弃 | 需要IT配合 | 共享链接+密码保护 |

### 用现有工具链拼出的AutoPM Lite

```
┌─────────────────────────────────────────────────┐
│              AutoPM Lite 架构图                   │
│            （1人+1帮手，零额外预算）                │
├─────────────────────────────────────────────────┤
│                                                   │
│  📊 可视化层                                      │
│  ┌─────────────────────────────────────────┐     │
│  │  AutoPM HTML v14.5 (SharePoint托管)      │     │
│  │  - 项目看板  - 甘特图  - 风险标记          │     │
│  └──────────────────┬──────────────────────┘     │
│                     │ 数据源                       │
│  📋 数据层         ↓                              │
│  ┌─────────────────────────────────────────┐     │
│  │  Excel Online on SharePoint              │     │
│  │  - 项目表  - 里程碑表  - 风险表            │     │
│  └──────────────────┬──────────────────────┘     │
│                     │ 自动化                       │
│  ⚡ 自动化层       ↓                              │
│  ┌─────────────────────────────────────────┐     │
│  │  Power Automate (M365免费版)              │     │
│  │  - 邮件→Excel  - Excel→Teams  - 每日摘要  │     │
│  └──────────────────┬──────────────────────┘     │
│                     │ AI                          │
│  🤖 AI层           ↓                             │
│  ┌─────────────────────────────────────────┐     │
│  │  Copilot Chat (免费) in Teams            │     │
│  │  - 项目问答  - 风险分析  - 状态总结        │     │
│  └─────────────────────────────────────────┘     │
│                                                   │
│  💬 通知层：Teams频道 + Outlook邮件                │
│  📁 文件层：SharePoint文档库                       │
│                                                   │
└─────────────────────────────────────────────────┘
```

### AutoPM Lite vs AutoPM Full 对比

| 维度 | AutoPM Lite（1人+1帮手） | AutoPM Full（有资源） |
|------|-------------------------|---------------------|
| 用户规模 | 5-10人 | 30-100人 |
| 数据更新 | 手动导CSV + 半自动 | E3/PLM API自动同步 |
| AI能力 | Copilot Chat基础问答 | AI Insights + 预测 + 智能摘要 |
| 部署方式 | SharePoint + Render免费层 | Azure中国区服务器 + SSO |
| 安全等级 | 低（GitHub暴露风险） | 高（内网+AD+审计） |
| 移动端 | 仅Teams通知 | 完整移动端 |
| 90天可覆盖项目 | 3-5个 | 15-20个 |
| 持续运维 | Sunny手动 | 系统自动 |

> 💡 **结论**：AutoPM Lite能证明概念有效，但无法规模化。它的价值是**换资源的筹码**，不是终点。

---

## 第五部分：给领导的一页纸Brief

---

**AutoPM — Status, Results & Resource Ask**

**What it is:**
An AI-assisted project visibility system for XPT/ACE. Instead of PMs chasing status through email chains and meetings, AutoPM pushes real-time status to them — milestones, risks, and AI-generated insights, all in one place.

**What we've achieved (zero budget, zero new headcount):**
- Built a working prototype (v14.5) with Project Overview, Gantt Chart, AI Insights, and Feedback modules
- Deployed and accessible via internal link (SharePoint + secure tunnel)
- CEO Mark Barrocas endorsed via company-wide email; 7 executives committed to support
- Completed full WBS (814 lines) and 30-day pilot plan for Color projects
- Zero-resource bootstrap plan operational: SharePoint + Power Automate + Teams + Copilot Chat

**What we're doing now (Week 1-4):**
- Running OF102 Color project pilot with 5 real users
- Measuring: status lookup time, milestone alert response time, weekly meeting efficiency
- Target: prove "people stop chasing information"

**What we need to scale:**

| Priority | Resource | Cost | Why |
|----------|----------|------|-----|
| Must-have | Azure China VM (B2as v2, 2vCPU/8GB) + 64GB SSD | ~$52/month (azure.cn pricing) | Current free-tier Render deployment is not secure; GitHub repo was exposed |
| Must-have | SSO via Azure AD | $0 (IT config) | No adoption without SSO — nobody wants another password |
| Must-have | 10 M365 Copilot Enterprise licenses | $300/month (MSRP $30/user/month) | AI is the core differentiator; without it, AutoPM is just a dashboard |
| Must-have | 1 backend developer (2 days/week, 12 weeks) | $0 (internal loan) or ~$8K (contractor) | Data pipeline from E3/PLM requires backend work |
| Nice-to-have | 5 Power Automate Premium licenses | $75/month ($15/user/month MSRP) | Enables E3/PLM HTTP connectors for auto-sync |
| Nice-to-have | 1 full-stack developer (3-4 days/week) | $0 (internal) or ~$10K (contractor) | Parallel front-end + back-end development |

**Total ask: $352/month in SaaS + 1 loaned developer = as low as $4,224/year**

*All prices verified from official sources: azure.cn (May 2026), Microsoft 365 pricing page (May 2026), Suzhou engineering salary benchmarks (Liepin/Jobui 2026)*

**ROI projection:**

| Metric | Without AutoPM | With AutoPM | Savings |
|--------|---------------|-------------|---------|
| Status lookup per project | ~2 hours/week | <2 minutes/week | ~1.9 hours/week |
| Milestone delay detection | 3 days average | Same-day alert | 3 days faster |
| Weekly meeting on status alignment | 30 minutes | 5 minutes | 25 minutes/week |

- 10 PMs × 1.9 hours/week × 52 weeks × $28/hour (Suzhou PM avg) = **$27,344/year in reclaimed productivity**
- vs. $4,224/year in SaaS costs = **6.5:1 ROI**

**Timeline:**

| Period | Milestone | Dependency |
|--------|-----------|------------|
| Week 1-4 | 5-user pilot running, first data collected | None (already started) |
| Week 5-8 | Semi-automated pipeline, server + SSO deployed | Server + SSO approval |
| Week 9-12 | 30-user ready, E3/PLM integration tested | Backend developer + Copilot licenses |

**Ask:** Approve $4,224/year in SaaS licenses + 1 internally loaned developer for 12 weeks. I'll have 30 active users by end of Quarter.

---

**Sunny Sun** | NPI PM, SharkNinja Suzhou | AutoPM Project Lead
*Per CEO Mark Barrocas' directive, per CDO Ross Goldberg's commitment to support*

---

*文件结束*
