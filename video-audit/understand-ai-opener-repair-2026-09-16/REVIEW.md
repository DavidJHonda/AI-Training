# Understand AI opener v7: SHIPPED 2026-09-16 ( the What Kind of Thing Is AI? card as the page frames it, the current section map, one phrase cut; retrofit of the shipped v4)

**Candidate:** `Prompts/understand-ai-opener-v7.mp4` (2:32.93, 4588 frames, 30 fps). v7 = v6 with David's two notes: (1) the card is shown
as the page frames it: the page crops the 1600x900 JPG to the navy card (OpenerNavyBoard, board 80,300–1520,600); v5/v6 showed the whole
canvas, so the card read as a thin band. The video now uses a 16:9 crop of the same JPG, [40,22,1560,877], centering the card at 94% of
the frame width (`canvas-kind-crop.png`, a temporary canvas of the canonical asset; nothing redrawn). (2) "As you move through the
course," (141.10–142.36) is cut, live frames 4231–4281, from the end of the pause to the trough before "you'll" (142.48–142.78, −46 to
−61 dB); the sentence resumes "you'll see that each topic builds directly on the one before it.", re-transcribed clean on the finished
file ("…how much math goes into it." 139.40 → pause → "You'll see that each topic…" 140.98). The audio is now edited, so the mux takes
the build's edited track rather than v4's stream. v6 = v5 plus the current section-map render (David: "We want the current board."); v5 and v6 superseded. **Scope** (David: "The live video is the base. We need to
add the board that appears in the lesson. The rest might be okay as is."): narrow visual repair of the shipped v4
(`course-assets/understand-ai-opener/understand-ai-opener.mp4`, sha256 e657b34b984d7ceb…). **Source limitation, disclosed:** the raw
rolls (`Prompts/understand-opener-3/4.mp4`) no longer exist, so the build takes the finished v4 as its picture source, replaces two spans,
and muxes v4's original audio stream back in untouched. Outside the two spans the picture is one more encoding generation of v4 (mean
per-pixel difference under 3, visually identical). **Shipped 2026-09-16** as `course-assets/understand-ai-opener/understand-ai-opener.mp4` (cache key 20260916ship1, pill 3 min); the v7 candidate removed from Prompts/. **Build:** `scripts/video/build_opener_understand_v7_retrofit.py`.
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

1. Decoded frames 4588 = plan (v4's 4638 minus the 50-frame cut); audio 152.939 s. Audio changed only at the cut (Build's 5 ms room-tone
   crossfades); every other span is v4's audio sample for sample.
2. `transition_guard.py` passed all three declared boundaries (352, 2451, 4360); `boundary-pairs.jpg` inspected: the card's last frame to
   Notebook's expert drawing on its own first frame; the reassurance drawing to the map's full view; the map's takeaway frame to the close.
3. Pauses on the final file (silencedetect −35 dB): 29.48–30.77, 35.31–36.65, 64.86–66.35, 80.49–81.89, 139.61–141.13, 144.04–145.50; close
   hold 149.20–152.94. The pause before the cut phrase now leads straight into "you'll see"; no pause added.
4. Ring states inspected (`states-kind.jpg`; `states/topic-*.jpg` and `states/map-takeaway.jpg` for the map): each gold ring traces one line
   of the card; each map ring traces its row, the takeaway ring the full banner; frame-by-frame comparison of the map span against the live
   file shows only the title and banner differing (mean per-pixel difference under 3).
5. The card is compact and still; the other boards' treatment as v4.
6. Not auditioned by ear: David should listen to 2:19–2:22 (the cut seam).
7. Nothing left undone in scope.

**At ship:** move to `course-assets/understand-ai-opener/understand-ai-opener.mp4`, new cache key on the `openerfoundations` entry
(currently `20260910repair1`), duration pill unchanged (3 min; 2:33).
