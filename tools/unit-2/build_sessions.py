"""Build the meeting index, student preparation sheet and HTML teacher guide."""
from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'grade7/unit-2'
E = html.escape

def activity(key, title, href, instruction):
    return dict(key=key, title=title, href=href, instruction=instruction)

MEETINGS = [
 dict(title='Seasons and school years', goal='Find when a school year begins and ends.',
      prep=['Write the four seasons in English.', 'Think: When does your school year begin?'],
      activities=[activity('listen','Read & Listen: the main text','reading/?text=school-calendars','Read the opening, Japan and the two US places. Listen again if you need help.'),activity('read','Find the calendar details','main-text.html','Find the start, the end and the summer holiday length for Japan and the two US places.'),activity('workbook','Workbook · page 1','files/unit2-workbook.pdf#page=1','Answer the two questions. Explain why Japan is different.')],
      timing=[(5,'Opening: name the seasons'),(12,'Vocabulary preview and retrieval'),(20,'Read Japan and the US examples'),(15,'Find and compare calendar facts'),(15,'Independent workbook answers'),(5,'Exit check')],
      check='Ask for a season, an end point and a holiday length. Check the fact before correcting the sentence.',
      support='Model one comparison. Then let pairs find a second one without your model.',
      exit='Say why Japan’s summer holiday does not end its school year.'),
 dict(title='Different holidays, different calendars', goal='Compare holidays and the length of a school year.',
      prep=['Read your notes from Meeting 1.', 'Write one question about a school holiday.'],
      activities=[activity('read','England, the UAE and Jersey','main-text.html','Read the remaining places. Find a season and a holiday length in each one.'),activity('listen','Read & Listen: compare the places','reading/?text=school-calendars','Listen to the remaining sections. Read the final section about the length of a school year.'),activity('workbook','Workbook · page 3, Part C','files/unit2-workbook.pdf#page=3','Answer the calendar questions. Use the text as evidence.')],
      timing=[(7,'Recall the earlier places'),(12,'Vocabulary preview and retrieval'),(18,'Read the remaining calendar sections'),(18,'Compare dates, seasons and holiday lengths'),(12,'Share and improve answers'),(5,'Exit check')],
      check='Distinguish a whole school-year span from uninterrupted lessons. Accept about nine months in Anchorage and about eleven in Kent.',
      support='Use a three-part prompt: starts / ends / summer holiday. Remove it for the final comparison.',
      exit='Explain one difference between Anchorage and Miami-Dade.'),
 dict(title='WhatsApp from Argentina: routines', goal='Describe a routine with I and he.',
      prep=['Think about how you get to school.', 'Prepare one sentence beginning with I.'],
      activities=[activity('message','A Horse Before Class · WhatsApp','journey-horse.html','Read Carlito’s message. Find who travels with him and how far they travel.'),activity('grammar','Present Simple A · slides 1–27','grammar-a/#1','Work on routines and third-person forms. Stop after the first writing task.'),activity('workbook','Workbook · page 2','files/unit2-workbook.pdf#page=2','Answer the reading questions and write two facts about Carlito.')],
      timing=[(5,'Opening diagnosis'),(10,'Vocabulary preview and retrieval'),(12,'Read the WhatsApp adaptation'),(18,'Routines and third person: selected slides'),(17,'Independent workbook writing'),(10,'Collect, discuss and check')],
      check='Look for he rides and he wants. The factual content and the third-person ending are separate checks.',
      support='Contrast I ride with he rides. Ask for a new sentence before showing the answer slide.',
      exit='Answer Carlito’s question in one or two sentences.'),
 dict(title='What we do and do not do', goal='Write clear negative sentences about routines.',
      prep=['Bring the two sentences you wrote about Carlito.', 'Think of one thing you do not do on school mornings.'],
      activities=[activity('grammar','Present Simple A · slides 28–46','grammar-a/#28','Practise do not and does not. Use the base verb after does not.'),activity('practice','Words in Context · set 4','vocabulary/practice.html?set=3','Choose the meaning that fits. Write your own sentence at the writing stop.'),activity('writing','Writing sheet · Part A','worksheet.html','In your notebook, write your routine, a friend’s routine and one negative sentence.')],
      timing=[(7,'Recall and diagnose'),(10,'Vocabulary preview and retrieval'),(20,'Negatives and base verbs'),(15,'Context practice'),(15,'Independent routine writing'),(5,'Exit check')],
      check='A correct negative needs both the meaning and the base verb. Do not accept doesn’t walks.',
      support='Keep the original meaning when correcting a sentence. Check be separately from action verbs.',
      exit='Write one true sentence with does not about a friend.'),
 dict(title='Email from India: questions and teamwork', goal='Ask and answer questions about a journey.',
      prep=['Think: Who travels with you?', 'Write one question beginning with Do or Does.'],
      activities=[activity('message','Four Kilometres Together · email','journey-wheelchair.html','Read Samuel’s email. Find how his brothers help him.'),activity('grammar','Present Simple B · slides 1–17','grammar-b/#1','Practise do/does questions and short answers.'),activity('workbook','Workbook · page 4','files/unit2-workbook.pdf#page=4','Answer the reading questions and practise the question forms.')],
      timing=[(5,'Opening question'),(10,'Vocabulary preview and retrieval'),(15,'Read the email adaptation'),(20,'Do/does and short answers'),(17,'Workbook questions and answers'),(5,'Exit check')],
      check='Require a detail from Samuel’s route. Ask who helps, how they help and how far they travel.',
      support='Use a short answer first, then a full sentence. Keep the routine tied to the documentary period.',
      exit='Ask a clear question about Samuel’s journey and answer it.'),
 dict(title='Ask a partner about the journey', goal='Use question words and frequency words in a conversation.',
      prep=['Prepare two questions about a journey to school.', 'Think of something you usually do and something you sometimes do.'],
      activities=[activity('grammar','Present Simple B · slides 18–43','grammar-b/#18','Practise question words, frequency words and the pair conversation.'),activity('speaking','Writing sheet · Part B','worksheet.html','Ask a partner how they travel and what they do after school. Record the answers.'),activity('workbook','Workbook · page 4, Your turn','files/unit2-workbook.pdf#page=4','Answer Samuel’s question. Compare your journey with his.')],
      timing=[(7,'Recall the email'),(10,'Vocabulary preview and retrieval'),(18,'Question words and frequency'),(20,'Partner interview'),(12,'Report a partner’s routine'),(5,'Exit check')],
      check='Who, where, when and how must match the information requested. A subject question such as Who helps Samuel? does not take does.',
      support='Let students rehearse with prompts, then ask a new partner without the prompts.',
      exit='Write one question and one sentence about your partner.'),
 dict(title='Instagram from the islands: listen first', goal='Find the main idea and details in a recording.',
      prep=['Bring headphones if you will listen on your own.', 'Think about travelling across water. Keep the boat text closed until you listen.'],
      activities=[activity('listening','Listen First · the school boat','listening.html','Listen once for the main idea, then for details. Answer before opening the transcript.'),activity('message','The School Boat · Instagram','journey-boat.html','After listening, read Zoe and Isaac’s post and check your answers.'),activity('workbook','Workbook · page 5','files/unit2-workbook.pdf#page=5','Take notes and compare the boat journey with an earlier message.')],
      timing=[(5,'Predict the topic'),(10,'Vocabulary preview and retrieval'),(12,'Two listening passes and notes'),(15,'Independent listening answers'),(20,'Read, check and compare'),(10,'Feedback and exit check')],
      check='Look for another island, five minutes and walking after the boat trip. Sometimes does not mean always.',
      support='Replay the relevant part at the selected speed. Open the transcript only after an independent attempt.',
      exit='Give one similarity and one difference between two documented journeys.'),
 dict(title='Write a reply', goal='Write a relevant reply of 50–70 words.',
      prep=['Choose Carlito, Samuel, or Zoe and Isaac as your reader.', 'Plan an answer to the question at the end of that message.'],
      activities=[activity('messages','Choose a message to answer','companion-stories.html','Choose the WhatsApp message, email or Instagram post. Find the sender’s question.'),activity('practice','Words in Context · set 9','vocabulary/practice.html?set=8','Review meanings. Choose two suitable vocabulary entries for your reply.'),activity('writing','Workbook · page 6','files/unit2-workbook.pdf#page=6','Plan and write your reply. Include a negative, a frequency word and two vocabulary entries.')],
      timing=[(5,'Choose the reader and purpose'),(10,'Vocabulary preview and retrieval'),(10,'Plan a relevant reply'),(25,'Independent first draft'),(15,'Feedback and revision'),(7,'Exit check')],
      check='Assess whether the reply answers the sender’s question before checking grammar. Check meaning, detail, cohesion and independent use.',
      support='Offer a planning prompt when needed. Avoid giving a full model before the student writes.',
      exit='Improve two sentences after feedback and explain one change.'),
 dict(title='Review and use it independently', goal='Use the unit language without a visible model.',
      prep=['Review your feedback from Meeting 8.', 'Choose three vocabulary entries you want to use without help.'],
      activities=[activity('practice','Words in Context · set 11','vocabulary/practice.html?set=10','Review the final set. Explain your choices and write an original sentence.'),activity('compare','Compare two messages from memory','companion-stories.html','Keep the texts closed while you write one similarity and one difference. Open them to check afterwards.'),activity('writing','Workbook · page 6, new reply','files/unit2-workbook.pdf#page=6','Choose a different reader and write a new reply in your notebook without copying your first draft.')],
      timing=[(7,'Recall without a model'),(10,'Final vocabulary preview and retrieval'),(15,'Independent comparison'),(20,'New reply to a different reader'),(15,'Feedback and targeted correction'),(5,'Choose the next learning step')],
      check='Use the new reply and comparison as evidence. Completing a checklist or viewing 165 entries does not establish mastery.',
      support='Record the specific difficulty. Use the reserve meeting for a short targeted task, then reassess.',
      exit='Identify one skill you can now use and one you still need to practise.'),
]

