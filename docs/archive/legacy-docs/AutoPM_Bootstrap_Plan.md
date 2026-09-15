# AutoPM 零资源落地方案

> 版本: v1.0 | 日期: 2026-05-13 | 原则: 没有资源不是停下来的理由，是换一条路走的信号

---

## 一、现实诊断

1. **项目有根无干**：你有原型、有思路、有时间，但没有开发团队、没有预算、没有组织授权——就像一棵发了芽的种子，土还没翻。
2. **领导有心无力**：直属领导接了这个项目但不懂，想推但推不动；Jen说了"I love it"但没动作——热情不等于承诺，口头支持不等于资源。
3. **窗口在关**：你80%精力已释放、项目移交正在进行，这个时间窗口不会一直开着。如果2周内不能证明AutoPM能自己跑起来，它就会变成"那个挺好的想法"。

---

## 二、零资源MVP路径

### 核心思路

WBS v2假设有DevOps + Backend + Frontend + AI Dev + Pilot PM，那是一条需要团队的路。**换一条路：用公司已有的工具链，一个人就能跑。**

### 你现在手上的牌

| 资产 | 状态 | 用法 |
|------|------|------|
| AutoPM HTML v13.1 | 能演示 | 做可视化展示层，先不改动 |
| Office 365 / Excel Online | 全公司可用 | 做数据存储，替代数据库 |
| SharePoint | 全公司可用 | 做共享文件中心，替代服务器 |
| Power Automate | 全公司可用 | 做自动化流程，替代后端 |
| Exchange / Outlook | 全公司可用 | 做AI输入输出通道，替代API |
| Teams | 全公司可用 | 做通知推送，替代独立前端 |
| Copilot | 全公司可用 | 做AI引擎，替代自建模型 |
| 你自己的时间 | 85%已释放 | 做一切 |

### 架构：从"建系统"变成"拼乐高"

```
WBS v2 的路径（需要团队）：
  E3/PLM → API → 后端服务器 → PostgreSQL → 前端 → 用户浏览器

零资源的路径（一个人就能跑）：
  E3手动导出 → Excel Online → SharePoint → Power Automate → Teams/邮件通知 → 用户
                                                      ↓
                                               Copilot（AI分析）
```

**关键转变**：不是"建一个系统"，是"用现有工具搭一条流水线"。系统是虚的，流水线是实的。

---

## 三、"一个人能跑"的3步

### Step 1：手动MVP — 今天就能做，零技术

**做什么**：把OF102两个Color项目的真实数据填进AutoPM HTML v13.1，让5个人打开就能看。

**具体动作**：

1. **今天下午**：打开E3/PLM，把OF102（BL1/GY和RD/GN3）的6项核心数据抄下来——项目清单、里程碑日期、当前阶段、审批状态、负责人、风险标记
2. **今天下班前**：手动把数据填进AutoPM HTML v13.1，保存为新版本（v13.2-pilot）
3. **明天早上**：把HTML文件放到SharePoint共享文件夹，链接发给5个人（2个OF102 NPI + 1个工程师 + 你领导 + Jen的EA）
4. **明天下午**：逐个问这5个人——"你看得懂吗？缺什么？多的什么？"

**交付物**：5个人打开一个链接就能看到OF102真实项目状态

**注意**：
- 不要解释"这是AI驱动的项目管理平台"，就说"我把OF102的状态整理到一个页面了，你看看"
- 不要等数据完美，缺的字段标"[待确认]"，比没有强
- 不要美化，真实数据的丑陋是第一份证据

---

### Step 2：半自动 — 1周内，用Power Automate + Excel Online

**做什么**：让数据不再依赖你手动更新，用公司工具实现半自动流转。

**具体动作**：

#### 2.1 建Excel Online数据源（第1-2天）

1. 在SharePoint创建`AutoPM_Data`文件夹
2. 创建Excel文件`OF102_Project_Tracker.xlsx`，sheet结构：

