# Boost Simulation

Grade 6, A2. User-supplied BOOST practice: two complete sets, each with four parts. 101 teaching slides because each question and reveal are separate. This is practice, not an official exam.

22 multiple-choice question/reveal pairs; four personal topics, with model answers split into three readable parts each; two four-picture stories, picture-by-picture model reveals and connected story models. Fourteen prerecorded synthetic American-English clips (Brian), user-initiated playback at 0.75 by default, with speed selection and stop on navigation/hidden tab. No browser speech synthesis.

The title, navigation and colors reuse the current Teachers presentation interface. Supports four-way touch swipe, arrows, wheel, hash links and a slide selector. Long content scrolls normally, and vertical swipes advance only at scroll boundaries. Home returns to the Grade 6 library.

The source prompt had ambiguous distractors in Set 1 response 5 and Set 2 response 4. Replaced only those distractors, preserving the target correct answers. Birthday question avoids assigning an unspecified gender to the speaker. Speaking and picture-story answers are models rather than uniquely correct answers. Teacher script includes full listening texts and answer keys.

Eight story scenes are AI-generated. Original contact sheet generated with the built-in image tool on 2026-10-04, converted to WebP for publication, displayed as numbered panels. Maintains boy identity and head covering across forest scenes and covered heads for males in the family scene.

Build: python tools/boost-simulation/build.py; audio: python tools/boost-simulation/build_audio.py (edge-tts, configured environment proxy certificate if needed). QA uses Playwright. Run tools/boost-simulation/qa.cjs from the parent of a checkout named teachers; optionally set BOOST_CHROMIUM to an available browser executable. qa-report.json records all-slide layout checks at four sizes, identical placement for 22 MCQ pairs, real CDP touch gestures and actual playback start for all 14 clips. Long slides remain accessible by scrolling.

Public paths: grade6/boost-simulation/ and teacher.html. Created 2026-10-04 after sunset in Israel (24 Tishrei 5787).
