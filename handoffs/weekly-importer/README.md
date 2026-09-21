# AutoPM 周报导入工具开发交接包

本目录用于把周报导入工具完整移交给下一位开发者。它说明工具为什么存在、当前做到哪里、实际匹配规则、业务规则与代码现状的差距，以及下一步应按什么顺序继续开发。

## 一句话目标

把 APAC Shark / Ninja 周报中的项目级信息安全导入 Airtable，再由 Airtable 生成和更新本地 All Tracker；All Tracker 回写 Airtable 只用于复验、补漏和经过人工审核的修正。

主链路：

```text
周报 Excel -> 解析和预览 -> Airtable -> All Tracker Excel 副本
                                      <- 人工审核后的有限回写
```

## 当前状态

- 当前源码版本：`2.4.0-rc5`，版本真源见 [`source/autopm/__init__.py`](source/autopm/__init__.py)。
- 已实现桌面界面、周报解析、Airtable schema 核对、写入预览、受保护写入、Airtable 到 All Tracker 导出、All Tracker 有基线的受控回写。
- 已修复企业代理证书信任、新电脑缺省映射、富文本列表编号回读误报及重复追加等问题。
- 2026-09-21 修复后的完整测试为 435 项通过；验证范围见 [`CHANGELOG.md`](CHANGELOG.md) 和 [`docs/05-完成情况测试与已知问题.md`](docs/05-完成情况测试与已知问题.md)。
- 当前代码仍把“正式编号 + SKU + 工厂”作为 Airtable 项目记录的严格身份。业务最终原则要求周报内容按 Project 管理，SKU 维度从 Airtable 开始，因此这部分仍需重构，不能把现状当成最终业务验收。
- rc5 已修复 All Tracker 的 Excel 时间／时长导致预览 JSON 失败；日期列异常值会报告具体坐标，未更新单元格保持原样。本次只交付源码。

## 建议阅读顺序

1. [`docs/01-目标与业务原则.md`](docs/01-目标与业务原则.md)
2. [`docs/02-数据流与匹配规则.md`](docs/02-数据流与匹配规则.md)
3. [`docs/03-字段映射与分表规则.md`](docs/03-字段映射与分表规则.md)
4. [`docs/04-架构运行与安全.md`](docs/04-架构运行与安全.md)
5. [`docs/05-完成情况测试与已知问题.md`](docs/05-完成情况测试与已知问题.md)
6. [`docs/06-接手开发顺序.md`](docs/06-接手开发顺序.md)
7. [`docs/07-资料来源与目录说明.md`](docs/07-资料来源与目录说明.md)

## 目录

| 目录 | 内容 | 使用原则 |
|---|---|---|
| `source/` | 当前可运行桌面工具、测试、构建配置、浏览器授权助手 | 当前开发基线 |
| `docs/` | 本次整理的业务、匹配、架构、测试和接手说明 | 先读这里 |
| `docs/reference/` | 历次修复、审计、All Tracker 方案和验证记录 | 作为证据和历史，不自动覆盖最新规则 |
| `legacy-reference/` | 早期独立 `weekly_importer` 实现 | 只供追溯，不作为当前入口 |

## 本地启动

在 `source/` 中运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\start.ps1
```

首次启动会创建 `.venv` 并安装 `requirements.txt`。Airtable Token 和 DeepSeek Key 只保存在本机设置或环境变量中，不在本仓库。

## 交接边界

本包没有包含：真实 Token/API Key、DPAPI 加密设置、`.venv`、运行日志、Airtable 记录快照、真实周报、真实 All Tracker、生成的 EXE、构建缓存及包含项目数据的 CSV/HTML 审核产物。

任何接手者都应先在本地预览和测试数据上验证，再处理正式数据。删除、合并、覆盖冲突或扩大同步范围必须单独审核。
