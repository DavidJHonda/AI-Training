# Document Trap — the 2026-09-21 reroll (rolls 7 and 8)

`Prompts/document-trap-7.mp4` (3:18.70, 36 cuts) and `-8.mp4` (3:28.90, 32 cuts), the first rolls from
the kit David rebuilt on the 2026-09-20 recipe — VOICE block, ten required-verbatim lines, beat spine,
Board 1 uploaded as a faceless variant. Rolls 1-6 (2026-09-18 and -20, both on the older kit) and the
live video are the donor pool; their bundles are in `video-audit/document-trap-comparison-2026-09-21/`.

**Verdict: REROLL, both. Each roll speaks seven of the ten required lines and misses the same three —
and so does every one of the six earlier rolls, so there is no donor to repair from. The three
failures are consecutive, they are the whole definition beat, and the rebuilt Markdown is the reason:
it demoted exactly those lines out of their own lines and out of bold. Fix the Markdown's layout
before rolling again.**

## The ten required lines

| # | Line | roll 7 | roll 8 |
|---|---|---|---|
| 1 | "How many fouls until I'm out of the game?" | MET 0:09.7 | MET 0:10.9 |
| 2 | "Five fouls and you foul out." | MET 0:13.2 | MET 0:15.0 |
| 3 | "The answer wasn't made up. It was incomplete." | **MISSED** — "This is an incomplete answer." | **MISSED** — "The AI provided a factually accurate answer based on one part of the text, but its search stopped short of the full picture." |
| 4 | "Document Trap is thinking 'uploaded' means 'fully read.'" | **MISSED** — "The document trap occurs when we assume uploaded means fully read." | **MISSED** — "This is the document trap. We tend to assume that uploading a file means the AI has fully read it." |
| 5 | "Uploading a file doesn't mean AI has read it all." | **MISSED by one word** — "doesn't mean **the** AI has read it all" | **MISSED** — absent; Board 1's content is never taught |
| 6 | "Search decides which parts reach the answer." | MET 1:32.6 | MET 1:37.6 |
| 7 | "Look in the tournament section. How many personal fouls are allowed? Quote the rule and any exceptions." | MET 2:24.0 | MET 2:28.9 |
| 8 | "A quotation is useful because you can check it, not because AI quoted it." | MET 2:48.1 | MET 2:55.4 |
| 9 | "A missing passage can change the answer." | MET 3:10.8 | MET 3:21.2 |
| 10 | "Ask for the passage. Then check it." | MET 3:13.3 | MET 3:23.8 |

Every quoted wording above was confirmed on a second decode with the `small.en` model, not just the
segment pass.

## Why those three, and what to change

Look at where the ten lines sit in `lessons/document-trap.md`:

- The seven that land are each **visually isolated**: dialogue inside quotation marks (1, 2, 7), or a
  sentence alone on its own line (6, 9, 10). Line 8 is the single exception — it ends a paragraph and
  still lands, probably because it is a distinctive aphorism.
- The three that fail are **buried in running prose**. Line 3 sits third and fourth in a four-sentence
  paragraph. Line 4 ends that same paragraph. Line 5 is the second sentence of Board 1's two-sentence
  teaching block.

That is not how they used to be laid out. Comparing the rebuilt Markdown against the committed version:

