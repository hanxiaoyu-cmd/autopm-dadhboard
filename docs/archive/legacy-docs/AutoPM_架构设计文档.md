# Auto-PM 智能项目调度系统架构设计文档

## 一、项目背景

SharkNinja作为高端家电企业，同时进行1000+项目，当前项目管理面临以下痛点：

- **信息不透明**：项目状态、进度数据分散，难以统一查看
- **层层审批**：流程冗长，决策效率低下
- **信息搬运**：项目经理80%时间用于信息收集、整理和汇报
- **救火式管理**：问题发生后才被动响应，缺乏预判机制

**Auto-PM目标**：用AI自动分派任务、自动流转信息、自动识别问题，让管理者从救火转向真正的管理。

---

## 二、系统架构图

### 2.1 整体架构概览

系统采用中心辐射型架构，以Auto-PM智能调度核心为中心，向外辐射四大层级：

```
                    ┌─────────────────┐
                    │   用户接入层    │
                    │ PMO / 管理者   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Auto-PM核心   │
                    │  智能调度引擎   │
                    └────────┬────────┘
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼───────┐     │     ┌────────▼─────────┐
    │   核心引擎层    │     │     │   工作站层       │
    │ 任务分解/分配   │     │     │ 12个业务部门    │
    │ 流程控制/风险   │     │     │ 状态实时更新    │
    └─────────────────┘     │     └──────────────────┘
                             │
                    ┌────────▼────────┐
                    │   数据持久层    │
                    │ 项目/任务/资源  │
                    └─────────────────┘
```

### 2.2 架构分层说明

#### 【用户接入层】
- **PMO（项目管理办公室）**：项目需求入口，整体进度监控
- **管理者**：查看项目大盘、瓶颈分析、资源调配决策
- **工作站用户**：各部门执行人员，接收任务、提交成果

#### 【Auto-PM智能调度核心】
- 圆形发光核心节点，视觉中心
- 统一任务分发、状态同步、信息流转中枢
- AI智能决策大脑

#### 【核心引擎层】
1. **任务分解引擎**：基于项目需求，智能拆解为可执行任务单元
2. **资源分配引擎**：根据部门负载、人员能力、任务优先级自动分配
3. **流程控制引擎**：管理任务依赖关系，控制流转顺序
4. **风险检测引擎**：实时监控进度偏差，预警潜在风险

#### 【工作站层】（12个业务部门）

| 工作站代码 | 部门名称 | 主要职责 |
|-----------|---------|---------|
| PD | 产品设计 | 产品需求、功能定义 |
| ID Spec | 工业设计 | 外观、结构设计 |
| UI Spec | UI设计规范 | 界面设计标准 |
| UI Flow | 交互流程 | 用户体验设计 |
| PSD | 原型设计 | 产品原型制作 |
| EE | 电子工程 | 电路、硬件设计 |
| DQTP | 质量测试 | 品质验证、测试 |
| Compliance | 合规认证 | 法规、认证申请 |
| Planning | 计划排期 | 生产计划制定 |
| SC | 供应链 | 物料采购、供应商 |
| Marketing | 市场营销 | 市场推广、销售 |
| Logistics | 物流仓储 | 仓储、配送管理 |

#### 【数据持久层】
- **项目数据库**：项目基本信息、里程碑、整体状态
- **任务数据库**：任务详情、分配记录、进度追踪
- **资源数据库**：人员信息、部门负载、能力标签

---

## 三、交互流程图

### 3.1 核心交互流程

```
PMO发起项目
    ↓
Auto-PM接收需求 → AI智能分解任务
    ↓                    ↓
              风险检测？→ 有风险 → 风险预警 → 管理者介入
                    ↓ 无风险
              分配任务到工作站
                    ↓
              工作站：接收任务 → 执行任务 → 提交成果
                    ↓                    ↓
              系统自动审核 ── 不通过 ──┘
                    ↓ 通过
              触发下一环节
                    ↓
              PMO监控进度 → 管理者查看大盘 → 决策优化
                    ↓
              项目完成
```

### 3.2 各角色详细交互

#### 【PMO角色】
1. **输入新项目需求**：点击Auto-PM核心，输入项目名称、目标、截止日期等关键信息
2. **监控项目整体进度**：实时查看所有项目状态，接收系统通知
3. **协调跨部门问题**：处理系统无法自动解决的冲突

