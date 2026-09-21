# Unit 1 — The Same Way

Hub: grade7/unit-1/index.html. All existing resources keep their original URLs and creation dates.

- build_content.py -> reading/content.json and data.js (two texts, 18 sentences, questions and evidence).
- build_pdf.py -> files/reading-workshop.pdf, 2 A4 pages, uses the same canonical texts. Requires reportlab and python-bidi. Includes black-and-white vector umbrella/bus illustrations; no remote assets.
- build_hub.py -> hub, teacher HTML presentation/data and grade7 index card. Teacher deck has 30 slides with the whole unit plan and keys.
- reading/lesson.js and lesson.css are maintained source, adapted from the verified grammar engine. 94 complete-deck slides; ?mode=home selects the shorter independent route. Word translations, paired reveal geometry, folder tabs and four-direction navigation are supported.

## Pending audio approval
Automatic approval review rejected sending the two new, not-yet-public texts to Microsoft speech.platform.bing.com using edge-tts. Do not retry or use a workaround without new explicit approval. No speech request should be made by the student browser. The current UI honestly labels new narration as pending and disables its buttons; existing unit resources retain their original recordings.

After approval: build_audio.py creates en-US-BrianNeural +10Hz recordings and WordBoundary cues. Validate numeric-token alignment for times, every sentence and translation slide, reader boundaries, pause/continue, persisted speed, and cancellation before enabling audioAvailable in lesson.js. Replace the placeholder Promise.resolve(null) with the audio.json fetch and update UI pending labels in build_hub.py. Do not claim the new audio is complete before actual playback tests.

## QA performed
94 slides at 1366x900, 1024x768, 390x844, 360x640; complete sentence-pair geometry; reader fit and all tooltips; every quiz right/wrong feedback, evidence and unrestricted forward navigation; genuine four-direction touch; hub links and clipboard; teacher deck navigation; two-page PDF rendering and exact served hash. Tests in /workspace/scratch/a8004f58ea11/qa-unit1.cjs.

The unit is a local teaching plan, not a ministry-approved hour allocation. A2 source is linked in the teacher deck. Exam assets remain in Drive; no exam content is copied into the public repo.
