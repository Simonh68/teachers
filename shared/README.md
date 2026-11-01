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

## Firebase for presentation remote control (Grade 12 pilot, 2026-11-01)

- Public Firebase Web App configuration: `/shared/firebase-config.js` for project `vocabdev-56392` (project number `858434938577`). Never ask Simon to re-enter this configuration for future decks.
- A single shared anonymous-auth promise in `/shared/firebase-anonymous-auth.js` prevents the phone remote and usage logger from accidentally signing in with different technical UIDs.
- Firebase Firestore was **newly enabled** on the existing Firebase project, with a new `(default)` database in `me-west1` (Tel Aviv), Standard edition, free-tier eligible and with delete protection enabled. No pre-existing Firestore or Realtime Database instances were found when provisioning.
- **Firebase Anonymous Authentication** was enabled. Teachers do not create accounts, enter names or email addresses, or sign in with Google. Firebase itself issues anonymous technical UIDs to authorize temporary remote sessions; these are not written to the usage log. Do not describe this as the absence of technical Firebase Auth records.
- The `/grade12/four-units/sentence-detective/` presentation retains the existing Firebase remote pilot; other Teachers presentations are covered by the central QR remote standard as they are rolled out. **Firebase is now the default** on the presentation's ordinary URL, and the QR explicitly links to `?sync=firebase&remote=...`. The original PeerJS remote is available via `?sync=peer` / the pairing-screen "Alternate remote" button. Legacy `?remote=...` PeerJS QR links remain compatible. Other decks are unchanged.
- The bilingual QR explains the use of the code in Hebrew and English (scan with phone, approve on computer, swipe to navigate and reveal hints). The phone is not a second counted presentation launch.
- Firestore security rules and TTL policies were **deployed**. The exact versioned configuration is in `/grade12/four-units/sentence-detective/firebase-backend/` (firebase.json, firestore.rules, firestore.indexes.json). Do not deploy the obsolete `FIREBASE_RULES_FRAGMENT.txt`.
- Three isolated collections: `teachersPresentationRemoteV1` (temporary state and anonymous technical UIDs), `teachersPresentationUsageV1` (append-only anonymous launch events with only deck/kind/openedAt), and `teachersPresentationStatsV1` (public aggregate count, no personal data). Temporary session and join-request documents have `expiresAt` TTL policies.
- `usage-log.js` counts one presenter-tab launch, not distinct teachers. Refreshes and switching remote modes in the same tab do not add an event; QR phone controller openings are excluded. An atomic Firestore batch creates the event and increments the public count. `usage-report.html` shows the total and last update in Hebrew and English.
- This project is **also used by English for Noar**. No English for Noar repository, learning collection, or existing Firestore database was modified; the new Firestore service and anonymous Auth provider were added to the shared Firebase project. Monitor quotas and billing. Since the presentation is public and allows anonymous access, consider Firebase App Check and abuse monitoring before rolling out widely.
- The user explicitly requested QR remote rollout to all Teachers presentation decks on 2026-11-01. The shared QR remote is independent of expanding Firebase rules: do not claim Firestore supports new decks without deployment verification. Use the central compatibility adapter in `/shared/phone-remote/`, respect the already-paired Firebase/PeerJS decks, and automatically attach the remote to future slide decks.

## All-presentation QR remote standard (2026-11-01)

See `PROJECT_CHARTER.md` (mandatory QR phone remote policy). The shared overlay uses a temporary pairing code plus explicit on-computer approval; no teacher registration. Student material and slide rendering remain untouched. All class deck entry points are handled by automatic rollout and an inventory report.
