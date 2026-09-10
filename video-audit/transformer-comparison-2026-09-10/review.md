# Transformer: two-version evaluation, September 10, 2026

Recommend **transformer-1 as the repair base**, with selected version-2 narration available as donor material. Version 1 is **4:15.43**, version 2 **4:26.10**. Neither raw video is ready to ship. Attempt a focused repair before requesting another roll; donor voice continuity and exact joins still need verification during the build.

## Evidence and scope

Read the live `HowAIReadsSection` in `index.html` (approximately lines 5440–5547), current `lessons/transformer.md`, both complete base.en transcripts and both complete small.en verification transcripts. Inspected all twelve contact sheets, both scene lists and holds, and prepared manual topic allocations in each `sections.txt`. Checked additional full-resolution frames for the BANK example, the order demonstration, and version 2's loop and named-dimension graphics. Original hashes and runtimes are recorded in `sources.json`.

This is a narration-first intake and visual repair assessment, not a finished-video shipping grade or a claim of continuous real-time audio listening. ASR disagrees on version 2's words immediately before “instantly draws context” at 1:51–1:56; do not treat its strange base-model transcription as a verified voice defect. All retained audio joins require listening and timing checks in the build. No source, live video, lesson, or prompt was changed.

Current lesson board authority, in order:

1. `lessons/transformer-context-problems-editorial.jpg`
2. `lessons/transformer-before-transformers-editorial.jpg`
3. `lessons/transformer-how-transformer-reads-editorial.jpg`
4. `lessons/transformer-attention-transformation-editorial.jpg`
5. `lessons/transformer-resolves-meaning-editorial.jpg`
6. `lessons/transformer-word-order-editorial.jpg`

## Version 1

Its strongest quality is the teaching arc: starting numbers → the LIGHT and pronoun problems → earlier sequential processing → the 2017 breakthrough → attention and transformation → the same examples resolved → position information. The two operations are correctly distinguished at **2:43–3:01**: attention calculates relevance and blends information into the token's numbers; transformation applies fixed patterns to those numbers. It does not make the earlier mistake of claiming that only transformation changes numbers.

The narration is more formal than the lesson and repeatedly promises “precise” meaning. Targeted trims would improve it:

- **0:05–0:13:** removable technical preamble after the initial prompt. Go directly to tokens and embeddings.
- **0:36.74–0:39.26:** cut “and use that data to finalize the definition.” The preceding context explanation stands without implying a definitive dictionary lookup.
- **0:58.94–1:14.26:** repeats that ambiguity requires mathematical work and was inefficient. The next sentence about earlier sequential models begins the actual explanation. Keep only what the transition needs.
- **1:56.56–2:10.64:** “instantly,” “physical distance,” and “solves the distance problem” oversell the advantage. Attention provides a direct computational connection; it does not eliminate every long-context difficulty. Retain the simultaneous-availability idea and a clean CAT-to-IT connection without the absolutes. An exact word-level cut must preserve natural speech.
- **2:19.92–2:30.62:** optional recall exercise appears before the operations have been taught. Remove or relocate; useful explanation immediately afterward should remain.
- **3:31.62–3:42.70:** the actual model does not first discard word order and later restore it. The following DOG/MAN comparison and “Without position data…” explanation already teach why positional information is needed. Cut the dramatic “severe mathematical problem”/“loses all inherent sense” lead-in where a clean transition permits.

### The returning examples need a precise repair

At **3:09–3:19**, the narration attributes the LIGHT and pronoun clues directly to “the attention mechanism.” In this context it can imply that IT's own representation attends to the later words “thirsty” and “fresh.” The lesson deliberately frames this board as interpreting complete sentences, not showing a causal token reading ahead. Preserve that distinction in the repaired narration.

There is usable donor material. Version 2 **2:57.78–3:05.62** describes “turn on” and “carry” as context; its **0:42.10–0:47.04** states the cat/milk interpretations plainly. Version 1's own opening pronoun explanation at **0:52.18–0:58.44** is another same-voice fallback. Build one coherent return-to-examples passage rather than cutting away the lesson's payoff. Do not retain version 2's “critical weights” continuation.

Both versions omit the explicit sentence that learned model weights stay fixed while token representations change. Version 1's “fixed patterns” is the closest spoken support. This is a coverage weakness, not evidence that it explicitly teaches online training. Preserve that phrase and distinguish the concepts clearly in the visual; do not claim the missing sentence has been supplied by a graphic. If the exact spoken distinction is required, additional narration would be needed. Version 1 also generalizes to complex phrasing without naming sarcasm or idioms; version 2 **3:24.24–3:35.08** is an optional complete donor for that extension.

## Version 2

Its **2:20–2:37** explanation of attention and transformation is concise and clear, and **3:24–3:35** explicitly reaches sarcasm and idioms. The opening examples also give the actual LIGHT phrases more fully. These are useful strengths.

It introduces more misleading detail:

- **0:11–0:21:** “baseline dictionary meaning” suggests that an embedding is a literal dictionary entry. Version 1's “starting meaning” is the safer introductory wording.
- **2:38–2:50:** “work together in a loop,” paired with an “Iterative Feedback Update” arrow returning transformation to the same attention box, suggests a feedback loop rather than successive Transformer blocks. Repeated processing is real, but this specific depiction needs replacement or removal.
- **3:06.14–3:16.78:** calls “thirsty” and “fresh” the “critical weights,” then says they determine the attention of IT. The words are context clues, not numerical weights; the later-word/earlier-token implication also conflicts with causal attention.
- **3:36–3:43:** says parallel reading “solves the context problem” and that the model “loses” order. Prefer the conditional explanation of what would be missing without position information.
- **2:52–2:57:** removable pause-and-identify prompt. **4:04–4:16** repeats the position takeaway after already teaching it. Neither is a reason to reject the video by duration alone.

