#!/usr/bin/env python3
"""Build the Grade 8 text-based worksheet and shared-standard companion deck.

Run from any directory with Python + reportlab. Content remains local, while
navigation, fitting and swipe come from shared/deck. No browser TTS.
"""
from pathlib import Path
import json, html, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'grade8/monkey-writing-workshop'
DATA = json.loads((OUT / 'content.json').read_text())
PARAS = json.loads((ROOT / 'grade8/monkey-festival/lesson.json').read_text())['paragraphs'][:6]
PDF = 'Grade8-Monkey-Festival-Worksheet.pdf'
FILES = OUT / 'files'
FILES.mkdir(exist_ok=True)
W,H = A4
M=34
FONT=Path('/usr/share/fonts/truetype/dejavu')
for name, fn in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/fn)))
INK=HexColor('#152b3c'); TEAL=HexColor('#166373'); RULE=HexColor('#b3c4ce'); LIGHT=HexColor('#edf4f6')

def wrap(text,width,size=11,font='Body'):
    lines=[]; line=''
    for word in text.split():
        trial=(line+' '+word).strip()
        if pdfmetrics.stringWidth(trial,font,size)>width and line:
            lines.append(line); line=word
        else: line=trial
    if line: lines.append(line)
    return lines

def en(c,text,x,y,width,size=11,bold=False,leading=None):
    font='Bold' if bold else 'Body'; leading=leading or size*1.4
    c.setFont(font,size); c.setFillColor(INK)
    for line in wrap(text,width,size,font): c.drawString(x,y,line); y-=leading
    return y

def he(c,text,xright,y,width,size=11,bold=False):
    # Hebrew-only phrases. Latin labels/numbers are drawn separately in LTR.
    font='Bold' if bold else 'Body'; c.setFont(font,size); c.setFillColor(INK)
    for line in wrap(text,width,size,font): c.drawRightString(xright,y,line[::-1]); y-=size*1.4
    return y

def rule(c,x,y,width):
    c.setStrokeColor(RULE);c.setLineWidth(.5);c.line(x,y,x+width,y)

def head(c,n,title,part):
    c.setFillColor(TEAL);c.rect(0,H-13,W,13,fill=1,stroke=0)
    en(c,'GRADE 8',M,H-40,110,13,True)
    he(c,title,W-M,H-40,410,16,True)
    he(c,'שם: ____________________    כיתה: ________    תאריך: __________',W-M,H-66,W-2*M,10)
    en(c,part,M,H-92,W-2*M,11,True)
    rule(c,M,38,W-2*M)
    en(c,'The Monkey Festival | Part One A-F',M,25,450,8)
    c.setFont('Body',8);c.drawRightString(W-M,25,f'{n} / 5')
    return H-119

ERRORS=[
 {'bad':'The monkeys is making loud noises.','good':'The monkeys are making loud noises.','he':'הנושא ברבים, ולכן משתמשים ב־are.'},
 {'bad':'The festival have live performances.','good':'The festival has live performances.','he':'הנושא ביחיד, ולכן משתמשים ב־has.'},
 {'bad':'The monkeys can takes sunglasses.','good':'The monkeys can take sunglasses.','he':'אחרי can משתמשים בצורת הבסיס.'},
 {'bad':'people prepare fruit in thailand.','good':'People prepare fruit in Thailand.','he':'מתחילים משפט ושם של מדינה באות גדולה.'}
]

