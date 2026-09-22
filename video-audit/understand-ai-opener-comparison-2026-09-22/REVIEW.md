# Understand AI opener: two new rolls against the live video (2026-09-22)

Narration review under `scripts/video/NARRATION-REVIEW.md`. Lesson authority: `index.html` OpenerFoundationsSection
(line 3579) and the rebuilt upload Markdown `lessons/Opener-Understand.md` (2026-09-21 recipe, seven required-verbatim
lines in `Prompts/opener-understand-video-prompt.txt`). Transcripts, scene cuts, holds and contact sheets for all three
files are in this folder (`grade_bundle.py`, faster-whisper base.en; uncertain spans and both closes re-heard with
small.en, word timestamps below).

Rolls: `Prompts/understand-ai-opener-1.mp4` (2:19.97) and `Prompts/understand-ai-opener-2.mp4` (2:37.57), both rolled
2026-09-22 on the new kit. Live: `course-assets/understand-ai-opener/understand-ai-opener.mp4` (2:32.93, v7 shipped
2026-09-16, a visual retrofit of the pre-recipe v4 roll).

## Teaching points (page order)

1. The card, four lines exactly: "It’s not magic. Not a person. Not normal software. It’s its own kind of thing." (verbatim)
2. PhD expert one moment, six-year-old mistake the next; how can the same tool do both; understanding what happens inside explains why.
3. The car: good at driving without opening the hood; knowing what is underneath tells you what it can do and why it might go wrong; the same goes for AI.
4. "Knowing how it works helps you Be Smarter Than the Tool." (verbatim)
5. Under the Hood board: the hood is up, the machinery is in plain view.
6. "This section takes you inside the machine, one piece at a time." (verbatim)
7. Some of this is new; each piece builds on the one before; no need to memorize every term.
8. "The goal is to understand how your words become an answer." (verbatim)
9. The section map: its title, then five topics in order, each with its one-line explanation.
10. "Each piece builds on the one before it." (verbatim)
11. Close: "The machine won’t feel like magic anymore." then "Take it a piece at a time." Nothing after. (verbatim)

