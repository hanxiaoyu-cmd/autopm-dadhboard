import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {Window} from '../qa/node_modules/happy-dom/lib/index.js';
import * as domain from '../dist/model.js';
import * as defaults from '../dist/workflow-rules.js';
const root=fileURLToPath(new URL('../',import.meta.url));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'autopm-workspace-qa-'));
const child=spawn(process.execPath,['server.mjs'],{cwd:root,env:{...process.env,PORT:'0',AUTOPM_DATA_DIR:tmp},windowsHide:true,stdio:['ignore','pipe','pipe']});
let url='',err='';child.stdout.on('data',chunk=>{url=String(chunk).match(/http:\/\/127.0.0.1:\d+/)?.[0]||url;});child.stderr.on('data',c=>err+=c);
async function waitFor(fn,label,ms=8000){const start=Date.now();while(Date.now()-start<ms){if(fn())return;await new Promise(r=>setTimeout(r,20));}throw new Error('Timed out: '+label+' '+err);}
await waitFor(()=>url,'QA server');
const win=new Window({url,settings:{enableJavaScriptEvaluation:true,disableCSSFileLoading:true}});
const body=fs.readFileSync(path.join(root,'dist/index.html'),'utf8').replace(/<script[^>]*>[\s\S]*?<\/script>/g,'');win.document.write(body);
win.fetch=(input,init)=>fetch(new URL(input,url),init);win.scrollTo=()=>{};win.HTMLElement.prototype.scrollIntoView=function(){};win.__domain=domain;
const agentTools=new Map();Object.defineProperty(win.document,'modelContext',{value:{registerTool(t){agentTools.set(t.name,t);}}});
win.__defaults=defaults;
win.eval('var {done,taskStatus,person,project,activeIssue,tasksFor,STAGES}=globalThis.__domain;var {taskDefaults,selectableProjects,isClosedProject,issueRole}=globalThis.__defaults;');
win.eval(fs.readFileSync(path.join(root,'dist/simple-ui.js'),'utf8').replace(/^import.*$/gm,'').replace('export function createSimpleUI','function createSimpleUI')+'\nwindow.__createSimpleUI=createSimpleUI;');
win.eval(fs.readFileSync(path.join(root,'dist/app.js'),'utf8').replace("import {createSimpleUI} from './simple-ui.js';",'const createSimpleUI=globalThis.__createSimpleUI;').replace(/^import \{([^}]+)\} from '\.\/model.js';/m,'const {$1}=globalThis.__domain;'));
const q=sel=>win.document.querySelector(sel);
const txt=()=>q('#main')?.textContent||'';
const click=(action,id)=>{const el=q(`[data-action="${action}"]${id!==undefined?`[data-id="${id}"]`:''}`);assert(el,'Button missing: '+action+' '+(id||''));el.click();};
const set=(id,value)=>{if(id==='person-select'){click('people');const el=q('#people-search');el.value=value;el.dispatchEvent(new win.Event('input',{bubbles:true}));click('choose-person',value);return;}if(id==='role-select'){click('demo-settings');const el=q('#f-previewMode');el.value=value;submit();return;}const el=q('#'+id);assert(el,'Input missing: '+id);el.value=value;el.dispatchEvent(new win.Event('change',{bubbles:true}));};
const submit=()=>q('#detail-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));
const state=()=>fetch(url+'/api/state').then(r=>r.json());
await waitFor(()=>q('[data-action="people"]'),'initial render');
test.after(()=>{child.kill();win.happyDOM.abort();});

test('six centers render real relations, person switching and combined report filters',async()=>{
 assert(txt().includes('Good morning, Sun'));set('person-select','emily');assert(txt().includes('Good morning, Emily'));assert(txt().includes('Compliance'));
 for(const page of ['projects','portfolio','reports','support','department','mywork']){click('nav',page);assert(txt().trim().length>120,page+' is populated');assert(!txt().includes('being completed'));}
 click('nav','portfolio');const g=(await state()).programs[0];click('program',g.id);assert(txt().includes('SKU execution across projects'));const pid=(await state()).projects.find(p=>p.programId===g.id).id;click('project',pid);assert(txt().includes('Project brief'));
 for(const tab of ['plan','skus','issues','team','documents','history']){click('project-tab',tab);assert(q('#main').textContent.length>150);}
 click('nav','department');click('department-pick','Compliance');assert(txt().includes('Compliance Department'));click('report-department','Compliance');assert(txt().includes('Status Reports'));
 click('report-scope');const inputs=[...win.document.querySelectorAll('input[name="projectIds"]')];inputs[0].checked=true;inputs[1].checked=true;submit();await waitFor(()=>!q('.drawer'),'filter applied');assert(txt().includes('2 projects selected'));
});

test('task form persists fields, assessment follow-up links, technical results and full reload',async()=>{
 set('person-select','sun');click('nav','projects');const initial=await state(),t=initial.tasks.find(t=>t.kind==='Assessment'&&t.ownerIds.includes('sun'));click('project',t.projectId);click('project-tab','plan');click('task',t.id);
 set('f-outcome','QA: packaging unchanged; certification review required.');set('f-assessmentDecision','No Further Work');q('input[name="confirmOwnPart"]').checked=true;submit();await waitFor(()=>!q('.drawer'),'task saved');
 const savedTask=(await state()).tasks.find(x=>x.id===t.id);assert.equal(savedTask.outcome,'QA: packaging unchanged; certification review required.');assert(savedTask.completedBy.includes('sun'));
 click('task',t.id);set('f-outcome','QA: revised assessment requires certification.');click('simple-follow-up',t.id);await waitFor(()=>q('#drawer-title')?.textContent==='Plan the follow-up work','assessment saved before planning');assert(q('#f-brief').value.includes('revised assessment requires certification'));set('f-title','QA certification follow-up');submit();await waitFor(()=>q('#drawer-title')?.textContent==='QA certification follow-up','follow-up created');
 const after=await state(),created=after.tasks.find(x=>x.title==='QA certification follow-up');assert.deepEqual(created.sourceAssessmentIds,[t.id]);click('close');
 const testTask=after.tasks.find(x=>x.projectId===t.projectId&&x.kind==='Test');click('task',testTask.id);set('f-testResult','Fail');set('f-outcome','Completed test; sample failed.');submit();await waitFor(()=>!q('.drawer'),'test outcome saved');assert.equal((await state()).tasks.find(x=>x.id===testTask.id).testResult,'Fail');
 const disk=JSON.parse(fs.readFileSync(path.join(tmp,'state.json'),'utf8'));assert(disk.tasks.some(x=>x.title==='QA certification follow-up'));assert(fs.existsSync(path.join(tmp,'state.json.bak')));
});

test('issue creation, individual action, resolution and lesson reuse work from forms',async()=>{
 click('nav','support');click('new-issue');set('f-title','QA configuration obstacle');set('f-details','The sample configuration does not match the reviewed change list.');set('f-ownerId','sun');submit();await waitFor(()=>q('#drawer-title')?.textContent==='QA configuration obstacle','issue created');
 let st=await state();const issue=st.issues.find(i=>i.title==='QA configuration obstacle');click('new-action',issue.id);set('f-title','QA confirm the configuration');set('f-result','Aligned against RKO v2.');set('f-status','Done');submit();await waitFor(()=>q('#drawer-title')?.textContent===issue.title,'action saved');st=await state();assert(st.actions.some(a=>a.issueId===issue.id&&a.status==='Done'));assert.equal(st.issues.find(i=>i.id===issue.id).status,'Open');
 click('resolve-issue',issue.id);set('f-resolution','Configuration corrected and rechecked.');set('f-prevention','Add the sample configuration to the kickoff checklist.');submit();await waitFor(()=>q('#drawer-title')?.textContent===issue.title,'issue resolved');click('save-lesson',issue.id);set('f-title','QA configuration lesson');submit();await waitFor(()=>!q('.drawer'),'lesson saved');assert(txt().includes('QA configuration lesson'));
 const lesson=(await state()).lessons.find(l=>l.title==='QA configuration lesson');click('reuse-lesson',lesson.id);submit();await waitFor(()=>q('#drawer-title')?.textContent.startsWith('Prevent recurrence: QA'),'lesson task created');assert((await state()).tasks.some(t=>t.brief.includes(issue.id)&&t.title.includes('QA configuration lesson')));click('close');
});

test('project creation, team edit, document and SKU execution are functional',async()=>{
 click('nav','projects');click('new-project');set('f-id','QA-UI-01');set('f-name','QA UI project');set('f-factory','QA Factory');set('f-skuNames','QA-EU, QA-UK');set('f-scope','New color and certification change.');submit();await waitFor(()=>txt().includes('QA UI project')&&!q('.drawer'),'project created');
 let st=await state();assert.equal(st.tasks.filter(t=>t.projectId==='QA-UI-01').length,11);click('edit-project','QA-UI-01');set('f-summary','QA project update appears in reports.');set('f-health','At Risk');submit();await waitFor(()=>!q('.drawer'),'project updated');
 click('project-tab','documents');click('new-document','QA-UI-01');set('f-name','QA change brief');set('f-content','A documented local design example.');submit();await waitFor(()=>q('#drawer-title')?.textContent==='QA change brief','document created');assert(q('.document-content').textContent.includes('local design'));click('close');
 click('project-tab','skus');st=await state();const ps=st.projectSkus.find(p=>p.projectId==='QA-UI-01');click('sku',ps.id);set('f-status','At Risk');set('f-overrideDate','2026-11-20');set('f-overrideReason','QA market certification');submit();await waitFor(()=>!q('.drawer'),'SKU saved');assert.equal((await state()).projectSkus.find(x=>x.id===ps.id).overrideDate,'2026-11-20');
});

test('snapshot stays unchanged and viewer can filter but cannot edit',async()=>{
 click('report-project','QA-UI-01');click('save-report');set('f-title','QA frozen snapshot');submit();await waitFor(()=>q('#drawer-title')?.textContent==='QA frozen snapshot','snapshot saved');click('close');const report=(await state()).reports.find(r=>r.title==='QA frozen snapshot');assert.equal(report.rows.length,1);assert.equal(report.rows[0].summary,'QA project update appears in reports.');
 set('role-select','viewer');click('report-scope');assert(!q('input[name="projectIds"]').disabled);submit();await waitFor(()=>!q('.drawer'),'viewer scope applied');click('nav','projects');assert(!q('[data-action="new-project"]'));click('project','QA-UI-01');assert(!q('[data-action="edit-project"]'));click('project-tab','plan');const t=(await state()).tasks.find(t=>t.projectId==='QA-UI-01');click('task',t.id);assert(q('#f-title').disabled);assert(!q('button[type="submit"][form="detail-form"]'));click('close');set('role-select','contributor');
});

test('report export creates a durable, scoped CSV with a working file URL',async()=>{
 set('role-select','contributor');click('nav','reports');click('clear-report');click('report-scope');const inputs=[...win.document.querySelectorAll('input[name="projectIds"]')];inputs[0].checked=true;inputs[1].checked=true;submit();await waitFor(()=>!q('.drawer'),'export scope selected');click('export-report');await waitFor(()=>q('#drawer-title')?.textContent==='Your file is ready','export generated');
 const href=q('a[download]').getAttribute('href'),response=await fetch(url+href),csv=await response.text();assert.equal(response.status,200);assert(response.headers.get('content-disposition').includes('attachment'));assert.equal(csv.trim().split('\r\n').length,3);assert(csv.includes('XSXA80183')&&csv.includes('XSXA80514'));assert(fs.existsSync(path.join(tmp,'exports',decodeURIComponent(href.split('/').at(-1)))));
 const rejected=await fetch(url+'/api/export',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'../outside.txt',content:'bad path'})});assert.equal(rejected.status,400);click('close');
});

