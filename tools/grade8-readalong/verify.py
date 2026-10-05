"""Regression tests for real Grade 8 sources; never weaken checks for publication."""
from __future__ import annotations
import functools,hashlib,http.server,json,threading,time,wave
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'grade8/read-along';SHOTS=Path('/tmp/grade8-readalong-qa');SHOTS.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.JSONDecoder().raw_decode(p.read_text().split('=',1)[1].lstrip())[0]
roll=json.loads((OUT/'ROLLOUT.json').read_text());D=js(ROOT/'grade8/unit-1/unit-data.js');A=js(OUT/'alignment.js');P=js(OUT/'phrase-data.js')
assert len(D['story'])==18 and len(D['words'])==110 and {w['group'] for w in D['words']}=={21,22}
assert digest(ROOT/'grade8/unit-1/unit-data.js')==roll['sourceSHA256']
assert digest(ROOT/'grade8/unit-1-reading-pilot/bilingual-sample/index.html')==roll['sourceSampleSHA256']
for s,r in zip(D['story'],P['sentences']):
 assert A[str(s['number'])]['plain']==s['plain'] and A[str(s['number'])]['he']==s['he']
 for part in r['parts']:
  f=OUT/part['src'];assert digest(f)==part['sha256']
  with wave.open(str(f)) as wav:assert abs(wav.getnframes()/wav.getframerate()-part['duration'])<.003
