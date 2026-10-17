#!/usr/bin/env python3
"""Build the two-page Grade 7 matching and reading practice worksheet.

Requires reportlab. Hebrew strings are Hebrew-only and drawn in visual RTL
order; numeric labels and English text are drawn separately in LTR order.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'grade7' / 'exam-matching-reading' / 'Grade7-Matching-and-Reading-Practice.pdf'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('Body', str(FONT_DIR / 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('Bold', str(FONT_DIR / 'DejaVuSans-Bold.ttf')))

PAIRS = [
 ('The school year starts in summer.', 'שנת הלימודים מתחילה בקיץ.'),
 ('The school year ends in spring.', 'שנת הלימודים מסתיימת באביב.'),
 ('The holiday starts in autumn.', 'החופשה מתחילה בסתיו.'),
 ('The holiday ends in late summer.', 'החופשה מסתיימת בסוף הקיץ.'),
 ('The summer holiday is six weeks long.', 'חופשת הקיץ נמשכת שישה שבועות.'),
 ('The school holiday is about eleven weeks long.', 'החופשה מבית הספר נמשכת כאחד עשר שבועות.'),
 ('The weather is hot in summer.', 'מזג האוויר חם בקיץ.'),
 ('Children have a holiday in spring.', 'לילדים יש חופשה באביב.'),
 ('Children start school in autumn.', 'ילדים מתחילים ללמוד בבית הספר בסתיו.'),
 ('Japanese children have a long holiday.', 'לילדים יפנים יש חופשה ארוכה.'),
 ('The children have six weeks of holiday.', 'לילדים יש שישה שבועות של חופשה.'),
 ('The children have a long school year.', 'לילדים יש שנת לימודים ארוכה.'),
 ('Six children start school in England.', 'שישה ילדים מתחילים ללמוד בבית הספר באנגליה.'),
 ('Eleven children start school in Japan.', 'אחד עשר ילדים מתחילים ללמוד בבית הספר ביפן.'),
 ('Japanese children have a holiday in Florida.', 'ילדים יפנים מבלים חופשה בפלורידה.'),
 ('Children in England have a holiday in Alaska.', 'ילדים שחיים באנגליה מבלים חופשה באלסקה.'),
 ('Children in Florida have a holiday in Japan.', 'ילדים שחיים בפלורידה מבלים חופשה ביפן.'),
 ('The summer holiday in England is about six weeks long.', 'חופשת הקיץ באנגליה נמשכת כשישה שבועות.'),
 ('In Alaska, children start school in late summer.', 'באלסקה, ילדים מתחילים ללמוד בבית הספר בסוף הקיץ.'),
 ('In Florida, the weather is hot when school starts.', 'בפלורידה, מזג האוויר חם כשהלימודים מתחילים.'),
 ('The holiday starts in spring and ends in summer.', 'החופשה מתחילה באביב ומסתיימת בקיץ.'),
 ('School starts in autumn and ends in late spring.', 'הלימודים מתחילים בסתיו ומסתיימים בסוף האביב.'),
 ('The school year starts when the summer holiday ends.', 'שנת הלימודים מתחילה כשחופשת הקיץ מסתיימת.'),
 ('The summer holiday starts when the school year ends.', 'חופשת הקיץ מתחילה כששנת הלימודים מסתיימת.'),
 ('The weather is hot during the summer holiday.', 'מזג האוויר חם במהלך חופשת הקיץ.'),
 ('The children have a holiday when the weather is hot.', 'לילדים יש חופשה כשמזג האוויר חם.'),
 ('Japanese children have a summer holiday in the USA.', 'ילדים יפנים מבלים חופשת קיץ בארצות הברית.'),
 ('The children have a long holiday during the school year.', 'לילדים יש חופשה ארוכה במהלך שנת הלימודים.'),
 ('Children in Japan and England have a summer holiday.', 'לילדים ביפן ובאנגליה יש חופשת קיץ.'),
 ('The school year in England starts and ends in different seasons.', 'שנת הלימודים באנגליה מתחילה ומסתיימת בעונות שונות.'),
]

# Hebrew index at each numbered position; no translation is directly opposite
# its English sentence. Keep the shuffle stable for classroom use.
ORDER = [16, 4, 24, 12, 1, 20, 9, 27, 6, 18, 29, 2, 14, 22, 7,
         25, 11, 28, 0, 15, 5, 26, 13, 8, 21, 3, 17, 10, 23, 19]

TEXT = [
 'Children around the world start school in different seasons.',
 'In Japan, the school year starts in spring.',
 'Japanese children have a summer holiday during the school year.',
 'In Alaska, in the USA, school starts in late summer and ends in spring.',
 'The summer holiday there is about eleven weeks long.',
 'In Florida, in the USA, school starts in summer, when the weather is hot.',
 'In England, school starts in autumn and ends in summer.',
 'Children in England have about six weeks of summer holiday.',
]

QUESTIONS = [
 'When does the school year start in Japan?',
 'Do Japanese children have a summer holiday?',
 'Who has a summer holiday during the school year?',
 'Does school in Japan start in summer?',
 'Where is Alaska?',
 'When does school start in Alaska?',
 'When does school end in Alaska?',
 'How many weeks is the summer holiday in Alaska?',
 'Does school in Alaska end in summer?',
 'Is the summer holiday in Alaska about six weeks long?',
 'Where is Florida?',
 'When does school start in Florida?',
 'What is the weather like when school starts in Florida?',
 'Does school in Florida start when the weather is hot?',
 'When does school start in England?',
 'When does school end in England?',
 'How many weeks of summer holiday do children in England have?',
 'Do children in England have a summer holiday?',
 'Does school start in the same season around the world?',
 'Name two places in the USA from the text.',
]

W, H = A4
INK = HexColor('#142536')
TEAL = HexColor('#146273')
LIGHT = HexColor('#f2f6f7')
RULE = HexColor('#c7cfd4')
M = 27

def wrap(text, max_width, size, font='Body'):
    lines, cur = [], ''
    for word in text.split():
        test = (cur + ' ' + word).strip()
        if cur and pdfmetrics.stringWidth(test, font, size) > max_width:
            lines.append(cur)
            cur = word
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

def he(c, text, right, y, size=10.5, bold=False):
    c.setFont('Bold' if bold else 'Body', size)
    c.drawRightString(right, y, text[::-1])

def en(c, text, x, y, size=10.5, bold=False):
    c.setFont('Bold' if bold else 'Body', size)
    c.drawString(x, y, text)

def heading(c, title, page):
    c.setFillColor(TEAL)
    he(c, title, W-M, H-33, 17, True)
    c.setFillColor(INK)
    en(c, 'GRADE 7', M, H-31, 10, True)
    c.setStrokeColor(RULE)
    c.setLineWidth(.6)
    c.line(M, H-43, W-M, H-43)
    c.setFillColor(INK)
    he(c, 'שם: ____________________    כיתה: __________    תאריך: __________', W-M, H-61, 10)
    c.setStrokeColor(RULE)
    c.line(M, 26, W-M, 26)
    c.setFillColor(INK)
    en(c, 'School Years Around the World', M, 14, 8)
    en(c, f'{page} / 2', W-M-24, 14, 8)

def matching_page(c):
    heading(c, 'הכנה למבחן באנגלית | התאמת משפטים', 1)
    he(c, 'קרא כל משפט באנגלית. מצא את התרגום שלו בטור הימני וכתוב את המספר על הקו.', W-M, H-80, 10.3)
    he(c, 'התרגומים מעורבבים. השתמש בכל מספר פעם אחת. שים לב לכל המילים במשפט!', W-M, H-95, 10.3)
    he(c, 'אלה משפטי תרגול שנבנו ממילים שבטקסט; חלקם מתארים מצבים דמיוניים.', W-M, H-110, 9.4)
    left_x = M
    right_edge = W-M
    mid = 314
    top = H-123
    header_h = 24
    c.setFillColor(TEAL)
    c.rect(M, top-header_h, W-2*M, header_h, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    en(c, 'English', left_x+36, top-16, 10.5, True)
    he(c, 'התרגומים בעברית', right_edge-9, top-16, 10.5, True)
    fs, leading = 10.0, 11.6
    rows=[]
    for i,(english,_) in enumerate(PAIRS):
        el = wrap(english, mid-(left_x+36)-10, fs)
        hl = wrap(PAIRS[ORDER[i]][1], right_edge-mid-34, fs)
        rows.append((el,hl,max(len(el),len(hl))))
    available = top-header_h-36
    base = sum(n*leading for _,_,n in rows)
    pad = (available-base)/30
    assert pad >= 3, (base, available, pad)
    y=top-header_h
    for i,(el,hl,n) in enumerate(rows):
        rh = n*leading+pad
        if i % 2 == 0:
            c.setFillColor(LIGHT)
            c.rect(left_x,y-rh,right_edge-left_x,rh,fill=1,stroke=0)
        c.setFillColor(INK)
        baseline=y-pad/2-fs
        for k,line in enumerate(el):
            en(c,line,left_x+36,baseline-k*leading,fs)
        for k,line in enumerate(hl):
            he(c,line,right_edge-28,baseline-k*leading,fs)
        en(c,str(i+1)+'.',right_edge-22,baseline,9.7,True)
        c.setStrokeColor(HexColor('#61717c'))
        c.setLineWidth(.65)
        c.line(left_x+6,baseline-1,left_x+28,baseline-1)
        c.setStrokeColor(RULE)
        c.setLineWidth(.3)
        c.line(left_x,y-rh,right_edge,y-rh)
        y-=rh
    c.setStrokeColor(RULE)
    c.line(mid,top-header_h,mid,y)
    assert y >= 35
    print(f'Matching: font={fs}, bottom={y:.1f}, minimum vertical padding={pad:.2f}')
    c.showPage()

def reading_page(c):
    heading(c, 'הכנה למבחן באנגלית | קוראים ועונים', 2)
    he(c, 'קרא את הטקסט וענה על השאלות שמתחתיו. כל התשובות נמצאות בטקסט שבעמוד הזה.', W-M, H-81, 10.2)
    he(c, 'כתוב תשובות קצרות באנגלית על השורות. בשאלות כן או לא אפשר לענות במילה אחת.', W-M, H-96, 10.2)
    title_y=H-121
    c.setFillColor(TEAL)
    en(c,'School Years Around the World',M+10,title_y,13,True)
    c.setFillColor(INK)
    y=title_y-20
    for sentence in TEXT:
        for line in wrap(sentence,W-2*M-20,11.1):
            en(c,line,M+10,y,11.1)
            y-=14.0
        y-=3.5
    bottom=y+5
    c.setStrokeColor(RULE)
    c.roundRect(M,bottom,W-2*M,title_y+15-bottom,5,fill=0,stroke=1)
    y0=bottom-24
    c.setFillColor(TEAL)
    he(c,'ענה לפי הטקסט',W-M,y0,11,True)
    c.setFillColor(INK)
    qtop=y0-20
    colw=(W-2*M-26)/2
    rowh=(qtop-42)/10
    assert rowh >= 39, rowh
    for i,q in enumerate(QUESTIONS):
        col=0 if i<10 else 1
        row=i%10
        x=M+col*(colw+26)
        qy=qtop-row*rowh
        lines=wrap(q,colw-24,10.1)
        assert len(lines)<=2,(q,lines)
        en(c,str(i+1)+'.',x,qy,10.1,True)
        for k,line in enumerate(lines):
            en(c,line,x+23,qy-k*12.2,10.1)
        ly=qy-rowh+13
        c.setStrokeColor(HexColor('#6b7984'))
        c.setLineWidth(.55)
        c.line(x+23,ly,x+colw,ly)
    print(f'Reading: question row height={rowh:.1f}; text bottom={bottom:.1f}')
    c.showPage()

def main():
    assert len(PAIRS)==30 and len(QUESTIONS)==20 and len(TEXT)==8
    assert sorted(ORDER)==list(range(30))
    assert all(i != j for i,j in enumerate(ORDER))
    assert len(set(p[0] for p in PAIRS))==30
    assert len(set(p[1] for p in PAIRS))==30
    OUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUT),pagesize=A4,pageCompression=1)
    c.setTitle('Grade 7 - Matching and Reading Practice')
    c.setAuthor('Simon Halevi - English for Noar')
    c.setSubject('30 English-Hebrew matches; original short text; 20 reading questions')
    matching_page(c)
    reading_page(c)
    c.save()
    print(OUT)

if __name__=='__main__':
    main()
