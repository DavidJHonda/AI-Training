# Honesty & Privacy v4 (2026-09-12) — candidate review kit

Source: Prompts/honesty-&-privacy-2.mp4 (roll 2, KEEP under NARRATION-REVIEW; comparison in
video-audit/honesty-and-privacy-comparison-2026-09-12/REVIEW.md), built from the ampersand-free copy
Prompts/honesty-and-privacy-2.mp4. Candidate: videos/honesty-and-privacy-v4.mp4, 7200 frames, 4:00.00 (v2 superseded: eight pauses inside boards; v3 superseded: JPG corner matte showed at the board bottoms; both owner reports 2026-09-12, fixed in the shared module).
Build: scripts/video/build_honesty_privacy_review.py (editspec_build). Live file videos/honesty-and-privacy.mp4 untouched.

## Edit
- No narration cuts. Ten room-tone pauses, each at a new idea (hook -> honesty question, into each board's section, into
  privacy, into uploads, into why this matters, into if-you-already-shared, before the close); none inside a board.
  Measured in the output as >= 1.2s silences.
- Board 1, Using AI in School (compact, still): arrives inside the silence before "This graphic breaks down…", full view
  9.9s + pause before the first ring; Acceptable green, Follow the Rules amber, Unacceptable red, whole-card rings.
- Board 2, When AI Help Is Allowed (faces; not uploaded): arrives at its own intro sentence ("Sometimes, a teacher will
  explicitly allow…", 1:03.3 source) and runs to 1:33.0, replacing Notebook's robot diagrams, 1-2-3 collage and handshake;
  10.5s of full view before the first ring; step columns ringed purple / blue / teal at "Step one/two/three"; banner
  ringed at "If your name is on the work".
- Board 3, How Much Should You Share (compact, still): from the silence before "This chart maps out…"; tiers ringed
  green / amber / red.
- Board 4, Share Only What AI Needs (compact, still): from the silence before "Say you snap a photo…"; each of the six
  items rings its photo callout and its legend row together at the spoken word (word-level onsets from small.en); banner
  ringed at "You meant to share the homework".
- Standard close from just before the engine card's arrival (3:39.2 source): 48 prehold, 150 push to 1.2x, settle, 120 tail.
  Notebook's text card and branding removed.
- Gemini corner mark: cleaned on all 3631 kept source frames (3168 clone, 463 glyph-mask inpaint, 0 declined); corner-check.jpg.
- Notebook's drawn scenes kept elsewhere; every person shown is a Notebook drawing (1:36, 2:56, 3:16 source), no archival photos.

## Ship checklist
- transition_guard: 29/29 boundaries pass (transitions/).
- Frame count 7200 decoded = manifest total. Frame 0 is Notebook's blank paper (no stock watermark).
- Board states: states-*.jpg. Output contact sheets and transcript: bundle/honesty-and-privacy-v4/.

## Listen (David's ear)
- Board arrivals sit a few frames ahead of Notebook's own cuts inside measured silence (0:22.5, 1:03.3, 1:59.5, 2:35.5 source);
  the close line "Two AI habits" (base.en misheard it, small.en confirms).

## Shipped
2026-09-12: v4 approved ("ship it"); copied to videos/honesty-and-privacy.mp4 (the lesson entry was comingSoon; now wired with cache key 20260912ship1), candidate and both Prompts rolls deleted. Receipt: shipping-receipt.json.
