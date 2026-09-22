# Unit 2 publication checkpoint

Published on 22 September 2026 following the user’s explicit instruction.

- Unit: https://simonh68.github.io/teachers/grade7/unit-2/
- Grade 7 page: https://simonh68.github.io/teachers/grade7/ — Unit 2 appears first; Unit 1 remains available.
- Initial published main commit: `916221300a58e3e37087b687769326577dcb43b5`.
- Initial deployment: successful GitHub Pages run 35675524395.
- Initial public verification: all 13 HTML pages and all 174 media/download files matched local checked files, including all 171 MP3 files. Live Read & Listen playback and menu pause passed on a 390×844 viewport.
- Acceptance checks before publication: three viewports, all unit components, complete grammar/vocabulary decks and reading sentence pairs, touch navigation, answer feedback and clipboard links.
- Detailed verification scope and environment notes: `publication-qa-report.json`.

The original vocabulary documentation book is corrected to version 4. E-Vocab software synchronization remains open under https://github.com/Simonh68/E-Vocab-Band-II/issues/5. Publication of Unit 2 does not close that separate task.

The draft branch retains this post-publication QA checkpoint. Future student-facing edits should start from current main and preserve other units.

## Seasonal reading and three message formats

The follow-up revision replaces fixed-year calendar examples with general seasonal patterns. Three separate classroom messages are distributed through the unit: WhatsApp from Argentina, email from India, and Instagram from the Isles of Scilly. All four reading recordings and contextual translations match the revised text. The workbook has six pages and ends with a reply-writing task.

Local acceptance: 23 reading parts and 51 English/Hebrew sentence pairs at three viewports, 102 automatic sentence plays, 165 vocabulary context tasks, all unit links, six live reading clip plays, and all source-audio hashes passed. The PDF was rendered and all six pages were inspected. Detailed reports: `reading-qa-report.json`, `activities-qa-report.json`, `release-qa-report.json` and `revision-qa-report.json`. Earlier release reports above describe the initial edition. Public verification of this revision is recorded separately after deployment.

Revision published on `main` at `56fe630e1da7850da804315c9a9f2a0b7729a605`; GitHub Pages deployment 35693935262 completed successfully. All 26 changed public unit files matched the checked local bytes, including the PDF and all four revised recordings. The live Instagram reader loaded the four-text edition at 390×844, played at 0.75× and paused on opening the menu, with no script errors. See `published-revision-qa-report.json` and `live-revision-browser-report.json`. The final short calendar-span wording was rechecked with `reading-layout-qa-report.json` and the exact-text audio checks in `revision-qa-report.json`.

## Meeting index and private checklist

Published at `1477aa58d0832e5c65b673ff74e0a0b44b3cd92c`; GitHub Pages run 35696381861 completed successfully. The main unit page now has nine meeting sections with 36 native activity checkboxes. The student preparation sheet and 27-slide HTML meeting guide follow the same sequence. Opened links and completed activities are independent. Progress is local to the browser and device.

All nine changed public files matched their local hashes. Live mobile checks at 390×844 confirmed checkbox persistence after reload, the correct Meeting 3 guide link, opened-link feedback after returning, and separately saved student preparation readiness. No script errors occurred. Local QA additionally verified actual browser restart, isolated browser contexts, blocked/corrupt storage, zero network requests for checkbox changes, every vocabulary start position and all guide slides/touch directions. See `meetings-qa-report.json`, `meetings-public-qa-report.json` and `meetings-live-browser-report.json`.

## Reset and restore opened-link history

The meeting index now offers Reset history and Restore history. These controls affect the unit's Opened markers and Last opened indicator. Completed activities and Ready checkboxes are independent. Cleared markers are backed up only in the same browser; restoring merges them with links opened afterwards. Repeated resets retain previously cleared markers until restoration. Native visited-link colours are overridden for tracked links so reset markers return to their original colour. The browser's own browsing history is not modified.

Existing version-1 checklist data is retained. Both checklist pages load versioned assets to receive the updated state reader. Local acceptance passed at 1366×900, 390×844 and 360×640: reset/restore, completion/readiness preservation, new visits and repeated resets, cross-page/tab updates, reload and browser restart, keyboard operation, blocked storage and browser isolation. Neither control sends network requests. See `qa_history.cjs` and `history-qa-report.json`. Public deployment verification is recorded after release.

Published at `a4c6369a278df0534db123b99cc8f3a597a62712`; GitHub Pages run 35700268107 completed successfully. All four changed public files matched local bytes. Live mobile checks at 390×844 passed opening a guide, resetting its marker, restoring after reload, persisting the restored history and preserving completion. No script errors occurred. See `history-public-qa-report.json`.

## Four dated meetings and balanced class/home work

The actual calendar replaces the earlier nine-meeting proposal with four double meetings: 29 October and 1, 5, 8 November 2026. Each is 12:00–13:20 (80 minutes), with 64 active minutes and 16 minutes for transitions. Vocabulary is allocated 42/41/41/41; all 165 original records are included once. Each date has four class activities, skills, exact links and three 15-minute home-review rounds. The 12-slide HTML teacher guide and preparation page follow the same dates. Context practice opens and stops at the precise home assignment, including practice-set boundaries. Earlier checklists and guide positions remain accessible with previous progress.

Local acceptance passed at 1366×900, 390×844 and 360×640. Checks cover exact calendar and workload totals, full vocabulary coverage, all 12 bounded practice ranges, all vocabulary links, guide layout and four-way touch, class/home/Ready independence, legacy progress, history controls, cross-tab and browser-restart persistence, blocked storage and browser isolation. See `dated-meetings-qa-report.json`. Public verification follows deployment.
