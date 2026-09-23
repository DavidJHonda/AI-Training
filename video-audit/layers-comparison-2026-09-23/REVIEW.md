# Layers: rolls 5 and 6 (2026-09-22 evening, on the corrected materials) against the live video

Narration review under `scripts/video/NARRATION-REVIEW.md`. Lesson authority: `index.html` LayersSection (line 7412) and
`lessons/layers.md` as updated 2026-09-22 (8c67f4d8: the pronoun in lower case so it is spoken as a word, the middle number
pairs out of the narration). Eight required-verbatim lines in `Prompts/layers-video-prompt.txt`. Earlier rolls 1–4 and the
`layers-v1` candidate built from roll 2 are recorded in `../layers-comparison-2026-09-22/` and `../layers-build-2026-09-22/`; roll 2
spelled the pronoun "I-T" and was superseded by the materials change. Rolls 5 and 6 were uploaded to `group-exercises/fake-trap/`
by mistake and moved to `Prompts/`. Bundles here: `layers-5/` (3:57.20), `layers-6/` (3:22.63), `layers/` (live v6 of 2026-09-17,
2:39.90). Word stamps with small.en in `*-words-small.txt` (rolls 5, 6 and 2).

**The pronoun check (the defect that sank roll 2):** in roll 6 every "it" runs 0.04–0.38 s against a 0.31 s mean for other two-letter
words; in roll 5, 0.08–0.38 s. Roll 2's spelled "I-T" ran 0.42–0.56 s. Both new rolls speak it as a word. The two longest instances
(roll 6 at 2:03.8 "the word it", 0.38 s; roll 5 at 2:13.2, 0.38 s) are stressed "the word IT" reads; David should still hear them.

## Teaching points (page order)

1. Hook; the horse sentence; three reads by name; "Each read updates the meaning until it clicks." (verbatim); working it out depends on repeated passes.
2. "AI doesn't read your message the way you do." (verbatim); a series of layers; attention and transformation update the numbers; updated numbers pass on; builds on what came before like rereading; "The whole stack of layers is called a neural network." (verbatim)
3. Board 2: numbers in, many layers, final numbers out; each row holds many numbers, two shown; .42 and −1.15 → .19 and −1.12; middle values not read; "Attention and transformation update the numbers at each layer." (verbatim)
4. Board 3: the sentence; 'it' could refer to different things; .12 and −.34; layer 1, layer 2, repeat; .41 and .06; "AI works out that 'it' refers to 'cat.'" (verbatim)
5. Scale: dozens of layers, sometimes more than a hundred; the horse sentence took a few reads; sarcasm, story twists, complicated reasoning take more; AI's layers give it more steps; why not keep adding; more computing power and time; "The extra benefit has to be worth the cost." (verbatim)
6. Close: "Meaning builds up, layer by layer." / "Attention and transformation. Dozens of times." Nothing after.

