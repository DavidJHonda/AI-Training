# People Skills — engagement review of two new rolls vs. live (2026-09-26)

Why: David judged the live video one of the weakest for engagement and generated two new rolls on the 2026-09-25 kit.

| File | Length | Board use |
|---|---|---|
| `Prompts/people-skills-1.mp4` | 3:56 (speech ends 3:52.9) | Neither course board appears. Notebook redrew both. |
| `Prompts/people-skills-2.mp4` | 2:49 (speech ends 2:46) | Board 1 real; Board 2 = faceless upload, Notebook-highlighted |
| `course-assets/people-skills/people-skills.mp4` (live) | 2:53 | Both real boards, ringed (shipped 9/12, 9/21) |

Bundles (transcript, scenes, holds, sheets) are in this folder. Only the live file can be listened to as a finished edit. I checked the roll audio by transcript and RMS level only. Roll 2's trailing "Thank you." is a Whisper hallucination: the audio is -91 dB from 2:46. Roll 1's post-close sentence is real speech, measured at -22 dB.

## Verdicts

- **Roll 1 — REROLL.** It has the most engaging visuals of the three, but its narration fails:
  - It adds a sentence after the close: "In an entirely automated world, choosing to be deeply human is your ultimate technological advantage." That misses a hard requirement.
  - It misses the verbatim line. It says "AI can suggest what words to say… Earn someone's trust or do the rep." ("for you" is dropped twice.)
  - The register is stiff throughout: "invisible architecture of all collaborative success", "inverse relationship", "soft skill" (a banned word), "most critical professional currency", "behavioral reliability", "executing genuine connection".
  - It invents statistics on screen: a "Human Value Outshines AI" curve at 1:48 and a "Literal words 15% / Tone 35%" bar chart at 2:40.
  - Neither course board appears.
  - Its four-ways narration is RICH and near-verbatim (2:25–3:12), but the live video already has that.
- **Roll 2 — REROLL.** It has the snappiest pace and one good addition, but the Four Ways are THIN:
  - Each way is cut to one clause ("Ask a genuine follow-up question." / "Pay attention to tone and behavior." / "Give clear credit.").
  - Lost from the four ways: don't plan your reply, before offering your opinion, before assuming what's wrong, ask, remember what they tell you, and specific appreciation.
  - The "AI Isn't the Edge" title is never spoken: it goes "Second… Third…" with no "First".
  - Trust drops "and leaders" and "keep promises".
  - It uses "framework" (a banned word) and adds filler at 2:12–2:23 ("…no algorithm can replicate").
  - The verbatim line opens "Artificial intelligence can suggest…".
  - Accurate additions worth considering for the page: "AI raises the floor… human connection raises the ceiling" (1:14) and "Every single conversation is a live repetition" (1:39), which sets up "do the rep".
- **Live — KEEP (unchanged from 2026-09-24).** It is the only one of the three that teaches the whole lesson.

Neither new roll offers a narration graft worth making: the live file's narration is RICH at every point where either roll is.

## Why the live video feels flat (diagnosis)

1. **About half the runtime is two text boards.** Board 1 holds 34.6 s (0:57.8–1:32.4) and Board 2 holds 51.1 s (1:41.1–2:32.2). That is 86 of 173 s. Both exceed the ~20 s hold-break rule (Edit Spec 8b/1b, 9/23), which postdates this ship.
2. **Two 3D text cards bookend the lesson.** "AI Capabilities | The Human Element" runs 0:00–0:09, so the first image a student sees is a stock-looking title. "AI Suggestion | Human Execution" runs 2:32–2:40. They are static and say nothing the narration doesn't.
3. **The other drawings are static paper-craft stills.** There is no movement except the board camera.
4. **Structure (lesson-level, not editing):** the lesson is list → list → list (5 traits, 3 reasons, 4 ways) with no moment or person in it. The prompt forbids adding scenarios, so no roll can dramatize one.

## Proposed rebuild — v2: live narration, new pictures (visual-only retrofit)

Keep the live audio untouched: remux the live PCM (TECHNICAL-RECIPES audio-remux gotcha). Keep the shipped rings and the close. Replace the two text cards and break both board holds with roll 1's animated diagrams, which illustrate the exact instructions.

**Source limitation:** the live roll's raw generation is gone, so the live MP4 is the source. That means one extra encode generation.

**Style caveat:** roll 1 draws flat animated diagrams, while the live drawings are paper-craft. This style mix is the same one Your Choices shipped today.

