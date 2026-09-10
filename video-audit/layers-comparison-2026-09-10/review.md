# Layers: two-roll comparison, 2026-09-10

Recommend **layers-1** as the repair base. No fresh roll is presently needed. Version 1 is 2:45.17; version 2 is 2:50.60. Both cover the lesson's broad arc. The duration is appropriate for a focused lesson and is not a deduction. Neither raw file is ready to ship.

## Evidence and scope

Read the current `lessons/layers.md` and live `LayersSection` in `index.html`; read both complete base.en transcripts, then both complete small.en verification transcripts; inspected all eight contact sheets, scene lists, holds, and manual section allocations. Checked adjacent full-resolution frames for version 1's architecture and vector-comparison diagrams. This is a narration-first raw-source evaluation, not a finished edit or full listening certification. Exact audio splice boundaries remain build work. Original source hashes are in `sources.json`; no source, live video, or lesson was changed.

Current board authority: `lessons/layers-horse-three-reads-editorial.jpg`, `lessons/layers-inside-layer-editorial.jpg`, `illustrations/layers-resolves-it.jpg`. The Markdown's `lessons/layers-3-resolves-it.jpg` is its upload reference; the live illustration is the editing authority. `WhyDozensBox` is a dormant function, not an active lesson board. Do not insert it.

## Version 1 narration

The stronger base. 0:16–0:43 teaches the horse's confusing grammar and reinterpretation. 0:43–1:18 explicitly names the neural network, attention and transformation inside each layer, changing numbers, and the handoff to the next layer. 1:25–1:45 reads the complete approved CAT sentence and follows the connection. 2:00–2:34 covers dozens/sometimes over a hundred layers, nuance, and the computing/time tradeoff. Both closing lines are present at 2:34–2:42 with harmless lead-in words.

Repair 1:31.52–1:35.74: “The AI starts with zero context. Raw numbers provide no clue.” This is too broad. The prompt provides context; IT's starting representation has not yet incorporated the sentence-specific information needed to resolve its reference. Version 2 supplies a more accurate donor: approximately 1:17–1:23, “Focus on the ambiguous word, it. Its starting numbers don't reveal the pronoun's reference.” Verify the exact word boundaries, voice continuity, and joins in the build.

Optional cut: 0:07.30–0:16.16 previews AI/layers before the horse example and repeats the later transition. Cutting it restores the lesson's human-example-first arc. Do not cut useful explanations solely to shorten the video.

The horse explanation ends “and then it fell.” The board explicitly identifies the horse; it is less precise than repeating “the horse,” but does not reverse the meaning as version 2 does. No need for a new roll on that basis.

## Version 2 narration

Covers the major topics but introduces substantive errors:

- About 0:23–0:27: “Someone raced a horse past a barn and then fell.” Both transcription models detect the missing subject before “fell.” Grammatically this makes the person fall. The visual has the right explanation, but does not repair the spoken ambiguity.
- About 1:52–1:59: “Because those numerical values now match...” teaches that the pronoun is resolved by matching IT's numbers to CAT's. The model can represent their relationship without those representations becoming identical. The lesson does not teach equality.
- About 2:30–2:36: “exponentially more computing power and processing time.” Adding otherwise equivalent layers does not inherently produce exponential growth; per-layer work accumulates. The accompanying exponential-cost graph repeats the error.
- 1:33–1:42 adds a pause-and-predict exercise that does not have a useful inferable numerical answer and leads into the false matching explanation. It is removable, not a runtime failure.

The shortened CAT sentence at 1:14–1:17 also loses the exact wording used across the course, although it still teaches the underlying pronoun connection. The strong donor is the precise START explanation around 1:17–1:23. The opening book visuals (0:00–0:09.10) are also usable if preferred.

## Preserve source graphics; targeted repair plan

Keep version 1's useful opening reader, rereading illustrations, and scale/cost visuals. Do not default to boards across whole sections. Course boards are useful for the horse interpretations, the within-layer operations/number table, and the five-stage IT example. Use their current captures only over those teaching spans, with standard outline emphasis and no Notebook highlights.

