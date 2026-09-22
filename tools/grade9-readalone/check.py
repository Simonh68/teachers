"""Browser QA for the complete Grade 9 reading upgrade; exits nonzero on failure."""
from __future__ import annotations
import argparse, json, subprocess, time, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade9/unit-1/read-alone'
ART=ROOT/'read-alone-qa'
ART.mkdir(exist_ok=True)
parser=argparse.ArgumentParser(); parser.add_argument('--live',action='store_true'); args=parser.parse_args()
base='https://simonh68.github.io/teachers/' if args.live else 'http://127.0.0.1:8765/'
server=None
if not args.live:
    server=subprocess.Popen(['python','-m','http.server','8765','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
report={'mode':'public' if args.live else 'local','checks':[],'errors':[]}
def passed(name,**facts): report['checks'].append({'test':name,'passed':True,**facts}); print('PASS',name,flush=True)
def ready(page):
    page.wait_for_function('window.TeachersReadAlone && window.TeachersReadAlone.data && window.TeachersReadAlone.timing && window.TeachersReadAlone.clip',timeout=60000)
def layout(page,label):
    boxes=page.evaluate('''() => { const box=s=>{const e=document.querySelector(s);if(!e)return null; const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,height:r.height}};return {width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,text:box('#raText'),toolbar:box('#raToolbar'),next:box('#raNext')}}''')
    assert boxes['scrollWidth']<=boxes['width']+1,(label,'horizontal overflow',boxes)
    assert boxes['text']['left']>=-1 and boxes['text']['right']<=boxes['width']+1,(label,'text clipped',boxes)
    assert boxes['text']['bottom']<=boxes['toolbar']['top']+1,(label,'audio overlaps text',boxes)
    assert boxes['next']['bottom']<=boxes['height']+2,(label,'navigation below viewport',boxes)
    return boxes
try:
    data=json.loads((OUT/'content.json').read_text())
    audio=json.loads((OUT/'audio.json').read_text())
    source=BeautifulSoup((ROOT/'tools/grade9-readalone/source-original.html').read_text(),'html.parser')
    current=BeautifulSoup((ROOT/'grade9/the-message-without-a-voice/index.html').read_text(),'html.parser')
    assert [p.get_text() for p in source.select('.story-sentence')]==[s['en'] for s in data['sentences']]
    assert len(audio['sentences'])==len(data['sentences'])==46
    original_ids=[s['id'] for s in source.select('section.slide')]
    assert [s['id'] for s in current.select('section.slide') if not s['id'].endswith('-translation')]==original_ids
    passed('all original story text and 96 original slide IDs preserved',sentences=46)
    assert [i for p in data['pages'] for i in p]==list(range(46))
    expected=[w['index'] for s in data['sentences'] for w in s['words']]
    actual=[w['index'] for s in audio['sentences'] for w in s['words']]
    assert expected==actual and len(set(actual))==len(actual)
    for s in data['sentences']:
        assert [i for u in s['units'] for i in range(u['first'],u['last']+1)]==list(range(len(s['words'])))
        assert all(w['he'] for w in s['words'])
    passed('every word has contextual translation and measured timing',words=len(actual),pages=len(data['pages']))
    with sync_playwright() as p:
        browser=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        context=browser.new_context(viewport={'width':1365,'height':900},reduced_motion='reduce')
        page=context.new_page(); errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        reader=base+'grade9/unit-1/read-alone/'
        page.goto(reader,wait_until='networkidle'); ready(page)
        assert page.locator('#raSpeed').input_value()=='0.75'
        assert page.evaluate('TeachersReadAlone.audio.paused')
        page.locator('[data-ra-play]').click()
        page.wait_for_function('!TeachersReadAlone.audio.paused && TeachersReadAlone.audio.currentTime > TeachersReadAlone.clip.start + .1',timeout=20000)
        page.wait_for_function("document.querySelectorAll('.ra-word.ra-spoken').length===1")
        assert page.evaluate('TeachersReadAlone.audio.preservesPitch')
        page.locator('[data-ra-play]').click()
        position=page.evaluate('TeachersReadAlone.audio.currentTime'); page.wait_for_timeout(180)
        assert abs(page.evaluate('TeachersReadAlone.audio.currentTime')-position)<.02
        assert page.locator('.ra-spoken').count()==0
        page.locator('[data-ra-play]').click(); page.wait_for_timeout(160)
        assert page.evaluate('TeachersReadAlone.audio.currentTime')>position
        page.locator('[data-ra-play]').click()
        passed('MP3 playback, one-word highlight, pause and resume without restart')
        for rate in ['1','0.75','0.5','0.35','0.25']:
            page.locator('#raSpeed').select_option(rate)
            assert page.evaluate('TeachersReadAlone.audio.playbackRate')==float(rate)
            page.locator('[data-ra-restart]').click(); page.wait_for_timeout(280)
            assert not page.evaluate('TeachersReadAlone.audio.paused')
            page.locator('[data-ra-play]').click()
        page.reload(wait_until='networkidle'); ready(page)
        assert page.locator('#raSpeed').input_value()=='0.25'
        passed('all five speeds play; selected quarter-speed survives reload')
        hit=page.locator('.ra-hit').first; box=hit.bounding_box(); hit.click()
        assert page.locator('#raTip').is_visible() and page.locator('#raTip').inner_text()
        assert hit.bounding_box()==box and page.evaluate('TeachersReadAlone.audio.paused')
        page.keyboard.press('Escape'); assert not page.locator('#raTip').is_visible()
        passed('contextual tooltip does not move English or start audio')
        page.locator('[data-ra-play]').click()
        page.evaluate('TeachersReadAlone.audio.currentTime=TeachersReadAlone.clip.end+.03')
        page.wait_for_function('TeachersReadAlone.audio.paused')
        assert page.locator('[data-ra-tab="0"]').get_attribute('aria-selected')=='true'
        page.locator('#raNext').click(); page.wait_for_function('!TeachersReadAlone.audio.paused')
        page.locator('[data-ra-tab="0"]').click(); assert page.evaluate('TeachersReadAlone.audio.paused')
        passed('segment end stops, Continue starts next, manual tab stops and returns')
        page.screenshot(path=str(ART/'desktop-text.png'),full_page=True)
        sizes=[(1365,900),(360,640),(390,844)] if not args.live else [(390,844)]
        for width,height in sizes:
            page.set_viewport_size({'width':width,'height':height})
            for i in range(len(data['pages'])):
                page.locator(f'[data-ra-tab="{i}"]').click(); page.wait_for_timeout(35)
                layout(page,f'text page {i+1} {width}x{height}')
            page.locator('[data-ra-tab="0"]').click()
            page.screenshot(path=str(ART/f'text-{width}x{height}.png'),full_page=True)
            page.locator('[data-mode="sentences"]').click()
            assert page.locator('#raSpeed').input_value()=='0.25'
            for i in range(92):
                if i: page.locator('#raNext').click()
                page.wait_for_timeout(25)
                boxes=layout(page,f'sentence slide {i+1} {width}x{height}')
                if i%2==0: previous=boxes['text']
                else: assert all(abs(previous[k]-boxes['text'][k])<.6 for k in previous),(i,'English moved on reveal',previous,boxes['text'])
            page.screenshot(path=str(ART/f'sentences-{width}x{height}.png'),full_page=True)
            passed('every text page and all 92 sentence slides fit; English fixed on reveal',viewport=f'{width}x{height}')
            page.locator('[data-mode="text"]').click(); page.locator('[data-ra-tab="0"]').click()
        page.goto(reader+'?mode=sentences&sentence=1',wait_until='networkidle');ready(page)
        page.evaluate('TeachersReadAlone.stop()')
        page.locator('#raNext').click(); page.wait_for_timeout(1200)
        assert page.evaluate('TeachersReadAlone.audio.paused')
        page.wait_for_function('!TeachersReadAlone.audio.paused',timeout=3000)
        passed('translation slide auto-reads English after two seconds')
        page.locator('#raNext').click();page.wait_for_timeout(200)
        page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
        page.wait_for_timeout(2200);assert page.evaluate('TeachersReadAlone.audio.paused')
        page.evaluate("delete document.hidden")
        passed('visibility event cancels delayed speech and active playback')
        first=current.select_one('[data-ra-sentence="0"]')['id']
        for width,height in [(1365,900),(360,640),(390,844)]:
            page.set_viewport_size({'width':width,'height':height})
            page.goto(base+'grade9/the-message-without-a-voice/#'+first,wait_until='networkidle');ready(page)
            assert page.locator('#raSpeed').input_value()=='0.25'
            for n in range(46):
                original=current.select_one(f'[data-ra-sentence="{n}"]')['id']
                page.evaluate('(id)=>location.hash=id',original);page.wait_for_timeout(70)
                en=page.locator('.slide.active .story-sentence'); b1=en.bounding_box()
                assert page.locator('.slide.active').get_attribute('data-ra-sentence')==str(n)
                assert b1['x']>=-1 and b1['x']+b1['width']<=width+1,(n,width,b1)
                dock=page.locator('.ra-deck-controls').bounding_box()
                assert b1['y']+b1['height']<=dock['y']+2,(n,width,'overlap',b1,dock)
                page.locator('.nav [data-step="1"]').first.click();page.wait_for_timeout(70)
                b2=page.locator('.slide.active .story-sentence').bounding_box()
                assert page.locator('.slide.active').get_attribute('id')==original+'-translation'
                assert all(abs(b1[k]-b2[k])<1 for k in b1),(n,width,'paired layout moved',b1,b2)
            page.screenshot(path=str(ART/f'original-upgraded-{width}.png'),full_page=True)
        page.goto(base+'grade9/the-message-without-a-voice/#slide-36',wait_until='networkidle')
        assert page.locator('.slide.active').get_attribute('id')=='slide-36'
        passed('original deck: 46 paired sentences fit three screens; saved slide 36 preserved')
        page.goto(reader,wait_until='networkidle');ready(page)
        page.evaluate("localStorage.setItem('teachers-read-alone-speed-v1','invalid-value')")
        page.reload(wait_until='networkidle');ready(page)
        assert page.locator('#raSpeed').input_value()=='0.75'
        context2=browser.new_context(viewport={'width':390,'height':844})
        context2.add_init_script("Object.defineProperty(window,'localStorage',{get:()=>{throw new DOMException('Blocked','SecurityError')}})")
        p2=context2.new_page();p2.goto(reader,wait_until='networkidle');ready(p2)
        assert p2.locator('#raSpeed').input_value()=='0.75'
        p2.locator('[data-ra-play]').click();p2.wait_for_function('!TeachersReadAlone.audio.paused')
        context2.close();passed('invalid stored speed and blocked storage fall back safely')
        assert not errors,errors
        passed('no JavaScript page errors')
        browser.close()
    report['status']='passed'
except Exception as exc:
    report['status']='failed';report['errors'].append(str(exc));print('FAILED',repr(exc),flush=True)
    try: page.screenshot(path=str(ART/'failure.png'),full_page=True)
    except Exception: pass
    raise
finally:
    name='public-qa-report.json' if args.live else 'qa-report.json'
    (OUT/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (ART/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if server: server.terminate()
