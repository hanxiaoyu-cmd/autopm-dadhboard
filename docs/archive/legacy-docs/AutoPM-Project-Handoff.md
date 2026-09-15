# AutoPM Dashboard — 项目交接文档

> **版本**: v17.2 (2026-05-22)  
> **代码仓库**: https://github.com/sunny-06064710-3/autopm-dadhboard  
> **在线地址**: https://autopm-dashboard.onrender.com  
> **管理账号**: sunny / autopm2026

---

## 一、项目是什么

AutoPM 是一个**项目组合管理仪表盘**，面向消费电子行业（SharkNinja）的 PMO 团队，用于跟踪 2000+ 个项目的状态、里程碑、风险和阻塞。核心能力：

- 四层钻透式架构：L1全局总览 → L2部门视角 → L3个人仪表盘 → L4项目详情
- AI 智能助手：项目优化建议、风险预警、自然语言问答
- PDF/DOCX 上传智能解析：上传项目文件自动提取项目信息导入系统
- 团队协作：关注/订阅项目、反馈建议、部门产能分析
- 实时告警引擎：超期预警、阻塞提醒

---

## 二、技术架构

```
┌──────────────────────────────────────────────┐
│  Frontend (Single-Page App)                  │
│  backend/frontend/index.html (14,477 行)     │
│  纯 HTML + CSS + Vanilla JS，无框架           │
│  通过 fetch() 调后端 API                      │
└───────────────┬──────────────────────────────┘
                │ REST API (JSON)
┌───────────────▼──────────────────────────────┐
│  Backend (FastAPI + SQLAlchemy)               │
│  backend/main.py (1,605 行) — 所有 API 路由   │
│  backend/models.py — 数据库模型               │
│  backend/schemas.py — Pydantic 校验模型        │
│  backend/pdf_parser.py — PDF 智能解析         │
│  backend/alerts_engine.py — 告警引擎          │
│  backend/auth.py — JWT 认证                   │
│  backend/database.py — 数据库连接             │
│  backend/seed.py — 种子数据 (2200项目)         │
└───────────────┬──────────────────────────────┘
                │ SQLAlchemy ORM
┌───────────────▼──────────────────────────────┐
│  Database                                     │
│  本地: SQLite (autopm.db)                     │
│  生产: PostgreSQL (通过 DATABASE_URL 环境变量) │
└──────────────────────────────────────────────┘
```

**部署**: Render.com (免费层)，`render.yaml` 配置自动部署  
**Git 推送 → Render 自动部署**，无需手动操作。

---

## 三、文件结构与职责

```
autopm-deploy/
├── backend/
│   ├── main.py              # ★ 核心后端：全部 API 路由 (52个端点)
│   ├── models.py            # ★ 数据库模型：Project/Milestone/Risk/Alert/User/Feedback/UserProject
│   ├── schemas.py           # ★ 请求/响应模型：Pydantic 定义
│   ├── pdf_parser.py        # PDF/DOCX 上传 + 智能解析引擎
│   ├── alerts_engine.py     # 告警计算：超期/阻塞/即将到期
│   ├── auth.py              # JWT 认证逻辑
│   ├── database.py          # 数据库连接配置 (SQLite/PostgreSQL 双模式)
│   ├── seed.py              # 种子数据生成器 (含 2200 项目模板)
│   ├── autopm.db            # SQLite 数据库文件
│   ├── requirements.txt     # Python 依赖
│   ├── Procfile             # Render 启动命令
│   ├── uploads/documents/   # 上传文件存放目录
│   └── frontend/
│       └── index.html       # ★ 唯一前端文件 (14,477行)，包含全部 CSS + JS
├── render.yaml              # Render.com 部署配置
├── README.md                # 部署指南 (中英双语)
└── .gitignore
```

**重要约定**：
- 前端只有 1 个 index.html，没有构建步骤，所有 CSS/JS 都内联
- 后端 main.py 是单文件路由，没有拆分 router（简单但文件较长）
- 数据库操作通过 SQLAlchemy ORM，session 通过 `Depends(get_db)` 注入

---

## 四、数据库模型

### Project (核心表)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| name | Text | 项目代码，如 XT-500, RV-900 |
| category | Text | Extension/Legacy/NPD/Dual Source 等 |
| status | Text | In Progress/Completed/On Hold/Cancelled |
| phase | Text | Kick Off → EB0 → EB1 → DQTP → MP |
| owner | Text | 项目负责人 |
| brand | Text | Shark / Ninja |
| factory | Text | 工厂 |
| start_date | Text | 开始日期 (YYYY-MM-DD) |
| end_date | Text | 结束日期 |
| progress | Float | 进度 0-100 |
| risk_flag | Text | None/Low/Medium/High/Critical |
| risk_note | Text | 风险说明 |
| source_system | Text | Manual/PDF Upload/SAP 等 |
| department | Text | PMO/PD/EE/ID/CMF/DQTP/SC 等 |
| blocked_at | Text | 阻塞日期 |
| blocked_days | Integer | 阻塞天数 |
| blocked_department | Text | 阻塞部门 |
| priority | Text | P0/P1/P2/P3 |
| notes | Text | 备注 |

