# Why-carrying board retrofit — 2026-07-26

Proven on `layers` the same day: teaches-vs-recites went 10 → 13/15 (catalog best)
when the lesson's why moved from prose onto a board whose rows ARE the reasons.
The engine walks boards reliably (board-content is the catalog's best dimension at
88.9%), so a reason-carrying board points its most dependable behavior at the
explanation. Named prompt bans, by contrast, have failed four batches running.

**Design test:** cover the title and read one row aloud. Have you taught anything?
"Shallow meaning" is a label. "Enough to settle the plain sense of a sentence" is
a reason.

**Selection rule:** only build where the lesson has a genuinely *unboarded*
explanatory passage. A low teaches-vs-recites score is the symptom, not the
diagnosis — several low-teach lessons are already fully boarded and their problem
is register, which no board fixes.

## Shipped this pass

| Lesson | New board | Source passage | Note |
|---|---|---|---|
| layers | `layers-3-why-dozens` | "Why are there dozens of layers?" | **rolled, 79 → 85, teach 13/15** |
| transformer | `transformer-4-payoff` | "Now let's answer the two questions we left open" | **capture only — the board already existed on the page and had never been captured into the kit.** Both rolls dropped or compressed this beat. |
| how-an-llm-works | `how-an-llm-works-5-myths` | the three myths `<ul>` | close board carries the three labels; this carries their reasons |
| hallucination | `hallucination-3-rag` | the RAG section | why it helps / why it isn't enough / and it still happens |
| questions-matter | `questions-matter-2-value` | "It changes where value lives" | finding the answer vs asking the question |
| training-bias | `training-bias-2-stale` | "Stale information" | what happens / why it isn't a hallucination / the fix |

Each one: component added to `index.html` (styled to the lesson's existing box
language), board captured 2x, close board renumbered, `board-specs.tsv` row added,
`.md` + `.pdf` re-exported, prompt updated with a hold-and-walk directive ending
"Speak the reason on each card, never just its heading."

**`training-bias` prompt written 2026-07-26** (4,939 chars) — its kit is now
complete and roll-ready: 3 boards + `.md` + prompt. Deduct-targeted from the
sheet's r3 row (79: cov 16 / mat 12 / teach 11 / brd 9 / cln 14 / pace 17), so
rule 7 is hardened against the named cleanliness defect — **style-prompt
leakage**, where the engine lettered "FINELINER WITH ALCOHOL-MARKER" and "ANALOG
TEXTURE AND ANNOTATINES" into the artwork at 0:20, 2:24 and 3:28 — and rule 6
targets the two gibberish spans (0:17 laptop, 1:34 fake whiteboard) by requiring
props to show shapes, not lettering. Rule 5 is the numbers-free ban with the
lesson's only two figures whitelisted (180 mph, four mechanisms), aimed at the
invented-accuracy-rate risk the cow study invites.

**Sizing technique worth reusing.** First draft ran 5,875 against the 5,000
ceiling. What got it under was *not* trimming rules — it was cutting the
restatement of each board's rows out of the body. The board already carries those
reasons verbatim, and so does the attached `.md`, so the prompt only has to force
the walk: name the rows in order, then "speaking the reason written under each
one, in the board's own words. Never read the four names and move on." That
freed ~560 chars and lost nothing, because the asset is doing the work.

## Audited and declined

- **welcome — wrong shape.** "WHY WE BUILT THIS" is Luke and Nate's origin story,
  not explanation. Carding it would flatten the voice, and the lesson already has
  a why-go-deeper board.
- **learn-with-ai — already covered.** The study-tools board carries Best use /
  The catch per tool, which is already reason-carrying. "Start here" is two short
  sentences; a board there would be thin.
- **does-school-matter — already covered.** The two-skills board's rows already
  carry their reasons. Its video's problem is register drift, not a missing board.
- **opener-avoid, opener-understand, opener-work — openers are section maps.**
  The rip-current and car-engine analogies are narrative, and both already have
  their own board.
- **critical-thinking (5 boards), evaluate-the-results (4), support-trap (4),
  flattery-trap (4), what-is-ai (4), document-trap (3)** — no unboarded
  explanatory section found.
- **ai-is-different, why-learn-ai, does-ai-think, tokens, vector-space — no kit
  boards on disk at all.** These need a kit built, not a board retrofitted;
  different job, and vector-space is already the catalog's best teacher at 13/15.

## Verify gate used on every one

JS syntax check → `validate()` clean at 57 lessons → the new card headings confirmed
present in the rendered lesson page over http → board jpg eyeballed at full size.
`design-check.sh` shows em-dashes 8 vs baseline 7, which is **pre-existing on HEAD**
and not from this work.
