# Full-story follow-along reader

Published entry: https://simonh68.github.io/teachers/grade7/follow-along/

The canonical story is `grade7/the-same-way/story.json`. Its 268 words and all
28 sentences are copied verbatim, including punctuation. The reader divides
it into ten short pages without rewriting it. Hebrew sentence translations
are also copied from the source. Build validation checks exact equality.

## Audio and translation

- `build_audio.py` uses `edge-tts==7.2.8` to create `assets/narration-full.mp3`
  and word-boundary timing data in `reading.json`.
- Voice: `en-US-AnaNeural`, a synthetic child voice (female voice catalog entry),
  replacing the adult Guy narrator. No claim of an actual boy recording.
- The MP3 is hosted on Teachers; the learner's device never synthesizes speech.
- `units.json` supplies contextual Hebrew translations for every word or phrase.
- HTML media playback rates: 1, .75, .5, .35 and .25. Labels are in simple Hebrew.
  `preservesPitch` stays enabled. Highlights use the audio timeline at every rate.
- Automatic page advance follows the narration; manual page changes pause it.
- Phrase tooltips support hover, keyboard and touch without covering the source.

## Static illustrations

Five original AI-generated photorealistic illustrations replace the SVG animation.
Dan: navy brimmed tembel/bucket hat without a front visor. Ben: beige knitted
kippah. Noam: red baseball cap, preserving the story clue. Identities, clothing
and headwear stay consistent. Photo assets are WebP, without animation.
The images are illustrative, not photographs of actual students.

## Verification

Exact source text/translation/word count, positive ordered timing cues, hosted
MP3 hash, all ten pages, phrase tooltips, real playback at one-quarter speed,
pitch preservation, seeking, page advance and static images are checked.