assert sum(len(r['parts']) for r in P['sentences'])==33
for f in ['reader.js','bootstrap.js','reader.css']:assert 'speechSynthesis' not in (OUT/f).read_text()
for f in ['index.html','grade8/index.html']:assert 'unit-1-reading-pilot' not in (ROOT/f).read_text(),'Pilot must stay unlisted'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8891),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
URL='http://127.0.0.1:8891/'
report={'passed':False,'standard':'grade8-bilingual-v1','sentences':18,'englishTokens':228,'hebrewSemanticUnits':150,'recordedAudioParts':33,'layout':[],'audio':[]}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for folder in ['unit-1','unit-1-reading-pilot']:
   for mode in ['sentences','chunks']:
    for w,h in [(1366,768),(1024,600),(390,844),(360,640),(844,390),(740,360)]:
     ctx=browser.new_context(viewport={'width':w,'height':h},has_touch=True,is_mobile=w<700)
     page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
     page.goto(URL+f'grade8/{folder}/?view={mode}',wait_until='networkidle');page.wait_for_function('window.__grade8Bilingual && __grade8Bilingual.ready');page.evaluate('document.fonts.ready')
     check=page.evaluate('''() => {
      const D=__grade8Bilingual;let seen=[],pairs=0,markers=0,issues=[];
      const rect=e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
      for(let p=0;p<D.pages.length;p++){
       D.show(p,false,{persist:false,schedule:false});
       if(getComputedStyle(document.getElementById('translation-slot')).visibility!=='hidden')issues.push(['early translation',p]);
       const en=document.getElementById('english'),nodes=[en,...en.querySelectorAll('[data-en]')],before=nodes.map(rect);
       D.show(p,true,{persist:false,schedule:false});
       if(en!==document.getElementById('english')||JSON.stringify(before)!==JSON.stringify(nodes.map(rect)))issues.push(['original moved',p]);
       if(getComputedStyle(document.getElementById('translation-slot')).visibility!=='visible')issues.push(['translation hidden',p]);
       for(const id of ['english','hebrew']){const el=document.getElementById(id),box=el.parentElement.getBoundingClientRect(),r=el.getBoundingClientRect();if(r.top<box.top-1||r.bottom>box.bottom+1||el.scrollWidth>el.clientWidth+1)issues.push(['text clipping',p,id,r.toJSON(),box.toJSON()]);}
       const ids=D.pages[p].ids;seen.push(...ids);
       if(en.textContent!==ids.map(i=>D.D.story[i].plain).join(' ')||document.getElementById('hebrew').textContent!==ids.map(i=>D.D.story[i].he).join(' '))issues.push(['source mismatch',p]);
       if(document.querySelector('details'))issues.push(['hidden reveal control',p]);
       for(const s of document.querySelectorAll('.reading span')){const c=getComputedStyle(s);if(parseFloat(c.borderLeftWidth)||parseFloat(c.borderRightWidth)||c.textDecorationLine!=='none')issues.push(['separator',p]);}
       for(const i of ids){const s=D.D.story[i];for(let n=0;n<s.tokens.length;n++){
        const t=s.tokens[n],part=D.records[i].parts.findIndex(x=>n>=x.firstToken&&n<=x.lastToken),seg=D.records[i].parts[part];
        D.player.sentence=i;D.player.part=part;D.player.queue=ids;D.player.phase='paused';D.player.offset=(t.start+t.end)/2-seg.sourceStart;D.player.onUpdate(D.player);
        const m=D.marker;if(m.en!==`${i}:${n}`||m.he!==`${i}:${D.alignment[s.number].map[n]}`)issues.push(['bad marker',i,n,m]);markers++;
        if(JSON.stringify(before)!==JSON.stringify(nodes.map(rect)))issues.push(['marker shifted original',i,n]);
       }}
       D.stop();pairs++;
      }
      if(JSON.stringify(seen)!==JSON.stringify(D.D.story.map((s,i)=>i)))issues.push(['incomplete coverage',seen]);
      if(document.documentElement.scrollWidth>innerWidth+1)issues.push(['page overflow']);
      D.show(0,false,{persist:false,schedule:false});return {pages:D.pages.length*2,pairs,markers,issues};
     }''')
     assert not check['issues'],json.dumps({'folder':folder,'mode':mode,'vp':[w,h],**check},ensure_ascii=False)
     assert check['markers']==228 and (mode!='sentences' or check['pairs']==18)
     if folder=='unit-1':
      page.evaluate('__grade8Bilingual.show(__grade8Bilingual.pages.findIndex(p=>p.ids.includes(10)),true,{schedule:false})');page.screenshot(path=str(SHOTS/f'{mode}-{w}x{h}.png'))
     page.evaluate('document.activeElement.blur();__grade8Bilingual.show(0,false,{schedule:false})')
     for key,result in [('ArrowDown',True),('ArrowUp',False),('ArrowRight',True),('ArrowLeft',False)]:page.keyboard.press(key);assert page.evaluate('__grade8Bilingual.reveal')==result
     session=ctx.new_cdp_session(page)
     for dx,dy,start,end in [(0,-80,False,True),(0,80,True,False),(-80,0,False,True),(80,0,True,False)]:
      page.evaluate('(r)=>__grade8Bilingual.show(0,r,{schedule:false})',start)
      box=page.locator('[data-en="0:4"]').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
      session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
      session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+dx,'y':y+dy}]})
      session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
      assert page.evaluate('__grade8Bilingual.reveal')==end,(folder,mode,w,h,dx,dy)
     page.evaluate('__grade8Bilingual.show(0,false,{schedule:false})');page.mouse.move(w/2,h/2);page.mouse.wheel(0,170);page.wait_for_timeout(80);assert page.evaluate('__grade8Bilingual.reveal')
     page.click('#contents');assert page.locator('#reading-menu').evaluate('(d)=>d.open');page.click('#sentence-list [data-jump="10"]');assert page.evaluate('__grade8Bilingual.pages[__grade8Bilingual.page].ids.includes(10)')
     assert not errors,errors
     report['layout'].append({'folder':folder,'mode':mode,'viewport':f'{w}x{h}','pages':check['pages'],'stationaryPairs':check['pairs'],'alignedTokenChecks':check['markers'],'clipping':False,'realTouchFourDirections':True,'keyboard':True,'wheel':True,'contents':True})
     print('LAYOUT PASS',folder,mode,w,h,flush=True)
     ctx.close()
  ctx=browser.new_context();page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for folder in ['unit-1','unit-1-reading-pilot']:
   for view in ['', '?view=vocab','?view=practice','?view=grammar','?view=teacher','?view=workbook']:
    page.goto(URL+f'grade8/{folder}/'+view,wait_until='networkidle');assert not page.evaluate('Boolean(window.__grade8Bilingual)')
    assert page.locator('#home' if not view else '#stage').inner_text().strip()
    assert len(page.evaluate('window.UNIT_DATA.words'))==110
   for alias,expected in [('reading/','chunks'),('sentences/','sentences')]:
    page.goto(URL+f'grade8/{folder}/'+alias,wait_until='networkidle');page.wait_for_function('window.__grade8Bilingual');assert page.evaluate('__grade8Bilingual.view')==expected
  assert not errors,errors
  report['legacyViewsPreserved']=True;report['aliasesPreserved']=True
  page.goto(URL+'grade8/unit-1/?view=sentences',wait_until='networkidle');page.wait_for_function('window.__grade8Bilingual');page.select_option('#speed','1.25')
  for i in range(18):
   for reveal in [False,True]:
    page.evaluate('([i,r])=>__grade8Bilingual.show(i,r,{schedule:false})',[i,reveal]);page.click('#replay')
    page.wait_for_function('__grade8Bilingual.player.phase==="playing" && __grade8Bilingual.player.sourceTime>.15',timeout=10000)
    assert page.evaluate('__grade8Bilingual.player.sentence')==i
    page.evaluate('__grade8Bilingual.stop()')
  report['all36SentenceSlidesPlay']=True
  for speed in ['0.5','1.25']:
   page.evaluate('__grade8Bilingual.show(10,true,{schedule:false});__grade8Bilingual.player.events=[]');page.select_option('#speed',speed);page.click('#replay')
   page.wait_for_function('__grade8Bilingual.player.phase==="playing" && __grade8Bilingual.player.sourceTime>.3');page.screenshot(path=str(SHOTS/f'marker-active-{speed}.png'))
   page.wait_for_function('__grade8Bilingual.player.phase==="ended"',timeout=50000)
   events=page.evaluate('__grade8Bilingual.player.events');gaps=[]
   for n,e in enumerate(events):
    if e['type']=='gap:start':
     end=next(x for x in events[n+1:] if x['type']=='gap:end');start=next(x for x in events[n+1:] if x['type']=='part:playing')
     gap=end['at']-e['at'];audible=start['at']-e['at'];assert 1490<=gap<=1720 and 1490<=audible<=1900,(gap,audible)
     gaps.append({'timerMs':round(gap,1),'audibleGapMs':round(audible,1)})
   assert len(gaps)==3 and page.evaluate('__grade8Bilingual.reveal')
   report['audio'].append({'speed':speed,'sentence':11,'gaps':gaps})
  for revealed in [False,True]:
   page.evaluate('(r)=>__grade8Bilingual.show(10,r)',revealed);page.wait_for_timeout(1000);assert page.evaluate('__grade8Bilingual.player.audio.paused')
   page.wait_for_function('__grade8Bilingual.player.phase==="playing"',timeout=3000)
   page.click('#contents');assert page.evaluate('__grade8Bilingual.player.audio.paused');page.click('#close-menu')
  page.evaluate('__grade8Bilingual.show(10,true,{schedule:false})');page.click('#replay');page.wait_for_function('__grade8Bilingual.player.phase==="gap"',timeout=15000);page.click('#play')
  assert page.evaluate('__grade8Bilingual.player.phase')=='pausedGap';part=page.evaluate('__grade8Bilingual.player.part');page.wait_for_timeout(1700);assert page.evaluate('__grade8Bilingual.player.part')==part
  page.click('#play');page.wait_for_function('__grade8Bilingual.player.part>0',timeout=5000);page.evaluate('__grade8Bilingual.stop()')
  assert page.evaluate('__grade8Bilingual.player.audio.paused')
  page.select_option('#speed','0.5');page.reload(wait_until='networkidle');page.wait_for_function('window.__grade8Bilingual');assert page.locator('#speed').input_value()=='0.5' and page.evaluate('__grade8Bilingual.player.rate')==.5
  report['twoSecondDelayBothStates']=True;report['pauseResume']=True;report['stopOnNavigationAndMenu']=True;report['speedPersistence']=True
  page.goto(URL+'grade8/unit-1/?view=chunks&p=9&reveal=1',wait_until='networkidle');page.wait_for_function('window.__grade8Bilingual');page.select_option('#speed','1.25');page.click('#play');old=page.evaluate('__grade8Bilingual.page')
  page.wait_for_function('__grade8Bilingual.player.phase==="ended"',timeout=40000);assert page.evaluate('__grade8Bilingual.page')==old and page.evaluate('__grade8Bilingual.reveal')
  report['chunkStopsWithoutAdvance']=True
  ctx2=browser.new_context();ctx2.add_init_script('Storage.prototype.getItem=function(){throw new Error("blocked")};Storage.prototype.setItem=function(){throw new Error("blocked")};');q=ctx2.new_page();q.goto(URL+'grade8/unit-1/?view=sentences',wait_until='networkidle');q.wait_for_function('window.__grade8Bilingual');assert q.locator('#speed').input_value()=='0.75';ctx2.close()
  report['blockedStorage']=True;browser.close()
 server.shutdown();report['passed']=True
except Exception as e:
 report['error']=str(e)
 raise
finally:
 report['checkedAtUTC']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
 (OUT/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 (SHOTS/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
