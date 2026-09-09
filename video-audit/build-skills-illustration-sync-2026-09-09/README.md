# Build Your Skills illustration video sync — September 9, 2026

Status: all three reviewed videos approved and shipped under their existing live filenames. Previous live videos and approved review copies are preserved in the build audit folders. Lesson images and index.html were not modified by shipping.

## Scope

Five installed, approved images across three videos: Honesty & Privacy (allowed-help flow), People Skills (four-way practice board), and Make Your Move (Nate and Luke note plus both career boards). The corrected September 9 career images are used.

Honesty & Privacy currently has `comingSoon: true` in index.html. Its video file is updated, but shipping does not re-enable the lesson video.

## Preserved behavior

Audio is packet-identical in every full candidate. Total frames, narration timing, closing, existing pauses, and native graphic cutaways are preserved. Rings use full component horizontal boundaries and the component accent. The gold takeaway uses standard video purple. People Skills keeps the approved pan onsets with slightly tighter whole-card framing to avoid a clipped board heading or adjacent-row strip.

## Shipped files

### honesty-and-privacy

- Live video: `/Users/davidobrien/Developer/AI-Training/videos/honesty-and-privacy.mp4`
- Archived short review: `/Users/davidobrien/Developer/AI-Training/video-audit/build-skills-illustration-sync-2026-09-09/build/honesty-and-privacy/approved-review-reel.mp4` (20.20 seconds)
- Frames: 6222/6222; audio identical; native playback passed.
- Reviewed all 7 edit/highlight boundaries with 25-frame strips; no old-graphic flashes found.
- Outside-span fidelity: 215 samples; worst mean channel difference 0.732/255 (single re-encode).

  Review 0.000s → full-video 63.400–83.600s.

### people-skills

- Live video: `/Users/davidobrien/Developer/AI-Training/videos/people-skills.mp4`
- Archived short review: `/Users/davidobrien/Developer/AI-Training/video-audit/build-skills-illustration-sync-2026-09-09/build/people-skills/approved-review-reel.mp4` (67.20 seconds)
- Frames: 4868/4868; audio identical; native playback passed.
- Reviewed all 7 edit/highlight boundaries with 25-frame strips; no old-graphic flashes found.
- Outside-span fidelity: 124 samples; worst mean channel difference 0.899/255 (single re-encode).

  Review 0.000s → full-video 63.467–130.667s.

### make-your-move

- Live video: `/Users/davidobrien/Developer/AI-Training/videos/make-your-move.mp4`
- Archived short review: `/Users/davidobrien/Developer/AI-Training/video-audit/build-skills-illustration-sync-2026-09-09/build/make-your-move/approved-review-reel.mp4` (101.63 seconds)
- Frames: 8619/8619; audio identical; native playback passed.
- Reviewed all 24 edit/highlight boundaries with 25-frame strips; no old-graphic flashes found.
- Outside-span fidelity: 355 samples; worst mean channel difference 1.981/255 (single re-encode).

  Review 0.000s → full-video 27.233–39.300s.
  Review 12.067s → full-video 73.167–105.033s.
  Review 43.933s → full-video 105.200–121.200s.
  Review 59.933s → full-video 124.300–140.233s.
  Review 75.867s → full-video 144.800–170.567s.

## Audit and reproduction

`replacement-plan.json` records frozen baseline/asset hashes, exact half-open frame spans, camera coordinates, and highlight states. Each build folder contains manifest, fidelity report, native playback logs, final QA frames, transition strips, and manual review resolution. Raw detector flags are retained: five People Skills moves and three Make Your Move moves were visually confirmed as continuous camera motion, not leaked frames.

Scripts: `scripts/video/scan_build_skills_illustrations.py`, `scripts/video/build_skills_character_sync.py`, and `scripts/video/qa_build_skills_character_sync.py`. Builders refuse existing candidate files/build directories. Shipping receipts record exact hashes and playback checks. No commits were performed.
