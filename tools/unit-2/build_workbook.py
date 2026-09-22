"""Build the printable student workbook from the same texts as Read & Listen."""
from pathlib import Path
import json
from html import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'grade7/unit-2'
DATA = json.loads((OUT / 'content.json').read_text())
pdfmetrics.registerFont(TTFont('UnitNunito', str(ROOT / 'grade7/the-same-way/assets/Nunito.ttf')))
INK, ACCENT = HexColor('#182c40'), HexColor('#176a78')
STYLES = {
    'body': ParagraphStyle('body', fontName='UnitNunito', fontSize=11.5, leading=15.5, textColor=INK, spaceAfter=6),
    'title': ParagraphStyle('title', fontName='UnitNunito', fontSize=25, leading=29, textColor=INK, spaceAfter=12),
    'head': ParagraphStyle('head', fontName='UnitNunito', fontSize=13, leading=17, textColor=ACCENT, spaceBefore=9, spaceAfter=4),
    'small': ParagraphStyle('small', fontName='UnitNunito', fontSize=8.5, leading=11.5, textColor=HexColor('#4b6072'), spaceAfter=5),
}
items = []
def p(text, style='body'):
    items.append(Paragraph(text, STYLES[style]))
def lines(count=1):
    class Lines(Flowable):
        def __init__(self):
            super().__init__(); self.height=count*23; self.width=490
        def draw(self):
            self.canv.setStrokeColor(HexColor('#b4c2cb')); self.canv.setLineWidth(.45)
            for i in range(count): self.canv.line(0,i*23+3,490,i*23+3)
    items.append(Lines())
def title(kicker, name):
    p(kicker.upper(),'small'); p(name,'title')
def page(canvas, doc):
    w,h=A4; canvas.saveState(); canvas.setStrokeColor(ACCENT); canvas.setLineWidth(1)
    canvas.line(46,h-35,w-46,h-35)
    canvas.setFont('UnitNunito',8); canvas.setFillColor(INK)
    canvas.drawString(46,25,'UNIT 2  /  School Years Around the World  /  Student workbook')
    canvas.drawRightString(w-46,25,str(doc.page)); canvas.restoreState()

def message(identity):
    story=next(s for s in DATA['stories'] if s['id']==identity)
    p(escape(story['channel']).upper()+' / FROM: '+escape(story['sender'])+' / '+escape(story['region']),'small')
    if identity=='wheelchair':p('To: Our English class / Subject: My way to school','small')
    p(escape(story['title']),'head')
    box=Table([[Paragraph(escape(story['en']),STYLES['body'])]],colWidths=[490])
    box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor({'horse':'#eaf5ef','wheelchair':'#fbf5e8','boat':'#edf3fc'}[identity])),('BOX',(0,0),(-1,-1),.6,ACCENT),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
    items.append(box);items.append(Spacer(1,8))
    p('Classroom message based on a documented routine; not an original message or a direct quotation.','small')
    publisher='BBC Teach, Life on the Isles of Scilly, 2024' if identity=='boat' else 'On the Way to School, documentary, 2013'
    p('Source: <link href="'+escape(story['source'],quote=True)+'" color="#176a78">'+escape(publisher)+'</link>','small')

title('Main reading / 01', 'One World, Different School Years')
p('Name: ____________________________   Class: __________','small')
for heading,en,_ in DATA['main']:
    if heading != DATA['main'][0][0]: p(escape(heading),'head')
    p(escape(en))
p('Find and explain','head')
p('1. Where does school begin in spring? _________________________________<br/>'
  '2. Is Japan’s summer holiday at the end of the school year? Explain.')
lines(1)
p('General local patterns; dates vary. Holiday lengths include weekends. A school-year span includes shorter holidays. Seasons use the Northern Hemisphere calendar. Official sources are linked on the main reading page.','small')
items.append(PageBreak())

title('Part 1 / Message 1 / 02', 'A WhatsApp Message from Argentina')
message('horse')
p('Read closely','head')
p('1. Who rides with Carlito?');lines(1)
p('2. How far is his school?');lines(1)
p('3. What does he want to be?');lines(1)
p('Present Simple A · Routines','head')
p('Choose the form that fits.<br/>1. I (carry / carries) my bag.<br/>'
  '2. Carlito (ride / rides) a horse.<br/>'
  '3. He does not (walk / walks) the whole way.')
p('Write two facts about Carlito. Use he in both sentences.');lines(2)
p('Your turn','head')
p('Answer the question at the end of his message.');lines(2)
items.append(PageBreak())

title('Word practice / 03', 'Seasons, Routines and Meaning')
p('A. Find the meaning in context.','head')
p('Circle the meaning that fits each sentence.')
p('1. The nearby station is open.<br/>A. close to this place &nbsp;&nbsp; B. far away<br/><br/>'
  '2. The kitchen is on fire.<br/>A. cooking food on a grill &nbsp;&nbsp; B. burning<br/><br/>'
  '3. We offer our thanks to the teacher.<br/>A. our expressions of gratitude &nbsp;&nbsp; B. a reason something happens<br/><br/>'
  '4. He bought a new ski.<br/>A. the action of skiing &nbsp;&nbsp; B. one long piece of equipment')