#### 【Auto-PM系统角色】
1. **智能任务分解**：AI将大项目分解为可执行的子任务
2. **自动资源分配**：根据工作站当前负载智能分配
3. **能量流形式分发**：视觉上像能量流动一样将任务发送到工作站
4. **实时风险检测**：监控进度偏差、资源冲突、质量问题
5. **自动成果审核**：校验提交物完整性、格式规范
6. **触发下一环节**：任务完成自动启动后续依赖任务

#### 【工作站角色】
1. **任务接收**：工作站变蓝闪烁，提示有新任务待处理
2. **任务执行**：点击接收，状态变为绿色（进行中）
3. **成果提交**：完成后点击"完成"，上传成果文件
4. **系统审核**：系统自动审核，通过则释放资源
5. **状态变化**：
   - ⚪ 灰色：空闲
   - 🔵 蓝色闪烁：有任务待处理
   - 🟢 绿色：任务进行中
   - 🟡 黄色：有风险/延迟
   - 🔴 红色：严重卡顿

#### 【管理者角色】
1. **项目监控大盘**：全局视图，一目了然看到卡点项目
2. **瓶颈分析**：点击卡点项目，查看详细原因、影响范围
3. **资源调配**：查看各部门负载，手动调整资源分配
4. **多维评分查看**：右上角实时显示"多、快、好、省"四维评分（0-5分）

---

## 四、数据模型设计

### 4.1 核心实体关系图

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Project   │1       *│    Task     │*       1│ Workstation │
│  (项目)     │────────▶│  (任务)     │────────▶│  (工作站)    │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ project_id  │         │ task_id     │         │ ws_id       │
│ name        │         │ name        │         │ name        │
│ description │         │ description │         │ department  │
│ status      │         │ status      │         │ status      │
│ start_date  │         │ priority    │         │ load        │
│ end_date    │         │ deadline    │         │ capacity    │
│ progress    │         │ assignee    │         │ skills      │
│ manager_id  │         │ depend_on   │         └─────────────┘
└─────────────┘         │ deliverable │
        │               │ output_file │
        │               └─────────────┘
        │                     │
        │                     │
        ▼                     ▼
┌─────────────┐         ┌─────────────┐
│   User      │         │ Attachment  │
│  (用户)     │         │  (附件)     │
├─────────────┤         ├─────────────┤
│ user_id     │         │ file_id     │
│ name        │         │ task_id     │
│ role        │         │ file_name   │
│ department  │         │ file_path   │
│ email       │         │ upload_time │
└─────────────┘         └─────────────┘
```

### 4.2 详细数据结构

#### 【项目表 (projects)】
```typescript
interface Project {
  project_id: string;           // 项目唯一ID
  name: string;                 // 项目名称
  description: string;          // 项目描述
  category: string;             // 项目分类（家电类型）
  priority: 'high' | 'medium' | 'low';  // 优先级
  
  // 时间维度
  start_date: Date;             // 开始日期
  target_date: Date;            // 目标完成日期
  actual_date?: Date;           // 实际完成日期
  
  // 进度状态
  status: 'planning' | 'executing' | 'delayed' | 'completed' | 'cancelled';
  progress: number;             // 进度百分比 0-100
  
  // 管理者信息
  pm_id: string;                // PMO负责人ID
  manager_id?: string;          // 管理层负责人
  
  // 四维评分
  scores: {
    quantity: number;           // "多" - 任务完成数量 0-5
    speed: number;              // "快" - 进度效率 0-5
    quality: number;            // "好" - 质量达标率 0-5
    saving: number;             // "省" - 成本控制 0-5
  };
  
  // 元数据
  created_at: Date;
  updated_at: Date;
  metadata: Record<string, any>;
}
```

#### 【任务表 (tasks)】
```typescript
interface Task {
  task_id: string;              // 任务唯一ID
  project_id: string;           // 所属项目ID
  workstation_id: string;       // 分配的工作站ID
  
  // 基本信息
  name: string;                 // 任务名称
  description: string;          // 任务描述
  task_type: string;            // 任务类型（设计/开发/测试等）
  
