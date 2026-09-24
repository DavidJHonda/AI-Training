# Pace of Change — rolls 1 and 2 of 2026-09-23 against the live video

David: "Two versions of pace-of-change uploaded to prompts. Please evaluate. And, evaluate the live
video too." Scope: narration review of `Prompts/pace-of-change-1.mp4` (5:06.50) and
`Prompts/pace-of-change-2.mp4` (4:44.57), rolled on the 2026-09-23 kit, compared beat by beat with the
live `course-assets/pace-of-change/pace-of-change.mp4` (4:11.93, v2 of 2026-09-18; its own evaluation
is in `video-audit/pace-of-change-evaluation-2026-09-23/`). Bundles (transcripts, scenes, holds,
sheets) in `pace-of-change-1/` and `pace-of-change-2/`. Nothing built, nothing shipped. Transcripts are
faster-whisper; nothing auditioned by ear.

Short version: **roll 1 is the build base (REPAIR: five beat cuts, all between silences). Roll 2 is
REROLL as a candidate and a picture donor only. The live loses to roll 1 on the hard requirements.**
No roll drew anything usable for Boards 3 and 4, so the second half stays a dive-and-pan board run.

```text
LESSON: pace-of-change
CANDIDATE: Prompts/pace-of-change-1.mp4 (5:06.50)
VERDICT: REPAIR
TEACHING POINTS:
  Hook — RICH — 0:00 "The conversation around artificial intelligence is getting louder by the day. The reason is simple. The technology is advancing at blazing speeds."
  Board 1 intro — TAUGHT but see ERRORS — 0:20 "This table gives us a direct comparison of chat GPT in 2023 versus its projected state in 2026, visualizing the leap in capabilities."
  Answering, both years — RICH — 0:33 (the "Look at the top row, answering." lead-in is furniture, 0:30.7–0:33.2)
  Images, both years — RICH — 0:47 (Spot named; bonus leg, rabbit ears; photoreal, readable signs, video with sound and dialogue)
  Context window, both years — RICH — 1:03 ("fell right out of its head"; million tokens; novel series)
  Doing, both years — RICH — 1:23 ("the doing phase"; "book flights, build software and fix code while you sit and watch" — the board says book, build, fix; harmless)
  Race; new models every couple of months; each release a stronger LLM replacing the last — RICH — 1:48–2:02
  "A limitation can disappear quickly, so today's no is not necessarily permanent." — RICH — 2:08 (exact)
  Why so fast; three concepts — RICH — 2:28 "Why so fast? There are three specific concepts driving this acceleration."
  "you already understand the first one" — TAUGHT — 2:36 "You likely understand this intuitively."
  Better training / More compute / AI helps build AI — RICH — 2:34 / 2:46 / 2:58
  Slow down; "AI is already helping people build better AI." — RICH — 3:11 "Let's slow down and consider that third concept. AI is already helping people build better AI." (exact)
  Four ideas; limited form vs not demonstrated — TAUGHT — 3:25 "There are four key ideas driving companies forward." The up-front one/three split is not spoken; each idea carries its tag as it comes (3:37 "happening in limited form today", 3:52 "entirely undemonstrated", 4:39 "purely hypothetical")
  Not four steps in order — RICH — 4:50 "It is tempting to put these milestones on a guaranteed timeline, but they are just ideas." (an accurate addition that delivers the prompt's guardrail)
  Automated AI research — RICH — 3:37–3:52
  Self-improving AI — RICH — 3:52–4:05
  Banner "One is human-directed. The other would be a self-reinforcing loop." — RICH — 4:09 (exact)
  AGI: no agreed finish line, no test, human-level across many kinds of work — RICH — 4:23–4:36
  ASI: hypothetical; exceeding the best humans; nobody knows whether it is possible — RICH — 4:36–4:50
  Banner "Nobody knows whether AI will reach either milestone." — RICH — 4:55 (exact)
HARD REQUIREMENTS:
  "A limitation can disappear quickly, so today's “no” is not necessarily permanent." — MET — 2:08.6
  "AI is already helping people build better AI." — MET — 3:14.9
  "One is human-directed. The other would be a self-reinforcing loop." — MET — 4:09.4
  "Nobody knows whether AI will reach either milestone." — MET — 4:55.6
  "AI keeps getting faster and more powerful." — MET — 4:58.6
  "Nobody is sure where it stops." — MET — 5:01.4; last words at 5:03.4, then Notebook's spinner card (replaced by the standard close)
ERRORS:
  0:25 — "versus its projected state in 2026" — 2026 is now, not a projection; cut the sentence (below).
  0:30 — "Look at the top row, answering." — board furniture; cut (below).
  2:26 — "This diagram answers a simple question." — furniture; cut (below).
  3:18 — "This creates a self-accelerating loop where the tool itself speeds up the invention of the next tool." — added; it pre-empts and blurs the human-directed / self-reinforcing distinction the next board draws; cut (below).
  3:31 — "This graphic shows the first two, mapping the boundary between reality and hypothesis." — furniture plus Notebook phrasing; cut (below).
  4:14 — "This brings us to the ultimate question driving the industry." — "ultimate" is on the banned list; cut (below).
  1:38 — "These direct comparisons prove a crucial point about this technology. What we assume to be a hard permanent limitation today can be completely shattered in a matter of months." — added, overwrought but accurate; optional cut, David's call.
SOURCE_QA: PASS
ADDITIONS: "It is tempting to put these milestones on a guaranteed timeline, but they are just ideas." (4:50) is worth keeping; it is what the prompt asked for and the page implies.
REPAIR PLAN (all cuts are whole sentences between the roll's own silences; measure each split at the RMS gap, never at a scenes.py cut):
  1. cut 0:20.60–0:30.70 "This table gives us … visualizing the leap in capabilities." (0:15 "…in just a three-year window." then runs into the Answering beat)
  2. cut 0:30.70–0:33.20 "Look at the top row, answering." (the Answering row ring carries the label; "In 2023, the model started typing…" follows)
  3. cut 2:26.30–2:28.90 "This diagram answers a simple question." ("Why so fast?" stays)
  4. cut 3:18.70–3:25.20 "This creates a self-accelerating loop …" ("AI is already helping people build better AI." then "So what does the future of AI look like?")
  5. cut 3:31.30–3:37.10 "This graphic shows the first two, mapping the boundary between reality and hypothesis." ("There are four key ideas driving companies forward." then "First is automated AI research…")
  6. cut 4:14.20–4:17.60 "This brings us to the ultimate question driving the industry." ("The other would be a self-reinforcing loop." then "How far can AI go?")
  Optional 7. cut 1:38.00–1:48.10 (the "shattered" pair).
  Runtime after cuts 1–6: about 4:36 (pill would round to 5 min); with cut 7 as well, about 4:26 (pill stays 4 min). Note for ship time.
EDITING NOTES:
  Photographs: none seen. Corner mark on every Notebook frame (expected; the build removes it).
  Notebook spans that cannot ship: 0:00–0:10 "AI GROWTH HITS ESCAPE VELOCITY" chart (capability index to 12K, invented); 0:12–0:16 calendar with a drawn silhouette person; 1:44–1:48 "2023 CONSTRAINTS" diagram; 1:52–2:02 "THE AI CAPABILITY RACE" chart naming GPT-4, Claude, Gemini; 2:16–2:24 "FRONTIER MODEL RELEASE CYCLE v1.0…v4.0 Ultra" and "DISTRIBUTED COMPUTE INFRASTRUCTURE"; 2:24–2:28 "PARALLEL TENSOR ACCELERATOR"; 3:12–3:28 "RECURSIVE AI" diagram with a drawn researcher and "CYCLE SPEED: 10x Exponential Loop"; 4:08–4:14 human-directed / self-reinforcing loop diagrams (a restatement of the banner); 4:52–4:58 "Theoretical & Unproven Trajectories AGI(?) ASI(?)" sketch (a timeline). Notebook's board renders (with its yellow highlights) at 0:24–1:36, 2:28–3:12, 3:28–4:06, 4:16–4:50 are replaced by the canonical boards.
  Usable drawings in roll 1: 0:16–0:20 the "2023–2026" torn-paper collage (under the intro); 1:40–1:44 two phones, chat vs a 3D build (re-time under Doing's 2026 half, 1:29.6–1:38.0); 2:04–2:14 the "Write Code / Generate Video / Hold Context" checklist and its red X (under the race beat, 1:48–2:14).
LISTENING: none. The six cut points and the level match at each are to be listened to at build.
```