```text
LESSON: understand-ai-opener
CANDIDATE: Prompts/understand-ai-opener-1.mp4 (2:19.97)
VERDICT: REPAIR
TEACHING POINTS:
  1 card                — RICH    — 0:00.0–0:08.4 "What kind of thing is AI? It's not magic, not a person, not normal software. It's its own kind of thing."
  2 expert/six-year-old — TAUGHT  — 0:08.4–0:24.5; "How can the exact same tool do both?" then "The only way to answer that is to look inside and see what is actually happening." (paraphrase of "understanding what happens inside helps explain why"; meaning intact)
  3 car analogy         — RICH    — 0:24.5–0:36.9, the page's sentences almost word for word, ending "The same goes for AI."
  4 Be Smarter line     — RICH    — 0:47.9–0:51.4
  5 hood up, machinery  — TAUGHT  — 0:43.9–0:47.9 "The hood is up and the machinery underneath is in plain view."
  6 section line        — RICH    — 0:51.4–0:55.4
  7 new / builds / memorize — RICH — 0:55.4–1:01.9; re-heard with small.en: "You don't need to memorize every term." (base.en had garbled it)
  8 goal line           — RICH    — 1:01.9–1:05.9
  9 map title + 5 topics — RICH   — "Understand AI." 1:12.4; topics 1:21.9, 1:27.9, 1:34.4, 1:41.4, 1:49.4, each with its full one-liner in the board's words
 10 each piece builds   — RICH    — 1:56.9–1:59.4
 11 close               — line 1 RICH 2:10.1–2:12.2; line 2 WRONG-wording 2:12.8–2:16.3 "Just remember to take it a piece at a time, and it will all make sense."
HARD REQUIREMENTS:
  "It’s not magic. Not a person. Not normal software. It’s its own kind of thing." — MET — 0:02.4–0:08.4 (spoken as one run, as the Markdown carries it)
  "Knowing how it works helps you Be Smarter Than the Tool."                        — MET — 0:47.9
  "This section takes you inside the machine, one piece at a time."                 — MET — 0:51.4
  "The goal is to understand how your words become an answer."                      — MET — 1:01.9
  "Each piece builds on the one before it."                                         — MET — 1:56.9 (also 0:57.3 inside point 7, as the page has it)
  "The machine won’t feel like magic anymore."                                      — MET — 2:10.1
  "Take it a piece at a time."                                                      — MISSED — wrapped in "Just remember to … and it will all make sense."
  Nothing spoken after the close                                                    — MET (the wrap is inside the line, not after it)
ERRORS: none factual. Wording additions the prompt forbade, all cuttable at sentence gaps:
  A 0:36.9–0:43.9 "If you want to use this technology effectively, you have to look past the clean interface and examine the actual mechanics driving it." (own Notebook scene 0:36.90–0:44.27)
  B 1:05.9–1:12.4 "We are simply going to track the path of your input, watching how the machine breaks it down and constructs a reply." (under the Under the Hood span; Notebook's tokens/weights/probability diagram sits here)
  C 1:14.4–1:21.9 "These numbered steps aren't a system architecture diagram. They represent the chronological sequence we will use to learn this material." (speaks the banned framing to deny it; under the map)
  D 1:59.4–2:09.9 "By tackling these concepts in this specific order, we prevent the technical details from piling up. You master a foundation, and then you step up to the next level." (the summary after the map the prompt banned; own Notebook scene 1:59.87–2:10.20)
SOURCE_QA: PASS. (The page's fifth topic reads "How AI Builds an Answer: How AI builds an answer, why answers vary…", so the roll's repetition at 1:49.4 is the page's, not the roll's.)
ADDITIONS: none worth keeping.
REPAIR PLAN:
  Close line 2: replace roll 1's 132.83–136.34 ("Just remember to take it a piece at a time, and it will all make sense.") with the live video's own standalone beat "Take it a piece at a time." at 148.06–149.14 (small.en word stamps; sits after a 0.76 s gap and ends the file, so it is a whole beat with a falling cadence). Same Notebook voice. Levels: roll 1 close line mean −13.9 dB, donor mean −15.8 dB (raise donor about +1.5 dB); noise floors −31.1 vs −35.4 dB in the adjacent gaps, no cliff. The join sits under the standard close board, our picture. Alternative if David prefers a single-source file: trim roll 1's own phrase to "take it a piece at a time" (133.68–135.00), but "time," carries a continuing cadence there; the live donor is the cleaner ending.
  Cuts A–D at the silences bracketing each sentence: A 36.7→44.1, B 66.0→72.7, C 74.5→82.2, D 119.5→130.0 (silencedetect −35 dB; see silences list). About 31.5 s out; projected runtime about 1:46, pill 2 min.
EDITING NOTES:
  Notebook's card render (0:00–0:24) carries its own yellow underline at 0:08; replaced by the canonical card with our rings.
  Notebook's car drawings 0:28–0:36 carry invented printed labels ("SURFACE INTERFACE | OPERATIONAL MASTERY", "65 MPH", "Combustion • Transmission"): drawn scenes, no people, no logos; acceptable to keep under the car analogy, or cover with the canonical Under the Hood board from "The same goes for AI." if David prefers.
  The invented mechanism diagrams (0:36 "AI UNDER THE HOOD | INTERNAL MACHINERY & DUAL OUTPUTS"; 1:08 "TOKENIZE / RELATIONS & WEIGHTS / PROBABILITY"; 2:04 "AI Core Concepts / Structured Learning Sequence"; 2:08 "ADVANCED AI & REASONING / FOUNDATION: CORE MASTERY") all sit under cuts A, B and D or under the canonical board span, so none survives the build.
  Torn-paper circuit collage 0:40–0:44 (photo-style) is inside cut A.
  Faceless Under the Hood variant on screen 0:44–1:05: replaced by the canonical board.
  Map 1:16–1:59 with Notebook's yellow highlights and zooms: replaced by our render at full view with row rings.
  Corner mark present throughout; the build removes it (Edit Spec 8). Frame 0 is the card, no stock image.
LISTENING: small.en re-hear confirms "memorize every term" (0:59.8–1:01.7) and the exact close wording. Not yet heard by ear: the levels match on the donor join and cadence at each of the four cuts; David or the build's transition_guard pass should listen to 0:36.7, 1:06.0, 1:14.5, 1:59.5 and the close.
```