  // 状态与进度
  status: 'pending' | 'assigned' | 'processing' | 'reviewing' | 'completed' | 'delayed' | 'blocked';
  progress: number;             // 任务进度 0-100
  
  // 时间信息
  created_at: Date;             // 创建时间
  assigned_at?: Date;           // 分配时间
  started_at?: Date;            // 开始时间
  deadline: Date;               // 截止时间
  completed_at?: Date;          // 完成时间
  
  // 人员分配
  assignee_id?: string;         // 执行人ID
  reviewer_id?: string;         // 审核人ID
  
  // 依赖关系
  dependencies: string[];       // 前置任务ID列表
  is_milestone: boolean;        // 是否里程碑任务
  
  // 优先级与权重
  priority: 1 | 2 | 3 | 4 | 5;  // 优先级 1-5
  weight: number;               // 任务权重（影响项目进度计算）
  
  // 成果物
  deliverables: string[];       // 要求交付物清单
  attachments: Attachment[];    // 已上传附件
  
  // 风险标记
  risk_level: 'none' | 'low' | 'medium' | 'high' | 'critical';
  risk_reason?: string;         // 风险原因
}
```

#### 【工作站表 (workstations)】
```typescript
interface Workstation {
  workstation_id: string;       // 工作站唯一ID
  name: string;                 // 工作站名称
  department: string;           // 所属部门
  code: string;                 // 部门代码（PD/ID/EE等）
  
  // 状态与负载
  status: 'idle' | 'busy' | 'warning' | 'critical';
  current_load: number;         // 当前负载百分比 0-100
  max_capacity: number;         // 最大并行任务数
  
  // 人员信息
  team_members: string[];       // 团队成员ID列表
  lead_id: string;              // 主管ID
  
  // 能力标签
  skills: string[];             // 能力标签
  specializations: string[];    // 专长领域
  
  // 绩效统计
  avg_completion_time: number;  // 平均完成时间（小时）
  on_time_rate: number;         // 准时完成率
  quality_score: number;        // 质量评分
  
  // 当前任务
  active_tasks: string[];       // 进行中任务ID列表
  pending_tasks: string[];      // 待处理任务ID列表
}
```

#### 【用户表 (users)】
```typescript
interface User {
  user_id: string;              // 用户唯一ID
  name: string;                 // 用户姓名
  email: string;                // 邮箱
  avatar?: string;              // 头像URL
  
  // 角色权限
  role: 'admin' | 'pmo' | 'manager' | 'workstation_lead' | 'team_member';
  permissions: string[];        // 权限列表
  
  // 所属部门
  workstation_id?: string;      // 所属工作站
  department: string;           // 部门
  
  // 工作能力
  skills: string[];             // 技能标签
  current_task_count: number;   // 当前任务数
  max_task_capacity: number;    // 最大任务承载
  
  // 绩效数据
  performance_score: number;    // 绩效评分
  task_completion_rate: number; // 任务完成率
}
```

#### 【附件表 (attachments)】
```typescript
interface Attachment {
  attachment_id: string;        // 附件唯一ID
  task_id: string;              // 关联任务ID
  project_id: string;           // 关联项目ID
  
  // 文件信息
  file_name: string;            // 文件名
  file_type: string;            // 文件类型
  file_size: number;            // 文件大小（字节）
  file_path: string;            // 存储路径
  
  // 上传信息
  uploaded_by: string;          // 上传人ID
  uploaded_at: Date;            // 上传时间
  version: string;              // 版本号
  
  // 审核状态
  review_status: 'pending' | 'approved' | 'rejected';
  reviewed_by?: string;         // 审核人
  reviewed_at?: Date;           // 审核时间
  review_comment?: string;      // 审核意见
}
```

#### 【事件日志表 (event_logs)】
```typescript
interface EventLog {
  log_id: string;               // 日志ID
  event_type: string;           // 事件类型（任务创建/状态变更/风险预警等）
  project_id?: string;          // 关联项目
  task_id?: string;             // 关联任务
  
  // 变更详情
  description: string;          // 事件描述
  old_value?: any;              // 旧值
  new_value?: any;              // 新值
  
  // 操作人
  triggered_by: string;         // 触发人（系统/用户ID）
  triggered_at: Date;           // 触发时间
  
