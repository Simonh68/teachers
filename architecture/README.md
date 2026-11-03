# Manifest-based publication migration (staging)
This branch is intentionally NOT deployed. The existing root index.html and GitHub Pages settings remain unchanged.

## Invariants
- Each grade owns only gradeN/**, including gradeN/manifest.json.
- Shared shell, workflow and publisher live in a separately controlled integration branch.
- The deployed site is built from pinned revisions; never merge grade histories into main.
- No direct pushes from grade workflows to main.
- No student data, scans, grades or identities in public artifacts.
- The publisher must preserve all existing public paths and use the last successful artifacts for other grades.
- Release is blocked until manifests for all grades are migrated, all existing links inventoried, Pages settings verified, and a staging browser smoke test passes.

## Next work
1. Inventory all existing cards, including Unit 1 archives and auxiliary links.
2. Generate all six grade manifests and compare counts/URLs against the current homepage.
3. Build a dynamic shell with loading/error handling and no content regression.
4. Configure pinned branch artifact retrieval and serialized Pages deployment.
5. Disable legacy workflows that push directly to main, after replacement is verified.
6. Stage, test and cut over atomically.
