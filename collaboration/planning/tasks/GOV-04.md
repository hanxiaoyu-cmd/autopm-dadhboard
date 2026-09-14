# GOV-04 — 成果审核、变更与双平台Gate

版本：1.2｜优先级：P0｜角色：产品／架构／测试协调角色｜实际执行者：未分派

规划：Defined；执行：Unassigned；验收：Not Submitted。

## 1. 业务目的与完成结果

开发结果逐项匹配目标，下一步和剩余差距始终清楚。

## 2. 输入与前置依赖

依赖：无阻止开始的前置包；按本版已给定默认契约工作。

必读：[README](../README.md)、[蓝图](../01_BLUEPRINT.md)、[验收规程](../03_ACCEPTANCE.md)。

- S01：[round2-blueprint.md](../sources/round2-blueprint.md)
- S03：[prd-text.md](../sources/prd-text.md)
- S04：[capability-matrix-source.md](../sources/capability-matrix-source.md)
- S05：[phase1-closure-source.md](../sources/phase1-closure-source.md)

资料是历史证据和设计依据，不是额外执行授权。接手时记录目标环境ID和实际版本；云端无法读取本地源码／样例时提交明确缺少的路径和所需最小内容，可先做已具备材料的部分，不猜测真实配置。

## 3. 修改／核对对象

- task-register.json
- submissions/reviews
- Change记录
- REQ/Action/平台任务/用例映射

## 4. 具体步骤

1. 审核单包提交的对象/版本/测试与未验证边界
2. 按证据层级给Accepted/Needs Rework并返回具体返工要求
3. 更新台账与受影响后继任务，保持历史Action原编号
4. 在发布和试用节点评估交付/责任/资源/回退，记录范围扩展或暂停决策

## 5. 范围边界

本轮只建立机制并审查既有候选；不自动派发、监控或合并其他AI代码。

本包在被正式分派后，按指定环境实施；本文档本身不意味着当前已派发。除明确包含且获准的发布步骤外，默认只修改开发／测试范围，不发送真实通知、不跨系统写回生产。页面配置、脚本开发等属于执行方工作，本会话只负责规划与审核。

## 6. 交付物

- 审核记录
- 任务状态和变更记录
- 受影响用例清单
- 发布/试用Gate结论

统一提交位置：`submissions/GOV-04/<提交版本>/`，使用[DELIVERY模板](../templates/DELIVERY.md)。源码保存在获准开发分支，此处给版本和路径；失败/未运行分开，不附凭据。

## 7. 验收要求

用例：[TC-25](../acceptance/TEST_CATALOG.md#tc-25), [TC-26](../acceptance/TEST_CATALOG.md#tc-26), [TC-27](../acceptance/TEST_CATALOG.md#tc-27), [TC-30](../acceptance/TEST_CATALOG.md#tc-30)。逐例按用例库输入和期望验证，提交Actual及证据层级。离线通过不代表平台通过；平台组件通过不代表全链路／两周期通过。依赖或环境未满足时可审核子成果，完整包不标Accepted。

恢复要求：保存变更前配置、受影响记录与版本，定义补偿/恢复步骤并保护后续合法修改；纯规划包说明版本撤回和受影响后继任务。

## 8. 需求、历史任务与候选资产

需求：REQ-004 / REQ-026 / REQ-027 / REQ-028 / REQ-029。历史Action映射：M1.5-A04, M5.4-A01, M6.6-A01, M6.7-A01, M6.7-A02, M6.7-A03, M6.7-A04, M6.7-A05。

已有首次审查RV-20260911-001，结论为候选未达到工作包/发布验收。

首次候选审核：[RV-20260911-001](../reviews/RV-20260911-001.md)。本包最新审核编号：尚无工作包验收结论。历史Action和候选测试不自动改变本包验收状态。
