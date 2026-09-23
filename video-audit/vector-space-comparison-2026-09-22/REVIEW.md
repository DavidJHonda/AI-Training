# Vector Space: rolls 1 and 2 (2026-09-22) against the live video

Narration review under `scripts/video/NARRATION-REVIEW.md`. Lesson authority: `index.html` VectorSpaceSection (line 7095) and
`lessons/vector-space.md` (2026-09-21 recipe, board-coverage pass 2026-09-21; eight required-verbatim lines in
`Prompts/vector-space-video-prompt.txt`, each standing alone in the Markdown). Bundles: `vector-space-1/` (4:14.47, 79 cuts),
`vector-space-2/` (4:06.87), `vector-space/` (live v5 of 2026-09-17, 3:52.90, a visual retrofit of the 2026-09-10 roll-4 build). Word
stamps with small.en in `*-words-small.txt`. The live's six boards hash-match the current `course-assets/vector-space/` files.

## Teaching points (page order)

1. Embeddings; the layers change the numbers; if the numbers change, how do they still represent meaning? Vector space.
2. Board 1: three cities, two coordinates each (Mountain View 37° N 122° W, Dallas 33° N 97° W, New York 41° N 74° W); two new positions; 38/120 is closest to Mountain View, 40/76 to New York.
3. Board 2: "When nothing matches exactly, distance finds the closest one." (verbatim)
4. Board 3: three drinks, seven dimensions in order; the three rows read; "Coke and Pepsi have more similar profiles than either does to coffee." (verbatim); the definition sentence and "That's vector space." (verbatim)
5. Board 4: the similarity map, two neighborhoods; the mystery drink's ratings 9,1,10,2,3,8,9; closest to Pepsi.
6. Board 5: "The mystery drink's ratings are closest to Pepsi's." (verbatim); distance: first six match, Citrus 9 vs 10 is a gap of 1, vs Coke's 1 a gap of 8; "Smaller gaps mean closer positions." (verbatim); thousands of dimensions learned in training; similar meanings nearby.
7. Board 6: the sentence; IT could refer to many things; the layers update IT's numbers to connect it to CAT; .12, −.34 to .41, .06; "IT's new position reflects its connection to CAT in this sentence." (verbatim)
8. Close: "Meaning is a position in vector space." / "Similar meanings usually sit close together." Nothing after.

