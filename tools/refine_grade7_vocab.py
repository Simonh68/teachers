"""Small, auditable corrections to this lesson only; preserve all source entries."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'grade7/band2-groups-01-02'
entries=json.loads((OUT/'entries.json').read_text(encoding='utf-8'))
fixes={
 'g01-38':{'sentence':'This cloud looks like a ship.','translation':'הענן הזה נראה כמו ספינה.'},
 'g01-43':{'sentence':'Please bring my book back.','translation':'החזר בבקשה את הספר שלי.'},
 'g01-55':{'sentence':'We are able to read this book.','translation':'אנחנו מסוגלים לקרוא את הספר הזה.'},
 'g02-07':{'sentence':'Walking is good exercise.','translation':'הליכה היא פעילות גופנית טובה.'},
 'g02-20':{'translation':'הכובע הזה יתאים לה.'},
 'g02-31':{'translation':'אגיד להם ליצור איתך קשר.'},
 'g02-41':{'sentence':'I stayed home because I was ill.','translation':'נשארתי בבית כי הייתי חולה.'},
 'g02-44':{'translation':'לא היה לנו השבוע הרבה מזל.'},
 'g02-45':{'meaning':'להפעיל; לתפעל'},
 'g02-47':{'translation':'הילד הביא לי פרוסת פאי.'},
 'g02-48':{'sentence':'We are responsible for keeping the classroom clean.','translation':'אנחנו אחראים לשמור על הכיתה נקייה.'}
}
for e in entries:
    e.update(fixes.get(e['id'],{}))
assert len(entries)==110
(OUT/'entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'vocabulary-audit.txt').write_text('\n'.join(f"{e['id']} | {e['word']} | {e['meaning']} | {e['sentence']} | {e['translation']}" for e in entries)+'\n',encoding='utf-8')
page=ROOT/'index.html'
text=page.read_text(encoding='utf-8')
link='grade7/band2-groups-01-02/'
if link not in text:
    anchor='<div id="grade7">'
    assert text.count(anchor)==1, 'Grade 7 anchor changed; refusing broad overwrite'
    card='<a class="week-card reading-card" style="margin-bottom:24px" href="grade7/band2-groups-01-02/?v=20260916-full1"><div><span class="tag">כיתה ז׳ · מצגת מלאה · קריינות AI</span><h3 lang="en" dir="ltr">Band II · Groups 01–02</h3><p>110 ערכים, שני שקפים לכל ערך והתנחתא חזותית אחרי כל שלושה ערכים. אנגלית ותרגום במיקום קבוע, וקובצי אודיו מהאתר.</p></div><span class="arrow">←</span></a>'
    page.write_text(text.replace(anchor,anchor+card,1),encoding='utf-8')
css=OUT/'lesson.css'
text=css.read_text(encoding='utf-8')
if '/* Fixed break heading */' not in text:
    text+='\n/* Fixed break heading */\n.break-title{margin:0}.art-note{top:78px}@media(max-width:650px){.art-note{top:80px}}@media(max-height:510px){.art-note{top:49px}}\n'
    css.write_text(text,encoding='utf-8')
print('Preserved all 110 entries; aligned example translations; linked complete deck from Grade 7.')
