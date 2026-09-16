# Grade 9 — The Message Without a Voice: exam practice

Approved 60-slide lesson for Wednesday, 16 September 2026, 10:25–11:45.
Follows `/PROJECT_CHARTER.md`: To Be design system, Heebo/Nunito, Hebrew student dates, stable question/answer pairs, class-home link and accessible keyboard/wheel/touch navigation.

Deliverables are under `/grade9/message-exam-practice/`:
- `index.html`: student deck, 60 slides and 12 silent three-frame animations.
- `lesson.css`, `lesson.js`: lesson-specific styles and animation controls.
- `teacher.html`: 80-minute script, sources and answer key.
- `files/message-exam-practice.pdf`: three-page printable student worksheet.
- `lesson.json`, `story.json`: editable content and source story.
- `assets/*.webp`: 12 generated sprite strips, each three equal square frames.

Each gap question displays three options immediately. The following slide preserves geometry and reveals the correct answer. This rule is also recorded in the project charter.

Sources: Grade 9 opening deck (Core I groups 01–02, exact examples/translations), the original story in the class log, and the published Grade 9 exam calendar. The story is practice material, not a promise about the forthcoming exam text. The writing length is a practice instruction, not a confirmed exam specification.

`build_lesson.py` authors the deck, lesson JSON and teacher page. `build_pdf.py` creates the worksheet using ReportLab and static Nunito font instances. Supply `Nunito-Variable.ttf` in `tools/message-exam-practice/fonts/`, or adapt the font path to a local licensed font. Runtime dependencies are the shared `/assets/lesson-decks/deck.css` and `deck.js`.

`preview.html` provides four viewport sizes, navigation to any slide, a DOM geometry audit of all 60 slides, stable-pair checks and a live animation-frame check. It is a development tool and is not linked from the student deck.

Image provenance: original images generated for this lesson. Three complete frames share the same characters, scale, baseline and deep navy background, with no text or logos. Delivery copies are WebP at 1536 × 512. CSS presents one frame at a time; nothing advances the slide automatically. Animation stops on exit and honors reduced-motion preferences.
