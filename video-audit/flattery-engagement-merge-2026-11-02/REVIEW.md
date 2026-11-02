# Flattery & Engagement v1

Built November 2, 2026 at David’s request to try the merged lesson using the two current installed videos. **Review candidate only.** No course video installed, course text changed, Git commit made, tracker edited, or publication performed in this video task.

Candidate: `Prompts/flattery-engagement-v1.mp4`.
Runtime: **6:27.133**, 1280×720, 30fps, 11,614 frames. The original pair totals 8:23.400; the merge removes **1:56.267**.
SHA-256: `8f0c43a1fc30be433e65f7c528df645b45fcd88ea7d8961500ee06f34d428b08`.

## What changed

All Flattery teaching survives through “Ask AI to improve the work, not approve of you.” It leads into the existing Engagement opening, slope comparison, and infinite-scroll explanation. The infinite-scroll takeaway now leads directly back to AI chat, then the commercial engagement explanation. Raskin’s regret/lifetimes claim, autoplay/streak material, and the entire Meta settlement/stopping-points discussion are removed.

The four-second existing line “The engagement trap feels like a helpful conversation that keeps going” introduces the second topic. The newly written page transition (“Even when the help is useful…”) has no recorded source. This version uses the existing complete sentence rather than synthetic speech or a word-level reconstruction. It leaves the page unchanged.

Both old closing pictures are replaced with the exact current merged closing JPG. Existing recorded lines now say, in order: “Look for specifics, not approval. Know what you came for. When you have it, choose what happens next.” The closing begins at 6:15.567, holds 48 frames, pushes to 1.2x over 150 frames, then holds through the literal final frame. No new pauses or overall volume changes.

The source MP4s are the stable v13 Flattery and v15 Engagement candidates, verified byte-identical to their installed `course-assets` counterparts. Original raw generations were unavailable for those shipped edits. This assembly encodes the retained material once; it preserves the existing visuals and animation timing except for two frames at the infinite-scroll-to-AI splice, where the incoming chat’s first frame covers the preceding phone picture.

## Teaching coverage against the merged lesson

The entire encoded transcript was read against the current lesson. These are **transcript-based coverage findings**, not a completed audiovisual KEEP verdict.

| Teaching point | Coverage | Candidate time / evidence |
|---|---|---|
| Flattery is approval mistaken for evaluation | TAUGHT | 0:00–0:22; encouragement versus objective evaluation |
| Gatsby intro, empty praise, missing thesis, specific next step | RICH | 0:23–1:22; complete worked example and positive-feedback qualifier |
| Human reviewers, agreeable answers, learned preference | RICH | 1:22–1:52; all three RLHF board stages explained |
| Sycophancy, gag-product example, rollback and ongoing mitigation | TAUGHT | 1:53–2:40; story, quoted praise, three-day rollback, multiple assistants, improved but not gone |
| Ask without supplying a verdict | RICH | 2:44–3:04; weak/better prompt and reason |
| Ask for gaps and an opposing view | RICH | 3:05–3:24; both prompts and specific targets |
| Use a rubric, quote evidence, identify improvement; check the result | RICH | 3:24–3:52; example, explanation and accuracy/grade caveat |
| Saved instruction | RICH | 3:59–4:11; app-support qualifier and complete “Be direct with me…” instruction |
| Useful help can continue without a conscious choice | TAUGHT | 4:15–4:29; existing recorded transition and conscious-decision distinction |
| Slope chat, useful follow-ups, one minute versus twenty-five | RICH for the trap distinction | 4:30–5:20; both outcomes and why usefulness alone does not decide whether to continue |
| Engagement definition | TAUGHT | 5:20–5:26; spending time never originally chosen |
| Infinite scroll removes a decision point | RICH | 5:26–5:52; Raskin, Next click, pause, automatic continuation, friction also being a choice |
| AI’s missing page break | TAUGHT | 5:52–6:02; answer ends, conversation continues, follow-up generated |
| Engagement incentives and habit | TAUGHT | 6:02–6:15; frequency, session length, advertising, purchases, subscriptions, daily habit |
| Combined closing | MET | 6:15–6:22; all three sentences spoken in the approved order |

