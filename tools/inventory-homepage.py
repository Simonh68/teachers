#!/usr/bin/env python3
"""Inventory public homepage links per grade without changing the site."""
from html.parser import HTMLParser
from pathlib import Path
import json, urllib.parse
ROOT=Path(__file__).resolve().parents[1]
class Inventory(HTMLParser):
    def __init__(self):
        super().__init__(); self.grade=None; self.depth=0; self.items={f"grade{i}":[] for i in range(7,13)}
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="div" and d.get("id") in self.items:
            self.grade=d["id"];self.depth=1;return
        if self.grade:
            if tag=="div": self.depth+=1
            if tag=="a" and d.get("href"):
                self.items[self.grade].append(d["href"])
    def handle_endtag(self,tag):
        if self.grade and tag=="div":
            self.depth-=1
            if self.depth==0:self.grade=None
def main():
    parser=Inventory();parser.feed((ROOT/"index.html").read_text(encoding="utf-8"))
    report={}
    for grade,links in parser.items.items():
        unique=list(dict.fromkeys(links))
        missing=[]
        for href in unique:
            u=urllib.parse.urlsplit(href)
            if u.scheme or href.startswith("#"):continue
            p=ROOT/urllib.parse.unquote(u.path)
            if not p.is_file() and not (p/"index.html").is_file():missing.append(href)
        report[grade]={"total_links":len(links),"unique_links":len(unique),"missing_local_paths":missing,"links":unique}
    dest=ROOT/"architecture"/"homepage-inventory.json"
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    for grade,entry in report.items():print(grade,entry["unique_links"],"unique links;",len(entry["missing_local_paths"]),"missing")
if __name__=="__main__":main()
