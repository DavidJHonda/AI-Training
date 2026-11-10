# Why Answers Vary — reroll preparation, November 10, 2026

Ready for a new roll. This update prepares sources and edit directions; it does not generate or install a video.

## Teaching progression

Two separate chats suggest Spot and Max for the same dog-name question. A brief overview shows three reasons answers vary: Model & Thinking, What AI Receives, and AI’s Choices. The lesson then focuses on choices: sampling can produce different selections, and temperature reshapes the odds.

## Changes for this roll

- Speak the approved dog-name opening verbatim: first request gives Spot; a new chat with the same question gives Max. These are two requests, not two names in one response. Do not assert identical hidden context across the two chats. Answer the opening question with the new overview board, covering Model & Thinking, What AI Receives, and AI’s Choices. Then say “Two techniques help explain AI’s choices: sampling and temperature.” Go straight into Sampling without repeating the token-by-token explanation from How AI Answers. Describe What AI Receives as “Your prompt and the other information available to AI can change its answer.” Keep the overview brief; no extended model comparisons, tools, or hardware discussion.
- Shorten sampling by consolidating repeated explanations. Keep the dog-name setup, the qualified 22-out-of-100 explanation, and one quick sequence of five independent picks at the same open token. Keep the odds fixed. Show Max, Spot, Buddy, Rex, Max; Spot occurs once and another set can differ. Do not restart the example or add a second sampling analogy.
- The sampling board has no yellow takeaway banner; its caption already explains the outcome. Keep “Unchanged across all five picks”; omit the redundant “One possible set” subtitle. Use the current 1600 × 822 asset.
- Ask “Why does AI work this way?” Explain variety, then say “Choosing a different token shapes what comes next and can send the answer in a different direction.” Move to temperature. Preserve “can make answers repetitive” and “can make answers more creative.”
- Introduce Temperature with the approved lines: “Sampling selects a token using probabilities.” / “Temperature adjusts those probabilities.” / “In ChatGPT, Gemini, and Claude, temperature is set for you behind the scenes.” Then say “Compare how different temperature settings change the probabilities for each dog name.” Let the board explain concentration and spread. Keep the sampling definition and the two-techniques transition as approved; do not add the rejected extra reminder about unchanged temperature.
- Explain lower temperature as concentrating more probability on the leading choices and higher temperature as spreading it more widely. Avoid saying every less-likely name loses at low temperature or gains at high: Max and Buddy also rise at low temperature. Preserve all authored percentages.
- Use the retained animated temperature scene as the main visual for that section in the finished edit. The uploaded complete JPG supplies accurate reference content for generation; it is not the intended continuous visual treatment.
- Close exactly: “AI answers vary.” / “Different inputs. Different odds. Different choices.”

## Beat and visual plan

| Beat | Essential narration | Visual direction |
| --- | --- | --- |
| Opening | Dog-name request gives Spot; a new chat with the same question gives Max; why? | Clearly separate illustrated chats; no title or preview. |
| Overview | Model & Thinking, What AI Receives, AI’s Choices; then “Two techniques help explain AI’s choices: sampling and temperature.” | Current EE-3FB overview JPG, three illustrated cards from left to right; emphasize AI’s Choices before moving on. |
| Sampling | Continue the dog example: unfinished reply, Spot at 22%, qualified 100-tries meaning, “That’s called sampling.” | Establish the open token once; use the current sampling graphic with a brief selection sequence. |
| Different picks | Five separate picks with unchanged odds; Spot once, another set could differ | Reveal picks as spoken, preserving a single blank across attempts; no five-name sentence. |
| What follows | Other likely choices add variety; a different token can change the continuation | Brief branching-answer scene. |
| Temperature | Sampling selects a token using probabilities; temperature adjusts them; set behind the scenes in ChatGPT, Gemini, and Claude; compare each dog name | Introduce the temperature comparison, then use the retained animated scene. |
| Starting → low → high | Training and context determine starting odds; Spot 22% → 36% at low, 22% → 16% at high | Reveal and animate each column on its spoken cue; high compares to the original baseline. |
| Comparison | 22%, 36%, 16%; Spot remains the most likely individual token; temperature changes its probability; illustrative numbers and Other qualification | Brief full comparison, with the entire Spot row outlined. |
| Close | Both approved closing lines, verbatim | Current canonical closing graphic; nothing after. |

