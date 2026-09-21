"""Deterministic fault matrix. Counts are generated scenarios, not real-world prevalence."""
from collections import defaultdict
from copy import deepcopy
from datetime import date
import argparse
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

from autopm.deepseek import DeepSeekClient, DeepSeekError, validate_model_project
from autopm.normalize import normalize_header, normalize_project_id, parse_date
from autopm.workbook import parse_local
from autopm.sync import build_plan, apply_plan
from tests.test_deepseek import evidence_fixture, valid_output, response
from tests.test_sync import fixture, FakeClient


def rejected(fn):
    try:
        fn()
    except (DeepSeekError, ValueError):
        return True
    return False


def scenarios():
    # Related permutations are reported together so date/spacing counts cannot
    # hide a failure in identity, association, or remote-write guard families.
    spaces=[" ","  ","\t","\n","\r\n","\u00a0","\u200b","\u200c","\u200d","\ufeff","\u3000","\u202f"]
    for name in ("Key Issues / Tasks","KEY ISSUES & TASKS","Key Issues and Tasks","Key Issues"):
        ev=evidence_fixture();next(c for c in ev["projects"][0]["cells"] if c["address"]=="B13")["text"]=name
        yield "issue_heading_variants",name,lambda e=ev: len(parse_local(e)["projects"][0]["issues"])==1 and len(validate_model_project(valid_output(),e["projects"][0])["issues"])==1
    for word in ("Project Number","Current Progress","NPI Lead","NPD Lead","Eng Update This Week","MP Start"):
        for s in spaces:
            v=s+word.swapcase().replace(" ",s)+s
            yield "header_format",repr(v),lambda v=v,w=word: normalize_header(v)==normalize_header(w)
    for pid in ("AB-123","AB123","AB/123","AB.123","AB_123"):
        for s in spaces:
            v=s+s.join(pid.lower())+s
            yield "identity_format",repr(v),lambda v=v,pid=pid: normalize_project_id(v)==pid
    for a in range(1,13):
        for b in range(1,13):
            if a!=b:
                value=f"{a:02}/{b:02}/2026"
                yield "ambiguous_dates",value,lambda v=value: parse_date(v) is None
    for order in ("MDY","DMY"):
        for a in range(1,13):
            value=f"{a}/13/2026" if order=="MDY" else f"13/{a}/2026"
            expected=date(2026,a,13).isoformat()
            yield "explicit_date_order",order+value,lambda v=value,o=order,e=expected: parse_date(v,date_order=o)==e
    for value in ("2026-02-29","2026-04-31","2026-00-03","2026-13-03","2026-09-03Tgarbage","2026-09-03T2027-01-01","9/31/2026","2026-09-01 -> 2026-10-01","09/10/26","NaN",45555,True):
        yield "invalid_dates",str(value),lambda v=value: parse_date(v) is None
    for month in (1,2,3):
        for day in (13,20,28):
            value=f"{month}/{day}"
            yield "year_boundary",value,lambda v=value: parse_date(v,"2026-12-20",date_order="MDY") is None
    for key in ("project_name","status","npi_lead","npd_lead","pmo","capacity","factory"):
        ev=evidence_fixture();out=valid_output()
        out["fields"][key]={"value":"Invented","evidence":["'Report'!D2"]}
        yield "fabricated_values",key,lambda o=out,e=ev: rejected(lambda:validate_model_project(o,e["projects"][0]))
    for value in ("ADMIN","NXA0006","",None,False,123,"NXA-0005"):
        out=valid_output();out["project_id"]=value
        yield "model_identity",str(value),lambda o=out: rejected(lambda:validate_model_project(o,evidence_fixture()["projects"][0]))
    for key in ("airtable_record_id","api_key","table_id","delete","completed_by"):
        out=valid_output();out["fields"][key]={"value":"recInjected","evidence":["'Report'!D2"]}
        yield "target_allowlist",key,lambda o=out: rejected(lambda:validate_model_project(o,evidence_fixture()["projects"][0]))
    for ref in ("'Report'!D27","'Other'!D2","'Report'!L10","'Report'!F23","recAttack",""):
        out=valid_output();out["fields"]["status"]["evidence"]=[ref]
        yield "cross_project_excluded_refs",ref,lambda o=out: rejected(lambda:validate_model_project(o,evidence_fixture()["projects"][0]))
    for key in ("npi_lead","npd_lead","pmo"):
        out=valid_output();out["fields"]={key:{"value":"AF800","evidence":["'Report'!B2","'Report'!D2"]}}
        yield "role_semantics",key,lambda o=out: rejected(lambda:validate_model_project(o,evidence_fixture()["projects"][0]))
    for group in ("tasks","issues"):
        for count in (2,3,8):
            out=valid_output();out[group]*=count
            yield "duplicate_model_items",group+str(count),lambda o=out: rejected(lambda:validate_model_project(o,evidence_fixture()["projects"][0]))
    for key in ("formula","kind","display_hidden"):
        ev=evidence_fixture();cell=next(c for c in ev["projects"][0]["cells"] if c["address"]=="B7")
        cell[key]={"formula":"TODAY()","kind":"error","display_hidden":True}[key]
        yield "ineligible_date_sources",key,lambda e=ev: not any(t["name"]=="Award" for t in parse_local(e)["projects"][0]["tasks"])
    for value in ("{",'{"project_id":"NXA0005","project_id":"ADMIN"}',"NaN","Infinity","-Infinity",'```json\n{}\n```',""):
        r={"choices":[{"finish_reason":"stop","message":{"content":value}}]}
        # A non-object NaN/Infinity is also invalid JSON for our contract.
        yield "malformed_json",value,lambda r=r: rejected(lambda:DeepSeekClient._response_output(r))
    for finish in ("length","content_filter","tool_calls",None):
        yield "truncated_output",str(finish),lambda f=finish: rejected(lambda:DeepSeekClient._response_output(response(finish=f)))
    for failure in ("identity","duplicate","newer_date","concurrent_field","schema"):
        def check(f=failure):
            snapshot,report=fixture();plan=build_plan(report,snapshot);client=FakeClient(snapshot)
            project=client.data["records"]["tbl_projects"][0]
            if f=="identity": project["fields"]["fld_projects_project_id"]="OTHER"
            elif f=="duplicate": client.data["records"]["tbl_projects"].append(deepcopy(project))
            elif f=="newer_date": project["fields"]["fld_projects_report_date"]="2026-10-01"
            elif f=="concurrent_field": project["fields"]["fld_projects_project_name"]="Someone else's edit"
            else: client.data["schema"]["tables"][0]["fields"]=[x for x in client.data["schema"]["tables"][0]["fields"] if x["id"]!="fld_projects_project_name"]
            with tempfile.TemporaryDirectory() as d:
                result=apply_plan(client,plan,d)
            return result["status"]=="blocked" and not client.writes
        yield "write_preflight",failure,check
    for sentinel in ("Network unavailable","Authentication denied","Quota unavailable"):
        def check(s=sentinel):
            with patch.object(DeepSeekClient,"_request",side_effect=DeepSeekError(s)) as request:
                return rejected(lambda:DeepSeekClient("test-key",workers=1).parse(evidence_fixture())) and request.call_count==1
        yield "failed_api_no_write_preview",sentinel,check


def run():
    families=defaultdict(list)
    for family,name,fn in scenarios():
        try:
            ok=bool(fn());error=None if ok else "Expected safety contract not met"
        except Exception as exc:
            ok=False;error=f"{type(exc).__name__}: {exc}"
        families[family].append({"case":name,"passed":ok,"error":error})
    count=sum(map(len,families.values()))
    passed=sum(r["passed"] for rows in families.values() for r in rows)
    macro=sum(all(r["passed"] for r in rows) for rows in families.values())/len(families)
    return {"scenario_count":count,"passed":passed,"scenario_pass_rate":passed/count,"families":dict(families),
        "family_count":len(families),"all_pass_family_rate":macro,"gate":passed/count>=.99 and macro==1,
        "scope":"Generated deterministic scenarios, not random real-world incident samples. Every critical family must fully pass."}


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);args=p.parse_args()
    result=run();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="families"},ensure_ascii=False,indent=2))
    if not result["gate"]:
        raise SystemExit(1)
