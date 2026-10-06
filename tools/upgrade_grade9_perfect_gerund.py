"""Upgrade the existing 46-sentence story and regenerate aligned narration."""
import json, re, subprocess, hashlib
from pathlib import Path
from bs4 import BeautifulSoup
R = Path(__file__).resolve().parents[1]
O = R/'grade9/unit-1/read-alone'
changes = {
 2: ("His class had already planned a book sale for a community library.", "כיתתו כבר תכננה מכירת ספרים למען ספרייה קהילתית.", "כיתתו|כיתה|כבר — עם had לציון עבר מושלם|כבר|תכננה|מכירת|ספרים|מכירה|למען|ספרייה|קהילתית|ספרייה"),
 9: ("Instead of asking for an explanation, he started writing an angry answer, then stopped.", "במקום לבקש הסבר, הוא התחיל לכתוב תשובה כועסת, ואז עצר.", "במקום|של — בצירוף instead of|לבקש|ל־|הסבר|הסבר|הוא|התחיל|לכתוב|תשובה|כועסת|תשובה|אז|עצר"),
 27: ("He and his father had finished making it late the night before.", "הוא ואביו סיימו להכין אותו בשעה מאוחרת בלילה הקודם.", "הוא|ו־|שלו|אבא|כבר — עם finished לציון עבר מושלם|סיימו|להכין|אותו|מאוחר|ה־|לילה|הקודם"),
 28: ("Suddenly, Noam understood why Eitan had answered so quickly.", "פתאום נועם הבין מדוע איתן ענה מהר כל כך קודם לכן.", "פתאום|נועם|הבין|מדוע|איתן|כבר — עם answered לציון עבר מושלם|ענה|כל כך|במהירות"),
 29: ("“I have never felt so embarrassed about assuming the worst,” Noam said.", "״מעולם לא הרגשתי נבוך כל כך בגלל ההנחה שהכול לרעה,״ אמר נועם.", "אני|עם felt לציון ניסיון עד עכשיו|מעולם לא|הרגשתי|כל כך|נבוך|בגלל|הנחת|ה־|הגרוע ביותר|נועם|אמר"),
 33: ("I have learned that explaining things clearly matters.”", "למדתי שחשוב להסביר דברים בצורה ברורה.״", "אני|עם learned לציון לקח התקף עכשיו|למדתי|ש־|להסביר|דברים|בבירור|חשוב"),
 40: ("“Helping your brother was important, and I appreciate your coming today,” Noam said.", "״העזרה לאחיך הייתה חשובה, ואני מעריך את זה שבאת היום,״ אמר נועם.", "לעזור|שלך|אח|הייתה|חשובה|ו־|אני|מעריך|שלך|ההגעה|היום|נועם|אמר"),
}
def main():
 data=json.loads((O/'content.json').read_text())
 assert len(data['sentences'])==46
 # Preserve sentence IDs and paragraph/page relationships.
 for sid,(en,he,gloss) in changes.items():
  row=data['sentences'][sid-1]; row.update(en=en,he=he)
  toks=list(re.finditer(r"[A-Za-z]+(?:['’][A-Za-z]+)*|[0-9]+",en)); gs=gloss.split('|')
  assert len(toks)==len(gs),(sid,len(toks),len(gs))
  row['words']=[]; pos=0
  for m,g in zip(toks,gs):
   row['words'].append(dict(word=m.group(),he=g,prefix=en[pos:m.start()]));pos=m.end()
  row['suffix']=en[pos:]
  row['units']=[dict(en=w['word'],he=w['he'],first=i,last=i) for i,w in enumerate(row['words'])]
 # Update the reading page before the existing audio builder reads its source.
 path=R/'grade9/unit-1/reading.html'; soup=BeautifulSoup(path.read_text(),'html.parser')
 nodes=soup.select('.story .sentence'); assert len(nodes)==46
 for sid,(en,_,_) in changes.items():
  n=nodes[sid-1]; label=n.select_one('.sid').extract(); n.clear(); n.append(label);n.append(en)
 path.write_text(str(soup))
 subprocess.run(['python','-u',str(R/'tools/grade9_read_alone_audio.py')],check=True)
 audio=json.loads((O/'audio.json').read_text());idx=0
 for row,a in zip(data['sentences'],audio['sentences']):
  assert row['en']==a['en'] and len(row['words'])==len(a['words'])
  for w,t in zip(row['words'],a['words']):
   assert w['word'].lower()==t['word'].lower()
   w.update(start=t['start'],end=t['end'],index=idx);t['index']=idx;idx+=1
 data.update(version='20261006-perfect-gerund',wordCount=idx,source_sha256=audio['source_sha256'])
 (O/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (O/'audio.json').write_text(json.dumps(audio,ensure_ascii=False,indent=2)+'\n')
 # Keep the complete teaching deck and its translation slides in sync.
 path=R/'grade9/the-message-without-a-voice/index.html';soup=BeautifulSoup(path.read_text(),'html.parser')
 for node in soup.select('[data-ra-sentence]'):
  sid=int(node['data-ra-sentence'])+1
  if sid not in changes:continue
  target=node.select_one('.story-sentence')
  if target:
   target.clear();target.append(changes[sid][0])
  tr=node.select_one('.translation')
  if tr:tr.string=changes[sid][1]
 path.write_text(str(soup))
 path=O/'index.html';s=path.read_text();s=s.replace('kind:"grade9",','kind:"grade9",assetVersion:"20261006-perfect-gerund",');path.write_text(s)
 assert hashlib.sha256((O/'assets/story.mp3').read_bytes()).hexdigest()==audio['sha256']
 report={'version':data['version'],'sentences':46,'updatedSentenceIds':list(changes),'words':idx,'audioSeconds':audio['duration'],'audioMatchesText':True,'grammar':['Past Perfect','Present Perfect','gerund after preposition','gerund as subject','gerund after finish/appreciate']}
 (O/'grammar-upgrade-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report),flush=True)
if __name__=='__main__':main()
