// Defaults support the form; they never infer a result, approval or completion.
export const isClosedProject=p=>['Closed','Cancelled'].includes(p?.lifecycle);
export function taskDefaults(s,{projectId,actorId,title='',sourceAssessmentIds=[]}){
 const p=s.projects.find(p=>p.id===projectId),source=s.tasks.find(t=>t.id===sourceAssessmentIds[0]);
 const team=new Set([...(p?.team||[]),p?.leadId]);
 const words=title.toLowerCase();
 const kind=source?'Execution':/\b(assess(?:ment)?|evaluate|evaluation)\b/.test(words)?'Assessment':/\becn\b/.test(words)?'Approval':/\b(test|testing|retest)\b/.test(words)&&!(/\b(prepare|preparation|sample|plan|schedule)\b/.test(words))?'Test':'Execution';
 const areaRules=[['Packaging',/packag/],['Compliance',/certification|compliance/],['EE',/firmware|software|\bee\b|pcba/],['CMF / ID',/\bcmf\b|colour|color/],['Tooling',/mould|mold|tooling/],['DQTP',/dqtp|drop test/],['ME',/production line|assembly line/],['SC',/cost|sourcing/]];
 return {kind,phase:kind==='Assessment'?'Assessment & Planning':kind==='Approval'?(p?.stage==='ECN DD Review'?'ECN DD Review':'ECN IMP Review'):(p?.stage||'Execution & Testing'),workstream:source?.workstream||areaRules.find(([,pattern])=>pattern.test(words))?.[0]||s.people.find(x=>x.id===actorId)?.department||'Unassigned',ownerIds:source?source.ownerIds.filter(id=>team.has(id)):team.has(actorId)?[actorId]:[]};
}
export function selectableProjects(s,personId,{includeClosed=false}={}){
 const assigned=new Set(s.tasks.filter(t=>t.ownerIds.includes(personId)).map(t=>t.projectId));
 return s.projects.filter(p=>(includeClosed||!isClosedProject(p))&&(p.leadId===personId||p.team?.includes(personId)||assigned.has(p.id)));
}
export function issueRole(s,issue,actorId){
 const pm=s.projects.find(p=>p.id===issue.projectId)?.leadId;
 if(issue.status==='Pending Verification'&&(issue.verifierId||pm)===actorId)return {label:'Waiting for your confirmation',action:'review-issue',button:'Review resolution'};
 if(issue.ownerId===actorId)return {label:issue.status==='Pending Verification'?'Submitted for confirmation':'You are coordinating this issue',action:'issue',button:'Open issue'};
 const action=s.actions.find(a=>a.issueId===issue.id&&a.ownerId===actorId&&!['Done','Cancelled'].includes(a.status));
 if(action)return {label:'Your recovery action is outstanding',action:'action',id:action.id,button:'Update my action'};
 if(pm===actorId)return {label:'An issue in your project',action:'issue',button:'View issue'};
 return {label:'Affects your project work',action:'issue',button:'View impact'};
}
