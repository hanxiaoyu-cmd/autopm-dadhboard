# 135个历史Action的完整去向

版本：v1.1。保留原Action ID、来源行、动作、产出和验收。映射是当前规划判断，未证明实际完成。原始Owner/日期/状态完整保存在CSV/JSON，不能直接继承为当前安排。

42能力包、135动作；原文[Phase1逐单元格转换](../sources/phase1-closure-source.md)。当前任务状态以[主台账](../task-register.json)为准。


## M1.1 — 业务对象定义

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M1.1-A01<br>Task Execution!F8 | 定义项目结构对象 | 产出：对象清单、定义及系统归属表<br>验收：对象定义唯一清晰，边界和系统归属明确 | 进行中 | REQ-001, REQ-002<br>[AT-00](../tasks/AT-00.md)、[AT-03](../tasks/AT-03.md)、[MS-02](../tasks/MS-02.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.1-A02<br>Task Execution!F9 | 定义计划执行对象 | 产出：对象清单、定义及系统归属表<br>验收：对象定义唯一清晰，边界和系统归属明确 | 未开始 | REQ-001, REQ-008, REQ-009<br>[AT-04](../tasks/AT-04.md)、[MS-02](../tasks/MS-02.md)、[MS-05](../tasks/MS-05.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.1-A03<br>Task Execution!F10 | 定义异常对象 | 产出：对象清单、定义及系统归属表<br>验收：对象定义唯一清晰，边界和系统归属明确 | 未开始 | REQ-001, REQ-012, REQ-013<br>[AT-05](../tasks/AT-05.md)、[MS-02](../tasks/MS-02.md)、[MS-07](../tasks/MS-07.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.1-A04<br>Task Execution!F11 | 定义恢复与决策对象 | 产出：对象清单、定义及系统归属表<br>验收：对象定义唯一清晰，边界和系统归属明确 | 未开始 | REQ-001, REQ-013, REQ-014<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md)、[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md)、[GOV-01](../tasks/GOV-01.md) | P0/P1分层：恢复对象P0由Tasks类型承载；独立Decision模型P1评估，不据本Action创建重复行动库。 |
| M1.1-A05<br>Task Execution!F12 | 定义组织责任对象 | 产出：对象清单、定义及系统归属表<br>验收：对象定义唯一清晰，边界和系统归属明确 | 未开始 | REQ-001, REQ-002, REQ-026<br>[AT-02](../tasks/AT-02.md)、[MS-02](../tasks/MS-02.md)、[MS-07](../tasks/MS-07.md)、[GOV-01](../tasks/GOV-01.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.1-A06<br>Task Execution!F13 | 确认对象系统归属 | 产出：对象清单、定义及系统归属表<br>验收：对象定义唯一清晰，边界和系统归属明确 | 进行中 | REQ-002, REQ-003, REQ-029<br>[AT-03](../tasks/AT-03.md)、[MS-02](../tasks/MS-02.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M1.2 — 对象关系模型

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M1.2-A01<br>Task Execution!F14 | 建立项目层级、计划、责任、异常和恢复结果关系 | 产出：业务对象关系图及关系规则<br>验收：任务、异常和行动可追溯，汇总可下钻，无孤立核心记录 | 未开始 | REQ-001, REQ-008, REQ-013, REQ-015<br>[AT-03](../tasks/AT-03.md)、[AT-04](../tasks/AT-04.md)、[AT-05](../tasks/AT-05.md)、[MS-02](../tasks/MS-02.md)、[MS-05](../tasks/MS-05.md)、[MS-07](../tasks/MS-07.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.2-A02<br>Task Execution!F15 | 建立汇总下钻规则 | 产出：业务对象关系图及关系规则<br>验收：任务、异常和行动可追溯，汇总可下钻，无孤立核心记录 | 未开始 | REQ-005, REQ-007<br>[AT-01](../tasks/AT-01.md)、[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.2-A03<br>Task Execution!F16 | 处理跨项目和多SKU关系 | 产出：业务对象关系图及关系规则<br>验收：任务、异常和行动可追溯，汇总可下钻，无孤立核心记录 | 未开始 | REQ-001<br>[AT-03](../tasks/AT-03.md)、[MS-02](../tasks/MS-02.md)、[MS-06](../tasks/MS-06.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M1.3 — 唯一标识与映射

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M1.3-A01<br>Task Execution!F17 | 定义Project、SKU、Milestone、Task、Issue、Action和Decision标识 | 产出：唯一标识、映射和去重规则<br>验收：同一对象不重复，上下游稳定匹配，历史记录可处理 | 进行中 | REQ-002<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：项目/任务/问题等身份P0；Decision ID预留设计，不代表P0建立Decision平台。 |
| M1.3-A02<br>Task Execution!F18 | 建立上游映射、去重和历史无ID处理规则 | 产出：唯一标识、映射和去重规则<br>验收：同一对象不重复，上下游稳定匹配，历史记录可处理 | 进行中 | REQ-002<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M1.4 — 字段与状态标准

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M1.4-A01<br>Task Execution!F19 | 定义身份、责任、日期、生命周期、健康、执行和数据确认字段 | 产出：字段字典、状态字典和转换规则<br>验收：日期和状态不混用，状态条件明确，自动结果可解释 | 进行中 | REQ-004, REQ-006, REQ-008<br>[AT-01](../tasks/AT-01.md)、[AT-02](../tasks/AT-02.md)、[AT-04](../tasks/AT-04.md)、[MS-02](../tasks/MS-02.md)、[MS-03](../tasks/MS-03.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.4-A02<br>Task Execution!F20 | 定义状态转换、重开和关闭规则 | 产出：字段字典、状态字典和转换规则<br>验收：日期和状态不混用，状态条件明确，自动结果可解释 | 未开始 | REQ-008, REQ-011, REQ-015<br>[AT-01](../tasks/AT-01.md)、[AT-05](../tasks/AT-05.md)、[MS-03](../tasks/MS-03.md)、[MS-07](../tasks/MS-07.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M1.5 — 数据来源与责任

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M1.5-A01<br>Task Execution!F21 | 确认关键字段正式来源 | 产出：数据来源矩阵、责任矩阵和读写规则<br>验收：关键字段有来源和责任，无规则双维护被消除，冲突可处理 | 进行中 | REQ-002, REQ-003, REQ-029<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-01](../tasks/MS-01.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.5-A02<br>Task Execution!F22 | 明确读写计算引用边界 | 产出：数据来源矩阵、责任矩阵和读写规则<br>验收：关键字段有来源和责任，无规则双维护被消除，冲突可处理 | 未开始 | REQ-002, REQ-003, REQ-029<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-01](../tasks/MS-01.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.5-A03<br>Task Execution!F23 | 指定业务与数据Owner | 产出：数据来源矩阵、责任矩阵和读写规则<br>验收：关键字段有来源和责任，无规则双维护被消除，冲突可处理 | 未开始 | REQ-002, REQ-026, REQ-028<br>[GOV-01](../tasks/GOV-01.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.5-A04<br>Task Execution!F24 | 定义冲突、失败和双系统维护规则 | 产出：数据来源矩阵、责任矩阵和读写规则<br>验收：关键字段有来源和责任，无规则双维护被消除，冲突可处理 | 未开始 | REQ-003, REQ-004, REQ-029<br>[AT-06](../tasks/AT-06.md)、[MS-08](../tasks/MS-08.md)、[MS-10](../tasks/MS-10.md)、[GOV-01](../tasks/GOV-01.md)、[GOV-04](../tasks/GOV-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M1.6 — 真实项目数据初始化

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M1.6-A01<br>Task Execution!F25 | 确认试点项目 | 产出：可运行试点数据及修复清单<br>验收：项目具有真实结构和执行数据，关系完整，业务抽样一致 | 未开始 | REQ-028<br>[GOV-03](../tasks/GOV-03.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.6-A02<br>Task Execution!F26 | 清理记录 | 产出：可运行试点数据及修复清单<br>验收：项目具有真实结构和执行数据，关系完整，业务抽样一致 | 进行中 | REQ-002, REQ-004<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-10](../tasks/MS-10.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.6-A03<br>Task Execution!F27 | 建立Project与SKU关系 | 产出：可运行试点数据及修复清单<br>验收：项目具有真实结构和执行数据，关系完整，业务抽样一致 | 未开始 | REQ-001, REQ-002<br>[AT-03](../tasks/AT-03.md)、[MS-02](../tasks/MS-02.md)、[MS-06](../tasks/MS-06.md)、[MS-10](../tasks/MS-10.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.6-A04<br>Task Execution!F28 | 导入Milestone、Task、成员、异常和Action | 产出：可运行试点数据及修复清单<br>验收：项目具有真实结构和执行数据，关系完整，业务抽样一致 | 进行中 | REQ-002, REQ-004<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-10](../tasks/MS-10.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.6-A05<br>Task Execution!F29 | 完成业务抽样 | 产出：可运行试点数据及修复清单<br>验收：项目具有真实结构和执行数据，关系完整，业务抽样一致 | 未开始 | REQ-004, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M1.7 — 数据质量与审计

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M1.7-A01<br>Task Execution!F30 | 建立必填、关系、重复、冲突、未更新和业务逻辑检查 | 产出：质量规则、问题清单和审计记录<br>验收：问题可识别、分配和关闭，关键变化可追溯 | 进行中 | REQ-004<br>[AT-01](../tasks/AT-01.md)、[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-03](../tasks/MS-03.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.7-A02<br>Task Execution!F31 | 记录关键变更和数据产生方式 | 产出：质量规则、问题清单和审计记录<br>验收：问题可识别、分配和关闭，关键变化可追溯 | 未开始 | REQ-004, REQ-011<br>[AT-05](../tasks/AT-05.md)、[AT-06](../tasks/AT-06.md)、[MS-03](../tasks/MS-03.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M1.7-A03<br>Task Execution!F32 | 关闭质量问题 | 产出：质量规则、问题清单和审计记录<br>验收：问题可识别、分配和关闭，关键变化可追溯 | 未开始 | REQ-004<br>[AT-06](../tasks/AT-06.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M2.1 — 项目进入与初始化

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.1-A01<br>Task Execution!F33 | 识别新增与重复项目 | 产出：已初始化项目及范围责任记录<br>验收：项目身份唯一，结构、责任和模板明确 | 进行中 | REQ-001, REQ-009<br>[AT-04](../tasks/AT-04.md)、[MS-05](../tasks/MS-05.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.1-A02<br>Task Execution!F34 | 确认Programme、Project Group、SKU、类型、阶段、范围、负责人、成员和模板 | 产出：已初始化项目及范围责任记录<br>验收：项目身份唯一，结构、责任和模板明确 | 未开始 | REQ-001, REQ-009<br>[AT-04](../tasks/AT-04.md)、[MS-05](../tasks/MS-05.md)、[GOV-01](../tasks/GOV-01.md) | P0：旧文Project Group与PRD冲突；保留原动作，按Program/Project/SKU正式对象和关系映射，不新增Project Group层级。 |

## M2.2 — 计划与任务建立

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.2-A01<br>Task Execution!F35 | 建立阶段和Milestone | 产出：项目基线计划及任务责任清单<br>验收：关键里程碑和任务有日期、责任、依赖并可执行 | 进行中 | REQ-008, REQ-009, REQ-018<br>[AT-04](../tasks/AT-04.md)、[MS-05](../tasks/MS-05.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.2-A02<br>Task Execution!F36 | 导入或生成Task | 产出：项目基线计划及任务责任清单<br>验收：关键里程碑和任务有日期、责任、依赖并可执行 | 进行中 | REQ-003, REQ-008, REQ-009<br>[AT-04](../tasks/AT-04.md)、[AT-06](../tasks/AT-06.md)、[MS-05](../tasks/MS-05.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.2-A03<br>Task Execution!F37 | 明确交付物和依赖 | 产出：项目基线计划及任务责任清单<br>验收：关键里程碑和任务有日期、责任、依赖并可执行 | 未开始 | REQ-008, REQ-009, REQ-018<br>[AT-04](../tasks/AT-04.md)、[MS-05](../tasks/MS-05.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.2-A04<br>Task Execution!F38 | 分配Owner | 产出：项目基线计划及任务责任清单<br>验收：关键里程碑和任务有日期、责任、依赖并可执行 | 进行中 | REQ-008, REQ-009, REQ-018<br>[AT-04](../tasks/AT-04.md)、[MS-05](../tasks/MS-05.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.2-A05<br>Task Execution!F39 | 设置Baseline与Due | 产出：项目基线计划及任务责任清单<br>验收：关键里程碑和任务有日期、责任、依赖并可执行 | 进行中 | REQ-008, REQ-009, REQ-018<br>[AT-04](../tasks/AT-04.md)、[MS-05](../tasks/MS-05.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.2-A06<br>Task Execution!F40 | 确认计划并记录变更 | 产出：项目基线计划及任务责任清单<br>验收：关键里程碑和任务有日期、责任、依赖并可执行 | 未开始 | REQ-008, REQ-009, REQ-018<br>[AT-04](../tasks/AT-04.md)、[MS-05](../tasks/MS-05.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M2.3 — 日常执行与更新

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.3-A01<br>Task Execution!F41 | 查看待办 | 产出：持续更新的执行状态及承诺结果记录<br>验收：状态真实，计划预测实际可比较，长期未更新可识别 | 进行中 | REQ-008, REQ-010<br>[AT-02](../tasks/AT-02.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.3-A02<br>Task Execution!F42 | 更新Task和Forecast | 产出：持续更新的执行状态及承诺结果记录<br>验收：状态真实，计划预测实际可比较，长期未更新可识别 | 未开始 | REQ-008, REQ-009<br>[AT-01](../tasks/AT-01.md)、[AT-04](../tasks/AT-04.md)、[AT-08](../tasks/AT-08.md)、[MS-05](../tasks/MS-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.3-A03<br>Task Execution!F43 | 提交交付物或证据 | 产出：持续更新的执行状态及承诺结果记录<br>验收：状态真实，计划预测实际可比较，长期未更新可识别 | 未开始 | REQ-008, REQ-011<br>[AT-01](../tasks/AT-01.md)、[AT-08](../tasks/AT-08.md)、[MS-05](../tasks/MS-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.3-A04<br>Task Execution!F44 | 记录下一步、等待、阻塞、变化、更新时间和更新人 | 产出：持续更新的执行状态及承诺结果记录<br>验收：状态真实，计划预测实际可比较，长期未更新可识别 | 未开始 | REQ-005, REQ-008<br>[AT-02](../tasks/AT-02.md)、[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M2.4 — 异常识别与记录

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.4-A01<br>Task Execution!F45 | 识别并分类Issue、Risk、Delay和Blocker | 产出：结构化异常记录及影响责任<br>验收：分类一致，影响对象、Owner、状态和下一步明确 | 未开始 | REQ-012<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.4-A02<br>Task Execution!F46 | 关联影响对象 | 产出：结构化异常记录及影响责任<br>验收：分类一致，影响对象、Owner、状态和下一步明确 | 未开始 | REQ-012<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.4-A03<br>Task Execution!F47 | 记录影响、严重度、原因、Owner、升级需求和重复异常 | 产出：结构化异常记录及影响责任<br>验收：分类一致，影响对象、Owner、状态和下一步明确 | 未开始 | REQ-012<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M2.5 — 恢复行动与升级

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.5-A01<br>Task Execution!F48 | 创建Recovery Action | 产出：恢复行动计划及责任日期结果<br>验收：关键异常有行动或处置结论，逾期无效行动可升级 | 未开始 | REQ-013<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.5-A02<br>Task Execution!F49 | 指定Owner | 产出：恢复行动计划及责任日期结果<br>验收：关键异常有行动或处置结论，逾期无效行动可升级 | 未开始 | REQ-013<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.5-A03<br>Task Execution!F50 | 设置Due和恢复目标 | 产出：恢复行动计划及责任日期结果<br>验收：关键异常有行动或处置结论，逾期无效行动可升级 | 未开始 | REQ-013<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.5-A04<br>Task Execution!F51 | 更新优先级、状态、进展和结果 | 产出：恢复行动计划及责任日期结果<br>验收：关键异常有行动或处置结论，逾期无效行动可升级 | 未开始 | REQ-013<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.5-A05<br>Task Execution!F52 | 识别逾期无效行动并升级 | 产出：恢复行动计划及责任日期结果<br>验收：关键异常有行动或处置结论，逾期无效行动可升级 | 未开始 | REQ-010, REQ-013<br>[AT-05](../tasks/AT-05.md)、[AT-09](../tasks/AT-09.md)、[MS-07](../tasks/MS-07.md)、[MS-09](../tasks/MS-09.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M2.6 — 管理决策

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.6-A01<br>Task Execution!F53 | 识别待决策事项 | 产出：待决策清单、决策记录和后续行动<br>验收：决策事项、人员、期限、理由和结果可追踪 | 未开始 | REQ-014<br>[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md)、[GOV-01](../tasks/GOV-01.md) | P1：独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。 |
| M2.6-A02<br>Task Execution!F54 | 记录背景、影响、时限、方案和建议 | 产出：待决策清单、决策记录和后续行动<br>验收：决策事项、人员、期限、理由和结果可追踪 | 未开始 | REQ-014<br>[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md)、[GOV-01](../tasks/GOV-01.md) | P1：独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。 |
| M2.6-A03<br>Task Execution!F55 | 指定决策人 | 产出：待决策清单、决策记录和后续行动<br>验收：决策事项、人员、期限、理由和结果可追踪 | 未开始 | REQ-014<br>[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md)、[GOV-01](../tasks/GOV-01.md) | P1：独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。 |
| M2.6-A04<br>Task Execution!F56 | 记录决定理由 | 产出：待决策清单、决策记录和后续行动<br>验收：决策事项、人员、期限、理由和结果可追踪 | 未开始 | REQ-014<br>[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md)、[GOV-01](../tasks/GOV-01.md) | P1：独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。 |
| M2.6-A05<br>Task Execution!F57 | 转化Action并跟踪结果 | 产出：待决策清单、决策记录和后续行动<br>验收：决策事项、人员、期限、理由和结果可追踪 | 未开始 | REQ-014<br>[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md)、[GOV-01](../tasks/GOV-01.md) | P1：独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。 |

## M2.7 — 结果确认与验证关闭

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.7-A01<br>Task Execution!F58 | 检查Action | 产出：验证关闭记录及结果证据<br>验收：Action完成不等于Issue关闭，关闭有结果、证据和验证人 | 未开始 | REQ-011, REQ-015<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.7-A02<br>Task Execution!F59 | 记录结果 | 产出：验证关闭记录及结果证据<br>验收：Action完成不等于Issue关闭，关闭有结果、证据和验证人 | 未开始 | REQ-011, REQ-015<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.7-A03<br>Task Execution!F60 | 确认影响是否消除或接受 | 产出：验证关闭记录及结果证据<br>验收：Action完成不等于Issue关闭，关闭有结果、证据和验证人 | 未开始 | REQ-011, REQ-015<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.7-A04<br>Task Execution!F61 | 指定验证人 | 产出：验证关闭记录及结果证据<br>验收：Action完成不等于Issue关闭，关闭有结果、证据和验证人 | 未开始 | REQ-011, REQ-015<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.7-A05<br>Task Execution!F62 | 提交证据 | 产出：验证关闭记录及结果证据<br>验收：Action完成不等于Issue关闭，关闭有结果、证据和验证人 | 未开始 | REQ-011, REQ-015<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.7-A06<br>Task Execution!F63 | 正式关闭或重开 | 产出：验证关闭记录及结果证据<br>验收：Action完成不等于Issue关闭，关闭有结果、证据和验证人 | 未开始 | REQ-011, REQ-015<br>[AT-05](../tasks/AT-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M2.8 — 历史与经验沉淀

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M2.8-A01<br>Task Execution!F64 | 保留计划和状态变化 | 产出：结构化执行历史及问题处理案例<br>验收：原因、行动、决定和结果可关联，案例来自真实关闭记录 | 未开始 | REQ-008, REQ-009, REQ-011<br>[AT-03](../tasks/AT-03.md)、[AT-04](../tasks/AT-04.md)、[AT-05](../tasks/AT-05.md)、[MS-05](../tasks/MS-05.md)、[MS-06](../tasks/MS-06.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M2.8-A02<br>Task Execution!F65 | 记录Root Cause、有效无效Action、关键Decision、最终Result和可检索案例 | 产出：结构化执行历史及问题处理案例<br>验收：原因、行动、决定和结果可关联，案例来自真实关闭记录 | 未开始 | REQ-011, REQ-016, REQ-017<br>[AT-10](../tasks/AT-10.md)、[MS-09](../tasks/MS-09.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |

## M3.1 — 个人执行入口

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M3.1-A01<br>Task Execution!F66 | 展示今日、即将到期、逾期、待更新、待确认、本人异常和Action | 产出：My Daily Work入口<br>验收：一个入口找到并完成核心工作，可返回项目背景，减少重复维护 | 进行中 | REQ-008, REQ-010<br>[AT-02](../tasks/AT-02.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M3.1-A02<br>Task Execution!F67 | 支持更新、提交结果并进入项目背景 | 产出：My Daily Work入口<br>验收：一个入口找到并完成核心工作，可返回项目背景，减少重复维护 | 进行中 | REQ-008, REQ-010<br>[AT-02](../tasks/AT-02.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M3.2 — 项目管理入口

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M3.2-A01<br>Task Execution!F68 | 展示项目、SKU、阶段、健康、Milestone、Task、异常、Action、待决策和缺失项 | 产出：Project Workspace及可信项目视图<br>验收：偏差、影响、Owner和下一步清楚，无需另做解释报告 | 未开始 | REQ-005<br>[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |
| M3.2-A02<br>Task Execution!F69 | 支持更新、审查和下钻 | 产出：Project Workspace及可信项目视图<br>验收：偏差、影响、Owner和下一步清楚，无需另做解释报告 | 未开始 | REQ-005<br>[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M3.3 — 异常处理入口

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M3.3-A01<br>Task Execution!F70 | 展示开放、缺失Owner/Action/Due、逾期和待关闭异常 | 产出：统一异常处理入口<br>验收：异常集中可见，可直接分配、行动、升级和关闭 | 未开始 | REQ-012, REQ-013, REQ-015<br>[AT-05](../tasks/AT-05.md)、[AT-08](../tasks/AT-08.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M3.3-A02<br>Task Execution!F71 | 支持分配、行动、更新、升级、决策和关闭 | 产出：统一异常处理入口<br>验收：异常集中可见，可直接分配、行动、升级和关闭 | 未开始 | REQ-012, REQ-013, REQ-015<br>[AT-05](../tasks/AT-05.md)、[AT-08](../tasks/AT-08.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |

## M3.4 — 周度管理入口

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M3.4-A01<br>Task Execution!F72 | 展示健康、变化、偏差、Top Risk、逾期、缺失、待决策和上周结果 | 产出：周度管理视图及决定行动记录<br>验收：周会直接使用AutoPM，决定回写，下周期验证结果 | 进行中 | REQ-019, REQ-020<br>[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md) | P1：独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。 |
| M3.4-A02<br>Task Execution!F73 | 支持确认、决定和行动回写 | 产出：周度管理视图及决定行动记录<br>验收：周会直接使用AutoPM，决定回写，下周期验证结果 | 未开始 | REQ-019, REQ-020<br>[AT-13](../tasks/AT-13.md)、[MS-12](../tasks/MS-12.md) | P1：独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。 |

## M3.5 — 领导审查与下钻

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M3.5-A01<br>Task Execution!F74 | 展示组合健康、关键风险延误、受影响Milestone和待决策项 | 产出：Leadership View及下钻路径<br>验收：汇总结论可下钻，管理决定和后续行动可追踪 | 未开始 | REQ-007<br>[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |
| M3.5-A02<br>Task Execution!F75 | 逐层下钻至Project、SKU、异常、Action、Owner和Result | 产出：Leadership View及下钻路径<br>验收：汇总结论可下钻，管理决定和后续行动可追踪 | 未开始 | REQ-007<br>[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M3.6 — 用户体验与动作效率

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M3.6-A01<br>Task Execution!F76 | 删除无用字段 | 产出：用户问题清单及界面修复任务<br>验收：核心动作易完成，信息一次维护，反馈转为可验收任务 | 未开始 | REQ-004, REQ-005<br>[AT-00](../tasks/AT-00.md)、[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md)、[GOV-01](../tasks/GOV-01.md) | P0：原删除意图改为消费者核对与先隐藏；删除需后续具体影响、恢复方案及范围授权，不直接执行旧文删除指令。 |
| M3.6-A02<br>Task Execution!F77 | 减少重复录入和页面切换 | 产出：用户问题清单及界面修复任务<br>验收：核心动作易完成，信息一次维护，反馈转为可验收任务 | 进行中 | REQ-005, REQ-028<br>[AT-00](../tasks/AT-00.md)、[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M3.6-A03<br>Task Execution!F78 | 突出下一步 | 产出：用户问题清单及界面修复任务<br>验收：核心动作易完成，信息一次维护，反馈转为可验收任务 | 未开始 | REQ-005, REQ-028<br>[AT-00](../tasks/AT-00.md)、[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M3.6-A04<br>Task Execution!F79 | 简化更新 | 产出：用户问题清单及界面修复任务<br>验收：核心动作易完成，信息一次维护，反馈转为可验收任务 | 未开始 | REQ-005, REQ-028<br>[AT-00](../tasks/AT-00.md)、[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M3.6-A05<br>Task Execution!F80 | 提供说明 | 产出：用户问题清单及界面修复任务<br>验收：核心动作易完成，信息一次维护，反馈转为可验收任务 | 未开始 | REQ-005, REQ-028<br>[AT-00](../tasks/AT-00.md)、[AT-08](../tasks/AT-08.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M3.6-A06<br>Task Execution!F81 | 收集并排序用户问题 | 产出：用户问题清单及界面修复任务<br>验收：核心动作易完成，信息一次维护，反馈转为可验收任务 | 未开始 | REQ-027, REQ-028<br>[AT-10](../tasks/AT-10.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M4.1 — 数据导入与初始化自动化

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M4.1-A01<br>Task Execution!F82 | 建立导入模板 | 产出：稳定导入流程及错误报告<br>验收：不重复，错误可定位，不静默覆盖真实数据 | 进行中 | REQ-003, REQ-004<br>[AT-06](../tasks/AT-06.md)、[AT-07](../tasks/AT-07.md)、[MS-01](../tasks/MS-01.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.1-A02<br>Task Execution!F83 | 校验格式 | 产出：稳定导入流程及错误报告<br>验收：不重复，错误可定位，不静默覆盖真实数据 | 进行中 | REQ-003, REQ-004<br>[AT-06](../tasks/AT-06.md)、[AT-07](../tasks/AT-07.md)、[MS-01](../tasks/MS-01.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.1-A03<br>Task Execution!F84 | 匹配ID和Owner | 产出：稳定导入流程及错误报告<br>验收：不重复，错误可定位，不静默覆盖真实数据 | 进行中 | REQ-003, REQ-004<br>[AT-06](../tasks/AT-06.md)、[AT-07](../tasks/AT-07.md)、[MS-01](../tasks/MS-01.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.1-A04<br>Task Execution!F85 | 防重复和静默覆盖 | 产出：稳定导入流程及错误报告<br>验收：不重复，错误可定位，不静默覆盖真实数据 | 进行中 | REQ-003, REQ-004<br>[AT-06](../tasks/AT-06.md)、[AT-07](../tasks/AT-07.md)、[MS-01](../tasks/MS-01.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.1-A05<br>Task Execution!F86 | 显示错误 | 产出：稳定导入流程及错误报告<br>验收：不重复，错误可定位，不静默覆盖真实数据 | 进行中 | REQ-003, REQ-004<br>[AT-06](../tasks/AT-06.md)、[AT-07](../tasks/AT-07.md)、[MS-01](../tasks/MS-01.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.1-A06<br>Task Execution!F87 | 支持修正和回退 | 产出：稳定导入流程及错误报告<br>验收：不重复，错误可定位，不静默覆盖真实数据 | 未开始 | REQ-003, REQ-004<br>[AT-06](../tasks/AT-06.md)、[AT-07](../tasks/AT-07.md)、[MS-01](../tasks/MS-01.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M4.2 — 状态与异常计算

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M4.2-A01<br>Task Execution!F88 | 计算到期、逾期、Next Milestone和偏差 | 产出：计算规则及可解释结果<br>验收：规则与业务定义一致，异常边界通过测试，不无依据覆盖 | 进行中 | REQ-006, REQ-009, REQ-010, REQ-023<br>[AT-01](../tasks/AT-01.md)、[AT-02](../tasks/AT-02.md)、[AT-04](../tasks/AT-04.md)、[MS-03](../tasks/MS-03.md)、[MS-04](../tasks/MS-04.md)、[MS-05](../tasks/MS-05.md)、[MS-07](../tasks/MS-07.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.2-A02<br>Task Execution!F89 | 识别缺失与冲突 | 产出：计算规则及可解释结果<br>验收：规则与业务定义一致，异常边界通过测试，不无依据覆盖 | 未开始 | REQ-004, REQ-006, REQ-023<br>[AT-01](../tasks/AT-01.md)、[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-03](../tasks/MS-03.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.2-A03<br>Task Execution!F90 | 展示依据并支持授权确认 | 产出：计算规则及可解释结果<br>验收：规则与业务定义一致，异常边界通过测试，不无依据覆盖 | 未开始 | REQ-005, REQ-006, REQ-023<br>[AT-01](../tasks/AT-01.md)、[AT-08](../tasks/AT-08.md)、[MS-03](../tasks/MS-03.md)、[MS-04](../tasks/MS-04.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M4.3 — 提醒与升级

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M4.3-A01<br>Task Execution!F91 | 建立到期、逾期、缺失和关键Delay提醒 | 产出：分级提醒和升级机制<br>验收：对象正确，已完成停止，重复受控，关键事项升级 | 进行中 | REQ-010, REQ-021<br>[AT-09](../tasks/AT-09.md)、[MS-09](../tasks/MS-09.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.3-A02<br>Task Execution!F92 | 建立去重、停止、升级及响应记录 | 产出：分级提醒和升级机制<br>验收：对象正确，已完成停止，重复受控，关键事项升级 | 未开始 | REQ-010, REQ-021<br>[AT-09](../tasks/AT-09.md)、[MS-09](../tasks/MS-09.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M4.4 — 报告生成

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M4.4-A01<br>Task Execution!F93 | 汇总状态、变化、风险、延误、行动和决定 | 产出：可确认、可追溯的周报草稿<br>验收：报告来自统一数据，缺失透明，可下钻，发布前人工确认 | 进行中 | REQ-019<br>[AT-09](../tasks/AT-09.md)、[MS-09](../tasks/MS-09.md) | P0：本动作的结构化周报、来源、确认与导出为P0；并不要求新增AI生成，AI增强另由AT-14/MS-12承接。 |
| M4.4-A02<br>Task Execution!F94 | 生成周报 | 产出：可确认、可追溯的周报草稿<br>验收：报告来自统一数据，缺失透明，可下钻，发布前人工确认 | 已完成 | REQ-019<br>[AT-09](../tasks/AT-09.md)、[MS-09](../tasks/MS-09.md) | P0：本动作的结构化周报、来源、确认与导出为P0；并不要求新增AI生成，AI增强另由AT-14/MS-12承接。 |
| M4.4-A03<br>Task Execution!F95 | 标记缺失待确认 | 产出：可确认、可追溯的周报草稿<br>验收：报告来自统一数据，缺失透明，可下钻，发布前人工确认 | 未开始 | REQ-019<br>[AT-09](../tasks/AT-09.md)、[MS-09](../tasks/MS-09.md) | P0：本动作的结构化周报、来源、确认与导出为P0；并不要求新增AI生成，AI增强另由AT-14/MS-12承接。 |
| M4.4-A04<br>Task Execution!F96 | 保留来源、下钻、确认和导出 | 产出：可确认、可追溯的周报草稿<br>验收：报告来自统一数据，缺失透明，可下钻，发布前人工确认 | 未开始 | REQ-019<br>[AT-09](../tasks/AT-09.md)、[MS-09](../tasks/MS-09.md) | P0：本动作的结构化周报、来源、确认与导出为P0；并不要求新增AI生成，AI增强另由AT-14/MS-12承接。 |

## M4.5 — PMO主数据连接

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M4.5-A01<br>Task Execution!F97 | 确认必要数据范围 | 产出：PMO读取验证及映射对账结果<br>验收：必要主数据稳定匹配，冲突和失败不静默处理 | 进行中 | REQ-002, REQ-003, REQ-007<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.5-A02<br>Task Execution!F98 | 建立Programme、Project、SKU和目标日期映射 | 产出：PMO读取验证及映射对账结果<br>验收：必要主数据稳定匹配，冲突和失败不静默处理 | 未开始 | REQ-002, REQ-003, REQ-007<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.5-A03<br>Task Execution!F99 | 验证读取 | 产出：PMO读取验证及映射对账结果<br>验收：必要主数据稳定匹配，冲突和失败不静默处理 | 未开始 | REQ-002, REQ-003, REQ-007<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.5-A04<br>Task Execution!F100 | 识别变化冲突 | 产出：PMO读取验证及映射对账结果<br>验收：必要主数据稳定匹配，冲突和失败不静默处理 | 未开始 | REQ-002, REQ-003, REQ-007<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.5-A05<br>Task Execution!F101 | 记录同步并对账 | 产出：PMO读取验证及映射对账结果<br>验收：必要主数据稳定匹配，冲突和失败不静默处理 | 未开始 | REQ-002, REQ-003, REQ-007<br>[AT-03](../tasks/AT-03.md)、[AT-06](../tasks/AT-06.md)、[MS-02](../tasks/MS-02.md)、[MS-08](../tasks/MS-08.md)、[GOV-01](../tasks/GOV-01.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M4.6 — 权限与审计

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M4.6-A01<br>Task Execution!F102 | 定义角色、项目、查看、编辑、确认、审批、导出和敏感字段权限 | 产出：Phase 1权限模型及审计记录<br>验收：访问和关键操作受控，越权经过测试，操作可追溯 | 未开始 | REQ-026<br>[AT-11](../tasks/AT-11.md)、[MS-03](../tasks/MS-03.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.6-A02<br>Task Execution!F103 | 记录变更 | 产出：Phase 1权限模型及审计记录<br>验收：访问和关键操作受控，越权经过测试，操作可追溯 | 未开始 | REQ-026<br>[AT-11](../tasks/AT-11.md)、[MS-03](../tasks/MS-03.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.6-A03<br>Task Execution!F104 | 测试越权 | 产出：Phase 1权限模型及审计记录<br>验收：访问和关键操作受控，越权经过测试，操作可追溯 | 未开始 | REQ-026<br>[AT-11](../tasks/AT-11.md)、[MS-03](../tasks/MS-03.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M4.7 — 运行监控与失败恢复

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M4.7-A01<br>Task Execution!F105 | 记录自动化和同步结果 | 产出：运行监控及失败处理机制<br>验收：失败及时发现，重试安全，故障有责任和回退 | 未开始 | REQ-027<br>[AT-07](../tasks/AT-07.md)、[AT-09](../tasks/AT-09.md)、[MS-08](../tasks/MS-08.md)、[MS-09](../tasks/MS-09.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.7-A02<br>Task Execution!F106 | 监控异常 | 产出：运行监控及失败处理机制<br>验收：失败及时发现，重试安全，故障有责任和回退 | 未开始 | REQ-027<br>[AT-10](../tasks/AT-10.md)、[MS-08](../tasks/MS-08.md)、[MS-10](../tasks/MS-10.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.7-A03<br>Task Execution!F107 | 告警并分配Owner | 产出：运行监控及失败处理机制<br>验收：失败及时发现，重试安全，故障有责任和回退 | 未开始 | REQ-027<br>[AT-07](../tasks/AT-07.md)、[AT-10](../tasks/AT-10.md)、[MS-08](../tasks/MS-08.md)、[MS-10](../tasks/MS-10.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.7-A04<br>Task Execution!F108 | 支持幂等重试 | 产出：运行监控及失败处理机制<br>验收：失败及时发现，重试安全，故障有责任和回退 | 进行中 | REQ-004, REQ-027<br>[AT-06](../tasks/AT-06.md)、[AT-07](../tasks/AT-07.md)、[MS-03](../tasks/MS-03.md)、[MS-08](../tasks/MS-08.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.7-A05<br>Task Execution!F109 | 防数据污染 | 产出：运行监控及失败处理机制<br>验收：失败及时发现，重试安全，故障有责任和回退 | 未开始 | REQ-004, REQ-027<br>[AT-06](../tasks/AT-06.md)、[MS-03](../tasks/MS-03.md)、[MS-08](../tasks/MS-08.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |
| M4.7-A06<br>Task Execution!F110 | 建立回退 | 产出：运行监控及失败处理机制<br>验收：失败及时发现，重试安全，故障有责任和回退 | 未开始 | REQ-027, REQ-029<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-02](../tasks/GOV-02.md) | P0：原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。 |

## M5.1 — Pilot范围确认

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M5.1-A01<br>Task Execution!F111 | 确认试点目标、团队、负责人、项目清单、选择标准、参与角色、使用承诺及启动暂停退出条件 | 产出：Pilot范围说明及团队项目清单<br>验收：团队、项目、角色和目标确认，未确认数量周期保持TBD | 未开始 | REQ-028<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M5.2 — 角色与责任

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M5.2-A01<br>Task Execution!F112 | 定义执行、项目、职能、管理、Data Owner和平台支持责任 | 产出：Pilot角色责任矩阵<br>验收：每类数据和行动有责任，PM不代替所有人维护 | 未开始 | REQ-026, REQ-028<br>[GOV-02](../tasks/GOV-02.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M5.3 — 使用规则

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M5.3-A01<br>Task Execution!F113 | 定义必须维护的信息、更新频率、异常Action升级关闭规则、人工确认和最低证据 | 产出：Pilot使用规则<br>验收：何时在哪里更新什么清楚，关键事实保留人工责任 | 未开始 | REQ-008, REQ-010, REQ-011, REQ-015, REQ-028<br>[GOV-01](../tasks/GOV-01.md)、[GOV-02](../tasks/GOV-02.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M5.4 — 双系统过渡

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M5.4-A01<br>Task Execution!F114 | 明确唯一维护位置、旧工具范围、读取写入链接同步方向、冲突失败、停止条件和回退方案 | 产出：双系统过渡方案<br>验收：无规则重复维护被消除，切换和回退不丢数据 | 进行中 | REQ-003, REQ-028, REQ-029<br>[MS-10](../tasks/MS-10.md)、[GOV-01](../tasks/GOV-01.md)、[GOV-03](../tasks/GOV-03.md)、[GOV-04](../tasks/GOV-04.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M5.5 — 角色上手

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M5.5-A01<br>Task Execution!F115 | 使用真实项目完成任务更新、状态异常维护、Action确认、管理审查和Decision | 产出：角色上手记录及首轮问题清单<br>验收：关键角色在真实项目完成核心动作，不以登录培训作为完成 | 未开始 | REQ-026, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |
| M5.5-A02<br>Task Execution!F116 | 记录问题和理解偏差 | 产出：角色上手记录及首轮问题清单<br>验收：关键角色在真实项目完成核心动作，不以登录培训作为完成 | 未开始 | REQ-026, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M5.6 — 周度运行节奏

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M5.6-A01<br>Task Execution!F117 | 按规则更新 | 产出：可重复周度运行机制<br>验收：真实项目持续更新，周会使用AutoPM，行动下周期验证 | 已完成 | REQ-019, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.6-A02<br>Task Execution!F118 | 检查数据 | 产出：可重复周度运行机制<br>验收：真实项目持续更新，周会使用AutoPM，行动下周期验证 | 未开始 | REQ-019, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.6-A03<br>Task Execution!F119 | 生成异常和周报 | 产出：可重复周度运行机制<br>验收：真实项目持续更新，周会使用AutoPM，行动下周期验证 | 进行中 | REQ-019, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.6-A04<br>Task Execution!F120 | 开展周度审查 | 产出：可重复周度运行机制<br>验收：真实项目持续更新，周会使用AutoPM，行动下周期验证 | 未开始 | REQ-019, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |
| M5.6-A05<br>Task Execution!F121 | 回写决定和Action | 产出：可重复周度运行机制<br>验收：真实项目持续更新，周会使用AutoPM，行动下周期验证 | 未开始 | REQ-019, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |
| M5.6-A06<br>Task Execution!F122 | 下周期验证结果 | 产出：可重复周度运行机制<br>验收：真实项目持续更新，周会使用AutoPM，行动下周期验证 | 未开始 | REQ-019, REQ-028<br>[AT-11](../tasks/AT-11.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M5.7 — 用户支持与问题处理

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M5.7-A01<br>Task Execution!F123 | 建立反馈入口 | 产出：问题改进清单及支持修复节奏<br>验收：关键问题有分类、影响、责任和状态，修复经用户验证 | 未开始 | REQ-027, REQ-028<br>[AT-10](../tasks/AT-10.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.7-A02<br>Task Execution!F124 | 分类问题 | 产出：问题改进清单及支持修复节奏<br>验收：关键问题有分类、影响、责任和状态，修复经用户验证 | 未开始 | REQ-027, REQ-028<br>[AT-10](../tasks/AT-10.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.7-A03<br>Task Execution!F125 | 评估影响优先级 | 产出：问题改进清单及支持修复节奏<br>验收：关键问题有分类、影响、责任和状态，修复经用户验证 | 未开始 | REQ-027, REQ-028<br>[AT-10](../tasks/AT-10.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.7-A04<br>Task Execution!F126 | 分配Owner | 产出：问题改进清单及支持修复节奏<br>验收：关键问题有分类、影响、责任和状态，修复经用户验证 | 未开始 | REQ-027, REQ-028<br>[AT-10](../tasks/AT-10.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.7-A05<br>Task Execution!F127 | 验证修复 | 产出：问题改进清单及支持修复节奏<br>验收：关键问题有分类、影响、责任和状态，修复经用户验证 | 未开始 | REQ-027, REQ-028<br>[AT-10](../tasks/AT-10.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M5.7-A06<br>Task Execution!F128 | 转化重复反馈 | 产出：问题改进清单及支持修复节奏<br>验收：关键问题有分类、影响、责任和状态，修复经用户验证 | 未开始 | REQ-027, REQ-028<br>[AT-10](../tasks/AT-10.md)、[MS-10](../tasks/MS-10.md)、[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M6.1 — 基线定义

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M6.1-A01<br>Task Execution!F129 | 定义人工追踪、周报汇总、数据质量、Task/Issue/Action/Delay基线 | 产出：指标定义及Pilot前基线<br>验收：定义和证据清楚，无基线不宣称改善 | 未开始 | REQ-028, REQ-029<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M6.1-A02<br>Task Execution!F130 | 定义算法来源Owner周期并在Pilot前记录 | 产出：指标定义及Pilot前基线<br>验收：定义和证据清楚，无基线不宣称改善 | 未开始 | REQ-028, REQ-029<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M6.2 — 使用与采用证据

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M6.2-A01<br>Task Execution!F131 | 记录活跃项目用户、频率及时性、周度审查、关键动作、中断退出和双系统维护 | 产出：Pilot使用证据包<br>验收：区分登录、一次录入和持续使用，负担和中断如实记录 | 未开始 | REQ-028<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M6.3 — 数据质量证据

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M6.3-A01<br>Task Execution!F132 | 记录字段、关系、Owner、Due、状态完整性，以及重复、冲突、同步失败、修正和关闭 | 产出：数据质量证据包<br>验收：指标可重复计算，问题可追溯，管理可用性有结论 | 进行中 | REQ-004, REQ-028<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M6.4 — 执行闭环证据

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M6.4-A01<br>Task Execution!F133 | 记录Task按期逾期、异常Action覆盖、责任日期关闭、Delay影响恢复、Issue验证关闭和Decision转Action | 产出：执行闭环证据包<br>验收：能识别闭环中断，区分Action完成和Issue关闭 | 未开始 | REQ-015, REQ-028<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。 |

## M6.5 — 效率与业务结果

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M6.5-A01<br>Task Execution!F134 | 比较查找、周报、追问、重复维护、问题发现升级关闭 | 产出：Pilot前后比较及价值结论<br>验收：基于基线，同时呈现改善、未改善、负面影响和数据不足 | 未开始 | REQ-028, REQ-029<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M6.5-A02<br>Task Execution!F135 | 记录决定结果、新增工作和负面影响 | 产出：Pilot前后比较及价值结论<br>验收：基于基线，同时呈现改善、未改善、负面影响和数据不足 | 未开始 | REQ-028, REQ-029<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M6.5-A03<br>Task Execution!F136 | 形成结论 | 产出：Pilot前后比较及价值结论<br>验收：基于基线，同时呈现改善、未改善、负面影响和数据不足 | 未开始 | REQ-028, REQ-029<br>[GOV-03](../tasks/GOV-03.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M6.6 — 平台能力评估

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M6.6-A01<br>Task Execution!F137 | 评估性能容量、中国访问、权限审计、自动化集成、导出迁移回退、支持许可成本及技术路线 | 产出：平台评估及Phase 2技术路线建议<br>验收：基于真实使用，事实限制建议分开，不预设最终平台 | 未开始 | REQ-029<br>[GOV-04](../tasks/GOV-04.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |

## M6.7 — Gate 1决策

| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |
|---|---|---|---|---|---|
| M6.7-A01<br>Task Execution!F138 | 汇总证据 | 产出：Gate 1评审包、决策记录及Phase 2条件<br>验收：决策由证据支持，未确认不转承诺，通过后才进入Phase 2 | 未开始 | REQ-026, REQ-028, REQ-029<br>[GOV-04](../tasks/GOV-04.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M6.7-A02<br>Task Execution!F139 | 评估成功条件 | 产出：Gate 1评审包、决策记录及Phase 2条件<br>验收：决策由证据支持，未确认不转承诺，通过后才进入Phase 2 | 未开始 | REQ-026, REQ-028, REQ-029<br>[GOV-04](../tasks/GOV-04.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M6.7-A03<br>Task Execution!F140 | 识别缺口风险 | 产出：Gate 1评审包、决策记录及Phase 2条件<br>验收：决策由证据支持，未确认不转承诺，通过后才进入Phase 2 | 未开始 | REQ-026, REQ-028, REQ-029<br>[GOV-04](../tasks/GOV-04.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M6.7-A04<br>Task Execution!F141 | 提出继续调整延长迁移停止建议 | 产出：Gate 1评审包、决策记录及Phase 2条件<br>验收：决策由证据支持，未确认不转承诺，通过后才进入Phase 2 | 未开始 | REQ-026, REQ-028, REQ-029<br>[GOV-04](../tasks/GOV-04.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
| M6.7-A05<br>Task Execution!F142 | 明确Phase 2条件和正式决定 | 产出：Gate 1评审包、决策记录及Phase 2条件<br>验收：决策由证据支持，未确认不转承诺，通过后才进入Phase 2 | 未开始 | REQ-026, REQ-028, REQ-029<br>[GOV-04](../tasks/GOV-04.md) | P0：治理／试用／度量／Gate工作；不机械转成新增表或代码功能。 |
