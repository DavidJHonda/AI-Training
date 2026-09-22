# Hallucination v12: SHIPPED 2026-09-21 (illustration sync over two camera walks, narrow visual repair)

**Scope.** David, 2026-09-21: "2:28 to 2:55 for the Hallucination illustration." The Real Text. Wrong Meaning. board
(`index.html` line 8478, `?v=20260921batch4`) was replaced in place by the cast refresh — same board, same 1387x1134 dimensions,
same title, photograph and takeaway banner, new cast in the photograph. Narration, timing, FPS, frame count and the audio stream
are untouched. Thirteenth of the day's illustration syncs.

**Both appearances were replaced, not just the named one.** This video shows the same asset twice, with two different walks:

| Walk | Output frames | Time | What it covers |
|---|---|---|---|
| pizza1 | 4447–5278 | 2:28.23–2:55.93 | the Reddit joke (the span David named) |
| pizza2 | 7295–8085 | 4:03.17–4:29.50 | the pizza application |

Replacing only the first would leave the same board showing a different cast about seventy seconds later in the same video, so
both walks take the new artwork. The second is separable: drop `'pizza2'` from `PIECES` in the build script and rebuild.

**Both walks are the shipped ones, verbatim.** Each is establish with a small push (2178 → 2112.66), 30-frame dive to the joke
card [739, 661, 616], hold, 30-frame move to the brass machine [1155, 626, 704], hold, 36-frame pull back, hold — pizza1 holding
150/150/307 frames, pizza2 holding 189/81/111 after a longer 313-frame establish. No rings on this board, so no stroke question.
The composition did not move in the refreshed art: both dive windows, drawn on each canvas, frame the same joke card and the same
machine.

Verified before building: the OLD JPG rendered through both shipped specs reproduces the live video frame for frame across all
1621 replaced frames at 2.56 mean per-pixel difference (max 2.99), which fixes both spans and every beat. The old asset's sha256
matches the one build-v11 recorded, and build-v11's `render_sha256` matches the live file; the build asserts the latter.

**Build.** `scripts/video/build_hallucination_pizza_sync.py`. Baseline: the shipped v11 itself, frozen here as
`baseline-live-2026-09-21-v11.mp4` (sha256 7522c552696b…, 8412 frames, gitignored). One canvas from
`editspec_build.Build.compose` at its default tall margin (2178x1226 at offset 395, 46) feeds both legs. Two
`ken_burns_path.py` legs, one concat pass over five pieces, audio packet-copied.

- Asset: `course-assets/hallucination/hallucination-glue-on-pizza.jpg` (918b5362d297…, 1387x1134). Previous: 69c28cbcadaf2045…,
  the sha v11 recorded.
- Candidate: `Prompts/hallucination-v12.mp4` (1c7189c1aeda…), shipped to `course-assets/hallucination/hallucination.mp4` and
  removed.
- Cache key `20260921ship2` → `20260921ship21` on the `hallucination` entry. Pill unchanged and correct (5 min; 4:40.40).

**Note.** The refreshed JPG was still uncommitted in the working tree at build time — it belongs to the parallel cast-refresh
session. This ship staged only the video, this script, this audit directory and the one `LESSON_VIDEOS` line.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 8412 frames at 30 fps, matching the baseline exactly. Legs decoded 831 and 790 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` on sixteen declared boundaries: all four splices pass and their strips were inspected (into and out of
   each walk), one clean cut each time. Twelve beat boundaries flag one-frame islands; running the same guard on the **baseline**
   flags the same twelve at the same frames, so it is the detector reacting to the shipped camera motion.
4. Frame diff against the baseline every 10th frame: inside the two spans mean 7.24 (the new cast); outside them mean 0.30, max
   1.21 — re-encode noise. Nothing outside the two walks changed visually.
5. Per-frame motion profile inside the spans correlates 0.9998 with the baseline's, maximum difference 1.27.
6. Walk states inspected in both (`state-004605-pizza1-joke-card.jpg`, `state-004785-pizza1-machine.jpg`,
   `state-007638-pizza2-joke-card.jpg`, `state-007857-pizza2-machine.jpg`, plus each open, pull-back and last frame): the joke
   card dive holds the jester card, the machine dive holds the brass machine with the glue card beside it, the pull-backs settle
   on the whole board with title and banner readable.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other three boards (Nothing Sounds Wrong, Why
   Hallucinations Happen, Check the Claim), which this repair does not touch and the refresh did not change.
