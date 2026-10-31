#!/usr/bin/env python3
"""Build distinct, licensed, semantically searched photographs for A Summer's Reading Part 1."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
from urllib.parse import urlparse
import io,json,re,time,hashlib,shutil,html
import requests
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=json.loads((HERE/'photo-manifest.json').read_text('utf8'))
ALL=DATA['background']+DATA['vocabulary']
OUTPUT=HERE/'photos';OUTPUT.mkdir(exist_ok=True)
SESSION=requests.Session()
SESSION.headers.update({'User-Agent':'EducationalSlides/1.0 (Simonh68/teachers GitHub educational project)','Accept':'application/json,image/jpeg,image/png,image/webp,*/*;q=0.7'})
API='https://commons.wikimedia.org/w/api.php'
used=set()
log=[]
def get(url,max_trials=4,timeout=28):
    last=None
    for attempt in range(max_trials):
        try:
            res=SESSION.get(url,timeout=timeout,headers={'Accept':'image/jpeg,image/png,image/webp,*/*'} if 'wikipedia.org' not in url else None)
            if res.status_code==429:
                delay=min(48,7*(2**attempt))
                print('Rate limit from',urlparse(url).netloc,'sleep',delay,flush=True)
                time.sleep(delay);continue
            res.raise_for_status()
            return res.content
        except (requests.RequestException,ValueError) as e:
            last=e;time.sleep(2+2*attempt)
    raise RuntimeError('Failed to retrieve %s: %r'%(url,last))
def safe_query(query):
    q={'action':'query','generator':'search','gsrsearch':query,'gsrnamespace':6,'gsrlimit':20,'prop':'imageinfo','iiprop':'url|size|mime|extmetadata','iiurlwidth':1200,'format':'json','formatversion':2}
    last=None
    for attempt in range(4):
        try:
            res=SESSION.get(API,params=q,timeout=35)
            if res.status_code==429:time.sleep(8+attempt*6);continue
            res.raise_for_status()
            return res.json().get('query',{}).get('pages',[])
        except (requests.RequestException,ValueError) as e:
            last=e;time.sleep(2+attempt*4)
    print('Search failed:',query,last,flush=True)
    return []
def choose(query):
    terms=[x for x in re.findall(r'[a-z]+',query.lower()) if x not in ('old','new','city','photograph','photo','people','person','man','woman','picture','closeup','1950','1940','historic','historical')]
    queries=[query]
    if len(terms)>3:queries.append(' '.join(terms[:3])+' photo')
    if len(terms)>2:queries.append(' '.join(terms[:2])+' photo')
    for query_attempt in queries:
        pages=safe_query(query_attempt)
        scored=[]
        for page in pages:
            try:
                info=page['imageinfo'][0]
                if (info.get('mime') or '').lower() not in ('image/jpeg','image/png','image/webp'):continue
                if min(info.get('width',0),info.get('height',0)) <300:continue
                raw=info.get('thumburl') or info.get('url')
                if not raw or raw in used:continue
                license=(info.get('extmetadata',{}).get('LicenseShortName',{}) or {}).get('value','')
                if not license or any(x in license.lower() for x in ['unknown','copyrighted','all rights reserved']):continue
                name=page['title'].lower()
                bad=['svg','flag of','coat of arms','logo','diagram','cartoon','drawing','poster','meme','award','signpost','painting','map of the world','2025','2026','2024','video thumbnail','screenshot']
                if any(x in name for x in bad):continue
                score=25-int(page.get('index',20))
                for t in terms:score+=(3 if t in name else 0)
                if 'photograph' in name or 'photo' in name:score+=3
                if '1950' in query and ('1950' in name or '1940' in name):score+=4
                scored.append((score,raw,page['title'],license,info.get('descriptionurl',raw)))
            except (KeyError,TypeError,ValueError):
                continue
        if scored:
            scored.sort(key=lambda x:x[0],reverse=True)
            for score,url,name,license,source in scored[:8]:
                try:
                    b=get(url,max_trials=2,timeout=28)
                    im=Image.open(io.BytesIO(b));im.load()
                    if min(im.size)<300:continue
                    used.add(url)
                    return im,{'url':url,'title':name,'license':license,'source':source,'score':score}
                except Exception as e:print('Candidate failed',name,repr(e)[:200],flush=True)
    raise RuntimeError('No appropriate CC photograph found for '+query)
def load_existing(name):
    path=ROOT/'images'/(name+'.jpg')
    if not path.exists(): raise FileNotFoundError(path)
    return Image.open(path),{'url':'../images/'+name+'.jpg','title':'Previously self-hosted teaching photograph: '+name,'license':'See main-site image credit','source':'../images/'+name+'.jpg'}
def load_direct(url):
    b=get(url,max_trials=4);return Image.open(io.BytesIO(b)),{'url':url,'source':url,'title':urlparse(url).path.rsplit('/',1)[-1],'license':'See original publisher license or public domain status'}
def save_one(ent):
    target=OUTPUT/(ent['key']+'.jpg')
    if target.is_file() and target.stat().st_size>10000:
        return {'key':ent['key'],'status':'cached','word':ent['word'],'path':str(target),'size':target.stat().st_size}
    sources=[]
    if ent.get('existing'):sources.append(('existing',ent['existing']))
    if ent.get('url'):sources.append(('direct',ent['url']))
    if ent.get('search'):sources.append(('search',ent['search']))
    last=None
    for kind,what in sources:
        try:
            if kind=='existing':im,license=load_existing(what)
            elif kind=='direct':im,license=load_direct(what)
            else:im,license=choose(what)
            im=ImageOps.exif_transpose(im).convert('RGB')
            im.thumbnail((1440,1080),Image.Resampling.LANCZOS)
            if min(im.size)<300:raise RuntimeError('Image too small')
            im.save(target,'JPEG',quality=86,progressive=True,optimize=True)
            digest=hashlib.sha256(target.read_bytes()).hexdigest()
            print('PHOTO',ent['key'],ent['word'],str(im.size),license['title'][:80],target.stat().st_size,flush=True)
            return {'key':ent['key'],'word':ent['word'],'status':'ok','photoSource':license,'size':target.stat().st_size,'sha256':digest,'path':str(target)}
        except Exception as err:
            last=err;print('Trying next source for',ent['key'],kind,repr(err)[:150],flush=True)
    if ent['key'] in ('bg-usa','bg-city') and not sources:
        raise RuntimeError('Maps need a source URL')
    raise RuntimeError('No usable image for '+ent['key']+' '+ent['word']+' : '+repr(last))
def contact_sheet(records):
    cols=5;w=260;h=198
    rows=(len(records)+cols-1)//cols
    sheet=Image.new('RGB',(w*cols,h*rows),(237,242,245))
    draw=ImageDraw.Draw(sheet)
    try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
    except Exception:font=ImageFont.load_default()
    for i,rec in enumerate(records):
        path=OUTPUT/(rec['key']+'.jpg')
        if not path.exists():continue
        pic=ImageOps.fit(Image.open(path).convert('RGB'),(w,h-34),method=Image.Resampling.LANCZOS)
        x=(i%cols)*w;y=(i//cols)*h;sheet.paste(pic,(x,y))
        text=rec['key']+' · '+rec['word'][:19]
        draw.text((x+7,y+h-29),text,font=font,fill=(15,34,48))
    sheet.save(OUTPUT/'contact-sheet.jpg','JPEG',quality=83,optimize=True)
def main():
    fails=[]
    for ent in ALL:
        try:log.append(save_one(ent))
        except Exception as err:
            fails.append([ent['key'],str(err)])
            print('ERROR:',ent['key'],str(err)[:300],flush=True)
        time.sleep(.7)
    contact_sheet(log)
    (OUTPUT/'sources.json').write_text(json.dumps({'photos':log,'errors':fails},indent=2,ensure_ascii=False),encoding='utf8')
    print('SUMMARY photo_count=%d expected=%d errors=%d'%(len(list(OUTPUT.glob('*.jpg')))-1,len(ALL),len(fails)),flush=True)
    if fails:raise SystemExit('Unresolved photographs '+str(fails))
if __name__=='__main__':main()