### Milestone (里程碑)
| 字段 | 类型 | 说明 |
|------|------|------|
| project_id | Integer FK | 关联项目 |
| name | Text | 里程碑名称 |
| phase | Text | 所属阶段 |
| due_date / actual_date | Text | 计划/实际日期 |
| status | Text | Not Started/In Progress/Completed |
| owner | Text | 负责人 |
| is_manual | Integer | 0=系统, 1=手动 |
| manual_priority | Text | P1-P4 |
| manual_notes | Text | 手动备注 |

### Risk (风险)
| 字段 | 类型 | 说明 |
|------|------|------|
| project_id | Integer FK | 关联项目 |
| description | Text | 风险描述 |
| severity | Text | Low/Medium/High/Critical |
| mitigation | Text | 缓解措施 |
| owner / status / days | — | 负责人/状态/天数 |

### Alert (告警)
| 字段 | 类型 | 说明 |
|------|------|------|
| project_id | Integer FK | 关联项目 |
| type / level / message | Text | 类型/级别/消息 |
| is_read | Integer | 0=未读, 1=已读 |

### User / Feedback / UserProject
- User: 用户认证 (username, password_hash, role)
- Feedback: 产品反馈 (name, role, category, content)
- UserProject: 用户关注的项目 (username, project_id)

---

## 五、API 端点一览

### 认证
- `POST /api/auth/login` → 登录，返回 JWT
- `GET /api/auth/me` → 当前用户信息

### 项目 CRUD
- `GET /api/projects` → 项目列表 (支持 ?status= & department= 等筛选)
- `GET /api/projects/{id}` → 项目详情 (含 milestones/risks/alerts)
- `POST /api/projects` → 新建项目
- `PUT /api/projects/{id}` → 更新项目
- `DELETE /api/projects/{id}` → 删除项目
- `GET /api/projects/summary` → **聚合统计** (by_status, by_department, overdue 等)
- `GET /api/projects/template` → CSV 模板下载
- `POST /api/projects/import` → CSV 批量导入
- `GET /api/projects/export` → CSV 导出

### 里程碑 / 风险 / 告警
- `GET/POST /api/milestones` | `PUT/DELETE /api/milestones/{id}`
- `GET/POST /api/risks` | `PUT /api/risks/{id}`
- `GET /api/alerts` | `PUT /api/alerts/{id}/read` | `POST /api/alerts/refresh`

### 仪表盘
- `GET /api/dashboard/stats` → Dashboard 统计
- `GET /api/dashboard/timeline` → 时间线数据

### PDF 上传 & 智能导入
- `POST /api/upload/document` → 上传文件，自动解析返回项目数据
- `POST /api/upload/import` → 确认导入解析出的项目
- `GET /api/upload/history` → 上传历史

### AI 助手
- `POST /api/ai-chat/message` → 发送消息
- `GET /api/ai-chat/history` → 历史记录
- `POST /api/ai-chat/feedback` → 对话反馈

### 其他
- `GET /api/departments/capacity` → 部门产能
- `GET /api/public/my-dashboard/{owner}` → 个人仪表盘
- `POST /api/feedback` | `GET /api/feedback` → 产品反馈
- `POST /api/user-projects` | `GET/DELETE /api/user-projects/{username}` → 关注项目
- `POST /api/admin/reseed` → 重置数据库

---

## 六、前端架构

### 四层钻透 (核心交互模式)

```
L1 全局总览    →  Pipeline漏斗 + 统计卡片 + 部门环图
   ↓ 点击钻入
L2 部门视角    →  热力图 + 项目列表 + 筛选器
   ↓ 选择项目
L3 个人仪表盘  →  我关注的项目 + AI建议 + 邮件布局
   ↓ 进入详情
L4 项目详情    →  里程碑甘特 + 风险卡片 + 任务看板 + 文档
```

**关键 JS 函数** (共 274 个)：
- `v16SwitchLevel(level)` — 切换层级
- `v16RenderL1/L2/L3/L4()` — 渲染各层级
- `openUploadModal()` — 打开 PDF 上传弹窗
- `v17ShowToast(msg, color)` — Toast 通知
- `aiChat()` — AI 助手对话

**CSS 变量体系**：
- 主色: `#7c3aed` (紫), `#3b82f6` (蓝), `#00CC66` (绿)
- 状态: 紫色=In Progress, 绿色=Completed, 黄色=On Hold, 红色=Cancelled
- 深色主题，所有颜色带透明度适配暗背景

