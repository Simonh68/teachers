# Module E, set 2: More Than an Old School Bag

Full original practice for Grade 11, in the Bagrut Trap Killer project. Fictional museum and residents; not an official examination.

ID `E-FULL-MUSEUMBAG-02`, version `1.0.0`. The teacher saw and approved the passage before production. 388 words, 26 sentences, 5 paragraphs, 35 printed lines. Nine reading questions /70 plus five lexical matching groups /30, modeled on January 2026 Module E (16471). Practice time: 75 minutes; no dictionary.

All 30 lexical options are entries or explicitly listed family members in Band III Core I List A. See `vocabulary-audit.json` for exact spreadsheet rows. List A is the teacher's requested focus, not a claim to cover the full current E vocabulary syllabus. Definitions, questions and passage are original.

## Use

Open `index.html`; keep `audio/` and `files/` alongside it. The deck embeds all scripts, styles and data and can run offline after extraction. The class navigation link needs the live site.

21 slides: opening, five paragraphs, nine reading questions, five matching groups, summary. Full-text access from every slide; question excerpts use the final PDF line numbers. Narrow screens may wrap one numbered print line across several screen lines.

Practice mode offers checking; exam mode withholds feedback until completion. Wrong multiple-choice answers provide an optional explanation of the selected trap. Recognized open answers earn credit; unknown paraphrases stay pending teacher review. Q3 counts each distinct detail once. Q5 partial answers need review under the PDF rubric. Answers persist locally under this set's separate ID. Final-only export includes article, questions, current answers and rubric; nothing is transmitted to an AI service automatically.

Trap coverage: negation and unsupported purposes (Q1); unless and order of actions (Q2); two-part reference (Q3); residents' assumption versus the team's actual criterion and word overlap (Q4); appearance versus reason (Q5); original aim versus later benefit (Q6); action versus purpose and one family's limits (Q7); proposed versus completed action (Q8); main idea versus extreme or reversed claims (Q9). These are teaching categories, not official labels.

## Reader

All 388 words map to 62 contextual Hebrew phrase glosses. Hover, focus/Enter or tap opens a bubble; it remains for 3.5 seconds then fades for 1 second, with up to three live and three fading bubbles. Overlays do not move text.

Five prerecorded US-English MP3s, voice Aria, contain real word timing cues. No live TTS or browser speech synthesis. Sixty-two natural reading chunks across 26 sentences: 1.5-second phrase pauses and 2-second sentence pauses. Speed choices .5, .75 default, 1 and 1.25 preserve wall-clock pause duration. Pause/resume, replay, foreground-only highlighting and navigation cancellation reuse the existing shared reader unchanged.

## Files and rebuild

`files/Module-E-Museum-Bag.pdf`: 4-page student paper. `files/Module-E-Museum-Bag-Teacher-Key.pdf`: 3-page teacher key with evidence, rubrics and trap feedback.

From repo root: `python tools/build_module_e_museum_bag.py`, then `python tools/build_module_e_museum_bag_html.py`. PDF uses ReportLab and embedded DejaVu fonts. Audio rebuild: `python tools/build_module_e_museum_bag_audio.py`, with edge-tts 7.3.1 and ffmpeg installed; generation requires internet, playback does not. Reinspect PDF and all line references if text or typography changes.

## Validation

The one-page reading PDF was visually inspected before questions were written. All final student and key pages inspected; two answer lines for each open response. Evidence checked against precise numbered lines. All MP3s decoded and all 388 words aligned, with SHA-256 verification. Automated checks cover full/blank/partial scoring, distinct details, pending paraphrases, 21 slides in each mode using a DOM stub, final-only export, speed-independent pauses, pause/resume and late-play cancellation. Actual browser layout and audible playback were unavailable in this environment; no browser or listening QA is claimed.

## Sources

- Exam format model: https://files.geva.co.il/geva_website/uploads/2026/01/שאלון-16471.pdf
- List A: https://katzir.org.il/wp-content/uploads/2024/07/Band_3-List_A-_Official.xlsx
