#!/usr/bin/env python3
"""Validate grade manifests and assemble static data without touching main."""
import json, pathlib, re, sys, shutil, urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"_site"
def fail(msg): raise SystemExit("ERROR: "+msg)
def validate(grade, data):
    if data.get("schemaVersion")!=1 or data.get("grade")!=grade: fail(f"grade {grade}: schema/version mismatch")
    items=data.get("materials")
    if not isinstance(items,list): fail(f"grade {grade}: materials must be an array")
    ids=set()
    for m in items:
        if not isinstance(m,dict) or not all(isinstance(m.get(k),str) and m[k] for k in ("id","title","url","unit")): fail(f"grade {grade}: invalid item")
        if not re.fullmatch(r"[a-z0-9-]+",m["id"]) or m["id"] in ids: fail(f"grade {grade}: duplicate or invalid ID")
        ids.add(m["id"])
        for field in ("url","worksheet"):
            if field not in m: continue
            url=m[field]
            if not isinstance(url,str) or url.startswith(("/", "//")) or urllib.parse.urlsplit(url).scheme not in ("","https"): fail(f"grade {grade}: unsafe URL {url}")
            if not urllib.parse.urlsplit(url).scheme:
                path=urllib.parse.unquote(urllib.parse.urlsplit(url).path)
                if ".." in pathlib.PurePosixPath(path).parts: fail("path traversal")
                if not (ROOT/path).is_file() and not (ROOT/path/"index.html").is_file(): fail(f"missing linked file: {url}")
    return items
def main():
    manifests={}
    for grade in range(7,13):
        p=ROOT/f"grade{grade}"/"manifest.json"
        if not p.exists(): fail(f"missing manifest {p}")
        manifests[f"grade{grade}"]=validate(grade,json.loads(p.read_text(encoding="utf-8")))
    OUT.mkdir(exist_ok=True)
    data=OUT/"data";data.mkdir(exist_ok=True)
    for grade,items in manifests.items():
        (data/f"{grade}.json").write_text(json.dumps({"schemaVersion":1,"grade":int(grade[5:]),"materials":items},ensure_ascii=False,indent=2),encoding="utf-8")
    print("Validated 6 classroom manifests; generated public data.")
if __name__=="__main__": main()
