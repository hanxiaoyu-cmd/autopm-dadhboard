from copy import deepcopy
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from autopm.deepseek import DeepSeekClient, DeepSeekError, validate_model_project
from autopm.normalize import parse_date
from autopm.workbook import parse_local, read_workbook, WorkbookError
from benchmarks.run import facts, score, summarize, lower_bound
from tests.test_deepseek import evidence_fixture, valid_output, response
from tests.test_workbook import fixture_workbook


class ResilienceTests(unittest.TestCase):
    def test_key_issues_tasks_variant_preserves_issue_in_both_extractors(self):
        for label in ("Key Issues / Tasks","KEY ISSUES & TASKS","Key Issues and Tasks"):
            ev=evidence_fixture()
            next(c for c in ev["projects"][0]["cells"] if c["address"]=="B13")["text"]=label
            with self.subTest(label=label):
                self.assertEqual(parse_local(ev)["projects"][0]["issues"][0]["text"],"Trim issue")
                self.assertEqual(validate_model_project(valid_output(),ev["projects"][0])["issues"][0]["text"],"Trim issue")

    def test_single_typo_heading_recovery_does_not_guess_ambiguous_roles(self):
        from autopm.workbook import field_key
        self.assertEqual(field_key("Stauts"),"status")
        self.assertEqual(field_key("CAPACIT"),"capacity")
        self.assertEqual(field_key("NPD Lead"),"npd_lead")
        self.assertIsNone(field_key("NP Lead"))
        self.assertIsNone(field_key("Project Number"))
        self.assertIsNone(field_key("Update on"))
        report=parse_local(evidence_fixture())
        self.assertEqual(report["projects"][0]["fields"]["status"],"On Track")

    def test_fault_matrix_every_critical_family(self):
        from benchmarks.faults import run
        result=run()
        for family,rows in result["families"].items():
            for row in rows:
                with self.subTest(family=family,case=row["case"]):
                    self.assertTrue(row["passed"],row["error"])

    def test_numeric_date_order_and_year_boundary(self):
        self.assertIsNone(parse_date("03/04/2026"))
        self.assertEqual(parse_date("03/04/2026",date_order="DMY"),"2026-04-03")
        self.assertEqual(parse_date("03/04/2026",date_order="MDY"),"2026-03-04")
        self.assertIsNone(parse_date("Jan 15","2026-12-20"))
        self.assertEqual(parse_date("2027-01-15","2026-12-20"),"2027-01-15")
        self.assertEqual(parse_date("2026-09-03T12:30:00+08:00"),"2026-09-03")
        with self.assertRaises(ValueError): parse_date("2026-09-03",date_order="BAD")

    def test_formula_value_does_not_shift_metadata_pair(self):
        ev=evidence_fixture();block=ev["projects"][0]
        next(c for c in block["cells"] if c["address"]=="D2")["formula"]='"AF800"'
        block["cells"].append({"ref":"'Report'!F2","address":"F2","row":2,"col":6,"text":"Wrong name","fill":{}})
        self.assertNotIn("project_name",parse_local(ev)["projects"][0]["fields"])
        out=valid_output()
        out["fields"]["project_name"]={"value":"Wrong name","evidence":["'Report'!B2","'Report'!F2"]}
        with self.assertRaises(DeepSeekError): validate_model_project(out,block)

    def test_invalid_existing_report_date_cannot_use_supplement(self):
        from zipfile import ZipFile
        for replacement in ('<f>TODAY()</f><v>46268</v>', '<v>46268</v>'):
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as d:
                source=Path(d)/"source.xlsx";mutated=Path(d)/"mutated.xlsx"
                fixture_workbook(source)
                with ZipFile(source) as src,ZipFile(mutated,"w") as dst:
                    for info in src.infolist():
                        data=src.read(info.filename)
                        if info.filename=="xl/worksheets/sheet1.xml":
                            xml=data.decode()
                            if replacement.startswith("<f>"):
                                xml=xml.replace('<c r="R1" s="1"><v>46268</v></c>', '<c r="R1" s="1">'+replacement+'</c>')
                            else:
                                xml=xml.replace('<c r="R1" s="1"><v>46268</v></c>', '<c r="R1" t="inlineStr"><is><t>03/04/2026</t></is></c>')
                            data=xml.encode()
                        dst.writestr(info,data)
                with self.assertRaisesRegex(WorkbookError,"无法确定"):
                    read_workbook(mutated,report_date="2026-09-03")

    def test_duplicate_model_items_repair_does_not_bypass_deduplication(self):
        out=valid_output();out["tasks"]*=3;out["issues"]*=2
        with patch.object(DeepSeekClient,"_request",return_value=response(out)):
            report=DeepSeekClient("key",workers=1).parse(evidence_fixture())
        self.assertEqual(len(report["projects"][0]["tasks"]),3)
        self.assertEqual(len(report["projects"][0]["issues"]),1)
        self.assertEqual(report["extraction_stats"]["rejected_model_items"],3)

    def test_metric_counts_missing_and_duplicate_facts(self):
        expected={"project_id":"X","fields":{"status":"On Track"},"tasks":[],"issues":[]}
        self.assertEqual(score(facts({"project_id":"X"}),facts(expected))["fn"],1)
        self.assertFalse(score(facts({}),facts(expected))["exact"])
        self.assertLess(lower_bound(12,12),.99)
        out=valid_output();base=facts(out,raw=True);out["tasks"]*=2
        self.assertGreater(score(facts(out,raw=True),base)["fp"],0)

    def test_metrics_include_repairs_and_no_key(self):
        invalid=valid_output();invalid["fields"]["status"]["evidence"]=[]
        with patch.object(DeepSeekClient,"_request",side_effect=[response(invalid),response()]):
            report=DeepSeekClient("do-not-log-this",workers=1).parse(evidence_fixture())
        metric=report["project_metrics"][0]
        self.assertEqual(metric["requests"],2)
        self.assertTrue(metric["repaired"])
        self.assertFalse(metric["first_pass"])
        self.assertNotIn("do-not-log-this",json.dumps(report))

    def test_optional_usage_metadata_never_breaks_valid_extraction(self):
        for usage in (None,"unexpected",[1],{"prompt_tokens":None,"completion_tokens":"42"}):
            with self.subTest(usage=usage):
                r=response();r["usage"]=usage
                with patch.object(DeepSeekClient,"_request",return_value=r):
                    report=DeepSeekClient("key",workers=1).parse(evidence_fixture())
                self.assertEqual(report["projects"][0]["fields"]["status"],"On Track")

    def test_non_object_api_response_fails_with_controlled_error(self):
        for value in (None,[],"bad"):
            with self.subTest(value=value),patch.object(DeepSeekClient,"_request",return_value=value):
                with self.assertRaises(DeepSeekError): DeepSeekClient("key",workers=1).parse(evidence_fixture())

    def test_wrong_returned_model_is_blocked_before_extraction(self):
        import httpx
        r=response();r["model"]="another-model"
        client=DeepSeekClient("key",workers=1)
        client._http_client=httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,json=r)))
        with self.assertRaisesRegex(DeepSeekError,"模型.*不一致"):
            client.parse(evidence_fixture())

    def test_retry_after_is_bounded_and_respected(self):
        import httpx
        calls=[]
        def handler(_):
            calls.append(1)
            return httpx.Response(429,headers={"Retry-After":"12"}) if len(calls)==1 else httpx.Response(200,json=response())
        client=DeepSeekClient("key",workers=1)
        client._http_client=httpx.Client(transport=httpx.MockTransport(handler))
        with patch("autopm.deepseek.time.sleep") as sleep:
            client.parse(evidence_fixture())
        sleep.assert_called_once_with(12)
        self.assertEqual(client.transport_attempts,2)

    def test_model_date_policy_matches_local_policy(self):
        ev=evidence_fixture();block=ev["projects"][0]
        next(c for c in block["cells"] if c["address"]=="B7")["text"]="05/12/2026"
        with self.assertRaises(DeepSeekError): validate_model_project(valid_output(),block)
        block["date_order"]="MDY"
        self.assertEqual(validate_model_project(valid_output(),block)["tasks"][0]["date"],"2026-05-12")

    def test_prompt_profiles_invalidate_cache(self):
        ev=evidence_fixture()
        with tempfile.TemporaryDirectory() as d:
            for hint in (False,True):
                with patch.object(DeepSeekClient,"_request",return_value=response()) as request:
                    DeepSeekClient("key",workers=1,cache_dir=d,source_hints=hint).parse(ev)
                    self.assertEqual(request.call_count,1)


if __name__=="__main__":
    unittest.main()
