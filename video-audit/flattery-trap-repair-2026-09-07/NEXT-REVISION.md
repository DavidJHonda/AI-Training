# Flattery Trap targeted re-roll and pending repairs

Status: donor evaluated and approved, and the combined review candidate built on 2026-09-07. Review `Prompts/flattery-trap-five-moves-patched.mp4` (6:21.5). See `video-audit/flattery-five-moves-hybrid-2026-09-07/REVIEW.md`. Neither candidate is shipped yet. The remainder of this file preserves the original revision brief.

## Upload kit

Upload only:
- lessons/flattery-trap-five-moves.md
- lessons/flattery-trap-4-five-moves.jpg

Paste Prompts/flattery-trap-five-moves-video-prompt.txt into the video customization prompt. Do not upload the full lesson, other boards, the existing video, or Master Prompt.md for this targeted generation. The JPG is byte-identical to the current on-page illustrations/flattery-trap-five-moves-v2.jpg and contains no faces. No duplicate JPG is needed.

Suggested returned filename: Prompts/flattery-trap-five-moves-reroll.mp4.

The supporting Markdown uses the board's compact prompt wording for narration. For move five, “Be honest with me” is an explicitly spoken weak comparison drawn from the lesson; the board itself only shows the saved instruction. No source lesson or board is changed.

## Acceptance before splicing

Each of the five moves must narrate the weak prompt, why it is weak, the complete better prompt, and why it helps. Naming the move and leaving the example on screen is insufficient. Keep the counterargument caveat and explain that saved instructions guide rather than guarantee responses. Preserve natural sentence endings. Prefer complete teaching over runtime. Assess the new segment before choosing exact splice frames.

Existing footage before the practical section is retained. Replace the old practical teaching block, including any duplicate caveat, with the approved new segment. Preserve or reinsert the current exact standard closing; do not play the takeaway or caveat twice. Candidate remains in Prompts until owner ships it.

## Approved repairs to perform in the same final edit

Times below refer approximately to the 4:06.5 patched review candidate, not the raw roll.

1. 0:20–0:22: replace FALSE PRAISE with FLATTERY TRAP when narration names the term. Preserve the existing graphic style and narration.
2. First Gatsby comparison: separately highlight the title, response, and explanatory sections as spoken. Card-section highlights use the same full outer column-width rails; vertical bounds follow the actual spoken content and balanced padding. Do not ring the whole header/image group while narration refers to a specific text component.
3. Training flow near 1:30: establish the full three-part board, then zoom to each complete component and pan in spoken order. Owner's new direction supersedes the previous compact-three-part full-board treatment here. Two-box comparisons can stay together when readable. Keep each complete active component inside the frame, without clipped text, rings, or arrows interfering with text.
4. Before “OpenAI” in the rollback transition (owner reference about 2:44; current cut is 2:45.767): add one measured second to the final timeline. Hold the current quote-board view throughout the pause; begin the next visual with the new thought. Use natural matching room tone, no duplicated breath.
5. Sycophancy response: highlight the exact narrated quotation phrases rather than whole paragraphs. Use actual rendered text coordinates and follow the spoken phrase; do not imply the whole paragraph is being read.
6. Five moves: use the new complete narration to walk weak prompt, better prompt, and explanation in order. Highlight complete prompt bubbles when active; keep full rows for row-level introductions. Do not attempt to supply missing teaching by silently displaying the board.

## Final QA gate

Record final-output splice frames after all cuts, inserted pause and new segment. Run transition_guard.py and inspect every-frame boundary strips, plus every settled highlight state. Check complete words and sentence transitions, breaths and signal continuity. Verify a full one-second inserted pause in encoded audio, with the quote visual held throughout. Exact course closing must be the literal final frame.

Do not modify index.html, live videos, or the current lesson in this preparation pass.
