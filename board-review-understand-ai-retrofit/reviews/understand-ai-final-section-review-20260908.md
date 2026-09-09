# Understand AI: final section review

Reviewed September 8, 2026. Review only; no lesson copy, illustration, prompt, PDF, or video changed.

## Overall assessment

Keep the sequence and the recurring examples. The section has a clear progression: training creates the learned numbers; probability introduces prediction; tokens identify pieces of text; embeddings represent them numerically; attention and layers work with context; vector space supplies a way to picture numerical relationships; inference builds the answer; sampling and temperature explain variation; the computation example establishes scale.

The repeated drinks and dog-name question are useful continuity, not unnecessary repetition. The cities make the mapping idea concrete before the abstract application. The cat example should also remain, but its mechanism needs more careful boundaries across Transformer, Layers, and Vector Space.

The section is not ready to feed into new video generation unchanged. The largest production problem is obsolete source material. Several old prompts explicitly require explanations the revised lessons deliberately removed.

## Teaching changes to discuss

### 1. Distinguish fixed weights from changing representations

**Where:** Training's ending; Embeddings' table/value definitions; the first explanation of layers in Transformer and Layers.

Training correctly says ordinary chat does not change the weights. Embeddings correctly identifies its learned table entries as parameters. Subsequent lessons repeatedly say that layers change the numbers. A beginner can reasonably hear this as a contradiction, or assume the model retrains itself while answering.

The missing connection is that the learned model uses its fixed weights to calculate changing representations of the current text. This needs one plain sentence near the first vector-update explanation, not a new lesson or new technical vocabulary.

Suggested wording:

> The model’s learned weights stay fixed. What changes is the row of numbers representing each token in your message.

