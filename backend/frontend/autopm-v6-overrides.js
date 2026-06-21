(function(){
  const V6_SCHEMA_VERSION=12;
  const V6_STORAGE_KEY='autopm_v6_data';
  const clone=value=>JSON.parse(JSON.stringify(value));
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));

  function persistableState(){
    return {
      _v:V6_SCHEMA_VERSION,
      projects:S.projects,tasks:S.tasks,deliverables:S.deliverables,issues:S.issues,milestones:S.milestones,
      knowledge:S.knowledge,people:S.people,projectMembers:S.projectMembers,documents:S.documents,
      workflowTemplates:S.workflowTemplates,referenceData:S.referenceData,importStaging:S.importStaging,
      activityLog:S.activityLog,users:S.users,lastValidation:S.lastValidation||null
    };
  }

  saveData=function(){
    try{localStorage.setItem(V6_STORAGE_KEY,JSON.stringify(persistableState()));}
    catch(error){console.error('AutoPM save failed',error);}
  };

  loadData=function(){
    const raw=localStorage.getItem(V6_STORAGE_KEY);
    if(!raw)return false;
    try{
      const data=JSON.parse(raw);
      if(data._v!==V6_SCHEMA_VERSION){localStorage.removeItem(V6_STORAGE_KEY);return false;}
      Object.assign(S,data);
      S.people=S.people||[];S.projectMembers=S.projectMembers||[];S.documents=S.documents||[];
      S.workflowTemplates=S.workflowTemplates||[];S.referenceData=S.referenceData||{};
      S.importStaging=S.importStaging||[];S.activityLog=S.activityLog||[];S.users=S.users||[];
      return true;
    }catch(error){console.error('AutoPM load failed',error);return false;}
  };

  initData=function(){
    if(loadData())return;
    if(!window.AUTOPM_IMPORT_DATA)throw new Error('autopm-v6-data.js was not loaded');
    const imported=clone(window.AUTOPM_IMPORT_DATA);
    Object.assign(S,imported);
    S.page='daily';S.subPage='';S.projectId=null;S._v=V6_SCHEMA_VERSION;
    saveData();
  };

  myTasks=function(){return S.tasks.filter(task=>task.owner==='Sun Sun'||task.owner==='Sunny')};

  window.recordActivity=function(entityType,entityId,projectId,field,fromValue,toValue,note=''){
    if(String(fromValue??'')===String(toValue??''))return;
    S.activityLog=S.activityLog||[];
    S.activityLog.unshift({
      id:'LOG-'+Date.now()+'-'+Math.random().toString(36).slice(2,6),entityType,entityId,projectId,field,
      fromValue:fromValue??'',toValue:toValue??'',changedBy:'Sun Sun',changedAt:new Date().toISOString(),note
    });
    if(S.activityLog.length>500)S.activityLog.length=500;
  };

  function validateDataset(data){
    const projects=data.projects||[],tasks=data.tasks||[],issues=data.issues||[],people=data.people||[];
    const duplicateIds=list=>list.map(item=>item.id).filter((id,index,all)=>id&&all.indexOf(id)!==index);
    const projectIds=new Set(projects.map(project=>project.id));
    const validStatuses=new Set(S.referenceData?.taskStatuses||['Not Started','In Progress','At Risk','Delayed','Blocked','Done']);
    const checks=[
      {name:'Duplicate Project IDs',count:new Set(duplicateIds(projects)).size,severity:'Critical'},
      {name:'Duplicate Task IDs',count:new Set(duplicateIds(tasks)).size,severity:'Critical'},
      {name:'Orphan Tasks',count:tasks.filter(task=>!projectIds.has(task.projectId)).length,severity:'Critical'},
      {name:'Orphan Issues',count:issues.filter(issue=>!projectIds.has(issue.projectId)).length,severity:'Critical'},
      {name:'Invalid Task Status',count:tasks.filter(task=>!validStatuses.has(task.status)).length,severity:'Warning'},
      {name:'Tasks Missing Named Owner',count:tasks.filter(task=>!task.owner||task.owner==='Unassigned').length,severity:'Warning'},
      {name:'Tasks Missing Due Date',count:tasks.filter(task=>task.active!==false&&!task.dueDate).length,severity:'Warning'},
      {name:'People Missing Email',count:people.filter(person=>!person.email).length,severity:'Info'},
      {name:'Open Data Gaps',count:(data.importStaging||[]).filter(item=>item.status!=='Resolved').length,severity:'Info'}
    ];
    return {
      checkedAt:new Date().toISOString(),checks,
      critical:checks.filter(check=>check.severity==='Critical').reduce((sum,check)=>sum+check.count,0),
      warnings:checks.filter(check=>check.severity==='Warning').reduce((sum,check)=>sum+check.count,0)
    };
  }

  window.runImportValidation=function(){
    S.lastValidation=validateDataset(S);
    recordActivity('System','IMPORT-VALIDATION','ALL','Validation','Not Run',S.lastValidation.critical?'Failed':'Passed',`${S.lastValidation.warnings} warnings`);
    saveData();render();
    toast(S.lastValidation.critical?'Validation found critical errors':'Validation passed; review warnings',S.lastValidation.critical?'error':'success');
  };

  exportData=function(){
    const blob=new Blob([JSON.stringify(persistableState(),null,2)],{type:'application/json'});
    const anchor=document.createElement('a');anchor.href=URL.createObjectURL(blob);anchor.download='autopm-v6-backup.json';anchor.click();
    toast('AutoPM v6 data exported');
  };

  importData=function(event){
    const file=event.target.files[0];if(!file)return;
    const reader=new FileReader();
    reader.onload=loadEvent=>{try{
      const candidate=JSON.parse(loadEvent.target.result);
      const validation=validateDataset(candidate);
      if(validation.critical){S.lastValidation=validation;saveData();render();toast('Import blocked: critical validation errors','error');return;}
      Object.assign(S,candidate);S.lastValidation=validation;
      recordActivity('System','JSON-IMPORT','ALL','Import','Existing Data',file.name,'Validated JSON import');
      saveData();render();toast('Validated data imported');
    }catch(error){toast('Invalid JSON file','error');}}
    reader.readAsText(file);event.target.value='';
  };

  window.resetToImportPackage=function(){
    localStorage.removeItem(V6_STORAGE_KEY);location.reload();
  };

  const baseChangeStatus=changeStatus;
  changeStatus=function(taskId,newStatus){
    const task=S.tasks.find(item=>item.id===taskId);const previous=task?.status;
    baseChangeStatus(taskId,newStatus);
    if(task&&task.status!==previous){recordActivity('Task',task.id,task.projectId,'Status',previous,task.status,'Status dropdown');saveData();}
  };

  const baseDwChangeStatus=dwChangeStatus;
  dwChangeStatus=function(newStatus){
    const task=S.tasks.find(item=>item.id===DW_SELECTED_TASK);const previous=task?.status;
    baseDwChangeStatus(newStatus);
    if(task&&task.status!==previous)recordActivity('Task',task.id,task.projectId,'Status',previous,task.status,'My Daily Work detail');
  };

  const baseDwQuickDone=dwQuickDone;
  dwQuickDone=function(taskId){
    const task=S.tasks.find(item=>item.id===taskId);const previous=task?.status;
    baseDwQuickDone(taskId);
    if(task&&task.status!==previous){recordActivity('Task',task.id,task.projectId,'Status',previous,task.status,'Quick complete');saveData();}
  };

  const baseSaveEditTask=saveEditTask;
  saveEditTask=function(taskId){
    const task=S.tasks.find(item=>item.id===taskId);
    const before=task?{status:task.status,owner:task.owner,dueDate:task.dueDate}:null;
    baseSaveEditTask(taskId);
    if(task&&before){
      recordActivity('Task',task.id,task.projectId,'Status',before.status,task.status,'Edit task');
      recordActivity('Task',task.id,task.projectId,'Owner',before.owner,task.owner,'Edit task');
      recordActivity('Task',task.id,task.projectId,'Due Date',before.dueDate,task.dueDate,'Edit task');
      saveData();
    }
  };

  const baseSaveNewTask=saveNewTask;
  saveNewTask=function(projectId){
    const before=S.tasks.length;baseSaveNewTask(projectId);
    if(S.tasks.length>before){const task=S.tasks.at(-1);recordActivity('Task',task.id,projectId,'Create','',task.name,'Manual task');saveData();}
  };

  const baseSaveNewIssue=typeof saveNewIssue==='function'?saveNewIssue:null;
  if(baseSaveNewIssue){
    saveNewIssue=function(projectId){
      const before=S.issues.length;baseSaveNewIssue(projectId);
      if(S.issues.length>before){const issue=S.issues.at(-1);recordActivity('Issue',issue.id,projectId,'Create','',issue.title,'Manual issue');saveData();}
    };
  }

  showNewProjectModal=function(){
    document.getElementById('modalTitle').textContent='+ New Project from Workflow Template';
    document.getElementById('modalOverlay').style.display='flex';
    const templates=S.workflowTemplates.map(template=>`<option value="${esc(template.id)}">${esc(template.name)}</option>`).join('');
    document.getElementById('modalContent').innerHTML=`
      <div class="form-grid">
        <div><label class="form-label">Project ID *</label><input class="form-input" id="v6_np_id" placeholder="e.g. AF500EUUK"></div>
        <div><label class="form-label">Model / Family</label><input class="form-input" id="v6_np_model" placeholder="e.g. AF500"></div>
        <div class="full"><label class="form-label">Project Name *</label><input class="form-input" id="v6_np_name" placeholder="e.g. AF500EU / AF500UK"></div>
        <div><label class="form-label">Workflow Template</label><select class="form-input" id="v6_np_tpl">${templates}</select></div>
        <div><label class="form-label">Brand</label><select class="form-input" id="v6_np_brand"><option>Ninja</option><option>Shark</option><option>TBD</option></select></div>
        <div><label class="form-label">Factory / Supplier</label><input class="form-input" id="v6_np_factory"></div>
        <div><label class="form-label">NPI Owner</label><select class="form-input" id="v6_np_owner">${S.people.map(person=>`<option value="${esc(person.name)}" ${person.name==='Sun Sun'?'selected':''}>${esc(person.name)}</option>`).join('')}</select></div>
        <div><label class="form-label">Start Date</label><input type="date" class="form-input" id="v6_np_start"></div>
        <div><label class="form-label">Target MP Date</label><input type="date" class="form-input" id="v6_np_launch"></div>
      </div>
      <div class="modal-footer" style="margin:16px -20px -20px;padding:12px 20px">
        <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
        <button class="btn btn-primary" onclick="saveNewProject()">Create Project & Tasks</button>
      </div>`;
  };

  saveNewProject=function(){
    const id=(document.getElementById('v6_np_id')?.value||'').trim().toUpperCase();
    const name=(document.getElementById('v6_np_name')?.value||'').trim();
    if(!id||!name){toast('Project ID and name are required','error');return;}
    if(S.projects.some(project=>project.id===id)){toast('Project ID already exists','error');return;}
    const template=S.workflowTemplates.find(item=>item.id===document.getElementById('v6_np_tpl')?.value)||S.workflowTemplates[0];
    const owner=document.getElementById('v6_np_owner')?.value||'Sun Sun';
    const factory=document.getElementById('v6_np_factory')?.value||'TBD';
    const start=document.getElementById('v6_np_start')?.value||'';
    const launch=document.getElementById('v6_np_launch')?.value||'';
    const gates=NPI_GATES.map(gate=>({name:gate.name,status:'Not Started',completion:0,targetDate:'',actualDate:''}));
    S.projects.push({
      id,name,sku:name,model:document.getElementById('v6_np_model')?.value||id,brand:document.getElementById('v6_np_brand')?.value||'TBD',
      type:template.projectType,workflowTemplateId:template.id,pm:owner,npiLead:owner,npilead:owner,pmo:'Sarah',factory,supplier:factory,oem:factory,
      status:'Not Started',riskLevel:'Low',healthScore:100,start,targetLaunch:launch,plannedFinish:launch,progress:0,delayDays:0,
      nextMs:'Kick Off',keyIssue:'No open issue',recoveryAction:'',currentGate:0,gates,
      team:{engineering:'Jeff chen',quality:'Vic li',supplyChain:'Lucia zhu',manufacturing:factory,packaging:'TBD',supplier:factory},
      sourceSystem:'Workflow Template',sourceRecordId:id,lastUpdated:new Date().toISOString().slice(0,10),updatedAt:new Date().toISOString(),updatedBy:'Sun Sun',active:true,archived:false,dataConfidence:'Draft'
    });
    template.taskNames.forEach((taskName,index)=>S.tasks.push({
      id:`${id}-T${String(index+1).padStart(3,'0')}`,projectId:id,sourceTaskId:'',wbs:String(index+1),taskType:'Task',name:taskName,
      prog:0,status:'Not Started',start:index===0?start:'',dueDate:'',durationDays:0,originalOwner:'CN NPI',owner,personId:S.people.find(person=>person.name===owner)?.id||'',
      department:'PM',pri:'medium',prioritySource:'Template default; not business-confirmed',riskFlag:false,delayFlag:false,blocker:'',delayDays:0,
      ms:'',impactedMs:'',relatedIssueIds:[],dep:'',desc:'Generated from workflow template',actionNote:'',rootCause:'',solution:'',recoveryAction:'',
      recoveryOwner:'',targetRecoveryDate:'',escalation:false,sourceSystem:'Workflow Template',sourceRecordId:`${id}:${index+1}`,lastUpdated:new Date().toISOString().slice(0,10),updatedBy:'Sun Sun',dataConfidence:'Draft',active:true,workflowTemplateId:template.id
    }));
    const defaults=S.projectMembers.filter(member=>member.projectId==='SL500EUUK'&&member.function!=='Factory');
    defaults.forEach((member,index)=>S.projectMembers.push({...clone(member),id:`PMEM-${id}-${index+1}`,projectId:id,sourceNote:'Copied from pilot default team; confirm before use.'}));
    S.projectMembers.push({id:`PMEM-${id}-FACTORY`,projectId:id,function:'Factory',personId:'',name:factory,memberType:'Organization',role:'Factory / Supplier',status:'Draft',sourceNote:'Entered during project creation',active:true});
    recordActivity('Project',id,id,'Create','',name,`Created from ${template.name}`);
    closeModal();saveData();navigateTo('projects',{projectId:id});toast('Project and template tasks created');
  };

  const baseTeamTab=pdTeamTab;
  pdTeamTab=function(project){
    const members=(S.projectMembers||[]).filter(member=>member.projectId===project.id);
    if(!members.length)return baseTeamTab(project);
    const cards=members.map(member=>`
      <div class="pd-team-card">
        <div style="display:flex;align-items:center;gap:10px">
          <div class="pd-team-avatar">${esc((member.name||'?').split(/\s+/).map(part=>part[0]).join('').slice(0,2))}</div>
          <div><div class="pd-team-name">${esc(member.name)}</div><div class="pd-team-role">${esc(member.role)}</div></div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap"><span class="pd-team-badge">${esc(member.function)}</span>${member.memberType?`<span class="badge bgr">${esc(member.memberType)}</span>`:''}</div>
        <div class="pd-team-contact">Assignment: ${esc(member.status)}</div>
      </div>`).join('');
    return `<div><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><span class="fw6" style="font-size:14px">Team Members (${members.length})</span><span class="badge bb">Linked by Project ID</span></div><div class="pd-team-grid">${cards}</div><div class="text-xs text-muted mt12">People and organizations are stored once and linked to each project through Project Members.</div></div>`;
  };

  const baseDocsTab=pdDocsTab;
  pdDocsTab=function(project){
    const docs=(S.documents||[]).filter(document=>document.projectId===project.id);
    if(!docs.length)return baseDocsTab(project);
    return `<div><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><span class="fw6" style="font-size:14px">Project Documents (${docs.length})</span><span class="badge bgr">SharePoint / Teams links</span></div><div style="overflow-x:auto"><table class="pd-docs-filetbl"><thead><tr><th>Document</th><th>Type</th><th>Milestone</th><th>Status</th><th>Source</th><th>Confidence</th></tr></thead><tbody>${docs.map(document=>`<tr><td style="font-weight:600">${esc(document.name)}</td><td>${esc(document.type)}</td><td>${esc(document.relatedMilestone||'—')}</td><td>${esc(document.status)}</td><td>${document.link?`<span title="${esc(document.link)}">Linked</span>`:'<span style="color:var(--amber)">Link required</span>'}</td><td>${esc(document.dataConfidence)}</td></tr>`).join('')}</tbody></table></div><div class="text-xs text-muted mt12">Files remain in SharePoint/Teams; AutoPM stores the link and project relationship.</div></div>`;
  };

  function foundationPanel(){
    const validation=S.lastValidation;
    const openGaps=(S.importStaging||[]).filter(item=>item.status!=='Resolved');
    const recent=(S.activityLog||[]).slice(0,10);
    const validationRows=validation?.checks?.map(check=>`<tr><td>${esc(check.name)}</td><td>${check.count}</td><td><span class="badge ${check.severity==='Critical'?'br':check.severity==='Warning'?'ba':'bgr'}">${check.severity}</span></td></tr>`).join('')||'<tr><td colspan="3" class="text-muted">Validation has not been run in this browser.</td></tr>';
    return `<div class="card mt16"><div class="card-hdr"><div class="card-title">Data Foundation · MVP v6</div><button class="btn btn-primary btn-sm" onclick="runImportValidation()">Run Import Validation</button></div><div class="card-body">
      <div class="kpi-row c4"><div class="kpi-card"><div class="kpi-label">Workflow Templates</div><div class="kpi-value">${S.workflowTemplates.length}</div><div class="kpi-sub">NPD · Extension · Color Refresh</div></div><div class="kpi-card"><div class="kpi-label">Reference Lists</div><div class="kpi-value">${Object.keys(S.referenceData||{}).length}</div><div class="kpi-sub">Controlled values</div></div><div class="kpi-card"><div class="kpi-label">Open Data Gaps</div><div class="kpi-value" style="color:var(--amber)">${openGaps.length}</div><div class="kpi-sub">Import staging review</div></div><div class="kpi-card"><div class="kpi-label">Activity Records</div><div class="kpi-value">${S.activityLog.length}</div><div class="kpi-sub">Latest 500 retained locally</div></div></div>
      <div class="grid-2 mt16"><div><div class="fw6 mb8">Validation Result ${validation?`· ${new Date(validation.checkedAt).toLocaleString()}`:''}</div><table class="pd-tasks-table"><thead><tr><th>Check</th><th>Count</th><th>Level</th></tr></thead><tbody>${validationRows}</tbody></table></div><div><div class="fw6 mb8">Import Staging / Data Gaps</div><table class="pd-tasks-table"><thead><tr><th>Project</th><th>Field</th><th>Priority</th></tr></thead><tbody>${openGaps.slice(0,8).map(item=>`<tr><td>${esc(item.projectId)}</td><td title="${esc(item.requiredAction)}">${esc(item.field)}</td><td>${esc(item.priority)}</td></tr>`).join('')||'<tr><td colspan="3">No open gaps</td></tr>'}</tbody></table></div></div>
      <div class="mt16"><div class="fw6 mb8">Recent Activity</div><table class="pd-tasks-table"><thead><tr><th>Time</th><th>Entity</th><th>Field</th><th>Change</th><th>By</th></tr></thead><tbody>${recent.map(log=>`<tr><td>${new Date(log.changedAt).toLocaleString()}</td><td>${esc(log.entityType)} · ${esc(log.entityId)}</td><td>${esc(log.field)}</td><td>${esc(log.fromValue||'—')} → ${esc(log.toValue)}</td><td>${esc(log.changedBy)}</td></tr>`).join('')||'<tr><td colspan="5">No activity yet</td></tr>'}</tbody></table></div>
      <div class="flex gap8 mt16"><button class="btn btn-secondary btn-sm" onclick="resetToImportPackage()">Reload Original Import Package</button><span class="text-xs text-muted" style="align-self:center">Current data: ${S.projects.length} projects · ${S.tasks.length} tasks · ${S.issues.length} issues</span></div>
    </div></div>`;
  }

  const baseRenderAdmin=renderAdmin;
  renderAdmin=function(container){baseRenderAdmin(container);container.insertAdjacentHTML('beforeend',foundationPanel());};

  try{
    window.__AUTOPM_DEFERRED_INIT__();
  }catch(error){
    const content=document.getElementById('content');
    if(content)content.innerHTML=`<div style="padding:40px;color:#ef4444;font-family:monospace"><h2>AutoPM v6 Init Error</h2><pre>${esc(error.stack||error.message)}</pre></div>`;
    console.error(error);
  }
})();
