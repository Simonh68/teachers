import asyncio,json,os,hashlib
from pathlib import Path
import edge_tts,edge_tts.communicate
OUT=Path(__file__).resolve().parents[2]/'grade6/boost-simulation'
VERSION='speaker-v2'
def narrator_plan(texts):
 plans={}
 for key,text in texts.items():
  if 'response' in key:
   female=int(key.rsplit('-',1)[1])%2==1
   plans[key]=dict(voice='en-US-JennyNeural' if female else 'en-US-GuyNeural',category='adult woman' if female else 'adult man',evidence='A short everyday situation. The script specifies neither gender nor age; voice is an editorial choice, not a fact about the speaker.',certainty='unspecified')
  elif key=='s1-passage-1':
   plans[key]=dict(voice='en-US-JennyNeural',category='woman',evidence='The narrator introduces herself as Sarah. The user explicitly identifies Sarah as a woman. The script does not specify an age.',certainty='gender confirmed by user; exact age unspecified')
  elif key=='s1-passage-2':
   plans[key]=dict(voice='en-US-GuyNeural',category='male',evidence='The narrator introduces himself as David. Exact age is not given; a male voice is used without claiming a specific age.',certainty='male name; age unspecified')
  elif key=='s2-passage-1':
   plans[key]=dict(voice='en-US-JennyNeural',category='woman',evidence='Birthday of the speaker’s mother. No name, gender or age is supplied. A female adult narrator is an editorial choice.',certainty='unspecified')
  elif key=='s2-passage-2':
   plans[key]=dict(voice='en-US-AnaNeural',category='school-age girl',evidence='The speaker plays with Max every morning before school. A child voice fits the school context. Female gender is an editorial choice because the script does not specify it. Exact age is not given.',certainty='school context; gender and exact age unspecified')
  else:raise ValueError('Missing speaker review: '+key)
  plans[key]['text']=text
 return plans
async def main():
 if os.environ.get('CODEX_PROXY_CERT'):edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ['CODEX_PROXY_CERT'])
 texts=json.loads((OUT/'audio-texts.json').read_text()); plans=narrator_plan(texts);sem=asyncio.Semaphore(3);manifest={}
 (OUT/'speaker-plan.json').write_text(json.dumps({'version':VERSION,'policy':'Review gender, age cues and context before voice selection. Record uncertainty; do not infer gender or exact age when absent. Voice cache includes text, voice and settings.','clips':plans},ensure_ascii=False,indent=2))
 async def generate(key,text):
  async with sem:
   plan=plans[key];voice=plan['voice'];fingerprint=hashlib.sha256((text+'|'+voice+'|'+VERSION).encode()).hexdigest()[:12]
   dest=OUT/'assets'/f'{key}-{fingerprint}.mp3'
   if not dest.exists() or dest.stat().st_size<1000:
    await edge_tts.Communicate(text,voice=voice,proxy=os.environ.get('HTTPS_PROXY')).save(str(dest))
   assert dest.stat().st_size>1000
   manifest[key]={'src':f'assets/{dest.name}','text':text,'voice':voice,'speaker':plan,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
   print(key,flush=True)
 await asyncio.gather(*(generate(k,t) for k,t in texts.items()))
 (OUT/'audio-manifest.json').write_text(json.dumps({'version':VERSION,'synthetic':True,'browserTTS':False,'files':manifest},ensure_ascii=False,indent=2))
asyncio.run(main())
