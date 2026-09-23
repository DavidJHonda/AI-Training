# One More Thing v11 — build verification (2026-09-23)

**Candidate:** `Prompts/one-more-thing-v11.mp4` — 6717 frames, 3:43.90, 1280x720, 30 fps.
**Built by:** `scripts/video/build_one_more_thing_v5.py`.
**Plan:** `video-audit/one-more-thing-comparison-2026-09-23/REVIEW.md`, approved by David ("build it").
**Supersedes:** v9 (roll 2), which predates the lesson rewrite. v10 was an intermediate render, deleted.
**Scope:** review candidate only. The live `course-assets/one-more-thing/one-more-thing.mp4` (v5) is unchanged.

## What was built

Roll 3 as the spine — the only roll that speaks all ten required verbatim lines — plus one replacement
graft and two cuts.

| Edit | Detail |
|---|---|
| Graft (audio only, under Board 1) | roll 3 **1628–1968** replaced by roll 4 **1803–2438**, +1.0 dB. Roll 3 named two of the six probabilities and never named the five picks; roll 4 reads the board completely, then runs into roll 3's verbatim "Spot was picked only once…" |
| Cut 1 | **3111–3206** — "This board shows how temperature alters odds." |
| Cut 2 | **4718–4831** — "This graphic illustrates how quickly that math adds up." |

All boundaries measured in silence. Level matched at the join, not file to file: the donor block is
−16.0 LUFS against roll 3's −14.5/−15.6 either side.

Three boards, all compact full view, all replacing roll 3's own recreations. Board 2 gained a
**Spot's 16%** ring in the High Temperature column, because roll 3 says "Spot falls to 16%" where
roll 2 said "Other shoots up to 39%".

## Most of this edit is covering roll 3's own drawings

Roll 3's narration is the best of the four rolls; its drawings are the worst.

| Span | What it shows | Fix |
|---|---|---|
| 76.10–103.97 (28 s) | "TOKEN SELECTION STRATEGY" with **STOCHASTIC SAMPLING**, "AUTOREGRESSIVE CONTEXT DYNAMICS", and a "Low Temp Concentrates AI Choice" bar chart whose invented numbers (37→88% for "the") **contradict our own Board 2** | Board 1 held to 81.87, then roll 2's branching-paths drawing, then Board 2 from 94.47 |
| 128.07–157.43 (29 s) | Formula plates "Softmax(Q Kᵀ/√d) V", "f(W₂·σ(W₁·x))", "10¹² Vector-Matrix Mult" over invented probabilities (130.87–134.03), then a black plate reading **"STATUS: LOCKED & FIXED (Inference)"** plus "SCALE: 1,000,000,000,000 **Parameters**" and "Internal Learned Parameter", legible for **22.4 s**. The plate fades in 0.6 s after the formula plates leave, so there is no clean window | Replaced wholesale with roll 4's weights scene |

Both borrowed pictures come from other rolls of this same lesson, and neither contributes audio:

- **Roll 2, 3152–3530** (12.6 s) — the branching-paths drawing: Max → is / chases / sleeps, Path A
  through chases → a ball → into the lake, then Path B through sleeps → on the sofa → until morning.
  David approved this exact drawing in v9 when he asked for graphics on this beat, and roll 3's line
  here ("a single different choice early on alters the entire subsequent response") is the same beat.
- **Roll 4, 6869–7481** (20.4 s) — the weights scene: the fixed weight matrix, "HYPOTHETICAL MODEL
  SCALE 1,000,000,000,000 — 1 TRILLION FIXED WEIGHTS", then "1 Trillion Fixed Weights × 2 FLOPs =
  2 Trillion Calculations" and "2,000,000,000,000 Operations → 1 Single Token". Nothing invented, no
  banned word prominent. Its last frame — the full equation — holds for the closing 9 s, under
  "roughly two calculations per weight", which is what it shows.

**Roll 2's version of the weights beat was checked and rejected**: it prints "TOTAL OPERATIONS:
1,680,046,647,230 ops / word", an invented figure that also contradicts the lesson's "about 2 trillion".

## Verification

| Check | Result |
|---|---|
| Decoded frame count | 6717, matches the manifest exactly (3:43.90) |
| Required verbatim lines | **10 / 10** in the output transcript |
| Banned narration | "this board/graphic/diagram/table shows", "randomness", "softmax", "inference" — all absent |
| Roll 3's status-plate signature in the weights leg | present in **0 of 882 frames** |
| `transition_guard.py`, 12 boundaries | pass, 0 failed |
| Engine corner mark | 2574 cloned, 304 inpainted, **0 declined** |
| Graft level on the finished file | 7082 speech RMS against roll 3's 7088 before and 6636 after — inside its neighbours |
| Pauses | all four frozen |
| Close | standard close card is the literal final frame |
| Protected files | all unchanged (live MP4, lesson Markdown, rolls 2 and 4, three board JPGs) |

Contact sheet: `contact-sheet.jpg`. Ring states: `states-*.jpg`. Output transcript: `transcript.txt`.

## Open for David

1. **The graft join wants your ear** — 54.27–75.43 in the finished file, the only place roll 4's voice enters.
2. **Roll 3's opening drawing** at 42.90–50.27 is headed "PROBABILISTIC TOKEN **SAMPLING**" and pairs the
   lesson's real probabilities with invented continuations ("…barking loudly.", "…running fast."). It is
   7.4 s and the header is small and pale, so I left it; covering it means bringing Board 1 in that much
   earlier and losing the hand-drawn "You could name him…" card that leads into it.
3. Runtime 3:43.90, so the pill stays "4 min".

## If it ships

Install as `course-assets/one-more-thing/one-more-thing.mp4`, bump the `inference` cache key in
`LESSON_VIDEOS` (currently `?v=20260918ship1`), and leave the pill at "4 min".
