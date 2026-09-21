# Document Trap — seven-way review (2026-09-21)

New candidates: `Prompts/document-trap-5.mp4` (4:04) and `-6.mp4` (3:17), both from 2026-09-21.
Earlier rolls, available as donors: `-1` (4:27) and `-2` (3:37) from 2026-09-18, `-3` (3:42) and `-4`
(2:56) from 2026-09-20. The live video (`course-assets/document-trap/document-trap.mp4`, 3:44) still
dates from 2026-09-08 and has never been replaced. All six rolls came from the 2026-09-18 kit.
Transcripts, scene cuts, holds, and contact sheets in the per-roll folders; word-level transcripts for
rolls 5 and 6 in `words/`.

**Verdict: roll 6 is the base, with three grafts. Neither new roll is clean. Roll 6 is structurally
the best and owns both payoff beats, but it garbles the one word the whole lesson turns on — see
"The six-foul problem" below, which needs David's ear before anything is built. Roll 5 is fuller but
breaks the prompt's conditional-language rule twice, in the middle of otherwise-good sentences, which
is harder to repair than roll 6's missing beats.**

## Hard requirements (from the Markdown and the prompt)

| Requirement | roll 1 | roll 2 | roll 3 | roll 4 | roll 5 | roll 6 | live |
|---|---|---|---|---|---|---|---|
| Closing lines verbatim, in order, nothing after | MET (lead-in "This graphic highlights the definitive rule…") | MISSED ("A single missing passage has the power to change the factual accuracy of an entire answer. Always ask for the source passage, then check it yourself.") | MET, but the engine's "Thank you. Thank you. Bye. Bye." runs 3:41–3:46 after it | MISSED ("can change the **final** answer") | MET (lead-in "Remember,", 236.08–236.28, removable) | MET (lead-in "As this graphic states,", 188.26–189.24, removable) | MET |
| Short file **may** fit in full; long file **may** be searched; never claim a long file is never read in full | MISSED ("a massive 200-page rulebook **cannot** be absorbed all at once"; "The AI itself **never** sees the whole book") | MET | MET ("might fit… but a long file forces the system to search") | MET | **MISSED** ("A short file **fits** in there perfectly… **forcing** the system to hunt", and again at 3:19.9: "rather than a human who has read the whole file cover to cover") | MET-ish ("A short file **might** drop in perfectly. But with a long file, the system **has to** filter") | MISSED (the short-file case is never mentioned) |
| RAG named only after split / search / load is explained | MET | MET | MET | MET | MET | MET | MET |
| Five fouls regular season, six in the tournament section, answer incomplete not invented | MET | MET | MET | MET | MET | MET | MET |
| All four moves named and explained | MET | MET | MET | MET | MET | MET | MISSED ("Ask One Thing" is never named) |
| The moves applied to the rulebook, with the verified six-foul result | MISSED (applied; no verified result) | MISSED | MET | MET (applied; result implied, not stated) | MISSED (applied; no verified result) | **GARBLED** — see below | MISSED |
| No embeddings or vector-database detail | MET | MET | MET | MET | MET | MET | MET |
| Never asks the viewer to pause or work something out | MET | MET | MET | MET | MET | MET | **MISSED** ("Think of a long, complex document in your own life… where missing a hidden exception could cause financial loss") |
| Runtime / cuts | 4:27 / 19 | 3:37 / 20 | 3:42 / 42 | 2:56 / 35 | 4:04 / 27 | 3:17 / 15 | 3:44 / 185 |

Roll 2 is REROLL on the close alone. Roll 1 is REROLL on the never-read-in-full claim, which it makes
three times. Roll 4 is REROLL on the altered closing line. Roll 3 passes every requirement but the
engine outro, and is the strongest of the earlier four — it is the donor of record below. The live
video misses three requirements and is the weakest of the seven.

## The six-foul problem (roll 6, 2:41.7–2:43.4)

Roll 6 is the only new roll that speaks the payoff — the moves applied to the rulebook returning the
verified answer. Three separate decodes of that phrase produce **"the correct sexile limit"**
(base.en, segment and word passes) and **"sex aisle limit"** (small.en); none produce "six-foul".
For comparison, roll 3's equivalent line decodes as "six-fowel" on base.en and cleanly as **"six-foul"**
on small.en, so the models can hear the word when it is said clearly.

That is strong evidence the narrator elides "six-foul" into something that does not read as the word,
and one plausible hearing is badly wrong for a 16-year-old audience. **I cannot listen; this is the
one check that decides the build.** The clip is at
`video-audit/document-trap-comparison-2026-09-21/document-trap-6-sixfoul-check.wav` (roll 6, 2:36–2:44), with roll 3's clean version beside it as `document-trap-3-sixfoul-reference.wav`.

If it sounds wrong, graft 3 below replaces the whole sentence. If it sounds fine, drop graft 3 and
build with two.

## Beat table: rolls 5 and 6

