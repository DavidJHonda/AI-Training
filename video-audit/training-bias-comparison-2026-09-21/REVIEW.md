# Training Bias — seven-way review and v4 build (2026-09-21)

Candidates: `Prompts/training-bias-1.mp4` (6:46) and `-2` (5:50) from 2026-09-18, `-3` (4:32) and
`-4` (3:39) from 2026-09-20, `-5` (4:29) and `-6` (4:20) from 2026-09-21, and the live v3
(`course-assets/training-bias/training-bias.mp4`, 4:06, shipped 2026-09-18 as a best-of over the
2026-09-08 spine). All six rolls came from the 2026-09-18 kit (no VOICE block). Transcripts and
sheets in the per-roll folders.

**Verdict: roll 6 is the base, no grafts, no narration cuts. Built as v4, then v5 and v6 (`Prompts/training-bias-v6.mp4`, 4:21) after David's ring notes: the three card boards are separate rounded cards, so each ring hugs its own card. v5 measured the cards against the stage colour and swallowed their drop shadows, so its rings floated 4–14 px outside the cards; v6 measures the cards from the illustration tile and the white area above the shadow. v6 matches v4 outside those three board spans.**

## Hard requirements (from the Markdown and the prompt)

| Requirement | roll 1 | roll 2 | roll 3 | roll 4 | roll 5 | roll 6 | live |
|---|---|---|---|---|---|---|---|
| Three prompts spoken word for word | MET | MET | MISSED ("don't fit the pattern" drops "you just gave") | MET | MET | MET | MISSED (all three paraphrased) |
| Chat: Claude's self-explanation is not evidence of the cause; hallucination not ruled out | MET | MET | MET | MET | MET, but "stale training is likely" | MET | MISSED (cause presented as stale, "the fix is straightforward") |
| RAG: material placed in the active context; no update to training data or weights | TAUGHT ("temporary information") | MISSED ("joins the internal information the AI can already use") | MET | MET | MET | MET | MISSED ("alongside the information it already knows"; no weights line) |
| Open on the cow example, no welcome or teaser | MISSED (teaser + "welcome to this explainer… I am absolutely pumped") | MISSED ("Welcome to this explainer. Let's jump right in") | MET | MET | MET | MET | MET |
| Closing lines verbatim, in order, nothing after | MET | MET | MET | MET | MET | MET | MET |

Rolls 1 and 2 are REROLL on register alone (chatty host voice, 5:50–6:46). Roll 3 is REROLL on the
prompt wording and two garbles ("Press the top portion", "utilizing"). The live v3 misses two hard
requirements. Rolls 4, 5, and 6 all pass; the beat table decides.

## Beat table: rolls 4, 5, 6

| Teaching point | roll 4 | roll 5 | roll 6 |
|---|---|---|---|
| Cow story: familiar photos, beach, fell apart, same animal different background | TAUGHT (compressed) | RICH | RICH |
| Shortcut: green grass means cow; learned the background | RICH | RICH | RICH ("absorbed the background instead of identifying the actual animal") |
| Narrow slice treated as the whole picture | RICH | RICH | RICH |
| Two traps: skewed = distorted, stale = old | TAUGHT | THIN (stale introduced only at 2:43) | RICH (0:36–0:46) |
| Banner: the model repeats the shape of its data | MISSING | RICH (1:21) | RICH (0:46, "An AI model repeats the shape of its training data") |
| Defaults / Blind Spots / Wrong Patterns | RICH | RICH | RICH |
| Consequences: demographic gaps, wrongful arrests | RICH | RICH | RICH |
| Cannot fact-check your way out; look for sameness; "every example looks alike… the model's default, not the world" | RICH | RICH | RICH ("data default, not reality") |
| Banner: the model often has the rest of the picture, doesn't lead with it | TAUGHT | RICH | RICH (1:59–2:08, spoken as the questions board's takeaway) |
| Training stops; after the cutoff is missing | RICH | RICH | RICH |
| Chat walk-through: questioned a true fact, web search, corrected, attributed to older information | TAUGHT (garble "staying") | RICH | RICH |
| Self-explanation is not evidence; cannot distinguish stale from hallucination | RICH | TAUGHT ("stale training is likely") | RICH (lesson wording) |
| When the date matters, verify with a current source | RICH | RICH | RICH |
| RAG named and expanded | RICH | RICH (heard as "REG" by the base model; "RAG" by the word model) | RICH (same) |
| Retrieve / Add to Context / Generate | RICH | RICH | RICH |
| Active context only; no training-data or weight update | RICH | RICH | RICH |
| More to read; no guarantee of reliability or interpretation | TAUGHT (interpretation dropped) | RICH | RICH |
| Runtime | 3:39 | 4:29 | 4:20 |

Roll 6 has no THIN or MISSING beat, the fewest register substitutions, and the cleanest chat
nuance. Roll 5 is the runner-up (one soft diagnosis). Roll 4 is complete but compressed and drops
the first banner. No beat in roll 4 or 5 is richer than roll 6's, so nothing is grafted.

## Per-roll block: training-bias-6 (BASE)

