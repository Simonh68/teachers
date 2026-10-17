from pathlib import Path
import ctypes
import ctypes.util
import json
import re

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'files'
OUT.mkdir(parents=True, exist_ok=True)
for name, file in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + file))

fb = ctypes.CDLL(ctypes.util.find_library('fribidi'))
fb.fribidi_get_bidi_type.argtypes = [ctypes.c_uint32]
fb.fribidi_get_bidi_type.restype = ctypes.c_uint32
fb.fribidi_log2vis.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_int,
    ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32),
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
fb.fribidi_log2vis.restype = ctypes.c_int

def rtl(text):
    n = len(text)
    src = (ctypes.c_uint32*n)(*[ord(c) for c in text])
    dst = (ctypes.c_uint32*n)()
    direction = ctypes.c_uint32(fb.fribidi_get_bidi_type(ord('א')))
    fb.fribidi_log2vis(src,n,ctypes.byref(direction),dst,None,None,None)
    return ''.join(chr(v) for v in dst)

W,H = A4
M=40
R=W-M
INK=colors.HexColor('#17252C')
MUTED=colors.HexColor('#53646B')
RULE=colors.HexColor('#A5AFB3')
LIGHT=colors.HexColor('#F0F3F4')

STORY = [
'''On Monday evening, Noam opened the school website on his family's computer. His class had already planned a book sale for a community library. He wanted to make friends with Eitan, the new boy, so he asked him to help with the display. Eitan's answer appeared a minute later: “Do it yourself.” Noam read the three words again. They sounded like an order. “He thinks he is better than me,” Noam told his brother. He felt his face grow hot. Instead of asking for an explanation, he started writing an angry answer, then stopped. Tomorrow, he decided, he would cancel their work together.''',
'''The next morning, Noam put the books on the table alone. His main concern was the welcome sign. The letters were uneven, and the table looked empty. When Eitan approached him with a large blue bag, Noam turned away. “You don't need to help,” he said. “I can see that you don't want to.” Eitan put down the bag. “What about the rest of my message?” he asked. Noam showed him the screen. Eitan looked surprised. “The second part is missing! I wrote, ‘Do it yourself for now. My little brother needs help. I can bring the stand tomorrow.’”''',
'''From his bag, Eitan took out a wooden stand. There was blue paint on his fingers. He and his father had finished making it late the night before. Suddenly, Noam understood why Eitan had answered so quickly. “I have never felt so embarrassed about assuming the worst,” Noam said. “But I didn't know for sure.” “My first words were unfriendly,” Eitan replied. “I agree. I have learned that explaining things clearly matters.” For a moment, neither boy spoke. Then Noam moved the books, and Eitan placed the stand in the middle. The welcome sign fitted perfectly.''',
'''Noam still remembered the hurt he felt. A missing sentence did not immediately make that feeling disappear. However, the stand was evidence that Eitan cared about their project. “Helping your brother was important, and I appreciate your coming today,” Noam said. That afternoon, they wrote a short rule for their next project: “If a message sounds strange, ask before you assume.” In other words, three words do not always tell the whole story. As the first visitors arrived, Eitan stood behind the table. Noam moved his own chair beside him. “This one is yours,” he said. Eitan sat down, and they opened the first box together.'''
]

