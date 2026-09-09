"""Rebuild the two September reading lessons and their print handouts.

Run from any directory: python3 tools/build_lessons_20260910.py
Requires reportlab. Artwork is maintained separately in each lesson's assets.
Vocabulary examples are copied exactly from the existing Grade 8 opening deck.
"""
from pathlib import Path
import html
import json
import re
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
G8 = ROOT / 'grade8/a-place-on-the-team'
G10 = ROOT / 'grade10/group-a/the-road-not-taken-review'
for folder in (G8, G10):
    (folder / 'files').mkdir(parents=True, exist_ok=True)
    (folder / 'assets').mkdir(exist_ok=True)

STORY = [
    'At the morning break, Amir stood beside the football pitch, turning a small stone under his shoe. He wanted to join the game with his classmates.',
    '“Amir, you’re with us,” Noam called. Amir ran onto the pitch. However, the boys kept passing the ball around him. Twice he raised his hand. Twice the ball went somewhere else.',
    'Noam stopped beside him. “Why are you standing here?”',
    '“No one passes to me,” Amir said. “I can’t get better by watching.”',
    'Noam now had a better understanding of the problem. But his team was one goal behind. He took the game seriously and wanted to win.',
    'On the next attack, Noam passed to Amir. Amir kicked too quickly and sent the ball to the other team by mistake.',
    '“Why did you pass to him?” Dan shouted.',
    'Amir looked down. “It’s fine. I’ll go back to class.”',
    '“Stay,” Noam said. “Try a short pass. I’ll stand near you. We all make mistakes.”',
    'He gave Amir a quick explanation and showed him where to stand. When the ball came again, Amir moved with more care. He passed it a short distance to Noam.',
    'They did not score. Later, Amir missed another pass. This time, Dan called, “Try again!”',
    'The bell rang. Their team lost by one goal, but Amir walked back with the others.',
    '“You’ll be able to practice with us tomorrow,” Noam said.',
    'The next morning, Amir left the small stone beside the pitch and ran toward his classmates. “Which team am I on?”',
]
POEM = [
    'Two roads diverged in a yellow wood,',
    'And sorry I could not travel both',
    'And be one traveler, long I stood',
    'And looked down one as far as I could',
    'To where it bent in the undergrowth;',
    'Then took the other, as just as fair,',
    'And having perhaps the better claim,',
    'Because it was grassy and wanted wear;',
    'Though as for that the passing there',
    'Had worn them really about the same,',
    'And both that morning equally lay',
    'In leaves no step had trodden black.',
    'Oh, I kept the first for another day!',
    'Yet knowing how way leads on to way,',
    'I doubted if I should ever come back.',
    'I shall be telling this with a sigh',
    'Somewhere ages and ages hence:',
    'Two roads diverged in a wood, and I—',
    'I took the one less traveled by,',
    'And that has made all the difference.',
]
BIO = 'Robert Frost (1874–1963) was an American poet. Many of his poems use New England landscapes and everyday speech to explore difficult human experiences. He lived in England from 1912 to 1915, where he became friends with the poet Edward Thomas.'
BRIDGE = 'Robert Frost and Edward Thomas often walked together in England. Thomas sometimes regretted the route they had chosen and imagined that another route would have been better. Frost partly drew on this habit when writing the poem, teasing his friend gently.'
SOURCES = [
    ('Poem: Academy of American Poets', 'https://poets.org/poem/road-not-taken'),
    ('Biography: Academy of American Poets', 'https://poets.org/poet/robert-frost'),
    ('Background: David Orr, Academy of American Poets', 'https://poets.org/text/road-not-taken-poem-everyone-loves-and-everyone-gets-wrong'),
]
IDIOM_SOURCE = 'https://dictionaryblog.cambridge.org/2021/06/02/at-sixes-and-sevens-phrases-with-numbers/'

