import csv, json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root.parent / 'program-mvp' / 'import'
def rows(name):
    with (source / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))
people = [
 ('sun','Sun Sun','NPI','Project lead'),('alan','Alan Han','NPD','Engineering lead'),
 ('maya','Maya Chen','Packaging','Packaging engineer'),('leo','Leo Wang','EE','EE engineer'),
 ('rachel','Rachel Lin','DQTP','Test engineer'),('emily','Emily Xu','Compliance','Compliance engineer'),
 ('jason','Jason Wu','CMF / ID','CMF engineer'),('kevin','Kevin Liu','Tooling','Tooling engineer'),
 ('grace','Grace Zhao','ME','Manufacturing engineer'),('sophie','Sophie Li','SC','Sourcing lead'),
 ('daniel','Daniel Zhang','Factory','Factory coordinator'),('nina','Nina Zhou','PMO','Portfolio viewer')]
people=[dict(id=i,name=n,department=d,role=r) for i,n,d,r in people]
rawp=rows('AutoPM_Projects.csv'); rawg=rows('AutoPM_Programs.csv'); links=rows('AutoPM_ProgramProjects.csv')
prog_by_proj={r['ProjectKey']:r['ProgramKey'] for r in links}
programs=[dict(id=r['ProgramKey'],name=r['Title'],code=r['ProgramCode'],brand=r['Brand'],category=r['Category'],status=r['ProgramStatus'],source='Airtable export: identity') for r in rawg]
for i,(n,c,b,cat) in enumerate([('FA300 Refresh','FA360','Shark','Home Environment'),('Dirt Hunter Prime','DH100','Shark','Floorcare'),('Prada2','HD400','Shark','Beauty / Personal Care'),('Stainforce Pro','SF200','Shark','Floorcare')]):
 programs.append(dict(id=f'pg-demo-{i}',name=n,code=c,brand=b,category=cat,status='Committed',source='Program name from user reference; demo relationships'))
chosen=[]
for pg in rawg:
 candidates=[r for r in rawp if prog_by_proj.get(r['ProjectKey'])==pg['ProgramKey']]
 candidates.sort(key=lambda r:(r['Title']==r['ProjectKey'],r['ProjectKey']))
 chosen.extend(candidates[:3])
stages=['Assessment & Planning','ECN DD Review','Execution & Testing','ECN IMP Review','MP']
projects=[]
for i,r in enumerate(chosen):
 projects.append(dict(id=r['ProjectKey'],name=r['Title'],programId=prog_by_proj[r['ProjectKey']],source='Airtable export: identity and scope; execution is illustrative'))
for i,pg in enumerate(programs[2:]):
 for j in range(2): projects.append(dict(id=f'DEMO-{i+1:02}-{j+1}',name=f'{pg["code"]} {"EU / UK extension" if j==0 else "new colorway"}',programId=pg['id'],source='Illustrative project'))
for i,p in enumerate(projects):
 p.update(stage=stages[i%5],health=['On Track','At Risk','Delayed','On Track','On Track'][i%5],leadId='sun' if i%2==0 else 'alan',factory=['Yueda','Curio','Partner factory'][i%3],type=['Extension','New CMF','NPD'][i%3],priority='High' if i%3==0 else 'Normal',targetMP=f'2026-{10+i//10:02}-{15+i%12:02}',summary=['Department assessments are being consolidated. Confirm the sample plan before freezing the schedule.','Certification evidence is the next decision point. The team is tracking recovery and the ECN response.','Design inputs are agreed. Follow the active plan and keep test results separate from completion.'][i%3],scope='Confirm the market extension and product changes against RKO v2. Coordinate packaging, certification, EE, tooling and factory readiness.',team=[x['id'] for x in people if x['id']!='nina'],documentIds=[],updatedAt='2026-09-14T08:00:00+08:00')