| # | Live span (narration) | Now | Replace with | Why |
|---|---|---|---|---|
| 1 | 0:00–0:09.4 "AI can do amazing things… that is people." | 3D text card | Roll 1 0:00–0:09: chip "Digital Capability", then a people triangle "Human Connection" builds | The same sentence was spoken over it in roll 1, so the timing is nearly 1:1, and it opens on motion |
| 2 | 0:24–0:35.8 definition + five traits | Diagram with invented tiny sub-captions | Roll 1 0:24–0:41: Understand/Communicate/Collaborate, then the five traits appearing one by one | Motion on each named trait; *check its sub-captions at full res first* |
| 3 | ~1:06–1:13 card 1 explanation ("…how you actually work with people…") | Board 1 | Roll 1 ~1:20–1:30: identical AI outputs, then people light up ("Primary Differentiator: Human Collaboration") | Splits the 34.6 s hold into 9 s + 19 s |
| 4 | ~1:48–1:54.4 "Do not plan your reply… one genuine follow-up question" | Board 2 dive | Roll 1 2:28–2:37: Speaker / Active Listener, "Internal Opinion: PAUSED", then a "Follow-up Question?" arrow | Draws the instruction literally |
| 5 | ~2:10–2:18.5 "Remember what they tell you… explicit credit" | Board 2 dive | Roll 1 2:52–3:00: person with "Details", "Effort", "CREDIT" tags | Same |
| 6 | ~2:22–2:30.5 "address difficult issues… without attacking the person" | Board 2 dive | Roll 1 3:04–3:12: "CHALLENGE IDEAS, NOT PEOPLE", The Individual vs The Idea | Same |
| 7 | 2:32.2–2:40.6 "AI can suggest… or do the rep for you." | 3D text card | Roll 1 3:24–3:36: Digital Domain vs Relational Domain (1. Comprehension, 2. Reliability, 3. The Rep); tail on roll 1's empty table with a chip in the middle (3:39–3:42) | Its three rows are the sentence's three things |

The board still arrives on its introducing line and each card still gets its ring at the spoken header. Cutaways only take the explanation after the header. After the rebuild, the longest board run is about 19 s.

Optional, not planned: a cutaway under "Notice what isn't being said" using roll 2's arms-crossed figure (2:13–2:17). It is paper-craft style and static, so I lean against it. Roll 1's picture there is the fake bar chart: never use it.

Pauses: none. The natural gaps measured 9/24 already carry each subject change.

## Separate, bigger lever (David's call)

For more engagement than editing can give, the lesson needs one concrete moment, e.g. a group-project beat where someone goes quiet, and how the four ways play out. Per the 9/21 rule, the upload Markdown is the page, so this would be a page edit followed by a reroll. It would not be a prompt addition.

---

# Round 2 — rolls 3 and 4 on the rewritten Maya lesson (2026-09-26, later)

The lesson was rewritten around Maya, so the live video is donor material only. Sources: `lessons/people-skills.md` (the version with Maya), `index.html` 9562–9587, and the kit prompt of 09:35. Bundles are in `people-skills-3/` and `people-skills-4/`. I re-transcribed roll 4 end to end with medium.en at word level. Silences were measured by RMS (below -45 dBFS). I have not listened: David needs to hear 0:21.8 on roll 4.

## Roll 3 (3:25) — REROLL (visual donor)
- **Reads a stage direction aloud:** 2:31.9 "Pause for seven seconds of absolute silence."
- **Close not verbatim:** 3:09.7 "AI can write the essay or code the software, but it cannot be the empathetic person in the room. To build a successful career, you need to listen well… your peers want to work with."
- **Four ways THIN:**
  - Notice drops "If you're unsure what a change means, ask."
  - Show drops "Remember what they tell you."
- **Board 3 THIN:** the "You'll Stand Out" title is never spoken; Trust is cut to "listen and respect them".
- **Invented detail:** "as you're packing up", "he says", "secure a better grade". 0:33 says "She is clearly stung", which asserts the certainty the prompt forbade.
- **Banned words:** framework, interpersonal dynamics, collaboration.
- **Visuals:** the best of any People Skills roll. A consistent illustrated Maya (auburn hair, jersey 96) and teammate (glasses, jersey 4) carry the whole story: celebration, Maya pointing at the screen, the stop-hand interrupt, a face close-up, Maya slumped, the group packing up without her (split top-down view), Maya and #4 over "Example 3", a Maya portrait, and Maya peeking over the table.
- **Continuity trap:** at 0:18–0:27 the interrupter is #4, but the canonical Next Move board makes #4 the one who invites her back. Do not use that shot.
- Also skip the off-model blonde "9" at 1:16 and the invented "A+" at 1:20.

