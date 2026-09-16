// Deterministic, additive local simulation. Never replaces existing business records.
export function expandSample(original){
 const s=structuredClone(original);if(s.sampleExpansion===1)return s;
 const areas=['NPI','Packaging','CMF / ID','DQTP','EE','Compliance','Tooling','NPD','ME','SC','Factory','PMO'];
 const given=['Alex','Jamie','Morgan','Taylor','Robin','Casey','Jordan','Sam','Chris','Avery'];
 const last=['Chen','Wang','Li','Zhang','Liu','Sun','Wu','Xu','Han','Zhou'];
 for(let n=0;n<1050;n++)s.people.push({id:`sim-person-${n}`,name:n===0?'Song Li':`${given[n%10]} ${last[Math.floor(n/10)%10]}`,department:areas[n%12],role:n%12===0?'Project lead':'Engineer',email:`sim.${String(n).padStart(4,'0')}@example.invalid`,sample:true});
 const leads=['sun','alan','sim-person-0','sim-person-12','sim-person-24','sim-person-36'];
 const names=['Cordless vacuum','Air purifier','Coffee system','Hair dryer','Wet cleaner','Food processor','Robot vacuum','Blender'];
 const plans=[['Assess packaging change','Assessment','Packaging'],['Review certification impact','Assessment','Compliance'],['Evaluate firmware change','Assessment','EE'],['Prepare color samples','Execution','CMF / ID'],['Update enclosure drawing','Execution','NPD'],['Prepare test samples','Execution','DQTP'],['Drop test','Test','DQTP'],['Firmware regression test','Test','EE'],['Confirm tooling readiness','Execution','Tooling'],['Review line readiness','Assessment','ME'],['ECN DD review','Approval','NPI'],['ECN IMP release','Approval','NPI'],['Confirm supplier schedule','Execution','SC'],['Pilot assembly','Execution','Factory'],['Finalize packaging artwork','Execution','Packaging'],['Review RKO changes','Assessment','NPI'],['Confirm component cost','Execution','SC'],['Electrical safety test','Test','Compliance'],['Prepare production instructions','Execution','ME'],['Archive release drawings','Execution','NPD'],['Evaluate UI update','Assessment','EE'],['Verify sample configuration','Execution','DQTP'],['Confirm market SKU scope','Execution','NPI'],['Approve color sample','Execution','CMF / ID']];
 const date=offset=>new Date(Date.UTC(2026,8,14+offset)).toISOString().slice(0,10);
 for(let n=0;n<120;n++){
  const id=`SIM-${String(n+1).padStart(4,'0')}`,lead=leads[n%6],team=[lead,...Array.from({length:12},(_,j)=>`sim-person-${(n*7+j)%1050}`)];
  if(n%6===0)team.push('maya','emily','rachel');
  const lifecycle=n%8===0?'Closed':n%19===0?'Cancelled':'Active';
  s.projects.push({id,name:`${names[n%8]} · ${['EU variant','UK launch','Color refresh','Supplier change','Firmware update'][n%5]} ${n+1}`,programId:s.programs[n%s.programs.length].id,leadId:lead,factory:`Simulation factory ${n%9+1}`,scope:'Illustrative change scope for usability testing.',type:['Extension','NPD','Dual Source'][n%3],priority:n%7===0?'High':'Normal',stage:['Assessment & Planning','ECN DD Review','Execution & Testing','ECN IMP Review','MP'][n%5],lifecycle,health:['On Track','At Risk','Delayed','On Hold'][n%4],targetMP:date(20+n%60),summary:'Simulation project — no production facts.',team:[...new Set(team)],documentIds:[],source:'Synthetic usability sample',sample:true});
  for(let j=0;j<32;j++){
   const [title,kind,area]=plans[(j+n)%plans.length],tid=`sim-task-${n}-${j}`;
   const candidate=team.find(pid=>s.people.find(p=>p.id===pid)?.department===area)||team[(j+1)%team.length];
   const owners=lifecycle!=='Active'&&j===0?[lead]:j%10===0?[]:j%7===0?[...new Set([lead,candidate])]:j%4===0?[lead]:[candidate];
   const complete=lifecycle!=='Active'?j>0:j%6===0;
   s.tasks.push({id:tid,projectId:id,title,kind,workstream:area,phase:s.projects.at(-1).stage,ownerIds:owners,completedBy:complete?[...owners]:j%7===0&&owners.length>1?[owners[1]]:[],start:date(-10+j%8),due:date((j*3+n)%35-12),priority:j%11===0?'High':'Normal',brief:`${title}. Check the agreed change scope and attach the result when ready.`,outcome:complete?'Simulation: work reviewed against the agreed scope.':'',assessmentDecision:kind==='Assessment'&&complete?(j%2?'Further Work Required':'No Further Work'):'',testResult:kind==='Test'&&complete?(j%2?'Pass':'Fail'):'Not Reported',approvalStatus:kind==='Approval'?(complete?'Approved':j%2?'In Review':'Returned'):'',approvalDate:kind==='Approval'&&complete?date(-2):'',predecessorIds:j%6===2?[`sim-task-${n}-${j-1}`]:[],sourceAssessmentIds:[],duration:5,durationBasis:'Working Days',deliverableId:'',sample:true});
  }
  const sku=`sim-sku-${n}`;s.skus.push({id:sku,name:`SIM SKU ${n+1}`,programId:s.projects.at(-1).programId,market:n%2?'EU':'UK',sample:true});s.projectSkus.push({id:`sim-ps-${n}`,skuId:sku,projectId:id,status:lifecycle==='Active'?'In Development':'In MP',active:true,overrideDate:'',overrideReason:'',sample:true});
  if(n%2===0){const iid=`sim-issue-${n}`,status=n%10===0?'Closed':Math.floor(n/2)%5===3?'Pending Verification':'In Recovery',owner=team[1];
   s.issues.push({id:iid,projectId:id,title:['Sample housing cracked','Certification input missing','Supplier capacity shortage','Firmware instability'][Math.floor(n/2)%4],details:'Simulation obstacle for testing assignment and resolution.',department:'NPI',ownerId:owner,severity:Math.floor(n/2)%4===0?'High':'Medium',status,category:'Technical',impact:'May delay the next project milestone.',impactMP:n%4===0,due:date(n%10-3),occurred:date(-8),phase:s.projects.at(-1).stage,rootCause:'Simulation analysis',resolution:['Closed','Pending Verification'].includes(status)?'Simulation: revised sample retested successfully.':'',closedDate:status==='Closed'?date(-1):'',prevention:'',affectedProjectSkuIds:[`sim-ps-${n}`],relatedTaskIds:[`sim-task-${n}-6`],sample:true});
   for(let j=0;j<3;j++)s.actions.push({id:`sim-action-${n}-${j}`,issueId:iid,title:['Check the affected sample','Agree the correction','Retest the corrected sample'][j],ownerId:j===0?lead:team[j+1],due:date(j-1),status:status==='In Recovery'&&j>0?'Open':'Done',result:status==='In Recovery'&&j>0?'':'Simulation: completed check.',evidenceUrl:'',formalTaskId:'',sample:true});
  }
 }
 s.sampleExpansion=1;s.revision++;return s;
}
