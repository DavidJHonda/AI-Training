# People Skills v2: SHIPPED 2026-09-21 (illustration sync with dives and rings, narrow visual repair)

**Scope.** David, 2026-09-21: "People Skills. The illustration starts at 1:42." The Four Ways to Practice board is the lesson's
second illustration (`index.html` line 9576, `?v=20260921batch6`); the cast refresh replaced it in place — same board, same
1351x1164 dimensions, same title and four cards, new cast in the photographs. Only that span changes. Narration, timing, FPS,
frame count and the audio stream are untouched. Nineteenth of the day's illustration syncs.

**Span.** Output frames 3033–4536 (1:41.10–2:31.20), 1503 frames. Verified by decoding: the pre-refresh JPG rendered through
the shipped leg spec (stroke forced to the old constant 5) reproduces the live video at 2.62 mean per-pixel difference, sampled
every 25 frames and at every beat and ring onset, nothing over 6.

**Two details this build had to get right.**

1. *Framing.* This video predates the 4% tall-board stage margin added on 2026-09-14, so the build composes with
   `tall_margin=False` to reproduce the 09-12 canvas: 2070x1166 at offset (359, 1), matching that manifest. The default would
   have produced 2236x1258 at (442, 47) and shifted every camera window.
2. *Stroke.* The artwork-scaled rule gives **4 px at full view and 8 px at the dives**, where the 09-12 build used a constant
   5 px. The dives here are tight — about 1014 board px across the 1280 frame — so the rule thickens the ring to hold its weight
   against the card's own text. This is the largest stroke change of the day's syncs; inspected at each dive, the heavier ring
   reads cleanly against the card and clips nothing.

**Dives and rings otherwise unchanged.** Establish, dive to Listen to Understand, across to Notice What Isn't Being Said, down
to Show People They Matter, across to Challenge Ideas Not People, pull back, hold — same beats, same four rectangles, colors and
onsets. The cards did not move in the refreshed art, checked by drawing all four on the new canvas.

**Build.** `scripts/video/build_people_skills_four_ways_sync.py`. Baseline: the shipped file itself, frozen here as
`baseline-live-2026-09-12.mp4` (sha256 138d2453553a…, 5199 frames, gitignored); the 09-12 manifest's `render_sha256` matches it,
which the build asserts. One `ken_burns_path.py` leg, one concat pass, audio packet-copied.

- Asset: `course-assets/people-skills/people-skills-four-ways.jpg` (fed74e640901…, 1351x1164). Previous: 90c1d10cb74e35dd….
  The refresh is committed (cc7e16e4).
- Candidate: `Prompts/people-skills-v2.mp4` (a6f76e48702f…), shipped to `course-assets/people-skills/people-skills.mp4` and
  removed.
- Cache key `20260912ship1` → `20260921ship27` on the `peopleskills` entry. Pill unchanged and correct (3 min; 2:53.30).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 5199 frames at 30 fps, matching the baseline exactly. Leg decoded its 1503 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` on twelve declared boundaries: both splices pass and their strips were inspected (the Notebook
   everyday-interactions drawing into the board at 3033, the board into the still-scene frame at 4536). Ten beat and ring
   boundaries flag one-frame islands; running the same guard on the **baseline** flags the same ten at the same frames, so it is
   the detector reacting to the shipped camera motion.
4. Frame diff against the baseline every 10th frame: inside the span mean 11.89 — the highest of the day's syncs, as expected
   from four large photographs changing plus the heavier dive stroke; outside it mean 0.39, max 1.11 — re-encode noise. Nothing
   outside 3033–4536 changed visually.
5. Per-frame motion profile inside the span correlates 0.9998 with the baseline's, maximum difference 2.95.
6. Dive states inspected against the baseline's own frames (`state-003157-ring1-listen-dive.jpg` through
   `state-004182-ring4-challenge-dive.jpg`, plus the open, pull-back and last frame): correct card ringed and fully in frame at
   each dive, card text readable, nothing clipped.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other board (Why People Matter), which this repair
   does not touch and the refresh did not change.

**Housekeeping.** The lossless leg was deleted as soon as the candidate verified.
