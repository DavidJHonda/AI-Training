# Where AI Works Best — repaired review candidate v4

## Recommendation

**KEEP this repaired candidate for owner review. Do not ship without approval.**

The candidate now gives a student the lesson's essential teaching accurately and completely: AI is unusually useful for reshaping existing material, exploring possibilities, finding what matters in a large body of information, and working through problems; those strengths come from broad training exposure, but fluent output still requires human verification and judgment. The close lands on the lesson's exact distinction: **“Can try” is not “built for.”**

Candidate: `Prompts/where-ai-works-best-v4.mp4`

- SHA-256: `00195b53996c3aa2b78897864f95e4962bbf2cf8c917e09baf3b38909eb3c7b1`
- 1280×720, 30 fps, 8,317 decoded frames, 4:37.23
- Base: `Prompts/where-ai-works-best-1.mp4`
- Donor: `Prompts/where-ai-works-best-2.mp4`
- Build: `scripts/video/build_where_ai_works_best_v3.py`
- Manifest: `edit-manifest.json`

## Narration findings

Verdict on the exact candidate: **KEEP**.

Six complete teaching beats use roll 2 narration. Output timestamps below are on v4; source and donor spans are frame-exact in the manifest.

| Output time | Replacement |
| --- | --- |
| 1:38.33–1:40.57 | “Your material. A more useful form.” |
| 2:14.90–2:17.50 | “More possibilities. You choose the direction.” |
| 2:58.20–3:01.10 | “A lot to read. A clearer place to focus.” |
| 3:40.80–3:43.17 | “Work through the pieces. Make your own call.” |
| 3:53.77–3:58.27 | “Code, essays, arguments, emails, stories, and conversations.” |
| 4:31.00–4:33.23 | “Can try is not built for.” |

These repairs restore the current lesson's four takeaway lines, its clean training-format list, and its exact conclusion. They are whole-beat replacements rather than isolated word edits. No pauses were added. Donor audio was raised 1.7 dB to match the base narration.

Targeted small.en transcription on the rendered audio confirmed the repaired wording. v4's decoded audio MD5 is `125d394a78b240cef0ac79cc7aa13896`, identical to the fully listened v3 audio; the v4-only change is the matching picture during the format list. Silence detection found natural short gaps and a 4.10-second settled final hold, with no automatic one-second pauses introduced.

## Visual and production notes

- Current course boards replace the obsolete Notebook strength cards. Each board opens full-frame and stays compact; a constant 5px ring follows **why it fits**, **what it does**, **examples**, then the takeaway banner.
- The “AI Helped Us Build This Course” illustration keeps the approved camera walk.
- At 3:53.77–3:58.27, roll 2's matching **Training Phase: Massive Heterogeneous Ingestion** diagram now accompanies the six-format list. This removes v3's contradictory “Code Brackets” card.
- The standard close is the literal final frame and remains settled for four seconds after narration.
- Engine-corner treatment: 1,256 cloned frames, 412 inpainted frames, zero declined frames.
- All 20 declared visual boundaries passed `transition_guard.py`. The two v4-specific donor-picture boundary strips were inspected frame by frame and contain clean single cuts with no stale-frame island.
- Full-runtime contact sheets were inspected at four-second intervals, plus half-second samples across the v4-only donor-picture span and the literal final frame. No old strength cards, watermarks, inappropriate imagery, or contradictory visuals remain in those checks.

## Verification and limits

- Full video decode completed: 8,317/8,317 planned frames.
- Protected raw rolls, live lesson video, lesson Markdown, and current board assets all match their pre-build hashes.
- The full soundtrack was listened to in three contiguous chunks on v3; v4's decoded soundtrack is byte-identical.
- I could not perform a continuous real-time visual watch of every intermediate frame in this environment. Visual verification used the complete runtime contact-sheet pass, every-frame splice strips, targeted half-second sampling of the only changed v4 span, and final-frame inspection. Owner playback remains the final subjective motion/cadence check.
- The candidate is review-stage only. The canonical lesson video, `index.html`, lesson Markdown, and deployment were not changed by this build.

