# Tokens v2: SHIPPED 2026-09-22

**Shipped** on David's instruction ("ship it") as `course-assets/tokens/tokens.mp4`, sha256 48f170a1ed6794de…, 5:05.27,
9158 frames, 30 fps. Cache key `20260916ship1` → `20260922ship6` on the `tokens` entry (ship1–ship5 were taken by other
sessions today), and the duration pill goes **4 min → 5 min** (the retired v8 was 3:37). Candidates v1 and v2 removed from
`Prompts/`; the raw rolls `tokens-1.mp4` and `tokens-2.mp4` are kept.

## v2 changes, on David's review of v1

1. **Board 4's rings were floating above the cards.** v1 took the card rectangles as [40, 122, 785, 718] and
   [815, 122, 1560, 718]; the cards' own bodies are [41, 128, 782, 715] and [817, 128, 1558, 715], measured off each
   coloured panel and its white body. The six-pixel overshoot at the top put the stroke on the board's background
   above the image, which is what David saw. Both sides are re-measured and the ring now traces the card edge
   (`state-4-cat-0144.jpg`, top-left corner inspected at full resolution).
2. **3:26–3:36 is deleted.** Removed: "All the text you send to AI gets split." and "Let's look at a few distinct
   examples of how the cl100k-based tokenizer handles different formats." The cut runs source 6108 → 6400, inside the
   silences either side (203.45–203.82 and 213.20–213.42), so nothing is clipped: the seam reads "…A token ID
   identifies the token. Meaning comes later." → one-second pause → "This list shows how AI chops up text."
   (transcribed from the candidate to confirm). Board 5 now arrives at source 6400, four frames before Notebook's own
   cut, so none of its own rendering of that board reaches the screen.

   *Teaching note:* this removes the lesson's bridge line ("All the text you send to AI gets split into tokens", the
   kit's beat 10), which the narration review rated TAUGHT. Board 5 still gets its own introduction. Flagged, not
   argued — David asked for the cut.
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
| B4 Humans See a Cat | 5450–6168 | Compact, still. Rings: Instant Understanding 183.60, Token ID 190.50, banner 199.80. Card rects re-measured in v2. |
| B5 How AI Splits Text Into Tokens | 6198–8188 | Dense: full view first, then dive to each of the five rows at 216.30 / 223.00 / 229.70 / 239.10 / 256.00, pull back at 270.30. The board is 1600x1288; at full view its body text is ~16 px on the delivered frame, so the rows are dived. |

**Board 2 is the face board.** The roll was fed `Prompts/tokens-building-blocks-faceless.jpg`; the canonical
`course-assets/tokens/tokens-building-blocks.jpg` (two students, Stars jerseys) replaces it in the edit, as the kit specifies.

**Four pauses of one second**, at idea boundaries only: after Board 1 into "how do your words become numbers" (output 945), after
Board 2 into where the pieces come from (3423), after Board 4 into the split examples (6168), and before the closing message
(8805). Standard close from Notebook's own close cut (source 9007), canonical `tokens-close.jpg`, prescribed push.

**One fix during the build.** The Board 2 walk first clamped its camera windows inside the photograph, which is the house rule for
scene boards; the reuse row sits *below* the photo, so the "move to the reuse row" beat was pulled back up into the machine. The
clamp is now the board itself, and the row reads clearly (`preview/2-blocks/kb5-hold-the reuse row-in.jpg`).

## Verification

1. Decoded 9158 frames at 30 fps, 5:05.27, matching the prepared plan exactly.
2. `transition_guard.py` on all fourteen declared boundaries: **PASS, none failed**. The new seam at 6198 was inspected frame
   by frame: the cat board holds through the pause with its banner ring, then one clean cut to Board 5 at full view. This video has no camera motion inside a
   compact board and no grafts, so there are no detector false positives to discount.
3. Pause audit (`silencedetect -35 dB`): exactly four long gaps, at 30.89, 113.58, 205.21 and 292.93 — the four planned
   boundaries and no others. No automatic one-second minimum was applied anywhere else.
4. Corner mark: 2,498 frames cloned, 266 inpainted, **0 declined**.
5. Protected files unchanged (roll 1, the live `tokens.mp4`, `lessons/tokens.md`, all five board JPGs).
6. Board states inspected on every ring and camera state (`states-*.jpg`, `preview/*`): correct component ringed in each, board
   text readable at every dive, nothing clipped at a frame edge, each board opens whole and unmarked.
7. The canonical close is the literal final frame, carrying both closing lines (`check-last-frame.jpg`).

## Not done / for David

- **Not watched end to end by me, and not auditioned by ear.** The narration is roll 1's, untouched, and it was reviewed in full
  from the transcript; David approved the ship without asking for a machine watch.
- One accepted pronunciation slip stands: "the Witten word cat" (190.74). The other, "Claw 100K base" for `cl100k_base`, sat
  inside the deleted 3:26–3:36 and is gone.
- The retired v8 (3:37, shipped 2026-09-16 under the old method) is superseded; it remains recoverable from git history.
