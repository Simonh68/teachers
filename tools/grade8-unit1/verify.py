"""Acceptance checks for the published unit. --live checks the actual public site."""
from pathlib import Path
import json,re,sys,threading,http.server,functools,subprocess,time,urllib.request,urllib.parse,concurrent.futures
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade8/unit-1';REPORT=OUT/'qa-report.json';results=[]
def record(name,detail=True):
    results.append({'check':name,'result':detail});print(name,detail,flush=True)
if '--live' in sys.argv:
    base='https://simonh68.github.io/teachers/grade8/unit-1/'
    def fetch(url):
        req=urllib.request.Request(url,headers={'User-Agent':'Teachers-Unit-QA/1.0','Cache-Control':'no-cache'})
        with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(),r.headers.get('Content-Type','')
    for attempt in range(12):
        try:
            status,html,ct=fetch(base+'?release=20260922-unit1');assert status==200 and b'unit-data.js' in html
            status,payload,ct=fetch(base+'unit-data.js?release=20260922-unit1');assert status==200 and b'2026-10-22' in payload
            break
        except Exception:
            if attempt==11:raise
            time.sleep(10)
    record('Public unit and data return HTTP 200')
    data=json.loads(payload.decode().removeprefix('window.UNIT_DATA=').strip().removesuffix(';'))
    urls=[urllib.parse.urljoin(base,s['audio']) for s in data['story']]+[urllib.parse.urljoin(base,w['audio']) for w in data['words']]
    def audio_check(url):
        status,body,ct=fetch(url)
        assert status==200 and len(body)>1000 and ('audio' in ct or body[:3]==b'ID3' or body[0]==255),(url,ct,len(body))
        return url
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:checked=list(pool.map(audio_check,urls))
    record('Public recorded MP3 clips return valid audio',len(checked))
    for name in ['reading/','sentences/','teacher.html']:assert fetch(base+name)[0]==200
    record('Public direct links',3)
    print(json.dumps({'live':True,'checks':results},ensure_ascii=False),flush=True)
    (OUT/'live-check.json').write_text(json.dumps({'live':True,'checks':results},ensure_ascii=False,indent=2));sys.exit(0)
html=(OUT/'index.html').read_text();scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',html,re.S)
js=Path('/tmp/grade8-unit1-check.js');js.write_text('\n'.join(scripts));subprocess.run(['node','--check',str(js)],check=True)
record('JavaScript syntax')
data=json.loads((OUT/'unit-data.js').read_text().removeprefix('window.UNIT_DATA=').strip().removesuffix(';'))
assert len(data['story'])==18 and len(data['words'])==55 and len(data['questions'])==7 and len(data['translations'])==6
assert data['exam']=='2026-10-22' and len(data['pages'])==10
assert sorted(i for page in data['pages'] for i in page)==list(range(18))
for s in data['story']:
    assert len(s['tokens'])==len(re.findall(r"[A-Za-z]+(?:[’'][A-Za-z]+)?",s['plain']))
    assert sorted(i for u in s['units'] for i in u['indices'])==list(range(len(s['tokens'])))
    assert all(t['he'] and t['start']<t['end'] for t in s['tokens'])
record('Approved scope and complete contextual translations',sum(len(s['tokens']) for s in data['story']))
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8768),functools.partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();base='http://127.0.0.1:8768/grade8/unit-1/'
shots=Path('/tmp/grade8-unit1-qa');shots.mkdir(exist_ok=True)
def ready(page):
    page.wait_for_function('window.UNIT_DATA && document.readyState==="complete"')
    page.evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
def progress_test(browser):
    context=browser.new_context(viewport={'width':1365,'height':900});page=context.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(base);ready(page)
    page.evaluate("window.clickEvidence=[];for(const name of ['click','input','change'])document.addEventListener(name,e=>clickEvidence.push({name,tag:e.target.tagName,id:e.target.dataset.tick,checked:e.target.checked,prevented:e.defaultPrevented}),true)")
    box=page.locator('[data-tick="m0-done"]')
    try:
        # Scroll and wait for two layout frames before the user click. Test the
        # native label, native input and keyboard separately, with no DOM writes.
        box.scroll_into_view_if_needed();ready(page)
        page.locator('label').filter(has=box).locator('span').click()
        expect(box).to_be_checked();assert page.locator('#home progress').get_attribute('value')=='1'
        box.click();expect(box).not_to_be_checked()
        box.focus();page.keyboard.press('Space');expect(box).to_be_checked()
        page.locator('a[href="?view=chunks"]').first.click();page.wait_for_selector('.word')
        page.goto(base);ready(page);expect(page.locator('#resetHistory')).to_be_enabled()
        page.locator('#resetHistory').click();expect(box).to_be_checked()
        page.locator('#restoreHistory').click();expect(page.locator('#resetHistory')).to_be_enabled()
        assert not errors,errors
    except Exception:
        page.screenshot(path=str(shots/'progress-failure.png'),full_page=True)
        evidence=page.evaluate('({url:location.href,state,clicks:window.clickEvidence,checkbox:document.querySelector(\'[data-tick="m0-done"]\')?.outerHTML,checked:document.querySelector(\'[data-tick="m0-done"]\')?.checked})')
        print('PROGRESS DIAGNOSTICS',json.dumps({'browser':evidence,'errors':errors},ensure_ascii=False),flush=True)
        raise
    context.close();record('Progress label/input/keyboard and history reset/restore preserve completion')
