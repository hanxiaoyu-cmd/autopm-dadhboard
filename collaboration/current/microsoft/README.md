# Power Apps 复刻：最小可运行输入包

主任务仓库为 autopm-dadhboard；backup 仅为历史资料来源，不领取任务、不写进度。
此包是源码快照和离线测试基线，不证明线上 Airtable 规则正确或 Dataverse 已部署。

## 阅读顺序

1. [正式启动任务书](../../planning/dispatch/START_MICROSOFT.md)与原 Issue。
2. [历史字段：Projects](../../planning/sources/projects-fields.md)、[其他表](../../planning/sources/other-core-fields.md)、[历史能力矩阵](../../planning/sources/capability-matrix-source.md)。字段快照需线上核对。
3. [既有 Bridge 说明](../../planning/sources/bridge-handover.md)、[候选代码审核](../../planning/reviews/RV-20260911-001.md)、[验收用例](../../planning/acceptance/TEST_CATALOG.md)。
4. 本包源码、测试、[文件指纹](source-manifest.json)和[测试记录](baseline-checks.json)。

## 输入与规则边界

- `legacy_bridge/`：本地既有 Bridge 原字节副本，含解析、Airtable 写入和 Tracker 输出；允许离线测试，禁止调用生产写入。
- `candidate_bridge/`：未验收候选 Bridge 与 verified_writer，需比较差异后选择复用，不覆盖 legacy 基线。
- `preparation/`：已有迁移准备工具、8项合成测试、历史12组功能对照；对照表不是完整线上盘点。
- 测试在临时目录生成合成工作簿/模拟记录；未上传真实周报、人员导出、凭据或配置。
- 保留现有 Task 完成机制，暂停项目进度改造。legacy 与候选代码中的绿色完成、日期推算等规则须登记冲突；旧测试通过不等于新业务规则获批。
- 旧 domain.py 含暂停的 Task 完成/项目进度改造，故不作为本轮可执行输入。需要纯函数时逐项证明不改变已确认行为，再由 Codex 审核。

## 可复现检查（Python 标准库）

从本目录运行，每组使用独立进程：
```text
python -m unittest discover -s legacy_bridge -p "test_*.py" -v
python -m unittest discover -s candidate_bridge -p "test_*.py" -v
python -m unittest discover -s preparation/tests -p "test_*.py" -v
```

禁止调用 Airtable 客户端进行实际请求；测试应使用模拟 API。缺失的真实样本、线上触发配置、Dataverse 环境和权限见 [依赖登记](../../../docs/DEPENDENCIES.md)。
