# AutoPM 完整上下文包

**打包时间：** 2026-06-01  
**打包人：** Sunny的AI助手  
**用途：** 交给其他AI协助AutoPM项目

---

## 一、AutoPM是什么

AutoPM是SharkNinja的NPI项目管理系统，目标是从50人Pilot扩展到2000人全员使用。

**愿景：** 简化流程，扁平化组织，加快速度，提高效率，全员参与。

**核心价值：**
1. 单一事实来源 — 所有项目数据汇聚一处（邮件、Teams、周报、时间表、会议纪要）
2. 实时可见性 — 从PM到高管，实时看到项目真实状态
3. 主动风控 — 风险爆发前被识别，不是事后救火
4. 效率革命 — PM从信息搬运中解放，时间花在决策
5. 组织记忆 — 知识留在系统里，不随人走

**四层架构：**
- L1 公司级：高管看全公司项目状态、Pipeline、风险雷达
- L2 部门级：部门项目概览、跨项目对比
- L3 个人级：我的项目列表、我的任务
- L4 项目级：项目详情（Overview/Tasks/Document/Workflow四个Tab）

---

## 二、系统信息

### 线上环境
- URL: https://autopm-dashboard.onrender.com
- 登录: sunny / autopm2026
- 当前版本: v18.1

### 技术栈
- 前端: 单页HTML (index.html)，无框架，纯JS+Tailwind CSS
- 后端: FastAPI (Python)，PostgreSQL (Neon, Singapore)
- 部署: Render.com (免费计划)
- CI/CD: GitHub push → Render自动部署

### GitHub
- 仓库: https://github.com/sunny-06064710-3/autopm-dadhboard.git
- 用户: sunny-06064710-3
- 注意: 仓库需保持Private（SN安全团队已警告）

### 数据库
- Neon PostgreSQL (Singapore)
- 连接串在Render环境变量中
- 4个真实项目: Project-S(52%), Project-B(61%), Project-A8(5%), Project-A1(9%)

### 关键API端点
- POST `/api/auth/login` — 登录
- GET `/api/projects?limit=200` — 项目列表
- GET `/api/milestones?project_id=X` — 项目milestone
- PATCH `/api/milestones/{id}/field` — 更新字段 (body: {field, value})
- POST `/api/admin/reseed` — 强制重新seed（需admin token）
- DELETE `/api/projects/{id}` — 删除项目

### 前端文件位置（重要）
- `/tmp/autopm-repo/frontend/index.html` — 顶层（git push用）
- `/tmp/autopm-repo/backend/frontend/index.html` — 实际服务文件
- 两个必须同步更新

---

## 三、项目历史

### 版本线
- v9-v13: 早期原型，多次迭代
- v14-v17.7: 功能扩展期（L1-L4页面、AI层等）
- v17.8-v18.2: 修复期，但引入大量bug，整体废弃
- **回滚到v17.5.4稳定版**（用户强烈要求）
- v17.5.5: 添加Document功能+版本号
- **v17.5.6**: seed.py重写+L4 Tasks从API加载+状态/日期可编辑
- v18.1: 当前稳定版，核心功能正常

### 关键教训
- **不要在千疮百孔的版本上打补丁，应回滚到稳定版再增量修改**
- **一次只改一个，检查无误再输出**
- **不要自主修改用户没提到的内容**
- **先上线再迭代**

---

## 四、4个真实项目

项目名已脱敏，映射关系：
- SL500EUUK → Project-S (52%)
- BW1001EUUK → Project-B (61%)
- AS080UK&EU → Project-A8 (5%)
- AS101KRxx → Project-A1 (9%)

每个项目有完整的milestone数据（Phase/Task/Status/Start/Finish/Owner），存储在seed.py中。

