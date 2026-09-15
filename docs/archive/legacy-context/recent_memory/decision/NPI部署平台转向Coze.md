# NPI流程AI助手部署平台决策

> 创建时间：2026-05-27 | 决策状态：已确认

## 决策
NPI流程AI助手从Copilot Studio转向Coze(扣子)平台部署

## 背景
- 用户在Copilot Studio创建Agent后，发现GPT和Claude模型在中国区被限制，无法使用
- 只能选择GPT和Claude两个模型，两者均不可用于中国区
- M365租户可能注册在中国区（21Vianet运营版），导致Copilot Studio AI功能受限

## 推理过程
1. **Copilot Studio不可用**：中国区模型限制是硬性约束，个人无法绕过
2. **Coze完全可用**：用户已在Coze上使用，无区域限制，支持知识库+Bot+分享
3. **知识库通用**：md文件两边都能用，迁移成本极低
4. **先验证后迁移**：先在Coze验证价值，等Copilot解锁再迁移

## 替代方案
- A. 等Copilot Studio区域问题解决 → 时间不确定
- B. 联系IT切换M365租户到全球区 → 流程复杂
- C. **在Coze上先做（已选择）** → 马上可用

## 结论
先在Coze上发布，快速验证价值。知识库是资产，平台是载体，随时可迁移。将来Copilot Studio解锁后10分钟重建。

## 影响范围
- Teams内嵌入体验暂不可用（Coze Bot只能通过链接分享）
- 同事需浏览器打开链接，不能直接在Teams里@Bot
