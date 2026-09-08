# How AI Answers: deep evaluation, September 8, 2026

Reviewed: live PredictionSection, DogRecapStrip, LastTokenBridgeBoard, AnswerBuildStrip, PredictionLoopTryIt; lesson Markdown; all four current raster boards; renderer sources for the boards; relevant prior Transformer/Vector Space decisions. No lesson edits made. Browser/device interaction and video were not tested.

## Judgment and first recommendation

Keep the phone analogy, concrete dog-name example, ranked alternatives, repeated append-and-predict loop, and the practice exercise. The learning objective should be moving from numerical representations to a sequence of output tokens. Some older explanations still reflect the former idea of choosing an answer from a meaning neighborhood.

First substantive recommendation: remove the Neighborhood badges from AnswerBuildStrip and the sentence about neighborhoods narrowing after it. The displayed ranked tokens are outputs of vocabulary scoring, not the result of first selecting a named neighborhood. These badges look like an algorithmic stage and conflict with the corrected Vector Space framing. Preserve the human observation that the developing sentence changes which continuation fits.

Possible replacement paragraph:

> You asked for a dog name, but AI began with You, a possible start to a reply. Each added token changes what can fit next. After You could name him, a dog name becomes a likely continuation.

The existing “Five predictions. One repeated move.” can remain once the separate punctuation issue is addressed. Do not make all revisions at once; user prefers one suggestion at a time.

## Remaining issues, ordered for discussion

1. Final token versus visible question mark. The question mark is the last displayed token in this simplified question, not necessarily the last input token used by an actual chat model. Chat templates can append assistant/control tokens. The TRY IT currently tests memorizing '?' as the mechanism, with wording “Which final token begins the answer?” that also conflates the input token with the first generated token. Avoid making the user learn chat-template internals; use a clearly simplified token sequence or focus the exercise on predicting from the available context. References below establish the distinction, not exact private formats for current proprietary chatbots.

2. Context is not a relay of a complete compressed question from token to token. “Carries the meaning ... from the whole question,” combined with “carries the context forward,” can sound like earlier positions are discarded. The last-position representation is used to score the next token; new tokens can attend to retained representations of previous tokens. Prefer “uses information from the question and the reply so far” rather than suggesting that one token alone stores all meaning. No KV-cache lecture needed.

3. Before the Answer Begins repeats the older Attention/Transformation split. Its step 4 reads “Attention connects the tokens, and transformation updates their meaning.” Prior lessons were corrected to say both contribute to updating numbers. Candidate: “Attention and transformation work together to update the numbers.” Step 3 could be called Starting Embeddings to match the previous lesson, but avoid gratuitous renaming until the recap's role is agreed.

4. Highest score is correctly restricted to this walkthrough in prose, but the final general inference board says “Take the top-ranked token.” Change the generic step to “Select a next token” and consider “SELECTED TOKEN” instead of “TOP TOKEN.” The illustrated selection may still be Spot; next lesson explains alternatives. Preserve the simple greedy worked example.

5. Scores versus percentages. The prose explains scores, but the boards display percentages with no bridge and no statement that the figures are examples. A short plain-language sentence can say scores become probabilities and the percentages here illustrate the process. Do not name softmax unless needed. Do not present invented percentages as measurements from ChatGPT, Claude, or Gemini. The displayed three percentages need not sum to 100 because they show only leading candidates.

6. Five word selections do not show punctuation or ending. The displayed answer adds a period that is not in a listed selection; “final prediction” sounds like no stop decision is needed. Calling the right panel the fifth prediction instead of final prediction avoids part of this. Either show the result as five words without a period inside the output display or explicitly include punctuation/stop as subsequent steps. A brief explanation of an end-of-response signal can finish the loop without another board.

7. TRY IT wording and learning value. Instruction 4 says “then name the complete process,” but the exercise never asks the learner to name it; the completion text supplies inference automatically. Remove that clause. Question 1 highlights '?' before asking which token it is, so it tests little; a question about the role of the final representation or available context would be stronger. Questions 2 and 4 do practice the greedy selection rule clearly. Keep simple practice, not a technical vocabulary exam.

8. Standalone token/word distinction. The recap briefly calls tokens pieces, while the examples display whole words as one token each. A single learner-friendly framing line can explain the whole-word simplification if needed. Do not verify or assert particular tokens of unavailable proprietary tokenizers. No need to reteach tokenization.

## Presentation and source consistency

- Live AnswerBuildStrip shows predictions 1 and 5 with three intermediate word tiles. Markdown describes five full rows and ranked lists. These are materially different presentations. Synchronize the Markdown when the live walkthrough revision is approved; do not blindly preserve the five-row source as if it were the current UI.
- The live board uses a three-column grid with a fixed 210px middle column and no responsive breakpoint in this component. It risks narrow-screen overflow. This is a source-based finding; not a tested browser rendering. Prefer a stacked small-screen layout if mobile is in scope.
- Paragraph after the live walkthrough lists intermediate neighborhood names that are not shown in its compressed version.
- Phone board has considerable white space for a short example, but this is a lower-priority design choice. Do not start with cosmetic changes while the prediction explanation needs correction.
- Title/banner styles on the latest Vector Space boards provide the current standard if How AI Answers boards are revised.
- Native script syntax check passed. All four live/Markdown raster asset pairs exist and match.
- Video was not reviewed. Do not infer current video correctness from the lesson review.

## Primary sources consulted

- https://arxiv.org/html/1706.03762v7#S3.SS4 : learned linear output projection and softmax yield next-token probabilities. No named-neighborhood selection stage. Attention includes weighted-value computation, not just finding related tokens.
- https://huggingface.co/docs/transformers/chat_templating : chat input includes role/control structure and often an assistant generation prompt after the visible user message. Formats vary by model.
- https://huggingface.co/docs/transformers/cache_explanation : previous keys and values are retained and combined with the newly processed token's information during autoregressive decoding.
- https://huggingface.co/docs/transformers/generation_strategies : greedy decoding and sampling are distinct selection strategies; choosing the top candidate is not universal.
