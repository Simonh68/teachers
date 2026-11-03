#!/usr/bin/env python3
"""Fail-closed validation of assembled classroom site before deployment."""
import json,pathlib,sys,urllib.parse,re
site=pathlib.Path(sys.argv[1]).resolve()
errors=[]
def err(s): errors.append(s)
if not (site/'index.html').is_file():err('missing homepage')
if not (site/'index2.html').is_file():err('missing preview')
for n in range(7,13):
 p=site/'data'/f'grade{n}.json'
 if not p.is_file():err(f'missing grade {n} data');continue
 try: d=json.loads(p.read_text(encoding='utf-8'))
 except Exception as ex:err(f'grade {n}: invalid JSON {ex}');continue
 if d.get('schemaVersion')!=1 or d.get('grade')!=n or not isinstance(d.get('materials'),list):err(f'grade {n}: invalid schema');continue
 ids=set()
 for item in d['materials']:
  if not isinstance(item,dict):err(f'grade {n}: non-object item');continue
  if not all(isinstance(item.get(k),str) and item[k].strip() for k in ('id','title','url','unit')):err(f'grade {n}: missing fields');continue
  if item['id'] in ids:err(f'grade {n}: duplicate {item["id"]}')
  ids.add(item['id'])
  for key in ('url','worksheet'):
   if key not in item:continue
   u=urllib.parse.urlsplit(item[key])
   if u.scheme:
    if u.scheme!='https':err(f'grade {n}: insecure external URL {item[key]}')
    continue
   if u.netloc or u.path.startswith('/') or '..' in pathlib.PurePosixPath(u.path).parts:err(f'grade {n}: unsafe path {item[key]}');continue
   f=site/urllib.parse.unquote(u.path)
   if not (f.is_file() or (f/'index.html').is_file()):err(f'grade {n}: missing target {item[key]}')
 if not d['materials']:err(f'grade {n}: empty manifest')
print('Publication validation:',sum(1 for n in range(7,13) if (site/'data'/f'grade{n}.json').is_file()),'manifests,',len(errors),'errors')
for e in errors:print('ERROR:',e)
if errors:sys.exit(1)
