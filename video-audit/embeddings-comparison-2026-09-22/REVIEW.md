# Embeddings — rolls 1 and 2 against the live video (2026-09-22)

Three files reviewed end to end against the current lesson (`lessons/embeddings.md`, the kit's stated
teaching authority, committed) and `Prompts/embeddings-video-prompt.txt` (rebuilt 2026-09-22 12:42; both
rolls were generated after it): `Prompts/embeddings-1.mp4` (5:13), `Prompts/embeddings-2.mp4` (4:04),
and the live `embeddings.mp4` (3:57). Bundles for all three are in this folder.

**Verdict: roll 1 is the base — REPAIR, and it is a long way ahead. Roll 2 is a REROLL. The live video
is the weakest of the three on completeness and should be replaced whichever way this goes.**

This kit is the most tightly specified in the course: eight required verbatim lines, a fixed definition
order, a long list of exact numbers, and explicit prohibitions. That makes the comparison unusually
clear-cut.

## The eight required verbatim lines

| # | Line | roll 1 | roll 2 | live |
|---|---|---|---|---|
| 1 | "An ID identifies you. It doesn't describe you." | **MET** | **MET** | missed |
| 2 | "Each position always means the same thing. The number says how much." | **MET** | half — drops "The number says how much." | missed |
| 3 | "The whole row of numbers is a vector." | **MET** | "In math, this row of numbers is a vector" | "In data science, this entire row…" |
| 4 | "Six numbers match. The seventh tells them apart." | **MET** | **MET** | missed |
| 5 | "That row is called an embedding." | **MET** | **MET** | "In AI, this complete row… is called an embedding" |
| 6 | "Both use a row of numbers to describe something." | **MET** | **MET** | missed |
| 7 | "AI uses numbers to work with meaning." | **MET** | **MISSED** | **MET** |
| 8 | "Those numbers help AI recognize similarities and differences." | **MET** | **MISSED** | **MET** |
| | **Total** | **8 / 8** | **4 / 8** | **2 / 8** |

## The numbers

The prompt says "Speak both drinks' six scores." Only roll 1 does.

| | roll 1 | roll 2 | live |
|---|---|---|---|
| Badges 1024, 2048, 3072, 4096 | all four | all four | **only 1024 and 2048** |
| Coke's six scores (9,1,10,2,3,8) | **all six** | only 9, 1, 10 | **only 9 and 10** |
| Coffee's six scores (1,9,0,9,8,10) | **all six** | only 1, 9, 0 | **only 9 and 8** |
| Citrus: Coke 1, Pepsi 10, coffee 0 | all three | all three | coffee's 0 missing |
| cat's ID 4719 | yes | yes | yes |
| cat's row 0.45, −0.23, 0.80, 0.17 … −0.35 | **all five, "negative" spoken** | all five | **entirely missing** |

## LESSON: embeddings · CANDIDATE: `Prompts/embeddings-1.mp4` (5:13)

**VERDICT: REPAIR** — every hard requirement met; the gaps are completeness, not accuracy.

- **All eight verbatim lines, all the numbers, and the definition order** (vector @2:03 → dimension and
  value @2:08) are correct.
- Content prohibitions all respected: it never says a token ID carries meaning, never calls AI's
  dimensions named traits, never names a model, adds no distance or similarity math, does not narrate the
  club activity, and uses none of the banned words.
- The 9-for-Sweet question is asked and **answered at once** ("you immediately know the answer. It's Coke.").

Gaps:
- **Board 4's rows 4 and 5 are compressed into one sentence** @3:37 ("these values don't have human labels,
  like sweet or fizz. They simply capture patterns in how a token is used in data"). The prompt asks for
  all five comparison rows, both sides; the taste-test side of "what they capture" and "you name them" is
  not spoken.
- **The other tokens are never named.** The lesson has cat's row sitting alongside dog, latte, truck,
  bicycle and map; roll 1 skips them.
- **"A value is one learned number… also called a parameter"** loses its first half: roll 1 says only that
  the number "is called a parameter", and omits "the circled 0.45".
- **The lesson's prose list is missing** — "whether you are funny, into hockey, or the person who steals
  fries at lunch."
- **Four board-furniture phrases**, which the prompt bans outright: "Look at this illustration of four
  students…" @0:23, "This table captures our ratings…" @1:22, "This updated table shows…" @2:24, "This
  comparison chart maps…" @3:01.
- Voice drift beyond the lesson's plain register: "In formal AI terminology", "master ledger", "model
  architecture", "complex decimals", "an organizational tool". None are on the banned list, but the kit
  asks for the Markdown's own voice.
- Calls un / belie / vable "syllables"; the lesson calls them tokens or pieces.

## CANDIDATE: `Prompts/embeddings-2.mp4` (4:04)

