"""Local tracker workflow: choose files, review cells, export a new workbook."""
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
import uuid

from .tracker import build_tracker_plan, export_tracker, fingerprint
from .design import FONT


class TrackerPage:
    def __init__(self,app,parent):
        from .ui import C,label,panel,set_text,readonly_text
        self.app=app;self.plan=None;self.reports=[];self.last_output=None;self.rows={};self.revision=0
        self.scope_context=None;self.scope_credentials=None;self._export_plan=None
        self.tracker=tk.StringVar(value=app.settings.get('local_tracker_path',''))
        self.source_kind=tk.StringVar(value='airtable');self.use_ai=tk.BooleanVar(value=False);self.query=tk.StringVar()
        self.source_summary=tk.StringVar(value='周报文件 → 本地总表')
        self.summary=tk.StringVar(value='选择原总表与周报，预览后导出新的 Excel。')
        app._page_title(parent,'本地总表','选择数据来源，核对单元格后导出 All Tracker 副本。')
        card=panel(parent);card.pack(fill='x',padx=26,pady=(0,10))
        label(card,'01  原始汇总表',13,bold=True).grid(row=0,column=0,sticky='w',padx=14,pady=12)
        entry=ttk.Entry(card,textvariable=self.tracker);entry.grid(row=0,column=1,sticky='ew',padx=10)
        card.columnconfigure(1,weight=1);app._controls.append(entry)
        app._button(card,'选择 All Tracker',self.pick_tracker,controlled=True).grid(row=0,column=2,padx=12)
        label(card,'02  数据来源',13,bold=True).grid(row=1,column=0,sticky='w',padx=14,pady=4)
        sources=tk.Frame(card,bg='white');sources.grid(row=1,column=1,columnspan=2,sticky='ew',padx=10)
        for value,title in (('airtable','Airtable → All Tracker'),('writeback','All Tracker → Airtable')):
            choice=ttk.Radiobutton(sources,text=title,variable=self.source_kind,value=value)
            choice.pack(side='left',padx=(0,18));app._controls.append(choice)
        self.scope_button=app._button(sources,'改为全库匹配',self.use_all_airtable,link=True)
        self.scope_button.pack(side='right',padx=6)
        self.report_label=label(card,'03  周报文件',13,bold=True)
        self.report_label.grid(row=2,column=0,sticky='nw',padx=14,pady=12)
        self.file_list=tk.Listbox(card,height=3,font=(FONT,-13),borderwidth=0,highlightthickness=0)
        self.file_list.grid(row=2,column=1,sticky='ew',padx=10,pady=(0,10))
        tools= tk.Frame(card,bg='white');tools.grid(row=2,column=2,padx=12,sticky='n')
        self.weekly_widgets=(self.report_label,self.file_list,tools)
        app._button(tools,'添加周报',self.pick_reports,controlled=True).pack(fill='x')
        app._button(tools,'移除选中',self.remove_report,controlled=True).pack(fill='x',pady=4)
        options= tk.Frame(parent,bg=C['bg']);options.pack(fill='x',padx=26,pady=(0,10))
        self.weekly_options=tk.Frame(options,bg=C['bg']);self.weekly_options.pack(side='left')
        mode=ttk.Checkbutton(self.weekly_options,text='使用 DeepSeek 解析周报',variable=self.use_ai)
        mode.pack(side='left');app._controls.append(mode)
        label(self.weekly_options,'未勾选时本地解析 Report。',12,C['muted']).pack(side='left',padx=12)
        self.preview_button=app._button(options,'生成本地更新预览',self.preview,True,True);self.preview_button.pack(side='right')
        label(parent,textvariable=self.source_summary,size=12,color=C['blue'],anchor='w',wraplength=850).pack(fill='x',padx=27,pady=(0,5))
        label(parent,textvariable=self.summary,size=13,color=C['muted'],anchor='w').pack(fill='x',padx=27,pady=(0,8))
        bottom=panel(parent);bottom.pack(side='bottom',fill='x',padx=26,pady=(8,20))
        self.export_button=app._button(bottom,'导出更新后的 Excel',self.export,True);self.export_button.pack(side='right',padx=12,pady=10)
        self.open_button=app._button(bottom,'打开导出目录',self.open_output);self.open_button.pack(side='right',padx=4)
        self.reuse_button=app._button(bottom,'将副本作为下次输入',self.use_output);self.reuse_button.pack(side='left',padx=12)
        style=ttk.Style(parent)
        style.configure('Tracker.TNotebook',background='white',borderwidth=0)
        style.configure('Tracker.TNotebook.Tab',background=C['bg'],foreground=C['muted'],padding=(15,9),font=(FONT,-13))
        style.map('Tracker.TNotebook.Tab',background=[('selected','#EAF1FF')],foreground=[('selected',C['blue'])])
        tabs=ttk.Notebook(parent,style='Tracker.TNotebook');tabs.pack(fill='both',expand=True,padx=26)
        self.tabs=tabs
        changes=tk.Frame(tabs,bg='white');notes=tk.Frame(tabs,bg='white')
        tabs.add(changes,text='单元格变更');tabs.add(notes,text='未写入内容与提示')
        search_row=tk.Frame(changes,bg='white');search_row.pack(fill='x',padx=10,pady=8)
        label(search_row,'搜索项目、字段或值',12,C['muted']).pack(side='left',padx=(0,10))
        search=ttk.Entry(search_row,textvariable=self.query);search.pack(side='left',fill='x',expand=True)
        self.tree=ttk.Treeview(changes,columns=('project','cell','field','before','after'),show='headings',height=2)
        for key,title,width in [('project','项目编号',100),('cell','单元格',85),('field','总表字段',180),('before','当前值',260),('after','周报新值',260)]:
            self.tree.heading(key,text=title);self.tree.column(key,width=width,minwidth=65)
        scroll=ttk.Scrollbar(changes,orient='vertical',command=self.tree.yview);scroll.pack(side='right',fill='y')
        self.tree.configure(yscrollcommand=scroll.set);self.tree.pack(fill='both',expand=True)
        self.detail=readonly_text(changes,height=4,size=12)
        self.notes=readonly_text(notes,height=6,size=13);self.notes.pack(fill='both',expand=True)
        note_scroll=ttk.Scrollbar(notes,orient='vertical',command=self.notes.yview)
        self.notes.configure(yscrollcommand=note_scroll.set);note_scroll.pack(side='right',fill='y');self.notes.pack_configure(side='left')
        self.tracker.trace_add('write',lambda *_:self.tracker_changed());self.use_ai.trace_add('write',lambda *_:self.invalidate())
        self.source_kind.trace_add('write',lambda *_:self.source_changed())
        self.query.trace_add('write',lambda *_:self.filter())
        self.tree.bind('<<TreeviewSelect>>',self.select)
        self.source_changed()

    def invalidate(self):
        self.revision+=1
        self.plan=None;self.rows={};self.tree.delete(*self.tree.get_children())
        from .ui import set_text
        set_text(self.detail,'');set_text(self.notes,'')
        self.detail.pack_forget()
        self.summary.set('文件或设置已变化，请重新生成本地更新预览。');self.refresh_controls()

    def tracker_changed(self):
        self.app.settings['local_tracker_path']=self.tracker.get().strip()
        self.invalidate()

    def source_changed(self):
        airtable=self.source_kind.get()!='weekly'
        for widget in self.weekly_widgets:
            if airtable:widget.grid_remove()
            else:widget.grid()
        if airtable:self.weekly_options.pack_forget()
        else:self.weekly_options.pack(side='left')
        self.preview_button.configure(text='读取 Airtable 并预览' if airtable else '生成本地更新预览')
        if self.source_kind.get()=='writeback':self.preview_button.configure(text='预览总表回写差异')
        self.update_scope_label();self.invalidate()

    def update_scope_label(self):
        if self.source_kind.get()=='writeback':
            text='All Tracker → Airtable · 编号＋SKU＋工厂匹配 · 比较导出原值、本地修改和云端现值'
        elif self.source_kind.get()!='airtable':
            text='周报文件 → 本地总表'
        elif self.scope_context:
            ids=self.scope_context.get('project_ids',[])
            text=f"Airtable → 本地总表 · 仅本次已同步 {len(ids)} 个项目："+'、'.join(ids[:8])
            if len(ids)>8:text+='…'
        else:text='Airtable → 本地总表 · 当前数据库全库匹配 · 无需周报或 DeepSeek'
        self.source_summary.set(text)

    def use_all_airtable(self):
        if self.app.busy:return
        self.scope_context=self.scope_credentials=None
        if self.source_kind.get()!='airtable':self.source_kind.set('airtable')
        else:self.update_scope_label();self.invalidate()

    def follow_sync(self,context,credentials):
        """Enter the read-only local stage after the Airtable writer has finished."""
        if self.app.busy:return False
        if credentials!=self.app._credential_key() or context.get('base_id')!=self.app.values['base_id'].get().strip():
            self.app._notice('Airtable 已同步，本地总表尚未更新：连接配置已变化，请核对数据库后重新读取。','warning')
            return False
        self.scope_context=deepcopy(context);self.scope_credentials=credentials
        self.source_kind.set('airtable');self.app._navigate(3)
        if not context.get('project_ids'):
            message='Airtable 同步已完成 · 本次没有已确认变更项目，本地总表无需自动更新。'
            self.summary.set(message);self.app.status.set(message);return False
        if not self.valid_tracker():
            message='Airtable 同步已完成，本地总表尚未更新：请选择 All Tracker，再点击“读取 Airtable 并预览”。'
            self.summary.set(message);self.app.status.set(message);self.app._notice(message,'success')
            return False
        return self.preview_airtable()

    def valid_tracker(self):
        path=Path(self.tracker.get())
        return bool(self.tracker.get()) and path.suffix.lower()=='.xlsx' and path.is_file()

    def refresh_controls(self):
        airtable=self.source_kind.get()!='weekly'
        available=(all(self.app.values[k].get().strip() for k in ('airtable_token','base_id')) if airtable else bool(self.reports))
        self.preview_button.configure(state='normal' if self.tracker.get() and available and not self.app.busy else 'disabled')
        self.export_button.configure(state='normal' if self.plan and (self.plan['changes'] or self.plan.get('roundtrip',{}).get('bindings')) and not self.app.busy else 'disabled')
        self.open_button.configure(state='normal' if self.last_output and not self.app.busy else 'disabled')
        self.reuse_button.configure(state='normal' if self.last_output and not self.app.busy else 'disabled')
        self.scope_button.configure(state='normal' if self.source_kind.get()=='airtable' and self.scope_context and not self.app.busy else 'disabled')

    def pick_tracker(self):
        if self.app.busy:return
        value=filedialog.askopenfilename(parent=self.app.root,title='选择原始 All Tracker 汇总表',filetypes=[('Excel 总表','*.xlsx')],initialdir=self.app.workspace)
        if value:self.tracker.set(value)

    def pick_reports(self):
        if self.app.busy:return
        values=filedialog.askopenfilenames(parent=self.app.root,title='选择一份或多份周报（只解析 Report）',filetypes=[('Excel 周报','*.xlsx')],initialdir=self.app.workspace)
        for value in values:
            path=str(Path(value).resolve())
            if path not in self.reports:self.reports.append(path)
        if values:self.update_files()

    def remove_report(self):
        if self.app.busy:return
        for i in reversed(self.file_list.curselection()):self.reports.pop(i)
        self.update_files()

    def update_files(self):
        self.file_list.delete(0,'end')
        for path in self.reports:self.file_list.insert('end',Path(path).name)
        self.invalidate()

    def preview(self):
        if self.source_kind.get()=='writeback':return self.preview_writeback()
        if self.source_kind.get()=='airtable':return self.preview_airtable()
        if self.app.busy or not self.tracker.get() or not self.reports:return
        from .config import ROOT
        tracker=self.tracker.get();paths=list(self.reports);use_ai=self.use_ai.get();config=self.app._config()
        override=self.app.report_date.get().strip() or None
        if use_ai and not config.get('deepseek_api_key'):
            self.app._notice('DeepSeek 解析需要 API Key；不勾选时可直接本地解析。','warning');return
        self.invalidate();revision=(self.app._revision,self.revision)
        def action(send):
            from .workbook import read_workbook,parse_local
            hashes={str(Path(p).resolve()):fingerprint(p) for p in [tracker,*paths]}
            reports=[]
            for i,path in enumerate(paths,1):
                send('status',f'本地总表 · 正在解析周报 {i}/{len(paths)}')
                evidence=read_workbook(path,report_date=override,date_order=config.get('date_order','AUTO'))
                if use_ai:
                    from .deepseek import DeepSeekClient
                    with DeepSeekClient(config['deepseek_api_key'],base_url=config['deepseek_base_url'],model=config['deepseek_model'],cache_dir=ROOT/'.local/model-cache') as client:
                        report=client.parse(evidence,progress=lambda *args:send('status',' '.join(map(str,args))))
                else:report=parse_local(evidence)
                reports.append(report)
            send('status','正在按项目编号与总表列标题核对差异…')
            plan=build_tracker_plan(tracker,reports);plan['source_kind']='weekly'
            if any(fingerprint(p)!=h for p,h in hashes.items()):raise ValueError('读取期间文件变化，请重新预览。')
            plan['source_files']={p:h for p,h in hashes.items() if p!=str(Path(tracker).resolve())}
            folder=ROOT/'Run Logs'/('tracker_'+datetime.now().strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:6]);folder.mkdir(parents=True)
            (folder/'tracker_preview.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
            send('tracker_preview',(plan,revision))
        self.app._start(action,config)

    def preview_airtable(self):
        if self.app.busy:return False
        from .ui import ROOT
        config=self.app._config();context=deepcopy(self.scope_context)
        if not all(config.get(k) for k in ('airtable_token','base_id')):
            self.app._notice('请先配置 Airtable Token 和数据库，再读取当前数据。','warning');return False
        if context and (self.scope_credentials!=self.app._credential_key() or context.get('base_id')!=config['base_id']):
            self.app._notice('本次同步的连接配置已变化，请核对数据库；可选择“改为全库匹配”开始新的只读预览。','warning');return False
        if not self.valid_tracker():
            self.app._notice('请选择一个存在的 .xlsx All Tracker 总表文件。','warning');return False
        project_ids=list(context['project_ids']) if context else None
        if project_ids==[]:
            self.summary.set('本次同步没有已确认变更项目，无需自动读取或更新本地总表。');return False
        tracker=self.tracker.get();self.invalidate();revision=(self.app._revision,self.revision)
        self.summary.set('Airtable 已同步，正在重新读取云端数据生成本地预览…' if context else '正在读取 Airtable 当前数据生成本地预览…')
        def action(send):
            from .airtable import AirtableClient
            from .schema_memory import SchemaMemoryStore
            from .workflow import prepare_airtable_tracker
            send('status','Airtable → 本地总表 · 正在读取更新后的云端数据…')
            with AirtableClient(config['airtable_token'],config['base_id'],on_event=lambda event:send('network',event)) as client:
                plan=prepare_airtable_tracker(client,tracker,config,SchemaMemoryStore(ROOT/'.local/schema-memory'),
                    project_ids=project_ids,progress=lambda event:send('status',f"本地总表 · 正在读取 Airtable {event.get('table','表结构')} · {event.get('records',0)} 条"))
            folder=ROOT/'Run Logs'/('tracker_airtable_'+datetime.now().strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:6]);folder.mkdir(parents=True)
            (folder/'tracker_preview.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
            send('tracker_preview',(plan,revision))
        return self.app._start(action,config,job_context={'kind':'airtable_tracker','cloud_synced':bool(context),'revision':revision})

    def preview_failed(self,message,revision,cloud_synced=False):
        if revision!=(self.app._revision,self.revision):return
        self.plan=None
        prefix='Airtable 已同步，本地总表尚未更新。' if cloud_synced else 'Airtable 数据读取未完成，本地总表尚未更新。'
        self.summary.set(prefix+' 点击“读取 Airtable 并预览”只重试读取。')
        self.app._notice(prefix+' '+str(message),'error',network=self.app._job_network_failed)
        self.app.status.set(prefix+' 可只读重试，不会再次执行同步写入。');self.refresh_controls()

    def render(self,payload):
        plan,revision=payload
        if revision!=(self.app._revision,self.revision):
            self.invalidate();self.summary.set('文件或设置已变化，本次本地预览已过期，请重新读取。');return
        self.plan=plan;self.filter()
        airtable=plan.get('source_kind')=='airtable'
        self.tree.heading('after',text='Airtable 新值' if airtable else '周报新值')
        from .ui import set_text
        set_text(self.notes,'\n\n'.join(f'{i:03}  {w}' for i,w in enumerate(plan['warnings'],1)) or '无额外提示。')
        self.summary.set(f"{plan['source_projects']} 个源项目 · 唯一匹配 {plan['matched_projects']} 个 · {len(plan['changes'])} 个单元格拟变更 · {len(plan['warnings'])} 条提示")
        if airtable:
            source=plan.get('airtable_source',{});scope=source.get('scope_project_ids')
            scope_text='全库匹配' if source.get('scope')=='all_projects' or scope is None else f'仅本次 {len(scope)} 个项目'
            self.source_summary.set(f"来源：Airtable {source.get('base_id','')} · {scope_text} · 采集时间：{source.get('captured_at','未提供')}")
        self.app.status.set('本地预览完成 · 导出副本中更新单元格将标为绿色底色')
        if airtable and self.scope_context:
            self.app._notice('Airtable 已同步，本地总表预览已生成。核对变更后导出 Excel 副本。','success')
        self.refresh_controls()

    def filter(self):
        self.tree.delete(*self.tree.get_children());self.rows={};query=self.query.get().strip().casefold()
        for i,row in enumerate((self.plan or {}).get('changes',[])):
            if query and query not in ' '.join(str(v) for v in row.values()).casefold():continue
            self.rows[str(i)]=row
            self.tree.insert('','end',iid=str(i),values=(row['project_id'],row['cell'],row['field'],str(row['before'] if row['before'] is not None else '')[:160],str(row['after'])[:160]))

    def select(self,_=None):
        from .ui import set_text
        selected=self.tree.selection()
        if not selected:return
        row=self.rows[selected[0]]
        self.detail.pack(side='bottom',fill='x')
        set_text(self.detail,f"{row['project_id']} · {row['cell']} · {row['field']}\n当前：{row['before']}\n更新：{row['after']}\n来源：{row['report']}  {row['source']}")

    def export(self):
        if self.app.busy or not self.plan or not (self.plan['changes'] or self.plan.get('roundtrip',{}).get('bindings')):return
        source=Path(self.plan['tracker_path'])
        destination=filedialog.asksaveasfilename(parent=self.app.root,title='导出更新后的总表副本',initialdir=source.parent,
            initialfile=source.stem+'_更新_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.xlsx',defaultextension='.xlsx',filetypes=[('Excel 总表','*.xlsx')])
        if not destination:return
        plan=deepcopy(self.plan);self._export_plan=deepcopy(plan);revision=(self.app._revision,self.revision)
        self.plan=None;self.refresh_controls()
        def action(send):
            send('status','正在保存并校验总表副本，保留原生格式与公式…')
            result=export_tracker(plan,destination);send('tracker_exported',(result,revision))
        self.app._start(action,self.app._config(),job_context={'kind':'tracker_export','revision':revision,
            'cloud_synced':bool(self.scope_context) and plan.get('source_kind')=='airtable'})

    def exported(self,result,revision=None):
        self.last_output=result['output'];self.plan=None;self._export_plan=None
        if revision is not None and revision!=(self.app._revision,self.revision):
            self.summary.set('副本已导出，但输入或设置已变化；新输入请重新生成预览。');self.refresh_controls();return
        self.summary.set(f"已导出 {result['changed_cells']} 个单元格变更，新增绿色底色标记更新（不表示任务完成）。")
        self.app._notice('本地总表已导出。请在 Excel 中刷新公式、透视表及外部链接。','success')
        self.app.status.set('导出完成 · 原始汇总表未覆盖');self.refresh_controls()

    def export_failed(self,message,revision,cloud_synced=False):
        if revision!=(self.app._revision,self.revision):return
        self.plan=deepcopy(self._export_plan)
        prefix='Airtable 已同步，本地总表导出尚未完成。' if cloud_synced else '本地总表导出尚未完成。'
        self.summary.set(prefix+' 可重新导出副本；源文件有变化时请重新预览。')
        self.app._notice(prefix+' '+str(message),'error')
        self.app.status.set(prefix+' 再次导出仅写本地副本。');self.refresh_controls()

    def use_output(self):
        if self.app.busy or not self.last_output:return
        if not Path(self.last_output).is_file():
            self.app._notice('导出副本已移动或不存在，请重新选择输入总表。','warning');return
        self.tracker.set(str(self.last_output))
        self.app.settings['local_tracker_path']=str(self.last_output)
        self.summary.set('已将导出副本作为下次输入；点击“保存连接设置”可记住该路径。')

    def open_output(self):
        if self.last_output:self.app._open_path(Path(self.last_output).parent)

    def preview_writeback(self):
        if self.app.busy or not self.valid_tracker():return False
        from .config import ROOT
        config=self.app._config();path=self.tracker.get()
        if not all(config.get(k) for k in ('airtable_token','base_id')):
            self.app._notice('请先配置 Airtable 连接。','warning');return False
        self.app.filename.set(path)
        self.app._invalidate()
        revision=self.app._revision;before=fingerprint(path)
        def action(send):
            from .airtable import AirtableClient
            from .schema_memory import SchemaMemoryStore
            from .workflow import prepare_tracker_writeback
            from .preview import save_preview
            with AirtableClient(config['airtable_token'],config['base_id'],on_event=lambda event:send('network',event)) as client:
                plan,effective=prepare_tracker_writeback(client,path,config,SchemaMemoryStore(ROOT/'.local/schema-memory'),
                    progress=lambda event:send('status',f"回写预览 · 正在读取 {event.get('table','表结构')} · {event.get('records',0)} 条"))
            if fingerprint(path)!=before:raise ValueError('预览期间总表变化，请重新读取。')
            report={'source':path,'report_date':None,'projects':[], 'warnings':[]}
            for guard in plan['project_guards']:
                report['projects'].append({'project_id':guard['project_id'],'report_date':guard['report_date'],
                    'fields':{},'tasks':[],'issues':[],'source':path})
            directory=ROOT/'Run Logs'/('tracker_writeback_'+datetime.now().strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:6])
            save_preview(report,plan,directory)
            send('preview',(report,plan,directory,effective,revision,before))
        self.app._navigate(0)
        return self.app._start(action,config)
