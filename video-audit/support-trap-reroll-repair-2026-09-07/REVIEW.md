# Support Trap reroll repair

Status: review candidate, not shipped. Approved repair built on 2026-09-07.

Output: `Prompts/support-trap-reroll-patched.mp4`, 3:30.100, 6,303 frames at 30 fps.
Source: `Prompts/support-trap-reroll.mp4`. Recipe: `scripts/video/build_support_trap_reroll_review.py`.

## Approved changes

- Current illustrated comparison replaces the face-free Notebook surrogate at source 0:13.500–1:02.800. Establish full board, focus complete sister/chatbot cards, then highlight the chatbot's spoken subtopics on measured full-width card rails. Standard purple full-width takeaway.
- Current two-card role board replaces source 1:02.800–1:21.067 and 1:41.967–2:00.633. Keep complete compact board visible. Retain the intervening grades and ordinary-venting examples and native graphics.
- The optional single-word cut of “safely” was not made: it is embedded in connected speech. Preserve the specific ordinary-venting example rather than risk a choppy syllable-level edit. This is not a general claim about crisis safety.
- Retain the spoken content note and its existing pause.
- Replace the invented article/portrait and simulated quoted chat with the reroll's face-free Harry phone artwork, using a continuous restrained push from source 2:09.033–2:24.800. No invented verbatim chat is shown. Preserve empty-room and black-box shots.
- Remove source 2:33.500–2:39.650, the entire “completely invisible” sentence. This joins at output 2:33.500. The mother's black-box account leads into the retained crisis/action sentence.
- Replace the woman lying by the phone with a restrained view of the existing empty-room artwork for that retained sentence.
- Remove source 2:43.650–2:48.200, “Reassurance means nothing...” and its complete visual span. Output 2:37.500 begins the approved danger board before the raw old-graphic transition.
- Current three-card danger board: full establish, complete-card zoom/pan in spoken order, inherited red rings, then standard purple full-banner ring. Preserve distinct 988/911 instructions and all three actions.
- Output 3:21.500–3:22.500 is a full one-second silent teaching pause on the prior board.
- Replace the Notebook close and outro with the exact current course close. Fixed 48-frame prehold, 150-frame push to 1.2x, and 30-frame settled finish. Both closing lines preserved. Final audio hold is 1.633 seconds; final picture is settled for one second.

## Lesson/source correction

Changed exactly the approved sentence in the Support Trap portion of `index.html` and in `lessons/support-trap.md`:

“The chats held details that made it harder for the people around her to understand the severity of her distress.”

This replaces the misleading implication that nobody around Sophie knew of the danger. [Laura Reiley's account](https://archive.ph/oiDQU) says Sophie disclosed suicidal thoughts to her parents, while shielding the severity of her distress. Prompt already instructs against claiming nobody knew, so no prompt change was needed. No lesson boards or PDF changed.

## Verification

- Sequential full-video decode: 6,303 frames; audio decode has no errors.
- Native macOS AVFoundation: playable YES and first-frame decode YES.
- Re-transcribed the full repaired narration. Both removed sentences are absent; the preceding and following sentences, 988/911 distinction, three actions, and closing lines remain intact. Transcript is an edit-integrity check, not a substitute for the owner's listening review.
- Inspected all 25 every-frame transition strips, covering 12 frames on either side. Five automatic alerts are continuous intended camera movements, not leaked intermediate graphics. No discarded shots identified in the inspected seams.
- Inspected settled frames for every state, including full-resolution comparison section rings. Full-width rails follow the card boundaries, no overlapping neighboring text. Every settled ring has at least 24px frame clearance.
- Measured zero amplitude inside both added silent holds. Last 30 video frames are settled, with only negligible codec differences (mean maximum 0.0078).
- Raw reroll, live Support Trap video, all current lesson boards, and closing asset hashes are unchanged by this build.
- No live replacement, video deletion, or commit. Unrelated existing workspace edits preserved.

Evidence: `manifest.json`, `integrity.json`, `qa/`, `transitions/transition-guard.json` and every-frame boundary strips.
