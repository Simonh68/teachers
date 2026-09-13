from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

R=Path(__file__).parent; O=R/'repo/grade8/monkey-festival/files';O.mkdir(parents=True,exist_ok=True)
d=json.loads((O.parent/'lesson.json').read_text())
fonts=Path('/root/.local/share/fonts/teacher')
for family in ('Nunito','Heebo'):
    for style in ('Regular','Bold'):
        pdfmetrics.registerFont(TTFont(family+style,str(fonts/(family+'-'+style+'.ttf'))))
W,H=A4; margin=43; usable=W-2*margin
c=Canvas(str(O/'monkey-festival-practice.pdf'),pagesize=A4)
c.setTitle('The Monkey Festival - Grade 8 exam preparation')
c.setAuthor('Simon Halevi - Teacher')
body=ParagraphStyle('body',fontName='NunitoRegular',fontSize=11.3,leading=14.6,textColor=HexColor('#15263a'))
small=ParagraphStyle('small',parent=body,fontSize=9,leading=11.5)
def p(text,y,style=body):
    q=Paragraph(text,style);_,h=q.wrap(usable,1000);q.drawOn(c,margin,y-h);return y-h
def header(sub):
    c.setFillColor(HexColor('#07111f'));c.rect(0,H-94,W,94,fill=1,stroke=0)
    c.setFillColor(HexColor('#dfff5b'));c.setFont('NunitoBold',24);c.drawString(margin,H-39,'The Monkey Festival')
    c.setFillColor(HexColor('#ffffff'));c.setFont('NunitoRegular',11);c.drawString(margin,H-65,sub)
def footer(n):
    c.setFont('NunitoRegular',8);c.setFillColor(HexColor('#435568'))
    c.drawString(margin,25,'Grade 8 | 14 September 2026 | Exam preparation')
    c.drawRightString(W-margin,25,str(n)+' / 2')
header('Reading text | Keep this page open while you answer the questions.')
y=H-112
for i,row in enumerate(d['paragraphs']):
    if i in (0,6):
        if i==6: y-=14
        c.setFillColor(HexColor('#075873'));c.setFont('NunitoBold',12)
        c.drawString(margin,y,'PART ONE' if i==0 else 'PART TWO');y-=20
    letter=row['label'].split(' · ')[-1]
    txt=row['text'].replace('–','-').replace('’',"'")
    y=p('<font name="NunitoBold">'+letter+'.</font> '+escape(txt),y)-7
y-=2
y=p('Reading support: unusual = not usual; annual = once a year; valuable = worth a lot; honor = show respect.',y,small)
y=p('Source: the Grade 8 October test in the teacher’s archive. Paragraph letters were added for practice.',y-5,small)
assert y>38,y
footer(1);c.showPage()
header('Independent work | Return to Zoom at 12:25. Submit by 12:40.')
y=H-115
y=p('First name: _______________________  Class: __________',y)-14
y=p('<font name="NunitoBold">A. Reading</font> - Answer in English. Add the paragraph letter.',y)-10
questions=[
'When does the festival take place each year?',
'What do many people wear at the festival?',
'Name two valuable things that the monkeys take.',
'Why should visitors be careful around the monkeys?',
'Why do people believe the monkeys can bring them good luck?']
for i,q in enumerate(questions,1):
    y=p(f'<font name="NunitoBold">{i}.</font> '+q,y)-6
    c.setStrokeColor(HexColor('#b7c1cc'));c.line(margin,y-12,W-margin,y-12);y-=31
y=p('<font name="NunitoBold">B. Translation</font> - Write these sentences in English.',y)-10
for i,t in enumerate(['אני בפסטיבל.','אני אוהב את הפסטיבל.','אני יכול להיות בפסטיבל.'],1):
    c.setFillColor(HexColor('#15263a'))
    c.setFont('NunitoBold',11);c.drawString(margin,y-12,str(i)+'.')
    c.setFont('HeeboRegular',12);c.drawRightString(W-margin,y-12,t[::-1]);y-=25
    c.line(margin,y-9,W-margin,y-9);y-=28
y=p('<font name="NunitoBold">C. Group 01</font> - Complete with: however / care',y)-9
y=p('1. It was hard. __________, I tried.',y)-6
y=p('2. The baby needs __________.',y)-13
y=p('<font name="NunitoBold">D. Optional challenge</font> - Would you visit this festival? Write two sentences and use one detail from the text. Write on a separate page.',y,small)-8
y=p('Before submitting: check your answers, paragraph letters, capital letters and full stops.',y,small)
assert y>38,y
footer(2);c.save()
print('PDF ready; final baseline:',round(y))
