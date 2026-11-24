# Guy Stern — A Future to Build

Grade 9 historical Read-Along, created 24 November 2026.

Live lesson: https://simonh68.github.io/teachers/grade9/guy-stern/

## Content and experience

The approved story is reproduced without changes: **748 words, six chapters**. The two-page PDF and editable Word version are in `files/`.

The lesson has 113 screens: an opening, six chapter introductions, 24 vocabulary cards, 57 reading passages, 12 questions with 12 separate answer screens, and a final reflection. Reading passages contain no more than 18 words and end at sentence boundaries. All 748 words expose contextual Hebrew help, mapped through 287 meaning units. Full Hebrew translations are optional and do not move the English text.

Each passage stops at its end. The teacher or learner chooses the next passage with the folder tabs, Next, keyboard or the shared deck gestures. Reading defaults to 0.75× unless the learner has already saved a valid Teachers reading-speed preference. The saved preference is `teachers-read-alone-speed-v1`. Playback controls include replay, sentence replay, passage seeking, and returning up to 15 seconds within the current passage.

Navigation and gestures come from `../../shared/deck/standard.js`; recording playback, real word-boundary highlighting and word glosses come from `../../shared/read-along/inline-reader.js`. The local adapter supplies this lesson's menu, media controls and content. It does not copy those shared engines. The shared QR remote is included without changes.

## Narrator and evidence

This is a third-person educational biography, not Guy Stern speaking in the first person. The editorial narrator is a calm adult male voice: Microsoft **en-US-BrianNeural**, US English, synthesis rate `-5%`. The voice is disclosed as synthetic in the sources panel. It is not an imitation of Guy Stern or a historical recording.

Six chapter MP3s provide 252.024 seconds of recorded narration at 1×. Each of the 24 vocabulary recordings speaks its exact word and example, with a 0.55-second pause between them. Audio is served from this lesson; the browser does not synthesize speech. Timestamps come from actual synthesis WordBoundary events, not estimated word lengths. `audio.json` and `audio/vocabulary/manifest.json` retain timing, source text and checksums.

`story.json` records the historical sources. `assets/attribution.json` records photo sources, licenses and context. The portrait is Guy Stern in 2017; the school photograph is dated 2014; Camp Ritchie is an authentic illustrated postcard; the D-Day photograph shows historical context and does not claim to show Guy, who arrived three days later.

## Rebuild

Content inputs are `story.json`, `lesson-support.json`, `audio.json` and `assets/attribution.json`.

```sh
python source/build_lesson.py
node --check lesson.js
node --check lesson-data.js
```

Narration generation requires Python, `edge-tts==7.3.1`, ffmpeg and ffprobe. Run from this lesson directory, using explicit source/output paths:

```sh
python source/build_audio.py --source story.json --output /tmp/guy-stern-narration
python source/build_vocabulary.py --source lesson-support.json --output /tmp/guy-stern-vocabulary
```

Copy the six resulting chapter MP3s into `audio/` and the resulting `audio.json` to this directory. Copy only the 24 final vocabulary MP3s and their manifest into `audio/vocabulary/`; keep the intermediate `parts/` cache out of publication. Then rebuild the HTML/data and verify the source text, timing and recordings together. A different voice requires regenerated recordings and timing.

## Validation and publication

See `validation.json` for checks completed and their limits. No student information or answers are collected by this lesson. Local reading progress and display preferences stay on the device. The host site's shared instrumentation and temporary QR controller remain owned by the shared site.

Publish only on `classroom/grade9`, with changes scoped to `grade9/**`. The class manifest supplies the first card on the main Grade 9 materials section; `grade9/index.html` also links the lesson first. The central classroom publisher assembles the site without merging this branch into main. Confirm the exact Grade 9 revision in the published `classroom-revisions.csv`, the successful Actions deployment, and the live material links.