```text
LESSON: understand-ai-opener
CANDIDATE: Prompts/understand-ai-opener-2.mp4 (2:37.57)
VERDICT: REROLL (rejected; roll 1 is the base)
TEACHING POINTS:
  1 card                — WRONG-wording — 0:06.6–0:15.3 "It's not magic. It is definitely not a person. And it doesn't run like normal software. It is entirely its own kind of thing." (the v4 adverbs the prompt named as banned); opens 0:00 with production talk "Let's look at this first board"
  2 expert/six-year-old — TAUGHT  — 0:15.3–0:28.7; then 0:28.9 "The answer comes down to what is happening inside the processor." (invented mechanism word)
  3 car analogy         — TAUGHT  — 0:32.5–0:54.2, heavily reworded ("highly capable driver", "The exact same logic applies to the internal workings of AI.")
  4 Be Smarter line     — MISSED  — 0:54.2 "Knowing how the mechanics actually operate is the only way to be smarter than the tool."
  5 hood up             — TAUGHT  — 0:58.9 "put the hidden machinery of AI in plain view"
  6 section line        — MISSED  — 1:04.5 "We'll take you inside the machine, one piece at a time."
  7 new / builds / memorize — TAUGHT — 1:08.4–1:18.5 ("write down or memorize every technical term")
  8 goal line           — MISSED  — 1:18.5 "your only goal is to simply understand the specific path your own words take to become a fully generated answer."
  9 map title + topics  — THIN/TAUGHT — title not spoken ("Here is the map we will use…" 1:27.0); topics called "Step one … step five", explanations paraphrased ("chopped up into tokens and designed numerical values")
 10 each piece builds   — MISSED  — 2:19.7 "this is a strict sequence. Every piece relies directly on the last." (also the banned sequence framing)
 11 close               — MISSED both — 2:27.6 "Once you see the math in action, the machine won't feel like magic anymore." / 2:32.3 "We just have to take it a piece at a time."
HARD REQUIREMENTS: 6 of 7 verbatim lines MISSED; only the card's meaning survives and not its words.
ERRORS: "inside the processor" 0:28.9 (not the lesson's claim); "strict sequence" 2:22.4 contradicts the learning-order guardrail.
SOURCE_QA: PASS
ADDITIONS: none worth keeping.
REPAIR PLAN: none; no beat here beats roll 1's.
EDITING NOTES: not assessed; the roll does not proceed.
LISTENING: transcript only (base.en); nothing here changes the verdict.
```

```text
LESSON: understand-ai-opener
CANDIDATE: course-assets/understand-ai-opener/understand-ai-opener.mp4 (2:32.93, live v7 of 2026-09-16)
VERDICT: superseded by roll 1 (as a narration it would be REPAIR-at-best against the current materials)
TEACHING POINTS:
  1 card                — WRONG-wording — 0:00–0:11.9 "It's not magic, it's not a person, and it's definitely not normal software. It is entirely its own kind of thing, operating by a completely different set of rules." (the known v4 paraphrase, flagged in the 2026-09-16 review)
  2 expert/six-year-old — RICH-with-additions — 0:11.9–0:36.8 ("handing you brilliant insights in seconds", "glaring illogical mistake")
  3 car analogy         — TAUGHT  — 0:36.8–0:53.3, reworded ("diagnose why it suddenly stalls on the highway"; "artificial intelligence")
  4 Be Smarter line     — MISSED  — 0:58.9 "Knowing how it works helps you use it thoughtfully, ensuring you remain smarter than the tool you're operating."
  5 hood up             — TAUGHT  — 0:53.3 "Knowing what's happening under the hood gives you a clearer picture…"
  6 section line        — MISSED  — 1:06.5 "We are going to take you inside the machine, but you don't need to memorize a dictionary of technical terms."
  7 new / builds / memorize — TAUGHT — 1:06.5 (memorize); "each topic builds directly on the one before it" arrives only at 2:22
  8 goal line           — MISSED  — 1:12.9 "Our single goal here is to help you understand a specific transformation, how the words you type turn into the answer you receive."
  9 map title + topics  — TAUGHT  — title not spoken ("This road map shows…" 1:22.0); learning-order guardrail spoken well at 1:25.2; five topics paraphrased but complete
 10 each piece builds   — MISSED  — 2:22 "each topic builds directly on the one before it"
 11 close               — line 1 MET 2:25.5; line 2 MET as words, 2:28.1 "Take it a piece at a time." (clean standalone beat; the donor for roll 1)
HARD REQUIREMENTS: 5 of 7 verbatim lines MISSED. Built before the verbatim list existed, so this is measured against the current materials, not its own kit.
ERRORS: none factual.
SOURCE_QA: PASS
ADDITIONS: the spoken learning-order guardrail at 1:25.2 is good teaching; roll 1's cut C tried the same and said it worse. Not needed once C is cut (the map's banner line carries the idea).
REPAIR PLAN: not proposed; roll 1 replaces it.
LISTENING: close re-heard with small.en for the donor stamps.
```

