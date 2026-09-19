"""Shared progress metadata and an English edition of the existing lesson."""
import copy, html, json, re
ORDINALS='First Second Third Fourth Fifth Sixth Seventh Eighth Ninth Tenth'.split()
ROLES=['Opening','My opinion','Against','If + since','For','Experience','Conclusion','Passive','Example','One more idea']
# Slide number: English title, student support, teacher note.
EN={
1:('Welcome','Bnei Akiva Yeshiva, Kiryat Herzog','Apply grammar already learned. Do not reteach the whole grammar unit.'),
2:('A clear essay, one step at a time','Use familiar words and useful sentence patterns.','Aim for clear, developed ideas in language students can use independently. This model does not guarantee an exam score.'),
3:('The writing task','Should everyone have a chance to play?','Distinguish class games from selection for a school team. This is a practice task.'),
4:('Four paragraphs','Opening and opinion; an idea against; an idea for; conclusion.','Practice target: 120–140 words. In an exam, follow the task instructions.'),
5:('Useful words for other essays','Choose a phrase that fits your idea.','Since gives a reason. Moreover adds an idea. Therefore gives a result. Reuse a small set of useful phrases.'),
6:('Words for this topic','Choose words you know how to use.','Prefer familiar, accurate words such as games, help and friends. A longer word is not automatically better.'),
7:('A short plan','What is one problem? What is one benefit?','Write two short notes. First-language notes are fine at this planning stage. Do not write the whole essay yet.'),
8:('', 'Introduce the topic. Do not give your opinion yet.',''),
10:('', 'Should every student have a chance to play?',''),
12:('A short break','','A ten-second pause about planning. No extra task.'),
13:('', 'What may happen if some players make mistakes?',''),
15:('First Conditional','A possible condition and result. No will after if.','Briefly review a familiar pattern. Do not introduce the Second Conditional here.'),
16:('A possible condition','','Ask students to identify the condition and result.'),
17:('A possible condition','If + Present Simple, will + verb.','Ask students to identify the condition and result.'),
18:('Since gives a reason','','Use since to build a useful habit. Choosing since instead of because does not automatically earn more marks.'),
19:('Since gives a reason','since = because. Follow it with a subject and a verb.','Use since to build a useful habit. Choosing since instead of because does not automatically earn more marks.'),
20:('', 'Give a possible result and explain the reason.',''),
22:('', 'How can playing together help students?',''),
24:('A short break','','A short pause about teamwork and the Present Perfect.'),
25:('Present Perfect','A past experience that matters to our idea now.','Some students have felt alone; a team can help them. Do not add a finished past time such as yesterday.'),
26:('A past experience','','Identify the plural subject; choose have and the V3 form.'),
27:('A past experience','Students is plural: have felt.','Identify the plural subject; choose have and the V3 form.'),
28:('', 'Connect a past experience to the benefit of playing together.',''),
30:('', 'Repeat your opinion briefly. Do not add a new argument.',''),
32:('Passive','Say what should happen to every student.','Keep the pattern simple: should be included. Focus on students receiving a chance to join in.'),
33:('A recommendation in the passive','','Check be and the V3 form. A longer verb is not needed.'),
34:('A recommendation in the passive','should be + V3: should be included.','Check be and the V3 form. A longer verb is not needed.'),
35:('', 'End with a recommendation that supports your opinion.',''),
37:('The draft is still short','Add an example in paragraph 2 and an idea in paragraph 3.','The draft has 100 words. Develop the body paragraphs. Do not add a fifth paragraph or empty words.'),
38:('', 'Give a simple example of a mistake. Put it in paragraph 2.',''),
40:('', 'What else can students learn? Put this idea in paragraph 3.',''),
42:('A short break','','A short return to the essay topic: friendship and a chance for everyone.'),
43:('Patterns for your next essay','Change the idea and topic words. Choose a pattern that fits.','Do not force a pattern into an unrelated idea. Playing and joining also model gerunds naturally; no separate unit is needed.'),
44:('Your own essay','Choose your opinion and develop your ideas.','Keep four paragraphs. Do not show a model for this new topic before students try.'),
45:('Plan your essay','Write three short notes.','Allow three minutes. Help with one idea at a time. Useful words: work, money, time, school, tired, help.'),
46:('Write your essay','Four paragraphs. One sentence at a time.','Protect 14 minutes of writing. Do not stop the class for each error. Give at most two key corrections per student. An unfinished draft can be completed later.'),
47:('Before you edit','Check ideas and four paragraphs first. Then check language.','Count words and develop the body if needed. Keep necessary ideas even when simplifying the language.'),
48:('Edit your essay','Improve one idea or explanation and one language point.','Protect three minutes of editing. Use the phrase bank without automatically replacing correct words.'),
49:('Exit question','','A simple sentence that explains an idea is better than one students cannot understand or use.'),
50:('Exit question','A clear sentence explains the idea.','A simple sentence that explains an idea is better than one students cannot understand or use.')}
ALTS={'tiny-goal':'A cat throws a paper ball; it lands on its own head.','two-friends':'Two cats try to high-five and finally succeed.','chair-friend':'A cat moves a chair for a friend and tries again after a mistake.'}
UI={'כיתה י״א · 5 יח״ל':'Grade 11 · 5-point English','ברוכים הבאים':'Welcome','ישיבת בני עקיבא קריית הרצוג':'Bnei Akiva Yeshiva, Kiryat Herzog','השהיית ההנפשה':'Pause animation','הפעלה מחדש':'Replay','זמן שנותר':'Time remaining','התחלה':'Start','איפוס':'Reset','+30 שניות':'+30 seconds','חזרה לכיתה י״א 5 יח״ל':'Grade 11 resources','לשקף הקודם':'Previous slide','לשקף הבא':'Next slide'}

