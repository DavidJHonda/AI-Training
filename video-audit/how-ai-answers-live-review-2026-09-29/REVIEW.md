# How AI Answers — live review, September 29, 2026

**Recommendation: keep the existing teaching and make a small visual repair. A reroll is not warranted by the evidence reviewed.** The dog-name example carries the mechanism well, the numerical walkthrough is complete, and the shortened ending reaches the takeaway directly. The weakest illustration is the dog beside an unexplained red square at 2:49–3:06.

This is a transcript-and-frame evaluation, not a completed listening or continuous-motion sign-off. No video, lesson, or website changes were made.

## Verified live version

- Public course: https://besmarterthanthetool.com/
- Served video: https://besmarterthanthetool.com/course-assets/how-ai-answers/how-ai-answers.mp4?v=20260928ship1
- Exact SHA-256: `451fa414b0e0fbc971e71b6ccb7ae8d1663e001b1a1ed25c297466e373d73b3e`.
- 19,403,584 bytes; 219.667 seconds (3:39.7); 6,590 decoded frames, 30 fps, 1280×720. Public file, canonical local MP4, and the prior v10 candidate hash agree.
- Public `PredictionSection`, `DogRecapStrip`, `LastTokenBridgeBoard`, and `AnswerBuildStrip` match the local lesson source exactly. The canonical local JPGs match the v10 build's protected hashes. This review did not separately hash the public JPG responses.
- Evidence: `public-verification.json`, `live-lesson-source.txt`, `current-assets-verification.json`, fresh `how-ai-answers/transcript.txt`, five contact sheets, and selected delivery-resolution frames.

## Findings, in priority order

1. **Clarify the dog-versus-red-square scene, 2:48.967–3:05.967.** During the explanation that the response starts with “You” rather than a dog name, the image shows a dog and a blank red square divided by a vertical line. At the sampled times, the square supplies no readable connection to “You.” The dog is relevant; the anonymous square makes the comparison harder to understand. Keep the dog and existing composition, and label the right-hand element “You,” preferably with a small “First reply token” label. This is a targeted teaching improvement, not a reason to replace the entire illustration with a board. See `frames/176.000.jpg` and the 2:52–3:04 contact-sheet sequence. Final placement and tracking need a motion preview.
2. **Improve the ending diagram's label contrast, approximately 3:21–3:25.** Purple `<EOS>` text sits on almost-black boxes. The narration clearly explains the stopping token, but the graphic's key label is needlessly hard to read. Keep the token sequence and stopping animation; brighten the text or use a light label patch. The illustrative 91% is not itself a defect or a sourced factual claim. See `frames/203.000.jpg`.
3. **Optional future tightening: the setup repeats its main point.** From about 1:06–1:33 the final vector/probability relationship is explained, restated as a “launching pad,” and introduced again as readiness to reply. The first worked prediction begins at 1:45.7. This is understandable, but more formal and slower than the later concrete example. I would audition a shorter transition if another narration edit is requested; I do not recommend reopening the approved audio solely to reduce runtime. No cut or splice is approved or auditioned in this review.

The recent question reprise at 1:43.76 is useful: it restores the actual question immediately before Prediction 1. The banner geometry and full-question highlight look correct in inspected encoded frames. The complete active prediction cards remain readable during zooms. Both closing lines are present, and the literal final frame is the standard course close.

## Narration review

LESSON: how-ai-answers

CANDIDATE: verified public v10, 3:39.7

VERDICT: **KEEP recommendation for the existing narration**, based on the fresh full transcript and the previously accepted simplifications documented in v9/v10. This is not a new unqualified end-to-end pass: actual listening remains unperformed.

| Teaching point | Assessment | Evidence from fresh transcript |
|---|---|---|
| Opening problem: how reading becomes a reply | TAUGHT | 0:00–0:09 asks how AI begins its reply after processing the prompt. |
| Concrete dog-name question | TAUGHT | 0:11–0:13 and again 1:43.76–1:45.68: “What should I name my new dog?” |
| Break the input into tokens | TAUGHT | 0:15.92–0:20.80 explains smaller pieces called tokens. |
| Positions preserve order | TAUGHT | 0:20.80–0:26.16 explains where each piece belongs. |
| Starting vectors carry initial meaning | TAUGHT | 0:26.16–0:31.68 explains turning tokens into numbers with starting meaning. |
| Layers update those numbers using context | TAUGHT, abbreviated recap | 0:31.68–0:39.36 names layers and attention using the message. The separate transformation operation is not spoken; see limitations below. |
| Final token gathers preceding information | RICH | 0:58.96–1:06.40 uses the funnel comparison and identifies the question mark. |
| Final vector drives next-token probabilities | RICH | 1:06.40–1:22.48 explains the link; 1:26.08–1:33.36 explicitly says every potential next token in the vocabulary. |
| Select, add, and use the expanded context again | TAUGHT | 1:33.92–1:43.76 states the repeating loop and the change to context. |
| Prediction 1 and all three values | RICH | 1:48.24–2:05.28: final question mark; You 18%, A 14%, Great 9%; selects You. ASR spells spoken “You” as “u.” |
| Three intermediate predictions | TAUGHT | 2:05.84–2:16.32 explicitly explains three cycles adding could, name, him. |
| Prediction 5 and updated final token | RICH | 2:17.12–2:28.64 explains the reply so far and him becoming the new final token. |
| Prediction 5 and all three values | RICH | 2:29.36–2:43.76: Spot 22%, Max 17%, Buddy 14%; selects Spot. |
| Completed sentence | TAUGHT | 2:44.32–2:48.16: “You could name him Spot.” |
| Why You can come before a dog name | RICH | 2:48.80–3:05.12 explains a natural conversational beginning. |
| Each addition changes likely continuations | RICH | 3:05.76–3:16.32 connects the growing phrase to the likely dog name. |
| Special token stops the answer | TAUGHT | 3:16.96–3:25.28 states the stopping condition. |
| Inference names the generation process | TAUGHT | 3:25.92–3:29.12 names the repeating cycle. |
| Both closing lines | TAUGHT / MET | 3:29.84–3:34.96 gives both lines in full. |

