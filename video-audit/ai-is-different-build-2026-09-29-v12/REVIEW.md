# AI Is Different v12 — September 29 repair candidate

**Scope:** the user approved the September 29 repair with “build it,” then authorized local shipping with “ship it” after the remaining listening limitation was disclosed. **Shipped locally; queued for batch deployment.** See the shipping record below.

**Candidate:** `Prompts/ai-is-different-v12.mp4` — 4:45.567, 8,567 frames at 30 fps, 1280×720. This adds 239 frames (7.967 seconds) to the live v11.

## Implemented changes

- **3:54.40–4:04.467:** replace the abbreviated deepfake clause with the complete two-sentence explanation from previous shipped v9: “There is also the issue of deepfakes. The system can use its patterns to create convincing fake media that can be used to target or humiliate individuals.” The retained scams sentence leads into this beat; “Even without malicious intent, AI can hallucinate” follows it.
- **3:58.90–4:02.90:** a new full-frame, four-second supporting image shows a fictional student discovering fabricated video of himself. The illustration is visibly annotated FABRICATED VIDEO. The course board returns before the next risk.
- **Two Ideas Behind Every Answer:** introduce each complete card before its section rings. Learn First whole-card at 0:54.167, Training explanation at 0:55.933, Patterns at 0:58.100. The right-card introduction starts beneath the preserved response animation, is visible on return at 1:05.567, then Probability at 1:06.533 and Prediction at 1:12.467. Full-board compact camera preserved.
- **Structured vs. Unstructured Data:** complete Normal Software card at 2:50.733, Input & Output at 2:55.333; complete AI card at 3:00.600; input/output ring carries through its associated cutaway and is visible briefly on return before the app-availability qualifier at 3:09.733. The existing useful input/output drawings remain.
- **Rules vs. Patterns:** keep full view through the question, then use the established complete-card camera. Preserve the explicitly approved 29.267-second uninterrupted board run.
- Rebuilt board rings use the existing exact-width supersampled rasterizer with the shared fixed 4-pixel width policy. The unaffected Rules board retains its established treatment.

The novel image is a supporting scene, not a replacement course board. It was created with the built-in **imagegen** tool and visually checked. Saved asset: [student-fabricated-video.png](../../scripts/video/assets/ai-is-different-deepfake/student-fabricated-video.png). Exact generation prompt: [PROMPT.txt](../../scripts/video/assets/ai-is-different-deepfake/PROMPT.txt). The original generated image remains in the tool's output directory; the build references the workspace copy.

## Preserved decisions

All three pristine September 26 rolls match the hashes recorded by the v11 manifest. The build reassembles that approved source timeline directly; it does not re-encode the live video as its base. Existing Notebook diagrams, robot/chef scenes, legal-pad story, data examples, backpack, and guardrail animations remain. No new pauses were added. The removed repetitive input/output narration remains removed.

The standard canonical white close is retained with a 48-frame hold, 150-frame push to 1.2×, then settled hold. Its new start is 4:33.267 and it remains the literal final frame. The longer Kryptonite board is divided by the image insert into 14.4- and 10.233-second runs; the longest unbroken teaching-board run remains the owner-approved Rules vs. Patterns exception.

## Donor and joins

Donor: `donor-v9.mp4`, recovered from `d88a1399:course-assets/ai-is-different/ai-is-different.mp4`, SHA-256 `c7a9dbb804a30673aca2df73c4cd6b1f36256518ef68b624f08c880c9657ce66`. It is an already encoded historical source, the only recovered source used for this new narration graft. Existing production uses the pristine raw rolls.

The donor extraction uses frames **7936–8238** (4:24.533–4:34.600), replacing raw roll 1 frames **6858–6921**. Cuts were chosen from the waveform's quiet gaps, preserving the complete final word beyond its approximate ASR boundary. Donor gain is **−4.0 dB**, based on the measured approximately 4 dB loudness difference. There are 5 ms room-tone fades at the outer audio boundaries. The internal picture cutaway does not split, fade, or restart the donor audio.

A fresh full transcription of the assembled audio confirms the full new wording and both surrounding sentences. The entry has roughly 0.4 seconds of low-level gap, with a brief threshold crossing; the exit has about 0.71 seconds below −45 dBFS. These measurements are not a listening pass.

