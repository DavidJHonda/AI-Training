# Training — repair feasibility for the current lesson flow

Review date: 2026-09-27. No candidate was built or published in this review.

**Recommendation: REPAIR, provisional until the reordered audio joins are auditioned.** The source contains complete sentence blocks for the new sequence and the essential teaching. A full reroll is not justified by the flow change alone. The repaired video can preserve meaning and sequence, but cannot speak the newly written bridge sentences verbatim using the available recording.

## Verified sources

- Current page: TrainingSection in index.html; current hand-edited lessons/training.md.
- Reviewed candidate: Prompts/training-v7.mp4, SHA-256 `f11f12ecc8a46594de330ed4725c5d83c06628691951442aa20a7ffd56126c13`.
- Published source: course-assets/training/training.mp4, SHA-256 `01a8b51a707a59d6c29288ee9d86c5500aa5546882dc45c26b307f80d1755ebe`.
- v7 has the same timeline and audio as the published source, established by both AAC packet and decoded PCM hashes in its verification record. The full timestamped source transcript therefore applies to v7.
- The original raw Training rolls are still unavailable in Prompts, archive and video-audit. v7 is a repair of the published source, not an alternate narration donor. Training Bias is a different lesson, not a suitable replacement narration source.
- Current canonical boards were inspected during the section review and subsequent lesson edit, including the revised What Pretraining Builds panel. Current Pretraining dimensions remain 1600 × 935; its wording and hash have changed since v7 was built.

## Teaching points in current lesson order

| Point | Assessment of existing narration | Evidence on the current timeline |
|---|---|---|
| Capabilities hook and practice analogy | RICH | 0:00–0:17.70: chemistry, code, essay, basketball attempts and adjustments. |
| Setup and training material | TAUGHT | 1:06.08–1:19.62: design and initial internal numbers; books, websites, conversations and code. The narration compresses the board’s longer list of modalities, as previously accepted. |
| Three-phase route, one comparison question | RICH | 1:24.52–1:50.26: three phases and “How do I shoot a basketball?” |
| Shared guess/check/adjust pattern | TAUGHT across the narration; misplaced in current cut | 0:18.60–0:22.52 gives the generic rule. Each phase later explains its examples/feedback and weight adjustments. “Across all three phases” is not explicitly spoken; the proposed move places the generic rule immediately after all three phases are introduced. |
| Peanut-butter worked example | RICH | 0:29–1:00.48: cloud versus jelly, comparison, adjustment, next example. |
| Meaning of weights | TAUGHT; move earlier | 2:04.18–2:10.08: “Every time it checks a guess against an actual example, training adjusts its internal numbers, called weights.” |
| Pretraining scale and outcomes | RICH | 1:51–2:00.22 and 2:10.82–2:36.82: large data scale, patterns, fluent basketball non-answer and instruction-following limitation. |
| Why instruction tuning follows | TAUGHT | 2:34.84–3:00.90: pattern recognition is not enough; helpful question/answer pairs guide further adjustments. |
| Instruction tuning’s example and limitation | RICH | 3:01.58–3:19.62: direct basketball instructions, followed by unclear/incomplete/unhelpful limitation. |
| Why preference tuning follows | TAUGHT | 3:12.16–3:45.48: follows the request but may be unhelpful; people compare answers and training favors the selected style. |
| Preference tuning’s example and fallibility | RICH | 3:46.64–4:16.34: improved basketball response, then wrong answers that sound right. |
| Training ends; chat uses fixed weights | TAUGHT | 4:17.00–4:39.02: ready for use, new context does not update weights during ordinary chat. |
| Closing two lines | MET | 4:39.98–4:45.54: “AI learns from examples and feedback. Guess, check, adjust, repeat.” |

The actual candidate is not KEEP against the new flow: substantial narration moves and removal of repeated mechanics are needed. The table rates content availability, not a completed repaired edit. The loop is now a shared mechanism before the phase walkthrough, not a standalone early stage or a Pretraining-only mechanism.

## Proposed assembly using existing audio

All times below refer to the existing published/v7 timeline, not future output time. Sentence ranges are descriptive; frame-level provisional cuts are in proposed-timeline.json.

1. **Keep 0:00–0:17.70:** capabilities hook and basketball analogy. Move the generic loop sentence out of this opening.
2. **Move 1:06.08–1:19.62 next:** “First, engineers set up the system…” and “Second, teams gather the data…”. Remove 1:01.32–1:05.22, “This illustration shows what has to happen before that loop can even begin.” It points backward to a loop no longer taught first.
3. **Move 1:24.52–1:50.26 next:** “To reach the level of a helpful assistant…” through the phase overview and shared basketball question. Remove 1:20.48–1:24.00, “Building the system and running this basic loop establishes the foundation.” That line assumes the loop has already been explained.
4. **Move 0:18.60–0:22.52 here:** “AI training follows a similar pattern — guess, check, and adjust.” Then keep the complete worked example at roughly 0:29–1:00.48. The immediately preceding basketball question gives “similar pattern” a usable reference. This remains an equivalent bridge, not the exact new sentence about all three phases.
5. **Move 2:04.18–2:10.08 here:** the complete existing sentence defining weights. Do not construct it by splicing individual words.
6. **Follow with 1:51–2:00.22:** “Looking closely at phase one, pre-training…” through the thousand-lifetimes comparison. Then jump to 2:10.82 and retain the outcomes, basketball answer, limitations and the remaining lesson.
7. **Delete 2:00.84–2:03.42:** “It does this by constantly guessing what comes next.” The loop has just taught that. Remove the weights sentence from its former position because it has moved earlier.
8. **Delete 0:23.38–0:28.74:** “Instead of physical force…” repeats the adjustment explanation and would have an awkward reference after reordering.