```text
LESSON: layers
CANDIDATE: Prompts/layers-6.mp4 (3:22.63)
VERDICT: REPAIR (base)
TEACHING POINTS:
  1 horse / three reads — RICH — 0:14–0:47: first read, "So you read it again", meaning clicks, "Raced describes the horse, and fell is what the horse did", "Working the sentence out depends entirely on these repeated passes", verbatim 0:47.32. Defects: the sentence itself is read as two pieces, "The horse raced past the barn." (6.76–7.96), a 1.0 s pause, "Fell." (9.42–9.62): the prompt asked for a beat after "fell", Notebook put it before; 0:10.5 "This infographic breaks down exactly why that sentence trips us up." (production phrase); 0:25.9 "Or did the horse raced past the barn afterward?" (grammar slip, inside the beat)
  2 AI / layers         — TAUGHT — 0:50 verbatim; 0:52 "It processes your text through a series of layers. In each layer, steps called attention and transformation work together to update the numbers…"; neural network verbatim 1:05.4. THIN here: "those updated numbers pass to the next layer" and the rereading analogy are not spoken at this point (the idea arrives at 2:26 "The numbers continue passing through more layers, each building directly on the previous layer's numbers")
  3 Board 2             — RICH — 1:13–1:51: numbers in/out, long line of layers each containing attention and transformation, many numbers / two, .42 and −1.15 → .19 and −1.12 with the middle values correctly skipped, "The numbers that come out are not the numbers that went in", verbatim 1:48.32. Defect: 1:08.8 "This diagram shows how those internal layers actually update the numbers." (production phrase)
  4 Board 3             — RICH — 2:02–2:43: all five stages by name in order, .12 and −.34, .41 and .06, verbatim 2:39.80. Defect: 1:57.8 "This chart maps out the five stages of how the AI resolves that pronoun." (production phrase)
  5 scale / why not     — TAUGHT with one garble — 2:43 dozens / more than a hundred with the qualifier; 2:52.9 "Untamelling sarcasm, story twists and complicated reasoning takes far more steps to build meaning than our simple horse sentence." (first word garbled on both decoders; the two page sentences compressed into one); "AI's layers give it more steps" folded into the question at 3:01; 3:06 more computing power and time; verbatim 3:10.80
  6 close               — both lines spoken, joined — 3:12.74 "Meaning builds up, layer by layer, attention and transformation, dozens of times." (a 0.38 s gap sits between "layer," and "attention"; the second half carries the board's own two-beat shape: "transformation," 0.5 s "dozens of times")
HARD REQUIREMENTS: 6 of 8 exact; the two closing lines spoken as one sentence.
ERRORS: none factual. Garble at 2:52.9; the split "Fell."; grammar slip at 0:25.9.
SOURCE_QA: PASS
ADDITIONS: "It doesn't stop at layer two." (2:26.6) is the prompt's guardrail spoken; keep.
REPAIR PLAN:
  a. Horse sentence + first production phrase: replace roll 6's 6.65–14.73 ("The horse raced past the barn. Fell. This infographic breaks down exactly why that sentence trips us up.", between the silences 6.18–6.65 and 14.28–14.73) with roll 5's 11.19–14.95 ("The horse raced past the barn fell." 11.90–13.60, spoken as one sentence, with its own 0.7 s lead-in and the 0.84 s beat after "fell" that the prompt asked for). Same-day voice; under Board 1 (ours). One graft removes both defects. Alternative if David likes the dramatic split: keep 6.65–9.70 and cut only 9.70–14.28.
  b. Cut 68.79–73.46 "This diagram shows how those internal layers actually update the numbers." (silences 68.32–68.79 / 73.05–73.46); Board 2 arrives at "Numbers go in on one side" (73.80).
  c. Cut 117.73–122.75 "This chart maps out the five stages of how the AI resolves that pronoun." (silences 117.13–117.73 / 122.17–122.75); Board 3 arrives at "At the start, the word it" (122.70).
  d. Graft roll 2's 192.82–205.66 ("The horse sentence took a few reads to untangle. Sarcasm, story twists, and complicated reasoning can take even more work. AI's layers give it more steps to work through those relationships and build meaning.", three whole sentences between the silences 192.35–193.03 and 205.79–206.36) in place of roll 6's 172.82–180.74 ("Untamelling sarcasm … horse sentence."). Restores the garbled word, the page's two sentences, and the "more steps" line roll 6 folded away. Roll 2 is 2026-09-22 morning, same Notebook voice; level-match. Picture: roll 6's own frames there are the stacked-layers drawing (2:44–2:52) then the invented "Simple Syntax / Complex Reasoning / 96+ Deep Layers" cards; hold the stacked-layers drawing over the whole graft and on through "why not…cost" (the invented "Depth: 32 Layers / 128+ Layers" cards run 2:56–3:13 and never ship).
  e. Close: separate the two lines without a graft by widening roll 6's own 195.73–196.11 gap to about 1.0 s with matched room tone, under the standard close board. The first line ends on a comma cadence; if that reads as a run-on to David's ear, the fallback is roll 5's line 1 "Meaning builds up, layer by layer." (227.50–229.42, period cadence, standalone) followed by roll 6's "attention and transformation, dozens of times." (196.12–198.78).
  About 5 s out (b, c, a's net), 6 s in (d); projected 3:24, pill 3 min (the live's pill; 3:24 rounds to 3).
EDITING NOTES:
  Notebook renders replaced: Board 1 0:12–0:52 (with its own arrows and rings), Board 2 1:12–1:51, Board 3 2:00–2:43. Rects measured for these three boards are in scripts/video/build_layers_v1.py (READS/B1_BANNER, DIAGRAM/NUMBER_CARDS/B2_BANNER, SENTENCE/STAGES); assets unchanged since (0311987d, 7333020c, 9d75b63a).
  Invented diagrams: 0:52.7–1:08 "LAYER 1 attention/transformation" with the value [0.42, −1.15] printed (cover: hold the 1:08 3D stacked-layers drawing back to 0:52.7, or bring Board 2 in early; the 0:52 phone drawing before it is harmless); 2:56–3:13 model-count cards (inside repair d's hold). Drawings worth keeping: desk lamp and book 0:00–0:08, "Fell?" card 0:08–0:12 (if repair a is taken, the card sits under roll 5's sentence; fine), phone 0:50–0:52, 3D layers 1:08–1:12, the sentence drawing 1:52–2:00, stacked layers 2:44–2:52. No photographs. Notebook's close render 3:14–3:19 and its end card never render.
LISTENING: small.en on every required line, the pronoun instances, the split "Fell.", the garble, and the close; base.en elsewhere. Not heard by ear.
```

