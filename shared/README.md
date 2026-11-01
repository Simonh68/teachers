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
- Only the `/grade12/four-units/sentence-detective/` presentation has this feature. The Firebase mode is `?sync=firebase` (also accessible via the pairing screen); the original PeerJS remote remains the default and fallback. Other decks are unchanged.
- The bilingual QR explains the use of the code in Hebrew and English (scan with phone, approve on computer, swipe to navigate and reveal hints). The phone is not a second counted presentation launch.
- Firestore security rules and TTL policies were **deployed**. The exact versioned configuration is in `/grade12/four-units/sentence-detective/firebase-backend/` (firebase.json, firestore.rules, firestore.indexes.json). Do not deploy the obsolete `FIREBASE_RULES_FRAGMENT.txt`.
- Three isolated collections: `teachersPresentationRemoteV1` (temporary state and anonymous technical UIDs), `teachersPresentationUsageV1` (append-only anonymous launch events with only deck/kind/openedAt), and `teachersPresentationStatsV1` (public aggregate count, no personal data). Temporary session and join-request documents have `expiresAt` TTL policies.
- `usage-log.js` counts one presenter-tab launch, not distinct teachers. Refreshes and switching remote modes in the same tab do not add an event; QR phone controller openings are excluded. An atomic Firestore batch creates the event and increments the public count. `usage-report.html` shows the total and last update in Hebrew and English.
- This project is **also used by English for Noar**. No English for Noar repository, learning collection, or existing Firestore database was modified; the new Firestore service and anonymous Auth provider were added to the shared Firebase project. Monitor quotas and billing. Since the presentation is public and allows anonymous access, consider Firebase App Check and abuse monitoring before rolling out widely.
- A future rollout to other decks requires an explicit user request. Do not automatically enable Firebase across all presentations.
