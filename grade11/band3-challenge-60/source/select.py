import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parents[2]/'module-e-vocab'
raw=json.loads((SOURCE/'data/vocabulary-master.json').read_text())
sections=[
('רשימה A · קשרים ומשמעות','nevertheless|provided that|even if|even though|otherwise|necessarily|in terms of|in actual fact|in the meantime|among other things'),
('רשימה A · הבחנות מדויקות','considerable|significant|essentially|deliberately|worthwhile|efficient|extraordinary|characteristic|supposed|reasonable'),
('רשימה A · מושגים ומשמעויות','consequence|emphasis|priority|means|figure|approach|objective|concern|conduct|claim'),
('רשימות B–D · ביטויים','put up with|take into account|get away with sth|for the sake of|might as well|hold up|give in|make up|not until|look forward to'),
('רשימות B–D · הבחנות מדויקות','peculiar|contemporary|apparent|outstanding|economical|domestic|genuine|acquire|distinguish|interpret'),
('רשימות B–D · מושגים ופעלים','determine|correspond|emerge|reassure|criterion|judgment|involvement|dispute|debt|range')]
ids={'otherwise':'A2-007','approach':'A2-051','range':'D3-005'}
entries=[]
for s,(title,words) in enumerate(sections,1):
 for word in words.split('|'):
  candidates=[r for r in raw if r['en']==word and (word not in ids or r['source_entry_id']==ids[word])]
  assert len(candidates)==1,(word,len(candidates))
  entries.append({'number':len(entries)+1,'section':s,'section_title':title,'list':candidates[0]['group'][0],**candidates[0]})
assert len(entries)==60 and len({r['en'] for r in entries})==60
assert all(e['list']=='A' for e in entries[:30]) and all(e['list']!='A' for e in entries[30:])
(ROOT/'entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
sha=subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'],text=True).strip()
(ROOT/'source/provenance.json').write_text(json.dumps({'repository':'Simonh68/module-e-vocab','commit':sha,'path':'data/vocabulary-master.json','records_reviewed':len(raw),'selection':'Editorial teaching judgment across A–D: idiomatic meaning, abstraction, confusable senses, pronunciation and spelling. Not an empirical or official difficulty ranking.','preserved_fields':['en','pos','mean_he','ex_en','ex_he','support_text','source_entry_id','group'],'speaker_plan':'Neutral adult teaching narrator for isolated vocabulary and all illustrative sentences. No character dialogue is being acted. US English en-US-AriaNeural.','spoken_expansions':{'get away with sth':'get away with something'}},ensure_ascii=False,indent=2)+'\n')
print('Selected',len(entries),'from',len(raw),'records',sha)
