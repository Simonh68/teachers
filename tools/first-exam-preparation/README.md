# First exam preparation

Run `python tools/first-exam-preparation/build_content.py` to regenerate content.json and data.js. Run `python tools/first-exam-preparation/build_audio.py` with edge-tts 7.2.8 to regenerate the full English narration and real engine word boundaries. HTTPS_PROXY and CODEX_PROXY_CERT are supported when needed.

The deck reuses the approved Teachers player and embeds the source story reader rather than duplicating its assets. English source sentences and Hebrew translations are unchanged. Question-word teaching and new grammar examples have per-word glosses. Keep the two-page exam in the teacher's Drive, not the public repository.

Validate all slides on desktop and at 360×640 and 390×844, exact reveal geometry, all quiz feedback states, four-direction swipes, reader tab endings and Continue, all sentence autoplay clips, saved speed, and no continuing audio on navigation. Publish only against the latest main without force and check the public page.
