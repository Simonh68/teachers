#!/usr/bin/env python3
"""Run a real Chromium readback of both public Grade 8 Unit 2 readers."""
import json
import time
from playwright.sync_api import sync_playwright

URL="https://simonh68.github.io/teachers/grade8/unit-2/"
CASES=[
 ("australia",12,"Australia is a very large"),
 ("coober-pedy",25,"Imagine a town")
]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
    try:
        for slug,count,opening in CASES:
            ctx=browser.new_context(viewport={"width":1280,"height":800})
            page=ctx.new_page()
            errors=[]
            resources=[]
            page.on("pageerror",lambda e: errors.append(str(e)))
            page.on("requestfailed",lambda req: resources.append({"url":req.url,"failure":req.failure}))
            page.on("response",lambda resp: resources.append({"asset":resp.url,"status":resp.status}) if "/shared/read-along/standard.css" in resp.url else None)
            url=URL+slug+"/?view=sentences"
            print("OPEN",url,flush=True)
            resp=page.goto(url,wait_until="domcontentloaded",timeout=30000)
            print("PAGE STATUS",resp.status if resp else "missing",flush=True)
            try:
                page.wait_for_function("Boolean(window.__grade8Bilingual?.ready)",timeout=20000)
                result=page.evaluate("""() => ({ready:window.__grade8Bilingual.ready,
                    count:window.__grade8Bilingual.D.story.length,
                    first:document.querySelector('#english')?.textContent,
                    speed:document.querySelector('#speed')?.value,
                    firstAudio:window.__grade8Bilingual.records[0].parts[0].src})""")
                print("READBACK",json.dumps(result,ensure_ascii=False),flush=True)
                assert result["count"]==count,(slug,"count",result["count"])
                assert opening in result["first"],(slug,"opening",result["first"])
                assert result["speed"]=="0.75",(slug,"speed",result["speed"])
                first_audio=ctx.request.get(result["firstAudio"],timeout=15000)
                print("AUDIO HTTP",first_audio.status,"BYTES",len(first_audio.body()),flush=True)
                assert first_audio.ok and len(first_audio.body())>2000,slug+" audio missing"
                page.locator("#play").click(timeout=10000)
                page.wait_for_timeout(1800)
                playback=page.evaluate("""() => ({phase:window.__grade8Bilingual.player.phase,
                 marker:window.__grade8Bilingual.marker})""")
                print("PLAYBACK",playback,flush=True)
                assert playback["phase"] in ("playing","gap","loading","ended"),slug+" playback did not begin"
                page.locator("#play").click(timeout=10000)
                page.locator('[data-step="1"]').first.click()
                assert page.evaluate("window.__grade8Bilingual.reveal"),"translation reveal broken"
                assert page.locator("#hebrew").inner_text(),"Hebrew translation missing"
                print("PASS",slug,flush=True)
            except Exception:
                print("FAILURE DEBUG",json.dumps({"errors":errors,"resources":resources[-18:],
                    "content":page.locator("body").inner_text()[:1200]},ensure_ascii=False),flush=True)
                raise
            finally:ctx.close()
    finally:browser.close()
