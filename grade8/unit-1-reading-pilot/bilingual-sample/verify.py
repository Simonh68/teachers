"""Test the requested one-sentence/two-slide sample with real existing narration."""
from __future__ import annotations
import functools, hashlib, http.server, json, os, re, subprocess, threading, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PILOT = HERE.parent
OUT = Path(os.environ.get('SAMPLE_QA_DIR', '/tmp/bilingual-sample-qa'))
OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8879/grade8/unit-1-reading-pilot/bilingual-sample/'
PUBLIC = 'https://simonh68.github.io/teachers/grade8/unit-1-reading-pilot/bilingual-sample/'

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
protected = [ROOT/'index.html', ROOT/'grade8/index.html', ROOT/'grade8/unit-1/index.html', PILOT/'index.html', PILOT/'reading-pilot.js', PILOT/'reading-pilot.css', PILOT/'phrase-player.js', PILOT/'phrase-data.js', PILOT/'unit-data.js']
before = {str(p.relative_to(ROOT)): digest(p) for p in protected}
html = (HERE/'index.html').read_text(encoding='utf-8')
assert 'SpeechSynthesis' not in html and 'speechSynthesis' not in html
inline = re.findall(r'<script>(.*?)</script>', html, re.S)
for n, code in enumerate(inline):
    path = OUT/f'inline-{n}.js'; path.write_text(code, encoding='utf-8')
    subprocess.run(['node', '--check', str(path)], check=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 8879), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
