import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {applyOperation,done,projectMetrics,reportRows} from '../dist/model.js';
const seed=JSON.parse(fs.readFileSync(new URL('../data/seed.json',import.meta.url),'utf8'));
const act=(s,type,id,values={},actorId='sun',mode='contributor')=>applyOperation(s,{type,id,values,actorId,mode});
test('seed relationships cover all six centers without dangling references',()=>{
 assert.equal(seed.programs.length,6);assert.equal(seed.projects.length,14);
 const projectIds=new Set(seed.projects.map(x=>x.id)),personIds=new Set(seed.people.map(x=>x.id)),taskIds=new Set(seed.tasks.map(x=>x.id)),issueIds=new Set(seed.issues.map(x=>x.id));
 for(const t of seed.tasks){assert(projectIds.has(t.projectId));t.ownerIds.forEach(p=>assert(personIds.has(p)));[...t.predecessorIds,...t.sourceAssessmentIds].forEach(id=>assert(taskIds.has(id)));}
 for(const i of seed.issues){assert(projectIds.has(i.projectId));i.affectedProjectSkuIds.forEach(id=>assert.equal(seed.projectSkus.find(x=>x.id===id).projectId,i.projectId));}
 seed.actions.forEach(a=>assert(issueIds.has(a.issueId)&&personIds.has(a.ownerId)));
 assert.equal(new Set(seed.projectSkus.map(ps=>ps.projectId+'|'+ps.skuId)).size,seed.projectSkus.length);
});
test('confirming a multi-owner task keeps all views tied to the same record',()=>{
 let s=structuredClone(seed);const t=s.tasks.find(t=>t.ownerIds.length===2);assert(t);t.completedBy=[];
 s=act(s,'confirmTask',t.id,{},t.ownerIds[0]).state;assert(!done(s.tasks.find(x=>x.id===t.id)));
 s=act(s,'confirmTask',t.id,{},t.ownerIds[1]).state;assert(done(s.tasks.find(x=>x.id===t.id)));
 assert.equal(reportRows(s,{projectIds:[t.projectId]})[0].done,projectMetrics(s,t.projectId).done);
 assert.throws(()=>act(s,'confirmTask',t.id,{},'nina'),/Only a listed owner/);
});
test('assessment can finish without requiring follow-up; test completion can retain Fail',()=>{
 let s=structuredClone(seed);let a=s.tasks.find(t=>t.kind==='Assessment'&&!done(t));
 s=act(s,'updateTask',a.id,{assessmentDecision:'No Further Work',outcome:'No packaging change is required.'}).state;
 const before=s.tasks.length;s=act(s,'confirmTask',a.id,{},a.ownerIds[0]).state;assert.equal(s.tasks.length,before);
 let t=s.tasks.find(t=>t.kind==='Test');s=act(s,'updateTask',t.id,{testResult:'Fail',outcome:'Housing cracked during the drop test.'}).state;
 if(!done(s.tasks.find(x=>x.id===t.id)))s=act(s,'confirmTask',t.id,{},t.ownerIds[0]).state;
 assert.equal(s.tasks.find(x=>x.id===t.id).testResult,'Fail');assert(done(s.tasks.find(x=>x.id===t.id)));
});
test('follow-up task traces to assessment and rejects cross-project links or cycles',()=>{
 let s=structuredClone(seed);const a=s.tasks.find(t=>t.kind==='Assessment');const r=act(s,'createTask','',{projectId:a.projectId,title:'New certification',ownerIds:['emily'],sourceAssessmentIds:[a.id],predecessorIds:[a.id],start:'2026-09-14',due:'2026-09-18'});s=r.state;
 assert.deepEqual(s.tasks.find(t=>t.id===r.id).sourceAssessmentIds,[a.id]);
 assert.throws(()=>act(s,'updateTask',a.id,{predecessorIds:[r.id]}),/cycle/);
 const foreign=s.tasks.find(t=>t.projectId!==a.projectId);assert.throws(()=>act(s,'updateTask',r.id,{predecessorIds:[foreign.id]}),/this project/);
 assert.throws(()=>act(s,'updateTask',r.id,{due:'2026-08-01'}),/before/);
});
test('issue actions remain separate; issue resolution, lesson and reuse retain lineage',()=>{
 let s=structuredClone(seed),i=s.issues.find(active=>active.status!=='Closed');const count=s.tasks.length;
 const r=act(s,'createAction','',{issueId:i.id,title:'Re-check samples',ownerId:'rachel',due:'2026-09-18'});s=r.state;assert.equal(s.tasks.length,count);
 s=act(s,'updateAction',r.id,{status:'Done',result:'Checked against the agreed configuration.'}).state;assert.notEqual(s.issues.find(x=>x.id===i.id).status,'Closed');
 assert.throws(()=>act(s,'updateIssue',i.id,{status:'Closed',resolution:''}),/resolution/);
 assert.throws(()=>act(s,'updateIssue',i.id,{status:'Closed',resolution:'Corrected and retested.'}),/remaining recovery actions/);
 for(const a of s.actions.filter(a=>a.issueId===i.id&&!['Done','Cancelled'].includes(a.status)))s=act(s,'updateAction',a.id,{status:'Done',result:'Confirmed result.'}).state;
 s=act(s,'updateIssue',i.id,{status:'Closed',resolution:'Corrected and retested.',prevention:'Confirm the sample configuration at kickoff.'}).state;
 const l=act(s,'saveLesson','',{issueId:i.id,title:'Sample version check',summary:'Confirm the sample configuration at kickoff.'});s=l.state;
 const reuse=act(s,'reuseLesson',l.id,{projectId:s.projects[1].id});s=reuse.state;assert(s.tasks.find(t=>t.id===reuse.id).brief.includes(i.id));assert.equal(s.lessons.find(x=>x.id===l.id).useCount,1);
 s=act(s,'updateIssue',i.id,{status:'In Recovery'}).state;assert.equal(s.issues.find(x=>x.id===i.id).closedDate,'');assert(s.history.some(x=>x.label.includes('Closed → In Recovery')));
});
test('saved report is immutable after project updates, and combined scope filters intersect',()=>{
 let s=structuredClone(seed);const p=s.projects[0],snap=act(s,'saveReport','',{title:'Status before edit',filter:{projectIds:[p.id]}});s=snap.state;
 const initial=s.reports[0].rows[0].summary;s=act(s,'updateProject',p.id,{summary:'Newer live update',health:'At Risk'}).state;
 assert.equal(s.reports[0].rows[0].summary,initial);assert.equal(reportRows(s,{projectIds:[p.id]})[0].summary,'Newer live update');
 const unrelated=s.programs.find(g=>g.id!==p.programId);assert.equal(reportRows(s,{projectIds:[p.id],programId:unrelated.id}).length,0);
});
test('same SKU in multiple projects has isolated execution dates',()=>{
 let s=structuredClone(seed);let ps=s.projectSkus.find(a=>s.projectSkus.some(b=>b.id!==a.id&&b.skuId===a.skuId));assert(ps,'seed must include multi-project SKU example');const other=s.projectSkus.find(x=>x.id!==ps.id&&x.skuId===ps.skuId),date=other.overrideDate;
 assert.throws(()=>act(s,'updateSku',ps.id,{overrideDate:'2026-11-01',overrideReason:''}),/Explain/);
 s=act(s,'updateSku',ps.id,{overrideDate:'2026-11-01',overrideReason:'Country certification'}).state;
 assert.equal(s.projectSkus.find(x=>x.id===other.id).overrideDate,date);
});
test('new project has independent assessments and unique identity; viewer cannot mutate',()=>{
 const r=act(seed,'createProject','',{id:'QA-PROJECT',name:'Design trial',programId:seed.programs[0].id,leadId:'sun',factory:'Demo factory',skuNames:'QA-EU, QA-UK',applyTemplate:true});
 assert.equal(r.state.tasks.filter(t=>t.projectId==='QA-PROJECT').length,11);assert.equal(r.state.projectSkus.filter(ps=>ps.projectId==='QA-PROJECT').length,2);
 assert.throws(()=>act(r.state,'createProject','',{id:'QA-PROJECT'}),/unique/);
 assert.throws(()=>act(seed,'updateProject',seed.projects[0].id,{summary:'No'},'nina','viewer'),/read only/);
});