| Line | Before the rebuild | After |
|---|---|---|
| 4, the definition | `**Document Trap is thinking 'uploaded' means 'fully read.'**` — bold | same sentence, **bold removed** |
| 5, Board 1's banner | on its own line, and repeated as `**Takeaway:** Uploading a file doesn't mean AI has read it all.` | second sentence of a two-sentence block, **no takeaway line** |
| 6, Board 2's banner | `**Takeaway:** Search decides which parts reach the answer.` | on its own line — still isolated, **and it still lands** |

So the rebuild removed the visual emphasis from exactly the two lines that now fail, and kept it on the
one beside them that still works. The required-verbatim list alone is not carrying them.

**Suggested change before rolling again:** put lines 3, 4 and 5 on their own lines, and restore the
definition to bold, so they are laid out the way lines 6, 9 and 10 are. That costs nothing on the page —
the Markdown is an upload source, not the lesson — and it is the one variable that separates the lines
that land from the lines that do not.

## Everything else, beat by beat

| Teaching point | roll 7 | roll 8 |
|---|---|---|
| Rulebook story: tournament next week, the 200-page upload, the question, the five-foul answer | RICH | RICH |
| Last year's memory; five in the regular season, six in the tournament section near the end | RICH | RICH |
| The AI pulled the standard limit and missed the exception | RICH | RICH |
| Short file **may** fit in full; long file **may** be searched | **WRONG** — "A short file easily fits in full… the system **has to** search" | **WRONG** — "A short document fits perfectly, but a long file… **is too big**. The system **must** search" |
| Board 1's content (the retrieval machine leaving the exception out) | RICH | **MISSING** |
| Split / Search / Load, each explained | RICH | RICH |
| How the rulebook mistake happens through that process | RICH | RICH |
| RAG named after the process; web or database | RICH | RICH |
| Retrieval hits: a specific question answered in seconds | RICH | **MISSING** — only the failure half |
| Retrieval misses: AI **may** miss it too | TAUGHT ("misses it too") | TAUGHT, hardened ("will **inevitably** miss it too") |
| Four moves, each named **with its explanation** | **THIN** — names them, but only "name the section" and "ask one thing" get a reason, and they are introduced together | RICH — all four named and explained separately |
| Applied: naming the section gives a specific target | RICH | RICH |
| Applied: asking one thing keeps it focused | **MISSING** | RICH |
| Paste the passage; ask for the quote; compare with the original | RICH | RICH |
| The six-foul result | **MISSING** | **MISSING** |
| Leases, contracts, insurance policies, financial-aid letters | RICH | RICH |
| Uploading and asking is a good starting point | TAUGHT ("**only** a good starting point") | TAUGHT ("a **fantastic** starting point, but you must always verify") |
| Close, nothing after | MET | MET |

Neither roll is a base the other can patch: roll 7 owns Board 1 and the retrieval-hit half, roll 8 owns
the four-move explanations and the second applied "why", and **both** miss the three verbatim lines, the
conditional wording and the six-foul result. A best-of would still fail five hard requirements.

## Two smaller notes for the next roll

- **The six-foul result has never landed.** No roll in eight has said, after applying the moves, that
  the tournament rule allows six. It is one sentence in the Markdown ("In this example, the tournament
  rule allows six fouls.") sitting mid-paragraph — the same shape as the three failing lines. Consider
  adding it to the verbatim list and giving it its own line.
- **Roll 8 draws a person.** A basketball player appears 0:20-0:24, against "Between boards use simple
  drawn scenes with no people." Roll 7 keeps to objects and panels throughout. Not a narration issue;
  noted because the instruction is new in this kit and only one roll honoured it.

## What is good

The new kit is clearly working on everything except that one beat. Both rolls open cold with no title
card, keep to the lesson's vocabulary — no embeddings, vector, chunk, semantic, pipeline, algorithm —
never ask the viewer to pause or guess, teach split/search/load properly, name RAG only after the
process, and land the close exactly with nothing after it. Roll 7's visuals are drawn, people-free and
on-message throughout. That is a much better starting point than the 9/18 and 9/20 rolls.

## Next step — materials changed 2026-09-21, ready to reroll

Applied on David's instruction:

- `lessons/document-trap.md` — the three failing lines now stand alone on their own lines, the
  definition is back in bold, and Board 1's banner is its own line again. The six-foul result gets its
  own line too. The context-window paragraph is split so "A short file may fit there in full." and
  "With a long file, the system may search…" each sit alone, rather than being the second and third
  sentences of a paragraph. Verified: all eleven required lines are now either quoted dialogue or alone
  on their own line — the two shapes every line that lands already had.
- `Prompts/document-trap-video-prompt.txt` — "In this example, the tournament rule allows six fouls."
  added as an eleventh required line; the verbatim preamble now names the layout ("Each stands alone on
  its own line in the Markdown"); the conditional instruction now names the hardenings to avoid ("has
  to", "must", "is too big"). Trimmed elsewhere to 499 words, inside the kit's under-500 guide.
- `gemini-notebook/document-trap/` restaged and the checklist regenerated; registry note and the kit
  entry record the revision.

The live video (2026-09-08) stays until a roll passes.
