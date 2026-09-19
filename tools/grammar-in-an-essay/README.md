# Advanced Grammar in an Essay

Grade 11, 5-point English. Simplified at Simon’s request after classroom review.

## Current lesson

50 slides and 72 planned minutes, including three short existing animations, 14 minutes of independent writing and 3 minutes of editing. In a 90-minute meeting, 18 minutes remain for unscheduled interruptions and transitions. The previous 108-slide version remains in Git history.

The model uses 123 words in four paragraphs. Topic vocabulary is deliberately familiar: games, play, team, friends, help, mistakes. Reusable connectors and structures carry the challenge: I claim that; On the one hand; On the other hand; since; For example; Moreover; In conclusion; Therefore. Since expresses a reason; no automatic scoring benefit over because is claimed.

First Conditional, Present Perfect and modal Passive remain. Gerunds occur naturally; the separate Second Conditional lesson and repeated explanations have been removed.

## Writing sequence

Ten short independent sentence attempts alternate with cumulative model reveals and actual word counts. Drafting order: opening, opinion, opposing idea, conditional with reason, supporting idea, previous experience, conclusion, passive recommendation, two body expansions. Final paragraph order: 1,2 / 3,4,9 / 5,6,10 / 7,8. The 8-sentence draft has 100 words; the expansions bring it to 111, then 123. Read only the new sentence at each cumulative reveal.

Independent practice: Should teenagers have an after-school job? Keep simple topic vocabulary and develop the ideas. Give content feedback first, then at most two key corrections. This is a teaching scaffold, not a guaranteed examination score.

## Files and rebuilding

- grade11/grammar-in-an-essay/: HTML, CSS, JS, lesson.json and teacher.html.
- files/grammar-in-an-essay.pptx: matching editable presentation.
- build_lesson.py: content and HTML generator; reuses the established player and visual style.
- build_pptx.mjs and fix_rtl.py: Artifact Tool builder and Hebrew direction repair.

Run the content generator first. Copy the PPTX builder and fix_rtl.py into a private build directory with the supplied runtime dependencies. Set ESSAY_ROOT, ESSAY_BUILD_DIR, ESSAY_WORKSPACE and ESSAY_FINAL_PPTX to task paths. Finalize to a new output, verify it, then replace the site download unchanged. HTML timers are interactive; PPTX timers are allocations with links to the live timers. GIF playback depends on the presentation application.

## Progress and English edition

The left sidebar shows the complete ten-sentence route from the first slide. Counts refer to the model essay, not to student drafts. Prompts highlight the sentence being attempted; reveals advance the completed count. Counts are derived from the model text: 14, 25, 37, 53, 67, 79, 91, 100, 111, 123. Backward navigation and direct links restore the exact state. Independent work retains the completed model count.

Both prompt and reveal headings use English ordinals. `versions.py`, called by `build_lesson.py`, adds metadata and generates `english.html`, `lesson.en.json` and `teacher.en.html` alongside the bilingual edition. The language switch preserves the current slide. English instructions, explanations, controls, alt text and teacher notes are translated. The essay, sequence, fifty slides and 72-minute plan are identical.

Build the English PPTX with `ESSAY_LANG=en` and its own private build directory and final filename `grammar-in-an-essay-en.pptx`. Both PPTXs have a native editable progress sidebar on every slide. Use a workspace parent containing both the private build and final output directories.
