# MS-01 Adapter Contract (Target-Neutral)

版本：attempt 1｜执行者：Qoder｜日期：2026-09-16 Asia/Shanghai

## 概述

定义 Airtable/Dataverse 适配器共同遵守的写入契约。复用 verified_writer 的安全写入思想，但解耦具体平台实现。本契约为 target-neutral，不绑定 Airtable 或 Dataverse。

## 核心原则（源自 verified_writer）

1. **Plan-first**：所有写入必须基于已审核的变更计划（reviewed plan）
2. **Identity-based**：创建操作必须有可验证的身份标识（identity），不靠猜测去重
3. **Read-back verify**：每次写入后必须独立读回验证，不信任写入响应
4. **No blind retry**：不确定的 POST 永不自动重试（防止重复创建）
5. **Atomic journal**：每步操作后持久化 journal，支持断点恢复
6. **Single writer**：同一时刻只有一个写入者（通过锁机制）
7. **Immutable receipt**：verified 状态的 journal 不可被后续操作覆盖

## 适配器接口

```python
class AdapterContract(Protocol):
    """Target-neutral adapter interface."""

    @property
    def base(self) -> str:
        """Base/environment identifier."""

    @property
    def table(self) -> str:
        """Primary table identifier."""

    def schema(self) -> dict:
        """Return table/field/type metadata."""

    def records(self, table: str) -> list[dict]:
        """Return all records for a table."""

    def request(self, url: str, method: str = "GET", body: dict = None) -> dict:
        """Execute an API request."""
```

## 写入流程

```
reviewed_plan → validate → lock → load_journal → reconcile
    → for each operation:
        → if update: pre_read → compare_old → write → readback → verify
        → if create: check_identity → check_duplicate → write → readback → verify
    → save_receipt → unlock
```

## Journal 结构

```json
{
    "journal_version": 2,
    "plan_sha256": "...",
    "status": "started|verified|needs_reconciliation",
    "before": [...],
    "operations": [
        {
            "op": "update|create",
            "table": "...",
            "record": "...",
            "pid": "...",
            "fields": {...},
            "old": {...},
            "status": "planned|sent|verified",
            "key": "table:op:index"
        }
    ],
    "confirmed": [...],
    "created": [...],
    "pending": [...]
}
```

## 错误处理

| 场景 | 行为 | 理由 |
|------|------|------|
| Plan SHA 不匹配 | 拒绝执行 | 源数据已变更 |
| Schema 变更 | 拒绝执行 | 目标结构已变 |
| 并发修改（pre-read 检测到 old 值已变） | 拒绝执行 | 他人已修改 |
| 创建超时（POST 无响应） | 标记 needs_reconciliation | 不盲目重试 |
| 读回不匹配 | 抛出 ReconciliationRequired | 写入未生效 |
| Journal 属于其他 plan | 拒绝覆盖 | 保护已有结果 |
| 已 verified 的 journal | 直接返回 | immutable receipt |

## Airtable 适配器特有约束

- 无 compare-and-swap：依赖 read-back 检测冲突
- Linked record 无序：_equal() 排序比较
- 空字段省略：None/''/[] 视为等价
- typecast 参数：tasks 表需 typecast=True

## Dataverse 适配器特有约束（未实现，待环境就绪）

- 需确认：是否有唯一键约束支持
- 需确认：是否有乐观并发控制（ETag/RowVersion）
- 需确认：批量操作 API 和限制
- 需确认：Connection Reference 配置方式
- 所有 Dataverse 特定项标记为 **Not Implemented**，待 MS-00 环境就绪后补充

## 离线验证覆盖

| TC | 覆盖的契约条款 | 测试状态 |
|----|--------------|---------|
| TC-04 | Plan 日期映射规则（BR-07） | 离线 Pass（合成数据） |
| TC-15 | 身份匹配 + SourceRecordMap 首次固化 | 离线 Pass（合成数据） |
| TC-16 | 旧来源不覆盖新值 + 版本冲突检测 | 离线 Pass（合成数据） |
| TC-17 | 部分失败 + 超时处理 + journal 恢复 | 离线 Pass（合成数据） |
| TC-18 | 绿色完成记录而非伪造 | 离线 Pass（合成数据） |
| TC-19 | Tracker XLSX 无损更新 | 离线 Pass（合成数据） |
| TC-30 | 相同输入两适配器计划一致 | 离线 Pass（合成数据） |

## 部署待办

- [ ] Dataverse 适配器实现（依赖 MS-00 环境）
- [ ] Connection Reference 配置
- [ ] 服务身份/凭据托管
- [ ] 端到端集成测试（需要真实环境）
- [ ] Codex 裁决 RC-01/RC-02/RC-03 后固化规则版本
