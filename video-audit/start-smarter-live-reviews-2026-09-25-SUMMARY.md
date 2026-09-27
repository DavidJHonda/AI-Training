# Start Smarter: live-video narration reviews with board timing (2026-09-25)

Evaluate-first pass over the seven shipped videos (Welcome has no video by design). Each lesson was reviewed in its
own fresh session under `scripts/video/NARRATION-REVIEW.md` against the VISIBLE page text of `index.html` exported
the same morning, the upload Markdown, the current boards, and the prompt's verbatim list. New this pass (owner
request): every course board's on-screen span was MEASURED with `scripts/video/board_spans.py` (ORB feature match
every 0.5 s) and judged under Edit Spec 8b as FINE / LONG (walking, over 30 s, no cut-away) / DEAD (narration past
the board). Bundles, `board-spans.txt`, and `REVIEW.md` live in `video-audit/<slug>-live-review-2026-09-25/`.
Contested lines were re-transcribed with medium.en; no audio was listened to by a person.

| Lesson | Runtime | Verdict | Points R/T/Th/M/W | Hard reqs | Longest board | Boards back to back | Deciding finding |
|---|---|---|---|---|---|---|---|
| Why Learn AI? | 3:57 | **REROLL** | 10/15/0/2/0 | 9/11 | Where AI Already Lives 56 s | no | Two page sentences never spoken ("Most of what it does today…", the how-to-start instruction); "Run it, or someone else will." reworded |
| What Is AI? | 2:57 | **REROLL** | 19/10/1/0/0 | 7/11 | Two Ways You Already Use AI 55.5 s | 1:05 to end, 112 s | All four verbatim lines paraphrased, including both closing lines; Ask the Desk leaves 2.9 s before its banner is spoken |
| How an LLM Works | 6:23 | **KEEP** | 17/15/0/0/0 | 13/13 | Same Word. Different Odds. 90.6 s | no | Complete, all eight percentages, close verbatim; `learn-once.jpg` is an orphan asset |
| Does AI Think? | 3:40 | **REROLL** (KEEP if banner waived) | 9/15/0/0/0 | 9/10 | When You Think. What AI Does. 72.5 s | no | Banner "Similar-looking answers can come from very different processes." never spoken; hedges hardened into assertions |
| Beyond the Average | 2:46 | **KEEP** (on the 9/14 waivers) | 12/7/0/1/0 | 9/10 | What to Start Building Today 54 s | no | Only gaps are the two already waived; every board within 0.8 s of its onset |
| In Your Hands | 3:04 | **REROLL** (KEEP if close waived) | 6/18/0/0/0 | 12/13 | What's in Your Hands? 81.5 s | 0:35 to end, 148 s | Closing line 1 says "the technology" for "AI"; otherwise complete |
| Learn with AI | 3:40 | **KEEP** | 10/13/0/0/0 | 3/3 | Which Study Tool for the Job? 60 s | no | Complete; two takeaway banners paraphrased (accepted at ship); kit gap: "It does not know what you did not give it." |

DEAD spans: none in any video. Every long span is the narration walking the board.

## Board timing: the section-wide problem

Every video in this section has at least one board over 50 s, and two run boards back to back to the last frame
(What Is AI 112 s, In Your Hands 148 s). None of these can be broken under 8b from existing material: the rolls
drew nothing usable under those beats (or drew people), and the pristine source rolls were deleted after shipping.
The only options per lesson are (a) accept the dive-and-pan as shipped, (b) re-time one of the file's own drawings
as a cut-away (proposed with timestamps in Learn with AI, How an LLM Works, What Is AI), or (c) reroll and plan
breaks from the new roll's drawings. Rerolls therefore double as the board-break fix.

Detector notes: two false positives in How an LLM Works (3.0 s at 2:31, 2.5 s at 5:59, Notebook drawings) and one
1.0 s in Why Learn AI (2:56.5); all under 3 s and identified as such by the reviewers. Same Tool in Beyond the
Average is on screen only 10 s and that fully covers its spoken content.

## Owner decisions needed

1. **Does AI Think**: waive the unspoken banner line and it is KEEP, editing only (8b breaks on the 72.5 s board;
   two Notebook cards with invented figures at 0:28.5 and 0:36.5 to replace).
2. **In Your Hands**: waive "the technology" for "AI" in closing line 1 (accepted at the 9/16 ship) and it is KEEP,
   editing only; the 148 s board run stays unless rerolled.
3. **Learn with AI**: confirm the two paraphrased takeaway banners stay accepted.
4. **What Is AI** and **Why Learn AI**: reroll. Both need kits on the 2026-09-20 recipe.

## Kit notes for rerolls (Start Smarter has no registry entries yet)

- All seven lessons are absent from `Prompts/upload-sets.json`; each reroll needs a registry entry and a sync.
- Why Learn AI: verbatim list must carry "Most of what it does today, it will do better tomorrow.", the how-to-start
  instruction, "Run it, or someone else will.", the press banner, and the close; press board uploads as a faceless
  variant.
- What Is AI: all four lines that were paraphrased (brain definition, Board 3 banner, both closing lines) into the
  verbatim list; Ask the Desk uploads as a faceless variant; guard against invented dates on timelines.
- Does AI Think (if rerolled): the banner line and the hedges ("may", "doesn't prove") as verbatim; side-by-side as
  a faceless variant.
- In Your Hands (if rerolled): both closing lines verbatim with no lead-in sentence; the stale
  `scripts/video/paths/what-you-can-control-*.json` files are housekeeping.
- Learn with AI: add "It does not know what you did not give it." to the Markdown before any reroll.
- How an LLM Works: remove or place `learn-once.jpg`; it is on no page, Markdown, or prompt.
