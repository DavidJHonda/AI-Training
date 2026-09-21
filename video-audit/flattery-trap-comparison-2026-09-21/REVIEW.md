# Flattery Trap — five-way review (2026-09-21)

New candidates: `Prompts/flattery-trap-3.mp4` (5:15) and `-4.mp4` (5:24), both from 2026-09-21.
Earlier rolls, available as donors: `-1` (5:09) and `-2` (5:01) from 2026-09-19. The live video
(`course-assets/flattery-trap/flattery-trap.mp4`, 6:07) still dates from 2026-09-08 and has never
been replaced. All four rolls came from the 2026-09-18 kit. Transcripts, scene cuts, holds, and
contact sheets in the per-roll folders; word-level transcripts for rolls 3 and 4 in `words/`.

**Verdict: roll 4 is the base, with one graft from roll 2. Roll 4 is the only roll of the five that
keeps the prompt's accuracy qualification on RLHF and speaks the standing instruction exactly as
written — the two places this lesson is easiest to get wrong. Roll 3 misses both, and garbles the
"ask for the gaps" payoff.**

## Hard requirements (from the Markdown and the prompt)

| Requirement | roll 1 | roll 2 | roll 3 | roll 4 | live |
|---|---|---|---|---|---|
| Closing lines verbatim, in order, nothing after | MET | MET | MET (no lead-in) | MET (no lead-in) | MET |
| Keep the qualification: agreeable answers **can** feel better and **can** earn approval; never "always", never "flattery is inevitably built in" | MISSED ("you **bypass the flattery entirely**") | MISSED ("AI tools are **built to be** encouraging… that constant **built-in** approval") | **MISSED** ("agreeable answers **simply** feel better"; "**consistently** earn higher ratings"; "AI is **wired at the training level to seek your approval**"; "bypass the AI's programming") | MET ("agreeable, confident answers **can** feel better in the moment") | MISSED ("why are these systems **designed to flatter** you"; "just feel better"; "the underlying bias remains") |
| Do not imply all positive feedback is sycophancy | MET | MET | MET | MET ("Positive feedback is perfectly fine, as long as it points to real, specific elements") | MET |
| The essay intro, the flattering reply and the useful reply all quoted | MET | **MISSED** (the American Dream intro is never read) | MET | MET | MET |
| OpenAI rolled the update back three days after launch and publicly called it sycophancy | MET | MET | MET ("three days later"; but attributes the industry-wide claim to OpenAI) | MET | MET |
| The problem has improved but has not disappeared | MISSED | **MET** (2:31.5–2:35.2) | MISSED | MISSED | MISSED |
| Every move: weak prompt, complete better prompt, and why the change helps | MET | MET | MET, but the move-2 "why" is garbled (see below) | MET | MET |
| The three limits (rubric, counterargument, standing instruction) | MET | MET | MET | MET | MET |
| Standing instruction spoken exactly: "Be direct with me. Lead with what needs work, point to specific evidence, and tell me when I'm wrong." | MISSED ("be direct… point to evidence") | MET | **MISSED** ("Be direct with me. Lead with what needs work. Point to evidence." — drops "specific" and the whole final clause) | **MET, word for word** | MET |
| Board 3: a short revealing excerpt, not the whole quotation | MET | MET | MET | MET | MET |
| Board 4 takeaway: "Ask AI to improve the work, not approve of you." | MET | MET | MISSED (paraphrased: "Your job is to always ask the AI to improve the work, not to approve of you") | MET, verbatim | MISSED (absent) |
| Never asks the viewer to pause or work something out | MET | MET | MET | MET | MET |
| Runtime / cuts | 5:09 / 23 | 5:01 / 40 | 5:15 / 27 | 5:24 / 27 | 6:07 / 204 |

