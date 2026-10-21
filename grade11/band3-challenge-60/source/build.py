from pathlib import Path
import json,html,csv
ROOT=Path(__file__).resolve().parents[1]
entries=json.loads((ROOT/'entries.json').read_text())
esc=lambda s:html.escape(str(s),quote=True)
slides=[];index=[]
def add(body,cls='',attrs=''):
 i=len(slides)+1;slides.append(f'<section id="slide-{i}" class="slide {cls}" hidden {attrs}><div class="frame">{body}</div></section>');return i
add('''<div class="eyebrow">BAND III · LISTS A–D</div><h1 class="cover-title en">60 Challenging Entries</h1><p class="cover-sub">30 ערכים מרשימה A תחילה</p><p class="instruction">קוראים באנגלית ומנסים להבין מההקשר.<br>בשקף הבא חושפים את הפירוש והתרגום.</p><p class="level">לכל ערך: הקראת מילה והקראת משפט בנפרד.</p><a class="start-link" href="#slide-2">מתחילים</a><p class="small-print">בחירה פדגוגית של מילים וביטויים מאתגרים מתוך הכרטיסיות הקיימות.</p>''','cover')
colors=['#4ee5ff','#a98cff','#ffc857','#dfff5b','#ff7163','#a98cff']
def visual(n):
 # Precise geometric patterns, no external images or scientific claims.
 color=colors[(n-1)%len(colors)]
 if n%3==1:
  shapes=''.join(f'<ellipse cx="350" cy="180" rx="{160-k*6}" ry="{65+k*3}" fill="none" stroke="{color}" stroke-opacity="{.3+k*.04}" stroke-width="2" transform="rotate({k*15} 350 180)"/>' for k in range(12))
 elif n%3==2:
  shapes=''.join(f'<rect x="{205+k*9}" y="{35+k*9}" width="{290-k*18}" height="{290-k*18}" rx="12" fill="none" stroke="{color}" stroke-width="3" transform="rotate({k*8} 350 180)"/>' for k in range(13))
 else:
  shapes=''.join(f'<circle cx="350" cy="180" r="{25+k*12}" fill="none" stroke="{color}" stroke-opacity="{1-k*.06}" stroke-width="{2+k%3}"/>' for k in range(12))
 return f'<svg viewBox="0 0 700 360" role="img" aria-label="דוגמה גאומטרית צבעונית להפוגה קצרה">{shapes}</svg>'
for e in entries:
 n=e['number']; group=e['group']; letter=e['list'];long='long' if len(e['en'])>19 else ''
 source=f'https://simonh68.github.io/module-e-vocab/{group}.html'
 # Visibility reserves translation geometry in both stages; standard.js fits the pair.
 common=f'''<div class="slide-meta"><span class="eyebrow">ערך {n} מתוך 60</span><span class="list-badge" data-list="{letter}">List {letter}</span><span class="eyebrow en">{esc(e['pos'])}</span></div>
 <div class="word-region"><h2 class="word en {long}" lang="en">{esc(e['en'])}</h2><button class="audio-button" data-vocab-audio="audio/{n:02}-word.mp3" data-audio-kind="word" aria-pressed="false" aria-label="הקראת הערך {esc(e['en'])}">▶ הקראת המילה / הביטוי</button></div>
 <div class="sentence-region"><p class="example en" lang="en">{esc(e['ex_en'])}</p><button class="audio-button" data-vocab-audio="audio/{n:02}-sentence.mp3" data-audio-kind="sentence" aria-pressed="false" aria-label="הקראת משפט הדוגמה של {esc(e['en'])}">▶ הקראת המשפט</button></div>'''
 for reveal in [False,True]:
  translation=f'<div class="translation-slot"><div class="{"" if reveal else "hidden-translation"}" {"" if reveal else "aria-hidden=true"}><p class="meaning" lang="he">{esc(e["mean_he"])}</p><p class="translation" lang="he">{esc(e["ex_he"])}</p></div><div class="resource-row"><a href="{source}" target="_blank" rel="noopener">כרטיסיות המקור · {group}</a><button data-copy-url="{source}">העתקת קישור</button></div></div>'
  idx=add(common+translation,'vocab'+(' reveal' if reveal else ''),f'data-pair="entry-{n}" data-entry="{esc(e["source_entry_id"])}" data-list="{letter}"')
  if not reveal:index.append((e,idx))
 if n%5==0 and n<60:
  label='המשך: רשימות B, C ו־D' if n==30 else f'{n} ערכים הושלמו'
  add(f'<div class="eyebrow">הפוגה קצרה</div>{visual(n//5)}<p class="part-he">{label}</p>','vocab-break')
add('<div class="eyebrow">60 / 60</div><h2 class="part-title">חזרה לפי הצורך</h2><p class="instruction">פותחים את רשימת הערכים ובוחרים מילים לחזרה.<br>מנסים להסביר את המשמעות לפני חשיפת העברית.</p><p class="level">ערכים 1–30: רשימה A · ערכים 31–60: רשימות B–D</p>','transition')
links=[]
for e,i in index:
 if (e['number']-1)%10==0:links.append(f'<div class="index-heading">{esc(e["section_title"])}</div>')
 links.append(f'<a href="#slide-{i}"><span class="list-badge" data-list="{e["list"]}">{e["list"]}</span><span>{e["number"]}. {esc(e["en"])}</span></a>')
page='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Band III · 60 Challenging Entries</title><meta name="description" content="60 challenging Band III vocabulary entries. First 30 from List A. Original flashcard examples, Hebrew reveal and separate prerecorded word and sentence audio."><link rel="stylesheet" href="../../shared/deck/standard.css"><link rel="stylesheet" href="../../shared/deck/vocabulary-audio.css?v=1"></head><body class="vocabulary-deck"><a class="home" href="../five-units/" aria-label="חזרה לכיתה י״א">⌂</a><div class="audio-toolbar"><button data-open-index>רשימת 60 הערכים</button><label for="speed">מהירות</label><select id="speed" data-audio-speed aria-label="מהירות הקראה"><option value="1">רגילה</option><option value="0.75">איטית</option><option value="0.5">איטית מאוד</option></select></div><main class="stage">'''+''.join(slides)+'''</main><nav class="nav" aria-label="ניווט שקפים"><div class="nav-group"><button data-step="-1" aria-label="השקף הקודם">←</button><button data-step="1" aria-label="השקף הבא">→</button></div><span class="progress" id="counter"></span></nav><div class="audio-status" data-audio-status role="status" aria-live="polite"></div><div class="progress-track"><div class="progress-fill"></div></div><dialog class="vocab-index" data-vocab-index><header><h2>60 הערכים</h2><button data-close-index>סגירה</button></header><div class="index-grid">'''+''.join(links)+'''</div></dialog><script src="../../shared/deck/standard.js"></script><script src="../../shared/deck/vocabulary-audio.js?v=1"></script></body></html>'''
(ROOT/'index.html').write_text(page)
with (ROOT/'source/selected-entries.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.writer(f,lineterminator="\n");writer.writerow(['Number','List','Group','Source ID','Entry','Part of speech','Hebrew meaning','English example','Hebrew example'])
 for e in entries:writer.writerow([e[k] for k in ['number','list','group','source_entry_id','en','pos','mean_he','ex_en','ex_he']])
(ROOT/'source/slide-map.json').write_text(json.dumps([{'number':e['number'],'slide':i,'entry':e['en'],'list':e['list']} for e,i in index],indent=2))
print('Built',len(slides),'slides; 60 exact source entries; 30 A first; 120 separate audio targets.')
