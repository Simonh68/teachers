"""Exercise the actual shared deck in desktop and mobile Chromium."""
import json, threading, functools
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'grade8-workshop-qa';OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',8765),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
URL='http://127.0.0.1:8765/grade8/monkey-writing-workshop/'
report={'slides':0,'viewports':[],'interactions':[]}; failures=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    for name,w,h in [('desktop',1280,720),('short',900,560),('mobile',390,844)]:
        context=browser.new_context(viewport={'width':w,'height':h},has_touch=True,is_mobile=name=='mobile')
        page=context.new_page();page.on('pageerror',lambda e: failures.append(str(e)))
        page.goto(URL);page.evaluate('document.fonts.ready');page.wait_for_timeout(200)
        count=page.locator('.slide').count();report['slides']=count
        assert count==82,count
        sizes=[]
        for i in range(1,count+1):
            page.evaluate('(i)=>location.hash="slide-"+i',i);page.wait_for_timeout(30)
            box=page.locator('.slide.active').evaluate('''s=>{const f=s.querySelector('.frame'),r=f.getBoundingClientRect();return {overflow:s.scrollWidth>s.clientWidth+2,left:r.left,right:r.right,top:r.top,bottom:r.bottom,scroll:s.scrollHeight>s.clientHeight+2,zoom:getComputedStyle(f).zoom}}''')
            if box['overflow'] or box['left'] < -1 or box['right']>w+1: failures.append(f'{name} slide {i}: {box}')
            sizes.append(box)
            if i in [1,4,14,20,45,68,81]:page.screenshot(path=str(OUT/f'{name}-{i}.png'))
        report['viewports'].append({'name':name,'size':[w,h],'slides_checked':count,'scroll_slides':sum(x['scroll'] for x in sizes)})
        def go(i):
            page.evaluate('(i)=>location.hash="slide-"+i',i);page.wait_for_timeout(80)
        def current():return int(page.locator('#counter').inner_text().split('/')[0].strip())
        go(4)
        for key,expected in [('ArrowRight',5),('ArrowLeft',4),('ArrowDown',5),('ArrowUp',4)]:
            page.keyboard.press(key);assert current()==expected,(name,key,current())
        page.locator('[data-step="1"]').click();assert current()==5
        page.locator('[data-step="-1"]').click();assert current()==4
        page.mouse.move(w/2,h/2);page.mouse.wheel(0,200);page.wait_for_timeout(100);assert current()==5
        # Native touch events, not calls to the navigation function.
        cdp=context.new_cdp_session(page)
        def swipe(x1,y1,x2,y2):
            cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x1,'y':y1}]})
            for t in [.25,.5,.75,1]:
                cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x1+(x2-x1)*t,'y':y1+(y2-y1)*t}]})
            cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});page.wait_for_timeout(100)
        go(2)
        for coords,expected in [((w*.7,h*.5,w*.25,h*.5),3),((w*.25,h*.5,w*.7,h*.5),2),((w*.5,h*.65,w*.5,h*.35),3),((w*.5,h*.35,w*.5,h*.65),2)]:
            swipe(*coords);assert current()==expected,(name,'swipe',current(),expected)
        go(4);page.locator('.slide.active .match-option').first.click()
        assert page.locator('.slide.active .match-option[aria-pressed="true"]').count()==1
        swipe(w*.7,h*.5,w*.25,h*.5);assert current()==5
        swipe(w*.7,h*.5,w*.25,h*.5);assert current()==6
        # Pair positions are stable at reveal, and alternate answers stay accessible.
        go(4);q1=page.locator('.slide.active .question').bounding_box()
        go(5);q2=page.locator('.slide.active .question').bounding_box()
        assert abs(q1['y']-q2['y'])<2,(name,q1,q2)
        alt=page.locator('.slide:has(details)').first
        ix=alt.evaluate('(s)=>[...document.querySelectorAll(".slide")].indexOf(s)+1');go(ix)
        page.locator('.slide.active summary').click();assert page.locator('.slide.active details').get_attribute('open') is not None
        page.locator('.section-nav button[data-jump="כתיבה"]').click()
        assert page.locator('.slide.active').get_attribute('data-section')=='כתיבה'
        go(1);swipe(w*.25,h*.5,w*.7,h*.5);assert current()==1
        go(count);swipe(w*.7,h*.5,w*.25,h*.5);assert current()==count
        # Internal linked resources, stylesheet, script and reused break images exist.
        urls=page.locator('[href],[src]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href")||e.getAttribute("src"))')
        for href in set(urls):
            if href and not href.startswith(('http','#')):
                from urllib.parse import urljoin
                response=context.request.get(urljoin(URL,href));assert response.status==200,(href,response.status)
        report['interactions'].append(name+': keys, buttons, wheel, four touch directions, choice/reveal/next, sections, alternatives, bounds')
        context.close()
    browser.close()
server.shutdown();report['failures']=failures
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
assert not failures,failures