Roll 2 is REROLL: it never reads the essay intro, so the comparison it then analyses has no text on
which to hang — but it owns the "improved but not disappeared" beat and is the donor below. Roll 1 is
REROLL on the "bypass the flattery entirely" overreach and an incomplete standing instruction. The live
video is thorough and its close is clean, but it opens the RLHF section by asking why these systems are
"designed to flatter you", which is the claim the prompt exists to prevent.

## The garble in roll 3 (3:26.6–3:31.5)

Roll 3's "ask for the gaps" payoff decodes as **"Broad requests trigger those cheerful, empty, yes,
actually what needs your attention"** on base.en and **"empty yes-actly what needs your attention"** on
small.en. Neither resolves to a sentence. Two independent decodes failing the same way is the same
signature as the Document Trap six-foul problem, and it sits on the *why* for one of the five moves —
the part the prompt specifically requires to be spoken. Roll 4's equivalent is clean: "Asking 'is my
essay good' is a broad request for approval, and a cheerful yes doesn't help you revise."

## Beat table: rolls 3 and 4

| Teaching point | roll 3 | roll 4 |
|---|---|---|
| Definition: treating AI's approval as honest evaluation | RICH | RICH |
| Essay intro quoted; flattering reply quoted; what it praised; "could fit almost any Gatsby essay" | RICH | RICH |
| Useful reply quoted; names the missing thesis; gives a next move | RICH | RICH |
| Takeaway: good feedback improves the work, empty praise improves the feeling | RICH | RICH ("improves the work itself… only improves how you feel in the moment") |
| Good feedback can still be positive | RICH | RICH |
| RLHF named; People Rank / Agreement Can Win / Numbers Move | RICH, **but the qualification is dropped** | RICH, qualification intact |
| Sycophancy defined | RICH | RICH |
| April 2025, the gag pitch, the excerpt | RICH (3 sentences) | TAUGHT (2 sentences) |
| Rolled back three days; publicly called sycophancy | RICH | RICH |
| Not limited to ChatGPT; found across multiple assistants | TAUGHT (attributed to OpenAI) | RICH ("the problem exists across many different AI assistants") |
| Companies now test for it; improved but not gone | THIN (testing implied, improvement denied) | THIN (testing covered, improvement missing) |
| Move 1 — ask, don't tell | RICH | RICH |
| Move 2 — ask for the gaps | **GARBLED why** | RICH |
| Move 3 — use a rubric, with its limit | RICH | RICH |
| Move 4 — argue the other side, with its limit | RICH | RICH |
| Move 5 — standing instruction, spoken exactly, with its limit | **MISSED wording** | RICH |
| Board 4 takeaway | TAUGHT (paraphrase) | RICH (verbatim) |
| Close | MET | MET |

Roll 4 wins or ties every contested beat. Roll 3's only edge is a slightly fuller Board 3 excerpt,
which is a beat the prompt asks us to keep *short*.

## Per-roll block: flattery-trap-4 (BASE)

```text
LESSON: flattery-trap
CANDIDATE: Prompts/flattery-trap-4.mp4 (5:23.97, 30 fps, 27 cuts)
VERDICT: REPAIR (one identified graft; KEEP on every other beat)
TEACHING POINTS: all RICH or TAUGHT except "the problem has improved, but it has not disappeared"
  (MISSING)
HARD REQUIREMENTS: all MET except that clause. Standing instruction at 4:50.0–4:56.0, word for word.
  Close: "Useful feedback points to the work." 5:16.4–5:17.9 and "Look for specifics, not approval."
  5:18.4–5:20.2, 0.54 s apart, last word 5:20.2, nothing after (3.8 s of silence to 5:24.0)
ERRORS: none factual
SOURCE_QA: PASS
ADDITIONS: "Artificial intelligence is built to be incredibly encouraging and polite" (0:00) leans on
  the framing the prompt guards against, though it never claims the behaviour is inevitable; "The
  praise literally gets baked in to the system" (1:50) restates the board's own title
REPAIR PLAN: graft roll 2's 2:31.54–2:34.75 ("But while the problem has improved, it has not
  disappeared.") into roll 4 at 2:37.2, inside the 0.39 s pause after "…many different AI assistants."
  Whole sentence between silences in roll 2 (0.51 s before, 0.53 s after).
EDITING NOTES: Notebook renders Boards 2, 3 and 4 itself; the canonical JPGs replace those spans.
  Board 1 is post-only. Screen references to cut or cover: "This diagram outlines why AI leans so
  heavily toward flattery" (1:23) and "This table outlines five ways to fight the flattery trap" (2:45).
LISTENING: transcripts read in full and every boundary measured; audio not auditioned.
```

