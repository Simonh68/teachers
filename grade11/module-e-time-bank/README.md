# Module E: A Bank That Uses Time

Standalone full-exam supplement for **Bagrut Trap Killer**, Grade 11.

- ID: `E-FULL-TIMEBANK-01`; version `1.0.0`.
- Original fictional reading passage: 392 words, 26 sentences, 5 paragraphs, 34 printed lines.
- 9 reading questions worth 70 points: 4 multiple-choice and 5 open / completion questions.
- 5 lexical groups, each with 6 options and 3 definitions: 15 matches worth 30 points.
- All 30 lexical options were checked against Band III Core I, List A. See `vocabulary-audit.json` for the exact entry mapping. The lexical section intentionally focuses on List A at the teacher's request. This is not the full current Module E vocabulary syllabus.
- Practice time: 75 minutes, no dictionary. Original practice material, not an official MOE examination.

## Use

Open `index.html` in a browser, or use the Grade 11 website. The HTML contains its own data and scripts and works offline. Keep `files/` and `audio/` beside it for the PDF downloads and recordings. The Grade 11 navigation link requires the live site.

The deck has 21 slides: introduction, 5 reading paragraphs, 9 reading questions, 5 vocabulary groups and a summary. Each numbered screen line corresponds to a PDF line; on narrow screens that line can wrap without changing its number. A full-text dialog and per-question line excerpts allow pupils to consult the article.

Choose practice mode for immediate checking or exam mode for feedback after completion. Wrong multiple-choice answers offer an optional explanation of the selected distractor. Recognized open answers receive credit. Unrecognized paraphrases remain pending teacher review rather than being marked wrong. Question 3 awards credit for two distinct details in either order. The final screen reports confirmed points and points awaiting review, and provides the answer key. This is the score of the current answers, including any revisions.

Responses persist in local storage on the learner's device. Reset clears this exam only. No external AI call occurs. A full copy/export for teacher or AI review becomes available after finishing the final vocabulary group. The export includes all questions, student answers, evidence and the marking rubric.

## Files

- `files/Module-E-Time-Bank.pdf`: 4-page pupil paper with line numbers and questions.
- `files/Module-E-Time-Bank-Teacher-Key.pdf`: 3-page key with evidence, marking and trap explanations.
- `content.json`: canonical text, questions, accepted examples and vocabulary.
- `lines.json`: exact PDF line mapping, also embedded in the HTML.
- `template.html` and `app.js`: editable presentation source.

## Trap coverage

The tasks distinguish normal prices from time credits (Q2), complete from incomplete references (Q3), an initial assumption from the discovered reason (Q4), an example from its explanation and a negative statement from its reversal (Q5), the original motive from later benefits (Q6), a pronoun's actual referent from nearby or overly broad alternatives (Q7), a proposal from a completed action (Q8), and a qualified main message from absolute claims (Q9). Q1 also tests unsupported restrictions and assumptions about money and direct exchange. These are teaching categories, not official MOE trap labels. No claim is made to cover every trap in the larger project.

## Sources and format

The structure follows the official January 2026 Module E (16471) paper mirrored by Geva: 70 reading points, 30 lexical points and five lexical matching groups. That model has nine reading questions. Other E papers may have a different number of reading questions. The passage, questions, distractors and definitions here are original.

- Exam model: https://files.geva.co.il/geva_website/uploads/2026/01/שאלון-16471.pdf
- Vocabulary list: https://katzir.org.il/wp-content/uploads/2024/07/Band_3-List_A-_Official.xlsx

The text was shown to the teacher first. PDF layout was then rendered and inspected, locking 34 lines before the questions were written. All four pupil pages and three key pages were rendered and visually checked. Logic checks covered scoring, blank answers, two-detail partial credit, paraphrase review, and exact text/line identity. Browser interaction and responsive layout were not visually tested in this environment.

## Rebuild

From the repository root, run `python tools/build_module_e_time_bank.py`, then `python tools/build_module_e_time_bank_html.py`. The PDF builder uses ReportLab and embedded DejaVu fonts. If text or typography changes, inspect the new PDF and update every question's line references before publishing.

This supplement does not change the locked E20 question bank or other Trap Killer bank versions.

## Hover translation and recorded Read Along (2026-10-18)

The header's text button opens the complete article from all 21 slides. Each paragraph slide and each question's text excerpt also supports the reader. Hover, keyboard focus/Enter, or a phone tap on any word shows a contextual Hebrew gloss. All 392 words belong to 125 reviewed word/phrase glosses. Bubbles remain for 3.5 seconds and fade for 1 second. At most three full bubbles and three fading predecessors remain. Bubbles sit in an overlay above the text when space allows; they do not alter text geometry or printed line numbers. Hebrew support can be switched off with the translation checkbox.

Five MP3 files contain prerecorded US English narration (Aria), with real engine word cues. The web page uses recorded media only, with no browser speech synthesis and no live TTS requests. Word highlights change foreground color only. The player divides the unchanged text into 77 natural reading chunks across 26 sentences, inserting wall-clock pauses of 1.5 seconds between chunks and 2 seconds between sentences. The speed selector offers 0.5, 0.75 (default), 1 and 1.25, without changing these pause durations. Pause/resume, replay and navigation cancellation are included. Opening/closing the article or changing slides preserves the questionnaire responses and stops the previous recording.

Reader sources are `shared/read-along/inline-reader.js` and `.css`. They are opt-in and leave the existing shared engines unchanged. The HTML builder embeds these sources, `glossary.json` and `audio.json`, so the ZIP can run offline once extracted. `reading-phrases.json` defines semantic pause positions. Regenerate the five recordings with `python tools/build_module_e_time_bank_audio.py` (edge-tts 7.3.1 and ffmpeg), then rebuild the HTML. The PDF content and exam storage key stay unchanged.

Validation: all five MP3 files decoded; all 392 spoken tokens aligned to the text; every word mapped to a Hebrew gloss; phrase ranges cover every word once; fixed gap durations tested at all four playback rates; pause/resume, delayed playback cancellation and exam scoring checked. Actual browser layout and speaker playback remain unverified in this environment.
