# Evaluate the Results v6: best-of build (2026-09-27)

Candidate: `Prompts/evaluate-the-results-v6.mp4` (3:53.60). Review copy only; the live video, the lesson and the boards are unchanged, and all protected hashes were verified after the render.
Build: `scripts/video/build_evaluate_the_results_v6.py`. Plan approved by David 2026-09-27: `../evaluate-the-results-reroll-review-2026-09-27/edit-plan.csv`.

What was verified on the encoded file:
- **Transcript** (`verify/evaluate-the-results-v6/transcript.txt`) matches the plan word for word:
  - all five check names, and "Explain the second paragraph in simpler terms."
  - "You decide whether the answer holds up." and "Then check the revised answer before you use it."
  - the roll 1 graft naming the official program page and the school calendar
  - "The answer is not the evidence.", then "The tool answers. You evaluate. / Read, understand, validate."
  - nothing after the close
  - none of the cut lines remain
- **transition_guard:** 35/35 boundaries pass (`transition-guard/`). The first render failed at the Dig pull-back (the camera was still moving as the board returned from the code cutaway); moving the pull-back to 168.5 s fixed it.
- **Contact sheets** (`verify/.../sheets/`): every cutaway is the intended drawing, rings land on the spoken cards, and the standard close is the final frame.
- **Corner mark:** 1586 frames cloned, 925 inpainted, 0 declined; roll 1 graft 181 cloned.
- **Board runs:** longest 20.1 s (Dig banner → 1 s pause → Make Your Move through "You can fix it."; it crosses a board change), every single-board span under 19 s, down from roll 3's 168 s and the live video's 203.5 s.

Not verified (needs David's ear):
- The "riding"/"writing" word at 1:45.5 (whisper still hears "writing").
- The joins: roll 3's "March 1," into roll 1's "Both the official program page…" at 3:28.8 (roll 1 at +2.3 dB), and roll 2's "The tool answers, you evaluate." at 3:43.8 (+1.5 dB).
- The second use of roll 3's "Read. Understand. Validate." at 3:47.1.

Note: frame 0 is roll 3's own blank paper before its first graphic draws in (unchanged from the roll).