## Not grafted

- Roll 3's fuller Board 3 excerpt. The prompt asks for a short excerpt; roll 4's two sentences meet it.
- Rolls 1, 2 and the live video all frame the behaviour as built in or designed in. Nothing from those
  spans should come across.

## Also worth fixing while this lesson is open

`index.html` gives the Flattery Trap video a **"4 min"** pill, but the live file is **6:07**. Whichever
roll ships, that pill needs to match — roll 4 plus the graft lands near 5:27.

## Listening checks for David

1. Roll 3, 3:26–3:32 — the garbled "ask for the gaps" line, if you want to confirm the call against
   roll 4. (Roll 4 is the recommendation regardless; this only matters if you prefer roll 3 otherwise.)
2. Roll 4, 4:50–4:56 — the standing instruction, the one line that must land exactly.
3. The graft boundary once built.

## v6 build (`build-v6/`, script `scripts/video/build_flattery_trap_v6.py`) — CURRENT

David's notes on v4, 2026-09-21:

- **The two response rings clipped their first line.** When the quote text was measured for v4 the
  scan started at y=960, which truncated the first line — it actually runs 948–1017 — so the rect top
  at 950 sat inside the text and the stroke crossed its ascenders. Both of David's crops show it. v5
  re-measured against the real gaps (heading ends 923, text 948–1017, the Praised label starts 1067)
  and centres the edges at 935 and 1040.
- **Ring weight is now constant against the artwork, not the frame** (new house rule; Edit Spec
  section 5, `ken_burns_path.ring_px`). A ring is 5 px where a 1600 px board fills the 1280 px frame —
  the library's usual framing, so every standard wide board keeps exactly the weight it has today —
  and scales in proportion as the camera dives or pulls back, with a 3 px floor. Measured on this
  build: the Five Ways ring is 3 px at full view and grows to 5 px as the camera dives (v4 was a flat
  5 px at both); the Cycle and Sycophancy boards are unchanged at 5 px; the comparison board's quote
  rings come down from 5 px to 3 px, which is what made them read heavy against that board's small
  letterboxed text. Videos shipped under the old constant-5 rule are not rebuilt.
- Candidate: `Prompts/flattery-trap-v6.mp4`; SHA-256
  `2449fbb325ec90a9c3440e0a546ad45634f475e77860fffbe04ba6c54e04b936`; 9,881 frames at 30 fps (5:29.37).
  Corner mark 1,292 cloned, 2,054 inpainted, 0 declined. `transition_guard.py` 18/18 pass. Audio,
  narration, timeline and runtime identical to v4; only the rings changed. Protected files unchanged.

## v4 build (`build-v4/`, script `scripts/video/build_flattery_trap_v4.py`; superseded by v6)

David's notes on v3, 2026-09-21, all applied:

- **0:40** — the Flattery card now rings the AI's response text ("Great start! You've clearly
  identified the central theme. This is a strong foundation.") at 0:40.3 as it is read, instead of the
  whole card at 0:38.7, then moves to Praised and Could Fit.
- **0:56** — the Useful Feedback response ("Right topic, but this needs work…") rings at 0:56.6 as it
  is spoken and holds until the Named row at 1:04.4.
- **Five Ways is now dense.** Each leg opens on the full board, dives to the complete active row, and
  pans to the next row as the narration moves. The dive window is 1600 px of a 2530 px canvas, so the
  rows render at about 80 percent of native instead of 63; the weak and better prompts are comfortably
  readable. The takeaway leg stays at full view, because the banner wants the whole board.
