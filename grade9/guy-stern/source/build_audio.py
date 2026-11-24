"""Build natural prerecorded narration with real synthesis word-boundary cues.

The approved text is sent only to the Microsoft speech service used by edge-tts.
No text changes, approximated chapter-wide timings, or runtime browser TTS.
"""
import argparse
import asyncio
import hashlib
import html
import json
import os
import re
import subprocess
from pathlib import Path

import edge_tts
import edge_tts.communicate as speech

if os.environ.get('SSL_CERT_FILE'):
    speech._SSL_CTX.load_verify_locations(os.environ['SSL_CERT_FILE'])

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--source', type=Path, default=Path(__file__).resolve().parent.parent / 'stern_work/story_data.json')
PARSER.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
ARGS = PARSER.parse_args()
OUT = ARGS.output
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = ARGS.source
VOICE = 'en-US-BrianNeural'
RATE = '-5%'

def norm(value):
    return re.sub(r'[^a-z0-9]', '', html.unescape(value).lower())

def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def align(chapter, cues):
    original = '\n\n'.join(chapter['paragraphs'])
    assert norm(original) == ''.join(norm(c['text']) for c in cues), 'Narration text differs from source'
    spans = []
    cursor = 0
    for cue in cues:
        size = len(norm(cue['text']))
        if not size:
            continue
        spans.append((cursor, cursor + size, cue))
        cursor += size
    words = []
    paragraphs = []
    cursor = 0
    for p, paragraph in enumerate(chapter['paragraphs']):
        pwords = []
        for token in paragraph.split():
            start_char, end_char = cursor, cursor + len(norm(token))
            cursor = end_char
            matched = []
            for a, b, cue in spans:
                low, high = max(start_char, a), min(end_char, b)
                if low < high:
                    length = cue['end'] - cue['start']
                    matched.append((cue['start'] + length * (low-a)/(b-a), cue['start'] + length * (high-a)/(b-a)))
            assert matched, token
            item = {'index': len(words), 'paragraph': p, 'text': token,
                    'start': round(matched[0][0], 5), 'end': round(matched[-1][1], 5)}
            words.append(item)
            pwords.append(item)
        paragraphs.append({'index': p, 'text': paragraph, 'start': pwords[0]['start'],
                           'end': pwords[-1]['end'], 'wordStart': pwords[0]['index'],
                           'wordEnd': pwords[-1]['index'] + 1})
    assert all(w['end'] > w['start'] for w in words)
    assert all(words[i]['start'] >= words[i-1]['end'] - .001 for i in range(1,len(words)))
    return words, paragraphs

async def generate(index, chapter):
    target = OUT / f'chapter-{index}.mp3'
    metadata = OUT / f'chapter-{index}-raw.json'
    text = '\n\n'.join(chapter['paragraphs'])
    source_hash = hashlib.sha256(text.encode()).hexdigest()
    reusable = False
    if target.exists() and metadata.exists():
        cached = json.loads(metadata.read_text())
        if (cached['source_sha256'] == source_hash and cached['sha256'] == checksum(target)
                and cached['voice'] == VOICE and cached['rate'] == RATE):
            cues = cached['cues']
            reusable = True
    if not reusable:
        for attempt in range(3):
            tmp = target.with_suffix('.tmp.mp3')
            cues = []
            try:
                with tmp.open('wb') as f:
                    async for event in edge_tts.Communicate(text, voice=VOICE, rate=RATE,
                                                           boundary='WordBoundary').stream():
                        if event['type'] == 'audio':
                            f.write(event['data'])
                        elif event['type'] == 'WordBoundary':
                            cues.append({'text': html.unescape(event['text']),
                                         'start': event['offset']/1e7,
                                         'end': (event['offset']+event['duration'])/1e7})
                assert len(cues) > 50 and tmp.stat().st_size > 10000
                tmp.replace(target)
                metadata.write_text(json.dumps({'voice': VOICE, 'rate': RATE,
                    'source_sha256': source_hash, 'sha256': checksum(target), 'cues': cues}, indent=2)+'\n')
                break
            except Exception as error:
                print(f'Chapter {index} attempt {attempt+1}: {type(error).__name__}: {str(error)[:200]}', flush=True)
                tmp.unlink(missing_ok=True)
                if attempt == 2:
                    raise
                await asyncio.sleep(2*(attempt+1))
    words, paragraphs = align(chapter, cues)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-f', 'null', '-'], check=True)
    duration = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration',
                    '-of','default=noprint_wrappers=1:nokey=1',str(target)], text=True))
    assert words[-1]['end'] <= duration+.1
    result = {'id': index, 'title': chapter['title'], 'src': f'audio/chapter-{index}.mp3',
              'duration': duration, 'source_sha256': source_hash, 'sha256': checksum(target),
              'words': words, 'paragraphs': paragraphs}
    print(f'Chapter {index}: {len(words)} timed words, {duration:.2f}s, {target.stat().st_size} bytes', flush=True)
    return result

async def main():
    source = json.loads(SOURCE.read_text())
    chapters = []
    for i, chapter in enumerate(source['chapters'], 1):
        chapters.append(await generate(i, chapter))
    result = {'version': 1, 'voice': VOICE, 'rate': RATE, 'synthetic': True,
              'timing': 'Microsoft synthesis WordBoundary events. Original whitespace words aligned by normalized characters; compound words combine their real boundary events.',
              'source_title': source['title'], 'chapters': chapters}
    (OUT / 'audio.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Complete:', sum(len(c['words']) for c in chapters), 'words;', round(sum(c['duration'] for c in chapters),2), 'seconds', flush=True)

if __name__ == '__main__':
    asyncio.run(main())