```text
LESSON: pace-of-change
CANDIDATE: Prompts/pace-of-change-2.mp4 (4:44.57)
VERDICT: REROLL (as a candidate); picture donor only
TEACHING POINTS:
  Hook — RICH — 0:00
  Board 1 four rows — RICH — 0:21–1:31 (Spot unnamed; context window gets an extra definition, "how much memory the AI has during a single conversation", 0:52; "the system forgot how you started", 1:02)
  Summary line — added — 1:31 "In just three years, we moved from a simple, easily confused text generator to a highly capable, active operating agent." (overclaim; not on the page)
  Race; every couple of months; replacing — TAUGHT — 1:40–1:52
  today's "no" line — THIN — 1:52 "a limitation that exists today can disappear quickly. A no right now does not necessarily mean a permanent no in the future." (not the line)
  Three concepts — RICH — 2:02–2:40 ("pure processing power, or compute"; "thousands of specialized chips")
  "AI is already helping people build better AI." — MISSING — replaced at 2:40 by "AI advancement is no longer limited purely by human speed. The technology is actively accelerating its own development." (WRONG in effect: it asserts the self-reinforcing loop the next board says is not demonstrated)
  Slow-down beat — MISSING
  Four ideas, not a timeline — TAUGHT — 2:48 "distinct theoretical concepts, not a guaranteed timeline"
  Automated AI research — RICH — 3:05
  Self-improving AI — TAUGHT — 3:19 ("with no human direction"; the board says little or no)
  Banner 1 — WRONG — 3:36 "One is human-directed, the other is a self-reinforcing loop." ("is", not "would be": states the undemonstrated loop as fact)
  AGI / ASI — RICH — 3:46–4:17 ("ultimate limits", "massive caveat")
  Banner 2 — THIN — 4:17 "Despite the billions of dollars and the massive processing power being deployed, nobody actually knows whether AI will ever reach either of these theoretical milestones."
HARD REQUIREMENTS:
  today's "no" line — MISSED
  "AI is already helping people build better AI." — MISSED
  "One is human-directed. The other would be a self-reinforcing loop." — MISSED (wording changed)
  "Nobody knows whether AI will reach either milestone." — MISSED
  "AI keeps getting faster and more powerful." / "Nobody is sure where it stops." — MISSED — 4:32 "AI keeps getting faster and more powerful, and as it continues to accelerate, nobody is sure exactly where it stops." then 4:42 "Thank you." — the two lines are merged, expanded, and followed by a sign-off.
ERRORS: as above; banned words used: theoretical (three times), ultimate, landscape, deployed.
SOURCE_QA: PASS
ADDITIONS: the context-window definition at 0:52 is a fair teaching add but not needed.
REPAIR PLAN: none as a candidate (5 of 6 hard requirements missed, one WRONG banner, sign-off after the close).
EDITING NOTES — as a donor:
  Usable drawings: 1:44–1:48 data-center aisle (under More Compute in roll 1, 2:48–2:58); 1:56–2:00 phone "System Error" turning to a check, and 2:00–2:04 the check/X torn paper (under the race beat). 1:36–1:44 (confused man at a computer, flight booking) has a drawn person; 1:48–1:56 "CONTINUOUS OBSOLESCENCE · ~60-DAY CADENCE" with invented scores; 2:52 "FOUR CORE AI TRAJECTORIES" (restatement); 2:56 "Theoretical Frameworks" collage — none ship.
  Its board renders run 0:10–1:32 (81 s) and 3:40–4:28 (48 s): the same hold profile as the live.
LISTENING: none.
```

