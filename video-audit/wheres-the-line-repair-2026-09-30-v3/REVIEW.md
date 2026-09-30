# Where’s the Line v3 review build

Built the visual repair authorized by “build please” on September 30, 2026. The candidate adds four supporting cutaways, corrects the company-response illustration, and redraws board highlights at the current fixed 4 px delivery width. The longest uninterrupted board run is now 15.27 seconds. The original narration, pauses, total runtime, and close timing are preserved.

**Candidate:** [wheres-the-line-v3.mp4](../../Prompts/wheres-the-line-v3.mp4), 1280×720, 30 fps, 6,059 frames, 3:21.97.

**SHA-256:** `9c555f497e97f91ef046428c470871584dec85b70035bb67aad469d874cef33b`.

**Status:** Ready for visual review; not a whole-file shipping signoff. No installation, commit, push, or deployment performed.

## Changes

| Output time | Frames, end exclusive | Treatment |
|---|---|---|
| 1:36.60–2:10.50 | 2898–3915 | Rebuilt the exact canonical “How DraftKings Uses AI” board, preserving the complete opening, whole-card/outcome sequence, and compact camera. Two cutaways interrupt it as listed below. |
| 1:47.00–1:50.00 | 3210–3300 | Reused the installed betting-phone drawing from source frames 2130–2220 under the promotion explanation. |
| 2:03.00–2:06.00 | 3690–3780 | Reused the installed help-path diagram from source frames 2640–2730 under the early-intervention explanation. Its “Thought Experiment B” heading retains its hypothetical status. |
| 2:14.10–2:21.70 | 4023–4251 | Corrected the existing paper illustration: “DraftKings says,” “Existing monitoring,” and “Predictive system not adopted.” Neutral bullets replace the check/X. Preserved the paper style and used a restrained 1.5% push. |
| 2:25.67–3:13.27 | 4370–5798 | Rebuilt the exact canonical “Making the Responsible Choice” board with complete-card framing, the existing item sequence, fixed-width rings, and summary pullback. Two cutaways interrupt it below. |
| 2:37.00–2:41.00 | 4710–4830 | New photographic illustration of students checking an AI event plan for access barriers. Shows the affected student participating in the decision. |
| 2:55.00–2:58.00 | 5250–5340 | New photographic illustration of students testing an AI review tool, with human review and a visible way to challenge a result. |

Both cutaways within each board return to a settled view before the next highlighted point. Board 1 runs are 10.4, 13.0, and 4.5 seconds; Board 2 runs are 11.33, 14.0, and 15.27 seconds. The standard close from frame 5798 through the literal final frame is retained.

## Audio limitation

The wording at 2:21.72–2:27.16 remains unchanged: the transcript renders it as “AI will do exactly what it is asked to do, even if the end result is harming people.” The earlier review proposed the more accurate conditional wording from the lesson, but identified no usable donor. The retained transcript for the former full-2 roll contains a suitable sentence, but that video and its audio are absent from the workspace and available local source searches. Git history contains only the installed finished version.

This build therefore completes the available visual work without inventing a verified audio repair. No direct auditory audition was performed. The automatic transcript’s possible “predict” pronunciation issue at about 1:44 also remains a listening check, not a confirmed spoken error. A full listening and motion review remains necessary before shipping.

## Verification

- Actual encoded candidate sequentially decoded: 6,059 frames, 30 fps; frame timestamp spacing matches 1/30 second.
- Encoded AAC packets and decoded PCM each hash-identical to the source. No new audio seams or pauses.
- Transition guard: 14/14 pass, zero failed boundaries. Every-frame strips inspected for all declared cuts; no stale intermediate scene observed.
- All eight settled highlight states inspected at full resolution; complete active cards/sections are visible. Full-board openings and final closing frame inspected.
- All five changed illustration spans inspected in actual encoded frames. New text is readable and stays within the crop.
- Eleven unchanged-picture samples, including the ending, differ by at most 0.433 mean pixel levels after re-encoding; maximum mean luma shift is 0.018. Source YUV was preserved before the single final video encode outside changed spans.
- Installed video, canonical JPGs, lesson text, and `index.html` remain hash-identical to their build-start versions.
- These checks certify the technical visual repair; frame sampling and transition strips do not substitute for continuous audiovisual viewing.

## Sources and build records

Only the finished source survives, so the build uses the immutable video from Git commit `000722b8`, materialized at `/private/tmp/wheres-the-line-v3-source-848ac733.mp4`. Its SHA-256 is `848ac733051b1a1ad1856fbb60099b54e2978ce7651027d5f7e7575cad47ff51`, identical to the installed file. The builder can recover that snapshot again and asserts its hash. The candidate requires one additional video encode; audio is copied.

- [Builder](../../scripts/video/build_wheres_the_line_v3.py)
- [QA command](../../scripts/video/qa_wheres_the_line_v3.py)
- [Manifest and hashes](edit-manifest.json)
- [Measured QA](qa.json)
- [Transition checks](transitions/transition-guard.json)
- [Affected people image](../../scripts/video/assets/wheres-the-line-v3/affected.png)
- [Protection and review image](../../scripts/video/assets/wheres-the-line-v3/protection.png)
- [Corrected response image](../../scripts/video/assets/wheres-the-line-v3/response.png)
- [Exact generation and edit prompts](../../scripts/video/assets/wheres-the-line-v3/PROMPTS.json)

All three image assets were produced with the built-in imagegen tool and saved in the repository. The two student scenes are purpose-generated photographic illustrations; the response image is an edit of source frame 4023. Existing effective Notebook scenes outside the identified changes remain in place.

Commands executed from the repository root:

```sh
.video-venv/bin/python scripts/video/build_wheres_the_line_v3.py --prepare-only
.video-venv/bin/python scripts/video/build_wheres_the_line_v3.py
.video-venv/bin/python scripts/video/qa_wheres_the_line_v3.py
```
