#!/usr/bin/env python3
"""Staging-only migration audit. Never deploys or modifies production."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,sys,urllib.parse
root=Path(__file__).resolve().parents[1]
class A(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.inside=False;self.depth=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=="div" and d.get("id")=="grade8":self.inside=True;self.depth=1;return
  if self.inside:
   if tag=="div":self.depth+=1
   if tag=="a" and "href" in d:self.links.append(d["href"])
 def handle_endtag(self,tag):
  if self.inside and tag=="div":
   self.depth-=1
   if self.depth==0:self.inside=False
def main():
 total=0;failed=[]
 for grade in range(7,13):
  file=root/f"architecture/staging/grade{grade}.json"
  obj=json.loads(file.read_text(encoding="utf-8"))
  if obj.get("grade")!=grade or obj.get("schemaVersion")!=1:failed.append(str(file)+": invalid grade/schema")
  ids=set()
  for item in obj.get("materials",[]):
   total+=1
   if item.get("id") in ids:failed.append(f"duplicate id in grade {grade}")
   ids.add(item.get("id"))
   url=item.get("url","")
   parsed=urllib.parse.urlsplit(url)
   if parsed.scheme and parsed.scheme!="https":failed.append(f"non-HTTPS external link: {url}")
   if not parsed.scheme:
    path=urllib.parse.unquote(parsed.path)
    if path.startswith("/") or ".." in Path(path).parts:failed.append(f"unsafe path: {url}")
    elif not (root/path).is_file() and not (root/path/"index.html").is_file():failed.append(f"missing: {url}")
 print(f"Staged items: {total}; failures: {len(failed)}")
 for issue in failed:print("FAIL:",issue)
 if failed:sys.exit(1)
if __name__=="__main__":main()