| Project | Milestone | Due Date | Actual Date | Status | Owner | Risk Flag | Last Updated |
|---------|-----------|----------|-------------|--------|-------|-----------|--------------|
| OF102-BL1 | M7 Color Selection | 2026-05-30 | | In Progress | [NPI名] | | |
| OF102-BL1 | M8 Color Approval | 2026-06-15 | | Not Started | [NPI名] | | |

3. 这个Excel就是你的"数据库"——简单、人人会改、不需要权限申请

#### 2.2 搭Power Automate流程（第3-5天）

**流程1：邮件→Excel自动录入**
- 触发：收到邮件，主题含"[AutoPM]"
- 动作：解析邮件正文（项目名+状态更新），写入Excel对应行
- 效果：NPI发一封邮件就能更新项目状态，不需要打开任何系统

**流程2：Excel→Teams通知**
- 触发：Excel行被修改
- 动作：在Teams的"OF102 AutoPM"频道发一条消息
- 格式：`⚠️ [OF102-BL1] M7 Due 5/30 — Status: In Progress — Owner: [NPI]`
- 效果：所有人不用追信息，状态变更自动推送到Teams

**流程3：每日摘要**
- 触发：每天早上8:00
- 动作：读取Excel，汇总今天到期的milestone + 已逾期 + 风险项
- 发送到：Teams频道 + 你的邮件
- 效果：每天早上一杯咖啡的时间就能知道OF102有没有问题

#### 2.3 接入Copilot做AI分析（第5-7天）

1. 在Teams频道里，直接@Copilot提问：
   - "OF102这个月有哪些milestone可能延期？"
   - "OF102-BL1和RD/GN3之间有没有资源冲突？"
2. Copilot能读Teams消息和SharePoint文件——你的数据已经在那里了
3. 不需要自己建AI模型，Copilot就是你的AI

**交付物**：
- Excel数据源在SharePoint上，多人可编辑
- Power Automate 3个流程在跑
- Teams频道每天自动推送状态
- Copilot能回答项目问题

**注意**：
- Power Automate的免费额度足够5人试点，不需要审批
- 不要追求完美流程，能跑就行，边跑边改
- Excel数据会有冲突——没关系，5个人不会有并发问题

---

### Step 3：证明价值 — 2周内，数据说话

**做什么**：收集数据证明AutoPM在解决问题，拿数据去换资源。

**具体动作**：

#### 3.1 定义3个可量化指标（第1天就定义，持续跟踪）

| 指标 | 基线（手动时代） | 目标（AutoPM时代） | 怎么量 |
|------|------------------|-------------------|--------|
| 信息获取时间 | 追人追2小时才拿到状态 | 2分钟从Teams看到 | 问NPI："你现在查OF102状态要多久？" |
| 逾期发现延迟 | milestone逾期3天后才发现 | 逾期当天推送 | 记录每次逾期是何时被发现的 |
| 周会信息对齐 | 每周30分钟对齐状态 | 5分钟确认，25分钟讨论问题 | 计时周会 |

#### 3.2 第1周结束：写一份1页纸的效果报告

格式：

```
AutoPM Week 1 Results — OF102 Pilot

What changed:
- 5 people now see OF102 status without chasing anyone
- 2 milestone alerts sent, both acted on within 4 hours
- 1 risk flag (M7 approval pending > 5 days) identified and escalated

What didn't work:
- [记录所有失败和摩擦，诚实]

Next week:
- [具体下一步]
```

#### 3.3 第2周结束：拿着数据去找领导

不是去要资源，是去**报告成果**。资源请求藏在成果报告的"下一步"里。

**交付物**：
- 2周运行数据
- 5个用户的真实反馈（好的坏的都要）
- 1份成效报告（英文，1页纸）

---

## 四、向上管理策略

### 核心原则

**不要让领导做问答题，给他做选择题。**

错误示范："领导，AutoPM需要开发资源，你觉得怎么办？"
正确示范："领导，AutoPM试点已经跑了2周，5个人用了都说好。下一步有两条路，A路线需要X资源，B路线只需要Y资源。我建议选B，因为___。"

### 给领导的1页纸Brief

