# Read Alone Text addition

Ten reader slides follow the complete story slide; all original 90 slide objects
remain unchanged and in order. `build_lesson.py` also inserts these ten slides.
The worksheet and canonical story are unchanged.

The approved reader implementation and media were copied from `grade7/follow-along`
at commit 636214f. Audio production and word boundaries are documented in
`tools/follow-along/README.md`; the MP3, images and timing data are reused verbatim.
`reading.json` and `units.json` contain all 268 words and 110 translation units.

`read-along.html` is embedded in one persistent, same-origin frame during the ten
reader slides. `window.readAlong` provides manual page selection and pause.
`reader-ready` and `reader-page` events synchronize the outer slide index. Automatic
reader transitions retain the live audio; manual outer navigation pauses and seeks.
Leaving the section pauses and removes the frame. Opening the menu pauses audio.
The reader scroll region and player occupy separate areas so controls do not cover
text. The mobile text scrolls normally; horizontal swipes change slides.

Validated: original-slide subsequence equality, exact story text, actual quarter-speed
playback, preserved pitch, pause/seek, automatic page advance without interruption,
translation without movement or playback, removal on exit, images and all ten pages
at 1280×720, 1000×600 and 390×844.
