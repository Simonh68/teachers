"""Copy the current Grade 8 Unit 1; change only the unlisted reading pilot.
No curriculum edits, no re-synthesis, no source-unit or navigation writes.
"""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, wave

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'grade8/unit-1'
DEST=ROOT/'grade8/unit-1-reading-pilot'
SLUG='unit-1-reading-pilot'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def run(*args): return subprocess.check_output(list(args),text=True).strip()
def unpack(path):
    text=path.read_text(encoding='utf-8')
    value,_=json.JSONDecoder().raw_decode(text.split('=',1)[1].lstrip())
    return value

def boundaries(sentence):
    text=sentence['plain']; tokens=sentence['tokens']; cuts={}
    # Each written comma, colon, semicolon or long dash is a breath boundary.
    # Word-internal hyphens and numeric commas are deliberately not split.
    for m in re.finditer(r'[,;:]|[–—]',text):
        if m.group()==',' and m.start()>0 and m.end()<len(text) and text[m.start()-1].isdigit() and text[m.end()].isdigit(): continue
        before=[i for i,t in enumerate(tokens) if t['startChar']<m.start()]
        if not before: continue
        i=before[-1]
        if i<len(tokens)-1: cuts[i]=m.end()
    # Long unpunctuated main/subordinate clauses; no arbitrary word-count chopping.
    for phrase in ['when you look around town','when thousands of excited monkeys','and eat as much fruit']:
        at=text.find(phrase)
        if at<0: continue
        i=next((j-1 for j,t in enumerate(tokens) if t['startChar']==at and j>0),None)
        if i is not None and i<len(tokens)-1: cuts[i]=at
    return cuts

