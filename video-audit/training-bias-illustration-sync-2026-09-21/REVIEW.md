# Training Bias v7: SHIPPED 2026-09-21 (illustration sync over a camera walk, narrow visual repair)

**Scope.** David, 2026-09-21: "Training Bias shows the illustration from :21 to :33." The Wrong Pattern. Wrong Answer. board is
the lesson's opening illustration (`index.html` line 6054, `?v=20260921batch3`); the cast refresh replaced it in place — same
board, same 1600x1308 dimensions, same title, photograph and takeaway banner, new cast in the photograph. Only that span
changes. Narration, timing, FPS, frame count and the audio stream are untouched. Fourteenth of the day's illustration syncs.

**Span.** Output frames 657–1012 (0:21.90–0:33.73), 355 frames — the whole board leg. Verified by decoding: the OLD JPG rendered
through the shipped leg spec reproduces the live video frame for frame across all 355 frames at 2.37 mean per-pixel difference
(max 2.71, nothing over 6). That JPG's sha256 matches the one build-v6 recorded, and build-v6's `render_sha256` matches the live
file, so baseline, spec and asset provably belong together; the build asserts the latter.

**The walk is the shipped one, verbatim.** 118-frame establish with a small push (2512 → 2436.64), 30-frame dive to the brass
machine [1331.56, 703, 1368.89], 85-frame hold, 30-frame move to the beach card [1507.56, 873, 1016.89], 92-frame hold. The walk
ends on that dive with no pull-back, as shipped. No rings, so no stroke question. The composition did not move in the refreshed
art — both dive windows, drawn on each canvas, frame the same machine and the same beach photograph.

**Build.** `scripts/video/build_training_bias_wrong_pattern_sync.py`. Baseline: the shipped v6 itself, frozen here as
`baseline-live-2026-09-21-v6.mp4` (sha256 705abdb1ad86…, 7830 frames, gitignored). Canvas from
`editspec_build.Build.compose` at its default tall margin: 2512x1414 at offset (456, 53), matching build-v6. One
`ken_burns_path.py` leg, one concat pass, audio packet-copied.

- Asset: `course-assets/training-bias/training-bias-wrong-pattern.jpg` (5d90908c4011…, 1600x1308). Previous: bee2a7956ec3029d…,
  the sha v6 recorded.
- Candidate: `Prompts/training-bias-v7.mp4` (0423a1b5f343…), shipped to `course-assets/training-bias/training-bias.mp4` and
  removed.
- Cache key `20260921ship3` → `20260921ship22` on the `trainingbias` entry. Pill unchanged and correct (4 min; 4:21.00).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 7830 frames at 30 fps, matching the baseline exactly. Leg decoded its 355 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` on six declared boundaries: both splices pass and their strips were inspected (the Notebook
   cow-on-the-beach drawing into the board at 657, the board into the two-traps drawing at 1012), one clean cut each way. The
   four beat boundaries flag one-frame islands; running the same guard on the **baseline** flags the same four at the same
   frames, so it is the detector reacting to the shipped camera motion.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.57 (the new cast); outside it mean 0.28, max 0.91 —
   re-encode noise. Nothing outside 657–1012 changed visually.
5. Per-frame motion profile inside the span correlates 0.9998 with the baseline's, maximum difference 0.97.
6. Walk states inspected (`state-000657-board-open.jpg`, `state-000805-machine-arrive.jpg`,
   `state-000920-beach-card-arrive.jpg`, `state-001011-board-last.jpg`): the first dive holds the brass machine with the
   holographic cow and the red X, the second holds the beach photograph in the student's hand, and the board opens whole with
   title and banner readable.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other four boards (How Skewed Data Distorts the
   Picture, Three Questions, Stale Information, How RAG Works), which this repair does not touch and the refresh did not change.
