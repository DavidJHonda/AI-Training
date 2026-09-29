# One More Thing — live-video evaluation, September 29, 2026

**Recommendation: retain the current edit. KEEP on transcript-based teaching evidence; final audiovisual verdict remains provisional because direct end-to-end listening/viewing was not completed.** No reroll or new narration edit is supported by this review. The remaining editorial weakness is two long board holds, not missing explanations.

## Exact live version

Fresh public-page and streamed-byte verification at 17:45 UTC selects `course-assets/one-more-thing/one-more-thing.mp4?v=20260929ship1`. Its 27,712,627 bytes match the local canonical MP4 and approved v14: SHA-256 `321a52242ce10b86e151a8ffcf000b4684db8a340945da06fe3b317eee8a86ca`. Runtime 3:24.23, 6,127 frames, 30 fps, 1280×720. The page displays “3 min.” Earlier September 27–28 reviews evaluated a different 3:43.90 file and do not describe this release.

Read the freshly fetched public InferenceSection, current lesson Markdown, full fresh timestamped ASR, shared workflow, Narration Review, and current Edit Spec. Four local canonical board assets still match the v13 build's recorded hashes; v14 preserves those visuals except for its two timeline cuts. Public JPG bytes were not independently rehashed.

## Teaching review

| Essential point | Assessment | Current output evidence |
|---|---|---|
| Three opening questions | TAUGHT | 0:00–0:12: different answers, predictable/varied choices, scale of math. Opening images follow those three topics. |
| Dog-name example and Spot as top choice at 22% | TAUGHT | 0:12–0:37: probability calculated for the next token; highest chance does not guarantee selection. |
| What 22% means | RICH | 0:37–0:45: about 22 in 100, on average, if odds stay the same; the 100-trial illustration reinforces it. |
| Unchanged probabilities across five picks | RICH | 0:45–0:59: explicitly unchanged odds; Max, Spot, Buddy, Rex, Max. |
| One possible set; another five can differ | TAUGHT | 0:59–1:09: Spot once, another set may differ, best chance is not a guarantee. |
| Variety from allowing other likely tokens | TAUGHT | 1:09–1:18: most likely versus other highly ranked tokens. “Makes answers robotic and repetitive” is more categorical than the page's “can make”; optional future wording polish, not a reason to undo the approved edit. |
| Each choice shapes what comes next | TAUGHT | 1:18–1:21: complete spoken dependency sentence, supported by branching continuations. No unsupported claim that every different token must change the entire answer. |
| Temperature bridge and mechanism | TAUGHT | 1:21–1:36: asks what changes predictability, names temperature, explains reshaping before each pick and behind-the-scenes handling. |
| Same baseline; low and high temperature | RICH | 1:36–2:00: starts at 22%; low concentrates to 36%; high spreads odds and reduces Spot to 16%. |
| Temperature changes odds, not learning | TAUGHT | 2:01–2:14: comparison across the top row and explicit distinction. |
| Training creates weights; fixed during inference | TAUGHT | 2:18–2:27: “the static numbers that shape every prediction,” followed by their use for each new token. The owner-requested removal of the redundant fixed-weights sentence does not remove the concept. |
| Hypothetical model and per-token work | TAUGHT | 2:27–2:41: imagine one trillion weights, roughly two calculations per weight, one pass produces two trillion calculations. |
| 100 and 1,000 generated tokens | RICH | 2:41–3:03: explicit multiplication gives 200 trillion and two quadrillion. |
| Estimates, generated tokens, not a real measurement | TAUGHT | 3:04–3:10: both scope and imagined-model qualification spoken. |
| Scale takeaway | TAUGHT | 3:10–3:15: even a short answer takes trillions of calculations. |
| Current two-line close | MET in ASR and image | 3:15–3:20: “Math and probability, one token at a time. Every time you hit send.” Standard close remains through the literal final frame. |

The narration carries the lesson arc: random selection → reshaping those probabilities → calculations behind each choice. The bridges are present. A viewer receives the essential explanations without needing to read the tables independently. The optional page activity remains a separate interaction; the video does not walk through its quiz answers.

**Errors:** no wrong worked-example number or missing essential explanation found in the transcript. ASR renders “dog” as “doc” and “ChatGPT” as “chat GBT”; these are listening flags, not established pronunciation errors. No fresh independent technical/source audit of every page claim was performed. The arithmetic is internally correct for the explicitly imagined model. No source change proposed.

