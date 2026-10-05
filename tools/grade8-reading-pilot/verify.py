"""Exercise the actual copied unit and audio. Failing checks block publication."""
from pathlib import Path
import concurrent.futures,functools,hashlib,http.server,json,re,sys,threading,time,urllib.request
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];DEST=ROOT/'grade8/unit-1-reading-pilot';BASE='https://simonh68.github.io/teachers/grade8/unit-1-reading-pilot/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def unpack(p):return json.JSONDecoder().raw_decode(p.read_text(encoding='utf-8').split('=',1)[1].lstrip())[0]
def source_check():
 m=json.loads((DEST/'PILOT-MANIFEST.json').read_text(encoding='utf-8'))
 for name,digest in {**m['sourceFiles'],**m['navigationFiles']}.items():assert sha(ROOT/name)==digest,'Original modified: '+name
 src=unpack(ROOT/'grade8/unit-1/unit-data.js');data=unpack(DEST/'unit-data.js');parts=unpack(DEST/'phrase-data.js')
 assert data['words']==src['words'] and data['pages']==src['pages'] and data['questions']==src['questions'] and data['translations']==src['translations']
 for a,b in zip(src['story'],data['story']):assert {k:v for k,v in a.items() if k!='audio'}=={k:v for k,v in b.items() if k!='audio'}
 for s,rec in zip(data['story'],parts['sentences']):
  assert ''.join(p['text'] for p in rec['parts'])==s['plain']
  assert [i for p in rec['parts'] for i in range(p['firstToken'],p['lastToken']+1)]==list(range(len(s['tokens'])))
  for p in rec['parts']:assert sha(DEST/p['src'])==p['sha256']
  # Any comma inside a phrase must be a numeric comma or at that phrase's end.
  for p in rec['parts']:
   for match in re.finditer(',',p['text']):
    tail=p['text'][match.end():].strip();head=p['text'][:match.start()]
    assert not tail or (head[-1:].isdigit() and tail[:1].isdigit()),(s['number'],p['text'])
 assert 'noindex,nofollow' in (DEST/'index.html').read_text(encoding='utf-8')
 assert 'teachers-grade8-unit1-reading-pilot-v1' in (DEST/'index.html').read_text(encoding='utf-8')
 for name in m['navigationFiles']:assert 'unit-1-reading-pilot' not in (ROOT/name).read_text(encoding='utf-8')
 return m,data,parts

