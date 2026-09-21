import unittest
from datetime import date

from autopm.weekly_remark import (
    MAX_REMARK_LENGTH, merge_weekly_remark, read_weekly_remark, uses_weekly_remark,
)



def legacy(day, progress):
    """Actual historic framing, built independently from the current writer."""
    return ('[[AUTOPM_WEEKLY_REPORT:v1]]\n周报日期: '+day+'\n工程进展:\n'+progress+
            '\n[[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]\n[[/AUTOPM_WEEKLY_REPORT]]')

class WeeklyRemarkTests(unittest.TestCase):
    def test_storage_mode_is_explicit_and_base_scoped(self):
        self.assertFalse(uses_weekly_remark({}))
        self.assertFalse(uses_weekly_remark({"project_report_storage": True}))
        enabled = {"project_report_storage": "engineering_remark"}
        self.assertTrue(uses_weekly_remark(enabled))
        self.assertTrue(uses_weekly_remark({**enabled, "base_id": "app1",
                                         "project_report_storage_base_id": "app1"}))
        self.assertFalse(uses_weekly_remark({**enabled, "base_id": "app2",
                                          "project_report_storage_base_id": "app1"}))
        self.assertFalse(uses_weekly_remark({**enabled, "project_report_storage_base_id": "app1"}))

    def test_storage_profiles_follow_copy_main_copy_switches(self):
        config = {"project_report_storage": "engineering_remark",
                  "project_report_storage_base_id": "appCopy",
                  "project_report_storage_by_base": {
                      "appCopy": "engineering_remark", "appMain": "engineering_remark"}}
        for base in ("appCopy", "appMain", "appCopy"):
            with self.subTest(base=base):
                self.assertTrue(uses_weekly_remark({**config, "base_id": base}))
        for base in ("appUnknown", "appmain", "", None):
            with self.subTest(base=base):
                self.assertFalse(uses_weekly_remark({**config, "base_id": base}))

    def test_explicit_base_normal_mode_overrides_legacy_remark_mode(self):
        config = {"base_id": "appMain", "project_report_storage": "engineering_remark",
                  "project_report_storage_base_id": "appMain",
                  "project_report_storage_by_base": {"appMain": "normal"}}
        self.assertFalse(uses_weekly_remark(config))

    def test_missing_base_profile_retains_guarded_legacy_fallback(self):
        config = {"project_report_storage": "engineering_remark",
                  "project_report_storage_base_id": "appLegacy",
                  "project_report_storage_by_base": {"appMain": "engineering_remark"}}
        self.assertTrue(uses_weekly_remark({**config, "base_id": "appLegacy"}))
        self.assertFalse(uses_weekly_remark({**config, "base_id": "appOther"}))

    def test_profile_can_enable_storage_without_legacy_mode(self):
        config = {"project_report_storage_by_base": {"appMain": "engineering_remark"}}
        self.assertTrue(uses_weekly_remark({**config, "base_id": "appMain"}))
        self.assertFalse(uses_weekly_remark({**config, "base_id": "appOther"}))

    def test_malformed_profile_configuration_cannot_enable_storage(self):
        config = {"base_id": "appMain", "project_report_storage": "engineering_remark",
                  "project_report_storage_base_id": "appMain"}
        for profiles in (None, True, [], "engineering_remark", {"appMain": None},
                         {"appMain": True}, {"appMain": []}, {"appMain": {"mode": "engineering_remark"}}):
            with self.subTest(profiles=profiles):
                self.assertFalse(uses_weekly_remark({**config, "project_report_storage_by_base": profiles}))
        self.assertFalse(uses_weekly_remark({**config, "base_id": [],
                                            "project_report_storage_by_base": {}}))

    def test_plain_notes_have_no_report_date(self):
        for value in (None, "", " 原有备注\r\n2026-09-10 完成试产 "):
            with self.subTest(value=value):
                self.assertEqual(read_weekly_remark(value), {"report_date": None, "fields": {}})

    def test_preserves_manual_notes_and_plain_unicode_progress(self):
        notes = ' 人工备注：\r\n- **保留格式**\n'
        progress = '\t第一行😀\n第二行  '
        value = merge_weekly_remark(notes,'2026-09-15',{'current_progress':progress,'update_this_week':'stored separately'})
        self.assertTrue(value.startswith(notes+'\n\n'))
        self.assertEqual(read_weekly_remark(value)['fields'],{'current_progress':progress})

    def test_exact_reimport_does_not_grow(self):
        fields = {"current_progress": "初版", "update_this_week": "新增任务"}
        value = merge_weekly_remark("原备注", "2026-09-15", fields)
        self.assertEqual(merge_weekly_remark(value, "2026-09-15", fields), value)

    def test_plain_writer_preserves_source_without_adding_wrappers(self):
        progress='1. A\n2. B\n2. C\n**bold** and `literal`'
        value=merge_weekly_remark('manual','2026-09-15',{'current_progress':progress},rich_text=True)
        self.assertEqual(value,'manual\n\n--- 2026-09-15 ---\n'+progress)
        self.assertEqual(read_weekly_remark(value)['fields']['current_progress'],progress)

    def test_legacy_escaped_footer_is_readable_without_rewriting_notes(self):
        old=legacy('2026-09-10','Old').replace('END_PROGRESS',r'END\_PROGRESS')
        new=merge_weekly_remark(old,'2026-09-15',{'current_progress':'New'},rich_text=True)
        self.assertTrue(new.startswith(old+'\n\n'))
        self.assertEqual(read_weekly_remark(new)['fields']['current_progress'],'New')

    def test_legacy_all_escaped_markers_and_crlf_are_supported(self):
        value=legacy('2026-09-15','Progress').replace('_',r'\_').replace('\n','\r\n')
        self.assertEqual(read_weekly_remark(value),{'report_date':'2026-09-15','fields':{'current_progress':'Progress'}})

    def test_legacy_marker_escape_does_not_hide_damage(self):
        value=legacy('2026-09-15','Progress').replace('_',r'\_')
        with self.assertRaises(ValueError):read_weekly_remark(value[:-1])
        with self.assertRaises(ValueError):merge_weekly_remark(value[:-1],'2026-09-16',{})

    def test_same_day_revision_preserves_history_and_is_latest(self):
        first = merge_weekly_remark("原备注", "2026-09-15", {"current_progress": "初版"})
        second = merge_weekly_remark(first, "2026-09-15", {"current_progress": "修正版"})
        self.assertTrue(second.startswith(first + "\n\n"))
        self.assertEqual(read_weekly_remark(second)["fields"]["current_progress"], "修正版")
        third = merge_weekly_remark(second, "2026-09-15", {"current_progress": "初版"})
        self.assertTrue(third.startswith(second))
        self.assertEqual(read_weekly_remark(third)["fields"]["current_progress"], "初版")

    def test_legacy_history_reads_highest_date_but_writer_rejects_older_input(self):
        value=legacy('2026-09-15','New')+'\n'+legacy('2026-09-01','Old')
        self.assertEqual(read_weekly_remark(value)['fields']['current_progress'],'New')
        with self.assertRaises(ValueError):merge_weekly_remark(value,'2026-09-01',{'current_progress':'Old'})

    def test_missing_none_blank_advance_date_without_clearing_progress(self):
        old=merge_weekly_remark('manual','2026-09-10',{'current_progress':'Keep'})
        for values in ({},{'current_progress':None},{'current_progress':''}):
            result=merge_weekly_remark(old,'2026-09-15',values)
            self.assertEqual(read_weekly_remark(result),{'report_date':'2026-09-15','fields':{'current_progress':'Keep'}})
            self.assertEqual(result.count('Keep'),1)

    def test_date_only_reports_are_saved_and_idempotent(self):
        value = merge_weekly_remark("原备注", "2026-09-15", {})
        self.assertEqual(read_weekly_remark(value), {"report_date": "2026-09-15", "fields": {}})
        self.assertEqual(merge_weekly_remark(value, "2026-09-15", {}), value)

    def test_unrelated_project_fields_are_ignored(self):
        value = merge_weekly_remark(None, "2026-09-15", {"owners": ["rec1"], "project_name": "Demo"})
        self.assertEqual(read_weekly_remark(value)["fields"], {})

    def test_crlf_plain_blocks_remain_readable_and_idempotent(self):
        value=merge_weekly_remark('manual','2026-09-15',{'current_progress':'First\nSecond'}).replace('\n','\r\n')
        self.assertEqual(read_weekly_remark(value)['fields']['current_progress'],'First\nSecond')
        self.assertEqual(merge_weekly_remark(value,'2026-09-15',{'current_progress':'First\nSecond'}),value)

    def test_stage_is_separate_and_progress_line_endings_are_idempotent(self):
        value=merge_weekly_remark('','2026-09-15',{'current_progress':'A\nB','update_this_week':'Stage A'})
        self.assertEqual(merge_weekly_remark(value,'2026-09-15',{'current_progress':'A\r\nB','update_this_week':'Stage B'}),value)
        self.assertNotIn('update_this_week',read_weekly_remark(value)['fields'])

    def test_internal_whitespace_and_unicode_changes_create_revisions(self):
        value=merge_weekly_remark('','2026-09-15',{'current_progress':'A\nB'})
        for revised in ('A \nB','A\n B','A\nB😀'):
            result=merge_weekly_remark(value,'2026-09-15',{'current_progress':revised})
            self.assertNotEqual(result,value)
            self.assertEqual(read_weekly_remark(result)['fields']['current_progress'],revised)

    def test_manual_notes_around_legacy_blocks_are_preserved(self):
        value='Before\n'+legacy('2026-09-10','Old')+'\nManual note after legacy block'
        new=merge_weekly_remark(value,'2026-09-15',{'current_progress':'New'})
        self.assertTrue(new.startswith(value+'\n\n'))
        self.assertEqual(read_weekly_remark(new)['fields']['current_progress'],'New')

    def test_invalid_dates_are_rejected(self):
        for invalid in (None, "", "2026-02-30", "2026-9-15", "0000-01-01", "2026-09-15T00:00:00",
                        "20260915", "2026-09-15 ", 20260915, date(2026, 9, 15), True):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                merge_weekly_remark(None, invalid, {})

    def test_invalid_types_are_rejected_instead_of_coerced(self):
        for value in ({}, [], 3, True, b"notes"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                read_weekly_remark(value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                merge_weekly_remark(value, "2026-09-15", {})
        for values in (None, [], "text"):
            with self.subTest(values=values), self.assertRaises(ValueError):
                merge_weekly_remark(None, "2026-09-15", values)
        for value in (1, False, [], {}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                merge_weekly_remark(None, "2026-09-15", {"current_progress": value})

    def test_reserved_markers_and_nested_history_are_rejected_in_progress(self):
        for value in ('[[AUTOPM_WEEKLY_REPORT:v1]]','[[/AUTOPM_WEEKLY_REPORT]]','--- 2026-09-15 ---\nOld'):
            with self.assertRaises(ValueError):merge_weekly_remark(None,'2026-09-15',{'current_progress':value})

    def test_damaged_blocks_are_rejected_by_read_and_merge(self):
        value = legacy("2026-09-15", "进展")
        broken_values = [
            value[:-1], value[1:], value.replace(":v1", ":v2"),
            value.replace("2026-09-15", "2026-02-30"),
            value.replace("周报日期:", "日期:"),
            value.replace("[[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]", ""),
            value.replace("\n[[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]", "[[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]"),
            value.replace("[[AUTOPM_WEEKLY_REPORT:END_PROGRESS]]", "[[AUTOPM_WEEKLY_REPORT:END_UPDATE]]"),
            value + "\n[[AUTOPM_WEEKLY_REPORT:v1]]",
            value.replace("工程进展:", "未经支持的字段:"),
            "[[/AUTOPM_WEEKLY_REPORT]]", "[[AUTOPM_WEEKLY_REPORT:v1]",
        ]
        for broken in broken_values:
            with self.subTest(broken=broken), self.assertRaises(ValueError):
                read_weekly_remark(broken)
            with self.subTest(broken=broken), self.assertRaises(ValueError):
                merge_weekly_remark(broken, "2026-09-16", {})

    def test_old_damaged_legacy_block_is_not_hidden_by_new_plain_block(self):
        old=legacy('2026-09-01','Old')[:-1]
        new=merge_weekly_remark(None,'2026-09-15',{'current_progress':'New'})
        with self.assertRaises(ValueError):read_weekly_remark(old+'\n\n'+new)

    def test_size_limit_never_truncates_notes_or_history(self):
        self.assertEqual(read_weekly_remark("a" * MAX_REMARK_LENGTH)["report_date"], None)
        with self.assertRaises(ValueError):
            read_weekly_remark("a" * (MAX_REMARK_LENGTH + 1))
        with self.assertRaises(ValueError):
            merge_weekly_remark("a" * MAX_REMARK_LENGTH, "2026-09-15", {})
        with self.assertRaises(ValueError):
            merge_weekly_remark(None, "2026-09-15", {"current_progress": "a" * MAX_REMARK_LENGTH})
        with self.assertRaises(ValueError):
            read_weekly_remark("😀" * (MAX_REMARK_LENGTH // 2 + 1))

    def test_invalid_unicode_is_rejected_as_value_error(self):
        with self.assertRaises(ValueError):
            read_weekly_remark("\ud800")


if __name__ == "__main__":
    unittest.main()