```text
LESSON: training-bias
CANDIDATE: Prompts/training-bias-6.mp4 (4:20)
VERDICT: KEEP
TEACHING POINTS: all RICH (see the beat table); the "historical conversation" framing the prompt asked for is carried as "this chat interface where a user tested a current fact" (TAUGHT)
HARD REQUIREMENTS: all MET; three prompts at 2:02.2, 2:08.9, 2:16.1 verbatim; close at 4:11.4 / 4:14.5 / 4:15.8, last word 4:16.8, nothing after
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: "questioning techniques", "mitigating stale data": register drift, harmless
REPAIR PLAN: none
EDITING NOTES: Notebook rendered Boards 2, 3, 4, 5 and the close; the post-only Board 1 is inserted over the shortcut beat; Notebook left Board 3's render at 2:19 for a latent-space drawing while the banner line was spoken, so the canonical board is held through 2:28 to ring it; drawn faces at 1:36 (facial-recognition diagram) are Notebook drawings, not photographs; corner mark on every frame
LISTENING: transcript read in full; audio not auditioned; the word "RAG" at 3:29.7 and 3:59.4 was heard as "REG" by the segment model and "RAG" by the word model, so confirm the pronunciation
```

## v6 build (`build-v6/`, script `scripts/video/build_training_bias_v6.py`; v4 and v5 superseded)

- SHA-256 `705abdb1ad860ea9b39b8baa52699a34ae7a5003761c184c8dcf73abf1045d70`; card rects x 41–524 / 558–1042 / 1076–1559, y 128–650 (skew, questions) and 128–609 (RAG); ring close-ups in `build-v6/ring-closeup-*.png`; six board seams re-guarded, pass.

## v5 build (superseded: rings included the drop shadows)

- SHA-256 `8fff278fd8c7eaa1f8c4f89550649d3ad8203418cf372d82b56df0b13d8a9654`; card rings measured to each card (x 37–532 / 554–1050 / 1072–1567, y 127–664 on the skew and questions boards, 127–623 on RAG); six board seams re-guarded, pass. The v4 figures below otherwise hold.

## v4 build (superseded)


- Candidate: `Prompts/training-bias-v4.mp4`; SHA-256 `4bc973790abc8e8a1af99cbbe7ac1a7eaed3b5ed2adb49e8b788fba2182ac209`; 7,830 frames at 30 fps (4:21.00), 1280×720.
- Narration: roll 6 start to finish, single voice, no cuts, no grafts. Only the engine outro after
  "changed." (256.82 s) is dropped. No added pauses: natural gaps at the board boundaries run
  0.34–0.80 s. Rendered transcript checked end to end; the closing lines are the last words.
- Boards: post-only Wrong Pattern. Wrong Answer. as an illustration walk 0:21.9–0:33.7 (full board
  under "Most of the cows… green pasture", to the machine on "The model picked up a shortcut", to
  the beach card and red X on "absorbed the background instead of identifying the actual animal");
  How Skewed Data Distorts the Picture 0:55.7–1:27.6 (full-height card rings at 1:02.0, 1:11.2,
  1:18.2; banner not spoken during the board, unringed); Three Questions That Reveal Bias
  1:52.3–2:28.6 (card rings at 2:00.7, 2:05.0, 2:12.4; banner ring at 2:19.5, the board held
  through the banner line in place of Notebook's latent-space drawing); Stale Information in Real
  Life 2:38.5–3:02.3 (bubble rings at 2:39.8, 2:45.9, 2:54.3, 2:57.4; the first ring pops 1.4 s
  after the board arrives because the narrator introduces the board and names the first turn at
  once); How RAG Works 3:21.3–3:59.3 (card rings at 3:30.6, 3:37.0, 3:44.9; banner spoken after the
  board's render ends, under Notebook's context-window drawing, unringed); standard close from
  4:11.7 as the literal final frame. Longest board run 38 s.
- Notebook spans kept: the monitor and cow drawings, the two-traps and donut diagrams, the
  facial-analysis and fact-card diagrams, the latent-space and knowledge-horizon diagrams, the
  self-explanation and Verify Dates drawings, the context-window diagram under the RAG caveat. No
  photographs, no invented statistics, no web addresses. Drawn faces in the facial-recognition
  diagram (1:36) are Notebook drawings.
- Corner mark cleaned on every kept frame: 2,802 cloned, 489 inpainted, 0 declined.
- `transition_guard.py` 11/11 pass; strips inspected. Contact sheets reviewed end to end. Protected
  files (live video, five rolls, six boards, lesson) unchanged.

## Listening checks for David

1. 3:29.7 and 3:59.4 — how the narrator says "RAG" (segment model heard "REG").
2. 2:38.5 — the chat board arrives on "Let's look at this chat interface"; the first bubble rings 1.4 s later.
3. 4:11.6 — the close board arrives on "AI repeats" (audio continuous, visual check).

## Ship notes

On approval: replace the live file, cache key `20260921ship3`, pill stays 4 min (4:21). Rolls 1–5
go at the ship; roll 6 stays as the source.
