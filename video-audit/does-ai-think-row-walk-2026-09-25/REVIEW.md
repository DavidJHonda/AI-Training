# Does AI Think? v8 candidate, 2026-09-25 (narrow repair: camera walk on the comparison board)

**Scope.** David, 2026-09-25: "The board that appears at 2:02. We need to zoom and pan between the lines as spoken."
The When You Think / What AI Does board was compact (still full view for 72.6 s). v8 makes it dense (Edit Spec rule 4).
Only the camera changes. Narration, timing, rings (rects, colors, onsets), artwork and audio are identical to live v7.

**Span.** Output frames 3669–5847 (2:02.30–3:14.90), same as v7. Build: `scripts/video/build_does_ai_think_row_walk.py`,
from the same frozen baseline as v7 (one re-encode). Candidate `Prompts/does-ai-think-v8.mp4` (fe8d537e47bc…) SHIPPED 2026-09-25 on David's approval ("ship it") to `course-assets/does-ai-think/does-ai-think.mp4`; candidate removed. Cache key `20260921ship11` -> `20260925ship12`.

**Camera walk** (house constants: 24-frame transit starting at the spoken onset, 30-frame pull-back, one uniform dive window,
w 1592 canvas px = 1.74x the full view, the board's full width, so each row is seen complete across both columns):
- 2:02.3 full view, unmarked, through the intro (7.6 s)
- 2:09.9 Meaning: ring + dive; 2:20.0 Experience; 2:30.3 Word choice; 2:39.5 Beauty; 2:51.2 Uncertainty: ring + pan down
- 3:04.6 banner: ring + pull back to full view, held to the exit at 3:14.9
Ring stroke follows the artwork-scaled rule: 5 px at the dive, 3 px at full view.

**Verification.**
1. 6600 frames decoded at 30 fps; the leg decodes 2178 frames. Audio packets identical to the baseline.
2. Frame diff vs live v7 every 10th frame: outside the span 0.00 (bit-identical picture); inside it changes by design.
3. `transition_guard.py`: the splices (3669, 5847) and the Meaning and Uncertainty onsets pass. It flags the Experience, Word choice,
   Beauty and banner onsets at onset+5..+12. Those are the middle of the 24-frame pan (moving text reads as cuts, the known
   false positive). Strips inspected: continuous glide, ring riding its row, no stale frames.
4. Settled frames inspected at full res (`state-*.jpg`): right row ringed, complete row inside the frame, text sharp, banner
   ring edge to edge at full view.
5. Not done: listening (audio unchanged), full end-to-end rewatch.
