"""Build the exact 110-entry vocabulary snapshot and site-hosted neural MP3s.
Only public curriculum text is processed. No browser speech synthesis or secrets.
"""
from pathlib import Path
import base64, hashlib, json, os, re, subprocess, sys, time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'grade7/band2-groups-01-02'
SOURCES = {1: '22b5993e84bb09bc2e09d2b9c89bf6b907b08e6d', 2: '2221b3fa5d6ff0f196b45016862900cadb9a97ef'}

def fetch_json(url):
    for attempt in range(4):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Teachers-curriculum-build', 'Accept': 'application/vnd.github+json'}), timeout=60) as response:
                return json.load(response)
        except Exception:
            if attempt == 3: raise
            time.sleep(2 ** attempt)

def snapshot():
    DEST.mkdir(parents=True, exist_ok=True)
    records = []
    for group, sha in SOURCES.items():
        blob = fetch_json(f'https://api.github.com/repos/Simonh68/E-Vocab-Band-II/git/blobs/{sha}')
        source = base64.b64decode(blob['content']).decode('utf-8')
        match = re.search(r'const\s+words\s*=\s*', source)
        if not match: raise RuntimeError('Missing source vocabulary array')
        words, _ = json.JSONDecoder().raw_decode(source[match.end():])
        if len(words) != 55: raise RuntimeError(f'Expected 55 entries in group {group}')
        for i, word in enumerate(words, 1):
            row = {key: word[key] for key in ('serial', 'en', 'pos', 'mean_he', 'ex_en', 'ex_he')}
            if not all(isinstance(row[k], str) and row[k].strip() for k in ('en','mean_he','ex_en','ex_he')):
                raise RuntimeError(f'Incomplete entry: {group}/{i}')
            row.update(group=group, number=i, id=f'g{group:02d}-{i:02d}')
            records.append(row)
    (DEST / 'data.js').write_text('window.VOCABULARY = ' + json.dumps(records, ensure_ascii=False) + ';\n', encoding='utf-8')
    (DEST / 'source-manifest.json').write_text(json.dumps({'sourceRepository':'Simonh68/E-Vocab-Band-II','sourceBlobs':SOURCES,'entries':len(records),'policy':'Original word, sense, example and translation preserved verbatim.'}, indent=2), encoding='utf-8')
    print(f'Snapshot: {len(records)} complete entries', flush=True)
    return records

def generate(records):
    import numpy as np
    import soundfile as sf
    import torch
    from kokoro import KPipeline
    torch.set_num_threads(2)
    audio_dir = DEST / 'audio'
    audio_dir.mkdir(exist_ok=True)
    pipeline = None
    manifest = {'engine':'Kokoro-82M v1.0', 'voice':'af_heart', 'language':'en-US', 'speed':0.87, 'format':'mp3', 'browserSpeechSynthesis':False, 'files':{}}
    old = {}
    old_path = audio_dir / 'manifest.json'
    if old_path.exists():
        old = json.loads(old_path.read_text()).get('files', {})
    for n, record in enumerate(records, 1):
        transcript = record['en'].rstrip('.!?') + '. ' + record['ex_en']
        digest = hashlib.sha256(('af_heart|0.87|' + transcript).encode()).hexdigest()
        target = audio_dir / (record['id'] + '.mp3')
        old_entry = old.get(record['id'], {})
        if target.exists() and target.stat().st_size > 1000 and old_entry.get('sha256Text') == digest:
            manifest['files'][record['id']] = old_entry
            continue
        if pipeline is None:
            pipeline = KPipeline(lang_code='a', device='cpu')
        chunks = []
        with torch.inference_mode():
            for _, _, audio in pipeline(transcript, voice='af_heart', speed=0.87, split_pattern=r'\n+'):
                chunks.append(audio.detach().cpu().numpy() if hasattr(audio, 'detach') else np.asarray(audio))
        if not chunks: raise RuntimeError('No audio: ' + record['id'])
        wave = np.concatenate(chunks)
        if len(wave) < 2400 or not np.isfinite(wave).all() or np.max(np.abs(wave)) < 0.001:
            raise RuntimeError('Invalid audio: ' + record['id'])
        temp = audio_dir / (record['id'] + '.wav')
        sf.write(temp, wave, 24000)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(temp),'-af','loudnorm=I=-18:TP=-2:LRA=7','-ar','24000','-ac','1','-codec:a','libmp3lame','-b:a','96k',str(target)], check=True)
        temp.unlink()
        manifest['files'][record['id']] = {'src': 'audio/' + target.name, 'text': transcript, 'sha256Text':digest, 'seconds':round(len(wave)/24000,2), 'bytes':target.stat().st_size}
        print(f'Audio {n}/{len(records)}: {record["en"]}', flush=True)
    if len(manifest['files']) != len(records): raise RuntimeError('Incomplete audio coverage')
    old_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (DEST / 'audio-manifest.js').write_text('window.VOCAB_AUDIO = ' + json.dumps(manifest, ensure_ascii=False) + ';\n', encoding='utf-8')
    print('All neural audio files verified and ready.', flush=True)

if __name__ == '__main__':
    records = snapshot()
    if '--data-only' not in sys.argv:
        generate(records)
