#!/usr/bin/env python3
"""Grade 8 Unit 2: actual public browser smoke of all lesson assets."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE="https://simonh68.github.io/teachers/grade8/unit-2/"
EXPECTED=[
 ("grade8 homepage","https://simonh68.github.io/teachers/#grade8","grade8-unit2-lesson"),
 ("grade8 library","https://simonh68.github.io/teachers/grade8/","unit-2-lesson"),
 ("unit 2","https://simonh68.github.io/teachers/grade8/unit-2/","lesson")
]
def log(msg):print(msg,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
    try:
        ctx=browser.new_context(viewport={"width":1440,"height":900},locale="he-IL")
        page=ctx.new_page()
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        for name,url,selector in EXPECTED:
            resp=page.goto(url,wait_until="domcontentloaded",timeout=30000)
            assert resp and resp.status==200,(name,"HTTP")
            assert page.locator("#"+selector).count()==1 or (name=="unit 2" and page.locator('a[href="lesson/"]').count()>0),(name,"missing entry")
            log("LINK PASS "+name)
        resp=page.goto(BASE+"lesson/",wait_until="domcontentloaded",timeout=30000)
        assert resp and resp.status==200,"lesson not public"
        page.wait_for_function("typeof S !== 'undefined' && S.length > 30 && document.querySelector('#stage')?.textContent.length>40",timeout=20000)
        count=page.evaluate("S.length")
        log("LESSON slides "+str(count))
        assert 36<=count<=52
        # Validate teacher links, word reveals and non-first correct positions
        idx=page.evaluate("S.findIndex(s=>s.type==='vocab')")
        page.evaluate("(i)=>go(i)",idx)
        assert page.locator(".vocab").count()==3
        page.locator('[data-vocab="0"]').click()
        assert "חצי הכדור" in page.locator(".vocab .translation").first.inner_text()
        log("VOCAB REVEAL PASS")
        idx=page.evaluate("S.findIndex(s=>s.type==='quiz')")
        page.evaluate("(i)=>go(i)",idx)
        page.locator('[data-choice="1"]').click()
        assert "נכון" in page.locator(".feedback").inner_text(),"answer choice B not accepted"
        log("QUESTION PASS: correct answer not always first")
        idx=page.evaluate("S.findIndex(s=>s.type==='grammar')")
        page.evaluate("(i)=>go(i)",idx)
        assert page.locator(".chunk.subject").count()==1 and page.locator(".chunk.verb").count()==1 and page.locator(".chunk.place").count()==1
        log("GRAMMAR STRUCTURE PASS")
        idx=page.evaluate("S.findIndex(s=>s.type==='map')")
        page.evaluate("(i)=>go(i)",idx)
        page.locator("img.climate-map").wait_for(timeout=10000)
        try:
            page.wait_for_function("document.querySelector('.climate-map')?.complete && document.querySelector('.climate-map')?.naturalWidth>0",timeout=16000)
            log("REAL CLIMATE MAP PASS "+str(page.evaluate("document.querySelector('.climate-map').naturalWidth")))
        except Exception:
            log("MAP EXTERNAL IMAGE NOT AVAILABLE, official source link remains visible")
            assert page.locator('a[href*="bom.gov.au"]').count()>0
        idx=page.evaluate("S.findIndex(s=>s.type==='worksheet')")
        page.evaluate("(i)=>go(i)",idx)
        assert page.locator('a[href="../worksheet.html"]').count()>=1
        assert page.locator('a[href*=".pdf"]').count()>=1
        log("WORKSHEET LINK PASS")
        page.screenshot(path="/tmp/grade8-unit2-lesson.png",full_page=True)
        # Student worksheet must have Hebrew instructions and print as two A4 pages.
        resp=page.goto(BASE+"worksheet.html",wait_until="domcontentloaded",timeout=30000)
        assert resp and resp.status==200
        assert page.locator(".page").count()==2
        assert page.locator('text=התאמה בין מילים לפירושיהן').count()>=1
        assert page.locator('text=השלמת מילות יחס').count()>=1
        assert page.locator('text=עבר פשוט').count()>=1
        assert page.locator('text=יצירת משפטים').count()>=1
        assert "מפתח תשובות" not in page.locator(".page").all_inner_texts()[0]
        log("TWO PAGE PRINTABLE WORKSHEET PASS")
        pdfurl=BASE+"files/Grade8-Unit2-Australia-CooberPedy-Worksheet.pdf"
        pdr=ctx.request.get(pdfurl,timeout=15000)
        assert pdr.status==200 and pdr.body()[:4]==b"%PDF" and len(pdr.body())>18000,(pdr.status,len(pdr.body()))
        log("LIVE PDF PASS "+str(len(pdr.body()))+" bytes")
        # Mobile viewport: no blank UI and links present.
        mobile=browser.new_context(viewport={"width":390,"height":844},device_scale_factor=1,is_mobile=True,has_touch=True)
        mp=mobile.new_page()
        mp.goto(BASE+"lesson/",wait_until="domcontentloaded",timeout=30000)
        mp.wait_for_function("typeof S !== 'undefined' && S.length>30",timeout=12000)
        assert mp.locator("#next").is_visible()
        mp.locator("#next").click()
        assert mp.locator("#counter").inner_text().startswith("2 /")
        log("MOBILE NAV PASS")
        mobile.close()
        if errors:raise AssertionError("Browser page errors: "+repr(errors))
        log("GRADE 8 UNIT 2 LESSON QA SUCCESS")
        ctx.close()
    finally:
        browser.close()
