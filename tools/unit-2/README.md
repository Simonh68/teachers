# Unit 2 — School Years Around the World

The approved `Grade7_Story_Plan_HE.md` and the user's subsequent instructions are recorded in `APPROVED_SCOPE.md`. The unit remains a complete teacher-review draft; student publication is a separate step. Unit 1 is not modified.

## Included

- A comparative main text: school-year starts and ends, summer holidays and seasons in Japan, Alaska, Florida, England, the UAE and Jersey.
- Five documentary companion texts: an Anchorage snow day, a horse journey in Argentina, Samuel's wheelchair journey in India, a school boat in the Isles of Scilly, and Barcelona's bike bus. Each has an English source reference; the two press photographs have English captions and credits.
- Read & Listen: six recordings, 63 sentences and 28 short parts; English/Hebrew sentence pairs, contextual word help, audio word highlighting, five speeds, sentence repeat, touch navigation and local progress.
- Exactly 165 Core I records from groups 03–05, their recorded English words/examples, 165 context questions and independent sentence tasks. The coverage map distinguishes exposure from mastery.
- Present Simple A and B: 46 and 43 slides, with independent responses before feedback.
- A listening activity, a four-page student PDF, a workbook answer key and a 20-slide HTML teacher guide.

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

## Verification and remaining review

Run `qa_foundation.cjs`, `qa_reading.cjs` and `qa_activities.cjs` with Node and Playwright. `UNIT2_CHROMIUM` may specify an installed Chromium executable. Each writes its corresponding JSON report. The PDF is rendered and visually inspected separately.

Jersey is the proposed English-speaking island. Florida's summer length is explicitly a summer 2026 example; other dated summer examples are 2027. Calendars are local examples, not universal country-wide dates. Documentary routines refer to their stated source dates; historical present does not imply current conditions. These scope choices remain visible for teacher review.
