from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]/'grade11/module-e-time-bank'
s=(root/'template.html').read_text()
for token,file in [('__EXAM_DATA__','content.json'),('__LINE_DATA__','lines.json')]:
 s=s.replace(token,json.dumps(json.loads((root/file).read_text()),ensure_ascii=False).replace('</','<\\/'))
s=s.replace('__APP_JS__',(root/'app.js').read_text())
(root/'index.html').write_text(s)
print(root/'index.html')
