"""Download and optimize openly licensed image illustrations into website images/."""
import io, json, pathlib, re, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from PIL import Image, ImageOps
BASE=pathlib.Path(__file__).resolve().parent
D=json.loads(re.sub(r';\s*$','',re.sub(r'^window\.SUMMER_DATA\s*=\s*','',(BASE/'content.js').read_text('utf-8'))))
KEYS=sorted({s[3] for lesson in ('lesson1','lesson2') for s in D[lesson]}|{'street','tenement','immigrant','office','typewriter','subwayOld','shoe','bookcase'})
OUT=BASE/'images'; OUT.mkdir(exist_ok=True)
def one(key):
 target=OUT/(key+'.jpg')
 if target.exists() and target.stat().st_size>8000:return (key,'exists',target.stat().st_size)
 url=D['photos'][key][2] if key in D['photos'] else D['unsplash'][key]
 err=None
 for attempt in range(3):
  try:
   r=requests.get(url,timeout=(12,44),headers={'User-Agent':'Mozilla/5.0 (compatible; ClassroomEducationalResource/1.0; +https://github.com/Simonh68/teachers)','Accept':'image/webp,image/jpeg,image/png,image/*;q=0.8'})
   r.raise_for_status()
   if len(r.content)>30000000:raise RuntimeError('image too large')
   im=Image.open(io.BytesIO(r.content));im.load();im=ImageOps.exif_transpose(im).convert('RGB')
   im.thumbnail((1400,1050),Image.Resampling.LANCZOS)
   im.save(target,'JPEG',quality=82,optimize=True,progressive=True)
   if target.stat().st_size<3000:raise RuntimeError('output unusually small')
   print('OK',key,im.size,target.stat().st_size,flush=True)
   return (key,'ok',target.stat().st_size)
  except Exception as e:
   err=str(e)
   time.sleep(.8+attempt*.5)
 print('FAILED',key,err,flush=True)
 return (key,'failed',err)
with ThreadPoolExecutor(max_workers=5) as pool:
 results=sorted([f.result() for f in as_completed([pool.submit(one,k) for k in KEYS])])
failed=[r for r in results if r[1]=='failed']
(OUT/'README.txt').write_text('Realistic teaching photographs sourced from Wikimedia Commons or Unsplash, source links are in content.js.\n'+'\n'.join(f'{k}: '+(D['photos'][k][2] if k in D['photos'] else D['unsplash'][k]) for k in KEYS),encoding='utf-8')
print('SUMMARY',len(KEYS),'photos',len(failed),'missing',flush=True)
if failed:raise SystemExit('Missing photos: '+repr(failed))
