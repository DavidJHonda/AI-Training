# Board-rules audit — 2026-08-04

Audit of the 15 FINAL & DONE videos that shipped before the evaluate-the-results
re-cut, against the two owner rules established on evaluate-the-results:

- **Rule 1:** the board in the video must exactly match the design on the page
  (same wrapper, same headline situation, no reformatting).
- **Rule 2:** boards are never resized — a different band width re-wraps every
  text line and ships a different experience than the lesson.
- **Rule 3 (made explicit 2026-08-05):** the board in the video must match the
  page's CURRENT CONTENT, not just its design. A shipped video board goes stale
  the moment its lesson box is edited; format-compliant boards can still fail
  this (caught twice by accident in these audits: critical-thinking's Maria
  callback, opener-work's bridge copy). Auditing a video means diffing its board
  text against today's page, and editing a lesson box means flagging its video.

NOTE: the 2026-08-04 audits below checked rules 1-2 systematically; rule 3 only
incidentally. "Compliant" verdicts below mean format-compliant — their content
parity has NOT been verified against the current page.

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

## Re-work status (updated as items ship)

| # | Video | Status |
|---|---|---|
| 1 | art-of-prompting | SHIPPED (owner-approved) |
| 2 | questions-matter | SHIPPED (owner-approved) |
| 3 | what-you-can-control | SHIPPED (owner-approved) |
| 4 | learn-with-ai | SHIPPED (owner-approved) |
| 5 | which-app | SHIPPED (owner-approved) — subgrid rings composited in post |
| 6 | what-is-ai | SHIPPED (owner-approved) — accent-ring L/L/M dives |
| 7 | ai-is-different | SHIPPED (owner-approved) — wide-with-rings |
| 8 | does-school-matter | SHIPPED (owner-approved) — wide-with-rings |
| 9 | opener-work | SHIPPED (owner-approved) — page header included; content drift also fixed |
| 10 | why-learn-ai | SHIPPED (owner-approved) — NumberedRows band + headline |

Highlight grammar (owner rule 2026-08-05, learn-with-ai comparison span): the
effect has two granularities, chosen per narration beat — a BOARD ring (panels:
boundary around the card/box) when the narration addresses the box as a whole,
and an ITEM ring (elements: boundary around a row/section/line) the moment the
narration names a part. If the narration walks a card's sections, the ring
walks them too; a card ring held across spoken sub-sections is the failure mode.

Framing (owner rules 2026-08-05): a dive frames the WHOLE card — never crop
or pan inside it (four-shapes redo). And on a sequential steps board (training
loop, phase walks), skip dives entirely: hold the full board and let the ring
walk the steps as they're named (how-an-llm-works loop redo).

Highlight treatment (owner rules 2026-08-05, how-an-llm-works pass): the ring
adopts the accent of the box it wraps — a purple ring on a purple-themed board,
the card's own border color on an accent card (`{"label","ring":"#f59e0b"}`),
and an explicit ring override recolors the label chip too. And on a box with
few words the boundary IS the highlight: pass `{"chip": false}` so the ring
draws with no pill behind the spoken words — owner showed three examples
(training-loop step card, patterns row, odds card) and the whole video went
ring-only.

Build pattern per item (proven on 1-4): intake span boundaries (scenes.py,
--seam for dissolves) + transcript for junction onsets; capture with
capture_board_states.js (BANDW 0 always; WRAP_UP=1 only when the innermost
match is inside a ShowcaseBox/NumberedRows wrapper — a board that IS its own
primaryFaint box needs WRAP_UP=0; NumberedRows row labels include their emoji
icon in textContent; Bad/Better labels are "Bad"/"Better" title case; bullet
rows prefix "•"); build runs via a builder script (upscale 2 on 2400x1400
canvases, 3 on 1600x900), junctions at narration word onsets; assemble with
the concat FILTER (never -c copy across mixed legs), -map 0:a -c:a copy;
verify frame count identical + audio MD5 identical + eyeball frames incl.
post-junction; deliver as videos/<name>-v2.mp4 for owner eye-test; install +
commit only on owner approval.

## Re-work cost

No re-rolls needed: narration and structure are untouched. Each fix is the
evaluate-the-results post pattern — recapture the board (WRAP_UP=1, BANDW 0),
re-derive camera windows from the new rects, re-render that board's runs, and
swap the leg in a single re-encode. Estimate: one board ≈ the L2 rebuild done
today. Suggested order = the violations table order (worst spans first).

# Final-batch audit — 2026-08-04 evening (critical-thinking → fake-trap, 21 videos)

Same two rules, same method (6 parallel frame audits). transformers-quiz has no
boards (by design, exempt). Compliant throughout: opener-understand, training,
transformer, layers, embeddings, mind-trap, engagement-trap, opener-avoid.

## Rebuild queue (clear violations — bare cards / no wrapper / no title)

| # | Video | Board | Span | Notes |
|---|---|---|---|---|
| 1 | critical-thinking | five-habits checklist | ~154-216s | page: primaryFaint HABITS box; bare cards, no title in video |
| 2 | flattery-trap | five-move playbook | ~156-252s | video's core span; bare card, no title, WEAK/BETTER sub-cards |
| 3 | document-trap | four-step retrieval list | ~198-262s | bare card, no title |
| 4 | fake-trap | Source/Context/Corroboration | ~138-196s | bare card, no title |
| 5 | training-bias | four bias-type cards | ~106-130s | bare cards, no title |
| 6 | tokens | tokenization 3-card board + tokenizer examples 01-05 | ~86-106s, ~182-214s | both bare, no title |
| 7 | support-trap | "Why AI feels like real support" | ~78-88s | bare cards w/ title |

## Page-check-needed (possible partial violations)

- one-more-thing: "Same list, five draws" (~90-116s) and "The Bill" (~222-258s)
- how-ai-answers: "Score every token" (~148-184s)
- vector-space: airplane token board (~110-131s, no title)
- ai-is-math: probability boards (composed-capture style; check lesson elements)
- hallucination: failure-modes board title, RAG board width; glue-recipe cards
  (likely prose-visualizing scenes, exempt)

Candidates land as videos/<name>-v2.mp4 for owner review; nothing installed
without approval.

# Content-parity sweep (Rule 3) — 2026-08-05

Seven parallel agents transcribed every non-rebuilt lesson board (~44 boards
across 24 videos) and diffed word-by-word against the current index.html.

**Result: ZERO content drift.** Every body line, data value, token ID, vector,
and percentage on every checked board matches today's page. The two drift cases
caught during the format audits (critical-thinking's Maria callback,
opener-work's bridge copy) were already fixed by their rebuilds, so the
catalogue is content-current everywhere.

Cosmetic, video-side findings (capture-era composition, not drift — low
severity, fix only if strict Rule-1 conformance is wanted; each is a leg swap):

| Video | Finding |
|---|---|
| transformer | 2 video-only board titles ("Two problems the words around a word have to solve", "The two steps inside every layer") — page carries the framing in adjacent prose |
| context-window | video-only headline "Same prompt. Different answers. On purpose." on the Luke/Nate board |
| fake-trap | video-only title "Same clip, two tests" |
| document-trap | video-only title "How AI handles a long document" |
| why-learn-ai | White House quote card shows the cite as a bold header |
| critical-thinking | equation board missing the page's THE EQUATION eyebrow; "Slim by Chocolate! Two reactions" is a video-only composite title |
| does-ai-think | left badge 🧠 vs page 🧑 |
| support-trap | sister-panel icon 👥 vs page 🧑 |
| training | GUESS/CHECK/NUDGE pill hook is video-only (composed hook diagram; compose exemption likely applies) |
| layers | takeaway line placed above cards in video, below on page (layout nuance) |

All other checked boards: exact match, no orphans.

## Exact-parity verdict (owner bar restated 2026-08-05: design + size + word-wrap + content)

Spot-checks against fresh 902px page captures confirm what the capture history
implies: boards from every pre-rule era FAIL exact wrap parity even where
wrapper and words match — welcome's path board wraps "neither are / you" on the
page but "you. Things / to" in the video; training's Pretraining intro is one
line on the page but wraps after "It" in the video. Every board captured before
the BANDW-0/902px rule (2026-08-04) rendered at some other width, so its line
breaks differ from the page by construction.

Bottom line: exact parity currently holds ONLY for the boards rebuilt on
2026-08-04/05 (the ten shipped re-works + the seven pending -v2 candidates).
Bringing the rest of the catalogue to the exact bar means leg-swap rebuilds of
roughly 45-50 remaining board spans across ~20 videos — the same routine
pipeline, batched. The cosmetic findings above (video-only titles, icon
substitutions) resolve automatically in those rebuilds.
