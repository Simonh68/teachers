#!/usr/bin/env python3
"""One shared QR remote injected into compatible HTML slide decks; no content edits.

Use --audit to list compatible presentations, --apply to add a script tag.
Existing Sentence Detective paired remotes are never replaced or doubled.
The script is idempotent and also runs on future HTML additions via GitHub Actions.
"""
from __future__ import annotations
import argparse, json, os, re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
REMOTE=ROOT/"shared/phone-remote/remote.js"
MANIFEST=ROOT/"shared/phone-remote/rollout-manifest.json"
PREF=("grade6/","grade7/","grade8/","grade9/","grade10/","grade11/","grade12/","seminar/","to-be/","first-course/","shared/lessons/","special/","standalone/")
SKIP_BASENAMES={
 "teacher.html","teacher.en.html","teacher-guide.html","teacher-method.html",
 "guide.html","worksheet.html","key.html","answer-key.html",
 "meeting-guide.html","student-preparation.html","earlier-guide.html",
 "earlier-meetings.html","resources.html","usage-report.html"
}
NAV=re.compile(
 r"""(?:\bid\s*=\s*['"](?:next|prev|nextBtn|prevBtn|down|up|previous|forward|deck-next|deck-prev|slideNext|slidePrev)['"]|
 \bdata-step\s*=\s*['"](?:-?1)['"]|data-jump=|
 \bclass\s*=\s*['"][^'"]*\b(?:navigation|slide-nav|slideshow-controls)\b)""",
 re.I|re.X
)
SLIDE=re.compile(
 r"""(?:\bclass\s*=\s*['"][^'"]*\b(?:slide|slides|slide-card)\b|
 \b(?:const|let|var)\s+(?:slides|allSlides|steps)\s*=|
 \b(?:showSlide|renderSlide|showStep|nextSlide|moveSlide|initGrade8Bilingual)\s*\(|#slide-\d+|
 \bdocument\.querySelectorAll\(['"]\.slide)""",re.I|re.X
)
READER=re.compile(r"(?:read-along|read-alone|readalone|follow-along|track-engine\.js|segmented-engine\.js)",re.I)
BOOT=re.compile(r"(?:(?:unit-data|bootstrap|phrase-data|track-engine|reader)\.js)",re.I)
EXISTING=re.compile(r"(?:firebase-remote\.js|remote-sync\.js|id=['\"]remoteToggle['\"]|id=['\"]pairDialog['\"])",re.I)
TAG=re.compile(r"shared/phone-remote/remote\.js",re.I)

def classify(path:str, html:str):
    if not path.startswith(PREF):return "out-of-scope"
    if path.endswith(".html") is False:return "not-html"
    if Path(path).name in SKIP_BASENAMES:return "support-document"
    if "<script" not in html.lower():return "support-document"
    if TAG.search(html):return "enabled"
    if EXISTING.search(html):return "already-has-remote"
    # Canonical read-along engines rebuild the entire body, so their initial
    # HTML shell may have no visible slide or navigation elements.
    if "location.replace(" in html and len(html)<1800:return "redirect"
    has_nav=bool(NAV.search(html)) or bool(re.search(r'id=["\\\'](?:v-next|v-prev)["\\\']',html,re.I))
    has_slide=bool(SLIDE.search(html))
    has_stage=bool(re.search(r'id=["\\\'](?:stage|deck|slide|main)["\\\']',html,re.I))
    has_count=bool(re.search(r'id=["\\\'](?:counter|position|v-position|slideCount)["\\\']',html,re.I))
    has_engine=bool(re.search(r'(?:lesson|app|sequence|bootstrap8?|track-engine|segmented-engine)\\.js',html,re.I))
    has_next=bool(re.search(r'\\bfunction\\s+(?:next|prev|move|advance)\\s*\\(',html))
    has_reader=bool(READER.search(path)) or bool(re.search(r'READ[ -]?ALON?G?|Read\\s+Along|Read\\s+Alone',html,re.I))
    is_readalong=has_reader and (has_engine or has_nav) and (has_stage or bool(BOOT.search(html)) or "read-along" in path)
    if is_readalong:return "compatible"
    if has_nav and (has_slide or has_stage or (has_count and has_engine)):return "compatible"
    if has_stage and has_count and (has_engine or has_next):return "compatible"
    if path.startswith("seminar/") and has_next and "showStep" in html:return "compatible"
    return "support-document"

def run(apply=False):
    enabled=[];compatible=[];existing=[];excluded=[];edited=[]
    for file in sorted(ROOT.rglob("*.html")):
        path=file.relative_to(ROOT).as_posix()
        if not path.startswith(PREF):continue
        if ".git/" in path or "/node_modules/" in path:continue
        txt=file.read_text(encoding="utf-8")
        verdict=classify(path,txt)
        if verdict=="enabled":enabled.append(path)
        elif verdict=="already-has-remote":existing.append(path)
        elif verdict=="compatible":
            compatible.append(path)
            if apply:
                rel=os.path.relpath(REMOTE,file.parent).replace(os.sep,"/")
                tag=f'<!-- Teachers QR remote · shared · auto-attached -->\n<script defer src="{rel}?v=20261101-1"></script>\n'
                result,count=re.subn(r"</body\s*>",lambda match:tag+match.group(),txt,count=1,flags=re.I)
                if count!=1:
                    # Two older, valid legacy decks use an implicit <body> and
                    # end with </script></html>. Append before </html> safely.
                    result,count=re.subn(r"</html\s*>",lambda match:tag+match.group(),txt,count=1,flags=re.I)
                    if count!=1:
                        excluded.append({"path":path,"reason":"no closing body/html"})
                        continue
                file.write_text(result,encoding="utf-8")
                edited.append(path)
        else:excluded.append({"path":path,"reason":verdict})
    items=sorted(set(enabled)|set(existing)|set(edited))
    # In audit-only, compatible files are reported but not considered installed.
    manifest={
      "name":"Teachers presentation QR phone remote",
      "version":"2026-11-01",
      "central_runtime":"shared/phone-remote/remote.js",
      "enabled_shared":sorted(set(enabled+edited)),
      "existing_custom_remotes":sorted(existing),
      "pending":sorted(set(compatible)-set(edited)),
      "support_documents_excluded":len(excluded),
      "counts":{"enabled":len(enabled+edited),"custom_existing":len(existing),"pending":len(set(compatible)-set(edited))},
      "rollout_paths":items
    }
    if apply:MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in manifest.items() if k not in ("enabled_shared","existing_custom_remotes","pending","rollout_paths")} | {"newly_updated":len(edited),"sample":edited[:24],"pending_sample":manifest["pending"][:20],"existing_custom":existing},ensure_ascii=False,indent=2))
    if apply and manifest["pending"]:raise SystemExit("Could not patch all compatible HTML files")
    return manifest

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--apply",action="store_true")
    options=ap.parse_args()
    run(apply=options.apply)
