# Why Learn AI? v3 (2026-09-13) — candidate review kit

Source: Prompts/Why_Learn_AI__The_Historical_Shift.mp4 (REPAIR under NARRATION-REVIEW; comparison in
video-audit/why-learn-ai-comparison-2026-09-13/REVIEW.md), built from the copy Prompts/why-learn-ai-2.mp4.
Candidate: videos/why-learn-ai-v3.mp4, 6486 frames, 3:36.20 (v2 superseded: its four stock photographs are replaced by drawings borrowed from the live video; owner call). Build: scripts/video/build_why_learn_ai_2_review.py.
Live file videos/why-learn-ai.mp4 untouched.

## Edit
- One narration cut (in measured silence): 3:23.0–3:31.8 ("We are looking at a massive economic and cultural shift…
  This brings us to one simple truth."), which also removes the engine's close card. Transcript confirms it is gone.
- Four room-tone pauses at new ideas: into AI is everywhere (0:24), into you can start now (1:11), into this has
  happened before (2:31), before the close (the cut). None inside a board.
- Board 1, AI Is the Press (faces; not uploaded; compact, still): over "You face two choices… take your place"
  (0:13.9–0:24.2 source), replacing Notebook's choice cards. Notebook's scribe drawings before it and its Gutenberg
  press diagram after it are kept.
- Board 2, Where AI Already Lives (five cards, dense): from its intro sentence on Notebook's own cut (0:36.83), 3.8s full
  view, dives to each card as spoken (purple / blue / red / green / amber), pulls back at 1:03.3 and rings the banner at
  "Long before anyone was talking to chatbots…".
- Board 3, Why You'll Thrive (three cards, dense): from its intro sentence six frames ahead of Notebook's cut (1:51.9),
  3s full view, dives per reason (purple / blue / teal), pulls back at 2:22.3 and rings the banner at "Start now…".
- Standard close from the cut: 48 prehold, 150 push to 1.2x, settle, 120 tail.
- Notebook spans kept (rule 8b report): scribe and 1000x disruption drawings 0:00–0:14; Gutenberg press diagram and
  workplace-tools cards 0:24–0:37; build-skills timeline, drafting tools, vintage computer photo, magazines, design-skill
  diagram, laptop drawing 1:11–1:52; anvil-to-data-center diagram, factory engine photo, old computer photo, narrow
  automation diagram, White House photo, action-plan cards 2:31–3:23. The roll's four stock photographs (vintage computer 1:28–1:33, factory engine
  2:37–2:44, old computer 2:44–2:50, the White House 2:59–3:10 source) are REPLACED, picture only, by Notebook drawings
  from the current live video of this lesson: the Layout Ready Macintosh (live 2:41.8–2:48.7) under "desktop publishing
  put powerful design tools on a teenager's desk"; the gear, lightning bolt, and globe sequence (live 3:04.0–3:15.2, last frame held 1.6s) under
  steam engine, electricity, internet; the Winning the Race document (live 3:22.6–3:31.8, last frame held 1.5s) under
  "In July 2025, the White House released…". No photograph remains in the candidate. Longest unbroken board run: 35s
  (thrive). No interleaving needed.
- Gemini corner mark cleaned on every kept source frame; corner-check.jpg.

## Ship checklist
- transition_guard: all boundaries pass (transitions/). Frame count decoded = manifest total.
- Board states: states-*.jpg. Output contact sheets and transcript: bundle/why-learn-ai-v3/.

## Listen (David's ear)
- The cut seam before the close (~3:22 output); "Run the machine, or someone else will take your place" (0:20) is the
  roll's paraphrase of the page's "Run it, or someone else will."

## Shipped
2026-09-13: v3 approved ("Ship it"); copied to videos/why-learn-ai.mp4, cache key 20260913ship1, candidate deleted, rolls kept in Prompts/. Receipt: shipping-receipt.json. Spec 8c (photographs never ship) added the same day.

## v4 (2026-09-14): the roll 1 Where AI Already Lives graft (beat-by-beat rule)

**Candidate:** `videos/why-learn-ai-v4.mp4` (3:57.2, 7117 frames; v3 was 3:40). v4 = the shipped v3 with one best-of graft from the
comparison REVIEW.md plan: roll 1's walk of the Where AI Already Lives board (roll 1 40.20–95.30, every row with its job and all its
examples, ending on "AI was already part of your daily routine long before these conversational chat bots arrived") replaces roll 2's
compressed version (36.83–70.9) under the board. Roll 1 lowered 2.24 dB (speech RMS; loudnorm puts the rolls 1.5 LU apart). The dense
leg's five dives and the banner follow roll 1's onsets (Recommends 44.54, Navigation 54.24, Face recognition 62.14, Voice assistants
72.98, Chatbots 80.04, pull back 88.7, banner 89.82). Roll 2 resumes at "The great news is…" after the existing pause. Nothing else changed.

Re-rendered twice. 15:53: the first v4's seam pairs showed one frame of Notebook's own board render after the pause (source 2127; v3
carried it too); the picture now resumes on Notebook's cut (2128). 17:57: David's note on the 15:53 file ("at 3:00 the narration is
about steam engines… but the graphics show the White House report") exposed a build bug: the three picture-only borrows
(`video_src=`) pointed at `videos/why-learn-ai.mp4`, which was the July video when v3 was built on 2026-09-13 and became v3 itself
when v3 shipped, so v4 borrowed v3's frames (the Winning the Race drawing under the steam-engine line, the close board under the
White House line). The borrows now come from the archived July video (`archive/why-learn-ai/why-learn-ai-live-before-2026-09-13.mp4`,
restored with `git show 13e9d84:videos/why-learn-ai.mp4`; gitignored; asserted and protected by the build). README gotcha added.
`v4-back-half-sheet.jpg` and `v4-mac-borrow-f3400.jpg` show the three drawings under their lines. Checks on the 17:57 render (13
boundaries now, the borrow seams added: 417, 757, 1135, 2818, 3340, 3487, 4048, 5253, 5428, 5813, 6099, 6421, 6841; all passed): decoded 7117 = plan, audio 237.248 s (one AAC frame over plan); `transition_guard.py` passed all 7
boundaries (417, 757, 1135, 2818, 4048, 5253, 6841), `boundary-pairs.jpg` inspected; pauses 23.84–25.33, 92.80–94.01 (after the graft),
173.41–175.07, 226.24–228.17, plus roll 1's own 0.95 s gap before its banner line at 86.47; joins re-transcribed on the final file:
"…hand you on day one." 36.90 → "This board shows where AI is already integrated into your day" 38.16, and "…chat bots arrived." 92.08 →
"The great news is you do not have to wait" 93.92; floors −59 to −75 dB into both onsets, no cliff. Corner mark 3139 cloned / 444
inpainted / 0 declined. `states-1-everyday.jpg` inspected: each dive lands on the named card at roll 1's onset, banner edge to edge.
**Listen:** 37–39 (roll 2 into roll 1, the voice is hotter in roll 1 so the −2.24 dB matters) and 92–94.5 (back to roll 2).
Live v3 unchanged until David ships.
