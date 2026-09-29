# Training — live evaluation, 2026-09-29

**Recommendation: keep the current version. Content verdict: provisional KEEP, pending an actual end-to-end audiovisual listening pass.** The current edit teaches the lesson coherently, with useful worked examples and explicit bridges. No essential omission or contradiction identified in the complete transcript warrants a reroll. This is a transcript-and-encoded-frame evaluation, not a completed listening or shipping certification.

## Exact video and evidence

- Public page checked successfully: https://besmarterthanthetool.com/
- Public reference: `course-assets/training/training.mp4?v=20260928ship1`.
- Public video streamed for hashing; it exactly matches `course-assets/training/training.mp4`, `Prompts/training-v9.mp4`, and the v9 manifest's render hash.
- SHA-256: `640748dfa2ef1de643f05c88395ed7e27af1986c095c0e94a3158e55af94e20d`; 19,064,519 bytes. See `public-verification.json`.
- Fresh sequential decode: **7,382 frames, 30 fps, 1280 × 720, 4:06.07**.
- Grounding: current local `index.html` TrainingSection, `lessons/training.md`, current canonical assets, current README / Narration Review / Edit Spec. The public video reference and video bytes were verified; the entire public lesson body was not independently compared with local HTML.
- Read the complete timestamped v9 transcript in `../training-v9-2026-09-27/transcripts/training-v9.txt`. Reuse is justified by the matching render hash, not its filename.
- Fresh visual inspection: all six contact sheets at four-second intervals, plus full-resolution samples at 0:24.3, 1:20, 1:54, 3:09, 3:26 and 4:05.9. Additional extracted frames are retained in `details/`. Every frame was decoded, but not every frame was visually inspected.
- All seven current canonical JPG hashes match the protected assets in the matching v9 build manifest.
- No video, board, lesson, tracker, release, or deployment changes made.

## Teaching evaluation

The narrative order is effective: capabilities and practice → preparation → three-phase overview → shared loop → weights → each phase's mechanism, sample answer and limitation → fixed weights during ordinary chat. The overview and detailed teaching have distinct jobs. The repeated basketball question makes the improvement concrete.

The evidence below is transcript evidence; quotes were read, not independently heard during this pass.

| Essential teaching point | Assessment | Evidence in the live timeline |
|---|---|---|
| Why training matters; repeated practice analogy | RICH | 0:00–0:23: chemistry, code, essay; shoot, inspect result, adjust mechanics. |
| Setup before training | TAUGHT | 0:23.68–0:34.22: engineers design the model, give internal numbers starting values, then training changes them. |
| Training data as curriculum | RICH | 0:35.10–0:44.24: all seven data kinds are spoken, followed by “This becomes the curriculum.” |
| Three named phases and their different roles | RICH | 0:45.76–1:03.62: Pretraining, Instruction Tuning, Preference Tuning; same basketball question. |
| One loop across all phases; changing examples and feedback | RICH | 1:04.86–1:14.38 explicitly connects all three phases to guess/check/adjust and says what changes. |
| Peanut-butter worked example | RICH | 1:17.16–1:40.64: cloud guess, jelly target, comparison, internal adjustment, then another example. |
| Weights definition | TAUGHT | 1:41.34–1:44.88: “the model's internal numbers, called weights.” |
| Pretraining scale and broad patterns | TAUGHT | 1:45.86–1:59.88: first phase, 1,000 lifetimes, vast text/code, language and information patterns. The board's longer account of sentences/ideas/code and a broad foundation is compressed; opening capabilities and the following comparison preserve the essential meaning. Optional graft C was previously explicitly declined; this is not a new missing-content finding. |
| Pretraining answer and limitation | RICH | 2:04.92–2:14.92: complete fluent-but-unhelpful answer ending “In this guide, we will cover…”; does not reliably follow instructions. |
| Bridge into later training | RICH | 2:15.78–2:23.52: weights keep changing; examples and feedback change. |
| Instruction tuning mechanism | TAUGHT | 2:24.30–2:37.30: question/helpful-answer pairs, practice, weight changes toward human examples. |
| Instruction answer and limitation | RICH | 2:38.10–2:53.70: direct basketball instructions read in full; may remain unclear, incomplete or unhelpful. |
| Preference tuning mechanism | RICH | 2:54.74–3:16.58: bridge from following instructions to feedback, multiple answers, comparison/selection, weight updates. |
| Preference answer and limitation | RICH | 3:20.58–3:40.80: complete improved basketball answer; wrong answers can still sound right. |
| Training versus ordinary chat | TAUGHT | 3:41.72–3:55.30: trained weights used during chat; new information can be used without changing them. |
| Both closing lines | Present in transcript and canonical visual | 3:56.18 onward: “AI learns from examples and feedback.” / “Guess, check, adjust. Repeat.” The ASR's 20ms timestamp for “Repeat” is unreliable; it is not evidence of a clipped word. Earlier owner review explicitly accepted it. Fresh auditory verification remains undone. |

**Errors:** no material contradiction with the current lesson identified in the transcript. “The response is highly polished” at 3:17.46 describes the illustrative answer; the subsequent explicit warning prevents it from functioning as an unqualified promise of correctness.

**Source QA:** no internal contradiction identified in the current lesson for this review; this is not an independent research audit of every AI training claim. The seven data types describe modern AI broadly, while the detailed examples concern language-model training.

