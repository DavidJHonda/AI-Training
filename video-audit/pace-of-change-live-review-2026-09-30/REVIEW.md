# Pace of Change: public-video evaluation, September 30, 2026

Scope: evaluation only. No lesson, prompt, board, video, tracker, or deployment changes.

## Recommendation

Keep this production as the base. A new generation is not justified by the evidence. The lesson coverage is strong; the clearest production defect is the missing camera pullback at the final board's takeaway. The late board sequence also needs better visual variety. A separate source-copy correction would improve the overbroad model-replacement claim.

This is a **transcript and sampled-frame evaluation**, not an end-to-end audiovisual sign-off. Audio was not heard, and animations were not continuously watched. Final KEEP / REPAIR / REROLL certification under Narration Review remains provisional for that reason. Proposed narration edits below have not been auditioned and are not verified repair joins.

## Exact release checked

- Public page: https://besmarterthanthetool.com/
- Public video: https://besmarterthanthetool.com/course-assets/pace-of-change/pace-of-change.mp4?v=20260924ship1
- Canonical local file: `course-assets/pace-of-change/pace-of-change.mp4`.
- Public, local, and recorded v8 render SHA-256 all match: `4cce8f2cb230d865ad54e6ff165a603fc779c6180514bd83bb8965cc8f6680d7`.
- Decoded 8,757 frames, 30 fps, 1280 × 720; duration 291.90 seconds (4:51.9).
- Public `PaceOfChangeSection` matches the local lesson function exactly.
- Read the complete current lesson and canonical boards. Read the complete fresh 83-segment transcript extracted from the exact current file (`pace-of-change/transcript.txt`), then compared it with the v7 output transcript and v8 build record. The new transcript confirms the quoted wording and timestamps; it does not substitute for listening.
- Inspected seven newly extracted contact sheets, sampled every four seconds across the complete file, plus selected full-resolution frames and the current board JPGs.
- Public verification is in `verification.json`; screenshots are in `frames/` and `details/`. Exact board intervals above come from the hash-matched v8 manifest, corroborated by fresh frames. The subsequently completed ORB scan corroborates the long final board run (`board-spans.txt`); its spurious 1:35 comparison-board match is not used.

## Findings, in priority order

### 1. Fix the off-screen takeaway at 4:33–4:36

At about 4:33 the narrator says, “Nobody knows whether AI will reach either milestone.” The camera remains on the ASI card. The gold takeaway banner is below the visible frame, so its purple highlight also falls outside the useful picture.

This is an encoded-video defect, not just a plan concern: see `details/273.00.jpg`, `details/275.80.jpg` (only the top of the purple banner outline is visible), and the 4:36 frame on `frames/sheet-05.jpg`. The v8 `leg-far.json` confirms that a banner ring is scheduled at local frame 990 but the camera track contains no pullback. The earlier self-improvement board does include its pullback and shows its banner correctly.

Proposed repair: return to the complete How Far Can AI Go? board before the takeaway starts, then outline the entire gold banner at its spoken onset. Preserve the narration and timing.

### 2. Break up the final 92.2-second board run

Could AI Improve Itself? occupies 3:03.90–4:00.10 (56.2 seconds). How Far Can AI Go? immediately follows until 4:36.10 (36.0 seconds). Camera moves and highlights guide attention, but there is no supporting scene anywhere in that 92.2-second run. This is a substantial shift from the earlier comparison's changing pictures and the two supporting scenes inside Why So Fast?

These are not 92 seconds of dead air: the narration is teaching different concepts. The concern is visual engagement and the current board-break standard, not runtime alone. Keep the full explanations and introduce meaningful supporting visuals. Proposed placements are in the board plan below; no existing raw Pace of Change rolls are present in `Prompts/`, so new artwork would be needed unless the owner supplies the originals.

### 3. Correct the overbroad replacement claim in both source and narration

At roughly 1:49.8–2:00.9, the narration says each new version introduces a stronger model that “outright replaces the previous one.” The page similarly says: “Each new ChatGPT, Claude, or Gemini release is a new, stronger LLM replacing the one before it.”