## Roll 4 (2:10) — REPAIR
Near-verbatim spine.
- **Four ways RICH:** all four are word for word with the card, including "If you're unsure… ask".
- **Close verbatim.**
- **Reflection question verbatim.**

Failures:
1. **WRONG, 0:21.80–0:22.44: "She seems heard."** Both base.en and medium.en hear "heard" with high confidence; the lesson says "hurt". No roll has a donor. Repair: cut the sentence. There is silence on both sides (21.36–21.78, 22.44–23.30), leaving "…body language changed. / What would you say or do next?" This leaves the verbatim line "She seems hurt" MISSING; a drawing of Maya's hurt face can show it, but the words aren't spoken. David's call: accept the cut or reroll for it.
2. **THIN, 0:42.02–0:43.38: "Her idea deserves to be heard."** It drops "even if the group decides not to use it." Donor: roll 3, 1:21.16–1:27.64, "Even if the group had ultimately decided to keep the draft exactly as it was, her idea deserved to be heard and considered." It is a whole beat between silences (0.72 s before, 0.90 s after), in the same Notebook voice. It adds +5.1 s. The seam needs a listen.
3. **No reflection pause:** 1:38.24–1:39.16 is a 0.92 s gap after "What would you say?". Propose about 4 s, under a Maya drawing.

TAUGHT (pass, noted):
- 0:34.9 "what she says matters": the board banner reads "has to say".
- 0:38.4 "The third example misses the instructions, helping the group improve."
- Board 3 is compressed:
  - Stand Out: "As AI normalizes polished work, collaboration sets you apart."
  - Trust drops "leaders" and "treat others well".
  - Connection: "people need to feel valued".

Visuals: weak and flat. A near-empty background for 0:00–0:04, UI cards, "YOUR TURN ⏸" 3D text at 1:32, and only one Maya shot, which is faceless and cropped. Two usable diagrams: Notice (1:00–1:10, Speaker/Observer with Tone/Hesitation/Enthusiasm/Behavior Shift) and Challenge (1:24–1:30, Person A/B with the idea in the middle). Board 2 appears as the Notebook-highlighted faceless upload, so it will be replaced.

