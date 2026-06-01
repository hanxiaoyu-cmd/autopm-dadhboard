# AutoPM PDF自动解析决策

> 更新时间：2026-05-28

## 背景（2026-05-25）
用户提出两个需求：
1. 新添加的任务缺少责任人和时间——Add Task弹窗只问name和phase，缺owner和due_date
2. 新上传的项目要自动出现在My Project List，并能自动拆解成任务+显示项目状态

## 讨论过程
- 用户问"能不能做到"上传PDF自动识别+拆解任务+百分比
- 评估结论：能做到，基于SharkNinja标准NPI流程自动映射
- 用户问"上传到网站还是对话框"——当前网站无此功能，只能通过对话上传
- 实际验证：用户上传SL500EUUK Project Plan PDF，成功解析并创建39个任务

## 决策
1. **短期方案**：用户通过对话上传PDF→AI解析→API创建项目+任务→出现在My Projects
2. **中期方案**：网站端集成PDF上传+自动解析功能（待开发）
3. **Add Task改进**：弹窗需增加owner和due_date字段（待开发）

## 待解决
- Add Task弹窗增加owner/due_date输入
- SL500EUUK(2877)的39个任务status/owner/due_date需批量更新完
- 网站端PDF上传功能开发
- 新项目自动出现在My Project List逻辑