def build_pdf():
    c=canvas.Canvas(str(FILES/PDF),pagesize=A4)
    c.setTitle('Grade 8 - The Monkey Festival - Worksheet')
    c.setAuthor('English for Noar - Simon Halevi')
    # Page 1: source and proofreading, comfortably readable.
    y=head(c,1,'דף עבודה באנגלית | קוראים ובודקים','READING  |  The Monkey Festival')
    y=he(c,'קראו את החלק הראשון. השתמשו בטקסט בכל חלקי דף העבודה.',W-M,y,W-2*M,11)-15
    for i,p in enumerate(PARAS):
        en(c,chr(65+i),M,y,18,11,True)
        y=en(c,p['text'].replace('–','-'),M+23,y,W-2*M-23,10.6,leading=15.5)-10
    y-=2
    y=he(c,'בדיקת דקדוק ואיות: תקנו את המשפטים על השורות.',W-M,y,W-2*M,11,True)-8
    for i,e in enumerate(ERRORS):
        y=en(c,f'{i+1}. {e["bad"]}',M,y,W-2*M,10.3)-8
        rule(c,M,y,W-2*M);y-=22
    assert y>38,('reading page overflow',y)
    c.showPage()
    # Page 2: exact Grade 7 format: English left + blank, Hebrew right + number.
    y=head(c,2,'מתאימים משפטים','A  |  Match 20 sentences')
    y=he(c,'כתבו ליד כל משפט באנגלית את מספר התרגום המתאים מימין.',W-M,y,W-2*M,11)
    y=he(c,'השתמשו בכל מספר פעם אחת. בדקו את משמעות המשפט כולו.',W-M,y,W-2*M,11)-20
    col=(W-2*M-24)/2
    en(c,'English',M+34,y,col-34,11,True)
    he(c,'עברית',W-M,y,col,11,True); y-=22
    order=DATA['matching_order']
    for i,item in enumerate(DATA['matching']):
        # Dynamic rows, at least 26 pt; Hebrew numbering is on its reading edge.
        right=DATA['matching'][order[i]]['he']
        rows=max(len(wrap(item['en'],col-34,9.7)),len(wrap(right,col-24,10)))
        height=max(25,rows*14+6)
        if i%2==0:
            c.setFillColor(LIGHT);c.rect(M-5,y-height+9,W-2*M+10,height,fill=1,stroke=0)
        rule(c,M,y-2,24)
        en(c,item['en'],M+34,y,col-34,9.7,leading=14)
        c.setFillColor(TEAL);c.setFont('Bold',10);c.drawRightString(W-M,y,f'{i+1}.')
        he(c,right,W-M-24,y,col-24,10)
        y-=height
    assert y>40,('matching page overflow',y)
    c.showPage()
    # Pages 3-4: each response has two full-width lines, with lighter scaffolds later.
    for page,start in [(3,0),(4,12)]:
        y=head(c,page,'יוצרים משפטים','B  |  Build and write sentences')
        y=he(c,'כתבו משפטים שלמים באנגלית. הוסיפו אות גדולה וסימן פיסוק.',W-M,y,W-2*M,11)-13
        for i in range(start,start+12):
            item=DATA['writing'][i]
            if i==0: y=he(c,'סדרו את כל החלקים למשפט שלם.',W-M,y,W-2*M,10,True)-5
            if i==4: y=he(c,'תרגמו לאנגלית לפי ההקשר בטקסט.',W-M,y,W-2*M,10,True)-5
            if i in (8,12): y=he(c,'כתבו לפי ההנחיה. אפשר יותר מניסוח נכון אחד.',W-M,y,W-2*M,10,True)-5
            en(c,f'{i+1}.',M,y,30,10.4,True)
            if item['type']=='translate':
                y=he(c,item['prompt'],W-M,y,W-2*M-30,10.5)
            else:
                y=en(c,item['prompt'],M+27,y,W-2*M-27,10.2,leading=13.8)
            y-=4;rule(c,M+27,y,W-2*M-27);y-=15
            rule(c,M+27,y,W-2*M-27);y-=15
        assert y>40,('writing page overflow',page,y)
        c.showPage()
    # Page 5: 20 open questions with two writing lines for each.
    y=head(c,5,'מבינים, מסבירים ועונים','C  |  Answer 20 questions')
    y=he(c,'ענו באנגלית במשפטים שלמים. חזרו לטקסט ותמכו במסקנות בפרטים ממנו.',W-M,y,W-2*M,10.4)-7
    y=he(c,'בשאלות האחרונות נדרשים גם הסבר, מסקנה או עצה.',W-M,y,W-2*M,10.4)-18
    top=y; gap=24; col=(W-2*M-gap)/2
    for column in range(2):
        x=M+column*(col+gap); y=top
        for i in range(column*10,column*10+10):
            q=DATA['questions'][i]
            yy=en(c,f'{i+1}. {q["q"]}',x,y,col,9.3,leading=12.3)
            yy-=8;rule(c,x,yy,col);rule(c,x,yy-17,col)
            y-=62
        assert y>36,('questions page overflow',y)
    c.showPage();c.save()

