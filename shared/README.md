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
