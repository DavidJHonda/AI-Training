# Learn with AI v3 (2026-09-14) — candidate review kit

Source: Prompts/learn-with-ai-1.mp4 (roll 1, REPAIR under NARRATION-REVIEW; comparison in
video-audit/learn-with-ai-comparison-2026-09-14/REVIEW.md); move two from roll 2. Candidate: videos/learn-with-ai-v3.mp4 (v2 superseded: the Exploration catch ring clipped its third line), 6415 frames,
3:33.83. Build: scripts/video/build_learn_with_ai_2_review.py. Live file videos/learn-with-ai.mp4 untouched.

## Edit
- Cuts (in measured silence): 1:50.8–2:00.83 ("Selecting the wrong column… hours of preparation", resuming on Notebook's EXAM F
  cut) and 3:33.3–3:36.0 ("The overarching rule for all of this is simple", which also removes Notebook's close card).
- Roll 1's garbled move two ("Add your [moats], the presentation slides…", 2:50.4–3:00.9) replaced, audio only, by roll 2's
  "Move two. Give it the full picture. Upload all materials, notes, slides, videos." (level-matched, −0.6 dB) with our Four
  Moves board staying on screen, its move-two card ringed. Transcript reads straight through it.
- Five room-tone pauses at new ideas: into the patient tutor (0:22), into the guiding question (0:39), into why Gemini
  Notebook (on the first cut), into the four moves (2:27), before the close (on the second cut). None inside a board.
- Board 1, Which Study Tool for the Job? (compact, still): from "As you can see here, there are two main categories…"; each
  side's sections ring as spoken (header, what it does, best use, the catch; blue then purple). The banner is not ringed
  because the roll never speaks it (it said the cut "wrong column" line instead).
- Board 2, How Gemini Notebook Works (faces; not uploaded; compact, still): arrives at "Gemini Notebook should be your
  primary tool" over Notebook's EXAM F drawing and its synthesis diagrams; You Upload (blue) and You Get (green) ring as
  spoken; banner ringed at "This pipeline takes a chaotic folder…", the roll's paraphrase of "Turn your class materials into
  the study tools you need" (kept for that reason).
- Board 3, Your Four Moves (2x2, dense): from "To get the most out of those uploaded materials…" (Notebook's own cut), 5.3s
  full view, dives per move (purple / blue / teal / amber), pulls back at 3:24.6 and rings the banner at "Executing these
  four moves…", the roll's paraphrase of "Use AI to strengthen the learning, not skip it."
- Notebook spans kept (8b): overwhelmed-student diagram, 24-hour math, 1:00 AM cards, patience loop (0:00–0:39); desk,
  materials and chat sketches (0:39–0:55). No photographs. Longest unbroken board run: 56s (which study tool). No interleaving.
- Standard close from the second cut; Gemini corner mark cleaned on every kept source frame; corner-check.jpg.

## Ship checklist
- transition_guard: 14/15 pass; the one flag (f4932) is the graft's start, where the dive to the move-two card begins on the
  same frame — camera motion, not a stale frame. Frame count decoded = manifest total.
- Board states: states-*.jpg. Output contact sheets and transcript: bundle/learn-with-ai-v3/.

## Listen (David's ear)
- The graft at ~2:44–2:51 (roll 2's voice under our board); the two cut joins (~1:52 and ~3:23); the compressed
  four-more-hours joke at 0:13 ("We cannot add four more hours to your day").

## Shipped
2026-09-14: v3 approved ("ship it"); copied to videos/learn-with-ai.mp4, cache key 20260914ship1, candidate deleted, rolls kept. Receipt: shipping-receipt.json.

## v4 (2026-09-14): two roll 2 grafts under Which Study Tool (beat-by-beat rule)

**Candidate:** `videos/learn-with-ai-v4.mp4` (3:40.4, 6613 frames; v3 was 3:34). v4 = the shipped v3 plus the two grafts from the
comparison REVIEW.md plan, both under the Which Study Tool board, both roll 2 at +0.65 dB (speech RMS; loudnorm puts roll 2 about 1 LU
under roll 1):
1. Focus best use and the catch: roll 2 43.10–57.75 ("Choose this path when you have the materials the test covers. Class notes,
   screenshots, study guides, a web page, or a YouTube video. There is a constraint. If notes miss a key concept, Gemini Notebook cannot
   reliably fill the gap.") replaces roll 1 72.70–86.05 ("This is best when… like class notes, study guides, or videos. The catch is…
   the AI cannot fill the gap."). The Focus card's best-use and catch rings follow roll 2's onsets.
2. The board's takeaway, absent from roll 1: roll 2 90.65–96.0 ("Avoiding that trap relies entirely on choosing the tool that matches how
   you need to learn.") added after the Exploration card, where roll 1's cut aside used to be; banner ring at its onset, then the
   existing pause into Why Gemini Notebook. The board is built as two legs (Focus through the graft; Exploration through the banner),
   both compact and still.

Checks on the 15:50 render: decoded 6613 = plan, audio 220.437 s (one AAC frame over plan); `transition_guard.py` passed all 7
boundaries (1698, 2241, 2680, 3422, 3612, 4656, 6325), `boundary-pairs.jpg` inspected; pauses 21.74–23.12, 39.42–41.01, 119.01–120.49
(after the banner line), 153.74–155.30, 209.64–210.93; joins re-transcribed on the final file: "…what you actually need to learn." 74.16
→ "Choose this path…" 75.04; "…cannot reliably fill the gap." 88.66 → "On the other side, we have exploration tools" 89.42; "…how your
teacher taught it." 113.58 → "Avoiding that trap…" 114.52 → "…need to learn." 118.66 → pause → "When you are studying…" 120.18; floors
−60 to −85 dB into each onset, no cliff. Corner mark 1347 cloned / 291 inpainted / 0 declined. `states-1-study-tools.jpg` and
`states-1-study-tools-b.jpg` inspected: Focus header, what, best use, catch; Exploration header, what, best use, catch; banner.
**Listen:** 74–75.5, 88.5–90, 113.5–115, and 118.5–120.5 (roll 2's voice in and out, three times).
**SHIPPED 2026-09-14** on David's "ship it": v5 moved to `videos/learn-with-ai.mp4`, cache key `?v=20260914ship2`, duration pill 3 → 4 min (3:40).

## v5 (2026-09-14): Notebook scenes between the boards (EDIT-SPEC 8b)

**Candidate:** `videos/learn-with-ai-v5.mp4` (3:40.4, 6613 frames; audio identical to v4). David on v4: "the boards start at :57 and appear
through the rest of the video." Neither roll drew anything for the Which Study Tool content (both rendered that board with crops), so
that board still runs 62 s; the other runs are now broken by roll 1's own drawings, and each board arrives 3 s before its first ring:
1. Notebook's notebook-and-chat sketch (roll 1 1638–1646, then held) carries "As you can see here, there are two main categories…";
   Which Study Tool arrives at 58.2 (v4: 54.6).
2. Notebook's source-grounded diagram (3625–3825, drawing itself) carries "Gemini Notebook should be your primary tool… exact sources
   your teacher provided"; How Gemini Notebook Works arrives at 127.5 (v4: 120.8) and leaves at 149.8 after the banner ring holds 3 s.
3. Notebook's files-to-sticky-notes-and-mind-map drawing (4494–4638, then held) carries "This pipeline takes a chaotic folder…",
   the pause, and "To get the most out of those uploaded materials…"; Your Four Moves arrives at 157.0 (v4: 154.6).
Not used: Notebook's "stop passive reading" card under the four-moves takeaway (Notebook replaces it with a three-column diagram
that is still drawing itself where the cut would land); the banner stays the last board image before the close.
Board runs now: 62 s (Which Study Tool), 22 s (How It Works), 53 s (Four Moves).

Checks on the 18:23 render: decoded 6613 = plan; `transition_guard.py` passed all 11 boundaries (1698, 1806, 2241, 2680, 3422, 3612,
3812, 4481, 4649, 4727, 6325), `boundary-pairs.jpg` inspected; pauses unchanged from v4 (21.74, 39.42, 119.01, 153.74, 209.64); graft
seams unchanged; corner mark 1871 cloned / 291 inpainted / 0 declined. Live v3 unchanged until David ships.
