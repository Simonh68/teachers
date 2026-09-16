"""Validate the complete published HTML sequence, not a mock or a demo."""
import functools, http.server, json, pathlib, threading
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
LESSON = ROOT / 'grade7/band2-groups-01-02'
source = (LESSON/'data.js').read_text(encoding='utf-8')
words = json.loads(source.split('=',1)[1].strip().rstrip(';'))
assert len(words) == 110
manifest = json.loads((LESSON/'audio/manifest.json').read_text(encoding='utf-8'))
assert len(manifest['files']) == 110
for w in words:
    c = manifest['files'][w['id']]
    assert c['text'] == w['en'].rstrip('.!?') + '. ' + w['ex_en']
    path = LESSON / c['src']
    assert path.is_file() and path.stat().st_size > 1000
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
server = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
report = {'entries':110, 'audioFiles':110, 'viewports':[]}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width,height in [(1366,768),(1024,600),(390,844),(844,390),(360,640)]:
        context = browser.new_context(viewport={'width':width,'height':height}, has_touch=True)
        page = context.new_page()
        errors=[]
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('http://127.0.0.1:8765/grade7/band2-groups-01-02/full.html', wait_until='networkidle')
        page.wait_for_function('window.TeachersDeck && !document.getElementById("sound").disabled')
        page.evaluate('document.fonts.ready')
        result = page.evaluate('''() => {
            const D=TeachersDeck; let issues=[],pairs=0,between=0,breaks=0;
            for(let i=0;i<D.slides.length;i++){
                const s=D.slides[i];
                if(s.type==='break'){if(between!==6)issues.push(['break-spacing',i,between]);between=0;breaks++;D.show(i);const a=document.querySelector('.break-en').getBoundingClientRect().toJSON();D.next();const b=document.querySelector('.break-en').getBoundingClientRect().toJSON();if(JSON.stringify(a)!==JSON.stringify(b))issues.push(['break-drift',i]);continue;}
                if(s.type!=='word')continue;between++;
                if(s.reveal)continue;
                D.show(i);let a=[...document.querySelectorAll('[data-original]')].map(e=>e.getBoundingClientRect().toJSON());
                D.next();let b=[...document.querySelectorAll('[data-original]')].map(e=>e.getBoundingClientRect().toJSON());
                if(JSON.stringify(a)!==JSON.stringify(b))issues.push(['drift',s.word.id]);
                const screen=document.querySelector('.screen').getBoundingClientRect();
                for(const e of document.querySelectorAll('.word,.example,.meaning,.translation')){let r=e.getBoundingClientRect();if(r.top<screen.top-1||r.bottom>screen.bottom+1||e.scrollWidth>e.clientWidth+1)issues.push(['overflow',s.word.id,e.className]);}
                pairs++;
            }
            return {slides:D.slides.length,pairs,breaks,issues};
        }''')
        assert result['pairs']==110 and result['breaks']==36 and result['slides']==261, result
        assert not result['issues'], result['issues']
        gestures=page.evaluate('''() => {TeachersDeck.show(3);const out=[];for(const [x,y,ex,ey] of [[170,350,60,350],[60,350,170,350],[170,350,170,180],[170,180,170,350]]){const s=document.getElementById('stage');s.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerType:'touch',pointerId:1,clientX:x,clientY:y}));s.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerType:'touch',pointerId:1,clientX:ex,clientY:ey}));out.push(TeachersDeck.current);}return out;}''')
        assert gestures==[4,3,4,3], gestures
        page.evaluate('TeachersDeck.show(3)')
        for key,expected in [('ArrowRight',4),('ArrowLeft',3),('ArrowDown',4),('ArrowUp',3)]:
            page.keyboard.press(key)
            assert page.evaluate('TeachersDeck.current')==expected
        page.click('#replay')
        page.wait_for_function('TeachersDeck.audio.currentTime > 0',timeout=15000)
        page.keyboard.press('ArrowRight')
        assert page.evaluate('TeachersDeck.audio.paused')
        assert not errors, errors
        report['viewports'].append({'width':width,'height':height,**result,'swipes':gestures,'audioPlayback':True})
        print('PASS',width,height,result,flush=True)
        context.close()
    browser.close()
server.shutdown()
(ROOT/'grade7-sequence-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 110 real entries; 220 fixed reveal slides; 36 correctly spaced breaks; four-way swipes; actual MP3 playback.',flush=True)
