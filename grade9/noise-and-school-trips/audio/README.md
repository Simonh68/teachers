# Lesson audio

The lesson uses synthetic English narration recorded with the Microsoft Edge Read Aloud neural voice `en-US-GuyNeural`, generated with `edge-tts` 7.3.1.

The recording rate is normal (1.0). The teaching player can default to 0.75 and can offer other speeds without changing the timing data. `words[].start` and `words[].end` are in seconds on the original media timeline and come from the speech service's WordBoundary events, not estimated word lengths. Match them against the audio element's `currentTime`.

`manifest.json` is the playback index. Files named `p1s1.mp3` and similar correspond to the numbered paragraph and sentence in the original worksheet. Vocabulary clips use `v01` (word) and `ve01` (example). Questions use `q1` and `q1answer`. Writing examples use `near1` / `far1` and their `v1`, `v2` alternatives. All are original lesson text. Generated narration is not a recording of a real teacher or student.

To regenerate, install `edge-tts` and FFmpeg, then run `python3 audio/generate_audio.py` with `content.json` in the parent lesson directory. The script reads the content and writes MP3 clips plus the manifest, with cached clips reused only when the text matches. Per-clip JSON files are generation caches, not needed by the player.