以下是英文原文，直接发给领导，他可以拿去向上汇报：

---

**AutoPM — Project Status & Next Steps**

**What it is:** An AI-assisted project visibility system for XPT/ACE. Instead of PMs chasing status through email and meetings, AutoPM pushes status to them automatically.

**What we've done (zero budget, zero new headcount):**
- Built a working pilot on OF102 (2 Color projects) using existing tools (SharePoint + Power Automate + Teams + Copilot)
- 5 team members now see project status without manual follow-up
- Automated daily status summaries and milestone alerts in Teams

**Early results (Week 1-2):**
- Status lookup time: from ~2 hours to <2 minutes
- Milestone alerts: 2 sent, both acted on same day
- Weekly meeting time on status alignment: reduced by 60%

**What we need next (pick one):**

| | Option A: Scale with existing tools | Option B: Build dedicated system |
|---|---|---|
| Time to 30 users | 4 weeks | 8-10 weeks |
| Resources needed | 0 (Sunny solo) | DevOps 1 + Backend 1 + Frontend 1 |
| Capability ceiling | Medium (no AI prediction, no API integration) | High (full AI pipeline, E3/PLM integration) |
| Risk | Low — already working | Medium — depends on headcount approval |
| My recommendation | ✅ Start here, prove value, then upgrade | Once Option A hits its ceiling |

**Ask:** Forward this to Jen with your endorsement for Option A. If she agrees, I can have 30 users on the system by end of June.

---

### 和领导沟通的3条铁律

1. **永远带成果去，不带问题去**。问题可以提，但必须是成果之后附带的问题。
2. **永远给选项，不给开放题**。"A还是B"比"你觉得怎么办"有效10倍。
3. **让他能复述**。如果他不能在30秒内向Jen说清楚AutoPM是什么、做了什么、要什么，你的沟通就失败了。上面那份Brief就是他的发言稿。

### 关于Jen的"I love it"

"I love it"不等于"I'll fund it"。把这句话当作许可，不当作承诺。你不需要Jen推你，你需要Jen**在你推出成果时点头**。策略是：

1. 你先跑出结果
2. 让领导拿着Brief去找Jen
3. Jen说"good"的那一刻，才是真正的授权信号

---

## 五、找人策略

### 思路转换：不找"开发者"，找"受益者"

WBS v2的思维是"我需要开发团队来建系统"。零资源版本不需要开发者，需要**用户**。

**逻辑**：谁痛谁帮忙。不痛的人不会给你时间，痛的人会主动投入。

### 找谁

| 角色 | 为什么痛 | 怎么让他受益 | 他能贡献什么 |
|------|---------|-------------|-------------|
| OF102的NPI | 同时管5-8个项目，追状态追到崩溃 | 给他一个不用追的仪表盘 | 试用+反馈+帮你在NPI圈子里传播 |
| OF102的工程师 | 每天被PM问"什么时候能交付" | 自动推送进度，减少被打扰 | 确认技术数据准确性 |
| 其他组的NPI | 和OF102 NPI一样痛 | 同样的方案复用 | 成为第2批试点用户 |
| Marcus（IT） | 每次数据权限申请都走他 | AutoPM规范了数据访问 | 帮你打通权限和安全审查 |

### 具体动作

1. **本周**：找OF102的2个NPI（你本来就认识），说"我帮你把OF102的状态追踪自动化了，你试试看，不好用算我的"。不要提"AI"、不要提"平台"、不要提"战略"。就说是**帮你省时间**的。

2. **试用第3天**：问他们"如果别人也想用，你愿意推荐吗？"如果他愿意，他就是你的传播节点。

3. **第2周**：让他带你去找另一个组的NPI。NPI之间的口口相传比你的邮件有效100倍。

4. **关于技术帮手**：不要找"开发者"，找"会用Excel的Power User"。Power Automate + Excel Online不需要写代码，会Excel公式就能搭。你的团队里一定有人是Excel高手，让他帮你优化数据模板和公式。

### 不要做的事

