# Fake Trap v6: SHIPPED 2026-09-21 (two illustration syncs with rings and dives, narrow visual repair)

**Scope.** David, 2026-09-21: "Fake-Trap. The new illustration starts about :27. A 2nd illustrations starts at about 2:17." Both
boards were replaced in place by the cast refresh — The Same Clip. Two Eras. (`index.html` line 11620, `?v=20260921batch8`,
1600x1470) and Check the Source, Not the Pixels (line 11660, `?v=20260921batch4`, 1387x1134) — same titles, scenario strip,
columns, rows and takeaway banners, new cast in the photographs. Only those spans change. Narration, timing, FPS, frame count
and the audio stream are untouched. Seventeenth of the day's illustration syncs.

**Spans.**

| Board | Output frames | Time | Treatment |
|---|---|---|---|
| comparison | 804–2037 | 0:26.80–1:07.90 | dense: establish, dive to Does It Look Real?, five rings down that column, across to Where Is It From?, six rings, pull back, banner |
| follow-source | 4123–4414 | 2:17.43–2:27.13 | compact, still, one ring on the takeaway line |

Verified by decoding: both OLD JPGs rendered through the shipped leg specs (stroke forced to the old constant 5 for the
comparison) reproduce the live video at 2.80 mean per-pixel difference, sampled every 25 frames and at all thirteen ring onsets,
nothing over 6. Both old shas match those recorded in build-v5's manifest, and build-v5's `render_sha256` matches the live file;
the build asserts the latter.

**Dives and rings, the shipped ones, verbatim.** Thirteen rings across the two boards, same rectangles, colors, radii and
onsets — including the comparison board's two simultaneous rings at frames 264–413 and its return to the second row at
977–1063. Both dive windows and all thirteen rectangles land exactly as before on the refreshed art, checked by drawing them on
each canvas.

Stroke follows the artwork-scaled rule, as the day's other syncs have: this video predates that rule and carried a constant
5 px, so the comparison rings are now 3 px at full view and 4 px at the dives, and the follow-source ring is 4 px.

**Build.** `scripts/video/build_fake_trap_boards_sync.py`. Baseline: the shipped v5 itself, frozen here as
`baseline-live-2026-09-20-v5.mp4` (sha256 5d9b0f00bfa4…, 9240 frames, gitignored). Canvases from
`editspec_build.Build.compose` at its default tall margin: 2824x1590 at offset (612, 60) and 2178x1226 at offset (395, 46),
both matching build-v5. Two `ken_burns_path.py` legs, one concat pass over five pieces, audio packet-copied.

- Assets: `fake-trap-comparison.jpg` (d53c23daebf6…) and `fake-trap-follow-the-source.jpg` (8b3a5326c09a…). Previous:
  b5b4d2152ca04f14… and 107634378198d38d…, the shas v5 recorded. Both refreshes are committed (cc7e16e4).
- Candidate: `Prompts/fake-trap-v6.mp4` (8fffe6bdf9de…), shipped to `course-assets/fake-trap/fake-trap.mp4` and removed.
- Cache key `20260920ship2` → `20260921ship25` on the `faketrap` entry. Pill unchanged and correct (5 min; 5:08.00).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 9240 frames at 30 fps, matching the baseline exactly. Legs decoded 1233 and 291 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed all sixteen declared boundaries — the four splices and the thirteen ring onsets (one shared
   frame). Splice strips inspected: one clean cut each way at 804, 2037, 4123 and 4414.
4. Frame diff against the baseline every 10th frame: inside the two spans mean 4.52 (the new cast and the finer strokes);
   outside them mean 0.32, max 1.05 — re-encode noise. Nothing outside the two boards changed visually.
5. Per-frame motion profile across the comparison leg correlates 0.9998 with the baseline's, maximum difference 1.00: the dives,
   holds and pull-back land on the same frames.
6. States inspected (`state-000804-comparison-open.jpg`, `state-000928-ring1-checked.jpg`,
   `state-001459-ring6-where-is-it-from.jpg`, `state-001943-banner.jpg`, `state-004123-follow-source-open.jpg`,
   `state-004291-follow-source-ring.jpg`, and each board's last frame): correct component ringed in each, card text readable at
   the dives, banner readable at full view, nothing clipped.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other two boards (Why Some Fakes Aren't Friendly, Move
   the Test Off the Image) or the six TRY IT photo pairs, none of which this repair touches.

**Housekeeping.** The lossless legs were deleted immediately after the candidate verified: the day's sixteen earlier syncs had
filled the disk with them, which stopped this build mid-verification until David cleared space. Later builds should delete each
leg as soon as its candidate passes.
