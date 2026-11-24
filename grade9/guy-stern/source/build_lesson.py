"""Build the story-specific content; shared Teachers modules own navigation and reading."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
story = json.loads((ROOT / 'story.json').read_text())
support = json.loads((ROOT / 'lesson-support.json').read_text())
audio = json.loads((ROOT / 'audio.json').read_text())
photos = json.loads((ROOT / 'assets/attribution.json').read_text())
esc = lambda s: html.escape(str(s), quote=True)
slides, chapters, records, glosses = [], [], [], []
global_word = 1
images = ['guy-stern.jpg','soldan-school-2014.jpg','camp-ritchie-postcard.jpg','normandy-1944.jpg','soldan-school-2014.jpg','guy-stern.jpg']
prompts = [
    'What would you need to learn in a new country?',
    'How can school help someone feel at home?',
    'How can a language become a useful skill?',
    'What changes when a person gains new skills?',
    'What can you do when a plan does not work?',
    'What is one step you can take towards a goal?'
]

def photo(name, cls=''):
    p = next(p for p in photos if p['filename'] == name)
    return f'''<figure class="history-photo {cls}"><img src="assets/{name}" alt="{esc(p['captionEn'])}" loading="lazy" width="900" height="1000"><figcaption>{esc(p['captionEn'])}<a href="{esc(p['sourceUrl'])}" target="_blank" rel="noopener">{esc(p['credit'])}</a></figcaption></figure>'''

def add(kind, body, chapter=None, **attrs):
    n = len(slides)+1
    meta = {'slide': n, 'kind': kind, 'chapter': chapter}
    meta.update(attrs)
    extra = ' '.join(f'data-{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())
    slides.append((meta, f'<section id="slide-{n}" class="slide {kind}" data-kind="{kind}" data-chapter="{chapter or 0}" {extra} hidden><div class="frame">{body}</div></section>'))
    return n

add('story-cover', f'''<div class="cover-grid"><div class="cover-copy"><p class="kicker">GUY STERN · A TRUE STORY</p><h1>A Future<br>to <em>Build</em></h1><p class="cover-summary">At fifteen, he left Germany for America.<br>A new language. A new country. A future to build.</p><p class="he-help cover-he" lang="he" dir="rtl">סיפורו האמיתי של גאי שטרן — על בחירות, הסתגלות ותקווה.</p><div class="story-facts"><span>Grade 9</span><span>6 chapters</span><span>748 words</span></div><div class="cover-actions"><button class="primary" data-start>Start the story</button><button data-open-menu>Choose a chapter</button><button id="resume" hidden>Continue</button></div><a class="download-link" href="files/Guy_Stern_A_Future_to_Build_Grade9.pdf" target="_blank" rel="noopener">Read or print the two-page story</a><p class="cover-note">Read, listen and think about the decisions that shaped his life.</p></div>{photo('guy-stern.jpg','cover-photo')}</div>''')

for ci,(ch,sup,track) in enumerate(zip(story['chapters'],support['chapters'],audio['chapters'])):
    cid = ci+1
    chapter = {'id':cid,'title':ch['title'],'titleHe':sup['titleHe'],'start':len(slides)+1,'reading':[],'vocabulary':[],'questions':[]}
    head = f'<p class="kicker">CHAPTER {cid} OF 6</p><h2>{esc(ch["title"])}</h2><p class="he-help" lang="he" dir="rtl">{esc(sup["titleHe"])}</p>'
    add('chapter-opening', f'''<div class="chapter-grid"><div>{head}<p class="place-label">{esc(sup['sceneLabel'])}</p><p class="chapter-prompt">{esc(prompts[ci])}</p><div class="chapter-actions"><button class="primary" data-vocabulary="{cid}">Explore 4 words</button><button data-listen-chapter="{cid}">Listen and read</button></div></div>{photo(images[ci])}</div>''', cid)
    for vi,v in enumerate(sup['vocabulary']):
        n = add('vocabulary-card', f'''<p class="kicker">CHAPTER {cid} · WORD {vi+1} / 4</p><h2 class="vocab-word">{esc(v['word'])}</h2><p class="vocab-example">{esc(v['exampleEnglish'])}</p><div class="vocab-actions"><button data-vocab-audio="audio/vocabulary/vocab-{cid}-{vi+1}.mp3" data-audio-action="toggle" aria-label="Listen to {esc(v['word'])} and its example">Listen</button><button class="primary" data-vocab-reveal data-reveal="answer" aria-expanded="false">Show the meaning</button></div><div class="vocab-answer" aria-live="polite"><div class="answer-content" hidden><p class="vocab-definition">{esc(v['definition'])}</p><p class="vocab-he" lang="he" dir="rtl">{esc(v['hebrew'])}</p></div></div><p class="subtle">Read the example. What could the word mean?</p>''',cid,vocab=vi)
        chapter['vocabulary'].append(n)
    record = {'src':track['src'],'duration':track['duration'],'words':[],'phrases':[]}
    word_gloss = []
    for pi,units in enumerate(sup['translationUnits']):
        assert ' '.join(u['text'] for u in units) == ch['paragraphs'][pi]
        for unit in units:
            gid = len(glosses)
            glosses.append({'en':unit['text'],'he':unit['hebrew']})
            word_gloss.extend([gid]*len(unit['text'].split()))
    base = global_word
    for wi,w in enumerate(track['words']):
        record['words'].append({'id':base+wi,'text':w['text'],'start':w['start'],'end':w['end']})
    pages = sup.get('readingPages') or [dict(paragraph=pi,wordStart=0,wordEnd=len(p.split()),text=p,hebrew=sup['paragraphsHe'][pi]) for pi,p in enumerate(ch['paragraphs'])]
    for page_index, pg in enumerate(pages):
        pi = pg['paragraph']
        pa = track['paragraphs'][pi]
        first = pa['wordStart']+pg['wordStart']
        last = pa['wordStart']+pg['wordEnd']-1
        assert ' '.join(w['text'] for w in track['words'][first:last+1]) == pg['text']
        words = ' '.join(f'<span class="ra-word" data-word="{base+wi}" data-gloss="{word_gloss[wi]}" tabindex="0" role="button" aria-label="{esc(track["words"][wi]["text"])} — Hebrew meaning">{esc(track["words"][wi]["text"])}</span>' for wi in range(first,last+1))
        reading_text = f'''<div class="reading-heading"><p class="kicker">CHAPTER {cid} · {esc(ch['title'])}</p><span class="passage-label">Passage {page_index+1} / {len(pages)}</span></div><div class="passage-tabs" role="tablist" aria-label="Chapter {cid} passages" data-tabs="{cid}" data-page="{page_index}"></div><div class="reading-grid"><div class="reading-copy" role="tabpanel" aria-label="Passage {page_index+1}"><p class="story-text" lang="en" dir="ltr">{words}</p><div class="translation-space"><p class="read-translation he-help" lang="he" dir="rtl">{esc(pg['hebrew'])}</p></div><p class="reading-help subtle">Touch or point to any word for Hebrew help.</p></div>{photo(images[ci], 'reading-photo')}</div>'''
        n = add('story-reading', reading_text,cid,first=base+first,last=base+last,page=page_index,paragraph=pi,start=track['words'][first]['start'],end=track['words'][last]['end'])
        chapter['reading'].append(n)
        record['phrases'].append({'first':base+first,'last':base+last,'gapMs':0,'pauseKind':'passage'})
    records.append(record)
    global_word += len(track['words'])
    for qi,q in enumerate(sup['questions']):
        qbody = f'''<p class="kicker">CHAPTER {cid} · THINK &amp; DISCUSS · {qi+1} / 2</p><h2 class="discussion-question">{esc(q['question'])}</h2><p class="question-he he-help" lang="he" dir="rtl">{esc(q['questionHe'])}</p>'''
        n = add('discussion', qbody+'''<div class="answer-space"><p class="discussion-instruction">Try an answer in your own words.</p><button class="primary" data-show-answer data-reveal="answer">Show a possible answer</button></div>''',cid,question=qi)
        chapter['questions'].append(n)
        add('discussion answer',qbody+f'''<div class="answer-space"><p class="answer-kicker">A POSSIBLE ANSWER</p><p class="model-answer">{esc(q['modelAnswer'])}</p><p class="model-he he-help" lang="he" dir="rtl">{esc(q['modelAnswerHe'])}</p></div>''',cid,question=qi)
    chapters.append(chapter)

ref=support['finalReflection']
add('final-reflection',f'''<div class="final-grid"><div><p class="kicker">AFTER THE STORY</p><h2>{esc(ref['title'])}</h2><p class="final-question">{esc(ref['question'])}</p><p class="he-help" lang="he" dir="rtl">{esc(ref['questionHe'])}</p><div class="writing-starters"><p>I would like to…</p><p>One step I can take is…</p></div><p class="subtle">Share an idea, or write two sentences in your notebook.</p><div class="chapter-actions"><button data-open-menu>Revisit a chapter</button><a class="button primary" href="../../#grade9">Grade 9 materials</a></div></div>{photo('guy-stern.jpg')}</div>''')

menu=''.join(f'''<article class="chapter-choice"><span class="chapter-number">{c['id']:02}</span><div><h3>{esc(c['title'])}</h3><p lang="he" dir="rtl">{esc(c['titleHe'])}</p><div><button data-jump-slide="{c['start']}">Start chapter</button><button data-listen-chapter="{c['id']}">Listen and read</button></div></div></article>''' for c in chapters)
sources=''.join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a><p>{esc(s["supports"])}</p></li>' for s in story['sources'])
credits=''.join(f'<li><a href="{esc(p["sourceUrl"])}" target="_blank" rel="noopener">{esc(p["title"])}</a><p>{esc(p["credit"])} · <a href="{esc(p["licenseUrl"])}" target="_blank" rel="noopener">{esc(p["license"])}</a></p><p>{esc(p["changes"])}</p></li>' for p in photos)
html_doc=f'''<!doctype html>
<html lang="en" dir="ltr" data-deck-layout="natural" data-essay-language="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Guy Stern · A Future to Build | Grade 9 Read-Along</title><meta name="description" content="Guy Stern's true story for Grade 9: six chapters, recorded English narration, word highlighting, Hebrew support and questions."><link rel="stylesheet" href="../../shared/deck/standard.css?v=20261124"><link rel="stylesheet" href="../../shared/read-along/inline-reader.css?v=20261124"><link rel="stylesheet" href="lesson.css?v=1"></head>
<body><header class="lesson-header"><a class="class-home" href="../../#grade9" aria-label="Grade 9 learning materials"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3 10 9-7 9 7v11h-6v-7H9v7H3z"/></svg><span>Grade 9</span></a><span class="header-title">GUY STERN</span><nav class="lesson-tools" aria-label="Lesson tools"><button data-open-menu>Chapters</button><button id="hebrew-toggle" lang="he" dir="rtl" aria-pressed="false">עברית</button><button id="copy-link" aria-label="Copy a link to this slide">Copy link</button><button id="fullscreen" aria-label="Full screen">Full screen</button></nav></header>
<main class="stage" aria-label="Read-Along lesson">{''.join(s[1] for s in slides)}</main>
<section id="reader-bar" class="reader-bar" data-reader data-first="1" data-last="1" hidden aria-label="Recorded narration controls"><div class="playback-row"><button id="play" class="primary" data-read-play data-audio-action="toggle">Listen</button><button data-read-restart aria-label="Replay the current passage">Replay</button><button id="rewind" aria-label="Back fifteen seconds within this passage">15s back</button><button id="replay-sentence">Sentence</button><label class="rate-label" for="speed">Speed<select id="speed"><option value="0.25">0.25×</option><option value="0.35">0.35×</option><option value="0.5">0.5×</option><option value="0.75">0.75×</option><option value="1">1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label><span data-read-status class="reader-status" role="status"></span></div><div class="seek-row"><time id="elapsed">0:00</time><input id="seek" type="range" min="0" max="1" value="0" step="0.01" aria-label="Position in the current passage"><time id="duration">0:00</time></div></section>
<nav class="nav lesson-nav" aria-label="Slide navigation"><button id="prev" data-step="-1">Previous</button><div class="nav-middle"><span id="counter" class="progress"></span><button data-open-sources>Sources</button></div><button id="next" data-step="1">Next</button></nav><div class="progress-track"><div class="progress-fill"></div></div>
<dialog id="chapter-menu"><div class="dialog-heading"><div><p class="kicker">A FUTURE TO BUILD</p><h2>Choose a chapter</h2></div><button data-close-dialog aria-label="Close chapter menu">Close</button></div><div class="chapter-choices">{menu}</div><div class="menu-downloads"><a href="files/Guy_Stern_A_Future_to_Build_Grade9.pdf" target="_blank" rel="noopener">Story PDF · 2 pages</a><a href="files/Guy_Stern_A_Future_to_Build_Grade9.docx" download>Editable story · Word</a><button data-jump-slide="{len(slides)}">Final reflection</button></div></dialog>
<dialog id="sources"><div class="dialog-heading"><h2>Sources &amp; credits</h2><button data-close-dialog>Close</button></div><p>This educational adaptation keeps the historical events separate from the questions and discussion prompts. The familiar-name episode is attributed to Guy Stern's own account.</p><h3>Historical sources</h3><ul>{sources}</ul><h3>Images</h3><ul>{credits}</ul><h3>Narration</h3><p>Prerecorded synthetic narration: Microsoft Brian Neural, US English. This is an educational narrator, not a recording or imitation of Guy Stern. Word timing comes from the recorded narration's synthesis boundaries.</p><p>Reading and navigation use the shared Teachers Read-Along and Deck modules. Progress and language preferences are saved on this device only.</p><p>Created 24 November 2026.</p></dialog>
<dialog id="copy-dialog"><div class="dialog-heading"><h2>Copy lesson link</h2><button data-close-dialog>Close</button></div><p>Select and copy this link:</p><input id="manual-link" readonly aria-label="Link to this slide"></dialog><div id="toast" role="status" aria-live="polite"></div><div id="hand-guide" hidden aria-hidden="true"><span>☝</span><small>Tap for Hebrew</small></div>
<script src="lesson-data.js?v=1"></script><script src="../../shared/deck/standard.js?v=20261124"></script><script src="../../shared/read-along/inline-reader.js?v=20261124"></script><script src="lesson.js?v=1"></script><script defer src="../../shared/phone-remote/remote.js?v=20261102-qrfix3"></script></body></html>'''
(ROOT/'index.html').write_text(html_doc,encoding='utf-8')
data={'chapters':chapters,'slides':[s[0] for s in slides],'records':records,'glosses':glosses,'wordCount':global_word-1,'final':len(slides)}
(ROOT/'lesson-data.js').write_text('window.STERN_LESSON = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
assert global_word-1==748
print(json.dumps({'slides':len(slides),'readingPages':sum(len(c['reading']) for c in chapters),'words':global_word-1,'glosses':len(glosses)},indent=2))