  // 重要级别
  severity: 'info' | 'warning' | 'error' | 'critical';
}
```

---

## 五、技术选型建议

### 5.1 整体技术栈

| 层级 | 技术选型 | 选型理由 |
|-----|---------|---------|
| **前端框架** | React 18 + TypeScript | 组件化开发，类型安全，生态完善 |
| **状态管理** | Zustand + React Query | 轻量高效，服务端状态与客户端状态分离 |
| **UI组件库** | Ant Design 5.x | 企业级组件，开箱即用，支持主题定制 |
| **动画引擎** | Framer Motion + GSAP | 流畅的任务流转动画、能量流动效果 |
| **图形可视化** | D3.js + React Flow | 自定义节点连线、任务流可视化 |
| **3D效果** | Three.js (可选) | 核心发光效果、沉浸式体验 |
| **后端框架** | Node.js + NestJS | TypeScript全栈，模块化架构，支持微服务 |
| **数据库** | PostgreSQL + Redis | 关系型数据+缓存，支持复杂查询与高性能 |
| **AI引擎** | Python + FastAPI + LangChain | AI任务分解、风险预测模型 |
| **实时通信** | Socket.io | 任务状态实时同步、消息推送 |
| **文件存储** | MinIO / AWS S3 | 分布式文件存储，支持大文件上传 |

### 5.2 前端技术详解

#### 【核心视觉效果实现】
1. **发光圆形核心按钮**
   - 使用CSS `box-shadow` + `filter: blur()` 创建光晕效果
   - 配合CSS动画实现呼吸灯效果
   - 鼠标悬停时增强发光效果

2. **能量流任务动画**
   - 使用SVG路径动画或Canvas绘制流动线条
   - Framer Motion实现节点状态过渡
   - 粒子效果增强能量流动感

3. **工作站状态变化**
   - 蓝色闪烁：CSS `@keyframes` 呼吸动画
   - 状态切换：平滑过渡动画 + 颜色渐变
   - 风险标记：脉冲动画 + 警告图标

#### 【页面结构设计】
```
src/
├── pages/
│   ├── Dashboard.tsx          # 项目监控大盘
│   ├── CoreHub.tsx            # Auto-PM核心交互页
│   ├── Workstation.tsx        # 单个工作站详情
│   ├── ProjectDetail.tsx      # 项目详情页
│   └── ManagerView.tsx        # 管理者视角
├── components/
│   ├── AutoPMCore/            # Auto-PM核心组件（发光圆形）
│   ├── WorkstationNode/       # 工作站节点组件
│   ├── TaskFlow/              # 任务流连线动画
│   ├── StatusBadge/           # 状态标记组件
│   ├── ScoreCard/             # 四维评分卡片
│   └── RiskAlert/             # 风险预警弹窗
├── hooks/
│   ├── useProjectStore.ts     # 项目状态管理
│   ├── useTaskFlow.ts         # 任务流逻辑
│   └── useRealtimeSync.ts     # 实时同步hook
└── styles/
    ├── theme.ts               # 深蓝主题配置
    └── animations.css         # 统一定义动画
```

### 5.3 后端架构设计

#### 【微服务划分】
```
Auto-PM System
┌─────────────────────────────────────────────────────┐
│                    API Gateway                       │
│                (Nginx / Kong)                        │
└─────────────┬───────────────────┬───────────────────┘
              │                   │
┌─────────────▼───────┐  ┌────────▼─────────┐  ┌───────────────┐
│  Project Service    │  │   Task Service   │  │  AI Engine    │
│  (项目管理)         │  │   (任务调度)     │  │  (智能分析)   │
└─────────────────────┘  └──────────────────┘  └───────────────┘
              │                   │                   │