skus=[]; projectSkus=[]; sr={s['SkuKey']:s for s in rows('AutoPM_SKUs.csv')}; sl=rows('AutoPM_ProjectSKUs.csv')
for i,p in enumerate(projects):
 real=[sr[x['SkuKey']] for x in sl if x['ProjectKey']==p['id'] and x['SkuKey'] in sr][:3]
 if not real:
  pg=next(g for g in programs if g['id']==p['programId'])
  real=[dict(SkuKey=f'sku-{i}-{j}',Title=f'{pg["code"]}{suffix}',Market=market) for j,(suffix,market) in enumerate([('EUSD','EU'),('UKSD','UK')])]
 for j,r in enumerate(real):
  sku=next((s for s in skus if s['id']==r['SkuKey']),None)
  if not sku:
   sku=dict(id=r['SkuKey'],name=r['Title'],market=r.get('Market') or ('EU' if j%2==0 else 'UK'),programId=p['programId']);skus.append(sku)
  projectSkus.append(dict(id=f'ps-{i}-{j}',projectId=p['id'],skuId=sku['id'],status='In Development' if p['stage']!='MP' else 'In MP',active=True,overrideDate=f'2026-11-{15+j:02}' if i==2 and j==1 else '',overrideReason='Market-specific certification window' if i==2 and j==1 else ''))
templates=[('Packaging change assessment','maya','Packaging'),('CMF / ID change assessment','jason','CMF / ID'),('DQTP test scope assessment','rachel','DQTP'),('EE change assessment','leo','EE'),('Compliance impact assessment','emily','Compliance'),('Tooling assessment','kevin','Tooling'),('3D / 2D design assessment','alan','NPD'),('Production line assessment','grace','ME'),('Cost and supplier assessment','sophie','SC'),('Factory production readiness','daniel','Factory')]
tasks=[];documents=[]
for i,p in enumerate(projects):
 kinds=[('Review RKO and change PPT',p['leadId'],'NPI','Assessment')]+[(n,o,d,'Assessment') for n,o,d in templates]+[('ECN DD approval',p['leadId'],'NPI','Approval'),('Prepare EB sample build','daniel','Factory','Execution'),('DQTP validation','rachel','DQTP','Test'),('Certification test and report','emily','Compliance','Test'),('ECN IMP approval',p['leadId'],'NPI','Approval')]
 for k,(title,owner,department,kind) in enumerate(kinds):
  tid=f't-{i}-{k}'
  done=(i%5>1 and k<11) or (i%5==4) or (i==0 and k in [1,3,7])
  owners=[owner,'alan'] if i==0 and k==0 else [owner]
  due=f'2026-09-{[14,10,15,16,17,18,21,23][(i+k)%8]:02}'
  tasks.append(dict(id=tid,projectId=p['id'],title=title,ownerIds=owners,completedBy=owners[:] if done else [],workstream=department,kind=kind,phase='Assessment & Planning' if k<11 else 'ECN DD Review' if k==11 else 'Execution & Testing' if k<15 else 'ECN IMP Review',start='2026-09-08',due=due,priority='High' if k in [0,11,14,15] else 'Normal',brief=f'Review the {department} change scope against RKO v2 and Change PPT v2. Confirm prerequisites, required work, resources and deliverables.',outcome='Reviewed the available inputs; follow-up work is included in the plan.' if done else '',assessmentDecision='Further Work Required' if done and kind=='Assessment' else 'Needs Information' if k==4 and i%3==0 else '',testResult='Pass' if done and kind=='Test' else 'Not Reported',approvalStatus='Approved' if done and kind=='Approval' else 'In Review' if kind=='Approval' else '',approvalDate='2026-09-11' if done and kind=='Approval' else '',predecessorIds=[f't-{i}-{12}'] if k in [13,14] else [f't-{i}-11'] if k==12 else [f't-{i}-13',f't-{i}-14'] if k==15 else [],sourceAssessmentIds=[f't-{i}-{3 if k==13 else 5}'] if k in [13,14] else [],duration=4 if k==14 else 5,durationBasis='Working Days',deliverableId=f'doc-{i}-test' if kind=='Test' else f'doc-{i}-change' if kind=='Assessment' else f'doc-{i}-ecn' if kind=='Approval' else f'doc-{i}-sample',updatedAt='2026-09-14T08:00:00+08:00'))
 for typ,name in [('rko','RKO input brief'),('change','Change PPT and department assessments'),('sample','Sample plan · EB1'),('test','Test report package'),('ecn','ECN approval record')]:
  did=f'doc-{i}-{typ}';p['documentIds'].append(did)
  content=f'{name}\nProject: {p["id"]} · {p["name"]}\nVersion: v2\n\nILLUSTRATIVE DOCUMENT — not an actual engineering release or approval.\n\nScope: market extension and change review.\nOwner: project team.\nNext step: review the corresponding task and record the actual outcome.\n'
  if typ=='sample':content+='\nSample requirements (illustrative):\nDQTP: 10 EU units, EB1 configuration.\nCompliance: 4 UK units, certification configuration.\nFactory must confirm whether reuse is possible; do not simply add these quantities.\n'
  documents.append(dict(id=did,projectId=p['id'],name=name,version='v2',type=typ,content=content,updated='2026-09-11',ownerId=p['leadId']))
