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
- Firebase remote uses the isolated Firestore collection `teachersPresentationRemoteV1` for temporary slide state, including *technical anonymous UIDs* for host/controller authorization. No one must create a teacher account or sign in with Google. No name, email, contact data, IP or teacher profile is written by the site. The user-visible QR explains in Hebrew **and** English that the phone becomes the presentation remote (scan → approve on the computer → swipe).
- The new per-presentation launch log `teachersPresentationUsageV1` is an opt-in Firestore extension. `usage-log.js` attempts one write for each presenter page open in either remote mode; controller phone opens are excluded. Each entry has only `deck`, `kind` and `openedAt` server timestamp. These entries count **launches, not distinct teachers**. No UID is written in the log; Firebase Authentication itself issues a technical anonymous identity to authorize writes.
- The reference Firestore rules are at `/grade12/four-units/sentence-detective/FIREBASE_RULES_FRAGMENT.txt` and are **NOT deployed**. Never paste the fragment as the full Firestore ruleset; review and merge into the existing English for Noar rules, test with the Firestore Rules simulator/emulator and consider App Check/abuse controls. Configure a TTL policy for `expiresAt` in the temporary remote collection if available. The usage log is not a universal cross-site counter.
- Runtime requires **Anonymous Authentication**, an enabled **Cloud Firestore default database**, the appropriate collection-scoped Firestore rules and compatible Firebase quota. Until confirmed on the actual Firebase project, do not claim the Firebase remote or the usage log is operational live, or that English for Noar's backend has been fully audited. Failure to log must never block the presentation.
- A future rollout to other decks requires an explicit new user request. Do not automatically enable Firebase on all presentations.
