# AI Is Different v10: review candidate, 2026-09-27

**Candidate:** `Prompts/ai-is-different-v10.mp4` (4:45.9, 8577 frames at 30 fps, decoded). This is not shipped, and the live video is unchanged.
**Build:** `scripts/video/build_ai_is_different_v10.py`. The manifest is `edit-manifest.json`.
**Plan:** `video-audit/ai-is-different-reroll-review-2026-09-26/REVIEW.md`, approved 2026-09-27 ("build it").

## What changed from the plan
- N6 (excise "completely") was dropped. The word sits in connected speech with no silence at either edge.
- Roll 3's chef drawing is used, but its recipe-wall drawing is left out because it's near-photographic.
- N4 (roll 2's "PDF or a photo... summary, table, or image") plays over the Structured board with a ring on the AI card's Input & Output line, instead of under a drawing. The narration matches the card text.
- Roll 3 AI-network break: the frames are verified by sequential decode (r3 frames 270–385).

## Verification
- Transcript (`transcript/`): every line of lesson narration is present in order, including all four grafts. Both closing lines are verbatim.
- `transition_guard.py`: 36/36 boundaries PASS (`guard/`).
- Corner mark: 3123 frames cloned, 629 inpainted, 0 declined; the graft legs have 0 declined.
- Pauses (transcript gaps): after "Patterns build a fresh one." 1.18 s (target 1.21); before Kryptonite 1.24 s (target 1.31).
- Graft join gaps: N1 0.54 / 0.78 s, N2 0.38 / 0.88 s, N3 0.78 / 0.64 s, N4 0.62 / 0.72 s, N5 1.02 s.
- Contact sheets (`sheet/`) inspected. There are no photos or logos; the floppy-disk photo is gone. Rings match the approved boards.
- Board runs: longest is Kryptonite at 20.7 s. The others run 11.3–18.3 s.

## Not done
- **No listening pass.** David needs to listen to all four grafts (roll 3 at 1:20 and 1:54, roll 2 at 2:35 and 3:09) and to the N5 cut at 3:32.
- Notebook's own blue underline strokes sit on its receipt/text drawing (2:28–2:32). They are in the source roll and were left as-is.
- The pill still says "6 min". Update the duration on ship.
