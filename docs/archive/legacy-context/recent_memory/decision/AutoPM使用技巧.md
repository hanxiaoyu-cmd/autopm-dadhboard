# AutoPM使用技巧
- ⭐铁律：复用原版组件，不重设计！架构: index.html(~14K行); 测试8088/生产8099
- v17 API: tasks/blockers/departments/capacity/Risk/milestones；/projects超时→summary+limit=200
- ⚠️字段：milestone.notes=manual_notes；Project无is_project_a/estimated_days（传了会500）
- ⚠️L3/L1数据源：/user-projects和/projects/summary；双前端目录：`backend/frontend/index.html`
- ⚠️v18.1 Bug：API认证失效返回dict而非array→.filter()崩溃；`<script>`提前闭合
- 常用参考：v17.5.4(基准)/v17.2(L4完整)/v15.2(Tasks)；版本档案`autopm-versions/`