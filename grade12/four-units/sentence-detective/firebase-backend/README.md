# Firebase backend — Grade 12 Sentence Detective

**Firebase project:** `vocabdev-56392` (also used by English for Noar).

## Live setup (2026-11-01)

- Firestore `(default)` database: `me-west1` (Tel Aviv), Standard edition, free-tier eligible, delete protection enabled.
- Authentication: Anonymous provider enabled. No teacher sign-up, names or emails are requested. Firebase itself creates technical anonymous UIDs for security checks.
- The exact `firestore.rules` and `firestore.indexes.json` in this directory were deployed to this new database. Rules deny access to unrelated collections.
- Temporary pairing sessions and unapproved join requests expire after four hours; TTL policies on their `expiresAt` fields remove stale documents asynchronously.
- Three collection groups: `teachersPresentationRemoteV1`, `teachersPresentationUsageV1`, and `teachersPresentationStatsV1`.
- Usage events contain only `deck`, `kind`, `openedAt`. The public aggregate contains `deck`, `opens`, `updatedAt`, and a random `lastEventId` to validate atomic batches. No user details are in these documents.
- The public report is `../usage-report.html`. Counts launches, not unique teachers; QA launches may be included.
- The Firebase QR remote is the default for this one deck. PeerJS fallback: `?sync=peer`. Existing no-`sync` PeerJS phone URLs with a `remote` parameter remain compatible.

## Safe deployment

Only deploy after reviewing the current production rules and confirming that English for Noar has not added its own Firestore collections.

```powershell
firebase deploy --only firestore --project vocabdev-56392
```

To enable only the anonymous Authentication provider from this directory:

```powershell
firebase deploy --only auth --project vocabdev-56392
```

**Never** deploy a permissive `firebase init` sample rules file or overwrite the project-wide rules without merging future changes.

## Verification

- A real two-browser QR test passed: phone approval, navigation both ways, hint reveal, and anonymous launch logging.
- The GitHub Actions workflow `grade12-firebase-live-qa.yml` verified the atomic launch counter, denied listing of private events, and denied unrelated writes. Manual reruns require confirmation because they add a test event.
- The read-only `grade12-and-englishfornoar-smoke.yml` verified HTTP 200 for the Grade 12 deck, usage report, English for Noar homepage and Module E pages.
- Monitor the shared project's Firebase usage and billing. Before expanding to other decks, consider App Check and abuse protection.
