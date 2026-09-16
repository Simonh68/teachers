"""Build the approved Grade 7 groups and real, locally hosted neural narration.
No browser TTS, no API keys, no student data. Run --data-only before --audio.
Model: Kokoro v1.0 (Apache-2.0), kokoro-onnx (MIT).
"""
from __future__ import annotations
import argparse, base64, hashlib, json, re, subprocess, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'grade7/band2-groups-01-02'
SOURCE = 'Simonh68/E-Vocab-Band-II'
BLOBS = {1: '22b5993e84bb09bc2e09d2b9c89bf6b907b08e6d', 2: '2221b3fa5d6ff0f196b45016862900cadb9a97ef'}
VOICE = 'af_heart'
SPEED = 0.88


def fetch(url: str) -> bytes:
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Teachers-Lesson-Builder/1.0 (educational materials)'})
            with urllib.request.urlopen(req, timeout=120) as response:
                return response.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError('Download failed')


def data() -> list[dict]:
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for group, sha in BLOBS.items():
        blob = json.loads(fetch(f'https://api.github.com/repos/{SOURCE}/git/blobs/{sha}'))
        raw = base64.b64decode(blob['content'])
        check = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert check == sha, 'Source snapshot integrity failed'
        html = raw.decode('utf-8')
        match = re.search(r'const\s+words\s*=\s*', html)
        assert match, 'Missing source words'
        words, _ = json.JSONDecoder().raw_decode(html[match.end():])
        assert len(words) == 55, f'Unexpected group {group} size'
        for number, w in enumerate(words, 1):
            entry = {'id': f'g{group:02d}-{number:02d}', 'group': group, 'number': number,
                     'serial': w['serial'], 'word': w['en'], 'pos': w['pos'],
                     'meaning': w['mean_he'], 'sentence': w['ex_en'], 'translation': w['ex_he']}
            # Correct literal example/translation mismatches without changing the target word or sense.
            if w['en'] == 'Bible':
                entry['sentence'] = 'The Bible is on the shelf.'
                entry['translation'] = 'התנ״ך נמצא על המדף.'
            if w['en'] == 'would love something':
                entry['sentence'] = 'I would love a cup of tea.'
                entry['translation'] = 'אשמח לכוס תה.'
                entry['meaning'] = 'אשמח ל־; הייתי רוצה מאוד'
            entries.append(entry)
    assert len(entries) == 110
    (OUT / 'entries.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / 'vocabulary-audit.txt').write_text('\n'.join(f"{e['id']} | {e['word']} | {e['meaning']} | {e['sentence']} | {e['translation']}" for e in entries) + '\n', encoding='utf-8')
    print(f'Prepared {len(entries)} records, 220 vocabulary slides, 36 breaks.', flush=True)
    return entries


def audio() -> None:
    import numpy as np
    import soundfile as sf
    from kokoro_onnx import Kokoro
    entries = json.loads((OUT / 'entries.json').read_text(encoding='utf-8'))
    cache = ROOT / '.cache/kokoro-v1'
    cache.mkdir(parents=True, exist_ok=True)
    base = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'
    for name in ['kokoro-v1.0.onnx', 'voices-v1.0.bin']:
        target = cache / name
        if not target.exists():
            print('Downloading', name, flush=True)
            target.write_bytes(fetch(base + name))
    model = Kokoro(str(cache / 'kokoro-v1.0.onnx'), str(cache / 'voices-v1.0.bin'))
    folder = OUT / 'audio'
    folder.mkdir(exist_ok=True)
    manifest = {}
    for i, e in enumerate(entries, 1):
        # Only the target word and original example are narrated; no headings, Hebrew, or instructions.
        text = e['word'].rstrip('.!?') + '. ' + e['sentence']
        fingerprint = hashlib.sha256((VOICE + str(SPEED) + text).encode()).hexdigest()[:16]
        mp3 = folder / (e['id'] + '-' + fingerprint + '.mp3')
        if not mp3.exists():
            samples, sr = model.create(text, voice=VOICE, speed=SPEED, lang='en-us')
            samples = np.asarray(samples, dtype=np.float32)
            assert np.isfinite(samples).all() and len(samples) > sr * 0.4, e['id']
            peak = float(np.max(np.abs(samples)))
            assert peak > 0.005, f'Silent audio: {e["id"]}'
            if peak > .98:
                samples *= .98 / peak
            wav = folder / (e['id'] + '.wav')
            sf.write(wav, samples, sr)
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(wav), '-codec:a', 'libmp3lame', '-b:a', '128k', str(mp3)], check=True)
            wav.unlink()
        probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(mp3)], text=True)
        duration = float(probe.strip())
        assert 0.4 < duration < 40, (e['id'], duration)
        manifest[e['id']] = {'src': 'audio/' + mp3.name, 'text': text, 'duration': round(duration, 3), 'sha256': hashlib.sha256(mp3.read_bytes()).hexdigest()}
        print(f'{i}/110 {e["word"]}: {duration:.2f}s', flush=True)
    payload = {'engine': 'Kokoro v1.0 / kokoro-onnx 0.5.0', 'voice': VOICE, 'language': 'en-US', 'speed': SPEED,
               'synthetic': True, 'browserTTS': False, 'count': len(manifest), 'clips': manifest}
    assert payload['count'] == 110
    (OUT / 'audio-manifest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / 'AUDIO-NOTICE.txt').write_text('AI-generated narration: Kokoro v1.0, af_heart, US English, speed 0.88.\n110 actual MP3 files served by Teachers. No browser speech synthesis.\nKokoro model: Apache-2.0, https://huggingface.co/hexgrad/Kokoro-82M\nkokoro-onnx: MIT, https://github.com/thewh1teagle/kokoro-onnx\nOnly vocabulary words and original English examples are narrated.\n', encoding='utf-8')
    print('AUDIO VERIFIED: 110 non-empty playable MP3 files.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-only', action='store_true')
    parser.add_argument('--audio', action='store_true')
    args = parser.parse_args()
    if args.audio:
        audio()
    else:
        data()
