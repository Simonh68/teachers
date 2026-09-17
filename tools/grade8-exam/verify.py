"""Real-browser tests against the final H8 lesson; public verification after deployment."""
from pathlib import Path
from urllib.request import Request,urlopen
import concurrent.futures, functools, hashlib, http.server, json, sys, threading, time
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'grade8/exam-01-preparation';BASE='https://simonh68.github.io/teachers/grade8/exam-01-preparation/'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def local():
 from playwright.sync_api import sync_playwright
 data=read(OUT/'lesson.json');m=read(OUT/'audio-manifest.json')
 assert len(data['words'])==55 and len(data['story'])==18 and len(data['questions'])==7 and len(data['translations'])==6
 assert sum(q['level']=='basic' for q in data['questions'])==4
 assert m['count']==73 and not m['browserTTS']
 assert 'speechSynthesis' not in (OUT/'exam.js').read_text()
 for x in data['words']+data['story']:
  text=x['en'].rstrip('.!?')+'. '+x['ex_en'] if 'ex_en'in x else x['plain'];c=m['clips'][x['id']]
  assert c['text']==text and sha(OUT/c['src'])==c['sha256']
 handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
 server=http.server.ThreadingHTTPServer(('127.0.0.1',8893),handler);threading.Thread(target=server.serve_forever,daemon=True).start()
 report={'passed':False,'words':55,'storySentences':18,'basicQuestions':4,'comprehensionQuestions':3,'translationExercises':6,'audioClips':73,'checks':[]}
 shots=Path('/tmp/h8-qa');shots.mkdir(exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for w,h in [(1366,768),(1024,600),(390,844),(844,390),(360,640)]:
   ctx=browser.new_context(viewport={'width':w,'height':h},has_touch=True,is_mobile=w<900)
   page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('http://127.0.0.1:8893/grade8/exam-01-preparation/',wait_until='networkidle')
   page.wait_for_function('window.ExamDeck && ExamDeck.ready');page.evaluate('document.fonts.ready')
   check=page.evaluate('''()=>{
    const D=ExamDeck;let run=0,breaks=0,pairs=0,issues=[];
    const bounds=()=>[...document.querySelectorAll('[data-original]')].map(el=>{const r=el.getBoundingClientRect();return [r.x,r.y,r.width,r.height,getComputedStyle(el).fontSize,el.textContent]});
    if(D.pages.length!==235)throw Error('Wrong number of slides '+D.pages.length);
    for(let i=0;i<D.pages.length;i++){
      const s=D.pages[i];
      if(s.type==='word')run++;
      if(s.type==='break'&&s.group==='vocab'&&s.phase===0){if(run!==6)issues.push(['break spacing',i,run]);run=0;breaks++;}
      D.show(i,false);
      if(s.phase===0&&['word','story','question','break','translation'].includes(s.type)){
        const a=JSON.stringify(bounds());D.show(i+1,false);if(a!==JSON.stringify(bounds()))issues.push(['source moved',i,s.key]);pairs++;
      }
      if(s.type==='question'){
        D.show(i,false);const ans=document.querySelector('.answer');
        if(s.phase<2&&getComputedStyle(ans).visibility!=='hidden')issues.push(['answer leaked',i]);
        if(s.phase===3&&document.querySelector('.ahe').getAttribute('aria-hidden')!=='false')issues.push(['missing answer translation',i]);
      }
      const frame=document.querySelector('.sheet').getBoundingClientRect();
      for(const el of document.querySelectorAll('[data-fit]')){
       const child=el.firstElementChild,r=el.getBoundingClientRect();
       if(child.scrollHeight>el.clientHeight+2||child.scrollWidth>el.clientWidth+2||r.bottom>frame.bottom+2||r.top<frame.top-2)issues.push(['clipping',i,el.className,child.scrollHeight,el.clientHeight]);
      }
      if(document.querySelector('.intro'))for(const el of document.querySelectorAll('.intro h1,.intro h2,.intro p,.intro nav')){const r=el.getBoundingClientRect();if(r.top<frame.top-1||r.bottom>frame.bottom+1)issues.push(['intro clipped',i,el.textContent]);}
    }
    if(breaks!==18||run!==2)issues.push(['vocabulary count',breaks,run]);
    return{pages:D.pages.length,pairs,breaks,issues};
   }''')
   assert not check['issues'],json.dumps({'viewport':[w,h],'issues':check['issues']},ensure_ascii=False)
   page.evaluate('ExamDeck.show(4,false)')
   for k,n in [('ArrowRight',5),('ArrowLeft',4),('ArrowDown',5),('ArrowUp',4)]:
    page.keyboard.press(k);assert page.evaluate('ExamDeck.current')==n
   session=ctx.new_cdp_session(page);cx=w//2;cy=h//2
   for dx,dy,start,expected in [(-85,0,4,5),(85,0,5,4),(0,-85,4,5),(0,85,5,4)]:
    page.evaluate(f'ExamDeck.show({start},false)')
    session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx,'y':cy}]})
    session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx+dx,'y':cy+dy}]})
    session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    assert page.evaluate('ExamDeck.current')==expected,('swipe',w,h,dx,dy)
   page.evaluate('ExamDeck.show(4,false)');page.mouse.move(cx,cy);page.mouse.wheel(0,150);page.wait_for_timeout(100);assert page.evaluate('ExamDeck.current')==5
   page.evaluate('ExamDeck.show(4,false)');page.click('#sound');page.wait_for_function('ExamDeck.player.currentTime>0',timeout=10000)
   page.keyboard.press('ArrowRight');assert page.evaluate('ExamDeck.player.paused')
   page.keyboard.press('ArrowRight');page.wait_for_timeout(750);assert page.evaluate('ExamDeck.player.paused')
   page.wait_for_function('!ExamDeck.player.paused',timeout=6500)
   page.evaluate("ExamDeck.show(ExamDeck.pages.findIndex(p=>p.type==='story'&&p.phase===0),false)");page.click('#replay');page.wait_for_function('ExamDeck.player.currentTime>0',timeout=10000)
   page.click('#contents');assert page.evaluate('ExamDeck.player.paused');page.click('.close')
   page.evaluate("ExamDeck.show(ExamDeck.pages.findIndex(p=>p.type==='break'),false)");assert page.evaluate('ExamDeck.player.paused')
   if w in (1366,390):
    for name,expression in [('opening','0'),('word','4'),('word-reveal','5'),('story',"ExamDeck.pages.findIndex(p=>p.type==='story')"),('story-reveal',"ExamDeck.pages.findIndex(p=>p.type==='story')+1"),('break',"ExamDeck.pages.findIndex(p=>p.type==='break')"),('question',"ExamDeck.pages.findIndex(p=>p.type==='question')+3")]:
     page.evaluate(f'ExamDeck.show({expression},false)');page.screenshot(path=str(shots/f'{w}-{name}.png'))
   assert not errors,errors
   report['checks'].append({'viewport':f'{w}x{h}','pages':check['pages'],'stationarySequences':check['pairs'],'textClipping':False,'fourDirectionTouch':True,'keyboard':True,'wheel':True,'vocabularyAudio':True,'storyAudio':True,'twoSecondDelay':True,'stopOnNavigation':True,'answerNotPremature':True})
   ctx.close()
  browser.close()
 server.shutdown();report['passed']=True;report['checkedAtUTC']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());write=OUT/'qa-report.json';write.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('LOCAL QA PASS',json.dumps(report,ensure_ascii=False),flush=True)

def live():
 paths=['index.html','exam.css','exam.js','visuals.js','lesson.json','audio-manifest.json','teacher.html','qa-report.json']
 expected={n:sha(OUT/n) for n in paths}
 def get(path):
  with urlopen(Request(BASE+path+'?verify='+str(int(time.time())),headers={'User-Agent':'Teachers-H8-Live-QA'}),timeout=30) as r:
   assert r.status==200;return r.read()
 for attempt in range(20):
  try:
   for n,d in expected.items():assert hashlib.sha256(get(n)).hexdigest()==d,'Public version not current: '+n
   break
  except Exception as e:
   print('Waiting for deployment:',e,flush=True)
   if attempt==19:raise
   time.sleep(10)
 m=read(OUT/'audio-manifest.json')
 def one(c):assert hashlib.sha256(get(c['src'])).hexdigest()==c['sha256'];return True
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:assert all(pool.map(one,m['clips'].values()))
 print('LIVE VERIFIED:',BASE,'exact source hashes and all 73 MP3 files HTTP 200.',flush=True)

if __name__=='__main__':live() if '--live'in sys.argv else local()
