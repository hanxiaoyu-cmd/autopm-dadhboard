"""Exercise the desktop controller with a hidden Tk window and no network.

Workers are run synchronously only when their dependencies are replaced with
test doubles. Settings and local materials are isolated in a temporary folder.
"""
from contextlib import ExitStack
from copy import deepcopy
from pathlib import Path
import tempfile
import time
import tkinter as tk
import unittest
from unittest.mock import ANY, Mock, patch

from autopm import ui


def preview_fixture():
    report = {
        "source": "weekly.xlsx", "report_date": "2026-09-03", "warnings": [],
        "projects": [{
            "project_id": "AB-123", "report_date": "2026-09-03",
            "fields": {"project_name": "Example project", "status": "On Track"},
            "source": "'Report'!D1:U25",
            "tasks": [{"name": "EB1", "date": "2026-09-12", "completed": False,
                       "source": "'Report'!H7", "evidence": ["'Report'!H5", "'Report'!H7"]}],
            "issues": [{"text": "Drawing approval", "action": "Review CAD",
                        "source": "'Report'!B14"}],
        }],
    }
    plan = {
        "plan_id": "test-plan", "base_id": "appTest", "warnings": [], "blockers": [],
        "changes": [
            {"kind": "projects", "project_id": "AB-123", "table_id": "tblProjects",
             "record_id": "recProject", "fields": {"fldName": "Example project", "fldStatus": "On Track"},
             "before": {"fldName": "Old name", "fldStatus": "At Risk"},
             "field_names": {"fldName": "Project Name", "fldStatus": "Status"}, "source": "'Report'!D2"},
            {"kind": "tasks", "project_id": "AB-123", "table_id": "tblTasks", "record_id": "recTask",
             "record_title": "EB1", "fields": {"fldDue": "2026-09-12"}, "before": {"fldDue": "2026-09-19"},
             "field_names": {"fldDue": "Due Date"}, "source": "'Report'!H7"},
            {"kind": "issues", "project_id": "AB-123", "table_id": "tblIssues", "record_id": "recIssue",
             "record_title": "Drawing approval", "fields": {"fldAction": "Review CAD"},
             "before": {"fldAction": "Wait"}, "field_names": {"fldAction": "Recovery Action"},
             "source": "'Report'!B14"},
        ],
    }
    return report, plan


