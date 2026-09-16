# Beyond the Average v7 — remove the 1:17 pause

**Candidate:** `Prompts/beyond-the-average-v7.mp4`  
**Source:** `Prompts/beyond-the-average-v6.mp4` (`a86b7068fe6f28d302628d1161e71beded50b235096b1dc5c6de479ddf6860a4`)  
**Output:** 2:46.13, 4,984 decoded frames, 30 fps, 1280×720, AAC mono 48 kHz  
**Output SHA-256:** `1472549cc38c37c6c73e005daf5cc9d0b7919a7e68fcbd98829c6dacc58393e0`  
**Scope:** narrow pause deletion only. **SHIPPED 2026-09-16** on David's approval ("Ship beyond-the-average-v7"): copied to `course-assets/beyond-the-average/beyond-the-average.mp4` (sha256 1472549cc38c37c6…), cache key 20260916ship1, pill 3 min (2:46); candidates v5–v7 removed from Prompts/.

## Change

Removed v6 frames 2322–2351 and the corresponding one second of audio at
1:17.400–1:18.400. This was the inserted pause between:

> “School provides the structured time and space required to develop those assets.”

and:

> “You write essays, solve difficult math equations…”

The silence shoulders were joined with a 5 ms crossfade. After the repair,
`silencedetect` at −35 dB measures 1:17.2545–1:17.4651: **0.2106 seconds**.
No narration was removed, and every later visual remains aligned to its original
spoken beat.

## Verification

- Full sequential decode: 4,984 frames, exactly 30 fewer than v6 and matching
  the plan; 30 fps, 1280×720.
- Fresh complete transcript contains both surrounding sentences with no missing
  or leaked word.
- `transition_guard.py`: PASS at all eight declared boundaries.
- Manual inspection of the new frame strip confirms one clean cut from the fully
  drawn Where Real Value Is Built diagram to the pen-and-essay scene; no stale or
  intermediate frames.
- v6, the live course video, lesson materials, and website remain unchanged.
- Not deployed.

## Listening limitation

This environment did not expose audible playback. The edit is structurally and
transcript-verified, but David should listen across approximately 1:16.8–1:18.0
to confirm the new 0.21-second transition feels natural and the 5 ms crossfade is
inaudible before shipping.

## Build and QA

- Build: `PYTHONDONTWRITEBYTECODE=1 .video-venv/bin/python scripts/video/build_beyond_the_average_v7.py`
- Manifest: `edit-manifest.json`
- Transition report: `guard/transition-guard.md`
- Fresh transcript bundle: `/tmp/beyond-average-v7-review/beyond-the-average-v7/`

