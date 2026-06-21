(function(){
  const API='/api/v7';
  const CLIENT_ID='client-'+Math.random().toString(36).slice(2,10);
  const USER_NAME='Sun Sun';
  const localSave=saveData;
  let revision=0;
  let dirty=false;
  let syncing=false;
  let conflict=false;
  let saveTimer=null;

  function snapshot(){
    return {
      schemaVersion:13,_v:13,
      projects:S.projects,tasks:S.tasks,deliverables:S.deliverables,issues:S.issues,milestones:S.milestones,
      knowledge:S.knowledge,people:S.people,projectMembers:S.projectMembers,documents:S.documents,
      workflowTemplates:S.workflowTemplates,referenceData:S.referenceData,importStaging:S.importStaging,
      activityLog:S.activityLog,users:S.users,lastValidation:S.lastValidation||null
    };
  }

  function setIndicator(state, detail=''){
    const chip=document.getElementById('v7SyncChip');
    if(!chip)return;
    const config={
      loading:['Syncing','v7-syncing'],saved:[`Shared r${revision}`,'v7-saved'],offline:['Offline cache','v7-offline'],
      conflict:['Sync conflict','v7-conflict'],dirty:['Saving...','v7-syncing']
    }[state]||['Shared','v7-saved'];
    chip.textContent=config[0];chip.className='v7-sync-chip '+config[1];chip.title=detail||'AutoPM v7 shared SQLite database';
  }

  function installIndicator(){
    const right=document.querySelector('.topbar-right');if(!right||document.getElementById('v7SyncChip'))return;
    const chip=document.createElement('button');chip.id='v7SyncChip';chip.className='v7-sync-chip v7-syncing';chip.textContent='Connecting...';
    chip.onclick=()=>{if(conflict)reloadSharedState(true);else pushState(true)};
    right.insertBefore(chip,right.firstChild);
  }

  function applyShared(data, meta){
    const page=S.page,subPage=S.subPage,projectId=S.projectId;
    Object.assign(S,data);
    S.page=page||'daily';S.subPage=subPage||'';S.projectId=projectId||null;
    revision=meta.revision;dirty=false;conflict=false;
    localSave();render();setIndicator('saved',`Updated ${meta.updatedAt||''} by ${meta.updatedBy||''}`);
  }

  async function reloadSharedState(force=false){
    if(dirty&&!force)return;
    setIndicator('loading');
    try{
      const response=await fetch(API+'/state',{cache:'no-store'});
      if(!response.ok)throw new Error(`HTTP ${response.status}`);
      const payload=await response.json();
      if(force||payload.revision>revision)applyShared(payload.data,payload);
      else setIndicator('saved',`Revision ${revision}`);
    }catch(error){setIndicator('offline',error.message);}
  }

  async function pushState(manual=false){
    if(syncing||(!dirty&&!manual)||conflict)return;
    syncing=true;setIndicator('loading');
    try{
      const response=await fetch(API+'/state',{
        method:'PUT',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({baseRevision:revision,changedBy:USER_NAME,clientId:CLIENT_ID,data:snapshot()})
      });
      if(response.status===409){
        const info=await response.json();conflict=true;dirty=true;
        setIndicator('conflict',`Shared data changed by ${info.updatedBy||'another user'}. Click to load shared version.`);
        toast('Another user updated AutoPM. Click Sync conflict to load the shared version.','error');return;
      }
      if(!response.ok)throw new Error(`HTTP ${response.status}`);
      const result=await response.json();revision=result.revision;dirty=false;conflict=false;
      setIndicator('saved',`Saved at ${result.updatedAt}`);
    }catch(error){setIndicator('offline',`Saved locally; ${error.message}`);}
    finally{syncing=false;}
  }

  saveData=function(){
    localSave();dirty=true;setIndicator('dirty');
    clearTimeout(saveTimer);saveTimer=setTimeout(()=>pushState(false),650);
  };

  window.AutoPMV7={
    syncNow:()=>pushState(true),
    reloadShared:()=>reloadSharedState(true),
    getStatus:()=>({revision,dirty,syncing,conflict,clientId:CLIENT_ID})
  };

  const style=document.createElement('style');
  style.textContent=`
    .v7-sync-chip{border:1px solid #d1d5db;border-radius:6px;padding:5px 9px;font-size:11px;font-weight:700;background:#fff;white-space:nowrap;cursor:pointer}
    .v7-saved{color:#166534;background:#f0fdf4;border-color:#bbf7d0}.v7-syncing{color:#1d4ed8;background:#eff6ff;border-color:#bfdbfe}
    .v7-offline{color:#92400e;background:#fffbeb;border-color:#fde68a}.v7-conflict{color:#b91c1c;background:#fef2f2;border-color:#fecaca}
  `;
  document.head.appendChild(style);
  installIndicator();
  reloadSharedState(true);
  setInterval(()=>reloadSharedState(false),5000);
})();
