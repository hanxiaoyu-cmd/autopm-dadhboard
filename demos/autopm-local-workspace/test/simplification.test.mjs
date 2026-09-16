import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {applyOperation,done,taskStatus} from '../dist/model.js';
import {taskDefaults,selectableProjects} from '../dist/workflow-rules.js';
import {expandSample} from '../tools/scale-sample.mjs';
const seed=JSON.parse(fs.readFileSync(new URL('../data/seed.json',import.meta.url),'utf8'));
const act=(s,id,values,actorId='sun')=>applyOperation(s,{type:'updateIssue',id,values,actorId,mode:'contributor'});
test('automatic defaults distinguish assessment, sample preparation, testing, ECN and unknown work',()=>{
 const spec={projectId:seed.projects[0].id,actorId:'sun'};
 for(const [title,kind] of [['EE test assessment','Assessment'],['Prepare test samples','Execution'],['Drop test','Test'],['ECN DD review','Approval'],['Supplier meeting','Execution']])assert.equal(taskDefaults(seed,{...spec,title}).kind,kind,title);
 const result=applyOperation(seed,{type:'createTask',values:{...spec,title:'EE change assessment',start:'2026-09-14',due:'2026-09-17'},actorId:'sun',mode:'contributor'});
 const t=result.state.tasks.find(t=>t.id===result.id);assert.equal(t.kind,'Assessment');assert.equal(t.phase,'Assessment & Planning');assert.equal(t.assessmentDecision,'');assert.equal(t.completedBy.length,0);
});
test('unknown project roles stay unassigned instead of assigning a random person or all employees',()=>{
 const r=applyOperation(seed,{type:'createProject',values:{id:'TEST-SMALL-TEAM',name:'Small team',factory:'Example',programId:seed.programs[0].id,leadId:'sun'},actorId:'sun',mode:'contributor'});
 const p=r.state.projects.find(p=>p.id===r.id);assert.deepEqual(p.team,['sun']);
 const tasks=r.state.tasks.filter(t=>t.projectId===p.id);assert(tasks.filter(t=>t.workstream!=='NPI').every(t=>t.ownerIds.length===0));assert(tasks.every(t=>!done(t)));
});
test('scale fixtures are additive and idempotent with diverse relationships and closed residual work',()=>{
 const s=expandSample(seed);assert(s.people.length>1000&&s.projects.length>100&&s.tasks.length>4000);
 assert.deepEqual(s.projects.slice(0,seed.projects.length),seed.projects);assert.deepEqual(s.tasks.slice(0,seed.tasks.length),seed.tasks);assert.deepEqual(expandSample(s),s);
 const projectIds=new Set(s.projects.map(x=>x.id)),peopleIds=new Set(s.people.map(x=>x.id)),taskIds=new Set(s.tasks.map(x=>x.id));
 for(const t of s.tasks){assert(projectIds.has(t.projectId));assert(t.ownerIds.every(id=>peopleIds.has(id)));assert(t.predecessorIds.every(id=>taskIds.has(id)));}
 assert.equal(new Set(s.tasks.map(t=>t.id)).size,s.tasks.length);
 const projects=selectableProjects(s,'sim-person-0');assert(projects.length>10);assert(projects.every(p=>!['Closed','Cancelled'].includes(p.lifecycle)));
 const closed=s.projects.find(p=>p.id==='SIM-0001');assert(s.tasks.some(t=>t.projectId===closed.id&&t.ownerIds.includes('sun')&&!done(t)));
 const sunIssues=s.issues.filter(i=>s.projects.find(p=>p.id===i.projectId).leadId==='sun');assert(new Set(sunIssues.map(i=>i.title)).size>3);assert(new Set(sunIssues.map(i=>i.status)).size>=3);
});
test('closed projects reject new work and planned start dates do not claim actual start',()=>{
 const s=expandSample(seed);assert.throws(()=>applyOperation(s,{type:'createTask',values:{projectId:'SIM-0001',title:'New work',start:'2026-09-14',due:'2026-09-16'},actorId:'sun',mode:'contributor'}),/Reopen/);
 assert.equal(taskStatus({ownerIds:['sun'],completedBy:[],start:'2026-09-01',due:'2026-09-20'},'2026-09-14'),'Scheduled');
});
test('issue owner submits, wrong reviewer is rejected, return/close/reopen retain results and identities',()=>{
 let s=expandSample(seed),i=s.issues.find(i=>i.id==='sim-issue-6');
 assert.throws(()=>act(s,i.id,{status:'Closed'},'alan'),/Only the project lead/);
 assert.throws(()=>act(s,i.id,{status:'In Recovery'},'sun'),/Describe/);
 s=act(s,i.id,{status:'In Recovery',returnReason:'Retest evidence needed.'},'sun').state;
 s=act(s,i.id,{status:'Pending Verification',resolution:'Retest passed.'},i.ownerId).state;
 assert.equal(s.issues.find(x=>x.id===i.id).submittedBy,i.ownerId);
 s=act(s,i.id,{status:'Closed'},'sun').state;assert.equal(s.issues.find(x=>x.id===i.id).closedBy,'sun');
 s=act(s,i.id,{status:'In Recovery'},'sun').state;assert.equal(s.issues.find(x=>x.id===i.id).closedDate,'');
 assert(s.history.some(h=>h.entityId===i.id&&h.status==='Closed'&&h.actorId==='sun'&&h.resolution==='Retest passed.'));
});
