# Board-rules audit — 2026-08-04

Audit of the 15 FINAL & DONE videos that shipped before the evaluate-the-results
re-cut, against the two owner rules established on evaluate-the-results:

- **Rule 1:** the board in the video must exactly match the design on the page
  (same wrapper, same headline situation, no reformatting).
- **Rule 2:** boards are never resized — a different band width re-wraps every
  text line and ships a different experience than the lesson.

Method: frame sweeps of every video (5 parallel audits, frames retained in the
session scratchpad), board compositions compared against the live components in
index.html. Drawn/sketch scenes, photo-composited scenes, diagrams, and close
boards are out of scope (they are not lesson-box boards).

## Verdicts

### Compliant (board matches page wrapper + headline; width at worst minor)

| Video | Boards checked |
|---|---|
| welcome | path board (ShowcaseBox band + "Here's your path." ✓), tools board ("What you'll need" ✓) |
| context-window | Luke/Nate paired boxes (blue/lavender wrappers ✓); diorama tour is a cinematic scene, exempt |
| where-ai-works-best | four-shapes board (four accent wrappers, accent rings ✓); TV poster is a photo scene, exempt |
| does-ai-think | think-vs-AI table (two-tone wrapper + headline ✓); card scene is drawn, exempt |
| why-learn-ai (board 1) | everyday-apps board (ShowcaseBox band + headline ✓) |
| learn-with-ai (boards 1–2) | study-tool comparison + feed-in pipeline (wrappers ✓) |
| ai-is-different (boards 1–2) | PS5 poster (photo scene, exempt) and rules-vs-patterns columns (wrappers ✓) |
| how-an-llm-works (board 2) | LEARN ONCE / ANSWER EVERY WORD pair (wrappers ✓) |

### Rule violations — wrapper dropped and/or resized (page has a lavender
### ShowcaseBox/NumberedRows band; video floats bare cards, often wider)

| Video | Board | Violation | Span |
|---|---|---|---|
| art-of-prompting | Three Moves walk | no wrapper, no overall headline, wide re-wrapped text | ~0:80–3:22 — the video's core |
| what-you-can-control | three-step action list (NumberedRows on page) | band dropped, widest text lines in the audit | ~1:46–2:34 |
| learn-with-ai | five-tip list (NumberedRows on page) | band dropped, no title in frame, near-full-frame text width | ~2:00–3:00 |
| questions-matter | four-qualities board | no wrapper, no headline, wide text | ~1:34–2:42 — the video's core |
| which-app | big-three board (page: primaryFaint band + in-band headline) + "What we used" board | bands dropped; "What we used" also headline-less | ~1:42–2:54, ~3:18–3:50 |
| what-is-ai | "What's an LLM?" (DecodeCards = ShowcaseBox on page) | band dropped | ~3:10–3:42 |
| ai-is-different | "You'll see stories like this" (ShowcaseBox on page) | band dropped | ~3:02–3:18 |
| does-school-matter | "Two skills" board (ShowcaseBox on page) | band dropped, wide text | ~1:10–1:54 |
| opener-work | "IN THIS SECTION / Work With AI" board | cards float bare; page treatment to confirm | ~1:34–1:54 |
| why-learn-ai | thrive board (NumberedRows on page) | wrapper ambiguous in frames; ~20-word lines suggest wider than the 902px page column | ~1:42–2:26 |

### Engine-era drift (not tour-related)

- **how-an-llm-works** boards 1, 3, 5, 7, 8: engine-drawn composed boards with
  marker underlines/yellow highlights on cream canvas. Several are composed
  one-offs (probability chart, prediction window) with no exact lesson element —
  the compose exemption applies — but the training-loop walk and the closing
  NOT MAGIC trio have page counterparts and carry hand-drawn marks the page
  doesn't. Lower priority; a re-treatment would be a full-video pass.

## Why this happened

Every pre-ETR highlight tour used capture_board_states.js before today's fixes:
the innermost-match rule lifted the card grid OUT of its ShowcaseBox/NumberedRows
wrapper, and BANDW was chosen per-capture for camera travel rather than pinned to
the lesson's 902px column. Both defects are fixed at the tool level (WRAP_UP=1 +
BANDW 0 standard invocation, committed 2026-08-04); this audit covers the
already-shipped catalogue.

## Re-work cost

No re-rolls needed: narration and structure are untouched. Each fix is the
evaluate-the-results post pattern — recapture the board (WRAP_UP=1, BANDW 0),
re-derive camera windows from the new rects, re-render that board's runs, and
swap the leg in a single re-encode. Estimate: one board ≈ the L2 rebuild done
today. Suggested order = the violations table order (worst spans first).
