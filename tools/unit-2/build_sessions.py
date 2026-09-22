"""Build the dated meeting index, home review and HTML teacher guide."""
from pathlib import Path
from datetime import date
import json, html, re
from dated_meetings import MEETINGS

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'grade7/unit-2'
E = html.escape
VERSION = '20260922-dates1'
EXAM = '2026-11-12'

def label(iso):
    return date.fromisoformat(iso).strftime('%a %d %b %Y')

def shell(title, body):
    return '<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | Unit 2</title><link rel="stylesheet" href="unit.css"><link rel="stylesheet" href="meetings.css?v='+VERSION+'"></head><body><main><header class="unit-header"><a class="home" href="../" aria-label="Grade 7">⌂</a><a href="./">Unit 2 · Meetings</a></header>'+body+'</main><script src="meetings.js?v='+VERSION+'"></script></body></html>'

def open_link(title, href, identity):
    return '<a class="activity-link" href="'+E(href,quote=True)+'" data-open-id="'+identity+'">'+E(title)+'</a><span class="opened-badge" data-open-status="'+identity+'" hidden>Opened</span>'

def activity(identity, title, minutes, instruction, links):
    return dict(id=identity,title=title,minutes=minutes,instruction=instruction,links=[dict(title=t,href=u) for t,u in links])

def render_activity(a):
    links='<div class="activity-links">'+''.join('<span>'+open_link(l['title'],l['href'],a['id']+'-link-'+str(i))+'</span>' for i,l in enumerate(a['links']))+'</div>'
    groups=[int(match.group(1)) for l in a['links'] if (match:=re.match(r'Group (\d+)',l['title']))]
    if groups:links+='<details class="group-options"><summary>Group practice & copy links</summary>'+group_links(groups)+'</details>'
    return '<li class="activity" data-activity="'+a['id']+'"><div><h3>'+E(a['title'])+' <span class="duration">'+str(a['minutes'])+' min</span></h3><p>'+E(a['instruction'])+'</p>'+links+'</div><label class="completion"><input type="checkbox" data-complete="'+a['id']+'" aria-label="Completed: '+E(a['title'],quote=True)+'"> Completed</label></li>'

def ranges(words, word_slides):
    grouped=[]
    for w in words:
        n=int(w['id'].split('-')[1])
        if not grouped or grouped[-1]['group']!=w['group']:
            grouped.append(dict(group=w['group'],start=n,end=n,href='vocabulary/full.html#slide-'+str(word_slides[w['id']])))
        else:grouped[-1]['end']=n
    for g in grouped:g['title']=f'Group {g["group"]:02} · entries {g["start"]}–{g["end"]}'
    return grouped

def group_links(groups):
    out=''
    for g in sorted(set(groups)):
        url=f'https://englishfornoar.co.il/band-ii/groups/group-{g:02}.html'
        out+=f'<p class="group-link"><a href="{url}">Open Group {g:02}</a> <button type="button" data-copy="{url}">Copy group link</button><span class="copy-status" role="status"></span></p>'
    return out

def home_list(m):
    return '<ol class="activity-list">'+''.join(render_activity(a) for a in m['homeActivities'])+'</ol>'

def skills(m):
    return '<p class="skills"><strong>Skills:</strong> '+E(' · '.join(m['skills']))+'</p>'

