import asyncio,json,os,hashlib
from pathlib import Path
import edge_tts,edge_tts.communicate
OUT=Path(__file__).resolve().parents[2]/'grade6/boost-simulation'
async def main():
 if os.environ.get('CODEX_PROXY_CERT'):edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ['CODEX_PROXY_CERT'])
 texts=json.loads((OUT/'audio-texts.json').read_text()); sem=asyncio.Semaphore(3);manifest={}
 async def generate(key,text):
  async with sem:
   dest=OUT/'assets'/f'{key}.mp3'
   if not dest.exists() or dest.stat().st_size<1000:
    await edge_tts.Communicate(text,voice='en-US-BrianNeural',proxy=os.environ.get('HTTPS_PROXY')).save(str(dest))
   assert dest.stat().st_size>1000
   manifest[key]={'src':f'assets/{key}.mp3','text':text,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
   print(key,flush=True)
 await asyncio.gather(*(generate(k,t) for k,t in texts.items()))
 (OUT/'audio-manifest.json').write_text(json.dumps({'voice':'en-US-BrianNeural','synthetic':True,'browserTTS':False,'files':manifest},ensure_ascii=False,indent=2))
asyncio.run(main())
