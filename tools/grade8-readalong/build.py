"""Apply approved Grade 8 read-along UI only; preserve live curriculum and sample."""
from __future__ import annotations
import hashlib,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DEST=ROOT/'grade8/read-along'
PILOT=ROOT/'grade8/unit-1-reading-pilot'
EXTRA_CSS='''
/* Multi-page additions retain the approved sample's fixed bilingual geometry. */
.paragraph-line{display:inline}.reading [data-en]{cursor:help}.reading [data-en]:focus-visible{outline:2px solid var(--cyan);outline-offset:2px;border-radius:3px}
#contents{font-size:14px;padding:8px 10px}#hint{white-space:normal}#counter{width:100px}.meta{letter-spacing:0}.meta .location{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tabstrip{display:flex;gap:4px;overflow-x:auto;overflow-y:hidden;scrollbar-width:thin;direction:ltr;flex:1}.tabstrip button{flex-shrink:0;font:800 12px Nunito,Heebo,sans-serif;padding:2px 8px;min-height:27px;border-radius:7px 7px 0 0;background:transparent}.tabstrip [aria-selected=true]{color:var(--marker);border-color:var(--marker);background:#294354}.tabstrip .done:after{content:' ✓';color:#91e5c1}.meta .step-label{flex-shrink:0;margin-left:10px}
#reading-menu{color:var(--ink);background:#0c2236;border:1px solid #52849b;border-radius:20px;width:min(760px,92vw);max-height:88dvh;padding:22px}#reading-menu::backdrop{background:#000b}.menu-heading{display:flex;align-items:center;justify-content:space-between;gap:15px}.menu-heading h2{margin:0;font-size:26px}.menu-modes{display:flex;gap:9px;flex-wrap:wrap;margin:14px 0}.menu-modes a{padding:8px 12px;border:1px solid #41647b;border-radius:9px;text-decoration:none}.menu-modes a[aria-current=page]{color:var(--marker);border-color:var(--marker)}.menu-note{font-size:14px;color:var(--muted)}#sentence-list{display:grid;gap:7px;margin:15px 0;max-height:48dvh;overflow-y:auto}#sentence-list button{text-align:left;direction:ltr;font:700 18px/1.5 Nunito,Arial,sans-serif;padding:10px 14px}#sentence-list small{font-size:12px;color:var(--cyan);margin-right:9px}.jump-row{display:flex;flex-wrap:wrap;gap:8px}
#reading-tip{position:fixed;z-index:20;max-width:min(320px,calc(100vw - 20px));padding:8px 12px;background:#eff9ff;color:#17263b;border:1px solid #72bcca;border-radius:10px;box-shadow:0 7px 22px #0008;font:600 16px/1.4 Heebo,Arial,sans-serif;pointer-events:none}.reading span.marker{font-weight:inherit}
@media(max-width:650px){.brand{display:none}.toolbar{gap:7px}.audio-controls{gap:5px}#contents{font-size:12px;padding:8px}#counter{width:98px}.meta .step-label{font-size:10px}.tabstrip{gap:2px}.tabstrip button{font-size:11px;padding:1px 6px}.sheet{grid-template-rows:30px minmax(0,1.1fr) minmax(0,1fr) 28px}}
@media(max-height:520px){.tabstrip button{min-height:20px;font-size:10px;padding:1px 6px}#contents{font-size:12px;padding:5px 9px}.sheet{grid-template-rows:23px minmax(0,1.1fr) minmax(0,1fr) 18px;gap:4px}}
'''
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read_js(path):return json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('=',1)[1].lstrip())[0]
def main():
    DEST.mkdir(exist_ok=True)
    sample=(PILOT/'bilingual-sample/index.html').read_text(encoding='utf-8')
    style=re.search(r'<style>(.*?)</style>',sample,re.S);assert style,'Approved sample stylesheet not found'
    (DEST/'reader.css').write_text(style.group(1)+EXTRA_CSS,encoding='utf-8')
    data=read_js(ROOT/'grade8/unit-1/unit-data.js');copied=read_js(PILOT/'unit-data.js')
    assert [{k:v for k,v in s.items() if k!='audio'} for s in data['story']]==[{k:v for k,v in s.items() if k!='audio'} for s in copied['story']],'Live story/timing and pilot differ; alignment requires review'
    assert len(data['story'])==18 and {w['group'] for w in data['words']}=={21,22},'Do not reset live curriculum'
    manual=json.loads((HERE/'alignment.json').read_text());aligned={}
    for s in data['story']:
        pairs=manual[str(s['number'])];cursor=0;units=[];mapping=[None]*len(s['tokens'])
        for n,(ids,text) in enumerate(pairs):
            at=s['he'].find(text,cursor);assert at>=0,(s['number'],text)
            assert not re.search(r'[\w\u0590-\u05ff]',s['he'][cursor:at]),(s['number'],'unmapped Hebrew')
            for i in ids:
                assert 0<=i<len(mapping) and mapping[i] is None,(s['number'],i)
                mapping[i]=n
            units.append({'indices':ids,'text':text,'start':at,'end':at+len(text)});cursor=at+len(text)
        assert not re.search(r'[\w\u0590-\u05ff]',s['he'][cursor:])
        assert all(i is not None for i in mapping),s['number']
        aligned[str(s['number'])]={'plain':s['plain'],'he':s['he'],'map':mapping,'units':units}
    (DEST/'alignment.js').write_text('window.GRADE8_ALIGNMENT='+json.dumps(aligned,ensure_ascii=False)+';\n',encoding='utf-8')
    phrase=read_js(PILOT/'phrase-data.js');assert len(phrase['sentences'])==18 and phrase['pauseMs']==1500
    (DEST/'audio').mkdir(exist_ok=True)
    for r,s in zip(phrase['sentences'],data['story']):
        assert r['number']==s['number']
        assert ''.join(p['text'] for p in r['parts']).strip()==s['plain'].strip()
        for part in r['parts']:
            src=PILOT/part['src'];assert digest(src)==part['sha256'];shutil.copyfile(src,DEST/part['src'])
    (DEST/'phrase-data.js').write_text('window.GRADE8_PHRASES='+json.dumps(phrase,ensure_ascii=False)+';\n',encoding='utf-8')
    shutil.copyfile(PILOT/'phrase-player.js',DEST/'phrase-player.js')
    for folder in ['unit-1','unit-1-reading-pilot']:
        path=ROOT/'grade8'/folder/'index.html';text=path.read_text(encoding='utf-8')
        if 'id="unit-legacy-app"' not in text:
            m=re.search(r"<script>\s*'use strict';\s*const D=window.UNIT_DATA",text);assert m,(folder,'Legacy application marker not found')
            start=text.index('<script>',m.start());text=text[:start]+text[start:].replace('<script>','<script type="text/plain" id="unit-legacy-app">',1)
            if folder.endswith('pilot'):
                for name in ['phrase-data.js','phrase-player.js','reading-pilot.js']:
                    pat=r'<script src="('+re.escape(name)+r'[^\"]*)"></script>'
                    text,count=re.subn(pat,lambda m:'<script type="text/plain" data-legacy-src="'+m.group(1)+'"></script>',text)
                    assert count==1,(folder,name,count)
            assert text.count('</body>')==1
            text=text.replace('</body>','<script src="../read-along/bootstrap.js?v=20261005-bilingual1"></script></body>')
            path.write_text(text,encoding='utf-8')
    charter=ROOT/'PROJECT_CHARTER.md';text=charter.read_text(encoding='utf-8')
    heading='## תקן הקריאה המחייב לכיתה ח׳ — מרקר דו־לשוני (5.10.2026)'
    if heading not in text:
        text+='\n\n'+heading+'\n\n'+'''- לפי אישור סיימון לדוגמה `grade8/unit-1-reading-pilot/bilingual-sample/`, כל מסכי ה־Read Along הפעילים של כיתה ח׳ משתמשים בתקן זה בלבד, הן בקריאה בקטעים והן במשפט בשקף. התקן גובר בכיתה ח׳ על הסתרת תרגום מאחורי כפתור/פרטים ועל קווי חלוקה בתוך משפטים. אין לשנות את כיתות ז׳ או ט׳ בעקבות הוראה זו.
- שקופית ראשונה: המקור באנגלית. השקופית הבאה: אותו מקור בדיוק, באותו מיקום, גודל ושבירת שורות, עם התרגום המלא גלוי. התרגום נשאר גלוי לאורך ההקראה ללא לחיצה נוספת.
- בזמן הקראת האנגלית מסמנים במרקר צהוב את המילה באנגלית ואת המילה או יחידת המשמעות המקבילה בעברית. מיפוי העברית מתועד ונבדק ידנית; אין להניח שסדר המילים זהה ואין להמציא תרגום למילות עזר שאינן מתורגמות בנפרד.
- משתמשים בהקלטות הקיימות בלבד. הפסקה של 1.5 שניות בין חלקי המשפט, לרבות אחרי פסיקים, נמדדת בזמן אמיתי ונשארת קבועה בכל מהירות. אין פסי חלוקה, גבולות ביטוי או סימנים נוספים בטקסט.
- משמרים השהיה/המשך, השמעה חוזרת, מהירות שמורה, תרגום מילה בנגיעה, בחירת קטע וסווייפ בארבעת הכיוונים. אין מעבר שקפים אוטומטי. מעבר ידני, תפריט, יציאה או הסתרת החלון עוצרים שמע ומתזמנים ממתינים. אחרי הפעלת השמע, שקף אנגלית וגם שקף עברית משמיעים את האנגלית בלבד אחרי שתי שניות.
- במצב קטעים מחלקים דף ארוך בין משפטים שלמים בלבד כדי ששתי השפות ייכנסו למסך. האנגלית אינה זזה בעת חשיפת התרגום. משמרים את סדר הטקסט וכל המשפטים.
- המימוש המשותף: `grade8/read-along/`. תוכן היחידה, קבוצות 21–22, המפגשים, התרגול והמבחן נשארים ללא שינוי. יחידה 1 הפעילה משתמשת בגרסה החדשה; הפיילוט נשאר מנותק מעץ האתר ובעל התקדמות נפרדת. הדוגמה שאושרה נשמרת ללא שינוי.
'''
        charter.write_text(text,encoding='utf-8')
    manifest={'standard':'grade8-bilingual-v1','approvedSample':'grade8/unit-1-reading-pilot/bilingual-sample/','sourceUnit':'grade8/unit-1/unit-data.js','sourceSHA256':digest(ROOT/'grade8/unit-1/unit-data.js'),'sourcePilotSHA256':digest(PILOT/'unit-data.js'),'sourceSampleSHA256':digest(PILOT/'bilingual-sample/index.html'),'sentences':18,'englishTokens':sum(len(s['tokens']) for s in data['story']),'semanticHebrewUnits':sum(len(v['units']) for v in aligned.values()),'audioParts':sum(len(r['parts']) for r in phrase['sentences']),'pauseMs':1500,'sourcePages':data['pages'],'routes':['grade8/unit-1/?view=chunks','grade8/unit-1/?view=sentences','grade8/unit-1-reading-pilot/?view=chunks','grade8/unit-1-reading-pilot/?view=sentences'],'curriculumPreserved':True,'samplePreserved':True,'detachedPilotPreserved':True}
    (DEST/'ROLLOUT.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