def build():
    assert SOURCE.is_dir(),'Live Unit 1 must exist'
    original={str(p.relative_to(ROOT)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
    navigation={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'index.html',ROOT/'grade8/index.html'] if p.exists()}
    data=unpack(SOURCE/'unit-data.js')
    assert len(data['story'])==18 and len(data['words'])==110
    assert {w['group'] for w in data['words']}=={21,22},'Do not replace current Core II with obsolete Core I'
    if DEST.exists():
        assert (DEST/'PILOT-MANIFEST.json').exists(),'Refusing to overwrite an unrelated existing folder'
    shutil.copytree(SOURCE,DEST,dirs_exist_ok=True)
    if (DEST/'qa-report.json').exists(): (DEST/'qa-report.json').unlink()
    audio_dir=DEST/'audio';audio_dir.mkdir(exist_ok=True)
    phrase_data=[]; all_cuts=[]
    for s in data['story']:
        old_audio=s['audio']
        assert not re.match(r'https?://',old_audio),'Expected same-repository original recordings'
        source_audio=(SOURCE/old_audio).resolve()
        assert source_audio.is_relative_to(ROOT) and source_audio.is_file(),str(source_audio)
        copied=audio_dir/f'story-{s["number"]:02d}-original{source_audio.suffix}'
        shutil.copy2(source_audio,copied)
        assert sha(copied)==sha(source_audio)
        s['audio']='audio/'+copied.name
        pcm=audio_dir/f'_source-{s["number"]:02d}.wav'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source_audio),'-ac','1','-ar','24000','-c:a','pcm_s16le',str(pcm)],check=True)
        with wave.open(str(pcm),'rb') as f: params=f.getparams(); rate=f.getframerate(); frames=f.readframes(f.getnframes()); frame_count=f.getnframes()
        frame_width=params.nchannels*params.sampwidth
        duration=frame_count/rate; tokens=s['tokens']; cuts=boundaries(s); last=-1; start_frame=0; char_start=0; parts=[]
        for end_word in sorted(set(cuts)|{len(tokens)-1}):
            if end_word==len(tokens)-1: end_frame=frame_count;char_end=len(s['plain'])
            else:
                left=float(tokens[end_word]['end']);right=float(tokens[end_word+1]['start'])
                midpoint=(left+right)/2
                end_frame=round(midpoint*rate)
                char_end=cuts[end_word]
            assert start_frame<end_frame<=frame_count,(s['number'],end_word,start_frame,end_frame,frame_count)
            part_path=audio_dir/f'story-{s["number"]:02d}-part-{len(parts)+1:02d}.wav'
            with wave.open(str(part_path),'wb') as f:
                f.setparams(params);f.writeframes(frames[start_frame*frame_width:end_frame*frame_width])
            part={'index':len(parts),'firstToken':last+1,'lastToken':end_word,'startChar':char_start,'endChar':char_end,'sourceStart':start_frame/rate,'sourceEnd':end_frame/rate,'duration':(end_frame-start_frame)/rate,'text':s['plain'][char_start:char_end],'src':'audio/'+part_path.name,'sha256':sha(part_path)}
            assert part['duration']>.015
            parts.append(part);last=end_word;char_start=char_end;start_frame=end_frame
        assert ''.join(p['text'] for p in parts)==s['plain']
        # Splits are lossless: every decoded source sample occurs exactly once.
        reconstructed=b''
        for part in parts:
            with wave.open(str(DEST/part['src']),'rb') as f: reconstructed+=f.readframes(f.getnframes())
        assert reconstructed==frames,'Audio sample was omitted or duplicated'
        pcm.unlink()
        phrase_data.append({'number':s['number'],'duration':duration,'parts':parts})
        all_cuts.append({'sentence':s['number'],'parts':[p['text'] for p in parts]})
        print('PHRASES',s['number'],[p['text'] for p in parts],flush=True)
    (DEST/'unit-data.js').write_text('window.UNIT_DATA='+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
    (DEST/'phrase-data.js').write_text('window.PILOT_PHRASES='+json.dumps({'pauseMs':1500,'sentences':phrase_data},ensure_ascii=False)+';\n',encoding='utf-8')
    html=(SOURCE/'index.html').read_text(encoding='utf-8')
    html=html.replace("STORE='teachers-grade8-unit1-v1'","STORE='teachers-grade8-unit1-reading-pilot-v1'").replace("SPEED='teachers-read-alone-speed-v1'","SPEED='teachers-read-alone-pilot-speed-v1'")
    assert 'teachers-grade8-unit1-reading-pilot-v1' in html
    html=html.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="robots" content="noindex,nofollow,noarchive">',1)
    html=html.replace('<title>','<title>עותק קריאה · ',1)
    html=html.replace('</head>','<link rel="stylesheet" href="reading-pilot.css?v=20261005-1"></head>',1)
    html=html.replace('class="home-icon" href="../"','class="home-icon" href="./"',1)
    html=html.replace('aria-label="חזרה לספריית כיתה ח"','aria-label="חזרה לעותק היחידה"',1)
    html=html.replace('<strong>ח׳2 · Unit 1</strong>','<strong>ח׳2 · Unit 1 <span class="pilot-label">עותק קריאה</span></strong>',1)
    html=html.replace('Read Alone','Read Along')
    html=html.replace('</body>','<script src="phrase-data.js?v=20261005-1"></script><script src="phrase-player.js?v=20261005-1"></script><script src="reading-pilot.js?v=20261005-1"></script></body>',1)
    assert html.count('phrase-player.js')==1
    (DEST/'index.html').write_text(html,encoding='utf-8')
    for filename in ['phrase-player.js','reading-pilot.js','reading-pilot.css']:shutil.copy2(HERE/filename,DEST/filename)
    # Old within-unit shortcuts must resolve inside the copy, not to the live original.
    for folder,query in [('reading','chunks'),('sentences','sentences')]:
        p=DEST/folder/'index.html';p.parent.mkdir(exist_ok=True)
        p.write_text(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=../?view={query}"><title>עותק קריאה</title></head><body><a href="../?view={query}">פתיחת הקריאה</a><script>const q=new URLSearchParams(location.search);q.set("view","{query}");location.replace("../?"+q.toString());</script></body></html>',encoding='utf-8')
    (DEST/'teacher.html').write_text('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=./?view=teacher"><title>מדריך בעותק הקריאה</title></head><body><a href="./?view=teacher">פתיחת המדריך</a></body></html>',encoding='utf-8')
    manifest={'pilot':SLUG,'source':'grade8/unit-1','sourceCommit':run('git','rev-parse','HEAD'),'sourceTree':run('git','rev-parse','HEAD:grade8/unit-1'),'sourceFiles':original,'navigationFiles':navigation,'unlisted':True,'access':'Public direct link; no authentication. Not linked from site navigation. noindex is not access control.','pauseMs':1500,'speech':'Existing AI narration, losslessly split after punctuation and selected long clause boundaries; pitch-preserving browser playback. No new TTS.','sentences':18,'parts':sum(len(s['parts']) for s in phrase_data),'sourceAudioCopied':18,'curriculumPreserved':True,'phraseMap':all_cuts}
    (DEST/'PILOT-MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (DEST/'BUILD-NOTES.md').write_text('# Unlisted Grade 8 Unit 1 reading copy\n\nSource: current grade8/unit-1; Core II 21–22, 110 entries, 18 Part One sentences. Curriculum, translations and schedule are copied unchanged. No original unit or navigation file is edited. Separate local-storage keys.\n\nNarration reuses the existing source recordings, split losslessly into WAV segments using the existing word alignment. Every comma and major punctuation boundary (except numeric punctuation) receives a 1.5-second wall-clock pause, independent of speech speed. A few long unpunctuated clauses are also separated. The current tab stops at its end.\n\nBuild: tools/grade8-reading-pilot/build.py. UI/player: adjacent templates. QA: verify.py. This link is unlisted, not private.\n',encoding='utf-8')
    for path,digest in {**original,**navigation}.items():assert sha(ROOT/path)==digest,'Original changed: '+path
    print('COPIED WITHOUT MODIFYING SOURCE:',manifest['parts'],'audio parts',flush=True)
if __name__=='__main__':build()
