# Document Trap v1 — stitched from the donors (2026-09-21)

`Prompts/document-trap-v1.mp4` — 3:46.00 (6780 frames), built by
`scripts/video/build_document_trap_v1.py`, audit bundle in this folder.

Ten rolls never landed the lesson's eleven verbatim lines in one take. Rolls 9 and 10 (3 of 11) were
worse than 7 and 8 (7 of 10), and the reroll review called for restoring the kit and rolling again.
This build stops rerolling and assembles the best take of each beat instead.

**Verdict: the best Document Trap that exists. It is the only version that speaks both the
"wasn't made up / incomplete" line and the "uploaded means fully read" line, explains moves one and
two rather than just naming them, and pays off the six-foul result on screen. Ready for David's eye
test; nothing shipped, live 2026-09-08 video untouched.**

## What it is made of

| | source | carries |
|---|---|---|
| spine | roll 7 | the lesson's order and 7 of the 11 verbatim lines |
| graft `lines34` | roll 3, audio only | "The answer wasn't made up, it was just incomplete." … "The document trap is thinking uploaded means fully read." — roll 7's own version of this stretch comes out |
| graft `moves12` | roll 8, audio only, −2.6 dB | moves one and two named *and explained*; roll 7's bare "Start with name the section and ask one thing." comes out |
| graft `askone` | roll 8, with its picture, −2.6 dB | "Asking only about personal fouls keeps the system focused entirely on a single question." — inserted, no roll 7 words removed |
| graft `sixfoul` | roll 3, over roll 8's panel, +0.2 dB | the verified six-foul result — inserted, no roll 7 words removed |

Rolls 7, 8 and 3 sit within 0.2–2.6 dB and 167–186 Hz, so the voice is continuous. Boards 1–3 are the
canonical page assets; roll 8's own retrieval footage carries the applied-moves stretch. Standard close.

## The eleven required lines

7 verbatim from roll 7: the foul question, "Five fouls and you foul out.", "Search decides which parts
reach the answer.", the full three-sentence tournament prompt, "A quotation is useful because you can
check it, not because AI quoted it.", "A missing passage can change the answer.", "Ask for the passage.
Then check it."

3 now spoken but a word off — and **no roll anywhere says them clean**, so this is the ceiling, not a
build defect: roll 3 says "wasn't made up, it was *just* incomplete" (no roll drops "just"); roll 3
leads with "*The* document trap is thinking…"; every one of the ten rolls says "doesn't mean *the* AI
has read it all."

1 still unspoken: "In this example, the tournament rule allows six fouls." No roll speaks it. Roll 3's
"uncover the verified six-foul tournament exception" carries the result in the narration, and roll 8's
panel shows the confirmed six-foul quote on screen underneath it. That is the best available without
an eleventh roll.

## QA

- **transition_guard: 15/15 pass, 0 failed** (`transition-audit/`). Strips inspected by eye at all four
  graft boundaries and the board arrivals — single clean cuts, no stale frames.
- **Audio.** Every one of the 15 row boundaries measured in the finished file sits in a pause: −49 dB
  or quieter across ±30 ms, with no word onset inside 60 ms of any graft in-point. No clipped words.
- **Gemini mark: 0 declined** (3206 frames cloned, 132 inpainted). `watermark_scan` reports 6 hits from
  1:30–1:37.5 — **false positive**: that span is the rendered Split, Search, Load board leg, and the ROI
  is sitting on the board's own `besmarterthanthetool.com` credit line, confirmed by eye at frame 2925.
  No residual mark.
- **Rings.** Boards 3's four cards each ringed to their own measured edges, no shadow trace, no clipped
  text; Board 1 rings only its banner, never the photograph; Board 2's columns run the shared box's full
  height. Built under the artwork-scaled ring rule.
- **Camera.** Board 1's walk lands where it was aimed: the glowing tray of selected pages, then the page
  with 5 struck through and 6 circled.
- **Transcript reads continuously** — the four grafts are undetectable in the prose.
- One decode artifact, not an audio fault: `small.en` and `base.en` hear "This trap does not **stare** on
  the basketball court"; `medium.en` hears "**stay**", which is what the line is. Noted so it is not
  re-flagged.

## Longest unbroken board run

29.0 s (Split, Search, Load). The narration is walking the board's three columns for the whole run.

## If David approves

1. Install over `course-assets/document-trap/document-trap.mp4`.
2. `index.html` line 1117: the entry still has **no cache key at all** and reads **"5 min"**. It needs
   `?v=20260921ship7` and **"4 min"** for a 3:46 runtime.
3. Commit the build script, this bundle and the reroll2 bundle.
