# Understand AI opener: comparison of two new rolls

## Recommendation

Reroll the opener with a tighter section-introduction brief. `Understand_AI__Opener.mp4` (3:21.8) is the stronger of these two for its explanation of answer generation and variation, but neither is ready for a straightforward visual repair. `Understand_AI__The_Engine_Under_the_Hood.mp4` (3:11.0) has a cleaner beginning, more accurate probability wording, and the exact closing, but its token and answer-variation explanations need new spoken wording.

The central shared problem is that both turn the five TOPICS students will learn into five runtime STEPS inside AI. This is a section roadmap. Training, probability, tokens, context, and answer generation are related topics, but this ordering is not a literal processing pipeline. The narration repeatedly reinforces that interpretation, so removing one sentence does not fix it. The recommendation is about narration accuracy and the purpose of an opener, not runtime, Notebook visual style, or replaceable highlighting.

## Scope and evidence

Read the full current `lessons/Opener-Understand.md`, the corresponding `OpenerFoundationsSection` in index.html, and the current app closing. Inspected both actual board assets. Current map copies `lessons/opener-understand-2-map.jpg` and `illustrations/opener-understand-section-map.jpg` are byte-identical. The current illustration is `illustrations/opener-understand-under-hood-v3.jpg`.

Read complete independent base.en and small.en transcripts for both candidates; read both scene and hold inventories and manually mapped teaching-allocation tables. Inspected all nine four-second contact sheets (four Engine, five Opener). Extracted adjacent frames for generated diagrams and endings, including settled Opener 0:52/0:53 and Engine 0:50. Both sources decoded completely (5,731 and 6,054 frames). ASR is used to verify narration wording; this is not a claim of a complete human listening pass or final edit-integrity certification. Source hashes and durations are in sources.json. No lesson, prompt, source video, or live video was changed.

This is narration intake with a visual-repair inventory, not a finished-video ship grade. No combined numeric score is used to prefer attractive visuals over accurate teaching.

## What both preserve

- AI is its own kind of tool, with the PhD-expert/six-year-old contrast.
- The car/under-the-hood analogy and the practical reason for learning how AI works.
- Reassurance that memorizing technical terms is unnecessary.
- All five subjects on the current section map.
- The idea of building understanding a piece at a time.

The main omissions are not missing topics. The difficulty is added explanation that changes the meaning of those topics.

## Engine Under the Hood — 3:11

### Strengths

- 0:14–0:41: expert/child contrast followed by the car analogy creates a direct reason for the section.
- 0:42–0:53: words-to-answers goal and no-memorization reassurance are explicit.
- 1:27–1:35: correctly emphasizes the specific words and information available when describing changing next-word probabilities.
- 2:20–2:29: gives a useful introductory account of words affecting one another and changing their numerical representations.
- 3:02–3:08: exact approved closing, “The machine won't feel like magic anymore. Take it a piece at a time.”

### Narration problems

1. 1:01–1:06 calls the section map the internal machinery across “five specific steps.” Steps are repeated throughout, and 2:47–3:02 turns the sequence into a foundational system rule. This should describe the learner's progression.
2. 2:13–2:20: tokens each receive “a number that represents its specific meaning.” This collapses the distinction between an identifying token ID and a vector of learned values. It requires replacement wording, not merely a correct graphic.
3. 2:32–2:40: a massive volume of math builds the response, “which explains why answers often vary.” Computation volume does not explain variation. The statement needs replacement, or a coherent removal that still previews the final topic.
4. 1:19–1:25 “scans these learned structures” risks suggesting a search through stored answers; 1:44–1:51 “highest mathematical likelihood” is unnecessary extra detail. Both are expendable in an opener.
5. 2:02–2:09 asks the student to pause and imagine turning a sentence into math. It adds an unneeded exercise before the concepts have been introduced.

Easy possible cuts: 0:53–1:01 predictable-framework sentence; 1:19–1:25 scans-learned-structures sentence; 1:36–1:51 repeated probability exposition; 2:02–2:09 pause instruction; 2:40–2:47 millions-of-translations sentence; much of 2:55–3:02 recap. These cuts alone do not cure points 1–3.

## Opener — 3:22

### Strengths

- 0:21–0:59 clearly connects uneven performance, the car analogy, and being smarter than the tool.
- 0:59–1:12 gives reassurance and the overall learning goal.
- 2:00–2:21 uses plural numbers for token representations, then connects their updates to surrounding words. This is closer to the approved introductory wording than the single-number statement in Engine.
- 2:31–2:49 explicitly connects word-by-word answer construction, probabilities, differing answers, and scale. It is the stronger version of the fifth topic. An opener need not explain sampling in depth here; the dedicated lesson does that.

### Narration problems