**Narration repair plan:** none. No additional pauses proposed without a listening pass. Do not restore the two phrases the owner explicitly requested removed.

## Board and camera recommendation

Preserve current treatment. This is an evaluation, not approval or execution of another build. All three boards are legible at full 1280×720 view in inspected frames; retain full views rather than introducing dives.

| Exact board | Highlighting sequence | Camera | Current spans / breaks | Judgment |
|---|---|---|---|---|
| Same Probabilities, Different Choices | Probability column → pick column and individual spoken selections → conclusion caption → banner | Full view, restrained push | 0:21.50–0:37.10 (15.60s); 0:45.13–1:09.57 (24.43s), separated by 100-trial drawing | Good worked-example pacing. Keep the five-pick demonstration together. |
| How Temperature Changes the Odds | Starting odds → low column/36% → high column/16% → comparison across Spot row → banner | Full view | Preview 0:04.23–0:08.17; intro 1:21.40–1:31.63; comparison 1:35.93–2:15.00 (39.07s). Behind-the-scenes illustration separates intro/comparison. | Longest board hold and primary pacing opportunity. Still purposeful: narration uses the columns throughout. Retain the approved exception unless a genuinely explanatory replacement is prepared. No verified better donor is proposed here. |
| The Math Adds Up Fast | Complete one-token card → short-answer card → longer-conversation card → banner | Full view | 2:29.03–3:03.90 (34.87s); hypothetical-model illustration 3:03.90–3:10.20; return 3:10.20–3:15.43 (5.23s) | Long, but the three calculations justify the sequence; the qualifier already has a useful visual break. |
| Math and probability, one token at a time. / Every time you hit send. | Unmarked | Existing standard hold/push/settle | 3:15.43–3:24.23 (8.80s) | Current wording and literal final frame are correct. |

Longest continuous board exposure is **39.07s**; no 60-second uninterrupted board chain. The two long holds exceed the roughly 20-second editorial trigger, but neither is dead time while narration discusses something else. Do not insert a decorative interruption or cut essential arithmetic merely to shorten them.

Retain supporting scenes: branching choices (0:00–0:04.23 and 1:18.20–1:21.40); fixed-weight illustration (0:08.17–0:12.17 and 2:15–2:26.80); dog question/blank answer (0:12.17–0:21.50); 100-trial example (0:37.10–0:45.13); repetitive/varied names (1:09.57–1:18.20); behind-the-scenes handling (1:31.63–1:35.93); hypothetical-model scale (2:26.80–2:29.03 and 3:03.90–3:10.20). Each serves a narrated point. These recommendations are based on sampled sequences, not a complete motion audition. No new photo, illustration, board replacement, or narration cut is proposed.

## Verification and limits

Completed fresh sequential decode, full fresh ASR and transcript review, all five four-second contact sheets, selected 720p detail frames, and final-frame inspection. Fresh transition_guard passed all **21 declared boundaries**, zero short visual-island flags. Not every transition strip was manually inspected, and automated visual checks do not certify sound.

The public MP4 loaded and displayed playback in the in-app browser. The course itself opened at the first-name/country entry gate; I did not submit invented learner details. Consequently the embedded lesson player, mobile layout, seeking, captions, and continuous streaming were not fully tested. The served MP4 was evaluated through its independently verified local-identical bytes.

**Direct listening and continuous audiovisual viewing were not completed.** Narrator warmth, pronunciation, cadence, audible joins, and animation/narration synchronization remain unverified. Especially audition v14 joins **1:46.33 and 2:22.30**. Earlier graft joins on the current timeline include **0:37.10, 1:18.20, 1:21.40, 1:35.93, 2:31.27, and 3:15.43**. Retained v14 waveform QA reports ~0.61s gaps at its two new joins, zero clipped samples, and a −0.45 dBFS peak; those measurements are existing evidence on the identical file, not a substitute for listening or fresh audio QA.

No tracker status was asserted or changed. No course content, video, prompt, source asset, or publication was changed.

Evidence: `public-verification.json`, `public-index.html`, `live-lesson.txt`, `board-asset-check.json`, `one-more-thing/transcript.txt`, `one-more-thing/scenes.txt`, `one-more-thing/sheets/`, and `transitions/` in this directory.
