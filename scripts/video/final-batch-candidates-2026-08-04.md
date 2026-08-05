# Final-batch board re-work — candidates for owner review (built overnight 2026-08-04)

Seven `-v2` candidates sit in `videos/`, one per re-worked video. Nothing is
installed: every original is untouched until you say ship per video. Every
candidate passed the standard battery — decoded frame count identical to its
original, audio stream bit-identical (MD5), dive/ring frames eyeballed.

Watch the listed span; nothing else in each video changed.

| Candidate | Changed span | What was wrong → what it is now |
|---|---|---|
| critical-thinking-v2 | 2:34–3:43 | Five-habits checklist floated bare with no title, and habit 2 still carried the Maria Petronoski callback cut from the lesson this morning. Now the actual lavender board with current copy; ring walks habits 1–5 on their narration onsets, wide open and close. |
| flattery-trap-v2 | 2:40–4:10 | Five-move playbook was a bare white card. Now the NumberedRows band at page width; ring walks all five moves (WEAK/BETTER sub-cards inside each ringed row). |
| document-trap-v2 | 3:23–4:22 | Four retrieval tactics floated bare with no title. Now the NumberedRows band; ring walks tactics 1–4. |
| fake-trap-v2 | 2:20–3:20 | Source/Context/Corroboration checklist was a bare card. Now the banded board; ring walks the three checks, wide out for "all three checks follow one rule." |
| training-bias-v2 | 1:46–2:15 | Four bias-mechanism cards floated bare. Now the ShowcaseBox band, 2×2 grid, ring visits each mechanism at its quick narration beat. |
| tokens-v2 | 1:27–1:49 and 2:57–3:34 | Both the tokenization 3-card board and the 01–05 tokenizer examples were bare. Both now banded at page width; second span's ring walks all five example rows. |
| support-trap-v2 | 1:20–1:35 | "Why AI feels like real support" cards floated bare with an invented in-board title (the page renders that line as a kicker outside the board). Now the banded two-card board, ring per card. |
| (shipped batch context) | — | These follow the exact pattern of the ten videos shipped earlier today; the build pattern is documented in board-audit-2026-08-04.md. |

## Not built (lower-severity, flagged for a follow-up pass)

Per the Final-batch audit, these boards are wrapped but have title/width nuances
worth a look before deciding whether they warrant rebuilds:

- one-more-thing: "Same list, five draws" and "The Bill" (titles on canvas, faint wrappers)
- how-ai-answers: "Score every token" (white-outline card, no colored band)
- vector-space: airplane token board (no title)
- ai-is-math: probability boards (composed-capture style; page-element check needed)
- hallucination: failure-modes board title; RAG board column width; glue-recipe
  cards are likely prose-visualizing scenes (exempt)

Also standing: how-an-llm-works engine-era drift (from the first audit) — owner-confirmed 2026-08-05: excluded from the exact-parity queue, gets its own dedicated full-video pass.