1. 1:12–1:18 calls the roadmap an internal logical step-by-step process; 1:18 onward enumerates runtime steps; 2:27 calls the fifth a final assembly phase; 2:59–3:09 repeats that the system follows the entire five-step sequence. As in Engine, this mislabels the teaching order as model architecture.
2. 1:22–1:38 says training builds patterns “rather than memorizing individual facts,” then assumes AI only learned patterns. This creates an unnecessary false opposition. Learned patterns can encode factual knowledge. The rhetorical question repeats the premise, so the tail of one sentence is not the only cut needed.
3. 1:41–1:47 says the “volume of information” changes what is likely. The lesson's point is which information is available, not simply its amount. Replace that phrase or sentence.
4. 2:21–2:27 defines context as a “rigid, measurable mathematical relationship.” This is obscure, unnecessary, and weaker than the preceding concrete explanation. Clean cut.
5. 1:47–1:54 “AI isn't thinking”/most-probable-next-step digression adds an unneeded claim and encourages always-pick-the-top-choice interpretation. The later paragraph is better. Clean cut.
6. 3:14–3:19 says “It won't feel like magic anymore,” rather than the exact current “The machine…” closing. Small difference; not a major teaching defect or the reason to reroll. The Engine version contains a possible donor if a composite is chosen.

Possible cuts: 1:26–1:38 fact/memorization comparison and its rhetorical question; 1:47–1:54 thinking/probability digression; 2:21–2:27 context definition; 2:50–2:58 massive-math recap; 2:59–3:14 process/blueprint recap. Important map framing and probability wording still require new narration. Both ASR engines render an odd word around 1:00 (“mere”); this is not classified as a confirmed spoken error without listening.

## Visuals: separate, repairable work

- Both use the current section map and give its five topics spoken attention. Long map holds are teaching spans, not dead time merely because the board stays onscreen.
- Engine: useful original Notebook car and sketch graphics at 0:00–0:41. Generated 0:42–0:53 “Tokens → Context → Patterns → Probability → Synthesis” diagram introduces an invented pipeline; replace if this source is reused. Settled frame 0:50 confirms the labels.
- Opener: generated technical diagrams at approximately 0:14–0:21, 0:34–0:41, and 1:05–1:12 reinforce the invented architecture. The car illustration at 0:52–0:53 literally labels a broken component and “Internal failure halts entire forward pipeline.” That extends the car metaphor into an inaccurate explanation for AI mistakes; use the course illustration or simpler Notebook car footage there.
- Preserve the useful Notebook shots. Replacing entire introductions with a static roadmap would not be the preferred fix.
- During map walkthroughs, use the exact current map with standard outline-only emphasis, replacing Notebook underlines, yellow fills, and orange marks. No penalty or reroll decision is based on temporary raw Notebook highlighting.
- The native map camera pans vertically: cropped earlier rows in later frames are not an unexplained missing-content claim. All five current rows are present and taught. A repair should use the course's full-board treatment with active-row outlines.
- Both need the standard app closing inserted over the spoken close. Opener has an explicit Notebook outro from roughly 3:18.8; Engine ends on the map. These are normal post-production fixes.

## Source QA and technical basis

The current lesson is sound as a section introduction. It previews the sequence of lessons; it does not assert that probability calculation happens before tokenization, or that the listed subjects are a single runtime sequence. “Each piece builds on the one before it” describes learning. The ambiguity can be prevented in video materials without rewriting the course lesson.

- [Hugging Face text generation](https://huggingface.co/docs/transformers/llm_tutorial): next-token generation uses the prompt plus prior generated outputs; sampling is distinguished from greedy selection. This supports rejecting computation volume as the explanation for varied answers and distinguishing the pedagogical map from a runtime pipeline.
- [PyTorch Embedding documentation](https://docs.pytorch.org/docs/2.14/generated/torch.nn.modules.sparse.Embedding.html): input indices retrieve fixed-size embedding vectors. This supports distinguishing one identifying number from the vector used to represent a token.
- [Language Models as Knowledge Bases?](https://aclanthology.org/D19-1250/): pretrained language models can encode and recall factual knowledge. Learning patterns and retaining factual information are not mutually exclusive.

## Recommended next generation brief

Keep the existing teaching content and make its purpose explicit:

“This is an inviting introduction to the Understand AI section. Explain why understanding the tool helps, use the PhD-expert/six-year-old contrast and the car analogy, and reassure students that they do not need to memorize terms. Present the five items on the Understand AI board as topics they will explore in the course, not five processing stages inside AI. Preview each with the approved explanation. Do not invent extra mechanics, exercises, definitions, or claims about facts, token IDs, or the cause of varied answers. Use conversational wording. End exactly: The machine won't feel like magic anymore. Take it a piece at a time.”

An edited composite could salvage parts of these two rolls, but it would require several narration repairs in addition to normal visual work. Given the user's preference for rerolling rather than searching for donor edit material, another roll with this clarification is the better next step. No reroll or prompt modification has been performed by this evaluation.