| Teaching point | roll 5 | roll 6 |
|---|---|---|
| Rulebook story: upload, the five-foul answer, last year's memory, the tournament section | RICH | RICH |
| Not invented, incomplete | RICH ("didn't make up the five foul limit… pulled the standard rule exactly as written") | RICH ("Its answer wasn't made up, just incomplete") |
| Definition: uploaded is not fully read | TAUGHT ("We assume that uploading a file means the AI has read every single word") | TAUGHT ("…has fully read and comprehended every single word inside it") |
| Short file may fit; long file may be searched | **WRONG** (both conditionals dropped) | TAUGHT |
| Split / Search / Load, all three explained | RICH | RICH |
| Search decides which parts reach the answer | RICH, but "Notice the banner at the bottom" | RICH ("Search acts as a strict gatekeeper") |
| The rulebook mistake replayed through the pipeline | RICH | RICH |
| RAG named and expanded | RICH | RICH |
| The same process pulls from the web or a database | **MISSING** | RICH (1:43–1:48) |
| Retrieval hits: a specific question answered in seconds | RICH (2:04.6) | **MISSING** — only the failure half is taught |
| Four moves named and explained | RICH | RICH (compressed) |
| Board 3 takeaway: make the right passages easier to find | RICH (3:02.0–3:07.8) | **MISSING** |
| Moves applied: "Look in the tournament section… Quote the rule and any exceptions." | TAUGHT (moves 1 and 2 applied; the prompt is not spoken) | RICH (the Markdown's prompt spoken in full, 2:31–2:37) |
| The verified six-foul result | **MISSING** | GARBLED (see above) |
| A quotation is useful because you can check it, not because AI quoted it | RICH | RICH |
| Leases, employment contracts, insurance policies, financial-aid letters | TAUGHT (financial aid dropped) | TAUGHT (financial aid dropped) |
| Uploading is a good starting point | RICH | RICH |
| Close | MET | MET |

Roll 6 wins the structure and both payoff beats; roll 5 wins coverage. The deciding difference is the
kind of defect: roll 6's are absent beats, which graft cleanly from identified donors, while roll 5's
are wrong statements inside sentences that are otherwise worth keeping, which would need sentence
replacement in two places plus the same missing-beat grafts.

## Per-roll block: document-trap-6 (BASE)

```text
LESSON: document-trap
CANDIDATE: Prompts/document-trap-6.mp4 (3:17.43, 30 fps, 15 cuts)
VERDICT: REPAIR (three identified grafts; KEEP on every other beat)
TEACHING POINTS: all RICH or TAUGHT except the retrieval-hit half (MISSING), Board 3's takeaway
  (MISSING), and the verified six-foul result (GARBLED)
HARD REQUIREMENTS: all MET except the six-foul payoff. Close: "A missing passage can change the
  answer." 3:09.7–3:11.7 and "Ask for the passage, then check it." 3:12.3–3:14.1, 0.41 s apart,
  last word 3:14.1, nothing after (3.4 s of silence to 3:17.4)
ERRORS: none factual; "has to filter" softens the lesson's "may search" but does not contradict it
SOURCE_QA: PASS
ADDITIONS: "comprehended" in the definition; "actively engineering a precise retrieval" (register
  drift, harmless)
REPAIR PLAN: three grafts, all whole sentences between silences (see below)
EDITING NOTES: Notebook renders Board 2 and Board 3 itself and re-typesets their text; the canonical
  JPGs replace those spans. Board 1 is post-only. Roll 6 draws its own "UPLOADED ≠ FULLY READ" card at
  0:44, which the canonical Board 1 replaces. Basketball players at 0:20–0:26 are Notebook drawings,
  not photographs. Corner mark on every frame. Screen references to cut or cover: "This breaks down
  the workflow" (1:06) and the close lead-in.
LISTENING: transcripts read in full and every graft boundary measured; audio not auditioned. The
  six-foul phrase at 2:41.7 is the blocking check.
```

## Graft plan (all verified as whole beats between silences)

| # | Into roll 6 at | From | Words | Boundaries |
|---|---|---|---|---|
| 1 | at 1:48, before roll 6's retrieval-miss sentence | roll 3, 2:01.09–2:03.71 | "When the retrieval step finds the right passages, the AI can answer your question in seconds." | 0.33 s / 0.23 s |
| 2 | after the fourth move (2:21) | roll 5, 3:02.06–3:07.50 | "The ultimate goal of all four moves is simply to make the correct passages easier to find." | 0.80 s / 0.40 s |
| 3 | replacing roll 6's 2:38.1–2:43.4 | roll 3, 2:41.98–2:50.75 | "By applying these precise moves, you force the system to look past the standard rules and uncover the verified six-foul tournament exception." | 0.57 s / 0.50 s |

Narrator pitch sits in a 167–191 Hz band across rolls 1, 3, 4, 5 and 6, consistent with one Notebook
voice, but the voice match on each graft is an ear judgement.

Graft 3 is a replacement, not an insert: roll 6's own sentence goes out and roll 3's comes in. It runs
8.8 s against roll 6's 5.3 s, so the span lengthens by 3.5 s. With all three grafts the candidate lands
near 3:30.

## Not grafted

- Roll 5's "Notice the banner at the bottom" and roll 1's "This infographic shows…" are screen
  references we would be cutting, not importing.
- Financial-aid letters are dropped from the examples list in both new rolls. Rolls 3 and 4 have the
  full list; it is one noun and not worth a seam. Flagged for David's call.

## Listening checks for David

1. **Roll 6, 2:38–2:44** — the six-foul phrase. This decides whether graft 3 is needed.
2. Roll 6, 3:08.3–3:09.2 — "As this graphic states," before the close; cleanly removable (0.49 s and
   0.38 s of silence around it).
3. Each graft boundary once built.

## Next step

Nothing is built. On a verdict for the six-foul phrase and approval of the graft plan, the build is
roll 6 as the spine with those grafts, the post-only Board 1 over the rulebook story, canonical
Boards 2 and 3 replacing Notebook's renders with card rings and banner rings, and the standard close.
