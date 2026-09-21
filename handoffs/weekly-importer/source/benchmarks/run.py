"""Run frozen corpus against real DeepSeek, with no response cache or Airtable.

python -m benchmarks.run --profile both --repeats 3 --output outputs/benchmark/run-id
Each execution is a new experiment. Existing results are never silently reused.
"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import time

from autopm.config import load_settings, redact
from autopm.deepseek import DeepSeekClient, DeepSeekError, SYSTEM_PROMPT, validate_model_project
from autopm.normalize import clean_text

HERE = Path(__file__).parent


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def facts(project, raw=False):
    """Multiset of business facts; ignores evidence/order, never ignores duplicates.

    One fact per field and per nonempty task/issue attribute. Missing values are
    false negatives; fabricated or repeated values are false positives.
    """
    result = []
    def add(*parts):
        result.append(json.dumps(parts,ensure_ascii=False,sort_keys=True))
    if not isinstance(project, dict):
        return Counter()
    add("project_id", project.get("project_id"))
    fields = project.get("fields", {})
    if isinstance(fields,dict):
        for key,value in fields.items():
            if raw and isinstance(value,dict):
                value = value.get("value")
            if value is not None and value != "":
                add("field",key,clean_text(value) if isinstance(value,str) else value)
    for group, identity, keys in (("tasks","name",("date","completed")),("issues","text",("action","risk","owner","due_date"))):
        items = project.get(group, [])
        if not isinstance(items,list):
            continue
        for item in items:
            if not isinstance(item,dict):
                add(group,"invalid-item",item)
                continue
            name = clean_text(item.get(identity))
            add(group,name,"identity")
            for key in keys:
                value = item.get(key)
                if value is not None and value != "":
                    add(group,name,key,clean_text(value) if isinstance(value,str) else value)
    return Counter(result)


def score(actual, expected):
    tp = sum((actual & expected).values())
    fp, fn = sum((actual-expected).values()), sum((expected-actual).values())
    return {"tp":tp,"fp":fp,"fn":fn,"precision":tp/(tp+fp) if tp+fp else None,
            "recall":tp/(tp+fn) if tp+fn else None,"exact":fp==fn==0}


def lower_bound(successes, total):
    # One-sided 95% Wilson bound; repeated same-case runs are correlated.
    if not total:
        return None
    z=1.6448536269514722
    p=successes/total
    return (p+z*z/(2*total)-z*math.sqrt(p*(1-p)/total+z*z/(4*total*total)))/(1+z*z/total)


def percentile(values, q):
    return sorted(values)[max(0, math.ceil(q*len(values))-1)] if values else None


def execute(case, profile, repeat, output, config):
    target=output / f"{profile}-{case['id']}-{repeat}.json"
    calls=[]
    class Measured(DeepSeekClient):
        def _request(self,payload):
            t=time.monotonic()
            before=self.transport_attempts
            entry={"request_hash":digest(payload),"requested_model":payload["model"]}
            try:
                response=super()._request(payload)
                entry.update(response=response,returned_model=response.get("model"),usage=response.get("usage",{}))
                return response
            except DeepSeekError as exc:
                entry["error"]=str(exc)
                raise
            finally:
                entry.update(seconds=round(time.monotonic()-t,4),http_attempts=self.transport_attempts-before)
                calls.append(entry)
    baseline=(HERE / "baseline-prompt.txt").read_text(encoding="utf-8")
    client=Measured(config["deepseek_api_key"],base_url=config["deepseek_base_url"],model="deepseek-v4-flash",
        workers=1,cache_dir=None,system_prompt=baseline if profile=="baseline" else SYSTEM_PROMPT,
        source_hints=profile!="baseline")
    start=time.monotonic()
    record={"case":case["id"],"category":case["category"],"profile":profile,"repeat":repeat,"calls":calls,
            "first_pass":False,"success":False,"local_cache":False}
    expected=facts(case["gold"])
    first={}
    try:
        report=client.parse(deepcopy(case["evidence"]))
        record.update(success=True,report=report)
    except Exception as exc:
        record["error"]=redact(exc,config)
    finally:
        client.close()
    if calls and calls[0].get("response"):
        try:
            first=client._response_output(calls[0]["response"])
            validated=validate_model_project(first,case["evidence"]["projects"][0])
            record["first_pass"]=any(validated[k] for k in ("fields","tasks","issues"))
        except (DeepSeekError, ValueError, TypeError) as exc:
            record["first_error"]=str(exc)
    final=facts(record["report"]["projects"][0]) if record["success"] else Counter()
    record.update(seconds=round(time.monotonic()-start,4),first_score=score(facts(first,raw=True) if first else Counter(),expected),
        final_score=score(final,expected),final_hash=digest(sorted(final.items())) if record["success"] else None,
        raw_hash=digest(sorted(facts(first,raw=True).items())) if first else None,
        missing_facts=list((expected-final).elements()),extra_facts=list((final-expected).elements()))
    target.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
    print(profile,case["id"],repeat,"first",record["first_pass"],"final",record["final_score"]["exact"],"calls",len(calls),flush=True)
    return record


def summarize(records):
    result={}
    for profile in sorted({r["profile"] for r in records}):
        rows=[r for r in records if r["profile"]==profile]
        n=len(rows)
        cases=defaultdict(list)
        for row in rows:
            cases[row["case"]].append(row)
        stats={"runs":n,"unique_cases":len(cases),"successful_runs":sum(r["success"] for r in rows),
            "first_pass_runs":sum(r["first_pass"] for r in rows),"repair_runs":sum(len(r["calls"])>1 for r in rows),
            "exact_final_runs":sum(r["final_score"]["exact"] for r in rows),
            "model_calls":sum(len(r["calls"]) for r in rows),"http_attempts":sum(c["http_attempts"] for r in rows for c in r["calls"]),
            "p50_seconds":statistics.median(r["seconds"] for r in rows),"p95_seconds":percentile([r["seconds"] for r in rows],.95),
            "prompt_tokens":sum((c.get("usage") or {}).get("prompt_tokens",0) for r in rows for c in r["calls"]),
            "completion_tokens":sum((c.get("usage") or {}).get("completion_tokens",0) for r in rows for c in r["calls"]),
            "rejected_items":sum(r.get("report",{}).get("extraction_stats",{}).get("rejected_model_items",0) for r in rows),
            "wrong_model_responses":sum(c.get("returned_model") not in (None,"deepseek-v4-flash") for r in rows for c in r["calls"])}
        for stage in ("first","final"):
            totals={k:sum(r[f"{stage}_score"][k] for r in rows) for k in ("tp","fp","fn")}
            tp,fp,fn=(totals[k] for k in ("tp","fp","fn"))
            stats[stage]={**totals,"precision":tp/(tp+fp) if tp+fp else None,"recall":tp/(tp+fn) if tp+fn else None}
        repeatable=[rs for rs in cases.values() if len(rs)>1]
        stats["repeated_cases"]=len(repeatable)
        for name in ("raw_hash","final_hash"):
            stats[name+"_consistent_cases"]=sum(all(r[name] for r in rs) and len({r[name] for r in rs})==1 for rs in repeatable)
        all_exact_cases=sum(all(r["final_score"]["exact"] for r in rs) for rs in cases.values())
        stats["all_exact_cases"]=all_exact_cases
        stats["case_wilson_lower_95"]=lower_bound(all_exact_cases,len(cases))
        # Candidate release gates. Confidence support is reported separately.
        stats["gates"]={"final_precision_100":stats["final"]["fp"]==0,
            "final_recall_99":(stats["final"]["recall"] or 0)>=.99,"first_pass_95":stats["first_pass_runs"]/n>=.95,
            "all_runs_success":stats["successful_runs"]==n,"stable_final":bool(repeatable) and stats["final_hash_consistent_cases"]==len(repeatable),
            "correct_model":stats["wrong_model_responses"]==0}
        result[profile]=stats
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile",choices=("baseline","candidate","both"),default="both")
    parser.add_argument("--repeats",type=int,default=3)
    parser.add_argument("--workers",type=int,default=4)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--corpus",type=Path,default=HERE/"corpus-v1.json")
    args=parser.parse_args()
    if not 1<=args.repeats<=20 or not 1<=args.workers<=4:
        parser.error("repeats 1..20 and workers 1..4 required")
    args.output.mkdir(parents=True,exist_ok=True)
    if any(args.output.glob("*-*-*.json")) or (args.output/"manifest.json").exists():
        parser.error("Output contains a prior run; choose a new directory.")
    config=load_settings()
    if not config.get("deepseek_api_key"):
        parser.error("Save DeepSeek credentials in the app or set DEEPSEEK_API_KEY.")
    corpus_path=args.corpus
    corpus=json.loads(corpus_path.read_text(encoding="utf-8"))
    profiles=("baseline","candidate") if args.profile=="both" else (args.profile,)
    manifest={"started_at":datetime.now(timezone.utc).isoformat(),"model":"deepseek-v4-flash","repeats":args.repeats,
        "profiles":profiles,"unique_cases":len(corpus["cases"]),"corpus_sha256":hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
        "candidate_prompt_sha256":hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "baseline_prompt_sha256":hashlib.sha256((HERE/"baseline-prompt.txt").read_bytes()).hexdigest(),
        "code_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.parent/"autopm").glob("*.py")},
        "local_cache":False,"airtable_writes":0,"note":"Paired old prompt vs candidate prompt+coordinate map, BOTH use current hardened validator. Repeated cases are correlated; no claim of 99% population coverage."}
    (args.output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    records=[]
    # Interleave profiles and repeats to reduce timing/order confounds.
    jobs=[(c,p,r) for r in range(1,args.repeats+1) for c in corpus["cases"] for p in profiles]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(execute,c,p,r,args.output,config) for c,p,r in jobs]
        for future in as_completed(futures):
            records.append(future.result())
            (args.output/"summary.json").write_text(json.dumps(summarize(records),ensure_ascii=False,indent=2),encoding="utf-8")
    summary=summarize(records)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if "candidate" in summary and not all(summary["candidate"]["gates"].values()):
        raise SystemExit(2)


if __name__=="__main__":
    main()
