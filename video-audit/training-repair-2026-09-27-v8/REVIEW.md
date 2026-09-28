# Training v8 — current lesson flow repair

Built 2026-09-27, following David’s “ok. Build the new version.” This is a **review candidate, not published**.

[Watch the candidate](../../Prompts/training-v8.mp4) · [Full timestamped transcript](transcripts/training-v8.txt) · [Verification](verification.json) · [Edit manifest](edit-manifest.json)

## Result

**4:31.07, 8,132 frames, 30 fps, 1280 × 720.** The approved repair removes 18.80 seconds. Setup and the three-phase overview now precede the shared loop. The weights definition follows the worked example, followed by Pretraining’s scale and outcomes. The repeated pretraining mechanics and backward references were removed. The current What Pretraining Builds board replaces the older version.

This is the approved existing-audio repair. It preserves the essential teaching and new sequence, using equivalent existing narration rather than the new lesson’s bridge sentences verbatim. No new narration was generated. The instruction-to-preference transition still says “a final layer of refinement based on human taste,” as identified in the approved plan.

**Ready for review; final KEEP/shipping verdict remains provisional pending listening.** Waveform measurements and transcript checks do not certify natural cadence, breath tails, voice continuity, or absence of audible clicks.

## Actual assembly

Times are precise edit boundaries, including natural quiet tails/heads; they are not word-level ASR estimates. Source means the published v6 file, whose timeline is also the v7 timeline.

| Output | Content | Source |
|---|---|---|
| 0:00.00–0:18.10 | Opening and basketball analogy | 0:00.00–0:18.10 |
| 0:18.10–0:32.50 | Before Training Starts | 1:05.80–1:20.20 |
| 0:32.50–0:58.77 | Three-phase overview | 1:24.47–1:50.73 |
| 0:58.77–1:03.43 | Shared loop introduction | 0:18.33–0:23.00 |
| 1:03.43–1:35.30 | Peanut-butter worked example | 0:29.07–1:00.93 |
| 1:35.30–1:41.93 | Weights definition | 2:03.97–2:10.60 |
| 1:41.93–1:51.80 | Pretraining introduction and scale | 1:50.73–2:00.60 |
| 1:51.80–4:31.07 | Pretraining outcomes through close | 2:10.60–4:49.87 |

All downstream narration from source 2:10.60 onward remains in its original sequence, moved 18.80 seconds earlier. Existing source grafts, the fixed-weights conclusion and standard close are retained.

## Teaching review of the new encoded candidate

Reviewed the current TrainingSection in index.html, lessons/training.md and the complete fresh ASR transcript. The following findings concern wording/content, not an auditory pass.

| Teaching point | Result | Output evidence |
|---|---|---|
| Capabilities and practice analogy | RICH | 0:00–0:17.78, chemistry/code/essay and basketball attempt/check/adjust. |
| Setup and data | TAUGHT | 0:18.42–0:32.14, initial internal numbers and training curriculum. Existing compression of the board’s modality list is retained. |
| Three phases and one comparison question | RICH | 0:32.94–0:58.48, names and purpose of all three phases and the basketball question. |
| Shared training loop | TAUGHT | 0:58.88–1:03.10, “AI training follows a similar pattern, guess, check, and adjust.” Located after the phase overview. “Across all three phases” is not explicitly spoken. |
| Worked training example | RICH | 1:03.78–1:35.04, peanut butter/cloud/jelly, compare, adjust, repeat. |
| Meaning of weights | TAUGHT | 1:35.64–1:41.52, full definition appears once before Pretraining. |
| Pretraining scale, outcome and limitation | RICH | ~1:42–2:18.16, vast text/code, thousand lifetimes, broad patterns, fluent basketball non-answer and instruction limitation. |
| Instruction tuning | RICH | 2:18.80–3:04.74, helpful question/answer examples, weight adjustments, complete basketball answer and remaining limitations. |
| Preference tuning | RICH | 3:05.48–3:57.62, answer comparison, feedback-driven weight updates, complete improved basketball answer, wrong answers can still sound right. |
| Training ends; ordinary chat uses fixed weights | TAUGHT | 3:58.40–4:20.28, ready for public use, new information can be used but does not change weights in real time. |
| Closing lines | MET | 4:21.28–4:26.80, both required lines present; canonical close is the literal final frame. |

No newly introduced wording error was identified in the transcript. Exact new bridge prose is an accepted difference, not a claim of verbatim alignment. The physical-force sentence, backward “before that loop” sentence, foundation sentence and repeated next-word-guessing line are absent.

## Boards, framing and continuous time

Current canonical JPGs used directly. Setup and phase overview remain full view. The loop uses the approved full-board framing and component rings. Dense phase panels use the established complete-active-section framing; inactive areas may leave the frame during the pan. The revised Pretraining panel remains fully inside its ring. The six full-board openings and all 24 preview states were inspected as actual encoded frames in the board contact sheets; selected dense-frame details and the final close were additionally inspected at full resolution.

**Longest single continuous teaching board: 27.80s. Longest adjacent-board chain: 40.00s.** Zooms, pans, holds and an internal audio cut on the same board do not reset the clock. The longest chain is Instruction Tuning’s final 12.20s plus Preference Tuning’s first 27.80s, 2:53.20–3:33.20. The three-phase board lasts 20.23s; Instruction and Preference retain the approved 25.47s and 27.80s initial runs rather than adding more repeated drawings.

