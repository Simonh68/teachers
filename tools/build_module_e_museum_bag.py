#!/usr/bin/env python3
"""Build line-locked Module E practice and its teacher key from one JSON source."""
from pathlib import Path
import json, sys, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'grade11/module-e-museum-bag'
FILES=OUT/'files';FILES.mkdir(exist_ok=True)
D=json.loads((OUT/'content.json').read_text())
W,H=A4; M=42; BODY=11.6; LEADING=16
FONTDIR=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('Times-Roman','DejaVuSerif.ttf'),('Times-Bold','DejaVuSerif-Bold.ttf'),('Helvetica','DejaVuSans.ttf'),('Helvetica-Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTDIR/file)))

def wrap(s,width,size=12,font='Times-Roman'):
    rows=[];line=''
    for word in s.split():
        trial=(line+' '+word).strip()
        if line and pdfmetrics.stringWidth(trial,font,size)>width: rows.append(line);line=word
        else:line=trial
    if line:rows.append(line)
    return rows

def text(c,s,x,y,width=W-84,size=12,font='Times-Roman',leading=None):
    c.setFont(font,size);c.setFillGray(0)
    for line in wrap(s,width,size,font):c.drawString(x,y,line);y-=leading or size*1.4
    return y

def head(c,page,section,total):
    c.setFillGray(0)
    c.setFont('Helvetica-Bold',9);c.drawString(M,H-35,'ENGLISH FOR NOAR  |  GRADE 11  |  MODULE E PRACTICE')
    c.setFont('Helvetica',9);c.drawRightString(W-M,H-35,'Bagrut Trap Killer')
    c.setLineWidth(.6);c.line(M,H-44,W-M,H-44)
    c.setFont('Times-Bold',15);c.drawString(M,H-70,section)
    c.setFont('Helvetica',8);c.drawString(M,25,'Original practice exam - not an official Ministry of Education examination.')
    c.drawRightString(W-M,25,f'{page} / {total}')
    return H-98

def locked_lines():
    rows=[]
    for p,para in enumerate(D['paragraphs'],1):
        for j,line in enumerate(wrap(para,463,BODY)):
            rows.append({'number':len(rows)+1,'paragraph':p,'start':j==0,'text':line})
    return rows

LINES=locked_lines()
(OUT/'lines.json').write_text(json.dumps(LINES,indent=2,ensure_ascii=False)+'\n')

def reading(c,total):
    y=head(c,1,'PART I: WRITTEN RECEPTION (70 points)',total)
    y=text(c,'Name: _________________________   Class: __________   Date: __________',M,y,size=11)-4
    y=text(c,'Time: 75 minutes. Answer in English. No dictionary. Total: 100 points.',M,y,size=10)-4
    y=text(c,'Read the article and answer questions 1-9. Line numbers refer to this page.',M,y,size=10.5)-9
    c.setFont('Times-Bold',16);c.drawCentredString(W/2,y,D['title']);y-=28
    romans=['I','II','III','IV','V']
    for line in LINES:
        if line['start']:
            if line['number']>1:y-=9
            c.setFont('Times-Bold',11);c.drawString(49,y,romans[line['paragraph']-1])
        c.setFillGray(.35);c.setFont('Helvetica',8);c.drawRightString(38,y,str(line['number']))
        c.setFillGray(0);c.setFont('Times-Roman',BODY);c.drawString(76,y,line['text']);y-=LEADING
    assert y>40,('reading overflow',y)
    c.showPage()

def question(c,q,y):
    label=f"{q['number']}. {q['stem']} ({q['scope']})"
    y=text(c,label,M,y,width=W-2*M,size=12,font='Times-Bold')-5
    if q['type']=='mc':
        for i,opt in enumerate(q['options']):
            y=text(c,f"{['i','ii','iii','iv'][i]})  {opt}",M+16,y,width=W-2*M-16,size=12)-3
    else:
        y=text(c,q['instruction'],M+16,y,size=10,font='Helvetica-Bold')-7
        if q.get('prefix'):y=text(c,q['prefix'],M+16,y,width=W-2*M-16,size=12)-7
        for _ in range(q.get('answer_lines',2)):
            c.setStrokeGray(.5);c.setLineWidth(.4);c.line(M+16,y,W-M,y);y-=23
    c.setFillGray(0);c.setFont('Times-Roman',10);c.drawRightString(W-M,y+1,f"({q['points']} points)")
    return y-23

def vocab(c,total):
    y=head(c,4,'PART II: LEXICAL KNOWLEDGE (30 points)',total)
    y=text(c,'Vocabulary focus: Band III Core I - List A.',M,y,size=11)-5
    y=text(c,'In each question, match three of the items 1-6 to the definitions on the right.',M,y,size=11)
    y=text(c,'Write the item number on each line. Use each item only once in each question.',M,y,size=11)
    y=text(c,'There are three extra items in every question. Each correct match is worth 2 points.',M,y,size=11)-20
    for v in D['vocabulary']:
        c.setFont('Times-Bold',12);c.drawString(M,y,f"({v['number']})")
        top=y-18
        for i,item in enumerate(v['items'],1):text(c,f'{i}. {item}',M+13,top-(i-1)*15,width=185,size=11)
        yy=top-3
        for definition in v['definitions']:
            c.setLineWidth(.4);c.setStrokeGray(.4);c.line(260,yy-1,279,yy-1)
            yy=text(c,definition,287,yy,width=W-M-287,size=10.5,leading=13)-9
        y=top-6*15-14
    assert y>38,('vocab overflow',y)
    c.showPage()

def teacher():
    out=FILES/'Module-E-Museum-Bag-Teacher-Key.pdf'
    c=canvas.Canvas(str(out),pagesize=A4);c.setTitle('Module E - More Than an Old School Bag - Teacher Key')
    y=head(c,1,'TEACHER KEY - Reading (70 points)',3)
    y=text(c,'Accept equivalent wording that preserves the required meaning. Minor language errors',M,y,size=10)
    y=text(c,'do not invalidate a clear reading answer. The trap labels are project teaching categories.',M,y,size=10)-14
    page=1
    for q in D['reading_questions']:
        if q['number']==5:
            c.showPage();page+=1;y=head(c,page,'TEACHER KEY - Reading continued',3)
        y=text(c,f"{q['number']}. {q['answer']} ({q['points']} points)",M,y,size=12,font='Times-Bold')-3
        y=text(c,'Evidence: '+q['evidence']+' ['+q['evidence_scope']+']',M,y,size=10)-2
        y=text(c,'Marking: '+q['rubric'],M,y,size=10)-2
        y=text(c,'Traps: '+', '.join(q['traps']),M,y,size=10)-2
        y=text(c,'Feedback: '+q['explanation_en'],M,y,size=10)-8
    assert y>42,('teacher overflow',y)
    c.showPage();page+=1;y=head(c,page,'TEACHER KEY - List A vocabulary (30 points)',3)
    for v in D['vocabulary']:
        y=text(c,f"{v['number']}. "+' / '.join(str(k) for k in v['keys'])+' (6 points)',M,y,size=12,font='Times-Bold')-2
        for d,k in zip(v['definitions'],v['keys']):y=text(c,f'{k}. {v["items"][k-1]}: {d}',M+12,y,size=11)-2
        y-=13
    y-=10
    y=text(c,'Vocabulary source',M,y,size=12,font='Times-Bold')
    y=text(c,'Band III Core I - List A, official spreadsheet mirrored by Katzir school.',M,y,size=10)
    y=text(c,'All 30 options were checked against entries or explicitly listed family members.',M,y,size=10)
    y=text(c,'Definitions and exam questions are original. The lexical section intentionally focuses',M,y,size=10)
    y=text(c,'on List A only, at the teacher\'s request; it is not a list of the full current E syllabus.',M,y,size=10)
    c.linkURL('https://katzir.org.il/wp-content/uploads/2024/07/Band_3-List_A-_Official.xlsx',(M,y-15,W-M,y+1),relative=0)
    y=text(c,'Source spreadsheet: katzir.org.il (click)',M,y,size=10)
    c.save();assert page==3,page

if __name__=='__main__':
    partial='--reading-only' in sys.argv
    file=FILES/('reading-layout.pdf' if partial else 'Module-E-Museum-Bag.pdf')
    c=canvas.Canvas(str(file),pagesize=A4);c.setTitle('Module E - More Than an Old School Bag');c.setAuthor('Simon Halevi - English for Noar')
    reading(c,1 if partial else 4)
    if not partial:
        for page,qs in [(2,D['reading_questions'][:4]),(3,D['reading_questions'][4:])]:
            y=head(c,page,'QUESTIONS (70 points)',4)
            y=text(c,'Answer according to the article. Circle ONE answer in questions 1, 2, 4 and 9.',M,y,size=10.5)
            y=text(c,'For the other questions, follow the instructions.',M,y,size=10.5)-18
            for q in qs:y=question(c,q,y)
            assert y>42,('question overflow',page,y)
            c.showPage()
        vocab(c,4)
    c.save()
    if not partial:teacher()
    print(file)
    for l in LINES:print(f"{l['number']:02} {l['text']}")