QUESTIONS8 = [
    ('When and where does the story begin?', 'It begins at the morning break, beside the school football pitch.'),
    ('Give one detail that shows Amir is on the team but is not really included.', 'The boys keep passing the ball around Amir. He raises his hand twice, but the ball goes somewhere else.'),
    ('Why is it difficult for Noam to decide to pass to Amir?', 'His team is one goal behind. He takes the game seriously and wants to win.'),
    ('What happens when Noam first passes the ball to Amir?', 'Amir kicks too quickly and sends the ball to the other team by mistake.'),
    ('Name two things Noam does to help Amir stay in the game.', 'He asks Amir to stay, suggests a short pass, stands near him, and explains where to stand. Any two are acceptable.'),
    ('How does Dan’s reaction to Amir’s mistakes change?', 'At first, Dan shouts at Noam for passing to Amir. Later, when Amir misses another pass, Dan encourages him: “Try again!”'),
    ('What does Amir’s question at the end suggest about how he feels? Use a story detail.', 'He seems more confident that he belongs. He runs toward his classmates and asks which team he is on, rather than waiting beside the pitch.'),
    ('Write 3–4 sentences: How can classmates include a player who is still learning? Use one story detail and three focus words.', 'Example: A classmate can join our game even if he is still learning. He may pass to the wrong team by mistake. We can give a short explanation and try again, as Noam does. Passing to him again helps him take part.'),
]
QUESTIONS10 = [
    ('Where is the speaker at the beginning, and what choice must he make?', 'He is in a yellow wood where two roads separate. He must choose one road because he cannot travel both at once.'),
    ('What prevents the speaker from seeing the whole first road?', 'The road bends into the undergrowth, so he cannot see beyond the bend (lines 4–5).'),
    ('Copy words that show the two roads are similar.', '“Had worn them really about the same” (line 10), or “both that morning equally lay” (line 11).'),
    ('Why does the speaker doubt that he will return?', 'He knows that “way leads on to way” (line 14): one journey or choice leads to others, making a return uncertain.'),
    ('What might the two roads represent? Explain the metaphor.', 'They can represent different choices in life. The traveler must choose without knowing the full result, just as people do when making important decisions.'),
    ('What might the “sigh” suggest? Support your interpretation with another detail.', 'It may suggest regret: he was “sorry” he could not travel both roads. It may also suggest reflection or satisfaction, linked to “all the difference.” The poem does not settle its meaning.'),
    ('Connect the background about Edward Thomas to one specific detail in the poem. Explain how the connection helps you understand it.', 'Thomas’s habit of imagining a better route helps explain the speaker’s focus on the road he did not take. The wish to keep it “for another day” suggests that choosing does not end his thoughts about the other possibility.'),
    ('Is the speaker satisfied with his choice? Write 60–80 words. Support your view with two details from the poem.', 'The speaker may feel satisfied, but the poem leaves room for doubt. He imagines saying that his choice made “all the difference,” which could sound positive. However, he also says that he was “sorry” he could not travel both roads. His future “sigh” may express regret or simply reflection. These details suggest mixed feelings rather than a clearly happy or unhappy ending.'),
]

raw_vocab = (ROOT / 'grade8/opening/index.html').read_text()
VOCAB_ALL = [dict(zip(('word', 'meaning', 'example', 'translation'), m)) for m in re.findall(r'\{w:"([^"]*)",m:"([^"]*)",e:"([^"]*)",h:"([^"]*)"\}', raw_vocab)]
WORDS = ['break', 'join', 'however', 'around', 'understanding', 'take something seriously', 'by mistake', 'fine', 'go back', 'explanation', 'care', 'be able to do something']
VOCAB = [next(w for w in VOCAB_ALL if w['word'] == word) for word in WORDS]
assert len(VOCAB_ALL) == 55
PATTERNS = [r'break', r'join', r'however', r'around', r'understanding', r'took the game seriously', r'by mistake', r'fine', r'go back', r'explanation', r'care', r'be able to']
FOCUS = re.compile(r'\b(?:' + '|'.join(PATTERNS) + r')\b', re.I)

def esc(text):
    return html.escape(str(text), quote=True)

def marked(text, tag='mark'):
    pieces, pos = [], 0
    for m in FOCUS.finditer(text):
        pieces += [esc(text[pos:m.start()]), '<' + tag + '>' + esc(m.group()) + '</' + tag + '>']
        pos = m.end()
    return ''.join(pieces) + esc(text[pos:])

