"""Build two one-page companion PDFs from the same task data as the HTML deck.
Requires reportlab and python-bidi. Tasks 2-4 reveal their questions on screen only.
"""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from bidi.algorithm import get_display
R=Path(__file__).resolve().parents[2]
D=json.loads((Path(__file__).parent/'worksheets.json').read_text())
for name in ['Heebo','Nunito']:
 pdfmetrics.registerFont(TTFont(name,str(R/f'grade7/the-same-way/assets/{name}.ttf')))
W,H=A4
out=R/'grade7/there-is-there-are/files';out.mkdir(exist_ok=True)
for part,sections in D.items():
 c=canvas.Canvas(str(out/f'part-{part.lower()}-companion.pdf'),pagesize=A4)
 c.setTitle(f'There is / There are - Part {part} companion');c.setAuthor('Simon Halevi')
 def he(text,y,size=11):
  c.setFont('Heebo',size);c.drawRightString(W-35,y,get_display(text))
 def en(text,y,size=13,x=43):
  c.setFont('Nunito',size);c.drawString(x,y,text)
 def line(n,y):
  en(n,y+5,11);c.setStrokeColorRGB(.45,.45,.45);c.line(75,y,W-40,y)
 en('There is / There are',H-38,19);he(f'כיתה ז׳ | דף מלווה | Part {part}',H-62,14)
 he('שם: ____________________     כיתה: ________     תאריך: __________',H-86)
 he('ממלאים רק את המשימה שהמורה מציג. השאירו את התשובות הקודמות כפי שהן.',H-105,10)
 y=H-134
 for number,s in enumerate(sections,1):
  c.setFillColorRGB(.93,.93,.93);c.rect(35,y-5,W-70,24,fill=1,stroke=0);c.setFillColorRGB(0,0,0)
  he(f'{number} | '+s['title'],y+2,13);y-=24
  ins=s['instruction'] if number==1 else ('קראו את משימה '+str(number)+' בשקף. כתבו כאן '+('כל משפט בשלמותו.' if number==3 else 'רק את המילה או הביטוי שבחרתם.'))
  he(ins,y,10.5);y-=19
  # Short lexical aids remain available on paper; grammar answers do not.
  vocab=s['vocab'].split(' · ');rows=[];row=''
  for v in vocab:
   test=(row+' · '+v) if row else v
   if pdfmetrics.stringWidth(get_display(test),'Heebo',10)>W-74:
    rows.append(row);row=v
   else:row=test
  rows.append(row)
  for row in rows:he(row,y,10);y-=15
  if number==1:
   for n,x in enumerate(s['items'],1):
    he(f'{number}.{n}  '+x['he'],y,11);y-=19
    en(x['en'],y,13);y-=27
  else:
   for n,x in enumerate(s['items'],1):
    y-=18 if number!=3 else 24
    line(f'{number}.{n}',y);y-=12
  y-=18
 assert y>43,(part,y)
 he('יש מילים לא ברורות? בקשו פירוש. המטרה היא להבין את מבנה המשפט.',32,9)
 c.showPage();c.save()
 print(part,'one page; content ends at',round(y))
