# Understand AI opener v6: review candidate (2026-09-16, the What Kind of Thing Is AI? board added, the current section map; visual-only retrofit of the shipped v4)

**Candidate:** `Prompts/understand-ai-opener-v6.mp4` (2:34.60, 4638 frames, 30 fps). v6 = v5 plus the current section-map render (David: "We want
the current board."); v5 superseded. **Scope** (David: "The live video is the base. We need to
add the board that appears in the lesson. The rest might be okay as is."): narrow visual repair of the shipped v4
(`course-assets/understand-ai-opener/understand-ai-opener.mp4`, sha256 e657b34b984d7ceb…). **Source limitation, disclosed:** the raw
rolls (`Prompts/understand-opener-3/4.mp4`) no longer exist, so the build takes the finished v4 as its picture source, replaces two spans,
and muxes v4's original audio stream back in untouched. Outside the two spans the picture is one more encoding generation of v4 (mean
per-pixel difference under 3, visually identical). **Live video unchanged.** **Build:** `scripts/video/build_opener_understand_v6_retrofit.py`.
**Manifest:** `edit-manifest.json` here.

## The three changed spans

1. **Output 0–352 (0:00–0:11.73): the What Kind of Thing Is AI? card** (`understand-ai-opener-kind.jpg`, 0c22c537be…, 1600x900; compact,
   still) replaces Notebook's data-center opening still while the narrator reads the card's four lines. Each line is ringed in the card's
   gold at its spoken onset (re-heard on the finished file): "It's not magic" 0.30, "it's not a person" 1.82, "and it's definitely not
   normal software" 3.12, "It is entirely its own kind of thing" 5.96; the last ring holds under "operating by a completely different set
   of rules". The first line is spoken from frame 0, so the first ring pops in the full view (Edit Spec rule 3). The board leaves on
   Notebook's own cut to its expert drawing at "Sometimes working with AI…" (0:11.73); v4's one blank wash frame before that cut (f351) is
   covered.
2. **Output 4410–4638 (from 2:27.00): the close** is the canonical closing JPG (`understand-ai-opener-close.jpg`, 92bb4e24b8…, 1746x600)
   on the white stage at the house pill size, where v4 had the legacy rendered pill on the lavender stage.

3. **Output 2451–4410 (1:21.70–2:27.00): the section map** is re-rendered from the current `understand-ai-opener-section-map.jpg`
   (ad14b2e2d2…, 1600x1091; the video had the Sep 10 render). Old and new maps measured identical in every row panel and text row; only the
   title alignment and the banner width (now edge to edge) differ. The shipped treatment is reproduced: the board at full view throughout,
   the five row rings at the same output frames (2813, 3039, 3286, 3627, 3906), the takeaway ring on the banner at 4231 following the new
   banner's edges, and the two pauses inside the span holding the frame before them. (The v4 script carried topic pans that the shipped
   file never used; a first pass reproduced those and was discarded once the frame comparison showed the live file at full view.)

Everything else is v4's picture: Notebook's drawings, the Under the Hood board with its banner ring, and the pauses.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 4638 = plan = v4; duration 2:34.60 = v4; audio stream MD5 identical to v4 (50dcb41df44eb9479cf15519d7645073).
2. `transition_guard.py` passed all three declared boundaries (352, 2451, 4410); `boundary-pairs.jpg` inspected: the card's last frame to
   Notebook's expert drawing on its own first frame; the reassurance drawing to the map's full view; the map's takeaway frame to the close.
3. No pause or audio edits (the audio is v4's stream, copied).
4. Ring states inspected (`states-kind.jpg`; `states/topic-*.jpg` and `states/map-takeaway.jpg` for the map): each gold ring traces one line
   of the card; each map ring traces its row, the takeaway ring the full banner; frame-by-frame comparison of the map span against the live
   file shows only the title and banner differing (mean per-pixel difference under 3).
5. The card is compact and still; the other boards' treatment as v4.
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/understand-ai-opener/understand-ai-opener.mp4`, new cache key on the `openerfoundations` entry
(currently `20260910repair1`), duration pill unchanged (3 min).