┌─────────────▼───────┐  ┌────────▼─────────┐  ┌───────────────┐
│ Workstation Service │  │ Notification Svc │  │ File Service  │
│  (工作站管理)        │  │   (消息通知)     │  │  (文件存储)    │
└─────────────────────┘  └──────────────────┘  └───────────────┘
```

#### 【关键技术点】
1. **任务分配算法**
   - 基于规则的初始分配
   - 机器学习优化分配策略
   - 实时负载均衡调整

2. **风险预警引擎**
   - 进度偏差检测
   - 资源冲突识别
   - 历史数据模式匹配

3. **实时同步机制**
   - Socket.io双向通信
   - 消息队列异步处理
   - 最终一致性保证

### 5.4 数据库设计优化

#### 【PostgreSQL 表优化】
- 使用分区表按项目/时间分片
- 关键字段建立索引（status, workstation_id, deadline）
- JSONB存储灵活扩展字段

#### 【Redis 缓存策略】
- 热点数据缓存（活跃项目、工作站状态）
- 实时排行榜（项目进度、部门负载）
- 发布订阅机制（状态变更通知）

### 5.5 部署与运维

#### 【容器化部署】
```yaml
# docker-compose.yml 概览
services:
  frontend:         # React前端
  backend-api:      # NestJS API服务
  ai-engine:        # Python AI服务
  postgres:         # 主数据库
  redis:            # 缓存/消息
  minio:            # 文件存储
  nginx:            # 反向代理
```

#### 【监控与告警】
- **系统监控**：Prometheus + Grafana
- **日志收集**：ELK Stack
- **性能追踪**：OpenTelemetry
- **业务告警**：自定义规则引擎（项目延迟、资源过载）

---

## 六、视觉设计规范

### 6.1 色彩系统（深邃科技蓝主题）

| 用途 | 色值 | 说明 |
|-----|-----|-----|
| **主背景** | `#0a1628` | 深邃蓝黑背景 |
| **卡片背景** | `#132238` | 半透明卡片 |
| **核心蓝色** | `#00d4ff` | Auto-PM核心发光色 |
| **高亮蓝色** | `#0099cc` | 按钮、链接 |
| **状态-空闲** | `#6b7280` | 灰色，工作站空闲 |
| **状态-待处理** | `#3b82f6` | 蓝色闪烁，新任务 |
| **状态-进行中** | `#10b981` | 绿色，正常执行 |
| **状态-有风险** | `#f59e0b` | 黄色，延迟警告 |
| **状态-严重** | `#ef4444` | 红色，卡顿阻塞 |
| **文字-主要** | `#f1f5f9` | 白色标题 |
| **文字-次要** | `#94a3b8` | 灰色正文 |

### 6.2 发光效果规范

```css
/* Auto-PM核心发光效果 */
.autopm-core {
  box-shadow: 
    0 0 20px rgba(0, 212, 255, 0.5),
    0 0 40px rgba(0, 212, 255, 0.3),
    0 0 60px rgba(0, 212, 255, 0.2),
    inset 0 0 20px rgba(0, 212, 255, 0.3);
  animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.5), ... }
  50% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.7), ... }
}
```

### 6.3 交互反馈标准

| 交互 | 反馈效果 |
|-----|---------|
| 悬停 | 光晕增强 + 轻微放大（scale: 1.05） |
| 点击 | 涟漪效果 + 按压反馈 |
| 状态变更 | 颜色渐变过渡（300ms ease） |
| 任务到达 | 蓝色脉冲动画 + 轻微震动 |
| 风险预警 | 黄色闪烁 + 声音提示（可选） |

---

## 七、实施路线图

### Phase 1: MVP版本（1-2个月）
- ✅ 核心架构搭建
- ⏳ 基础项目CRUD
- ⏳ 工作站状态展示
- ⏳ 简单任务分配流程

### Phase 2: AI增强（2-3个月）
- ⏳ 智能任务分解
- ⏳ 自动资源分配
- ⏳ 基础风险检测
- ⏳ 能量流动画效果

### Phase 3: 完整功能（3-4个月）
- ⏳ 12个工作站完整接入
- ⏳ 项目监控大盘
- ⏳ 管理者视角与分析
- ⏳ 四维评分系统

### Phase 4: 优化迭代（持续）
- ⏳ 性能优化与扩展
- ⏳ AI模型持续训练
- ⏳ 用户体验优化
- ⏳ 移动端适配

---

## 附录：文件清单

1. `AutoPM_系统架构图.drawio` - 系统整体架构图
2. `AutoPM_交互流程图.drawio` - 详细交互泳道图
3. 本文档 - 完整架构设计说明

---

**版本**：v1.0  
**最后更新**：2024年  
**设计者**：Auto-PM Architecture Team