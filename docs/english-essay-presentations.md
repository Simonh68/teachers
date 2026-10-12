# English Essay Presentations — Simon's Standard
Applies to future English essay presentations, especially Grade 11 Module G. These are the user's settled requirements from the smartphone-age presentation. Use the current grade11/smartphone-age-essay/index.html as the visual and interaction reference. Read its latest version, not an earlier copy.

## Writing and teaching
- Use simple, natural English accessible to Israeli EFL students. Avoid needlessly formal words, long sentences, repeated details and complicated qualifications.
- First slide: "Write an essay on the following topic:", the question, and brief instructions to state an opinion and support it with reasons and examples. Do not describe this as an authentic GRE task.
- Four paragraphs: opening, counterargument, supporting argument, conclusion.
- Two sentences per paragraph by default.
- Opening: sentence 1 restates the dilemma with contrasting views; sentence 2 states the student's own opinion. Do not insert general background as a third sentence.
- Show the chosen position clearly (e.g. a chosen age). Develop reasons for that specific position, rather than generic advantages/disadvantages of the topic.
- Counterargument: short claim and short explanation/result. Supporting paragraph: claim and concrete example.
- Conclusion: restate and strengthen the opinion, then finish with a relevant hope. Do not reopen the debate with unnecessary qualifications or repeat practical details.
- At least 125 words in the complete base essay for this format. Count the actual displayed essay. Simple English and short sentences remain priorities; add meaningful development rather than filler.
- For each sentence use the same teaching sequence: invite students to think first (Hebrew question), show a simple starting sentence, then develop it with a useful reason/example/result/condition. Keep explanations brief. Show a paragraph only after its sentences have been taught; complete essay after all four paragraphs.
- Provide many clickable phrase-level paraphrases throughout sentence examples, paragraph examples and the full essay. Prefer equivalent meaning and correct grammar in every combination. Explain differences when a variant changes emphasis. Examples: because/since/as; safely/in a safe way; In conclusion/To sum up/To conclude.
- Counts update whenever wording changes. Do not claim that every alternative stays above the minimum unless verified.
- Include an explanation slide per relevant grammar structure and a color-coded summary. Distinguish structures actually in the essay from extra examples. Do not force a tense into the essay or add a redundant sentence merely to demonstrate grammar.

## Visual style and text flow
- Preserve the established dark navy Teacher deck, readable light text, cyan/lime accents, Heebo for Hebrew and Nunito for English. Reuse current fonts and shared standard rather than redesigning.
- English is LTR and left-aligned. Hebrew instructions are RTL.
- Paragraphs are separated by whitespace only: no border lines, repeated paragraph-start/end labels or oversized gaps.
- Interactive phrases must flow as ordinary inline text, wrapping at words. Use inline spans with role=button and tabindex, not inline-block button blocks that force phrases onto separate lines.
- No dominant underlines or phrase boxes. Default background transparent; a subtle hover/focus indication is sufficient. Maintain visible keyboard focus.
- Keep punctuation inside the clickable phrase and preserve it when switching alternatives. Never leave a period/comma detached on the next line.
- Full essay mobile text about 22px, line-height about 1.65; reasonable paragraph gaps about 1.6em. Desktop typography responsive. Do not shrink a long essay to fit one screen; allow scrolling.
- Avoid entrance animation, layout jumps and unnecessary zoom changes. Switching wording may reflow naturally but must not reset reading position or navigate.

## Navigation
- Four progress squares numbered 1–4: opening, against, for, conclusion. Highlight current paragraph. Each is also a link to the first teaching slide of its part.
- Arrow controls and keyboard navigation remain available.
- Upward swipe = next; downward swipe = previous on slides that fit.
- On a long slide, vertical gestures scroll the text. Record whether the gesture BEGAN at the top/bottom. Reaching the edge during a reading gesture must not navigate.
- Only a fresh outward swipe beginning at the relevant edge may navigate. Long-slide wheel scrolling must not jump slides.
- Multi-touch/pinch should not trigger navigation. Prevent double handling by the shared swipe listener.
- Ensure content can be read to the bottom with clearance from fixed controls.

## Implementation and validation
- Inspect every loaded shared script for injected sample slides; never carry over AI/parks/other-topic examples into a new topic. Avoid premature automatic two-paragraph demonstrations.
- Preserve scope: independent essay presentation with its own URL.
- Check sentence sequence, paragraph boundaries, word count, all phrase variants, punctuation after switching, chapter links, mobile flow and edge-scroll navigation.
- Verify the rendered page on phone dimensions when supported. If only code checks were possible, do not claim visual verification.
- For every publication response include BOTH the presentation URL and the latest commit status URL:
  https://github.com/Simonh68/teachers/commit/<sha>/checks
- Describe verification/deployment state accurately; a committed change is not proof that deployment finished.

## Required shared display stylesheet
All teaching presentations for English essays must load shared/deck/essay-clean.css as the final stylesheet in the head. Do not load essay-paragraphs.css: it contains obsolete paragraph borders and labels. This standard also removes the decorative background grid, which can look like separation lines. Paragraphs use whitespace alone; clickable text remains inline with no underlines, boxes, borders or pseudo-element markers. Keep only the four navigation squares and necessary navigation controls visually outlined. Preserve the documented stable reading-scroll behavior. Include this shared stylesheet in new decks and keep it when editing existing ones.

## Optional transition icon — final behavior
At the end of the first paragraph only (both opening-paragraph slide and full essay), show a small ✨ icon. No explanation below the essay and no popup. Native hover tooltip says only "משפט אופציונלי". Clicking reveals a yellow optional sentence at the end of the opening; clicking the sentence cycles grammatical alternatives: "In this essay, I will explain my opinion.", "I will explain my opinion.", "I will expand on my opinion.", "In the following essay, I will explain my opinion.", "In the following essay, I will expand on my opinion.", "This will be my answer." Never show the incomplete fragment "I will in the following essay". Synchronize sentence visibility and chosen wording across opening/full essay and update visible-text word counts, excluding hidden text and the icon. Clicking ✨ again removes the optional sentence. Preserve the two-sentence base opening. Target 125 words for teaching; exam instructions currently ask for 120–140 words.
