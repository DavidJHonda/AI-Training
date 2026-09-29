# Where AI Works Best v8 — September 29, 2026

**Built and verified as a review candidate:** `Prompts/where-ai-works-best-v8.mp4`, 3:52.900, 1280×720 at 30 fps, 6,987 frames, 22,267,887 bytes.

SHA-256: `32c3113238eda2d98ae818c432ceb2b359ba7227c6f880c3461d32b73194238e`.

Approved scope: the user said “build it” after the [current-spec evaluation](../where-ai-works-best-current-spec-review-2026-09-29/REVIEW.md). This is a narrow repair of the missing translation example and oversized highlights. It does not install the candidate, change the course page, commit a release, or deploy.

## Changes

- Replaced v7 output frames 2156–2516 (1:11.867–1:23.867) with one complete examples passage from roll 1, source frames 2257–2643 (1:15.233–1:28.100). Both audio endpoints are in measured quiet intervals. The donor is 0.8 dB quieter in the assembly to match the original examples passage (measured approximately −19.6 versus −20.4 LUFS before adjustment).
- New output examples: 1:11.867–1:24.733. It now includes study notes, a voice memo, **“translate a message,”** and technical instructions. No internal audio cut was made at the visual return.
- Kept the study-guide/to-do-list drawings; return to the full canonical Reshape board at 1:19.933. Its complete EXAMPLES section is outlined from 1:20.400; contextual ASR places “translate” at 1:20.440. The board returns unmarked before that onset. The takeaway switches to its banner near 1:25.113, after a brief unmarked transition.
- Corrected the Explore WHY outline and three Problems teal outline appearances using the even-snapped, outer-minus-inner drawer established in Your Home Base v6. The new blue EXAMPLES outline uses that drawer too. Other existing ring geometry and camera choices are preserved. The fix lives in a v8-specific helper; the shared renderer was not edited.
- Reassembled from the same three pristine raw rolls and current canonical boards. Preserved all other source selections, existing graft gains, the existing Explore phrase cut, the exposure-banner patch, room-tone pause, and standard close. Duration increases by 26 frames (0.867 s), to **3:52.900 / 6,987 frames**.

## Narration

The contextual assembled-audio transcript reads:

> Just provide something you already have and ask the AI to return it in a different format, preserving your original meaning. For example, take messy notes and have AI organize them into a clean study guide. Turn a scattered voice memo into a strict to-do list, translate a message, or rewrite technical instructions into plain English. Your material, a more useful form.

This repairs the identified omission. “Into another language” is compressed to “translate a message,” as disclosed in the approved plan. The exact transfer sentence “It learned patterns it can apply to new problems” remains the previously accepted omission. No new narration or synthetic speech was created.

No pauses were added. The visual-only row division inside the new donor passage does not divide the PCM block or apply an audio fade. `new-seam-levels.json` records quiet entry/exit measurements, and `reshape-context.wav` provides surrounding sentences for listening.

## Visual plan carried through

The five teaching boards remain compact, full-view, and stationary. The standard closing asset retains its 48-frame hold, 150-frame push to 1.2×, and settled hold. Supporting drawings retain their teaching roles; no new images or stock photographs were introduced.

The longest individual board appearance remains **19.0 seconds**. The longest uninterrupted sequence across adjacent boards is **25.867 seconds**, the returned Reshape examples/takeaway followed by Explore's first board appearance. Both remain within the current §8b limits. Exact planned runs are in `board-runs.json`.

## Verification status

Finished-file verification completed:

- **Frame count:** full sequential decode yields 6,987/6,987 planned frames at 30 fps.
- **Narration:** read the complete fresh small.en transcript from the encoded MP4. It confirms all four Reshape examples, all nine required lines as words, the four named strengths, and the preserved lesson arc. The missing example is repaired; a formal listening-based KEEP certification is still withheld for the limitation below. ASR punctuation cannot certify the cadence of the close.
- **Rings:** all **93 detected course-ring samples across 18 runs measure 4.0 px**, including the previously oversized amber/teal runs and new blue EXAMPLES ring. The gold detections are the Explore illustration, not course outlines. Scan interval: one second. Every changed settled ring was also inspected at full resolution in the encoded file.
- **Transitions:** automated guard passes **27/27** declared boundaries. Inspected every-frame strips for the new donor entry (frame 2156), drawing-to-board return (2398), and donor exit/takeaway transition (2542). No stale board or drawing frames appear in those strips.
- **Audio preservation:** decoded PCM before the repair matches v7 exactly in the compared interval. After the repair, accounting for the 26-frame offset, correlation is **0.9999768**; differences are consistent with AAC encoding. New donor audio correlates **0.9999821** with the selected source after the specified gain. These are preservation checks, not listening verdicts.
- **Visual preservation:** sampled retained frames agree with v7 to a maximum mean absolute channel difference of 0.0789/255, except the deliberately unmarked Reshape takeaway lead-in (frame 2550, 1.3402/255). The initial QA exclusion window did not include those additional 12 lead-in frames; the larger difference is the planned disappearance of the old early banner ring, not unexpected changed imagery. Raw measurements are retained in `qa.json` and `qa.log`.
- **Silences:** at a −40 dB threshold the donor entry gap is 1:11.653–1:12.292 (0.639 s), and its exit has quiet intervals 1:24.304–1:24.961 (0.657 s) and 1:24.962–1:25.076 (0.114 s), separated by a 1 ms threshold crossing. The retained pre-close gap measures 3:42.939–3:44.048 (1.109 s) at this threshold. No new silence was inserted; the older 1.02 s close measurement used a different measurement context.
- **Assets and protection:** all protected files retain their pre-build hashes, including the course MP4, prior v7 candidate, raw rolls, Markdown, and six canonical JPGs. Engine-mark cleanup reports 3,306 cloned frames, 63 inpainted frames, and zero declined frames.
- **Visual review:** inspected the four encoded contact sheets spanning the whole file, full-size changed ring frames, affected transition strips, and the literal final frame. Full-board framing and final close are intact. Continuous playback was not performed.

Evidence: `edit-manifest.json`, `qa.json`, `qa.log`, `ring-stroke.txt`, `transcript/where-ai-works-best-v8.txt`, `transitions/`, `silences.txt`, `overview-*.jpg`, and `frames/`. A short contextual video is available as `reshape-review.mp4` (full-video 1:05–1:29).

**Listening limitation:** nothing was heard by ear in this session. ASR, waveform measurements, and sample correlations do not certify cadence or an inaudible seam. The new donor entry/exit, existing “Your material” cadence, Explore phrase cut, other donor joins, and closing statements still require listening. Continuous real-time motion review is also not claimed. This is a review candidate, not a new whole-file shipping certification.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_where_ai_works_best_v8.py`.

The board legs rendered successfully on the first preparation run; a manifest-key collision was corrected before final encoding. Final encoding used `--render-existing` to reuse those verified v8 legs. `build.log` retains the preparation record; `render.log` records the final run.

Build helper: `scripts/video/where_ai_works_best_v8_support.py`. Encoded verification: `scripts/video/qa_where_ai_works_best_v8.py`. Raw rolls, prior v7 candidate, course MP4, lesson Markdown, and all canonical JPGs are protected by hashes in `edit-manifest.json`.