**VERDICT: REROLL.** Two failures are disqualifying on their own.

- **Both closing lines are missing.** It ends on an invented summary — "By translating meaning into
  mathematics, models can instantly identify how concepts are alike and how they differ." The prompt says
  to end on the two closing lines, in order, with nothing after.
- **Only three of six scores for each drink**, against an explicit instruction to speak all six.
- Drops "The number says how much." and rewrites the vector line as "In math, this row of numbers is a
  vector."
- **"This graphic shows what that looks like inside an actual model"** @2:43 — the exact construction the
  prompt forbids — plus "The main board is the embedding table" @2:56, naming a production label.
- Adds a mathematical register the lesson does not use: "Mathematically", "complex mathematical patterns",
  "Characteristics become math."

What it owns, and roll 1 does not:
- **Board 4's rows 4 and 5, both sides** @2:19–2:36: "We explicitly named our traits, like sweet or fizz.
  An AI has no dimension labels at all. It simply captures complex mathematical patterns based on how a
  token is used, and those unlabeled values work together."
- **The other tokens** @2:58: "cat sits right alongside rows for dog, latte, truck, and bicycle" (map missing).
- **"the circled .45"** @3:30.
- Identifies the fry-stealer as **student 3072**, which I checked against the canonical board: it is
  correct. Roll 2 was generated from the faceless variant, which does not show it, so this is a lucky
  inference rather than a sourced fact — but it is not an error.

## The live video

Weakest of the three on completeness, and it should be replaced regardless:
- **2 of 8 verbatim lines.**
- **Two of six scores** for each drink; only two of the four badge numbers; coffee's Citrus 0 missing.
- **Cat's row values are never read** — the board's whole payload.
- Board 5's first two columns are never named; the other tokens are never named.
- **"It typically utilizes thousands…"** — "utilize" is on the kit's banned-word list.
- Describes Board 1 as "four student ID cards" rather than four students at a table, and never puts the
  fry-stealer on the board.

It does have one thing neither roll does: the lesson's prose list, @0:31 — "if that person is funny,
plays hockey, or steals fries at lunch."

## BEST-OF PLAN: embeddings

```
BASE: Prompts/embeddings-1.mp4 — 8/8 verbatim lines, every number correct, definition order correct,
      every content prohibition respected.

  Board 4, rows 4 and 5, both sides
      roll 1 compressed @3:37 | roll 2 RICH @2:19-2:36 (but says "complex mathematical patterns")
      — TAKE roll 2, under Board 4

  cat's row sits alongside other tokens
      roll 1 MISSING | roll 2 TAUGHT @2:58 (dog, latte, truck, bicycle; map missing) | live MISSING
      — TAKE roll 2, under Board 5

  "the circled 0.45"
      roll 1 says "like that 0.45" | roll 2 says "like the circled .45"
      — OPTIONAL, same sentence as above; low value on its own

  "funny, into hockey, or steals fries at lunch"
      roll 1 MISSING | roll 2 MISSING | live TAUGHT @0:31
      — DAVID'S CALL: the only donor is the live video, and it is the widest floor step of the three.

GRAFTS: 2 planned, both under boards; a third offered.
```

**Feasibility, with a caveat worth reading.** Loudness is close — roll 1 −15.28 LUFS, roll 2 −16.66, live
−15.72, all within 1.4 LU. **But roll 1's noise floor is −56.4 dB against roll 2's −62.8 and the live's
−63.1** — roll 1 is the noisiest of the three by 6–7 dB. Every graft into it therefore steps *down* into a
quieter room and back *up* on the way out. That is well short of the 17 dB cliff that disqualified roll 3
as an audio donor on Engagement Trap, and the down-then-up direction is the less audible one, but it is
the largest floor mismatch in an otherwise-viable set and it will not be invisible. Short grafts landing
under a board are the safer shape; exact in/out frames measured against each donor's own waveform at
build time.

## Editing notes for whichever version is built

- **The board-furniture phrases are in all three rolls**, and the prompt bans them. Two of roll 1's four
  are standalone sentences that could be cut ("This table captures our ratings for the two drinks.",
  "This comparison chart maps…"); the other two carry teaching content and cannot be removed cleanly.
- **"vable" versus "fable" is acoustically ambiguous in both rolls.** Under prompt biasing both flip
  either way; roll 1's unbiased decode lands on "Vable" and roll 2's on "fable". Worth David's ear rather
  than a claim from me — the /v/–/f/ distinction is genuinely hard here.
- No title cards in any of the three; all open straight into content, as the prompt requires.
- Roll 2's opening drawn scene labels a token "Apple" with ID 4092 — not in the lesson, not narrated.

## Nothing built

No candidate was produced. The live video, rolls, lesson and boards are unchanged.