```text
LESSON: vector-space
CANDIDATE: Prompts/vector-space-1.mp4 (4:14.47)
VERDICT: REPAIR (one wrong number; otherwise the best Understand AI roll so far)
TEACHING POINTS:
  1 embeddings/question — RICH   — 0:00–0:14 "if the numbers change, how do they still represent meaning?"
  2 Board 1 cities      — RICH with one WRONG number — 0:17–0:56: "Mountain View sits at 37 north, 120 west." (0:24.76–0:27.54; the board and Markdown say 122° W); Dallas and New York correct; both new positions answered aloud (0:47, 0:52)
  3 Board 2 / closest   — RICH   — 0:56–1:05, verbatim line at 1:02.10
  4 Board 3 drinks      — RICH   — 1:12–1:54: seven dimensions named in order, all three rows read digit by digit, verbatim Coke/Pepsi line at 2:10.88, definition verbatim at 1:45.76–1:53.72 including "That's vector space."
  5 Board 4 map/mystery — RICH   — 1:54–2:34: two neighborhoods, long lines to coffee, mystery ratings read, "its closest match is Pepsi"
  6 Board 5 distance    — RICH   — 2:34–3:12: first six match, Citrus 9 vs 10 gap of 1, vs Coke's 1 gap of 8, verbatim "closest to Pepsi's" at 2:51.06, verbatim "Smaller gaps" at 2:56.08, thousands of dimensions learned in training, similar meanings nearby. Additions: "This is how the math of meaning works." (2:53, harmless); "In this massive architecture" (3:06, one banned word)
  7 Board 6 IT          — RICH   — 3:13–4:05: the sentence, IT ambiguous, starting numbers 0.12 negative 0.34, the layers update, 0.41 0.06, lands next to cat; the required line spoken as "Its new position reflects its connection to cat in the sentence." (4:01.86–4:04.92; "the" for "this")
  8 close               — RICH   — 4:06.12 / 4:09.06, exact, nothing after
HARD REQUIREMENTS: 7 of 8 exact; the eighth one word off ("in the sentence" for "in this sentence").
ERRORS: 0:24.8 "37 north, 120 west" for Mountain View (should be 122 west). 
SOURCE_QA: PASS
ADDITIONS: "This is how the math of meaning works." worth keeping.
REPAIR PLAN:
  a. Replace roll 1's 24.60–27.60 ("Mountain View sits at 37 north, 120 west.") with roll 2's 22.20–26.90 ("Mountain View sits at 37 degrees north, 122 degrees west,"; small.en 22.36–26.72; the trailing comma continues into roll 2's "Dallas", so take the tail at the 26.72 word end plus ~0.15 s). Audio-only graft under Board 1 (our picture); same-day voice; level-match. Roll 2 says "degrees" where roll 1 does not; acceptable, and the live also says "degrees".
  b. Optional: the "in the sentence"/"in this sentence" miss has no donor (roll 2 says "contextual connection to cat", the live "its specific contextual connection"). Accept as TAUGHT.
  c. Cuttable production phrases, David's call: "This map displays three cities, describing their physical positions using two numbers, latitude and longitude." (0:17.9–0:23.8; carries the latitude/longitude intro, so recommend keeping), "This chart breaks down three everyday drinks" (1:12.9), "This map of drink similarities visualizes those seven dimensions." (1:54.6), "This tabletop map visualizes how a specific sentence behaves in that space." (3:13.2). None is wrong; the prompt asked for none of them. Recommend keeping all four; they are the board introductions the Edit Spec wants a board to arrive on.
EDITING NOTES:
  Notebook renders of all six boards replaced by the canonical JPGs (0:20–0:37 Board 1 with its own zooms; 0:40–0:59 Board 2; 1:16–1:47 Board 3; 1:56–2:11 Board 4; 2:16–2:49 Board 5; 3:16–4:02 Board 6). The roll's own zooms and yellow highlights on the boards never ship.
  Invented diagrams to cover: 0:04–0:15 layers/embedding strip under the opening (hold or let Board 1 arrive at "This map displays", 0:17.9); 1:08–1:12 "Vector Space: Mapping Meaning / High-Dimensional AI Embedding (Thousands of Numbers)" (cover: Board 3 arrives at "This chart", 1:12.9, so hold the 1:04 drawing through it); 1:48–1:53 "2D Coordinate Space / 7-Dimensional Feature Vector" with invented values 8.5, 2.0… and a sparkling-citrus profile (under the definition sentence: hold Board 3 through it or bring Board 4 in early at 1:45.8); 3:00–3:07 "High-Dimensional Vector Space / Token Embedding Vector 1,536 Dimensions" (a real model's dimension count printed on screen, which the prompt bans: cover with the 3:08 network drawing held back to 2:58, or hold the 2:52 distance drawing).
  Paper-craft scenes kept: 1:00 map collage, 1:04 circles, 2:12 two cans and a cup, 2:52 MATHEMATICAL DISTANCE, 4:04 IT/CAT tiles. No photographs; Board 6's photo-real cat and dog are the page asset's own.
  Notebook's spinner at 4:12 never renders.
LISTENING: small.en for every required line, the Mountain View coordinate, "vectors" at 2:35 (base.en heard "victors"; small.en hears "vectors"), and the close.
```

```text
LESSON: vector-space
CANDIDATE: Prompts/vector-space-2.mp4 (4:06.87)
VERDICT: REROLL (donor only)
TEACHING POINTS: complete and TAUGHT, with the correct Mountain View coordinate (0:23 "37 degrees north, 122 degrees west"), all rows read, the gaps worked, IT's numbers. Register slips: "Instead of hand-coding traits like sweetness or fizziness" (2:50, invented mechanism aside), "Changing the numbers is exactly how an AI tracks shifting context" (3:53), "massive gap".
HARD REQUIREMENTS: 0 of 8 as written: "When nothing matches exactly…" replaced by "you can systematically find the closest relative match"; "more similar profiles" → "share a much more similar profile"; the definition → "plot a unique position in a seven-dimensional vector space" (no "That's vector space"); "closest to Pepsi's" → "its closest match is immediately Pepsi"; "Smaller gaps" → "Smaller numerical gaps mean closer spatial positions"; the IT line → "mathematically reflect its contextual connection to cat"; the two closing lines joined into one sentence with "and".
ADDITIONS: the Mountain View sentence is the donor for roll 1's repair a.
```

