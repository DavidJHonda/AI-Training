# Fake Trap revision 2 — 2026-09-20

## Result

- Candidate: `Prompts/fake-trap-v2.mp4`
- Duration: 4:44.367 (8,531 frames at 30 fps)
- SHA-256: `143f8fae061e66034d34c2e95c3070255850a61b756a8fa9148efa9d8c1dc08a`
- Build entry point: `scripts/video/build_fake_trap_v2.py`
- Status: rendered and technically verified; the cross-version voice joins still require perceptual listening.

## User-requested corrections

### Stronger live opening

- Replaced the prior candidate's first 0:56.567 with the exact live video from frame 0 through frame 2229 (0:00.000–1:14.300).
- The endpoint is the live scene cut after the complete sentence, “The context makes it clear that no one is meant to believe it.”
- Candidate 2 resumes at its frame 1697 (0:56.567), a scene cut inside the quiet gap before, “The danger doesn't come from the software itself.”
- New output join: 1:14.300.
- The transition strip passes. The last live frame is the hockey-team image; the first candidate-2 frame is the existing notebook drawing for the deception boundary. No stale visual island is present.
- Sample-level audio measurement at the join: pre-window −59.77 dBFS, post-window −53.17 dBFS, single-sample jump 0.00397 full scale. The live opening received +0.8 dB gain; human listening is still required for voice/delivery continuity.

### CyberTipline shown with its spoken mention

- The source narration is unchanged: “This is the NCMEC CyberTipline.”
- Output narration onset: approximately 4:06.88; replacement scene begins at 4:07.567 on the source scene cut.
- Visual donor changed from live frames 6087–6306 to live frames 6180–6300 (3:26.000–3:30.000).
- The first donor frame already shows the complete `NCMEC / Take It Down — REPORT — CyberTipline` layout. The last complete frame holds for the remainder of the eight-second source span.
- The transition strip passes, and whole-timeline contact sheets confirm both resource labels remain visible at 4:08 and 4:12.
- Candidate 2's large displayed URL remains excluded.

## Preserved v1 repairs

- Complete Money, Power, Fame, and Cruelty teaching passage from candidate 1.
- Unsupported “software cannot reliably grade other software” sentence removed.
- Source, Context, and Corroboration board treatment retained.
- “Your eyes still work…” conclusion remains before the hard close.
- Standard close remains final with a four-second settled hold.
- No automatic one-second pauses were added.

## Verification

- Full decode: pass, 8,531/8,531 frames.
- Output metadata: pass, 30 fps and 284.367 seconds.
- Render hash matches the manifest.
- All nine protected media, board, and Fake Trap lesson inputs remained unchanged through render.
- `index.html` was intentionally excluded from the final render-integrity set because an unrelated “Where’s the Line” edit was changing it concurrently. Inspection confirmed that concurrent diff did not touch Fake Trap or `LESSON_VIDEOS`.
- Rendered transcript: 791 timestamped words. The live opening ends cleanly, candidate 2 resumes with the complete deception-boundary sentence, and the CyberTipline wording is intact.
- Six whole-timeline contact sheets reviewed.
- Thirteen every-frame transition strips reviewed. Twelve pass the automatic gate. The sole automatic failure is the same known false positive at the audio-only candidate-1 motive entry: continuous reasons-board camera motion is misclassified as one-frame visual islands. Manual review confirms no stale visual.
- Opening seam and CyberTipline transition both pass the automatic and manual transition checks.

## Listening limitation

This environment supports timestamped transcription, silence detection, sample-level seam measurement, and frame-by-frame visual inspection, but not perceptual audio playback. A human should listen at 1:14.300, 1:32.433, and 2:03.767 for voice/delivery changes before deployment.

Two encodes rejected only because unrelated `index.html` edits occurred during their render are retained in this audit directory. They are not deliverables. No live video, raw candidate, lesson file, board asset, tracker, or deployment was changed.
