# Advanced Grammar in an Essay

Grade 11, 5-point English. Follow-up to the completed Advanced Grammar lesson.

The lesson has 96 slides, including 12 silent three-frame cat animations, stable question/answer and translation pairs, and five timed activities. The full model opinion essay contains 125 words in four paragraphs. The writing topic is inclusion in class sports games; independent transfer practice asks about changing partners in class.

Live materials: `/grade11/grammar-in-an-essay/`. The class hub and the Grade 11 five-point library link directly to the lesson. Downloads use the label `PPTX`.

## Pedagogy

- Build an opinion and two distinct reasons before adding grammar.
- Develop each reason with explanation and a relevant example.
- Teach gerunds, modal passive, present perfect, first/second conditionals and connectors through the same essay.
- All gaps have options on the question slide and the correct choice only on the next, visually stable slide.
- Four paragraphs and four different advanced structures are classroom practice targets. They are not presented as an official minimum for every task.
- The 120–140 word range follows published Module G tasks from 2026. Topics and model writing are original classroom practice.
- Full route: about 90 minutes. The teacher script gives an 80-minute adaptation and a natural break for a further lesson.

## Files

- `index.html`, `lesson.css`, `lesson.js`, `lesson.json`: editable HTML lesson and content.
- `teacher.html`: full teacher script and timing guidance.
- `files/grammar-in-an-essay.pptx`: all 96 slides with editable text, notes and embedded animated GIFs.
- `assets/`: Teachers cat sprite strips, derived GIFs and Heebo/Nunito fonts.
- `preview.html`: development preview and geometry audit at four viewport sizes. Not linked from student pages.

The HTML timers support start, pause, reset and +30 seconds. They stop when leaving a slide and never advance slides automatically. Animations respect reduced motion and stop on exit. PPTX has static time allocations and a hyperlink to the corresponding live timer; animated GIF playback depends on the presentation software.

## Rebuilding

Use the installed Codex primary runtime and the Presentations skill. `build_lesson.py` generates content, HTML and the teacher script. `build_pptx.mjs` uses `@oai/artifact-tool`; `fix_rtl.py` preserves Hebrew paragraph direction in the exported package. Finalize and visually inspect a new output path before copying it into `files/`.

The cat artwork was originally generated for Teachers. Each scene is used once in this lesson with a new grammar-related caption. The originals are preserved. GIF derivatives contain three cropped frames with 0.6 seconds per frame, repeated six times.

Source for writing length: https://meyda.education.gov.il/sheeloney_bagrut/pitronot_bagrut/2026/6/016582-8-HEB-1400-1600.pdf
