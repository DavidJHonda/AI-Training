# Build Your Skills: live-video narration reviews (2026-09-24)

Evaluate-first pass over the eight shipped videos (Where's the Line? excluded: shipped 2026-09-23 on the
current recipe). Each lesson was reviewed in its own fresh session under `scripts/video/NARRATION-REVIEW.md`
against the VISIBLE page text of `index.html` (hidden `md-source` blocks excluded), the upload Markdown, the
current boards, and the prompt's verbatim list. Bundles (base.en transcript, scenes, holds, contact sheets)
plus a `REVIEW.md` live in `video-audit/<slug>-live-review-2026-09-24/`. Contested lines were re-transcribed
with medium.en; no audio was listened to by a person.

| Lesson | Runtime | Verdict | Points R/T/Th/M/W | Hard reqs | Source QA | Deciding finding |
|---|---|---|---|---|---|---|
| Opener | 2:29 | **REROLL** | 2/20/0/4/0 | 7/11 | PASS (kit gap) | Map row 2 never taught; creed and keep-in-mind question paraphrased, no donor |
| Your Choices | 3:00 | **REROLL** (narrow) | 18/7/1/1/0 | 8/10 | PASS | "depending on the app and your subscription" spoken without "the app and" (0:11); framing sentence never spoken |
| Next Level Moves | 3:15 | **REROLL** | 4/22/8/3/0 | 11/18 | PASS | Profit example loses its numbers; Learn With AI method one clause; conversations summarized, not read |
| Honesty & Privacy | 4:00 | **KEEP** | 27/10/1/2/0 | 10/10 | PASS | Best-practices board fully narrated; privacy lists trimmed (not essential) |
| People Skills | 2:53 | **KEEP** | 16/2/0/0/0 | 7/7 | PASS | Four Ways board fully narrated 1:44-2:30 |
| Creative Thinking | 2:54 | **REROLL** or one-cut REPAIR | 16/5/0/0/0 | 7/9 | **FAIL** (page) | Video matches the page; page still carries the 2026-09-12 "similar answers" sentence the 9/18 materials removed |
| Curious & Flexible | 3:36 | **KEEP** | 9/7/0/0/0 | 9/9 | PASS | One line MET by paraphrase ("Newer is not automatically better"), owner to confirm |
| Make Your Move | 5:29 | **KEEP** | 14/12/0/0/0 | 2/2 | PASS | Note spoken in full (third person); "may help" hedge dropped on careers, distinction intact |

## Owner decisions needed

1. **Creative Thinking page fix.** `index.html` (line ~9494 at review time) still says everyone using the same AI
   gets similar answers. The Markdown and prompt were revised 2026-09-18 to forbid that claim. Fix the page
   first. Then either (a) cut 1:37.44-1:43.10 from the live file (both ends in measured silence) and re-review
   for KEEP, or (b) reroll on the current recipe to get the new verbatim line spoken.
2. **Your Choices.** The only hard miss is four words. Under the Fake Trap precedent (two lines taught in
   meaning, shipped anyway) this can be a KEEP by owner call; otherwise it needs a reroll.
3. **Curious & Flexible.** Confirm that the paraphrase of "Newer is not automatically better" passes.
4. **Honesty & Privacy.** Confirm the trimmed privacy list items (preferences, medication, family situations,
   identification numbers, other people's; "read by people at the AI company", "handed over if the law
   requires it") are not essential. If they are, this becomes a reroll.

## Rerolls: kits to rebuild on the 2026-09-20 recipe

Opener, Next Level Moves, and (pending decision) Your Choices and Creative Thinking. Procedure:
`Prompts/README.md` "Prepare a new lesson"; add each to `Prompts/upload-sets.json`; run
`scripts/video/sync_gemini_notebook.py --lesson <slug>` to stage `gemini-notebook/<slug>/`.
Kit notes from the reviews:
- Opener: add the roadmap sentence and the map title "Build Your Skills" as spoken lines; every map row in the verbatim list.
- Next Level Moves: profit numbers (10 x $30, $120 labor, $30 gas/supplies, $150 profit) and the Learn With AI
  steps in the verbatim list; require conversation turns and Board 4's four questions to be read; name
  Think/Learn/Start/Iterate at their examples.
- Make Your Move / People Skills / Honesty & Privacy kits still carry the old "post-production only / reserve
  narration" labels; refresh only if those lessons ever reroll.
- Comparing new rolls: the live file is a donor candidate in every case (beat-by-beat table, best-of plan).

## Editing-only notes (do not affect verdicts)

- Curious & Flexible: hold board full view over 1:54-2:06 (gibberish email mock-up) and 3:09-3:26 (illegible diagram).
- People Skills: optional hold of the Four Ways board through the "AI can suggest" takeaway.
- Make Your Move: optional 7.7 s trim at 0:28.16-0:35.90; earlier board arrivals for Skills and Moves.
- Creative Thinking: 0:35-0:46 photographic Macintosh still; "Identical Outputs (Zero Variance)" drawing under the cut sentence.
- Opener: close still uses the pre-2026-09-15 close capture.