E=html.escape
def p(text,cls='',lang='he'):
    return f'<p class="{cls}" lang="{lang}" dir="{"ltr" if lang=="en" else "rtl"}">{E(text)}</p>'

slides=[]; pairs=0; since_break=0
def add(body,section,cls='',pair=None):
    attr=f' data-pair="{pair}"' if pair else ''
    slides.append(f'<section class="slide {cls}" data-section="{section}"{attr}><div class="frame">{body}</div></section>')

def transition(section,title,instruction):
    add(f'<h2 class="part-title">{E(title)}</h2>'+p(instruction,'instruction'),section,'transition')

def respite(section):
    global since_break
    idx=(len(slides)//10)%3
    fn=['banana_guest.jpg','monkey_detective.jpg','banana_calendar.jpg'][idx]
    add(f'<img class="break-image" src="../monkey-festival/assets/{fn}" alt="איור דמיוני של קופים ובננות להפסקה קצרה">',section,'break')
    since_break=0

def pair(section,label,prompt,answer,why,tense='',lang='en',extra='',alternative=None):
    global pairs,since_break
    pairs+=1; key=f'p{pairs}'
    common='<div class="slide-meta">'+p(label,'eyebrow')+p(tense,'tense')+'</div>'+p(prompt,'question '+('en' if lang=='en' else ''),lang)+extra
    first='<div class="answer-slot">'+p('כתבו או אמרו את התשובה לפני המעבר לשקף הבא.','write-cue')+'</div>'
    result='<div class="answer-slot">'+p('תשובה לדוגמה' if alternative or section=='כתיבה' else 'תשובה','answer-label')+p(answer,'possible-answer en','en')+p(why,'explanation')
    if alternative:
        result+=f'<details class="alternative"><summary>ניסוח אפשרי נוסף</summary>{p(alternative,"possible-answer en","en")}</details>'
    result+='</div>'
    add(common+first,section,'qa question-slide',key)
    add(common+result,section,'qa reveal',key)
    since_break+=2
    if since_break>=10: respite(section)

def build_deck():
    add('<h1 class="cover-title">The Monkey Festival</h1>'+p('כיתה ח׳ · דף עבודה ותרגול כתיבה','cover-sub')+p('Part One A–F','level en','en')+'<div class="resource-links"><a href="files/'+PDF+'">דף העבודה · PDF</a><a href="../unit-1/sentences/">קריאת הטקסט עם שמע</a></div>'+p('נוצר: יום ראשון בערב, ח׳ בחשוון תשפ״ז (18.10.2026)','level'),'פתיחה','cover transition')
    add('<h2 class="part-title">מנסים לבד, ואז בודקים יחד</h2>'+p('בדף: טקסט ובדיקת דקדוק, 20 התאמות, 24 משימות כתיבה ו־20 שאלות.','instruction')+p('המצגת מדגימה מבחר משימות. למפתח המלא אפשר להגיע בסוף.','instruction')+p('השתמשו בחצים, בגלגלת או בהחלקה. כל שאלה ואחריה שקף פתרון.','navigation-help'),'פתיחה','transition')
    transition('התאמה','התאמת משפטים','בעמוד 2: באנגלית יש קו. בעברית יש מספר. כותבים את מספר התרגום על הקו.')
    for idx in [1,4,8,18]:
        item=DATA['matching'][idx]; correct=DATA['matching_order'].index(idx)+1
        decoy=(correct+7)%20+1
        opts=sorted([correct,decoy])
        choices='<div class="match-options">'+''.join(f'<button class="match-option" type="button" aria-pressed="false"><b>{n}.</b> {E(DATA["matching"][DATA["matching_order"][n-1]]["he"])}</button>' for n in opts)+'</div>'
        pair('התאמה',f'התאמה · משפט באנגלית {idx+1}',item['en'],f'{correct}',f'התרגום המתאים: {item["he"]}',extra=choices)
    for start in [0,10]:
        rows=''.join(f'<li><span>{E(DATA["matching"][i]["en"])}</span><b>{DATA["matching_order"].index(i)+1}</b></li>' for i in range(start,start+10))
        add(p('בדיקה לאחר עבודה עצמאית','eyebrow')+f'<h2 class="part-he">מפתח התאמות {start+1}–{start+10}</h2><ol class="match-key en" lang="en" start="{start+1}">{rows}</ol>','התאמה')
    transition('כתיבה','יצירת משפטים','בעמודים 3–4: מתחילים מחלקים מוכנים, ובהמשך בוחרים מילים ומנסחים בעצמכם.')
    selected=[0,2,3,4,6,8,10,11,12,15,20,21,22,23]
    for idx in selected:
        item=DATA['writing'][idx]
        title={'order':'סדר מילים','translate':'תרגום לאנגלית','join':'חיבור משפטים','create':'כתיבה עצמאית'}[item['type']]
        pair('כתיבה',f'B{idx+1} · {title}',item['prompt'],item['answer'],item['explain'],item['tense'],'he' if item['type']=='translate' else 'en',alternative=item.get('alternative'))
    transition('הבנה','תשובה מלאה לפי הטקסט','בעמוד 5: מאתרים מידע, מנסחים תשובה מלאה ומסבירים כשצריך. השאלות האחרונות דורשות גם הסקת מסקנות.')
    for idx in [0,1,6,7,10,13,15,16,17,18,19]:
        item=DATA['questions'][idx]
        pair('הבנה',f'C{idx+1} · Paragraph {item["ref"]}',item['q'],item['a'],item['why'])
    transition('בדיקה','בודקים דקדוק ואיות','בעמוד 1: לכל משפט יש תיקון. בדקו את הנושא, הפועל והאותיות הגדולות.')
    for i,item in enumerate(ERRORS):
        pair('בדיקה',f'תיקון {i+1}',item['bad'],item['good'],item['he'])
    add('<h2 class="part-title">בדיקה עצמית</h2>'+p('האם המשפט שלי מתאים לטקסט?','instruction')+p('האם יש בו נושא ופועל? האם הפועל מתאים לנושא?','instruction')+p('האם השתמשתי במילת הקישור שהתבקשה ובסימן פיסוק?','instruction'),'בדיקה','transition')
    add('<h2 class="part-title">המשך עבודה ובדיקה</h2>'+'<div class="resource-links"><a href="files/'+PDF+'">דף העבודה · PDF</a><a href="teacher.html">מפתח מלא לכל המשימות</a><a href="../unit-1/sentences/">הטקסט עם שמע ותרגום</a><a href="../">חזרה לכיתה ח׳</a></div>','בדיקה','transition')
    nav=''.join(f'<button data-jump="{x}">{x}</button>' for x in ['התאמה','כתיבה','הבנה','בדיקה'])
    doc=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>כיתה ח׳ · The Monkey Festival · דף עבודה ומצגת</title><meta name="description" content="20 התאמות, 24 משימות כתיבה ו־20 שאלות על החלק הראשון של The Monkey Festival"><link rel="stylesheet" href="../../shared/deck/standard.css"><link rel="stylesheet" href="lesson.css"></head><body><a class="home" href="../" aria-label="חזרה לכיתה ח׳">⌂</a><nav class="section-nav" aria-label="חלקי המצגת">{nav}</nav><main class="stage">{''.join(slides)}</main><nav class="nav" aria-label="ניווט"><div class="nav-group"><button data-step="-1" aria-label="השקף הקודם">←</button><button data-step="1" aria-label="השקף הבא">→</button></div><a class="pdf-link" href="files/{PDF}">PDF</a><span class="progress" id="counter"></span></nav><div class="progress-track"><div class="progress-fill"></div></div><script src="../../shared/deck/standard.js"></script><script src="practice.js"></script><noscript>הפעילו JavaScript לצפייה במצגת. דף העבודה זמין בקישור PDF.</noscript></body></html>'''
    (OUT/'index.html').write_text(doc)
    return len(slides)

def build_key():
    sections=[]
    sections.append('<h2>תיקון דקדוק ואיות · עמוד 1</h2><ol>'+''.join('<li>'+p(e['good'],'en','en')+p(e['he'])+'</li>' for e in ERRORS)+'</ol>')
    sections.append('<h2>התאמות · עמוד 2</h2><ol>'+''.join('<li>'+p(f'{m["en"]} = {DATA["matching_order"].index(i)+1}','en','en')+'</li>' for i,m in enumerate(DATA['matching']))+'</ol>')
    sections.append('<h2>יצירת משפטים · עמודים 3–4</h2><p>אלה תשובות אפשריות. מקבלים ניסוח אחר אם הוא תקין, מתאים להנחיה ומבוסס על הטקסט. בסידור חלקים משתמשים בכל החלקים.</p><ol>'+''.join('<li>'+p(m['prompt'],'prompt','he' if m['type']=='translate' else 'en')+p(m['answer'],'en','en')+(p(m['alternative'],'en alt','en') if m.get('alternative') else '')+p(m['explain'])+'</li>' for m in DATA['writing'])+'</ol>')
    sections.append('<h2>הבנה וחשיבה · עמוד 5</h2><ol>'+''.join('<li>'+p(m['q'],'prompt en','en')+p(m['a'],'en','en')+p(m['why'])+p('Paragraph '+m['ref'],'ref en','en')+'</li>' for m in DATA['questions'])+'</ol>')
    (OUT/'teacher.html').write_text('''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>מפתח תשובות · The Monkey Festival</title><style>body{max-width:900px;margin:auto;padding:28px;font:18px/1.7 Arial,sans-serif;color:#142536;background:#f7fafb}a{color:#08677b}h1,h2{line-height:1.3}h2{border-top:2px solid #9fbec7;padding-top:22px;margin-top:35px}li{padding:12px 5px;border-bottom:1px solid #ccd9df}.en{direction:ltr;text-align:left;font-size:19px}.prompt{font-weight:bold}.alt{color:#186c4e}.ref{font-size:14px;color:#456}p{margin:8px 0}@media print{body{font-size:12px}.en{font-size:12px}li{break-inside:avoid}nav{display:none}}</style></head><body><nav><a href="./">למצגת</a> · <a href="../">לכיתה ח׳</a></nav><h1>The Monkey Festival · מפתח מלא</h1><p>החלק הראשון בלבד, פסקאות A–F. אפשר לתרגל עם הטקסט פתוח. אין להסיק שהמספר ראה היום מלחמת אוכל רק מפני ששמע על כך ומקווה לראות אחת.</p><p>הצעת שימוש: קריאה ובדיקה קצרה; התאמות; כתיבה אישית; בדיקת דוגמאות נבחרות במצגת; שאלות הבנה. אפשר לפצל לשני שיעורים. לתלמידים הזקוקים לתמיכה מתחילים במשימות הכתיבה 1–8; לאחרים נותנים גם משימות ניסוח עצמאיות.</p>'''+''.join(sections)+'</body></html>')

if __name__=='__main__':
    assert len(DATA['matching'])==20 and len(DATA['writing'])==24 and len(DATA['questions'])==20
    assert sorted(DATA['matching_order'])==list(range(20))
    assert all(i!=j for i,j in enumerate(DATA['matching_order']))
    build_pdf();count=build_deck();build_key()
    print(json.dumps({'pdf_pages':5,'slides':count,'matching':20,'writing':24,'questions':20,'grammar':4,'source_words':len(' '.join(p['text'] for p in PARAS).split())}))
