# Teachers shared standards

## Deck standard
Canonical runtime:
- /shared/deck/standard.js
- /shared/deck/standard.css

Existing presentations that still load /assets/lesson-decks/deck.js or deck.css automatically route to the shared standard through compatibility wrappers. New presentations should load /shared/deck/standard.js and /shared/deck/standard.css directly.

Presentation files should contain content and presentation-specific configuration only. Navigation, keyboard control, swipe/wheel behavior, fitting, progress, common layout, reveal stability and media controls belong in the shared standard.

## Read Along standard
Canonical runtime:
- /shared/read-along/standard.css
- /shared/read-along/track-engine.js — prerecorded continuous-track audio
- /shared/read-along/phrase-player.js + segmented-engine.js — prerecorded segmented audio

Local units keep only content, translations, timing/alignment data, audio files and configuration. Shared behavior must not be copied into a grade/unit directory.

## Rule
Content local; behavior central.

A feature change requested as a standard change must be implemented under /shared first. Local overrides are permitted only when the lesson genuinely requires different behavior.

## Firebase for presentation remote control (opt-in, 2026-11-01)

- Shared, public-only Firebase Web App configuration: `/shared/firebase-config.js` for the existing `vocabdev-56392` project (project number `858434938577`). Never ask Simon to re-enter this configuration for another presentation.
- This Firebase project also belongs to the separate **English for Noar** project. Do not modify its Firestore rules, Authentication providers, other collections, apps, users, or data without auditing its live configuration and confirming that existing access is preserved.
- The **only** presentation with an experimental Firebase remote is `/grade12/four-units/sentence-detective/`, via `?sync=firebase` / the "בדיקת Firebase" button. The prior PeerJS pairing remains the default.
- Firebase remote stores only transient slide state in the isolated collection `teachersPresentationRemoteV1`. The reference security rules are at `/grade12/four-units/sentence-detective/FIREBASE_RULES_FRAGMENT.txt` and are **NOT deployed**. Never paste the fragment as the full Firestore ruleset; merge and test against the existing rules first.
- Runtime requires Firebase Anonymous Authentication and appropriate collection-scoped Firestore rules. Until these are confirmed on the actual Firebase project, do not claim that the Firebase route works live or that the English for Noar backend was fully audited.
- A future rollout to other decks requires an explicit new user request. Do not automatically enable Firebase on all presentations.
