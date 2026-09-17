# Embeddings v6: SHIPPED 2026-09-17 (v5 + camera walk over Inside a Real Model)

**Candidate:** `Prompts/embeddings-v6.mp4` (3:58.17, 7145 frames, 30 fps, sha256 40bd17b71fea…). **Scope:** v5
(`../embeddings-repair-2026-09-17/REVIEW.md`: the five current boards and the canonical close re-rendered into the shipped v4, audio
copied) plus one change David asked for after eye-testing v5 ("At 2:59, we show the illustration board. When we show these, we typically
zoom and pan. This time, we didn't." / "Agree"): the Inside a Real Model span (output frames 5352-6509, 2:58-3:37) becomes a camera
walk. Everything else is v5, frame for frame (every-10th-frame diff against v5: only 5380-6220 differs). **Build:**
`scripts/video/build_embeddings_v6_retrofit.py` (imports v5's timeline, events, and renderers). **Manifest:** `edit-manifest.json` here.

## The walk (v4's rings at v4's frames; only the camera changed)

v4 cut between three framings of this illustration board: full view, a crop at the cat (3:04), a second crop at the dimension columns
(3:20), and back to full at Value (3:26). v6 replaces the three cuts with moves; the ring schedule is untouched.

| Output frames | Camera | Ring (v4) |
|---|---|---|
| 5352-5516 | full board, slight push to 97% (establish) | none |
| 5516-5540 | 24-frame glide into the cat window (cat card + Token ID card, x 40-1112, y 302-905) | cat card |
| 5632 | (hold) | Token ID card |
| 5763-5787 | 24-frame glide to the lookup-row window (x 437-1543, y 552-1174) | lookup row |
| 6015-6039 | 24-frame glide up to the dimensions window (x 387-1542, y 127-777; starts where v4's own crop did, so the EMBEDDING TABLE caption is whole) | d1-dn header |
| 6194-6224 | 30-frame pull-back to the full board | Value (amber, both parts) |
| 6362-6509 | full board, static; ends on the full illustration | Embedding row + caption (teal) |

Windows are 16:9 in image px, widened 10% around the components they hold, and clamped to the illustration's own rectangle (x 40-1559,
y 127-1174) so the board's lavender margin never enters a dived frame (the Where AI Works Best lesson). A ring that would clip during a
move waits until it is fully inside the frame; every settled ring sits at least 20 px inside. The student-ID board keeps v4's own glide.

## Verification (Edit Spec section 10, narrow repair)

1. Decoded frames 7145 = plan = v4; duration 3:58.17; audio stream MD5 identical to the live v4 (306b1d5ac0f635d0f651702a43b076d6).
2. `transition_guard.py` passed all 10 declared boundaries (561, 1171, 1518, 2776, 3741, 3881, 5187, 5352, 6509, 6891); every strip
   inspected (`guard/`, `guard-sheet.jpg`): one cut per boundary, destination on the first frame. The three intra-board cuts v4 had are gone.
3. No pause or audio edits.
4. Settled frames decoded from the encoded file at every window and every ring state (`final-*.jpg`, `final-walk-sheet.jpg`): right
   component, complete inside its ring, 5 px stroke. Frame-to-frame motion across the walk peaks mid-glide (smoothstep) with no spike at
   any move start or end.
5. Density: illustration camera walk with v4's rings (this board's components are named one by one, so the rings stay).
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope. The superseded v5 candidate is still in `Prompts/` for side-by-side; remove both candidates at ship.

**Shipped 2026-09-17** as `course-assets/embeddings/embeddings.mp4` (cache key 20260917ship1, pill 4 min); both candidates removed from `Prompts/`. Ship recipe was: copy to `course-assets/embeddings/embeddings.mp4`, new cache key on the `embeddings` entry (currently `20260910repair1`),
duration pill unchanged (4 min), refresh the manifest `video_assets` hash and size, remove `Prompts/embeddings-v5.mp4` and `-v6.mp4`.
