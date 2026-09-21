import copy
import unittest

from autopm.presentation import build_change_rows, build_review_data, filter_change_rows, filter_warning_rows, classify_warning


def sample():
    report = {"source": "weekly.xlsx", "warnings": ["Report 存在条件格式；完成状态只使用显式绿色填充。"],
              "projects": [{"project_id": "AB-123", "fields": {"project_name": "Example Project"},
                            "tasks": [{"name": "Award", "source": "'Report'!B7", "evidence": ["'Report'!B5", "'Report'!B7"]}],
                            "issues": [{"text": "Frozen CAD drawing for P2", "source": "'Report'!B64"}]}]}
    plan = {"plan_id": "test", "schema": {"tables": [{"id": "tblTasks", "fields": [
        {"id": "fldTaskName", "name": "Task Name (Manual)"},
        {"id": "fldUnknown", "name": "Additional Future Field"}]}]}, "changes": [
        {"kind": "tasks", "record_id": "recTask", "table_id": "tblTasks", "project_id": "AB-123",
         "fields": {"fldDue": "2026-09-12", "fldOwners": ["recJane"]},
         "before": {"fldDue": "2026-09-19", "fldOwners": ["recOld"]},
         "display_before": {"fldDue": "2026-09-19", "fldOwners": ["Old Owner"]},
         "display_after": {"fldDue": "2026-09-12", "fldOwners": ["Jane Smith"]},
         "field_names": {"fldDue": "Due Date (Manual)", "fldOwners": "Tasks Owners (Manual)"},
         "source": "'Report'!B7", "identity": {"title_field": "fldTaskName", "title": "award"},
         "completed": True, "custom_payload": {"must_survive": [1, 2, 3]}},
        {"kind": "issues", "record_id": "recIssue", "table_id": "tblIssues", "project_id": "AB-123",
         "fields": {"fldAction": "NPD support to freeze CAD drawing for P2"},
         "before": {"fldAction": "Wait for review"}, "field_names": {"fldAction": "Recovery Action (Manual)"},
         "source": "'Report'!B64", "identity": {"title_field": "fldIssueText", "title": "frozencaddrawingforp2"}},
        {"kind": "tasks", "record_id": None, "table_id": "tblTasks", "project_id": "XY-456",
         "fields": {"fldTaskName": "MP Start (VN)", "fldUnknown": False}, "before": {},
         "field_names": {"fldTaskName": "Task Name (Manual)"},
         "display_after": {"fldUnknown": False}, "source": "'Sheet2'!H10",
         "identity": {"title_field": "fldTaskName", "title": "mpstart(vn)"}}],
        "warnings": list(report["warnings"]) + [
            "AB-123: People 'Jane': ambiguous (2 matches); field skipped",
            "AB-123: 未配置里程碑映射，任务未写入",
            "AB-123: duplicate Airtable records; 该任务未写入",
            "AB-123 模型日期未通过来源校验，已排除无可靠来源的模型字段",
            "'Report'!B9 日期含删除线，未自动写入。"],
        "blockers": ["Required setup: Projects.Date must be date"]}
    return report, plan