def shell(title, body, script=True):
    return '<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | Unit 2</title><link rel="stylesheet" href="unit.css"><link rel="stylesheet" href="meetings.css"></head><body><main><header class="unit-header"><a class="home" href="../" aria-label="Grade 7">⌂</a><a href="./">Unit 2 · Meetings</a></header>'+body+'</main>'+('<script src="meetings.js"></script>' if script else '')+'</body></html>'

def open_link(label, href, identity, extra=''):
    return '<a class="activity-link '+extra+'" href="'+E(href,quote=True)+'" data-open-id="'+identity+'">'+E(label)+'</a><span class="opened-badge" data-open-status="'+identity+'" hidden>Opened</span>'

def build():
    # Retain the full resource catalogue; foundation calls this after generating it.
    hub=OUT/'index.html'
    if 'data-meeting-index' not in hub.read_text():
        (OUT/'resources.html').write_text(hub.read_text().replace('class="home" href="../"','class="home" href="./"'))
    words=json.loads((OUT/'vocabulary/entries.json').read_text())
    word_slides={};slide=2;previous=None
    for i,w in enumerate(words):
        if w['group']!=previous:slide+=1;previous=w['group']
        word_slides[w['id']]=slide+1;slide+=2
        if (i+1)%3==0:slide+=1
    meetings=[]
    for i,base in enumerate(MEETINGS):
        n=i+1;group=3+i//3;start=[1,19,37][i%3];end=[18,36,55][i%3]
        word=f'g{group:02}-{start:02}';url='vocabulary/full.html#slide-'+str(word_slides[word])
        m=dict(base,id=f'm{n}',number=n,group=group,start=start,end=end,guideSlide=1+i*3)
        m['activities']=[activity('vocab',f'Vocabulary · Group {group:02}, entries {start}–{end}',url,'Preview this batch. Choose three to five entries for active use; stop at the end of the stated range.')]+base['activities']
        assert sum(x[0] for x in m['timing'])==72
        meetings.append(m)
    (OUT/'meetings.json').write_text(json.dumps(meetings,ensure_ascii=False,indent=2)+'\n')
    body='<div data-meeting-index><p class="eyebrow">Grade 7 · Unit 2</p><h1>Meetings</h1><p class="unit-title">School Years Around the World</p><p>Nine meetings. Open an activity, then tick Completed when you have finished it.</p>'
    body+='<nav class="top-links" aria-label="Unit resources">'+open_link('Student preparation','student-preparation.html','unit-prep')+open_link('Teacher guide','meeting-guide.html','unit-guide')+'<a href="resources.html">All resources</a></nav>'
    body+='<section class="progress-panel" aria-label="My progress"><strong id="overall-progress">0 of 9 meetings completed</strong><progress id="overall-meter" max="9" value="0" aria-label="Completed meetings"></progress><button id="continue-meeting" type="button">Continue</button><p id="last-opened">No activity opened yet.</p></section>'
    body+='<p class="privacy-note">Your ticks and opened links stay only in this browser on this device. They are not sent to anyone or synced to another device. Clearing browser data removes them.</p><p id="save-status" class="save-status" role="status"></p><noscript><p>Links work without JavaScript. Turn on JavaScript to save your checkboxes on this device.</p></noscript>'
    body+='<div class="meeting-list">'
    for m in meetings:
        mid=m['id'];number=m['number'];guide='meeting-guide.html#'+str(m['guideSlide'])
        body+='<details class="meeting" id="'+mid+'" data-meeting="'+mid+'"><summary><span class="meeting-number">'+str(number)+'</span><span><span class="meeting-title">'+E(m['title'])+'</span><span class="meeting-summary" data-meeting-summary="'+mid+'">0 of 4 activities completed</span></span><span class="meeting-state" data-meeting-state="'+mid+'">Not started</span></summary><div class="meeting-body"><p class="goal">'+E(m['goal'])+'</p>'
        body+='<div class="meeting-links">'+open_link('Before this meeting','student-preparation.html#'+mid,mid+'-prep')+open_link('Teacher guide',guide,mid+'-guide')+'</div>'
        body+='<label class="meeting-complete"><input type="checkbox" data-complete-meeting="'+mid+'"> Mark this meeting completed</label><ul class="activity-list">'
        for a in m['activities']:
            aid=mid+'-'+a['key']
            body+='<li class="activity" data-activity="'+aid+'"><div>'+open_link(a['title'],a['href'],aid)+'<p>'+E(a['instruction'])+'</p></div><label class="completion"><input type="checkbox" data-complete="'+aid+'" aria-label="Completed: '+E(a['title'],quote=True)+'"> Completed</label></li>'
        body+='</ul></div></details>'
    body+='</div><p class="footnote">The order can be adjusted to your class. A meeting has up to 72 planned minutes, with time left for transitions and interruptions.</p></div>'
    hub.write_text(shell('Meetings',body))

    body='<p class="eyebrow">Grade 7 · Unit 2</p><h1>Student preparation</h1><p>Before each meeting, spend 5–10 minutes on the steps below. Bring your notebook and workbook.</p><p class="privacy-note">Your Ready ticks stay only in this browser on this device.</p><p id="save-status" class="save-status" role="status"></p><button class="print-button" onclick="window.print()">Print preparation sheet</button><details class="hebrew-help"><summary>Hebrew help</summary><p lang="he" dir="rtl">לפני כל מפגש הקדישו 5–10 דקות להכנה. הביאו מחברת ודף עבודה. אפשר לסמן Ready לאחר ההכנה; הסימון נשמר רק בדפדפן ובמכשיר שלכם.</p></details>'
    for m in meetings:
        mid=m['id'];group=m['group'];url=f'https://englishfornoar.co.il/band-ii/groups/group-{group:02}.html'
        body+='<section class="prep-card" id="'+mid+'"><p class="eyebrow">Meeting '+str(m['number'])+'</p><h2>'+E(m['title'])+'</h2><ol>'+''.join('<li>'+E(x)+'</li>' for x in m['prep'])+'<li>Preview five entries from the vocabulary batch below. Try to use one in a sentence.</li></ol><div class="meeting-links">'+open_link(f'Vocabulary · Group {group:02}, entries {m["start"]}–{m["end"]}',m['activities'][0]['href'],mid+'-prep-vocab')+'</div><p class="group-link"><a href="'+url+'">Open Group '+f'{group:02}'+'</a> <button type="button" data-copy="'+url+'">Copy group link</button><span class="copy-status" role="status"></span></p><label class="completion"><input type="checkbox" data-ready="'+mid+'"> Ready for Meeting '+str(m['number'])+'</label><p><a href="./#'+mid+'">Meeting '+str(m['number'])+' activities →</a></p></section>'
    (OUT/'student-preparation.html').write_text(shell('Student preparation',body))

    slides=[]
    for m in meetings:
        prefix='Meeting '+str(m['number'])+' · '
        prep='<ul>'+''.join('<li>'+E(x)+'</li>' for x in m['prep'])+'</ul>'
        slides.append(dict(title=prefix+m['title'],body='<p><strong>Goal:</strong> '+E(m['goal'])+'</p><p><strong>Before class:</strong></p>'+prep+'<p class="mini">Vocabulary: Group '+f'{m["group"]:02}'+f', entries {m["start"]}–{m["end"]}. Preview the batch; select only three to five entries for active use. Slow down when retrieval is weak.</p><p class="mini"><a href="student-preparation.html#'+m['id']+'">Student preparation</a> · <a href="./#'+m['id']+'">Meeting activities</a></p>'))
        timing='<ol class="timing-list">'+''.join('<li><strong>'+str(minutes)+' min</strong> · '+E(task)+'</li>' for minutes,task in m['timing'])+'</ol>'
        slides.append(dict(title=prefix+'72-minute teaching sequence',body=timing+'<p class="mini">Plan 72 active minutes in a double meeting. Keep the remaining time for transitions and interruptions. Select slides according to the class response.</p>'))
        slides.append(dict(title=prefix+'Evidence and next steps',body='<p><strong>Check:</strong> '+E(m['check'])+'</p><p><strong>Support:</strong> '+E(m['support'])+'</p><p><strong>Exit task:</strong> '+E(m['exit'])+'</p><p class="mini"><a href="workbook-key.html">Workbook answer key</a> · <a href="./#'+m['id']+'">Back to this meeting</a></p>'))
    (OUT/'meeting-guide-data.js').write_text('const TEACHER = '+json.dumps(slides,ensure_ascii=False)+';\n')
    template=(OUT/'teacher.html').read_text().replace('lang="he" dir="rtl"','lang="en" dir="ltr"').replace('Unit 2 · מדריך למורה','Unit 2 · Meeting guide').replace('teacher-data.js?v=unit2-draft1','meeting-guide-data.js').replace('teacher.js?v=unit2-draft1','meeting-guide.js').replace('בחירת שקף','Choose a slide').replace('השקף הקודם','Previous slide').replace('השקף הבא','Next slide').replace('כיתה ז׳','Grade 7').replace('</head>','<link rel="stylesheet" href="meetings.css"></head>')
    (OUT/'meeting-guide.html').write_text(template)
    engine=(OUT/'teacher.js').read_text().replace('Unit 2 · מדריך למורה','Unit 2 · Meeting guide')
    engine=engine.replace("+'</h1>'+S[i].body", "+'</h1><p class=\"mini\" lang=\"he\" dir=\"rtl\">נוצר: יום שלישי, י״א בתשרי תשפ״ז (22.9.2026)</p>'+S[i].body")
    (OUT/'meeting-guide.js').write_text(engine)
    print(json.dumps(dict(meetings=9,activities=sum(len(m['activities']) for m in meetings),teacher_slides=len(slides),vocabulary_records=len(words))))

if __name__=='__main__':build()