| Board | Output interval | Unbroken duration |
|---|---|---|
| Before Training Starts | 0:18.10–0:32.50 | 14.40s |
| Three Phases of Training | 0:38.53–0:58.77 | 20.23s |
| The Training Loop | 1:03.43–1:23.37 | 19.93s |
| The Training Loop | 1:30.37–1:35.30 | 4.93s |
| 1 · Pretraining | 1:41.93–2:01.20 | 19.27s |
| 1 · Pretraining | 2:09.20–2:18.73 | 9.53s |
| 2 · Instruction Tuning | 2:18.73–2:44.20 | 25.47s |
| 2 · Instruction Tuning | 2:53.20–3:05.40 | 12.20s |
| 3 · Preference Tuning | 3:05.40–3:33.20 | 27.80s |
| 3 · Preference Tuning | 3:46.20–3:58.10 | 11.90s |

The retained closing message is a separate 9.80s span, 4:21.27–4:31.07, after a Notebook scene.

Reused drawing spans (all from the same published source, with animation played once followed by a settled hold when needed):

| Output | Drawing | Duration |
|---|---|---|
| 0:32.50–0:38.53 | Basketball drawing | 6.03s |
| 0:58.77–1:03.43 | Basketball drawing | 4.67s |
| 1:23.37–1:30.37 | Weights drawing | 7.00s |
| 1:35.30–1:41.93 | Weights drawing | 6.63s |
| 2:01.20–2:09.20 | Basketball drawing | 8.00s |
| 2:44.20–2:53.20 | Basketball drawing | 9.00s |
| 3:33.20–3:46.20 | Basketball drawing | 13.00s |

Original Notebook scenes also remain in the opening and fixed-weights conclusion. The earlier foundational-loop drawing is removed from the overview, so a second loop diagram is not introduced before the worked example. The existing opening paper-craft appearance and illustrative numbers/“Optimal Output” label in the weights donor remain disclosed limitations of this narrow repair.

## New audio joins for listening

No duration was added. Each cut joins complete sentence blocks inside measured quiet audio. Only 5ms on each side is smoothed toward a shared boundary sample; all other pre-encode PCM samples exactly match the approved source assembly. There is no inserted digital silence and no speech-level normalization. Encoded signal-to-error ratio against the edited master: 40.89dB; 768 samples of AAC padding, within one codec frame.

The following gaps were measured on the encoded candidate using 10ms RMS windows at −35dBFS. Quiet amplitude alone does not establish a natural join. Each context clip starts three seconds before its seam; clips are from the edited PCM master.

| Output join | Measured quiet gap | Listening aid |
|---|---|---|
| 0:18.10 | 0.70s | [7-second context clip](join-01-00543.wav) |
| 0:32.50 | 0.75s | [7-second context clip](join-02-00975.wav) |
| 0:58.77 | 0.34s | [7-second context clip](join-03-01763.wav) |
| 1:03.43 | 0.49s | [7-second context clip](join-04-01903.wav) |
| 1:35.30 | 0.53s | [7-second context clip](join-05-02859.wav) |
| 1:41.93 | 0.43s | [7-second context clip](join-06-03058.wav) |
| 1:51.80 | 0.58s | [7-second context clip](join-07-03354.wav) |

Previously existing graft regions also remain unauditioned in this pass, including approximately 3:34.70–3:38.50 and 3:58.10–4:05.93. They were not newly repaired.

## Verification and limitations

- Complete sequential decode confirms the planned 8,132 frames, 30 fps and 1280 × 720 size.
- Transition guard passes all 37 declared output boundaries. All 37 sequential contact strips were manually inspected; no stale-frame islands observed. See guard/transition-guard.json and guard/review-00.jpg through review-12.jpg.
- 24 encoded ring measurements (18 settled plus six during movement) measure 4 pixels on every sampled side. Width is independent of camera zoom.
- Every retained source frame and every reused drawing frame was compared against its intended decoded source frame. Maximum mean absolute pixel error stays below 2.57/255; board-state comparisons below 3.19/255, consistent with encoding.
- Protected published video, lesson Markdown and canonical board hashes are unchanged by this build. The previously approved page and board edits remain local; this build does not publish them.
- Fresh full small.en transcript generated and read. No duplicated weights definition, old backward reference or repeated pretraining mechanism remains. The closing lines are complete.
- **Not performed:** real-time end-to-end watching/listening; audible click/breath/cadence/voice matching at new or existing joins; mobile/player playback; manual inspection of every encoded frame. No full shipping certification is claimed.
- The raw Training rolls remain unavailable. This build decodes the published v6 once and re-encodes it, using the v7 repair recipe and current canonical assets; it does not re-encode the v7 candidate.
- Video Tracker was not accessed or updated. No commit, push or deployment was performed.

## Reproducibility

Candidate SHA-256: `a36e4985469826933a62be8fb5452287ef92f3de5b563a3e8d4376711092a850`.

Published source SHA-256: `01a8b51a707a59d6c29288ee9d86c5500aa5546882dc45c26b307f80d1755ebe`. The hash-verified snapshot path is in source-snapshot.json; keep it while this candidate is under review.

Build: `.video-venv/bin/python scripts/video/build_training_v8.py` (refuses to overwrite an existing candidate).

QA: `.video-venv/bin/python video-audit/training-repair-2026-09-27-v8/verify-candidate.py`.

Transcript: `HF_HUB_OFFLINE=1 .video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/training-v8.mp4 --model small.en --output-dir video-audit/training-repair-2026-09-27-v8/transcripts`.

Transition guard: `scripts/video/transition_guard.py`, with all 37 boundaries from edit-manifest.json and output directory guard/. The approved source/output frame ranges and picture map are preserved in edit-manifest.json and frame-map.json.