**Additions:** basketball mechanics and the visual control-panel analogy help make iterative adjustment concrete. No new lesson copy is proposed.

**Narration repair plan:** none recommended. No new pauses recommended from transcript evidence alone.

## Visual findings and retention plan

Keep the existing supporting drawings. The shot/error/target sequence at 1:04–1:15 connects the practice analogy to the shared training loop. The changing internal-number diagram at 2:15–2:24 supports the transition to later phases. Its 34% → 98% and “Optimal Output” are illustrative, not sourced performance measurements; their presence alone is not a reason to replace the scene. Only sampled states were inspected, so animation timing and motion remain unverified.

Other useful supporting spans: capabilities/basketball at 0:00–0:23; desk/court at 0:45–0:48.5; repeated practice at 1:38.4–1:41.1; control panel at 1:41.1–1:45.5; missed shot at 2:00.3–2:04.6; frustrated student at 2:10.3–2:15.3; shot at 2:37.8–2:41.7; thinking student at 2:54.1–3:01; smiling student at 3:17–3:20.3; ordinary chat at 3:41.3–3:55.8. Their illustrations support the accompanying ideas; no replacement is proposed merely to change style.

The following is a **retain-as-is recommendation**, not a new build request. Full-view openings in the matching manifest range from 2.03 to 3.97 seconds, consistent with sampled encoded frames. Dense-board crops keep the active section intact; inactive sections can leave the frame.

| Board | Highlight sequence | Camera | Actual continuous spans / breaks | Recommendation |
|---|---|---|---|---|
| Before Training Starts | Set Up the System → Gather the Data | Full view | 0:23.30–0:45.00, 21.70s; then desk/court | Keep. Slightly above the approximate 20s guideline; narration is still explaining both cards. |
| Three Phases of Training | Same question → Pretraining → Instruction Tuning → Preference Tuning | Full view | 0:48.50–1:04.20, 15.70s; then shot/error animation | Keep. Clear orientation before detail. |
| The Training Loop | Guess → Check → Adjust | Full view | 1:14.80–1:38.37, **23.57s**; then repeated-practice drawing | Keep the complete worked example together. This is the main board-duration exception; inserting a drawing into the comparison could hide useful information. |
| 1 · Pretraining | What Pretraining Builds → What an Answer Might Look Like | Full view, then complete active section | 1:45.50–2:00.30, 14.80s; missed shot; 2:04.60–2:10.27, 5.67s; frustrated student carries limitation | Keep. The limitation is spoken over the drawing, so a third ring is unnecessary. |
| 2 · Instruction Tuning | Learn to Follow Instructions → answer → What Still Needs Work | Full view, then complete active section | 2:24.00–2:37.77, 13.77s; shot; 2:41.73–2:54.07, 12.33s | Keep. The answer and limitation remain readable. |
| 3 · Preference Tuning | Learn from Feedback → answer → What Still Needs Work | Full view, then complete active section | 3:00.97–3:17.00, 16.03s; smiling student; 3:20.27–3:41.33, 21.07s | Keep. Final run is slightly above 20s but carries a complete answer and caveat. |
| Closing message | Unmarked | Standard hold/push/settle | 3:55.77–4:06.07, 10.30s | Keep. Matching manifest specifies 48-frame hold, 150-frame push to 1.2×, 111-frame settle; late encoded frame shows canonical close. |

**Longest uninterrupted teaching board, and longest adjacent-board run: 23.57 seconds**, the loop. All other teaching boards are separated by supporting scenes. The old v9 prose erroneously locates the loop at 0:59.8–1:23.4; the correct output interval is 1:14.80–1:38.37.

Fresh ORB measurement (`board-spans.txt`) agrees within its 0.5s sampling precision. It falsely matches some shared illustration features to Instruction Tuning at 0:46.5–0:48.5 and around 3:17–3:20; the contact sheets show drawings there. Those false matches are excluded from the durations above.

**Minor production issue:** the matching v9 measurement record shows blue/purple outlines around 4–4.5px and teal/green around 5px. This is a small consistency issue, not a teaching failure. Standardize to the current fixed 4px at 720p during a future authorized build; it does not justify rerolling narration or rebuilding this shipped video by itself. No fresh ring-width scan was performed. Large 10–12px detections in that record include artwork features and should not be reported as actual outline widths without frame validation.

No sampled frame showed a disruptive watermark, stock photograph, unreadable active card or wrong canonical board. Sampling cannot establish their absence in every frame.

## Remaining verification

I did **not** hear the audio or watch continuous real-time playback in this pass. The toolset used provides frame inspection and text, not an auditory listening channel. Consequently, cadence, voice continuity, breaths, clicks, complete motion, and natural pacing remain unverified. The existing transition-guard pass belongs to the matching v9 record; it was not rerun or treated as an audio pass.

An auditory pass should particularly check the source changes at 0:23.30 and 1:04.20, the edited quote at approximately 2:08.17, and the final “Repeat.” Those are listening targets, not newly observed faults. No phone/player playback test was performed. Video Tracker was not accessed or updated.

The supported conclusion is **keep the current teaching and visual structure; no substantive repair or reroll identified by this review**. A fully verified KEEP still requires the end-to-end audiovisual review above.
