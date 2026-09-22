# Layers: rolls 1 and 2 against the live video (narration review, 2026-09-22)

**Candidates:** `Prompts/layers-1.mp4` (3:41.53, 6646 frames) and `Prompts/layers-2.mp4` (3:43.50, 6705 frames), both rolled on
the 2026-09-21 kit. **Live:** `course-assets/layers/layers.mp4` (2:39.90, 4797 frames), v6 shipped 2026-09-17 under the old
method. Grounding: the Layers section of `index.html`, `lessons/layers.md`, and the kit's beat spine, verbatim lines and
guardrails. Full transcripts are beside this file.

## Verdicts

| Roll | Verdict | Why |
|---|---|---|
| **layers-2** | **KEEP** | Every beat RICH or TAUGHT, **all eight verbatim lines exact**, every board number spoken, and it delivers David's pause after the horse sentence on its own. |
| layers-1 | REROLL (not the spine) | Misses the Board 1 banner line, drops the last of Board 2's four number pairs, gives no pause after the horse sentence, thins the second read, and says the AI builds "understanding" — a banned word. |
| live v6 | Would not pass today | Three of eight verbatim lines, and **no board numbers at all**: both number boards are described rather than read, which is the teaching this lesson turns on. |

## Required verbatim lines

| Line | layers-1 | layers-2 | live |
|---|---|---|---|
| "Each read updates the meaning until it clicks." | ❌ "Each read updates the context." (24.66) | ✅ 47.60 | ❌ "With every read, you update the meaning of the words until the whole thought makes sense." |
| "AI doesn't read your message the way you do." | ✅ 26.48 | ✅ 50.56 | ❌ "AI doesn't read the way we do." |
| "The whole stack of layers is called a neural network." | ✅ 51.82 | ✅ 67.12 | ❌ "a mathematical stack called a neural network" |
| "Attention and transformation update the numbers at each layer." | ✅ 89.78 | ✅ 121.92 | ❌ |
| "AI works out that IT refers to CAT." | ✅ 160.42 ("the AI works out…") | ✅ 178.96 | ❌ "the results mathematically conclude, it refers to cat" |
| "The extra benefit has to be worth the cost." | ✅ 208.48 | ✅ 211.28 | ❌ "Developers have to balance the intelligence of their model against the cost" |
| "Meaning builds up, layer by layer." | ✅ | ✅ | ✅ |
| "Attention and transformation. Dozens of times." | ✅ | ✅ | ✅ |
| **Total** | **7 / 8** | **8 / 8** | **3 / 8** |

## Beat by beat

| # | Beat | layers-1 | layers-2 | live v6 |
|---|---|---|---|---|
| 1 | English-class hook | TAUGHT (0.00) | TAUGHT (0.00) | TAUGHT (0.00) |
| 2 | Speak the sentence, then a beat of silence | **MISSING the beat** — the sentence ends 12.12 and the next line starts at 12.12; no gap | **RICH** — 0.63 s of silence at 12.36–12.99, exactly the pause David asked for in the prompt | TAUGHT — 1.24 s, but spliced in at the v6 edit, not spoken |
| 3 | Board 1, three reads by name + banner | TAUGHT — first read "feels broken, as if a word is missing" ✓; second read only "Did the barn fall?"; click ✓; **banner wrong** | **RICH** — all three reads with the lesson's own clauses ("You reach fell and the sentence seems to stop short", "Did a barn fall? Did the horse race past the barn afterward?", "Raced describes the horse. And fell is what the horse did.") + banner verbatim | TAUGHT — three reads compressed, no banner |
| 4 | Pivot, layers, attention and transformation, updated numbers pass on | **RICH** (26.48–51.82) | **RICH** (50.56–69.68), incl. "Those updated numbers pass to the next layer." | TAUGHT (37.92–53.90) |
| 5 | "The whole stack of layers is called a neural network." | RICH | RICH | TAUGHT (substance, not the line) |
| 6 | Board 2: numbers in / layers / out, two positions, **all four pairs** | TAUGHT — .42/−1.15, .51/−.87, .27/−1.21 spoken; **the final .19/−1.12 is MISSING** | **RICH** — all four pairs plus "The values shift at every layer, so the numbers that come out are not the numbers that went in." | **THIN** — "the numbers shift at every stage" with no values at all |
| 7 | Bridge: follow IT | TAUGHT | TAUGHT | TAUGHT |
| 8 | Board 3: five stages with IT's numbers | **RICH** — .12/−.34, .18/−.22, .25/−.09, repeat, .41/.06 | **RICH** — same five, each tied to its stage name | **THIN** — "moving through layers one and two, the numbers update"; no values |
| 9 | Scale, with the qualifier | RICH (165.78) | RICH (182.08) | RICH (116.60) |
| 10 | Why depth | RICH, but see the guardrail note | **RICH** (192.88–205.68) | TAUGHT (125.56–141.80) |
| 11 | Why not keep adding layers | RICH + verbatim | RICH + verbatim | TAUGHT, no verbatim |
| 12 | Close, both lines | RICH | RICH | RICH |

## Guardrails

- **layers-1 breaches one:** "…require these massive stacks of layers to build up a deep enough **understanding** to be accurate"
  (191.26). The kit bans saying AI understands. No other banned word appears in either roll; neither previews Vector Space,
  narrates the Brain Break, names a model, or reads the site address.
- layers-2: no breach found.
- Both rolls keep the scale qualifier ("companies don't always share" / "keep their exact designs private").

