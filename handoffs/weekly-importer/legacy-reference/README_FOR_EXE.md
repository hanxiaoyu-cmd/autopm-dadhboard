# AutoPM · 项目同步工作台 - Windows 可执行版

## 这是什么？

一个独立的 Windows 图形界面程序，把 Excel 周报（ALL Tracker）的进度内容同步写入 Airtable **Projects** 表的 Engineering remark 字段。

**无需安装 Python**，双击 `weekly_importer_gui.exe` 即可使用。

---

## 快速开始

### 1. 启动程序

双击 `weekly_importer_gui.exe`，进入「AutoPM · 项目同步工作台」。

### 2. 配置连接（只需一次）

点击左侧导航「**连接设置**」：

1. 粘贴你的 Airtable **完整 Token**（`pat...` 开头）；
2. 点击「**检测并选择数据库**」；
3. 程序自动列出可用数据库并识别 Projects 表，底部显示「已连接：… → Projects 表」。

> 你只需要提供 Token。**Base ID、表 ID 会自动检测，无需填写、无需了解。**
> Token 只保存在本次运行的会话内存中，不写入磁盘。

如何获取 Token：https://airtable.com/create/tokens
（勾选 `data.records:read` 与 `data.records:write` 权限即可）

### 3. 选择周报并导入

点击左侧导航「**周报导入**」：

1. 点击「选择文件」，默认打开 `AutoPM_Source_20260915` 目录（也可在「本地文件」页扫描历史周报，双击直接使用）；
2. 点击「**规则检查 · 预览变更**」先查看将写入的内容（不会改任何数据）；
3. 确认无误后点击「**写入 Airtable**」，在确认框中点击确认后执行。

---

## 界面说明

| 区域 | 功能 |
|------|------|
| 左侧导航 | 周报导入 / 本地文件 / 连接设置 / 本地总表 |
| 顶部状态标签 | 显示 Airtable 连接状态（待配置 / 已连接） |
| 周报导入页 | 四步流程指示 + 选择周报 + 预览/写入 + 运行日志 |
| 连接设置页 | 只填 Token，自动检测数据库和表 |
| 本地文件页 | 扫描默认目录中的 Excel 周报，双击即可使用 |

---

## Excel 格式预期（标准 ALL Tracker）

| 列 | 表头 | 内容 |
|----|------|------|
| 项目列 | `Project Name , Description` | 项目名（需与 Airtable 匹配） |
| 进度列 | `Engineering Remarks` | 周报进度文本（自动按表头匹配） |
| 日期列 | `Date Added` | 报告日期（YYYY-MM-DD） |

列头自动识别；日期无效或缺失的行会跳过，不中断整个导入。

---

## 命令行模式（可选）

带参数运行时仍走命令行接口：

| 命令 | 作用 |
|------|------|
| `weekly_importer_gui.exe --help` | 显示命令行帮助 |
| `weekly_importer_gui.exe --init-config` | 生成配置文件模板 |
| `weekly_importer_gui.exe --excel "file.xlsx" --dry-run` | 预览不写入 |
| `weekly_importer_gui.exe --excel "file.xlsx"` | 执行导入 |
| `weekly_importer_gui.exe --clean` | 清理旧 AutoPM 格式备注 |

---

## 故障排查

- **提示缺少 Token**：到「连接设置」页粘贴完整 Token 并点击检测。
- **检测不到数据库**：确认 Token 权限包含读取记录；检查网络。
- **项目未匹配**：Excel 项目名需与 Airtable `Project name (Manual)` 一致（忽略大小写与首尾空格）。
- **网络错误**：程序自动重试 3 次，仍失败会在日志区显示原因。

---

## 功能特性

- **只填 Token**：Base 与表 ID 自动检测，用户无需知道表 ID
- **Delta 更新**：内容无变化时不写入
- **本地解析**：无需 DeepSeek 等外部 AI Key
- **预览先行**：写入前可核对变更
- **批量处理**：支持数千行记录
- **断点重试**：网络异常自动重试

---

## 版本

v1.1.0 - 2026-09-19（工作台界面重写，Token 自动检测）