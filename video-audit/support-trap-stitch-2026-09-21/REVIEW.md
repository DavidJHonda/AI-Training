# Support Trap v4 — roll 1 plus three grafts and one added pause (2026-09-21)

`Prompts/support-trap-v4.mp4` — 4:23.67 (7910 frames), built by
`scripts/video/build_support_trap_v1.py`. Three-way comparison of rolls 1 and 2 against the live video
is in `video-audit/support-trap-comparison-2026-09-21/REVIEW.md`.

**Verdict: ready for David's eye test and ear. Every measurable check passes, and the accuracy
requirements were verified on the encoded file rather than assumed from the plan. Nothing shipped;
the live video, rolls, lesson and boards are unchanged.**

## What it is made of

| | source | carries |
|---|---|---|
| spine | roll 1 | the lesson's order, both safety-critical lines verbatim, the fullest Board 1 and Board 3 |
| `blackbox` | live video, audio only, +1.1 dB | "After Sophie died by suicide, her mother described the chats as a black box. The AI offered empathetic words, but those private conversations held crucial details that made it harder for the people around her to understand how serious her distress was and to intervene." |
| `leavechat` | roll 2, own picture, +0.7 dB | "Most of AI literacy is about how to use tools well. Here, using the tool well means knowing when to leave the chat." |
| `cwlead` | live video, own picture, +1.1 dB | "A quick note before we continue." — **and the live video's full-screen CONTENT WARNING card**, which then holds across the note and the pause |
| added pause | matched room tone, 100 frames | **3.96 s** of silence under the warning card, against roll 1's own 0.52 s |

**David's note, 2026-09-21:** "I do like the way the live video has the content warning at 2:00." He was
right, and it was more than the wording: the live holds a full-screen **CONTENT WARNING — Sensitive
subject matter regarding self-harm** card for 8.4 s across the spoken line and the silence, while v3
played roll 1's line over a drawing of an empty chair. Restrained, but no visual warning at all, so a
viewer who needed to look away got no signal and anyone watching muted got none either. The card and the
lead-in are now borrowed; **roll 1's wording stays**, because "The next story discusses suicide." is the
lesson's line and the live video's "The following story…" is not. The beat now runs 0.58 s of room tone,
the lead-in, 0.48 s, the exact note, then 3.96 s of silence - the card on screen throughout.

Roll 1 −16.92 LUFS / 168.4 Hz, live −17.98 / 170.2, roll 2 −17.59 / 170.2; pause floors −60.6, −63.1
and −59.0 dB, within 4 dB, so no noise cliff.

## Why the blackbox graft exists

This is the one that matters. Roll 1 said, of a real young woman's death:

> "**Because she relied on the bot**, the AI's isolated digital environment **actively** held details that
> made it harder for the real people in Sophie's life to understand the severity of her distress."

That asserts a cause the lesson does not assert and gives the software intent; the prompt forbids
inventing causes here. Roll 2 fails the same sentence differently, generalising it into "Pouring distress
into an AI creates a false sense of communication", and additionally drops "by suicide" — the exact
euphemism the 2026-09-19 repair removed from the live video. Only the live video's repaired passage stays
with the lesson's claim, so it is grafted back in.

## Accuracy requirements, verified on the encoded file

| Requirement | Result |
|---|---|
| Content note exactly as written | **MET** @2:16.50 "The next story discusses suicide." |
| Room for a pause after it | **MET** — **3.96 s** measured, under the warning card (roll 1 alone: 0.52 s) |
| A visual content warning | **MET** — the live video's CONTENT WARNING card holds across the lead-in, the note and the pause |
| Attribution to Laura Reiley, 2025 | **MET** @2:18.50, with "her 29-year-old daughter, Sophie Rottenberg" |
| No invented cause | **MET** — roll 1's causal claim is gone; the live passage states only what the lesson states |
| "died by suicide", not euphemised | **MET** @2:54.80 |
| 988 and 911, said distinctly | **MET** @3:27.80 "In the U.S., call or text 988 for crisis support." / @3:31.80 "Call 911 if someone is in immediate danger." |
| Safety outranks secrecy | MET in substance — roll 1 says "Safety always outranks secrecy" (the lesson has no "always") |
| Two closing lines, exact, nothing after | **MET** @4:12.80–4:18.80 |
| Drawn scenes only | **MET** — the Sophie passage runs over an empty chair, a phone on torn paper, a literal black box and a drawn support-system panel. No photographs, no people, no logos anywhere in the file. |

