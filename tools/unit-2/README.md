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

The main unit page organizes the materials into four dated double meetings: 29 October and 1, 5, 8 November 2026, 12:00–13:20. The 25 October school trip and 12 November exam are excluded. Each meeting has 64 active minutes within its actual 80-minute slot, four class activities and three 15-minute home rounds. The HTML teacher guide has 12 slides. The existing twelve-component resource catalogue is retained at `resources.html`. Preparation and home review are in `student-preparation.html`; teacher guidance is in `meeting-guide.html`. Calendar evidence and workload decisions are in `sources/meeting-calendar-review.md`.

Native HTML checkboxes mark activities or classwork for whole meetings as completed. Home-round and Ready checkboxes are separate; class bulk completion never completes homework. Link colour and an Opened badge separately show links opened from the index. Reset history and Restore history affect opened markers only. State remains under `teachers-unit2-meetings-v1` in localStorage; no data is transmitted or synced. Earlier IDs, checkboxes and guide positions remain usable through `earlier-meetings.html`, `earlier-preparation.html` and `earlier-guide.html`. New dated activities use date IDs and never inherit completion from differently scoped earlier tasks. Clearing browser data removes local progress; blocked storage has an explicit notice and in-memory fallback.

`dated_meetings.py` holds the allocation; `build_sessions.py` builds the index, preparation sheet and teacher guide without rewriting texts, recordings or workbook. `build_foundation.py` calls it on future rebuilds. Vocabulary batches are 42/41/41/41, covering all 165 records in order without changing their content. Home rounds cover 14/14/14 or 14/14/13 records. Vocabulary links open the exact first unrevealed slide; context-practice links use `item` and `end` to restrict each home round to its assigned global range, including boundaries between practice sets.

Run `qa_dated_meetings.cjs` (also available through `qa_meetings.cjs` and `qa_history.cjs`). It checks date/count/time consistency, exact 165-record class/home coverage, all 12 bounded context ranges, all vocabulary start positions, desktop and two mobile sizes, the 12-slide teacher guide and four touch directions, class/home/Ready independence, earlier state/archive preservation, history reset/restore, cross-tab and browser-restart persistence, isolation and blocked storage. Earlier JSON reports describe earlier releases.
