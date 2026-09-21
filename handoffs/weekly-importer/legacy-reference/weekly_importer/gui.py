"""AutoPM workbench GUI for weekly report importing.

A tkinter implementation inspired by the AutoPM project sync workbench:
left navigation, step indicator, status badges and a local status bar.
The user only needs to provide the Airtable token in the connection
settings page; base and table IDs are auto-detected or defaulted.
"""

from __future__ import annotations

import json
import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

import openpyxl

# Make the package importable both from source and frozen builds
if getattr(sys, "frozen", False):
    _CONFIG_DIR = Path(sys.executable).parent
    sys.path.insert(0, str(_CONFIG_DIR))
else:
    _CONFIG_DIR = Path(__file__).parent.parent

from weekly_importer import (
    AirtableClient,
    RemarkCleaner,
    WeeklyImporter,
    AllTrackerExporter,
    LedgerSync,
)

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
COLOR_BG = "#FFFFFF"
COLOR_SIDEBAR = "#F5F7FA"
COLOR_PRIMARY = "#2563EB"
COLOR_PRIMARY_LIGHT = "#EFF4FF"
COLOR_PRIMARY_DARK = "#1E40AF"
COLOR_TEXT = "#1F2937"
COLOR_MUTED = "#6B7280"
COLOR_BORDER = "#E5E7EB"
COLOR_LOGO_BG = "#0F172A"
COLOR_OK = "#10B981"
COLOR_WARN = "#F59E0B"

FONT_UI = "Microsoft YaHei UI"
FONT_BOLD = "Microsoft YaHei UI"

DEFAULT_BASE_ID = "appOMWiK4CTOH7iQu"
DEFAULT_BASE_NAME = "AutoPM V2（Pilot）"
DEFAULT_TABLE_ID = "tbllvOHZdwfBRWGM0"
DEFAULT_TABLE_NAME = "Projects"
REMARK_FIELD = "Engineering remark(Manual)"
PROJECT_NAME_FIELD = "Project name (Manual)"
DEFAULT_EXCEL_DIR = r"D:\个人资料\AI学习圈\SN Auto PM\05-真实项目数据 Real data\Weekly report\AutoPM_Source_20260915"
CONFIG_FILE = "auto_connection.json"


def _config_path() -> Path:
    return _CONFIG_DIR / CONFIG_FILE


