#!/usr/bin/env python3
"""Grade 9 George story CONTENT ADAPTER for the existing READ ALONG engine.
Generates recorded WAV phrases, phrase metadata, alignment metadata and story data.
Does not modify the reader or player; output is compatible with existing runtime.
"""
import array,json,os,re,subprocess,wave,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ROWS=[{"en":"Imagine walking into your classroom and feeling that nobody really understands you.","he":"דמיינו שאתם נכנסים לכיתה ומרגישים שאף אחד לא באמת מבין אתכם.","p":1},{"en":"That's how George, a nine-year-old boy from the USA, sometimes felt.","he":"כך הרגיש לפעמים ג'ורג', ילד בן תשע מארצות הברית.","p":1},{"en":"He loved video games, music, and having fun, just like his classmates.","he":"הוא אהב משחקי מחשב, מוזיקה וליהנות, בדיוק כמו חבריו לכיתה.","p":1},{"en":"But George had autism, and his brain worked a little differently.","he":"אבל ג'ורג' היה אוטיסט, והמוח שלו פעל קצת אחרת.","p":1},{"en":"One day, he decided to do something brave: make a video to show his classmates what life was like for him.","he":"יום אחד הוא החליט לעשות מעשה אמיץ: ליצור סרטון שיראה לחבריו לכיתה איך נראים החיים מנקודת מבטו.","p":1},{"en":"Imagine hearing every sound in the classroom at once.","he":"דמיינו שאתם שומעים כל צליל בכיתה בבת אחת.","p":2},{"en":"For George, even normal sounds could feel too loud.","he":"בשביל ג'ורג', גם צלילים רגילים יכלו להישמע חזקים מדי.","p":2},{"en":"Sometimes, he needed extra time to answer a question.","he":"לפעמים הוא היה זקוק לזמן נוסף כדי לענות על שאלה.","p":2},{"en":"Other times, he looked away when someone spoke to him.","he":"בפעמים אחרות הוא הסיט את מבטו כשמישהו דיבר אליו.","p":2},{"en":"People might think he wasn't listening, but they were wrong.","he":"אנשים יכלו לחשוב שהוא לא מקשיב, אבל הם טעו.","p":2},{"en":"George was listening.","he":"ג'ורג' הקשיב.","p":2},{"en":"He just experienced things differently.","he":"הוא פשוט חווה דברים בדרך שונה.","p":2},{"en":"George didn't want people to feel sorry for him.","he":"ג'ורג' לא רצה שאנשים ירחמו עליו.","p":3},{"en":"He wanted something much simpler: friends who understood him.","he":"הוא רצה דבר פשוט בהרבה: חברים שיבינו אותו.","p":3},{"en":"Sometimes, he liked being alone, but he also wanted to laugh, play, and have fun with other kids.","he":"לפעמים אהב להיות לבד, אבל הוא גם רצה לצחוק, לשחק וליהנות עם ילדים אחרים.","p":3},{"en":"His message was clear: I'm a kid just like you.","he":"המסר שלו היה ברור: אני ילד בדיוק כמוכם.","p":3},{"en":"Being different didn't mean he had nothing in common with his classmates.","he":"העובדה שהוא שונה לא אמרה שאין לו דברים משותפים עם חבריו לכיתה.","p":3},{"en":"George made the video for just 21 classmates.","he":"ג'ורג' הכין את הסרטון רק עבור 21 חברים לכיתה.","p":4},{"en":"But then something amazing happened.","he":"אבל אז קרה דבר מדהים.","p":4},{"en":"His mother shared it online, and the video spread around the world.","he":"אמו שיתפה אותו באינטרנט, והסרטון התפשט ברחבי העולם.","p":4},{"en":"Thousands of people watched it.","he":"אלפי אנשים צפו בו.","p":4},{"en":"A small video became a big message.","he":"סרטון קטן הפך למסר גדול.","p":4},{"en":"George showed everyone that sometimes, the best way to change how people see you is to help them see the world through your eyes.","he":"ג'ורג' הראה לכולם שלפעמים הדרך הטובה ביותר לשנות את הדרך שבה אנשים רואים אותך היא לעזור להם לראות את העולם דרך העיניים שלך.","p":4}]
GLOSS={
"imagine":"דמיינו","walking":"הולכים","into":"לתוך","your":"שלכם","classroom":"כיתה","and":"ו־","feeling":"מרגישים","that":"ש־","nobody":"אף אחד","really":"באמת","understands":"מבין","you":"אתכם","that's":"כך","how":"איך","george":"ג'ורג'","a":"אחד / א־","nine-year-old":"בן תשע","boy":"ילד","from":"מ־","the":"ה־","usa":"ארצות הברית","sometimes":"לפעמים","felt":"הרגיש","he":"הוא","loved":"אהב","video":"וידאו / מחשב","games":"משחקים","music":"מוזיקה","having":"ליהנות / שיש","fun":"כיף","just":"בדיוק / רק","like":"כמו","his":"שלו","classmates":"חברים לכיתה","but":"אבל","had":"היה לו","autism":"אוטיזם","brain":"מוח","worked":"פעל","little":"קצת","differently":"אחרת","one":"אחד","day":"יום","decided":"החליט","to":"ל־","do":"לעשות","something":"משהו","brave":"אמיץ","make":"ליצור","show":"להראות","what":"מה","life":"חיים","was":"היה","for":"עבור","him":"לו / אותו","hearing":"שמיעה","every":"כל","sound":"צליל","in":"ב־","at":"ב־","once":"בבת אחת","even":"אפילו","normal":"רגיל","sounds":"צלילים","could":"היה יכול","feel":"להרגיש","too":"מדי","loud":"רועש / חזק","needed":"היה זקוק","extra":"נוסף","time":"זמן","answer":"לענות","question":"שאלה","other":"אחרים","times":"פעמים","looked":"הביט","away":"הצידה","when":"כאשר","someone":"מישהו","spoke":"דיבר","people":"אנשים","might":"עשויים","think":"לחשוב","wasn't":"לא היה","listening":"מקשיב","they":"הם","were":"היו","wrong":"טעו","experienced":"חווה","things":"דברים","didn't":"לא","want":"לרצות","sorry":"מצטער / מרחם","wanted":"רצה","much":"הרבה","simpler":"פשוט יותר","friends":"חברים","who":"אשר / מי","understood":"הבינו","liked":"אהב","being":"להיות","alone":"לבד","also":"גם","laugh":"לצחוק","play":"לשחק","have":"לקיים / לעשות","with":"עם","kids":"ילדים","message":"מסר","clear":"ברור","i'm":"אני","kid":"ילד","different":"שונה","mean":"משמעותו","nothing":"שום דבר","common":"משותף","made":"יצר","then":"אז","amazing":"מדהים","happened":"קרה","mother":"אמא","shared":"שיתפה","it":"אותו / זה","online":"באינטרנט","spread":"התפשט","around":"ברחבי","world":"עולם","thousands":"אלפים","of":"של","watched":"צפו","small":"קטן","became":"הפך","big":"גדול","showed":"הראה","everyone":"לכולם","best":"הטובה ביותר","way":"דרך","change":"לשנות","see":"רואים","is":"הוא / היא","help":"לעזור","them":"להם","through":"דרך","eyes":"עיניים",
"21":"21"
}
RATE=22050
def audio(text):
    """Record whole sentence, and capture word-boundary metadata from that same neural synthesis stream."""
    import asyncio,tempfile,edge_tts
    async def collect():
        stream=edge_tts.Communicate(text,voice="en-US-JennyNeural",rate="-12%")
        chunks=[]; boundaries=[]
        async for chunk in stream.stream():
            if chunk["type"]=="audio": chunks.append(chunk["data"])
            elif chunk["type"]=="WordBoundary":
                boundaries.append({"text":chunk["text"],"start":chunk["offset"]/10000000,"duration":chunk["duration"]/10000000})
        return b"".join(chunks),boundaries
    media,boundaries=asyncio.run(collect())
    with tempfile.TemporaryDirectory() as temp:
        mp3=Path(temp)/"speech.mp3";wav=Path(temp)/"speech.wav"
        mp3.write_bytes(media)
        subprocess.run(["ffmpeg","-nostdin","-hide_banner","-loglevel","error","-y","-i",str(mp3),"-ar",str(RATE),"-ac","1","-c:a","pcm_s16le",str(wav)],check=True)
        with wave.open(str(wav),"rb") as w:
            return w.readframes(w.getnframes()),boundaries

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
    # Preserve natural sentence-level prosody; the existing player handles one recorded segment per sentence.
    word_groups=[list(range(len(matches)))]
    raw_fragments=[];time_base=0;parts=[]
    for pi,gg in enumerate(word_groups):
        left=matches[gg[0]].start();right=matches[gg[-1]].end()
        piece=en[left:right]
        raw,boundaries=audio(piece)
        duration=len(raw)/(2*RATE)
        raw_fragments.append(raw)
        # Approximate internal word boundaries by weighted pronunciation length;
        # phrase boundaries are exact from the WAV recordings.
        weights=[max(1.8,len(re.sub('[^a-zA-Z]','',matches[j].group()))**0.72) for j in gg]
        total=sum(weights);elapsed=0
        for j,weight in zip(gg,weights):
            m=matches[j];start=time_base+duration*elapsed/total;elapsed+=weight
            end=time_base+duration*elapsed/total
            if len(boundaries)==len(gg):
                event=boundaries[gg.index(j)]
                start=time_base+max(0,min(duration,event["start"]))
                end=time_base+max(start-time_base,min(duration,event["start"]+event["duration"]))
            elif boundaries:
                # Retain weighted fallback only for unmatched tokenizer boundaries.
                # Never claim unmatched word boundaries are exact.
                pass
            while len(tokens)<=j:tokens.append(None)
            clean=m.group().strip('.,!?;:“”"')
            gloss=GLOSS.get(clean.lower(), 'פירוש חסר')
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
pages=[]
for p in range(1,5):
    pages.append([i for i,r in enumerate(ROWS) if r["p"]==p])
# Runtime expects indexes and exact consistency with the original shared reading engine.
(ROOT/"unit-data.js").write_text("window.UNIT_DATA="+json.dumps({"story":story,"pages":pages},ensure_ascii=False,separators=(',',':'))+";",encoding="utf-8")
(ROOT/"alignment.js").write_text("window.GRADE8_ALIGNMENT="+json.dumps(align,ensure_ascii=False,separators=(',',':'))+";",encoding="utf-8")
(ROOT/"phrase-data.js").write_text("window.GRADE8_PHRASES="+json.dumps({"pauseMs":1500,"sentences":phrases},ensure_ascii=False,separators=(',',':'))+";",encoding="utf-8")
assert all(t["he"] != "פירוש חסר" for s in story for t in s["tokens"])
print(f"Generated {len(story)} recorded sentences, {sum(len(x['parts']) for x in phrases)} recorded phrases and aligned tokens")