Concrete replacement reasons:

- 0:43.30–0:50.07: generated stack labels token embeddings, self-attention, feed-forward, and deep representation as separate numbered stages L1–L4. This conflicts with the immediately following explanation of attention and transformation within each repeated block. Reuse the sound repeated-block Notebook diagram from the earlier preview if its labels pass settled-frame review, or bring in the existing operations board only for this explanation.
- 1:09.43–1:18.47: generated human/machine comparison assigns CAT the same two numbers as IT's final row, implying the matching mechanism. Adjacent 72s and 76s frames verify this; it is not a sampling artifact. Replace only that illustration span or retain the relevant current number-update board through this directly related explanation.
- 1:18.47–1:25.50: the cat/ice-cube/ruler picture does not clearly explain following IT through the layers. Use a better existing Notebook shot or a Notebook-style replacement if necessary; do not invent a course board for this video-only bridge.
- Native highlights on actual boards are normal raw material to replace, not a reason to reject either roll. Sampled cropped board views often resolve by panning; no blanket gibberish or clipping deduction is made from transition samples.
- Insert the standard course close over the spoken closing message and remove the generated end card. Add one-second pauses at genuine idea changes in editing.

No changes have been built or shipped from this comparison.

## Independent dimension scores (raw material; no total)

| Dimension | Version 1 | Version 2 |
|---|---|---|
| Teaching coverage /20 | 19: all major beats; 1:36–1:45 compresses the layer-1/layer-2/repeat distinctions | 19: all major beats; 0:40 names the neural network without the first version's explicit stack definition |
| Lesson material /15 | 15: both worked examples, number-update demonstration, scale/tradeoff, close retained; replacing the core examples would cost credit | 13: horse paraphrase changes the subject, CAT sentence shortened, 2:30 cost explanation departs from source |
| Teaches vs recites /15 | 13: explains operations and handoff clearly; 1:31–1:35 overstates what the starting numbers lack | 10: apparent explanatory depth at 1:52 and 2:30 supplies false mechanisms |
| Board teaching /10 | 9: all three boards taught; five-stage progression compressed at 1:36–1:45 | 8: all three addressed; final stage 1:52 incorrectly explained as number matching |
| Cleanliness /20 | 20: settled content is generally readable; pan samples not treated as stable clipping. A persistent illegible teaching label would cost credit. Accuracy/board-format defects logged separately | 20: readable content and graph; wrong graph is an accuracy issue. A persistent illegible teaching label would cost credit |
| Pacing /20 | 18: redundant AI preview 0:07–0:16; otherwise useful explanation and working holds | 18: removable pause question 1:33–1:42 and extended result repeat; no deduction for being 2:51 |

SOURCE_QA: PASS for the introductory teaching model (lesson lines 23–46, 66–78). Exact decimal rows and early/late stages are schematic examples, not empirical traces. Do not infer an equality test or fixed layer count for individual relationships.

Narration verdict: version 1 REPAIR; version 2 REPAIR/REGENERATE if used alone, but unnecessary as a base because version 1 plus the small donor is stronger. As-is accuracy and substitute gates are not passed by either: version 1 has the zero-context claim and erroneous generated diagrams; version 2 has the matching and exponential-cost claims. Both contain the closing teaching spine. No prohibited imagery or stock attribution was identified in the sampled record; incidental book text is not treated as instructional content. Both require post-production board treatment and standard close. Edit integrity is pending because no repair has been rendered.

## Technical checks

The original architecture describes stacked blocks with attention and feed-forward sublayers; it computes updated representations through weighted combinations and transformations, not a rule requiring two token representations to become equal. Its per-layer complexity also supports the inference that adding otherwise equivalent layers accumulates work rather than inherently making cost exponential. [Vaswani et al., sections 3.1–3.3 and Table 1](https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf).

Published Meta configurations include 32-, 80-, and 126-layer models, supporting the lesson's broad dozens-to-over-a-hundred scale without speculating about private chatbot architectures. [Meta model configurations](https://github.com/meta-llama/llama-models/blob/main/models/sku_list.py).