```text
LESSON: vector-space
CANDIDATE: course-assets/vector-space/vector-space.mp4 (3:52.90, live v5)
VERDICT: superseded by roll 1
TEACHING POINTS: the shape of the lesson is there but the worked content is thin against the current page: the three drink rows are not read (only "both scoring 9 in sweetness and 10 in fizz"; coffee "a 1 and a 0"), the mystery drink's ratings are never spoken ("its own seven-number rating vector"), IT's starting and updated numbers are not spoken, and the second new-position answer is compressed. Register is the old formal one ("numerically quantify… across multiple dimensions simultaneously", "Distance in vector space is simply a matter of comparing numerical gaps in matching positions"). Board 1's Mountain View coordinate is spoken correctly (0:36 "37 degrees north and 122 degrees west").
HARD REQUIREMENTS: 2 of 8 (the closing lines, 3:43.9 and 3:46.6).
ERRORS: none factual.
```

```text
BEST-OF PLAN: vector-space
BASE: Prompts/vector-space-1.mp4 (7 of 8 required lines exact, every number on every board spoken, the lesson's voice)
  Mountain View coordinate — roll 1 WRONG @0:24.8 "37 north, 120 west" | roll 2 RIGHT @0:22.4 "37 degrees north, 122 degrees west" | live RIGHT @0:36 (inside a longer clause) — TAKE roll 2 (under Board 1)
  Everything else — KEEP roll 1
GRAFTS: 1, audio-only under Board 1. No cuts unless David wants the four "This map/chart" lead-ins out.
```

## Proposed edit plan (for David's approval before the first build; Edit Spec 1b; onsets from small.en)

| Board | Highlighting sequence | Camera | Reason or exception |
|---|---|---|---|
| Three Cities, Two Coordinates Each | city label rings Mountain View 0:24.8, Dallas 0:28.9, New York 0:31.5; banner ring at "They share the same two dimensions" 0:34.9 | full board (compact) | board arrives at "This map displays" 0:17.9 |
| Use the Map to Find the Closest City | the two new-position labels as one ring at "Suppose you are handed" 0:37.2; Mountain View pair ring at 0:47.7; New York pair ring at 0:52.1; banner ring at the verbatim line 1:02.1 | full board (compact) | leaves at 1:05.8 ("We can map abstract meaning") for the paper-craft drawings |
| Three Drinks, Seven Dimensions Each | header row ring at "sweet, bitter, fizz" 1:22.2; Coke row 1:28.5; Pepsi row 1:34.4; Coffee row 1:39.6; banner ring at "Coke and Pepsi have more similar profiles" 2:10.9 is on Board 4's span, so on Board 3 the banner rings at the definition 1:45.8 instead: unmarked | full board (compact) | the three rows read at full view |
| A Map of Drink Similarities | soft drinks neighborhood ring at 1:58.4; hot drinks ring at 2:03.8; banner ring at 2:10.9 (the verbatim Coke/Pepsi line) | full board (compact) | |
| Use the Map to Find the Closest Drink | Mystery Drink card ring at 2:24.9; Pepsi pair ring at 2:31.2; Citrus cells (mystery + Pepsi) at 2:40.3; Coke's Citrus at 2:47.3; banner ring at 2:50.9 | full board (compact) | |
| How Context Changes IT's Position | illustration walk (no rings): establish 3:13.2; glide to the starting IT at 3:31.5; follow the path at 3:42.3; land on the animals neighborhood at 3:55.9; banner ring at 4:01.9 | camera walk, then full | photo-real page asset; the Avoid opener's Read the Water pattern |
| Standard close | none | full | from 4:06.1 |

Pauses (Edit Spec 6): none proposed; the roll's own gaps (0.4–0.6 s) already breathe, and the board-to-drawing hand-offs land on its scene cuts.

## Build: v6 review candidate (2026-09-22, from the approved plan: one graft, no cuts, the four lead-ins kept)

**Candidate:** `Prompts/vector-space-v6.mp4` (7691 frames, 4:16.37, sha256 5cf9fd0915e291e3…), a full production pass on roll 1
(`scripts/video/build_vector_space_v6.py`, folder `build-v6/`). Output frames below; source frames are in the script.