```text
BEST-OF PLAN: pace-of-change
BASE: Prompts/pace-of-change-1.mp4 (all six required lines exact; every point RICH/TAUGHT; the not-steps beat; six furniture/added sentences, all cuttable as whole beats)
  Board 1 intro — roll 1 TAUGHT @0:09 "To truly grasp … three-year window. This table gives us … projected state in 2026 …" | live TAUGHT @0:09 "To visualize exactly how fast things are moving, this board shows a direct comparison between the AI available in 2023 and the models we have in 2026." | roll 2 TAUGHT @0:10 "let's look at a baseline comparison of chat GPT from its breakout year in 2023, versus what models can do in 2026." — TAKE roll 1 with cut 1 (alternative: graft the live's sentence under Board 1's full view; not needed)
  today's "no" — roll 1 RICH @2:08 exact | live TAUGHT @1:34 "today's no is not necessarily a permanent no" | roll 2 THIN — TAKE roll 1
  AI builds AI line — roll 1 RICH @3:14 exact | live TAUGHT @2:26 "AI is already actively helping people build better AI" | roll 2 MISSING — TAKE roll 1
  Four ideas framing — roll 1 TAUGHT @3:25 + RICH @4:50 (not a guaranteed timeline) | live THIN @3:24 "ultimate finish lines" | roll 2 TAUGHT @2:53 — TAKE roll 1
  Banner 1 — roll 1 RICH @4:09 exact | live TAUGHT @3:15 "entirely human-directed … hypothetical self-reinforcing loop" | roll 2 WRONG — TAKE roll 1
  AGI — roll 1 RICH @4:23 | live RICH @3:29 (the 9/18 graft, with "look at the tag above it") | roll 2 RICH @3:46 — TAKE roll 1
  Banner 2 — roll 1 RICH @4:55 exact | live TAUGHT @3:57 | roll 2 THIN — TAKE roll 1
  Close — roll 1 MET | live MET (roll-1-of-9/18 graft) | roll 2 MISSED — TAKE roll 1
GRAFTS: 0 audio grafts. Picture donors: roll 2 ×3 spans, roll 1's own ×3 spans (listed above).
```

