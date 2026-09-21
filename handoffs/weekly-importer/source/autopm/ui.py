"""A focused desktop workspace: select, review, synchronize."""

from __future__ import annotations

from collections import deque
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import queue
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import uuid
from PIL import ImageTk

from .config import DEFAULTS, ROOT, import_legacy, load_settings, redact, save_settings
from . import __version__
from .preview import save_preview, enrich_display
from .local_files import workspace_root, scan_local_files
from .presentation import build_review_data, filter_change_rows, filter_warning_rows

from .design import C, FONT, rounded_buttons, rounded_image
from .glass import GlassButton, GlassLabel, GlassScene
from .brand import window_identity, monogram, glyph, ASSET_ROOT


def label(parent, text="", size=15, color=None, bold=False, bg=None, **kwargs):
    return GlassLabel(
        parent,
        text=text,
        font=(FONT, -max(size, 14), "bold" if bold else "normal"),
        bg=bg or parent.cget("bg"),
        fg=color or C["ink"],
        bd=0,
        **kwargs,
    )


def panel(parent):
    frame = tk.Frame(parent, bg=C["card"], highlightthickness=0)
    frame._glass_panel = True
    return frame


def readonly_text(parent, height=4, bg=None, size=14):
    widget = tk.Text(
        parent,
        height=height,
        wrap="word",
        bg=bg or C["card"],
        fg=C["ink"],
        font=(FONT, -size),
        relief="flat",
        borderwidth=0,
        padx=12,
        pady=9,
        selectbackground="#CFE0FF",
        insertwidth=0,
        cursor="arrow",
    )
    widget.configure(state="disabled")
    return widget