EVENTS = [
    'Noam asks Eitan to help with the display.',
    'Noam reads only the words “Do it yourself.”',
    'Noam decides to cancel their work together.',
    'The next morning, Noam turns away from Eitan.',
    'Eitan explains that part of his message is missing.',
    'Eitan takes a wooden stand out of his bag.',
    'That afternoon, the boys write a rule for their next project.',
    'Eitan sits down, and the boys open the first box together.'
]
ORDER=[5,1,7,3,0,6,2,4]
TF = [
 ('Noam sent Eitan an angry answer.',False,'Noam started writing an angry answer, but he stopped.','A'),
 ('The letters on the welcome sign were uneven.',True,None,'B'),
 ('Eitan and his father made the stand together.',True,None,'C'),
 ('Noam received all of Eitan’s message.',False,'Noam received only part of the message.','B'),
 ('Noam knew from the start that Eitan wanted to help.',False,'At first, Noam thought that Eitan did not want to help.','A-B'),
 ('Eitan agreed that his first words were unfriendly.',True,None,'C'),
 ('Noam’s hurt feelings disappeared immediately.',False,'Noam’s hurt feelings did not disappear immediately.','D'),
 ('At the end, the boys opened the first box together.',True,None,'D')
]
MATCH = [
 ('Noam wanted to become friends with the new boy.','נועם רצה להתיידד עם הילד החדש.'),
 ('The class planned a book sale for a community library.','הכיתה תכננה מכירת ספרים למען ספרייה קהילתית.'),
 ('The short message made Noam feel angry and hurt.','ההודעה הקצרה גרמה לנועם להרגיש כועס ופגוע.'),
 ('Noam began an angry reply, but he did not send it.','נועם התחיל לכתוב תשובה כועסת, אבל לא שלח אותה.'),
 ('He decided to stop working with Eitan.','הוא החליט להפסיק לעבוד עם איתן.'),
 ('The welcome sign was Noam’s main concern.','שלט קבלת הפנים היה הדאגה העיקרית של נועם.'),
 ('Eitan arrived with a large blue bag.','איתן הגיע עם תיק כחול גדול.'),
 ('Noam received only part of Eitan’s message.','נועם קיבל רק חלק מההודעה של איתן.'),
 ('Eitan needed to help his little brother.','איתן היה צריך לעזור לאחיו הקטן.'),
 ('Eitan offered to bring the stand the next day.','איתן הציע להביא את המעמד למחרת.'),
 ('Eitan and his father made the stand together.','איתן ואביו הכינו יחד את המעמד.'),
 ('Noam felt embarrassed about his mistake.','נועם הרגיש נבוך בגלל הטעות שלו.'),
 ('Eitan learned to explain things clearly.','איתן למד להסביר דברים בצורה ברורה.'),
 ('Noam’s hurt feelings did not disappear at once.','תחושת הפגיעה של נועם לא נעלמה מיד.'),
 ('The boys decided to ask before making assumptions.','הילדים החליטו לשאול לפני שהם מניחים הנחות.'),
 ('Noam moved his chair beside Eitan.','נועם העביר את הכיסא שלו ליד איתן.')
]
HE_ORDER=[8,3,12,0,10,6,14,5,15,2,9,13,7,1,11,4]
MATCH_KEY=[HE_ORDER.index(i)+1 for i in range(len(MATCH))]

QUESTIONS = [
 ('What did the class plan to do for the community library?',
  'The class planned a book sale for the community library.','A'),
 ('Why did Noam ask Eitan to help with the display?',
  'He wanted to make friends with Eitan, the new boy.','A'),
 ('Which three words appeared in Eitan’s message?',
  '“Do it yourself.”','A'),
 ('Why did the words “Do it yourself” hurt Noam?',
  'Noam thought that Eitan believed he was better than Noam.','A'),
 ('What did Noam do instead of asking for an explanation?',
  'He started writing an angry answer, but then he stopped.','A'),
 ('What did Noam decide to cancel?',
  'He decided to cancel their work together.','A'),
 ('What was Noam’s main concern the next morning?',
  'His main concern was the welcome sign.','B'),
 ('Give one detail that shows a problem with the display.',
  'The letters were uneven. / The table looked empty.','B'),
 ('How did Noam react when Eitan approached him?',
  'He turned away and told Eitan that he did not need to help.','B'),
 ('Why couldn’t Eitan help Noam right away?',
  'He needed to help his little brother first.','B'),
 ('What did Eitan offer to bring, and when?',
  'He offered to bring the stand the next day.','B'),
 ('Who made the stand, and when did they finish it?',
  'Eitan and his father made it. They finished late the night before.','C'),
 ('What does the blue paint on Eitan’s fingers suggest?',
  'It suggests that he had been painting the stand. / He probably painted the stand.','C'),
 ('Why did Noam feel embarrassed?',
  'He had assumed the worst about Eitan without knowing the whole story.','C'),
 ('What did Eitan learn about writing messages?',
  'He learned that it is important to explain things clearly.','C'),
 ('Did Noam stop feeling hurt immediately? Explain.',
  'No. The missing sentence did not immediately make his hurt feelings disappear.','D'),
 ('What rule did the boys write for their next project?',
  '“If a message sounds strange, ask before you assume.”','D'),
 ('What does Noam’s action with the chair show? Explain.',
  'It shows that he wants to include Eitan and work with him. He moves the chair beside Eitan and offers it to him.','D')
]
FIX = [
 ('Eitan carryed a blue bag.','Eitan carried a blue bag.','בפועל שמסתיים בעיצור ואחריו האות ואי, מחליפים אותה בסיומת איי־אי־די בזמן עבר.'),
 ('Noam did not sent the angry answer.','Noam did not send the angry answer.','אחרי דיד נוט משתמשים בצורת הבסיס של הפועל.'),
 ('The two boys was ready to work together.','The two boys were ready to work together.','הנושא הוא ברבים, ולכן משתמשים בוור ולא בווז.')
]

