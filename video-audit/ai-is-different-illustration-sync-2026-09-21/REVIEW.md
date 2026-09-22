# AI Is Different v9: SHIPPED 2026-09-21 (two illustration syncs with rings and dives, narrow visual repair)

**Scope.** David, 2026-09-21: "AI is Different has 2 illustrations we need to replace. Starting at 2:11 to 2:56. The second
appears right after from 2:57 to 3:03 AND 3:10 to 3:22. There are highlights in these." Both boards were replaced in place by the
cast refresh — Rules vs. Patterns (`index.html` line 5459, `?v=20260921cast2`, 1600x1401) and Structured vs. Unstructured Data
(line 5481, same cache tag, 1600x1328) — same titles, columns, rows, banners and URL lines, new cast in the photographs. Only
those spans change. Narration, timing, FPS, frame count and the audio stream are untouched. Seventh of the day's illustration
syncs and the first covering two boards in one pass.

**Spans.** Output frames equal source frames through this stretch:

| Piece | Output frames | Time | Leg frames |
|---|---|---|---|
| Rules vs. Patterns | 3930–5317 | 2:11.00–2:57.23 | rvp 0–1387 |
| Structured vs. Unstructured Data | 5317–5509 | 2:57.23–3:03.63 | structured 0–192 |
| *(Notebook spreadsheet drawing, untouched)* | 5509–5712 | 3:03.63–3:10.40 | structured 192–395 unused |
| Structured vs. Unstructured Data | 5712–6098 | 3:10.40–3:23.27 | structured 395–781 |

**Both walks and every ring are the shipped ones, verbatim.** Rules vs. Patterns: establish at full view, dive to THE QUESTION,
then down the Normal Software column card by card, across to AI Software and down its three rows, pull back for the banner — ten
rings, twenty-one beats. Structured vs. Unstructured Data: establish, dive to Normal Software, hold, cross to AI Software, hold —
two column rings. The columns did not move in the refreshed art, checked by drawing all twelve rectangles on both boards' canvases,
so every ring lands on the same component and every dive frames the same card.

**Stroke follows the current rule.** Per David's 09-21 instruction that a synced video takes the current highlighting, the rings
use the artwork-scaled rule: 3 px at each board's full view and 4 px at the dives, where the shipped video carried a constant 5 px
everywhere. Measured on the candidate at the full-view ring: 3 px core against the baseline's 5 px. Rectangles, colors, radii and
onsets are unchanged. (If the old weight is wanted back, it is a re-render of the two legs, nothing else.)

**Build.** `scripts/video/build_ai_is_different_boards_sync.py`. The rolls this video was assembled from no longer exist, so the
baseline is the shipped v8 itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 68d188908 05ce…, 9674 frames, gitignored).
Canvases come from the same code that built the shipped legs, `editspec_build.Build.compose` at its default tall margin: 2690x1514
at offset (545, 56) and 2550x1436 at offset (475, 54), both matching the offsets recorded in the 09-16 manifest. Two
`ken_burns_path.py` legs, one concat pass over six pieces, audio packet-copied.

- Assets: `ai-is-different-rules-vs-patterns.jpg` (84416643f487…) and `ai-is-different-structured.jpg` (35dda88ee9a3…).
  Previous: 8a2824aeba4b… and 40c6916b1a7b…, same dimensions.
- Candidate: `Prompts/ai-is-different-v9.mp4` (c7a9dbb804a3…), shipped to `course-assets/ai-is-different/ai-is-different.mp4`
  and removed.
- Cache key `20260916ship1` → `20260921ship15` on the `aivscode` entry. Pill untouched (6 min; the file is 5:22 — already on the
  list of pill mismatches reported separately, not changed here).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 9674 frames at 30 fps, matching the baseline exactly. Legs decoded 1387 and 781 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. Spans and mapping proven before building: both OLD JPGs rendered through the shipped specs with the stroke forced to 5
   reproduce the live video across all 1965 replaced frames at 2.55 mean per-pixel difference (max 3.06, nothing over 6). That
   fixes both spans, the skipped leg stretch under the spreadsheet drawing, every dive and every ring onset in one test.
4. `transition_guard.py` on 17 declared boundaries: 13 pass. The four flagged are camera pans, not splices —
   `rvp-ring-588-331`, `rvp-ring-1364-331`, `rvp-ring-585-1329`, `structured-ring-1294-182` — and running the same guard on the
   **baseline** flags the same four boundaries at the same frames with the same counts, so the detector is reacting to the
   shipped motion, not to anything this build introduced. Strips inspected: the camera pans between columns while the ring hands
   over, no stale frames. All four splice boundaries (3930, 5317, 5509, 5712, 6098) pass and were inspected.
5. Frame diff against the baseline every 10th frame: inside the spans mean 11.04 (the new cast, plus the finer stroke); outside
   them mean 0.38, max 1.69 — re-encode noise. Nothing outside the three pieces changed visually.
6. Per-frame motion profile inside the spans correlates 0.9998 with the baseline's, maximum difference 1.21: the camera dives,
   holds and pans on the same frames at the same speed.
7. Ring and dive states inspected (`state-003970-rvp-ring-question.jpg` … `state-006097-structured-last.jpg`): correct component
   ringed in each, card text readable at every dive, nothing clipped at frame edges.
8. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
9. Not performed: a full end-to-end rewatch, and no check of the lesson's other three boards (Rules Look Like This, Two Ideas,
   Kryptonite, Weak Spots), which this repair does not touch and the cast refresh did not change.