def build():
    hub=OUT/'index.html'
    # The full resource catalogue is built by foundation; keep it before replacing the hub.
    if 'data-meeting-index' not in hub.read_text():
        (OUT/'resources.html').write_text(hub.read_text().replace('class="home" href="../"','class="home" href="./"'))
    words=json.loads((OUT/'vocabulary/entries.json').read_text())
    word_slides={};slide=2;previous=None
    for i,w in enumerate(words):
        if w['group']!=previous:slide+=1;previous=w['group']
        word_slides[w['id']]=slide+1;slide+=2
        if (i+1)%3==0:slide+=1
    meetings=[];offset=0
    for i,base in enumerate(MEETINGS):
        m=dict(base,number=i+1,id='d'+base['date'].replace('-',''),guideSlide=1+i*3)
        mid=m['id'];batch=words[offset:offset+m['count']]
        m['vocabularyIds']=[w['id'] for w in batch];m['ranges']=ranges(batch,word_slides)
        m['homeDue']=MEETINGS[i+1]['date'] if i+1<len(MEETINGS) else EXAM
        m['timing']=[(20,'Vocabulary: recall, introduce the assigned batch and use four to six entries'),(18,'Reading or listening: find evidence and compare'),(14,'Grammar: model, try and check'),(8,'Independent writing or speaking'),(4,'Exit check and home-review plan')]
        m['activities']=[
            activity(mid+'-vocab','Vocabulary · '+str(m['count'])+' entries',20,'Work through the stated ranges. Recall earlier words, then focus on four to six examples for active use. Review every assigned entry at home.',[(g['title'],g['href']) for g in m['ranges']]),
            activity(mid+'-reading','Read, listen and compare',18,m['reading_task'],m['reading']),
            activity(mid+'-grammar','Grammar in use',14,m['grammar_task'],[m['grammar']]),
            activity(mid+'-writing','Use it independently · includes exit check',12,m['writing_task'],m['writing'])]
        m['homeActivities']=[]
        for n in range(3):
            start=n*14;part=batch[start:min(start+14,len(batch))];rr=ranges(part,word_slides)
            absolute=offset+start+1;last=absolute+len(part)-1
            practice=f'vocabulary/practice.html?set={(absolute-1)//15}&item={absolute}&end={last}'
            extra,extra_href=m['home'][n]
            instruction=f'Review these {len(part)} entries: listen, cover the meaning and recall it. Practise context items {absolute}–{last}; stop at {last}. '+extra
            links=[(g['title'],g['href']) for g in rr]+[(f'Context practice · items {absolute}–{last}',practice),('Review task',extra_href)]
            workbook=re.search(r'workbook page (\d+)',extra,re.I)
            if workbook:
                page=workbook.group(1);url='files/unit2-workbook.pdf#page='+page
                if url!=extra_href:links.append(('Workbook · page '+page,url))
            a=activity(mid+'-home-'+str(n+1),'Home round '+str(n+1)+' · '+str(len(part))+' entries',15,instruction,links)
            a['vocabularyIds']=[w['id'] for w in part];a['firstItem']=absolute;a['lastItem']=last
            m['homeActivities'].append(a)
        assert sum(t[0] for t in m['timing'])==64
        assert sum(a['minutes'] for a in m['activities'])==64
        assert sum(a['minutes'] for a in m['homeActivities'])==45
        meetings.append(m);offset+=m['count']
    assert offset==165 and len(set(w for m in meetings for w in m['vocabularyIds']))==165
    (OUT/'meetings.json').write_text(json.dumps(meetings,ensure_ascii=False,indent=2)+'\n')
    total=len(meetings)
    body='<div data-meeting-index data-dated-plan><p class="eyebrow">Grade 7 · Unit 2</p><h1>Meetings by date</h1><p class="unit-title">School Years Around the World</p><p>Four double meetings · 12:00–13:20. Each meeting has 64 active minutes and 16 minutes for transitions and interruptions.</p><p class="schedule-note">Next exam: <time datetime="'+EXAM+'">'+label(EXAM)+'</time>. The school trip on 25 October and the exam day are excluded from these four meetings.</p>'
    body+='<nav class="top-links" aria-label="Unit resources">'+open_link('Preparation & home review','student-preparation.html','unit-prep')+open_link('Teacher guide','meeting-guide.html','unit-guide')+'<a href="resources.html">All resources</a></nav>'
    body+='<nav class="date-nav" aria-label="Meeting dates">'+''.join('<a href="#'+m['id']+'">'+label(m['date'])+'</a>' for m in meetings)+'</nav>'
    body+=f'<section class="progress-panel" aria-label="My progress"><strong id="overall-progress">0 of {total} meetings completed</strong><progress id="overall-meter" max="{total}" value="0" aria-label="Completed meetings"></progress><button id="continue-meeting" type="button">Continue</button><p id="last-opened">No activity opened yet.</p></section>'
    body+='<section class="history-controls" aria-label="Opened-link history"><div class="history-buttons"><button id="reset-history" type="button" aria-describedby="history-help" disabled>Reset history</button><button id="restore-history" type="button" aria-describedby="history-help" disabled>Restore history</button></div><p id="history-help">Clear or restore this unit’s Opened markers. Completed and Ready ticks stay saved.</p><p id="history-status" role="status">No cleared history to restore.</p></section>'
    body+='<p class="privacy-note">Your ticks and opened links stay only in this browser on this device. They are not sent to anyone or synced to another device. Clearing browser data removes them.</p><p id="save-status" class="save-status" role="status"></p><noscript><p>Links work without JavaScript. Turn on JavaScript to save your checkboxes on this device.</p></noscript><div class="meeting-list">'
    for m in meetings:
        mid=m['id'];day=label(m['date'])
        body+='<details class="meeting" id="'+mid+'" data-meeting="'+mid+'" data-number="'+str(m['number'])+'"><summary><span class="meeting-number">'+str(m['number'])+'</span><span><time class="meeting-date" datetime="'+m['date']+'">'+day+'</time><span class="meeting-title">'+E(m['title'])+'</span><span class="meeting-summary" data-meeting-summary>0 of 4 class activities completed</span></span><span class="meeting-state" data-meeting-state>Not started</span></summary><div class="meeting-body">'
        body+=skills(m)+'<p class="goal">'+E(m['goal'])+'</p><div class="meeting-links">'+open_link('Preparation & home review','student-preparation.html#'+mid,mid+'-prep')+open_link('Teacher guide','meeting-guide.html#'+str(m['guideSlide']),mid+'-guide')+'</div>'
        body+='<h2>In class · 64 active minutes</h2><label class="meeting-complete"><input type="checkbox" data-complete-meeting="'+mid+'"> Mark classwork completed</label><ol class="activity-list" data-classwork>'+''.join(render_activity(a) for a in m['activities'])+'</ol>'
        body+='<section data-homework><h2>At home · three 15-minute rounds</h2><p>Finish before <time datetime="'+m['homeDue']+'">'+label(m['homeDue'])+'</time>. Review the vocabulary taught in this meeting and complete the linked tasks.</p><p class="home-summary" data-home-summary>0 of 3 home rounds completed</p>'+home_list(m)+'</section></div></details>'
    body+='</div><p class="footnote">Vocabulary: 42, 41, 41 and 41 entries. All 165 entries in Groups 03–05 are included. Each meeting has the same class time and the same home-review time.</p><p class="footnote"><a href="earlier-meetings.html">Earlier checklist and saved ticks</a></p></div>'
    hub.write_text(shell('Meetings by date',body))
    body='<p class="eyebrow">Grade 7 · Unit 2</p><h1>Preparation & home review</h1><p>Before class: bring your notebook and prepare the short prompt. After class: complete three 15-minute review rounds before the next date.</p><p class="privacy-note">Your Ready and Completed ticks stay only in this browser on this device.</p><p id="save-status" class="save-status" role="status"></p><button class="print-button" onclick="window.print()">Print preparation sheet</button><details class="hebrew-help"><summary>Hebrew help</summary><p lang="he" dir="rtl">לפני המפגש מביאים את הציוד ומכינים את שאלת הפתיחה. לאחריו חוזרים בבית על אוצר המילים ועל החומר שנלמד בשלושה סבבים קצרים. לכל תאריך יש קישורים מדויקים. הסימונים נשמרים רק בדפדפן ובמכשיר שלכם.</p></details>'
    for m in meetings:
        mid=m['id']
        body+='<section class="prep-card" id="'+mid+'" data-prep-meeting="'+mid+'" data-number="'+str(m['number'])+'"><p class="eyebrow">Meeting '+str(m['number'])+' · <time datetime="'+m['date']+'">'+label(m['date'])+'</time></p><h2>'+E(m['title'])+'</h2>'+skills(m)+'<h3>Before class · 2 minutes</h3><ul>'+''.join('<li>'+E(t)+'</li>' for t in m['prep'])+'</ul><label class="completion"><input type="checkbox" data-ready="'+mid+'"> Ready for this meeting</label><h3>After class · before '+label(m['homeDue'])+'</h3>'+home_list(m)+group_links(g['group'] for g in m['ranges'])+'<p><a href="./#'+mid+'">Open class activities for '+label(m['date'])+' →</a></p></section>'
    (OUT/'student-preparation.html').write_text(shell('Preparation & home review',body))
    slides=[]
    for m in meetings:
        prefix='Meeting '+str(m['number'])+' · '+label(m['date'])+' · '
        ranges_text='; '.join(g['title'] for g in m['ranges'])
        slides.append(dict(title=prefix+m['title'],body='<p><strong>Goal:</strong> '+E(m['goal'])+'</p>'+skills(m)+'<p><strong>Vocabulary:</strong> '+E(ranges_text)+'. '+str(m['count'])+' entries. Introduce the complete batch in 20 minutes; focus on four to six entries for active use. All entries return in three home rounds.</p><p class="mini">Before class: '+E(' '.join(m['prep']))+'</p><p class="mini"><a href="./#'+m['id']+'">Dated classwork and home links</a></p>'))
        timing='<ol class="timing-list">'+''.join('<li><strong>'+str(minutes)+' min</strong> · '+E(task)+'</li>' for minutes,task in m['timing'])+'</ol>'
        slides.append(dict(title=prefix+'64-minute teaching sequence',body=timing+'<p class="mini">Scheduled class: 12:00–13:20 (80 minutes). Keep 16 minutes for transitions and interruptions. The writing block includes an independent attempt before feedback. Use the indexed grammar examples; remaining practice returns at home.</p>'))
        slides.append(dict(title=prefix+'Check and review at home',body='<p><strong>Check:</strong> '+E(m['check'])+'</p><p><strong>Support:</strong> '+E(m['support'])+'</p><p><strong>Exit:</strong> '+E(m['exit'])+'</p><p><strong>At home:</strong> three 15-minute rounds; vocabulary batches of '+', '.join(str(len(a['vocabularyIds'])) for a in m['homeActivities'])+' entries, with linked reading, grammar and writing. Due before '+label(m['homeDue'])+'.</p><p class="mini"><a href="student-preparation.html#'+m['id']+'">Exact home-review links</a> · <a href="workbook-key.html">Workbook answer key</a></p>'))
    (OUT/'meeting-guide-data.js').write_text('const TEACHER = '+json.dumps(slides,ensure_ascii=False)+';\n')
    template=(OUT/'teacher.html').read_text().replace('lang="he" dir="rtl"','lang="en" dir="ltr"').replace('Unit 2 · מדריך למורה','Unit 2 · Meeting guide').replace('teacher-data.js?v=unit2-draft1','meeting-guide-data.js?v='+VERSION).replace('teacher.js?v=unit2-draft1','meeting-guide.js?v='+VERSION).replace('בחירת שקף','Choose a slide').replace('השקף הקודם','Previous slide').replace('השקף הבא','Next slide').replace('כיתה ז׳','Grade 7').replace('</head>','<link rel="stylesheet" href="meetings.css?v='+VERSION+'"></head>')
    (OUT/'meeting-guide.html').write_text(template)
    engine=(OUT/'teacher.js').read_text().replace('Unit 2 · מדריך למורה','Unit 2 · Meeting guide')
    engine=engine.replace("+'</h1>'+S[i].body", "+'</h1><p class=\"mini\" lang=\"he\" dir=\"rtl\">נוצר: יום שלישי, י״א בתשרי תשפ״ז (22.9.2026)</p>'+S[i].body")
    (OUT/'meeting-guide.js').write_text(engine)
    print(json.dumps(dict(meetings=total,dates=[m['date'] for m in meetings],class_minutes=64,home_minutes=45,teacher_slides=len(slides),vocabulary_counts=[m['count'] for m in meetings])))

if __name__=='__main__':build()
