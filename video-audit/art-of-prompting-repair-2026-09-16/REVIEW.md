# Art of Prompting — repaired candidate review

## Recommendation

**KEEP the repaired candidate for human review. Do not publish yet.**

The candidate now teaches the lesson's essential distinctions and four-move prompting framework accurately and completely. It uses the strongest narration from the two Art of Prompting rolls plus one concise donor line from Questions Matter, while retaining the stronger worked examples and conclusion from roll 1.

The live course video was not changed. This is a review candidate only.

## Deliverables

- Candidate: `Prompts/art-of-prompting-v3.mp4`
- Build script: `scripts/video/build_art_of_prompting_review.py`
- Manifest: `video-audit/art-of-prompting-repair-2026-09-16/edit-manifest.json`
- Final transcript: `video-audit/art-of-prompting-repair-2026-09-16/transcript/art-of-prompting-v2.txt` (audio-identical visual revision)
- Visual-splice guard: `video-audit/art-of-prompting-repair-2026-09-16/transition-guard-visual-v2/transition-guard.md` (splice timing unchanged in v3)

Candidate metadata:

- 1280x720 H.264 video with AAC audio
- 30 fps
- 7,209 frames
- 240.30 seconds
- SHA-256: `c0b9ecb5460aee21892e7a663356346d681073ee55217d6e507a4dd3a7f347ab`

## Narration repairs

The repaired narration earns a **Keep** verdict.

1. **The four qualities of a good question are now explained, not merely named.**

   - Output `00:31.07–00:40.10`: roll 2, source `00:35.27–00:44.30`, explains Open-Minded and Specific. Gain: -0.8 dB.
   - Output `00:40.10–00:44.73`: Questions Matter roll 1, source `02:31.70–02:36.33`, explains On Target. Gain: +1.7 dB.
   - Output `00:44.73–00:49.07`: roll 2, source `00:46.67–00:51.00`, explains Open-Ended. Gain: -1.5 dB.

   The final transcript states that Open-Minded invites multiple possibilities, Specific supplies enough detail, On Target addresses the actual problem, and Open-Ended creates room for explanation rather than a yes/no answer. These distinctions match the lesson material.

2. **Literal placeholder words were removed without changing picture timing.**

   - Output `01:54.10–01:54.57`: “Paragraph” replaced with matched room tone.
   - Output `01:57.23–01:57.60`: “Question” replaced with matched room tone.

   The surrounding worked example now reads naturally: “Here is my opening paragraph. Here is the essay question…”

3. **The overclaim was removed.**

   - Source `03:10.33–03:20.00` was cut: “Moves three and four protect you…” through the claim that the framework forces the tool to reason more carefully.
   - A requested one-second pause now begins at `03:19.90` between “Let’s work on the thesis first” and “You don’t need to apply this entire framework every single time.” The transcript places the two phrases at `03:18.38–03:19.66` and `03:20.84–03:23.86`.

   This preserves the useful one-job-at-a-time advice without overstating what prompting can guarantee.

4. **One selective pause was added.** Exactly 30 frames of matched room tone were inserted after the thesis-first example. No other teaching pauses were added; the terminal silence remains the standard settled close.

## Visual and production repairs

- Replaced the Socrates photograph at the opening with roll 2's watercolor conversation drawing.
- Replaced the gibberish document sequence with roll 2's server-room and structured-briefing drawings.
- Removed the later stock-photo sequence along with the narration overclaim; a destination drawing is held for four frames to prevent a flash at the resume point.
- Replaced the raw course-board captures with the current canonical boards:
  - `art-of-prompting-good-question.jpg`
  - `art-of-prompting-four-moves.jpg`
  - `art-of-prompting-four-moves-continued.jpg`
- Preserved the useful Notebook worked-example drawings between board sections.
- Dense boards use a full-board establishing view, complete-card zooms, and 5 px emphasis rings that do not cover text.
- The `00:29` foundation ring now matches the yellow banner's measured bounds instead of extending into the footer.
- The Move 1 `INCLUDE` ring visible around `01:17` now clears the label and bullet dots with safe interior padding.
- The remaining subsection rings at `01:20`, `01:36`, `01:46`, and `02:54` now extend beyond the leftmost label or bullet column instead of overlaying it.
- The close uses the canonical message: “A prompt is a briefing, not magic words. The more the result matters, the more you bring.” It holds for 48 frames, pushes gently to 1.2x over 150 frames, and settles on the exact endpoint.
- Corner-mark cleanup completed with 3,482 cloned frames and 796 inpainted frames; no cleanup regions were declined.

## Teaching completeness

Compared with `index.html` and `lessons/art-of-prompting.md`, the candidate now includes:

- why prompting is shared-context briefing rather than magic wording;
- the four qualities of a good question, with the important distinctions stated aloud;
- Move 1: name the goal;
- Move 2: bring the material;
- Move 3: set the rules;
- Move 4: work in steps;
- worked examples for the moves;
- the qualification that the full framework is not required for every small task;
- the correct concluding principle that the amount of briefing should scale with how much the result matters.

## Verification performed

- Protected source videos and canonical board hashes remained unchanged.
- Candidate decode, duration, frame rate, frame count, and final-frame extraction passed.
- A complete timestamped transcript was generated and reviewed.
- Final audio was listened to end-to-end; the donor joins, placeholder removals, overclaim cut, and close were also auditioned separately.
- Pause analysis found natural short gaps around the inserted definitions and no new universal teaching pauses.
- All 15 actual visual splice boundaries passed the automated transition guard and were manually inspected.
- The broader 24-boundary diagnostic flagged frames 1,342 and 1,472 because the same dense board was moving across audio-only boundaries. Manual strip inspection confirmed continuous intended camera motion with no stale or intermediate frame.
- Full-timeline contact sheets at four-second intervals, every boundary strip, every board state sheet, and the close's first/hold/settled/final frames were inspected.
- Photographs, gibberish course-board text, engine corner marks, and stale course-board frames were not observed in the inspected candidate frames.

## Explicit limitation and publishing status

This environment did not provide a trustworthy way to watch the entire four-minute visual track continuously in real time. The full narration was heard, and the complete visual timeline was inspected through dense contact sheets, state sheets, boundary strips, and targeted frame sequences, but a final uninterrupted human playback remains required before shipping.

No file was copied to `course-assets/art-of-prompting/art-of-prompting.mp4`, and nothing was deployed or published.

For the final human pass, pay particular attention to the joins at `00:31.07`, `00:40.10`, `00:44.73`, `00:49.07`, `01:54.10`, `01:57.23`, and the new pause at `03:19.90`, plus the close beginning at `03:44.67`.

**SHIPPED 2026-09-16** on David's "ship art-of-prompting-v3": candidate hash re-verified (c0b9ecb5…, matches the manifest's render_sha256), copied to `course-assets/art-of-prompting/art-of-prompting.mp4` (20,411,894 bytes), decoded 7,209 frames, cache key `?v=20260916ship1`, pill stays "4 min" (4:00.30). Candidates v1–v3 removed from Prompts/; raw rolls kept. `manifest.json` video_assets entry updated in the working tree, left for the pending manifest commit.
