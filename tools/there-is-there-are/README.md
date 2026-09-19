# Grade 7 — There is / There are

HTML lesson: `grade7/there-is-there-are/index.html`.
Canonical content: `content.json`; generated browser data: `data.js`.

Run `python tools/there-is-there-are/build_content.py` after editing the source.
If sentence text changes, run `python tools/there-is-there-are/build_audio.py`
(edge-tts 7.2.8) and verify all new cues against the exact displayed tokens.
The MP3 is prerecorded, with the same Brian voice and +10Hz pitch approved in
The Same Way. No browser TTS. Existing Teachers fonts and nature assets are reused.

148 slides: 34 sentence/translation pairs; 21 question/feedback pairs;
worked examples, vocabulary support, two summaries, four open tasks and reviews,
full reading text, and explicit boundary/retrieval restart between two meetings.

Selected words are traced to `grade7/band2-groups-01-02/entries.json`.
Group 01: drawer, Bible, break, explanation.
Group 02: soccer, history, piano, exercise, mouse, lock.
Their teaching status is not inferred from being present in the vocabulary bank.
Teacher notes contain the schedule, accepted alternative answers and rationale.

Validation before publication: every slide at 1366×900, 1024×768, 390×844,
360×640; stable English sentence geometry on translation reveals; stable question
geometry; right/wrong feedback for all questions; genuine four-direction CDP
touch gestures and free forward movement from feedback; word tooltips; actual
playback of all 68 sentence slides with engine word highlighting and stop on
navigation; persistent rate at 0.25 and default 0.75; all 223 word timings,
translations and audio hash. Verify live URL and first Grade 7 card after deploy.
