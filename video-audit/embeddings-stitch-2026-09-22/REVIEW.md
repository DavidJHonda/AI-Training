# Embeddings v5 — roll 1 plus two grafts, four cuts, rings on the words (2026-09-22)

`Prompts/embeddings-v5.mp4` — 4:38.33 (8350 frames), built by `scripts/video/build_embeddings_v1.py`.
Three-way comparison of rolls 1 and 2 against the live video is in
`video-audit/embeddings-comparison-2026-09-22/REVIEW.md`.

**SHIPPED 2026-09-22 on David's "ship it"** as `course-assets/embeddings/embeddings.mp4`
(`a47d96f33271…`), 4:38.33, replacing the 3:57 live video. Cache key `20260917ship1` -> `20260922ship7`
(ship1 through ship6 were taken by other sessions today). Pill **4 min -> 5 min**.

## What changed from v3

David's direction, 2026-09-22: hold both photographic boards at full view, stop reading aloud what the
boards already show, and open Board 5 on the full illustration rather than a zoom.

| | change | result |
|---|---|---|
| Board 1 | was a camera walk (badges → fry-thief → pull back) | **static full view**, banner ringed only |
| 0:23.70–0:41.18 | **cut** | removes "Look at this illustration… into a shirt pocket." — the banned board-furniture line, the four badge numbers and the fry-stealer description |
| 1:39.20–1:49.53 | **cut** | removes coffee's six scores |
| Board 5 in-point | source 7071 → **6980** | opens at full view, ahead of roll 1's own cut to a zoomed recreation at 6987 |
| 4:17.90–4:36.50 | **cut** | removes "Reading across cat's row, the values start at 0.45 … at the end." |
| Board 3 | — | **coffee's Citrus 0 now rings as it is spoken** |
| runtime | 5:24.73 → **4:38.33** | 46.4 s out |

The pill stays **5 min** by the course's convention (4:25 → 4 min, 4:37 → 5 min).

### The cut that had to move

David asked for 1:39–1:46. `and ten for dark. Because we keep the columns aligned,` is a single unbroken
run with no gap inside it, so stopping at 1:46 would have orphaned "and ten for dark." onto the end of
"coffee gets a completely different set of scores." Ending at **1:49.53** takes the "Because we keep the
columns aligned," preamble with it, so verbatim line 2 now opens its own sentence:

> "…coffee gets a completely different set of scores. **Each position always means the same thing. The
> number says how much.**"

**This is the one edge where both decoders were wrong and the waveform settled it.** Whisper puts "each"
at 109.58 and `silencedetect` opens the gap at 109.51. The RMS trace shows "aligned," decaying through
**109.31**, true room tone only from **109.50**, and "each" actually starting at **109.73**. Cutting on
either decoder's number would have shaved the front off a verbatim line. The cut sits at 109.53, mid-floor,
keeping 0.20 s of breath. Every other edge was checked the same way and sits in a 440–920 ms quiet window.

## Verified on the encoded file

| Requirement | Result |
|---|---|
| All eight verbatim lines | **8 / 8** — @0:20.44, 1:21.90, 1:37.82, 2:24.60, 2:43.66, 3:20.04, 4:26.54, 4:29.60 |
| Coke's six scores | **all six** — 9, 1, 10, 2, 3, 8 |
| Citrus trio | Coke 1, Pepsi 10, **coffee 0** |
| cat's ID and the circled 0.45 | 4719; "like that 0.45, is called a parameter" intact |
| Both grafts | land clean, in full, with roll 1's own next line finishing Board 4's row |
| The three cuts | all four removed phrases absent; all three joins read as continuous sentences |
| transition_guard | **18 / 18 pass** |
| Audio | **zero dips** at all 18 boundaries (−50 to −67 dB, all room tone); **no true-silence windows** |
| Gemini mark | **0 real hits / 279 sampled** — 33 flags are our own `besmarterthanthetool.com` credit line, 1 is a drawing's panel border, all inspected |
| Protected sources | **9 / 9** hashes unchanged |

### The joins, as encoded

> **A** — "…An ID identifies you. It doesn't describe you. The badges perfectly identify which student is
> which…" The fry gag survives the cut: it still pays off at 0:32 with "His ID number won't tell you he's
> the one who steals fries."
>
> **B** — "…coffee gets a completely different set of scores. Each position always means the same thing."
>
> **C** — "…the dimensions marked D1 through Dn. Each individual learned number in this sequence, like
> that 0.45, is called a parameter."

### Every board exit inspected frame by frame

