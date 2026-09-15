# Rodyr/Ufuk AutoPM提案审查

> 日期：2026-05-25 | ✅审查完毕，邮件回复草稿已写
> 版本：Proposal V2.2.1

## 关键人物
Ufuk(ufuk@rodyr.com,Rodyr创始人)/Matthieu(不重复造轮子)/Jen(visibility)/Ashbury(pa@rodyr.com)

## S01·4处纠正
1."Not managing tasks"是优先级非排除→已有Task CRUD 2.根因=无PM系统非集成问题 3."30%"是举例非验证 4."sit on top"指AutoPM非PLM/E3

## Cards审查
- Foundation(01-05)：已建好，增量低 | Feature(06-10)：真正缺口
- 06 Insight最有价值但缺数据 | 08 Digest对Jen最有用可行性高
- Expansion(11)低优(行为问题非技术) | Integration(14)Email高值,(15)Pilot过早

## 整体问题
1/3重复造轮子|Integration前提错|零定价|缺数据采集Card

## 用户核心立场
⚠️不能依赖Matthieu/外部→先自证价值再扩展 | MVP：20项目+100人试点

## Prerequisites(6项)
3缺失(IT/pilot team/mandate)|2可立即给(mailbox/JSON)|1待IT(数据驻留)

## Open Qs修正
Q1:2200+占位仅~5真|Q8:O365+Teams无Lark|Q6-9:待IT call|Q11:决策未被记录

## 邮件回复
4处纠正+3个开会重点(MVP scope/数据/定价)|我们定义Phase1，Rodyr执行


## 全面调研评估（2026-05-29补充）

### 一、Rodyr公司概况
- **成立时间**：2025年
- **总部**：柏林（德国）
- **团队规模**：极小型（2-3人，核心为创始人Ufuk Karaca）
- **核心产品**：Ody - 团队知识运行时（Skills runtime）

### 二、技术能力评估
- ✅ 自适应RAG + 知识图谱（自研）
- ✅ MCP协议深度集成（Claude Code/Cursor/Codex）
- ✅ On-prem部署 + 自带LLM方案
- ⚠️ 底层仍依赖OpenRouter/OpenAI等第三方LLM
- ⚠️ 缺乏Oracle ERP、SharePoint等企业系统集成经验

### 三、综合评估得分：3.45/10

### 四、合作建议
**不建议作为AutoPM主要合作伙伴**，推荐：
1. **技术顾问角色**：邀请Ufuk作为AI能力外部顾问（按小时付费）
2. **特定模块采购**：采购Ody的Skills运行时作为AutoPM子系统
3. **POC验证**：先做3-6个月概念验证，评估技术价值后再扩展