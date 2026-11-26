# Grade 8 Translation Challenge

70 challenges, 210 fixed presentation steps. The single required key is **ArrowDown**:

1. The question appears, with all three options for multiple-choice items.
2. ArrowDown reveals a possible answer and highlights the correct option.
3. ArrowDown reveals one short grammar explanation.
4. ArrowDown opens the next question.

The first question opens immediately. There is no start button, text input, scoring, automatic timer or required answer selection. Each of the ten seven-question rounds follows **easy, core, easy, core, easy, core, challenge**. There are 30 multiple-choice items and 40 open items, with 35 source sentences in each language. Multiple-choice positions remain fixed so the PDF and the presentation match.

## Files

- `data.json`: single content source, including bilingual explanations and grammar cues.
- `index.html`, `style.css`, `app.js`: static presentation, including persistent interface language, round navigation, copy link and links back to class materials.
- `worksheet.pdf`: two A4 pages with 14 selected matching challenges.
- `answer-key.pdf`: separate two-page key.
- `build-worksheet.py`: regenerates both PDFs from the content source.

The worksheet uses challenge IDs 1, 2, 15, 16, 24, 25, 35 and 36, 39, 43, 48, 52, 55, 70. Each page preserves the seven-question difficulty cycle. PDF wording and choices come directly from `data.json`.

## Curriculum scope

This is a focused review of basic structures within Grade 8, not a complete annual syllabus: Present Simple, Present Continuous, Past Simple, future with will and going to, basic modals, and conjunctions. The harder seventh item combines familiar structures. The underlying Ministry references are:

- https://meyda.education.gov.il/files/Mazkirut_Pedagogit/English/CurriculumIntermediate2.pdf
- https://meyda.education.gov.il/files/Mazkirut_Pedagogit/English/CurriculumFilesAugust21/GrammarBandII.pdf

## Shared phone remote

The optional first-question QR launcher loads the existing `../../shared/phone-remote/remote.js` only on request. This prevents its automatic pairing panel from interrupting the required Down-Arrow-only flow. Controller URLs containing `teacherRemote` load the shared controller automatically. The presenter still approves any remote connection. `window.next`, `window.prev` and `#counter` expose the same 210-step sequence to the shared remote. Local swipe up advances and swipe down reverses one step.

## Publication

Owned source: `classroom/grade8`, under `grade8/**`. The class page links this lesson first; `grade8/manifest.json` lists the lesson first and its worksheet second so the central publisher places them at the top of the main Grade 8 section. The existing central workflow assembles the independent classroom branch. No merge into main is needed.