with sync_playwright() as p:
    browser=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    progress_test(browser)
    for width,height in [(360,640),(390,844),(1365,900)]:
        context=browser.new_context(viewport={'width':width,'height':height},has_touch=True,is_mobile=width<600)
        page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base);page.wait_for_function('window.UNIT_DATA && document.querySelectorAll(".meeting").length===5')
        assert '22.10.2026' in page.locator('#home').inner_text();assert page.locator('.meeting').count()==5
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        if width==390:page.screenshot(path=str(shots/'home-mobile.png'),full_page=True)
        for view,count in [('chunks',10),('sentences',36)]:
            for i in range(count):
                page.goto(base+'?view='+view+'&p='+str(i));page.wait_for_selector('.reading-text')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,view,i,'horizontal overflow')
                assert page.locator('#next').is_visible()
                assert page.evaluate('document.querySelector(".toolbar").getBoundingClientRect().bottom<=innerHeight+1'),(width,view,i,'toolbar')
                ids=data['pages'][i] if view=='chunks' else [i//2]
                assert page.locator('.word').count()==sum(len(data['story'][j]['tokens']) for j in ids)
                for j in ids:assert page.locator(f'[data-text="{j}"]').inner_text()==data['story'][j]['plain']
                if view=='sentences' and i%2==0:
                    before=page.locator('.sentence-text').bounding_box();page.locator('#next').click();after=page.locator('.sentence-text').bounding_box()
                    assert before==after,(width,i,'English moved on translation reveal')
                if i==0 and width in (360,1365):page.screenshot(path=str(shots/f'{view}-{width}.png'))
        record(f'All 10 reading pages and 36 sentence/translation slides fit at {width}x{height}')
        page.goto(base+'?view=sentences');page.locator('#speed').select_option('0.25');page.goto(base+'?view=chunks')
        assert page.locator('#speed').input_value()=='0.25';page.reload();assert page.locator('#speed').input_value()=='0.25'
        record(f'Speed persists across standards and reload at {width}')
        page.goto(base+'?view=sentences&p=8');page.locator('.word').first.click();assert page.locator('#tip').is_visible()
        r=page.locator('#tip').bounding_box();assert r['x']>=0 and r['x']+r['width']<=width+1
        page.keyboard.press('Escape');assert page.locator('#tip').is_hidden();client=context.new_cdp_session(page)
        def swipe(x,y,dx,dy):
            client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
            for k in range(1,6):client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+dx*k/5,'y':y+dy*k/5}]})
            client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});page.wait_for_timeout(150)
        for dx,dy,delta in [(-70,0,1),(70,0,-1),(0,-70,1),(0,70,-1)]:
            page.goto(base+'?view=sentences&p=8');page.wait_for_selector('.word');page.evaluate('document.querySelector("#stage").scrollTop=0')
            b=page.locator('.word').first.bounding_box();x=max(85,min(width-85,b['x']+b['width']/2));y=b['y']+b['height']/2
            swipe(x,y,dx,dy);current=int(page.locator('#counter').inner_text().split('/')[0].strip())-1
            if dy and page.evaluate('document.querySelector("#stage").scrollHeight>document.querySelector("#stage").clientHeight+4'):continue
            assert current==8+delta,(width,dx,dy,current)
        record(f'Touch navigation and independent word tooltips at {width}')
        for v in ['grammar','practice','teacher','workbook','rehearsal','vocab']:
            page.goto(base+'?view='+v);page.wait_for_selector('#stage > *');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,v)
        assert not errors,errors;context.close()
    context=browser.new_context(viewport={'width':1365,'height':900});page=context.new_page()
    for i in range(36):
        page.goto(base+'?view=sentences&p='+str(i));page.wait_for_selector('.word');page.wait_for_timeout(900)
        assert page.locator('#play').inner_text()=='▶ הקראה'
        page.wait_for_function('!audio.paused && audio.currentTime>0',timeout=10000)
        assert page.evaluate('audio.playbackRate')==.75 and page.evaluate('audio.currentTime')>0
        page.evaluate('audio.currentTime=D.story[sentenceIndex].tokens[0].start+0.01');page.wait_for_timeout(30)
        assert page.locator('.word.playing').count()<=1
    record('Actual recorded audio starts on all 36 sentence and translation slides after the delay')
    page.goto(base+'?view=sentences&p=8');page.wait_for_selector('.word');page.locator('#next').click();page.locator('#next').click();page.wait_for_timeout(2400)
    assert page.evaluate('sentenceIndex')==5;record('Rapid navigation cancels the previous audio timer')
    page.goto(base+'?view=chunks&p=0');page.locator('#play').click();page.wait_for_function('!audio.paused')
    page.evaluate('sentenceIndex=D.pages[pos].at(-1);audio.currentTime=audio.duration-.05');page.wait_for_timeout(500)
    assert page.evaluate('audio.paused') and page.evaluate('pos')==0;record('Chunk playback pauses at page boundary')
    page.goto(base+'?view=practice');page.locator('#checkAnswer').click();assert page.locator('#modelAnswer').is_hidden()
    page.locator('#response').fill('It takes place in Thailand.');page.locator('#checkAnswer').click();assert page.locator('#modelAnswer').is_visible()
    record('Practice model answer follows a student attempt');context.close()
    context=browser.new_context();context.add_init_script("Object.defineProperty(Storage.prototype,'setItem',{value(){throw new Error('blocked')}});Object.defineProperty(Storage.prototype,'getItem',{value(){throw new Error('blocked')}})")
    page=context.new_page();page.goto(base+'?view=chunks');page.wait_for_selector('.word');assert 'חסומה' in page.locator('#saveStatus').inner_text();context.close()
    record('Blocked browser storage does not break learning');browser.close()
REPORT.write_text(json.dumps({'passed':True,'checks':results},ensure_ascii=False,indent=2)+'\n');server.shutdown()
