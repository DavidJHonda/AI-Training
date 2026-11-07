# How AI Learns v11 — phase-focused video edit

Review candidate: `Prompts/how-ai-learns-v11.mp4`. User authorized this build after approving the matching page simplification. No local installation or publishing in this task.

## Scope

Keep the opening basketball analogy. Remove the overview basketball question and the three phase-specific sample-answer passages, including their introductions. Replace the four changed course boards with the exact current page JPGs. Remove the basketball prompt and answer text from the existing feedback illustration. Preserve the useful shared-loop illustration before the detailed phases, all other narration and drawings, and the existing close.

## Narration cuts

| Source v10 interval | Removed | Output join |
|---|---|---|
| 48.500–53.500s | Overview basketball question | 48.500s |
| 120.300–130.267s | Pretraining sample-answer introduction and answer | 115.300s |
| 157.767–167.900s | Instruction-tuning sample-answer introduction and answer | 142.800s |
| 197.000–214.167s | Preference-tuning polished-answer introduction and answer | 171.900s |

The four cuts remove 42.267 seconds. Output: 6,114 frames at 30 fps, 3:23.800. Each boundary falls in measured quiet audio (source 10 ms windows below −61 dBFS). No new pauses; five-millisecond fades at retained-span edges.

## Board plan

| Board | Highlight sequence | Camera | Duration / supporting scene |
|---|---|---|---|
| Three Phases of Training | Pretraining → Instruction Tuning → Preference Tuning | Complete board throughout | 14.20 s; arrives on the overview introduction |
| 1 · Pretraining | What Pretraining Builds | Complete board throughout | 14.80 s, followed by retained frustrated-student illustration during the limitation |
| 2 · Instruction Tuning | Learn to Follow Instructions → What Still Needs Work | Complete board throughout | 19.93 s, followed by updated feedback-comparison illustration |
| 3 · Preference Tuning | Learn from Feedback → What Still Needs Work | Complete board throughout | 23.20 s, then retained training-finished illustration |

All changed boards use the canonical asset directly and fixed 4 px outlines after scaling. No zoom is needed at delivered size. Preference’s first explanation begins 1.9 seconds after the board arrives; the outline follows that spoken onset while the full board stays visible (Edit Spec section 3 exception). No pause is added.

## Provenance and limits

Stable source is `Prompts/how-ai-learns-v10.mp4`, SHA-256 `8e4cf9a1d123b2534045adbe5c3515e24e9133e427f262b9372803897ac8d796`. Retained pictures use this finished source, adding one video encode; current boards and the feedback UI come from original assets. The raw historical build depends on superseded live donors, so it was not rerun. The current installed video and lesson assets are protected by hashes.

Continuous audiovisual listening remains pending; do not treat a transcript or automated checks as a full listen-through.

## Encoded-file verification

- Fully decoded: 6,114 frames, 1280×720, 30 fps, continuous timestamps, 203.800 seconds.
- 165 sampled frames, including exact edit boundaries, match the intended source or lossless replacement legs; maximum reduced-image MAE 2.771/255.
- All 18 transition guards pass. Inspected all 18 frame strips and the encoded changed-board/feedback contact sheet; no stale sample-answer graphic flashes at cuts.
- Encoded audio correlates 0.999986 with the assembled edit. The four join windows measure −66.7, −79.9, −82.1, and −76.5 dBFS. Source speech is retained across each excision.
- Fresh `small.en` transcription of the actual candidate contains one basketball mention, in the opening at 9.12 seconds. No hoop, fingertips, follow-through, sample answers, or “highly polished” narration remains after the opening.
- All three phase roles, their limitations, the shared training loop, ordinary-chat weights explanation, and complete closing are retained in the fresh transcript.
- All protected source/lesson/asset hashes are unchanged. Candidate is not installed or published.
- Full audiovisual listen-through has not been performed. This is a review build, not a completed shipping certification.

Evidence: `qa.json`, `narration-check.json`, `transcripts/how-ai-learns-v11.txt`, `transitions/transition-guard.md`, and the encoded contact sheets in this directory.

Changed-board ring samples measure 4–5 thresholded pixels (blue 4, purple 4–4.5, green 5), consistent with the fixed 4 px renderer plus the colored card border/antialiased edge. Full-view framing and complete-card bounds were visually checked on the encoded frames. The detector also finds decorative purple shapes in the unchanged setup illustrations; those are not new highlight rings.

## Local release — November 7, 2026

User approved with “ship it” after review delivery and disclosure of the pending full listen-through. Installed the exact approved v11 candidate; no new listening claim. Commit `b16aa6844e96a79047e6a431d395987c7e744ce8`. Cache key `20261107ship11`, displayed runtime `3 min`, exact runtime 3:23.800. Installed SHA-256 `4356ef2e10104ccd955636b4238b37fc262242d8feb1791b175e2745f0bd91fb`. Asset-integrity verification and 13 lesson tests passed. The design checker’s two font and nine em-dash flags predate this release. Only How AI Learns changes were staged; unrelated work remains in the workspace. Shipped locally; queued for batch deployment. No push or deployment performed.
