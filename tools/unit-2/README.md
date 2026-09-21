# Unit 2 — School Years Around the World

The current Grade7_Story_Plan_HE.md was successfully read. APPROVED_SCOPE.md records the source and the user's subsequent directions. Earlier connection failures no longer block work.

Run `python3 tools/unit-2/build_foundation.py` from the repository root. This builds the review draft at `grade7/unit-2/` using Unit 1's HTML engines and the exact 165 vocabulary records in groups 03–05. No Unit 1 files are changed.

The committed `templates/` snapshot pins the engines from revision `ee4ad42`, so later Unit 1 audio work cannot silently enable unbuilt Unit 2 audio when regenerating this draft.

The draft contains two Present Simple decks, the vocabulary deck, a main comparative text with scoped school calendars, five sourced companion texts, printable exercises, and an HTML teacher presentation. The latest companion text follows a real school day disrupted by snow in Anchorage. English present tense sometimes narrates a dated historical event; source notes distinguish this from current routine.

The main text covers school-year start and end, summer-holiday length and seasons. Jersey is a proposed English-speaking island. Florida's holiday length is explicitly a summer 2026 example; other exact summer examples are 2027. These are local calendars, not country-wide universal dates.

This is a teacher review draft, not a finished student unit. Remaining gates are tracked in `grade7/unit-2/build-report.json`: recorded audio, full Read Alone support, documented vocabulary corrections, contextual vocabulary coverage, listening work, final worksheet PDF and student publication.

The old poster-story draft is retired and is not imported. Source vocabulary fields are preserved; identified source errors must be corrected through a documented transformation before student delivery.

Two inspected source photographs have credits in `grade7/unit-2/assets/CREDITS.md`. Real published names are retained. The snow photograph shows the setting, not Kali; the Barcelona photo does not identify each rider.

Draft browser QA is reproducible with `node tools/unit-2/qa_foundation.cjs` and Playwright. Set `UNIT2_CHROMIUM` to an installed Chromium executable if required. Results are in `qa-report.json`. These checks do not substitute for the remaining audio and Read Alone acceptance gates.