For a standalone Layers lesson, incorporate the same distinction into its opening explanation without repeating a long definition of tokens. Keep “numbers” conversational, but make clear which numbers change. Transformer architectures maintain and update a representation at each token position as it passes through the layers; these intermediate values are distinct from the learned parameters. [Anthropic's architecture description, Methods](https://transformer-circuits.pub/2026/workspace/index.html#methods).

### 2. Separate interpreting a whole sentence from an earlier token reading later words

**Where:** Transformer opening and resolution boards, “Be the Attention” TRY IT, and narration of the shared cat sentence.

The human examples work: “thirsty” versus “fresh” changes the interpretation of IT; “river” helps us interpret BANK. The issue is presenting these as literal attention operations at the earlier IT or BANK position in an autoregressive decoder.

Causal attention prevents an earlier token from attending to later tokens. In the two cat/milk sentences, everything through IT is identical. Consequently, IT's own representation at that position cannot change because of the later choice of “thirsty” or “fresh.” Later positions can combine the preceding information and support a different answer about the sentence. [Hugging Face caching explanation](https://huggingface.co/docs/transformers/cache_explanation).

Keep the opening puzzles and the solution board framed as interpretation of the complete sentence. Use an earlier clue for any illustration intended to depict a specific token's attention. Two possible approaches for discussion:

- Keep the existing sentences and say that AI uses the completed sentence to work out the reference, without claiming that the later clue updates the earlier IT position.
- Where a literal token-update example is needed, put the decisive clue first, such as “The cat was tired, so IT sat on the mat.”

The current “IT can draw on information from the earlier word CAT” sentence is helpful and can stay. “Reads your whole message at once” can describe parallel prompt processing; it should not be narrated as every token having unrestricted access to every other token.

The TRY IT's “Be the Attention” name and laptop feedback (“Won’t turn on” ... “so attention links IT there”) blur this boundary. Preserve the fun clue-finding activity; consider framing it as finding contextual clues instead of literally performing one attention operation.

### 3. Remove the remaining promise of a measured, steady journey toward CAT

**Where:** Layers' “How AI Connects ‘IT’ to ‘CAT’” board; narration accompanying the final Vector Space map.

Layers still says “In Layer 1 ... shifting toward CAT,” “Closer to CAT than to MAT,” and “keep shifting toward CAT.” These are stronger claims than Vector Space's revised banner, “IT’s new position reflects its connection to CAT in this sentence.”

A useful illustration of contextual relationships does not establish that a real model's IT vector moves monotonically toward the standalone embedding of CAT, or that nearest-neighbor lookup determines the referent. Contextual representations vary with layer and context, and their geometry is not simply a dictionary of fixed word meanings. [Ethayarajh, 2019](https://aclanthology.org/D19-1006/). Reading out next-token scores is a learned output mapping; it is not generally a closest-original-embedding search. [Anthropic, Methods](https://transformer-circuits.pub/2026/workspace/index.html#methods).

Recommendation: retain the map and its approved connection banner. Change the Layers captions to describe incorporating information and building the contextual connection, without claiming specific distance comparisons at Layer 1 or Layer 2. Avoid adding “conceptual view” labels everywhere. The substantive fix is what the narrative asserts.

### 4. Update the opener's final promise

**Where:** `index.html` OpenerFoundationsSection groups; `lessons/Opener-Understand.md`; the section-map image and its renderer.

“How AI chooses each next token, why answers vary, and what keeps a conversation going” retains the old memory/transcript emphasis.

Suggested replacement:

> How AI builds an answer, why answers vary, and how much math it takes.

This covers the revised final two lessons without introducing temperature before it has context.

### 5. Small terminology and attribution cleanup

- **Prediction versus selection:** How AI Answers says “Each selection is a prediction,” while One More Thing distinguishes probabilities from choosing a token. Prefer “AI makes a new prediction each time it chooses the next token,” or simply remove the extra definition. Keep probability calculation and selection distinguishable without teaching logits or softmax.
- **Vocabulary sizes:** The scale is defensible: OpenAI publishes an approximately 200k encoding, and Google's Gemma paper explicitly describes inheriting Gemini's 256k vocabulary. These are published examples, not proof of every current model behind each chatbot. If retaining brand-specific counts, attach them to published designs rather than an unqualified permanent property of the app. [OpenAI tokenizer definitions](https://github.com/openai/tiktoken/blob/main/tiktoken_ext/openai_public.py), [Gemma technical report, section 3](https://arxiv.org/html/2403.08295v4).
- **Earlier AI:** “The further it read, the more the early words faded” is too inevitable. “Earlier systems could lose track of words as passages grew longer” would match the adjacent board's already careful “often struggled.” Optional wording improvement, not a reason to add a history detour.

## Lesson-by-lesson assessment

| Lesson | What works | Remaining attention |
| --- | --- | --- |
| Understand AI opener | Car analogy; five-part map; permission not to memorize everything | Update final promise; replace obsolete four-part video outline |
| Training | Basketball analogy; guess/check/adjust; three phases with one question; normal-chat weights distinction | Carry the weights distinction into later lessons; prepare a current prompt in the active Prompts folder |
| AI is Math | Equal-likelihood condition; two coins; new evidence; dog-name preview | Current video prompt still teaches removed Bayes/rain/phone material; optional removal of generic final TRY IT instruction |
| Tokens | Reusable pieces; setup versus chat; fixed vocabulary; verified examples | Old video/PDF token IDs and splits must not return; optional narrower vocabulary attribution |
| Embeddings | Taste test before AI; comparison table; integrated definitions | Clarify later that table parameters stay fixed during chat; provide accessible numerical values and input labels |
| Transformer | Problem, explanation, solution, return to examples; attention updates numbers too | Causal direction in examples/activity; old prompt still imposes older mechanism and position-stamp timing |
| Layers | Human rereading analogy; passing updated numbers forward; depth/cost explanation | Fixed weights versus changing rows; distance claims in the IT board; stale video instructions about a blank box |
| Vector Space | Two city maps; repeated drinks; dimension order; new point comparison | Preserve map as explanation of representation, not a nearest-word inference algorithm |
| How AI Answers | Prompt before answer; final-position explanation; visible prediction loop; inference summary | Prediction/selection wording; source prompt still equates a meaning neighborhood with output ranking |
| One More Thing | Expected frequency; temperature comparison; hypothetical computation scale | Update accessibility values and old video metadata; newest prompt is broadly aligned |

## Video preparation: confirmed stale sources

These are production issues even if no further teaching changes are accepted.

| Prompt | Confirmed obsolete instructions |
| --- | --- |
| `Prompts/opener-understand-video-prompt.txt` | Four rows and old category names, versus five current rows |
| `Prompts/ai-is-math-video-prompt.txt` | One-coin board, Bayes biography/theorem, phone keyboard, and rainy-afternoon example, all outside the revised lesson |
| `Prompts/tokens-video-prompt.txt` | CAT ID 9246 instead of 4719; un/believ/able instead of un/belie/vable; seven URL tokens instead of eight; old close and old board inventory |
| `Prompts/embeddings-video-prompt.txt` | Drink token IDs removed from the taste test; CAT 9246; map/truck scored on Sweet/Fizz, which incorrectly carries literal taste dimensions into AI; obsolete closing copy and missing new boards |
| `Prompts/transformer-video-prompt.txt` | Attention as weighing only; transformation as the sole vector update; position stamp “before the first layer”; old close and overly absolute earlier-AI wording |
| `Prompts/layers-video-prompt.txt` | Literal rereading; blank box; removed depth board; “why not hundreds” explanation |
| `Prompts/vector-space-video-prompt.txt` | Requires “It finds the closest match” and “You did exactly what AI does”; old offshore coordinates; old single-map arrangement; obsolete close |
| `Prompts/how-ai-answers-video-prompt.txt` | Phone tray; obsolete ten-board inventory; mandatory claim that neighborhood equals top of ranked list; “takes the top” selection wording |
| Training | No current `Prompts/training-video-prompt.txt` found. An archived prompt exists; it should not silently become the current source. |
| `Prompts/one-more-thing-video-prompt.txt` | Broadly aligned with the revised lesson; make final vocabulary match “writing” and current approved copy when freezing the kit |

The saved PDFs also contain earlier versions. Text extraction confirms old openings in the opener and Training; Bayes in AI is Math; 9246 in Tokens and Embeddings; the blank box and “why not hundreds” in Layers; closest-match inference in Vector Space; the old map-to-answer opening in How AI Answers; and transcript rereading in One More Thing. Regenerate any PDF intended for use from the frozen lesson source. This was a text freshness check, not PDF layout approval.

Also refresh video metadata in `index.html`: Layers still promises “one box stays blank”; One More Thing still advertises “the lottery, the transcript, and the bill.” These descriptions do not match the revised lessons.

Production recommendation: after approved teaching fixes, prepare one current upload kit per lesson containing the approved Markdown, exact boards in teaching order, a close generated from `CLOSE_BOARDS`, and a prompt rewritten around those assets. Do not patch old prompts piecemeal when their required narration contradicts the current lesson. Existing MP4s were not audited in full during this review.

## Visuals and activities

The 43 Markdown-referenced teaching images were inspected as contact sheets plus a separate full view of the final Vector Space illustration. The revised boards largely share the intended title, frame, inner-card, and takeaway treatment. The strongest visual continuity is the drink values, repeated question format, and distinct IT/CAT markers.

Items worth addressing during production or accessibility cleanup:

- Training's three phase boards and the Transformer resolution board are text-dense. Give the relevant card enough narration time and a readable crop/zoom if needed. Do not shorten useful examples just to meet obsolete runtime targets.
- Tokens still uses a ginger cat on its human-versus-token-ID board, whereas Transformer and Vector Space use the approved ragdoll. Optional visual consistency change; it does not affect the teaching.
- Embeddings' numerical inputs have no explicit accessible label per club/dimension in the inspected markup. Add labels without changing the visible exercise.
- Some raster table alternatives omit numerical data, notably the low/high temperature columns and the first taste table. Supply equivalent accessible data. Do not add visible explanatory clutter.
- AI is Math retains “Watch the probability chart change after each clue until the number is found.” This resembles the generic feedback-review instruction the user asked to remove throughout TRY ITs. Optional deletion; the earlier steps already tell students how to play.
- Keep the intentional mental breaks. Do not replace Layers' joke exercise or Vector Space's 2048 game with a forced technical quiz. The live Layers activity still contains six older Transformer claims; reconcile the final joke source and video inventory before producing a replacement. The draft Lemon Pie joke is not in this live activity.

## Checks and limits

- Reviewed all ten section entries: opener plus nine lessons; corresponding Markdown; live lesson functions; associated activity content/logic; available prompt files; closing-copy definitions.
- All 43 Markdown teaching-image references exist. Their file hashes match files referenced in `index.html`, including differently named live/Markdown copies. This verifies image synchronization, not an automated proof that every prose sentence matches.
- Drink values and seven-dimension ordering agree across Embeddings and Vector Space. Mystery-drink Euclidean distances: Pepsi 1, Coke 8, coffee approximately 19.672. The maps illustrate relative relationships rather than an exact plotted metric.
- Starting, low-temperature, and high-temperature displayed columns each total 100%. Shared starting values are Spot 22, Max 17, Buddy 14, Rex 9, Biscuit 6, Other 32. AI is Math's Other 47 is consistent because that board displays only the first three named choices.
- The hypothetical calculation sequence is internally consistent: 2 trillion per token, 200 trillion for 100, 2 quadrillion for 1,000. Preserve its explicit example-model framing; do not attribute the trillion-weight size to undisclosed current chatbots.
- Current CAT ID 4719 and token examples agree across lesson sources. Tokenizer execution was not rerun: tiktoken was not installed in the inspected runtimes. Earlier verification is recorded in the repository.
- Inline JavaScript passes `node --check`; `git diff --check` passes.
- No live browser interaction, small-screen playback, complete video listening, or PDF layout verification was performed in this pass. Those remain production checks, not claimed successes.
- No need to restore the removed memory/cache section, teach temperature as a student-facing app control, add a generic disclaimer to every illustration, or fact-check the deliberately absurd horse joke.

Suggested discussion order: fixed weights versus changing rows; causal-context examples; Layers distance captions; opener promise; minor wording/accessibility; then freeze and rebuild video source kits.
