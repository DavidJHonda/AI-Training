# Hallucination v19 — shorter worked applications

Narrow, approved edit of [v18](../../Prompts/hallucination-v18.mp4). [V19 candidate](../../Prompts/hallucination-v19.mp4): 4:21.300 video, 7,839 frames at 30 fps, 1280×720. The two applications now occupy **3:28.967–4:10.700 (41.733 seconds)**, down from 62.400 seconds. The edit removes 20.667 seconds. Shipped locally on 2026-09-30 after the owner’s “ship it” approval; queued for batch deployment.

## Teaching retained

Both examples remain because they teach different checks. Stanford demonstrates looking for the original paper, rather than accepting a university name as proof. No paper supports the invented numbers, and the narration retains the real-search caveat: failing to find a source does not strictly prove the claim false; it remains unverified. Pizza demonstrates finding a real comment, then rejecting its use as cooking evidence because it was a joke. The takeaway remains: finding real text is insufficient; it must support the claim.

The second spoken reading of Stanford's year, sample size, and percentage is removed. Those details were already fully introduced and remain visible in the application. Repeated “First / Second / Third” announcements are removed from both applications. The three-step teaching earlier in the video, including v18's clearer Find the Source / Check the Match passage, is retained. The existing complete sentences are used; no new narration or donor voice was generated.

Teaching assessment on transcript evidence: Stanford source-checking **TAUGHT**; missing-source caveat **TAUGHT**; pizza's real-source/wrong-meaning distinction **RICH**; Check the Match application **TAUGHT**; both closing lines **MET**. The earlier lesson is unchanged. This is a review candidate, not a claim of completed subjective listening or a shipping verdict.

## Exact cuts and audio joins

All source ranges below refer to pristine roll 3; v18 times are three seconds later in this section. Cuts are half-open frame ranges.

| Raw source frames | Raw source time | Removed content | New join |
|---|---|---|---|
| 6235–6577 | 3:27.833–3:39.233 | First/Second announcements and repeated Stanford details | 3:30.833 |
| 6727–6783 | 3:44.233–3:46.100 | Stanford Third announcement | 3:35.833 |
| 7333–7404 | 4:04.433–4:06.800 | Pizza First announcement | 3:54.167 |
| 7494–7571 | 4:09.800–4:12.367 | Pizza Second announcement | 3:57.167 |
| 7713–7787 | 4:17.100–4:19.567 | Pizza Third announcement | 4:01.900 |

Joins are in measured quiet gaps, with 5 ms smoothing and no inserted pauses. The base audio is the lossless assembled v18 PCM, preserving its original source and donor choices. Pictures are rebuilt from pristine rolls through the v18 renderer, rather than re-encoding v18's video.

## Picture timing

- At 3:28.967–3:30.833, show the established Stanford claim from raw frame 6420. This lets the abbreviated introduction identify the example without an unfinished opening animation.
- At 3:44.733–3:50.400, hold the settled unverified-study result from raw frame 7050. The source animation otherwise introduces pizza before the Stanford caveat finishes. Pizza now appears just before its spoken introduction at approximately 3:50.55.
- Other retained application footage follows its source narration through the cuts. The search and missing-study outcome, real Reddit source, and joke-versus-evidence reveal remain.
- All canonical course boards and their highlighting retain v18's timing and appearance. Longest board run: 27.8 seconds for the complete opening chat reading; Why: 18.73 seconds; Check the Claim: 19.60 seconds. No new board or ring treatment.
- The standard close moves to 4:10.700. Its 48-frame hold, 150-frame push, and 120-frame tail remain.

## Review limits and reproduction

Encoded QA passed: all 7,839 frames decoded without errors; 221 preview samples matched their intended renders; 254 retained-picture samples matched v18 at mapped source frames (maximum MAE 0.460/255). The five joins measure approximately −72 to −78 dBFS after smoothing. Assembled audio exactly matches retained v18 PCM outside the 5 ms bridges; the encoded audio matches at zero offset with 45.63 dB signal-to-error ratio. Independent small.en transcription of the final export preserves every retained application sentence and both closing lines, with no repeated step announcements or Stanford-number recital.

All 30 transition guards passed. Every boundary strip, one-second application contact sheets, and full-resolution frames of the retimed claim, Stanford result, pizza handoff, and joke outcome were inspected. No stale-frame islands were found. All 14 protected source, prior-candidate, PCM, lesson, index, canonical-board, and live-video files matched their pre-build hashes. No full subjective audiovisual playback was performed.

Candidate SHA-256: `312154b35f9c0bde4ec85c3d1b3f1f103d8fae8da7f7a7fe9c8b52fd05f953f1`.

Subjective listening and continuous real-time audiovisual playback are unperformed. Transcription and signal measurements do not establish whether a join sounds natural. The five join times above are provided for listening. `application-review.mp4` and `application-review.wav` begin at output 3:28.5 and include the full revised application sequence and closing lines.

Build previews: `.video-venv/bin/python scripts/video/build_hallucination_v19.py --preview`. Build candidate: same command without `--preview`; it refuses an existing candidate path. Encoded checks: `.video-venv/bin/python scripts/video/qa_hallucination_v19.py`.

Evidence is recorded in `edit-manifest.json`, `qa.json`, `encoded-application-asr.json`, `mapped-transcript.json`, `encoded-preview/`, and `transitions/`. The mapped whole-video transcript is source-derived and not manually corrected.

## Local release — 2026-09-30

Installed the approved candidate at `course-assets/hallucination/hallucination.mp4`; its bytes match the candidate SHA-256 above. Updated only the Hallucination entry in `LESSON_VIDEOS` to cache key `20260930ship19` and display runtime `4 min`, and synchronized the asset manifest hash and byte count. Verified the canonical reference and installed bytes.

Local commit: `bdfc89d0c32f518bf428baa4e5bb9b9ee3763786` — `Ship Hallucination v19 with shorter worked examples`. The commit contains only the canonical video and its two metadata changes. Prior unrelated working changes were preserved. No push or deployment was performed. **Shipped locally; queued for batch deployment.**

The owner authorized shipping after the disclosed listening limitation. Subjective listening remains unperformed by the agent; the authorization is not recorded as evidence that listening occurred. Prior encoded QA applies to the byte-identical installed candidate. The external Video Tracker was not accessed or modified.

Cleanup is limited to this v19 build’s regenerable WAV and canvas scratch. The MP4 review clip, source rolls, candidates, build scripts, transcripts, manifests, contact sheets, transition strips, and earlier v18 source PCM dependency remain locally available.
