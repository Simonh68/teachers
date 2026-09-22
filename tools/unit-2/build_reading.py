"""Compile canonical texts into short pages, paired sentences and contextual glosses."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'grade7/unit-2';DEST=OUT/'reading';DEST.mkdir(exist_ok=True)
D=json.loads((OUT/'content.json').read_text())
GLOSS='''a|מילת יידוע לא־מסוים: אחד או אחת
about|בערך
according|לפי (בביטוי according to)
after|אחרי
alaska|אלסקה
all|כולם
almost|כמעט
along|לאורך
also|גם
always|תמיד
anchorage|אנקורג׳
and|ו־
approximately|בערך
april|אפריל
are|פועל קישור ברבים בהווה
argentina|ארגנטינה
arrives|מגיעה
at|ב־
august|אוגוסט
barcelona|ברצלונה
become|להיות; להפוך ל־
before|לפני
begin|מתחילים
bike|אופניים
boat|סירה
book|ספר
break|חופשה
brings|מביא
brothers|אחים
bryher|ברייר, אי באנגליה
bus|אוטובוס
busy|עמוס
calendar|לוח שנה
calendars|לוחות שנה
called|נקרא
can|יכול; יכולה
cannot|אינו יכול; אינה יכולה
carlito|קרליטו
chair|כיסא; כאן כיסא גלגלים
children|ילדים
chiverito|צ׳יבריטו, שם הסוס
class|כיתה
clear|לפנות
company|חברה; נוכחות של אחרים
couch|ספה
country|מדינה
crossing|חצייה; לחצות
dangerous|מסוכן; מסוכנים
day|יום
days|ימים
different|שונה; שונים
difficult|קשה
does|פועל עזר בשאלה בהווה לגוף שלישי יחיד
dolphins|דולפינים
driveway|שביל הגישה לבית
earn|להרוויח
eight|שמונה
eighteen|שמונה־עשר
eleven|אחד־עשר
end|סוף
ends|מסתיימת
english|אנגלית
even|אפילו; גם
event|אירוע
every|כל
example|דוגמה
examples|דוגמאות
extra|נוספים
families|משפחות
finds|מוצאת; כאן חווה את הלמידה כקשה יותר
finishes|מסיימת
five|חמש
five-year-old|בן חמש
florida|פלורידה
follow|פועלים לפי
for|בשביל; למשך
four|ארבעה
friday|יום שישי
fridays|ימי שישי
from|מ־
full|מלא
get|להגיע, בביטוי get to
gives|נותן; מספק
go|הולכים; ללכת
goes|הולכת
going|הליכה; הגעה
grade|כיתה
group|קבוצה
harder|קשה יותר
has|יש לו או לה
have|יש להם
he|הוא
help|עוזרים
her|שלה
him|לו; אותו
his|שלו
holiday|חופשה
home|בית
horse|סוס
in|ב־
includes|כולל
india|הודו
individual|כל אחד בנפרד
is|פועל קישור ביחיד בהווה
isaac|אייזק
island|אי
it|הוא או היא, לדבר שאינו אדם
its|שלו או שלה, לדבר שאינו אדם
japan|יפן
jersey|ג׳רזי
join|מצטרפות
journey|דרך; מסע; נסיעה
july|יולי
june|יוני
kali|קאלי
kent|קנט, מחוז באנגליה
kilometres|קילומטרים
language|שפה
lasts|נמשכת
late|סוף החודש
learning|למידה
little|קטנה
live|גרים
lives|גר
long|ארוכה
main|עיקרית
make|להפוך; לעשות
makes|הופכת
many|רבים
march|מרץ
matter|חשובים; משפיעים
may|מאי
means|פירושה; משמעותה
meet|פוגשים
miami-dade|מיאמי־דייד
micaela|מיקאלה
middle|אמצע
minutes|דקות
misses|מתגעגעת
money|כסף
more|יותר
morning|בוקר
mother|אֵם
mountains|הרים
nearby|סמוך; קרוב
nearly|כמעט
new|חדשה
next|הבאה
no|לא
not|לא
november|נובמבר
of|של
on|ב־; על
one|אחד; אחת
online|באינטרנט; מרחוק
only|רק
or|או
other|אחרים
outside|החוצה
own|משלו; משלה
palm|דקל
parents|הורים
part|חלק
patagonia|פטגוניה
place|מקום
police|משטרה
protect|להגן
public|ציבוריים
pull|מושכים
push|דוחפים
reads|מקריא
regular|קבועה
return|חוזרים
ride|רוכבים; רכיבה
rides|רוכב או רוכבת
rivers|נהרות
road|כביש
roads|כבישים
route|מסלול
routine|שגרה
runs|נמשך, כאן על לוח השנה
same|אותו; אותה
samuel|סמואל
sand|חול
school|בית ספר; לימודים בתוך ביטוי
schools|בתי ספר
sea|ים
season|עונה
see|רואים
september|ספטמבר
seven|שבעה
she|היא
sister|אחות
six|שישה
small|קטן
snow|שלג
snowstorm|סופת שלג
snowy|מושלג
some|חלק; כמה
sometimes|לפעמים
son|בן
spring|אביב
start|להתחיל
starts|מתחילה
stops|תחנות; עוצרת
story|סיפור
students|תלמידים
summer|קיץ
takes|נמשכת; אורכת
teacher|מורה
teacher-training|הכשרת מורים
ten|עשרה
than|מ־, בהשוואה
the|ה־, ה״א הידיעה
their|שלהם
them|אותם; להם
these|האלה
they|הם; הן
this|הזה; הזאת
through|דרך
to|ל־; לפני פועל מסמן שם פועל
today|היום
together|יחד
too|גם
training|הכשרה
trees|עצים
tresco|טרסקו, אי באנגליה
twenty-five|עשרים וחמש
two|שניים
uae|איחוד האמירויות הערביות
uses|משתמש
vacation|חופשה
vet|וטרינר; רופא חיות
walk|הולכים ברגל
wants|רוצה
way|דרך
weather|מזג האוויר
weeks|שבועות
wheelchair|כיסא גלגלים
where|שבו; שבה
with|עם
year|שנה
younger|צעירים יותר
zoe|זואי'''
gloss=dict(line.split('|',1) for line in GLOSS.splitlines())
numbers={'13':'שלושה־עשר','2':'שניים','20':'עשרים','2023':'שנת 2023','2026':'שנת 2026','2026–27':'שנת הלימודים 2026–2027','2027':'שנת 2027','28':'עשרים ושמונה','3':'שלושה','30':'שלושים','31':'שלושים ואחד','7':'שבע','9':'תשעה'}
gloss.update(numbers)
gloss.update(dict(line.split('|',1) for line in '''1|אחד: היום הראשון בחודש
am|פועל קישור עם I בהווה
around|בסביבות; מסביב
autumn|סתיו
bad|גרוע
be|להיות
both|שניהם; שתיהן
change|להשתנות
come|באים
comes|מגיעה; חלה
cross|חוצים
dates|תאריכים
do|פועל עזר לשאלה בהווה
during|במהלך
early|בתחילת; מוקדם
england|אנגליה
everywhere|בכל מקום
hello|שלום
hi|שלום; היי
holidays|חופשות
how|איך
i|אני
include|כוללות
lengths|אורכים
let|תנו; כאן בביטוי בואו
look|נביט; להסתכל
me|אותי; לי
months|חודשים
nine|תשעה
my|שלי
near|ליד; קרוב ל־
our|שלנו
rules|כללים
short|קצרות
states|מדינות בארצות הברית
then|אחר כך
trip|נסיעה; כאן שיט
us|ארצות הברית (US); או לנו (us)
usa|ארצות הברית
usually|בדרך כלל
want|רוצה
water|מים
we|אנחנו
who|מי
world|עולם
you|אתם; אתן
your|שלכם; שלכן'''.splitlines()))
PHRASES={
 'school year':'שנת לימודים','school calendars':'לוחות לימודים','school calendar':'לוח לימודים','summer vacation':'חופשת קיץ','summer holiday':'חופשת קיץ','summer break':'חופשת קיץ','in the middle of':'באמצע','according to':'לפי','a little more than':'מעט יותר מ־','teacher training':'הכשרת מורים','at many schools':'בבתי ספר רבים','the end of':'סוף','go to school':'ללכת לבית הספר','get to school':'להגיע לבית הספר','rides a horse':'רוכב על סוס','is called':'נקרא','along the way':'לאורך הדרך','palm trees':'עצי דקל','school routine':'שגרת בית הספר','make this long journey':'עושים את הדרך הארוכה הזאת','every morning':'בכל בוקר','on fridays':'בימי שישי','bike bus':'אוטובוס אופניים: קבוצה הרוכבת יחד','on the way to school':'בדרך לבית הספר','school day':'יום לימודים','online learning':'למידה מרחוק','at the place':'במקום','goes outside':'יוצאת החוצה','clear snow':'לפנות שלג','earn some money':'להרוויח קצת כסף','the other children':'הילדים האחרים','where english':'שבו אנגלית','grade 7':'כיתה ז׳'
}
# Context help is tied to sentence text so revisions cannot shift a gloss to another sentence.
PHRASES.update({'let us':'בואו', 'around the world':'סביב העולם', 'school years':'שנות לימודים', 'school days':'ימי לימודים', 'from school to school':'מבית ספר לבית ספר', 'late summer':'סוף הקיץ', 'late spring':'סוף האביב', 'early summer':'תחילת הקיץ', 'early autumn':'תחילת הסתיו', 'with me':'איתי', 'our boat trip':'השיט שלנו', 'on your way to school':'בדרך שלכם לבית הספר'})
OVERRIDES={
 ('Let us look around the world.','us'):'כאן בביטוי let us: בואו',
 ('In Japan, the year goes from one spring to the next, with holidays along the way.','goes'):'נמשכת',
 ('It comes during the school year, from late July to the end of August.','it'):'היא: חופשת הקיץ',
 ('It ends in late spring, in May.','it'):'הם: הלימודים',
 ('It ends in early summer, in early June.','it'):'הם: הלימודים',
 ('It ends in summer, in late July.','it'):'היא: שנת הלימודים',
 ('It ends in summer, around July 1.','it'):'היא: שנת הלימודים',
 ('It ends in summer, in July.','it'):'היא: שנת הלימודים',
 ('In Kent, it runs for about eleven months.','it'):'היא: שנת הלימודים',
 ('Bad weather can make the journey difficult.','make'):'להפוך את הדרך לקשה',
 ('They push and pull my chair for four kilometres.','for'):'לאורך',
 ('We make this long journey together.','make'):'עושים את הדרך',
 ('Our school is on Tresco, a nearby island.','on'):'באי',
 ('Every morning, we meet the other children where the boat stops.','stops'):'עוצרת',
 ('Our boat trip takes five minutes.','takes'):'נמשך',
 ('Who goes to school with you?','goes'):'הולך או הולכת'
}
def clean(s):return re.sub(r'^[^\w]+|[^\w]+$','',s).lower()
def split(s):return [x.strip() for x in re.findall(r'.+?(?:[.!?](?=\s|$)|$)',s) if x.strip()]
sentences=[];texts=[]
main_sections=[]
for j,(title,en,he) in enumerate(D['main']):
    ens,hes=split(en),split(he)
    assert len(ens)==len(hes),(title,len(ens),len(hes))
    main_sections.append((title,list(zip(ens,hes))))
main=dict(id='school-calendars',title='School Years Around the World',period='General seasonal patterns; local dates vary',sources=list(dict.fromkeys(u for c in D['calendar'] for u in c['sources'])),sections=main_sections,questions=[
 ['Why does Japan give a different example?','Its summer vacation is inside the school year.'],
 ['Do all schools in the USA follow one calendar?','No. Anchorage and Miami-Dade have different dates.'],
 ['Which example has a summer break of about eleven weeks?','Anchorage, Alaska.'],
 ['When does the school year usually start in Kent?','In early autumn, around September 1.']])
alltexts=[main]
for i,s in enumerate(D['stories']):
    ens,hes=split(s['en']),split(s['he']);assert len(ens)==len(hes)
    alltexts.append(dict(id=s['id'],title=s['channel']+': '+s['title'],period=s['channel']+' · '+s['sender']+' · '+s['region']+' · Classroom adaptation',sources=[s['source']],sections=[(s['title'],list(zip(ens,hes)))],questions=s['questions'],photo=s.get('photo'),messageStyle=s['messageStyle'],sourcePeriod=s['period']))
for t in alltexts:
    text=dict(id=t['id'],title=t['title'],period=t['period'],sources=t['sources'],questions=t['questions'],ids=[],pages=[],photo=t.get('photo'),messageStyle=t.get('messageStyle'),sourcePeriod=t.get('sourcePeriod'))
    for heading,pairs in t['sections']:
        page=[];wc=0
        for en,he in pairs:
            n=len(sentences);tokens=en.split();words=[]
            for token in tokens:
                k=clean(token);assert k in gloss,(n,token)
                words.append(dict(word=token,he=OVERRIDES.get((en,k),gloss[k])))
            units=[];cursor=0
            while cursor<len(words):
                match=None
                for phrase,meaning in sorted(PHRASES.items(),key=lambda x:-len(x[0])):
                    keys=phrase.split();span=words[cursor:cursor+len(keys)]
                    if [clean(w['word']) for w in span]==keys:match=(len(keys),meaning);break
                length,meaning=match or (1,words[cursor]['he'])
                if match:
                    for w in words[cursor:cursor+length]:
                        if clean(w['word']) in ['to','of','in','on','at']:w['he']='חלק מהביטוי: '+meaning
                        else:w['he']+=' · בביטוי: '+meaning
                units.append(dict(start=cursor,end=cursor+length,he=meaning));cursor+=length
            sentences.append(dict(id=n,textId=t['id'],en=en,he=he,heading=heading,words=words,units=units))
            text['ids'].append(n)
            if page and wc+len(tokens)>26:text['pages'].append(dict(title=heading,ids=page));page=[];wc=0
            page.append(n);wc+=len(tokens)
        if page:text['pages'].append(dict(title=heading,ids=page))
    texts.append(text)
old={}
if (DEST/'content.json').exists():old=json.loads((DEST/'content.json').read_text())
for s in sentences:
    previous=next((o for o in old.get('sentences',[]) if o['textId']==s['textId'] and o['en']==s['en']),{})
    for k in ['audio','start','end','timings']:
        if k in previous:s[k]=previous[k]
for t in texts:
    previous=next((o for o in old.get('texts',[]) if o['id']==t['id']),{})
    if all('audio' in sentences[i] for i in t['ids']):
        for k in ['audio','sha256']:
            if k in previous:t[k]=previous[k]
data=dict(title='School Days Around the World',texts=texts,sentences=sentences,wordCount=sum(len(s['words']) for s in sentences),source='Unit 2 canonical main text and three classroom messages based on documented journeys')
(DEST/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(DEST/'data.js').write_text('window.READING = '+json.dumps(data,ensure_ascii=False)+';\n')
print(json.dumps(dict(texts=len(texts),sentences=len(sentences),words=data['wordCount'],pages=sum(len(t['pages']) for t in texts)),ensure_ascii=False))
