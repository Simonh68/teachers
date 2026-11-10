# The Enemy — Grade 11 release and recovery checkpoint

Updated: 2026-11-10. Branch: `classroom/grade11`. Never merge into main.

## Verified publishing fix

- GitHub permission failure on 2026-11-09: HTTP 403 at the repository_dispatch endpoint due to `contents: read`.
- Workflow `.github/workflows/notify-classroom-publisher.yml` corrected to `contents: write` in commit `2a4c86446ae20a280eb1606911cbe2bd57e23bbc`.
- The notification and central GitHub Pages publisher both passed a real end-to-end test on 2026-11-10.
- The latest five-part guided-reading public deployment before this checkpoint: https://github.com/Simonh68/teachers/actions/runs/42809420592 ; status: SUCCESS.

## Published now — interim guided reading companion, NOT the original fully timed narration

- Source path: `grade11/the-enemy/read-along/index.html`
- Public URL: https://simonh68.github.io/teachers/grade11/the-enemy/read-along/
- Five actual parts matching the school's teaching edition; adapted original teaching text, 175 presentation slides, 15 vocabulary terms, 30 comprehension questions, and 40 teaching sentences each shown twice (English and English + Hebrew).
- Interactive browser-based speech synthesis at 0.75 rate, highlighted word based on boundary events when provided by device, 4-second automatic read after user activation, stars for hints, swipe both directions, keyboard and buttons.
- The Grade 11 public five-unit page and Grade 11 manifest link to this companion. The original discussion lesson remains preserved and cross-linked.
- This is an ORIGINAL ADAPTED teaching companion, not a claim that the complete Pearl S. Buck story and original recording have been published.

## The original user's audio has been recovered from the November 9 uploaded source

- `videoplayback.mp4` found in user's persistent ChatGPT Library, size 39,857,995 bytes.
- Duration: 3215.987 seconds (53 minutes, 35.99 seconds).
- Original AAC mono audio, 44.1 kHz, 72 kbps; soundtrack extracted losslessly as `The-Enemy-original-audio.m4a` in the recovery chat's file artifacts (approximately 29 MB).
- This media file is NOT in GitHub yet. Do not invent live URLs or imply it has been deployed.
- On 2026-11-10, the extracted original-audio M4A was also uploaded to the user's connected Google Drive as `The-Enemy-original-audio.m4a` (29,498,973 bytes; permission remains PRIVATE to owner). This is durable storage for subsequent recovery work, not a public lesson audio URL.
- The previously reported five recorded parts, 7,729 word timings and 30 comprehension stops were not in this GitHub branch when recovered. No exact timing/segment boundaries were preserved in the repo.

## Remaining tasks before the original requested Read-Along is truly complete

1. Recover the five synchronized audio+timing bundles from prior work, or regenerate correct timings from the original user recording.
2. Upload the binary audio sections and their aligned transcript using a supported file-write transfer path. The current GitHub connector writes UTF-8 text but does not upload binary media.
3. Upgrade `read-along/index.html` from adapted narration to actual word-synchronized original narration with accurate five-part boundaries and readable text.
4. Perform browser-level play/pause/seek/speed/sync QA across phone, tablet and desktop; verify accessible link after exact successful Pages deploy.

## Verification process

- Source and live URL smoke test: `.github/workflows/verify-grade11-enemy.yml`.
- Report precise links to exact successful publish and test Actions runs, along with the public site link and specific missing assets.
