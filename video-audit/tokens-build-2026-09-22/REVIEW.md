# Tokens v1: review candidate, built 2026-09-22

**Candidate:** `Prompts/tokens-v1.mp4` — 5:15.00, 9450 frames, 30 fps, sha256 457283a003724e81….
**Base:** `Prompts/tokens-1.mp4` (roll 1), which earned KEEP in `video-audit/tokens-comparison-2026-09-22/REVIEW.md`.
**Scope:** full production pass, picture only. David, 2026-09-22: the "hasn't published Claude's" line is fine on listening and
neither optional donor from the live video is wanted, so **the narration ships uncut and ungrafted** — no cuts, no grafts, no
re-ordering. Build: `scripts/video/build_tokens_v1.py`.

## What was built

Five boards, each replacing Notebook's own rendering at the roll's own visual cut (`scenes.py`):

| Board | Output span | Treatment |
|---|---|---|
| B1 You Use Words. AI Uses Numbers. | 309–945 | Compact, still. Rings: the YOU bubble at 17.00, the AI bubble at 21.30 held through the whole reply. AI Chat rule — no dive into a conversation. |
| B2 Building Blocks for Language | 1947–3423 | Photo camera walk: establish with a small push, dive to the machine at 72.80 (TEXT card → un / belie / vable), move down to the reuse row at 96.30, pull back to the full illustration at 106.50, ring the banner at 110.20. No rings on the photograph. |
| B3 What Happens When You Hit Send | 4349–5480 | Compact, still. Rings: Start With Text 146.10, Split Into Tokens 150.30, Look Up Token IDs 155.80 held through the three IDs, banner 175.60. |
| B4 Humans See a Cat | 5480–6200 | Compact, still. Rings: Instant Understanding 183.60, Token ID 190.50, banner 199.80. |
| B5 How AI Splits Text Into Tokens | 6554–8540 | Dense: full view first, then dive to each of the five rows at 216.30 / 223.00 / 229.70 / 239.10 / 256.00, pull back at 270.30. The board is 1600x1288; at full view its body text is ~16 px on the delivered frame, so the rows are dived. |

**Board 2 is the face board.** The roll was fed `Prompts/tokens-building-blocks-faceless.jpg`; the canonical
`course-assets/tokens/tokens-building-blocks.jpg` (two students, Stars jerseys) replaces it in the edit, as the kit specifies.

**Four pauses of one second**, at idea boundaries only: after Board 1 into "how do your words become numbers" (output 945), after
Board 2 into where the pieces come from (3423), after Board 4 into "all the text you send" (6200), and before the closing message
(9097). Standard close from Notebook's own close cut (source 9007), canonical `tokens-close.jpg`, prescribed push.

**One fix during the build.** The Board 2 walk first clamped its camera windows inside the photograph, which is the house rule for
scene boards; the reuse row sits *below* the photo, so the "move to the reuse row" beat was pulled back up into the machine. The
clamp is now the board itself, and the row reads clearly (`preview/2-blocks/kb5-hold-the reuse row-in.jpg`).

## Verification

1. Decoded 9450 frames at 30 fps, 5:15.00, matching the prepared plan exactly.
2. `transition_guard.py` on all fifteen declared boundaries: **PASS, none failed**. This video has no camera motion inside a
   compact board and no grafts, so there are no detector false positives to discount.
3. Pause audit (`silencedetect -35 dB`): exactly four gaps of ~1.6 s (the roll's own ~0.6 s plus the inserted second) at 30.89,
   113.58, 205.21 and 302.66 — the four planned boundaries and no others. No automatic one-second minimum was applied anywhere else.
4. Corner mark: 2,792 frames cloned, 266 inpainted, **0 declined**.
5. Protected files unchanged (roll 1, the live `tokens.mp4`, `lessons/tokens.md`, all five board JPGs).
6. Board states inspected on every ring and camera state (`states-*.jpg`, `preview/*`): correct component ringed in each, board
   text readable at every dive, nothing clipped at a frame edge, each board opens whole and unmarked.
7. The canonical close is the literal final frame, carrying both closing lines (`check-last-frame.jpg`).

## Not done / for David

- **Not watched end to end by me, and not auditioned by ear.** The narration is roll 1's, untouched, and it was reviewed in full
  yesterday; but the ship checklist wants a human watch before publication.
- **The pill would go 4 min → 5 min** (the file is 5:15 against today's live 3:37).
- Two accepted pronunciation slips from the review stand: "Claw 100K base" for `cl100k_base` (159.46) and "the Witten word cat"
  (190.74).
- Nothing has been shipped. The live `course-assets/tokens/tokens.mp4` and `index.html` are untouched.
