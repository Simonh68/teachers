# Mandatory presentation controls — Teachers site

Every newly created presentation in this repository MUST include:
1. The existing shared phone remote: load /shared/phone-remote/remote.js with the correct relative path.
2. A visible QR pairing launcher on the opening slide only; never overlap narration controls.
3. The QR pairs a phone as a controller without a user account, requiring presenter approval.
4. Swipe UP on the phone remote advances one slide; swipe DOWN goes to the previous slide. On touch slide decks, support the same gestures locally.
5. Provide stable next/previous buttons or an adapter recognizable by the shared remote.
6. Narration controls remain accessible; remote pairing must not interfere with Read-Along.
7. Test both phone and desktop navigation, QR pairing, swipe and narration before declaring deployment complete.
8. Use shared implementations rather than rebuilding per presentation.

Implementation requirement: include a check for the remote script and swipe support in the authoring/QA checklist for every new deck.