issues=[];actions=[];lessons=[]
names=[('Certification sample configuration mismatch','Compliance','emily','High'),('Color standard is awaiting US confirmation','CMF / ID','jason','Medium'),('Drop test identified housing cracks','DQTP','rachel','Critical'),('Packaging matrix contains an obsolete SKU','Packaging','maya','High'),('EB fixture is not ready for the build','ME','grace','High'),('Supplier lead time exceeds the build window','SC','sophie','Medium'),('EE test firmware version mismatch','EE','leo','Medium'),('Artwork specification was inconsistent','Packaging','maya','Medium')]
for i,(title,department,owner,severity) in enumerate(names):
 p=projects[i%len(projects)];iid=f'ISS-DEMO-{i+1:03}';closed=i>=6
 issues.append(dict(id=iid,projectId=p['id'],title=title,details='Illustrative scenario: a difference was found between the agreed input and the material available to the team. Record the observed facts and avoid assuming a root cause.',department=department,ownerId=owner,severity=severity,status='Closed' if closed else 'In Recovery' if i%2==0 else 'Open',category=['Technical','Input / Documentation','Supplier / Resource'][i%3],impact='Blocks the next review until the required evidence is available.',impactMP=i in [0,2,4],due=f'2026-09-{12+i:02}',occurred='2026-09-09',phase=p['stage'],rootCause='The version reference was not included in the handover checklist.' if closed else '',resolution='Aligned the source version, repeated the affected review and confirmed the corrected result.' if closed else '',closedDate='2026-09-12' if closed else '',prevention='Include source version and SKU scope in the next kickoff checklist.' if closed else '',affectedProjectSkuIds=[s['id'] for s in projectSkus if s['projectId']==p['id']][:1],relatedTaskIds=[t['id'] for t in tasks if t['projectId']==p['id'] and t['workstream']==department][:1],updatedAt='2026-09-14T08:00:00+08:00'))
 for k,txt in enumerate(['Confirm the exact requirement and source version','Coordinate the correction with the responsible team','Review the result and record the remaining impact']):
  actions.append(dict(id=f'act-{i}-{k}',issueId=iid,title=txt,ownerId=owner if k<2 else p['leadId'],due=f'2026-09-{13+i+k:02}',status='Done' if closed or k==0 else 'Open',result='Source version confirmed with the team.' if closed or k==0 else '',evidenceUrl='',formalTaskId=''))
 if closed:lessons.append(dict(id=f'lesson-{i}',issueId=iid,title=f'Check the source version before {department.lower()} handover',department=department,category='Handover quality',summary=issues[-1]['prevention'],created='2026-09-12',useCount=0))
seed=dict(version=1,revision=0,scenarioDate='2026-09-14',people=people,programs=programs,projects=projects,skus=skus,projectSkus=projectSkus,tasks=tasks,issues=issues,actions=actions,documents=documents,lessons=lessons,reports=[],history=[],sourceNote='Program and selected project/SKU identities reuse local Airtable export files. Assignments, dates, status, issues, documents and outcomes are illustrative design scenarios; no live Airtable writes.')
(root/'data').mkdir(parents=True,exist_ok=True)
(root/'data/seed.json').write_text(json.dumps(seed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:len(seed[k]) for k in ['people','programs','projects','skus','projectSkus','tasks','issues','actions','documents']},ensure_ascii=False))
