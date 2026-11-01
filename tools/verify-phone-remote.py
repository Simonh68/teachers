#!/usr/bin/env python3
"""Real browser two-device test of Teachers QR phone remote.

Uses the actual PeerJS WebRTC signaling and approval path, without changing
Firebase or sending any identity/answer data. Local file server avoids a Pages
deployment race. Also checks a Read-Along shell and shared deck compatibility.
"""
from __future__ import annotations
import json, threading, time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PORT=18771
BASE=f"http://127.0.0.1:{PORT}"
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):pass

httpd=ThreadingHTTPServer(("127.0.0.1",PORT),Handler)
threading.Thread(target=httpd.serve_forever,daemon=True).start()

SELECT="#teachers-qr-remote-host"
CASES=[
    ("grade8-unit2", "grade8/unit-2/lesson/", "counter"),
    ("standard-deck","shared/lessons/bagrut-reading-traps/", "counter")
]

def read_state(page):
    return page.evaluate("window.teachersPhoneRemote && {role:window.teachersPhoneRemote.role,connected:window.teachersPhoneRemote.connected,status:window.teachersPhoneRemote.lastStatus}")

def check_case(browser,name,path,counter_id):
    desktop=browser.new_context(viewport={"width":1400,"height":860})
    phone=browser.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=1)
    host=desktop.new_page();handset=phone.new_page()
    errors=[]
    host.on("pageerror",lambda e:errors.append("host "+str(e)))
    handset.on("pageerror",lambda e:errors.append("phone "+str(e)))
    try:
        url=BASE+"/"+path
        response=host.goto(url,wait_until="domcontentloaded",timeout=25000)
        assert response and response.status==200,(name,"page HTTP")
        host.wait_for_function("Boolean(window.teachersPhoneRemote && document.querySelector('#teachers-qr-remote-host'))",timeout=15000)
        assert read_state(host)["role"]=="presenter"
        launch=host.locator(f"{SELECT} #launch")
        launch.click(timeout=10000)
        host.locator(f"{SELECT} #link").wait_for(timeout=15000)
        host.wait_for_function("""() => Boolean(document.querySelector('#teachers-qr-remote-host')?.shadowRoot?.getElementById('link')?.value)""",timeout=32000)
        link=host.locator(f"{SELECT} #link").input_value()
        assert "teacherRemote=" in link and "remote=" not in link.replace("teacherRemote=",""),link
        assert host.locator(f"{SELECT} #qr img, {SELECT} #qr canvas").count()>0,"QR graphic not rendered"
        print("QR PASS",name,flush=True)
        response=handset.goto(link,wait_until="domcontentloaded",timeout=26000)
        assert response and response.status==200
        handset.wait_for_function("Boolean(window.teachersPhoneRemote && window.teachersPhoneRemote.role==='controller')",timeout=16000)
        assert handset.locator(f"{SELECT} #next").is_disabled(),"Unauthorized phone must not navigate"
        print("UNAPPROVED CONTROLLER BLOCKED",name,flush=True)
        host.locator(f"{SELECT} #approve").wait_for(state="visible",timeout=32000)
        host.locator(f"{SELECT} #approve").click()
        handset.wait_for_function("Boolean(window.teachersPhoneRemote?.connected)",timeout=18000)
        assert read_state(host)["connected"]
        print("EXPLICIT APPROVAL PASS",name,flush=True)

        original=host.evaluate("(id) => document.getElementById(id)?.textContent.trim()",counter_id)
        handset.locator(f"{SELECT} #next").click()
        host.wait_for_function("(old) => document.querySelector('#counter')?.textContent?.trim() !== old",original.strip(),timeout=12000)
        after=host.evaluate("(id) => document.getElementById(id)?.textContent.trim()",counter_id)
        print("NEXT SYNC",name,repr(original),"to",repr(after),flush=True)
        handset.locator(f"{SELECT} #previous").click()
        host.wait_for_function("(old) => document.querySelector('#counter')?.textContent?.trim() !== old",after.strip(),timeout=12000)
        print("PREVIOUS SYNC PASS",name,flush=True)

        # Host-side navigation updates the phone's slide counter, too.
        host.evaluate("""() => (document.querySelector('#next') || document.querySelector('[data-step="1"]'))?.click()""")
        current=host.evaluate("(id) => document.getElementById(id)?.textContent.trim()",counter_id)
        handset.wait_for_function("(expected) => document.querySelector('#teachers-qr-remote-host')?.shadowRoot?.getElementById('counter')?.textContent?.trim()===expected",current,timeout=12000)
        print("PRESENTER TO PHONE SYNC PASS",name,flush=True)

        if name=="grade8-unit2":
            host.evaluate("go(S.findIndex(s=>s.type==='reveal'))")
            host.wait_for_timeout(600)
            assert host.locator(".hiddenAnswer").count()==0
            handset.locator(f"{SELECT} #reveal").click()
            host.locator(".hiddenAnswer").wait_for(state="visible",timeout=10000)
            print("HINT REVEAL PASS",name,flush=True)
        # Reset disconnects/invalidates the old approved controller.
        host.locator(f"{SELECT} #launch").click()
        host.locator(f"{SELECT} #reset").click()
        handset.wait_for_function("!window.teachersPhoneRemote?.connected",timeout=15000)
        assert handset.locator(f"{SELECT} #next").is_disabled()
        print("RESET / REVOKE PASS",name,flush=True)
        assert not errors,errors
        print("FULL TWO-DEVICE CASE PASS",name,flush=True)
    finally:
        phone.close()
        desktop.close()

def check_reader(browser):
    ctx=browser.new_context()
    try:
        p=ctx.new_page();p.goto(BASE+"/grade8/unit-2/australia/?view=sentences",wait_until="domcontentloaded",timeout=20000)
        p.wait_for_function("Boolean(window.__grade8Bilingual?.ready)",timeout=16000)
        p.wait_for_function("Boolean(document.querySelector('#teachers-qr-remote-host'))",timeout=12000)
        assert p.locator(f"{SELECT} #launch").count()==1
        assert p.locator("#english").inner_text().startswith("Australia")
        print("READ-ALONG BODY REBUILD COMPATIBILITY PASS",flush=True)
    finally:ctx.close()

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
    try:
        for name,path,counter in CASES:check_case(browser,name,path,counter)
        check_reader(browser)
    finally:browser.close()
httpd.shutdown()
print("ALL QR REMOTE TESTS PASSED",flush=True)