p('B. Use it.','head')
p('Choose nearby or on fire. Write a new sentence that makes its meaning clear.');lines(2)
p('C. Compare school years.','head')
p('1. In which season does school usually start in Kent?');lines(1)
p('2. How long is the summer holiday in UAE public schools?');lines(1)
p('3. Write one difference between the school calendars in Anchorage and Miami-Dade.');lines(2)
p('4. Does the school-year span mean lessons every day? Give a detail from the main reading.');lines(2)
items.append(PageBreak())

title('Part 2 / Message 2 / 04', 'An Email from India')
message('wheelchair')
p('Read closely','head')
p('1. Who helps Samuel?');lines(1)
p('2. How do they help? Give a detail from the message.');lines(2)
p('Present Simple B · Questions','head')
p('1. Complete: Samuel’s brothers (help / helps) him.<br/>'
  '2. Complete: (Do / Does) Samuel use a wheelchair?<br/>'
  '3. Write a question with Who. The answer is: His two younger brothers.');lines(1)
p('4. Ask a partner how they get to school. Write the question and answer.');lines(2)
p('Your turn','head')
p('Answer Samuel’s question. Then write one similarity or difference between your journey and his.');lines(3)
items.append(PageBreak())

title('Part 3 / Message 3 / 05', 'An Instagram Post from the Isles of Scilly')
p('Listen first','head')
p('Open the unit’s Listen First page. Listen to the boat message before reading the box below. '
  'Listen once for the main idea, then again for details.')
p('Who? _______________________  Where? ______________________________<br/>'
  'Why do they need a boat? ___________________________________________<br/>'
  'How long is the boat trip? __________________________________________<br/>'
  'What do they do after the boat trip? __________________________________')
p('Now read and check','head')
message('boat')
p('Read closely','head')
p('Do Zoe and Isaac always see dolphins? Which word tells you?');lines(1)
p('Your turn','head')
p('Answer their question. Write one detail about your own journey.');lines(2)
p('Connect two messages','head')
p('Choose one of the earlier messages. Write one similarity and one difference. Use a detail from each message.');lines(3)
items.append(PageBreak())

title('Independent writing / 06', 'A Reply from You')
p('Plan your reply','head')
p('Choose Carlito, Samuel, or Zoe and Isaac. Write a WhatsApp reply, an email reply, or an Instagram comment of 50–70 words. '
  'Answer their question and describe your school routine. Include how you travel, '
  'one negative sentence, one frequency word and two vocabulary entries from groups 03–05. '
  'Connect ideas with and, but or because.')
p('My message is for: _________________________________________________<br/>'
  'My two vocabulary entries: ___________________ / ___________________<br/>'
  'One detail from their message I want to respond to:');lines(2)
p('My reply','head');lines(9)
p('Check and revise','head')
p('Does your reply answer the sender’s question? Check your meaning first. Then check '
  'Present Simple, your negative sentence and spelling. Underline your two vocabulary entries. '
  'Improve one sentence after feedback.');lines(2)
p('Teacher: assess the message, supporting details and independent use of language. '
  'Completing a page alone does not establish vocabulary mastery.','small')

(OUT/'files').mkdir(exist_ok=True)
dest=OUT/'files/unit2-workbook.pdf'
SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=47,bottomMargin=43,
                  title='Unit 2 — School Years Around the World',author='English for Noar').build(items,onFirstPage=page,onLaterPages=page)

key='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Workbook key | Unit 2</title><link rel="stylesheet" href="unit.css"></head><body><main dir="ltr"><a href="teacher.html">Teacher guide</a><h1>Workbook answer key</h1>
<h2>Page 1</h2><p>1. Japan. 2. No. The year begins in spring and ends the following spring; the summer holiday falls within it.</p>
<h2>Page 2</h2><p>1. His sister Micaela. 2. Eighteen kilometres. 3. A vet. Grammar: carry; rides; walk. Accept supported facts such as: He rides a horse. He wants to be a vet. The reply should explain the pupil’s own journey.</p>
<h2>Page 3</h2><p>A: A, B, A, B. B: Accept a new sentence with the correct meaning; “on fire” means burning. C: 1. Early autumn. 2. About eight weeks. 3. Anchorage ends in late spring; Miami-Dade ends in early summer. Alternatively, about eleven versus ten weeks of summer holiday. 4. No. The year includes shorter holidays.</p>
<h2>Page 4</h2><p>His two younger brothers help him. They push and pull his chair for four kilometres. Grammar: help; Does; Who helps Samuel? Accept clear questions and relevant partner answers. The reply should identify who accompanies the pupil and support the comparison with a detail from Samuel’s message.</p>
<h2>Page 5</h2><p>Zoe and Isaac; Bryher and Tresco, Isles of Scilly. Their school is on another island. Five minutes. They walk to school after the boat trip. They do not always see dolphins: “Sometimes”. Accept supported comparisons using both selected messages.</p>
<h2>Page 6</h2><p>Assess a relevant reply of 50–70 words: an answer to the sender’s question, a clear school routine, supporting details, transport, a negative, a frequency word and two target vocabulary meanings. Assess the message before form. Allow revision. Correct choices and task completion alone do not demonstrate mastery.</p></main></body></html>'''
(OUT/'workbook-key.html').write_text(key)
print(dest)