```text
BEST-OF PLAN: understand-ai-opener
BASE: Prompts/understand-ai-opener-1.mp4 (six of seven verbatim lines exact, the lesson's own sentences throughout, complete coverage; the only miss is the wrapped second closing line)
  Close line 2 — roll 1 WRONG-wording @2:12.8 "Just remember to take it a piece at a time, and it will all make sense." | roll 2 MISSED @2:32.3 "We just have to take it a piece at a time." | live MET @2:28.1 "Take it a piece at a time." — TAKE live (under the standard close board)
  Every other point — roll 1 RICH or TAUGHT; roll 2 weaker on all; live weaker on 1, 4, 6, 8, 10 — KEEP roll 1
GRAFTS: 1, under the close board. Plus four cuts (A–D) of roll 1's own additions, all at sentence silences.
```

## Proposed edit plan (for David's approval before the first build; Edit Spec 1b)

| Board | Highlighting sequence | Camera | Reason or exception |
|---|---|---|---|
| What Kind of Thing Is AI? | four gold line rings at the spoken onsets: "It's not magic" 0:02.4, "not a person" and "not normal software" (word stamps to be measured at build), "It's its own kind of thing" 0:06.3; last ring holds through "…do both?" and the look-inside line | compact still, the page's card crop as v7 used (`canvas-kind-crop`) | board holds 0:00–0:24.5, leaving on Notebook's own cut to the car drawing at 0:24.6 |
| Under the Hood (canonical, with the students) | unmarked, then banner ring at "Knowing how it works helps you Be Smarter Than the Tool." 0:47.9–0:51.4, then unmarked | full board | on screen from "The hood is up" (0:43.9, the join after cut A) through "…become an answer." (1:05.9, cut B follows); replaces the faceless variant and Notebook's diagram |
| Understand AI (section map) | whole board at "Understand AI." 1:12.4 (title ring optional), then row rings at 1:21.9, 1:27.9, 1:34.4, 1:41.4, 1:49.4, then banner ring at "Each piece builds on the one before it." 1:56.9 | full view throughout, as the shipped v7 (rows legible at full view) | leaves at the close (cut D removes the summary scene) |
| Standard close | none | full | from "The machine won't feel like magic anymore." (2:10.1 on the roll); the grafted "Take it a piece at a time." follows after about 0.7 s; close board is the literal last frame |

Narration changes: cuts A–D and the one close graft, exactly as in roll 1's REPAIR PLAN above.

Selective pauses (Edit Spec 6; existing gaps from silencedetect, all 0.4–0.7 s; proposal adds about 2.4 s):
- after the card's last line, 8.09–8.71 (0.62 s) → about 1.3 s before "Sometimes…"
- before "Think about driving a car.", 24.07–24.79 (0.72 s) → about 1.3 s
- before "Understand AI." at the map (the join after cut B, 72.5) → about 1.2 s
- before "The machine won't feel like magic anymore." (the join after cut D, 130.0) → about 1.2 s
No other pauses; the roll's natural gaps are even.

## Notes for the kit

Roll 1 is the first Understand AI roll on the rebuilt materials and the first opener roll to land the card's four lines
and five of the six other verbatim lines. Its failures are all the prompt's stated negatives being ignored once each
(one summary after the map, one denial of the "architecture" framing, two mechanism asides). Worth carrying into the
kit as the batch's pattern if the next lessons repeat it.

## Build: v9 review candidate (2026-09-22, David: "build it")

**Candidate:** `Prompts/understand-ai-opener-v9.mp4` (3240 frames, 1:48.00, 30 fps, sha256 70ad80142cba579e…). Built by
`scripts/video/build_understand_ai_opener_v9.py` from `Prompts/understand-ai-opener-1.mp4`; build folder `build-v9/`
(edit-manifest.json, legs, state sheets, guard strips, kept-span sheet). Review only: live video, both raw rolls,
lesson, and boards unchanged (manifest `protected_files_unchanged` all true). v8 was the same build minus the fix
below; it was never handed over and is deleted.