```text
LESSON: layers
CANDIDATE: Prompts/layers-5.mp4 (3:57.20)
VERDICT: REPAIR-grade narration, but roll 6 is the better base; donor for the horse sentence
TEACHING POINTS: complete and mostly RICH: the sentence spoken as one line (11.90–13.60) with a beat after it; three reads by name; "Raced describes the horse, and fell is the action the horse took"; Board 2 with the middle values correctly skipped; all five stages; the scale with its qualifier. Weaker than roll 6 on the required lines and on additions: "Every row contains thousands of numbers" (invented count; the page says many), "Identifying a pronoun only requires the model to look back at a few nearby words … information found hundreds of words earlier" (invented mechanism, 3:15–3:29), "This continuous numerical transformation is the machine equivalent of rereading" (2:00), and 3:33 "sprawlal relationships" (garble).
HARD REQUIREMENTS: 5 of 8 exact. "Attention and transformation update the numbers at each layer." MISSING (1:24 "Inside every layer, two steps, attention and transformation, update the numbers" is the nearest); "AI works out" spoken as "the AI works out that it refers to cat" (3:02); close line 2 wrapped: "It relies on attention and transformation, dozens of times." Close line 1 exact and standalone (227.50–229.42): the fallback donor for repair e.
VISUALS: 1:04–1:12 invented network diagram with values; 3:00–3:08 "Layer 1/24 … Layer 24/24 Referent Resolved 98%" (a layer count and percentages on screen); 2:08 the cat-and-"it" drawing is charming and could be borrowed under roll 6's Board 3 lead-in if a Notebook interleave is wanted.
```

```text
LESSON: layers
CANDIDATE: course-assets/layers/layers.mp4 (2:39.90, live v6)
VERDICT: superseded by roll 6
TEACHING POINTS: the shape is there in the old formal register ("mathematical stack called a neural network", "shifting decimal values are the machine's version of a human rereading", "step-by-step mathematical journey"). Against the current page it is THIN on Board 1 (the three reads are not named; "someone raced a horse past a barn, and then it fell" leaves "it" ambiguous), on Board 2 (no numbers spoken; "the bottom table shows a word's initial state"), and on Board 3 (no starting or final numbers; layers one and two collapsed). Sarcasm beat present. Scale present with qualifier.
HARD REQUIREMENTS: 0 of 8 as written; the two closing lines joined ("Ultimately, meaning builds up layer by layer, with attention and transformation, dozens of times.").
```