def lines(text, width, font='Sans',size=11,he=False):
    result=[]; current=''
    for word in text.split():
        candidate=(current+' '+word).strip()
        visual=rtl(candidate) if he else candidate
        if pdfmetrics.stringWidth(visual,font,size)<=width:
            current=candidate
        else:
            if current: result.append(current)
            current=word
    if current:result.append(current)
    return result

def draw_text(c,text,x,top,size=11,font='Sans',color=INK):
    c.setFillColor(color);c.setFont(font,size)
    c.drawString(x,H-top-size,text)

def heb(c,text,right,top,size=11,font='Sans',color=INK):
    c.setFillColor(color);c.setFont(font,size)
    c.drawRightString(right,H-top-size,rtl(text))

def paragraph(c,text,x,top,width,size=11,leading=16,font='Sans',he=False):
    ls=lines(text,width,font,size,he)
    for idx,line in enumerate(ls):
        if he:heb(c,line,x+width,top+idx*leading,size,font)
        else:draw_text(c,line,x,top+idx*leading,size,font)
    return top+len(ls)*leading

def line(c,x1,x2,top,color=RULE):
    c.setStrokeColor(color);c.setLineWidth(.5)
    c.line(x1,H-top,x2,H-top)

def box(c,x,top,width,height,fill=None):
    c.setStrokeColor(RULE);c.setLineWidth(.6)
    if fill:c.setFillColor(fill)
    c.rect(x,H-top-height,width,height,fill=bool(fill),stroke=True)

def base(c,page,total,section,teacher=False):
    draw_text(c,'THE MESSAGE WITHOUT A VOICE',M,25,10,'Bold')
    heb(c,'מפתח למורה | כיתה ט׳' if teacher else 'הכנה למבחן | כיתה ט׳',R,25,10,'Bold')
    line(c,M,R,47,INK)
    draw_text(c,section,M,60,19,'Bold')
    if not teacher:
        heb(c,'שם: ____________________    כיתה: ______    תאריך: __________',R,91,10)
    line(c,M,R,799)
    draw_text(c,'Grade 9 | Reading comprehension',M,809,8,color=MUTED)
    c.setFont('Sans',8);c.setFillColor(MUTED)
    c.drawRightString(R,H-817,f'{page} / {total}')

def section(c,title,hetitle,top):
    draw_text(c,title,M,top,13,'Bold')
    heb(c,hetitle,R,top,12,'Bold')