## Recommendation

**Ship layers-2 as the spine, uncut and ungrafted.** It is the only roll that reads every board value, lands all eight verbatim
lines, and carries the requested pause in the narration itself. Nothing in layers-1 is richer: where the two overlap, roll 2 is
equal or fuller, and roll 1's one distinctive stretch (the why-depth beat) is the one that breaks a guardrail.

## Editing notes (layers-2)

- **Runtime 3:43.50** against the live 2:39.90, so the pill would go **3 min → 4 min**.
- **The lesson's video title is stale and must change at ship.** `LESSON_VIDEOS.layers.title` (index.html line 1125) still reads
  "Meaning builds up, layer by layer — and one box stays blank." David resolved on 2026-09-21 that the cliffhanger is not coming
  back and the title gets rewritten when this reroll ships. Suggested: "Meaning builds up, layer by layer."
- Boards to install in the edit: `layers-horse-three-reads.jpg`, `layers-inside-layer.jpg`, `layers-resolves-it.jpg`, and the
  canonical close. `layers-why-dozens.jpg` stays out (David, 2026-09-21). No face boards, so no faceless variants.
- Notebook renders its own versions of all three boards, with its own yellow highlighting on the IT/CAT board; those spans are
  what our boards replace.
- Frames sampled at 0, 900, 2400, 4200 and 6000 in both rolls: no stock photographs and no watermark beyond the standard Gemini
  Notebook corner mark. **This is a sample, not a sweep** — the v5/v6 reviews found two photograph spans in the old roll, so the
  build should check the full file.

---

# Second pass: layers-3 and layers-4 on the updated materials (2026-09-22, evening)

**Candidates:** `Prompts/layers-3.mp4` (2:52.10, 5163 frames) and `Prompts/layers-4.mp4` (3:44.87, 6746 frames), rolled after the
materials were rewritten (commit 8c67f4d8: ‘it’ and ‘cat’ as words, first and final number pairs only, the rereading beat added).
Transcripts beside this file.

## Verdicts

| Roll | Verdict | Why |
|---|---|---|
| layers-3 | **REPAIR** — the best spine available, but not shippable as it stands | Four lesson lines are missing, and every one of them exists in roll 2 as a clean donor. The pronoun *appears* fixed; two instances need David's ear. |
| layers-4 | REJECT | Still spells "I-T" throughout, drops two verbatim lines including "AI works out that ‘it’ refers to ‘cat,’" says "This diagram illustrates" and "This infographic tracks" — both banned — and adds jargon the lesson does not use. |

## Did the materials fix the two defects?

**The pronoun: fixed in layers-3, not in layers-4.** Word durations, the same measure that caught it the first time:

| Roll | "it"/"IT" durations at the IT/CAT board | Reading |
|---|---|---|
| layers-2 (previous) | 0.42, 0.44, 0.50, 0.56, 0.70 | spelled, every time |
| **layers-3** | 0.10, 0.22, 0.24, **0.36, 0.36** | mostly the word; two instances ambiguous |
| layers-4 | 0.38, 0.46, 0.46, 0.54, 0.56 | spelled, every time |

Ordinary "it" in layers-3 runs 0.08–0.18 and "cat" runs 0.18–0.22, so the three short instances are the word. The two at 0.36
(99.90 and 111.80) sit between "word with emphasis" and "spelled" and cannot be settled from the transcript. **David should listen
to layers-3 at 1:39.9 and 1:51.8 before we commit to it.**

**The number rule: not fixed, and the cause is now clear.** Both rolls read all four pairs on Board 2 and all four on Board 3 —
values that are no longer in the Markdown at all. They are printed on the board images, and Notebook read them off the boards. The
prompt negative ("speak only the first and final pairs; never read the middle values") did not hold against the picture. Removing
them from the Markdown cannot fix this; only a different board, or accepting the recitation, will.

## What layers-3 is missing (all four exist in roll 2)

| Missing from layers-3 | Donor in layers-2 |
|---|---|
| "The whole stack of layers is called a neural network." — says "This entire stack of layers…" | 67.12–69.68 |
| The final meaning of the sentence: "Someone raced a horse past a barn. Then the horse fell." — layers-3 gives only "Raced describes the horse. Fell is what it did." | 36.56–40.56 |
| "Numbers go in on one side and final numbers come out the other." — Board 2's opening line | 73.60–77.36 |
| The scale qualifier: "AI companies don't always share how many layers their models use." | 182.08–192.24 |

None of the four donor beats contains the pronoun, so roll 2's spelling defect does not travel with them. Integrated loudness is
−17.3 LUFS (layers-3) against −17.0 (layers-2): a 0.3 dB match, well inside the ~1 dB graft tolerance.

**Also missing from both rolls:** the rereading beat added to the Markdown for this reroll ("Working the sentence out depends on
each repeated pass…"). Neither roll speaks it. It can be left out, or taken from the live v6 as originally proposed.

## Recommendation

1. **David listens to layers-3 at 1:39.9 and 1:51.8.** If the pronoun is spoken as a word there, layers-3 is the spine.
2. Build it with **four grafts from layers-2**, each a whole sentence between silences, each landing under a course board.
3. If those two instances are spelled, neither roll is usable and the next prompt needs the negative moved into REQUIRED VERBATIM
   AUDIO, where the model follows most literally, rather than VOICE.

Runtime would land near 3:05 with the grafts — pill 3 min, unchanged from today's live.
