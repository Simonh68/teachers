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
    canvas.drawString(46,25,'UNIT 2  /  School Years Around the World  /  Teacher review edition')
    canvas.drawRightString(w-46,25,str(doc.page)); canvas.restoreState()

title('Reading / 01', 'One World, Different School Years')
p('Name: ____________________________   Class: __________','small')
for heading,en,_ in DATA['main']:
    if heading != DATA['main'][0][0]: p(escape(heading),'head')
    p(escape(en))
p('Find and explain','head')
p('1. Where does the school year begin in spring? __________________________<br/>'
  '2. Is Japan’s summer vacation at the end of its school year? Explain.')
lines(1)
p('Calendar scope: local examples, not one calendar for every school in a country. '
  'Florida’s summer example is 2026; other dated summer examples are 2027. '
  'Holiday lengths include weekends. See the linked School Calendars page for official sources.','small')
items.append(PageBreak())

title('True journeys / 02', 'One Sea. One Snowstorm.')
for idx in (0,3):
    s=DATA['stories'][idx];p(escape(s['title']),'head');p(escape(s['en']))
    publisher='KTUU / Alaska’s News Source, 10 November 2023' if idx==0 else 'BBC Teach, Life on the Isles of Scilly, 2024'
    p('Source: <link href="'+escape(s['source'],quote=True)+'" color="#176a78">'+escape(publisher)+'</link>','small')
p('Read closely','head')
p('1. What stops Kali from travelling to school? Give a detail from the text.');lines(2)
p('2. Why do Zoe and Isaac need a boat? How long does their boat journey take?');lines(2)
p('3. Do the island children always see dolphins? Which word tells you?');lines(1)
p('4. Compare the two school days. Write one difference and use evidence from both texts.');lines(3)
items.append(PageBreak())

title('Language practice / 03', 'Routines, Questions and Meaning')
p('A. Choose the form that fits.','head')
p('1. I (carry / carries) my bag to school.<br/>'
  '2. Samuel’s brothers (help / helps) him.<br/>'
  '3. The boat (stop / stops) near the island.<br/>'
  '4. Kali (do not / does not) go to school on this snow day.<br/>'
  '5. Carlito does not (walk / walks) the whole way.')
p('B. Ask and answer.','head')
p('1. Write a question with How: Carlito goes to school by horse.');lines(1)
p('2. Write a question with When: The bike bus travels on Fridays.');lines(1)
p('3. Ask a partner about the journey to school. Write your question and the answer.');lines(2)
p('C. Find the meaning in context.','head')
p('Circle the meaning that fits each sentence.')
p('1. The nearby station is open.<br/>A. close to this place &nbsp;&nbsp; B. far away<br/><br/>'
  '2. The kitchen is on fire.<br/>A. cooking food on a grill &nbsp;&nbsp; B. burning<br/><br/>'
  '3. We offer our thanks to the teacher.<br/>A. our expressions of gratitude &nbsp;&nbsp; B. a reason something happens<br/><br/>'
  '4. He bought a new ski.<br/>A. the action of skiing &nbsp;&nbsp; B. one long piece of equipment')
p('D. Use it.','head')
p('Choose nearby or on fire. Write a new sentence that makes its meaning clear.');lines(2)
items.append(PageBreak())

title('Listening and writing / 04', 'My School Routine')
p('Listen first','head')
p('Play “A Snow Day, a Screen and a Shovel” from the unit’s Listen First page. '
  'Keep the reading page closed. Listen once for the main idea and again for details.')
p('Who? _______________________  Where? ______________________________<br/>'
  'What changes that day?');lines(1)
p('Where is the teacher during the online lesson? _________________________<br/>'
  'Why does Kali clear the snow? _______________________________________')
p('Plan your writing','head')
p('Write 50–70 words about your school routine. Include how you travel, '
  'one negative sentence, one frequency word and two vocabulary entries from groups 03–05. '
  'Connect ideas with and, but or because.')
p('My two vocabulary entries: ___________________ / ___________________<br/>'
  'An idea I want my reader to understand:');lines(1)
p('My paragraph','head');lines(8)
p('Check and revise','head')
p('Check your meaning first. Then check Present Simple, your negative sentence and spelling. '
  'Underline your two vocabulary entries. Improve one sentence after feedback.');lines(2)
p('Teacher: assess the message, supporting details and independent use of language. '
  'Completing a page alone does not establish vocabulary mastery.','small')

(OUT/'files').mkdir(exist_ok=True)
dest=OUT/'files/unit2-workbook.pdf'
SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=47,bottomMargin=43,
                  title='Unit 2 — School Years Around the World',author='English for Noar').build(items,onFirstPage=page,onLaterPages=page)

key='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Workbook key | Unit 2</title><link rel="stylesheet" href="unit.css"></head><body><main dir="ltr"><a href="teacher.html">Teacher guide</a><h1>Workbook answer key</h1>
<h2>Page 1</h2><p>1. Japan. 2. No. The year begins in April and ends in March; summer vacation is in the middle.</p>
<h2>Page 2</h2><p>1. The snowstorm makes the roads dangerous. 2. Their school is on another island; five minutes. 3. No: “Sometimes”. 4. Accept supported comparisons: Kali learns at home online while Zoe and Isaac cross the sea and then walk to school.</p>
<h2>Page 3</h2><p>A: carry; help; stops; does not; walk.</p><p>B: How does Carlito go to school? When does the bike bus travel? Accept grammatically clear questions and relevant partner answers.</p><p>C: A, B, A, B. D: Accept a new sentence with the correct meaning. Do not accept the cooking sense for “on fire”.</p>
<h2>Page 4</h2><p>Kali; Anchorage, Alaska; a snowstorm prevents travel to school. The teacher is on his couch. Kali wants to earn money.</p><p>Writing: look for a clear school routine, supporting details, transport, a negative, a frequency word and two record-appropriate target meanings. Assess the message before form. Allow revision. Correct choices and task completion alone do not demonstrate mastery.</p></main></body></html>'''
(OUT/'workbook-key.html').write_text(key)
print(dest)
