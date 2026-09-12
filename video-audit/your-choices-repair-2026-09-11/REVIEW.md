# Your Choices v2 (2026-09-11) — candidate review kit

Source: Prompts/your-choices-1.mp4 (roll 1, REPAIR under NARRATION-REVIEW; comparison in
video-audit/your-choices-comparison-2026-09-11/REVIEW.md). Candidate: videos/your-choices-v3.mp4 (v2 superseded 2026-09-12: uncapped push clipped board 1 ring; board 1 now still, board 2 push capped at 1.5%), 5532 frames, 3:04.40.
Build: scripts/video/build_your_choices_review.py (editspec_build). Live file videos/your-choices.mp4 untouched.

## Edit
- Narration cuts (both in measured silence): 0:55.85–1:04.23 ("Understanding these initial parameters… first prompt")
  and 2:45.25–2:54.80 ("Mastering these engine settings… deep analytical tool"). Output transcript reads cleanly across both.
- Nine 1s room-tone pauses at idea boundaries; measured in the output as 1.25–1.65s silences at 0:07.8, 0:39.1, 0:57.6,
  1:03.8, 1:21.9, 1:52.7, 2:00.3, 2:23.4, 2:44.7.
- Board 1 (Choose the Tool, compact) from Notebook's own board cut at 1:04.27 through "…too weak a model"; full view
  5.4s + pause before the first ring; Which App ringed in purple at "Choice one is which app", Which Model in blue at
  "Choice two, which model". Rings trace the whole card (image + text panel), 5px, post-crop.
- Board 2 (Choose How It Works, compact) from its cut at 1:56.60 through "…many different sources"; Reasoning ringed
  teal, Research amber. Notebook's stock scenes elsewhere kept (all drawn; no archival photographs).
- Standard close from the engine close card's arrival cut (2:54.83 source): 48 prehold, 150 push to 1.2x, settle, 120 tail.
  Notebook's text card and branding removed.
- Gemini corner mark: cleaned on all 1676 kept source frames (1539 clone, 137 glyph-mask inpaint, 0 declined); corner-check.jpg.

## Ship checklist
- transition_guard: 20/20 boundaries pass (transitions/).
- Frame count 5532 decoded = manifest total. Frame 0 is Notebook's music-app drawing (no stock watermark).
- Board states: states-1-choose-tool.jpg, states-2-choose-how.jpg. Output contact sheets: bundle/your-choices-v2/sheets/.

## Listen (David's ear)
- Cut seams at 0:57.6 and 2:44.7; "teen accounts" (0:51) and "too weak a model" (1:52) wording.

## Shipped
2026-09-12: v3 approved ("ship it"); copied to videos/your-choices.mp4, cache key videos/your-choices.mp4?v=20260912ship1, candidate and both Prompts rolls deleted. Receipt: shipping-receipt.json.
