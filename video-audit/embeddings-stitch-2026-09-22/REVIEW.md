# Embeddings v3 — roll 1 plus two grafts from roll 2 (2026-09-22)

`Prompts/embeddings-v3.mp4` — 5:24.73 (9742 frames), built by `scripts/video/build_embeddings_v1.py`.
Three-way comparison of rolls 1 and 2 against the live video is in
`video-audit/embeddings-comparison-2026-09-22/REVIEW.md`.

**Verdict: ready for David's eye test. Every measurable check passes, and the eight verbatim lines and
every number were verified on the encoded file rather than assumed from the plan. Nothing shipped; the
live video, rolls, lesson and boards are unchanged.**

## What it is made of

| | source | carries |
|---|---|---|
| spine | roll 1 | all eight verbatim lines, every number the lesson gives, the definition order |
| `labels` | roll 2, audio only, +1.4 dB | "We explicitly named our traits, like sweet or fizz. An AI has no dimension labels at all." — Board 4's last two rows, whose taste-test side roll 1 left unspoken |
| `neighbours` | roll 2, audio only, +1.4 dB | "It stores one embedding for every single token, meaning cat sits right alongside rows for dog, latte, truck, and bicycle." — names the neighbours roll 1 skips, and removes its "master ledger" |

Both grafts replace rather than insert, and both sit under a board.

**The `labels` graft was deliberately cut short.** Roll 2 continues "It simply captures complex
mathematical patterns…", which is not the lesson's register. Taking only its first two sentences leaves
roll 1's own next line — "They simply capture patterns in how a token is used in data", which *is* the
lesson's wording — to finish the row. Verified in the encoded file:

> "…including complex decimals. **We explicitly named our traits, like sweet or fizz. An AI has no
> dimension labels at all.** They simply capture patterns in how a token is used in data. Both use a row
> of numbers to describe something."

## Verified on the encoded file

| Requirement | Result |
|---|---|
| All eight verbatim lines | **8 / 8** — including "Each position always means the same thing." @1:47 + "The number says how much." @1:52, and "Six numbers match. The seventh tells them apart." @2:52 |
| Badge numbers | **all four** — 1024, 2048, 3072, 4096 |
| Coke's six scores | **all six** — 9, 1, 10, 2, 3, 8 |
| Coffee's six scores | **all six** — 1, 9, 0, 9, 8, 10 |
| Citrus trio | Coke 1, Pepsi 10, coffee 0 |
| cat's ID and row | 4719; 0.45, negative 0.23, 0.80, 0.17 … negative 0.35, with "negative" spoken |
| Definition order | vector → dimension → value |
| Content prohibitions | no token-ID-carries-meaning, no named traits for AI, no named model, no distance or similarity math, no club activity, none of the banned words |
| Opening | no title card |

## QA

- **transition_guard: 15/15, a clean pass.** v2's single flag was Board 5's pull-back camera move; that
  board is now static at full view on David's direction, so the motion the detector was tripping on is
  gone. No false positives remain.
- **Audio: zero dips** at any of the 15 boundaries; **no true-silence windows** anywhere.
- **Gemini mark: 0 hits across 217 sampled frames.**
### David's highlight direction, 2026-09-22 — applied

Every rect below is measured off the artwork, not estimated: Board 2's chips column by column
(SWEET 441-543, BITTER 631-730, FIZZ 818-918, HEAT 1001-1103, CAFFEINE 1189-1291, DARK 1378-1479),
Board 3's the same plus CITRUS 1389-1492 with Pepsi's dark-green chip at 1392-1489, and Board 5's table
body and plaques by colour.

- **Board 2.** After the takeaway, the rings keep moving with the narration: **Coke plus 9, 1 and 10** as
  the question names them, **Coke's whole row** on "the whole row of numbers is a vector", **the six
  dimension headings** on "each individual position", and **a single value chip** on "the specific number
  placed inside it".
- **Board 3.** It had been ringing Coke while the narration introduced Pepsi. Now: **the name Pepsi
  alone**, then **only her first six values** with Citrus deliberately outside the ring, then **the CITRUS
  heading**, then **Pepsi's 10 and Coke's 1 as each is spoken**.
- **Board 4.** The last two comparison rows are **one ring across both**, not two.
- **Board 5.** **The full illustration holds for the board's whole run - no dive** - because seeing how
  the pieces fit together is the teaching. Rings move item to item: both left plaques as the token and its
  ID are named, the other tokens' rows under the graft, the first two columns, the d1-dn headings, cat's
  row, the circled 0.45, then the whole row again as the embedding.

Boards 2 and 3 no longer use the API's `banner_at`, which forces the banner ring to hold to the end of the
board. Both keep teaching after their takeaway line, so the banner is now an ordinary ring in the sequence.

- **Boards.** Ring colour measured off each board: Boards 2 and 3 label their rows in plain black with no
  accent, so their rows take the neutral video purple; Board 4's columns measure #149288 teal and #5334c5
  purple, but its rings run whole rows across both columns, which is a whole-board point and therefore
  neutral too. Board 5's elements have no accents of their own either, so its rings are neutral as well -
  which also keeps them distinct from the board's built-in purple glow and yellow circle.
- **Protected sources: 8/8 hashes unchanged.**

### One defect QA caught

**Thirteen frames of roll 1's own recreation of the embedding-table board** survived after our canonical
Board 5 left (source 8652–8664; roll 1 cuts at 8665). Fixed with `picture_advance`.

This is the sixth consecutive stitch in which a board exit leaked the roll's own recreation, and it is
worth stating that the two detection routes are complementary rather than redundant:

- **transition_guard caught this one** because roll 1's recreation is visually distinct from our board.
- **It did not catch Support Trap's**, where the recreation was near-identical to the real board, so the
  cut between them fell under the detector's change threshold and only a frame-by-frame look found it.
- **It also misses long ones** — Engagement Trap's nine-frame leak passed the gate because the detector
  needs two cuts within six frames.

A board exit therefore needs both the guard and an eye on the frames either side. That is now noted in
this build script.

## Notes for the eye test

- **Board 2 runs 62.9 s**, the longest in the file — roll 1 covers the whole taste test in one unbroken
  scene, so there is no alternate footage to cut away to. It now carries eight ring states rather than
  three, which keeps the board moving with the teaching.
- **The floor step.** Roll 1's pause floor is −56.4 dB against roll 2's −62.8, so each graft steps down
  6.4 dB into a quieter room and back up on the way out. Both are short and under a board, and down-then-up
  is the less audible direction, but it is the one thing here I cannot judge without ears.
- **"vable" versus "fable"** is acoustically ambiguous in both rolls and flips under prompt biasing either
  way. The build uses roll 1, whose unbiased decode lands on "Vable". Worth your ear.
- Roll 1's board-furniture phrases remain — "Look at this illustration…", "This table captures…", "This
  updated table shows…", "This comparison chart maps…" — which the kit bans. Two are standalone sentences
  that could be cut if you want them gone; the other two carry teaching content.
- Voice drift roll 1 adds beyond the lesson's register: "In formal AI terminology", "model architecture",
  "complex decimals", "an organizational tool". None are banned words.
- The lesson's prose line "funny, into hockey, or the person who steals fries at lunch" is in none of the
  rolls; only the live video has it.

## At ship time

`index.html` carries the Embeddings entry with its current cache key and pill; both need updating, and
5:24.73 is a **5 min** pill by the course's convention (4:25 → 4 min, 4:37 → 5 min).
