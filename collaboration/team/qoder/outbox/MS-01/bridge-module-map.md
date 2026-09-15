# MS-01 Bridge Module Map

版本：attempt 1｜执行者：Qoder｜日期：2026-09-16 Asia/Shanghai
基线提交：c747374474e9 (codex/autopm-management-20260914)

## 概述

本文档比较 `legacy_bridge/` 和 `candidate_bridge/` 的模块结构差异。

## 文件对照

| 文件 | legacy_bridge | candidate_bridge | 差异说明 |
|------|:---:|:---:|------|
| bridge.py | ✅ (70561b, 1058行) | ✅ (67266b, 1016行) | 3个关键差异区域（见下） |
| test_bridge.py | ✅ (13112b) | ✅ (13298b) | 新增日期范围和绿色完成测试 |
| verified_writer.py | ❌ 不存在 | ✅ (10690b) | 新增安全写入模块 |
| test_verified_writer.py | ❌ 不存在 | ✅ (5948b) | 12项安全写入测试 |

## bridge.py 差异详情

### 差异 1：日期处理（BR-07，行 728-740）

**Legacy**：单日期字段 + 硬编码 7 天偏移
```python
start_date = entry['date']
days = 0 if milestone in ('Award', 'MP Start') else 7
due_date = (dt.date.fromisoformat(start_date) + dt.timedelta(days=days)).isoformat()
```

**Candidate**：显式 start_date/due_date 映射，无默认 7 天
```python
start_date = entry.get('start_date')
due_date = entry.get('due_date')
if not (start_date and due_date):
    if milestone or entry.get('date_role') == 'single_day':
        start_date = due_date = entry.get('date')
    else:
        skipped.append({...})  # 跳过而非猜测
```

### 差异 2：绿色完成处理（行 740-768）

**Legacy**：绿色自动设置 completed_by = owners
```python
if entry.get('green') and default_owners:
    fields[TASK_FIELDS['completed_by']] = default_owners
```

**Candidate**：绿色记录为 reported_completion，需人工确认
```python
if entry.get('green'):
    reported_completion.append({
        'pid': key, 'task_name': task_name,
        'claim': 'source_reported_complete',
        'requires_confirmation': True
    })
```

### 差异 3：apply_airtable() 委托（行 774-815）

**Legacy**：~40 行内联写入逻辑（批量 PATCH/POST + 读回验证）
```python
def apply_airtable(plan, api, journal, progress=None):
    # 内联批量写入、读回验证、journal 管理
```

**Candidate**：3 行委托给 verified_writer
```python
def apply_airtable(plan, api, journal, progress=None):
    from verified_writer import apply_reviewed_plan
    return apply_reviewed_plan(plan, api, journal, progress)
```

### 差异 4：rule_version 字段（行 770）

**Legacy**：无版本标记
**Candidate**：输出包含 `rule_version: 'BR-2026-09-11'`

## verified_writer.py 模块结构（仅 candidate）

| 组件 | 职责 |
|------|------|
| `_save(path, value)` | 原子写入（tempfile + fsync + replace） |
| `_lock(path)` | 单写者互斥锁（tempdir + O_EXCL） |
| `_equal(left, right)` | Airtable 字段等价比较（空值/列表排序） |
| `_matches(record, fields)` | 记录身份匹配 |
| `ReconciliationRequired` | 冲突/未知结果异常 |
| `apply_reviewed_plan(plan, api, journal, progress)` | 核心写入函数 |

### apply_reviewed_plan 安全机制

1. **Plan 验证**：kind/base/table/source_sha256 校验
2. **身份去重**：create 操作需 reviewed identity，重复身份拒绝
3. **Schema 校验**：目标字段和类型变更检测
4. **Before-image**：更新前记录原始值
5. **Pre-write re-read**：PATCH 前重新读取检测并发修改
6. **Post-write readback**：写入后独立读回验证
7. **Journal 持久化**：每步保存状态，支持断点恢复
8. **Uncertain POST 不重试**：创建超时不自动重试 POST
9. **Immutable receipt**：verified 状态不可覆盖

## preparation/ 模块（两版本共享）

| 文件 | 职责 |
|------|------|
| tools/prepare_migration.py | 迁移准备工具（解析/映射/计划生成） |
| tests/test_migration.py | 8 项合成测试（迁移逻辑回归） |
| functional-parity.csv | 12 项功能对照表（F01-F12） |

## 测试统计

| 测试组 | legacy | candidate | 差异 |
|--------|--------|-----------|------|
| test_bridge.py | 12 tests | 12 tests | 相同用例，candidate 版本有额外覆盖 |
| test_verified_writer.py | N/A | 12 tests | 新增 |
| test_migration.py | 8 tests | 8 tests | 相同 |
| **合计** | **20** | **32** | candidate +12 verified_writer 测试 |
| **全部通过** | ✅ | ✅ | 44/44 离线合成数据 |
