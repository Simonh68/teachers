"""Download curated, term-specific realistic classroom images. Sources credited below."""
from pathlib import Path
from PIL import Image,ImageOps
from io import BytesIO
from urllib.parse import quote
import requests,time
ROOT=Path(__file__).parent/'images'/'curated'
ROOT.mkdir(parents=True,exist_ok=True)
files={
'tenement-interior':('https://cdn4.picryl.com/photo/1900/01/01/new-york-city-interior-of-tenement-house-1024.jpg','Library of Congress / Detroit Publishing Co., 1900–1910, no known restrictions'),
'delivery-boy':('https://images.pexels.com/photos/9502199/pexels-photo-9502199.jpeg?auto=compress&cs=tinysrgb&w=1400','Omar Ramadan, 2021, Pexels free-use photo; modern delivery worker as illustration'),
'token-booth':('https://commons.wikimedia.org/wiki/Special:FilePath/Lex_Av_63rd_St_IND_td_05.jpg?width=1400','Tdorante10, Wikimedia Commons, CC BY-SA; present-day booth as structural reference'),
'shoemaker2':('https://commons.wikimedia.org/wiki/Special:FilePath/'+quote('Shoemaker in his shop, Kenner, Louisiana 1938.jpg')+'?width=1400','US Farm Security Administration 1938, public-domain photograph of American shoemaker'),
'stoop':('https://images.unsplash.com/photo-1561069934-eee225952461?auto=format&fit=crop&w=1400&q=86','Unsplash street-level brownstone reference'),
'cleaning':('https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1400&q=86','Unsplash real cleaning worker'),
'stock-clerk':('https://images.unsplash.com/photo-1605902711622-cfb43c4437d1?auto=format&fit=crop&w=1400&q=86','Unsplash warehouse shelves, illustrative'),
'carpenter':('https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=1400&q=86','Unsplash carpentry equipment, illustrative'),
}
s=requests.Session()
s.headers.update({'User-Agent':'Educational-photo-reference/1.0 (contact: webmaster of teachers site)','Accept':'image/webp,image/png,image/jpeg,image/*;q=0.8'})
ok=[]
for key,(url,credit) in files.items():
 target=ROOT/(key+'.jpg')
 if target.exists() and target.stat().st_size>7000:
  ok.append(key);continue
 try:
  for attempt in range(3):
   try:
    response=s.get(url,timeout=30)
    response.raise_for_status()
    image=Image.open(BytesIO(response.content)).convert('RGB')
    image=ImageOps.exif_transpose(image)
    image.thumbnail((1500,1100),Image.Resampling.LANCZOS)
    image.save(target,'JPEG',quality=84,optimize=True)
    if target.stat().st_size<7000: raise ValueError('unusually small file')
    print('IMAGE',key,image.size,target.stat().st_size,flush=True)
    ok.append(key);break
   except Exception as e:
    print('RETRY',key,attempt,str(e)[:180],flush=True)
    time.sleep(3+attempt*4)
  time.sleep(1)
 except Exception as e:print('ERROR',key,str(e),flush=True)
(ROOT/'SOURCES.txt').write_text('\n'.join(f'{key}: {credit}\n{url}\n' for key,(url,credit) in files.items()),encoding='utf-8')
print('OK',len(ok),'of',len(files),flush=True)
if len(ok)<6:raise SystemExit('Not enough custom photos; fix sources before publication')