## Best-of plan (PROPOSED)
BASE: roll 4 (it alone teaches all four ways and the close verbatim). NARRATION: 1 cut (#1), 1 graft (#2), 1 pause (#3). PICTURES: roll 3's Maya drawings for the story and the question; canonical boards; roll 4's own two diagrams.

Output timings below are roll-4 source times; everything after 0:42 shifts by about +5.1 s from the graft and about -1.5 s from the cut.

| Span (roll 4) | Narration | Picture |
|---|---|---|
| 0:00–0:07.1 | finished project, group feels great | roll 3 0:00–0:11 (group at table → celebration) |
| 0:07.8–0:10.8 | Maya notices a problem | roll 3 0:11–0:18 (Maya pointing at the laptop) |
| 0:11.6–0:14.6 | "Someone interrupts. We are done…" | roll 4's own red "We are done. No more suggestions." callout (avoids the #4 stop-hand continuity clash) |
| 0:15.4–0:17.3 | Maya goes quiet, group moves on | roll 3 0:36–0:38 (group packing, Maya apart) |
| 0:18.3–0:21.4 | expression and body language changed | roll 3 0:27–0:32 (Maya face close-up) |
| 0:23.3–0:27.4 | "What would you say or do next? … people skills" | roll 3 0:38–0:56 (top-down split: Maya alone vs group) |
| 0:27.4–0:37.1 | Your Next Move | **Canonical board**, full view (compact). Ring the speech bubble at 0:30.08 "Ask, Maya…"; ring the banner at 0:34.94 "Show her…" |
| 0:37.2 → graft end | "Maya has a point… third example…" + roll 3 "Even if…" | roll 3 1:04.8–1:12.4 (Maya and #4 over "Example 3"), slow push |
| 0:44.3–1:02.4 | Four Ways intro, Listen, Notice header | **Canonical board**: full view, then dive card by card. Listen ring 0:49.04; Notice ring 0:59.30 |
| 1:02.4–1:10.3 | Notice instruction | roll 4's own Notice diagram (1:00–1:10) |
| 1:10.3–1:23.7 | Show + Challenge header | Board again, dive. Show ring 1:11.10; Challenge ring 1:20.70 |
| 1:23.7–1:30.4 | Challenge instruction | roll 4's own Challenge diagram (1:24–1:30) |
| 1:31.3–1:38.2 + ~4 s pause | "Think back to Maya… What would you say?" | roll 3 2:20–2:27 (Maya portrait), then roll 3 2:40–2:46 (Maya peeking over the table) through the pause |
| 1:39.2–1:58.1 | People Skills Matter More | **Canonical board**, full view, whole-card rings: Stand Out 1:42.24, Trust 1:48.12, Connection 1:53.52 |
| 1:58.96 → end | close lines | standard close |

The longest board runs are about 18 s (Four Ways) and about 19 s (Matter More), both within the hold-break rule.

Fallback if David rejects the "heard" cut: one more roll, grafting only the opening (0:00 through "…use your People Skills.") from the new roll. The rest stays roll 4.

---

# Build — Prompts/people-skills-v2.mp4 (2026-09-26, David: "build it")

- **Build:** `scripts/video/build_people_skills_v2.py`. The manifest, board state sheets, and transition strips are in `build-v2/`.
- **Output:** 4157 frames at 30 fps, 2:18.57, 1280x720, -20.9 LUFS.
- **Verified checks:**
  - **Transcript** (base.en on the encoded file): the plan's narration in order. "She seems heard" is gone. The roll 3 "Even if…" sentence is in place, followed by all four ways and both closing lines.
  - **Splices:** `transition_guard.py` passes all 19. The first render flagged the Four Ways return (f2243): the board came back on Notice and panned to Show 0.4 s later. The fix: the camera leads (`lead_camera`), and the Show move completes under the Notice diagram (`camera_at` 70.30). It now returns settled on Show.
  - **Measured gaps at every audio seam:**
    - cut "She seems heard": 0.74 s (21.36–22.10)
    - into the graft: 0.62 s (40.28–40.90)
    - out of the graft: 0.94 s (47.38–48.32)
    - reflection pause: 3.92 s (102.20–106.12)
  - medium.en hears every word either side of the cut and the graft.
  - **Corner mark:** 578 frames cloned and 1060 inpainted, none declined. The graft leg had 219 frames inpainted, and its first 4 frames (the tail of roll 3's A+ drawing) are covered.
  - **Final frame:** the close board.
  - **Protected files unchanged:** both rolls, all boards, the close JPG, and the live MP4.
- **Tool fix:** `make_close_board.py` now strips the `?v=` cache key from `CLOSE_BOARD_ASSETS` paths. The peopleskills entry carries one as of today, which broke `--lesson`.
- **Not done:** I cannot listen. David to check by ear:
  - the cut at 0:21.4 ("…changed. / What would you say")
  - the graft seams at 0:40.9 and 0:47.4 (roll 3 voice and level, -0.3 dB)
  - the pacing of the 3.9 s pause
- **Known, accepted:** 0:11–0:15 is roll 4's own flat callout card, which carries small invented labels ("Case 3: Roman Governance", "TIMELINE ERROR"). "She seems hurt" is not spoken (David accepted the cut). Board 3's compressed wording is TAUGHT.
- **Status:** review candidate, not shipped. The live video is unchanged.

---

# v3 — Prompts/people-skills-v3.mp4 (2026-09-26, David after watching v2)

Instruction: "Delete from 1:35 to 1:45. The part about 'Think back to Maya...'".

`scripts/video/build_people_skills_v3.py` is v2 with roll 4 90.80–98.70 removed, which includes the Maya question and the 90-frame pause. v2 is left untouched.

- **Output:** 3830 frames, 2:07.67.
- **New join:** "…without attacking the person." / "People skills matter even more in the AI future." The gap is 0.88 s (94.34–95.22), and medium.en hears both sentences whole. The picture cuts from the Challenge diagram straight to the Matter More board (f2843, strip clean).
- **Checks:** `transition_guard.py` passes all 16 boundaries. No corner-mark frames were declined. Protected files are unchanged, and the final frame is the close board.
- **Note:** the page's "Apply It to Maya" section still asks the question. The video no longer does, by David's call.
- **Still for David's ear:** the cut at 0:21 and the graft seams at 0:41 and 0:47 (all unchanged from v2), plus the new join at 1:34.
