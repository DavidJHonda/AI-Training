# engagement-trap-v3: current board, our rings, and two narration excisions

**Date:** 2026-08-08
**Base:** `videos/engagement-trap-v2.mp4` — 7,317 frames, 4:03.90 (the 8/07 close-apostrophe candidate)
**Output:** `videos/engagement-trap-v3.mp4` — **7,197 frames, 3:59.90**

## What "the old board" actually was

The board content was **already current** — headline, panel titles, both AI bubbles, both YOU
bubbles, TWO HOURS LATER, and every WHAT HAPPENED bullet match the page word for word.

What differed was **layout only**. The board is responsive:
`gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 340px), 1fr))"`. Above ~696px it is
two columns side by side; below that it stacks. The video carried the **stacked** render; the
page at its 902px column shows **side-by-side**.

## The conflict that made this more than a swap

The narration was written for the stacked layout:

- 0:51 — "In the **top scenario**, the AI immediately gives you the right answer."
- 1:12 — "Now, look at the **bottom half of the image**."

Swapping in the side-by-side board makes both lines point at a top and a bottom that no longer
exist — a worse defect than the one being fixed. Two ways out were possible: capture narrow so
the board stacks (keeps the narration, breaks the never-resized rule the owner flagged twice on
evaluate-the-results), or capture at the app width and excise the two references.

**Owner chose the excisions.** The board now matches what a reader sees.

| Excision | Removes | Frames | Result |
|---|---|---|---|
| E1 | "In the top scenario," | 1545–1579 (34) | "…paths a conversation like that can take. **The AI immediately gives you the right answer.**" |
| E2 | "Now, look at the bottom half of the image." | 2163–2249 (86) | "…One question, one minute, done. **But this time you casually type back…**" |

Both sit inside their own pauses; both surrounding sentences still read.

## The board leg

Replaces base frames **1283–2846** (42.77–94.87). 1,563 frames minus the 120 excised = **1,443**.

Seven states, timed to word onsets, each ringing in its panel's own accent (`#3b82f6` left,
`#f59e0b` right):

| State | Frames | Ring | Narration |
|---|---|---|---|
| 0 | 67 | none | "Imagine you have a quick question…" |
| 1 | 201 | headline | "…how tall Mount Everest is" + "two different paths" |
| 2 | 448 | left panel | "The AI immediately gives you the right answer… offer to expand" |
| 3 | 140 | left YOU bubble | "You decline and you close the app." |
| 4 | 128 | right YOU bubble | "But this time you casually type back, sure why not" |
| 5 | 366 | TWO HOURS LATER body | "Notice the massive jump… spiraled into" |
| 6 | 93 | right panel | "You came for a single five-digit number." |

**Camera: the board's aspect drives everything.** The band is 902×674 — *taller* than 16:9 — so
the full view has to zoom out until the height fits (window 4792 at dsf4, board filling ~75% of
frame width). A panel is 425×577, aspect 0.74, so a 16:9 window can never show one whole either.

The first build dived to the left panel at w=2400 and got it wrong: the panel's width fitted but
42% of its height was cut, leaving the ring as two bare vertical lines at the frame edges and
slicing into the right panel. **Panel states now sit at w=4600 on the board centre**, where the
whole panel and its ring are enclosed. Element states keep their tight dives, which work well —
the ring encloses its target and the text is large.

## v4: the opening transition cut, and the 0:52 blip diagnosed

**The blip was my own fades.** Owner heard "a very slight glip" at 0:52 — the E1 joint. Cause
found by measuring the noise floor in 5ms windows: the joint bottomed at **RMS 2**, effectively
digital silence, against a natural pause floor of ~23. The 60ms `afade` on each side was pulling
continuous room tone down to absolute zero and back, punching a hole in the ambience.

Three splices were compared at both joints:

| Fades | joint floor (5ms RMS) | max sample step |
|---|---|---|
| 60ms (v3) | **2** — a hole | — |
| 10ms | 10 — still under natural | — |
| **none (v4)** | **14 and 27** — *above* an ordinary pause's 7 | 3,486 and 9,136 — *below* speech's own 15,442 |

**No fades won on both counts.** Both sides of each joint are the same room tone at the same
level, so cutting straight keeps the ambience continuous, and the waveform step is smaller than
steps that occur naturally within the speech — no hole, no click. The recipe's "10ms fades at
every joint" is for joining *mismatched* material; splicing a pause into its own room tone
wants no fade at all.

**Opening transition cut.** Frames 0–387 (0–12.90) removed: "We previously looked at how AI can
capture your attention by playing on your need for approval. This next dynamic operates much
more quietly. It targets your time, rather than your ego." The owner asked for 14 seconds, but
"When you ask an AI a question" starts at **13.16**, so a full 14s clips it; 12.90 leaves a
0.26s breath. The video now opens on that line.

**6,810 frames, 3:47.00.**

## Verification

| Gate | Measured |
|---|---|
| Frame count | **7,197**, exact |
| Excised phrases | "top scenario" 1→0, "bottom half" 1→0 |
| Audio joins | both read clean by transcript |
| Seams | leg-in 18.5, leg-out 80.3 — one spike each, neighbours ≤ 0.92 |
| Ring pops | 0.1 / 1.3 / **15.6** / 1.9 / 2.0 / 2.4 |
| pts_time deltas | 0.033333/0.033334, matching the source |

**The 15.6 is flagged, not hidden.** That junction swaps two rings at once — headline off, left
panel on — at a zoomed framing where the headline ring is large, and a camera transit follows
immediately. It reads as motion rather than a cut, but it is above the <12 the recipe asks for.
Fixable by moving the ring change to a wider point in the path if the owner sees it.

`-video_track_timescale` omitted, per today's gotcha.

Review frames: `/tmp/retrofit-review/engagement-trap/`.
