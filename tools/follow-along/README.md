# Follow-along reader

Published entry: https://simonh68.github.io/teachers/grade7/follow-along/

`The Green Bag` is an 80-word Grade 7 reading inspired by the existing lesson
`The Same Way`. Three pages show enlarged text with contextual SVG animations; every boy wears a cap. Automatic narration advances pages; manual page navigation pauses and seeks to the selected page. Reduced-motion preferences disable animation. The speech is AI-generated American English (en-US-GuyNeural),
generated once at a reduced rate and hosted as an MP3 with the page. The browser
only plays the file; it does not request TTS, a microphone, an account or API keys.

## Content and timing

- `build_audio.py` is the reproducible build source for the story and narration.
- `grade7/follow-along/units.json` is the hand-authored, context-sensitive translation
  segmentation. All units must concatenate to the exact sentence text.
- `reading.json` contains the rendered text, translations and word boundary times
  supplied by the speech engine. Each cue is checked against the transcript.
- Run `python tools/follow-along/build_audio.py` after installing `edge-tts==7.2.8`.
  The build needs network access; the deployed reader does not need the speech service.
- Both the sentence selection and active word use `HTMLMediaElement.currentTime`.
  `requestAnimationFrame` provides smooth highlights; media events handle seeking,
  pausing and completion. Speed changes keep the same audio timeline.
- Translation units remain in place; the floating Hebrew tooltip sits above or
  below the entire unit. Hover, keyboard focus and touch are supported. Escape,
  scrolling, blur and outside taps dismiss the tooltip.
- A separate button plays one sentence. Tapping a translation never starts speech.
- No student identity or learning record is collected by this reader.

## Acceptance checks

Check real MP3 playback, exact word mapping, pause/resume, speed changes, seeking,
repeat sentence, completion, hidden-tab pause, mobile and desktop overflow,
all translation units, tooltip placement, unchanged text position, keyboard and
touch translation, quiz feedback, public asset availability and navigation.