test('optimistic concurrency rejects stale writes without overwriting saved state',async()=>{
 const current=await state(),req={type:'updateProject',id:current.projects[0].id,values:{summary:'Concurrent writer'},actorId:'sun',mode:'maintainer',revision:current.revision};
 let res=await fetch(url+'/api/operation',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(req)});assert.equal(res.status,200);
 req.values.summary='Stale overwrite';res=await fetch(url+'/api/operation',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(req)});assert.equal(res.status,409);assert.equal((await state()).projects[0].summary,'Concurrent writer');
});

test('optional WebMCP registration has the expected contract (mock context only)',async()=>{
 assert.deepEqual([...agentTools.keys()],['autopm_list_current_work','autopm_open_project','autopm_update_task_outcome']);
 const result=agentTools.get('autopm_list_current_work').execute({});assert.equal(result.person,'sun');assert(Array.isArray(result.tasks));
 assert.throws(()=>agentTools.get('autopm_open_project').execute({projectId:'DOES-NOT-EXIST'}),/Unknown/);
 assert.throws(()=>agentTools.get('autopm_list_current_work').execute({unexpected:true}),/Invalid tool input/);
 assert.throws(()=>agentTools.get('autopm_open_project').execute({projectId:42}),/Invalid tool input/);
 assert.throws(()=>agentTools.get('autopm_update_task_outcome').execute({taskId:'t-0-0'}),/Invalid tool input/);
});
