# Data Centers — rolls 1 and 2 (reviewed 2026-09-24)

Two rolls on the 2026-09-23 kit (`Prompts/data-centers-1.mp4`, `-2.mp4`). Reviewed under
NARRATION-REVIEW against `lessons/data-centers.md` (matches the live page) and the seven required
lines. Transcripts (faster-whisper base.en), scenes, holds and sheets are in the roll subfolders;
`live/transcript.txt` is the shipped 2026-09-05 video, transcribed as a possible donor. Findings
come from the transcripts and contact sheets. The audio has not been listened to.

## Verdicts

| | Roll 1 (4:40.0) | Roll 2 (3:57.4) |
|---|---|---|
| Structure | **Two passes**: a full lesson 0:00–3:17 ending on the close, then a second take of Responses → close 3:17–4:37 | Single pass |
| Verbatim lines | 7/7 (banner line exact only in the 2nd pass, 3:46–3:52) | 0/7 (the close says "what is"; compute, ChatGPT, somebody-pays, banner and no-guilt lines are all reworded) |
| Board 2 (neighbors) | Wrong numbers ×3, noise thin | Wrong water number, electricity thin, noise thin |
| Voice | "massive" ×5, "sheer scale", "environment" (2nd pass) | "environmental" (banned), "microscopic", "monumental", "commanding", "comprehends" |
| Pictures | Warm sketch + Notebook diagrams; invented figures (10,000+ units, 100+ MW, 4× surge, 65%, 10²¹); a mid-video close card at 3:12; seated figure 3:08; Gemini card 4:40 | Same style; invented GW/TWh/J-per-query/+260% and "Profit $45.2M"; **drawn people with faces** 3:40, 3:48; blank frames 0:00, 1:24; Gemini card 3:56 |
| **Verdict** | **REROLL** (best base if you'd rather repair; see below) | **REROLL** |

The deciding problem is shared: **neither roll teaches the neighbors board correctly**, and it's
the lesson's core. Both squash four paragraphs into four one-liners, and the numbers break when
they're squashed.

## Beat by beat

| Beat | Roll 1 | Roll 2 | Better |
|---|---|---|---|
| Hook: type, send | RICH 0:00 | RICH 0:00 | tie |
| Math assumption | RICH 0:12–0:40. Says "each new word" where the lesson says token; adds "that single word takes two trillion calculations" (a useful step) | RICH 0:16–0:39 "each new word, or token" | tie; 2 is more precise, 1 is clearer |
| Compute (verbatim) | **MET** 0:40 | MISSED 0:39 "The industry has a specific name… It is called Compute." | 1 |
| Millions of people / more data centers | TAUGHT 0:43 | TAUGHT 0:46 | tie |
| Warehouse of GPUs, around the clock | RICH 0:57 | RICH 1:00 | tie |
| Board 1 | TAUGHT 1:04 "This image shows the inside…" (production phrase) | RICH 1:07 "This is the inside of an AI data center." | 2 |
| Football fields / small city | TAUGHT 1:19 | TAUGHT 1:23 | tie |
| Scale varies by facility | MISSING | MISSING | none |
| ChatGPT line (verbatim) | **MET** 1:30 | MISSED 1:35 "When you hit send on your computer, this is the physical machine that answers." | 1 |
| Somebody pays (verbatim) | **MET** 1:35 | MISSED 1:45 "and somebody has to pay for it" | 1 |
| Affects communities | TAUGHT 1:37 | TAUGHT 1:47 | tie |
| Electricity | **WRONG** 1:47 "4.4%… in 2023, projecting 12% by 2028, raising local bills": no Berkeley Lab; gives the top of the range as the projection | **WRONG/THIN** 1:59 "projected up to 12% by 2028 raises household bills": no 4.4%, no 2023, no 6.7 | neither |
| Water | **WRONG** 1:57 "evaporate up to a million gallons of water daily"; no hot day, no recycling | **WRONG** 2:06 "consumes a million gallons of water daily"; same errors | neither |
| Noise | THIN 2:02 "Constant fan noise disrupts neighbors." | THIN 2:09 "24-7 fan noise causes lawsuits." | 2 |
| Permanent jobs | **WRONG** 2:05 "around 100 permanent jobs"; no supermarket | TAUGHT 2:13 "only provide 100 to 200 permanent jobs"; no supermarket, no construction | 2 |
| Three responses | 2nd pass TAUGHT 3:17–3:43 (says "fresh water drawn from the environment") | TAUGHT 2:30–2:50 | tie |
| Banner (verbatim) | 1st pass "…demand, while better…" MISSED; **2nd pass MET 3:46–3:52** | MISSED 2:50 (reworded) | 1 (2nd pass) |
| Efficiency ≠ smaller total | 2nd pass RICH 3:52–4:05 | TAUGHT 3:00, but says "environmental" (banned) | 1 |
| One request is small | TAUGHT 4:05 | TAUGHT 3:18 | tie |
| Every tech has a footprint | TAUGHT 4:19 "Like streaming video or daily commutes…" | MISSING | 1 |
| Who pays: dollars, watts, water, quiet | THIN and misplaced 2:10 (before Responses, no "company in dollars") | **RICH** 3:29 "paid for by the company in dollars, the grid in watts, and the local neighborhood in water and quiet" | 2 |
| No-guilt line (verbatim) + reason | **MET** 4:25; reason TAUGHT 4:28 | MISSED 3:36 (reworded); reason TAUGHT 3:41 | 1 |
| Close (verbatim ×2) | **MET** 4:32–4:37 | line 2 MISSED 3:49–3:54 "what is behind the magic" (medium.en, corrected in the roll 3–4 pass) | 1 |

## Why a repair doesn't meet the bar

Roll 1's duplicate is easy to fix. "Technology companies recognize these constraints…" starts both
passes (2:18.92 and 3:17.40), so a cut **2:18.92 → 3:17.40** removes the whole first pass of
Responses/Close, the mid-video close card and the non-verbatim banner. It lands at about 3:38 with
all 7 required lines exact.

Board 2 is the problem. The only complete donor audio is the old live video
(`course-assets/data-centers/data-centers.mp4`, 2026-09-05 generation):

- Electricity: live 1:31.6–1:51.6 (4.4% in 2023, Berkeley Lab 6.7–12% by 2028; also includes the
  "all data centers, not AI alone" qualifier). Household bills would be lost.
- Water: live 1:59.2–2:10.2 (evaporate; hot day; about a million gallons; some recycle). Includes
  "to keep the hardware from melting."
- Jobs: live 2:25.0–2:34.8 (construction vs. 100 to 200 permanent).
- Noise: **no complete donor anywhere**. Lawsuits appear only in roll 2 ("24-7 fan noise causes
  lawsuits"), and none of the three sources has "lost sleep."
- Supermarket comparison: **in no source**.

That's a three-source splice on the key board that still leaves noise thin and three details
missing. Under the rules that makes it a reroll. If you'd still rather ship sooner, roll 1 with
the duplicate cut plus the three live grafts is the closest available. Optional extra: roll 2
3:18.6–3:36.1 (one request + "company in dollars…") in place of roll 1 4:05.8–4:19.1. That one sits
under a Notebook scene, so it's riskier.

## What the next roll needs (prompt change)

Both rolls followed "teach all four neighbor effects by name with their numbers" by compressing
each one to a headline. The fix is to make Board 2 hard audio, the same way the seven lines are:

> REQUIRED BOARD 2 AUDIO — read each of these sentences in full, in order, while Board 2 is on screen:
> "U.S. data centers used about 4.4% of electricity in 2023. Berkeley Lab projected 6.7 to 12% by 2028. In some places, added demand is already raising household bills."
> "Some facilities evaporate water to cool them, and a large data center can use about a million gallons on a hot day. Others recycle or reuse it."
> "Cooling fans run 24 hours a day. In some towns, neighbors have sued over the hum and lost sleep."
> "A finished facility may need only 100 to 200 permanent workers. That is about the staff of a big supermarket."

Also add: say "The scale varies by facility."; add "massive" to the avoid list; and "No drawn
people or faces, including hands holding phones beside a face" (roll 2 broke the no-people rule).
Keep roll 1's two-quadrillion walk-through: it's the best version of the math so far.

## Editing notes (either roll)

- Invented on-screen numbers to replace: roll 1 at 1:00, 1:40, 2:52, 3:56–4:04, 4:16. Roll 2 at
  2:52–3:16 and 3:32.
- Roll 1 at 0:52/0:56 shows cooling towers that read as a power plant. Worth replacing.
- Trim the Gemini Notebook outro on both.
- Board highlight/camera plan (Edit Spec 1b): provisional until a roll is chosen.

---

# Rolls 3 and 4 (revised kit, reviewed 2026-09-24)

These two rolls were generated on the kit revised after rolls 1–2, with 14 required lines and the
Board 2 sentences on their own lines. Transcripts are base.en and medium.en (`transcript-medium.txt`,
`words-medium.txt`); both models agree on every quote below. Silences were measured from the audio
at −40 dB. Findings are still unheard: nobody has listened to the audio yet.

## Verdicts

| | Roll 3 (3:55.1) | Roll 4 (3:01.3) |
|---|---|---|
| Board 2 | **RICH**: all four effects, every number, bills, recycling, lawsuits, supermarket | **WRONG again**: "12% of national usage by 2028", "about 200 permanent workers"; no 4.4%, Berkeley Lab, bills, recycling, lawsuits or supermarket |
| Required lines exact | 7/14. Five Board 2 lines are changed by a word or phrase with the meaning kept; **both closing lines have added words** | 7/14. Board 2 is reworded to fragments; close line 2 is "You now understand the physical system that drives the results." |
| Additions | Two short bridges to cut (below); "efficiency paradox" | "massive" ×2, "engaging with", "accurately understands" |
| **Verdict** | **REPAIR**: two cuts plus a close graft from roll 1 | **REROLL**; no beat beats roll 3 |

## Roll 3, required lines

| Line | Status | Spoken |
|---|---|---|
| compute | MET 0:28.2 | exact |
| scale | MET 1:10.9 | exact, then ", but the mechanical process is consistent." |
| ChatGPT | MET 1:15.0 | base heard "in", medium heard "and"; listen |
| somebody pays | MET 1:19.2 | exact |
| 4.4% in 2023 | MET 1:35.2 | exact |
| Berkeley Lab | changed 1:40.2 | "Berkeley Lab projected that number could reach 6.7 to 12% by 2028." |
| water | changed 1:52.4 | "…evaporate water to cool them down, and…" (adds "down") |
| sued | changed 2:06.0 | "neighbors have actually sued over the hum after losing sleep." |
| construction | changed 2:12.7 | "While initial construction employs many people, a finished facility may need only 100 to 200 permanent workers." |
| supermarket | changed 2:19.9 | "That is roughly the staff of a big supermarket." |
| banner | MET 2:53.4 | exact, two sentences |
| no-guilt | MET 3:38.0 | exact |
| close 1 | **MISSED** 3:46.3 | "Every **single** AI chat costs something real." |
| close 2 | **MISSED** 3:49.4 | "**And** now you know **exactly** what's behind the magic." |

None of the five changed Board 2 lines alters a fact, and no roll has an exact version of any of
them to graft, so they stay. The close is a hard requirement, and an exact donor exists.

## Roll 3, teaching

Every essential point is RICH or TAUGHT, in lesson order:

- The math, 0:09–0:27: "each new piece of text" where the lesson says token, but tokens are named
  in the next sentence.
- Compute, millions of people, and why companies build more data centers.
- The warehouse and the photograph walk, 0:50–1:02, close to the board text.
- Football fields, a small city, and "The scale varies by facility."
- Communities.
- All four neighbor effects.
- All three responses by name, with the banner.
- Efficiency not shrinking the total, 3:04–3:13. It says "will still rise" where the lesson says
  "can"; this is inside the "if use grows fast enough" condition, so it isn't wrong.
- One request, then streaming video and cars.
- "The company pays in dollars, the grid pays in watts, and the neighborhood pays in water and
  quiet."
- The no-guilt line, with its reason nearly word for word (3:40.8).

Nothing is WRONG. Source QA: PASS.

## Roll 3 repair plan (needs your approval before building)

1. **Cut the bridge**, 2:22.9 → 2:30.3: "The digital cloud relies on heavy physical infrastructure,
   and that infrastructure takes up space in the real world." There's silence on both sides
   (2:22.46–2:23.27 and 2:29.91–2:30.74), and the next words are "Looking at this panel…" at 2:30.78.
2. **Cut "paradox"**, 2:58.8 → 3:03.5: "But looking at this chart, you can see the efficiency paradox
   in action." There's silence on both sides (2:58.50–2:59.17 and 3:03.18–3:03.90), and the next
   words are "Making tasks more efficient…" at 3:03.92.
3. **Graft the close**: replace roll 3 from 3:45.9 to the end with **roll 1 4:32.08–4:36.84**, "Every
   AI chat costs something real. / Now you know what's behind the magic." Medium.en confirms it's
   exact, with 0.49 s between the lines. Roll 1's first close (3:12) runs into "Technology…", and
   roll 2's says "what is", so neither works. The graft sits under our close board, the safe place
   for a graft. Joining it: roll 1 speech is about 3 dB louder than roll 3, so match the gain.
   Median pitch is 192 Hz against roll 3's 163 Hz on the close (176 against 178 across each whole
   roll). It's the same narrator, but the close is pitched higher; **listen to this seam before
   approving.**
4. Optional, and not recommended: ", but the mechanical process is consistent" (1:12.3–1:14.4) has
   only a 0.11 s gap after "facility," at comma pitch. It's harmless; keep it.
5. Kept as is: "This graphic breaks down…" (1:26.9) and "Looking at this panel…" (2:30.8). These are
   production phrasing, but each carries the lesson's lead-in sentence for its board.

Result is about 3:43. It needs a fresh review before it can earn KEEP.

## Board and camera plan (provisional; follows the 2026-09-18 highlighting call)

| Board | Enters / leaves (roll 3 time) | Treatment |
|---|---|---|
| Board 1 photograph | 0:50.4 "Here is the inside…" → 1:02.6 | Full view, no highlight |
| Board 2 neighbors | 1:26.9 → 2:22.4 | Full view on the title, then whole-card rings at Electricity 1:33.2, Water 1:49.8, Noise 2:01.7, Jobs 2:10.7 |
| Board 3 demand | 2:30.8 → 2:58.4 | Full view, card rings at More Power 2:35.7, Better Cooling 2:40.9, Chips 2:47.3, banner 2:53.4 |
| Close | 3:45.9 (graft) → end | Standard close, no highlight |

## Roll 3 editing notes (visuals)

- Blank frames: 0:00–0:04 and 3:28.
- **Drawn man with a visible face**, 3:44: replace.
- Invented or wrong on-screen numbers:
  - "2×10¹⁴ ops/sec" at 0:48
  - "−75% energy/task" and "+1000% multiplier" at 3:00–3:12
  - at 3:36, **"1M+ gallons/day"** (the "daily" error, on screen), "Up to 12% US supply" and
    "24/7 fan acoustic load"

  Replace or cover all of these.
- Cooling towers at 1:12 read as a power plant.
- No Gemini outro card; the roll ends on black after the close.

## Roll 4, in brief

The opening through "Somebody pays" is good, and "The scale varies by facility." is exact. Then
Board 2 falls back to the roll 1–2 failure: one fragment per effect, the top of the range given as
the projection, and "about 200 permanent workers". Close line 2 is rewritten. Nothing here beats
roll 3 at a graftable seam. REROLL, but it isn't needed if roll 3's repair is approved.

## Materials note

The revision worked where it counted: roll 3 is the first roll to teach Board 2 fully. Roll 4 shows
that Notebook can still ignore the verbatim list, so the kit doesn't need another change for this.
