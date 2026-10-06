import csv, json, html, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent
OUT.mkdir(exist_ok=True)
fields=['word','meaning1','en1','he1','meaning2','en2','he2','related','note','why']
read=lambda path:[dict(zip(fields,r)) for r in csv.reader(open(path,encoding='utf-8'),delimiter='\t')]
entries=read(ROOT/'entries.tsv')
omit={'reasonable','material','current','cut down'}
entries=[e for e in entries if e['word'] not in omit]
new=read(ROOT/'refinements.tsv')
# Place grammatical auxiliaries among the highest instructional priorities.
entries=entries[:3]+new[:3]+entries[3:]+new[3:]
assert len(entries)==50 and len({e['word'] for e in entries})==50
import urllib.request
source_url='https://raw.githubusercontent.com/Simonh68/module-e-vocab/912053cc5030cd6be4a936e642f34775fd07fb67/data/vocabulary-master.json'
raw=urllib.request.urlopen(source_url).read()
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='89ee7153930a5e5e04f92485a22f63ba24a9d38b'
v=[e for e in json.loads(raw) if e['group'][0] in 'AB']
by={}
for r in v: by.setdefault(r['en'],[]).append(r)
assert all(e['word'] in by for e in entries)
selected={e['word']:e for e in entries}
# Expert bands assess difficulty of independent learning, not word frequency or spelling.
poly4=set('advance|age|altogether|apparent|appear|atmosphere|average|behind|brilliant|challenge|chance|change|common|conditions|contemporary|current|cut down|deliver|demonstrate|design|determine|development|differ|done|double|drop|economical|element|expression|extend|farther/further|feature|final|fit|fresh|gain|genuine|go out|image|impression|input|instruction|intelligence|interest|interpret|jam|judgment|keen|learn|lecture|light|living|low|lower|material|measure|mend|name|native|naturally|notice|occupation|occupy|oil|operate|organ|outstanding|particular|patient|peculiar|perform|personally|place|plant|policy|potential|prime|principal|produce|promote|public|quality|question|reach|reason|reasonable|register|regret|regular|relate|remote|respect|retire|review|revise|role|rough|rule|rush|sample|satisfy|scale|scene|schedule|sensitive|service|setting|shortly|society|speech|study|support|surface|theme|transport|turn|undo|view|vision|waste|wealth|welcome|within'.split('|'))
grammar4=set('be responsible for|can|do|must|except that|fetch|in|in terms of|just about|kind of|likely|more or less|neither ... nor|not ... a word|not only|on the whole|others|prevent|provided that|put up with|so-called|take into account|take place|thanks to|to|unlike|whom|worthwhile'.split('|'))
grammar3=set('all of a sudden|among other things|at least|be in charge|be situated in/on/by|before|believe in|come after/first/last|either way|fed up|focus on/upon|get rid of|get wrong|get worse|hopefully|in actual fact|in connection with|in that case|in the meantime|it looks like/as if/as though|just as ... as|keep on doing|look at|make sense|make up your mind|not at all|on the one hand ... on the other hand|out of date|part-time|point of view|rely on/upon|run out of|set up|shut down|slow down/up|sooner or later|start off|sum up|take part|take seriously|take the opportunity|take/accept/claim responsibility|the headlines|the heart of|the main thing|the reality of|throw away/out|to start with|underneath|up-to-date|use up|wherever'.split('|'))
abstract3=set('acquire|addition|advanced|analysis|appropriate|blame|block|characteristic|competitive|consequence|considerable|cope|criterion|critic|declare|deliberately|demanding|detect|disagreement|efficient|emerge|emphasis|essentially|exactly|exception|exchange|expense|feedback|finding/findings|flexible|guidance|highlight|historic|ideal|illustrate|immigration|impress|incredible|initial|interaction|interrupt|introduce|invest|involvement|justice|lack|limited|mention|misunderstand|nevertheless|occasional|official|priority|private|probable|proof|proposed|purpose|recommend|relevant|reliable|replace|request|research|result|risk|significant|similarity|slight|specific|structure|summary|uncomfortable|unique|united|unlikely|vary|virtual reality'.split('|'))
basic1=set('bad|calculate|copy|decade|disappointed|dislike|enjoyable|essay|exist|flu|frighten|hidden|identical|illness|inside|kit|monthly|nightmare|planet|population|relax|salary|trash|understand|unemployed|unexpected|unfortunately|unhealthy|unknown|urgent|visible'.split('|'))
ranking=[]
for word,records in by.items():
 if word in selected:
  score=5; why=selected[word]['why']; order=list(selected).index(word)
 elif word in poly4:
  score=4; why='משמעויות נוספות או צירופים שכיחים עלולים להטעות; יש להבחין בחלק הדיבור ובהקשר.'; order=1000
 elif word in grammar4:
  score=4; why='מבנה דקדוקי, מילת תפקוד או צירוף שהתרגום הקצר אינו מסביר את שימושו.'; order=1000
 elif word in grammar3:
  score=3; why='צירוף או מילת קישור: ההקניה דורשת דוגמה ותשומת לב למבנה, אך המשמעות המרכזית ניתנת ללמידה עצמית.'; order=1000
 elif word in abstract3:
  score=3; why='משמעות מופשטת, הבחנה סמנטית או צירוף מקובל; תרגום אחד מועיל אך אינו מספיק לשימוש פעיל.'; order=1000
 elif word in basic1:
  score=1; why='משמעות המקור ישירה יחסית, עם מקבילה עברית זמינה; עדיפות נמוכה להקניה מיוחדת בכיתה.'; order=1000
 else:
  score=2; why='משמעות המקור ניתנת ללמידה עצמית בעזרת דוגמה; נדרשת חזרה על הצורה או על ההקשר, ללא מכשול מרכזי המצדיק מקום ב־50 הראשונים.'; order=1000
 ranking.append(dict(word=word,score=score,why=why,order=order,lists='/'.join(sorted({r['group'][0] for r in records})),ids='; '.join(r['source_entry_id'] for r in records),pos='; '.join(sorted({r['pos'] for r in records})),senses=' | '.join(r['record_sense_en'] for r in records)))