## QA

- **transition_guard: 12/12 pass**, no false positives.
- **Audio: zero dips** at any of the 12 row boundaries.
- **No true-silence windows** anywhere — room tone is continuous end to end.
- **Gemini mark: 0 hits across 176 sampled frames, 0 declined.**
- **Boards.** Ring colour measured off each board, never chosen: Board 1's scenario strip #5e45b9 → purple,
  "Your Older Sister" #3066e3 → blue, "The Chatbot" #a87b2e → amber; Board 2 teal and red; all three
  Board 3 cards red. Each ring hugs its own measured card body.
- **Every picture edge inspected frame by frame**, not just the ones the guard flagged.
- **Protected sources: 6/6 hashes unchanged.**

### Three defects QA caught

1. **A hole of true digital silence.** The live video carries ~200 ms of absolute zero at 168.76 — an
   artifact of its own 2026-09-19 build — and the graft, ending inside it, punched 120 ms of dead air into
   the candidate. The donor out-point now stops at 168.70, keeping 0.36 s of its real room tone.
   **`silencedetect` reports true zero and quiet room tone identically; splicing into zero leaves a hole
   no crossfade can fill.**
2. **Five frames of roll 1's own Board 2 recreation** survived after our canonical board left (2790–2794).
   **transition_guard did not catch this**: its recreation is near-identical to the real board, so the cut
   between them fell under the detector's change threshold and the two-cuts-within-six-frames pattern never
   formed. Only a frame-by-frame look found it. Fixed with `picture_advance` to roll 1's own cut at 2795.
   The same class at Board 3's exit was anticipated and handled by `cover_intro` (9 frames).
3. **A truncated candidate after the disk filled.** The first render died of ENOSPC mid-write; the rebuild
   then hit the build's own "dest exists" assertion, which correctly refused to overwrite. Worth knowing:
   that assertion message contains the output filename, so a watch that greps the log for the filename
   reads the failure as a success. Watch for the failure patterns first, and verify the MP4 opens.

## Notes for the eye test

- **Board 1 runs 60.1 s** — the longest in the file. Roll 1 covers the whole comparison in a single
  unbroken scene, so unlike Engagement Trap there is no alternate footage to cut away to. The camera dives
  to the scenario, then each reply's card, then pulls back for the banner.
- **Board 2 is thin in every version and cannot be fixed by editing.** The lesson lists three things AI can
  do and four it cannot; roll 1 speaks two and three, roll 2 a different two and three, and the live
  video's sentence is broken. Only a reroll gets the board whole.
- **"Safety always outranks secrecy"** carries an "always" the lesson does not have.
- The narrator's board-furniture habit persists ("This guide defines…", "This is a protocol chart showing…").

## v4 against the live video, beat by beat

| Beat | v4 | live |
|---|---|---|
| Board 2 "What Is Missing" | intact, 3 of 4 items | **broken sentence** — "Notice what you leave out of your prompts" |
| 988 / 911 | **exact, two distinct sentences** | inverted — "If someone is in immediate danger, call 911" |
| Content note wording | **exact** | "The following story discusses suicide." |
| Content warning card and pause | **card + lead-in + 3.96 s** (borrowed) | card + lead-in + 4.7 s |
| Three roles before the story | all three named and explained | danger not clearly a third role |
| Board 3 "Do It Now" | fullest — cannot call, show up, protect, carry responsibility | paraphrased |
| "Know When to Leave the Chat" | present (roll 2) | **missing** |
| Sophie's surname | Rottenberg | "Sophie" only |
| Black-box passage | the live video's own repaired passage, grafted | same |
| Runtime | 4:23.67 | 3:40 |

v4 is ahead of the live video on every beat except the length of the pause, which is 0.7 s shorter.

## Separately: the live video has a broken sentence, shipped

At 1:48 the live video says "AI cannot take physical action. **Notice what you leave out of your prompts,**
take responsibility, or check on you the next day." — Board 2's list with its governing "AI cannot" lost
and "notice what changed" replaced by an instruction to the viewer. Confirmed on two decoders. This
candidate replaces it, but it is worth knowing it is live right now.

## At ship time

`index.html:1136` carries `?v=20260920ship1` and "4 min"; both need updating (4:20.77 keeps "4 min").
Board 1's refreshed illustration is already committed (`cc7e16e4`).
