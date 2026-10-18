#!/usr/bin/env python3
"""Build line-locked Module C practice and its teacher key from one JSON source."""
from pathlib import Path
import json, sys, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'grade12/four-units/module-c-school-radio'
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
    c.setFont('Helvetica-Bold',8);c.drawString(M,H-35,'ENGLISH FOR NOAR  |  GRADE 12 / 4 UNITS  |  MODULE C PRACTICE')
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
    y=text(c,'Practice time: 90 minutes. Answer in English. An approved dictionary may be used.',M,y,size=10)-4
    y=text(c,'Read the article and answer questions 1-7. Line numbers refer to this page.',M,y,size=10.5)-9
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
    if q['type'] in ('mc','multi'):
        if q['type']=='multi':y=text(c,'PUT A CHECK BY THE TWO CORRECT ANSWERS.',M+16,y,size=10,font='Helvetica-Bold')-6
        for i,opt in enumerate(q['options']):
            y=text(c,f"{'___ ' if q['type']=='multi' else ''}{['i','ii','iii','iv','v','vi'][i]})  {opt}",M+16,y,width=W-2*M-16,size=12)-3
    else:
        y=text(c,q['instruction'],M+16,y,size=10,font='Helvetica-Bold')-7
        if q.get('prefix'):y=text(c,q['prefix'],M+16,y,width=W-2*M-16,size=12)-7
        for k in range(2 if q['number']==3 else q.get('answer_lines',2)):
            if q['number']==3:
                c.setFont('Times-Roman',11);c.drawString(M+16,y+3,f'({k+1})')
            c.setStrokeGray(.5);c.setLineWidth(.4);c.line(M+40 if q['number']==3 else M+16,y,W-M,y);y-=28 if q['number']==3 else 23
    c.setFillGray(0);c.setFont('Times-Roman',10);c.drawRightString(W-M,y+1,f"({q['points']} points)")
    return y-23


def writing(c):
    y=head(c,4,'PART II: WRITTEN PRODUCTION (30 points)',4)
    q=D['writing']
    y=text(c,q['instruction'],M,y,size=12,font='Times-Bold')-12
    y=text(c,'8. '+q['stem'],M,y,size=13,font='Times-Bold')-25
    y=text(c,'Plan your ideas here (optional rough draft):',M,y,size=10,font='Helvetica')-12
    for _ in range(4):
        c.setStrokeGray(.65);c.line(M,y,W-M,y);y-=25
    y-=24
    y=text(c,'Write your final version here:',M,y,size=12,font='Times-Bold')-15
    for _ in range(12):
        c.setStrokeGray(.45);c.setLineWidth(.4);c.line(M,y,W-M,y);y-=26
    assert y>40,('writing overflow',y)
    c.showPage()

def teacher():
    out=FILES/'Module-C-School-Radio-Teacher-Key.pdf'
    c=canvas.Canvas(str(out),pagesize=A4)
    c.setTitle('Module C - A Voice for Every Student - Teacher Key')
    for page,qs in [(1,D['reading_questions'][:4]),(2,D['reading_questions'][4:])]:
        y=head(c,page,'TEACHER KEY - Reading (70 points)',3)
        y=text(c,'Accept equivalent answers that preserve meaning. Unrecognized open responses',M,y,size=10)
        y=text(c,'remain pending in the app; they are not automatically marked wrong.',M,y,size=10)-16
        for q in qs:
            y=text(c,f"{q['number']}. {q['answer']} ({q['points']} points)",M,y,size=11.5,font='Times-Bold')-3
            y=text(c,'Evidence: '+q['evidence']+' ['+q['evidence_scope']+']',M,y,size=10.5)-3
            y=text(c,'Marking: '+q['rubric'],M,y,size=10)-3
            y=text(c,'Traps: '+', '.join(q['traps']),M,y,size=10)-3
            y=text(c,'Feedback: '+q['explanation_en'],M,y,size=10)-15
        if page==2:
            y-=12
            y=text(c,'Calibration and use',M,y,size=12,font='Times-Bold')-6
            y=text(c,'Original fictional article: 292 words, 24 sentences, four paragraphs, 24 printed lines. Concrete school vocabulary, mostly simple past and present; contrasts, relative clauses, a passive form and one past-perfect clause.',M,y,size=10.5)-8
            y=text(c,'Qualitatively calibrated against Module C papers; not a validated difficulty score. Seven reading questions total 70 points: 8 + 8 + 14 + 16 + 8 + 8 + 8. The 90-minute practice target follows Summer 2026 A. Duration can vary by sitting.',M,y,size=10.5)-8
            y=text(c,'Hover translations and recorded reading are learning supports in the website. They do not represent examination-room permissions. Trap categories are teaching labels used by this project.',M,y,size=10.5)
        assert y>40,('key overflow',page,y)
        c.showPage()
    y=head(c,3,'TEACHER KEY - Writing (30 points)',3)
    q=D['writing']
    y=text(c,'8. '+q['stem'],M,y,size=12,font='Times-Bold')-5
    y=text(c,q['instruction'],M,y,size=11)-15
    for item in q['rubric']:
        y=text(c,f"{item['name']} - {item['points']} points",M,y,size=11,font='Times-Bold')-2
        y=text(c,item['description'],M,y,size=10.5)-9
    y=text(c,'One possible response (80 words)',M,y,size=12,font='Times-Bold')-5
    y=text(c,q['model'],M,y,size=11)-14
    y=text(c,q['marking_note'],M,y,size=10)-15
    y=text(c,'Sources and provenance',M,y,size=12,font='Times-Bold')-5
    for i,source in enumerate(D['sources'],1):
        start=y
        y=text(c,str(i)+'. '+source['title']+' (click)',M,y,size=9.5)-3
        c.linkURL(source['url'],(M,y,W-M,start+12),relative=0)
        y=text(c,source['use'],M+10,y,width=W-2*M-10,size=9)-8
    assert y>40,('writing key overflow',y)
    c.showPage();c.save()

if __name__=='__main__':
    partial='--reading-only' in sys.argv
    file=FILES/('reading-layout.pdf' if partial else 'Module-C-School-Radio.pdf')
    c=canvas.Canvas(str(file),pagesize=A4)
    c.setTitle('Module C - A Voice for Every Student')
    c.setAuthor('Simon Halevi - English for Noar')
    reading(c,1 if partial else 4)
    if not partial:
        for page,qs in [(2,D['reading_questions'][:4]),(3,D['reading_questions'][4:])]:
            y=head(c,page,'QUESTIONS (70 points)',4)
            y=text(c,'Answer questions 1-7 according to the article. In questions 1 and 6, circle ONE answer.',M,y,size=10)
            y=text(c,'In question 4, mark TWO answers. Follow the instructions in the other questions.',M,y,size=10)-20
            for q in qs:y=question(c,q,y)
            assert y>42,('question overflow',page,y)
            c.showPage()
        writing(c)
    c.save()
    if not partial:teacher()
    print(file)
