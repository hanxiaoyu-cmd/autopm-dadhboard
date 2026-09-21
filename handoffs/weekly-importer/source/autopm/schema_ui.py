"""Review and persist schema bindings without mutating Airtable schema."""
from collections import deque
from copy import deepcopy
import queue
import threading
import tkinter as tk
from tkinter import ttk

from .airtable import AirtableClient
from .config import redact
from .schema_memory import DEFAULT_FIELDS, SchemaMemoryError, reconcile, schema_hash
from .schema_advisor import suggest_mappings
from .design import C, FONT


class SchemaEditor(tk.Toplevel):
    def __init__(self,parent,schema,config,store,on_saved,*,on_network=None):
        super().__init__(parent)
        self.title("表结构与映射记忆")
        self.geometry("1080x700");self.minsize(850,600)
        self.configure(background=C['bg'])
        style=ttk.Style(self)
        style.configure('Memory.TFrame',background=C['bg'])
        style.configure('Memory.TLabel',background=C['bg'],foreground=C['ink'],font=(FONT,-13))
        self.transient(parent);self.grab_set()
        self.schema,self.config,self.store,self.on_saved=schema,deepcopy(config),store,on_saved
        self.on_network=on_network;self._network_events=deque(maxlen=80);self._network_window=None
        self.selections={"tables":{},"fields":{}};self.busy=False;self.events=queue.Queue();self.controls=[]
        self.status=tk.StringVar();self.table_vars={};self._rows={};self.memory=None
        memory_error=None
        try: self.memory=store.load(config["base_id"])
        except SchemaMemoryError as exc: memory_error=str(exc)+" 本页核对后保存可重建。"
        ttk.Label(self,style='Memory.TLabel',text="按 Base 记住已验证的表和字段 ID；改名可自动适应，删除或类型变化需重新核对。",wraplength=810).pack(anchor="w",padx=18,pady=(16,6))
        ttk.Label(self,style='Memory.TLabel',text="只保存本地映射，不修改 Airtable 表结构。DS 建议只填入待确认选择。",wraplength=810).pack(anchor="w",padx=18)
        top=ttk.Frame(self,style='Memory.TFrame');top.pack(fill="x",padx=18,pady=12)
        self.table_labels={f"{t['name']}  ·  {t['id']}":t["id"] for t in schema["tables"]}
        initial=reconcile(schema,config,self.memory)
        for i,kind in enumerate(DEFAULT_FIELDS):
            top.columnconfigure(i,weight=1)
            ttk.Label(top,style='Memory.TLabel',text=kind.title()).grid(row=0,column=i,sticky="w")
            var=tk.StringVar(value=next((label for label,tid in self.table_labels.items() if tid==initial["table_ids"].get(kind)),""))
            combo=ttk.Combobox(top,textvariable=var,values=list(self.table_labels),state="readonly",width=18)
            combo.grid(row=1,column=i,sticky="ew",padx=(0,6));self.controls.append(combo);self.table_vars[kind]=var
            combo.bind("<<ComboboxSelected>>",lambda _,k=kind:self._table_changed(k))
        frame=ttk.Frame(self,style='Memory.TFrame');frame.pack(fill="both",expand=True,padx=18)
        self.tree=ttk.Treeview(frame,height=5,columns=("kind","key","name","type","status"),show="headings",selectmode="browse")
        for col,title,width in (("kind","表",95),("key","业务字段",185),("name","当前 Airtable 字段",290),("type","类型",130),("status","检查结果",245)):
            self.tree.heading(col,text=title);self.tree.column(col,width=width,minwidth=70)
        scroll=ttk.Scrollbar(frame,orient="vertical",command=self.tree.yview);self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right",fill="y");self.tree.pack(side="left",fill="both",expand=True)
        self.tree.bind("<<TreeviewSelect>>",self._select)
        row=ttk.Frame(self,style='Memory.TFrame');row.pack(fill="x",padx=18,pady=12)
        ttk.Label(row,style='Memory.TLabel',text="为选中业务字段指定目标：").pack(side="left")
        self.field_var=tk.StringVar();self.field_combo=ttk.Combobox(row,textvariable=self.field_var,state="readonly",width=55)
        self.field_combo.pack(side="left",fill="x",expand=True,padx=8);self.controls.append(self.field_combo)
        assign=ttk.Button(row,text="设为此映射",command=self._assign);assign.pack(side="right");self.controls.append(assign)
        ttk.Label(self,style='Memory.TLabel',textvariable=self.status,wraplength=810,foreground="#996600").pack(fill="x",padx=18,pady=(0,8))
        buttons=ttk.Frame(self,style='Memory.TFrame');buttons.pack(fill="x",padx=18,pady=(0,16))
        for text,action in (("DS 建议缺失映射",self._suggest),("重新读取表结构",self._refresh),("确认并保存记忆",self._save)):
            button=ttk.Button(buttons,text=text,command=action);button.pack(side="left",padx=(0,10));self.controls.append(button)
        ttk.Button(buttons,text="网络报告",command=self._show_network_report).pack(side="right")
        self._refresh_rows();self.protocol("WM_DELETE_WINDOW",self._close)
        if memory_error:self.status.set(memory_error)
        self._timer=self.after(100,self._poll)

    def _table_changed(self,kind):
        self.selections["tables"][kind]=self.table_labels[self.table_vars[kind].get()]
        self.selections["fields"].pop(kind,None);self._refresh_rows()

    def _refresh_rows(self):
        self.state_data=reconcile(self.schema,self.config,self.memory,selections=self.selections)
        self.tree.delete(*self.tree.get_children());self._rows={}
        for i,row in enumerate(self.state_data["rows"]):
            iid=str(i);self._rows[iid]=row
            self.tree.insert("","end",iid=iid,values=(row["kind"],row["key"],row["field_name"] or "—",row["type"],row["status"]))
        if self.state_data["blockers"]: self.status.set("；".join(self.state_data["blockers"][:3]))
        else: self.status.set("核对映射后点击保存；缺失的可选字段仍会在导入时提示。")

    def _select(self,_=None):
        selected=self.tree.selection()
        if not selected:return
        row=self._rows[selected[0]]
        table=next((t for t in self.schema["tables"] if t["id"]==row["table_id"]),None)
        self.field_labels={"不导入此字段（仅限可选字段）":None}
        if table:self.field_labels.update({f"{f['name']}  ·  {f['type']}  ·  {f['id']}":f["id"] for f in table["fields"]})
        self.field_combo.configure(values=list(self.field_labels))
        self.field_var.set(next((label for label,fid in self.field_labels.items() if fid==row["field_id"]),""))

    def _assign(self):
        selected=self.tree.selection()
        if self.busy or not selected or self.field_var.get() not in getattr(self,"field_labels",{}):return
        row=self._rows[selected[0]]
        self.selections["fields"].setdefault(row["kind"],{})[row["key"]]=self.field_labels[self.field_var.get()]
        self._refresh_rows()

    def _run(self,action,callback):
        if self.busy:return
        self.busy=True
        for control in self.controls:control.configure(state="disabled")
        if self._network_window is not None and self._network_window.winfo_exists():
            self._network_window.retry_button.configure(state="disabled")
        def worker():
            try:self.events.put((True,action(),callback))
            except Exception as exc:self.events.put((False,redact(exc,self.config),None))
        threading.Thread(target=worker,daemon=True).start()

    def _suggest(self):
        if not self.config.get("deepseek_api_key"):
            self.status.set("DS 建议需要 DeepSeek Key；手动映射和本地解析同步无需 Key。");return
        selections=deepcopy(self.selections)
        self.status.set("DS 正在根据当前结构和已验证历史记忆提出建议…")
        def done(proposals):
            reasons=[]
            for p in proposals["tables"]:
                self.selections["tables"][p["kind"]]=p["table_id"]
                self.table_vars[p["kind"]].set(next(label for label,tid in self.table_labels.items() if tid==p["table_id"]))
                reasons.append(p["reason"])
            for p in proposals["fields"]:
                self.selections["fields"].setdefault(p["kind"],{})[p["key"]]=p["field_id"];reasons.append(p["reason"])
            self._refresh_rows()
            self.status.set(f"已填入 {len(reasons)} 条待确认建议，尚未保存。"+"；".join(reasons)[:400])
        self._run(lambda:suggest_mappings(self.schema,self.config,self.memory,selections),done)

    def _fresh_schema(self):
        with AirtableClient(self.config["airtable_token"],self.config["base_id"],
                            on_event=lambda event:self.events.put(("network",event,None))) as client:return client.get_schema()

    def _network_report_text(self):
        from .ui import network_report_text
        return network_report_text(self._network_events)

    def _show_network_report(self):
        from .ui import NetworkReportWindow
        if self._network_window is None or not self._network_window.winfo_exists():
            self._network_window=NetworkReportWindow(self,self._network_report_text,self._retry_connection)
        self._network_window.refresh(self.busy)
        self._network_window.deiconify();self._network_window.lift()

    def _retry_connection(self):
        self._run(self._fresh_schema,lambda schema:self.status.set("连接检测成功，当前待保存映射已保留。"))

    def _refresh(self):
        def done(schema):
            self.schema=schema;self.selections={"tables":{},"fields":{}}
            self.table_labels={f"{t['name']}  ·  {t['id']}":t["id"] for t in schema["tables"]}
            for combo in self.controls[:5]:combo.configure(values=list(self.table_labels))
            state=reconcile(schema,self.config,self.memory)
            for kind,var in self.table_vars.items():var.set(next((label for label,tid in self.table_labels.items() if tid==state["table_ids"].get(kind)),""))
            self._refresh_rows()
        self._run(self._fresh_schema,done)

    def _save(self):
        state=reconcile(self.schema,self.config,self.memory,selections=self.selections)
        if state["blockers"]:self.status.set("；".join(state["blockers"][:3]));return
        expected=schema_hash(self.schema)
        def action():
            fresh=self._fresh_schema()
            if schema_hash(fresh)!=expected:raise SchemaMemoryError("保存前表结构已变化，请重新读取并核对。")
            self.store.save(state["memory"])
            return state["memory"]
        def done(memory):
            self.memory=memory;self.on_saved();self.status.set("已保存到此 Base 的长期映射记忆。请重新解析或生成同步预览。")
        self._run(action,done)

    def _poll(self):
        try:
            while True:
                ok,value,callback=self.events.get_nowait()
                if ok == "network":
                    self._network_events.append(deepcopy(value))
                    self.status.set(value.get("message",""))
                    if self.on_network:self.on_network(value)
                    if self._network_window is not None and self._network_window.winfo_exists():
                        self._network_window.refresh(self.busy)
                    continue
                self.busy=False
                for control in self.controls:control.configure(state="readonly" if isinstance(control,ttk.Combobox) else "normal")
                if self._network_window is not None and self._network_window.winfo_exists():
                    self._network_window.retry_button.configure(state="normal")
                if ok:callback(value)
                else:self.status.set(str(value))
        except queue.Empty:pass
        self._timer=self.after(100,self._poll)

    def _close(self):
        if self.busy:self.status.set("任务正在执行，请等待当前请求完成后关闭。");return
        self.after_cancel(self._timer);self.grab_release();self.destroy()
