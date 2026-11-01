#!/usr/bin/env python3
"""Produce an A4 two-page student worksheet PDF; no student answer key."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
src=root/"grade8"/"unit-2"/"worksheet.html"
dst=root/"grade8"/"unit-2"/"files"/"Grade8-Unit2-Australia-CooberPedy-Worksheet.pdf"
dst.parent.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
    page=browser.new_page(viewport={"width":1280,"height":960})
    page.goto(src.as_uri(),wait_until="load",timeout=30000)
    page.emulate_media(media="print")
    page.pdf(path=str(dst),print_background=True,format="A4",margin={"top":"0","right":"0","bottom":"0","left":"0"},prefer_css_page_size=True)
    browser.close()
print(f"PDF created: {dst}, size {dst.stat().st_size} bytes")
import fitz
doc=fitz.open(dst)
assert len(doc)==2,f"Worksheet should be exactly 2 pages, got {len(doc)}"
for i,page in enumerate(doc):
    txt=page.get_text()
    assert len(txt)>700, f"Page {i+1} is empty or broken"
    assert "אוסטרליה" in txt or "Australia" in txt, f"Page {i+1} missing lesson text"
    print(f"Page {i+1} verified: {len(txt)} chars")
assert "תשובות לדוגמה" not in "".join(p.get_text() for p in doc), "Student file must not include answer key"