ranking.sort(key=lambda r:(-r['score'],r['order'],r['word']))
assert len(ranking)==436
for i,r in enumerate(ranking,1): r['rank']=i
with open(OUT/'Band3-AB-Full-Ranking.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f); w.writerow(['דירוג','ערך','רשימה','קושי בהקניה עצמית 1–5','נבחר','נימוק','חלקי דיבור במקור','משמעויות הרשומות באנגלית','מזהי רשומות'])
 for r in ranking:w.writerow([r['rank'],r['word'],r['lists'],r['score'],'כן' if r['word'] in selected else 'לא',r['why'],r['pos'],r['senses'],r['ids']])
for e in entries:
 e['ids']=[r['source_entry_id'] for r in by[e['word']]]
 e['source_senses']=[r['record_sense_en'] for r in by[e['word']]]
 e['pos']=list(dict.fromkeys(r['pos'] for r in by[e['word']]))
# Extensions are identified explicitly instead of enlarging the official requirement silently.
extensions={'once','otherwise','little','issue','present','conduct','nature','domestic','keep','claim','miss','anxious','right','do','objective'}
for e in entries:e['second_scope']='הרחבה שימושית מעבר למשמעות או לחלק הדיבור של הרשומה' if e['word'] in extensions else 'שימוש נוסף או הקשר נוסף להבחנה'
esc=lambda s:html.escape(str(s),quote=True)
rich=lambda s:esc(s).replace('[[','<mark>').replace(']]','</mark>')
plain=lambda s:s.replace('[[','').replace(']]','')
slides=[];script=[]
def slide(kind,section,body,note='',pair=None):
 n=len(slides)+1
 attr=f' data-pair="{pair}"' if pair else ''
 slides.append(f'<section class="slide {kind}" data-section="{esc(section)}"{attr} id="slide-{n}"><div class="frame">{body}</div></section>')
 script.append(f'שקף {n} | {section}\n'+html.unescape(__import__('re').sub('<[^>]+>',' ',body)).strip()+'\nהנחיית מורה: '+note+'\n')
slide('cover','פתיחה','<h1 class="cover-title en">Band III<br>50 Words in Context</h1><p class="cover-sub">כיתה י׳ א׳ · רשימות A ו־B</p>', 'מאגר לחמישה מפגשים; אין ללמד 50 ערכים חדשים בשיעור אחד.')
slide('transition','פתיחה','<h2 class="part-title">משמעות לפי ההקשר</h2><p class="instruction">נראה מילה, נקרא משפט, ואז נחשוף את הפירוש. נשווה שימוש נוסף ונקשר למילים שכבר מכירים.</p>', 'שאלו מה במשפט עוזר לבחור משמעות. אין לשנן את כל ההרחבות כאילו הן רשימת חובה.')
for i,e in enumerate(entries):
 section=f'חלק {i//10+1}'
 if i%10==0:
  slide('transition',section,f'<h2 class="part-title">חלק {i//10+1}</h2><p class="cover-sub">ערכים {i+1}–{i+10}</p>', 'כ־45–60 דקות לכל עשרה ערכים, בהתאמה לשליפה ולידע הקודם. זאת הצעת רצף, לא שיעור שכבר התקיים.')
 meta=f'<div class="slide-meta"><p class="eyebrow">י׳ א׳ · {i+1}/50 · {esc(", ".join(e["ids"]))}</p></div>'
 word=f'<h2 class="word en">{esc(e["word"])}</h2>'
 slide('cover',section,meta+word, 'הצג את הערך ללא תרגום. בקש משמעות אחת שהכיתה מכירה; אל תאשר פירוש בלי הקשר.')
 for j in [1,2]:
  pair=f'e{i+1}-{j}'
  scope='משמעות מרכזית מן הרשימה' if j==1 else e['second_scope']
  base=meta+word+f'<p class="example en">{rich(e[f"en{j}"])}</p>'
  trans=f'<p class="meaning">{esc(e[f"meaning{j}"])}</p><p class="translation">{esc(e[f"he{j}"])}</p>'
  for reveal in [False,True]:
   slot=f'<div class="translation-slot"'+('' if reveal else ' style="visibility:hidden" aria-hidden="true"')+'>'+trans+'</div>'
   slide('vocab',section,base+slot, ('חשיפה: '+scope+'. '+e['note']) if reveal else 'קראו את המשפט לפני התרגום. שאלו: מה כאן פירוש הערך, ומהו הרמז בהקשר?',pair)
 # Relationships are split into compact lines, labelled by relation in their wording.
 rel=''.join(f'<p class="translation">{esc(x.strip())}</p>' for x in e['related'].split(';'))
 slide('transition',section,meta+word+rel,'הרחבה לפי צורך בלבד. '+e['note']+' שאלת שליפה: חברו משפט חדש שבו הפירוש אינו זה המוכר ביותר.')
 if i%10==9:
  slide('transition',section,'<h2 class="part-title">בדיקת שליפה</h2><p class="instruction">בחרו שני ערכים מן החלק הזה. כתבו לכל אחד משפט והסבירו בעברית מדוע הפירוש מתאים להקשר.</p>', '2–3 דקות כתיבה. תקן רק משמעות ומבנה מרכזי. חזור בתחילת המפגש הבא על הערכים שהתבלבלו בהם.')
slide('transition','סיום','<h2 class="part-title">תרגול מסכם</h2><p class="instruction">כתבו פסקה קצרה על למידה בבית הספר. השתמשו בשלושה ערכים, וסמנו את המשמעות שבחרתם לכל אחד.</p>', 'בדיקה: המשמעות מתאימה, המבנה נכון, והכותב מסוגל להסביר את השימוש. אין חובה לדחוס כמה משמעויות לאותו משפט.')
slide('transition','סיום','<h2 class="part-title">מקורות וחומר למורה</h2><p class="instruction">הערכים מרשימות A ו־B של Band III. משפטי הדוגמה והתרגומים נכתבו למצגת זו.</p><div class="resource-links"><a href="Band3-50-Teacher-Script.txt">התסריט המלא</a><a href="Band3-AB-Full-Ranking.csv">דירוג כל 436 הערכים</a></div>', 'הדירוג הוא שיקול דעת פדגוגי לתלמידים דוברי עברית, לא מדד מחקרי ולא שינוי ברשימה הרשמית.')
html_doc='''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Band III 50 Words in Context — י׳ א׳</title><link rel="stylesheet" href="https://simonh68.github.io/teachers/shared/deck/standard.css?v=1"></head><body><a class="home" href="https://simonh68.github.io/teachers/#grade10" aria-label="חזרה לכיתה י׳">⌂</a><main class="stage">'''+''.join(slides)+'''</main><nav class="nav" aria-label="ניווט"><div class="nav-group"><button data-step="-1" aria-label="השקף הקודם">←</button><button data-step="1" aria-label="השקף הבא">→</button></div><span class="progress" id="counter"></span></nav><div class="progress-track"><div class="progress-fill"></div></div><script src="https://simonh68.github.io/teachers/shared/deck/standard.js?v=1"></script></body></html>'''
(OUT/'index.html').write_text(html_doc,encoding='utf-8')
intro="""Band III A and B — תסריט מלא לכיתה י׳ א׳

מטרה: להבין 50 ערכים בעייתיים ללמידה עצמית באמצעות הקשר, השוואה ומבנה, ולא רק תרגום.
היקף: 478 רשומות מקור, 436 ערכים ייחודיים לאחר איחוד כתיב זהה ושמירת כל חלקי הדיבור והמשמעויות. A ו־B הן רשימות באותה רמה.
קהל: כיתה י׳ א׳, דוברי עברית; משפטים קצרים בתחילה והסבר מפורש של השימוש.
סולם דירוג: 5 — צורך גבוה מאוד בהקניה; 4 — קושי משמעותי; 3 — קושי בינוני; 2 — קושי מתון; 1 — יחסית ישיר. המדד בוחן ריבוי משמעויות, פער תרגומי, תלות במבנה ונטייה לטעות. אורך מילה ונדירות אינם הקריטריון המרכזי.
דירוגי הקושי הם הערכת הוראה, לא נתוני ניסוי. סדר 50 הנבחרים הוא סדר עדיפות מקצועי; יתר הערכים מסודרים לפי ציון ובתוך כל ציון בסדר אלפביתי. אין לייחס הבדל מדוד לשני ערכים באותו ציון.
הבחירה אינה טוענת שאי אפשר ללמוד את הערכים לבד. היא מזהה היכן למורה יש ערך מוסף משמעותי בהבחנה ובתיקון הבנה.
ההרחבות מסומנות בנפרד: חלק דיבור אחר, שימוש שכיח נוסף או צירוף קשור אינם הופכים אוטומטית לחומר חובה רשמי.
בכיתה: חמישה חלקים של עשרה ערכים; מומלץ לפרוס לחמישה מפגשים ולהקדיש בתחילת כל אחד שליפה מן הקודם. בכיתה שכבר מכירה חלק מן הערכים אפשר להתקדם מהר יותר.
המצגת מציגה: ערך לבדו → משפט באנגלית → אותו משפט עם פירוש ותרגום → משפט נוסף → חשיפת תרגום → קשרים שימושיים. באנגלית מודגש הערך או הצירוף כולו.
זמני עבודה מוצעים לערך: 15 שניות לשליפה ראשונה; 20–30 שניות להסיק משמעות בכל משפט; דקה להסבר והבחנה; דקה למשפט חדש. הזמן בפועל תלוי בידע הקודם.
אין שמע שהופק למצגת זו. אין שימוש בהקראת מכשיר, ואין כפתור שמע מדומה.

מקור הערכים: Simonh68/module-e-vocab, data/vocabulary-master.json.
commit מקור: 912053cc5030cd6be4a936e642f34775fd07fb67; Git blob: 89ee7153930a5e5e04f92485a22f63ba24a9d38b.
https://github.com/Simonh68/module-e-vocab/blob/912053cc5030cd6be4a936e642f34775fd07fb67/data/vocabulary-master.json
משפטים, תרגומים, נימוקים וקשרים הם חומר הוראה מקורי. מסד המקור לא שונה.

50 הערכים והערות ההקניה
"""
summaries=[]
for i,e in enumerate(entries,1):
 summaries.append(f"""{i}. {e['word']} — קושי 5/5
מקור: {', '.join(e['ids'])}; חלקי דיבור ברשימה: {', '.join(e['pos'])}.
משמעויות הרשומות באנגלית: {' | '.join(e['source_senses'])}
מדוע בכיתה: {e['why']}
דוגמה 1: {plain(e['en1'])}
פירוש בהקשר: {e['meaning1']}. תרגום: {e['he1']}
דוגמה 2: {plain(e['en2'])}
פירוש בהקשר: {e['meaning2']}. תרגום: {e['he2']}
מעמד הדוגמה השנייה: {e['second_scope']}.
קשרים שימושיים: {e['related']}
הנחיית המורה: {e['note']}
תרגול: חברו משפט חדש; ציינו פירוש ורמז מההקשר. אם מדובר בשתי משמעויות, החליפו בכל משפט את הערך בחלופה באנגלית המתאימה רק לאותו שימוש.
""")
(OUT/'Band3-50-Teacher-Script.txt').write_text(intro+'\n'.join(summaries)+'\n\nתסריט שקף אחר שקף\n\n'+'\n'.join(script),encoding='utf-8')
(ROOT/'lesson-data.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
manifest={'entries':len(entries),'slides':len(slides),'records':len(v),'unique':len(by),'source_sha':'89ee7153930a5e5e04f92485a22f63ba24a9d38b','scores':{s:sum(r['score']==s for r in ranking) for s in range(1,6)},'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in OUT.iterdir()}}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,ensure_ascii=False))
