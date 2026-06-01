# Ody vs Agileex 供应商策略决策

> 创建时间：2026-05-30  
> 更新：2026-05-30（v2 - 六维框架重构）  
> 背景：Sunny重构评估框架，确立AutoPM核心愿景  
> 状态：**当前有效策略**

---

## 核心需求重新定义

**不是"打通PLM"，而是"把SN内部所有项目数据汇聚到单一事实来源"**

- 周报、月报、时间表、邮件、会议纪要、Teams聊天——全散在不同地方，没有人能串起来
- 目标：信息不再需要经过人传递，PM不再追数据，而是数据追人

---

## 决策结论

**Ody为主平台 + Agileex为辅（可选BI展示）**

但关键前提：Ody的声称能力必须先验证通过才能推进。

---

## 六维评估框架

| 维度 | Ody | Agileex | 关键差距 |
|------|-----|---------|----------|
| D1 PM理解力与产品力 | ★★☆☆☆ | ★☆☆☆☆ | 两家都不懂PM，SN必须自己设计流程；Ody有定制空间，Agileex做不到 |
| D2 数据集成 | ★★★★☆ | ★★☆☆☆ | Ody自动采集 vs Agileex手动填报；前者打破信息墙，后者只是换地方填表 |
| D3 AI与洞察 | ★★★★★ | ★☆☆☆☆ | 代际差距；Ody的6大Agent是产品核心，Agileex只是套个大模型 |
| D4 团队与交付 | ★★☆☆☆ | ★★★★☆ | 能力强的交付不了，交付力强的做不出 |
| D5 安全与主权 | ★★★★☆ | ★★★☆☆ | Ody数据在SN手里，Agileex数据在微软手里 |
| D6 扩展与锁定 | ★★★☆☆ | ★★☆☆☆ | Ody可能人跑了但数据带走，Agileex做不下去但换不掉 |
| **总体** | **★★★☆☆** | **★★☆☆☆** | |

---

## ⚠️ 关键洞察

### 1. 两家都不懂项目管理
Sunny的AutoPM prototype是唯一有PM灵魂的东西，SN必须承担流程设计责任，供应商只是执行者。

### 2. Ody能力大量基于声称未验证
给Jen汇报时必须透明说明：Ody的连接器、AI准确率、实际案例都未在SN环境验证。Discovery Phase的目的就是验证这些声称。

### 3. 核心矛盾：短期能活 vs 长期能成
Agileex Pilot阶段更快更稳，但走不到2000人；Ody方向对但风险高。Pilot选错方向的代价远大于多花几周验证Ody。

---

## AutoPM愿景

简化流程，扁平化组织，加快速度，提高效率，全员参与。从50人Pilot到2000人全员，改变SN的NPI运行方式。

---

## 推荐路径

| 步骤 | 行动 | 产出 |
|------|------|------|
| 本周 | 列出Ody关键能力验证清单 | 第二轮深度问题清单 |
| 1-2周内 | 与Ody深度验证会（不再听介绍，直接问细节和案例） | Ody能力验证结论 |
| 验证后 | 通过→Discovery Phase；失败→评估备选 | 决策 |
| 并行 | 系统化定义PM流程（基于Sunny prototype） | PM流程设计文档 |
| Agileex | 暂不作为AutoPM主供应商 | 保留为Power BI备选 |

---

## 备选方向

Ody验证失败且Agileex不够时：
- **自建团队**：基于Sunny prototype组建内部团队
- **成熟PM SaaS+定制集成**：Monday.com/Asana + 集成商打通数据
- **数据平台先行**：MuleSoft/Boomi先打通管道，再上应用层

---

## 相关文件

- 详细评估报告：`Ody_vs_Agileex_对比报告_Jen_v2.md`
- 英文汇总报告：`AutoPM_Vendor_Assessment_Summary.md`
- Agileex会议纪要：`用户上传/Meeting with Agileex 2026-05-29*.docx.parsed.md`
- Agileex调研报告：`recent_memory/project/Agileex调研报告.md`
- Rodyr提案审查：`recent_memory/decision/Rodyr提案审查.md`