def student():
    path=OUT/'Grade9-The-Message-Without-a-Voice-Worksheets.pdf'
    c=canvas.Canvas(str(path),pagesize=A4)
    c.setTitle('Grade 9 - The Message Without a Voice - Worksheets')
    c.setAuthor('Simon Halevi | English for Noar')
    base(c,1,6,'Read the story')
    heb(c,'קראו את הסיפור. תוכלו לחזור אליו בכל הפעילויות.',R,116,11)
    top=147
    for i,p in enumerate(STORY):
        draw_text(c,chr(65+i),M,top,12,'Bold')
        top=paragraph(c,p,M+23,top,W-2*M-23,11.1,16.0)+15
    assert top<782,top
    c.linkURL('https://simonh68.github.io/teachers/grade9/unit-1/reading.html',
              (M,H-788,R,H-771),relative=0)
    heb(c,'האותיות לצד הפסקאות נועדו לעזור לכם למצוא מידע בסיפור.',R,774,9,color=MUTED)
    c.showPage()

    base(c,2,6,'Follow the plot')
    section(c,'1. Put the events in order','סידור העלילה',119)
    heb(c,'כתבו מספר בכל ריבוע: 1 לאירוע הראשון, ועד 8 לאירוע האחרון.',R,141,10.5)
    top=166
    for idx in ORDER:
        box(c,M,top+1,18,18)
        end=paragraph(c,EVENTS[idx],M+28,top,W-2*M-28,10.4,13)
        assert end-top<=27
        top+=27
    section(c,'2. True or false?','נכון או לא נכון?',397)
    heb(c,'הקיפו נכון או לא נכון. אם המשפט שגוי, כתבו תיקון באנגלית בשורה.',R,419,10.4)
    top=444
    for i,(s,truth,correction,ref) in enumerate(TF,1):
        draw_text(c,f'{i}. {s}',M,top,10.0)
        heb(c,'נכון / לא נכון',R,top,9.2)
        line(c,M+20,R,top+32)
        top+=42
    c.showPage()

    base(c,3,6,'Match the meanings')
    heb(c,'התאימו כל משפט באנגלית לתרגום שלו בעברית.',R,116,11)
    heb(c,'כתבו על הקו משמאל את מספר התרגום המתאים. השתמשו בכל מספר פעם אחת.',R,134,10.2)
    split=309;top=162;row=37.7
    draw_text(c,'English',M+31,top,11,'Bold')
    heb(c,'עברית',R,top,11,'Bold')
    top+=24
    for i,(en,_) in enumerate(MATCH):
        if i%2==0:
            c.setFillColor(LIGHT);c.rect(M,H-top-row,W-2*M,row,fill=1,stroke=0)
        line(c,M+4,M+25,top+20,INK)
        el=lines(en,split-M-43,'Sans',10.0)
        assert len(el)<=2,(en,el)
        paragraph(c,en,M+34,top+5,split-M-43,10.0,13)
        heb(c,str(i+1)+'.',R-5,top+5,10.0,'Bold')
        ht=MATCH[HE_ORDER[i]][1]
        hl=lines(ht,R-split-38,'Sans',10.3,True)
        assert len(hl)<=2,(ht,hl)
        paragraph(c,ht,split+9,top+5,R-split-38,10.3,13,he=True)
        top+=row
    assert top<793,top
    c.setStrokeColor(RULE);c.line(split,H-183,split,H-top)
    c.showPage()

    for part in range(3):
        start=part*6
        base(c,part+4,6,f'Answer the questions | {start+1}-{start+6}')
        heb(c,'ענו באנגלית במשפטים קצרים וברורים. הסתמכו על הסיפור.',R,116,10.6)
        if part<2:
            heb(c,'בשאלות שמתחילות במילה מדוע, הסבירו את הסיבה.',R,134,10.2)
        else:
            heb(c,'בשאלות שדורשות הסבר, הוסיפו פרט מהסיפור.',R,134,10.2)
        top=165
        step=99 if part<2 else 76
        for qn in range(start,start+6):
            q=QUESTIONS[qn][0]
            end=paragraph(c,f'{qn+1}. {q}',M,top,W-2*M,11.2,15,'Bold')
            for ln in range(3 if part<2 else 2):
                line(c,M+18,R,end+18+ln*18)
            top+=step
        if part==2:
            top=628
            section(c,'Optional: fix the sentence','רשות: תיקון כתיב ודקדוק',top)
            heb(c,'בכל משפט יש שגיאה אחת. כתבו את המשפט המתוקן.',R,top+23,10.3)
            top+=48
            for i,(bad,good,rule) in enumerate(FIX,1):
                draw_text(c,f'{i}. {bad}',M,top,10.4)
                line(c,M+18,R,top+28)
                top+=38
        c.showPage()
    c.save()
    return path

