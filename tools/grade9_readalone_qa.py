"""Browser QA for all Read Alone pages and original teaching slides."""
import functools, http.server, json, os, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'grade9/unit-1/read-alone';OUT=R/'grade9-ra-qa';OUT.mkdir(exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8765),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start()
base=os.environ.get('READ_ALONE_BASE','http://127.0.0.1:8765')
report={'base':base,'checks':[],'screens':[],'errors':[]}
def check(name,ok,detail=None):
 report['checks'].append({'name':name,'pass':bool(ok),'detail':detail})
 if not ok:raise AssertionError(f'{name}: {detail}')
def ready(page):page.wait_for_function('window.TeachersReadAlone?.data && window.TeachersReadAlone?.timing && document.querySelector("#raText")',timeout=45000)
def bounds(page):return page.evaluate('''()=>{const panel=document.querySelector('#raPanel'),r=panel.getBoundingClientRect();const nodes=[...document.querySelectorAll('#raText .ra-word')];const bad=nodes.map(n=>{const a=n.getBoundingClientRect();return a.left<r.left-1||a.right>r.right+1||a.top<r.top-1||a.bottom>r.bottom+1?n.textContent:null}).filter(Boolean);const nav=document.querySelector('.ra-nav').getBoundingClientRect();return {bad,hscroll:document.documentElement.scrollWidth>innerWidth+1,navBottom:nav.bottom,height:innerHeight,panelHeight:r.height,textSize:getComputedStyle(document.querySelector('#raText')).fontSize}}''')
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for width,height in [(1440,900),(390,844),(360,640)]:
   context=browser.new_context(viewport={'width':width,'height':height});page=context.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
   page.goto(base+'/grade9/unit-1/read-alone/',wait_until='networkidle');ready(page)
   data=page.evaluate('TeachersReadAlone.data');check(f'{width} source 46 sentences',len(data['sentences'])==46)
   for mode,total in [('text',len(data['pages'])),('sentences',92)]:
    previous_box=None
    for n in range(total):
     page.evaluate('([n,m])=>TeachersReadAlone.setPage(n,m)',[n,mode]);page.wait_for_timeout(35)
     b=bounds(page);check(f'layout {width} {mode} {n+1}',not b['bad'] and not b['hscroll'] and b['navBottom']<=height+1,b)
     if mode=='text':
      strings=page.locator('.ra-sentence').all_text_contents();expect=[data['sentences'][s]['en'] for s in data['pages'][n]];check(f'text preserved {width} page {n+1}',strings==expect)
     else:
      check(f'sentence preserved {width} step {n+1}',page.locator('#raText').text_content()==data['sentences'][n//2]['en'])
      box=page.locator('#raText').bounding_box()
      if n%2:check(f'reveal does not move English {width} pair {n//2+1}',all(abs(box[k]-previous_box[k])<1 for k in ['x','y','width','height']),{'before':previous_box,'after':box})
      previous_box=box
     if (mode=='text' and n in [0,len(data['pages'])-1]) or(mode=='sentences' and n in [0,1,80,81]):
      name=f'{width}-{mode}-{n+1}.png';page.screenshot(path=str(OUT/name));report['screens'].append(name)
   page.goto(base+'/grade9/the-message-without-a-voice/',wait_until='networkidle');page.wait_for_function('window.TeachersReadAlone?.data');check(f'deck slide count {width}',page.locator('.slide').count()==142)
   slide_ids=page.locator('.slide').evaluate_all('(els)=>els.map(e=>e.id)')
   for slide_id in slide_ids:
    page.evaluate('(id)=>location.hash=id',slide_id);page.wait_for_timeout(25)
    visible=page.locator('.slide.active');check(f'deck active {width} {slide_id}',visible.get_attribute('id')==slide_id)
    if visible.get_attribute('data-ra-sentence') is not None:
     b=page.evaluate('''()=>{let el=document.querySelector('.slide.active .story-sentence'),a=el.getBoundingClientRect(),c=document.querySelector('.ra-deck-controls').getBoundingClientRect();return {left:a.left,right:a.right,top:a.top,bottom:a.bottom,controls:c.top,w:innerWidth}}''');check(f'deck fit {width} {slide_id}',b['left']>=-1 and b['right']<=width+1 and b['top']>=0 and b['bottom']<=b['controls']+1,b)
   context.close()
  context=browser.new_context(viewport={'width':390,'height':844});page=context.new_page();page.goto(base+'/grade9/unit-1/read-alone/',wait_until='networkidle');ready(page)
  page.wait_for_timeout(2200);check('cold load silent',page.evaluate('TeachersReadAlone.audio.paused'))
  check('default speed 0.75',page.locator('#raSpeed').input_value()=='0.75')
  page.locator('[data-ra-play]').click();page.wait_for_function('!TeachersReadAlone.audio.paused && TeachersReadAlone.audio.currentTime > TeachersReadAlone.clip.start+.15',timeout=15000);check('real audio plays',True)
  page.wait_for_function('(()=>{const t=TeachersReadAlone.audio.currentTime,w=TeachersReadAlone.clip.words.find(w=>t>=w.start&&t<w.end),n=document.querySelector(".ra-spoken");return w&&n?.dataset.w===String(w.index)})()',timeout=8000);check('yellow word tracks audio',True)
  page.locator('[data-ra-play]').click();before=page.evaluate('TeachersReadAlone.audio.currentTime');page.wait_for_timeout(300);check('pause preserves time',abs(page.evaluate('TeachersReadAlone.audio.currentTime')-before)<.02)
  page.locator('[data-ra-play]').click();page.wait_for_function('(v)=>TeachersReadAlone.audio.currentTime>v+.08',arg=before,timeout=5000);check('resume from same time',True)
  for value in ['1','0.75','0.5','0.35','0.25']:
   page.locator('#raSpeed').select_option(value);check('speed '+value,page.evaluate('TeachersReadAlone.audio.playbackRate')==float(value))
  page.locator('[data-ra-tab="1"]').click();page.wait_for_timeout(250);check('manual tab stops audio',page.evaluate('TeachersReadAlone.audio.paused'))
  page.reload(wait_until='networkidle');ready(page);check('speed restored after reload',page.locator('#raSpeed').input_value()=='0.25')
  first=page.locator('.ra-unit').first;before=first.bounding_box();first.click();check('phrase translation visible',page.locator('#raTip').is_visible() and len(page.locator('#raTip').text_content())>0);after=first.bounding_box();check('translation does not move English',before==after)
  page.locator('.ra-mode[data-mode="sentences"]').click();page.wait_for_timeout(700);check('sentence delay initially silent',page.evaluate('TeachersReadAlone.audio.paused'));page.wait_for_timeout(1700);check('sentence delayed autoplay',not page.evaluate('TeachersReadAlone.audio.paused'))
  page.locator('[data-ra-play]').click();page.locator('.ra-word.ra-hit').first.click();check('word translation visible',page.locator('#raTip').is_visible())
  page.locator('#raNext').click();page.wait_for_timeout(2300);check('English audio on Hebrew reveal',not page.evaluate('TeachersReadAlone.audio.paused'))
  page.locator('.ra-mode[data-mode="text"]').click();page_before_end=page.evaluate('TeachersReadAlone.page');page.locator('[data-ra-play]').click();page.evaluate('TeachersReadAlone.audio.currentTime=TeachersReadAlone.clip.end-.04');page.wait_for_timeout(800);check('stops at passage boundary',page.evaluate('TeachersReadAlone.audio.paused'));check('no automatic passage advance',page.evaluate('TeachersReadAlone.page')==page_before_end)
  page.locator('#raNext').click();page.wait_for_timeout(350);check('continue starts next passage',not page.evaluate('TeachersReadAlone.audio.paused'))
  check('continue advances one passage',page.evaluate('TeachersReadAlone.page')==page_before_end+1)
  page.evaluate('Object.defineProperty(document,"hidden",{configurable:true,get:()=>true});document.dispatchEvent(new Event("visibilitychange"));');check('visibility change stops',page.evaluate('TeachersReadAlone.audio.paused'))
  context.close()
  context=browser.new_context();context.add_init_script('Storage.prototype.getItem=function(){throw Error("blocked")};Storage.prototype.setItem=function(){throw Error("blocked")};');page=context.new_page();page.goto(base+'/grade9/unit-1/read-alone/',wait_until='networkidle');ready(page);check('blocked storage still usable',page.locator('#raSpeed').input_value()=='0.75');context.close()
  context=browser.new_context();context.add_init_script('localStorage.setItem("teachers-read-alone-speed-v1","invalid")');page=context.new_page();page.goto(base+'/grade9/unit-1/read-alone/',wait_until='networkidle');ready(page);check('invalid saved speed fallback',page.locator('#raSpeed').input_value()=='0.75');context.close()
  browser.close()
 check('no browser JavaScript errors',not report['errors'],report['errors'])
 report['passed']=True
except Exception as e:
 report['passed']=False;report['failure']=str(e)
 try:page.screenshot(path=str(OUT/'failure.png'),full_page=True)
 except Exception:pass
 raise
finally:
 (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));(O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('QA',len(report['checks']),'checks; passed:',report.get('passed'),flush=True);server.shutdown()
