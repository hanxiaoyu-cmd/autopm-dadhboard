# 新 Program 补齐市场：待部署

脚本已完成；2026-09-14 九类离线测试通过。尚未在 Airtable Automation 运行或启用，不代表平台端验收通过。

## 接入步骤

1. 在 AutoPM V2 (Pilot) 检查是否已有同用途自动化，只保留一个写入入口。
2. 创建自动化 `Program Markets — Ensure five markets`。触发器：PMO Roadmap Programs 新建记录。
3. Run a script 动作，添加输入变量 `programRecordId`，绑定触发记录的 Airtable record ID，不绑定 Program 名称或业务代码。
4. 粘贴 `ensure-program-markets.js`。不需要 PAT、邮箱或外部服务。
5. 使用隔离测试 Program 验证：第一次生成 US/CA/MX/UK/EU；同 ID 重跑 createdCount=0；只保留部分市场后重跑只补缺。测试记录清理按正常可恢复方式处理。
6. 检查五行日期继承、市场排序、Interface 显示，确认后启用唯一的自动化。

## 规则与边界

- 2026-09-14 接口核对：Market 是文本；Program 是关联 PMO Roadmap Programs 的多记录关联字段。脚本写入单一 Program，并拒绝发现的多 Program 行。
- 只读取当前 Program 的反向关联记录，不逐个扫描所有 Program。
- 有重复市场、未知市场、异常关联时停止，不自动删行或纠正业务数据。
- 日期、Lookup、公式均不写入；原 Program 日期继续是维护位置。
- 新行同时写入 Market Order（US=1 至 EU=5）和 Program Market Key（Program record ID + `|` + Market）。已核对两列实际为数字/文本，沿用现有记录格式。
- 同一个 Program 顺序重试不重复生成。Airtable 无原子组合唯一约束，本脚本不保证两个并发运行的绝对唯一性；不要建立第二套同用途触发器，人工重试要等当前运行结束。读回发现重复会报错，需要人工对账。
- 部分写入抛错时不要判断为“全部失败”。等待结束后对同一 Program 重试，脚本会重新读取再补缺。
- 现有 152 个 Program 的市场行已经建立，不需要全量重新生成。

## 离线验收

运行 `test-ensure-program-markets.cjs`。

覆盖：空集合、顺序重试、部分市场、重复市场、未知市场、Program 不存在、输入非法、多 Program 关联、部分写入后恢复。
测试使用模拟 Airtable API；实际 API 可用性、触发器输入、Lookup 更新时序和权限必须在线补验。