class Deck:
    def __init__(self, folder, title, grade, home, shared, nav):
        self.folder, self.title, self.grade = folder, title, grade
        self.home, self.shared, self.nav = home, shared, nav
        self.slides = []
        self.pairs = 0

    def add(self, kind, section, body, **attrs):
        self.slides.append(dict(kind=kind, section=section, body=body, **attrs))

    def meta(self, text, tense=''):
        return f'<div class="slide-meta"><p class="eyebrow">{esc(text)}</p><p class="tense" lang="he" dir="rtl">{esc(tense)}</p></div>'

    def transition(self, section, english, hebrew, instruction):
        self.add('transition', section, self.meta(self.grade) + f'<h1 class="part-title en">{esc(english)}</h1><h2 class="part-he">{esc(hebrew)}</h2><p class="instruction">{instruction}</p>')

    def info(self, section, label, text, tense=''):
        self.add('reading', section, self.meta(label, tense) + f'<p class="story-sentence en">{text}</p>')

    def qa(self, section, question, answer, label='Think & answer', answer_label='תשובה אפשרית'):
        self.pairs += 1
        head = self.meta(label) + f'<div class="question-area"><h2 class="question en">{esc(question)}</h2></div>'
        for reveal in (False, True):
            body = head + ('<div class="answer-slot"><p class="answer-label">' + esc(answer_label) + '</p><p class="possible-answer en">' + esc(answer) + '</p></div>' if reveal else '<div class="answer-slot" aria-hidden="true"></div>')
            self.add('qa' + (' reveal' if reveal else ''), section, body, pair=f'q{self.pairs}', reveal=str(reveal).lower())

    def picture(self, section, filename, alt):
        if filename == 'cats-roads':
            ident = 'cat-' + str(len(self.slides))
            # One source image, one contour and two identical uses. No mirroring.
            contour = 'M355 36 C380 52 407 97 437 123 L488 138 L548 145 C580 119 606 85 648 72 C672 98 671 166 656 221 C668 258 681 306 683 331 C721 354 748 397 769 438 C835 445 883 476 916 522 C958 579 972 658 992 740 C1010 814 1038 891 1030 954 C1028 1011 1003 1058 994 1100 C982 1145 951 1170 901 1179 C859 1217 799 1239 728 1252 C591 1275 431 1255 338 1226 C253 1207 202 1174 195 1123 C183 1090 202 1050 235 1034 C280 1010 316 1052 336 1094 L351 1102 C338 1077 350 1051 388 1047 C375 1003 362 947 367 905 C370 856 387 824 407 791 C378 749 363 709 346 667 C326 624 328 582 340 542 L354 478 L367 422 C328 400 313 371 308 343 C295 312 305 267 318 239 L343 194 C348 142 344 72 355 36 Z'
            svg = f'<svg class="break-image forest-composition" viewBox="0 0 1671 941" role="img" aria-label="{esc(alt)}"><defs><clipPath id="{ident}-clip"><path d="{contour}"/></clipPath><g id="{ident}"><image href="assets/identical-cat.webp" width="1145" height="1374" clip-path="url(#{ident}-clip)"/></g></defs><image href="assets/forest-empty-cats.webp" width="1671" height="941"/><use href="#{ident}" transform="translate(191 319) scale(.13)"/><use href="#{ident}" transform="translate(1295 319) scale(.13)"/></svg>'
            self.add('break', section, svg + '<span class="sr-only">הפסקת תוכן</span>')
        else:
            self.add('break', section, f'<img class="break-image" src="assets/{filename}.webp" alt="{esc(alt)}"><span class="sr-only">הפסקת תוכן</span>')

    def idiom(self, section):
        head = self.meta('Visual riddle') + '<div class="question-area"><h2 class="question en">Which English idiom is hidden in this scene?</h2></div>'
        video = '<video class="riddle-video" muted playsinline preload="none" poster="' + self.shared + 'cats-seven-six.webp" aria-label="Silent visual riddle: seven cats in the top row, six in the bottom row"><source src="' + self.shared + 'cats-seven-six.mp4" type="video/mp4"></video><button class="clip-play" data-play-clip aria-label="הפעלת הסרטון השקט" title="הפעלת הסרטון השקט">▶</button>'
        self.add('riddle', section, head + '<div class="media-stage">' + video + '<div class="answer-slot idiom-answer" aria-hidden="true"></div></div>',pair='idiom',reveal='false')
        self.add('riddle reveal', section, head + '<div class="media-stage"><img class="riddle-still" src="' + self.shared + 'cats-seven-six.webp" alt="Seven cats in one row and six in another"><div class="answer-slot idiom-answer"><h3 class="en">At sixes and sevens</h3><p class="en">Confused or disorganized. · <span lang="he" dir="rtl">מבולבלים או בחוסר סדר</span></p></div></div>',pair='idiom',reveal='true')
        self.info(section, 'Idiom in context', '“We were at sixes and sevens before the game. Nobody knew which team to join.”', 'עבר')

    def write(self):
        sections = []
        for i, slide in enumerate(self.slides, 1):
            attrs = ' '.join(f'data-{k}="{esc(v)}"' for k,v in slide.items() if k not in ('kind','body'))
            sections.append(f'<section id="slide-{i}" class="slide {slide["kind"]}{" active" if i == 1 else ""}" {attrs} role="group" aria-roledescription="שקף" aria-label="{i} מתוך {len(self.slides)}"{ "" if i == 1 else " hidden"}><div class="frame">{slide["body"]}</div></section>')
        nav = ''.join(f'<button data-jump="{k}">{v}</button>' for k,v in self.nav)
        page = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07111f"><title>{esc(self.title)} · {self.grade} · Teacher</title><link rel="stylesheet" href="{self.shared}deck.css?v=20260910f"></head>