Existing source limitations remain: the slope formula is spoken but its plain-language definition is displayed rather than narrated; this example teaches the continuation choice, not slope as a mathematics objective. The gag response is abbreviated in the previously approved video, and the under-18 aside is not spoken. The source’s sycophancy story phrase around 2:00 produces inconsistent ASR (“prime exhale…” for the apparent “prime example…”); this unchanged phrase requires listening rather than treating ASR as proof of pronunciation. No newly synthesized narration was used to fill those differences.

The on-page lab and stopping quiz are intentionally not narrated. They remain unchanged in the course.

## Visual treatment

The six existing teaching boards retain their approved highlighting and camera work. The slope board keeps David’s explicit zoom/pan exception. Supporting drawings and animations remain attached to their original narration: encouraging student, weak-work reaction, agreeable-output comparison, sycophancy definition, gag product, rollback devices, training preferences, neutral input, rubric alignment, standards/checklist, continuing-chat phone, task-to-follow-up loop, chat reveal, Raskin interface, and engagement-metrics loop.

The longest retained uninterrupted board run is the approximately 60-second Gatsby worked example (source 0:23–1:23), an existing approved treatment. The training board also retains its approximately 30-second run. This merge does not claim a new broad board-hold redesign. Changed comparison/tactic treatments otherwise retain their source breaks; the new closing lasts 11.567 seconds. Exact board plan and source ranges are in `EDIT-PLAN.md`.

## Actual encoded-file verification

- Fully decoded all 11,614 frames and verified regular 1/30-second presentation intervals.
- Compared every output frame against its declared source frame, or the newly rendered canonical closing, at 80×45 thumbnail resolution. Maximum mean channel error: 2.941/255. This verifies picture mapping, not perceptual equality after encoding.
- Encoded audio versus planned floating-point PCM correlation: **0.999990**.
- All four edits land inside measured encoded quiet intervals. No new silence was inserted:

| Edit | Time | Actual quiet interval | Gap |
|---|---|---|---|
| Flattery to Engagement | 4:15.367 | 4:15.242–4:15.632 | 0.391s |
| Infinite scroll to AI | 5:52.033 | 5:51.878–5:52.180 | 0.302s |
| Merged closing begins | 6:15.567 | 6:15.520–6:15.807 | 0.286s |
| Second recorded closing voice | 6:18.067 | 6:17.850–6:18.313 | 0.463s |

- Transition guard passed **4/4** declared boundaries. Inspected every-frame strips for all four and all four overview sheets. No old closing, phone-shot flash, or settlement/stopping-points material appears at the new joins. The AI-chat transition starts with that source animation’s brief paper-background reveal.
- Inspected the encoded full-size final frame: exact merged text, complete sticky and pill, no clipping.
- New transcription confirms the retained teaching and closing, and the absence of the removed lifetime estimate and settlement discussion.
- Installed videos, lesson text, index, manifest and canonical boards retain their pre-build hashes.

## Listening and release status

**Perceptual listening and continuous audiovisual playback were not performed.** No available tool supplied audio audition. Transcription, waveform measurements and image sequences cannot certify voice continuity or conversational cadence. This is ready for David’s review, with special attention to **4:15** and the closing at **6:15–6:22**; it is not a whole-file shipping certification.

Convenient encoded excerpts:

- `qa/flattery-to-engagement.mp4`: 20s starting at full-video 4:08.367.
- `qa/scroll-to-ai.mp4`: 21s starting at full-video 5:46.033.
- `qa/combined-closing.mp4`: 16.567s starting at full-video 6:10.567.

## Reproduction and evidence

Build: `.video-venv/bin/python scripts/video/build_flattery_engagement_v1.py`.
QA: `.video-venv/bin/python scripts/video/qa_flattery_engagement_v1.py`.

`edit-manifest.json` records source hashes, half-open source/output frame ranges, quiet-boundary blends, the canonical close, and protected-file hashes. `qa/summary.json`, `qa/transcript.txt`, `qa/silences.txt`, overview sheets and `qa/transitions/` record checks on the encoded result. The builder refuses to overwrite the candidate; a revision requires a new version filename.