class PresentationTests(unittest.TestCase):
    def test_date_only_task_and_action_only_issue_recover_full_titles(self):
        report, plan = sample()
        data = build_review_data(report, plan)
        self.assertEqual(data["rows"][0]["record_title"], "Award")
        self.assertEqual(data["rows"][2]["record_title"], "Frozen CAD drawing for P2")
        self.assertEqual(data["rows"][3]["record_title"], "MP Start (VN)")
        self.assertEqual(data["rows"][0]["source"], "'Report'!B7")
        self.assertEqual(data["rows"][0]["evidence"], ["'Report'!B5", "'Report'!B7"])

    def test_display_people_names_never_replace_retained_write_ids(self):
        report, plan = sample()
        original_report, original_plan = copy.deepcopy(report), copy.deepcopy(plan)
        data = build_review_data(report, plan)
        owner = next(row for row in data["rows"] if row["field_id"] == "fldOwners")
        self.assertEqual(owner["before_text"], "Old Owner")
        self.assertEqual(owner["after_text"], "Jane Smith")
        self.assertEqual(data["changes"][0]["fields"]["fldOwners"], ["recJane"])
        self.assertEqual(data["changes"][0]["custom_payload"], {"must_survive": [1, 2, 3]})
        owner["after_text"] = "Edited UI text"
        self.assertEqual(data["changes"][0]["fields"]["fldOwners"], ["recJane"])
        data["changes"][0]["fields"]["fldOwners"].append("recIndependentCopy")
        self.assertEqual(plan, original_plan)
        self.assertEqual(report, original_report)

    def test_filters_keep_every_matching_row_and_combine_with_and(self):
        report, plan = sample()
        data = build_review_data(report, plan)
        rows = data["rows"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(len(filter_change_rows(rows, kind="任务")), 4)
        self.assertEqual(len(filter_change_rows(rows, kind="tasks", action="新增")), 2)
        self.assertEqual(len(filter_change_rows(rows, "AB-123 Jane", kind="tasks", action="update")), 1)
        self.assertEqual(len(filter_change_rows(rows, "Frozen CAD", project_id=" ab- 123 ")), 1)
        self.assertEqual(len(filter_change_rows(rows, field="Due Date (Manual)")), 1)
        self.assertEqual(len(filter_change_rows(rows, kind="全部", action="全部")), 5)
        self.assertFalse(filter_change_rows(rows, "not in any full value"))
        self.assertEqual(data["summary"]["change_count"], 3)
        self.assertEqual({row["change_index"] for row in rows}, {0, 1, 2})

    def test_unknown_fields_false_zero_and_empty_change_are_not_lost(self):
        report, plan = sample()
        plan["changes"].append({"project_id": "AB-123", "kind": "projects", "record_id": "recProject", "fields": {}})
        data = build_review_data(report, plan)
        unknown = next(row for row in data["rows"] if row["field_id"] == "fldUnknown")
        self.assertEqual(unknown["field_name"], "Additional Future Field")
        self.assertEqual(unknown["after_text"], "否")
        self.assertEqual(data["rows"][-1]["record_title"], "Example Project")
        self.assertEqual(data["rows"][-1]["field_name"], "无字段变更")
        self.assertEqual(len(data["changes"]), 4)
        self.assertEqual(data["summary"]["field_count"], 5)
        self.assertEqual(data["summary"]["row_count"], 6)

    def test_warnings_categorized_with_original_text_and_no_report_double_count(self):
        report, plan = sample()
        data = build_review_data(report, plan)
        self.assertEqual(len(data["warnings"]), 6)
        self.assertEqual(sum(data["warning_counts"].values()), 6)
        self.assertEqual(len(data["blockers"]), 1)
        self.assertEqual(data["warning_counts"]["completion"], 1)
        self.assertEqual(data["warning_counts"]["model"], 1)
        self.assertEqual(data["warnings"][4]["message"], plan["warnings"][4])
        self.assertEqual(len(filter_warning_rows(data["warnings"], category="人员 / 工厂", project_id="AB-123")), 1)
        self.assertEqual(len(filter_warning_rows(data["warnings"], "来源校验", category="model")), 1)
        self.assertEqual(classify_warning("AB-123: Factory 'ABC': no unique match")["category"], "people_factory")

    def test_long_issue_and_values_remain_complete_and_searchable(self):
        report, plan = sample()
        long_title = "CAD issue " + "x" * 300 + " uniquely searchable end"
        report["projects"][0]["issues"][0]["text"] = long_title
        plan["changes"][1]["identity"]["title"] = "unavailable-title-fallback-to-source"
        data = build_review_data(report, plan)
        issue = data["rows"][2]
        self.assertEqual(issue["record_title"], long_title)
        self.assertLess(len(issue["record_title_preview"]), len(long_title))
        self.assertEqual(len(filter_change_rows(data["rows"], "uniquely searchable end")), 1)

    def test_offline_report_shows_all_record_kinds_without_write_operations(self):
        report, _ = sample()
        report["projects"][0]["report_date"] = "2026-09-07"
        report["projects"][0]["fields"].update(capacity="32K/month", custom_value=0)
        report["projects"][0]["tasks"][0].update(date="2026-09-10", completed=False)
        report["projects"][0]["issues"][0].update(action="Review P2 CAD", owner="Jane Smith", risk="H")
        original = copy.deepcopy(report)
        data = build_review_data(report, None)
        rows = data["rows"]
        self.assertEqual(data["mode"], "offline")
        self.assertEqual(data["changes"], [])
        self.assertEqual(data["summary"]["change_count"], 0)
        self.assertEqual(data["summary"]["create_count"], 0)
        self.assertEqual(data["summary"]["update_count"], 0)
        self.assertEqual(data["summary"]["source_by_kind"], {"projects": 1, "tasks": 1, "issues": 1})
        self.assertEqual({row["kind"] for row in rows}, {"projects", "tasks", "issues"})
        self.assertEqual({row["source_record_index"] for row in rows}, {0, 1, 2})
        self.assertTrue(all(row["before_text"] == "未对比 Airtable" for row in rows))
        self.assertTrue(all(row["action_label"] == "仅离线读取" and row["action"] == "read" for row in rows))
        self.assertTrue(all(row["field_id"] is None and row["record_id"] is None and row["change_index"] is None for row in rows))
        self.assertEqual(filter_change_rows(rows, field="capacity")[0]["after_text"], "32K/month")
        self.assertEqual(filter_change_rows(rows, field="custom_value")[0]["after_text"], "0")
        self.assertEqual(filter_change_rows(rows, field="completed")[0]["after_text"], "否")
        self.assertEqual(len(filter_change_rows(rows, "Jane Smith", kind="issues")), 1)
        self.assertFalse(filter_change_rows(rows, action="新增"))
        self.assertEqual(len(filter_change_rows(rows, action="仅离线读取")), len(rows))
        rows[0]["after_text"] = "UI edited text"
        self.assertEqual(report, original)

    def test_explicit_empty_plan_stays_empty_while_offline_records_remain_visible(self):
        report, _ = sample()
        report["projects"].append({"project_id": "EMPTY-1", "fields": {}, "tasks": [{}], "issues": [{}]})
        offline = build_review_data(report, None)
        self.assertEqual(offline["summary"]["source_record_count"], 6)
        self.assertEqual(len({row["source_record_index"] for row in offline["rows"]}), 6)
        self.assertEqual(len({row["row_id"] for row in offline["rows"]}), len(offline["rows"]))
        self.assertTrue(build_change_rows(report, None))
        comparison = build_review_data(report, {"changes": [], "warnings": [], "blockers": []})
        self.assertEqual(comparison["mode"], "comparison")
        self.assertEqual(comparison["rows"], [])
        self.assertEqual(comparison["changes"], [])


if __name__ == "__main__":
    unittest.main()