```text
BEST-OF PLAN: layers
BASE: Prompts/layers-6.mp4 (6 of 8 required lines exact, the middle number values correctly unspoken, tight at 3:23, every board's content read)
  Horse sentence — roll 6 split "…barn. [1 s] Fell." | roll 5 RICH @0:11.9 one sentence + beat — TAKE roll 5 (under Board 1)
  Untangle / sarcasm / more steps — roll 6 garbled + compressed @2:52 | roll 2 RICH @3:12.8–3:25.7, three sentences | roll 5 TAUGHT with invented "hundreds of words" — TAKE roll 2 (under a held drawing)
  Close — roll 6 joined @3:12.7 | roll 5 line 1 standalone @3:47.5 | rolls 1–4 and the live all joined — widen roll 6's own gap first; roll 5 line 1 is the fallback
  Everything else — KEEP roll 6
GRAFTS: 2 audio-only (roll 5, roll 2) + 1 tone insert; cuts b and c. Note: all six Layers rolls and the live join the closing pair. "Attention and transformation. Dozens of times." is a fragment, and Notebook attaches it to the sentence before it every time; the recipe's banner rule applies to this close too.
```

## Proposed edit plan (for David's approval before the first build; Edit Spec 1b; onsets from small.en on roll 6, shifting with repairs a–c)

| Board | Highlighting sequence | Camera | Reason or exception |
|---|---|---|---|
| "The Horse Raced Past the Barn Fell" | board arrives on the grafted sentence; First Read column at "On the first read" 14.64; More Reads at "So you read it again" 22.64; Meaning Clicks at "Finally, the meaning clicks" 34.36; banner at 47.32 | full board (compact); the three reads are columns in one white box, so full-height rings (layers-v1 pattern) | leaves at "AI doesn't read" 50.00 for the phone drawing |
| How Layers Update the Numbers | whole diagram at "Numbers go in" 73.80; Starting Numbers card at "We start with a pair" 91.52; Final Numbers card at "finishing at" ~1:40; banner at 108.32 | full board (compact) | the After One Layer / After Many Layers cards are never ringed, matching the narration that skips them |
| How AI Connects 'it' to 'cat' | sentence strip at 122.70; Start 122.70 (pops in full view), Layer 1 at 131.80, Layer 2 at 137.64, Repeat at 145.08, Result at 154.80; banner at "AI works out" 159.80 | full board (compact); five narrow cards read at full view | |
| Standard close | none | full | from 192.74; the widened gap sits inside it |

Pauses (Edit Spec 6): none beyond the close-gap widening in repair e; roll 6's own gaps (0.3–0.6 s) breathe, and repair a carries roll 5's beat after "fell".

## Build: v2 review candidate (2026-09-23, David approved repairs a–e as written, a as the graft)

**Candidate:** `Prompts/layers-v2.mp4` (5841 frames, 3:14.70, sha256 18abdd45624fa50c…), a full production pass on roll 6
(`scripts/video/build_layers_v2.py`, folder `build-v2/`). The `layers-v1` candidate (roll 2) is superseded. Every audio edge was placed
on a 20 ms RMS profile + silencedetect, not on the word stamps (small.en ran 0.65 s early at "Meaning" and 0.35 s late at "Numbers").

