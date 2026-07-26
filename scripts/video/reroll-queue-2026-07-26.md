# Re-roll queue — 20 weakest videos, 2026-07-26

Ranked by the **sheet's** r3 grade (the authoritative source; the CSVs in this
folder are stale and disagree). Ties at 82 broken by the weaker teaching
sub-scores, which is why welcome / why-learn-ai / opener-avoid make the cut and
hallucination / document-trap / engagement-trap (also 82) sit just outside.

**Every kit below is complete and roll-ready: prompt + boards + `.md` on disk,
every prompt under the 5,000-character cap.** Upload the lesson `.md` plus the
numbered jpgs in order, then paste the prompt.

| # | lesson | grade | cov | mat | tea | brd | cln | pac | boards | prompt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | does-school-matter | 76 | 17 | 11 | 11 | 8 | 13 | 16 | 2 | 4,018 |
| 2 | which-app | 76 | 17 | 10 | 12 | 8 | 14 | 15 | 3 | 4,561 |
| 3 | ai-is-math | 76 | 15 | 12 | 12 | 8 | 14 | 15 | 3 | 4,752 |
| 4 | transformer | 76 | 15 | 12 | **10** | 8 | 14 | 17 | 5 ⭐ | 4,673 |
| 5 | fake-trap | 78 | 15 | 12 | 12 | 8 | 15 | 16 | 4 | 4,930 |
| 6 | training-bias | 79 | 16 | 12 | 11 | 9 | 14 | 17 | 3 ⭐ | 4,939 🆕 |
| 7 | flattery-trap | 79 | 15 | 12 | 11 | 9 | 16 | 16 | 4 | 4,780 |
| 8 | learn-with-ai | 80 | 16 | 11 | 11 | 10 | 16 | 16 | 4 | 4,765 |
| 9 | ai-is-different | 80 | 16 | 12 | 11 | 8 | 16 | 17 | 4 🆕 | 5,000 🆕 |
| 10 | questions-matter | 80 | 15 | 12 | 11 | 9 | 16 | 17 | 4 ⭐ | 4,723 |
| 11 | evaluate-the-results | 80 | 17 | 12 | 11 | 9 | 15 | 16 | 4 | 4,996 🆕 |
| 12 | critical-thinking | 80 | 16 | 12 | 11 | 8 | 16 | 17 | 5 | 4,795 |
| 13 | what-is-ai | 81 | 16 | 12 | 11 | 9 | 16 | 17 | 4 | 4,777 |
| 14 | how-an-llm-works | 81 | 16 | 12 | 11 | 9 | 16 | 17 | 6 ⭐ | 4,777 |
| 15 | where-ai-works-best | 81 | 17 | 11 | 12 | 10 | 16 | 15 | 5 | 4,775 |
| 16 | embeddings | 81 | 17 | 13 | 12 | 8 | 15 | 16 | 3 | 4,624 |
| 17 | mind-trap | 81 | 17 | 13 | 12 | 9 | 15 | 15 | 2 | 4,980 🆕 |
| 18 | welcome | 82 | 17 | 11 | 11 | 8 | 18 | 17 | 3 | 4,669 |
| 19 | why-learn-ai | 82 | 16 | 12 | 11 | 9 | 17 | 17 | 4 🆕 | 4,964 🆕 |
| 20 | opener-avoid | 82 | 17 | 11 | 11 | 10 | 17 | 16 | 3 | 4,231 |

⭐ carries a why-carrying board (the lever that took layers from 10 to 13/15 on
teaches-vs-recites). 🆕 built or written today.

## Built to fill the gaps

Four kits were unrollable this morning. All four are now complete.

- **ai-is-different** — had **no boards and no prompt** for the course's longest
  lesson. Four boards captured: `1-normal`, `2-ai` (the side-by-side split into
  a matched pair, since each column already carries What it needs / So how it
  acts / Superpower with its reasons), `3-kryptonite`, `4-close`. Prompt written.
  The PS5 three-asks element was captured and **discarded** — it renders as a
  tall portrait block inside 16:9, which is exactly the shape that makes the
  engine zoom and pan. That beat stays in the narration, off-board.
- **why-learn-ai** — had **no boards and no prompt**. Four captured:
  `1-everyday`, `2-thrive` (already why-carrying — each numbered row is a
  reason), `3-quote` (the White House card), `4-close`. Prompt written.
  The everyday-apps grid was 4-across with an orphan fifth card and ~60% dead
  space in row two, so it got the same `numcols-3` treatment as welcome: 3+2,
  second row centred. Page and board stay in sync per the standing rule.
- **evaluate-the-results** — had 4 boards, no prompt. Written.
- **mind-trap** — had 2 boards, no prompt. Written.

## Prompt-sizing note

All four new prompts blew the 5,000-cap on first draft (5,558–6,485). What got
them under was **not** trimming rules — it was cutting the restatement of each
board's rows out of the body. The board and the attached `.md` already carry
those reasons verbatim, so the prompt only has to force the walk: name the rows
in order, then *"speaking the reason written under each, in the board's own
words. Never read the headings and move on."*

`ai-is-different` needed a structural cut on top of that: its rules block was
consolidated from 13 to 12 by merging the two narration-style rules. Even so it
lands at exactly 5,000. If that lesson ever needs another prompt clause,
something else has to come out.

## Upload manifests

Boards are numbered in upload order. Three files on disk are **repair assets, not
kit boards** — do not upload them: `training-bias-cow-insert.jpg`,
`hallucination-1-why-card.jpg`, `hallucination-2-patterns-card.jpg`.
`flattery-trap-4-guardrail.jpg` **is** a kit board (added during the 7/22 repair).

## Deduct-targeting already in the prompts

Every prompt in this queue carries rule 7 against style-prompt leakage and rule 6
against pseudo-text in props — the two defect classes that cost the most
cleanliness points across the catalog. `training-bias`'s rule 7 is the hardened
version, written against its own named defect (the engine lettered "FINELINER
WITH ALCOHOL-MARKER" and "ANALOG TEXTURE AND ANNOTATINES" into the artwork at
0:20, 2:24 and 3:28).
