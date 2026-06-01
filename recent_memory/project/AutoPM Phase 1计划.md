# AutoPM Phase 1计划（Agileex合作）

**项目日期**: 2026-05-28
**负责人**: Sunny + Agileex (Summer/Ruotong)

## 目标
4-6周内交付基础可用的PM系统，让PM能在系统内完成日常操作，替代Excel

## 交付物
1. **Power Apps PM操作界面**
   - 任务创建/编辑/更新
   - 项目概览视图
   - 我的任务列表
   - 状态更新表单

2. **Power BI基础报表**
   - 项目健康度看板
   - 任务进度跟踪
   - 逾期任务预警

3. **Power Automate流程**
   - ECN邮件自动创建任务
   - 状态变更邮件通知

4. **SharePoint对接**
   - 项目文档关联
   - PLM文件夹同步

5. **AI接口预留**
   - 提供API/Webhook规范
   - 支持SN内部AI服务调用系统数据和操作

## 进度计划
| 阶段 | 时间 | 内容 | 依赖 |
|------|------|------|------|
| 需求确认 | 第1周 | 对齐Phase 1需求，确认交付物范围 | Sunny提供业务逻辑 |
| 界面开发 | 第2-3周 | Power Apps界面开发与测试 | Agileex团队 |
| 报表开发 | 第3-4周 | Power BI报表开发与测试 | Agileex团队 |
| 集成开发 | 第4-5周 | 邮件/SharePoint集成开发 | Agileex团队 |
| 测试验收 | 第5-6周 | 用户测试，修复Bug | Sunny + PM团队 |
| 上线部署 | 第6周 | 正式上线，用户培训 | Agileex + Sunny |

## 资源需求
- Agileex: 2名开发人员（Power Apps/Power BI）
- Sunny: 业务逻辑定义，验收测试，用户培训
- 不需要IT部门支持（Phase 1使用手动+SharePoint数据）

## 风险与应对
| 风险 | 应对 |
|------|------|
| Agileex不理解PM场景 | Sunny定义详细业务规则，提供原型参考 |
| 开发延迟 | 分阶段验收，每周同步进度 |
| 用户不接受 | 提前邀请PM参与需求确认和测试 |