def teacher():
    path=OUT/'Grade9-The-Message-Without-a-Voice-Answer-Key.pdf'
    c=canvas.Canvas(str(path),pagesize=A4)
    c.setTitle('Grade 9 - The Message Without a Voice - Answer Key')
    c.setAuthor('Simon Halevi | English for Noar')
    base(c,1,3,'Teacher answer key',True)
    heb(c,'תשובות לדוגמה: קבלו כל ניסוח נכון המבוסס על הסיפור.',R,101,11)
    section(c,'1. Plot order','סדר המספרים מלמעלה למטה',135)
    draw_text(c,'6, 2, 8, 4, 1, 7, 3, 5',M,159,14,'Bold')
    section(c,'2. True / false','נכון, לא נכון ותיקונים',201)
    top=230
    for i,(s,truth,correction,ref) in enumerate(TF,1):
        text=f'{i}. '+('TRUE' if truth else 'FALSE')+f' [{ref}]'
        draw_text(c,text,M,top,10.5,'Bold')
        if correction:paragraph(c,correction,M+100,top,W-2*M-100,10.2,14)
        top+=39 if correction else 27
    section(c,'3. Sentence matching','לפי סדר המשפטים באנגלית',530)
    draw_text(c,', '.join(str(n) for n in MATCH_KEY),M,556,11.2,'Bold')
    heb(c,'ההתאמה נבדקה כך שלכל משפט יש תרגום אחד, ללא חזרות.',R,581,10.4)
    section(c,'Suggested timing','חלוקת זמן מוצעת',632)
    heb(c,'קריאה: 5 דקות | סדר עלילה: 7 דקות | נכון ולא נכון: 10 דקות',R,659,10.6)
    heb(c,'התאמה: 12 דקות | שאלות פתוחות: 26 דקות',R,683,10.6)
    heb(c,'תרגיל תיקון השגיאות מיועד למי שסיים מוקדם או להמשך בבית.',R,717,10.4)
    c.showPage()

    for part,(start,endq) in enumerate([(0,9),(9,18)]):
        base(c,part+2,3,f'Open questions | {start+1}-{endq}',True)
        heb(c,'האות בסוגריים מציינת את הפסקה המתאימה בדף הקריאה.',R,100,10.5)
        top=130
        for i in range(start,endq):
            q,ans,ref=QUESTIONS[i]
            if part==0:
                top=paragraph(c,f'{i+1}. {q}',M,top,W-2*M,10.6,14,'Bold')+5
                top=paragraph(c,ans+f' [{ref}]',M+16,top,W-2*M-16,10.5,14)+20
            else:
                top=paragraph(c,f'{i+1}. {ans} [{ref}]',M,top,W-2*M,10.5,14)+15
        if part==1:
            heb(c,'בשאלות 13 ו־18 נדרשת מסקנה סבירה המבוססת על פרטי הסיפור.',R,top+4,10.2)
            top+=42
            section(c,'Optional: corrections','תיקון שגיאות',top)
            top+=29
            rules=[
                'Spelling: consonant + y becomes -ied in the past (carry → carried).',
                'Grammar: after did not, use the base form (send).',
                'Grammar: use were with the plural subject the two boys.'
            ]
            for i,((bad,good,_),rule) in enumerate(zip(FIX,rules),1):
                top=paragraph(c,f'{i}. {good}',M,top,W-2*M,10.6,14,'Bold')+3
                top=paragraph(c,rule,M+16,top,W-2*M-16,10.2,14)+13
        assert top<791,('teacher',part,top)
        c.showPage()
    c.save()
    return path

if __name__=='__main__':
    assert sorted(ORDER)==list(range(8))
    assert sorted(HE_ORDER)==list(range(16))
    assert all(HE_ORDER[i]!=i for i in range(16))
    assert len(QUESTIONS)==18
    files=[student()]
    print(json.dumps({'files':[str(p) for p in files], 'story_words':len(' '.join(STORY).split()),
          'matching_answers':MATCH_KEY},ensure_ascii=False))
