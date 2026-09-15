# AutoPM改革项目详情

> 更新时间：2026-05-30（v18.1浏览器验证✅）

## 当前版本：v18.1 ✅
- **v18.0（2026-05-30）**：版本号更新至v18.0
- **v18.1（2026-05-30）**：修3个Bug——API认证失效dict崩溃/defensive check/`<script>`提前闭合/`<style>`拼写错误
- **v18.2（2026-05-30）**：L3项目详情面板（右侧显示按Phase分组milestone+状态切换）| L4 Document侧边栏布局（左侧文件夹树+右侧文件列表）| L3 API加limit=200确保真实项目显示 | L3默认订阅优先ID2882-2885真实项目 | elapsedDays动态计算（替换Day 42硬编码）| L4 Tab栏移除Workflow和Team

## v18.1 Browser验证结果（2026-05-30）✅
| 验证项 | 状态 | 说明 |
|--------|------|------|
| 无console错误 | ✅ | 无"projects.filter is not a function" |
| L4 Overview | ✅ | milestone stats/blocker banner/timeline/dept wheel正常 |
| Task Board | ✅ | 39 tasks，4列(Not Started/In Progress/Blocked/Completed) |
| 状态切换 | ✅ | 点击"Not Started"→"Blocked"正常 |
| Document | ✅ | NPI 00-13（14个文件夹），每个4文件 |
| ⚠️版本号 | 异常 | 站点显示v18.0而非v18.1（可能未重新部署）|

### 验证方法（agent-browser）
```bash
agent-browser open https://autopm-dashboard.onrender.com/
eval('v16SwitchLevel("L4")')    # L级切换
eval('v16SwitchTab("Tasks")')   # Tab切换
eval('button.click()')          # 状态循环
```

## Bug修复详情
### v18.1（2026-05-30）
- Bug1：`projects.filter is not a function` → token失效时API返回`{detail:...}`dict；修复：L2 Overview/L3 My Work/L4 Overview/L4 Tasks/L2 Projects加`Array.isArray()`检查
- Bug2：第二个DOMContentLoaded在`</script>`后，v16ExitToImport成纯文本；修复：删除重复handler，移入第一个
- Bug3：文件末尾`</style>`拼写成`</script>`

### v17.9.1 L4（2026-05-30）
- 根因：`AI_HINTS`/`aiBubble`/`v16ShowToast`/`C`颜色常量合并时丢失
- 修复：补回C/AI_HINTS/aiBubble/v16ShowToast；Overview sl500LoadTasks()→API milestones；部门轮盘→内联计算；v16ShowDeptDetail用window._v17L4ProjectMilestones
- ⚠️文件清空事故：每步替换后立即write+verify

### ⚠️合并Bug教训（2026-05-29）
XT-500→stead_of_xt500断裂 | v16OpenProject被覆盖 | auth_token vs autopm_token不一致 | 只更新frontend/未同步backend/frontend/

## 真实项目（IDs 2882-2885，141ms）
SL500EUUK(2882)EB0 62% 39ms | BW1001EUUK(2883)EB0 61% 56ms | AS080UK/EU(2884)EB1 5% 29ms | AS101KRxx(2885)EB1 9% 17ms

## 用户明确要求（2026-05-29）
L1/L2不动 | L3排列满意点击跳转L4 | L4 Overview：Blocker横幅+4统计卡+Milestone时间线+部门轮盘 | L4 Tasks：v15.2风格Phase分组状态可切换 | L4 Document：NPI 00-13文件夹 | ⚠️底部Speed/Simulation删掉 | 改前备份 | 改完浏览器验证

## 版本档案（autopm-versions/）
v14-v18.1完整备份；关键：v17.5.4(满意基准)/v17.2(L4完整)/v15.2(Tasks)；⚠️Render服务backend/frontend/index.html

## v18.0验证发现（2026-05-29）
### 核心问题
- **My Work页面（L3 Personal）Bug**：`projects.filter is not a function`，根因：API返回401未授权时返回`{detail: "Could not validate credentials"}` dict而非array，前端未做防御性检查
- **API端点错误**：前端调用不存在的`/api/user-projects/`端点，正确端点为`/api/projects`
- **UI显示异常**：API返回100个项目，但UI显示"No project found"；直接访问项目URL返回404
- **登录状态问题**：使用用户名sunny、密码autopm2026可成功登录获取token，但UI未正确使用token加载数据

### 修复措施（已在v18.1中实现）
- L2 Overview/L3 My Work/L4 Overview/L4 Tasks/L2 Projects添加`Array.isArray()`防御性检查
- 前端API调用从`/api/user-projects/`改为`/api/projects`
- 确保登录后token正确注入所有API请求
- 优化项目列表渲染逻辑，确保API返回数据正确显示