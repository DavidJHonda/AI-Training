# Why Answers Vary — reroll preparation, November 9, 2026

Ready for a new roll. This update prepares sources and edit directions; it does not generate or install a video.

## Teaching progression

Changes in the model, prompt, or context can change an answer; even with the same model and information, sampling can produce different choices, and temperature reshapes the odds used for those choices.

## Changes for this roll

- Speak the approved opening paragraph verbatim, including the model as well as prompt and context. The lesson narrows to token selection; do not expand into model comparisons, tools, hardware, or an exhaustive list of causes.
- Shorten sampling by consolidating repeated explanations. Keep the dog-name setup, the qualified 22-out-of-100 explanation, and one quick sequence of five independent picks at the same open token. Keep the odds fixed. Show Max, Spot, Buddy, Rex, Max as one possible set; Spot occurs once and another set can differ. Do not restart the example or add a second sampling analogy.
- Give variety and branching answers one brief connecting beat, then move to temperature. Preserve “can make answers repetitive.”
- Use the lesson’s temperature demonstration as the main visual for that section in the finished edit. The uploaded complete JPG supplies accurate reference content for generation; it is not the intended continuous visual treatment.
- Close exactly: “AI answers vary.” / “Different inputs. Different odds. Different choices.” The unchanged-learning point stays in the temperature explanation.

## Beat and visual plan

| Beat | Essential narration | Visual direction |
| --- | --- | --- |
| Opening | Approved model/prompt/context paragraph, then token probabilities and the sampling/temperature introduction | Direct illustrated opening; no title or preview. |
| Sampling | Dog prompt, unfinished reply, Spot at 22%, qualified 100-tries meaning, “That’s called sampling.” | Establish the open token once; use the current sampling graphic with a brief selection sequence. |
| Different picks | Five separate picks with unchanged odds; one possible set, Spot once, another set could differ | Reveal picks as spoken, preserving a single blank across attempts; no five-name sentence. |
| What follows | Other likely choices add variety; a different token can change the continuation | Brief branching-answer scene. |
| Temperature | Concentrated versus spread odds; already set behind the scenes | Introduce the current lesson demonstration. |
| Starting → low → high | Training and context determine starting odds; Spot 22% → 36% at low, 22% → 16% at high | Reveal and animate each column on its spoken cue; high compares to the original baseline. |
| Comparison | 22%, 36%, 16%; temperature changes probabilities, not learning; illustrative numbers and Other qualification | Brief full comparison, with the entire Spot row outlined. |
| Close | Both approved closing lines, verbatim | Current canonical closing graphic; nothing after. |

No forced runtime. Reduce repetition rather than speed up speech or remove essential qualifications. Judge pacing from the new narration; do not inherit timestamps from old versions.

## Temperature capture for editing

Source: `TemperatureScene`, `TEMPERATURE_DATA`, and `TEMPERATURE_STATES` in `index.html`. Generate the preview using `node scripts/video/preview_temperature.cjs`. The static upload reference is `assets/why-answers-vary-temperature.jpg`; its displayed values match the current component.

Use `/previews/temperature.html?capture=1&step=0` and `window.setTemperatureScene(step)`:

| State | Cue |
| --- | --- |
| 0 | Starting odds visible; Spot 22%. |
| 1 | Reveal low temperature; Spot 36%; less likely names lose probability. |
| 2 | Reveal high temperature; Spot 16%; less likely names gain probability relative to the starting odds. |
| 3 | Brief full-row comparison of Spot 22%, 36%, 16%; learning unchanged. |

The current preview’s capture mode disables bar transitions for still captures. For the motion pass, override `.capture .temperature-bar > span` to restore `transition: width 450ms ease` before advancing states, with reduced motion off. Record the transitions, not just settled screenshots. Verify those transitions in the encoded video and align them with the new narration. Keep all values and the combined Other row intact. No demonstration shell, instructions, buttons, or cursor in the finished video. Keep the white-panel layout and unfinished reply; do not restore the deleted prompt box. Use the current Edit Spec for framing and highlights.

## Upload and review

Upload the four files in `upload/`: current lesson Markdown, sampling JPG, complete temperature-reference JPG, and updated closing JPG. Paste `PROMPT.txt` into customization; do not upload the prompt or these notes. No face variants are needed for these graphics.

Save as `Prompts/why-answers-vary-reroll.mp4`, or the next unused `-reroll-N` filename. Preserve existing raw rolls and candidates.

Before editing, check every required line against the new transcript and listen to the narration. Confirm concise sampling, independent picks, the same temperature baseline, explicit behind-the-scenes setting, unchanged learning, and both new closing lines. A correct static temperature illustration in the raw roll is usable: the animated scene is inserted during editing. Reject omissions or invented explanations, not merely repairable visuals.

## Current installed reference

The local course points to `why-answers-vary.mp4?v=20261023ship4`, v4, 3:21.10. Its SHA-256 was verified during this prep update: `3692635c319e3fbf439ff676efbc4c6d452dc1013cd39968b39bda72d2b4fa57`. Installation record: `video-audit/board-font-sync-round2-2026-10-23/why-answers-vary/installation.json`. No public verification or new playback review is claimed. September v14 records are historical and do not describe the current installed file.
