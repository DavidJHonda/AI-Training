# One More Thing v7 — build verification (2026-09-22)

**Candidate:** `Prompts/one-more-thing-v7.mp4` — 8077 frames, 4:29.23, 1280x720, 30 fps.
**Built by:** `scripts/video/build_one_more_thing_v2.py`. (v6 is deleted; it carried the clipped word below.) **Manifest:** `edit-manifest.json`.
**Plan:** `video-audit/one-more-thing-comparison-2026-09-22/REVIEW.md`, approved by David 2026-09-22
("Build it"), optional third graft declined.
**Scope:** review candidate only. The live `course-assets/one-more-thing/one-more-thing.mp4` (v5) is unchanged.

## What was built

Roll 2 (`one-more-thing-2.mp4`, KEEP) uncut as the spine, plus the two approved grafts from roll 1,
both audio-only so roll 2's picture never has to carry roll 1's, both landing under one of our own boards.

| Graft | Donor (roll 1) | Into roll 2 | Length | Gain |
|---|---|---|---|---|
| The five tries in order | 52.33–61.03 | gap at 84.73, under Board 1 | 261 f / 8.70 s | +1.6 dB |
| The tokens-AI-writes caveat | 216.27–219.37 | gap at 235.70, under Board 3 | 93 f / 3.10 s | +0.9 dB |

Three boards, all at roll 2's own visual cuts, all compact full view with no dives — every ring target is a
whole panel, column or card, so there is nothing on these boards small enough to need a camera move.

| Board | Source span | Ring order |
|---|---|---|
| Same Probabilities, Different Choices | 1570–3546 | The Probabilities 57.28 → the Other row 68.16 → Five Separate Tries 74.40 (held through graft 1) → banner 89.40 |
| How Temperature Changes the Odds | 3546–5013 | Low Temperature column 130.62 → Spot's 36% 139.32 → High Temperature column 146.00 → Other's 39% 150.80 → banner 162.68 |
| The Math Adds Up Fast | 6187–7291 | One Token 213.24 → A Short Answer 217.28 → A Longer Conversation 227.88 (held through graft 2) → banner 239.68 |

Ring onsets are roll 2's own spoken timestamps. Because each graft inserts frames inside its board, those two
legs are rendered longer than their source spans by the graft length, the `keep()` after each graft picks the
leg up past it, and the onsets after a graft carry the graft's duration (Board 1's banner 89.40 → 98.10,
Board 3's banner 239.68 → 242.78). Board 3's middle ring fires on "Now look at the middle panel" (217.28)
rather than on the sentence after it.

Three pauses of one second, at idea boundaries only: 3801 (into "so how do you control that variety"),
5304 (into what a single answer costs), 7692 (before the closing message).

## v7: a clipped word in front of two of the pauses

David on v6: "At 4:16, there's an audio glitch. It starts saying the word 'Not' before the closing message
starts." Correct, and the same defect was in one more place. Both audio splits had been taken from
Notebook's own **picture** cut, and its cuts land a few frames after the next line has already begun.

| Pause | v6 split | Next line actually starts | Frames of it stranded | v7 split |
|---|---|---|---|---|
| Board 3 → close (4:16) | 7291 / 243.033 | "Not a mind." at 7283 / 242.76 | 8 | **7278 / 242.60** |
| Board 1 → Board 2 (2:06.8) | 3546 / 118.200 | "So how do you control that variety?" at 3544 / 118.14 | 2 | **3540 / 118.00** |

