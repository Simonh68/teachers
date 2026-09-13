# Monkey Festival lesson build sources

Source and delivery files for the Grade 8 Zoom lesson on 14 September 2026.

The lesson content is also stored in `grade8/monkey-festival/lesson.json`.
The scripts were executed in the Codex primary runtime with `@oai/artifact-tool`, ReportLab, Nunito and Heebo installed.
To rerun in the same build workspace, place these scripts at its root, and place the repository under `repo/`. Supply `grade8-index.html` from the prior class index when regenerating the card.
Run `author_content.py`, `build_html.py`, `build_pdf.py`, then `build_pptx.mjs`. Provide generated image assets under the lesson's `assets/` directory.
`fix_rtl.py` sets native OOXML Hebrew paragraph direction after artifact-tool export. Verify mixed-direction text in an office renderer before replacing the final PPTX.
Use a new final output path via `FINAL_PPTX` when rebuilding; the finalizer will not overwrite an existing finalized output.