**Timeline (output frames → roll 6 frames):** 0–155 lamp/book drawing (0–155) · 155–198 Board 1 arrives at the roll's cut to the
"Fell?" card, under "Try this sentence." (155–198) · 198–302 **graft a**, roll 5 342–446 audio only under Board 1 (replaces roll 6
198–440) · 302–1359 Board 1 (440–1497): First Read 14.72, More Reads 22.54, Meaning Clicks 34.22, banner 47.16 (roll-6 seconds) ·
1359–1431 phone drawing (1497–1569) · 1431–1819 3D stacked-layers frame 2000 held back over the invented LAYER 1 diagram (1569–1957) ·
1819–1923 3D layers live (1957–2061) · **cut b** 2061–2201 · 1923–3079 Board 2 from the resume (2201–3357): whole diagram 73.45,
Starting Numbers 91.42, Final Numbers 100.70, banner 107.86 · 3079–3243 sentence drawing (3357–3521) · **cut c** 3521–3676 ·
3243–4451 Board 3 from the resume (3676–4884): sentence strip + Start 122.74, Layer 1 131.72, Layer 2 137.56, Repeat 144.92, Result
154.66 (no banner on this board; the Result ring holds through "AI works out") · 4451–4744 stacked layers live, both of Notebook's
framings (4884–5177) · 4744–5150 **graft d**, roll 2 5780–6186 audio only under stacked-layers frame 5150 held (replaces roll 6
5177–5431) · 5150–5520 the hold continues under "If more layers… worth the cost." (5431–5801; the invented Depth/Optimal cards never
show) · 5520 standard close from the measured "Meaning" onset (5801) · 5599–5616 17 frames of matched room tone inside the
"layer," / "attention" gap (at 5880) · 5616–5721 "attention and transformation, dozens of times." to 5985 (after the sibilant; the
roll's digital zero from 199.54 never renders) · 5721–5841 close hold, 0.4 s of tone then a 1.2 s fade to silence.

**Grafts:** a at output 6.60–10.07, gain −2.67 dB (speech RMS: roll 6 neighbours 3192 vs roll 5 4339); volumedetect mean −20.2 dBFS
against −20.9 before / −20.1 after. d at 158.13–171.67, gain +2.60 dB (5875 vs 4355); mean −15.0 against −15.0 / −14.9. Donor lead-ins
and tails (0.46/0.76 s; 0.29/0.40 s) ramped from/into roll 6's tone. Floors: roll 5's gaps sit 9.9 dB below roll 6's near the horse
sentence (58.5 vs 18.8 RMS; roll 6's includes the "sentence." tail hum), roll 2's 1.5 dB below roll 6's near the scale beat.

**Checks (Edit Spec 10):**
1. Decoded 5841 = plan; each leg decoded its span (render_legs assertion).
2. `transition_guard.py` 16/16 PASS (155, 198, 302, 1359, 1431, 1819, 1923, 3079, 3243, 4451, 4744, 5150, 5520, 5599, 5616, 5721);
   strips inspected: every board in/out, both graft seams, both cuts, both cover holds and the gap insert land on the destination at
   the first frame (only the intended cuts spike; holds and audio-only seams show delta 0).
3. Pauses: none added except the close gap. silencedetect on the finished file: 186.45–187.31 at −40 dB (0.86 s), 186.50–187.31 at
   −45 dB (0.81 s); word edge to word edge ("layer." ends 186.28, "attention" onset 187.28) 1.00 s; the first 0.2 s of the gap is the
   roll's own breath at −47 to −54 dBFS. Gaps at the four narration seams: 0.76 s before the horse sentence, 0.77 s after it, 0.70 s
   before "Numbers go in", 0.47 s before "At the start", 0.54 s before "The horse sentence took", 0.47 s before "If more layers".
   Tail: tone at −66 to −68 dBFS for 0.4 s after "times.", fade to −150 by 192.3, digital silence to 194.71. Not heard by ear.
4. Every settled ring frame inspected (`states-*.jpg`, full-res `state-*.jpg`): right card, complete inside the ring, nothing clipped;
   Board 1's three reads are full-height column rings in the shared white box; Board 2's Starting/Final cards hug their measured edges.
5. All three boards compact, still (push=False), full view first: Board 1 opens 9.6 s before its first ring; Boards 2 and 3 arrive at
   the resumes and their first rings pop in the full view 0.08 s / 0.21 s later (min_open=0, spec rule 3).
6. Transcript (small.en, `final-transcript-small.txt`): "Try this sentence. / The horse raced past the barn fell. / On the first
   read…" as one line; no "infographic", "diagram" or "chart"; "The horse sentence took a few reads to untangle. Sarcasm, story
   twists, and complicated reasoning can take even more work. AI's layers give it more steps to work through those relationships and
   build meaning."; close as two lines "Meaning builds up, layer by layer." / "Attention and transformation, dozens of times."; nothing
   after. All 11 roll-6 pronoun instances present with their durations (0.04–0.36 s); roll 2 adds one ("give it more steps").
   Corner mark: 883 cloned, 1069 inpainted, 0 declined. Protected files (live video, rolls 2/5/6, three boards, close JPG, lesson,
   index.html) unchanged. Kept spans contact-sheeted (`kept-notebook-spans.jpg`): all line drawings, no photographs, no invented
   numbers or layer counts on screen. Longest unbroken board run 40.1 s (Board 1).
7. Live video and lesson unchanged. Not committed.

**Decisions and deviations:** Board 1 arrives at 5.17 (the roll's cut to the "Fell?" card) rather than at the graft start 6.60, because
the card would otherwise flash for 1.4 s and never return; Board 3 opens with one combined ring (sentence strip + Start) at "At the
start"; Board 3 has no takeaway banner, so the Result ring carries the verbatim line; ring onsets re-measured on the RMS profile
(within 0.1–0.5 s of the plan's stamps); the whole-diagram ring uses the neutral purple, the card rings the cards' purple accent; the
Starting Numbers ring holds through "As they pass through the layers…" until "finishing" (the approved sequence; an unmarked state
there is a one-line change if David prefers). Runtime is 3:14.7, not the plan's 3:24 (the plan did not subtract the roll's own
close render and end card).

**Not auditioned by ear:** the six narration seams above (6.60, 10.07, 64.5, 108.2, 158.1, 171.7), the widened close gap at
186.3–187.3, and roll 2's voice against roll 6 across graft d.

**At ship (not authorized yet):** copy to `course-assets/layers/layers.mp4`, cache key `20260923ship1`, pill stays 3 min (3:15),
manifest video hash/bytes; rewrite `LESSON_VIDEOS.layers.title` (it still says "and one box stays blank", which David said to rewrite
at ship). Rolls 1–6 and the v1 candidate stay until David says otherwise.

## v3 (2026-09-23): the live video's animation under the scale / why-not beat

David, after v2: "2:29 to 3:06 shows a single graphic. The original video had more engaging graphics here." The live v6 carries one
continuous drawn animation for this beat (1:56–2:31): a layer stack growing with "Total Layers: 128" and "100+ Layers in modern
models" printed, then LINGUISTIC RESOLUTION: PRONOUN TO NOUN ("her" → "scientist"), then HIGH-LEVEL NUANCE & DEEP REASONING (the
stack filling red, labels Sarcasm & Tone Context / Narrative Twists & Shifts / Complex Multi-step Logic), then THE ARCHITECTURAL
TRADE-OFF (a balance: Model Capacity against Running Cost, "Optimal Engineering Equilibrium"). The first scene prints real-looking
counts, so it stays out; roll 6's own stacked-layers drawing remains under "dozens and sometimes more than a hundred". Live frames
3886–4541 (2:09.5–2:31.4) then play continuously under graft d and the why-not beat: the pronoun scene under "The horse sentence took
a few reads to untangle", its dissolve into the nuance scene landing about a second into "Sarcasm, story twists…", and the dissolve
into the trade-off landing at "If more layers give the system better reasoning, why not…"; the settled balance holds 4 s under
"…worth the cost." (the borrowed span is 249 frames short of the row, so keep() holds its last frame). Live frames are corner-cleaned
by render(). `Prompts/layers-v3.mp4` (3:14.70, 5841 frames, sha256 22c403f13e4dcab9…), script `scripts/video/build_layers_v3.py`,
folder `build-v3/`. Guard 16/16, decoded 5841 = plan, corner mark 0 declined, protected files unchanged, audio identical to v2. v2
deleted. Listen list unchanged from v2.