Both new splits sit inside the silence (242.44–242.76 and 117.85–118.14), and the row after each pause
picks up at the same source frame the row before it ended on, so no audio is dropped: still 8077 frames.
On the finished file both lines now read whole ("So how do you control that variety?" at 127.92, "Not a
mind." at 257.98) and both pauses are entered from silence.

**Rule this establishes:** take a pause split from the silence, never from `scenes.py`. The scene cut tells
you where the picture may change; it does not tell you where the sentence begins.

## Two departures from the plan as written

1. **Graft 2 starts after roll 1's "Keep in mind,"** (216.27) rather than at the sentence head the review gave
   (215.56). Roll 2's very next line is "Keep in mind, these are conservative estimates for an imagined model",
   and the two openings back to back read as a stutter. The finished narration reads: "…around two quadrillion
   calculations. **These counts only cover the tokens the AI actively writes.** Keep in mind, these are
   conservative estimates for an imagined model. Even a short answer takes trillions of calculations."
2. **Per-graft levels instead of one file-level correction.** The review's +2.1 dB came from the whole-file gap
   (roll 1 −17.6 LUFS, roll 2 −15.5). Measured over the spans themselves: donor 1 is −18.3 integrated and
   −18.9 short-term median against roll 2's −17.1/−17.2 either side (≈1.7 dB), donor 2 is −15.2 against
   −14.7/−14.0 (≈0.9 dB). A first render at +2.1 came back 0.5 and 1.25 dB hot on the finished file, so the
   shipped candidate uses +1.6 and +0.9. On the finished file the grafts now sit inside their neighbours'
   speech level (graft 2 exactly between them; graft 1 still reads slightly hot on raw RMS, which is not
   K-weighted and ignores the pauses between the five tries — both LUFS methods agree on 1.6–1.8 dB).

## Verification

| Check | Result |
|---|---|
| Decoded frame count | 8077, matches the manifest exactly (4:29.23) |
| Engine corner mark | 2209 frames cloned, 535 inpainted, **0 declined** |
| Protected files | all unchanged (live MP4, lesson Markdown, donor roll, three board JPGs) |
| `transition_guard.py`, 12 declared boundaries | **pass, 0 failed** (strips in `transitions/`) |
| Graft picture continuity | mean per-pixel diff across all four graft joins 0.005–0.52; the board leg runs straight through |
| Pauses | all four frozen (max frame diff 0.01–0.52, i.e. encoder noise on a held frame) |
| Close | standard close card is the literal final frame, with the prescribed push and 4 s settle |
| Verbatim lines | all 8 present in the output transcript (`transcript.txt`) |
| Both grafts | read whole and unclipped, no "Keep in mind" stutter |
| Pause entries | all three entered from silence; no clipped word attacks (the v7 fix, re-measured on the finished file) |
| Source watermark | frame 0 and five sampled drawings clean; no Getty or stock mark anywhere sampled |

Contact sheet: `contact-sheet.jpg`. Ring states: `states-*.jpg`. Output transcript: `transcript.txt`.

## Open for David

1. **Both graft joins want your ear.** They are the only two places where a second roll's voice enters, at
   84.96–93.64 and 246.62–249.64 in the finished file.
2. **A kept Notebook drawing contradicts Board 1.** Frames **755–1309 (0:25.2–0:43.6, 18.5 s)** show Notebook's
   own "Vocabulary Distribution (Next-Token Probabilities)" bar chart for the same dog-name prompt, with
   **Spot 22%, Max 14%, Bella 11%, Luna 8%, Charlie 7%, Rocky 5%, Daisy 4%, Buster 3%**. Nine seconds later the
   course board says **Spot 22%, Max 17%, Buddy 14%, Rex 9%, Biscuit 6%, Other 32%**. Only Spot's 22% is spoken
   over the chart, so nothing wrong is said — but the numbers and four of the names are legible and they do not
   match the board the lesson is built on. The rest of that span (the prompt typing in, and the "100 Independent
   Trials — 22/100 picks for Spot" grid) is good and directly illustrates the verbatim line. Options: leave it;
   cover just those 18.5 seconds with Board 1's full view, which would put Board 1 on screen from 0:25 to 1:58;
   or ban invented probability tables in the next roll of this kit. Not changed here — it is outside the
   approved plan.

## If it ships

Install as `course-assets/one-more-thing/one-more-thing.mp4`, bump the `inference` cache key in
`LESSON_VIDEOS` (currently `?v=20260918ship1`), and leave the pill at "4 min" — 4:29 still rounds to 4.
