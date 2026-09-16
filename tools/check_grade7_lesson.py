"""Validate the actual lesson files and public deployment, not a demo fixture."""
import functools, hashlib, http.server, json, os, threading, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'grade7/band2-groups-01-02'
entries=json.loads((OUT/'entries.json').read_text(encoding='utf-8'))
manifest=json.loads((OUT/'audio-manifest.json').read_text(encoding='utf-8'))
assert len(entries)==manifest['count']==110
for e in entries:
    c=manifest['clips'][e['id']]
    assert c['text']==e['word'].rstrip('.!?')+'. '+e['sentence'], e['id']
    f=OUT/c['src']
    assert f.stat().st_size>1000 and hashlib.sha256(f.read_bytes()).hexdigest()==c['sha256']
assert 'speechSynthesis' not in (OUT/'lesson.js').read_text()
server=http.server.ThreadingHTTPServer(('127.0.0.1',8877),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
result={'entries':110,'vocabulary_slides':220,'breaks':36,'total_slides':259,'audio_files':110,'browser_tts':False,'checks':[]}
URL='http://127.0.0.1:8877/grade7/band2-groups-01-02/'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for w,h,mobile in [(1366,768,False),(390,844,True),(844,390,True)]:
        context=browser.new_context(viewport={'width':w,'height':h},has_touch=mobile,is_mobile=mobile)
        page=context.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        assert page.goto(URL,wait_until='networkidle').status==200
        page.wait_for_function('window.__lessonTest && window.__lessonTest.audio.ready')
        state=page.evaluate('''() => {
          const t=window.__lessonTest;
          let run=0,breaks=0;
          for (const s of t.slides) {
            if(s.type==='word')run++;
            if(s.type==='break'){if(run!==6)throw Error('Wrong break cadence: '+run);run=0;breaks++}
          }
          if(breaks!==36||run!==4||t.slides.length!==259)throw Error('Wrong complete lesson count');
          const rect=el=>{let r=el.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(x=>Math.round(x*100)/100)};
          let overflow=[],shifts=[],pairs=0;
          for(let i=0;i<t.slides.length;i++){
            const s=t.slides[i];
            if(s.type!=='word'||s.reveal)continue;
            t.show(i,false);
            const original=document.querySelector('.sentence-line');
            const word=document.querySelector('.word-line');
            const before=[rect(original),rect(word)];
            t.show(i+1,false);
            if(original!==document.querySelector('.sentence-line')||JSON.stringify(before)!==JSON.stringify([rect(original),rect(word)]))shifts.push(s.entry.id);
            for(const el of document.querySelectorAll('[data-fit]'))if(el.scrollHeight>el.clientHeight+2||el.scrollWidth>el.clientWidth+2)overflow.push([s.entry.id,el.className,el.scrollHeight,el.clientHeight]);
            pairs++;
          }
          if(shifts.length)throw Error('Source moved: '+JSON.stringify(shifts));
          if(overflow.length)throw Error('Text clipped: '+JSON.stringify(overflow));
          if(document.documentElement.scrollWidth>innerWidth+1)throw Error('Horizontal overflow');
          t.show(2,false);return{pairs,breaks,slides:t.slides.length};
        }''')
        page.keyboard.press('ArrowDown');assert page.evaluate('__lessonTest.index')==3
        page.keyboard.press('ArrowUp');assert page.evaluate('__lessonTest.index')==2
        page.keyboard.press('ArrowRight');assert page.evaluate('__lessonTest.index')==3
        page.keyboard.press('ArrowLeft');assert page.evaluate('__lessonTest.index')==2
        page.mouse.move(w//2,h//2);page.mouse.wheel(0,160);page.wait_for_timeout(100)
        assert page.evaluate('__lessonTest.index')==3
        if mobile:
            session=context.new_cdp_session(page)
            cx,cy=w//2,h//2
            for dx,dy,expected in [(0,-85,3),(0,85,2),(-85,0,3),(85,0,2)]:
                if expected==3:page.evaluate('__lessonTest.show(2,false)')
                else:page.evaluate('__lessonTest.show(3,false)')
                session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx,'y':cy}]})
                session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx+dx,'y':cy+dy}]})
                session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
                assert page.evaluate('__lessonTest.index')==expected,(dx,dy)
        page.evaluate('__lessonTest.show(2,false)')
        page.click('#audioToggle')
        page.wait_for_function('!__lessonTest.audio.paused',timeout=10000)
        page.evaluate('__lessonTest.navigate(1)')
        assert page.evaluate('__lessonTest.audio.paused')
        page.evaluate('__lessonTest.show(4,false)')
        page.wait_for_timeout(1000)
        assert page.evaluate('__lessonTest.audio.paused'), 'Audio started before delay'
        page.wait_for_function('!__lessonTest.audio.paused',timeout=7000)
        page.evaluate('__lessonTest.show(8,false)')
        assert page.evaluate('__lessonTest.audio.paused'), 'Audio leaked into break'
        assert not errors,errors
        result['checks'].append({'viewport':f'{w}x{h}','pairs_stationary':state['pairs'],'no_text_clipping':True,'arrow_keys':True,'wheel':True,'four_direction_touch':mobile,'real_audio_playback':True,'audio_stops_on_navigation':True,'two_second_auto_delay':True})
        context.close()
    browser.close()
server.shutdown()
# Verify the actual public URL and all runtime assets. Wait for GitHub Pages, never invent a link.
base='https://simonh68.github.io/teachers/grade7/band2-groups-01-02/'
expected={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in ['index.html','lesson.css','lesson.js','visuals.js','entries.json','audio-manifest.json']}
last=''
for attempt in range(24):
    try:
        verified={}
        for name,digest in expected.items():
            req=urllib.request.Request(base+name+'?qa='+str(int(time.time())),headers={'User-Agent':'Teachers-Public-Verification/1.0'})
            with urllib.request.urlopen(req,timeout=30) as response:
                payload=response.read();assert response.status==200
            assert hashlib.sha256(payload).hexdigest()==digest,'Outdated deployment: '+name
            verified[name]='HTTP 200; exact content hash'
        for key in ['g01-01','g02-55']:
            clip=manifest['clips'][key]
            with urllib.request.urlopen(base+clip['src'],timeout=30) as response:
                payload=response.read();assert response.status==200
            assert hashlib.sha256(payload).hexdigest()==clip['sha256']
            verified[key]='Public MP3 HTTP 200; exact audio hash'
        result['public_url']=base
        result['public_checks']=verified
        break
    except Exception as e:
        last=str(e);print('Waiting for public deployment:',last,flush=True);time.sleep(15)
else:
    result['public_verification_error']=last
result['passed']=bool(result.get('public_checks'))
result['timestamp_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
(OUT/'qa-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
if not result['passed']:raise SystemExit('Local QA passed; public deployment not yet verified')