## Preserve Notebook visuals; repair concrete defects

Version 1 has useful paper-style opening art, a sequential-processing animation, the 2017/Transformer graphic, lamp/cat imagery, and interlocking gears. Preserve these wherever the retained narration fits. No blanket board replacement is recommended.

Specific visual work:

- **Version 1, approximately 0:28–0:40:** the BANK animation draws information from the later word “overflowing” into BANK's updated vector. Full-resolution frames at 0:33 and 0:37 confirm this is content, not a transition artifact. Retain the earlier token/embedding build; replace the offending contextualization beat with a causally sound Notebook-style visual, for example BANK drawing from the preceding RIVER. Do not invent a new course board.
- **Version 1, 2:07–2:20:** the illustrative attention animation is potentially useful, but remove any presentation that treats the displayed attention weight as confidence that IT has a particular referent. Its “Resolved referent” footer needs particular care. Attention weight is not a calibrated pronoun-answer probability.
- **Version 1, 3:38–3:43:** the sequential-to-scattered-word animation is coherent across adjacent frames, not gibberish. Its “Positional Order Lost” label reinforces the misleading lost-and-restored story; remove with the narration trim or replace that short beat with the existing order comparison.
- **Version 2, 2:38–2:50:** do not borrow the loop animation or final BANK panel. The latter labels embedding dimensions “Water/Stream,” “Financial Institution,” etc. as if those were literal model dimensions, undermining the preceding Embeddings lesson. This is a teaching accuracy issue, not a palette preference.
- Source boards have Notebook underlines, yellow fills, arrows, and camera crops. These are normal raw material. Reinsert current exact boards for their specific teaching spans and apply course outline-only highlights. Do not lower raw narration selection because of native highlighting. Full-board or complete-card framing must be restored where selected.
- Keep useful generated explanatory graphics between those board spans. Standard course closing board replaces the generated ending; both narrations contain the two required closing lines. Add one-second pauses at actual idea transitions, not indiscriminately after every sentence.

## Independent raw-source scores; no total

| Dimension | Version 1 | Version 2 |
|---|---|---|
| Teaching coverage /20 | **18** — all six major board ideas; fixed-model-weights distinction not explicit, broader applications compressed at 3:19–3:31 | **19** — all major ideas plus sarcasm/idioms at 3:24–3:35; fixed-model-weights distinction omitted |
| Lesson material /15 | **14** — examples and sequence retained; 0:36 “finalize the definition” and absolute distance claims go beyond source | **12** — dictionary-entry, feedback-loop, and critical-weights explanations add misleading mechanisms at 0:17, 2:38, 3:06 |
| Teaches vs recites /15 | **12** — good attention blending at 2:47; return examples need causal clarification and “loses order” distorts the why | **11** — strong 2:20–2:37 explanation, weakened by explicit words-as-weights and feedback-loop claims |
| Board teaching /10 | **9** — every board concept addressed; returning examples 3:09–3:19 require clearer complete-sentence framing | **9** — every board concept addressed; return-board explanation 3:06–3:17 gives a misleading mechanism |
| Cleanliness /20 | **20** — settled teaching labels generally readable; blurred transition frames not mistaken for persistent defects. Persistent unreadable teaching content would cost credit. Accuracy and course-format issues logged separately | **20** — settled content readable; named dimensions are an accuracy problem, not illegibility. Persistent unreadable teaching labels would cost credit |
| Pacing /20 | **17** — removable setup 0:05–0:13, repeated transition 0:59–1:14, recall detour 2:20–2:31 postpone the central mechanics | **18** — useful coverage, but pause prompt 2:52–2:57 and repeated order summary 4:04–4:16 add little |

Source QA: PASS for the approved introductory model, with “whole message at once” understood as prompt availability/parallel processing, not unrestricted future-token attention. The source explicitly qualifies the return examples as complete-sentence interpretation and labels the order comparison “Without Position Information.” Those constraints should survive editing.

Narration verdict: **version 1 REPAIR**, version 2 useful donor rather than preferred base. Neither passes an as-is accuracy/shipping decision: version 1 includes a future-to-earlier BANK vector update visually and ambiguous return-example mechanics; version 2 adds the explicit critical-weights and loop issues. Broad teaching coverage and both spoken closing lines are present. Neither is a fully equivalent finished substitute until the flagged mechanics are repaired. No prohibited imagery or third-party stock attribution was identified in the sampled record. Engine branding is not treated as third-party stock provenance. Both need standard close, board treatment, and sync checks; edit integrity and full boundary inspection remain pending because no new edit exists.

## Technical reference

The original Transformer paper distinguishes stacked attention/feed-forward blocks, weighted combinations, causal masking in the decoder, and positional information. It supports the corrections above; applying those constraints to the videos is this review's inference. See sections 3.1–3.3 and 3.5 of [Attention Is All You Need](https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf). The position-stamp illustration is an introductory metaphor, not a claim that every modern model literally appends an integer tag.
