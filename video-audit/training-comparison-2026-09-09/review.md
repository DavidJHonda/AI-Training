# Training: two-candidate review

Reviewed September 9, 2026. **Recommendation: use training-2.mp4 as the edit source.** Its narration covers the essential teaching and preserves the exact closing. Both candidates are usable raw generations, but version 2 needs fewer substantive repairs. A reroll is not needed to obtain the core teaching.

No videos were edited, replaced, shipped, or deleted during this review.

## Evidence and review scope

- Version 1: `Prompts/training-1.mp4`, 4:32.77, 8,183 frames at 30 fps, approximately 729 spoken words.
- Version 2: `Prompts/training-2.mp4`, 4:50.10, 8,703 frames at 30 fps, approximately 783 spoken words.
- Teaching authority: current `lessons/training.md`, `Prompts/training-video-prompt.txt`, and the Training section of `index.html`.
- Read complete local small.en transcripts for both candidates and cross-checked with independent base.en transcriptions. Both passes agree on the material editorial findings. ASR wording is not a substitute for listening to candidate cut boundaries.
- Inspected all six contact sheets, sampled every five seconds across both videos. These establish visual presentation and approximate board coverage, not every-frame transition integrity.
- This is a narration-first intake review, not a final shipping grade, a complete audio-performance review, or approval of any proposed splice. Proposed times refer to the raw source files and need listening and frame-level adjustment during editing.

## Teaching coverage

| Teaching point | Version 1 | Version 2 |
| --- | --- | --- |
| Basketball analogy and numerical adjustments | 0:07–0:28: clear connection to guess/check/adjust. | 0:09–0:38: equally clear core explanation, with an unnecessary hard-drive aside. |
| Peanut butter/cloud/jelly loop | 0:28–0:57: all three steps and the increased likelihood of jelly are spoken. | 1:00–1:25: all three steps and the increased likelihood of jelly are spoken. |
| Engineers establish starting values and gather data | 0:58–1:22: both covered. Adds an overly restrictive claim about learning only facts and patterns contained in the collection at 1:23–1:32. | 0:39–0:57: both covered without that added claim. It moves this board ahead of the concrete training-loop example. |
| Same basketball prompt across three phases | Explicitly established at 1:33–1:43 and carried through. | Explicitly established at 1:26–1:38 and carried through. |
| Pretraining: next-word prediction, weights, fluent text, weak instruction following | 1:43–2:20: main teaching is present. Additional language about storing facts is less helpful than the lesson’s pattern explanation. | 1:38–2:19: main teaching is present, including the source’s scale comparison and why fluent prose is not yet reliable instruction following. |
| Instruction tuning: example question/answer pairs and weight updates | 2:21–3:11: teaches the mechanism and limitations. The basketball example stops at “push up.” | 2:20–3:00: teaches the mechanism and limitations. Reads the full instruction-tuning basketball answer, including release and follow-through. |
| Preference tuning: several responses, human comparison, changed weights | 3:12–3:49: covered, but says weights are adjusted “one last time.” | 3:16–4:11: covered, but similarly says “one final time” and appends an unsupported causal explanation of hallucinations. |
| Improvement still does not guarantee correctness | Explicit at 3:39–3:49. | Explicit at 3:56–4:08. Keep this; remove the following “because” clause. |
| Normal chat can use new information without changing weights | 4:10–4:17 says conversations do not change weights, but omits the balancing point that new information can still be used. | 4:21–4:40 explicitly teaches both, using a pasted document as the concrete example. |
| Exact approved closing | Says “Guess, check, adjust, repeat,” but substitutes a longer summary for the first line. | 4:41–4:47 delivers both approved lines. |

The truncated preference-tuning answer in both videos is sufficient to illustrate the difference: it introduces starting close to the hoop and using the other hand to steady the ball. Reading the entire board aloud is unnecessary. Version 1’s recognition output says “study the ball”; verify by ear before treating that as a spoken error. This ambiguity is not a basis for the recommendation.

## Why version 2 is stronger

The student hears a complete progression: starting values and data, repeated numerical adjustments, three different training jobs, and what changes when the finished model is used. The same basketball question makes the differences concrete. The final document example prevents the student from concluding that fixed weights mean AI cannot work with information supplied in a chat.

Version 1 has more changes of scene, but it also adds claims and recap passages that would need attention. The sentence at 1:23–1:32 that the model can only learn the facts and patterns “contained within” its collection is too restrictive and obscures generalization. Its ending is more absolute and less complete than version 2’s. Its extra visual variety therefore does not make it the better narration source.

