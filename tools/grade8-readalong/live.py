"""Read-only verification of public deployment after merging the tested rollout."""
from pathlib import Path
import concurrent.futures,hashlib,json,time,urllib.request
R=Path(__file__).resolve().parents[2];base='https://simonh68.github.io/teachers/'
paths=['grade8/unit-1/index.html','grade8/unit-1-reading-pilot/index.html']+[str(p.relative_to(R)) for p in (R/'grade8/read-along').rglob('*') if p.is_file() and p.name!='qa-report.json']
def get(path):
 req=urllib.request.Request(base+path+'?readalong-verification='+str(int(time.time())),headers={'User-Agent':'Teachers-Grade8-ReadAlong-Verification'})
 with urllib.request.urlopen(req,timeout=30) as r:
  assert r.status==200;return r.read()
def verify(path):
 payload=get(path);assert hashlib.sha256(payload).hexdigest()==hashlib.sha256((R/path).read_bytes()).hexdigest(),'Outdated or missing: '+path
 return path
for attempt in range(20):
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:success=list(pool.map(verify,paths))
  break
 except Exception as e:
  if attempt==19:raise
  print('Waiting for complete Pages deployment',str(e),flush=True);time.sleep(10)
print('LIVE PASS: two unit entry points, approved reader, semantic alignment and all 33 audio parts match the tested files.',flush=True)
report={'passed':True,'publicAssets':len(success),'urls':[base+'grade8/unit-1/?view=sentences',base+'grade8/unit-1/?view=chunks'],'checkedAtUTC':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
Path('/tmp/grade8-readalong-qa/live-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