Provisional runtime: **4:31.07**, about **18.8 seconds shorter**. This includes the original close and preserves downstream narration and existing voice grafts. Final duration depends on listening-led seam placement; the proposal does not add new pauses or impose a uniform silence length.

## How to handle the new written bridges

- **Before the loop:** the source has the generic loop sentence, but not the explicit new “Across all three phases…” sentence. Moving the generic explanation after the phase overview, followed by the distinct training methods, preserves the teaching connection. A recording of the exact new bridge would make this more explicit, but no such donor exists locally.
- **After the loop:** the full existing weights-definition sentence plus “Looking closely at phase one, pre-training…” provides both ideas in the revised paragraph without inventing speech.
- **Phase 1 → 2:** keep “Basic pattern recognition is not enough,” then the current explanation of helpful question/answer pairs and further weight adjustments. It teaches the change in training material. It does not repeat the exact new bridge.
- **Phase 2 → 3:** the current limitation and feedback explanation already teach the reason for the next phase. “It requires a final layer of refinement based on human taste” is less plain than the new prose. Removing that optional sentence is a possible refinement, but not required by the proposed timeline and not assumed approved here.

**If exact new bridge wording is required, existing-audio-only repair cannot meet that requirement.** New short narration would be needed and would require voice/cadence matching. This review neither assumes a compatible donor nor recommends regenerating the entire strong narration solely to obtain those transitions.

## Board, camera and pacing plan

| Board | Treatment after reordering | Pacing |
|---|---|---|
| Before Training Starts | First board; full view, then Setup and Data outlines at spoken onsets. The first item starts soon after arrival, so its ring follows speech without an artificial two-second pause. | About 14.4s of setup audio. |
| Three Phases of Training | Full view; question, then each phase card. Use the basketball drawing during the introductory overview sentence rather than replaying a Notebook loop diagram before teaching the loop. | About 20.2s on the board after the intro drawing. |
| The Training Loop | Full view; Guess, Check, Adjust. Reuse the approved 0:49–0:56 weights break on its relocated timeline. Retain the unmarked repeat beat. | About 19.9s before the drawing and 5.0s after. |
| 1 · Pretraining | Use the current revised JPG, not v7’s older text. Full opening; outline What Pretraining Builds, example, limitation. Reassess density against actual output; no automatic reuse of old highlight timing after narration is moved. | Removing the repeated mechanism reduces the initial board run to about 19.3s if the existing 2:20–2:28 basketball break is retained. |
| 2 · Instruction Tuning | Preserve approved full opening and complete-section framing; current exact asset, 4px outlines. | Retain the 3:03–3:12 basketball break and approved 25.5s maximum individual run. |
| 3 · Preference Tuning | Preserve approved framing, complete active sections and 4px outlines. Keep the existing graft under the same narration. | Retain the 3:52–4:05 basketball break and approved 27.8s maximum individual run. |
| Close | Retain current literal final message and motion. | Original 9.8s. |

Use the basketball drawing for the relocated generic loop sentence and the weights drawing for the relocated definition, so the new order does not simply create another long adjacent-board chain. With those meaningful drawing spans, the longest proposed chain is about **40s** (Instruction Tuning’s final 12.2s followed by Preference Tuning’s first 27.8s). That is a planned duration, not an encoded measurement. Camera moves count continuously.

The opening’s paper-craft style remains flagged as before. Resolving it is separate from the narration-order repair; it does not justify a reroll. The weights donor retains its illustrative numbers/“Optimal Output” label, previously disclosed. Original raw sources are unavailable; build from the retained published source and canonical boards in one assembly, using the v7 repair recipe, to avoid stacking another video encode on v7.

## Checks performed and limitations

- Read current page/source text and the complete timestamped transcript; verified actual candidate and published-file hashes.
- Reused the v7 exact-audio identity verification and its decoded frame/transition evidence because those files are unchanged. No new full-playback claim.
- Measured decoded source audio in 10ms windows at a −35dBFS quiet threshold. Quiet gaps exist around the proposed sentence-block boundaries, including the ASR boundaries at ~0:29 and ~1:51 that misleadingly show adjacent sentences touching. See source-gap-measurements.json.
- Quiet amplitude alone does not establish a natural join or exclude soft breath/consonant tails. **No new joins were auditioned; no real-time end-to-end listening, cadence/voice continuity or mobile playback was performed.** Proposed cuts must be listened to in context before certification.
- The replacement Pretraining board will need new encoded-frame inspection and ring verification after a build. The reordered timeline needs a fresh transition guard and continuous-board-duration check.
- No new narration was generated, no audio assembly was rendered, no video was built, and nothing was published during this review.