HARD REQUIREMENTS: “inference,” “Every answer is built one token at a time,” and “The whole run is called inference” are present in the transcript. All six example percentages are correct.

ERRORS: No contradictory example values or reversed mechanism found. Two previously accepted compressions should remain visible in the record rather than being silently counted as verbatim coverage:

- The page explicitly says words are shown as single tokens for simplicity. That sentence is **not spoken**. Early narration uses “word” at about 0:43–0:47 and 1:10–1:14; later teaching consistently says token and initially defines tokens as smaller pieces. Add the caveat if generating new narration. It would make this video more self-contained without changing the worked example.
- The page's layer recap says attention and transformation work together. The audio names attention but omits transformation. The contextual-update relationship is taught, and the prior v9/v10 review records the abbreviated recap as accepted. A future full generation should name both. This recommendation does not claim that those words are currently spoken.

SOURCE_QA: No blocking lesson-source error found for this introductory example. Selection from a vocabulary distribution and EOS stopping are consistent with [Hugging Face's generation documentation](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation); sampling can select something other than the maximum, as distinguished in [its decoding-strategy documentation](https://github.com/huggingface/transformers/blob/main/docs/source/en/generation_strategies.md). Treat the question-mark final position and whole-word tokens as the lesson's simplified example, not universal chat-template/tokenizer behavior. No advanced architecture material needs adding to this introductory video.

ADDITIONS: The funnel analogy, “Once upon a” illustration, and end-token illustration support the lesson. Their illustrative numbers do not warrant removal simply because they are not in the page text. The wording “only after” at 3:09 is stronger than the page's “becomes a likely continuation”; in context it explains this chosen sentence, not a universal rule about where dog names can appear.

REPAIR PLAN: No narration graft, new voice, or reroll proposed. No donor audition was performed.

LISTENING: None. ASR establishes evidence about wording, not cadence, voice continuity, or absence of clicks. The inserted-question joins at 1:43.600 and 1:45.633 and the closing join at 3:29.400 remain listening checkpoints.

## Board and camera plan

For the recommended narrow visual repair, preserve the existing boards and their timing. The table documents that retention; it is not an instruction to rebuild them. Current board assets were visually inspected.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| Before the Answer Begins | Tokens → Positions → Starting Vectors → Through Layers → takeaway banner | Full unmarked opening, then complete-card zoom/pan, return to full board | 0:13.333–0:49.067, 35.733 s | Dense. Retain the previously approved long-run exception; the narration walks the four stages. No decorative break proposed. |
| Why the Final Token Matters | The Question → The Final Token → takeaway banner | Full board; no new dive | 0:49.067–0:54.000 and 0:58.000–1:23.900; 4.933 s and 25.900 s | Compact. Preserve question-token drawing at 0:54–0:58. |
| The Answer, Token by Token | Question → Prediction 1 whole card and explained sections → three intermediate predictions → Prediction 5 whole card and explained sections → final sentence | Full-view arrival/question, then complete active prediction-card zooms, return to full view | 1:43.533–2:07.733 and 2:15.933–2:48.967; 24.200 s and 33.033 s | Dense. Preserve the intermediate-token reveal at 2:07.733–2:15.933 and the newly repeated question. |
| Standard close | Unmarked | Preserve established hold, push, settled final frame | 3:29.400–3:39.667, 10.267 s | Both closing lines and final course image are intact. |

Longest continuous board run: 35.733 s. Longest board-to-board chain: 40.667 s. These exact times come from the manifest for this verified file hash; the fresh ORB scan is corroborating evidence with half-second sampling, not frame-exact cut detection. Long board exposure alone does not establish dead time: these spans still explain their displayed material.

Supporting scenes to retain: opening context/final-token sequence (0:00–0:13.333); question-token drawing (0:54–0:58 and 1:28.3–1:33.967); vocabulary/selection imagery (1:23.9–1:28.3 and approximately 1:33.967–1:43.533); growing answer (2:07.733–2:15.933); final-token/prediction/stopping sequence (3:05.967–3:25.933); Inference title over answer tokens (3:25.933–3:29.400). Repair the dog comparison's missing connection and EOS contrast while keeping the surrounding artwork and sequence. These retention recommendations are based on sampled successive frames and narration timestamps; continuous animation timing has not been certified.

Selective pauses: none proposed. Without listening, there is no basis to prescribe added silence.

## Verification limits

Performed: live HTML fetch; complete public MP4 stream hash; live/local lesson-source comparison; fresh full-file transcription; complete sequential video decode; inspection of all five four-second contact sheets, selected full-resolution frames, three canonical boards, and the literal final frame; exact-build asset-hash comparison. Opened the public MP4 in the browser and observed it playing.

Not performed: perceptual audio listening, uninterrupted end-to-end visual observation, a fresh every-splice transition guard, phone testing, or the embedded lesson-player flow behind the course entry form. Prior v10 checks are historical evidence for this same file, not substitutes for newly performed tests. Tracker status was not checked or changed. No edits, commits, shipping, or deployment were undertaken.