def _load_connection() -> dict:
    path = _config_path()
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_connection(cfg: dict) -> None:
    """Persist non-secret connection settings only. Token never touches disk."""
    safe = {
        "base_id": cfg.get("base_id", ""),
        "base_name": cfg.get("base_name", ""),
        "table_id": cfg.get("table_id", ""),
        "table_name": cfg.get("table_name", ""),
    }
    _config_path().write_text(
        json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _resolve_sheet(path: str) -> str:
    """Pick the best worksheet for weekly import."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        names = wb.sheetnames
    finally:
        wb.close()
    for cand in ("ALL PROJECTS", "All Projects", "ALL"):
        if cand in names:
            return cand
    for name in names:
        if "project" in name.lower():
            return name
    return names[0] if names else "ALL PROJECTS"


def _detect_columns(path: str, sheet_name: str) -> dict:
    """Locate project-name / progress / date columns in the header row."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        ws = wb[sheet_name]
        header = {}
        for row in ws.iter_rows(min_row=2, max_row=2, values_only=True):
            for idx, value in enumerate(row, start=1):
                if value:
                    header[idx] = str(value).strip()
    finally:
        wb.close()

    name_key = progress_key = date_key = None
    for key in header.values():
        low = key.lower()
        if "project name" in low and name_key is None:
            name_key = key
        elif "engineering remark" in low and progress_key is None:
            progress_key = key
        elif "date" in low and "added" in low and date_key is None:
            date_key = key

    return {
        "project_name_column": name_key or "Project Name , Description",
        "progress_column": progress_key or "Engineering Remarks",
        "date_column": date_key or "Date Added",
    }


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------
class AutoPMWorkbench:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("AutoPM · 项目同步工作台")
        root.geometry("1120x720")
        root.minsize(960, 620)
        root.configure(bg=COLOR_BG)

        self.conn = _load_connection()
        self.conn.setdefault("base_id", DEFAULT_BASE_ID)
        self.conn.setdefault("base_name", DEFAULT_BASE_NAME)
        self.conn.setdefault("table_id", DEFAULT_TABLE_ID)
        self.conn.setdefault("table_name", DEFAULT_TABLE_NAME)
        self.token = ""  # in-memory only, never persisted

        self.pages: dict[str, tk.Frame] = {}
        self.nav_buttons: dict[str, tk.Button] = {}
        self.status_badge: tk.Label | None = None

        self._build_shell()
        self._build_pages()
        self._show_page("import")

    # ---- shell -----------------------------------------------------------
    def _build_shell(self) -> None:
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Left sidebar
        sidebar = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=210)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        logo = tk.Frame(sidebar, bg=COLOR_LOGO_BG)
        logo.pack(fill="x")
        tk.Label(
            logo,
            text="AP",
            bg=COLOR_PRIMARY,
            fg="white",
            font=(FONT_BOLD, 13, "bold"),
            padx=8,
            pady=4,
        ).pack(side="left", padx=14, pady=12)
        logo_text = tk.Frame(logo, bg=COLOR_LOGO_BG)
        logo_text.pack(side="left")
        tk.Label(
            logo_text,
            text="AutoPM",
            bg=COLOR_LOGO_BG,
            fg="white",
            font=(FONT_BOLD, 12, "bold"),
        ).pack(anchor="w")
        tk.Label(
            logo_text,
            text="周报与项目同步",
            bg=COLOR_LOGO_BG,
            fg="#94A3B8",
            font=(FONT_UI, 8),
        ).pack(anchor="w")

        tk.Label(
            sidebar,
            text="工作空间",
            bg=COLOR_SIDEBAR,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(anchor="w", padx=16, pady=(16, 6))

        nav_items = [
            ("import", "周报导入", "📥"),
            ("files", "本地文件", "📁"),
            ("settings", "连接设置", "🔗"),
            ("ledger", "本地总表", "📊"),
        ]
        for key, label, icon in nav_items:
            btn = tk.Button(
                sidebar,
                text=f"  {icon}  {label}",
                anchor="w",
                relief="flat",
                bd=0,
                bg=COLOR_SIDEBAR,
                fg=COLOR_TEXT,
                activebackground=COLOR_PRIMARY_LIGHT,
                activeforeground=COLOR_PRIMARY,
                font=(FONT_UI, 10),
                padx=12,
                pady=8,
                cursor="hand2",
                command=lambda k=key: self._show_page(k),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[key] = btn

        tk.Label(
            sidebar,
            text="本地文件 · 云端同步",
            bg=COLOR_SIDEBAR,
            fg=COLOR_MUTED,
            font=(FONT_UI, 8),
        ).pack(side="bottom", pady=8)
        tk.Label(
            sidebar,
            text="每一处变更，确认后写入",
            bg=COLOR_SIDEBAR,
            fg=COLOR_MUTED,
            font=(FONT_UI, 8),
        ).pack(side="bottom")

        # Right content area
        self.content = tk.Frame(self.root, bg=COLOR_BG)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)

    def _header(self, parent: tk.Widget, page_title: str, subtitle: str) -> None:
        top = tk.Frame(parent, bg=COLOR_BG)
        top.pack(fill="x", padx=28, pady=(18, 4))
        tk.Label(
            top,
            text=f"AutoPM / {page_title}",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(side="left")
        badges = tk.Frame(top, bg=COLOR_BG)
        badges.pack(side="right")
        for text, fg in (
            ("动效 · 开", COLOR_PRIMARY),
            ("网络报告", COLOR_PRIMARY),
        ):
            tk.Label(
                badges,
                text=text,
                bg=COLOR_PRIMARY_LIGHT,
                fg=fg,
                font=(FONT_UI, 9),
                padx=8,
                pady=3,
            ).pack(side="left", padx=4)
        self.status_badge = tk.Label(
            badges,
            text=self._badge_text(),
            bg=COLOR_PRIMARY_LIGHT if self.token else "#FEF3C7",
            fg=COLOR_PRIMARY if self.token else COLOR_WARN,
            font=(FONT_UI, 9),
            padx=8,
            pady=3,
        )
        self.status_badge.pack(side="left", padx=4)

        tk.Label(
            parent,
            text=page_title,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=(FONT_BOLD, 16, "bold"),
        ).pack(anchor="w", padx=28, pady=(8, 0))
        tk.Label(
            parent,
            text=subtitle,
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 10),
        ).pack(anchor="w", padx=28, pady=(2, 10))

    def _badge_text(self) -> str:
        if self.token and self.conn.get("base_id"):
            return "Airtable · 已连接"
        if self.token:
            return "Airtable · 已填写，待检测"
        return "Airtable · 待配置"

    def _refresh_badge(self) -> None:
        if self.status_badge is None:
            return
        connected = bool(self.token and self.conn.get("base_id"))
        self.status_badge.configure(
            text=self._badge_text(),
            bg=COLOR_PRIMARY_LIGHT if connected else "#FEF3C7",
            fg=COLOR_PRIMARY if connected else COLOR_WARN,
        )

    def _switch_nav(self, active_key: str) -> None:
        for key, btn in self.nav_buttons.items():
            btn.configure(
                bg=COLOR_PRIMARY_LIGHT if key == active_key else COLOR_SIDEBAR,
                fg=COLOR_PRIMARY if key == active_key else COLOR_TEXT,
            )

    def _show_page(self, key: str) -> None:
        for page in self.pages.values():
            page.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        self._switch_nav(key)

    def use_excel(self, path: str) -> None:
        """Switch to the import page and load an Excel file into it."""
        import_page = self.pages["import"]
        if hasattr(import_page, "_set_excel"):
            import_page._set_excel(path)  # type: ignore[attr-defined]
        self._show_page("import")

    # ---- pages -----------------------------------------------------------
    def _build_pages(self) -> None:
        self.pages["import"] = ImportPage(self)
        self.pages["files"] = FilesPage(self)
        self.pages["settings"] = SettingsPage(self)
        self.pages["ledger"] = LedgerPage(self)


# ---------------------------------------------------------------------------
# Shared widgets
# ---------------------------------------------------------------------------
class Card(tk.Frame):
    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(
            parent,
            bg=COLOR_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            **kwargs,
        )


class StepIndicator(tk.Frame):
    def __init__(self, parent: tk.Widget, steps: list[str], current: int = 0) -> None:
        super().__init__(parent, bg=COLOR_BG)
        for idx, label in enumerate(steps):
            active = idx == current
            done = idx < current
            color = COLOR_PRIMARY if active else (COLOR_OK if done else COLOR_MUTED)
            bg = COLOR_PRIMARY_LIGHT if active else "#F3F4F6"
            tk.Label(
                self,
                text=f"0{idx + 1}",
                bg=bg,
                fg=color,
                font=(FONT_BOLD, 9, "bold"),
                padx=7,
                pady=2,
            ).pack(side="left", padx=(0, 6))
            tk.Label(
                self,
                text=label,
                bg=COLOR_BG,
                fg=color,
                font=(FONT_UI, 9, "bold" if active else "normal"),
            ).pack(side="left", padx=(0, 12))


class LogPanel(scrolledtext.ScrolledText):
    def __init__(self, parent: tk.Widget, height: int = 12) -> None:
        super().__init__(
            parent,
            height=height,
            wrap="word",
            state="disabled",
            bg="#F9FAFB",
            fg=COLOR_TEXT,
            relief="flat",
            font=("Consolas", 9),
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )

    def clear(self) -> None:
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")

    def write(self, text: str) -> None:
        self.configure(state="normal")
        self.insert("end", text + "\n")
        self.see("end")
        self.configure(state="disabled")


# ---------------------------------------------------------------------------
# Import page
# ---------------------------------------------------------------------------
class ImportPage(tk.Frame):
    def __init__(self, app: AutoPMWorkbench) -> None:
        super().__init__(app.content, bg=COLOR_BG)
        self.app = app
        self.excel_path = tk.StringVar()
        self.sheet_name = tk.StringVar(value="ALL PROJECTS")
        self.cols: dict = {}

        app._header(self, "周报导入", "选择周报，核对变更后同步到 Airtable。")

        steps = tk.Frame(self, bg=COLOR_BG)
        steps.pack(fill="x", padx=28)
        StepIndicator(
            steps, ["选择周报", "核对变更", "写入 Airtable", "本地总表"], current=0
        ).pack(side="left")
        ttk.Button(steps, text="选择文件", command=self._browse).pack(side="right")

        card = Card(self)
        card.pack(fill="x", padx=28, pady=(18, 12))
        row = tk.Frame(card, bg=COLOR_BG)
        row.pack(fill="x", padx=16, pady=12)
        tk.Label(
            row,
            text="选择一份 Excel 周报",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=(FONT_BOLD, 11, "bold"),
        ).pack(side="left")
        tk.Label(
            row,
            text="支持 .xlsx · 自动识别项目、任务与问题",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(side="left", padx=10)

        entry_row = tk.Frame(card, bg=COLOR_BG)
        entry_row.pack(fill="x", padx=16, pady=(0, 14))
        tk.Entry(
            entry_row,
            textvariable=self.excel_path,
            font=(FONT_UI, 10),
            relief="flat",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        ).pack(side="left", fill="x", expand=True, ipady=4)

        actions = ttk.Frame(self)
        actions.pack(fill="x", padx=28)
        ttk.Button(actions, text="规则检查 · 预览变更", command=self._preview).pack(
            side="left"
        )
        ttk.Button(actions, text="写入 Airtable", command=self._import).pack(
            side="left", padx=10
        )
        ttk.Button(actions, text="清理旧格式备注", command=self._clean).pack(
            side="left"
        )

        tk.Label(
            self,
            text="运行日志",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(anchor="w", padx=28, pady=(14, 6))
        self.log = LogPanel(self, height=14)
        self.log.pack(fill="both", expand=True, padx=28, pady=(0, 18))

        # footer status
        self.footer = tk.Label(
            self,
            text="就绪 · 选择一份周报开始",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        )
        self.footer.pack(side="bottom", anchor="w", padx=28, pady=10)

    def _browse(self) -> None:
        initial = self.excel_path.get().strip() or DEFAULT_EXCEL_DIR
        path = filedialog.askopenfilename(
            title="选择 Excel 周报",
            initialdir=os.path.dirname(initial) if os.path.isfile(initial) else initial,
            filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")],
        )
        if path:
            self._set_excel(path)

    def _set_excel(self, path: str) -> None:
        self.excel_path.set(path)
        try:
            self.sheet_name.set(_resolve_sheet(path))
            self.cols = _detect_columns(path, self.sheet_name.get())
            self.log.write(
                f"已选择: {path}\n工作表: {self.sheet_name.get()}\n"
                f"列映射: 项目={self.cols['project_name_column']} | "
                f"进度={self.cols['progress_column']} | 日期={self.cols['date_column']}"
            )
        except Exception as exc:
            self.log.write(f"解析工作表失败: {exc}")

    def _check_ready(self) -> bool:
        if not self.app.token:
            messagebox.showwarning(
                "需要连接", "请先在「连接设置」中粘贴 Airtable Token 并完成检测。"
            )
            return False
        if not self.excel_path.get().strip():
            messagebox.showwarning("需要周报", "请先选择一份 Excel 周报。")
            return False
        return True

    def _preview(self) -> None:
        if not self._check_ready():
            return
        self._run(dry_run=True)

    def _import(self) -> None:
        if not self._check_ready():
            return
        if not messagebox.askokcancel(
            "确认写入",
            "将把周报进度合并写入 Airtable Engineering remark 字段。\n确认执行吗？",
        ):
            return
        self._run(dry_run=False)

    def _clean(self) -> None:
        if not self.app.token:
            messagebox.showwarning("需要连接", "请先完成 Airtable 连接设置。")
            return
        if not messagebox.askokcancel(
            "确认清理", "将清理 Airtable 中旧的 AutoPM 周报格式备注。\n确认执行吗？"
        ):
            return
        self._run(clean=True)

    def _run(self, dry_run: bool = False, clean: bool = False) -> None:
        self.footer.configure(text="运行中…", fg=COLOR_PRIMARY)
        self.log.clear()
        self.log.write("开始处理，请稍候…")
        token = self.app.token
        base_id = self.app.conn["base_id"]
        table_id = self.app.conn["table_id"]
        excel = self.excel_path.get().strip()
        sheet = self.sheet_name.get()
        cols = dict(self.cols)

        threading.Thread(
            target=self._worker,
            args=(token, base_id, table_id, excel, sheet, cols, dry_run, clean),
            daemon=True,
        ).start()

    def _worker(
        self, token, base_id, table_id, excel, sheet, cols, dry_run, clean
    ) -> None:
        try:
            client = AirtableClient(
                api_token=token,
                base_id=base_id,
                request_timeout=30,
                max_retries=3,
                retry_delay=1.0,
            )
            if clean:
                cleaner = RemarkCleaner(
                    client=client,
                    table_id=table_id,
                    field_name=REMARK_FIELD,
                    batch_size=10,
                )
                stats = cleaner.clean_all()
                lines = [
                    "清理完成：",
                    f"  总记录: {stats['total']}",
                    f"  已清理: {stats['cleaned']}",
                    f"  跳过: {stats['skipped']}",
                    f"  错误: {stats['errors']}",
                ]
                self._post(
                    "".join(line + "\n" for line in lines), ok=stats["errors"] == 0
                )
                return

            importer = WeeklyImporter(
                client=client,
                projects_table_id=table_id,
                remark_field=REMARK_FIELD,
                project_name_field=PROJECT_NAME_FIELD,
                batch_size=10,
            )
            result = importer.import_from_excel(
                excel_path=excel,
                sheet_name=sheet,
                date_column=cols.get("date_column", "Date Added"),
                progress_column=cols.get("progress_column", "Engineering Remarks"),
                project_name_column=cols.get(
                    "project_name_column", "Project Name , Description"
                ),
                dry_run=dry_run,
            )
            mode = "预览（未写入）" if dry_run else "已写入"
            lines = [
                f"导入完成 [{mode}]:",
                f"  状态: {result['status']}",
                f"  Excel 行数: {result['total']}",
                f"  匹配并应用: {result['applied']}",
                f"  跳过: {result['skipped']}",
                f"  未匹配/失败: {result['failed']}",
            ]
            if dry_run and "preview_count" in result:
                lines.append(f"  待写入记录: {result['preview_count']}")
            ok = not dry_run or result["failed"] == 0
            self._post("".join(line + "\n" for line in lines), ok=ok)
        except Exception as exc:
            import traceback

            self._post(f"错误: {exc}\n{traceback.format_exc()}", ok=False)

    def _post(self, text: str, ok: bool) -> None:
        def apply() -> None:
            self.log.write(text)
            self.footer.configure(
                text="LOCAL · READY" if ok else "执行失败，请查看日志",
                fg=COLOR_OK if ok else "#DC2626",
            )
            self.app._refresh_badge()

        self.app.root.after(0, apply)


# ---------------------------------------------------------------------------
# Files page
# ---------------------------------------------------------------------------
class FilesPage(tk.Frame):
    def __init__(self, app: AutoPMWorkbench) -> None:
        super().__init__(app.content, bg=COLOR_BG)
        self.app = app
        app._header(self, "本地文件", "扫描默认目录中的 Excel 周报，双击使用。")

        card = Card(self)
        card.pack(fill="both", expand=True, padx=28, pady=(8, 14))

        row = tk.Frame(card, bg=COLOR_BG)
        row.pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(
            row,
            text="扫描目录",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(side="left")
        tk.Label(
            row,
            text=DEFAULT_EXCEL_DIR,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=(FONT_UI, 9),
        ).pack(side="left", padx=8)
        ttk.Button(row, text="刷新", command=self._refresh).pack(side="right")
        ttk.Button(row, text="打开目录", command=self._open_dir).pack(
            side="right", padx=6
        )

        cols = ("file", "size", "mtime")
        self.tree = ttk.Treeview(card, columns=cols, show="headings", height=14)
        self.tree.heading("file", text="文件")
        self.tree.heading("size", text="大小")
        self.tree.heading("mtime", text="修改时间")
        self.tree.column("file", width=520)
        self.tree.column("size", width=90, anchor="e")
        self.tree.column("mtime", width=160)
        self.tree.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.tree.bind("<Double-1>", self._use_selected)

        tk.Label(
            card,
            text="双击文件可在「周报导入」页直接使用",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 8),
        ).pack(anchor="w", padx=14, pady=(0, 10))
        self._refresh()

    def _collect(self) -> list[tuple[Path, int, float]]:
        base = Path(DEFAULT_EXCEL_DIR)
        roots: list[Path] = []
        if base.exists():
            roots.append(base)
        # 真实周报常驻于父目录的数据子目录
        for name in ("Data", "weekly report data test"):
            candidate = base.parent / name
            if candidate.exists():
                roots.append(candidate)

        found: list[tuple[Path, int, float]] = []
        for root in roots:
            for path in root.rglob("*.xlsx"):
                if path.name.startswith("~$"):
                    continue
                try:
                    stat = path.stat()
                    found.append((path, stat.st_size, stat.st_mtime))
                except OSError:
                    continue
        found.sort(key=lambda item: item[2], reverse=True)
        return found

    def _refresh(self) -> None:
        from datetime import datetime

        for item in self.tree.get_children():
            self.tree.delete(item)
        for path, size, mtime in self._collect():
            self.tree.insert(
                "",
                "end",
                values=(
                    str(path),
                    f"{size / 1024:.0f} KB",
                    datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M"),
                ),
            )

    def _use_selected(self, _event=None) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        path = self.tree.item(sel[0], "values")[0]
        self.app.use_excel(path)

    def _open_dir(self) -> None:
        os.startfile(DEFAULT_EXCEL_DIR)  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Settings page
# ---------------------------------------------------------------------------
class SettingsPage(tk.Frame):
    def __init__(self, app: AutoPMWorkbench) -> None:
        super().__init__(app.content, bg=COLOR_BG)
        self.app = app
        self.token_var = tk.StringVar(value="")
        self.base_var = tk.StringVar(value="")
        self.table_info_label: tk.Label | None = None
        self.advanced_visible = False

        app._header(self, "连接设置", "保存一次，之后直接选择周报开始。")

        # Airtable card
        card = Card(self)
        card.pack(fill="x", padx=28, pady=(8, 10))
        tk.Label(
            card,
            text="Airtable 数据",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=(FONT_BOLD, 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 4))

        tk.Label(
            card,
            text="完整 Token (Token Key)",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(anchor="w", padx=16, pady=(6, 2))
        entry_row = tk.Frame(card, bg=COLOR_BG)
        entry_row.pack(fill="x", padx=16)
        tk.Entry(
            entry_row,
            textvariable=self.token_var,
            show="*",
            font=(FONT_UI, 10),
            relief="flat",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        ).pack(side="left", fill="x", expand=True, ipady=4)
        ttk.Button(entry_row, text="检测并选择数据库", command=self._detect).pack(
            side="left", padx=(10, 0)
        )

        tk.Label(
            card,
            text="粘贴创建时显示的完整密钥。Token 仅保存在本次会话内存中，不写入磁盘。",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 8),
        ).pack(anchor="w", padx=16, pady=(6, 4))

        tk.Label(
            card,
            text="目标数据库",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(anchor="w", padx=16, pady=(4, 2))
        self.base_combo = ttk.Combobox(
            card,
            textvariable=self.base_var,
            state="readonly",
            values=[self.app.conn.get("base_name", "") or DEFAULT_BASE_NAME],
        )
        self.base_combo.pack(fill="x", padx=16)
        self.base_combo.bind("<<ComboboxSelected>>", self._on_base_selected)

        self.table_info_label = tk.Label(
            card,
            text="",
            bg=COLOR_BG,
            fg=COLOR_OK,
            font=(FONT_UI, 9),
        )
        self.table_info_label.pack(anchor="w", padx=16, pady=(8, 4))

        advanced_btn = tk.Label(
            card,
            text="高级设置：数据库和表 ID  ＋",
            bg=COLOR_BG,
            fg=COLOR_PRIMARY,
            font=(FONT_UI, 9),
            cursor="hand2",
        )
        advanced_btn.pack(anchor="w", padx=16, pady=(2, 6))
        advanced_btn.bind("<Button-1>", self._toggle_advanced)

        self.advanced = tk.Frame(card, bg=COLOR_BG)
        self.advanced.pack(fill="x", padx=16, pady=(0, 12))
        self._build_advanced()

        # Local parsing note
        note = Card(self)
        note.pack(fill="x", padx=28)
        tk.Label(
            note,
            text="本地解析（无需 AI Key）",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=(FONT_BOLD, 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(12, 2))
        tk.Label(
            note,
            text="当前版本使用离线规则解析 Report 工作表，不依赖 DeepSeek 等外部 AI 服务。",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 12))

    def _build_advanced(self) -> None:
        rows = [
            ("Base ID", "base_id"),
            ("Projects 表 ID", "table_id"),
            ("Association 表", "localhost"),
        ]
        for idx, (label, key) in enumerate(rows):
            tk.Label(
                self.advanced,
                text=label,
                bg=COLOR_BG,
                fg=COLOR_MUTED,
                font=(FONT_UI, 9),
            ).grid(row=idx, column=0, sticky="w", padx=6, pady=3)
            tk.Label(
                self.advanced,
                text=self.app.conn.get(key, ""),
                bg=COLOR_BG,
                fg=COLOR_TEXT,
                font=("Consolas", 9),
            ).grid(row=idx, column=1, sticky="w", padx=6, pady=3)

    def _toggle_advanced(self, _event=None) -> None:
        self.advanced_visible = not self.advanced_visible
        if self.advanced_visible:
            self.advanced.pack(fill="x", padx=16, pady=(0, 12))
        else:
            self.advanced.pack_forget()

    def _token(self) -> str:
        return self.token_var.get().strip()

    def _detect(self) -> None:
        token = self._token()
        if not token:
            messagebox.showwarning("缺少 Token", "请先粘贴 Airtable 完整 Token。")
            return
        self.app.token = token
        self.app._refresh_badge()
        self._status("正在检测…", COLOR_WARN)
        threading.Thread(target=self._detect_worker, args=(token,), daemon=True).start()

    def _detect_worker(self, token: str) -> None:
        try:
            client = AirtableClient(
                api_token=token,
                base_id="",
                request_timeout=20,
                max_retries=1,
                retry_delay=0.5,
            )
            bases = client.list_bases()
            if not bases:
                self._post_detect("该 Token 未关联任何数据库。", ok=False)
                return
            names = [b.get("name", "") for b in bases]
            ids = {b.get("name", ""): b.get("id", "") for b in bases}

            def apply() -> None:
                self.base_combo.configure(values=names)
                preferred = next(
                    (n for n in names if "autopm" in (n or "").lower()),
                    names[0],
                )
                self.base_var.set(preferred)
                # Default to known production base if present
                if DEFAULT_BASE_ID in ids.values():
                    for n, bid in ids.items():
                        if bid == DEFAULT_BASE_ID:
                            self.base_var.set(n)
                            break
                self._on_base_selected()

            self.app.root.after(0, apply)
        except Exception as exc:
            self._post_detect(f"检测失败: {exc}", ok=False)

    def _post_detect(self, text: str, ok: bool) -> None:
        def apply() -> None:
            if self.table_info_label is not None:
                self.table_info_label.configure(
                    text=text, fg=COLOR_OK if ok else "#DC2626"
                )
            self.app._refresh_badge()

        self.app.root.after(0, apply)

    def _status(self, text: str, color: str) -> None:
        if self.table_info_label is not None:
            self.table_info_label.configure(text=text, fg=color)

    def _on_base_selected(self, _event=None) -> None:
        name = self.base_var.get()
        if not name:
            return
        token = self.app.token
        base_id = (
            self.app.conn.get("base_id", DEFAULT_BASE_ID)
            if name == self.app.conn.get("base_name", DEFAULT_BASE_NAME)
            else None
        )
        threading.Thread(
            target=self._table_worker, args=(token, name, base_id), daemon=True
        ).start()

    def _table_worker(self, token: str, name: str, base_id: str | None) -> None:
        try:
            if not base_id:
                client = AirtableClient(
                    api_token=token,
                    base_id="",
                    request_timeout=20,
                    max_retries=1,
                    retry_delay=0.5,
                )
                bases = client.list_bases()
                for base in bases:
                    if base.get("name", "") == name:
                        base_id = base.get("id", "")
                        break
            if not base_id:
                self._post_detect("未找到对应数据库 ID。", ok=False)
                return

            client = AirtableClient(
                api_token=token,
                base_id=base_id,
                request_timeout=20,
                max_retries=1,
                retry_delay=0.5,
            )
            meta = client.get_table_meta()
            tables = meta.get("tables", [])
            table_id = ""
            table_name = ""
            preferred = next(
                (
                    t
                    for t in tables
                    if (t.get("name") or "").strip().lower() == "projects"
                ),
                None,
            )
            if preferred is None:
                preferred = next(
                    (t for t in tables if "project" in (t.get("name") or "").lower()),
                    None,
                )
            if preferred:
                table_id = preferred.get("id", "")
                table_name = preferred.get("name", "")
            elif tables:
                table_id = tables[0].get("id", "")
                table_name = tables[0].get("name", "")

            self.app.conn["base_id"] = base_id
            self.app.conn["base_name"] = name
            self.app.conn["table_id"] = table_id or DEFAULT_TABLE_ID
            self.app.conn["table_name"] = table_name or "Projects"
            _save_connection(self.app.conn)

            def apply() -> None:
                if self.table_info_label is not None:
                    self.table_info_label.configure(
                        text=f"已连接：{name} → {self.app.conn['table_name']} 表",
                        fg=COLOR_OK,
                    )
                self.app._refresh_badge()

            self.app.root.after(0, apply)
        except Exception as exc:
            self._post_detect(f"读取数据表失败: {exc}", ok=False)


# ---------------------------------------------------------------------------
# Ledger page
# ---------------------------------------------------------------------------
class LedgerPage(tk.Frame):
    def __init__(self, app: AutoPMWorkbench) -> None:
        super().__init__(app.content, bg=COLOR_BG)
        self.app = app
        self.export_path = tk.StringVar()
        self.sync_path = tk.StringVar()

        app._header(
            self,
            "本地总表",
            "Airtable 与本地 Excel 的双向同步：导出主表、编辑后回写。",
        )

        # ---- Export card ----
        card1 = Card(self)
        card1.pack(fill="x", padx=28, pady=(8, 8))
        tk.Label(
            card1,
            text="① 从 Airtable 导出 All Tracker",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=(FONT_BOLD, 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Label(
            card1,
            text="把当前 Airtable 全部项目导出为本地 Excel，作为可编辑主表。\n"
            "导出的 Excel 第 100 列隐藏了 record_id，供回写时自动匹配。",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 8))

        export_row = tk.Frame(card1, bg=COLOR_BG)
        export_row.pack(fill="x", padx=16, pady=(0, 12))
        tk.Entry(
            export_row,
            textvariable=self.export_path,
            font=(FONT_UI, 10),
            relief="flat",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        ).pack(side="left", fill="x", expand=True, ipady=4)
        ttk.Button(
            export_row,
            text="选择保存位置…",
            command=self._browse_export,
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            export_row,
            text="导出",
            command=self._export,
        ).pack(side="left", padx=(6, 0))

        # ---- Sync-back card ----
        card2 = Card(self)
        card2.pack(fill="x", padx=28, pady=(8, 8))
        tk.Label(
            card2,
            text="② 本地编辑后回写 Airtable",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=(FONT_BOLD, 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Label(
            card2,
            text="选择已导出的 All Tracker Excel（须保留第 100 列的 record_id），\n"
            "程序自动比对 Airtable 当前值，只推送你修改过的字段。\n"
            "注意：Engineering remark(Manual) 属于周报导入链路，回写时不会覆盖。",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 8))

        sync_row = tk.Frame(card2, bg=COLOR_BG)
        sync_row.pack(fill="x", padx=16, pady=(0, 12))
        tk.Entry(
            sync_row,
            textvariable=self.sync_path,
            font=(FONT_UI, 10),
            relief="flat",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        ).pack(side="left", fill="x", expand=True, ipady=4)
        ttk.Button(
            sync_row,
            text="选择本地 Excel…",
            command=self._browse_sync,
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            sync_row,
            text="预览变更",
            command=lambda: self._sync(dry_run=True),
        ).pack(side="left", padx=(6, 0))
        ttk.Button(
            sync_row,
            text="确认回写",
            command=lambda: self._sync(dry_run=False),
        ).pack(side="left", padx=(6, 0))

        # ---- Log area ----
        tk.Label(
            self,
            text="运行日志",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        ).pack(anchor="w", padx=28, pady=(14, 6))
        self.log = LogPanel(self, height=12)
        self.log.pack(fill="both", expand=True, padx=28, pady=(0, 18))

        self.footer = tk.Label(
            self,
            text="就绪 · 导出或选择本地 Excel 回写",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=(FONT_UI, 9),
        )
        self.footer.pack(side="bottom", anchor="w", padx=28, pady=10)

    def _browse_export(self) -> None:
        path = filedialog.asksaveasfilename(
            title="导出 All Tracker",
            initialdir=DEFAULT_EXCEL_DIR,
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")],
            initialfile="All Tracker_导出_" + _today() + ".xlsx",
        )
        if path:
            self.export_path.set(path)

    def _export(self) -> None:
        if not self.app.token:
            messagebox.showwarning(
                "需要连接", "请先在「连接设置」中配置 Airtable Token。"
            )
            return
        path = self.export_path.get().strip()
        if not path:
            path = filedialog.asksaveasfilename(
                title="导出 All Tracker",
                initialdir=DEFAULT_EXCEL_DIR,
                defaultextension=".xlsx",
                filetypes=[("Excel 文件", "*.xlsx")],
                initialfile="All Tracker_导出_" + _today() + ".xlsx",
            )
            if not path:
                return
            self.export_path.set(path)
        self.footer.configure(text="导出中…", fg=COLOR_PRIMARY)
        threading.Thread(target=self._export_worker, args=(path,), daemon=True).start()

    def _export_worker(self, path: str) -> None:
        try:
            client = AirtableClient(
                api_token=self.app.token,
                base_id=self.app.conn["base_id"],
                request_timeout=30,
                max_retries=3,
                retry_delay=1.0,
            )
            exporter = AllTrackerExporter(
                client=client,
                table_id=self.app.conn["table_id"],
                project_name_field=PROJECT_NAME_FIELD,
                remark_field=REMARK_FIELD,
            )
            result = exporter.export(path)
            lines = [
                f"导出完成：",
                f"  文件: {result['path']}",
                f"  记录数: {result['count']}",
                f"  导出字段: {', '.join(result['fields'])}",
            ]
            self._post("\n".join(lines), ok=True)
        except Exception as exc:
            import traceback

            self._post(f"导出失败:\n{exc}\n{traceback.format_exc()}", ok=False)

    def _browse_sync(self) -> None:
        path = filedialog.askopenfilename(
            title="选择本地 All Tracker Excel",
            initialdir=DEFAULT_EXCEL_DIR,
            filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")],
        )
        if path:
            self.sync_path.set(path)

    def _sync(self, dry_run: bool) -> None:
        if not self.app.token:
            messagebox.showwarning(
                "需要连接", "请先在「连接设置」中配置 Airtable Token。"
            )
            return
        path = self.sync_path.get().strip()
        if not path:
            messagebox.showwarning(
                "需要文件", "请先选择已导出的本地 All Tracker Excel。"
            )
            return
        if not dry_run and not messagebox.askokcancel(
            "确认回写",
            "将把本地 Excel 中修改过的字段回写至 Airtable。\n"
            "Engineering remark(Manual) 不会被覆盖。\n确认执行吗？",
        ):
            return
        self.footer.configure(
            text="回写中…" if not dry_run else "预览中…", fg=COLOR_PRIMARY
        )
        threading.Thread(
            target=self._sync_worker, args=(path, dry_run), daemon=True
        ).start()

    def _sync_worker(self, path: str, dry_run: bool) -> None:
        try:
            client = AirtableClient(
                api_token=self.app.token,
                base_id=self.app.conn["base_id"],
                request_timeout=30,
                max_retries=3,
                retry_delay=1.0,
            )
            sync = LedgerSync(
                client=client,
                table_id=self.app.conn["table_id"],
                project_name_field=PROJECT_NAME_FIELD,
            )
            result = sync.sync_from_excel(path, dry_run=dry_run)
            mode = "预览" if dry_run else "已回写"
            lines = [
                f"回写完成 [{mode}]：",
                f"  状态: {result['status']}",
                f"  总记录: {result['total']}",
                f"  有变更: {result['changed']}",
                f"  无变更: {result['unchanged']}",
                f"  冲突/跳过: {result['conflicts']}",
                f"  错误: {result['errors']}",
            ]
            self._post("\n".join(lines), ok=result["errors"] == 0)
        except Exception as exc:
            import traceback

            self._post(f"回写失败:\n{exc}\n{traceback.format_exc()}", ok=False)

    def _post(self, text: str, ok: bool) -> None:
        def apply() -> None:
            self.log.write(text)
            self.footer.configure(
                text="LOCAL · READY" if ok else "执行失败，请查看日志",
                fg=COLOR_OK if ok else "#DC2626",
            )
            self.app._refresh_badge()

        self.app.root.after(0, apply)


def _today() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y%m%d")


def main() -> None:
    root = tk.Tk()
    AutoPMWorkbench(root)
    root.mainloop()


if __name__ == "__main__":
    main()
