"""Build Grade 9 Read Alone from the existing, unmodified story and translations.
Requires verified audio.json from grade9_read_alone_audio.py. Idempotent.
"""
from pathlib import Path
import copy, hashlib, html, json, re, shutil, urllib.request
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]; T=R/'tools/grade9-readalone'; U=R/'grade9/unit-1'; O=U/'read-alone'
W=re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*|[0-9]+")
def norm(x):return re.sub('[^a-z0-9]','',x.lower())
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def wordhtml(s):return ''.join(html.escape(w['prefix'])+'<span class="ra-word ra-hit" role="button" tabindex="0" data-w="'+str(w['index'])+'" data-he="'+html.escape(w['he'],quote=True)+'" aria-label="'+html.escape(w['word'],quote=True)+' — פירוש">'+html.escape(w['word'])+'</span>' for w in s['words'])+html.escape(s['suffix'])
def main():
 O.mkdir(parents=True,exist_ok=True);(O/'assets').mkdir(exist_ok=True)
 audio=json.loads((O/'audio.json').read_text());assert len(audio['sentences'])==46
 assert hashlib.sha256((O/'assets/story.mp3').read_bytes()).hexdigest()==audio['sha256']
 soup=BeautifulSoup((U/'reading.html').read_text(),'html.parser');original=[]
 for node in soup.select('.story .sentence'):
  node.select_one('.sid').extract();original.append(node.get_text().strip())
 tr=json.loads((T/'translations.json').read_text());assert len(original)==len(tr)==46
 sentences=[];global_index=0
 for i,(en,translation,a) in enumerate(zip(original,tr,audio['sentences'])):
  assert en==a['en'],('source differs',i+1)
  matches=list(W.finditer(en));assert len(matches)==len(a['words'])
  word_gloss=[];units=[];cursor=0
  for u in translation['u']:
   expected=W.findall(u[0]);assert [norm(x.group()) for x in matches[cursor:cursor+len(expected)]]==list(map(norm,expected)),('unit mismatch',i+1,u[0])
   gloss=u[2].split('|') if len(u)>2 else [u[1]]
   assert len(gloss)==len(expected),('gloss mismatch',i+1,u)
   units.append({'en':u[0],'he':u[1],'first':cursor,'last':cursor+len(expected)-1});word_gloss+=gloss;cursor+=len(expected)
  assert cursor==len(matches),('untranslated words',i+1)
  words=[];pos=0
  for j,(match,he,timing) in enumerate(zip(matches,word_gloss,a['words'])):
   assert norm(match.group())==norm(timing['word'])
   words.append({'word':match.group(),'he':he,'prefix':en[pos:match.start()],'index':global_index,'start':timing['start'],'end':timing['end']})
   timing['index']=global_index;global_index+=1;pos=match.end()
  row={'id':i+1,'en':en,'he':translation['he'],'words':words,'units':units,'suffix':en[pos:]};assert ''.join(w['prefix']+w['word'] for w in words)+row['suffix']==en;sentences.append(row)
 pages=[];page=[];nwords=0
 for n,s in enumerate(sentences):
  if page and (len(page)>=3 or nwords+len(s['words'])>25 or n in [10,24,36]):pages.append(page);page=[];nwords=0
  page.append(n);nwords+=len(s['words'])
 if page:pages.append(page)
 assert [n for p in pages for n in p]==list(range(46))
 image=O/'assets/library.webp'
 if not image.exists():
  from PIL import Image
  import io
  url='https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=960&auto=format&fit=crop&q=82'
  raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Teachers educational reading resource'}),timeout=45).read()
  im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((1000,1000));im.save(image,'WEBP',quality=84)
 content={'version':'20260922-ra1','title':'The Message Without a Voice','sentences':sentences,'pages':pages,'image':'assets/library.webp','imageCredit':{'source':'https://unsplash.com/photos/a-book-shelf-filled-with-lots-of-books-sfL_QOnmy00','file':'https://images.unsplash.com/photo-1507842217343-583bb7270b66','description':'Static library illustration, not a photograph of the fictional characters.'},'wordCount':global_index,'source_sha256':audio['source_sha256']}
 dump(O/'content.json',content);dump(O/'audio.json',audio)
 js=(T/'player.js').read_text()
 # Stop timers reliably, give repeats their own stop boundary, and stop other tabs.
 js=js.replace('clearTimeout(timer); cancelAnimationFrame(frame);','clearTimeout(timer); timer = 0; cancelAnimationFrame(frame);')
 js=js.replace("let standalone = false, deck = false, loading = true;", "let standalone = false, deck = false, loading = true, repeatEnd = null; const tabId = Math.random().toString(36).slice(2); let broadcast; try { broadcast = new BroadcastChannel('teachers-read-alone-audio-v1'); broadcast.onmessage = e => { if(e.data !== tabId) stop(); }; } catch (_) {}")
 js=js.replace('function range(ids) { stop();', 'function range(ids) { repeatEnd = null; stop();')
 js=js.replace('if (clip && audio.currentTime >= clip.end + .015) { finished(); return; }', "if (repeatEnd !== null && audio.currentTime >= repeatEnd + .015) { audio.currentTime = repeatEnd; repeatEnd = null; stop(); status('סיום המשפט. לחצו להמשך הקטע.'); return; } if (clip && audio.currentTime >= clip.end + .015) { finished(); return; }")
 js=js.replace('try { await audio.play();', "try { broadcast?.postMessage(tabId); await audio.play();")
 js=js.replace("audio.currentTime = Math.max(0,timing.sentences[id].start - .015); play();", "repeatEnd = timing.sentences[id].end; audio.currentTime = Math.max(0,timing.sentences[id].start - .015); play();")
 js=js.replace("$('#raSeek').oninput = e => { if (clip) {", "$('#raSeek').oninput = e => { clearTimeout(timer); timer = 0; repeatEnd = null; if (clip) {")
 # Do not initiate narration merely because a stored page was restored.
 js=js.replace("let standalone = false, deck = false, loading = true, repeatEnd = null;", "let interacted = false; document.addEventListener('pointerdown',()=>interacted=true,{once:true}); document.addEventListener('keydown',()=>interacted=true,{once:true}); let standalone = false, deck = false, loading = true, repeatEnd = null;")
 js=js.replace('function auto() { const token', 'function auto() { if(!interacted)return; const token')
 # Expose deterministic navigation for testing, not student data.
 js=js.replace('window.TeachersReadAlone = {stop,', "window.TeachersReadAlone = {stop, setPage(n,m='text'){mode=m;if(m==='text')page=n;else sentenceSlide=n;render();}, get mode(){return mode;}, get page(){return page;}, get sentenceSlide(){return sentenceSlide;},")
 # Fit each page; translations reserve the same space on both sentence slides.
 fit="""function fitReading(){if(!standalone)return;const panel=$('#raPanel'), text=$('#raText');if(!panel||!text)return;let size=mode==='text'?(innerWidth<760?25:36):(innerWidth<760?29:49);text.style.fontSize=size+'px';while(panel.scrollHeight>panel.clientHeight+2&&size>20){size--;text.style.fontSize=size+'px';}} window.addEventListener('resize',fitReading);\n"""
 js=js.replace('function savePosition()',fit+'function savePosition()')
 js=js.replace('range(ids); savePosition();', 'range(ids); savePosition(); fitReading(); requestAnimationFrame(fitReading);')
 (O/'player.js').write_text(js)
 css=(T/'reader.css').read_text()+'''\n/* Keep navigation outside the reading viewport on small phones. */
.ra-page{height:100dvh;overflow:hidden}.ra-page #raApp{height:100%;display:flex;flex-direction:column;min-height:0}.ra-page .ra-header,.ra-page .ra-title,.ra-page .ra-subtitle,.ra-page .ra-modes,.ra-page #raTabs,.ra-page #raControls,.ra-page .ra-nav,.ra-page #raProgress,.ra-page .ra-meta{flex-shrink:0}.ra-page #raPanel{flex:1;min-height:0;overflow:auto;overscroll-behavior:contain;touch-action:pan-y}.ra-page #raFullTranslation{position:fixed;bottom:160px;left:5%;right:5%;max-height:35vh;z-index:30;border:2px solid #92c8d6}.ra-page .ra-title{font-size:clamp(20px,2.6vw,32px);margin:8px 0 4px}.ra-page .ra-subtitle{margin:0 0 4px}.ra-page .ra-modes{margin:6px 0}.ra-page #raProgress{margin:5px 0}.ra-page .ra-meta{margin-top:3px}.ra-page .ra-toolbar{padding-top:7px}.ra-page #raPanel{padding:18px 24px}.ra-page .ra-sentence-card{gap:18px}.ra-page #raTip{pointer-events:none}
@media(max-width:760px){.ra-page #raApp{padding:8px 12px}.ra-page .ra-subtitle{display:none}.ra-page #raPanel{padding:12px 14px}.ra-page .ra-title{font-size:21px}.ra-page .ra-modes button{min-height:34px}.ra-page #raCounter{font-size:10px}.ra-page .ra-toolbar{padding-top:6px}.ra-page .ra-meta small{font-size:9px}.ra-page .ra-translation{font-size:20px;line-height:1.45}.ra-page .ra-sentence-card{gap:13px}}
@media(max-height:600px){.ra-page .ra-meta,.ra-page .ra-subtitle{display:none}.ra-page .ra-header{font-size:11px;min-height:23px}.ra-page .ra-title{font-size:19px;margin:4px 0}.ra-page .ra-modes{margin:4px 0}.ra-page #raPanel{padding:10px}.ra-page .ra-toolbar{padding:4px 0}.ra-page #raStatus{min-height:14px}}
'''
 (O/'reader.css').write_text(css)
 pagehtml='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#081423"><title>The Message Without a Voice · Read Alone · כיתה ט׳</title><link rel="stylesheet" href="reader.css?v=20260922-ra1"><script defer src="player.js?v=20260922-ra1"></script></head><body class="ra-page"><main id="raApp"><header class="ra-header"><a class="ra-home" href="../../../#grade9" aria-label="חזרה לכיתה ט׳">⌂</a><a href="../">Unit 1 · כיתה ט׳</a><a href="../../the-message-without-a-voice/">המצגת המלאה</a></header><h1 class="ra-title" lang="en">The Message Without a Voice</h1><p class="ra-subtitle">קריאה, הקראה מוקלטת ותרגום · קבוצות 21–23</p><nav class="ra-modes" aria-label="סוג הקריאה"><button class="ra-mode" data-mode="text" aria-pressed="true">Read Alone Text · קטעים</button><button class="ra-mode" data-mode="sentences" aria-pressed="false">מילה־במילה · משפט בשקף</button></nav><div id="raTabs" role="tablist" aria-label="חלקי הסיפור"></div><section id="raPanel" aria-label="טקסט הקריאה"><p>טוען את הסיפור…</p></section><div id="raControls"></div><nav class="ra-nav" aria-label="ניווט בקריאה"><button id="raPrev">→ הקודם</button><output id="raCounter" aria-live="polite"></output><button id="raNext">המשך ←</button></nav><progress id="raProgress" max="1" value="0" aria-label="התקדמות בקריאה"></progress><div class="ra-meta"><button id="raReveal">תרגום הקטע</button><small>נוצר: י״א בתשרי תשפ״ז · 22.9.2026<br>קריינות סינתטית מוקלטת. ההתקדמות והמהירות נשמרות במכשיר בלבד.</small><a href="../practice.html#reading-questions">שאלות וראיות</a></div><div id="raFullTranslation" lang="he" dir="rtl" hidden></div></main></body></html>'''
 (O/'index.html').write_text(pagehtml)
 # Preserve the original full teaching deck, adding a translation slide after each sentence.
 deckpath=R/'grade9/the-message-without-a-voice/index.html'; backup=T/'original-deck.html'
 if not backup.exists():shutil.copyfile(deckpath,backup)
 deck=BeautifulSoup(backup.read_text(),'html.parser');reading=deck.select('.slide.reading');assert len(reading)==46
 for i,node in enumerate(reading):
  text=node.select_one('.story-sentence');assert norm(text.get_text())==norm(original[i]),('original deck mismatch',i+1)
  text.clear();text.append(BeautifulSoup(wordhtml(sentences[i]),'html.parser'))
  node['data-ra-sentence']=str(i);node['data-pair']='ra-sentence-'+str(i)
  slot=deck.new_tag('div',attrs={'class':'translation-slot'});p=deck.new_tag('p',attrs={'class':'translation','lang':'he','dir':'rtl'});p.string=sentences[i]['he'];p['style']='visibility:hidden';p['aria-hidden']='true';slot.append(p);node.select_one('.frame').append(slot)
  clone=copy.deepcopy(node);clone['id']='slide-ra-translation-'+str(i+1);clone['data-reveal']='true';clone['class']=[c for c in clone['class'] if c!='active'];clone['hidden']='';cp=clone.select_one('.translation');del cp['style'];del cp['aria-hidden'];node.insert_after(clone)
 deck.body['data-ra-deck']='true'
 for n,s in enumerate(deck.select('.slide')):s['aria-label']=f'{n+1} מתוך {len(deck.select(".slide"))}'
 link=deck.new_tag('link',attrs={'rel':'stylesheet','href':'../unit-1/read-alone/reader.css?v=20260922-ra1'});deck.head.append(link)
 script=deck.new_tag('script',attrs={'defer':'','src':'../unit-1/read-alone/player.js?v=20260922-ra1'});deck.head.append(script)
 cover=deck.select_one('.cover .frame');cover.append(BeautifulSoup('<div class="ra-inline-links"><a href="../unit-1/read-alone/">Read Alone Text · קריאה בקטעים</a><a href="../unit-1/read-alone/?mode=sentences">מילה־במילה · קריאה עצמאית</a></div>','html.parser'))
 raw=str(deck)
 raw=raw.replace('    fit();\n  }','    fit();\n    document.dispatchEvent(new CustomEvent(\'teachers:slidechange\'));\n  }',1)
 raw=re.sub(r"function fromHash\(\) \{[^\n]+\}","function fromHash() { const id=location.hash.slice(1); const found=slides.findIndex(s=>s.id===id); show(found>=0?found:0,false); }",raw)
 raw=raw.replace("'#slide-' + (current + 1)","'#' + slide.id")
 raw=raw.replace("if (e.altKey || e.ctrlKey", "if (e.defaultPrevented || e.target.closest('.ra-hit') || e.altKey || e.ctrlKey")
 assert 'teachers:slidechange' in raw;deckpath.write_text(raw)
 banner='''<section class="panel" id="read-alone-links"><h2>שני מסלולי Read Alone · כל הסיפור</h2><p>הקראה מוקלטת והדגשת המילה הנשמעת; תרגום בנגיעה; האטה עד רבע מהמהירות.</p><div class="actions"><a class="button primary" data-track href="read-alone/">Read Alone Text · קריאה בקטעים</a><a class="button" data-track href="read-alone/?mode=sentences">מילה־במילה · משפט ותרגום בשקפים</a><a class="button" data-track href="../the-message-without-a-voice/">המצגת המלאה עם הקראה</a></div><p>בנייד: לחצו פעם אחת על ▶ הקראה להפעלת האודיו. החלפת טאב ידנית עוצרת את ההקראה.</p></section>'''
 for name in ['index.html','reading.html','resources.html','student-preparation.html']:
  path=U/name;s=BeautifulSoup(path.read_text(),'html.parser');old=s.select_one('#read-alone-links')
  if old:old.decompose()
  target=s.select_one('.hero') or s.select_one('.tabs');assert target,name;target.insert_after(BeautifulSoup(banner,'html.parser'));path.write_text(str(s))
 # Source verification after all integration edits.
 after=BeautifulSoup((U/'reading.html').read_text(),'html.parser');again=[]
 for node in after.select('.story .sentence'):node.select_one('.sid').extract();again.append(node.get_text().strip())
 assert again==original
 report={'version':'20260922-ra1','original_text_unchanged':True,'original_slides_preserved':96,'added_translation_slides':46,'full_deck_slides':142,'sentence_reader_slides':92,'passages':len(pages),'sentences':46,'words_with_translation_and_timing':global_index,'meaning_units':sum(len(s['units']) for s in sentences),'audio_seconds':audio['duration'],'audio_sha256':audio['sha256']}
 dump(O/'build-report.json',report)
 (O/'README.md').write_text('# Grade 9 Unit 1 — Read Alone\n\nBoth reading standards cover the original complete story. Source: ../reading.html. Vocabulary: Band II Core II groups 21–23.\n\nText: short manually navigated passages; sentence mode: English then Hebrew reveal, 92 slides. The full original teaching deck retains all 96 original slides and adds 46 translation slides. Existing original slide anchors remain stable.\n\nAudio: prerecorded Microsoft en-US-BrianNeural, pitch +10Hz; measured WordBoundary timings, not uniform estimates. Shared saved speed key: teachers-read-alone-speed-v1. No browser TTS or student data submission.\n\nImage is a static library illustration, not a depiction of the fictional story. Photo source: '+content['imageCredit']['file']+'\n\nRebuild: python tools/grade9_read_alone_audio.py; python tools/grade9_complete_readalone.py. Browser checks: tools/grade9_readalone_qa.py.\n')
 print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