## Teaching and review status

The previously THIN deepfake point now explains convincing fake media and its potential to target or humiliate people. The remainder carries the reviewed v11 teaching and accepted compression; both closing lines remain verbatim. **Content supports KEEP, subject to audible verification; this is not a certified whole-file shipping verdict.**

No real-time end-to-end audiovisual playback or listening has been completed. The new donor joins require review around **3:54 and 4:04.5**, especially voice continuity and cadence. Existing unlistened graft joins remain around 1:20, 1:54, and 2:35, with narration cuts around 3:09 and 3:24. A short encoded audio review excerpt is supplied as [deepfake-review.mp3](deepfake-review.mp3), covering 3:49–4:13 of the candidate.

Build: `scripts/video/build_ai_is_different_v12.py`; verification: `scripts/video/qa_ai_is_different_v12.py`. `edit-manifest.json` records the exact source/output mapping, asset hashes, ring coordinates, and declared boundaries. `transcript/edited.txt` contains the full assembled transcript. Encoded checks and final hash follow.


## Final encoded checks

- **PASS:** all 8,567 video frames decoded, matching the plan; 1280×720 at 30 fps. Every rendered leg matched its planned span. Prepared audio has exactly 13,707,200 samples at 48 kHz.
- **PASS:** transition guard passed all 37 declared boundaries. All 37 every-frame boundary strips were visually inspected, including both picture cuts and both narration joins for the new insert. No old-board flashes or short visual islands were found. Retained Notebook animations begin in their existing fade-in state.
- Six contact sheets sampled the complete encoded runtime every two seconds; changed states and the literal final frame were also inspected. Full-frame insert framing and the standard closing layout are correct.
- Rebuilt rings use the fixed 4-pixel renderer; a native rasterizer test confirms 4-pixel straight sides. The encoded colour-threshold audit measures 2–4 solid-core pixels on rebuilt rings because of colour thresholds/chroma subsampling; the magnified crop retains the intended visible stroke. The untouched Rules board retains one 5-pixel sampled stroke. This is a preserved pre-existing exception, not a blanket claim that every encoded ring measures exactly four solid pixels.
- Fresh transcription of the final encoded 3:45–4:18 context confirms both complete donor sentences and the adjoining scams and hallucination sentences. Encoded quiet-gap measurements match the assembly: entry 3:54.15–3:54.57 with a brief threshold crossing; exit 4:04.10–4:04.81 (10 ms RMS windows, −45 dBFS threshold).
- All protected source rolls, the historical donor, lesson file, canonical boards, and current published MP4 are byte-identical to their pre-build hashes. No live lesson references were changed.
- **Remaining:** end-to-end listening and real-time audiovisual playback. Neither transcripts nor frame inspection certify voice continuity or cadence. Review the new joins at 3:54 and 4:04.5 before shipping.

Candidate SHA-256: `758d62de72dd420870a974682fecf96a83b40558bd22e9af7bc309b68c3fa9b1`.

Evidence: [qa.json](qa.json), [transition guard](guard/transition-guard.md), [encoded transcript](encoded-transcript/deepfake-encoded-context.txt), [encoded quiet gaps](graft-gap-encoded.json), [ring audit](ring-audit/ring-stroke.txt), [rasterizer check](ring-rasterizer-check.json).


## Local shipping — 2026-09-29

User authorization: “ship it.” Installed the exact reviewed v12 candidate at `course-assets/ai-is-different/ai-is-different.mp4` and committed only that MP4 and its `LESSON_VIDEOS.aivscode` cache key in **`f849742ca2f077a035e3be309adcaa78758bfdb4`**. The cache key is `20260929ship1`; the rounded display remains **5 min** for the 4:45.567 runtime. Installed and committed bytes both match the candidate SHA-256 above.

**Status: shipped locally; queued for batch deployment.** No push or deployment was performed, and public availability has not been verified for v12. The assistant did not perform listening or real-time playback; owner shipping authorization followed explicit disclosure of those limitations and does not turn them into passed checks. The pre-shipping verification results above remain the evidence for this exact file.

Render-scratch cleanup is restricted to this v12 audit folder; source rolls, the candidate, donor, review evidence, transcripts, and audio review MP3 are retained.