The pace-of-progress point is sound, but the universal replacement claim is too strong. Model families coexist and serve different balances of capability, speed, and cost; retirement is a separate lifecycle decision. See [Anthropic's model-family explanation](https://www.anthropic.com/news/claude-3-family) and [model-deprecation documentation](https://docs.anthropic.com/en/docs/about-claude/model-deprecations).

Suggested source copy: “New releases can improve what AI can do, how fast it works, or how much it costs. A limitation can disappear quickly, so today's ‘no’ is not necessarily permanent.”

The next sentence, at 2:01.4–2:07.2, says “we have to stop judging AI by its temporary flaws.” This is also less careful than the lesson's useful point: test today's tool, but do not assume today's limitations last forever.

A possible cut using the existing canonical audio is identified below. No new narration generation is required merely to remove these sentences. Source wording and the upload copy should be aligned before any narration repair is finalized.

### 4. Preserve what works

- **0:28.6–1:33:** the animated comparison teaches answering, images, context, and action through different visual examples. The malformed dog, pages versus novel-series capacity, and steps versus completed actions support the narration. This was explicitly approved by David on September 24; a blanket replacement with a static course board would disregard that decision. Retention remains subject to an actual playback check of motion and synchronization.
- **2:12.6–3:03.9:** Why So Fast? arrives with “This diagram outlines…”, has relevant data-center and keyboard breaks, and returns with the third card highlighted for “Slow down…” and the repeated AI-builds-AI point. Those prior timing fixes are present in the current file.
- **3:19–3:59:** the human-directed versus hypothetical autonomous-loop distinction is clearly developed. The extra explanation after the banner reinforces it without contradicting it.
- **4:08–4:42:** AGI and ASI are distinguished, uncertainty is explicit, and the narration says these are not a guaranteed timeline. “No agreed finish line” is adequate compression of the source's absence of an accepted definition/test; it is not an essential missing explanation.
- **4:42.7–end:** the current canonical close is present and the sampled final frame is clean. Exact motion and audio still require playback verification.

Older outline thickness is not itself a repair request: Edit Spec explicitly grandfathers videos shipped before the September 26 stroke change. Any newly rendered board spans should use the current 4 px at 720p standard.

## Teaching coverage

These ratings concern the meaning in the transcript; they do not certify delivery or audio quality.

| Teaching point | Rating | Output time / evidence |
|---|---|---|
| Louder argument because AI advances rapidly | RICH | 0:00–0:21; connects debate to a moving capability baseline |
| Answering, 2023 versus 2026 | RICH | 0:28.9–0:41.3; immediate output versus time spent working |
| Image/video progress | RICH | 0:42–0:59.8; malformed dog, readable signs, sound and dialogue |
| Context window | RICH | 1:00.4–1:17.3; few pages versus million tokens / novel series |
| Advice versus action | RICH | 1:17.9–1:32.5; instructions versus booking, building, fixing |
| Competitive release cycle | TAUGHT | 1:39.3–1:49.3; race and releases every couple of months |
| Every release replaces the previous model | WRONG as a universal claim | 1:49.8–2:00.9; source-copy issue too |
| Today's limitation need not be permanent | TAUGHT | 2:07.2–2:12.2; required sentence intact |
| Better training | RICH | 2:21.5–2:31.3; data and improved results |
| More compute | RICH | 2:31.8–2:42.9; chips, data centers, investment |
| AI helps people build AI | RICH | 2:43.4–3:03.4; well-defined coding tasks and explicit refrain |
| Four future ideas, one limited / three unproven | TAUGHT | 3:06.9–3:18.3; calls the latter three milestones, but subsequent explanation establishes the loop as a process |
| Automated AI research and human direction | RICH | 3:19.1–3:30; code, experiments, analysis, human goals and verification |
| Hypothetical self-improvement | RICH | 3:30.8–3:42.8; improve design, stronger version, repeat with little/no direction |
| Human-directed versus self-reinforcing loop | RICH | 3:43.6–3:59.5; exact banner plus clarifying comparison |
| AGI and undefined finish line | TAUGHT | 4:08.6–4:18.7; full term and broad human-level capability |
| ASI and uncertainty | RICH | 4:19.4–4:35.6; full term, best humans, cognitive fields, possibility unknown |
| Concepts are not guaranteed future events | TAUGHT | 4:36.2–4:42.6 |
| Closing takeaway | TAUGHT | 4:42.9–4:48.8; both required lines |

Hard requirements present in the transcript: “A limitation can disappear quickly, so today's no is not necessarily permanent”; “AI is already helping people build better AI”; “One is human-directed. The other would be a self-reinforcing loop”; “Nobody knows whether AI will reach either milestone”; “AI keeps getting faster and more powerful”; “Nobody is sure where it stops.” AGI and ASI are both expanded.

The missing dog name Spot, Training-lesson callback, and “wished you luck” are harmless compression. No missing essential explanation justifies a reroll. Source QA flags the model-replacement sentence above; this was not an exhaustive September 2026 fact-check of every capability/future-research claim.

## Proposed board and camera plan

Evaluation proposal only. Original-output times are used throughout; a narration cut would shift later times. Supporting illustrations are concepts, not approved or generated assets.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| ChatGPT: 2023 vs. 2026 | Preserve unmarked canonical overview and approved native comparison | Preserve | Canonical 0:21.03–0:28.63, followed by animated comparison to 1:33 | Preserve the approved, useful explanation |
| Why So Fast? | Whole Better Training card → More Compute → AI Helps Build AI; retain third card at “Slow down” | Full board throughout | 2:12.63–3:03.90, retaining data-center break 2:34.03–2:43.30 and keyboard 2:46.47–2:55.80 | Already communicates each driver; longest existing piece 21.4 s |
| Could AI Improve Itself? | Whole automated-research card → whole self-improvement card → gold contrast banner | Full opening, complete-card views, full view for banner | Proposed supporting research workflow around 3:22–3:29 and a human-directed-versus-hypothetical-loop visual around 3:51–3:59; retain original 56.2 s topic duration | Show code/experiments/results with human verification; reinforce the distinction instead of holding the banner through a repeat |
| How Far Can AI Go? | Whole AGI card → whole ASI card → full gold uncertainty banner | Full opening, complete cards, **restore full view by 4:33** | Proposed clearly hypothetical capability illustration around 4:23–4:31; keep original 36 s topic duration | Break the board run and make the closing uncertainty visible |
| Canonical close | Unmarked | Preserve existing motion, subject to playback check | 4:42.7–4:51.9 | Correct asset and final frame |

For the two new conceptual inserts, prefer simple explanatory graphics to unrelated people at computers. The self-improvement illustration must mark the autonomous loop as hypothetical and keep human-directed research visibly separate. ASI imagery must not depict a dated or guaranteed arrival. These proposed breaks reduce the longest board-only stretch to roughly 24 seconds; exact edges should be adjusted to the spoken explanations during playback, without adding silence.

Other retained supporting scenes: brain/sound-wave opening 0:00–0:04.4; year collage 0:04.4–0:13.57; capability overview 0:13.57–0:21.03; robot arm 1:33–1:39.07; stopwatch 1:39.07–1:49.73; MOMENTUM 1:49.73–2:01.30; phone/check sequence 2:01.30–2:12.63; forked uncertainty graphic 4:36.10–4:42.70. These spans were inspected as sampled sequences, not certified in motion. MOMENTUM and most of the phone scene would disappear if the narration cut below is chosen.

## Possible narration repair, not auditioned

Use the existing canonical MP4 as the source. Retain “pushing them to release new models every couple of months” (ending about 1:49.28), then join to “A limitation can disappear quickly, so today's no is not necessarily permanent” (beginning about 2:07.20).

This removes approximately 18 seconds comprising:

> Each time a major player releases a new version of ChatGPT, Claude, or Gemini, they are introducing a stronger large language model that outright replaces the previous one. Because of this constant replacement, we have to stop judging AI by its temporary flaws.

The retained sentences make a coherent argument without the inaccurate universal replacement claim. These are transcript timings, not validated edit boundaries. The exact split must be placed inside the actual silence, and the assembled join listened to. No donor audio has been verified; no cut has been made. The underlying raw rolls are absent from `Prompts/`, so the surviving finished MP4 is the available repair source.

No added pauses are proposed. Existing pause quality cannot be certified from a transcript; retain timing for the visual repair and assess the one proposed audio join by listening before any build.

## Remaining verification

- Listen end to end, especially the existing joins around 0:24.4, 1:10.5, 1:33, and 3:03.9.
- Watch the animated comparison and forked uncertainty graphic continuously with narration.
- Audition any new narration cut and confirm the revised source wording.
- For any build, verify board highlight onsets, every changed boundary, full-frame close motion, and copied/edited audio as applicable.
- Video Tracker was not consulted or changed; no workflow status is inferred from it.


## Approved build follow-up

David approved the plan with “Agree. Build it please.” v9 has been built for review: [build record](../pace-of-change-build-2026-09-30-v9/REVIEW.md). Public v8 remains unchanged.
