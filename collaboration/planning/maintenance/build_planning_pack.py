"""Build planning documents from task-register.json; never operates business apps.

python maintenance/build_planning_pack.py
python maintenance/build_planning_pack.py --check
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('D:/个人资料/AI学习圈/SN Auto PM')
PRODUCT = Path('C:/Users/40734/Documents/Codex/autopm-review-draft-20260911/docs/autopm-review/01-product')

SOURCES = [
 ('S01','round2-blueprint.md',WORK/'09-AutoPM Audit by Chatgpt/AutoPM_Traceable_Blueprint_2026-09-11.md'),
 ('S02','round2-supplement.md',WORK/'09-AutoPM Audit by Chatgpt/AutoPM_Round2_Supplement_2026-09-11.md'),
 ('S03','prd-text.md',WORK/'09-AutoPM Audit by Chatgpt/design/PRD_extracted_text.txt'),
 ('S04','capability-matrix-source.md',PRODUCT/'capability-matrix-source.md'),
 ('S05','phase1-closure-source.md',PRODUCT/'phase1-closure-source.md'),
 ('S06','bridge-handover.md',WORK/'07-脚本与数据治理 Scripts & data ops/sync_bridge/AutoPM_Bridge_Maintenance_Handover_2026-09-07.md'),
 ('S07','projects-fields.md',WORK/'03-开发计划 Development plan/Data Architecture/Projects_Field_Architecture_Plan.md'),
 ('S07','other-core-fields.md',WORK/'03-开发计划 Development plan/Data Architecture/Other_Core_Tables_Field_Architecture_Plan.md'),
 ('S08','microsoft-preparation.md',WORK/'10-AutoPM Microsoft/README.md'),
 ('S09','round1-audit.md',WORK/'09-AutoPM Audit by Chatgpt/AutoPM_System_Audit_2026-09-10.md'),
 ('S10','dual-route-baseline.md',WORK/'03-开发计划 Development plan/AutoPM_双路线功能与开发任务基线_2026-09-10.md'),
 ('S12','powerapps-mvp-status-2026-09-10.md',WORK/'outputs/program-mvp/implementation-status-2026-09-10.md'),
]

# Capability-level mappings, refined by explicit action exceptions below.
# All historical titles, outputs and criteria are retained in the generated crosswalk.
CAP = {
 'M1.1':('1 2','AT-00 AT-03 MS-02 GOV-01'),
 'M1.2':('1','AT-03 MS-02 MS-06 GOV-01'),
 'M1.3':('2','AT-03 AT-06 MS-02 MS-08 GOV-01'),
 'M1.4':('4 6 8','AT-01 MS-03 GOV-01'),
 'M1.5':('2 3 29','AT-03 AT-06 MS-01 MS-02 MS-08 GOV-01'),
 'M1.6':('2 4','AT-03 AT-06 MS-10 GOV-01'),
 'M1.7':('4','AT-06 MS-08 GOV-01'),
 'M2.1':('1 9','AT-04 MS-05 GOV-01'),
 'M2.2':('8 9 18','AT-04 MS-05'),
 'M2.3':('8 11','AT-01 AT-02 MS-07'),
 'M2.4':('12','AT-05 MS-07'),
 'M2.5':('13','AT-05 MS-07'),
 'M2.6':('14','AT-13 MS-12 GOV-01'),
 'M2.7':('11 15','AT-05 MS-07'),
 'M2.8':('11 16 17','AT-10 MS-09'),
 'M3.1':('8 10','AT-02 MS-07'),
 'M3.2':('5','AT-08 MS-04'),
 'M3.3':('12 13 15','AT-05 AT-08 MS-07'),
 'M3.4':('19 20','AT-13 MS-12'),
 'M3.5':('7','AT-08 MS-04'),
 'M3.6':('5 28','AT-00 AT-08 MS-04'),
 'M4.1':('3 4','AT-06 AT-07 MS-01 MS-08'),
 'M4.2':('6 8 9 23','AT-01 AT-04 MS-03 MS-05'),
 'M4.3':('10 21','AT-09 MS-09'),
 'M4.4':('19 22','AT-09 AT-14 MS-09 MS-12'),
 'M4.5':('2 3 7','AT-03 AT-06 MS-02 MS-08 GOV-01'),
 'M4.6':('26','AT-11 MS-03 GOV-02'),
 'M4.7':('27 29','AT-10 MS-00 MS-10 GOV-02'),
 'M5.1':('28','GOV-03'),
 'M5.2':('26 28','GOV-02 GOV-03'),
 'M5.3':('28','GOV-03'),
 'M5.4':('28 29','GOV-03 GOV-04'),
 'M5.5':('26 28','AT-11 MS-10 GOV-03'),
 'M5.6':('19 28','AT-11 MS-10 GOV-03'),
 'M5.7':('27 28','AT-10 MS-10 GOV-03'),
 'M6.1':('28 29','GOV-03'),
 'M6.2':('28','GOV-03'),
 'M6.3':('4 28','GOV-03'),
 'M6.4':('15 28','GOV-03'),
 'M6.5':('28 29','GOV-03'),
 'M6.6':('29','GOV-04'),
 'M6.7':('26 28 29','GOV-04'),
}

# Row-specific refinement prevents a broad capability match from assigning a
# concrete action to the wrong implementation owner. Values are REQs, task IDs.
ACTION_OVERRIDES = {
 'M1.1-A02':('1 8 9','AT-04 MS-02 MS-05 GOV-01'),
 'M1.1-A03':('1 12 13','AT-05 MS-02 MS-07 GOV-01'),
 'M1.1-A05':('1 2 26','AT-02 MS-02 MS-07 GOV-01 GOV-02'),
 'M1.1-A06':('2 3 29','AT-03 MS-02 GOV-01'),
 'M1.2-A01':('1 8 13 15','AT-03 AT-04 AT-05 MS-02 MS-05 MS-07 GOV-01'),
 'M1.2-A02':('5 7','AT-01 AT-08 MS-04 GOV-01'),
 'M1.4-A01':('4 6 8','AT-01 AT-02 AT-04 MS-02 MS-03 GOV-01'),
 'M1.4-A02':('8 11 15','AT-01 AT-05 MS-03 MS-07 GOV-01'),
 'M1.5-A03':('2 26 28','GOV-01 GOV-02'),
 'M1.5-A04':('3 4 29','AT-06 MS-08 MS-10 GOV-01 GOV-04'),
 'M1.6-A01':('28','GOV-03'),
 'M1.6-A03':('1 2','AT-03 MS-02 MS-06 MS-10'),
 'M1.6-A05':('4 28','AT-11 MS-10 GOV-03'),
 'M1.7-A01':('4','AT-01 AT-03 AT-06 MS-03 MS-08 GOV-01'),
 'M1.7-A02':('4 11','AT-05 AT-06 MS-03 MS-08'),
 'M2.2-A02':('3 8 9','AT-04 AT-06 MS-05 MS-08'),
 'M2.3-A01':('8 10','AT-02 MS-07'),
 'M2.3-A02':('8 9','AT-01 AT-04 AT-08 MS-05 MS-07'),
 'M2.3-A03':('8 11','AT-01 AT-08 MS-05 MS-07'),
 'M2.3-A04':('5 8','AT-02 AT-08 MS-04 MS-07'),
 'M2.5-A05':('10 13','AT-05 AT-09 MS-07 MS-09'),
 'M2.8-A01':('8 9 11','AT-03 AT-04 AT-05 MS-05 MS-06 MS-07'),
 'M3.6-A01':('4 5','AT-00 AT-08 MS-04 GOV-01'),
 'M3.6-A06':('27 28','AT-10 MS-10 GOV-03'),
 'M4.2-A01':('6 9 10 23','AT-01 AT-02 AT-04 MS-03 MS-04 MS-05 MS-07'),
 'M4.2-A02':('4 6 23','AT-01 AT-03 AT-06 MS-03 MS-08'),
 'M4.2-A03':('5 6 23','AT-01 AT-08 MS-03 MS-04'),
 'M4.4-A01':('19','AT-09 MS-09'),
 'M4.4-A02':('19','AT-09 MS-09'),
 'M4.4-A03':('19','AT-09 MS-09'),
 'M4.4-A04':('19','AT-09 MS-09'),
 'M4.7-A01':('27','AT-07 AT-09 MS-08 MS-09'),
 'M4.7-A02':('27','AT-10 MS-08 MS-10 GOV-02'),
 'M4.7-A03':('27','AT-07 AT-10 MS-08 MS-10 GOV-02'),
 'M4.7-A04':('4 27','AT-06 AT-07 MS-03 MS-08'),
 'M4.7-A05':('4 27','AT-06 MS-03 MS-08 GOV-02'),
 'M4.7-A06':('27 29','AT-11 MS-10 GOV-02'),
 'M5.3-A01':('8 10 11 15 28','GOV-01 GOV-02 GOV-03'),
 'M5.4-A01':('3 28 29','MS-10 GOV-01 GOV-03 GOV-04'),
}

def write(rel, content):
    p=ROOT/rel
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content,encoding='utf-8',newline='\n')

def dump(rel, value):
    write(rel,json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def md(v):
    return str(v).replace('|','\\|').replace('\n','<br>').replace('\r','')

def bullet(items):
    return '\n'.join('- '+str(x) for x in items)

def csv_write(rel, rows, fields):
    stream=io.StringIO(newline='')
    w=csv.DictWriter(stream,fieldnames=fields)
    w.writeheader()
    for row in rows:
        w.writerow({k:(' ; '.join(row.get(k,[])) if isinstance(row.get(k),list) else row.get(k,'')) for k in fields})
    write(rel,'\ufeff'+stream.getvalue())

def parse_actions():
    raw=(ROOT/'sources/phase1-closure-source.md').read_text('utf-8')
    section=raw.split('## Task Execution\n',1)[1].split('\n## ',1)[0]
    actions=[]
    for m in re.finditer(r'^### Row (\d+)\s*\n(.*?)(?=^### Row |\Z)',section,re.M|re.S):
        n=int(m.group(1))
        c={a:v.strip() for a,_,v in re.findall(r'^\*\*([A-Z]+)(\d+)\*\*\s*\n(.*?)(?=^\*\*[A-Z]+\d+\*\*|\Z)',m.group(2),re.M|re.S)}
        if n<8 or not c.get('F'):continue
        aid=c['F'];cap=aid.split('-A')[0]
        reqs,taskids=ACTION_OVERRIDES.get(aid,CAP[cap])
        route='P0'
        disposition='原目标保留；按本版BR及目标对象实施，历史Done不继承为验收。'
        if cap.startswith('M5') or cap.startswith('M6'):
            disposition='治理／试用／度量／Gate工作；不机械转成新增表或代码功能。'
        if cap in ['M2.6','M3.4']:
            route='P1'
            disposition='独立Decision／高级Review按用户范围放P1；现有周报和Issue中的待决责任仍保留，不能静默删去原Action。'
        if cap=='M4.4':
            route='P0'
            disposition='本动作的结构化周报、来源、确认与导出为P0；并不要求新增AI生成，AI增强另由AT-14/MS-12承接。'
        if aid=='M1.1-A04':
            route='P0/P1分层';taskids='AT-05 MS-07 AT-13 MS-12 GOV-01';reqs='1 13 14'
            disposition='恢复对象P0由Tasks类型承载；独立Decision模型P1评估，不据本Action创建重复行动库。'
        if aid=='M1.3-A01':
            disposition='项目/任务/问题等身份P0；Decision ID预留设计，不代表P0建立Decision平台。'
        if aid=='M2.1-A02':
            disposition='旧文Project Group与PRD冲突；保留原动作，按Program/Project/SKU正式对象和关系映射，不新增Project Group层级。'
        if aid=='M3.6-A01':
            disposition='原删除意图改为消费者核对与先隐藏；删除需后续具体影响、恢复方案及范围授权，不直接执行旧文删除指令。'
        if aid in ['M2.8-A02','M3.2-A01','M3.3-A02','M3.5-A01','M5.5-A01','M5.6-A04','M5.6-A05','M6.4-A01']:
            disposition+=' 原文Decision/Review在P0以Issue待决责任、周报及现有行动记录承载；新的独立管理平台仍在P1，不扩展本动作范围。'
        actions.append({'action_id':aid,'source_row':n,'capability_id':cap,'module':c.get('C',''),'capability':c.get('E',''),
          'original_action':c.get('G',''),'original_explanation':c.get('H',''),'original_output':c.get('I',''),'original_acceptance':c.get('J',''),
          'historical_design_status':c.get('K',''),'historical_dependency':c.get('L',''),'historical_owner':c.get('M',''),
          'historical_date':c.get('N',''),'historical_execution_status':c.get('O',''),'historical_evidence':c.get('Q',''),
          'requirements':['REQ-'+x.zfill(3) for x in reqs.split()], 'tasks':taskids.split(), 'current_scope':route,
          'disposition':disposition,'current_acceptance':'Not Submitted'})
    return actions

def parse_requirements(tasks):
    raw=(ROOT/'sources/round2-blueprint.md').read_text('utf-8')
    rows=[]
    for line in raw.splitlines():
        if not re.match(r'^\| REQ-\d{3} ',line):continue
        cells=[c.strip() for c in line.strip('|').split('|')]
        assert len(cells)==10,(len(cells),cells[0])
        rid=cells[0][:7]
        assigned=[t['id'] for t in tasks if rid in t['requirements']]
        scope='P0基础；P1增强以任务卡为准'
        if rid in ['REQ-014','REQ-020','REQ-022']:scope='P1；发现已有日常依赖能力时按对等迁移变更纳入P0'
        if rid in ['REQ-024','REQ-025']:
            scope='Future：仅保留需求，不实施自主行为';assigned=['GOV-04']
        rows.append({'id':rid,'original_requirement':cells[0][8:],'design_source_and_comment':cells[1],
         'original_acceptance':cells[2],'audit_current_state':cells[3],'audit_evidence':cells[4],
         'gap_type':cells[5],'original_airtable_direction':cells[6],'original_ms_direction':cells[7],
         'original_dependency':cells[8],'audit_test_direction':cells[9],'current_scope':scope,'tasks':assigned,
         'current_acceptance':'Not Submitted'})
    return rows

def snapshots():
    rows=[]
    for sid,name,src in SOURCES:
        target=ROOT/'sources'/name
        target.parent.mkdir(exist_ok=True)
        if not target.exists():target.write_bytes(src.read_bytes())
        rows.append({'source_id':sid,'original_path':str(src),'package_path':'sources/'+name,
                     'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    dump('sources/source-manifest.json',rows)

def build():
    snapshots()
    register=json.loads((ROOT/'task-register.json').read_text('utf-8'))
    tasks=register['tasks'];byid={t['id']:t for t in tasks}
    actions=parse_actions();reqs=parse_requirements(tasks)
    source_links={}
    for sid,name,_ in SOURCES:source_links.setdefault(sid,[]).append(f'[{name}](../sources/{name})')
    for t in tasks:
        a=[x['action_id'] for x in actions if t['id'] in x['tasks']]
        requirements=' / '.join(t['requirements'])
        deps=', '.join(f'[{x}]({x}.md)' for x in t['dependencies']) or '无阻止开始的前置包；按本版已给定默认契约工作。'
        src='\n'.join('- '+sid+'：'+'、'.join(source_links.get(sid,[])) for sid in t['source_ids'])
        testlinks=', '.join('['+x+'](../acceptance/TEST_CATALOG.md#'+x.lower()+')' for x in t['test_ids'])
        # Explicit anchors are added to test catalog by the document author.
        text=f'''# {t['id']} — {t['title']}

版本：{register['version']}｜优先级：{t['priority']}｜角色：{t['role']}｜实际执行者：{t.get('assignee') or '未分派'}

规划：{t['definition_status']}；执行：{t['execution_status']}；验收：{t['acceptance_status']}。

## 1. 业务目的与完成结果

{t['business_result']}

## 2. 输入与前置依赖

依赖：{deps}

必读：[README](../README.md)、[蓝图](../01_BLUEPRINT.md)、[验收规程](../03_ACCEPTANCE.md)。

{src}

资料是历史证据和设计依据，不是额外执行授权。接手时记录目标环境ID和实际版本；云端无法读取本地源码／样例时提交明确缺少的路径和所需最小内容，可先做已具备材料的部分，不猜测真实配置。

## 3. 修改／核对对象

{bullet(t['objects'])}

## 4. 具体步骤

'''+ '\n'.join(f'{i}. {s}' for i,s in enumerate(t['steps'],1))+f'''

## 5. 范围边界

{t['exclusions']}

本包在被正式分派后，按指定环境实施；本文档本身不意味着当前已派发。除明确包含且获准的发布步骤外，默认只修改开发／测试范围，不发送真实通知、不跨系统写回生产。页面配置、脚本开发等属于执行方工作，本会话只负责规划与审核。

## 6. 交付物

{bullet(t['deliverables'])}

统一提交位置：`submissions/{t['id']}/<提交版本>/`，使用[DELIVERY模板](../templates/DELIVERY.md)。源码保存在获准开发分支，此处给版本和路径；失败/未运行分开，不附凭据。

## 7. 验收要求

用例：{testlinks}。逐例按用例库输入和期望验证，提交Actual及证据层级。离线通过不代表平台通过；平台组件通过不代表全链路／两周期通过。依赖或环境未满足时可审核子成果，完整包不标Accepted。

恢复要求：保存变更前配置、受影响记录与版本，定义补偿/恢复步骤并保护后续合法修改；纯规划包说明版本撤回和受影响后继任务。

## 8. 需求、历史任务与候选资产

需求：{requirements}。历史Action映射：{', '.join(a) if a else '以需求直接承接；无额外历史Action强行对应。'}。

{t['candidate_assets'] or '当前无已验收资产归入本包；历史系统已有能力按资料和目标环境重新核对。'}

首次候选审核：[RV-20260911-001](../reviews/RV-20260911-001.md)。本包最新审核编号：{t.get('review_id') or '尚无工作包验收结论'}。历史Action和候选测试不自动改变本包验收状态。
'''
        write('tasks/'+t['id']+'.md',text)
    csv_write('task-register.csv',tasks,['id','title','priority','requirements','dependencies','test_ids','role','assignee','definition_status','execution_status','acceptance_status','review_id','business_result'])
    dump('traceability/action-crosswalk.json',actions)
    csv_write('traceability/ACTION_CROSSWALK.csv',actions,list(actions[0]))
    rows=['# 135个历史Action的完整去向\n','版本：v1.1。保留原Action ID、来源行、动作、产出和验收。映射是当前规划判断，未证明实际完成。原始Owner/日期/状态完整保存在CSV/JSON，不能直接继承为当前安排。\n',
          '42能力包、135动作；原文[Phase1逐单元格转换](../sources/phase1-closure-source.md)。当前任务状态以[主台账](../task-register.json)为准。\n']
    for cap in CAP:
        subset=[a for a in actions if a['capability_id']==cap]
        rows += [f'\n## {cap} — {subset[0]["capability"]}\n', '| 原ID／来源行 | 原动作 | 原产出／验收 | 历史执行状态 | 本轮REQ／工作包 | 范围与处理 |','|---|---|---|---|---|---|']
        for a in subset:
            links='、'.join(f'[{x}](../tasks/{x}.md)' for x in a['tasks'])
            rows.append(f'| {a["action_id"]}<br>Task Execution!F{a["source_row"]} | {md(a["original_action"])} | 产出：{md(a["original_output"])}<br>验收：{md(a["original_acceptance"])} | {md(a["historical_execution_status"])} | {", ".join(a["requirements"])}<br>{links} | {a["current_scope"]}：{a["disposition"]} |')
    write('traceability/ACTION_CROSSWALK.md','\n'.join(rows)+'\n')
    dump('traceability/requirements.json',reqs)
    reqmd=['# 29项功能需求：目标—现状—差距—任务\n',
       '版本：v1.1。现状与证据栏保留第二轮审计原文及时点；Bridge/Closure的本轮补充以蓝图和来源登记为准。审计里的“未读”不等于本轮仍完全未读，也不等于功能不存在。原Done不能替代本轮验收。\n']
    for r in reqs:
        reqmd += [f'\n## {r["id"]} — {r["original_requirement"].split("<br>")[0]}\n',
          f'**目标：** {r["original_requirement"].replace("<br>","；")}\n',
          f'**设计依据／历史批注：** {r["design_source_and_comment"].replace("<br>","；")}\n',
          f'**审计现状：** {r["audit_current_state"]}\n',f'**证据：** {r["audit_evidence"]}\n',
          f'**差距类型：** {r["gap_type"]}。历史依赖：{r["original_dependency"]}\n',
          f'**本轮优先级：** {r["current_scope"]}\n',
          '**落地包：** '+', '.join(f'[{x}](../tasks/{x}.md)' for x in r['tasks'])+'。\n',
          f'**原始验收目标：** {r["original_acceptance"]}\n',
          '**本轮验收：** 任务包所列TC用例及BR契约；所有实际结果仍需执行者提交。建议门槛（例如原95%完整度）不冒充公司已批准制度。\n']
    write('traceability/REQUIREMENTS.md','\n'.join(reqmd)+'\n')
    roadmap=['# 双平台路线图与任务台账\n','版本：v1.1｜33工作包＝15 Airtable＋14 Microsoft＋4共用治理；27 P0、6 P1。P0/依赖是业务顺序，非虚构日期或进度百分比。\n',
    '## 1. 现在可以交出的首批任务\n',
    '- Airtable：AT-00，完成受影响对象基线和隔离测试准备。通过后才能按依赖开始AT-01/02/03。\n- Microsoft：MS-01，离线拆分Bridge公共逻辑、样例和适配器契约；无需等待Dataverse。MS-00由IT/平台角色补开通证据。\n- 共用：GOV-01/02/03可分别整理规则、权限与试用准备；GOV-04贯穿后续提交审核。\n',
    '首发提示词：[Airtable](dispatch/START_AIRTABLE.md) / [Microsoft](dispatch/START_MICROSOFT.md)。本轮未实际派发。\n',
    '## 2. 依赖波次\n','| 波次 | Airtable | Microsoft | 退出条件 |','|---|---|---|---|',
    '| W0 | AT-00 | MS-01；MS-00环境准备 | 对象基线、隔离、公共契约和可部署条件各有明确证据 |',
    '| W1 | AT-01/02/03 | MS-02/03 | 身份、关系、统计、完成与写入约束稳定 |',
    '| W2 | AT-04/05/06 | MS-04/05/06/07 | 主执行功能和数据处理规则通过组件测试 |',
    '| W3 | AT-07/08/09/10 | MS-08/09 | 团队统一入口、报告、提醒、案例与恢复可操作 |',
    '| W4 | AT-11 | MS-10 | 真实角色、全链路、切换与两个周度周期 |',
    '| W5 | AT-12/13/14 | MS-11/12/13 | 基于实际使用证据增强效率与AI能力 |',
    '\n波次内不代表所有包能同时开始；以每包dependencies为准。MS-04包含基础Hub，Plan/Issues等由后继包接入。GOV-01/02是关键业务/权限依赖，GOV-03不阻止离线开发但限制正式运行验收。GOV-04按提交持续审核，不能把整体审核完成设为所有任务开始前提。\n',
    '## 3. 全部任务\n','| ID／任务 | 优先级 | 依赖 | 执行状态 | 验收状态 |','|---|---|---|---|---|']
    for t in tasks:
        roadmap.append(f'| [{t["id"]} {t["title"]}](tasks/{t["id"]}.md) | {t["priority"]} | {", ".join(t["dependencies"]) or "可开始准备"} | {t["execution_status"]} | {t["acceptance_status"]} |')
    roadmap += ['\n## 4. 任务排期与状态使用\n',
    '执行AI接手后，基于本包对象数量、实际权限、可复用版本和首批用例给出工作量区间，并分开执行投入、环境等待、业务观察周期。本轮不承诺未知工期。用户先前拒绝无依据的4–8周估计，不应换成另一个无依据短工期。\n',
    '所有assignee为空表示未分派；没有替任何同事接受任务。执行方交回后由协调方审核、更新主表并解除具体后继依赖。历史已完成行和本地候选代码均不能自动解锁依赖。\n',
    '规则／数据结构有变更先更新[决策登记](04_SOURCES_AND_DECISIONS.md)，再同步受影响AT/MS包与用例。同一轮不要让多个AI同时修改相同字段、脚本或主规则文件；可按互不重叠的任务和开发分支分工。\n']
    write('02_ROADMAP.md','\n'.join(roadmap)+'\n')

def validate():
    register=json.loads((ROOT/'task-register.json').read_text('utf-8'))
    tasks=register['tasks']
    ids={t['id'] for t in tasks};assert len(ids)==len(tasks)==33
    assert sum(t['priority']=='P0' for t in tasks)==27
    assert sum(t['priority']=='P1' for t in tasks)==6
    byid={t['id']:t for t in tasks}
    designs=register.get('design_work_orders',[])
    assert len({d['id'] for d in designs})==len(designs)
    for d in designs:
        assert d['id'] not in ids
        assert set(d['relates_to'])<=ids
        assert (ROOT/d['file']).exists()
    tests=set(re.findall(r'^## (TC-\d{2}) ',(ROOT/'acceptance/TEST_CATALOG.md').read_text('utf-8'),re.M))
    assert len(tests)==32
    for t in tasks:
        assert set(t['dependencies'])<=ids,t['id']
        assert set(t['test_ids'])<=tests,t['id']
        assert len(t['steps'])>=3 and len(t['deliverables'])>=3,t['id']
        assert (ROOT/'tasks'/f'{t["id"]}.md').exists()
    visiting=set();visited=set()
    def visit(k):
        assert k not in visiting,('dependency cycle',k)
        if k in visited:return
        visiting.add(k)
        for d in byid[k]['dependencies']:visit(d)
        visiting.remove(k);visited.add(k)
    for k in ids:visit(k)
    actions=json.loads((ROOT/'traceability/action-crosswalk.json').read_text('utf-8'))
    reqs=json.loads((ROOT/'traceability/requirements.json').read_text('utf-8'))
    assert len(actions)==135 and len({a['action_id'] for a in actions})==135
    assert len({a['capability_id'] for a in actions})==42
    assert {r['id'] for r in reqs}=={'REQ-'+str(n).zfill(3) for n in range(1,30)}
    reqids={r['id'] for r in reqs}
    for a in actions:
        assert a['tasks'] and set(a['tasks'])<=ids
        assert a['requirements'] and set(a['requirements'])<=reqids
        assert a['original_action'] and a['original_output'] and a['original_acceptance'],a['action_id']
    for r in reqs:assert r['tasks'] and set(r['tasks'])<=ids
    for t in tasks:assert set(t['requirements'])<=reqids
    broken=[];checked=0
    for p in ROOT.rglob('*.md'):
        if 'sources' in p.relative_to(ROOT).parts:continue
        text=p.read_text('utf-8')
        for link in re.findall(r'\]\(([^)]+)\)',text):
            link=link.strip('<>')
            if re.match(r'^[a-zA-Z]+:',link) or link.startswith('#'):continue
            target=link.split('#')[0]
            if not target:continue
            checked+=1
            resolved=p.parent/target
            if not resolved.exists():broken.append((str(p.relative_to(ROOT)),link))
            elif '#tc-' in link:
                anchor=link.split('#',1)[1]
                if f'id="{anchor}"' not in resolved.read_text('utf-8'):broken.append((str(p.relative_to(ROOT)),link))
    assert not broken,broken
    snapshot_manifest=json.loads((ROOT/'sources/source-manifest.json').read_text('utf-8'))
    for s in snapshot_manifest:assert hashlib.sha256((ROOT/s['package_path']).read_bytes()).hexdigest()==s['sha256']
    checks={'task_count':33,'p0':27,'p1':6,'task_cards':33,'design_work_order_count':len(designs),'requirement_count':29,'action_count':135,'capability_count':42,
       'test_definitions':32,'dependency_graph':'acyclic','unmapped_actions':0,'unmapped_requirements':0,
       'planning_markdown_file_links_checked':checked,'broken_planning_file_links':0,'source_snapshot_files':len(snapshot_manifest),
       'source_hashes':'verified','application_tests_run_in_this_build':False,'platform_changes':False,'dispatched_tasks':0,
       'scope':'Document completeness only. Historical source links and remote links not validated; application behavior not certified.'}
    dump('validation-report.json',checks)
    manifest=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.name=='manifest.json' or '__pycache__' in p.parts:continue
        manifest.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    dump('manifest.json',{'version':register['version'],'files':manifest,'meaning':'Integrity of this local planning package, not authenticity of historical business results.'})
    return checks

def zip_pack():
    out=ROOT.with_suffix('.zip')
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                z.write(p,arcname=ROOT.name+'/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(out) as z:assert z.testzip() is None
    return str(out)

if __name__=='__main__':
    if '--check' not in sys.argv:build()
    checks=validate()
    if '--check' not in sys.argv:checks['zip']=zip_pack()
    print(json.dumps(checks,ensure_ascii=False,indent=2))