**Timeline (source frames of roll 1 → output frames):**
- 0–252 card, four line rings → 0–252; pause 18 (holds the ringed card); 252–739 card through "…actually happening." → 270–757; pause 15
- 739–945 Notebook car drawings (hood closed, hood open) → 772–978; 945–1097 hold of frame 944 (the hood-open drawing) → 978–1130
- cut A (1097→1324): "If you want to use this technology effectively… the actual mechanics driving it." removed
- 1324–1976 Under the Hood, canonical board, banner ring 48.14–51.44 → 1130–1782
- cut B (1976→2177): "We are simply going to track the path of your input…" removed; resume inside the natural gap before "Understand AI."
- 2177–2234 map: title → 1782–1839; cut C (2234→2460): "These numbered steps aren't a system architecture diagram…" removed
- 2460–3585 map: five topics (row rings at 82.32, 88.06, 94.74, 101.86, 109.74) and banner ring at 117.40 → 1839–2964; pause 21
- cut D (3585→3899): "By tackling these concepts in this specific order… step up to the next level." removed
- 3899–3978 "The machine won't feel like magic anymore." under the standard close → 2985–3064
- live v7 4432–4488 "Take it a piece at a time." (audio-only graft, +1.57 dB to match roll 1's close-line speech RMS) → 3064–3120; settled hold 120 → 3240

**v9 fix over v8:** the guard strip at 1130 showed Notebook's invented "AI UNDER THE HOOD | INTERNAL MACHINERY" diagram on
screen for the last twelve frames before the board. A per-frame scan against a clean hood-open frame found the diagram
dissolving in from source frame 945 (31.50 s), not at the 36.90 cut the scene list reported (the dissolve never spikes the
frame diff; TECHNICAL-RECIPES dissolve-onset rule). Frame 944 now holds from 945 to cut A under "…what the car can do and
why something might go wrong. The same goes for AI." The guard's 978 strip confirms the hold is seamless; the 1130 strip
shows the hood-open drawing to frame 1129 and the canonical board from 1130.

**Checks (Edit Spec section 10):**
1. Decoded 3240 frames = plan; each leg decoded its span exactly (render_legs assert).
2. `transition_guard.py` passed all ten declared boundaries (270, 757, 772, 978, 1130, 1782, 1839, 2964, 2985, 3064); strips
   inspected at 772 (card → Notebook's own fade-in of the car drawing), 978, 1130, 1782 (board → map at full view), 2985
   (map → close), 3064 (close held through the graft).
3. Pauses on the finished file (silencedetect −35 dB): 8.09–9.31 (1.22 s, plan ~1.26), 24.67–25.89 (1.22 s, plan ~1.30),
   98.54–99.73 (1.19 s, plan ~1.19); close hold 103.60–108.01. The gap before "Understand AI." is the roll's own 1.3 s
   with the narrator's breath intact (cut B resumes before the breath onset). Gap between the two closing lines 0.74 s.
4. Ring states inspected (`states-kind.jpg`, `states-hood.jpg`, `states-map.jpg`): four gold line rings tight to the card
   text at their spoken onsets; the Under the Hood banner ring for the Be Smarter line only; five row rings and the banner
   ring on the map, each tracing its row edge to edge. Artwork-scaled stroke (ken_burns_path.ring_px).
5. Density: card compact and still (page crop, as v7); Under the Hood compact and still, tall-board margins; map compact at
   full view, still. Every board opens whole and unmarked ≥ 2 s before its first ring (map: 2.2 s of output).
6. Corner mark: 358 kept Notebook frames cloned, 0 inpainted, 0 declined. Kept Notebook span (output 772–1130) sampled every
   30 frames (`kept-notebook-span.jpg`): car drawings only, no photographs, no diagrams; the torn-paper collage and all
   three invented diagrams are inside cuts A, B, D or under the board hold.
7. Transcript of the finished file (small.en) reads exactly the approved narration: all four additions gone, seven of seven
   verbatim lines exact, nothing spoken after "Take it a piece at a time."
8. Levels across the close graft: −15.0 dB mean before, −15.1 dB after (volumedetect on 2.7 s / 1.4 s windows).

**Not auditioned by ear (David):** the four cut joins at 0:36.6 (car drawing, mid-hold), 0:59.4 (into the map), 1:01.3
(before "One"), 1:38.5 (before the close), and the close graft at 1:42.5. Transcript and level checks do not certify them.

**At ship (not authorized yet):** copy to `course-assets/understand-ai-opener/understand-ai-opener.mp4`, cache key
`?v=20260922ship1` on `openerfoundations` (currently 20260916ship1), pill 3 min → 2 min (1:48), manifest video_assets
hash + bytes, then commit; David maintains the tracker.