PDF源文件路径：
- SL500EUUK: `用户上传/SL500EUUK Project plan(9th May update)_1780035324791_0_jz3o.pdf`
- BW1001EUUK: `用户上传/BW1001EUUK-0518_1779971541205_0_7kte.pdf`
- AS080UK&EU: `用户上传/AS080UK&EU project plan_0330_1779971541205_1_3eq6.pdf`
- AS101KRxx: `用户上传/AS101KRxx Project plan MP on Sep 10_1779971541206_2_q3wn.pdf`

---

## 五、供应商评估（截至2026-05-29）

### 评估结论
- **Agileex确认不行** — 微软生态填报+BI工具，无PM能力、无AI理解、无自动数据采集
- **Ody方向对但未验证** — AI知识平台，声称自动采集+AI洞察，但全部未在SN环境验证
- **两家都不懂PM** — SN必须自己承担流程设计

### Ody (Rodyr)
- 创始人: Ufuk Karaca
- 商务模式: 3种（Bespoke/Licensing/Reuse），推荐Licensing
- NDA: 需补充residuals clause
- 下一步: Discovery Phase (6-8周)
- IT Onboarding文档: `用户上传/2026-04-22_it-onboarding-overview_1780037563814_0_k7a5.pdf`

### Agileex
- 130人团队，11年微软生态经验
- MVP 4周可交付
- 但Power Apps天花板明确

### 推进计划
- 周二(6/2) Jen向Ross汇报
- 目标: 拿到Ody Discovery Phase批准
- 待做: Jen汇报brief、Ody深度验证问题清单、约Ufuk第二轮会

---

## 六、Sunny的约束和偏好

### 绝对不可违反
- ❌不提Ross/CEO/Jen ❌不叫Dashboard ❌说prototype ❌不说"加入AutoPM"
- ❌未经确认不推GitHub
- 允许慢但千万不要乱搞
- 一次做一个
- 学术论文绝不能有AI痕迹

### 输出质量
- 精简>详尽
- 先想再写
- 未知留空不瞎填
- 听指令不改指令
- 站在受众角度
- Signal through contrast, not through volume

### Sunny背景
- SharkNinja苏州PM
- 华东师大CTO学院MEM
- 厨房清洁机器人创始人
- 直属老板Jian隔2层到CDO Ross

---

## 七、待办清单

### 紧急（本周）
- [ ] Jen汇报brief（一页英文，周二前）
- [ ] Ody深度验证问题清单
- [ ] 约Ufuk第二轮会议

### 网站待办
- [ ] L4 Overview页面动态化（目前有硬编码数据）
- [ ] 版本号显示bug修复
- [ ] 移动端适配

### 长期
- [ ] 从50人Pilot到2000人推广方案
- [ ] AI层接入（SN内部AI团队负责）
- [ ] 与Ody Discovery Phase推进

---

## 八、文件清单

本包内文件：
```
autopm-package/
├── AutoPM_FULL_CONTEXT.md    ← 你正在读的这个文件
├── frontend/                  ← 前端代码（index.html）
├── backend/                   ← 后端代码（FastAPI + seed.py + 数据库）
├── render.yaml                ← 部署配置
├── README.md                  ← 项目README
├── docs/                      ← 所有文档
│   ├── AutoPM_Vendor_Evaluation.md
│   ├── AutoPM_Vendor_Assessment_Summary.md
│   ├── Ody_vs_Agileex_对比报告_Jen_v2.md
│   ├── AutoPM_供应商推进计划.md
│   ├── AutoPM_Strategic_Plan.md
│   ├── AutoPM-Project-Handoff.md
│   ├── AutoPM_60Day_Roadmap.md
│   ├── AutoPM-Phase1-Full-Plan.md
│   ├── AutoPM_架构设计文档.md
│   ├── AutoPM_Platform_WBS.md
│   ├── AutoPM_市场调研报告.md
│   ├── Rodyr调研报告.md
│   ├── AutoPM_4Projects_Breakdown_v2.xlsx
│   └── ... (更多文档)
└── recent_memory/             ← 决策记录和项目进度
    ├── decision/
    ├── project/
    ├── todo/
    └── index.json
```
