# Advanced Grammar in an Essay

Grade 11, 5-point English. Updated to Simon's Module G structure on 19 September 2026.

The 108-slide lesson preserves the existing design, 12 cat animations, timers, and question/answer and translation reveal pairs. Its sports-participation model is a 128-word for-and-against essay with exactly four paragraphs.

## Writing structure

Drafting steps: 1 neutral opening; 2 opinion with `I claim that`; 3 opposing idea; 4 first conditional; 5 support for the opinion; 6 present perfect; 7 conclusion; 8 passive; 9–10 body expansions.

Final reading order: **1,2 / 3,4,9 / 5,6,10 / 7,8**. Paragraph 2 begins `On the one hand,`; paragraph 3 begins `On the other hand,`. The second conditional is retained only as a comparison, not as the model's required conditional.

Ten cumulative essay slides show the draft and actual word count after each step. The eight-sentence draft has 107 words and is explicitly unfinished. Step 9 brings it to 118; step 10 brings it to 128. Expansions stay inside the body; there is no fifth paragraph.

Independent practice uses `Should teenagers have an after-school job?` from Simon's supplied list. The transfer example uses the fixed cellphone-age topic. Teachers ask for one sentence at a time, provide neutral starters, correct minimally, and keep the student's draft and word count visible. Required classroom vocabulary avoids `good` and `important`; choose precise alternatives by meaning.

## Files and rebuilding

- `grade11/grammar-in-an-essay/index.html`, `lesson.css`, `lesson.js`, `lesson.json`: live lesson.
- `teacher.html`: updated teacher script and model.
- `files/grammar-in-an-essay.pptx`: matching editable download.
- `build_lesson.py`: content, HTML and teacher-script generator.
- `build_pptx.mjs`: Artifact Tool builder; `fix_rtl.py` preserves Hebrew paragraph direction.

Run the content generator first. For the PPTX builder, set `ESSAY_ROOT` to the repository root, optionally set `ESSAY_BUILD_DIR` and `ESSAY_WORKSPACE` to a private task workspace, and set `ESSAY_FINAL_PPTX` to a new output path. Validate and visually review the new output before replacing the live download.

The HTML timers can start, pause, reset and add 30 seconds; leaving a slide pauses its timer. PPTX displays a time allocation and a link to the live timer. Animated GIF playback depends on the presentation software.

The supplied structure is a classroom writing scaffold. Follow the actual exam task's directions.
