#!/usr/bin/env python3
"""Grade 8 Tilly Smith story CONTENT ADAPTER for the existing READ ALONG engine.
Generates recorded WAV phrases, phrase metadata, alignment metadata and story data.
Does not modify the reader or player; output is compatible with existing runtime.
"""
import array,json,os,re,subprocess,wave,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ROWS=json.loads("[{\"en\":[\"In December 2004, a ten-year-old girl named Tilly Smith went on vacation with her family to Thailand.\",\"בדצמבר 2004 ילדה בת עשר בשם טילי סמית נסעה עם משפחתה לחופשה בתאילנד.\",\"One morning, they went to the beach.\",\"בוקר אחד הם הלכו לחוף הים.\",\"The weather was beautiful, but Tilly saw something strange.\",\"מזג האוויר היה יפה, אבל טילי ראתה משהו מוזר.\",\"The water in the sea was moving in an unusual way.\",\"המים בים נעו בצורה לא רגילה.\"],\"p\":1},{\"en\":[\"Tilly remembered a lesson from school.\",\"טילי נזכרה בשיעור מבית הספר.\",\"Her teacher showed the class a video about tsunamis.\",\"המורה שלה הראה לכיתה סרטון על גלי צונאמי.\",\"She learned that strange changes in the sea could mean danger.\",\"היא למדה ששינויים מוזרים בים עלולים להעיד על סכנה.\",\"“We must leave the beach now!” she shouted.\",\"״אנחנו חייבים לעזוב את החוף עכשיו!״ היא צעקה.\",\"Her parents listened to her and told the hotel workers.\",\"הוריה הקשיבו לה וסיפרו לעובדי המלון.\",\"The workers helped people leave the beach.\",\"העובדים עזרו לאנשים לעזוב את החוף.\"],\"p\":2},{\"en\":[\"A few minutes later, a huge tsunami reached the beach.\",\"כעבור כמה דקות צונאמי עצום הגיע אל החוף.\",\"The people were already in a safe place.\",\"האנשים כבר היו במקום בטוח.\",\"Tilly's warning helped save about 100 lives.\",\"האזהרה של טילי עזרה להציל כמאה אנשים.\",\"She became famous, but she was just a young girl who remembered her teacher's lesson.\",\"היא התפרסמה, אבל הייתה רק ילדה צעירה שזכרה את השיעור של המורה שלה.\",\"Her story shows that children can save lives too.\",\"הסיפור שלה מראה שגם ילדים יכולים להציל חיים.\"],\"p\":3}]")
ROWS=[{"en":row["en"][i],"he":row["en"][i+1],"p":row["p"]} for row in ROWS for i in range(0,len(row["en"]),2)]
RATE=22050
def audio(text):
    out=subprocess.run(["espeak","-v","en-us","-s","142","-a","170","--stdout",text],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
    import io
    with wave.open(io.BytesIO(out),'rb') as w:
        raw=w.readframes(w.getnframes());channels=w.getnchannels();swidth=w.getsampwidth();rate=w.getframerate()
    if channels!=1 or swidth!=2 or rate!=RATE: raise RuntimeError((channels,swidth,rate))
    return raw
def write_wav(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(raw)
story=[];phrases=[];align={}
for index,row in enumerate(ROWS):
    en=row["en"];he=row["he"];num=index+1
    matches=list(re.finditer(r"\S+",en))
    if not matches:continue
    tokens=[]
    groups=[]
    # Natural 3-6 word phrases, no added visible punctuation or movement.
    word_groups=[];group=[]
    for j,m in enumerate(matches):
        group.append(j)
        if (len(group)>=5 or en[m.end()-1] in ',;:!?') and j<len(matches)-1:
            word_groups.append(group);group=[]
    if group:word_groups.append(group)
    raw_fragments=[];time_base=0;parts=[]
    for pi,gg in enumerate(word_groups):
        left=matches[gg[0]].start();right=matches[gg[-1]].end()
        piece=en[left:right]
        raw=audio(piece)
        duration=len(raw)/(2*RATE)
        raw_fragments.append(raw)
        # Approximate internal word boundaries by weighted pronunciation length;
        # phrase boundaries are exact from the WAV recordings.
        weights=[max(1.8,len(re.sub('[^a-zA-Z]','',matches[j].group()))**0.72) for j in gg]
        total=sum(weights);elapsed=0
        for j,weight in zip(gg,weights):
            m=matches[j];start=time_base+duration*elapsed/total;elapsed+=weight
            end=time_base+duration*elapsed/total
            while len(tokens)<=j:tokens.append(None)
            clean=m.group().strip('.,!?“”"')
            gloss={"strange":"מוזר","beach":"חוף","vacation":"חופשה","tsunami":"צונאמי","tsunamis":"גלי צונאמי","danger":"סכנה","saved":"הצילה","save":"להציל","warning":"אזהרה","teacher":"מורה","lesson":"שיעור","huge":"עצום","safe":"בטוח","people":"אנשים","remembered":"נזכרה","water":"מים","sea":"ים","shouted":"צעקה","famous":"מפורסמת","children":"ילדים","workers":"עובדים","moving":"נעים","unusual":"יוצא דופן","listened":"הקשיבו","hotel":"מלון","learned":"למדה","family":"משפחה","parents":"הורים"}.get(clean.lower(),clean)
            tokens[j]={"text":m.group(),"he":gloss,"startChar":m.start(),"endChar":m.end(),"start":round(start,5),"end":round(end,5)}
        part_path=ROOT/"audio"/f"story-{num:02d}-part-{pi+1:02d}.wav"
        write_wav(part_path,raw)
        parts.append({"index":pi,"firstToken":gg[0],"lastToken":gg[-1],"startChar":left,"endChar":right,"sourceStart":round(time_base,5),"sourceEnd":round(time_base+duration,5),"duration":round(duration,5),"text":piece,"src":str(part_path.relative_to(ROOT))})
        time_base+=duration
    he_matches=list(re.finditer(r"\S+",he))
    units=[{"indices":[],"text":m.group(),"start":m.start(),"end":m.end()} for m in he_matches]
    mapping=[min(len(units)-1,math.floor(j*len(units)/len(tokens))) for j in range(len(tokens))]
    for j,k in enumerate(mapping):units[k]["indices"].append(j)
    align[str(num)]={"plain":en,"he":he,"map":mapping,"units":units}
    story.append({"number":num,"paragraph":row["p"],"plain":en,"he":he,"tokens":tokens})
    phrases.append({"number":num,"duration":round(time_base,5),"parts":parts})
pages=[list(range(0,4)),list(range(4,10)),list(range(10,15))]
# Runtime expects indexes and exact consistency with the original Grade 8 engine.
(ROOT/"unit-data.js").write_text("window.UNIT_DATA="+json.dumps({"story":story,"pages":pages},ensure_ascii=False,separators=(',',':'))+";",encoding="utf-8")
(ROOT/"alignment.js").write_text("window.GRADE8_ALIGNMENT="+json.dumps(align,ensure_ascii=False,separators=(',',':'))+";",encoding="utf-8")
(ROOT/"phrase-data.js").write_text("window.GRADE8_PHRASES="+json.dumps({"pauseMs":1500,"sentences":phrases},ensure_ascii=False,separators=(',',':'))+";",encoding="utf-8")
print(f"Generated {len(story)} recorded sentences, {sum(len(x['parts']) for x in phrases)} recorded phrases and aligned tokens")
