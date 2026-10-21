# Band III: 60 challenging entries

Created 2026-10-21 for Teachers. Exactly 60 unique entries drawn from the existing Module E flashcards. Entries 1–30 are List A. Entries 31–60 contain 19 from B, 9 from C and 2 from D. Every teaching slide labels its list and links to its exact source group. The source vocabulary pages were not edited.

Selection is a pedagogical judgment about idioms, abstract language, confusable meanings, pronunciation and spelling, not an official or empirical ranking. First-half priority for List A follows Simon's explicit instruction. The original word, part of speech, Hebrew gloss, English example and Hebrew example are preserved byte-for-byte in entries.json. Source commit and selection policy are in source/provenance.json.

The HTML deck has 133 slides: a cover, 60 English/Hebrew reveal pairs, 11 short geometric visual breaks and a closing slide. English retains its position on translation reveal. The entry index links directly to every word. This is the ordinary paired vocabulary format, not VOCAB-3X2.

Navigation, fit, keyboard, wheel and swipe use ../../shared/deck/standard.js and standard.css. Separate recorded audio controls and their styles are opt-in shared modules vocabulary-audio.js/css. The central standard runtime is not forked or modified. A single audio player stops when slides change, the index opens, or the page is hidden. Word and sentence clips never queue each other. Speed is manually selectable. There is no runtime TTS.

120 prerecorded US English MP3 files use en-US-AriaNeural at -10% rate. A neutral teaching narrator reads the public flashcard words and example sentences. The abbreviation `sth` is spoken as `something`. audio-manifest.json retains the exact spoken text, word-boundary transcript, duration and SHA-256 of each clip. All clips were decoded successfully with ffmpeg and checked against the spoken source text.

Rebuild HTML: python3 source/build.py. Regenerate audio: python3 source/build_audio.py (requires edge-tts and ffmpeg). source/select.py expects a sibling clone of Simonh68/module-e-vocab at the repository parent; it rebuilds the selected source data. It must not silently select another sense of a repeated entry.

Validation: exact field comparison against all selected source HTML flashcards; 30 A entries first; all 120 file paths, hashes and decoded MP3s; browser word and sentence play controls, stopping on slide change, entry menu, English reveal geometry, and responsive viewport checks. All 133 slides passed 360×640 content-bound checks and all 60 pairs preserved exact English coordinates. Sample pairs passed 390×844 and 844×390 checks. Synthetic TouchEvent gestures starting on the word passed left, up, right and down with exactly one slide per gesture. Physical-device gestures have not been tested. Clipboard API is blocked in the HTTP preview, where the manual-copy fallback was verified.