---

## 七、PDF 智能解析 (pdf_parser.py)

上传 PDF/DOCX → 提取文本 → 正则匹配关键实体 → 结构化输出

**识别能力**：
| 实体 | 匹配规则 | 示例 |
|------|----------|------|
| 项目代码 | `[A-Z]{2,4}[-]\d{2,4}` | XT-500, RV-900 |
| 品牌 | Shark / Ninja 关键词 | |
| 部门 | PMO/PD/EE/ID/CMF/DQTP/SC 等 12 个 | |
| 负责人 | Owner:/PM:/Lead: 后跟人名 | |
| 阶段 | Kick Off → MP 共 10 个阶段关键词 | |
| 优先级 | P0-P3 / Critical/High/Medium/Low | |
| 风险 | risk/blocker/issue/delay 后跟描述 | |
| 里程碑 | G1-G6 / Gate / milestone / checkpoint | |
| 日期 | YYYY-MM-DD / MM/DD/YYYY / Jan 15 2026 | |

**解析流程**：
1. 文件上传到 `uploads/documents/`
2. `pdfplumber` 提取文本+表格 (PDF) 或 `python-docx` (DOCX)
3. 全文正则扫描实体
4. 以项目代码为中心，取 ±200 字符上下文推断关联属性
5. 返回 `projects[]` + `summary` + `preview`
6. 用户确认后调用 `/api/upload/import` 写入数据库

---

## 八、部署方式

### 方式 A：Render.com (当前方案)
1. 推代码到 GitHub
2. Render 连接仓库，自动部署
3. 环境变量：`DATABASE_URL` (可选，默认 SQLite)
4. 免费层限制：休眠、750h/月、SQLite 不持久

### 方式 B：本地运行
```bash
cd backend
pip install fastapi uvicorn sqlalchemy pdfplumber PyJWT python-multipart
uvicorn main:app --host 0.0.0.0 --port 8088
# 访问 http://localhost:8088
```

### 方式 C：Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt && pip install pdfplumber
EXPOSE 8088
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
```

---

## 九、已知问题 & 改进方向

### 当前已知问题
1. **SQLite 并发**: 多人同时写入可能锁库，生产环境建议换 PostgreSQL
2. **AI 聊天**: 当前是本地关键词匹配，非真正 LLM；如需接入真实 AI，需替换 `/api/ai-chat/message` 实现
3. **PDF 解析精度**: 依赖正则匹配，对非标准格式文档可能提取不全；扫描件 PDF 无法解析
4. **前端单文件**: index.html 14,477 行，维护困难；长期应拆分为组件化框架

### 优先改进方向
1. **接入真实 AI** — 替换 AI 聊天为 LLM API (OpenAI/Claude/国产大模型)
2. **PDF 解析增强** — 接入 OCR (扫描件) + LLM 抽取 (复杂文档)
3. **数据持久化** — 生产环境配 PostgreSQL，避免 SQLite 重置
4. **权限体系** — 目前只有 admin/member 两级，可细化到部门级权限
5. **移动端适配** — 当前为桌面设计，移动端体验待优化
6. **前端重构** — 考虑迁移到 React/Vue 组件化架构

---

## 十、设计约定 & 代码风格

1. **后端**: FastAPI 同步函数为主，`Depends(get_db)` 注入数据库 session
2. **前端**: Vanilla JS，无框架；全局变量以 `v16`/`v17` 前缀区分版本
3. **命名**: API 路径 kebab-case (`/api/projects/{id}`)；JS 函数 camelCase；CSS BEM-ish
4. **日期**: 全部用文本存储 `YYYY-MM-DD`，不做时区转换
5. **颜色**: 深色主题，主色 `#7c3aed`，状态色固定（紫/绿/黄/红）
6. **数据**: 项目代码格式 `[A-Z]{2-4}-[0-9]{2-4}`，如 XT-500
7. **Git**: commit 格式 `AutoPM vX.Y: 功能描述`，主分支 main

---

## 十一、快速上手清单

拿到代码后，按以下步骤确认系统正常：

- [ ] `cd backend && pip install -r requirements.txt && pip install pdfplumber`
- [ ] `uvicorn main:app --port 8088` 启动成功
- [ ] 访问 `http://localhost:8088` 看到仪表盘
- [ ] 登录 sunny/autopm2026
- [ ] L1 总览能加载数据
- [ ] 点击项目能钻入 L4 详情
- [ ] 侧边栏 📄 按钮打开 Upload 弹窗
- [ ] 上传一个 PDF/DOCX 能解析出项目
- [ ] AI 聊天面板能打开
- [ ] `/api/health` 返回 `{"status": "ok"}`

---

*文档生成于 2026-05-22，基于 AutoPM v17.2 代码*
