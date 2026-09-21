from pathlib import Path
import json,textwrap
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from bidi.algorithm import get_display
R=Path(__file__).resolve().parents[2];D=json.loads((R/'grade7/unit-1/reading/content.json').read_text());W,H=A4
for f in ['Heebo','Nunito']:pdfmetrics.registerFont(TTFont(f,str(R/f'grade7/the-same-way/assets/{f}.ttf')))
c=canvas.Canvas(str(R/'grade7/unit-1/files/reading-workshop.pdf'),pagesize=A4)
c.setTitle('Unit 1 - Reading Workshop');c.setAuthor('Simon Halevi')
def he(t,y,size=11,x=None):c.setFont('Heebo',size);c.drawRightString(x or W-36,y,get_display(t))
def en(t,y,size=12,x=43):c.setFont('Nunito',size);c.drawString(x,y,t)
def wrap(t,width,font,size):
 lines=[];row=''
 for w in t.split():
  s=(row+' '+w).strip()
  if pdfmetrics.stringWidth(s,font,size)>width:lines.append(row);row=w
  else:row=s
 return lines+[row]
def umbrella(x,y):
 c.setLineWidth(1.5);p=c.beginPath();p.moveTo(x,y);p.curveTo(x+4,y+26,x+40,y+26,x+44,y);p.lineTo(x,y);c.drawPath(p);c.line(x+22,y+20,x+22,y-17);c.arc(x+10,y-23,x+22,y-11,180,180)
 for dx in [7,20,35]:c.line(x+dx,y+35,x+dx-3,y+29)
def bus(x,y):
 c.roundRect(x,y,65,27,5);c.rect(x+7,y+13,15,8);c.rect(x+25,y+13,15,8);c.rect(x+43,y+5,12,16);c.circle(x+14,y,5,fill=0);c.circle(x+52,y,5,fill=0)
def header(page):
 en('UNIT 1 / READ • THINK • WRITE',H-34,15);he('כיתה ז׳ | The Same Way',H-54,12)
 he('שם: ____________________    כיתה: ________    תאריך: __________',H-76,10)
 he('קראו, ענו וסמנו בטקסט ראיה. מותר להיעזר בפירושים. אל תמחקו תשובה קודמת.',H-94,9.5)
 he(f'עמוד {page} מתוך 2',25,9)
def q(n,prompt,y,lines=1):
 he(f'{n}. {prompt}',y,11);y-=23
 for k in range(lines):c.setStrokeColorRGB(.5,.5,.5);c.line(45,y,W-40,y);y-=24
 c.setStrokeColorRGB(0,0,0);he('תיקון / הוספה:',y+7,8);c.line(45,y+4,W-115,y+4)
 return y-15
header(1);umbrella(W-100,H-160)
en(D['texts'][0]['title'],H-129,17)
c.roundRect(35,H-318,W-70,173,8)
y=H-166
for s in D['texts'][0]['lines']:en(s[0],y,12);y-=20
he('rainy = גשום · open = פתוח · from = החל ב־ · wait = לחכות',H-339,10)
he('wet umbrellas = מטריות רטובות · near = ליד · under = מתחת · lessons = שיעורים',H-356,10)
he('message = הודעה · students = תלמידים · room = חדר · chairs and tables = כיסאות ושולחנות',H-373,9.5)
he('put your bags = הניחו את התיקים שלכם · friends = חברים · start = מתחילים',H-390,9.5)
y=H-416
y=q(1,'למי מיועדת ההודעה?',y)
y=q(2,'הגעתם ביום גשום בשעה 7:40. לאיזה חדר תוכלו להיכנס?',y)
y=q(3,'היכן מניחים את התיקים?',y)
he('4. כתבו הודעה משלכם: בחרו חדר ושעה, והשלימו את שלוש השורות.',y,11);y-=24
en('Room ____ is open from ________.',y,12);y-=29
en('There are ____________________ in the room.',y,12);y-=29
en('Please put your bags ________________________.',y,12);y-=24
he('לעזרה: chairs = כיסאות · tables = שולחנות · near the door = ליד הדלת',y,9.5);y-=17
he('בהשוואה בזוגות: הראו היכן מצאתם ראיה לשאלות 1–3.',y,9.5)
assert y>40,y
c.showPage();header(2);bus(W-108,H-143)
en(D['texts'][1]['title'],H-125,17)
y=H-151
paras=[' '.join(x[0] for x in D['texts'][1]['lines'][:3]),' '.join(x[0] for x in D['texts'][1]['lines'][3:6]),' '.join(x[0] for x in D['texts'][1]['lines'][6:8]),' '.join(x[0] for x in D['texts'][1]['lines'][8:])]
for paragraph in paras:
 for row in wrap(paragraph,W-85,'Nunito',11.5):en(row,y,11.5);y-=16
 y-=5
he('choose = בוחרים · subject = מקצוע לימוד · journey = נסיעה · harder = קשה יותר',y-2,9.5);y-=19
he('different ways = דרכים שונות · far away = רחוק · together = יחד · arrive = מגיעים',y-2,9.5);y-=27
for row in ['children = ילדים · get to school = מגיעים לבית הספר · some = חלקם', 'walk = הולכים ברגל · take a bus or a train = נוסעים באוטובוס או ברכבת', 'near home = קרוב לבית · easy = קל · want to study = רוצים ללמוד', 'music = מוזיקה · science = מדעים · another = אחר · like = אוהבים', 'long = ארוכה · takes time = דורשת זמן · travel = נוסעים · talk = מדברים', 'on the way = בדרך · tired = עייפים · happy = שמחים · but = אבל']:
 he(row,y,9.5);y-=16
y-=5
he('5. הקיפו את הנושא המרכזי:',y,11);y-=18
he('דרכים להגיע לבית הספר / שיעורי מוזיקה בלבד / משחקים ברכבת',y,10);y-=21
he('תיקון: _________________________________________________',y,9);y-=24
y=q(6,'מדוע חלק מהילדים בוחרים בית ספר רחוק? אפשר לענות בעברית.',y)
y=q(7,'למי מתייחסת They במשפט They talk on the way?',y)
y=q(8,'כתבו דבר אחד המשותף לקטע ולסיפור The Same Way.',y)
c.setFillColorRGB(.93,.93,.93);c.rect(35,y-53,W-70,72,fill=1,stroke=0);c.setFillColorRGB(0,0,0)
he('משימות יציאה: פתרו לבד רק כשהמורה מציג הודעה חדשה.',y+3,10)
he('9. איזה חדר פתוח ב־7:25? ______________________________',y-20,10)
he('10. היכן מניחים תיקים? _________________________________',y-43,10)
assert y-53>38,(y,y-53)
c.showPage();c.save();print('PDF created: 2 pages')