One clean cut at each, static frames either side, no second cut within six — no recreation leaked. This
matters because the guard has missed this class three times (Support Trap's near-identical recreation fell
under its change threshold; Engagement Trap's nine-frame leak was too long for its two-cuts-within-six
pattern). The guard and an eye on the frames are complementary, not redundant.

**Board 5's new in-point was the reason to look.** Roll 1 cuts to a zoomed recreation of the embedding
table at 6987; the board now takes the screen at 6980, seven frames ahead of it, and the strip confirms
the notebook drawing cuts straight to our board at full view.

## Rings: every onset measured against the spoken word

Each onset was checked against roll 1's word timings rather than estimated. All 21 now sit within ±0.3 s
of their cue. **Five were corrected after v4 was encoded**, including one drift that had been wrong in v3
and would have shipped unnoticed:

| Ring | was | spoken at | now |
|---|---|---|---|
| Board 2, Coke's whole row | 123.20 | **125.66** | 125.60 — it had been firing 2.5 s before "the whole row of numbers is a vector", during the "In formal AI terminology," preamble |
| Board 2, the row as a whole | 134.50 | 133.82 | 133.90 |
| Board 3, the CITRUS heading | 162.00 | 162.90 | 162.90 — lands on "a seventh dimension", holds through "Citrus" 2.7 s later |
| Board 5, the token + its ID | one paired ring @238.60 | cat 236.80, ID 238.74 | **split in two** — one ring was early for one half and late for the other |

- **Board 1.** Full view throughout, banner ringed as verbatim line 1 is spoken. The badge walk had nothing
  left to walk to: the narration that read the four numbers aloud is cut A. They remain legible on roll 1's
  own drawing immediately afterwards.
- **Board 2.** Coke's row, coffee's row (on "Moving down to the next row"), the banner, then Coke + 9, 1, 10
  as the question names them, Coke's whole row on the vector line, the six headings, one value chip, and the
  row as a whole.
- **Board 3.** Pepsi's name alone, her first six with Citrus deliberately outside the ring, the CITRUS
  heading, then **10, 1 and 0** as each is spoken, then the banner.
- **Board 5.** Full illustration throughout, no dive. Token, its ID, the other tokens' rows under the graft,
  the first two columns, the d1–dn headings, cat's row, the circled 0.45, the whole row as the embedding.
  The ring that used to walk cat's values as they were read is gone with cut C.
- Boards 2 and 3 no longer use `banner_at`, which would force the banner ring to hold to the board's end.
  Both keep teaching after their takeaway, so the banner is an ordinary ring in the sequence.
- Ring colour is measured, never chosen: Boards 2, 3 and 5 carry no locked accent, so their rings take the
  neutral video purple, which also keeps them clear of Board 5's own purple glow and yellow circle.

## The one thing that needs your decision

**Each of the three cuts removes something `Prompts/embeddings-video-prompt.txt:16` requires the narration
to say** — "four badge numbers, and the fry gag", "Speak both drinks' six scores", and "the first values".

All three remain legible on the boards, and the rings now point at them as they are discussed, so the
teaching survives visually — which is the case for the edit. But the prompt is the spec a reroll is
generated from, so **unless line 16 is amended, the next roll will argue with this edit.** The prompt is
unchanged; amending the generation spec is a bigger move than an edit and is David's call.

## Notes for the eye test

- **The floor step.** Roll 1's pause floor is −56.4 dB against roll 2's −62.8, so each graft steps down
  6.4 dB into a quieter room and back up. Both are short and under a board, and down-then-up is the less
  audible direction, but it is the one thing here I cannot judge without ears.
- **"vable" versus "fable"** is acoustically ambiguous and flips under prompt biasing either way. The build
  uses roll 1, whose unbiased decode lands on "Vable". Worth your ear.
- **Two of roll 1's four board-furniture phrases are now gone** with cut A ("Look at this illustration…")
  and cut B (the cut took "Because we keep the columns aligned," but "This table captures our ratings…"
  survives at 1:02). "This updated table shows…" and "This comparison chart maps…" also remain; both carry
  teaching content and cannot be lifted cleanly.
- Voice drift beyond the lesson's register: "In formal AI terminology", "model architecture", "complex
  decimals", "an organizational tool". None are banned words.
- The lesson's prose line "funny, into hockey, or the person who steals fries at lunch" is in none of the
  rolls; only the live video has it.

## Shipped

`index.html:1123` updated: cache key `20260917ship1` -> `20260922ship7`, pill `4 min` -> `5 min`.
Render intermediates swept per the ship checklist (1.63 GB freed). Candidates removed from `Prompts/`;
the rolls and the comparison bundle are kept.

**Not done here:** the file was not watched end to end or auditioned by ear. David approved the ship on
the measured checks.
