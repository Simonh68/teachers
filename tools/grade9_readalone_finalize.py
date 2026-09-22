"""Final layout/integration pass; run after grade9_complete_readalone.py."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];O=R/'grade9/unit-1/read-alone'
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main():
 content=json.loads((O/'content.json').read_text())
 # Keep two short sentences together; a long original sentence remains intact.
 pages=[];page=[];words=0
 for n,s in enumerate(content['sentences']):
  if page and (len(page)>=2 or words+len(s['words'])>20 or n in [10,24,36]):pages.append(page);page=[];words=0
  page.append(n);words+=len(s['words'])
 if page:pages.append(page)
 assert [n for p in pages for n in p]==list(range(46));content['pages']=pages
 # Attribute the verified image file rather than an unverified photo-page slug.
 content['imageCredit']['source']=content['imageCredit']['file'];save(O/'content.json',content)
 doc=BeautifulSoup((O/'index.html').read_text(),'html.parser')
 if not doc.select_one('#raMeaningDock'):
  dock=doc.new_tag('div',attrs={'id':'raMeaningDock','dir':'rtl','aria-label':'פירוש בעברית'});doc.select_one('#raPanel').insert_after(dock)
 (O/'index.html').write_text(str(doc))
 js=(O/'player.js').read_text()
 if 'const meaningDock = standalone' not in js:
  js=js.replace("bind(); status('טוען טקסט והקלטה…');", "const meaningDock = standalone ? $('#raMeaningDock') : host.appendChild(Object.assign(document.createElement('div'),{id:'raMeaningDock',dir:'rtl'})); meaningDock.append($('#raTip'));\n bind(); status('טוען טקסט והקלטה…');")
  js=js.replace('async function play(reset = false) {', 'async function play(reset = false) {\n if(reset)repeatEnd=null;')
  js=js.replace('range([Number(s.dataset.raSentence)]); status', "range([Number(s.dataset.raSentence)]); requestAnimationFrame(()=>{document.body.style.setProperty('--ra-toolbar-space',(host.offsetHeight+10)+'px');window.dispatchEvent(new Event('resize'));}); status")
 (O/'player.js').write_text(js)
 css='''
/* A reserved meaning strip prevents translations from obscuring or moving English. */
#raMeaningDock{flex:none;min-height:43px;height:43px;max-height:43px;margin-top:5px;border:1px solid #486b83;border-radius:8px;background:#0e2233;padding:5px 9px;overflow:auto;text-align:right;direction:rtl;font:15px/1.4 Arial,sans-serif;color:#d3ef9b}
#raMeaningDock:has(#raTip[hidden])::before{content:'נגיעה או ריחוף על מילה או ביטוי — לפירוש';color:#b0c4d5;font-size:12px}
#raMeaningDock #raTip{position:static!important;max-width:none!important;width:auto;background:transparent;color:#d3ef9b;border:0;border-radius:0;box-shadow:none;padding:0;font:inherit;pointer-events:none;line-height:1.4}
.ra-deck-controls #raMeaningDock{height:36px;min-height:36px;max-height:36px;margin:0 0 6px;font-size:14px;padding:4px 7px}
body[data-ra-deck] .slide.reading{padding-bottom:calc(var(--nav-height) + var(--ra-toolbar-space,165px))}
@media(max-width:760px){
 body.ra-page #raToolbar{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;padding:5px 0 3px}
 body.ra-page #raToolbar button{min-width:0!important;padding:5px 6px;font-size:12px;min-height:35px}
 body.ra-page .ra-speed{grid-column:1/3;grid-row:2;display:flex;justify-content:flex-start;font-size:11px;gap:5px}
 body.ra-page #raSpeed{width:100%;min-width:0;max-width:170px;font-size:12px;min-height:30px}
 body.ra-page #raSeek{grid-column:3;grid-row:2;min-width:0;width:100%;height:27px}
 body.ra-page #raFollowLabel{display:none!important}
 body.ra-page #raStatus{grid-column:1/-1;font-size:10px;min-height:14px;line-height:1.3}
 body.ra-page #raMeaningDock{font-size:14px;height:39px;min-height:39px;max-height:39px;padding:4px 8px}
 body.ra-page #raPanel{padding:10px 12px}
 body.ra-page .ra-text{line-height:1.44}
 body.ra-page .ra-sentence{margin-bottom:.4em}
 body.ra-page[data-mode=sentences] .ra-meta{display:none}
 body.ra-page[data-mode=sentences] .ra-translation{font-size:19px;line-height:1.38;padding-top:10px}
 body.ra-page[data-mode=sentences] .ra-single{line-height:1.42}
}
'''
 if 'A reserved meaning strip' not in (O/'reader.css').read_text():(O/'reader.css').write_text((O/'reader.css').read_text()+css)
 report=json.loads((O/'build-report.json').read_text());report['passages']=len(pages);report['translation_space']='reserved strip, does not cover English';save(O/'build-report.json',report)
 teacher=R/'grade9/unit-1/teacher.html';doc=BeautifulSoup(teacher.read_text(),'html.parser')
 if not doc.select_one('#read-alone-teacher-text'):
  fragment=BeautifulSoup('''<section class="deck-slide" id="read-alone-teacher-text"><h1>Read Alone Text · קריאה בקטעים</h1><p>אותו סיפור, בשלמותו. לשוניות קצרות, הקראה מוקלטת והדגשת המילה הנשמעת.</p><p>נגיעה או ריחוף על ביטוי מציגים פירוש בעברית ברצועה נפרדת. בסוף כל קטע ההקראה נעצרת; התלמיד ממשיך בלחיצה.</p><p>בכיתה: קריאה, עצירה ושאלת הבנה לפני ההמשך. בבית: חזרה על הקטעים שנלמדו, ללא צורך להאזין לכול שוב.</p><a class="button primary" href="read-alone/">פתיחת הקריאה בקטעים</a></section><section class="deck-slide" id="read-alone-teacher-words"><h1>Read Alone מילה־במילה</h1><p>משפט אחד בכל שקף; בשקף הבא אותו משפט עם תרגום לעברית. בכל שקף אפשר לקבל פירוש נפרד לכל מילה.</p><p>לאחר הפעלת האודיו הראשונה, ההקראה מתחילה לאחר שתי שניות במעבר לשקף. גם שקף התרגום מקריא את האנגלית.</p><p>ברירת המחדל: איטית. אפשר להאט עד רבע מהמהירות; הבחירה נשמרת בין שני המצבים ובמצגת המקורית. פתיחה חדשה אינה מפעילה אודיו מעצמה.</p><a class="button primary" href="read-alone/?mode=sentences">פתיחת משפט־משפט</a></section>''','html.parser')
  doc.select_one('.deck-controls').insert_before(fragment)
 teacher.write_text(str(doc))
 readme=O/'README.md';extra='\nFinal responsive and teacher-guide integration: python tools/grade9_readalone_finalize.py (after the main builder, before browser QA).\n'
 if extra not in readme.read_text():readme.write_text(readme.read_text()+extra)
 print('Finalized',len(pages),'passages; reserved Hebrew dock; small-screen controls; teacher guide.',flush=True)
if __name__=='__main__':main()
