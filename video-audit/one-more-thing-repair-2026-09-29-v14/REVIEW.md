# One More Thing v14 — two requested narration cuts

Narrow repair requested September 29. Candidate: `Prompts/one-more-thing-v14.mp4`, 3:24.23 (6,127 frames at 30 fps). Not published.

## Changes from v13

1. Remove the isolated “Up” before “Spot's chance jumps from 22% up to 36%.” Keep the intended “up to 36%.” Cut v13 frames [3190, 3205), 1:46.333–1:46.833. New join is 1:46.333. The targeted small.en transcription identified the stray word at 1:46.54–1:46.60; waveform activity lies inside the chosen quiet endpoints. Spot's onset is preserved.
2. Remove “When you use AI, these weights stay fixed.” Cut v13 frames [4284, 4379), 2:22.800–2:25.967. New join is 2:22.300 after the earlier half-second cut. The preceding sentence still calls weights “the static numbers that shape every prediction”; it now leads directly into “For each new token, AI uses these weights in a massive set of calculations.”

Total removed: 110 frames / 3.667 seconds. Existing natural gaps are shortened to roughly 0.6 seconds at both joins. No new pauses. Five-millisecond ramps only at the two cut boundaries.

Reconstructed the original v13 picture timeline from pristine raw rolls, its canonical board canvases, and its hash-bound old-live donor snapshot. Removed the same picture spans as audio; all later highlights, board transitions and standard closing motion follow the same frame mapping. Used v13's assembled PCM master before its AAC encode; no extra picture/audio generation was stacked onto the encoded v13 MP4.

## Verification

Exact source identities, cut frames, kept spans, output boundaries and protected hashes: `edit-manifest.json`. Targeted original word timings and 10 ms RMS readings: `up-words.json`, `weights-words.json`, and matching RMS files. Listening context clips are retained before and after each cut.

Encoded verification completed: all 6,127 frames decoded at 30 fps; all declared boundaries passed transition_guard with zero flags. Inspected the two cut frame sequences and the literal final closing frame. Fresh small.en ASR confirms “Spot's chance jumps from 22% up to 36%” without the stray word, and the direct transition from “every prediction” to “For each new token.” Encoded audio has no clipped samples; peak −0.45 dBFS. Both new joins have a one-sample difference below −90 dBFS. All protected hashes remain unchanged.

Encoded checks are recorded in `qa.json`, `transitions/`, and `edited-passages-transcript.txt`. This is a narrow repair; no new full-lesson teaching review or continuous audiovisual playback was performed. **Direct listening is still required at the two new joins (1:46.33 and 2:22.30).** ASR and waveform checks do not certify cadence or pronunciation. Existing v13 listening limitations remain.

Build: `.video-venv/bin/python scripts/video/build_one_more_thing_v14.py`.

QA: `.video-venv/bin/python video-audit/one-more-thing-repair-2026-09-29-v14/verify.py`.

Live MP4, v13 candidate, raw rolls, lesson Markdown and board JPGs are protected and remain unchanged. No site update or publication.

## Shipping authorization — 2026-09-29

David explicitly instructed “ship it” after v14 was delivered with its listening limitation disclosed. Installed the exact approved bytes at the canonical course path and updated the lesson cache key to `20260929ship1`, with a “3 min” display. This is owner-approved publication; it does not retroactively claim agent listening. See `shipping-receipt.json` and `publication-status.json` for release/deployment results.

Production verified at 2026-09-29T13:04:29.347079+00:00: commit `5ff1d1f4`, Vercel success, public page references `20260929ship1`, and the public MP4 matches the approved v14 SHA-256 and byte count. The production commit contains only `index.html` and the canonical MP4; audit material remains local on `codex/one-more-thing-v14-local-audit` and in this workspace. Reclaimed 0.04 GB of v14 WAV scratch; retained the v13 assembly dependency and all raw rolls.
