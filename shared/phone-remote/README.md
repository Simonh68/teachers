# Teachers shared phone-to-projector QR remote

Source of truth: \`remote.js\`. Automatically included in eligible teaching decks via
\`tools/rollout-phone-remote.py\`. Future changes should be made in this shared file.

## What a QR code does
The QR does **not** just open the deck. It starts a private, temporary phone
controller for the presentation already open on the computer/projector.
The presenter must approve the connection on the computer. No teacher email,
name, profile, Google sign-in or student data is required. One remote can
control the authorized presentation. The code stops working when the presenter
closes the tab, resets it or the four-hour session expires.

The presenter can open QR with the small 📱 button, scan it with the phone,
and approve the phone on the computer. The phone has next/previous, reveal,
audio toggle when supported, and left/up/right/down swipes. A small status
counter follows navigation on the computer.

This generic remote uses the already-established PeerJS signaling/WebRTC path.
It **does not** extend or modify Firebase Firestore rules or collections.
The separate Grade 12 Firebase pilot and Grade 11 PeerJS integration are not
replaced. The English for Noar site is unaffected.

## Rollout/testing
- Run \`python tools/rollout-phone-remote.py\` to audit.
- Run \`python tools/rollout-phone-remote.py --apply\` to attach one script
  to compatible published presentations; no teacher notes or printouts.
- The automated GitHub workflow applies the same check on all future HTML pushes.
- See \`rollout-manifest.json\` for exact covered paths and exclusions.
- Before reporting 100% coverage, review the manifest, run public Chromium
  host/controller pairing tests, verify response to keyboard and touch, and
  inspect any nonstandard deck navigation.
