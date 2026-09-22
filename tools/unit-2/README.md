# Unit 2 — School Years Around the World

The approved `Grade7_Story_Plan_HE.md` and the user's subsequent instructions are recorded in `APPROVED_SCOPE.md`. The user explicitly authorized publication on 22 September 2026. The unit is published at https://simonh68.github.io/teachers/grade7/unit-2/ and linked first on the Grade 7 page. Unit 1 is not modified.

## Included

- A comparative main text: school-year starts and ends, summer holidays and seasons in Japan, Alaska, Florida, England, the UAE and Jersey.
- Three classroom message adaptations based on documented journeys, distributed across three unit parts: a WhatsApp message from Argentina (South America), an email from India (Asia), and a Instagram post from the Isles of Scilly (Europe). Each has its own page, English source reference and clear adaptation label.
- Read & Listen: four recordings, 51 sentences and 23 short parts; English/Hebrew sentence pairs, contextual word help, audio word highlighting, five speeds, sentence repeat, touch navigation and local progress.
- Exactly 165 Core I records from groups 03–05, their recorded English words/examples, 165 context questions and independent sentence tasks. The coverage map distinguishes exposure from mastery.
- Present Simple A and B: 46 and 43 slides, with independent responses before feedback.
- A listening activity, a six-page student PDF with messages on pages 2, 4 and 5, a workbook answer key and a 20-slide HTML teacher guide.

## Vocabulary correction

The raw source snapshot, serial IDs, grouping, order, POS and source English definitions remain unchanged. `sources/vocabulary-corrections.json` documents 35 field corrections in 25 records; the builder also keeps each corrected Hebrew sense aligned with its gloss.

The original documentation book `E-Vocab-Band-II-Traceability-and-QA.xlsx` was corrected in place to version 4, with dated before/after notes and reasons. All 2,181 formulas and unrelated content were preserved. Software synchronization remains tracked in [E-Vocab issue #5](https://github.com/Simonh68/E-Vocab-Band-II/issues/5). See `sources/vocabulary-correction-log.md`. Do not close the software task merely because Unit 2 and the book are corrected.

## Rebuild

Run from the repository root:

```sh
python3 tools/unit-2/build_foundation.py
python3 tools/unit-2/build_reading.py
python3 tools/unit-2/build_audio.py --reading
python3 tools/unit-2/build_audio.py --vocabulary
python3 tools/unit-2/build_activities.py
python3 tools/unit-2/build_workbook.py
```

Audio builds reuse files only when their recorded text hashes match. The source audio is pre-recorded; browser speech synthesis is not used. Grammar template engines are pinned under `templates/` from revision `ee4ad42` so later Unit 1 work cannot silently change this unit. The retired poster story is not a build input.

## Verification and scope

Run `verify_revision.py`, `qa_foundation.cjs`, `qa_reading.cjs` and `qa_activities.cjs` with Node and Playwright. `UNIT2_CHROMIUM` may specify an installed Chromium executable. Each writes its corresponding JSON report. The PDF is rendered and visually inspected separately.

Jersey is the English-speaking island used in this edition. The main text uses general seasonal patterns, rounded holiday lengths and supplemental dates, with no fixed calendar year. School-year spans include shorter holidays. The messages use first-person classroom adaptations, not original messages or direct quotations. See `sources/seasonal-calendar-review.md`.

## Meeting index and local checklist

The main unit page now organizes the materials into nine double meetings. Each meeting links to student preparation, the corresponding slides in the 27-slide HTML meeting guide, and four lesson activities. The existing twelve-component resource catalogue is retained at `resources.html`. The printable student preparation sheet is `student-preparation.html`; teacher guidance is `meeting-guide.html`.

Native HTML checkboxes mark activities or whole meetings as completed. Link colour and an Opened badge separately show links opened from the index; opening a link never completes an activity. State is stored only under `teachers-unit2-meetings-v1` in localStorage. No checklist data is transmitted or synced between devices. Clearing browser data removes it. Blocked storage gets an explicit warning and an in-memory fallback. Student readiness ticks are separate from completed lesson activities.

`build_sessions.py` builds the index, preparation sheet and meeting guide without rewriting the texts, recordings or workbook. `build_foundation.py` also calls it to preserve the organization on future rebuilds. The nine vocabulary links open the first unrevealed slide of the specified entry range. Three batches cover each of groups 03–05 without changing any source record.

`qa_meetings.cjs` checks desktop and two mobile sizes, all 27 teacher-guide slides, four-direction touch navigation, link/checkbox independence, reload and browser-restart persistence, separate-browser isolation, blocked/corrupt storage, exact vocabulary start positions and zero network traffic when ticking a box.
