# Monkey Festival lesson build sources

Source and delivery files for the Grade 8 Zoom lesson on 14 September 2026.

The lesson content is also stored in `grade8/monkey-festival/lesson.json`.
The scripts were executed in the Codex primary runtime with `@oai/artifact-tool`, ReportLab, Nunito and Heebo installed.
Run the scripts from this repository: `author_content.py`, `build_html.py`, `build_pdf.py`, then `build_pptx.mjs`. The HTML builder updates the existing class card in place. The image assets are already stored under the lesson's `assets/` directory.
Use the primary runtime's Python and Node executables, and make `@oai/artifact-tool` available to Node. Set `LESSON_BUILD_ROOT` to a temporary build directory and `FINAL_PPTX` to a new output path. Copy the verified PPTX to `grade8/monkey-festival/files/monkey-festival.pptx` only after finalization.
`fix_rtl.py` sets native OOXML Hebrew paragraph direction after artifact-tool export. Verify mixed-direction text in an office renderer before replacing the final PPTX.
Use a new final output path via `FINAL_PPTX` when rebuilding; the finalizer will not overwrite an existing finalized output.

Pupil-facing dates use weekday, Hebrew date and Gregorian date in parentheses. Time ranges are isolated left-to-right. The reading image and the original exam questions are separately linked in `lesson.json`; the upcoming test syllabus is not inferred from either source. `preview.html` checks all 70 slides at four viewport sizes and exercises navigation.
