# Creative Thinking v3 (2026-09-12) — candidate review kit

Source: Prompts/creative-thinking-1.mp4 (roll 1, REPAIR under NARRATION-REVIEW; comparison in
video-audit/creative-thinking-comparison-2026-09-12/REVIEW.md). Candidate: videos/creative-thinking-v3.mp4, 5207 frames, 2:53.57 (v2 superseded: the first cut resumed 8 frames before Notebook's scene cut and flashed the brain drawing; owner report).
Build: scripts/video/build_creative_thinking_review.py (editspec_build). Live file videos/creative-thinking.mp4 untouched.

## Edit
- Narration cuts (all in measured silence): 0:23.0–0:29.77 ("Creativity isn't some mystical state of mind…"), 1:45.9–1:49.95
  ("We have reached a point where standard output is instantly available to all"), 2:51.5–2:55.1 ("This final image
  summarizes your role in a modern workflow", which also removes the engine's close card). Output transcript confirms none survive.
- Four room-tone pauses at new ideas: into who thinks creatively (0:22.7), into why it matters (1:33.4), into the four
  ways (1:52.6), before the close (2:43.7). None inside a board.
- Archival photograph of Steve Jobs (source 0:41.13–0:46.43) covered by the roll's own next frame, the Macintosh "hello"
  product shot (corner mark inpainted), so the cover runs seamlessly into that scene.
- Board 1, Who Thinks Creatively (tall 2x2 on side bars, dense): arrives at its intro sentence ("This board lays out…"),
  7.9s full view, dives to lawyer / entrepreneur / engineer / doctor as spoken (purple / blue / teal / amber), pulls back
  for "Creativity is not a job title…", ends at Notebook's own cut.
- Board 2, Four Ways to Think Creatively (dense): arrives at the lead-in "Creative thinking is a set of habits…", 8.2s full
  view, dives per way, pulls back for "These four habits widen your options. Then judgment picks the one that fits."
- Standard close from the third cut: 48 prehold, 150 push to 1.2x, settle, 120 tail.
- Gemini corner mark cleaned on every kept source frame (0 declined); corner-check.jpg. No other people appear.

## Ship checklist
- transition_guard: 14/14 boundaries pass (transitions/). Frame count 5207 decoded = manifest total.
- Board states: states-*.jpg. Output contact sheets and transcript: bundle/creative-thinking-v3/.

## Listen (David's ear)
- The three cut seams (output ~0:23, ~1:41, ~2:44) and the Jobs cover span (~0:35–0:41) for audio continuity.

## Shipped
2026-09-12: v3 approved ("ship it"); copied to videos/creative-thinking.mp4, cache key 20260912ship1, candidate and both Prompts rolls deleted. Receipt: shipping-receipt.json.

## Reshipped (v4)
2026-09-12: the first-row cards of both boards had been framed text-only (grid detector). Both board legs re-rendered with whole-card boxes and spliced into the v3 live render (build_creative_thinking_reframe.py; audio copied; 14/14 transitions; unchanged frames ~39 dB PSNR vs v3). Cache key 20260912ship2. Manifest: edit-manifest-v4.json; states-*-v4.jpg; transitions-v4/.
