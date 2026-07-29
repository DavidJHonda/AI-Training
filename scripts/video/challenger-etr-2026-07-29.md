# evaluate-the-results challenger — 2026-07-29

One roll in `Prompts/`, against the sitting video. Both graded in the same sitting
under r3, with the **redefined Pacing** (allocation, not runtime) in force for the
first time. Nothing moved: the challenger is a REJECT by 3 points.

| | incumbent | challenger |
|---|---|---|
| runtime | 4:12.47 | 2:59.27 |
| Coverage (20) | 17 | 16 |
| Lesson's material (15) | 13 | 13 |
| Teaches vs recites (15) | 11 | 12 |
| Board content (10) | 9 | 9 |
| Cleanliness (20) | 18 *(post-repair)* | 17 |
| Pacing & attention (20) | 18 | 16 |
| **total** | **86** | **83** |

Watermark clean on both (challenger max 0.367, 0 hits in 120 samples).

## The interesting result: the shorter video loses on Pacing

Under the old reading, 2:59 against 4:12 would have looked like the tighter cut.
Allocation says the opposite. The challenger gives **Step 2 one second** — 0.6% of
its runtime against 8.5% of the lesson's words, a **−7.9 gap**. The whole step is
*"Step 2. Understand. You cannot validate what you don't comprehend."* The lesson's
own move for that step (*"Explain the second paragraph in simpler terms" costs you
one message*) never gets said. Step 3 then runs **+10.0** over.

The incumbent's worst gap is +7.0, and that one is the Petronoski worked example,
which legitimately takes longer to say than to write. Neither video has dead time.

This is the first case where the redefinition changed a verdict rather than a score,
and it changed it against the shorter file. Worth remembering the next time a roll
comes back a minute shorter and looks like a win.

## Where the challenger is genuinely better

- **Deck-referential narration collapses to one** (*"As this final summary shows"*,
  2:47) against the incumbent's three. That is the catalogue's weakest dimension.
- **No garbles.** The incumbent still carries two, both reproduced on isolated
  re-transcription: 2:22 *"how much is **writing** on the answer"* (riding) and
  2:45 *"the page actually says **with** the AI claims"* (what).
- **It uses the rebuilt boards.** 0:24 shows the new `1-steps` capture with full
  bodies, 1:12 the new `2-decide`, 1:32 `3-dig` with a highlight sweep tracking the
  narration down the bullets. The board rebuild landed.

## Where it loses

- Step 2 starved (above), and 2 of the 6 dig moves on the Step 5 board — *challenge
  the AI*, *the almost-true trap* — are displayed but never narrated. "Walk away"
  is named but not elaborated.
- **Register drift, badly.** *"a critical failure"*, *"validate against your
  knowledge base"*, *"mandates further investigation"*, *"zero escalation"*,
  *"an active interrogator"*, *"the facade of absolute authority"*, *"professional
  mastery"*. That is not the lesson's voice, and it is the thing that keeps Teaches
  at 12 instead of higher.
- The Step 4 board at 1:12–1:28 renders small in the upper-left of an otherwise
  empty frame for 16s.

## Harvest

Nothing nominated. The one visual worth wanting — an uncropped outcomes board — was
better solved from the lesson's own jpg (see the repair below), and the challenger's
version runs 15.8s against the 27.8s span it would have to fill.

The Petronoski ID-card-then-DOES-NOT-EXIST-stamp sequence (0:40–0:56) is the only
other candidate: it is a stronger visual than the incumbent's wall of lesson text
with a green underline, and the incumbent's narration for that beat (1:42.6–1:57.0,
14.4s) fits inside the donor's 16s. Not taken — it is a style swap, not a defect
fix, and the incumbent's board is page-faithful. Left on the table deliberately.

## Repair shipped to the incumbent

**The outcomes board was clipped for 24 of its 27.8 seconds.** Frames 6396–7229 were
a slow zoom-in that started with all three cards in frame and tightened until the
"Walk away" card was cut mid-word at the right edge — *"Wrong tool, cst answers /
yourself, or tad, / actually knov"* — resolving only in the final ~3s, which is
exactly when the narration reaches *"you choose to walk away and find a
professional."* Confirmed sustained at 2fps sampling, not a dissolve artifact.

Replaced the visuals with a Ken Burns path over `lessons/evaluate-the-results-4-outcomes.jpg`,
three beats matched to the use-it / fix-it / walk-away narration, camera kept wide
enough (w 1600→1540, cx 800→772→800→828) that all three cards stay legible end to
end. Spec at `scripts/video/paths/evaluate-the-results-outcomes.json`.

Verify gate: frame count 7575 → 7575, audio MD5 bit-identical, donor landed across
the full span. Cleanliness 17 → 18, total 85 → 86.

## Correction to the 7/29 re-grade

I reported a board/narration mismatch at 0:28 — the board supposedly reading *"1932
winter athletic games"* against correct narration. **That was wrong.** The incumbent
shows a "Verified Fact" boiling-point card at 0:28; the Petronoski board arrives at
1:42 and carries the lesson text verbatim, Athens and Los Angeles both correct. The
material score is 13, not 12, and the incumbent's pre-repair total was 85.