def build_versions(g):
    out,S,body=g['OUT'],g['S'],g['body']
    completed=0
    for s in S:
        # Draft prompts and cumulative reveals both have an explicit English ordinal.
        step=s.get('step') or s.get('draftStep')
        if step:
            s['title']=f'{ORDINALS[step-1]} sentence · '+('Our essay so far' if s['kind']=='essay' else ROLES[step-1])
        if s['kind']=='essay':completed=s['step']
        s['completedSentences']=completed
        s['completedWords']=len(' '.join(g['SENTENCES'][:completed]).split())
        s['writingStep']=s.get('draftStep',0)
    en=copy.deepcopy(S)
    for s in en:
        if s['kind']=='essay':
            s['he']=f'{s["step"]}/10 sentences · {s["completedWords"]} words'
            s['note']='Read only the new sentence: '+g['SENTENCES'][s['step']-1]+' Keep sentences 9 and 10 inside the body paragraphs.'
        else:
            title,support,note=EN[s['n']]
            if title:s['title']=title
            s['he']=support
            s['note']=note or 'Allow a short independent attempt. Accept simple, correct wording. Reveal the model afterwards.'
        if s['kind']=='cover':s['text']='Grade 11 · 5-point English'
        if s.get('asset'):s['alt']=ALTS[s['asset']]
    base=(out/'index.html').read_text()
    items=''.join(f'<li data-sentence="{i}"><span class="sentence-number">{i}</span><span class="sentence-role">{role}</span></li>' for i,role in enumerate(ROLES,1))
    rail=f'<aside class="essay-progress" dir="ltr" lang="en" aria-label="Model essay progress"><h2>Model essay</h2><div class="essay-stats" aria-live="polite" aria-atomic="true"><strong><span data-sentence-count>0</span><small> / 10</small></strong><span>sentences</span><strong data-word-count>0</strong><span>words so far</span></div><progress aria-label="Completed model sentences" max="10" value="0"></progress><ol>{items}</ol><p class="word-target">Goal: 120–140 words</p></aside>'
    for lang,slides,name in [('he',S,'index.html'),('en',en,'english.html')]:
        is_en=lang=='en'
        sections=''.join(f'<section class="slide {s["kind"]}{" reveal" if s.get("reveal") else ""}" data-slide="{s["n"]}" data-section="{s["section"]}" data-completed="{s["completedSentences"]}" data-words="{s["completedWords"]}" data-writing-step="{s["writingStep"]}"'+(f' data-pair="{s["pair"]}"' if s.get('pair') else '')+f' aria-label="{("Slide" if is_en else "שקף")} {s["n"]} / 50" hidden><div class="frame">{body(s)}</div></section>' for s in slides)
        page=re.sub(r'<main class="stage">.*?</main>',lambda _:f'{rail}<main class="stage">{sections}</main>',base,flags=re.S)
        switch=f'<a class="language-switch" href="{("index.html" if is_en else "english.html")}" lang="{("he" if is_en else "en")}">{("עברית" if is_en else "English")}</a>'
        page=page.replace('<nav class="lesson-sections">',switch+'<nav class="lesson-sections">')
        page=page.replace('20260919-simple72','20260919-progress-en').replace('src="lesson.js"','src="lesson.js?v=20260919-progress-en"')
        if is_en:
            page=page.replace('lang="he" dir="rtl"','lang="en" dir="ltr"').replace('<title>י״א ·','<title>Grade 11 ·').replace('files/grammar-in-an-essay.pptx','files/grammar-in-an-essay-en.pptx')
            for he,eng in UI.items():page=page.replace(he,eng)
            for he,eng in [('תכנון','Plan'),('דקדוק','Grammar'),('חיבור','Essay'),('כתיבה','Write')]:page=page.replace('>'+he+'</a>','>'+eng+'</a>')
            # The language switch intentionally keeps the other language's native name.
            assert not re.search('[\u0590-\u05ff]',page.replace('עברית',''))
        (out/name).write_text(page)
        data=copy.deepcopy(g['data']);data.update(slides=slides,language=lang,grade='Grade 11 · 5-point English' if is_en else data['grade'],sentenceRoles=ROLES)
        (out/('lesson.en.json' if is_en else 'lesson.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2))
    teacher=(out/'teacher.html').read_text().replace('20260919-simple72','20260919-progress-en')
    teacher=teacher.replace('<h2>סדר הכתיבה</h2>','<h2>סרגל ההתקדמות</h2><p>בצד שמאל מוצגים מראש כל עשרת המשפטים. הספירה מתייחסת לחיבור לדוגמה: ניסיון עצמאי עדיין אינו מוסיף משפט; בחשיפת המשפט מתעדכנים מספר המשפטים והמילים. חזרה אחורה מחזירה את הספירה המתאימה. משפטים 9–10 מרחיבים את הגוף. בזמן התרגול העצמאי הסרגל ממשיך להציג את המודל שהושלם.</p><p><a href="english.html">English presentation</a> · <a href="teacher.en.html">English teacher script</a> · <a href="files/grammar-in-an-essay-en.pptx?v=20260919-progress-en">English PPTX</a></p><h2>סדר הכתיבה</h2>')
    for s in S:
        teacher=re.sub(rf'<summary>שקף {s["n"]}: .*?</summary>',lambda _,s=s:f'<summary>שקף {s["n"]}: {html.escape(s["title"])}</summary>',teacher)
    (out/'teacher.html').write_text(teacher)
    time_labels=['Task, structure and familiar words','Opening, opinion and opposing idea','First Conditional, since and sentence 4','Supporting idea and Present Perfect','Conclusion and passive recommendation','Two body expansions and useful patterns','Plan the after-school job essay','14 minutes of independent writing','Check and three minutes of editing','Exit question']
    rows=''.join(f'<tr><td>{a}</td><td>{next(s["n"] for s in S if s["section"]==b)}</td><td>{time_labels[i]}</td></tr>' for i,(a,b,_) in enumerate(g['timeline']))
    script=''.join(f'<details><summary>Slide {s["n"]}: {html.escape(s["title"])}</summary><p>{html.escape(s["note"])}</p><p class="en">{html.escape(s["text"])}</p><a href="english.html#slide-{s["n"]}">Open slide</a></details>' for s in en)
    style=re.search(r'<style>.*?</style>',teacher,re.S).group().replace('text-align:right','text-align:left')
    en_teacher=f'''<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Teacher script · Advanced Grammar in an Essay</title>{style}</head><body><main><a href="../five-units/">Grade 11 resources</a><h1>Advanced Grammar in an Essay</h1><p>50 slides · 72 planned minutes · 123-word model.</p><p><a href="english.html">English presentation</a> · <a href="files/grammar-in-an-essay-en.pptx?v=20260919-progress-en">English PPTX</a> · <a href="teacher.html">Hebrew teacher script</a></p><h2>Teaching approach</h2><p>Use familiar topic words: games, play, team, friends, help, mistakes. Reuse useful connectors and grammar patterns. Develop explanations and examples instead of choosing longer words. Since is the preferred reason connector for this practice; it does not automatically earn more marks than because. Marks also depend on task fulfilment, development, organization, appropriate range and accuracy. This is a teaching model, not a guaranteed score.</p><h2>Time</h2><p>Plan for 72 minutes of work in a 90-minute meeting, leaving 18 minutes for interruptions and transitions. Three short animation breaks are already included. Review previously learned grammar briefly. Give one short independent sentence attempt before each model reveal. Read only the newly added sentence. Protect 14 minutes of writing and three minutes of editing; shorten whole-class sharing if delayed. Unfinished drafts can be completed later.</p><table><tr><th>Minutes</th><th>First slide</th><th>Activity</th></tr>{rows}</table><h2>Progress sidebar</h2><p>All ten sentence steps are visible from the start. The count belongs to the model essay, not to individual students. A prompt highlights the next sentence; the count increases only when its model is revealed. Moving backwards restores the count for that slide. The completed model remains at 10 sentences and 123 words during independent practice.</p><h2>Writing order</h2><p>Draft sentences 1–8, then add sentence 9 inside paragraph 2 and sentence 10 inside paragraph 3. Final reading order: 1,2 / 3,4,9 / 5,6,10 / 7,8. The eight-sentence draft has 100 words; the expansions bring it to 111, then 123. Keep four paragraphs.</p><h2>Grammar</h2><p>First Conditional: If + Present Simple, will + verb. Present Perfect: have + V3. Passive: should be + V3. Playing and joining provide natural gerund examples without a separate teaching unit. These are practice choices; students must follow the instructions on their actual exam.</p><h2>Independent practice</h2><p>Should teenagers have an after-school job?</p><p>Students choose their position and write one sentence at a time. Useful words: work, money, time, school, tired, help. Give feedback on content before language, with at most two key corrections. Do not dictate a ready-made answer.</p><h2>Timers and breaks</h2><p>Website timers start on click, can be paused or extended, and pause when leaving a slide. Slides do not advance automatically. PPTX timers show time allocations with links to the website timers. GIF playback depends on the presentation application.</p><h2>Topic</h2><p>{html.escape(g['TOPIC'])}</p><h2>Model essay: 123 words</h2>{''.join('<p>'+html.escape(p)+'</p>' for p in g['P'])}<h2>Slide-by-slide script</h2>{script}<h2>Writing task source</h2><a href="{g['SOURCE']}">Module G, summer 2026</a></main></body></html>'''
    assert not re.search('[\u0590-\u05ff]',en_teacher)
    (out/'teacher.en.html').write_text(en_teacher)
