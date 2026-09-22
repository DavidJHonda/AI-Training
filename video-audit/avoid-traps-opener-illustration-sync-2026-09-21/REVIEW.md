# Avoid Traps opener v7: SHIPPED 2026-09-21 (illustration sync over a camera walk, narrow visual repair)

**Scope.** David, 2026-09-21: "Opener-Avoid. 1:14 to 1:32 needs the illustration replacement." The Read the Water board is the
lesson's illustration (`index.html`, `?v=20260921batch3`); the cast refresh replaced it in place — same board, same 1387x1134
dimensions, same title, photograph and takeaway banner, new cast in the photograph. Only that span changes. Narration, timing,
FPS, frame count and the audio stream are untouched. Twelfth of the day's illustration syncs, and the first onto a video that
shipped earlier the same day (v6, 11:11).

**Span.** Output frames 2212–2777 (1:13.73–1:32.57), 565 frames. Verified by decoding: the OLD JPG rendered through the shipped
leg spec reproduces the live video frame for frame across all 565 frames at 2.83 mean per-pixel difference (max 3.27, nothing
over 6). The old asset's sha256 matches the one recorded in build-v6's manifest, and that manifest's `render_sha256` matches the
live file, so baseline, spec and asset all belong together — the build asserts both.

**The walk is the shipped one, verbatim.** 175-frame establish with a small push (2178 → 2112.66), 30-frame dive to the channel
[1110, 516.25, 1085.33], 58-frame hold, 30-frame move out to the lifeguard framing [944.22, 600, 1603.56], 152-frame hold,
36-frame pull back to the full illustration, 84-frame hold. No rings, so no stroke question. The composition did not move in the
refreshed art — both dive windows, drawn on each canvas, frame the same rip channel and the same two-figure shot, the second
including the same sliver of stage margin at the left that it always did.

**Build.** `scripts/video/build_opener_avoid_water_sync.py`. Baseline: the shipped v6 itself, frozen here as
`baseline-live-2026-09-21-v6.mp4` (sha256 dada263ebcae…, 6543 frames, gitignored). Canvas from
`editspec_build.Build.compose` at its default tall margin: 2178x1226 at offset (395, 46), matching build-v6. One
`ken_burns_path.py` leg, one concat pass, audio packet-copied.

- Asset: `course-assets/avoid-traps-opener/avoid-traps-opener-read-the-water.jpg` (0c19d08cbfa8…, 1387x1134). Previous:
  54b69984fd2044b6…, the sha v6 recorded.
- Candidate: `Prompts/avoid-traps-opener-v7.mp4` (95624e7e42fd…), shipped to
  `course-assets/avoid-traps-opener/avoid-traps-opener.mp4` and removed.
- Cache key `20260921ship1` → `20260921ship20` on the `openerprotect` entry. Pill unchanged and correct (4 min; 3:38.10).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 6543 frames at 30 fps, matching the baseline exactly. Leg decoded its 565 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` on eight declared boundaries: both splices pass and their strips were inspected (the Notebook
   syntax-error drawings into the board at 2212, the board into the surprise-box drawing at 2777), one clean cut each way. Four
   beat boundaries flag one-frame islands; running the same guard on the **baseline** flags the same four at the same frames, so
   it is the detector reacting to the shipped camera motion.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.37 (the new cast); outside it mean 0.35, max 1.38 —
   re-encode noise. Nothing outside 2212–2777 changed visually.
5. Per-frame motion profile inside the span correlates 0.9995 with the baseline's, maximum difference 2.05: the camera dives,
   widens and pulls back on the same frames at the same speed.
6. Walk states inspected (`state-002212-board-open.jpg`, `state-002417-channel-arrive.jpg`, `state-002505-lifeguard-arrive.jpg`,
   `state-002693-pullback-arrive.jpg`, `state-002776-board-last.jpg`): the channel dive holds the rip between the two figures,
   the lifeguard framing matches the shipped one including its left margin, the pull-back settles on the whole board with title
   and banner readable.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the opener's other boards (The Traps Ahead and the section map),
   which this repair does not touch and the cast refresh did not change.
