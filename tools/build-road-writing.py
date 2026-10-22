"""Build Simon's six-step Road Not Taken writing lesson from local content."""
from pathlib import Path
from html import escape as esc
import json

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'grade10/group-a/road-writing-minimum'
QUESTIONS = json.loads((DEST / 'questions.json').read_text())
PHASES = ['השאלה באנגלית', 'מבינים את השאלה', 'חושבים בעברית', 'התשובה בעברית', 'כותבים באנגלית', 'שאלה ותשובה']


def answer(q):
    rows = []
    for n, options in enumerate(q['sentences']):
        assert len(options) == len(set(options)) == 6
        variants = ''.join(f'<span class="sentence-variant{" is-current" if i == 0 else ""}" aria-hidden="{str(i != 0).lower()}">{esc(text)}</span>' for i, text in enumerate(options))
        rows.append(f'<div class="sentence-row"><div class="sentence-caption" dir="rtl">משפט {n+1}<span class="variant-count" aria-hidden="true">1 / 6</span></div><span class="sentence-choice en" lang="en" role="button" tabindex="0" data-sentence="{n}" data-choice="0" aria-label="{esc(options[0])} לחצו לניסוח אחר">{variants}</span></div>')
    return f'<div class="sentence-answer" data-answer-group="q{q["id"]}" data-interval="10000">'+''.join(rows)+'</div>'


def question(q):
    return f'<h1 class="question-en en" lang="en">{esc(q["question"])}</h1>'


slides = []
for q in QUESTIONS:
    for phase in range(6):
        number = (q['id']-1)*6+phase+1
        meta = f'<div class="lesson-meta"><span class="question-number en">QUESTION {q["id"]:02} / 06</span><span class="phase-name">{PHASES[phase]}</span></div>'
        if phase in (0, 1):
            # Both slides contain identical geometry, including the hidden translation slot.
            body = question(q) + f'<div class="question-translation{" unrevealed" if phase == 0 else ""}" aria-hidden="{str(phase == 0).lower()}"><p class="hebrew-question">{esc(q["translation"])}</p><p class="question-meaning">{esc(q["meaning"])}</p><p class="keywords">{esc(q["keywords"])}</p></div>'
        elif phase == 2:
            body = question(q) + '<div class="think-he"><h2>מה נענה בעברית?</h2><p>נסחו תשובה בקול, לפני שממשיכים.</p></div>'
        elif phase == 3:
            body = '<h1 class="hebrew-title">תשובה אפשרית בעברית</h1><div class="hebrew-answer">' + ''.join(f'<p>{esc(t)}</p>' for t in q['hebrewAnswer']) + '</div><p class="small-note">עכשיו נלמד לכתוב את הרעיון באנגלית.</p>'
        elif phase == 4:
            body = '<h1 class="answer-title">שני משפטים פשוטים</h1>' + answer(q)
            body += '<div class="answer-tools"><button class="sequence-toggle" aria-pressed="true">Ⅱ השהיית ההחלפות</button><span class="timing-note">10 שניות · המשפטים מתחלפים בתור</span></div>'
            if q.get('upgrade'):
                body += f'<details class="optional-upgrade"><summary>שדרוג לבחירה</summary><p class="en" lang="en">{esc(q["upgrade"])}</p><p>{esc(q["upgradeNote"])}</p></details>'
            else:
                body += f'<p class="copy-note">{esc(q["copyNote"])}</p>'
        else:
            body = question(q)
            if q.get('copyQuote'):
                body += f'<div class="exam-copy"><p class="answer-caption">תשובת המבחן — העתקה מדויקת</p><blockquote class="en" lang="en">“{esc(q["copyQuote"])}”</blockquote><p class="line-label">שורה {q["copyLine"]}</p></div>'
            else:
                body += answer(q)
                body += '<div class="answer-tools"><button class="sequence-toggle" aria-pressed="true">Ⅱ השהיית ההחלפות</button><span class="timing-note">10 שניות · המשפטים מתחלפים בתור</span></div>'
            body += f'<div class="difficulty"><strong>רמת קושי: {esc(q["difficulty"])}</strong><p>{esc(q["check"])}</p></div>'
        slides.append(f'<section class="slide writing-slide phase-{phase+1}{" transition" if phase == 0 else ""}" hidden id="slide-{number}" data-section="q{q["id"]}" data-question="{q["id"]}" data-phase="{phase+1}" aria-label="שאלה {q["id"]}, {PHASES[phase]}"><div class="frame">{meta}{body}</div></section>')

nav = ''.join(f'<button data-jump="q{q["id"]}" aria-label="שאלה {q["id"]}">{q["id"]}</button>' for q in QUESTIONS)
html = '''<!doctype html>
<html lang="he" dir="rtl" data-deck-layout="natural">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#07111f"><meta name="description" content="The Road Not Taken: שש שאלות ליבה, הסבר בעברית, תשובות פשוטות וחלופות ניסוח צבעוניות.">
<title>The Road Not Taken · כותבים תשובה · כיתה י׳</title>
<link rel="stylesheet" href="../../../shared/deck/standard.css">
<link rel="stylesheet" href="../../../shared/deck/short-answer.css?v=20261022">
<link rel="stylesheet" href="../../../shared/deck/essay-clean.css">
</head><body>
<a class="home" href="../library/" aria-label="חזרה לכיתה י׳">⌂</a>
<nav class="section-nav" aria-label="שש שאלות הליבה">'''+nav+'''</nav>
<main class="stage">'''+''.join(slides)+'''</main>
<nav class="nav" aria-label="ניווט שקפים"><div class="nav-group"><button data-step="-1" aria-label="לשקף הקודם">←</button><button data-step="1" aria-label="לשקף הבא">→</button></div><div class="deck-name en" lang="en">The Road Not Taken</div><output id="counter" class="progress" aria-live="polite"></output></nav>
<div class="progress-track"><div class="progress-fill"></div></div>
<noscript><p>יש להפעיל JavaScript כדי לצפות במצגת.</p></noscript>
<script src="../../../shared/deck/standard.js?v=20261022-natural"></script>
<script src="../../../shared/deck/sentence-sequence.js?v=20261022"></script>
</body></html>
'''
(DEST / 'index.html').write_text(html)
print(f'Built {len(slides)} slides; {sum(len(s) for q in QUESTIONS for s in q["sentences"])} sentence alternatives.')