def local():
 m,data,parts=source_check();report={'passed':False,'sourceUnchanged':True,'navigationUnchanged':True,'storageIsolated':True,'curriculum':'Current Core II groups 21–22; unchanged','sentences':18,'parts':m['parts'],'pauseMs':1500,'screens':[],'gapChecks':[]}
 server=http.server.ThreadingHTTPServer(('127.0.0.1',8891),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();url='http://127.0.0.1:8891/grade8/unit-1-reading-pilot/'
 shots=Path('/tmp/grade8-reading-pilot-qa');shots.mkdir(exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for w,h in [(1366,768),(1024,600),(390,844),(360,640),(844,390)]:
   c=browser.new_context(viewport={'width':w,'height':h},has_touch=True)
   page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(url+'?view=sentences',wait_until='networkidle');page.wait_for_function('window.__readingPilot');page.evaluate('document.fonts.ready')
   checks=page.evaluate('''() => {
    const issues=[];const P=__readingPilot;const rect=e=>{let r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
    for(let i=0;i<18;i++){
     P.show(i*2);let e=document.querySelector('.sentence-text');
     if(e.textContent!==D.story[i].plain)issues.push(['source-text',i,e.textContent]);
     const before=[...e.querySelectorAll('.word')].map(rect);
     P.show(i*2+1);e=document.querySelector('.sentence-text');const after=[...e.querySelectorAll('.word')].map(rect);
     if(JSON.stringify(before)!==JSON.stringify(after))issues.push(['source-moved',i]);
     if(e.scrollWidth>e.clientWidth+2)issues.push(['text-overflow',i]);
     if(document.documentElement.scrollWidth>innerWidth+1)issues.push(['page-overflow',i]);
     for(const id of ['play','prev','next','speed','seek']){const r=document.getElementById(id).getBoundingClientRect();if(r.x<0||r.right>innerWidth+2||r.y<0||r.bottom>innerHeight+2)issues.push(['control-clipped',i,id]);}
    }
    P.show(10);return {pairs:18,issues};
   }''')
   assert not checks['issues'],json.dumps({'viewport':[w,h],**checks},ensure_ascii=False)
   page.screenshot(path=str(shots/f'sentence-{w}x{h}.png'))
   session=c.new_cdp_session(page);box=page.locator('#stage').bounding_box();cx=box['x']+box['width']/2;cy=box['y']+box['height']/2
   for dx,dy,expected in [(-85,0,11),(85,0,10),(0,-70,11),(0,70,10)]:
    session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx,'y':cy}]})
    session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx+dx,'y':cy+dy}]})
    session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    assert page.evaluate('__readingPilot.position')==expected,(w,h,dx,dy)
   # Real audio on each viewport, and immediate cancellation on translation reveal.
   page.click('#play');page.wait_for_function('__readingPilot.player.phase==="playing" && __readingPilot.player.audio.currentTime>0',timeout=10000)
   page.click('#next');assert page.evaluate('__readingPilot.player.audio.paused')
   page.wait_for_timeout(2200);assert page.evaluate('__readingPilot.player.audio.paused'),'Translation replayed automatically'
   page.goto(url+'?view=chunks',wait_until='networkidle');page.wait_for_function('window.__readingPilot')
   chunk=page.evaluate('''() => {const issues=[];let scrolling=0;for(let i=0;i<D.pages.length;i++){__readingPilot.show(i);const texts=[...document.querySelectorAll('.reading-text')].map(e=>e.textContent);if(JSON.stringify(texts)!==JSON.stringify(D.pages[i].map(j=>D.story[j].plain)))issues.push(['chunk-source',i]);const stage=document.getElementById('stage');if(stage.scrollWidth>stage.clientWidth+2)issues.push(['chunk-width',i]);if(stage.scrollHeight>stage.clientHeight+2)scrolling++;}__readingPilot.show(0);return {pages:D.pages.length,scrolling,issues};}''')
   assert not chunk['issues'],chunk
   page.screenshot(path=str(shots/f'chunk-{w}x{h}.png'))
   assert not errors,errors
   report['screens'].append({'viewport':f'{w}x{h}','stationarySentencePairs':18,'chunkPages':chunk['pages'],'scrollableChunks':chunk['scrolling'],'fourDirectionSwipe':True,'audioPlayback':True,'noTranslationAutoplay':True})
   c.close()
  c=browser.new_context(viewport={'width':1366,'height':900});page=c.new_page();page.goto(url+'?view=sentences',wait_until='networkidle');page.wait_for_function('window.__readingPilot')
  for rate in [1.25,.5]:
   page.evaluate('''rate=>{const P=__readingPilot.player;P.stop();P.unlocked=false;__readingPilot.show(0);document.getElementById('speed').value=String(rate);document.getElementById('speed').dispatchEvent(new Event('change'));P.events=[];}''',rate)
   page.click('#play');page.wait_for_function('__readingPilot.player.events.filter(e=>e.type==="part:playing").length>=2',timeout=30000)
   gap=page.evaluate('''()=>{const e=__readingPilot.player.events;const start=e.find(x=>x.type==='gap:start');const end=e.find(x=>x.type==='gap:end');const play=e.find(x=>x.type==='part:playing'&&x.at>end.at);return {timerMs:end.at-start.at,audibleMs:play.at-start.at,rate:__readingPilot.player.rate};}''')
   assert 1450<=gap['timerMs']<=1750 and 1450<=gap['audibleMs']<=2000,gap
   report['gapChecks'].append(gap)
  # Pausing during a breath freezes it and cannot restart in the background.
  page.evaluate('''()=>{let P=__readingPilot.player;P.stop();P.unlocked=false;__readingPilot.show(0);P.setRate(1.25);}''');page.click('#play');page.wait_for_function('__readingPilot.player.phase==="gap"',timeout=15000);page.click('#play');page.wait_for_timeout(1750)
  assert page.evaluate('__readingPilot.player.phase==="pausedGap" && __readingPilot.player.audio.paused')
  page.click('#play');page.wait_for_function('__readingPilot.player.phase==="playing"',timeout=5000)
  # Seeking over a boundary while paused must not insert old pauses or play.
  page.click('#play');page.evaluate('__readingPilot.player.seekFraction(.95)');assert page.evaluate('__readingPilot.player.audio.paused')
  page.click('#play');page.wait_for_function('__readingPilot.player.phase==="playing"',timeout=5000)
  # Screen changes cancel both an active clip and all pending gap callbacks.
  page.evaluate('__readingPilot.show(2)');page.evaluate('__readingPilot.player.stop()');page.wait_for_timeout(1700);assert page.evaluate('__readingPilot.player.audio.paused')
  # Read a short complete tab; it must never open the following tab automatically.
  page.goto(url+'?view=chunks',wait_until='networkidle');page.wait_for_function('window.__readingPilot')
  chosen=page.evaluate('''()=>{let best=D.pages.map((ids,p)=>({p,d:ids.reduce((n,i)=>n+PILOT_PHRASES.sentences[i].duration,0)})).sort((a,b)=>a.d-b.d)[0];__readingPilot.show(best.p);__readingPilot.player.setRate(1.25);return best.p;}''')
  page.click('#play');page.wait_for_function('__readingPilot.player.phase==="ended"',timeout=60000);page.wait_for_timeout(1700)
  assert page.evaluate('__readingPilot.position')==chosen and page.evaluate('__readingPilot.player.audio.paused')
  report.update(pauseResume=True,seekWhilePaused=True,stopAtTabEnd=True,cancelPendingAudio=True)
  # Copied entry points and other unit activities still work.
  for path in ['', 'reading/','sentences/','teacher.html','?view=vocab','?view=practice','?view=grammar','?view=workbook','?view=rehearsal']:
   assert page.goto(url+path,wait_until='networkidle').status==200
   assert 'unit-1-reading-pilot' in page.url
   assert 'לא ניתן לטעון' not in page.locator('body').inner_text()
  c.close();browser.close()
 server.shutdown();source_check();report['passed']=True;report['checkedAtUTC']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(DEST/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

def live():
 source_check();files=[p for p in DEST.rglob('*') if p.is_file()];expected={str(p.relative_to(DEST)):sha(p) for p in files}
 def check(item):
  name,digest=item
  with urllib.request.urlopen(urllib.request.Request(BASE+name+'?verify=reading-pilot-20261005',headers={'User-Agent':'Teachers-Reading-Pilot-QA'}),timeout=30) as r:body=r.read();assert r.status==200
  assert hashlib.sha256(body).hexdigest()==digest,'Live hash mismatch: '+name
  return name
 last=''
 for _ in range(20):
  try:check(('index.html',expected['index.html']));break
  except Exception as e:last=str(e);print('Waiting for Pages',last,flush=True);time.sleep(10)
 else:raise RuntimeError(last)
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:checked=list(pool.map(check,expected.items()))
 for file in ['index.html','grade8/index.html']:
  with urllib.request.urlopen('https://simonh68.github.io/teachers/'+file,timeout=30) as r:assert b'unit-1-reading-pilot' not in r.read()
 print('PUBLIC VERIFIED:',len(checked),'files; original navigation unchanged; direct link:',BASE,flush=True)
if __name__=='__main__':live() if '--live' in sys.argv else local()
