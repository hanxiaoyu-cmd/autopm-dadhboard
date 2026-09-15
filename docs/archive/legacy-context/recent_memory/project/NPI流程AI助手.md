# NPI流程AI助手项目

> 创建：2026-05-27 | 更新：2026-05-27 | 状态：进行中

## 核心思路
- **知识驱动**：封装用户NPI知识，不接公司系统，零授权
- **双层漏斗**：流程地图（免费）→ AutoPM项目视图（登录）
- **撬动AutoPM**：学会流程→"我的项目走到哪了"→导入AutoPM

## 产品形态
1. **HTML页面**（`./NPI_Process_AI_Assistant.html`，V2=44KB）
   - 流程地图+AI对话+AutoPM入口 | 4Tab | V2：深色UI+发光+瓶颈动画+扩充知识库+9快捷按钮
2. **Coze Bot**（2026-05-27转向Coze）
   - Copilot Studio中国区GPT/Claude被限制，不可用
   - Coze无限制：上传知识库+发布Bot+分享链接→同事浏览器打开即用
   - 模型选豆包(Doubao)，纯问答不需Tools
   - 将来Copilot解锁后用同一份知识库重建（10分钟）
3. **知识库**：`./NPI_Process_Copilot_KnowledgeBase.md`（34KB）

## 知识库扩展优先级
1.🔴 认证/合规知识（最大价值） 2.🟡 ECN变更影响速查 3.🟢 内部术语 4.⚪ SharePoint

## 下一步
- ⏳ coze.cn创建Bot，上传知识库，设置Instructions，发布
- ⏳ 逐Gate核对知识库（有inaccuracies）
- ⏳ 收集同事反馈补知识
- ⏳ 认证知识整理（价值增量最大）
- ⏳ Coze Bot嵌入HTML右侧（边看边问）

## 战略
- 流程指南="教人游泳"，AutoPM="给人泳池" | 知识库=资产，平台=载体，随时搬家