<body><a class="home" href="{self.home}" aria-label="חזרה לחומרי הכיתה" title="חזרה לחומרי הכיתה"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m3 11 9-8 9 8M5 10v10h5v-6h4v6h5V10"/></svg></a><nav class="section-nav" aria-label="חלקי המצגת">{nav}</nav>
<main class="stage" aria-label="{esc(self.title)}">{''.join(sections)}</main>
<nav class="nav" aria-label="ניווט שקפים"><div class="nav-group"><button data-step="-1" aria-label="השקף הקודם — למעלה">↑</button><button data-step="-1" aria-label="השקף הקודם — שמאלה">←</button><button data-step="1" aria-label="השקף הבא — ימינה">→</button><button data-step="1" aria-label="השקף הבא — למטה">↓</button></div><output id="counter" class="progress" aria-live="polite" aria-atomic="true"></output></nav><div class="progress-track" aria-hidden="true"><div class="progress-fill"></div></div><script src="{self.shared}deck.js?v=20260910f"></script></body></html>'''
        (self.folder / 'index.html').write_text(page)
        print(f'{self.title}: {len(self.slides)} slides; {self.pairs} discussion pairs')

def grade8():
    d = Deck(G8, 'A Place on the Team', 'כיתה ח׳', '../', '../../assets/lesson-decks/', [('words','מילים'),('story','קריאה'),('questions','שאלות'),('finish','סיום')])
    d.add('cover', 'words', d.meta('כיתה ח׳ · קריאה') + '<h1 class="cover-title en">A Place on<br>the Team</h1><p class="cover-sub">מקום בקבוצה</p><p class="level en">Band II · Core I · Group 01</p>')
    d.transition('words','Before reading','חזרה על מילים מקבוצה 01','12 מילים וביטויים לקראת הסיפור. המילה ומשפט הדוגמה תחילה; המשמעות בשקף הבא.')
    for i,w in enumerate(VOCAB,1):
        tense = {'however':'עבר','around':'הווה','understanding':'הווה','by mistake':'עבר','fine':'הווה','explanation':'הווה','care':'הווה','be able to do something':'הווה'}.get(w['word'],'')
        head = d.meta(f'Band II · Core I · Group 01 · {i}/12',tense) + f'<h2 class="word en">{esc(w["word"])}</h2><p class="example en">{esc(w["example"])}</p>'
        for reveal in (False,True):
            body = head + ('<div class="translation-slot"><p class="meaning">' + esc(w['meaning']) + '</p><p class="translation">' + esc(w['translation']) + '</p></div>' if reveal else '<div class="translation-slot" aria-hidden="true"></div>')
            d.add('vocab' + (' reveal' if reveal else ''),'words',body,pair=f'w{i}',reveal=str(reveal).lower(),word=w['word'])
        if i in (5,10):
            d.picture('words', 'tortoise-football' if i==5 else 'penguin-referee', 'A tortoise in enormous football boots joins a game.' if i==5 else 'A penguin referee measures a football with a banana.')
    d.transition('story','Read the story','קריאה','קראו ועקבו אחר השינוי: מה גורם לאמיר להרגיש שהוא חלק מהקבוצה?')
    for i,p in enumerate(STORY,1):
        d.info('story',f'Reading · paragraph {i}/{len(STORY)}',marked(p), 'עבר' if '“' not in p else '')
        if i == 8:
            d.picture('story','tortoise-football','A tortoise in enormous football boots joins a game.')
    d.info('story','Your turn','Read the worksheet. Answer questions 1–7. Use details from the story.')
    d.transition('questions','Reading comprehension','שאלות הבנה','תשובות שונות מתקבלות כשהן מתאימות לפרטים שבסיפור.')
    for i,(q,a) in enumerate(QUESTIONS8[:7],1):
        d.qa('questions',q,a,label=f'Worksheet · Question {i}')
        if i == 5:
            d.picture('questions','penguin-referee','A penguin referee measures a football with a banana.')
    d.idiom('questions')
    d.qa('questions','Complete: Amir sent the ball to the other team ________.','by mistake',label='Group 01 · use the word',answer_label='תשובה')
    d.qa('questions','Complete: Noam gave Amir a short ________ of where to stand.','explanation',label='Group 01 · use the word',answer_label='תשובה')
    d.transition('finish','Write & reflect','כתיבה וסיכום','ענו על שאלה 8 בדף העבודה. השתמשו בפרט מהסיפור ובשלוש מילים מהחזרה.')
    d.qa('finish',QUESTIONS8[7][0],QUESTIONS8[7][1],label='Worksheet · Question 8')
    d.info('finish','Exit ticket','Name one action that helps a classmate take part—even after a mistake.')
    d.add('transition resources','finish',d.meta('כיתה ח׳') + '<h2 class="part-title en">Lesson materials</h2><div class="resource-links"><a href="files/a-place-on-the-team-worksheet.pdf" target="_blank" rel="noopener">דף עבודה לתלמידים · PDF</a><a href="files/a-place-on-the-team-answer-key.pdf" target="_blank" rel="noopener">מפתח תשובות ותסריט למורה · PDF</a><a href="https://englishfornoar.co.il/band-ii/groups/group-01.html" target="_blank" rel="noopener">תרגול כל קבוצה 01</a></div><p class="navigation-help">ניווט: ארבעת החצים, גלגלת העכבר או החלקה. לחזרה לחומרי הכיתה: סמל הבית.</p>')
    d.write()
    return d

def grade10():
    d = Deck(G10,'The Road Not Taken · Review','כיתה י׳ · 5 יח״ל','../library/','../../../assets/lesson-decks/', [('review','חזרה'),('questions','שאלות'),('extend','העמקה'),('finish','סיום')])
    d.add('cover','review',d.meta('כיתה י׳ · 5 יח״ל · ספרות') + '<h1 class="cover-title en">The Road<br>Not Taken</h1><p class="cover-sub en">Robert Frost</p><p class="level en">Review · choices · reading between the lines</p>')
    d.transition('review','Back to the poem','חזרה קצרה','היזכרו במצב הפותח את השיר, ואז חזרו אל המילים המדויקות.')
    d.qa('review','What is the traveler’s problem at the beginning?','Two roads separate. He wants to explore both, but he must choose one.',label='Recall')
    d.info('review','Meet the poet','Robert Frost<br><span class="subline">1874–1963 · American poet</span>')
    d.info('review','Robert Frost',esc('Many of his poems use New England landscapes and everyday speech to explore difficult human experiences.'))
    d.info('review','Robert Frost',esc('Frost lived in England from 1912 to 1915. There, he became friends with the poet Edward Thomas.'),'עבר')
    d.qa('review','Which region often appears in Frost’s poetry?','New England, in the northeastern United States.',label='Background check',answer_label='תשובה')
    d.qa('review','Which poet became Frost’s friend in England?','Edward Thomas.',label='Background check',answer_label='תשובה')
    d.picture('review','cats-roads','A traveler faces two narrow woodland roads, each with the same ginger cat waiting ahead.')
    d.info('review','Read again','Read the whole poem on your worksheet. Listen for what the speaker knows—and what he can only imagine.')
    for n in range(4):
        lines = ''.join(f'<span><small>{i+1}</small>{esc(POEM[i])}</span>' for i in range(n*5,n*5+5))
        d.add('poem','review',d.meta(f'Stanza {n+1} / 4') + '<div class="poem-lines en">' + lines + '</div>')
    d.info('review','Your turn','Answer worksheet questions 1–6. For questions 3, 5 and 6, underline words that support your answer.')
    d.transition('questions','Read closely','שאלות על השיר','קודם עונים, ואז משווים לתשובה אפשרית. בפרשנות יש לבסס את התשובה על השיר.')
    for i,(q,a) in enumerate(QUESTIONS10[:6],1):
        d.qa('questions',q,a,label=f'Worksheet · Question {i}')
        if i == 5:
            d.picture('questions','fox-map-snail','A fox studies an enormous map while a tiny snail confidently leads the way.')
    d.idiom('questions')
    d.qa('questions','Do the roads look clearly different when the speaker chooses?','No. Although one seems to have a “better claim,” he then says they are worn “about the same” and lie equally in leaves.',label='A useful tension')
    d.qa('questions','What changes between the choice itself and the story he imagines telling later?','At the choice, the roads look similar. In his imagined future story, he says he chose the road “less traveled by.” He may be reshaping how he remembers the choice.',label='Think further')
    d.transition('extend','If time allows','מושגים, חשיבה גבוהה ו־Bridging','אפשר לעבור ישירות לסיכום. ההעמקה מתאימה גם לפתיחת השיעור הבא.')
    for term,meaning in [
        ('Poem / poet','A poem is the literary text. A poet is the person who writes it. Frost is the poet of this poem.'),
        ('Speaker','The voice speaking inside a poem. The speaker is not automatically the poet.'),
        ('Line / stanza','A line is one row of a poem. A stanza is a group of lines. This poem has 20 lines in four stanzas.'),
        ('Metaphor','A comparison in which one thing stands for another. The roads can stand for choices in life.'),
        ('Theme','A central idea explored in a text. Here: making choices without certainty, and the stories we later tell about those choices.'),
    ]:
        d.qa('extend',f'What does “{term}” mean?',meaning,label='Literary tools',answer_label='מושג')
    d.picture('extend','cats-roads','A traveler faces two narrow woodland roads, each with the same ginger cat waiting ahead.')
    d.info('extend','LOTS · basic understanding','Find, identify or recall information stated in the text. Example: Where is the speaker standing?')
    d.info('extend','HOTS · higher-order thinking','Infer, compare, explain or evaluate. Connect details and show your reasoning. Example: How does the speaker’s future story differ from the original choice?')
    d.qa('extend','“Copy words that show the roads are similar.” Basic understanding or higher-order thinking?','Basic understanding: locate explicit information. A question about what that similarity means would require further reasoning.',label='Classify the thinking')
    d.qa('extend','“What might the sigh suggest?” Basic understanding or higher-order thinking?','Higher-order thinking: infer a possible meaning and support it. The thinking required matters more than the question word.',label='Classify the thinking')
    d.info('extend','Bridging text and context',esc(BRIDGE))
    d.info('extend','Build a bridge','Connect one background fact to one detail in the poem. Then explain what that connection helps you understand.')
    d.qa('extend',QUESTIONS10[6][0],QUESTIONS10[6][1],label='Optional worksheet · Question 7')
    d.picture('extend','fox-map-snail','A fox studies an enormous map while a tiny snail confidently leads the way.')
    d.qa('extend','Improve this answer: “Frost knew Thomas. The poem has roads.”','Thomas sometimes regretted a chosen walking route. This helps explain why the speaker keeps imagining the road he did not take. The wish to save it “for another day” shows continuing interest in the rejected choice.',label='Make the connection clear')
    d.info('extend','Optional writing · Question 8',esc(QUESTIONS10[7][0]))
    d.transition('finish','Before you leave','סיכום','השלימו את המשפט בעזרת פרט אחד מן השיר.')
    d.info('finish','Exit ticket','“At first I thought the poem was about ________. Now, because of the words ________, I also think ________.”')
    links = '<a href="files/the-road-not-taken-worksheet.pdf" target="_blank" rel="noopener">דף עבודה לתלמידים · PDF</a><a href="files/the-road-not-taken-answer-key.pdf" target="_blank" rel="noopener">מפתח תשובות ותסריט למורה · PDF</a>'
    d.add('transition resources','finish',d.meta('כיתה י׳ · 5 יח״ל') + '<h2 class="part-title en">Lesson materials</h2><div class="resource-links">' + links + '</div><p class="navigation-help">ניווט: ארבעת החצים, גלגלת העכבר או החלקה. לחזרה לחומרי הכיתה: סמל הבית.</p>')
    source_links = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{esc(t)}</a>' for t,u in SOURCES)
    d.add('transition resources','finish',d.meta('References') + '<h2 class="part-title en">Sources</h2><div class="resource-links en">' + source_links + f'<a href="{IDIOM_SOURCE}" target="_blank" rel="noopener">Idiom: Cambridge Dictionary</a></div>')
    d.write()
    return d

# Print materials: plain white pages, embedded fonts, generous writing space.
FONTDIR = Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTDIR/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
INK = colors.HexColor('#15263a')
ACCENT = colors.HexColor('#23687c')
LIGHT = colors.HexColor('#c7d3d9')
W,H = A4
M = 43

class PDF:
    def __init__(self,path,title):
        self.c = canvas.Canvas(str(path),pagesize=A4)
        self.c.setTitle(title)
        self.c.setAuthor('Teacher · Simon')
        self.page = 0
        self.title = title
        self.y = H-M

    def start(self,label,title,sub=''):
        if self.page:
            self.finish_page()
            self.c.showPage()
        self.page += 1
        self.y = H-M
        self.c.setFillColor(ACCENT)
        self.c.setFont('Bold',9)
        self.c.drawString(M,self.y,label.upper())
        self.y -= 28
        self.p(title,size=22,font='Bold',leading=27,after=8)
        if sub:
            self.p(sub,size=10,leading=14,after=11)
        self.c.setStrokeColor(LIGHT)
        self.c.line(M,self.y,W-M,self.y)
        self.y -= 18

    def p(self,text,size=11.1,font='Body',leading=None,after=7,color=INK):
        style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.4,textColor=color,spaceAfter=0)
        p=Paragraph(text,style)
        _,height=p.wrap(W-2*M,1000)
        assert self.y-height >= 45, (self.title,self.page,'page overflow',self.y,height,text[:60])
        p.drawOn(self.c,M,self.y-height)
        self.y-=height+after

    def lines(self,n=2,gap=18):
        self.c.setStrokeColor(LIGHT)
        self.c.setLineWidth(.55)
        for _ in range(n):
            self.y-=gap
            assert self.y>=48,(self.title,self.page,'writing lines overflow')
            self.c.line(M,self.y,W-M,self.y)
        self.y-=9

    def finish_page(self):
        self.c.setFillColor(ACCENT)
        self.c.setFont('Body',8)
        self.c.drawString(M,25,'TEACHER · '+self.title)
        self.c.drawRightString(W-M,25,str(self.page))

    def save(self):
        self.finish_page()
        self.c.save()

def pdf8():
    p=PDF(G8/'files/a-place-on-the-team-worksheet.pdf','A Place on the Team')
    p.start('Grade 8 · Reading','A Place on the Team','Name: __________________________    Class: ________    Date: __________')
    for i,text in enumerate(STORY,1):
        p.p(f'<b>{i:02d}</b>  '+marked(text,'b'),size=10.4,leading=14.6,after=5.8)
    p.p('<b>Word help:</b> pitch = an area for playing a sport · goal = a point in football · short pass = sending the ball to a player near you',size=9.2,leading=13,after=0)
    p.start('Grade 8 · Worksheet','Read, think, write','Answer in English. Use details from the story. Focus words are bold in the text.')
    for i,(q,_) in enumerate(QUESTIONS8,1):
        p.p(f'<b>{i}.</b> '+esc(q),size=10.6,leading=14.2,after=0)
        p.lines(4 if i==8 else 2,gap=16)
    p.save()
    p=PDF(G8/'files/a-place-on-the-team-answer-key.pdf','A Place on the Team · Teacher key')
    p.start('Teacher copy · Grade 8','Answer key & lesson script','A2 reading · 12 focus items from Band II, Core I, Group 01')
    p.p('<b>80-minute lesson:</b> opening 5; vocabulary 12; shared reading 12; worksheet 18; discussion 15; picture breaks and idiom 5; writing 10; exit ticket 3.',size=10.2)
    p.p('<b>Teaching focus:</b> Amir gets repeated chances to participate. He still makes mistakes, and the team loses. Discuss belonging and practical support without making inclusion depend on sporting success.',size=10.2)
    for i,(q,a) in enumerate(QUESTIONS8,1):
        p.p(f'<b>{i}.</b> '+esc(a),size=10.4,leading=14.5,after=8)
    p.p('<b>Accept alternatives:</b> assess text evidence and clear meaning. For question 8, check the practical action, one relevant story detail, and three focus words. Do not require the sample wording.',size=10.2)
    p.p('<b>Visual riddle:</b> At sixes and sevens = confused or disorganized. The cat numbers are a visual wordplay clue, not an explanation of the idiom’s historical origin.',size=10.2)
    p.p(f'<b>Sources:</b> original classroom story; exact vocabulary examples from the existing Grade 8 opening deck. <link href="{IDIOM_SOURCE}" color="#23687c">Idiom meaning: Cambridge Dictionary.</link>',size=9,leading=12)
    p.save()

def pdf10():
    p=PDF(G10/'files/the-road-not-taken-worksheet.pdf','The Road Not Taken')
    p.start('Grade 10 · 5 units · Poetry','The Road Not Taken','Robert Frost (1874–1963)<br/>Name: __________________________    Class: ________    Date: __________')
    for i,line in enumerate(POEM,1):
        p.p(f'<font face="Body" color="#667c88" size="8">{i:02d}</font>   '+esc(line),size=12,font='Serif',leading=18,after=1)
        if i in (5,10,15):
            p.y-=9
    p.y-=10
    p.p('<b>Word help</b><br/>diverged = separated · undergrowth = plants growing under trees<br/>fair = attractive · wanted wear = needed to be walked on<br/>trodden = stepped on · hence = from now · sigh = a long breath',size=10.2,leading=15)
    p.p(f'<link href="{SOURCES[0][1]}" color="#23687c">Text: Academy of American Poets.</link> Public-domain poem, published in 1915; collected in <i>Mountain Interval</i> (1916).',size=8.7,leading=12)
    p.start('Core worksheet · Questions 1–6','Read closely','Answer in English. Support interpretations with words or line numbers from the poem.')
    for i,(q,_) in enumerate(QUESTIONS10[:6],1):
        p.p(f'<b>{i}.</b> '+esc(q),size=11.1,leading=15.4,after=1)
        p.lines(3 if i in (4,5,6) else 2,gap=19)
    p.p('<b>Before you finish:</b> Check that you have distinguished what the speaker says directly from what you infer.',size=10.2,leading=14)
    p.start('Optional extension · Questions 7–8','Connect & interpret','Complete in class if time allows, or continue next lesson.')
    p.p('<b>Background for question 7</b>',size=11.5,after=4)
    p.p(esc(BRIDGE),size=11,leading=15.5)
    p.p(f'<link href="{SOURCES[2][1]}" color="#23687c">Adapted from David Orr, Academy of American Poets.</link>',size=8.5,leading=12,after=15)
    p.p('<b>7.</b> '+esc(QUESTIONS10[6][0]),size=11,leading=15.5,after=1)
    p.lines(4,gap=19)
    p.p('<b>8.</b> '+esc(QUESTIONS10[7][0]),size=11,leading=15.5,after=1)
    p.lines(9,gap=20)
    p.p('<b>Response check:</b> clear view · two details · explanation of how each detail supports your view',size=10,leading=14)
    p.save()
    p=PDF(G10/'files/the-road-not-taken-answer-key.pdf','The Road Not Taken · Teacher key')
    p.start('Teacher copy · Grade 10 · 5 units','Answer key & lesson script','Core questions 1–6. Questions 7–8 and the literary tools section are extensions.')
    p.p('<b>90-minute lesson:</b> recall 5; poet background 8; rereading 7; worksheet 20; discussion 20; visual breaks and idiom 5; optional extension 20; exit ticket 5.',size=10.4)
    p.p('<b>Poet background:</b> '+esc(BIO),size=10.4)
    p.p('<b>Reading stance:</b> distinguish Frost from the speaker. Compare lines 9–12 with the imagined later story in lines 16–20. Avoid presenting “choose the unpopular path” as the only meaning. The sigh permits more than one supported interpretation.',size=10.4)
    for i,(_,a) in enumerate(QUESTIONS10[:6],1):
        p.p(f'<b>{i}.</b> '+esc(a),size=10.6,leading=15,after=10)
    p.start('Teacher copy · Optional extension','Thinking, context & writing')
    p.p('<b>7. Bridging sample:</b> '+esc(QUESTIONS10[6][1]),size=10.6)
    p.p('<b>8. Sample response:</b> '+esc(QUESTIONS10[7][1]),size=10.6)
    p.p('<b>Assessment:</b> accept satisfaction, regret, mixed feelings or uncertainty when two relevant details are explained. “All the difference” does not itself state whether the result was good or bad.',size=10.6)
    p.p('<b>LOTS:</b> finding, identifying and recalling explicit information. <b>HOTS:</b> inferring, comparing, explaining or evaluating with evidence. The question word alone does not determine the thinking level.',size=10.6)
    p.p('<b>Literary tools:</b> poem = literary text; poet = writer; speaker = voice in the poem; line = one row; stanza = group of lines; metaphor = one thing standing for another; theme = a central idea explored in the text.',size=10.6)
    p.p('<b>Bridging:</b> background detail + poem detail + an explained connection. The Thomas background opens a useful reading; it does not prove that the speaker is Thomas or settle every ambiguity.',size=10.6)
    p.p('<b>Visual riddle:</b> At sixes and sevens = confused or disorganized. The cats are a playful number clue, not the idiom’s origin. The silent clip plays only when selected; moving slides stops playback.',size=10.6)
    p.p('<b>Sources</b>',size=11.5,after=4)
    for name,url in SOURCES+[('Idiom: Cambridge Dictionary',IDIOM_SOURCE)]:
        p.p(f'<link href="{url}" color="#23687c">{esc(name)}</link>',size=9.5,leading=13,after=5)
    p.save()

if __name__ == '__main__':
    count=len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",' '.join(STORY)))
    assert 250<=count<=300,count
    a,b=grade8(),grade10()
    pdf8()
    pdf10()
    manifest={'story_word_count':count,'vocabulary':VOCAB,'grade8':{'slides':len(a.slides),'questions':QUESTIONS8},'grade10':{'slides':len(b.slides),'questions':QUESTIONS10},'poem':POEM}
    (ROOT/'tools/lessons_20260910_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(f'Story: {count} words. Four PDFs written.')