## Proposed edit plan (for David's approval before the first build)

Scope: full production pass on roll 1. Narration: cuts 1–6 above (7 optional). No audio grafts.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| ChatGPT: 2023 vs. 2026 | whole board (unmarked) under the intro, then row rings at spoken onsets: Answering 0:33.2, Images 0:46.3, Context Window 1:03.1, Doing 1:23.2; each ring spans the full row, both columns | full view, then dive to each complete row, pan row to row, pull back for Doing's 2026 half | arrives ~0:15 on "…in just a three-year window" (the 2023–2026 collage sits under 0:09–0:15); board ~0:15–1:30 (≈60 s after cut 1) ; cut to roll 1's two-phones drawing under "In 2026, it actually does the thing. AI agents can book flights…" 1:29.6–1:38.0 and stay on it into the race beat | dense (four rows of small text). No roll drew anything for the four rows, so the first 60 s is an unbroken dive-and-pan; the longest run in the candidate. |
| (race beat, Notebook) | — | — | 1:38–2:29: roll 1's checklist + red X (2:04–2:14) re-timed, plus roll 2's phone-error→check (1:56–2:00) and check/X (2:00–2:04) as needed, in place of roll 1's invented charts | 8b, 8c: the capability-race chart, constraints diagram and release-cycle diagrams never ship |
| Why So Fast? | whole board on "Why so fast?" 2:28.9, then card rings: Better Training 2:34.0, More Compute 2:46.0, AI Helps Build AI 2:58.2; whole-board again for "Let's slow down…" 3:11.7 | full view throughout (compact: three cards, text reads at full view; the live shipped it this way) | ~2:29–3:18 (49 s); break: roll 2's data-center aisle under More Compute 2:48.0–2:57.0, back on the board ~1 s before "The third driver" | |
| Could AI Improve Itself? | whole board on "So what does the future of AI look like?" 3:25.2 (after cut 5 the board's own intro is gone; the full-view hold runs under "There are four key ideas…"), then Automated AI Research 3:37.1, Self-Improving AI 3:52.1, banner 4:09.4 | full view, dive to each complete card, pull back for the banner | ~3:25–4:14 (49 s), unbroken | no roll drew anything usable for these beats (roll 1's recursive-AI and loop diagrams are a person + an invented figure, and a banner restatement) |
| How Far Can AI Go? | whole board on "How far can AI go?" 4:17.6 (after cut 6 it follows Board 3's banner directly), then AGI 4:23.6, ASI 4:36.4, banner 4:55.6 | full view, dive to each card, pull back for the banner | ~4:17–4:58 (41 s), unbroken; **Boards 3 and 4 abut: a 90 s board run** | no roll drew anything usable; roll 1's 4:52 trajectories sketch is a timeline |
| Close | canonical close on "AI keeps getting faster…" 4:58.6; standard motion; hold | — | — | replaces Notebook's spinner card |

Selective pauses (proposed; measure existing gaps at build): (a) before "So what does the future of AI
look like?" at 3:25.2, only if the gap after cut 4 lands short of ~0.6 s; (b) before the close at
4:58.6, target ~0.8 s total. No other pauses.

**The open question for David.** This plan fixes the narration (6/6 required lines, no furniture) and
breaks the first two boards, but Boards 3 and 4 still run 90 s back to back because neither roll drew
a usable scene for the future-ideas beats; the live has the same problem. Options: (1) build this and
accept the second-half run; (2) roll once more with the BOARDS AND VISUALS block asking for a drawn
scene before each of the last two boards (a lab bench for automated research; a horizon for how far),
and use that roll as a picture donor only; (3) both, in that order.


---

# Build v4 — `Prompts/pace-of-change-v4.mp4` (2026-09-23) — REVIEW CANDIDATE, not shipped

David: "Build it from roll 1. Agree with cut 1. 2-Not a cut. 3-Not a cut. 4-Why cut this? 5-We just need to cut 'mapping the
boundary between reality and hypothesis'. 6-What is wrong with that?" Built with cut 1 and the phrase cut 5'; lines 2, 3, 4 and 6
kept. Script: `scripts/video/build_pace_of_change_v4.py`; artifacts in `build-v4/` (edit-manifest.json, leg-*.json, state sheets,
transitions/, bundle/ with transcript and contact sheets). 4:54.37, 8831 frames, sha256 ad652c07…; roll 1 audio otherwise untouched.

## Narration (two edits, both at sentence silences; no grafts, no added pauses)

| Edit | Source | Output | Measured gap after the join (silencedetect −35 dB) |
|---|---|---|---|
| cut 1: "This table gives us a direct comparison of chat GPT in 2023 versus its projected state in 2026, visualizing the leap in capabilities." | 20.60–30.50 | join at 0:20.60 | 0.62 s (20.35–20.98) |
| cut 5': ", mapping the boundary between reality and hypothesis" (the sentence now ends "This graphic shows the first two.") | 213.20–216.60 | join at 3:23.30 | 0.62 s (203.21–203.83) |

Close: "AI keeps getting faster and more powerful." 4:45.4, "Nobody is sure where it stops." 4:48.1, last word 4:49.5; settled hold to
4:54.4 with the room tone faded to silence after 0.4 s (Transformer v10 pattern). Pill would read 5 min (4:54).

## Pictures (output timeline)

| Span | What is on screen | Replaces |
|---|---|---|
| 0:00–0:09.7 | roll 1's own 2023–2026 torn-paper collage (re-timed from 0:15.6, last frame held) | "AI GROWTH HITS ESCAPE VELOCITY" chart |
| 0:09.7–1:22.4 | **ChatGPT: 2023 vs. 2026**, canonical, dense: full view under "To truly grasp… three-year window" (cut 1 inside the static establish), row rings at "answering" 0:21.9, "Next is images" 0:36.3, "Then there is the context window" 0:53.1, "Finally, the doing phase" 1:12.9; camera dives to each complete row, arriving at the onset | calendar with a drawn silhouette, then Notebook's board render |
| 1:22.4–1:32.1 | roll 1's own two-phones drawing (chat vs a 3D build; re-timed from 1:37.97 source) | the Doing row's second half: "AI agents can book flights…", "These direct comparisons prove…" |
| 1:32.1–1:42.0 | roll 2's phone "System Error" turning to a check (roll 2 3375–3531, last frame held) | "2023 CONSTRAINTS" diagram + start of the capability-race chart |
| 1:42.0–1:52.1 | roll 2's green check / grey X (3531–3670, held) | "THE AI CAPABILITY RACE" chart naming GPT-4, Claude, Gemini |
| 1:52.1–2:04.5 | roll 1's own Write Code / Generate Video / Hold Context checklist, then its red X (in place) | — |
| 2:04.5–2:12.5 | the red-X frame held | "FRONTIER MODEL RELEASE CYCLE", "DISTRIBUTED COMPUTE INFRASTRUCTURE", "PARALLEL TENSOR ACCELERATOR" |
| 2:12.5–2:38.2 | **Why So Fast?**, canonical, compact, full view: arrives on "We need to see exactly what is powering this speed under the hood"; rings Better Training 2:24.1, More Compute 2:36.1 | Notebook's board render |
| 2:38.2–2:47.4 | roll 2's data-center aisle (3019–3151, held) under "AI requires massive amounts of chips… physical infrastructure" | (breaks the board hold) |
| 2:47.4–3:15.3 | Why So Fast? again: ring AI Helps Build AI 2:48.3; unmarked from "Let's slow down…" 3:01.6 through "AI is already helping people build better AI" and the self-accelerating-loop sentence | Notebook's render, then the "RECURSIVE AI / 10x Exponential Loop" diagram with a drawn researcher |
| 3:15.3–4:00.9 | **Could AI Improve Itself?**, canonical, dense: full view under "So what does the future of AI look like? … This graphic shows the first two." (cut 5' inside the establish); ring + dive Automated AI Research 3:27.5 (0.47 s after "First", before "automated"), Self-Improving AI 3:42.1; pull back and ring the banner at "One is human-directed" 3:58.7; stays through "This brings us to the ultimate question" | Notebook's render, then the HUMAN-DIRECTED / SELF-REINFORCING LOOP diagrams |
| 4:00.9–4:45.3 | **How Far Can AI Go?**, canonical, dense: arrives on "How far can AI go?"; AGI 4:10.3, ASI 4:23.2; back to full view, no ring, for "It is tempting to put these milestones on a guaranteed timeline…" 4:36.9; banner ringed at "Nobody knows whether AI will reach either milestone." 4:42.2 | Notebook's render, then the "Theoretical & Unproven Trajectories" sketch |
| 4:45.3–4:54.4 | standard close (canonical close board, 48-frame hold, 150-frame push to 1.2x, settle) | Notebook's closing card and spinner |

Board runs: Board 1 72.7 s (dense dive-and-pan; no roll drew anything for the four rows); Board 2 25.6 s + 27.9 s around the
data-center break; **Boards 3 and 4 back to back 90.0 s** (no shippable drawing in either roll for the future-ideas beats; reported
in the 2026-09-23 review as the open question). Rings are drawn by `ken_burns_path.ring_px` (5 px at the wide framing, scaling with
the dive, per the 2026-09-21 rule). Corner mark: 500 frames cloned, 1572 inpainted, 0 declined.

## Verification

- 8831 frames decoded = plan; duration 294.37 s; protected files (both rolls, four boards, close, lesson, index.html) unchanged.
- `transition_guard.py`: 13 of 14 declared boundaries PASS. The one FAIL, f6099 (cut 5' inside Board 3), was inspected frame by
  frame: delta 0.0 across the cut itself (f6095–f6101), then a smooth ramp 1.5 → 3.9 → 5.6 → 7.1 → 8.6 → 10.1 → 11.3 → 12.0 →
  13.1 → 13.3 as the dive to the Automated AI Research card eases in (f6101–f6125). That is the camera move crossing the guard's
  12-point threshold on consecutive frames — the "cut count is not a strobe measure" pattern in TECHNICAL-RECIPES — not a stale
  frame or a leaked scene. Strip: `build-v4/transitions/boundary-006099-cut5-inside-board3.jpg`.
- A first render (v3) put the Automated ring at "First" (216.98), which fell mid-dive; v4 moves the ring to the camera's arrival
  (217.45). v3 and its folder were deleted before handover (identical audio, MD5 b7f4f85c…).
- Every ring state inspected on the four state sheets: complete row/card inside the ring, nothing clipped, banner rings at full view.
- Whole-file contact sheets (4 s cells) inspected start to close: no Notebook board render, no chart, no photograph, no person,
  no chapter card remains; the close is the literal final frame.
- Edited gaps measured in the encoded file (table above). No other audio changed; the roll's own gaps stand.

## Not auditioned (David's listening list)

1. 0:20.6 — the cut-1 join: "…in just a three-year window." → "Look at the top row, answering."
2. 3:23.3 — the cut-5' join: "This graphic shows the first two." → "First is automated AI research…"
3. 4:45–4:54 — the two closing lines and the faded hold.


---

# Build v5 — `Prompts/pace-of-change-v5.mp4` (2026-09-23) — REVIEW CANDIDATE, supersedes v4

David on v4: "highlights on this board extend too far right. Each row does that. Fix that please." Measured on the canonical board:
the 2026 boxes end at x=1520, the white card's margin runs 1521–1559, the stage starts at 1560; v4's row rings ran to 1600. v5 ends
every row ring at 1532 (12 px past the box, 27 px inside the card). Nothing else changed: same audio (MD5 b7f4f85c…), same 8831
frames, same corner-mark result (500 cloned, 1572 inpainted, 0 declined), same 13/14 guard result with the same inspected f6099
ease-in ramp. Script `scripts/video/build_pace_of_change_v5.py`; artifacts in `build-v5/` (the four output ring states are in
`rings-v5.jpg`). v4 and its folder deleted; the v4 section above describes v5 in every other respect.

## Next: reroll for the race beat (David 2026-09-23)

"From 1:23 to 2:12, the Gemini Notebook graphics are disappointing. I think we should use this video as the base and reroll to
get more engaging graphics for that part of the video." That output span is roll 1's 92.3–142.4 s: "AI agents can book flights…"
through "…the underlying mechanics", where v5 shows the two phones, roll 2's error-to-check phone and check/X, the roll's own
checklist and red X, and the red X held (the source there was the 2023 CONSTRAINTS diagram, the AI CAPABILITY RACE chart and the
release-cycle / compute / chip diagrams, none shippable). Plan: v5 stays the base (its audio does not change); the new roll is a
picture donor only for that span, dropped in with `keep(..., video_src=<new roll>)` under Edit Spec 8b.

Prompt amended for the reroll (`Prompts/pace-of-change-video-prompt.txt`, 498 words; synced): BOARDS AND VISUALS now adds "After
the comparison board, the race needs drawings, not diagrams: for the companies racing and new models every couple of months, and
for today's "no" not being permanent, draw a starting line, a calendar flipping pages, or a closed door swinging open." Three
trims made room (the runtime sentence, the formal-language sentence, and a tighter four-ideas sentence in the beat spine); the
verbatim list and the spine's content are unchanged.
