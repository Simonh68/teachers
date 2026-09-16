from pathlib import Path
import json, html, re
from fontTools.ttLib import TTFont as Font
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade9/message-exam-practice'
FONTS=Path(__file__).resolve().parent/'fonts';FONTS.mkdir(exist_ok=True)
for weight,name in [(600,'Nunito'),(800,'NunitoBold')]:
    dest=FONTS/f'{name}.ttf'
    if not dest.exists():
        f=Font(FONTS/'Nunito-Variable.ttf')
        instantiateVariableFont(f,{'wght':weight},inplace=True).save(dest)
    pdfmetrics.registerFont(TTFont(name,str(dest)))
pdfmetrics.registerFontFamily('Nunito',normal='Nunito',bold='NunitoBold')
story=[
'On Monday evening, Noam opened the school website on his family\'s computer. His class was preparing a book sale for a community library. He wanted to make friends with Eitan, the new boy, so he asked him to help with the display. Eitan\'s answer appeared a minute later: “Do it yourself.”',
'Noam read the three words again. They sounded like an order. “He thinks he is better than me,” Noam told his brother. He felt his face grow hot. He started writing an angry answer, then stopped. Tomorrow, he decided, he would cancel their work together.',
'The next morning, Noam put the books on the table alone. His main concern was the welcome sign. The letters were uneven, and the table looked empty. When Eitan approached him with a large blue bag, Noam turned away. “You don\'t need to help,” he said. “I can see that you don\'t want to.”',
'Eitan put down the bag. “What about the rest of my message?” he asked. Noam showed him the screen. Eitan looked surprised. “The second part is missing! I wrote, ‘Do it yourself for now. My little brother needs help. I can bring the stand tomorrow.’”',
'From his bag, Eitan took out a wooden stand. There was blue paint on his fingers. He and his father finished it late the night before. Suddenly, Noam understood why Eitan answered so quickly.',
'“I assumed you were angry,” Noam said. “But I didn\'t know for sure.”',
'“My first words were unfriendly,” Eitan replied. “I agree. I should explain things more clearly.”',
'For a moment, neither boy spoke. Then Noam moved the books, and Eitan placed the stand in the middle. The welcome sign fitted perfectly.',
'Noam still remembered the hurt he felt. A missing sentence did not immediately make that feeling disappear. However, the stand was evidence that Eitan cared about their project. Noam thanked him and asked about his brother.',
'That afternoon, they wrote a short rule for their next project: “If a message sounds strange, ask before you assume.” In other words, three words do not always tell the whole story.',
'As the first visitors arrived, Eitan stood behind the table. Noam moved his own chair beside him. “This one is yours,” he said. Eitan sat down, and they opened the first box together.'
]
(OUT/'story.json').write_text(json.dumps(story,ensure_ascii=False,indent=2))
W,H=A4;M=43;IW=W-2*M
INK=HexColor('#132840');TEAL=HexColor('#087C8F');GREY=HexColor('#5A6775')
c=Canvas(str(OUT/'files/message-exam-practice.pdf'),pagesize=A4)
c.setTitle('Grade 9 — The Message Without a Voice — Exam practice')
c.setAuthor('Simon • English for Noar')
body=ParagraphStyle('body',fontName='Nunito',fontSize=11.5,leading=15.2,textColor=INK)
question=ParagraphStyle('question',parent=body,fontSize=11.5,leading=16)
small=ParagraphStyle('small',parent=body,fontSize=9.3,leading=12.5,textColor=GREY)
def para(text,y,style=body,x=M,width=IW):
    p=Paragraph(text,style);_,h=p.wrap(width,H);p.drawOn(c,x,y-h);return y-h
def header(page,title,subtitle):
    c.setFillColor(TEAL);c.rect(0,H-8,W,8,fill=1,stroke=0)
    c.setFillColor(TEAL);c.setFont('NunitoBold',10);c.drawString(M,H-37,'GRADE 9  /  EXAM PRACTICE')
    c.setFillColor(INK);c.setFont('NunitoBold',21);c.drawString(M,H-68,title)
    para(subtitle,H-83,small)
    c.setStrokeColor(HexColor('#B6C5D0'));c.line(M,36,W-M,36)
    c.setFont('Nunito',8.5);c.setFillColor(GREY);c.drawString(M,23,'English for Noar • The Message Without a Voice');c.drawRightString(W-M,23,f'{page} / 3')
    return H-116
def lines(y,n=2,gap=21):
    c.setStrokeColor(HexColor('#A9B9C5'));c.setLineWidth(.45)
    for _ in range(n):c.line(M,y,W-M,y);y-=gap
    return y
y=header(1,'The Message Without a Voice','Name: __________________________  Class: __________  Date: ______________')
y=para('Read again. Underline one misunderstanding and one action that helps the friendship.',y,small)-9
for i,p in enumerate(story):
    c.setFont('NunitoBold',10);c.setFillColor(TEAL);c.drawString(M,y-10,chr(65+i))
    y=para(html.escape(p),y,body,x=M+18,width=IW-18)-6
assert y>45,('page1 overflow',y)
c.showPage()
y=header(2,'Read • Find evidence • Explain','Write in full sentences. Add a paragraph letter when asked.')
questions=[
('1. What was the class preparing? Give the paragraph letter.',2),
('2. What did Noam think Eitan meant? What did Eitan actually mean? Use paragraphs B and D.',3),
('3. Which two details show that Eitan wanted to help? Give the paragraph letter.',3),
('4. Put the events in the correct order. Write the letters.',0),
('5. Why does Noam move his chair at the end? Explain what his action suggests. Use paragraph K.',3),
('6. Noam still feels hurt. Why does he thank Eitan anyway? Use paragraph I.',2)]
for i,(q,n) in enumerate(questions):
    y=para(q,y,question)-18
    if i==3:
        for item in ['A. Eitan explains the missing message.','B. Noam reads the short message.','C. The boys welcome the first visitors.','D. Eitan brings a wooden stand.']:
            y=para(item,y,body)-2
        y=para('Order: 1. ______     2. ______     3. ______     4. ______',y-8,question)-24
    else:y=lines(y,n,19)-8
assert y>42,('page2 overflow',y)
c.showPage()
y=header(3,'Choose • Write • Check','Circle one answer in each question. Then write your own paragraph.')
gaps=[
('1. I took your book ______. I thought it was mine.','A. on purpose     B. by mistake     C. at last'),
('2. She worked hard to ______ her goal.','A. achieve     B. describe     C. forget'),
('3. I checked the date twice. I am ______ the test is on Sunday.','A. afraid     B. lonely     C. certain'),
('4. I ______ with you.','A. agree     B. am agreeing     C. agrees'),
('5. Noam was still hurt. ______, he thanked Eitan for the stand.','A. Because     B. However     C. For example'),
('6. Noam misunderstood Eitan ______ part of the message was missing.','A. however     B. although     C. because')]
for q,options in gaps:
    y=para(q,y,question)-2;y=para(options,y,small)-13
y=para('<b>Writing · 70–100 words</b>',y-1,question)-6
y=para('Write about a misunderstanding between two friends. Explain what happened, what each friend thought, and how they solved the problem. You may invent a story.',y,body)-7
y=para('<b>Use three:</b> by mistake · however · understanding · so far · achieve · relations · certain · be responsible for something',y,small)-10
y=para('<b>Check:</b> a clear problem and solution · mainly Past Simple · because and however',y,small)-15
y=lines(y,10,20)
assert y>35,('page3 overflow',y)
c.save()
print('PDF written; story words:',len(re.findall(r"\b[\w’\'-]+\b",' '.join(story))))
