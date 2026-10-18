# A Voice for Every Student — Module C

Original full Module C practice for Grade 12, four units. Bagrut Trap Killer project.

Live: https://simonh68.github.io/teachers/grade12/four-units/module-c-school-radio/
Class catalogue: https://simonh68.github.io/teachers/#grade12four

292 words, 24 sentences, four paragraphs, 24 locked PDF lines. Seven reading questions /70 and one 70–90 word writing task /30. Mixed single-choice, two-choice, short-answer and sentence-completion formats. Original fictional school setting. Sources and calibration limits are in content.json and the teacher key. The practice time is 90 minutes, following Summer 2026 A; sitting-specific official durations may differ.

## Interaction

- Four reading slides, seven reading questions, writing with a word counter, final review: 14 slides total.
- Complete text available from every slide; PDF line numbers preserved on narrow screens.
- Contextual Hebrew hover / focus / tap bubbles, fading after 3.5 seconds over 1 second.
- Four prerecorded en-US-AriaNeural MP3s. No runtime TTS or external speech generation.
- Semantic chunks with 1500 ms pauses inside sentences and 2000 ms between sentences. Playback speeds 0.5, 0.75 (default), 1 and 1.25 do not change pauses.
- Uses the shared inline-reader.js/CSS module without modifying it.
- Answers saved locally under C-SCHOOL-RADIO-01-1.0.0.
- Exact recognized open answers receive credit; unknown paraphrases remain pending. Two distinct details receive separate credit, and selecting the same meaning twice earns one detail only.
- Writing always requires human or AI-assisted review. Word length alone earns no marks. Rubric category maximums: 10/8/8/4.
- Practice and exam-feedback modes. Final-only answer/key export for AI review; no automatic transmission.

## Print

files/Module-C-School-Radio.pdf — four pupil pages.
files/Module-C-School-Radio-Teacher-Key.pdf — three teacher pages.

## Build

From repository root, run tools/build_module_c_school_radio.py, then tools/build_module_c_school_radio_html.py with Python. Audio rebuilding uses tools/build_module_c_school_radio_audio.py with edge-tts 7.3.1 and ffmpeg installed, and requires network access at creation time only. Keep all JSON data, MP3 files and PDFs together when distributing the offline package.

## Validation

Rendered every final PDF page with Poppler and visually inspected layout. Verified identical text across numbered lines, translations and recording word cues; all evidence ranges, audio hashes and timings; scoring full/blank/partial/two-choice responses; unknown-answer review; writing count; and fixed-gap/pause/resume/cancellation logic. Browser and live-speaker checks were unavailable in this environment. Reading and writing level is qualitatively calibrated, not classroom-validated.