- **The 106-second run is broken into three legs** — 26 s, 42 s and 15 s — by three drawings borrowed
  from roll 3, each matched to the beat it covers:
  | Output | Roll 3 frames | Drawing | Under |
  |---|---|---|---|
  | 3:15.5–3:20.3 | 5693–5836 | biased input echoed, neutral input rigorously evaluated | "A neutral question gives the AI less of your own confidence to reflect back at you." |
  | 4:02.3–4:07.6 | 6940–7082 | the work checked claim by claim against the rubric | "…not an official guarantee of accuracy or a final grade." |
  | 4:23.0–4:36.0 | 7455–7847 | "No Strong Objection" → "Model Limitation" → "You are the final judge" | "If the AI fails to produce a strong counterargument, that does not prove your position is flawless." |
  Each donor is a whole drawn scene of roll 3's own. The rubric span starts after roll 3's mock
  "GRADE: 94%" badge fades, so no invented figure reaches the build; the last 17 frames hold.
- Longest board run is now 42 s (was 106 s). Audio, narration and runtime are unchanged from v3.
- Candidate: `Prompts/flattery-trap-v4.mp4`; SHA-256
  `b476cd5aeafdd46ce4b8b5f8d64672461a884127eeecaedc01447cd2ea2972c7`; 9,881 frames at 30 fps (5:29.37).
  Corner mark: 1,292 cloned, 2,054 inpainted, 0 declined. `transition_guard.py` 18/18 pass. All
  eighteen row boundaries measured: -60 to -73 dBFS in the 60 ms after the splice, worst peak sample
  difference 0.0038. Protected files unchanged.

## v3 build (`build-v3/`, script `scripts/video/build_flattery_trap_v3.py`; v1 and v2 superseded)

Built on David's instruction, 2026-09-21.

- Candidate: `Prompts/flattery-trap-v3.mp4`; SHA-256
  `54c6c64f014599f3eac1d74bbde789ec7eb69f30bca6133489590642915723b6`; 9,881 frames at 30 fps
  (5:29.37), 1280x720.
- Narration: roll 4 start to finish, no cuts, plus the approved graft - roll 2's 2:31.23-2:35.00
  carrying "But while the problem has improved, it has not disappeared." - inserted at 2:37.23 in the
  pause after "…many different AI assistants." Audio only: roll 2's own picture there is an invented
  "Sycophantic Agreement Rate 82% -> 26%" chart, which the prompt bans and which never enters the
  build. Finished gaps 0.74 s before the grafted sentence and 0.78 s after. Graft trimmed -0.9 dB to
  match roll 4 (-16.3 against -17.2 LUFS). Only the engine outro after "not approval." is dropped. No
  pauses added. Standing instruction intact word for word at 4:52.9; close "Useful feedback points to
  the work." 5:20.2 and "Look for specifics, not approval." 5:22.2, last word 5:24.0, nothing after.
- Boards (output time): post-only Flattery vs. Useful Feedback 0:23.00-1:22.90 - the scenario strip
  rings at 0:28.9, the Flattery card at 0:38.7 then its Praised and Could Fit rows at 0:45.5 and
  0:50.5, the Useful Feedback card at 0:53.7 then its Named and Result rows at 1:04.4 and 1:07.8, and
  the banner at 1:10.6. Canonical How the Praise Got Baked In 1:22.90-1:52.83 with full-box-height
  column rings at 1:32.5, 1:39.0 and 1:44.1. Canonical Sycophancy 2:13.33-2:23.90, first paragraph
  ringed at 2:18.4 as the narrator reads its excerpt. Canonical Five Ways to Fight the Flattery Trap
  in three legs - 2:49.43-4:36.03 with row rings at 2:59.9, 3:20.8, 3:40.2 and 4:08.2; 4:43.03-5:00.23
  for the fifth move, ringed at 4:43.2; and 5:12.60-5:19.60 for the takeaway banner, ringed at 5:16.3.
  Standard close from 5:19.60 as the literal final frame.
