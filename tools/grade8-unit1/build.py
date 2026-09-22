"""Rebuild the current Grade 8 unit without changing its aligned reading/audio."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade8/unit-1'
p=OUT/'unit-data.js'
d=json.loads(p.read_text().split('=',1)[1].strip().rstrip(';'))
words=[w for w in json.loads((ROOT/'grade9/unit-1/vocab.json').read_text()) if w['group'] in (21,22)]
assert len(words)==110 and len(d['story'])==18
for i,w in enumerate(words):
    w.update(number=i+1,id=f"g{w['group']}-{w['position']:02d}",audio=None)
d.update(words=words,scopeApproved='Core II Groups 21–22 (110 entries); Part One A–F only',version='20260922-core2-21-22')
p.write_text('window.UNIT_DATA='+json.dumps(d,ensure_ascii=False)+';\n')
(OUT/'index.html').write_text((Path(__file__).parent/'unit.html').read_text())
print('Built Grade 8: Core II groups 21–22, 110 entries; reading/audio preserved.')
