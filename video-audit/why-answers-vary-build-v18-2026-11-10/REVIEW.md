# Why Answers Vary v18 — thinking-time narration

Narrow repair requested by David: use version 6's narration about the model and
its thinking time. Candidate: `Prompts/why-answers-vary-v18.mp4`, 1280 × 720,
30 fps, 5,473 frames, **3:02.43**. Review only; installed lesson video unchanged.

## Edit

Replace v17 **0:17.50–0:21.10**, “First, the specific model you use and its
processing time,” with raw version 6 **0:17.90–0:22.10**:

> First, the model you use and its thinking time changes the answer.

The complete donor sentence occupies output **0:17.50–0:21.70**, adding
0.6 seconds. The first overview card's existing highlight stays on screen for
that extra time. Later visuals and audio shift together by 0.6 seconds. No
speech stretching, synthesized voice, or isolated-word replacement.

Both splice endpoints are inside measured quiet gaps. The donor gain is
−0.519 dB, the established version-6-to-version-4 speech-level match, with
5ms transitions through matching source room tone. Unaffected PCM is identical
outside the two seam regions. Pictures were assembled from the original source
rolls and canonical boards, avoiding another finished-video transcoding pass.

The v17 one-second pause, continuous canonical temperature board with zoom,
and removed Other callout are preserved. Source hashes, frame mappings, and
donor endpoints are recorded in `edit-manifest.json`.

## Verification and review limits

Encoded decode, transition, protected-file, and wording results are in `qa.json`.
The independent encoded narration check is in `encoded-graft-asr.json`; the
12.5-second context excerpt is `encoded-thinking-time-context.wav`.

Complete encoded decode and all 34 transition checks passed, with exactly 5,473
frames. Encoded ASR confirms the full thinking-time sentence and the following
“Second, what the AI receives” beat. The six strips covering the graft, added
hold, and overview highlight changes were visually inspected, along with the
settled first-card frame. Highlights remain aligned; protected hashes pass.

Perceptual listening and uninterrupted audiovisual playback have not been
performed. Listen to **0:17–0:23** to judge donor voice continuity and cadence.
ASR is a wording check, not a listening certificate.

Pre-existing issues outside this repair remain: the overview techniques sentence
is paraphrased rather than the exact approved line, and the repetition/creativity
explanation lacks the approved “can” qualifiers. The prior review records these
limitations; this narrow repair does not establish whole-file shipping approval.

No installation, commit, push, or publication was performed.

Build: `.video-venv/bin/python scripts/video/build_why_answers_vary_v18.py`.
Verify: `.video-venv/bin/python video-audit/why-answers-vary-build-v18-2026-11-10/verify.py`.

## Local shipping — 2026-11-10

David explicitly approved this candidate with “ship it,” following the disclosed
listening limitation. Installed and committed as `9df24ee38b40b44aa2dd4e53a8f9823f62189777`.

Installed SHA-256: `dac4a6939ee3985fa15f9c1777a603634eebb8647194ff90373f3a7869fa9ddc`; 14,598,976 bytes.
The canonical video reference uses `20261110ship18`; displayed runtime stays
3 min (actual 3:02.43). Only the video, its manifest record, and that reference
were committed. Unrelated working changes remain intact.

All 12 Why Answers Vary asset records verify. The global asset check reports
the same pre-existing How AI Answers board mismatch seen before installation.
No perceptual listening was performed or claimed. Previous narration limitations
remain documented above; owner shipping authorization is recorded separately.

**Shipped locally; queued for batch deployment.** No push or deployment performed.

Post-commit cleanup removed 29 regenerable WAV/canvas intermediates (about
0.15 GB) only from this lesson’s v15–v18 build folders. Raw generations, review
candidates, scripts, transcripts, QA, manifests, and visual review records remain.
