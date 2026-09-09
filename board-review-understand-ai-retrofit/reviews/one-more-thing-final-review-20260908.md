# One More Thing: final review after the temperature move

## Judgment and scope

The current lesson has a cohesive arc: probabilistic token selection, temperature, then computational scale. The shared dog-name prefix and identical starting percentages make the first two boards work as a sequence. Keep all three boards and the short two-bullet explanation. Keep the humorous TRY IT as the owner intends, including the horse joke; do not reopen its factual verification.

Reviewed current index.html InferenceSection, Markdown, three rendered board images, temperature renderer mathematics, closing text, TRY IT data/control flow, video metadata, and video-generation prompt. No lesson edits in this review. About 314 prose words excluding image descriptions. Source checks and image inspection completed; no new browser interaction or full video playback review.

## Suggestions in priority order

1. **Clarify Other as a combined category in both probability boards.** The text calls Spot the top individual choice at 22%, but Other is shown at 32%. The first board has a striped bar; the temperature board has no equivalent distinction. Recommend `Other` with a smaller `(combined)` directly underneath, consistently in both boards. This makes the existing math clear without adding body copy or changing the distribution.
2. **Finish the proposed deletion.** `Other choices would account for the remaining 78.` remains in both lesson files. The owner questioned its necessity and the assistant recommended deletion, but no deletion was executed. The 22-out-of-100 explanation and board are sufficient. Hold for the iterative review rather than silently altering the prose.
3. **Accessible temperature comparison.** Current image alt and hidden summary state the direction of the change but omit the low/high values. Include a semantic data table or equivalent accessible rows with all three columns so the numerical comparison is available without sight. This can be implementation cleanup without lengthening the visible lesson.
4. **Video alignment remains unfinished.** The existing One More Thing MP4 has not been rebuilt for this revised lesson. The metadata still reads `Three more things: the lottery, the transcript, and the bill.` The new generation prompt correctly removes memory/caching and the drawing analogy and uses the new boards. When the video is updated, replace the obsolete metadata and verify its narration/boards against this final text. Your Choices was separately cut and shipped; do not redo it.

## Factual and numerical checks

- Expected frequency is properly qualified by `on average` and unchanged odds. Five example tries do not promise an exact 22% outcome in a small sample. No requirement to reintroduce the word sampling, tickets, or a formal statistics lesson.
- Temperature is correctly presented as a generation setting used by the app, with no promise that students can change it. It changes selection probabilities, not learned weights. Additional decoding controls are beyond this lesson's scope. Primary references: [Transformers generation strategies](https://huggingface.co/docs/transformers/generation_strategies#sampling) and [Generation configuration](https://huggingface.co/docs/transformers/main_classes/text_generation).
- Starting values: 22, 17, 14, 9, 6, 32. Low: 36, 21, 15, 6, 3, 19. High: 16, 14, 13, 10, 8, 39. Each displayed column sums to 100. Every whole-number entry differs from the underlying calculated value by less than one percentage point.
- Renderer uses p^(1/T), normalized, with T=0.5 and T=2. The Other group is an explicit illustrative assumption of four individual choices at 8% each, transformed individually then combined. Its low/high totals are not uniquely determined by the group’s initial 32% alone. This is a valid constructed example, not a measurement of a proprietary model. Keep this implementation note out of the learner’s flow.
- Hypothetical trillion active weights × roughly two operations × 1, 100, or 1,000 generated tokens gives 2 trillion, 200 trillion, and 2 quadrillion. This is a rough weight-computation illustration, not a full bill for a real chatbot. [Scaling Laws for Neural Language Models, section 2.1](https://arxiv.org/html/2001.08361v1#S2.SS1) gives the dominant 2N forward-pass term with additional context-dependent attention costs. The present hypothetical framing is appropriate; no need to introduce more architecture details.
- TRY IT number comparisons and their assumed physical dimensions were checked in the earlier review and have not changed. Writing 1,000 tokens now matches the math board's language. The activity need not become a technical quiz.

## Presentation and integration

Standard board titles, matching prompt strips, banners, and core colors are consistent. Temperature is substantially easier to scan without bars and decimals. Math has room around its totals but no clipping; this does not justify another redesign. Retain the first board’s five outcomes to make probabilistic choice concrete.

All three live/Markdown image pairs match byte for byte. JavaScript syntax passed with Node. git diff --check passed. TRY IT data still contains five items with valid answer choices and right/wrong feedback; the final joke intentionally selects the humorous option. No recommendation to change that behavior.