def set_text(widget, text):
    widget.configure(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", text)
    widget.configure(state="disabled")


def fingerprint(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(part)
    return digest.hexdigest()


def network_report_text(events):
    """Format already-sanitized transport events for display and copying."""
    if not events:
        return "尚无网络请求记录。点击“重新检测连接”可只读验证 Airtable 连接。"
    stages = {
        "request": "正在请求",
        "retry": "等待重试",
        "recovered": "请求成功",
        "failed": "请求失败",
    }
    lines = [
        "Airtable 网络报告",
        "以下为本次打开程序以来的近期记录（最多 80 条，最新记录在前）。",
        "报告不包含 Token、请求正文或记录内容。",
        "",
    ]
    for event in reversed(events):
        title = stages.get(event.get("stage"), "网络状态")
        lines.append(f"[{event.get('at', '')}] {title}")
        lines.append(str(event.get("report") or event.get("message") or "无详细信息"))
        lines.append("─" * 48)
    return "\n".join(lines)


class NetworkReportWindow(tk.Toplevel):
    """A modeless report viewer; callers update it only from their Tk queue."""

    def __init__(self, parent, report_provider, retry):
        super().__init__(parent)
        self.title("Airtable · 网络报告")
        self.geometry("880x640")
        self.minsize(600, 420)
        self.configure(bg=C["bg"])
        self.transient(parent)
        self.report_provider = report_provider
        label(self, "网络诊断与重试记录", 22, bold=True, anchor="w").pack(
            fill="x", padx=22, pady=(20, 8)
        )
        label(
            self,
            "重新检测只读取连接与表结构，不会重复执行之前的写入。",
            13,
            C["muted"],
            anchor="w",
            wraplength=760,
        ).pack(fill="x", padx=22, pady=(0, 14))
        frame = tk.Frame(self, bg=C["card"])
        frame.pack(fill="both", expand=True, padx=22)
        self.text = readonly_text(frame, size=14)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        actions = tk.Frame(self, bg=C["bg"])
        actions.pack(fill="x", padx=22, pady=16)
        self.retry_button = GlassButton(
            actions, text="重新检测连接", command=retry, style="Primary.TButton"
        )
        self.retry_button.pack(side="left")
        self.copy_button = GlassButton(
            actions, text="复制报告", command=self.copy_report
        )
        self.copy_button.pack(side="left", padx=10)
        self.copy_status = label(actions, "", 12, C["muted"])
        self.copy_status.pack(side="left")
        GlassButton(actions, text="关闭", command=self.destroy).pack(side="right")
        self.refresh()

    def refresh(self, busy=False):
        report = self.report_provider()
        if report != self.text.get("1.0", "end-1c"):
            position = self.text.yview()[0]
            set_text(self.text, report)
            self.text.yview_moveto(0 if position < 0.002 else position)
            self.copy_status.configure(text="")
        self.retry_button.configure(state="disabled" if busy else "normal")

    def copy_report(self):
        self.clipboard_clear()
        self.clipboard_append(self.report_provider())
        self.copy_status.configure(text="已复制安全报告")


class AutoPMApp:
    def __init__(self, root):
        self.root, self.workspace = root, workspace_root(ROOT)
        root.title(f"AutoPM · 周报工作台 v{__version__}")
        root.geometry(
            f"{min(1560, root.winfo_screenwidth() - 80)}x{min(1040, root.winfo_screenheight() - 80)}"
        )
        root.minsize(1200, 760)
        root.configure(bg=C["bg"])
        window_identity(root)
        self.events = queue.Queue()
        self.busy = False
        self.plan = self.report = self.run_dir = self.plan_settings = None
        self._revision, self._job_id, self._preview_revision = 0, None, None
        self._source_fingerprint, self._job_started, self._filter_timer = None, 0, None
        self._rows, self._row_lookup, self._view_data = [], {}, {}
        self._stale, self._active_page, self._warning_category = False, 0, None
        self._controls, self._library_buttons = [], []
        self._network_events = deque(maxlen=80)
        self._network_window = None
        self._job_network_failed = False
        self._job_credentials = None
        self._job_context = None
        self._pending_tracker_followup = None
        self._last_sync_context = self._last_sync_credentials = None
        self._connection_verified = self._connection_verified_at = None
        self._connection_state = None
        self.local_files = scan_local_files(self.workspace)
        try:
            self.settings = load_settings()
        except Exception:
            self.settings = dict(DEFAULTS)
        legacy = self.workspace / "All Projects Tracker SUNNY (1)" / "sync_config.json"
        if not self.settings.get("airtable_token") and legacy.exists():
            self.settings.update(import_legacy(legacy))
        self.values = {
            key: tk.StringVar(value=self.settings.get(key, ""))
            for key in (*DEFAULTS, "deepseek_api_key", "airtable_token")
        }
        self._connection_credentials = self._credential_key()
        self._last_airtable_token = self.values["airtable_token"].get().strip()
        self.filename, self.report_date = tk.StringVar(), tk.StringVar()
        self.date_mode = tk.StringVar(value="due_only")
        self.require_milestone = tk.BooleanVar(
            value=self.settings.get("require_milestone", True)
        )
        self.auto_tracker = tk.BooleanVar(
            value=self.settings.get("sync_local_tracker_after_sync", True)
        )
        self.status = tk.StringVar(value="就绪 · 选择一份周报开始")
        self.summary = tk.StringVar(value="选择周报，核对变更后同步到 Airtable。")
        self.search, self.kind_filter = tk.StringVar(), tk.StringVar(value="全部类型")
        self.warning_search = tk.StringVar()
        self._build()
        root.bind("<Configure>", self._responsive, add="+")
        for value in (
            self.filename,
            self.report_date,
            self.date_mode,
            self.require_milestone,
            *self.values.values(),
        ):
            value.trace_add("write", self._invalidate)
        self.values["airtable_token"].trace_add("write", self._token_changed)
        self.search.trace_add("write", self._schedule_filter)
        self.kind_filter.trace_add("write", self._schedule_filter)
        self.warning_search.trace_add("write", lambda *_: self._show_warnings())
        self._refresh_controls()
        self._connection_badge()
        root.after(100, self._poll)
        root.protocol("WM_DELETE_WINDOW", self._close)

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=(FONT, -16))
        style.configure(
            "TButton",
            background=C["card"],
            foreground=C["ink"],
            borderwidth=0,
            relief="flat",
            padding=(16, 10),
            focusthickness=0,
        )
        style.map(
            "TButton",
            background=[("active", "#EDF2F9"), ("disabled", "#F0F3F8")],
            foreground=[("disabled", "#A6B0BF")],
        )
        style.configure(
            "Primary.TButton",
            background=C["blue"],
            foreground="white",
            font=(FONT, -15, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("disabled", "#DCE6F7"), ("active", "#175EEA")],
            foreground=[("disabled", "#8A9DBD"), ("!disabled", "white")],
        )
        style.configure(
            "Link.TButton", background=C["bg"], foreground=C["blue"], padding=(8, 5)
        )
        style.map(
            "Link.TButton",
            background=[("active", C["blue_light"]), ("disabled", C["bg"])],
        )
        style.configure(
            "TEntry",
            fieldbackground="#F8FAFD",
            foreground=C["ink"],
            bordercolor=C["line"],
            lightcolor=C["line"],
            darkcolor=C["line"],
            padding=8,
            insertcolor=C["ink"],
        )
        style.map(
            "TEntry",
            bordercolor=[("focus", C["blue"])],
            fieldbackground=[("disabled", "#F0F3F7")],
        )
        style.configure(
            "TCombobox",
            fieldbackground="white",
            background="white",
            bordercolor=C["line"],
            padding=7,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "white")],
            foreground=[("readonly", C["ink"])],
        )
        for name in ("TCheckbutton", "TRadiobutton"):
            style.configure(
                name, background="white", foreground=C["ink"], padding=(0, 5)
            )
            style.map(name, background=[("active", "white")])
        style.configure(
            "Treeview",
            background="white",
            fieldbackground="white",
            foreground=C["ink"],
            borderwidth=0,
            rowheight=39,
            font=(FONT, -15),
            bordercolor=C["line"],
            lightcolor="white",
            darkcolor="white",
        )
        style.map(
            "Treeview",
            background=[("selected", "#EAF1FF")],
            foreground=[("selected", "#174AAB")],
        )
        style.configure(
            "Treeview.Heading",
            background="#F7F9FC",
            foreground=C["muted"],
            font=(FONT, -14),
            borderwidth=0,
            padding=(10, 11),
            relief="flat",
        )
        style.map("Treeview.Heading", background=[("active", "#EDF2FA")])
        style.layout("Pages.TNotebook.Tab", [])
        style.configure(
            "Pages.TNotebook",
            background=C["bg"],
            borderwidth=0,
            tabmargins=0,
            bordercolor=C["bg"],
            lightcolor=C["bg"],
            darkcolor=C["bg"],
        )
        style.configure(
            "Thin.Horizontal.TProgressbar",
            background=C["blue"],
            troughcolor=C["line"],
            borderwidth=0,
            thickness=3,
            lightcolor=C["blue"],
            darkcolor=C["blue"],
        )
        style.configure(
            "Vertical.TScrollbar",
            background="#CBD6E5",
            troughcolor="white",
            borderwidth=0,
            arrowsize=10,
            relief="flat",
        )
        self._style_images = rounded_buttons(style, self.root)
        style.layout("Link.TButton", style.layout("TButton"))
        style.configure("Link.TButton", padding=(12, 7))

    def _button(
        self, parent, text, command, primary=False, controlled=False, link=False
    ):
        widget = GlassButton(
            parent,
            text=text,
            command=command,
            style="Primary.TButton"
            if primary
            else ("Link.TButton" if link else "TButton"),
        )
        if controlled:
            self._controls.append(widget)
        return widget

    def _build(self):
        self._style()
        self.sidebar = tk.Frame(
            self.root,
            bg=C["nav"],
            width=212,
            highlightbackground=C["line"],
            highlightthickness=1,
        )
        self.sidebar._glass_panel = True
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        brand = tk.Frame(self.sidebar, bg=C["nav"])
        brand.pack(fill="x", padx=22, pady=(27, 3))
        mark = tk.Canvas(brand, width=38, height=38, bg=C["nav"], highlightthickness=0)
        mark.pack(side="left", padx=(0, 10))
        self._brand_image = ImageTk.PhotoImage(monogram(38), master=mark)
        mark.create_image(0, 0, image=self._brand_image, anchor="nw")
        label(brand, "AutoPM", 25, C["ink"]).pack(side="left")
        label(self.sidebar, "周报与项目同步", 13, C["muted"], anchor="w").pack(
            fill="x", padx=23, pady=(10, 37)
        )
        label(self.sidebar, "工作空间", 12, C["muted"], anchor="w").pack(
            fill="x", padx=26, pady=(0, 12)
        )
        self.nav_buttons = []
        self.nav_icons = []
        for i, text in enumerate(("周报导入", "本地文件", "连接设置", "本地总表")):
            icon_name = ("report", "folder", "connection", "tracker")[i]
            icons = tuple(
                ImageTk.PhotoImage(glyph(icon_name, 23, color), master=self.root)
                for color in (C["muted"], C["blue"])
            )
            self.nav_icons.append(icons)
            button = GlassButton(
                self.sidebar,
                text=text,
                style="Nav.TButton",
                cursor="hand2",
                image=icons[0],
                compound="left",
                command=lambda n=i: self._navigate(n),
                takefocus=True,
            )
            button.pack(fill="x", padx=14, pady=4)
            self.nav_buttons.append(button)
        bottom = tk.Frame(self.sidebar, bg=C["nav"])
        bottom.pack(side="bottom", fill="x", padx=24, pady=25)
        tk.Frame(bottom, height=1, bg=C["line"]).pack(fill="x", pady=(0, 17))
        label(bottom, "本地文件 · 云端同步", 13, C["ink"], anchor="w").pack(fill="x")
        label(bottom, "每一处变更，确认后写入", 12, C["muted"], anchor="w").pack(
            fill="x", pady=(7, 0)
        )
        shell = tk.Frame(self.root, bg=C["bg"])
        shell.pack(side="left", fill="both", expand=True)
        top = tk.Frame(shell, bg="white", height=56)
        top.pack(fill="x")
        top.pack_propagate(False)
        self.breadcrumb = label(
            top, f"AutoPM v{__version__}  /  周报导入", 13, C["muted"]
        )
        self.breadcrumb.pack(side="left", padx=26)
        self.connection = label(top, "", 12, C["muted"], bg="#F5F8FC", padx=13, pady=6)
        self.connection.pack(side="right", padx=(9, 24))
        self.network_button = self._button(
            top, "网络报告", self._show_network_report, link=True
        )
        self.network_button.pack(side="right", padx=4)
        self.motion_button = self._button(
            top, "动效 · 开", self._toggle_motion, link=True
        )
        self.motion_button.pack(side="right", padx=8)
        self.model_label = label(
            top, "DEEPSEEK V4 FLASH", 11, C["blue"], bg=C["blue_light"], padx=13, pady=6
        )
        tk.Frame(shell, height=1, bg=C["line"]).pack(fill="x")
        footer = tk.Frame(shell, bg="white")
        footer.pack(side="bottom", fill="x")
        progress_track = tk.Frame(footer, bg=C["line"], height=3)
        progress_track.pack(fill="x")
        self.progress = ttk.Progressbar(
            progress_track, mode="indeterminate", style="Thin.Horizontal.TProgressbar"
        )
        self.progress.place(x=0, y=0, relwidth=1, relheight=1)
        status_row = tk.Frame(footer, bg="white")
        status_row.pack(fill="x", padx=25, pady=10)
        self.elapsed_label = label(status_row, "LOCAL · READY", 11, C["muted"])
        self.elapsed_label.pack(side="right", padx=(20, 0))
        label(
            status_row, textvariable=self.status, size=12, color=C["muted"], anchor="w"
        ).pack(side="left", fill="x", expand=True)
        self.notice = tk.Frame(shell, bg=C["blue_light"])
        self.notice._glass_exempt = True
        self.notice_label = label(
            self.notice, "", 13, C["blue"], anchor="w", justify="left", padx=16, pady=10
        )
        self.notice_report_button = self._button(
            self.notice, "查看网络报告 →", self._show_network_report, link=True
        )
        self.notice_label.pack(side="left", fill="x", expand=True)
        self.notebook = ttk.Notebook(shell, style="Pages.TNotebook", takefocus=False)
        self.notebook.pack(fill="both", expand=True)
        self.pages = []
        for text in ("周报导入", "本地文件", "连接设置", "本地总表"):
            page = tk.Frame(self.notebook, bg=C["bg"])
            self.pages.append(page)
            self.notebook.add(page, text=text)
        self._build_import(self.pages[0])
        self._build_library(self.pages[1])
        self._build_settings(self.pages[2])
        from .tracker_ui import TrackerPage

        self.tracker_page = TrackerPage(self, self.pages[3])
        self.glass = GlassScene(self.root)
        self.motion_button.configure(
            text="动效 · 开" if self.glass.enabled else "动效 · 关"
        )
        self._navigate(0)

    def _page_title(self, parent, title, subtitle):
        frame = tk.Frame(parent, bg=C["bg"], height=65)
        frame.pack(fill="x", padx=26, pady=(23, 15))
        frame.pack_propagate(False)
        heading = label(frame, title, 29, anchor="w")
        heading._title_x = 48
        heading.place(x=48, y=0)
        caption = label(frame, subtitle, 14, C["muted"], anchor="w")
        caption._title_x = 48
        caption.place(x=48, y=41)
        kind = {
            "周报导入": "report",
            "本地文件": "folder",
            "连接设置": "connection",
            "本地总表": "tracker",
        }.get(title, "report")
        icon = tk.Canvas(frame, width=34, height=38, bg=C["bg"], highlightthickness=0)
        icon.place(x=0, y=2)
        icon._brand_glyph = ImageTk.PhotoImage(glyph(kind, 32), master=icon)
        icon.create_image(17, 18, image=icon._brand_glyph)
        parent._title_items = [(heading, 0, C["ink"]), (caption, 41, C["muted"])]

    def _build_import(self, parent):
        self._page_title(parent, "周报导入", "选择周报，核对变更后同步到 Airtable。")
        steps = tk.Frame(parent, bg=C["bg"])
        steps.pack(fill="x", padx=27, pady=(0, 12))
        self.step_labels = []
        for number, text in (
            ("01", "选择周报"),
            ("02", "核对变更"),
            ("03", "写入 Airtable"),
            ("04", "本地总表"),
        ):
            item = label(steps, f"{number}  {text}", 12, C["muted"])
            item.pack(side="left", padx=(0, 20))
            self.step_labels.append(item)
        self.date_toggle = self._button(
            steps, "日期补充", self._toggle_date, controlled=True, link=True
        )
        self.date_toggle.pack(side="right", padx=10)
        self.source_card = panel(parent)
        self.source_card.pack(fill="x", padx=26, pady=(0, 12))
        icon = tk.Canvas(
            self.source_card, width=44, height=48, bg="white", highlightthickness=0
        )
        icon.pack(side="left", padx=(19, 15), pady=15)
        icon._brand_glyph = ImageTk.PhotoImage(glyph("report", 33), master=icon)
        icon.create_image(22, 24, image=icon._brand_glyph)
        file_text = tk.Frame(self.source_card, bg="white")
        file_text.pack(side="left", fill="both", expand=True, pady=17)
        self.file_title = label(
            file_text, "选择一份 Excel 周报", 16, bold=True, anchor="w"
        )
        self.file_title.pack(fill="x")
        self.file_subtitle = label(
            file_text,
            "支持 .xlsx  ·  自动识别项目、任务与问题",
            12,
            C["muted"],
            anchor="w",
        )
        self.file_subtitle.pack(fill="x", pady=(6, 0))
        self.ai_button = self._button(
            self.source_card, "AI 解析并预览", lambda: self._analyze(True), True, True
        )
        self.ai_button.pack(side="right", padx=(8, 17))
        self.local_button = self._button(
            self.source_card, "规则检查", lambda: self._analyze(False), controlled=True
        )
        self.local_button.pack(side="right", padx=(8, 0))
        self.pick_button = self._button(
            self.source_card, "选择文件", self._pick, controlled=True
        )
        self.pick_button.pack(side="right", padx=(12, 0))
        file_text.pack_configure(after=self.pick_button)
        self.file_title.bind(
            "<Configure>",
            lambda e: self.file_title.configure(wraplength=max(220, e.width)),
        )
        self.date_row = panel(parent)
        label(self.date_row, "补充缺失的周报日期", 13).pack(
            side="left", padx=14, pady=9
        )
        self.date_entry = ttk.Entry(
            self.date_row, textvariable=self.report_date, width=14, font=(FONT, -14)
        )
        self.date_entry.pack(side="left", padx=8)
        self._controls.append(self.date_entry)
        label(
            self.date_row, "YYYY-MM-DD；文件内已有的项目日期始终优先", 12, C["muted"]
        ).pack(side="left", padx=10)
        self.metric_frame = tk.Frame(parent, bg=C["bg"])
        self.metrics = []
        for i, (name, detail) in enumerate(
            (
                ("识别项目", "来自当前周报"),
                ("拟变更记录", "项目 / 任务 / 问题"),
                ("提示与检查", "查看分类后处理"),
            )
        ):
            self.metric_frame.columnconfigure(i, weight=1, uniform="metrics")
            card = panel(self.metric_frame)
            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(0 if i == 0 else 6, 0 if i == 2 else 6),
            )
            number = label(card, "—", 27, C["blue"] if i < 2 else C["amber"], True)
            number.pack(side="left", padx=18, pady=10)
            stack = tk.Frame(card, bg="white")
            stack.pack(side="left", pady=10)
            label(stack, name, 13, bold=True, anchor="w").pack(fill="x")
            caption = label(stack, detail, 11, C["muted"], anchor="w")
            caption.pack(fill="x", pady=(3, 0))
            self.metrics.append((number, caption))
        self.result_container = panel(parent)
        self.result_container.pack(fill="both", expand=True, padx=26, pady=(0, 20))
        self._build_empty(self.result_container)
        self.review = tk.Frame(self.result_container, bg="white")
        toolbar = tk.Frame(self.review, bg="white")
        toolbar.pack(fill="x", padx=16, pady=(5, 0))
        self.result_buttons = {}
        for key, text in (("changes", "变更明细"), ("warnings", "提示与检查")):
            button = GlassButton(
                toolbar,
                text=text,
                cursor="hand2",
                command=lambda k=key: self._select_result(k),
            )
            button.pack(side="left", padx=(0, 7))
            self.result_buttons[key] = button
        self.logs_button = self._button(toolbar, "打开本次日志 ↗", self._open_logs)
        self.logs_button.pack(side="right")
        tk.Frame(self.review, height=1, bg=C["line"]).pack(fill="x")
        self.change_page = tk.Frame(self.review, bg="white")
        self.warning_page = tk.Frame(self.review, bg="white")
        filters = tk.Frame(self.change_page, bg="white")
        filters.pack(fill="x", padx=16, pady=10)
        self.search_entry = ttk.Entry(
            filters, textvariable=self.search, width=30, font=(FONT, -14)
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Escape>", lambda _: self.search.set(""))
        label(filters, "搜索项目、任务、字段或内容", 11, C["muted"]).pack(
            side="left", padx=10
        )
        self.kind_combo = ttk.Combobox(
            filters,
            textvariable=self.kind_filter,
            state="readonly",
            width=10,
            font=(FONT, -14),
            values=("全部类型", "项目", "任务", "问题"),
        )
        self.kind_combo.pack(side="right")
        self.row_count = label(filters, "", 11, C["muted"])
        self.row_count.pack(side="right", padx=12)
        self.apply_bar = tk.Frame(self.review, bg="#F8FAFD")
        self.apply_bar.pack(side="bottom", fill="x")
        self.apply_button = self._button(
            self.apply_bar, "确认写入 Airtable", self._apply, True
        )
        self.apply_button.pack(side="right", padx=16, pady=10)
        self.local_preview_button = self._button(
            self.apply_bar, "本地结果 → Airtable 预览", self._connect_local
        )
        self.local_preview_button.pack(side="right", pady=10)
        self.write_scope = label(self.apply_bar, "", 12, C["muted"], anchor="w")
        self.write_scope.pack(side="left", fill="x", expand=True, padx=18)
        self.write_scope.bind(
            "<Configure>",
            lambda event: self.write_scope.configure(wraplength=max(180, event.width)),
        )
        followup_bar = tk.Frame(self.review, bg="white")
        followup_bar.pack(side="bottom", fill="x", before=self.apply_bar)
        self.auto_tracker_check = ttk.Checkbutton(
            followup_bar, text="同步后生成本地总表预览", variable=self.auto_tracker
        )
        self.auto_tracker_check.pack(side="left", padx=18, pady=5)
        self._controls.append(self.auto_tracker_check)
        self.tracker_followup_button = self._button(
            followup_bar, "Airtable → 本地总表", self._open_tracker_followup
        )
        self.tracker_followup_button.pack(side="right", padx=16, pady=4)
        self.detail = tk.Frame(
            self.change_page,
            bg="#F8FAFD",
            highlightbackground=C["line"],
            highlightthickness=1,
        )
        self.detail._glass_exempt = True
        titlebar = tk.Frame(self.detail, bg="#F8FAFD")
        titlebar.pack(fill="x", padx=12, pady=(7, 1))
        self.detail_title = label(titlebar, "", 13, bold=True, anchor="w")
        self.detail_title.pack(side="left", fill="x", expand=True)
        self._button(titlebar, "收起 ×", self._hide_detail, link=True).pack(
            side="right"
        )
        self.detail_source = label(self.detail, "", 11, C["muted"], anchor="w")
        self.detail_source.pack(fill="x", padx=13, pady=(0, 6))
        values = tk.Frame(self.detail, bg="#F8FAFD")
        values.pack(fill="both", expand=True, padx=12, pady=(0, 9))
        values.columnconfigure((0, 1), weight=1, uniform="detail")
        self.detail_texts = []
        for i, (text, color, bg) in enumerate(
            (("当前值", C["muted"], "#EFF3F8"), ("周报新值", C["blue"], "#EDF3FF"))
        ):
            col = tk.Frame(values, bg=bg)
            col.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(0 if i == 0 else 5, 5 if i == 0 else 0),
            )
            label(col, text, 11, color, bold=True, padx=12, pady=4).pack(anchor="w")
            content = readonly_text(col, 2, bg=bg)
            scroll = ttk.Scrollbar(col, orient="vertical", command=content.yview)
            scroll.pack(side="right", fill="y")
            content.configure(yscrollcommand=scroll.set)
            content.pack(fill="both", expand=True)
            self.detail_texts.append(content)
        table = self.table_frame = tk.Frame(self.change_page, bg="white")
        table.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(
            table,
            columns=("project", "kind", "action", "record", "field", "before", "after"),
            show="headings",
            selectmode="browse",
        )
        for name, text, width in (
            ("project", "项目", 96),
            ("kind", "类型", 58),
            ("record", "任务 / 项目 / 问题", 220),
            ("action", "操作", 58),
            ("field", "字段", 165),
            ("before", "当前值", 240),
            ("after", "周报新值", 250),
        ):
            self.tree.heading(name, text=text, anchor="w")
            self.tree.column(
                name,
                width=width,
                minwidth=50,
                stretch=name not in {"project", "kind", "action"},
            )
        scroll = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(fill="both", expand=True)
        self.tree.tag_configure("odd", background="#FAFBFE")
        self.tree.bind("<<TreeviewSelect>>", self._show_row)
        self.tree.bind("<Double-1>", self._show_row)
        self.tree.bind("<Return>", self._show_row)
        self.no_matches = label(
            table,
            "没有匹配内容 · 可清空搜索或切换类型",
            14,
            C["muted"],
            bg="white",
            padx=20,
            pady=20,
        )
        warning_filters = tk.Frame(self.warning_page, bg="white")
        warning_filters.pack(fill="x", padx=16, pady=(10, 0))
        warning_entry = ttk.Entry(
            warning_filters,
            textvariable=self.warning_search,
            width=30,
            font=(FONT, -14),
        )
        warning_entry.pack(side="left")
        warning_entry.bind("<Escape>", lambda _: self.warning_search.set(""))
        label(warning_filters, "搜索项目编号或提示内容", 11, C["muted"]).pack(
            side="left", padx=10
        )
        self.warning_groups = tk.Frame(self.warning_page, bg="white")
        self.warning_groups.pack(fill="x", padx=15, pady=(10, 4))
        body = tk.Frame(self.warning_page, bg="white")
        body.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        self.notes = readonly_text(body, 12)
        scroll = ttk.Scrollbar(body, orient="vertical", command=self.notes.yview)
        scroll.pack(side="right", fill="y")
        self.notes.configure(yscrollcommand=scroll.set)
        self.notes.pack(fill="both", expand=True)
        self._select_result("changes")

    def _build_empty(self, parent):
        self.empty = tk.Frame(parent, bg="white")
        self.empty.pack(fill="both", expand=True)
        content = tk.Frame(self.empty, bg="white")
        content.place(relx=0.5, rely=0.48, anchor="center", relwidth=0.88)
        icon = tk.Canvas(content, width=96, height=84, bg="white", highlightthickness=0)
        icon.pack(pady=(0, 20))
        icon._brand_glyph = ImageTk.PhotoImage(glyph("sync", 80), master=icon)
        icon.create_image(48, 42, image=icon._brand_glyph)
        label(content, "导入周报，开始同步", 27).pack()
        label(
            content,
            "读取 Report 工作表，集中核对项目、里程碑与问题变更。",
            15,
            C["muted"],
        ).pack(pady=(12, 23))
        actions = tk.Frame(content, bg="white")
        actions.pack()
        self._button(
            actions, "选择 Excel 周报", self._pick, primary=True, controlled=True
        ).pack(side="left", padx=6)
        self._button(actions, "查看本地资料", lambda: self._navigate(1)).pack(
            side="left", padx=6
        )
        weekly = [item for item in self.local_files if item["kind"] == "weekly"]
        if weekly:
            label(content, "也可以使用本地已有的周报", 12, C["muted"]).pack(
                pady=(26, 10)
            )
            buttons = tk.Frame(content, bg="white")
            buttons.pack()
            for item in weekly:
                button = self._button(
                    buttons,
                    item["label"] + "  ↗",
                    lambda p=item["path"]: self._choose(p),
                    controlled=True,
                )
                button.pack(side="left", padx=6)
                self._library_buttons.append(button)
        label(
            content,
            "规则检查可离线运行  ·  更新 Excel 请前往“本地总表”",
            12,
            C["muted"],
        ).pack(pady=(22, 0))

    def _scroll_page(self, parent):
        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        inner = tk.Frame(canvas, bg=C["bg"])
        window = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        inner.bind(
            "<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>", lambda e: canvas.itemconfigure(window, width=e.width)
        )

        def wheel(event):
            if self.notebook.select() == str(parent):
                canvas.yview_scroll(int(-event.delta / 120), "units")

        parent.bind_all("<MouseWheel>", wheel, add="+")
        return inner

    def _build_library(self, parent):
        self._page_title(parent, "本地文件", "看清资料用途，直接选用已有周报。")
        area = self._scroll_page(parent)
        intro = tk.Frame(area, bg=C["bg"])
        intro.pack(fill="x", padx=26, pady=(0, 14))
        label(intro, "原始资料", 14, bold=True).pack(side="left")
        self._button(
            intro,
            "打开资料文件夹 ↗",
            lambda: self._open_path(self.workspace / "All Projects Tracker SUNNY (1)"),
            link=True,
        ).pack(side="right")
        if not self.local_files:
            label(
                area,
                "当前文件夹没有附带样例。可在“周报导入”选择自己的 .xlsx 文件。",
                15,
                C["muted"],
                pady=35,
            ).pack()
        for item in self.local_files:
            card = panel(area)
            card.pack(fill="x", padx=26, pady=(0, 11))
            text = tk.Frame(card, bg="white")
            text.pack(side="left", fill="both", expand=True, padx=18, pady=15)
            title = tk.Frame(text, bg="white")
            title.pack(fill="x")
            role = {
                "weekly": "可导入周报",
                "tracker": "参考总表",
                "rules": "规则说明",
                "legacy": "历史程序",
            }[item["kind"]]
            label(
                title,
                role,
                11,
                C["blue"] if item["kind"] == "weekly" else C["muted"],
                bg=C["blue_light"] if item["kind"] == "weekly" else "#F1F4F8",
                padx=8,
                pady=3,
            ).pack(side="left")
            label(title, item["label"], 17, bold=True).pack(side="left", padx=12)
            label(text, item["filename"], 12, C["muted"], anchor="w").pack(
                fill="x", pady=(9, 4)
            )
            label(
                text,
                "  ·  ".join(filter(None, (item["date_label"], item["size_text"]))),
                12,
                C["ink"],
                anchor="w",
            ).pack(fill="x")
            label(
                text,
                item["description"],
                12,
                C["muted"],
                anchor="w",
                justify="left",
                wraplength=830,
            ).pack(fill="x", pady=(5, 0))
            if item["kind"] == "weekly":
                button = self._button(
                    card,
                    "用于导入 →",
                    lambda p=item["path"]: self._choose(p),
                    True,
                    True,
                )
                self._library_buttons.append(button)
            else:
                target = (
                    Path(item["path"]).parent
                    if item["kind"] == "legacy"
                    else Path(item["path"])
                )
                button = self._button(
                    card,
                    "所在文件夹 ↗" if item["kind"] == "legacy" else "打开查看 ↗",
                    lambda p=target: self._open_path(p),
                )
            button.pack(side="right", padx=18)
            text.pack_configure(after=button)
            for child in text.winfo_children():
                if isinstance(child, tk.Label):
                    child.bind(
                        "<Configure>",
                        lambda e, w=child: w.configure(wraplength=max(220, e.width)),
                    )
        guide = panel(area)
        guide.pack(fill="x", padx=26, pady=(7, 22))
        label(guide, "项目文件怎么用", 16, bold=True, anchor="w").pack(
            fill="x", padx=18, pady=(16, 9)
        )
        lines = "日常操作   在“周报导入”选择周报、核对变更并同步。\n资料来源   原始资料目录含总 Tracker、两份周报、规则 PPT 和旧版程序。\n同步结果   Airtable 同步成功后，可读取更新后的云端数据生成本地总表预览，核对后导出新版 Excel 副本；原表保留。\n源码与记录   autopm 是源码；docs 是说明；Run Logs 是操作记录；.local 保存加密配置与缓存。"
        label(
            guide, lines, 13, C["muted"], justify="left", anchor="w", wraplength=1020
        ).pack(fill="x", padx=18, pady=(0, 13))
        self._button(
            guide, "打开项目文件夹 ↗", lambda: self._open_path(self.workspace)
        ).pack(anchor="w", padx=18, pady=(0, 16))

    def _setting_entry(self, parent, key, title):
        label(parent, title, 13, bold=True, anchor="w").pack(fill="x", pady=(12, 6))
        entry = ttk.Entry(
            parent,
            textvariable=self.values[key],
            font=(FONT, -14),
            show="●" if key in ("deepseek_api_key", "airtable_token") else "",
        )
        entry.pack(fill="x")
        self._controls.append(entry)

    def _build_settings(self, parent):
        self._page_title(parent, "连接设置", "保存一次，之后直接选择周报开始。")
        area = self._scroll_page(parent)
        two = tk.Frame(area, bg=C["bg"])
        two.pack(fill="x", padx=26)
        two.columnconfigure((0, 1), weight=1, uniform="settings")
        for i, title in enumerate(("AI 解析", "Airtable 数据")):
            card = panel(two)
            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(0 if i == 0 else 9, 9 if i == 0 else 0),
            )
            body = tk.Frame(card, bg="white")
            body.pack(fill="both", expand=True, padx=22, pady=20)
            label(
                body,
                "01  /  DEEPSEEK" if i == 0 else "02  /  AIRTABLE",
                11,
                C["blue"],
                anchor="w",
            ).pack(fill="x")
            label(body, title, 20, bold=True, anchor="w").pack(fill="x", pady=(7, 3))
            if i == 0:
                self._setting_entry(body, "deepseek_api_key", "API Key")
                self._setting_entry(body, "deepseek_model", "模型")
                self._setting_entry(body, "deepseek_base_url", "API 地址")
                label(
                    body,
                    "解析时会发送所选周报的文本、日期与样式证据。",
                    12,
                    C["muted"],
                    anchor="w",
                    wraplength=460,
                ).pack(fill="x", pady=(14, 0))
            else:
                self._setting_entry(body, "airtable_token", "完整 Token（Token Key）")
                label(
                    body,
                    "粘贴创建时显示的完整密钥。Token ID 无需填写。",
                    12,
                    C["muted"],
                    anchor="w",
                    wraplength=440,
                ).pack(fill="x", pady=(8, 10))
                self._button(
                    body,
                    "检测并选择数据库",
                    self._discover_airtable,
                    primary=True,
                    controlled=True,
                ).pack(anchor="w")
                self._airtable_bases = []
                self.base_choice = tk.StringVar(
                    value=self.settings.get("base_name", "尚未检测")
                )
                self.base_picker = ttk.Combobox(
                    body,
                    textvariable=self.base_choice,
                    state="readonly",
                    font=(FONT, -13),
                )
                self.base_picker.pack(fill="x", pady=(14, 6))
                self.base_picker.bind(
                    "<<ComboboxSelected>>", self._select_airtable_base
                )
                self.base_hint = label(
                    body,
                    "检测后自动识别表格；多个数据库时按名称选择。",
                    12,
                    C["muted"],
                    anchor="w",
                    wraplength=440,
                )
                self.base_hint.pack(fill="x")
                self.table_fields = tk.Frame(body, bg="white")
                self._setting_entry(
                    self.table_fields, "base_id", "Base ID（app 开头，不是 Token ID）"
                )
                for key, text in (
                    ("projects_table_id", "Projects 表 ID"),
                    ("tasks_table_id", "Tasks 表 ID"),
                    ("issues_table_id", "Issues 表 ID"),
                ):
                    self._setting_entry(self.table_fields, key, text)
                self._button(
                    body, "高级设置：数据库和表 ID  +", self._toggle_tables
                ).pack(anchor="w", pady=(13, 0))
        rule = panel(area)
        rule.pack(fill="x", padx=26, pady=18)
        content = tk.Frame(rule, bg="white")
        content.pack(fill="x", padx=22, pady=18)
        label(content, "任务日期与里程碑", 17, bold=True, anchor="w").pack(
            fill="x", pady=(0, 10)
        )
        self._button(
            content, "表结构与映射记忆 →", self._open_schema_memory, controlled=True
        ).pack(anchor="w", pady=(0, 12))
        for text, value in (
            ("文本日期：自动判断，有月/日歧义时跳过", "AUTO"),
            ("文本日期：月 / 日（MDY）", "MDY"),
            ("文本日期：日 / 月（DMY）", "DMY"),
        ):
            radio = ttk.Radiobutton(
                content, text=text, variable=self.values["date_order"], value=value
            )
            radio.pack(anchor="w")
            self._controls.append(radio)
        label(
            content,
            "跨年或距离周报超过半年且未写年份的日期，需要在周报中补全年份。",
            12,
            C["muted"],
            anchor="w",
        ).pack(fill="x", pady=(5, 10))
        label(
            content,
            "里程碑日期 → Due Date：当前计划结束日期，直接使用周报有效日期。",
            12,
            anchor="w",
        ).pack(fill="x")
        label(content, "匹配已有里程碑；未匹配的有效日期任务仍导入，里程碑留空。", 12,
              anchor="w").pack(fill="x", pady=(8, 0))
        label(
            content,
            "保留已有开始日期和工期；划掉的旧日期忽略，只读取唯一有效的新日期。",
            12,
            C["muted"],
            anchor="w",
        ).pack(fill="x", pady=(8, 0))
        actions = tk.Frame(area, bg=C["bg"])
        actions.pack(fill="x", padx=26, pady=(0, 14))
        self.save_button = self._button(actions, "保存连接设置", self._save, True, True)
        self.save_button.pack(side="left")
        self.import_button = self._button(
            actions, "导入已有 sync_config.json", self._import, controlled=True
        )
        self.import_button.pack(side="left", padx=12)
        label(
            area,
            "密钥使用 Windows 加密保存，仅当前 Windows 用户可解密。",
            12,
            C["muted"],
            anchor="w",
        ).pack(fill="x", padx=27, pady=(0, 25))

    def _navigate(self, page):
        self._active_page = page
        self.notebook.select(page)
        self.breadcrumb.configure(
            text="AutoPM  /  " + ("周报导入", "本地文件", "连接设置", "本地总表")[page]
        )
        for i, button in enumerate(self.nav_buttons):
            button.configure(
                style="NavActive.TButton" if i == page else "Nav.TButton",
                image=self.nav_icons[i][int(i == page)],
            )
        if hasattr(self, "glass"):
            self.glass.enter_page(self.pages[page])
        self._update_source()

    def _toggle_motion(self):
        self.glass.set_motion(not self.glass.enabled)
        self.motion_button.configure(
            text="动效 · 开" if self.glass.enabled else "动效 · 关"
        )

    def _notice(self, text, kind="info", *, network=False):
        bg, fg = {
            "info": (C["blue_light"], "#2455A5"),
            "success": ("#E9F6F1", C["green"]),
            "warning": ("#FFF4DE", C["amber"]),
            "error": ("#FDEEF0", C["red"]),
        }[kind]
        self.notice.configure(bg=bg)
        if network:
            self.notice_report_button.pack(
                side="right", padx=(8, 16), before=self.notice_label
            )
        else:
            self.notice_report_button.pack_forget()
        self.notice_label.configure(
            text=text,
            bg=bg,
            fg=fg,
            wraplength=max(450, self.root.winfo_width() - (470 if network else 270)),
        )
        self.notice.pack(fill="x", before=self.notebook)

    def _config(self):
        return deepcopy(
            {
                **self.settings,
                **{k: v.get().strip() for k, v in self.values.items()},
                "task_date_mode": "due_only",
                "require_milestone": False,
                "project_identity_mode": "number_sku_factory",
                "sync_local_tracker_after_sync": self.auto_tracker.get(),
                "local_tracker_path": self.tracker_page.tracker.get().strip()
                if hasattr(self, "tracker_page")
                else self.settings.get("local_tracker_path", ""),
            }
        )

    def _credential_key(self, config=None):
        if config is not None:
            return tuple(
                str(config.get(k, "")).strip() for k in ("airtable_token", "base_id")
            )
        return tuple(
            self.values[k].get().strip() for k in ("airtable_token", "base_id")
        )

    def _connection_badge(self):
        complete = all(
            self.values[k].get().strip() for k in ("airtable_token", "base_id")
        )
        verified = self._connection_verified == self._credential_key() and complete
        if self._connection_state == "failed":
            text, color = "Airtable · 连接失败", C["red"]
        elif self._connection_state == "retry":
            text, color = "Airtable · 正在重试", C["amber"]
        elif verified:
            text, color = (
                f"Airtable · 已连接 {self._connection_verified_at}",
                C["green"],
            )
        elif self._connection_state == "success":
            text, color = (
                f"Airtable · 最近请求成功 {self._connection_verified_at}",
                C["green"],
            )
        else:
            text, color = (
                ("Airtable · 已填写，未验证" if complete else "Airtable · 待配置"),
                C["amber"],
            )
        self.connection.configure(text=text, fg=color)
        self.model_label.configure(
            text=self.values["deepseek_model"]
            .get()
            .strip()
            .upper()
            .replace("-", " ")[:34]
            or "未选择模型"
        )

    def _mark_connection_verified(self):
        self._connection_verified = self._credential_key()
        self._connection_verified_at = datetime.now().strftime("%H:%M")
        self._connection_state = None
        self._connection_badge()

    def _network_report_text(self):
        return network_report_text(self._network_events)

    def _show_network_report(self):
        if self._network_window is None or not self._network_window.winfo_exists():
            self._network_window = NetworkReportWindow(
                self.root, self._network_report_text, self._retry_connection
            )
        self._network_window.refresh(self.busy)
        self._network_window.deiconify()
        self._network_window.lift()

    def _retry_connection(self):
        """Start only discovery, never replay a previous operation or write plan."""
        if not self.busy:
            self._discover_airtable(self.values["base_id"].get().strip() or None)

    def _record_network_event(self, event, *, credentials=None):
        if credentials is not None and credentials != self._credential_key():
            return
        event = deepcopy(event)
        self._network_events.append(event)
        stage, message = event.get("stage"), str(event.get("message", ""))
        if message:
            self.status.set(message)
        if stage == "retry":
            self._connection_state = "retry"
            self._notice(message, "warning", network=True)
        elif stage == "failed":
            self._connection_state = "failed"
            self._connection_verified = None
            self._job_network_failed = True
            self._notice(message, "error", network=True)
        elif stage == "recovered":
            self._connection_state = "success"
            self._connection_verified_at = datetime.now().strftime("%H:%M")
            if event.get("attempt", 1) > 1:
                self._notice(message, "success", network=True)
        self._connection_badge()
        if self._network_window is not None and self._network_window.winfo_exists():
            self._network_window.refresh(self.busy)

    def _invalidate(self, *_):
        self._revision += 1
        credentials = self._credential_key()
        if credentials != self._connection_credentials:
            self._connection_credentials = credentials
            self._connection_verified = self._connection_verified_at = None
            self._connection_state = None
        if hasattr(self, "tracker_page"):
            self.tracker_page.invalidate()
        if self.report is not None:
            self.plan = None
            self._stale = True
            self._hide_detail()
            self._notice(
                "预览已过期：文件或设置已改变。请重新解析后再写入。", "warning"
            )
            self.write_scope.configure(text="预览已过期 · 当前列表仅供参考")
        self._update_source()
        self._connection_badge()
        self._refresh_controls()

    def _update_source(self):
        path = Path(self.filename.get())
        if self.filename.get():
            name = path.name
            self.file_title.configure(text=name if len(name) < 66 else name[:62] + "…")
            self.file_subtitle.configure(
                text=f"{path.parent.name}  ·  已选择周报，点击解析生成预览"
            )
            self.pick_button.configure(text="更换文件")
        else:
            self.file_title.configure(text="选择一份 Excel 周报")
            self.file_subtitle.configure(text="支持 .xlsx  ·  自动识别项目、任务与问题")
            self.pick_button.configure(text="选择文件")
        local_stage = self._active_page == 3 or bool(
            self._last_sync_context and self._stale
        )
        for i, active in enumerate(
            (
                not self.filename.get() and not local_stage,
                bool(self.filename.get() and not self.plan and not local_stage),
                bool(self.plan) and not local_stage,
                local_stage,
            )
        ):
            self.step_labels[i].configure(fg=C["blue"] if active else C["muted"])

    def _refresh_controls(self):
        for widget in self._controls:
            widget.configure(state="disabled" if self.busy else "normal")
        for button in (self.ai_button, self.local_button):
            button.configure(
                state="normal" if self.filename.get() and not self.busy else "disabled"
            )
        can_apply = (
            self.plan
            and self.plan.get("changes")
            and not self.plan.get("blockers")
            and not self._stale
            and not self.busy
        )
        self.apply_button.configure(state="normal" if can_apply else "disabled")
        self.local_preview_button.configure(
            state="normal"
            if self.report and not self.busy and not self._stale
            else "disabled"
        )
        self.tracker_followup_button.configure(
            state="disabled" if self.busy else "normal"
        )
        self.logs_button.configure(state="normal" if self.run_dir else "disabled")
        self.base_picker.configure(state="disabled" if self.busy else "readonly")
        if self._network_window is not None and self._network_window.winfo_exists():
            self._network_window.retry_button.configure(
                state="disabled" if self.busy else "normal"
            )
        if hasattr(self, "tracker_page"):
            self.tracker_page.refresh_controls()

    def _choose(self, path):
        if self.busy:
            return
        self.filename.set(str(path))
        self._navigate(0)
        if self.report is None:
            self.status.set("周报已选择 · 点击“解析并预览”继续，或先离线检查")

    def _pick(self):
        if self.busy:
            return
        initial = self.workspace / "All Projects Tracker SUNNY (1)"
        name = filedialog.askopenfilename(
            title="选择 Excel 周报",
            filetypes=[("Excel 周报", "*.xlsx")],
            initialdir=initial if initial.exists() else self.workspace,
        )
        if name:
            self._choose(name)

    def _toggle_date(self):
        if self.date_row.winfo_manager():
            self.date_row.pack_forget()
        else:
            self.date_row.pack(fill="x", padx=26, pady=(0, 12), after=self.source_card)

    def _toggle_tables(self):
        if self.table_fields.winfo_manager():
            self.table_fields.pack_forget()
        else:
            self.table_fields.pack(fill="x", pady=6)

    def _token_changed(self, *_):
        token = self.values["airtable_token"].get().strip()
        if token == self._last_airtable_token:
            return
        self._last_airtable_token = token
        self._airtable_bases = []
        self.base_picker.configure(values=())
        self.base_choice.set("Token 已更换，请重新检测")
        self.base_hint.configure(text="检测后自动识别表格；多个数据库时按名称选择。")
        self.values["base_id"].set("")
        self.settings.pop("base_name", None)
        for kind in ("projects", "tasks", "issues"):
            self.values[kind + "_table_id"].set("")

    def _discover_airtable(self, base_id=None):
        if self.busy:
            return
        config = self._config()

        def action(send):
            from .connection import discover_connection

            send("status", "正在验证 Token 并识别可访问的数据库…")
            send(
                "airtable_connection",
                discover_connection(
                    config.get("airtable_token", ""),
                    base_id,
                    on_event=lambda event: send("network", event),
                ),
            )

        self._start(action, config)

    def _select_airtable_base(self, *_):
        index = self.base_picker.current()
        if not self.busy and 0 <= index < len(self._airtable_bases):
            self.values["base_id"].set("")
            self._discover_airtable(self._airtable_bases[index]["id"])

    def _airtable_connection_ready(self, result):
        self._airtable_bases = result["bases"]
        choices = [f"{b['name']} · {b['id']}" for b in self._airtable_bases]
        self.base_picker.configure(values=choices)
        if "base" not in result:
            self.values["base_id"].set("")
            self.base_choice.set("请选择要更新的数据库")
            self._notice(
                f"Token 已验证，可访问 {len(choices)} 个数据库。请选择更新目标。"
            )
            return
        base = result["base"]
        self.base_picker.current(
            next(i for i, b in enumerate(self._airtable_bases) if b["id"] == base["id"])
        )
        self.values["base_id"].set(base["id"])
        self.settings["base_name"] = base["name"]
        for kind in ("projects", "tasks", "issues"):
            self.values[kind + "_table_id"].set(result["tables"][kind])
        self.base_hint.configure(text="已识别项目、任务、问题、人员和工厂表。")
        self._mark_connection_verified()
        self._notice(
            f"已连接 {base['name']}，表格已自动匹配。请保存连接设置。", "success"
        )

    def _save(self):
        if self.busy:
            return
        try:
            if self.values["base_id"].get().strip().startswith("pat"):
                self._notice(
                    "Base ID 中填写的是 Token ID，请点击“检测并选择数据库”。", "error"
                )
                return
            self.settings = self._config()
            save_settings(self.settings)
            self._notice(
                "连接设置已保存，密钥已加密。可以选择周报开始解析。", "success"
            )
            self.status.set("设置已保存")
        except Exception as exc:
            self._notice("保存失败：" + redact(exc, self._config()), "error")

    def _import(self):
        if self.busy:
            return
        path = filedialog.askopenfilename(
            title="导入已有连接",
            filetypes=[("JSON 配置", "*.json")],
            initialdir=self.workspace,
        )
        if path:
            try:
                for key, value in import_legacy(path).items():
                    self.values[key].set(value)
                self._notice("已导入 Airtable 连接。点击“保存连接设置”后生效。")
            except Exception as exc:
                self._notice("导入失败：" + redact(exc, self._config()), "error")

    def _start(self, action, config, *, job_context=None):
        if self.busy:
            return False
        self.busy = True
        self._job_id, self._job_started = uuid.uuid4().hex, time.monotonic()
        job, config = self._job_id, deepcopy(config)
        self._job_credentials = self._credential_key(config)
        self._job_context = deepcopy(job_context)
        self._job_network_failed = False
        self.progress.start(12)
        self._refresh_controls()

        def send(kind, value):
            self.events.put((job, kind, value))

        def worker():
            try:
                action(send)
            except Exception as exc:
                send("error", redact(exc, config))
            finally:
                send("done", None)

        threading.Thread(target=worker, daemon=True).start()
        return True

    def _analyze(self, use_ai):
        if self.busy:
            return
        path, override, config = (
            self.filename.get(),
            self.report_date.get().strip() or None,
            self._config(),
        )
        if not path or not Path(path).is_file() or Path(path).suffix.lower() != ".xlsx":
            self._notice("请选择一个存在的 .xlsx 周报文件。", "error")
            return
        if use_ai and not all(
            config.get(k) for k in ("deepseek_api_key", "airtable_token", "base_id")
        ):
            self._navigate(2)
            self._notice(
                "还需要配置 DeepSeek API Key、Airtable PAT 和 Base ID，才能生成同步预览。",
                "warning",
            )
            return
        revision = self._revision
        self.plan = self.plan_settings = None
        self._stale = self.report is not None
        self._hide_detail()
        self.notice.pack_forget()
        self.status.set("正在读取周报文件…")
        self.write_scope.configure(text="正在生成新的预览 · 请等待完成")

        def action(send):
            from .workbook import read_workbook, parse_local

            preview_config = config
            before = fingerprint(path)
            evidence = read_workbook(
                path, report_date=override, date_order=config.get("date_order", "AUTO")
            )
            if fingerprint(path) != before:
                raise ValueError("读取期间周报文件发生变化，请保存 Excel 后重新解析。")
            if use_ai:
                from .deepseek import DeepSeekClient
                from .airtable import AirtableClient
                from .workflow import prepare_preview
                from .schema_memory import SchemaMemoryStore

                send("status", "正在使用 DeepSeek 解析并核对来源…")
                report = DeepSeekClient(
                    config["deepseek_api_key"],
                    base_url=config["deepseek_base_url"],
                    model=config["deepseek_model"],
                    cache_dir=ROOT / ".local/model-cache",
                ).parse(
                    evidence,
                    progress=lambda *args: send("status", " ".join(map(str, args))),
                )
                send("status", "正在读取 Airtable 当前数据，生成变更预览…")
                with AirtableClient(
                    config["airtable_token"],
                    config["base_id"],
                    on_event=lambda event: send("network", event),
                ) as client:
                    plan, preview_config = prepare_preview(
                        client,
                        report,
                        config,
                        SchemaMemoryStore(ROOT / ".local/schema-memory"),
                        progress=lambda event: send(
                            "status",
                            f"Airtable · {event.get('table', '表结构')} · 已读取 {event.get('records', 0)} 条",
                        ),
                    )
            else:
                report, plan = parse_local(evidence), None
            if fingerprint(path) != before:
                raise ValueError("解析期间周报文件发生变化，请重新解析当前文件。")
            directory = (
                ROOT
                / "Run Logs"
                / (datetime.now().strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6])
            )
            save_preview(report, plan, directory)
            send("preview", (report, plan, directory, preview_config, revision, before))

        self._start(action, config)

    def _connect_local(self):
        if self.busy or not self.report or self._stale:
            return
        config = self._config()
        if not all(config.get(k) for k in ("airtable_token", "base_id")):
            self._navigate(2)
            self._notice(
                "本地解析同步只需 Airtable PAT 和 Base ID，无需 DeepSeek Key。",
                "warning",
            )
            return
        path, before = self.filename.get(), self._source_fingerprint
        try:
            if fingerprint(path) != before:
                self._invalidate()
                return
        except OSError:
            self._invalidate()
            return
        report, revision = deepcopy(self.report), self._revision
        self.plan = None
        self.status.set("正在用本地解析结果读取 Airtable，生成同步预览…")

        def action(send):
            from .airtable import AirtableClient
            from .workflow import prepare_preview
            from .schema_memory import SchemaMemoryStore

            if fingerprint(path) != before:
                raise ValueError("源文件已变化，请重新解析。")
            with AirtableClient(
                config["airtable_token"],
                config["base_id"],
                on_event=lambda event: send("network", event),
            ) as client:
                plan, effective = prepare_preview(
                    client,
                    report,
                    config,
                    SchemaMemoryStore(ROOT / ".local/schema-memory"),
                    progress=lambda event: send(
                        "status",
                        f"Airtable · {event.get('table', '表结构')} · 已读取 {event.get('records', 0)} 条",
                    ),
                )
            if fingerprint(path) != before:
                raise ValueError("生成预览期间源文件已变化，请重新解析。")
            directory = (
                ROOT
                / "Run Logs"
                / (datetime.now().strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6])
            )
            save_preview(report, plan, directory)
            send("preview", (report, plan, directory, effective, revision, before))

        self._start(action, config)

    def _open_schema_memory(self):
        if self.busy:
            return
        config = self._config()
        if not all(config.get(k) for k in ("airtable_token", "base_id")):
            self._notice("请先填写 Airtable PAT 和 Base ID。", "warning")
            return

        def action(send):
            from .airtable import AirtableClient

            with AirtableClient(
                config["airtable_token"],
                config["base_id"],
                on_event=lambda event: send("network", event),
            ) as client:
                schema = client.get_schema()
            send("schema_editor", (schema, config))

        self._start(action, config)

    def _apply(self):
        if (
            self.busy
            or not self.plan
            or not self.plan.get("changes")
            or self.plan.get("blockers")
            or self._stale
        ):
            return
        try:
            if (
                self._preview_revision != self._revision
                or fingerprint(self.filename.get()) != self._source_fingerprint
            ):
                self._invalidate()
                self._notice("源文件或设置已发生变化。请重新解析后再写入。", "warning")
                return
        except OSError:
            self._invalidate()
            self._notice("源文件已移动或无法读取。请重新选择文件并解析。", "warning")
            return
        count = len(self.plan.get("changes", []))
        if not messagebox.askyesno(
            "确认同步完整预览",
            f"将写入当前完整预览中的 {count} 条记录变更。\n搜索、类型筛选和选中行仅用于查看，不改变本次写入范围。\n\n是否继续写入 Airtable？",
            parent=self.root,
        ):
            return
        config, plan, directory = (
            deepcopy(self.plan_settings),
            deepcopy(self.plan),
            self.run_dir,
        )
        context = {
            "base_id": config["base_id"],
            "plan_id": plan.get("plan_id", ""),
            "project_ids": sorted(
                {
                    str(change["project_id"])
                    for change in plan.get("changes", [])
                    if change.get("project_id")
                }
            ),
            "auto_tracker": bool(self.auto_tracker.get()),
        }
        revision = self._revision
        self._pending_tracker_followup = None
        self._last_sync_context = self._last_sync_credentials = None
        source_path, source_hash = self.filename.get(), self._source_fingerprint
        self.plan = None
        self._stale = True
        self.status.set("正在重新核对 Airtable 并写入变更…")
        self.write_scope.configure(text="正在写入已确认的完整预览")

        def action(send):
            from .airtable import AirtableClient
            from .sync import apply_plan

            if fingerprint(source_path) != source_hash:
                raise ValueError("确认期间周报文件发生变化，请重新解析后再写入。")
            with AirtableClient(
                config["airtable_token"],
                config["base_id"],
                on_event=lambda event: send("network", event),
            ) as client:
                result = apply_plan(client, plan, directory)
            send("applied", (result, context, revision))

        self._start(action, config)

    def _render(self, report, plan, directory, config, revision=None, source_hash=None):
        self.report, self.plan = deepcopy(report), deepcopy(plan)
        self.run_dir, self.plan_settings = Path(directory), deepcopy(config)
        self._preview_revision = self._revision if revision is None else revision
        self._source_fingerprint, self._stale = source_hash, False
        self._view_data = build_review_data(self.report, self.plan)
        self._rows = self._view_data["rows"]
        self.search.set("")
        self.kind_filter.set("全部类型")
        self.warning_search.set("")
        self._warning_category = None
        self.empty.pack_forget()
        self.review.pack(fill="both", expand=True)
        self._responsive()
        projects = self.report.get("projects", [])
        change_count, warnings = (
            len((self.plan or {}).get("changes", [])),
            self._view_data.get("warnings", []),
        )
        blockers = self._view_data.get("blockers", [])
        blocker_reason = self._short(blockers[0]["message"], 110) if blockers else ""
        self.metrics[0][0].configure(text=f"{len(projects):,}")
        dates = sorted(
            {p.get("report_date") or report.get("report_date") or "" for p in projects}
        )
        self.metrics[0][1].configure(text="更新至 " + (dates[-1] if dates else "—"))
        self.metrics[1][0].configure(
            text=f"{change_count:,}" if plan is not None else "—"
        )
        self.metrics[1][1].configure(
            text="全量记录 · 筛选仅影响查看"
            if plan is not None
            else "离线检查 · 尚未连接 Airtable"
        )
        self.metrics[2][0].configure(
            text=f"{len(warnings) + len(self._view_data.get('blockers', [])):,}"
        )
        self.metrics[2][1].configure(
            text=f"{len((plan or {}).get('blockers', []))} 项阻止写入"
            if (plan or {}).get("blockers")
            else "按类别查看来源与处理提示"
        )
        self.ai_button.configure(text="AI 重新解析")
        self.write_scope.configure(
            text=f"⚠ 发现 {change_count:,} 条拟变更 · 请点击上方「变更明细」Tab 仔细核对后再写入。"
            if plan is not None
            else "离线解析完成；可直接生成 Airtable 预览。"
        )
        no_changes = plan is not None and not change_count and not blockers
        if blockers:
            self.metrics[1][0].configure(text="受阻")
            self.metrics[1][1].configure(
                text=f"{len(blockers)} 项阻止写入 · 请查看提示"
            )
            self.write_scope.configure(
                text=f"预览受阻 · {blocker_reason}；请在“提示与检查”中处理后重新预览。"
            )
        elif no_changes:
            self.metrics[1][1].configure(text="已连接 Airtable · 查看提示中的跳过项")
            self.write_scope.configure(
                text="Airtable 比对完成 · 当前规则下无待写入变更；跳过项请查看“提示与检查”。"
            )
        self._hide_detail()
        self._render_warning_groups()
        self._filter_rows()
        self._select_result("warnings" if (plan or {}).get("blockers") else "changes")
        self._update_source()
        self.status.set(
            "预览已生成 · 选中一行查看完整值与来源"
            if plan is not None
            else "离线检查完成 · 已展示项目、任务和问题"
        )
        if blockers:
            self.status.set(f"预览受阻 · {blocker_reason}")
        elif no_changes:
            self.status.set(
                "Airtable 比对完成 · 0 条待写入；不代表提示中的跳过项已同步"
            )
        self._refresh_controls()

    def _responsive(self, event=None):
        if event is not None and event.widget != self.root:
            return
        if self.report is not None and self.root.winfo_height() >= 850:
            self.metric_frame.pack(
                fill="x", padx=26, pady=(0, 12), before=self.result_container
            )
        else:
            self.metric_frame.pack_forget()

    def _schedule_filter(self, *_):
        if self._filter_timer:
            self.root.after_cancel(self._filter_timer)
        self._filter_timer = self.root.after(140, self._filter_rows)

    def _filter_rows(self):
        if self._filter_timer:
            self.root.after_cancel(self._filter_timer)
        self._filter_timer = None
        kind = {"项目": "projects", "任务": "tasks", "问题": "issues"}.get(
            self.kind_filter.get()
        )
        rows = filter_change_rows(self._rows, query=self.search.get(), kind=kind)
        self.tree.delete(*self.tree.get_children())
        self._row_lookup = {}
        self._hide_detail()
        for i, row in enumerate(rows):
            self._row_lookup[str(i)] = row
            self.tree.insert(
                "",
                "end",
                iid=str(i),
                tags=("odd",) if i % 2 else (),
                values=(
                    row["project_id"],
                    row["kind_label"],
                    row["action_label"],
                    self._short(row["record_title"], 65),
                    row["field_name"],
                    self._short(row["before_text"], 95),
                    self._short(row["after_text"], 95),
                ),
            )
        self.row_count.configure(text=f"{len(rows):,} / {len(self._rows):,} 项字段")
        if rows:
            self.no_matches.place_forget()
        else:
            if self.plan is not None and self.plan.get("blockers"):
                message = "预览存在阻止项\n请在“提示与检查”中查看原因。"
            elif self._rows:
                message = "当前筛选没有匹配内容\n可清空搜索或切换类型。"
            elif self.plan is not None:
                compared = len(self.plan.get("project_guards", []))
                total = len((self.report or {}).get("projects", []))
                title = (
                    "已连接 Airtable · 当前规则下无需写入"
                    if compared
                    else "已连接 Airtable · 没有可纳入比对的项目"
                )
                message = f"{title}\n已纳入比对 {compared} / {total} 个项目。\n未匹配及被跳过的内容，请查看“提示与检查”。"
            else:
                message = (
                    "尚未生成 Airtable 变更预览\n请点击“本地结果 → Airtable 预览”。"
                )
            self.no_matches.configure(text=message)
            self.no_matches.place(relx=0.5, rely=0.45, anchor="center")

    @staticmethod
    def _short(value, limit):
        value = " ".join(str(value or "—").split())
        return value if len(value) <= limit else value[: limit - 1] + "…"

    def _show_row(self, event=None):
        selection = self.tree.selection()
        if not selection or self._stale:
            return
        row = self._row_lookup.get(selection[0])
        if not row:
            return
        self.detail_title.configure(
            text=self._short(
                f"{row['project_id']}  /  {row['record_title']}  /  {row['field_name']}",
                115,
            )
        )
        match_note = (
            (row.get("match_note", "") + " · ") if row.get("match_note") else ""
        )
        self.detail_source.configure(
            text=f"{row['action_label']}  ·  {match_note}来源：{self.report.get('source', '')}  {row['source']}"
        )
        set_text(self.detail_texts[0], row["before_text"] or "（空）")
        set_text(self.detail_texts[1], row["after_text"] or "（空）")
        self.detail.pack(
            side="bottom", fill="x", padx=12, pady=(0, 10), before=self.table_frame
        )

    def _hide_detail(self):
        if hasattr(self, "detail"):
            self.detail.pack_forget()
            for widget in self.detail_texts:
                set_text(widget, "")

    def _select_result(self, key):
        for page in (self.change_page, self.warning_page):
            page.pack_forget()
        (self.change_page if key == "changes" else self.warning_page).pack(
            fill="both", expand=True
        )
        for name, button in self.result_buttons.items():
            button.configure(style="Primary.TButton" if name == key else "TButton")

    def _render_warning_groups(self):
        for widget in self.warning_groups.winfo_children():
            widget.destroy()
        warnings, counts = (
            self._view_data.get("blockers", []) + self._view_data.get("warnings", []),
            {},
        )
        for item in warnings:
            counts.setdefault((item["category"], item["category_label"]), 0)
            counts[item["category"], item["category_label"]] += 1
        values = [(None, "全部", len(warnings))] + [
            (key, text, count) for (key, text), count in counts.items()
        ]
        for i, (key, text, count) in enumerate(values):
            button = GlassButton(
                self.warning_groups,
                text=f"{text}  {count}",
                cursor="hand2",
                style="Primary.TButton" if key == self._warning_category else "TButton",
                command=lambda k=key: self._filter_warnings(k),
            )
            button.grid(row=i // 6, column=i % 6, sticky="w", padx=(0, 6), pady=(0, 6))
        self._show_warnings()

    def _filter_warnings(self, category):
        self._warning_category = category
        self._render_warning_groups()

    def _show_warnings(self):
        warnings = filter_warning_rows(
            self._view_data.get("blockers", []) + self._view_data.get("warnings", []),
            query=self.warning_search.get(),
            category=self._warning_category,
        )
        text = "\n\n".join(
            f"{i:02d}  [{'阻止写入 · ' if item['severity'] == 'blocker' else ''}{item['category_label']}]  {item.get('short_text', '')}\n{item['message']}"
            for i, item in enumerate(warnings, 1)
        )
        set_text(self.notes, text or "没有匹配提示 · 可清空搜索或切换分类。")

    def _applied(self, result, context=None, revision=None):
        status = result.get("status")
        applied, skipped = result.get("applied", 0), result.get("skipped", 0)
        summary = result.get("summary", {})
        operations = result.get("operations", [])
        prefix = {
            "completed": "同步已完成",
            "partial": "部分记录已写入",
            "blocked": "本次写入已停止",
        }.get(status, "写入已结束")
        kind_labels = {
            "projects": "项目",
            "tasks": "任务",
            "issues": "问题",
        }
        detail_parts = []
        failed_total = 0
        for key, label in kind_labels.items():
            item = summary.get(key) or {}
            if not item.get("total"):
                continue
            failed_total += item.get("failed", 0)
            detail_parts.append(
                f"{label}：写入 {item.get('applied', 0)} / 跳过 {item.get('skipped', 0)} / 失败 {item.get('failed', 0)}"
            )
        message = f"{prefix}：已写入 {applied} 条，跳过 {skipped} 条。"
        if result.get("written_unverified"):
            message = (f"本次写入已停止：校验通过 {applied} 条，另有 {result['written_unverified']} 条"
                       "已返回写入成功但未通过回读校验，云端可能已改变。请先核对日志。")
        if detail_parts:
            message += "（" + " · ".join(detail_parts) + "）"
        message += "继续导入前请重新生成预览。"
        self._notice(
            message,
            "success" if status == "completed" and not failed_total else "error",
            network=self._job_network_failed,
        )
        self.status.set(message)
        self.write_scope.configure(text="本次预览已使用 · 请重新解析后继续")
        self.plan, self._stale = None, True
        self._hide_detail()
        self._pending_tracker_followup = None
        if status == "completed" and context:
            self._last_sync_context = deepcopy(context)
            self._last_sync_credentials = self._job_credentials
            if context.get("auto_tracker", True):
                if (
                    revision == self._revision
                    and self._job_credentials == self._credential_key()
                ):
                    self._pending_tracker_followup = (
                        self._job_id,
                        deepcopy(context),
                        revision,
                        self._job_credentials,
                    )
                    self.write_scope.configure(
                        text="Airtable 已同步 · 即将用更新后的云端数据预览本地总表"
                    )
                else:
                    self._notice(
                        "Airtable 已同步，本地总表尚未更新：文件或连接设置已变化，请核对后重新读取。",
                        "warning",
                    )
        elif status != "completed":
            self._last_sync_context = self._last_sync_credentials = None
        result_items = list(result.get("errors") or [])
        for op in operations:
            if op.get("status") != "failed":
                continue
            label = kind_labels.get(op.get("kind"), op.get("kind", "unknown"))
            ident = op.get("project_id") or op.get("project_record_id") or "未知记录"
            reason = {
                "uncertain_write": "写入结果不确定（创建后未获确认）",
                "write_error": "写入或校验失败",
                "verification_failed": "已返回写入成功，回读校验未通过",
            }.get(op.get("reason"), op.get("reason", "写入失败"))
            result_items.append(f"[{label}失败] {ident}：{reason}")
        if result_items:
            self._view_data["blockers"] = [
                {
                    "category": "write_result",
                    "category_label": "写入结果",
                    "severity": "blocker",
                    "message": str(error),
                    "project_id": "",
                    "search_text": str(error).casefold(),
                }
                for error in result_items
            ]
            self.warning_search.set("")
            self._warning_category = "write_result"
            self._render_warning_groups()
            self._select_result("warnings")
        self._update_source()

    def _open_tracker_followup(self):
        if self.busy:
            return
        if (
            self._last_sync_context
            and self._last_sync_credentials == self._credential_key()
        ):
            self.tracker_page.follow_sync(
                self._last_sync_context, self._last_sync_credentials
            )
        else:
            self.tracker_page.use_all_airtable()
            self._navigate(3)
            self.tracker_page.summary.set(
                "选择 All Tracker，读取 Airtable 当前数据后核对并导出副本。"
            )

    def _finish_tracker_followup(self, job):
        pending = self._pending_tracker_followup
        self._pending_tracker_followup = None
        if not pending or pending[0] != job:
            return
        _, context, revision, credentials = pending
        if revision != self._revision or credentials != self._credential_key():
            self._notice(
                "Airtable 已同步，本地总表尚未更新：文件或连接设置已变化，请核对后重新读取。",
                "warning",
            )
            return
        self.tracker_page.follow_sync(context, credentials)

    def _poll(self):
        try:
            while True:
                job, kind, payload = self.events.get_nowait()
                if job != self._job_id:
                    continue
                if kind == "status":
                    self.status.set(str(payload)[:125])
                elif kind == "network":
                    self._record_network_event(
                        payload, credentials=self._job_credentials
                    )
                elif kind == "preview":
                    if payload[4] != self._revision:
                        self.plan = None
                        self._notice(
                            "文件或设置已变化，本次解析结果已过期。请重新解析。",
                            "warning",
                        )
                    else:
                        self._render(*payload)
                elif kind == "schema_editor":
                    from .schema_ui import SchemaEditor
                    from .schema_memory import SchemaMemoryStore

                    credentials = self._credential_key(payload[1])
                    SchemaEditor(
                        self.root,
                        payload[0],
                        payload[1],
                        SchemaMemoryStore(ROOT / ".local/schema-memory"),
                        self._invalidate,
                        on_network=lambda event, key=credentials: (
                            self._record_network_event(event, credentials=key)
                        ),
                    )
                elif kind == "airtable_connection":
                    if self._job_credentials == self._credential_key():
                        self._airtable_connection_ready(payload)
                elif kind == "tracker_preview":
                    self.tracker_page.render(payload)
                elif kind == "tracker_exported":
                    if isinstance(payload, tuple):
                        self.tracker_page.exported(*payload)
                    else:
                        self.tracker_page.exported(payload)
                elif kind == "error":
                    self.plan = None
                    context = self._job_context or {}
                    if context.get("kind") == "airtable_tracker":
                        self.tracker_page.preview_failed(
                            payload,
                            context.get("revision"),
                            context.get("cloud_synced", False),
                        )
                    elif context.get("kind") == "tracker_export":
                        self.tracker_page.export_failed(
                            payload,
                            context.get("revision"),
                            context.get("cloud_synced", False),
                        )
                    else:
                        self._notice(
                            "操作未完成：" + str(payload),
                            "error",
                            network=self._job_network_failed,
                        )
                        self.status.set(
                            "操作未完成 · 请查看网络报告，可重新检测连接"
                            if self._job_network_failed
                            else "操作未完成 · 可查看提示后重新解析；已验证的缓存会继续复用"
                        )
                        self.write_scope.configure(text="本次操作未完成 · 无可执行预览")
                elif kind == "applied":
                    if isinstance(payload, tuple):
                        self._applied(*payload)
                    else:
                        self._applied(payload)
                elif kind == "done":
                    self.busy = False
                    self.progress.stop()
                    self._job_id = None
                    self._refresh_controls()
                    self._finish_tracker_followup(job)
        except queue.Empty:
            pass
        if self.busy:
            elapsed = int(time.monotonic() - self._job_started)
            self.elapsed_label.configure(
                text=f"运行中  {elapsed // 60:02d}:{elapsed % 60:02d}", fg=C["blue"]
            )
        else:
            self.elapsed_label.configure(text="LOCAL · READY", fg=C["muted"])
        self.root.after(100, self._poll)

    def _open_path(self, path):
        try:
            os.startfile(str(path))
        except OSError:
            self._notice(
                "无法打开此文件或文件夹，请检查文件是否存在及默认打开程序。", "error"
            )

    def _open_logs(self):
        if self.run_dir:
            self._open_path(self.run_dir)

    def _close(self):
        if self.busy:
            self._notice("当前操作仍在进行，请等待完成后关闭。", "warning")
        else:
            self.root.destroy()


def main():
    import sys

    if os.name == "nt":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "AutoPM.ProjectWorkspace"
        )
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except OSError:
            pass
    root = tk.Tk()
    if "--self-test" in sys.argv:
        root.withdraw()
        app = AutoPMApp(root)
        root.update_idletasks()
        import httpx
        import openpyxl
        from . import (
            deepseek,
            workbook,
            airtable,
            sync,
            schema_memory,
            schema_advisor,
            schema_ui,
            workflow,
            tracker,
            native_xlsx,
            network,
        )
        from inspect import signature

        network_defaults = signature(airtable.AirtableClient).parameters
        destination = ROOT / ".local"
        destination.mkdir(parents=True, exist_ok=True)
        checks = {
            "started": True,
            "tabs": len(app.notebook.tabs()),
            "apply_disabled": str(app.apply_button["state"]) == "disabled",
            "local_preview_disabled": str(app.local_preview_button["state"])
            == "disabled",
            "schema_memory_modules": True,
            "tracker_export_disabled": str(app.tracker_page.export_button["state"])
            == "disabled",
            "airtable_tracker": {
                "source_selector": hasattr(app.tracker_page, "source_kind"),
                "read_preview": callable(
                    getattr(app.tracker_page, "preview_airtable", None)
                ),
                "sync_followup_entry": app.tracker_followup_button.winfo_exists() == 1,
                "sync_followup_option": app.auto_tracker_check.winfo_exists() == 1,
                "workflow_available": callable(
                    getattr(workflow, "prepare_airtable_tracker", None)
                ),
                "copy_as_next_input": app.tracker_page.reuse_button.winfo_exists() == 1,
            },
            "network": {
                "report_entry": app.network_button.winfo_exists() == 1,
                "failure_report_entry": app.notice_report_button.winfo_exists() == 1,
                "diagnosis_available": bool(
                    network.diagnose_network_error(TimeoutError()).code
                ),
                "max_attempts": network_defaults["max_retries"].default + 1,
                "timeout_seconds": network_defaults["timeout"].default,
                "history_limit": app._network_events.maxlen,
            },
            "dependencies": {
                "openpyxl": openpyxl.__version__,
                "httpx": httpx.__version__,
            },
        }
        from .design import FONT_LOADED, FONT_PATH
        from tkinter import font as tkfont

        actual_font = tkfont.Font(
            root=root, family=FONT, weight="normal", slant="roman"
        ).actual()
        actual_family = actual_font["family"]
        checks["font"] = {
            "family": FONT,
            "actual_family": actual_family,
            "private_loaded": FONT_LOADED,
            "available": actual_family in tkfont.families(root),
            "bundled": FONT_PATH.is_file(),
            "weight": actual_font["weight"],
            "slant": actual_font["slant"],
            "license_bundled": (FONT_PATH.parent / "OFL.txt").is_file(),
        }
        from PIL import __version__ as pillow_version

        checks["glass"] = {
            "renderer": "application-backdrop-alpha-composite",
            "pillow": pillow_version,
            "animated_buttons": isinstance(app.ai_button, GlassButton),
            "motion_toggle": hasattr(app, "motion_button"),
        }
        checks["brand"] = {
            "title": root.title(),
            "window_icons": len(root._brand_icons),
            "packaged_ico": (ASSET_ROOT / "autopm.ico").is_file(),
            "caption_attributes": root._caption_attributes,
        }
        if "--schema-check" in sys.argv:
            source = Path(sys.argv[sys.argv.index("--schema-check") + 1])
            evidence = json.loads(source.read_text(encoding="utf-8"))
            state = schema_memory.reconcile(evidence["schema"], {**DEFAULTS, "base_id": evidence["base_id"]})
            checks["fresh_profile"] = {
                "blockers": state["blockers"], "warnings": state["warnings"],
                "field_mapping": state["config"]["field_mapping"],
                "project_report_storage": state["config"].get("project_report_storage"),
            }
        if "--network-check" in sys.argv:
            # Explicit packaged diagnostic: no credentials or business data sent.
            import urllib.request
            import urllib.error
            opener = airtable._HttpxOpener(timeout=15)
            try:
                response = opener(urllib.request.Request("https://api.airtable.com/v0/meta/bases"), 15)
                response.close()
                checks["network_probe"] = {"tls_verified": True, "http_status": 200}
            except urllib.error.HTTPError as exc:
                checks["network_probe"] = {"tls_verified": True, "http_status": exc.code}
            except Exception as exc:
                diagnosis = getattr(exc, "diagnosis", None) or network.diagnose_network_error(exc)
                checks["network_probe"] = {"tls_verified": False, "diagnosis": diagnosis.as_dict()}
            finally:
                opener.close()
        if "--report" in sys.argv:
            source = sys.argv[sys.argv.index("--report") + 1]
            parsed = workbook.parse_local(workbook.read_workbook(source))
            checks["offline_projects"] = len(parsed["projects"])
        (destination / "boot_check.json").write_text(
            json.dumps(checks, indent=2), encoding="utf-8"
        )
        root.destroy()
        return
    AutoPMApp(root)
    root.mainloop()
