# Final-batch board re-work — candidates for owner review (built overnight 2026-08-04)

Seven `-v2` candidates sit in `videos/`, one per re-worked video. Nothing is
installed: every original is untouched until you say ship per video. Every
candidate passed the standard battery — decoded frame count identical to its
original, audio stream bit-identical (MD5), dive/ring frames eyeballed.

Watch the listed span; nothing else in each video changed.

| Candidate | Changed span | What was wrong → what it is now |
|---|---|---|
| ~~critical-thinking-v2~~ | — | SUPERSEDED and SHIPPED 2026-08-05 (7023d49): the exact-parity queue rebuilt all four boards (equations, chocolate, habits) in one owner-approved pass under the current ring-only rules. |
| ~~flattery-trap~~ | 0:37–0:52, 1:56–2:17, 2:45–4:10 | SHIPPED 2026-08-06 as v5 (owner: "Great video. Ship-it."); incumbent retired to Prompts/donors/2026-08-06/. v3 added the Gatsby responses board rebuild at 0:37–0:52 (banded 902px two-column, panel rings amber/blue, bullet-row rings via new `row:true` capture option). v4 adds both owner-flagged fixes on top: (1) 1:56–2:17 the off-lesson reply card replaced with the lesson's own amber ChatGPT board, four sentences highlighted as quoted (new `mark:true` sentence-highlight option — soft amber text background, zero layout shift); (2) 2:45–4:10 five-move playbook rebuilt with the art-of-prompting response grammar — purple row ring walks the moves as before, PLUS red ring on WEAK and green ring on BETTER as each prompt is spoken; entry crossfade from the sketch scene reproduced, exits on the original cut to the close leg. Battery: 7742 frames exact, audio MD5 identical to shipped, one spike per hard seam, fade/junction diffs in range. v2/v3 kept for comparison until approval. |
| ~~document-trap~~ | 1:57–2:27, 2:50–3:12, 3:15–4:14 | SHIPPED 2026-08-06 as v3 (owner: "ship-it"); incumbent retired to Prompts/donors/2026-08-06/. Was: SUPERSEDES v2 (owner lesson pass + video flags). v3 = v2's four-tactics rebuild (now at 3:15–4:14 after the excision) PLUS: (1) chunks board 1:57–2:27 rebuilt on the page's redesigned 3-step box (title+body rows, compact-board full-frame hold, row rings walk the steps); (2) white-on-light query-grid span 2:50–3:04 replaced with a Ken Burns tour of the lesson's own illustration (open → tournament booklet outside the dashed border → summary note), narration untouched; (3) the "rigid mathematical proximity rather than true comprehension" sentence excised (audio+video, 234 frames) — same abstraction the owner cut from the lesson. Runtime 5:14 → 5:06; label stays 5 min. Battery: 9,175 frames exact (9,409−234), four joints one-spike-clean, audio splice whisper-verified ("…make the cut. If the phrasing…"), pts-delta histogram single-valued. EAR-TEST the audio joint at 3:04. |
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