- 不要发全员邮件找人——那是在求人，不是在吸引人
- 不要开宣讲会——没有人有空听你讲愿景
- 不要等领导帮你协调——他不理解，协调不了
- 不要找IT部门要人——他们的排程已经排到Q3

---

## 六、2周时间线

### Week 1: 让它跑起来

| 天 | 做什么 | 交付物 |
|----|--------|--------|
| Day 1 (今天) | 手动抄OF102数据到AutoPM HTML v13.1 | v13.2-pilot，含真实数据 |
| Day 2 | 放到SharePoint，发给5个人 | 5人可访问，开始收集反馈 |
| Day 3 | 建Excel Online数据源（OF102_Project_Tracker.xlsx） | Excel数据源上线 |
| Day 4 | 搭Power Automate流程1（邮件→Excel） | NPI发邮件可更新状态 |
| Day 5 | 搭Power Automate流程2+3（Excel→Teams + 每日摘要） | Teams自动推送启动 |
| Day 6-7 | 接入Copilot，测试AI问答；修复Week 1的bug | Copilot可用 |

### Week 2: 证明它有价值

| 天 | 做什么 | 交付物 |
|----|--------|--------|
| Day 8 | 收集Week 1数据（3个指标） | Week 1效果数据 |
| Day 9 | 问5个用户：好不好用、缺什么、愿意推荐吗 | 用户反馈记录 |
| Day 10 | 根据反馈调整流程和模板 | v2改进版 |
| Day 11 | 写1页纸Brief给领导 | Brief文档 |
| Day 12 | 和领导15分钟沟通：成果 + Option A/B | 领导点头Option A |
| Day 13 | 请领导把Brief转给Jen | Jen看到实际成果 |
| Day 14 | 写Week 2效果报告 + 下一步计划 | 完整2周报告 |

---

## 七、如果2周后还是没资源

2周后可能出现3种情况：

### 情况A：领导支持了，Jen也点头了
→ 恭喜，你可以拿着授权去要资源了。这时候要1个后端开发+1个Power Automate高手，不需要整个团队。

### 情况B：领导支持了，Jen没表态
→ 继续跑。从OF102扩展到OF101/OF120（你还在关的项目），用更多数据说话。Jen不表态 = 不反对 = 你可以继续。

### 情况C：领导也没推动
→ 这时候你有两个选择：
1. **继续自己跑**：AutoPM在SharePoint+Power Automate上已经能跑，你一个人维护5-10个项目没问题。速度慢但方向对。
2. **战略性暂停**：把2周成果文档化，等下一个窗口。但文档化不是放弃——是"我准备好了，等组织跟上"。

**无论哪种情况，2周后的你都比2周前的你更有筹码。** 因为你不再是"我有一个想法"，而是"我有一个在跑的东西"。

---

## 八、和WBS v2的关系

这份Bootstrap Plan不是替代WBS v2，是**它的起跑线**。

```
Bootstrap Plan（零资源）          WBS v2（有资源）
├── Step 1: 手动MVP         ←→  Phase 0.4: 手动MVP（相同）
├── Step 2: 半自动          ←→  Phase 1: MVP可见性（用不同工具实现相同目标）
├── Step 3: 证明价值         ←→  Phase 1成功标准（用数据验证）
└── 2周后如果有资源          ←→  进入WBS v2的Phase 2（智能化+API对接）
```

**区别**：WBS v2从Phase 2开始才需要开发团队。Bootstrap Plan用公司工具链绕过了Phase 2对开发资源的依赖。

**转换条件**：当Bootstrap版本服务超过20人、Excel+Power Automate出现瓶颈时，就是启动WBS v2 Phase 2的时机。这时候你有了用户、有了数据、有了证明——要资源比现在容易10倍。

---

## 九、今天立刻做的3件事

1. **现在**：打开E3，抄OF102的6项核心数据
2. **下午**：填进AutoPM HTML，保存v13.2-pilot
3. **下班前**：上传SharePoint，把链接发给2个OF102 NPI

其他的，明天再想。先让它跑起来。