report = {'passed': False, 'sampleSentences': 1, 'slides': 2, 'pauseMs': 1500, 'viewports': [], 'speechRuns': []}
try:
 with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for w,h in [(1366,768),(1024,600),(390,844),(360,640),(844,390),(740,360)]:
        ctx = browser.new_context(viewport={'width':w,'height':h}, has_touch=True, is_mobile=w<700)
        page = ctx.new_page(); errors=[]
        page.on('pageerror', lambda e:errors.append(str(e)))
        assert page.goto(URL,wait_until='networkidle').status==200
        page.wait_for_function('window.__bilingualSample && __bilingualSample.ready')
        page.evaluate('document.fonts.ready')
        checks = page.evaluate('''() => {
          const D=__bilingualSample;
          const r=e=>{const a=e.getBoundingClientRect();return [a.x,a.y,a.width,a.height]};
          D.show(0);
          if(getComputedStyle(document.getElementById('translation-slot')).visibility!=='hidden')throw Error('Hebrew revealed on first slide');
          const node=document.getElementById('english');
          const original=[r(node),...Array.from(node.querySelectorAll('span')).map(r)];
          D.show(1);
          if(node!==document.getElementById('english'))throw Error('English DOM replaced');
          if(JSON.stringify(original)!==JSON.stringify([r(node),...Array.from(node.querySelectorAll('span')).map(r)]))throw Error('English moved on translation reveal');
          if(getComputedStyle(document.getElementById('translation-slot')).visibility!=='visible')throw Error('Hebrew requires another reveal');
          if(node.textContent!==D.sentence.plain||document.getElementById('hebrew').textContent!==D.sentence.he)throw Error('Source text changed');
          for(const id of ['english','hebrew']){
            const e=document.getElementById(id),box=e.parentElement.getBoundingClientRect(),a=e.getBoundingClientRect();
            if(a.top<box.top-1||a.bottom>box.bottom+1||e.scrollWidth>e.clientWidth+1)throw Error('Clipped '+id+': '+JSON.stringify([a.toJSON(),box.toJSON()]));
            for(const s of e.querySelectorAll('span')){
              const c=getComputedStyle(s);
              if(parseFloat(c.borderLeftWidth)||parseFloat(c.borderRightWidth)||c.textDecorationLine!=='none')throw Error('Visible phrase separators');
            }
          }
          if(document.querySelector('details'))throw Error('Translation hidden in details');
          if(Object.keys(D.heMap).length!==D.sentence.tokens.length)throw Error('Incomplete bilingual mapping');
          if(document.documentElement.scrollWidth>innerWidth+1)throw Error('Page overflow');
          return{stationaryEnglish:true,translationVisibleOnSecondSlide:true,sourceTextExact:true,noTextClipping:true,noAddedSeparators:true,semanticWordMapping:D.semantic};
        }''')
        page.screenshot(path=str(OUT/f'{w}x{h}-bilingual.png'))
        page.evaluate('document.activeElement.blur();__bilingualSample.show(0)')
        for key,expected in [('ArrowDown',1),('ArrowUp',0),('ArrowRight',1),('ArrowLeft',0)]:
            page.keyboard.press(key);assert page.evaluate('__bilingualSample.slide')==expected
        session = ctx.new_cdp_session(page)
        cx,cy=w/2,h/2
        for dx,dy,start,expected in [(0,-85,0,1),(0,85,1,0),(-85,0,0,1),(85,0,1,0)]:
            page.evaluate('__bilingualSample.show(arguments[0])' if False else '(n)=>__bilingualSample.show(n)',start)
            session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx,'y':cy}]})
            session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx+dx,'y':cy+dy}]})
            session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
            assert page.evaluate('__bilingualSample.slide')==expected,(w,h,dx,dy)
        page.evaluate('__bilingualSample.show(0)')
        page.mouse.move(cx,cy);page.mouse.wheel(0,160);page.wait_for_timeout(70)
        assert page.evaluate('__bilingualSample.slide')==1
        checks.update(viewport=f'{w}x{h}',keyboard=True,fourDirectionRealTouch=True,wheel=True)
        assert not errors,errors
        report['viewports'].append(checks)
        ctx.close()
    ctx=browser.new_context(viewport={'width':1366,'height':768})
    page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(URL+'#slide-2',wait_until='networkidle');page.wait_for_function('window.__bilingualSample && __bilingualSample.ready')
    for speed in ['1.25','0.5']:
        page.select_option('#speed',speed)
        page.evaluate('''() => {
          const D=__bilingualSample;D.player.events=[];
          window.sampleMarks=[];
          const old=D.player.onUpdate;
          D.player.onUpdate=p=>{old(p);if(p.phase==='playing')sampleMarks.push({time:p.sourceTime,en:D.marker.en,he:D.marker.he,part:p.part,visible:getComputedStyle(document.getElementById('translation-slot')).visibility});};
        }''')
        page.click('#replay');page.wait_for_function('__bilingualSample.player.phase==="playing"')
        page.wait_for_function('__bilingualSample.player.sourceTime>0.5')
        page.screenshot(path=str(OUT/f'active-marker-{speed}.png'))
        page.wait_for_function('__bilingualSample.player.phase==="ended"',timeout=60000)
        events=page.evaluate('__bilingualSample.player.events');marks=page.evaluate('sampleMarks')
        gaps=[];starts=[]
        for i,e in enumerate(events):
            if e['type']=='gap:start':
                end=next(x for x in events[i+1:] if x['type']=='gap:end')
                playing=next(x for x in events[i+1:] if x['type']=='part:playing')
                timer=end['at']-e['at']; actual=playing['at']-e['at']
                assert 1490<=timer<=1700, timer
                assert 1490<=actual<=1800, actual
                gaps.append({'timerMs':round(timer,1),'audibleGapMs':round(actual,1)})
            if e['type']=='part:playing': starts.append(e['part'])
        assert len(gaps)==3 and starts==[0,1,2,3], (gaps,starts)
        active=[m for m in marks if m['en'] is not None]
        assert active and all(m['visible']=='visible' and m['he'] is not None for m in active)
        assert set(m['part'] for m in active)=={0,1,2,3}
        mapping=page.evaluate('__bilingualSample.heMap')
        assert all(mapping[str(m['en'])]==m['he'] for m in active)
        report['speechRuns'].append({'speed':speed,'pauseGaps':gaps,'bilingualSamples':len(active),'matchedHebrewUnits':len(set(m['he'] for m in active))})
    # Stop on slide change; the following bilingual slide starts again only after a delay.
    page.click('#replay');page.wait_for_function('__bilingualSample.player.phase==="playing"')
    page.evaluate('__bilingualSample.show(0)');assert page.evaluate('__bilingualSample.player.audio.paused')
    page.evaluate('__bilingualSample.stop();__bilingualSample.show(1);__bilingualSample.stop()')
    page.select_option('#speed','1.25');page.click('#replay')
    page.wait_for_function('__bilingualSample.player.phase==="gap"',timeout=15000)
    page.click('#play');assert page.evaluate('__bilingualSample.player.phase')=='pausedGap'
    part=page.evaluate('__bilingualSample.player.part');page.wait_for_timeout(1700)
    assert page.evaluate('__bilingualSample.player.part')==part
    assert page.evaluate('getComputedStyle(document.getElementById("translation-slot")).visibility')=='visible'
    page.click('#play');page.wait_for_function('__bilingualSample.player.part>0',timeout=5000)
    page.evaluate('__bilingualSample.stop()');assert page.evaluate('__bilingualSample.player.audio.paused')
    assert not errors,errors
    report['pauseResume']=True;report['stopOnSlideChange']=True
    report['source'] = page.evaluate('({en:__bilingualSample.sentence.plain,he:__bilingualSample.sentence.he,semantic:__bilingualSample.semantic,parts:__bilingualSample.record.parts.map(x=>x.src)})')
    browser.close()
 server.shutdown()
 # Verify the public sample, exact code, and the existing source audio; no publication writes here.
 def get(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Teachers-Sample-QA'})
    with urllib.request.urlopen(request,timeout=30) as r:
        assert r.status==200,(url,r.status)
        return r.read()
 for attempt in range(18):
    try:
        live=get(PUBLIC+'?qa='+str(int(time.time())))
        assert hashlib.sha256(live).hexdigest()==digest(HERE/'index.html'),'Public sample is not yet current'
        break
    except Exception:
        if attempt==17: raise
        time.sleep(5)
 for p in ['unit-data.js','phrase-data.js','phrase-player.js']:
    payload=get(PUBLIC+'../'+p)
    assert hashlib.sha256(payload).hexdigest()==digest(PILOT/p),p
 for src in report['source']['parts']:
    filename=src.rsplit('/',1)[1];payload=get(PUBLIC+'../audio/'+filename)
    assert hashlib.sha256(payload).hexdigest()==digest(PILOT/'audio'/filename)
    assert payload[:4]==b'RIFF',filename
 for p in protected: assert digest(p)==before[str(p.relative_to(ROOT))]
 assert 'bilingual-sample' not in (ROOT/'grade8/index.html').read_text(encoding='utf-8')
 assert 'bilingual-sample' not in (ROOT/'index.html').read_text(encoding='utf-8')
 report.update(passed=True,publicURL=PUBLIC,publicFilesVerified=True,originalUnitUntouched=True,pilotUntouched=True,unlisted=True,checkedAtUTC=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
except Exception as e:
 report['error']=str(e)
 raise
finally:
 (OUT/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
