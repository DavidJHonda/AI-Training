# Make Your Move v4 (2026-09-12) — candidate review kit

Source: Prompts/make-your-move-1.mp4 (roll 1, REPAIR under NARRATION-REVIEW; comparison in
video-audit/make-your-move-comparison-2026-09-12/REVIEW.md). Candidate: videos/make-your-move-v4.mp4, 9877 frames, 5:29.23 (v3 superseded: boards ran wall-to-wall from 1:12 to the close; owner call, Notebook's own drawings now break them up).
Build: scripts/video/build_make_your_move_3_review.py (editspec_build). Live file videos/make-your-move.mp4 untouched.

## Edit
- Five narration cuts (all in measured silence, ~62s): 1:01.5–1:11.47 ("You do not need a perfect map…", resuming on
  Notebook's scene cut); 2:21.9–2:34.9 ("Across these information-heavy professions…", keeping "This rule extends directly
  into physical and trades work" as the second career board's intro); 3:25.2–3:38.8 ("Regardless of the industry…");
  4:41.5–4:52.2 ("Mastering these four skills…"); 5:55.4–6:12.9 ("Taking these specific actions… This image summarizes…",
  which also removes the engine's close card). The transcript confirms none survive.
- Five room-tone pauses at new ideas: into the note (0:35.6), into careers (the first cut), into skills that travel (the
  third cut), into the four moves (the fourth cut), before the close (the fifth cut). None inside a board.
- Board 1, A Note from Nate and Luke (faces; not uploaded; compact, still): over Notebook's "Message from the Creators"
  card and the creators sketch, 0:35.8–1:01.5, no rings.
- Notebook's own drawings break up the boards (v4): its career-monolith diagrams run under "a job is a collection of
  tasks"; the whiteboard silhouettes (re-timed from a cut span) under "This rule extends…"; the clipboard and meeting
  drawings (re-timed) under the skills intro; the city drawing (re-timed) under the moves intro; and inside the skills and
  moves boards the board leaves after each ring holds for Notebook's core-competency diagrams, the two people talking,
  the hands at a keyboard, and the donation drive, returning one second before the next title so every cut lands on a
  still view. Notebook's own renders of our boards never appear.
- Boards 2a/2b, How AI Might Change Careers (faces; not uploaded; three cards, dense): 2a arrives 3s before the doctor
  rings and dives to doctor / teacher / lawyer (purple / blue / teal), pulling back before the cut; 2b arrives at "If you
  are an electrician" with the ring popping in the full view and the dive waiting 2s (spec rule 3), then designer and
  entrepreneur, pulling back before the cut.
- Boards 3 and 4 (2x2, dense): arrive ~3s before their first ring, dive per card; board 3 pulls back before the cut,
  board 4 leaves for the donation drive.
- Standard close from the fifth cut: 48 prehold, 150 push to 1.2x, settle, 120 tail.
- Gemini corner mark cleaned on every kept source frame (0 declined); corner-check.jpg. Every person Notebook drew is a
  drawing; the career boards' people are the course's own page assets.

## Ship checklist
- transition_guard: 26/26 boundaries pass (transitions/). Frame count 9877 decoded = manifest total.
- Board states: states-*.jpg. Output contact sheets and transcript: bundle/make-your-move-v4/.

## Listen (David's ear)
- The five cut seams (output ~1:02, ~2:13, ~3:04, ~4:07, ~5:12); the first closing line's spoken preface ("By understanding
  how these models work and where human judgment remains critical, you know how to be smarter than the tool").

## Shipped
2026-09-12: v4 approved ("Ship it"); copied to videos/make-your-move.mp4, cache key 20260912ship1, candidate deleted, source rolls kept in Prompts/. Receipt: shipping-receipt.json.
