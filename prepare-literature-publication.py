from pathlib import Path
import base64
ROOT=Path(__file__).parent
decks=[('count-that-day-lost-revision','Count That Day Lost'),('the-road-not-taken-revision','The Road Not Taken')]
for rel in ['index.html','grade10/group-a/index.html','grade10/group-a/library/index.html']:
    path=ROOT/rel
    text=path.read_text()
    cards=[]
    for slug,title in decks:
        prefix='grade10/group-a/' if rel=='index.html' else '../' if 'library/' in rel else ''
        h='h3' if rel=='index.html' else 'h2'
        cards.append(f'<a class="material" href="{prefix}{slug}/"><div><span class="tag">כיתה י׳ · ספרות · חזרה אינטראקטיבית</span><{h} lang="en" dir="ltr">{title} · Bagrut Revision</{h}><p>48 שקפים · 20 שאלות עם שתי אפשרויות לבחירה ותשובות לדוגמה · רמת A2–B1 · מילות קישור והכנה לכתיבת תשובות.</p><div class="created"><b>נוצר:</b> יום ראשון, ל׳ בתשרי תשפ״ז (<time datetime="2026-10-11">11.10.2026</time>)</div></div><span class="arrow">←</span></a>')
    anchor='<div id="grade10" class="grade-panel list hidden">' if rel=='index.html' else '<section class="materials">'
    assert text.count(anchor)==1
    # Idempotent generator: refuse a duplicate insertion.
    if 'count-that-day-lost-revision/' not in text:
        text=text.replace(anchor,anchor+'\n'+'\n'.join(cards))
        path.write_text(text)

for slug,title in decks:
    folder=ROOT/'grade10/group-a'/slug
    out=folder/'files';out.mkdir(exist_ok=True)
    text=(folder/'index.html').read_text()
    text=text.replace('../../../shared/deck/','https://simonh68.github.io/teachers/shared/deck/')
    text=text.replace('href="../library/"','href="https://simonh68.github.io/teachers/grade10/group-a/library/"')
    original='count-that-day-lost' if slug.startswith('count') else 'the-road-not-taken-review'
    text=text.replace(f'href="../{original}/"',f'href="https://simonh68.github.io/teachers/grade10/group-a/{original}/"')
    image=base64.b64encode((folder/'assets/pause.svg').read_bytes()).decode()
    text=text.replace('src="assets/pause.svg"',f'src="data:image/svg+xml;base64,{image}"')
    text=text.replace('<script src="activity.js"></script>','<script>'+(folder/'activity.js').read_text()+'</script>')
    (out/(slug+'.html')).write_text(text)
print('Prepared 2 decks, 3 class entry points, and 2 portable downloads.')