**Timeline.** 0–535 (0:00–0:17.8) Notebook's opening drawing (knowledge → embedding → layers, origin axes). 535–1151 (0:17.8–0:38.4)
Three Cities at the roll's own cut: ring Mountain View 0:24.9, Dallas 0:29.7, New York 0:32.6, banner 0:35.9. **Graft a** sits at
**output 740–884 (0:24.67–0:29.47)**: roll 2 frames 684–828 (22.80–27.60, "Mountain View sits at 37 degrees north, 122 degrees
west,") replaces roll 1 frames 740–852 (24.67–28.40, "…37 north, 120 west."), cut inside the floors either side; **gain +1.64 dB**
(speech RMS against roll 1's Dallas/New York sentences: −15.9 vs −16.2 dBFS after gain); roll 2's gap floor is −64.5 dBFS against
roll 1's −54.0, so roll 1's matched room tone is bedded under the whole donor and its 0.26 s lead-in / 0.43 s tail blended over
their full length (no floor cliff: −53.8 / −56.5 / −53.0 / −56.8 dBFS across the two seams); the donor peaks at −0.01 dBFS like
roll 1, so 253 samples above −1 dBFS are bent with a tanh knee instead of hard-clipping (0 full-scale samples in the span). Net
+32 frames; everything after is 1.07 s later. 1151–1723 (0:38.4–0:57.4) Closest City at the roll's cut: both NEW POSITION labels
0:41.2, Mountain View pair 0:48.8, New York pair 0:53.2. 1723–1894 the roll's paper map collage (kept, under "The new coordinates
don't match…"). 1894–2009 Closest City again, banner ring at the verbatim line 1:03.2. 2009–2221 the roll's three-circles drawing,
re-timed over its invented Mapping Meaning card. 2221–3474 (1:14.0–1:55.8) Three Drinks at the roll's cut: header 1:23.3, Coke
1:29.8, Pepsi 1:35.7, Coffee 1:40.9, unmarked from the definition 1:46.8 (covers the invented 2D / 7-Dimensional Feature Vector
drawing). 3474–4086 (1:55.8–2:16.2) Drink Similarities at the roll's cut: soft drinks 1:59.6, hot drinks 2:05.1, banner at the
verbatim Coke/Pepsi line 2:12.1 (covers the cans). 4086–5246 (2:16.2–2:54.9) Closest Drink from "Now imagine": mystery card 2:26.1,
Pepsi point 2:32.3, citrus cells (mystery + Pepsi) 2:41.4, Coke's citrus 2:48.6, banner at the verbatim line 2:52.1. 5246–5383
MATHEMATICAL DISTANCE (re-timed from 171.00). 5383–5630 the network drawing held back over the invented Point A/B/C → **1,536
Dimensions** card; 5630–5834 the network's own span. 5834–7404 (3:14.5–4:06.8) How Context Changes IT's Position at the roll's
cut: establish full, glide to the starting IT 3:32.6, follow the path 3:43.4, land on the animals neighborhood 3:57.0, pull back
4:01.9–4:02.9, banner ring 4:02.9. Close from 4:06.8 (inside the floor before "Meaning is a position"), audio to 4:12.4, 120-frame hold.

**Checks (Edit Spec 10):** 1. decoded 7691 = plan; every leg decoded its span. 2. guard 16/16 at every row boundary
(`build-v6/guard/`), strips inspected: each first frame after a boundary is already the destination (Board 1's two graft seams are
inside its continuous leg). 3. no pauses added; silences on the finished file: 24.29–24.94 (0.65 s before the grafted sentence;
roll 1's own gap was 0.61), 29.18–29.64 (0.47 s after it; roll 1's was 0.52), 246.63–247.09 between the closing lines, hold
252.11–256.38. 4. every settled ring frame inspected (`states-*.jpg`, `state-*.jpg`): label rings hug the measured boxes, row rings
on the rows' own border lines, circle rings on the fill extents, chip rings on the chip borders, banners edge to edge. 5. Boards 1–5
compact and still, Board 6 a walk with no rings; every board opens whole and unmarked (Board 1 7.1 s, Board 2 2.9 s, Board 3 9.3 s,
Board 4 3.8 s, Board 5 9.9 s, Board 6 19.2 s; the banner leg at 1:03.1 is a return to a board already seen whole). 6. small.en on the
finished file: "…using two numbers, latitude and longitude. Mountain View sits at 37 degrees north, 122 degrees west. Dallas is at
33 north, 97 west. New York City is at 41 north, 74 west. They share the same two dimensions." and "…landing it next to cat in the
animal's neighborhood. Its new position reflects its connection to cat in the sentence. Meaning is a position in vector space.
Similar meanings usually sit close together.", nothing after. `kept-notebook-spans.jpg` samples every kept Notebook span: the 1,536
Dimensions card, the 7-Dimensional Feature Vector drawing and the Mapping Meaning card never appear. Corner mark: 884 cloned, 622
inpainted, 0 declined. Protected files (both rolls, live video, six boards, close JPG, lesson) unchanged. 7. Longest unbroken board
run 100.8 s (Boards 3–5, 1:14.0–2:54.9): the plan had no interleaves there and the roll's only drawings in that span are the
invented 2D/7-D card and the 4 s cans under the verbatim banner line.

**Deviations from the plan (all in the manifest):** Board 2's first ring is at 0:41.2 (the first spoken coordinate) rather than at
"Suppose" — the board arrives at the roll's own cut (37.30), which is also the measured onset of "Suppose", so a ring there would
open it ringed. Board 2 is split around the roll's own paper collage (rings leg, collage, banner leg) and the circles drawing is
moved to cover the Mapping Meaning card. Board 4 and Board 6 hold through their verbatim lines, so the cans (131.0–135.1) and the
IT/CAT tiles (241.9–245.7) are not shown. Graft edges follow the measured word edges (roll 2's "Mountain" starts 23.06, not small.en's
22.36), so the graft adds 1.07 s rather than ~1.7 s. Ring onsets use the small.en word stamps where the table quoted segment starts.

**Not auditioned by ear:** the graft's two seams at 0:24.7 and 0:29.5 (roll 2's voice against roll 1's Dallas sentence), the
close transition at 4:06.8.

**At ship (not authorized yet):** copy to `course-assets/vector-space/vector-space.mp4`, cache key `20260922ship6` on `vectorspace` (currently 20260917ship1),
pill 3 min → 4 min (4:16), manifest video hash/bytes. Rolls 1 and 2 and the live v5 stay until David says otherwise.

## v7 (2026-09-22): the Three Drinks rows are no longer read

David, after v6: the map boards keep their numbers, but the Three Drinks table should not be read digit by digit; the point is that
Coke and Pepsi are alike and coffee is not. Materials changed to match: `lessons/vector-space.md` Board 3 drops the three "ratings
are" lines for "Look across the rows. Coke's and Pepsi's numbers are nearly the same. Coffee's numbers are different in almost every
column." (the banner line stays); `Prompts/vector-space-video-prompt.txt` says do not read the rows digit by digit, read numbers only
on the map boards. `Prompts/vector-space-v7.mp4` (3:59.27, 7178 frames, sha256 2d50b55500a7e950…) = v6 plus one cut: roll 1
88.43–105.53 ("Coke receives the following ratings… Coffee has a radically different profile, 1, 9, 0, 9, 8, 10, and 0."), out inside
the 88.18–88.67 gap after "citrus.", in inside the 105.34–105.90 gap before "Just as"; the three row rings go with it, the header ring
stays. Script `scripts/video/build_vector_space_v7.py`, folder `build-v7/`. Guard 17/17, decoded 7178 = plan, corner mark 0 declined,
protected files unchanged. Transcript across the cut: "We measure them by sweet, bitter, fizz, heat, caffeine, dark, and citrus. Just
as latitude and longitude give a city a position…". v6 deleted (never handed over as a ship candidate). Listen: 0:24.7, 0:29.5 (graft),
1:29.3 (the row cut), 3:50.3 (close). At ship: cache key 20260922ship6, pill 4 min (3:59).

## Decision (2026-09-22, David): the live video stays

After David rewrote the page's opening (an exact match isn't necessary; the relationships between the numbers matter; nearby
positions can represent similar meanings) and dropped the digit-by-digit read of the drinks table, the live v5 was re-evaluated
against the new page. It teaches the lesson; its drinks table is already read the new way ("both scoring 9 in sweetness and 10 in
fizz… coffee, scoring a 1 and a 0… entirely different"); boards hash-match. Gaps noted and accepted: the new opening hinge is
delivered by the map example at 1:05 and 3:00 rather than stated up front; "values learned during training" unspoken; dimension
names, the mystery ratings, IT's numbers and two cities' coordinates shown on boards rather than spoken; a "12,288 DIMENSIONS" card
on screen 3:04–3:15 (a real model's count; a visual-only repair if ever wanted). Rolls 1 and 2 are retained as raw rolls; the v6/v7/v8
candidates, their build scripts and build folders were removed on David's instruction. Two of eight required lines as written; the
review stands as the record of why that does not decide it here.
