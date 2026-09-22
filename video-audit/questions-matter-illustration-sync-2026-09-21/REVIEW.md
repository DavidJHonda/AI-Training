# Questions Matter v6: SHIPPED 2026-09-21 (illustration sync with rings, narrow visual repair)

**Scope.** David, 2026-09-21: "Questions Matter needs the new illustration from :08 to about 1:02. There is highlighting but no
zooming." The How Answers Got Easier and Faster board is the lesson's second illustration (`index.html` line 13076,
`?v=20260921batch5`); the cast refresh replaced it in place — same board, same 1600x958 dimensions, same title, three columns with
their photographs, TIME TO ANSWER rows and takeaway banner, new cast in the photographs. Only that span changes. Narration,
timing, FPS, frame count and the audio stream are untouched. Ninth of the day's illustration syncs.

**Span.** Output frames 235–1906 (0:07.83–1:03.53), 1671 frames — the whole board leg, still at full view with no camera move, as
David described. Verified by decoding: the OLD JPG rendered through the shipped leg spec (stroke forced to the old constant 5 for
the comparison) reproduces the live video at 3.01 mean per-pixel difference, sampled every 25 frames and at all seven ring onsets,
nothing over 6. The old asset's sha256 also matches the one recorded in the 09-16 v5 manifest, so baseline and spec belong to each
other.

**Highlights.** The shipped seven rings reused verbatim: The Library card, Search card, AI card, then each column's TIME TO ANSWER
row in turn, then the banner — same rectangles, colors, radii and onsets. The columns did not move in the refreshed art, checked
by drawing all seven rectangles on the new canvas. Stroke follows the artwork-scaled rule (owner, 2026-09-21, and his instruction
today that a synced video takes the current highlighting): 4 px at this camera, where the shipped video carried 5 px. Measured on
the candidate against the baseline at the Library ring: 4 px against 5.

**Build.** `scripts/video/build_questions_matter_answers_sync.py`. The rolls this video was assembled from no longer exist, so the
baseline is the shipped v5 itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 7ec1f3a73430…, 6688 frames, gitignored).
Geometry comes from the same code that built the shipped leg, `editspec_build.Build.compose` at its default tall margin: an
1840x1036 canvas at offset (120, 39) and the full-view camera [920, 518, 1840], matching the 09-16 v5 manifest. One
`ken_burns_path.py` leg, one concat pass, audio packet-copied.

- Asset: `course-assets/questions-matter/questions-matter-answers-faster.jpg` (6b8df44b0d50…, 1600x958). Previous: cf6069f59be6…,
  the sha the shipped build recorded.
- Candidate: `Prompts/questions-matter-v6.mp4` (45a69035d7fc…), shipped to `course-assets/questions-matter/questions-matter.mp4`
  and removed.
- Cache key `20260916ship1` → `20260921ship17` on the `questionsvaluable` entry. Pill unchanged and correct (4 min; 3:42.93).

**Note.** At build time the refreshed JPG was still uncommitted in the working tree — it belongs to the cast-refresh session
running in parallel, which commits its own assets and alt text. This ship staged only the video, this script, this audit directory
and the one `LESSON_VIDEOS` line.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 6688 frames at 30 fps, matching the baseline exactly. Leg decoded its 1671 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed all nine declared boundaries — the two splices and the seven ring onsets; both splice strips were
   inspected frame by frame (the Notebook inquiry-engine diagram into the board at 235, the board into the Pre-AI / With-AI value
   board at 1906), one clean cut each way, no stale frames, no board-render leak.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.39 (the new cast, plus the finer stroke); outside it
   mean 0.35, max 0.88 — re-encode noise. Nothing outside 235–1906 changed visually.
5. Ring states inspected (`state-000585-ring1-library.jpg` … `state-001642-banner.jpg`): correct component ringed in each, board
   still and whole throughout, card text readable, nothing clipped.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch, and no check of the lesson's other three boards (Where the Value Lives, and the two
   qualities boards), which this repair does not touch and the cast refresh did not change.
