"""Snapshot the two assigned word lists and generate actual neural MP3 recordings.

Run during the Teachers Pages build, never in the student's browser. Only the
English word and its example are sent to the speech service. No student data,
credentials, Hebrew translations or teacher directions are sent.
"""
from __future__ import annotations
import argparse
import asyncio
import hashlib
import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'grade7/band2-groups-01-02'
VOICE = 'en-US-GuyNeural'
RATE = '-12%'
SOURCES = {
    1: 'https://raw.githubusercontent.com/Simonh68/E-Vocab-Band-II/main/groups/group-01.html',
    2: 'https://raw.githubusercontent.com/Simonh68/E-Vocab-Band-II/main/groups/group-02.html',
}

def get_text(url: str) -> str:
    request = urllib.request.Request(url, headers={'User-Agent': 'Teachers-lesson-build/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return response.read().decode('utf-8-sig')
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
    raise RuntimeError('Download failed')

def snapshot() -> list[dict]:
    all_words = []
    for group, url in SOURCES.items():
        text = get_text(url)
        match = re.search(r'const\s+words\s*=\s*', text)
        if not match:
            raise ValueError(f'Group {group}: no source word array')
        words, _ = json.JSONDecoder().raw_decode(text[match.end():].lstrip())
        if len(words) != 55:
            raise ValueError(f'Group {group}: expected 55 records, got {len(words)}')
        for position, word in enumerate(words, 1):
            row = {key: str(word.get(key, '')).strip() for key in ('en', 'pos', 'mean_he', 'ex_en', 'ex_he')}
            if any(not row[key] for key in ('en','mean_he','ex_en','ex_he')):
                raise ValueError(f'Missing teaching text in group {group}, record {position}')
            # Correct a demonstrable name mismatch without changing the assigned word.
            if word['serial'] == 112 and row['ex_en'] == 'The boy reads the Bible at home.':
                row['ex_he'] = 'הילד קורא בתנ״ך בבית.'
            if word['serial'] == 1081 and row['ex_en'] == 'I am sure the boy would love it.':
                row['ex_he'] = 'אני בטוח שהילד יאהב את זה.'
            row.update(id=f'g{group:02d}-{word["serial"]}', serial=word['serial'], group=group, position=position)
            all_words.append(row)
        print(f'Group {group:02d}: {len(words)} source records validated', flush=True)
    if len({w['id'] for w in all_words}) != 110:
        raise ValueError('Duplicate group/serial identifiers')
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / 'words.json').write_text(json.dumps({'sources': SOURCES, 'words': all_words}, ensure_ascii=False, indent=2), encoding='utf-8')
    return all_words

def filename(word: dict) -> str:
    spoken = word['en'].rstrip('.!?') + '. ' + word['ex_en']
    digest = hashlib.sha256((VOICE+'|'+RATE+'|'+spoken).encode()).hexdigest()[:12]
    return f'{word["id"]}-{digest}.mp3'

def valid_mp3(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 1500:
        return False
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(path)], capture_output=True, text=True, timeout=12)
        return result.returncode == 0 and float(result.stdout.strip()) > .3
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False

async def make_audio(words: list[dict]) -> dict:
    import edge_tts
    folder = DEST / 'audio'
    folder.mkdir(exist_ok=True)
    started = time.monotonic()
    files, missing = {}, []
    semaphore = asyncio.Semaphore(3)
    failed = 0
    async def one(word: dict, attempts: int = 2) -> bool:
        nonlocal failed
        target = folder / filename(word)
        if valid_mp3(target):
            files[word['id']] = 'audio/' + target.name
            return True
        if time.monotonic() - started > 400 or failed >= 8:
            missing.append(word['id'])
            return False
        for attempt in range(attempts):
            temp = target.with_suffix('.part.mp3')
            try:
                text = word['en'].rstrip('.!?') + '. ' + word['ex_en']
                speech = edge_tts.Communicate(text, VOICE, rate=RATE, connect_timeout=10, receive_timeout=20)
                await asyncio.wait_for(speech.save(str(temp)), timeout=32)
                if not valid_mp3(temp):
                    raise ValueError('Generated audio did not pass MP3 validation')
                temp.replace(target)
                files[word['id']] = 'audio/' + target.name
                print(f'AUDIO {word["id"]} verified ({target.stat().st_size} bytes)', flush=True)
                return True
            except Exception as exc:
                temp.unlink(missing_ok=True)
                print(f'Audio attempt {attempt+1} for {word["id"]}: {type(exc).__name__}: {exc}', flush=True)
                await asyncio.sleep(1 + attempt)
        failed += 1
        missing.append(word['id'])
        return False
    # A preflight avoids hammering an unavailable service with 110 requests.
    first_ok = await one(words[0])
    async def limited(word: dict):
        async with semaphore:
            await one(word)
            await asyncio.sleep(.15)
    if first_ok:
        await asyncio.gather(*(limited(w) for w in words[1:]))
    else:
        for w in words[1:]:
            target=folder/filename(w)
            if valid_mp3(target): files[w['id']]='audio/'+target.name
            else: missing.append(w['id'])
    manifest = {'voice': VOICE, 'rate': RATE, 'provider': 'Microsoft neural text-to-speech, generated at build time', 'total': len(words), 'available': len(files), 'complete':len(files)==len(words), 'files': files, 'missing': missing}
    (folder/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'AUDIO RESULT: {len(files)} / {len(words)} validated local MP3 files', flush=True)
    return manifest

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--no-audio',action='store_true');args=parser.parse_args()
    words=snapshot()
    report={'entries':len(words), 'groups':[55,55], 'vocabulary_pages':220, 'brain_breaks':36, 'visual_policy':'Original vector landscapes and geometry only; no people, characters or religious symbols.'}
    if not args.no_audio:
        try:
            audio=asyncio.run(make_audio(words));report['audio_available']=audio['available'];report['audio_complete']=audio['complete']
        except Exception as exc:
            print(f'Audio generation unavailable: {type(exc).__name__}: {exc}',flush=True)
            report.update(audio_available=0,audio_complete=False)
            folder=DEST/'audio';folder.mkdir(exist_ok=True)
            (folder/'manifest.json').write_text(json.dumps({'total':110,'available':0,'complete':False,'files':{}}))
    (DEST/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__': main()
