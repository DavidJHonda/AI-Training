# Make Your Move v5: SHIPPED 2026-09-21 (two career-board legs REBUILT to the current spec)

**Scope.** David, 2026-09-21: "Make Your move. The first illustration appears at 1:18. The second appears at 2:18," then, after
the findings below, "Rebuild the two legs to today's spec." Both career boards were replaced in place by the cast refresh —
How AI Might Change Careers (1 of 2) and (2 of 2), 1601x982 and 1602x982, same titles and three cards each, new cast in the
photographs. Twentieth of the day's illustration syncs, and **the only one that is a rebuild rather than a reproduction.**

**Why a rebuild.** Two findings, both established before any build:

1. *No record to reproduce.* The `make-your-move-repair-2026-09-12` audit directory was removed in the 09-15 cleanup and the
   source roll with it. The leg specs here are reconstructed from that build's own parameters in
   `scripts/video/build_make_your_move_3_review.py` — same source spans (fr 85.5–141.9 and 159.06–205.2), same spoken onsets,
   same pull-backs — and re-emitted by today's `editspec_build.board()`.
2. *The shipped motion is not what current code emits.* Fitting the live frames against the canvas showed a slow push during
   the establish (1746 → 1696, exactly the compact push formula, reached by frame ~80) and only then a dive to each card.
   Reproducing that hybrid got most of the way — most samples within 3 of the live — but the dive transits stayed a few frames
   out, which is fitting rather than reproducing. David's instruction was to rebuild instead.

**What changed on screen, beyond the cast.**

* The establish is now a static full view for 89 frames (careers-a) / 60 frames (careers-b) instead of a slow push, then the
  24-frame move to each card, the holds at the shipped onsets, a 30-frame pull-back and the full hold. Because these cards are
  wide relative to the board, `window()` clamps each dive close to centre, so on screen the move still reads as a gentle zoom
  with the ring handing over — close to what the video did before.
* **The boards gain the site credit.** The live video's career boards predate the 2026-09-14 attribution pass and carry no
  `besmarterthanthetool.com` line; the refreshed assets do (confirmed pixel-by-pixel against the pre-attribution JPGs,
  a272c7de9ee6… and 81271f201523…). Unavoidable while using the current artwork, and it brings these two boards in line with
  every other board in the course.

**Two deliberate holds against "today's default".** `tall_margin=False`, because these boards are tall and today's default
would add the 4% stage margin and shrink them inside the frame, out of step with this video's other three boards; and the card
rectangles come from the refreshed artwork's own `cards_grid` detection, which lands within a pixel of the pre-refresh one.

**Spans** (found by matching the reconstructed legs against the live file, best-offset search):

| Leg | Output frames | Time | Cards |
|---|---|---|---|
| careers-a | 2327–4019 | 1:17.57–2:13.97 | Doctor, Teacher, Lawyer |
| careers-b | 4144–5528 | 2:18.13–3:04.27 | Electrician, Graphic Designer, Entrepreneur |

**Stroke.** The artwork-scaled rule gives 5 px at both the full view and the dives here, which is what the video already
carried, so the highlights do not change weight.

**Build.** `scripts/video/build_make_your_move_careers_sync.py`. Baseline: the shipped file itself, frozen here as
`baseline-live-2026-09-12.mp4` (sha256 e3a9c6250ee8…, 9877 frames, gitignored). Two `ken_burns_path.py` legs, one concat pass
over five pieces, audio packet-copied.

- Assets: `make-your-move-doctors-teachers-lawyers.jpg` (9c85204d43f4…) and
  `make-your-move-electricians-designers-entrepreneurs.jpg` (0d41e4eb1d3e…). Both refreshes are committed (cc7e16e4).
- Candidate: `Prompts/make-your-move-v5.mp4` (703395a06d51…), shipped to `course-assets/make-your-move/make-your-move.mp4`
  and removed.
- Cache key `20260912ship1` → `20260921ship28` on the `makeyourmove` entry. Pill unchanged and correct (5 min; 5:29.23).

## Verification

1. Decoded 9877 frames at 30 fps, matching the baseline exactly. Legs decoded 1692 and 1384 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded, so every
   ring and camera move still lands on the sentence it always did.
3. `transition_guard.py` on twenty declared boundaries: all four splices pass and their strips were inspected. Four beat
   boundaries flag one-frame islands — the ring hand-offs at the Teacher, Lawyer, Graphic Designer and Entrepreneur moves,
   where the ring switches colour while the camera eases; strips inspected, the deltas rise and settle with no stale frame.
   (A baseline comparison is not meaningful here: the motion is new by instruction.)
4. Frame diff against the baseline every 10th frame: outside the two spans mean 0.42, max 1.33 — re-encode noise, so nothing
   else in the video moved. Inside them mean 10.08, as expected from new cast, new credit line and rebuilt motion.
5. States inspected (`state-002327-careers-a-open.jpg` through `state-005527-careers-b-last.jpg`): each board opens whole, the
   correct card is ringed at each hold, card text is readable throughout, the credit line sits clear of the frame edge, and the
   pull-backs settle on the full board.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file.
7. Not performed: a full end-to-end rewatch; no check of the lesson's other three boards (the note, Four Skills to Build, Moves
   to Make), which this repair does not touch. Those three still carry their pre-attribution artwork in the video — the same
   finding as the career boards, left alone here and worth a separate decision.

**Housekeeping.** The lossless legs were deleted as soon as the candidate verified.