class UIControllerTests(unittest.TestCase):
    def test_token_change_clears_stale_target(self):
        self.app.values["airtable_token"].set("patNew.secret")
        self.assertEqual(self.app.values["base_id"].get(), "")
        self.assertEqual(self.app.values["projects_table_id"].get(), "")
        self.assertIn("重新检测", self.app.base_choice.get())

    def test_connection_result_and_multiple_base_selection(self):
        bases = [{"id": "appOne", "name": "Copy"}, {"id": "appTwo", "name": "Copy"}]
        self.app._airtable_connection_ready({"bases": bases})
        self.assertEqual(self.app.values["base_id"].get(), "")
        with patch.object(self.app, "_discover_airtable") as discover:
            self.app.base_picker.current(1)
            self.app._select_airtable_base()
            discover.assert_called_once_with("appTwo")
        self.app._airtable_connection_ready({"bases": bases, "base": bases[1],
                                            "tables": {k: "tblNew" + k for k in ("projects", "tasks", "issues")}})
        self.assertEqual(self.app.values["base_id"].get(), "appTwo")
        self.assertEqual(self.app.values["tasks_table_id"].get(), "tblNewtasks")
        self.app._refresh_controls()
        self.assertEqual(str(self.app.base_picker["state"]), "readonly")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.source = self.folder / "weekly.xlsx"
        # Controller tests fingerprint bytes; no workbook parsing is performed.
        self.source.write_bytes(b"source version one")
        self.settings = {**ui.DEFAULTS, "deepseek_api_key": "fake-deepseek-key",
                         "airtable_token": "fake-airtable-token", "base_id": "appTest"}
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for target, value in (("ROOT", self.folder), ("load_settings", Mock(return_value=self.settings)),
                              ("scan_local_files", Mock(return_value=[]))):
            self.stack.enter_context(patch.object(ui, target, value))
        self.confirm = self.stack.enter_context(patch.object(ui.messagebox, "askyesno", return_value=False))
        self.file_dialog = self.stack.enter_context(patch.object(ui.filedialog, "askopenfilename", return_value=""))
        # Fail closed if a missing test double ever reaches an HTTP transport.
        self.stack.enter_context(patch("httpx.Client.send", side_effect=AssertionError("UI tests must not use a network")))
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk display unavailable: {exc}")
        self.root.withdraw()
        self.addCleanup(self._destroy_root)
        self.app = ui.AutoPMApp(self.root)

    def _destroy_root(self):
        self.root.update_idletasks()
        for timer in self.root.tk.call("after", "info"):
            # ttk's indeterminate progress timer is a Tcl command list, not a
            # Python callback name accepted by tkinter.after_cancel().
            self.root.tk.call("after", "cancel", timer)
        self.root.destroy()

    def _render(self, plan=None, *, offline=False):
        report, default_plan = preview_fixture()
        self.app.filename.set(str(self.source))
        self.app._render(report, None if offline else (default_plan if plan is None else plan),
                         self.folder / "logs", self.settings, self.app._revision, ui.fingerprint(self.source))
        return report, default_plan

    def _poll(self):
        # Drive one queue drain deterministically without scheduling another.
        with patch.object(self.root, "after"):
            self.app._poll()

    def _new_job(self, job="current"):
        self.app._job_id, self.app.busy = job, True
        self.app._job_credentials = self.app._credential_key()
        self.app._job_started = time.monotonic()
        self.app._refresh_controls()

    def _network_event(self, stage="retry", attempt=1):
        return {"stage": stage, "message": f"Airtable · {stage} · 第 {attempt}/3 次 · 代理连接被拒绝",
                "report": f"操作：读取表结构\n请求：GET api.airtable.com\n第 {attempt}/3 次\n"
                          "具体原因：代理连接被拒绝\n建议：检查代理服务后重新检测。",
                "attempt": attempt, "max_attempts": 3, "timeout": 45, "retry_in": 0.5,
                "operation": "读取表结构", "at": "2026-09-11 18:00:00",
                "diagnosis": {"code": "proxy", "title": "代理连接失败", "detail": "代理连接被拒绝",
                              "advice": "检查代理服务后重新检测。", "retryable": True, "error_type": "ProxyError"}}

    def test_network_retry_failure_and_recovery_are_visible_and_copyable(self):
        self._new_job()
        self.app._show_network_report()
        window = self.app._network_window
        window.withdraw()
        self.assertEqual(str(window.retry_button["state"]), "disabled")
        self.app.events.put(("current", "network", self._network_event()))
        self._poll()
        self.assertTrue(self.app.busy)
        self.assertIn("第 1/3 次", self.app.status.get())
        self.assertIn("正在重试", self.app.connection["text"])
        self.assertEqual(self.app.notice_report_button.winfo_manager(), "pack")
        self.assertIn("代理连接被拒绝", window.text.get("1.0", "end"))

        self.app.events.put(("current", "network", self._network_event("failed", 3)))
        self.app.events.put(("current", "error", "连接失败，已尝试 3 次"))
        self.app.events.put(("current", "done", None))
        self._poll()
        self.assertIn("连接失败", self.app.connection["text"])
        self.assertEqual(self.app.notice_report_button.winfo_manager(), "pack")
        self.assertEqual(str(window.retry_button["state"]), "normal")
        with patch.object(window, "clipboard_clear") as clear, patch.object(window, "clipboard_append") as append:
            window.copy_report()
        clear.assert_called_once()
        append.assert_called_once_with(self.app._network_report_text())
        self.assertIn("第 3/3 次", append.call_args.args[0])
        self.assertNotIn(self.settings["airtable_token"], append.call_args.args[0])

        self._new_job("recovery")
        self.app.events.put(("recovery", "network", self._network_event("recovered", 2)))
        self._poll()
        self.assertIn("最近请求成功", self.app.connection["text"])
        self.assertEqual(self.app.notice_label["fg"], ui.C["green"])
        report = window.text.get("1.0", "end")
        self.assertIn("请求成功", report)
        self.assertIn("请求失败", report)

    def test_old_network_events_and_changed_credentials_cannot_change_connection_state(self):
        self._new_job()
        self.app.events.put(("old-job", "network", self._network_event("failed", 3)))
        self._poll()
        self.assertFalse(self.app._network_events)
        self.app.values["base_id"].set("appChanged")
        self.app.events.put(("current", "network", self._network_event("recovered")))
        self.app.events.put(("current", "airtable_connection", {"bases": []}))
        with patch.object(self.app, "_airtable_connection_ready") as ready:
            self._poll()
        ready.assert_not_called()
        self.assertFalse(self.app._network_events)
        self.assertIn("未验证", self.app.connection["text"])

    def test_network_history_is_bounded_and_newest_first(self):
        for number in range(90):
            event = self._network_event("request")
            event.update(at=f"event-{number}", report=f"report-{number}")
            self.app._record_network_event(event)
        self.assertEqual(len(self.app._network_events), 80)
        text = self.app._network_report_text()
        self.assertNotIn("[event-0]", text)
        self.assertLess(text.index("[event-89]"), text.index("[event-10]"))

    def test_new_events_keep_report_scrolled_and_clear_stale_copy_confirmation(self):
        for _ in range(20):
            self.app._record_network_event(self._network_event("request"))
        self.app._show_network_report()
        window = self.app._network_window
        window.withdraw()
        self.root.update_idletasks()
        window.text.yview_moveto(0.5)
        window.copy_status.configure(text="已复制安全报告")
        self.app._record_network_event(self._network_event("failed", 3))
        self.assertGreater(window.text.yview()[0], 0.1)
        self.assertEqual(window.copy_status["text"], "")

    def test_manual_network_retry_only_discovers_connection_and_does_not_repeat_writes(self):
        result = {"bases": [{"id": "appTest", "name": "Current Base"}],
                  "base": {"id": "appTest", "name": "Current Base"},
                  "tables": {kind: "tbl" + kind for kind in ("projects", "tasks", "issues")}}
        def discover(token, base_id, *, on_event):
            on_event(self._network_event("request"))
            return result
        with patch.object(ui.threading, "Thread") as thread, \
                patch("autopm.connection.discover_connection", side_effect=discover) as connection, \
                patch("autopm.sync.apply_plan") as apply, patch("autopm.airtable.AirtableClient") as client:
            self.app._retry_connection()
            self.app._retry_connection()
            self.assertEqual(thread.call_count, 1)
            thread.call_args.kwargs["target"]()
            self._poll()
        connection.assert_called_once_with("fake-airtable-token", "appTest", on_event=ANY)
        client.assert_not_called()
        apply.assert_not_called()
        self.assertIn("已连接", self.app.connection["text"])
        self.assertEqual(len(self.app._network_events), 1)
        self.assertFalse(self.app.busy)

    def test_verified_badge_survives_same_token_and_expires_when_base_or_token_changes(self):
        self.assertIn("已填写，未验证", self.app.connection["text"])
        self.app._mark_connection_verified()
        self.app.values["airtable_token"].set(self.settings["airtable_token"])
        self.assertEqual(self.app.values["base_id"].get(), "appTest")
        self.assertIn("已连接", self.app.connection["text"])
        self.app.values["base_id"].set("appOther")
        self.assertIn("未验证", self.app.connection["text"])
        self.app._mark_connection_verified()
        self.app.values["airtable_token"].set("replacement-token")
        self.assertNotIn("已连接", self.app.connection["text"])
        self.assertIsNone(self.app._connection_verified)

    def test_busy_reentry_keeps_one_worker_and_disables_mutating_controls(self):
        self._render()
        with patch.object(ui.threading, "Thread") as thread:
            self.assertTrue(self.app._start(Mock(), self.settings))
            job = self.app._job_id
            self.assertFalse(self.app._start(Mock(), self.settings))
            self.app._choose(self.folder / "other.xlsx")
            self.app._analyze(True)
            self.app._apply()
            self.app._pick()
            self.app._import()
            with patch.object(ui, "save_settings") as save:
                self.app._save()
                save.assert_not_called()
            self.assertEqual(thread.call_count, 1)
            thread.return_value.start.assert_called_once()
            self.assertEqual(self.app._job_id, job)
            self.assertEqual(self.app.filename.get(), str(self.source))
            self.assertTrue(all(str(widget["state"]) == "disabled" for widget in self.app._controls))
            self.confirm.assert_not_called()
            self.file_dialog.assert_not_called()

    def test_worker_error_uses_its_frozen_config_and_always_finishes(self):
        config = deepcopy(self.settings)
        action = Mock(side_effect=ValueError("failed fake-deepseek-key fake-airtable-token"))
        with patch.object(ui.threading, "Thread") as thread:
            self.app._start(action, config)
            config["deepseek_api_key"] = "changed-after-start"
            config["airtable_token"] = "changed-after-start"
            thread.call_args.kwargs["target"]()
        self._poll()
        self.assertFalse(self.app.busy)
        self.assertIsNone(self.app.plan)
        message = self.app.notice_label["text"]
        self.assertIn("操作未完成", message)
        self.assertNotIn("fake-deepseek-key", message)
        self.assertNotIn("fake-airtable-token", message)

    def test_file_date_and_connection_changes_invalidate_preview_and_details(self):
        changes = ((self.app.filename, str(self.folder / "other.xlsx")),
                   (self.app.report_date, "2026-09-04"), (self.app.values["base_id"], "appOther"),
                   (self.app.values["deepseek_model"], "different-model"),
                   (self.app.date_mode, "due_minus_7"), (self.app.require_milestone, False))
        for variable, value in changes:
            with self.subTest(value=value):
                self._render()
                self.app.tree.selection_set("0")
                self.app._show_row()
                self.assertEqual(self.app.detail.winfo_manager(), "pack")
                revision = self.app._revision
                variable.set(value)
                self.assertGreater(self.app._revision, revision)
                self.assertIsNone(self.app.plan)
                self.assertTrue(self.app._stale)
                self.assertIn("预览已过期", self.app.notice_label["text"])
                self.assertEqual(str(self.app.apply_button["state"]), "disabled")
                self.assertEqual(self.app.detail.winfo_manager(), "")
                self.assertTrue(all(not widget.get("1.0", "end").strip() for widget in self.app.detail_texts))

    def test_old_job_events_cannot_replace_preview_or_finish_current_job(self):
        self._render()
        previous_plan = deepcopy(self.app.plan)
        self._new_job()
        self.app.status.set("Current job")
        for kind, payload in (("status", "Old status"), ("preview", (None,) * 6),
                              ("applied", {"status": "completed"}), ("error", "Old error"), ("done", None)):
            self.app.events.put(("old-job", kind, payload))
        self._poll()
        self.assertTrue(self.app.busy)
        self.assertEqual(self.app.plan, previous_plan)
        self.assertEqual(self.app.status.get(), "Current job")
        self.assertEqual(str(self.app.apply_button["state"]), "disabled")
        self.app.events.put(("current", "done", None))
        self._poll()
        self.assertFalse(self.app.busy)

    def test_current_job_result_with_old_input_revision_is_rejected(self):
        self._render()
        revision = self.app._revision
        self._new_job()
        report, plan = preview_fixture()
        self.app.report_date.set("2026-09-04")
        self.app.events.put(("current", "preview", (report, plan, self.folder, self.settings,
                                                      revision, ui.fingerprint(self.source))))
        self.app.events.put(("current", "done", None))
        with patch.object(self.app, "_render") as render:
            self._poll()
        render.assert_not_called()
        self.assertFalse(self.app.busy)
        self.assertIsNone(self.app.plan)
        self.assertIn("结果已过期", self.app.notice_label["text"])
        self.assertEqual(str(self.app.apply_button["state"]), "disabled")

    def test_current_preview_becomes_applicable_only_when_worker_finishes(self):
        self.app.filename.set(str(self.source))
        self._new_job()
        report, plan = preview_fixture()
        self.app.events.put(("current", "preview", (report, plan, self.folder, self.settings,
                                                      self.app._revision, ui.fingerprint(self.source))))
        self._poll()
        self.assertTrue(self.app.busy)
        self.assertEqual(str(self.app.apply_button["state"]), "disabled")
        self.app.events.put(("current", "done", None))
        self._poll()
        self.assertFalse(self.app.busy)
        self.assertEqual(str(self.app.apply_button["state"]), "normal")
        self.assertEqual(self.app.plan, plan)

    def test_filter_and_selection_never_reduce_the_confirmed_write_plan(self):
        _, expected_plan = self._render()
        self.app.search.set("EB1")
        self.app.kind_filter.set("任务")
        self.app._filter_rows()
        self.assertEqual(len(self.app.tree.get_children()), 1)
        self.assertEqual(self.app.row_count["text"], "1 / 4 项字段")
        self.app.tree.selection_set("0")
        self.app._show_row()
        self.assertEqual(self.app.plan, expected_plan)
        self.confirm.return_value = True
        with patch.object(self.app, "_start") as start:
            self.app._apply()
        self.assertIn("3 条记录变更", self.confirm.call_args.args[1])
        self.assertIn("筛选和选中行仅用于查看", self.confirm.call_args.args[1])
        action, config = start.call_args.args
        # Changing a display row cannot change the captured write payload.
        self.app._rows[0]["after_text"] = "Changed display only"
        with patch("autopm.airtable.AirtableClient") as client, patch("autopm.sync.apply_plan") as apply:
            apply.return_value = {"status": "completed", "applied": 3}
            action(Mock())
        self.assertEqual(apply.call_args.args[1], expected_plan)
        self.assertEqual(config["base_id"], "appTest")
        client.assert_called_once_with("fake-airtable-token", "appTest", on_event=ANY)
        self.assertIsNone(self.app.plan)
        self.assertTrue(self.app._stale)

    def test_cancel_confirmation_preserves_preview_without_starting_a_worker(self):
        _, expected_plan = self._render()
        with patch.object(self.app, "_start") as start:
            self.app._apply()
        self.confirm.assert_called_once()
        start.assert_not_called()
        self.assertEqual(self.app.plan, expected_plan)
        self.assertFalse(self.app._stale)

    def test_modified_or_removed_source_cannot_reuse_preview(self):
        for removed in (False, True):
            with self.subTest(removed=removed):
                self.source.write_bytes(b"source version one")
                self._render()
                self.confirm.reset_mock()
                if removed:
                    self.source.unlink()
                else:
                    self.source.write_bytes(b"source version two")
                with patch.object(self.app, "_start") as start:
                    self.app._apply()
                start.assert_not_called()
                self.confirm.assert_not_called()
                self.assertIsNone(self.app.plan)
                self.assertTrue(self.app._stale)
                self.assertIn("源文件", self.app.notice_label["text"])
                self.assertEqual(str(self.app.apply_button["state"]), "disabled")

    def test_source_modified_during_confirmation_is_rejected_before_airtable(self):
        self._render()
        def modify_then_confirm(*_args, **_kwargs):
            self.source.write_bytes(b"changed while confirmation was open")
            return True
        self.confirm.side_effect = modify_then_confirm
        with patch.object(ui.threading, "Thread") as thread:
            self.app._apply()
            with patch("autopm.airtable.AirtableClient") as client, patch("autopm.sync.apply_plan") as apply:
                thread.call_args.kwargs["target"]()
            client.assert_not_called()
            apply.assert_not_called()
        self._poll()
        self.assertIn("确认期间周报文件发生变化", self.app.notice_label["text"])
        self.assertFalse(self.app.busy)
        self.assertIsNone(self.app.plan)
        self.assertEqual(str(self.app.apply_button["state"]), "disabled")

    def test_blockers_are_visible_and_prevent_even_direct_apply(self):
        _, plan = preview_fixture()
        blocker = "Required setup: Projects.Date must be date"
        plan["blockers"] = [blocker]
        self._render(plan)
        self.assertIn(blocker, self.app.notes.get("1.0", "end"))
        self.assertIn("阻止写入", self.app.notes.get("1.0", "end"))
        self.assertEqual(self.app.warning_page.winfo_manager(), "pack")
        self.assertEqual(str(self.app.apply_button["state"]), "disabled")
        with patch.object(self.app, "_start") as start:
            self.app._apply()
        start.assert_not_called()
        self.confirm.assert_not_called()
        self.app._filter_warnings("fields")
        self.assertIn(blocker, self.app.notes.get("1.0", "end"))

    def test_zero_change_schema_failure_is_shown_as_blocked_preview(self):
        _, plan = preview_fixture()
        plan["changes"] = []
        blocker = "Required setup: Projects.report_date must be date"
        plan["blockers"] = [blocker, "Required setup: Projects.update_this_week must be multilineText"]
        self._render(plan)
        self.assertEqual(self.app.metrics[1][0]["text"], "受阻")
        self.assertIn("2 项阻止写入", self.app.metrics[1][1]["text"])
        self.assertIn("预览受阻", self.app.write_scope["text"])
        self.assertIn(blocker, self.app.write_scope["text"])
        self.assertIn(blocker, self.app.status.get())
        self.assertNotIn("预览已生成", self.app.status.get())
        self.assertNotIn("无待写入变更", self.app.write_scope["text"])
        self.assertEqual(self.app.warning_page.winfo_manager(), "pack")
        self.assertEqual(str(self.app.apply_button["state"]), "disabled")

    def test_unblocked_zero_changes_and_offline_results_keep_distinct_messages(self):
        _, plan = preview_fixture()
        plan["changes"] = []
        plan["project_guards"] = [{"project_id": "AB-123"}]
        self._render(plan)
        self.assertEqual(self.app.metrics[1][0]["text"], "0")
        self.assertIn("无待写入变更", self.app.write_scope["text"])
        self.assertIn("0 条待写入", self.app.status.get())
        self.assertNotIn("受阻", self.app.status.get())
        self.assertEqual(self.app.change_page.winfo_manager(), "pack")
        self._render(offline=True)
        self.assertEqual(self.app.metrics[1][0]["text"], "—")
        self.assertIn("离线解析完成", self.app.write_scope["text"])
        self.assertIn("离线检查完成", self.app.status.get())
        self.assertNotIn("受阻", self.app.status.get())

    def test_completed_partial_and_blocked_feedback_consumes_preview(self):
        for status, applied, skipped, prefix in (("completed", 3, 0, "同步已完成"),
                                                ("partial", 1, 1, "部分记录已写入"),
                                                ("blocked", 0, 0, "本次写入已停止")):
            with self.subTest(status=status):
                self._render()
                self._new_job()
                errors = [] if status == "completed" else ["AB-123: record changed since preview"]
                self.app.events.put(("current", "applied", {"status": status, "applied": applied,
                                                              "skipped": skipped, "errors": errors}))
                self.app.events.put(("current", "done", None))
                self._poll()
                self.assertIn(prefix, self.app.notice_label["text"])
                self.assertIn(f"已写入 {applied} 条，跳过 {skipped} 条", self.app.status.get())
                self.assertEqual(self.app.notice_label["fg"], ui.C["green"] if status == "completed" else ui.C["red"])
                self.assertFalse(self.app.busy)
                self.assertIsNone(self.app.plan)
                self.assertTrue(self.app._stale)
                self.assertEqual(str(self.app.apply_button["state"]), "disabled")
                self.assertIn("预览已使用", self.app.write_scope["text"])
                if errors:
                    self.assertIn(errors[0], self.app.notes.get("1.0", "end"))
                    self.app._filter_warnings(None)
                    self.assertIn(errors[0], self.app.notes.get("1.0", "end"))
                    self.app._filter_warnings("write_result")
                    self.assertIn(errors[0], self.app.notes.get("1.0", "end"))

    def test_successful_response_with_failed_readback_is_not_reported_as_zero_writes(self):
        self._render()
        self.app._applied({'status':'partial', 'applied':0, 'skipped':0,
                           'written_unverified':1, 'errors':['Readback differs']})
        self.assertIn('已返回写入成功', self.app.status.get())
        self.assertIn('云端可能已改变', self.app.status.get())
        self.assertNotIn('已写入 0 条', self.app.status.get())

    def test_offline_analysis_does_not_connect_to_ai_or_airtable(self):
        self.app.filename.set(str(self.source))
        report, _ = preview_fixture()
        with patch.object(ui.threading, "Thread") as thread, \
                patch("autopm.workbook.read_workbook", return_value={"test": "evidence"}), \
                patch("autopm.workbook.parse_local", return_value=report), \
                patch.object(ui, "save_preview") as save, \
                patch("autopm.deepseek.DeepSeekClient") as deepseek, \
                patch("autopm.airtable.AirtableClient") as airtable:
            self.app._analyze(False)
            thread.call_args.kwargs["target"]()
            self._poll()
        deepseek.assert_not_called()
        airtable.assert_not_called()
        save.assert_called_once()
        self.assertEqual(self.app.report, report)
        self.assertIsNone(self.app.plan)
        self.assertFalse(self.app.busy)
        self.assertEqual(str(self.app.apply_button["state"]), "disabled")
        self.assertEqual({row["kind"] for row in self.app._rows}, {"projects", "tasks", "issues"})
        self.assertTrue(all(row["action_label"] == "仅离线读取" for row in self.app._rows))
        self.assertEqual(self.app._view_data["changes"], [])
        self.app.kind_filter.set("任务")
        self.app._filter_rows()
        self.assertTrue(self.app.tree.get_children())
        self.assertTrue(all(row["kind"] == "tasks" for row in self.app._row_lookup.values()))

    def test_source_changed_while_reading_never_publishes_preview(self):
        self.app.filename.set(str(self.source))
        def read_changed(*_args, **_kwargs):
            self.source.write_bytes(b"changed during workbook read")
            return {"test": "evidence"}
        with patch.object(ui.threading, "Thread") as thread, \
                patch("autopm.workbook.read_workbook", side_effect=read_changed), \
                patch("autopm.workbook.parse_local") as parse, patch.object(ui, "save_preview") as save:
            self.app._analyze(False)
            thread.call_args.kwargs["target"]()
            self._poll()
        parse.assert_not_called()
        save.assert_not_called()
        self.assertIsNone(self.app.report)
        self.assertIsNone(self.app.plan)
        self.assertFalse(self.app.busy)
        self.assertIn("读取期间周报文件发生变化", self.app.notice_label["text"])

    def test_local_result_can_preview_and_apply_with_no_model_key(self):
        from test_schema_memory import PreviewClient
        from test_sync import fixture
        snapshot,report=fixture()
        snapshot['records']['tbl_projects'][0]['fields'].update(fld_projects_sku='SKU-1',fld_projects_factory=['recFactory'])
        report['projects'][0]['fields'].update(sku='SKU-1',factory='F1')
        client=PreviewClient(snapshot)
        report['projects'][0]['tasks']=[{'name':'EB1','date':'2026-09-10'}]
        report['projects'][0]['issues']=[{'text':'Drawing approval','action':'Review CAD'}]
        self.app.values['deepseek_api_key'].set('')
        self.app.filename.set(str(self.source))
        self.app._render(report,None,self.folder/'initial',self.app._config(),self.app._revision,ui.fingerprint(self.source))
        self.assertEqual(str(self.app.local_preview_button['state']),'normal')
        with patch.object(ui.threading,'Thread') as thread, patch('autopm.airtable.AirtableClient') as airtable, \
             patch('autopm.deepseek.DeepSeekClient') as deepseek:
            airtable.return_value.__enter__.return_value=client
            self.app._connect_local();thread.call_args.kwargs['target']();self._poll()
            self.assertFalse(self.app.plan['blockers']);self.assertFalse(client.writes)
            self.assertEqual(str(self.app.apply_button['state']),'normal')
            self.confirm.return_value=True
            self.app._apply();thread.call_args.kwargs['target']();self._poll()
        deepseek.assert_not_called()
        self.assertEqual(len(client.writes),3)
        self.assertIn('同步已完成',self.app.notice_label['text'])

    def test_local_preview_rejects_changed_source_without_network(self):
        self._render(offline=True)
        self.source.write_bytes(b'changed')
        with patch.object(self.app,'_start') as start:
            self.app._connect_local()
        start.assert_not_called();self.assertTrue(self.app._stale)

    def test_schema_editor_save_rechecks_live_schema_before_persisting(self):
        from test_sync import fixture
        from autopm.schema_ui import SchemaEditor
        from autopm.schema_memory import SchemaMemoryStore
        schema=fixture()[0]['schema'];store=SchemaMemoryStore(self.folder/'memory');saved=Mock()
        editor=SchemaEditor(self.root,schema,self.settings,store,saved)
        try:
            changed=deepcopy(schema);changed['tables'][0]['name']='changed after review'
            with patch.object(ui.threading,'Thread') as thread,patch.object(editor,'_fresh_schema',return_value=changed):
                editor._save();thread.call_args.kwargs['target']()
                with patch.object(editor,'after'):editor._poll()
            self.assertIsNone(store.load('appTest'));saved.assert_not_called()
            self.assertIn('保存前表结构已变化',editor.status.get())
            with patch.object(ui.threading,'Thread') as thread,patch.object(editor,'_fresh_schema',return_value=schema):
                editor._save();thread.call_args.kwargs['target']()
                with patch.object(editor,'after'):editor._poll()
            self.assertIsNotNone(store.load('appTest'));saved.assert_called_once()
        finally:editor.destroy()

    def test_schema_editor_reports_network_events_on_the_ui_queue_without_finishing_worker(self):
        from test_sync import fixture
        from autopm.schema_ui import SchemaEditor
        from autopm.schema_memory import SchemaMemoryStore
        schema=fixture()[0]['schema'];received=Mock()
        editor=SchemaEditor(self.root,schema,self.settings,SchemaMemoryStore(self.folder/'memory'),Mock(),on_network=received)
        editor.withdraw()
        try:
            with patch('autopm.schema_ui.AirtableClient') as client:
                client.return_value.__enter__.return_value.get_schema.return_value=schema
                editor._fresh_schema()
                client.call_args.kwargs['on_event'](self._network_event())
            received.assert_not_called()
            editor.busy=True
            with patch.object(editor,'after'):editor._poll()
            self.assertTrue(editor.busy)
            received.assert_called_once_with(self._network_event())
            self.assertIn('代理连接被拒绝',editor.status.get())
            editor._show_network_report();editor._network_window.withdraw()
            self.assertIn('第 1/3 次',editor._network_window.text.get('1.0','end'))
            self.assertEqual(str(editor._network_window.retry_button['state']),'disabled')
        finally:editor.destroy()

    def test_schema_network_retry_preserves_unsaved_mapping_choices(self):
        from test_sync import fixture
        from autopm.schema_ui import SchemaEditor
        from autopm.schema_memory import SchemaMemoryStore
        schema=fixture()[0]['schema'];saved=Mock();store=SchemaMemoryStore(self.folder/'memory')
        editor=SchemaEditor(self.root,schema,self.settings,store,saved)
        editor.withdraw()
        try:
            editor.selections={'tables':{'projects':schema['tables'][0]['id']},
                               'fields':{'projects':{'project_name':'fld_unsaved_choice'}}}
            choices=deepcopy(editor.selections)
            changed=deepcopy(schema);changed['tables'][0]['name']='renamed in Airtable'
            with patch.object(ui.threading,'Thread') as thread, \
                    patch.object(editor,'_fresh_schema',return_value=changed) as fresh, \
                    patch.object(store,'save') as save:
                editor._retry_connection()
                thread.call_args.kwargs['target']()
                with patch.object(editor,'after'):editor._poll()
            fresh.assert_called_once()
            save.assert_not_called();saved.assert_not_called()
            self.assertEqual(editor.selections,choices)
            self.assertEqual(editor.schema,schema)
            self.assertIn('连接检测成功',editor.status.get())
        finally:editor.destroy()

    def test_schema_editor_model_suggestion_is_pending_until_save(self):
        from test_sync import fixture
        from autopm.schema_ui import SchemaEditor
        from autopm.schema_memory import SchemaMemoryStore,reconcile
        schema=fixture()[0]['schema'];store=SchemaMemoryStore(self.folder/'memory');saved=Mock()
        memory=reconcile(schema,self.settings)['memory'];store.save(memory)
        schema['tables'][0]['fields'][1]['id']='fld_new_title'
        editor=SchemaEditor(self.root,schema,self.settings,store,saved)
        proposal={'tables':[],'fields':[{'kind':'projects','key':'project_name','field_id':'fld_new_title','reason':'title'}]}
        try:
            with patch.object(ui.threading,'Thread') as thread,patch('autopm.schema_ui.suggest_mappings',return_value=proposal):
                editor._suggest();thread.call_args.kwargs['target']()
                with patch.object(editor,'after'):editor._poll()
            self.assertEqual(editor.selections['fields']['projects']['project_name'],'fld_new_title')
            self.assertEqual(store.load('appTest'),memory);saved.assert_not_called()
            self.assertIn('尚未保存',editor.status.get())
        finally:editor.destroy()

    def test_tracker_default_requires_cloud_connection_for_confirmed_chain(self):
        from test_tracker import tracker_fixture,report_fixture
        tracker=self.folder/'alltracker.xlsx';tracker_fixture(tracker)
        output=self.folder/'updated.xlsx';page=self.app.tracker_page
        self.app.values['deepseek_api_key'].set('');self.app.values['airtable_token'].set('')
        self.app._navigate(3);page.tracker.set(str(tracker));page.reports=[str(self.source)];page.update_files()
        with patch.object(ui.threading,'Thread') as thread,patch('autopm.workbook.read_workbook',return_value={}), \
             patch('autopm.workbook.parse_local',return_value=report_fixture()), \
             patch('autopm.deepseek.DeepSeekClient') as model,patch('autopm.airtable.AirtableClient') as airtable:
            page.preview()
            thread.assert_not_called()
        model.assert_not_called();airtable.assert_not_called()
        self.assertEqual(page.source_kind.get(),'airtable')
        self.assertFalse(output.exists())
        self.assertIsNone(page.plan)

    def test_local_tracker_settings_change_invalidates_export(self):
        page=self.app.tracker_page
        page.plan={'changes':[{}]}
        self.app.values['deepseek_model'].set('different')
        self.assertIsNone(page.plan);self.assertEqual(str(page.export_button['state']),'disabled')

    def _airtable_tracker_fixture(self, *, selected=True):
        from test_tracker import tracker_fixture,report_fixture
        from autopm.tracker import build_tracker_plan
        tracker=self.folder/'alltracker.xlsx';tracker_fixture(tracker)
        plan=build_tracker_plan(tracker,[report_fixture()])
        plan['source_kind']='airtable'
        plan['airtable_source']={'base_id':'appTest','captured_at':'2026-09-11T18:30:00+00:00',
            'scope_project_ids':['AB-123'],'scope':'selected_projects' if selected else 'all_projects'}
        return tracker,plan

    def _sync_context(self,ids=None):
        return {'base_id':'appTest','plan_id':'confirmed-plan','project_ids':['AB-123'] if ids is None else ids,'auto_tracker':True}

    def test_airtable_tracker_manual_preview_needs_no_report_or_model_and_shows_full_scope(self):
        tracker,plan=self._airtable_tracker_fixture(selected=False);page=self.app.tracker_page
        self.app.values['deepseek_api_key'].set('');page.tracker.set(str(tracker));page.source_kind.set('airtable')
        self.assertFalse(page.reports)
        self.assertEqual(str(page.preview_button['state']),'normal')
        with patch.object(ui.threading,'Thread') as thread, patch('autopm.airtable.AirtableClient') as airtable, \
                patch('autopm.workflow.prepare_airtable_tracker',return_value=plan) as prepare, \
                patch('autopm.deepseek.DeepSeekClient') as model,patch('autopm.workbook.read_workbook') as read:
            page.preview();thread.call_args.kwargs['target']();self._poll()
        model.assert_not_called();read.assert_not_called()
        self.assertIsNone(prepare.call_args.kwargs['project_ids'])
        airtable.assert_called_once_with('fake-airtable-token','appTest',on_event=ANY)
        self.assertEqual(page.tree.heading('after')['text'],'Airtable 新值')
        self.assertIn('全库匹配',page.source_summary.get());self.assertIn('2026-09-11T18:30',page.source_summary.get())
        self.assertEqual(str(page.export_button['state']),'normal')
        audit=next((self.folder/'Run Logs').glob('tracker_airtable_*/tracker_preview.json')).read_text(encoding='utf-8')
        self.assertNotIn('fake-airtable-token',audit);self.assertNotIn('fake-deepseek-key',audit)

    def test_successful_sync_starts_local_read_only_after_writer_done_and_uses_full_confirmed_scope(self):
        _,remote=self._render();remote=deepcopy(remote);remote['changes'][1]['project_id']='CD-456'
        self._render(remote);tracker,local=self._airtable_tracker_fixture();self.app.tracker_page.tracker.set(str(tracker))
        self.app.search.set('Drawing');self.app.kind_filter.set('问题');self.app._filter_rows()
        self.confirm.return_value=True
        with patch.object(ui.threading,'Thread') as thread,patch('autopm.airtable.AirtableClient'), \
                patch('autopm.sync.apply_plan',return_value={'status':'completed','applied':3}) as apply, \
                patch('autopm.workflow.prepare_airtable_tracker',return_value=local) as prepare:
            self.app._apply();writer_job=self.app._job_id
            thread.call_args.kwargs['target']()
            applied_event=self.app.events.get_nowait();done_event=self.app.events.get_nowait()
            self.assertEqual(applied_event[1],'applied');self.assertEqual(done_event[1],'done')
            self.app.events.put(applied_event);self._poll()
            self.assertTrue(self.app.busy);self.assertEqual(thread.call_count,1);prepare.assert_not_called()
            self.app.events.put(done_event);self._poll()
            self.assertEqual(thread.call_count,2);self.assertTrue(self.app.busy);self.assertNotEqual(writer_job,self.app._job_id)
            thread.call_args.kwargs['target']();self._poll()
        self.assertEqual(prepare.call_args.kwargs['project_ids'],['AB-123','CD-456'])
        self.assertEqual(apply.call_count,1);self.assertFalse(self.app.busy)
        self.assertEqual(self.app._active_page,3);self.assertIn('本地总表预览已生成',self.app.notice_label['text'])
        self.assertNotIn('fake-airtable-token',str(self.app._last_sync_context))

    def test_successful_sync_without_tracker_preserves_scope_for_later_read(self):
        self._render();self.confirm.return_value=True
        with patch.object(ui.threading,'Thread') as thread,patch('autopm.airtable.AirtableClient'), \
                patch('autopm.sync.apply_plan',return_value={'status':'completed','applied':3}), \
                patch('autopm.workflow.prepare_airtable_tracker') as prepare:
            self.app._apply();thread.call_args.kwargs['target']();self._poll()
            prepare.assert_not_called();self.assertEqual(thread.call_count,1)
        page=self.app.tracker_page
        self.assertFalse(self.app.busy);self.assertEqual(self.app._active_page,3)
        self.assertEqual(page.scope_context['project_ids'],['AB-123'])
        self.assertIn('请选择 All Tracker',page.summary.get())
        tracker,plan=self._airtable_tracker_fixture();page.tracker.set(str(tracker))
        with patch.object(ui.threading,'Thread') as thread,patch('autopm.airtable.AirtableClient'), \
                patch('autopm.workflow.prepare_airtable_tracker',return_value=plan) as prepare:
            page.preview();thread.call_args.kwargs['target']();self._poll()
        self.assertEqual(prepare.call_args.kwargs['project_ids'],['AB-123'])

    def test_partial_blocked_and_disabled_followup_do_not_start_local_read(self):
        for status,enabled in (('partial',True),('blocked',True),('completed',False)):
            with self.subTest(status=status,enabled=enabled):
                self._render();self._new_job();context=self._sync_context();context['auto_tracker']=enabled
                self.app.events.put(('current','applied',({'status':status,'applied':1},context,self.app._revision)))
                self.app.events.put(('current','done',None))
                with patch.object(self.app.tracker_page,'follow_sync') as follow:self._poll()
                follow.assert_not_called();self.assertFalse(self.app.busy)

    def test_empty_confirmed_scope_never_expands_into_a_full_database_read(self):
        tracker,_=self._airtable_tracker_fixture();page=self.app.tracker_page;page.tracker.set(str(tracker))
        with patch.object(self.app,'_start') as start:
            page.follow_sync(self._sync_context([]),self.app._credential_key())
            page.preview()
        start.assert_not_called();self.assertIn('没有已确认变更项目',page.summary.get())
        _,empty=preview_fixture();empty['changes']=[];self._render(empty)
        with patch.object(self.app,'_start') as start:self.app._apply()
        start.assert_not_called()

    def test_followup_failure_keeps_cloud_success_and_retry_never_replays_apply(self):
        tracker,plan=self._airtable_tracker_fixture();page=self.app.tracker_page;page.tracker.set(str(tracker))
        with patch.object(ui.threading,'Thread') as thread,patch('autopm.airtable.AirtableClient'), \
                patch('autopm.workflow.prepare_airtable_tracker',side_effect=[RuntimeError('读取响应超时'),plan]) as prepare, \
                patch('autopm.sync.apply_plan') as apply:
            page.follow_sync(self._sync_context(),self.app._credential_key())
            thread.call_args.kwargs['target']();self._poll()
            self.assertIn('Airtable 已同步，本地总表尚未更新',self.app.notice_label['text'])
            self.assertIn('只读重试',self.app.status.get());self.assertIsNone(page.plan)
            self.assertEqual(str(page.preview_button['state']),'normal')
            page.preview();thread.call_args.kwargs['target']();self._poll()
        apply.assert_not_called();self.assertEqual(prepare.call_count,2);self.assertIsNotNone(page.plan)

    def test_followup_input_changes_between_applied_and_done_cancel_automatic_read(self):
        self._render();self._new_job();revision=self.app._revision
        self.app._applied({'status':'completed','applied':3},self._sync_context(),revision)
        self.app.report_date.set('2026-09-12')
        self.app.events.put(('current','done',None))
        with patch.object(self.app.tracker_page,'follow_sync') as follow:self._poll()
        follow.assert_not_called();self.assertIn('Airtable 已同步，本地总表尚未更新',self.app.notice_label['text'])

    def test_changed_credentials_or_old_job_cannot_start_followup_or_accept_local_preview(self):
        tracker,plan=self._airtable_tracker_fixture();page=self.app.tracker_page;page.tracker.set(str(tracker))
        page.scope_context=self._sync_context();page.scope_credentials=self.app._credential_key()
        self.app.values['base_id'].set('appOther')
        with patch.object(self.app,'_start') as start:page.preview_airtable()
        start.assert_not_called();self.assertIn('连接配置已变化',self.app.notice_label['text'])
        self._new_job('local');revision=(self.app._revision,page.revision)
        page.tracker.set(str(self.folder/'another.xlsx'))
        self.app.events.put(('old','applied',({'status':'completed'},self._sync_context(),self.app._revision)))
        self.app.events.put(('old','tracker_preview',(plan,revision)))
        self.app.events.put(('local','tracker_preview',(plan,revision)))
        self.app.events.put(('local','done',None))
        self._poll();self.assertIsNone(page.plan);self.assertIn('已过期',page.summary.get())

    def test_airtable_preview_busy_reentry_and_network_events_use_existing_queue(self):
        tracker,plan=self._airtable_tracker_fixture();page=self.app.tracker_page;page.tracker.set(str(tracker));page.source_kind.set('airtable')
        def prepare(*args,**kwargs):
            callback=airtable.call_args.kwargs['on_event'];callback(self._network_event('retry'))
            return plan
        with patch.object(ui.threading,'Thread') as thread,patch('autopm.airtable.AirtableClient') as airtable, \
                patch('autopm.workflow.prepare_airtable_tracker',side_effect=prepare):
            page.preview();page.preview();self.assertEqual(thread.call_count,1)
            self.assertEqual(str(page.export_button['state']),'disabled')
            thread.call_args.kwargs['target']();self._poll()
        self.assertEqual(len(self.app._network_events),1);self.assertIn('第 1/3 次',self.app._network_report_text())

    def test_airtable_export_failure_retains_preview_and_only_retries_local_export(self):
        tracker,plan=self._airtable_tracker_fixture();page=self.app.tracker_page;page.tracker.set(str(tracker));page.source_kind.set('airtable')
        page.scope_context=self._sync_context();page.scope_credentials=self.app._credential_key()
        page.render((plan,(self.app._revision,page.revision)))
        output=self.folder/'copy.xlsx'
        result={'output':str(output),'changed_cells':3}
        with patch.object(ui.threading,'Thread') as thread,patch.object(ui.filedialog,'asksaveasfilename',return_value=str(output)), \
                patch('autopm.tracker_ui.export_tracker',side_effect=[PermissionError('文件正在使用'),result]) as export, \
                patch('autopm.sync.apply_plan') as apply,patch('autopm.workflow.prepare_airtable_tracker') as read:
            page.export();thread.call_args.kwargs['target']();self._poll()
            self.assertIn('Airtable 已同步，本地总表导出尚未完成',self.app.notice_label['text'])
            self.assertIsNotNone(page.plan);self.assertEqual(str(page.export_button['state']),'normal')
            page.export();thread.call_args.kwargs['target']();self._poll()
        self.assertEqual(export.call_count,2);apply.assert_not_called();read.assert_not_called()

    def test_tracker_path_and_followup_option_save_and_export_can_be_next_input(self):
        tracker,plan=self._airtable_tracker_fixture();page=self.app.tracker_page;page.tracker.set(str(tracker))
        self.app.auto_tracker.set(False)
        with patch.object(ui,'save_settings') as save:self.app._save()
        self.assertEqual(save.call_args.args[0]['local_tracker_path'],str(tracker))
        self.assertFalse(save.call_args.args[0]['sync_local_tracker_after_sync'])
        output=self.folder/'exported.xlsx';output.write_bytes(b'exported file')
        page.last_output=str(output);page.use_output()
        self.assertEqual(page.tracker.get(),str(output));self.assertEqual(self.app.settings['local_tracker_path'],str(output))

    def test_airtable_source_switch_preserves_weekly_file_workflow(self):
        page=self.app.tracker_page;page.reports=[str(self.source)];page.update_files()
        page.source_kind.set('airtable');self.assertEqual(page.file_list.winfo_manager(),'')
        page.source_kind.set('weekly');self.assertEqual(page.file_list.winfo_manager(),'grid')
        self.assertEqual(page.reports,[str(self.source)])
        self.assertEqual(page.preview_button['text'],'生成本地更新预览')

    def test_local_tracker_is_a_real_fourth_workflow_step(self):
        self.assertEqual(len(self.app.step_labels),4)
        self.app._navigate(3)
        self.assertEqual(self.app.step_labels[3]['fg'],ui.C['blue'])
        self.app._navigate(0)
        self.assertEqual(self.app.step_labels[0]['fg'],ui.C['blue'])
        self.assertEqual(self.app.step_labels[3]['fg'],ui.C['muted'])

    def test_compact_sync_view_preserves_space_for_changes_and_followup_controls(self):
        self._render()
        with patch.object(self.root,'winfo_height',return_value=760):self.app._responsive()
        self.assertEqual(self.app.metric_frame.winfo_manager(),'')
        self.assertEqual(self.app.tracker_followup_button.winfo_manager(),'pack')
        self.assertEqual(self.app.auto_tracker_check.winfo_manager(),'pack')
        with patch.object(self.root,'winfo_height',return_value=900):self.app._responsive()
        self.assertEqual(self.app.metric_frame.winfo_manager(),'pack')


if __name__ == "__main__":
    unittest.main()