- Both tall boards are compact: every line reads at full view (previews in the build folder), and each
  comparison card is taller than a 16:9 dive can hold, so the camera stays still throughout.
- Notebook spans kept: the student at the laptop, the marked-up essay, the artificial-praise card, the
  April 2025 calendar, the gag product, Update Rolled Back, the three devices, the training-model map,
  the speech bubble, the crossed-out thumbs-up, and the standing-instruction diagram with its
  limitation box. No photographs, no chapter cards, no invented statistics.
- Corner mark cleaned on every kept frame: 598 cloned, 2,054 inpainted, 0 declined.
- `transition_guard.py` 13/13 pass; strips inspected. Contact sheets reviewed end to end. Every one of
  the thirteen row boundaries measured: -60 to -73 dBFS in the 60 ms after the splice, peak sample
  difference at or below 0.004, no clipped words. Protected files (live video, three rolls, five
  boards, lesson) unchanged.

## Three QA rounds

1. **v1** passed on audio but `transition_guard.py` caught three leaks: roll 4 holds its own render of
   a board 4-5 frames past the pause the audio cuts in, so the Cycle, Five Ways and Five Ways (fifth
   move) exits each exposed Notebook's version of that board.
2. **v2** fixed them the same way Mind Trap v3 did - the audio boundary stays in the pause and the
   resumed picture starts at roll 4's own cut, leading its audio by 4-5 frames. Guard clean. But the
   audio measurement then showed the graft's own in-point sat 7 ms before roll 2 says "But", so the
   5 ms row crossfade was clipping the first word of the grafted sentence.
3. **v3** widens the graft into roll 2's own pauses on both sides (0.30 s lead-in, 0.25 s tail). All
   thirteen boundaries clean.

## Shipped

**SHIPPED 2026-09-21 on David's instruction.** `Prompts/flattery-trap-v6.mp4` copied to
`course-assets/flattery-trap/flattery-trap.mp4` (SHA-256 verified identical,
`2449fbb325ec90a9c3440e0a546ad45634f475e77860fffbe04ba6c54e04b936`, decodes 9,881 frames at 30 fps);
`index.html` cache key `?v=20260921ship5`; **pill corrected from "4 min" to "5 min"** — it had been
understating the old 6:07 live video by two minutes, and the new candidate is 5:29. Kit status line
added to `Prompts/AVOID-TRAPS-VIDEO-KITS.md`; registry note and generated checklist updated.

The build borrows picture only from rolls 2 and 3, not from the live video, so nothing here depends on
the superseded live file. Rolls 2, 3 and 4 are all still needed: roll 4 is the base, roll 2 the audio
donor, roll 3 the picture donor for the three interleaves. Roll 1 is now unused.

## Worth a look before shipping

- The Five Ways board carries one unbroken 106-second leg (2:49.4-4:36.0) while four of the five moves
  are taught, with a ring change every 20-30 seconds. That is far longer than any board run we have
  shipped (Training Bias 38 s, Mind Trap 55 s). It is what the lesson's own structure asks for, but it
  is your call whether it wants breaking up.
- The pill in `index.html` still says "4 min". This candidate is 5:29.

## Listening checks for David

1. 2:37.2-2:41.0 - the graft. Roll 2's voice against roll 4's, and both seams. The room-tone floors
   measure within a couple of dB, so there is no level step, but the voice match is an ear judgement.
2. 4:52.9 - the standing instruction, the one line that must land exactly.
3. 2:44-2:51 - the speech-bubble card holds its last frame for 4.1 s to absorb the graft's added
   frames. It is a static card, so it should read as a held illustration rather than a freeze.
4. The whole file end to end. I read the rendered transcript and measured every boundary, but I did not
   audition the audio.