Version 2 reorders the first two boards: setup comes before the peanut-butter demonstration. That differs from the requested source order, but the spoken transitions form a coherent sequence. I would retain that order instead of making an edit solely to restore the Markdown’s ordering.

## Recommended version 2 repairs

| Source time | Recommendation | Reason |
| --- | --- | --- |
| About 0:28.04–0:30.62 | Remove “or simply saving exact files to a hard drive.” | An unnecessary contrast in an otherwise clear analogy. Keep the physical-force/numerical-adjustment connection. |
| About 0:31.72–0:32.10 | Optionally remove “strictly,” if the audio join is natural. | “Training involves tweaking…” is sufficient. Do not damage a sentence for this minor cleanup. |
| About 1:13.20–1:14.06 | Optionally remove “Because it’s wrong,” keeping “the system enters the adjust phase.” | Avoid suggesting updates occur only when the top prediction is wrong. The example itself is acceptable; no new technical explanation is needed. |
| About 3:01.16–3:15.16 | Remove the reflection question beginning “Think back to the basic training loop…” | About 14 seconds that delay the next phase. The preceding limitation already motivates preference tuning, and the next sentence introduces it. Add the standard one-second transition pause where appropriate. |
| About 3:32.80–3:33.96 | Remove “one final time.” | Preference tuning is a training process with repeated updates, not one final numerical adjustment. Preserve the surrounding sentence about human selections changing weights. |
| About 4:07.96–4:10.54 | Remove “because it was trained to sound like a helpful human.” | The lesson correctly says wrong answers remain possible; it does not teach this single-cause explanation. End the sentence after “sounds correct.” |
| After approximately 4:46.56 | Replace the Notebook ending with the standard course closing treatment. | Retain both approved spoken lines and add the one-second pause before the closing message. |

These repairs should leave a video around four and a half minutes, depending on pauses and final holds. Runtime is not the objective. Preserve clear, complete sentences and the teaching sequence.

Instruction tuning is described a little narrowly as matching templates and format, and preference tuning as matching style and structure. The surrounding narration also discusses following requests, clarity, accuracy, and usefulness, so the main distinction survives. Retain the current board wording during these passages; another explanatory detour or a reroll is not warranted just for those phrases.

## Visual editing approach

Use the existing Notebook basketball opening and other useful transitions. Do not replace the whole video with static course boards. Both videos contain generative diagrams that introduce unnecessary technical labels; these are visual repair opportunities, not reasons to discard sound narration.

For version 2:

- Preserve the useful basketball/shot visuals around 0:09–0:18. The later generic numerical-network material can be simplified if it distracts from the spoken analogy.
- Restore the exact setup and training-loop boards for their walkthroughs. Current generated camera moves crop content, and the loop example receives yellow highlight shading.
- Use the exact three training-phase boards during their explanations. Version 2 keeps these onscreen for extended stretches: roughly 1:40–2:19, 2:20–3:01, and 3:20–4:11. Guide attention with the course’s outline highlights as the narration moves through the explanation, example, and remaining limitation. Do not add title shading or marker fills.
- The generated overview around 1:30 labels later stages “Fine-Tuning” and “Alignment,” while the lesson teaches “Instruction Tuning” and “Preference Tuning.” Replace those labels/that graphic during editing to maintain terminology.
- If the 3:01–3:15 question is cut, its accompanying question-mark classroom visual is unnecessary.
- Preserve the useful final contrast between a normal chat and unchanged weights around 4:21–4:40, subject to checking the generated labels at full resolution.
- Add one-second pauses at major idea changes where the narration needs room, including before the closing message. Measure the resulting pauses during editing rather than assuming a visual hold is silent.

## Technical grounding

The distinction between supervised demonstrations and human preference rankings is supported by the primary [InstructGPT paper](https://arxiv.org/abs/2203.02155). That paper also reports remaining mistakes after feedback-based training; it does not establish the video’s added explanation that sounding helpful causes those mistakes. The stages here are an introductory teaching structure, not a claim that every modern model follows an identical recipe.

The next-token prediction objective is documented in [Hugging Face’s causal language-modeling guide](https://huggingface.co/docs/transformers/tasks/language_modeling). The lesson’s “guess, check, adjust” wording is an instructional simplification of the training objective; it does not require a new detour into loss functions, gradients, or reward models.

## Decision

**Keep version 2 and repair it.** Version 1 is not needed as an audio donor for the essential lesson. Leave both originals and the current live Training video untouched until the next requested action.