No forced runtime. Reduce repetition rather than speed up speech or remove essential qualifications. Judge pacing from the new narration; do not inherit timestamps from old versions.

## Temperature capture for editing

The desktop lesson and video upload use the static standard board with all three columns visible and short explanations under the headings. The phone layouts stack readable cards; those page adaptations are not video-upload assets. The explanations appear as regular lesson body text immediately below the board, not inside the image. They read: “Spot remains the most likely individual token at all three settings. Temperature changes its probability.” Columns read Low / Starting / High; start the video with the center baseline, then reveal left and right. Thicker bars share a 0–40% scale across all columns; all percentages are unchanged. The worked-example board follows the shared editorial shell: 56 px title, 40 px headings, 27 px column explanations at the owner’s request, 32 px row labels, 27 px percentages, 112.5 px row spacing, and a 1600 × 1140 frame with content-derived height with 40 px bottom margins. There are no learner controls. Canonical renderer: `scripts/video/render_why_answers_vary_temperature.py`; canonical page and upload asset: `course-assets/why-answers-vary/why-answers-vary-temperature.jpg`. This renderer supersedes the legacy `render_when_you_need_more_temperature.py` for this asset.

The animated build remains available for video editing through `TemperatureScene`, `TEMPERATURE_DATA`, and `TEMPERATURE_STATES` in `index.html`. Generate its preview using `node scripts/video/preview_temperature.cjs`. Capture the scene alone, without captions or controls. Its values match the board. The label reads “All other” then “tokens” on a second line; the separate illustrative-probabilities footer remains removed.

Use `/previews/temperature.html?capture=1&step=0` and `window.setTemperatureScene(step)`:

| State | Cue |
| --- | --- |
| 0 | Starting odds visible; Spot 22%. |
| 1 | Reveal low temperature; Spot 36%; more probability concentrated on the leading choices. |
| 2 | Reveal high temperature; Spot 16%; probability spread more widely relative to the starting odds. |
| 3 | Brief full-row comparison of Spot 22%, 36%, 16%; Spot remains the most likely individual token; its probability changes. |

The current preview’s capture mode disables bar transitions for still captures. For the motion pass, override `.capture .temperature-bar > span` to restore `transition: width 450ms ease` before advancing states, with reduced motion off. Record the transitions, not just settled screenshots. Verify those transitions in the encoded video and align them with the new narration. Keep all values and the combined Other row intact. No demonstration shell, instructions, buttons, or cursor in the finished video. Keep the white-panel layout and unfinished reply; do not restore the deleted prompt box. Use the current Edit Spec for framing and highlights.

## Upload and review

The on-page TRY IT, Build an AI Response, stays outside narration and the upload bundle. It has 243 manually constructed names, context-dependent next-word probabilities, and optional replay with an unexpected-names list. Do not narrate those controls or restore the matching activity here.

Upload the five files in `upload/`: current lesson Markdown, overview JPG, sampling JPG, complete temperature-reference JPG, and updated closing JPG. Paste `PROMPT.txt` into customization; do not upload the prompt or these notes. No face variants are needed for these graphics.

Save as `Prompts/why-answers-vary-reroll.mp4`, or the next unused `-reroll-N` filename. Preserve existing raw rolls and candidates.

Before editing, check every required line against the new transcript and listen to the narration. Confirm two separate opening requests, all three overview reasons, the transition into choices, concise sampling, independent picks, the same temperature baseline, the exact sampling-to-temperature bridge, the named-app sentence, accurate concentration/spread wording, the updated Spot comparison, and both new closing lines. A correct static temperature illustration in the raw roll is usable: the animated scene is inserted during editing. Reject omissions or invented explanations, not merely repairable visuals.

## Current installed reference

The local course points to `why-answers-vary.mp4?v=20261023ship4`, v4, 3:21.10. Its recorded SHA-256 is: `3692635c319e3fbf439ff676efbc4c6d452dc1013cd39968b39bda72d2b4fa57`. Installation record: `video-audit/board-font-sync-round2-2026-10-23/why-answers-vary/installation.json`. No public verification or new playback review is claimed. September v14 records are historical and do not describe the current installed file.
