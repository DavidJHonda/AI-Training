# How AI Answers, roll 4: narration review

Candidate: `Prompts/how-ai-answers-4.mp4`, 3:22.792. Explainer format. Scope is narration only, as requested; no assessment of visual suitability or edit authorization is implied. The three forthcoming cinematic rolls are not part of this review.

## Assessment

The transcript teaches every essential point in the current lesson. It is a strong narration reference for the cinematic comparison, particularly the spoken why, the question plus You explanation, and the question plus all four answer words at him. No material conceptual error or missing essential explanation was identified in the transcript.

This is a provisional transcript-based assessment, not final KEEP clearance. The complete small.en transcript was reviewed against the current live lesson, upload Markdown, and prompt. A medium.en re-transcription checked the You passage. Direct listening was not performed, so delivery, pronunciation, and any graft feasibility remain unverified. One required sentence has a possible extra word; the recognizers disagree about that word. It should not be silently marked verbatim MET or treated as a demonstrated conceptual failure.

The separate 525-word NARRATION-DRAFT.md was a review draft, not the active upload source. Roll 4 is assessed against the actual current lesson and upload instructions, not penalized for failing to read that draft word for word.

## Essential teaching, in order

Quotes below are transcribed wording, with source timestamps. Capitalization of tokens is normalized for readability.

| Teaching point | Assessment | Evidence |
| --- | --- | --- |
| How an answer begins | TAUGHT | 0:08.20–0:15.96: the system processes the words together, then faces “How does it actually begin an answer?” |
| Words shown as single tokens | TAUGHT | 0:16.52–0:19.94: “We’ll show words as single tokens to make this example much easier to follow.” Also redundantly introduced at 0:05.32. |
| Dog-name question | TAUGHT | 0:20.84–0:23.24: “What should I name my new dog?” |
| Tokens, positions, starting vectors, layers | TAUGHT | 0:28.12–0:43.42 explains breaking into pieces, marking positions, starting numbers, and attention plus transformation updating them. |
| Prior tokens affect each vector | RICH | 0:44.48–0:50.26: “each token’s vector is updated using information from the tokens before it.” This leads directly into the example. |
| Follow the question mark through the layers | RICH | 0:50.64–1:09.26 explicitly labels the example simplified, follows the starting vector, and explains numbers changing with the dog-name question. |
| Same token, different context | RICH | 1:10.32–1:32.12 compares naming a dog and choosing dinner, explains why the numbers differ, and says the dog question mark reflects “the context of your whole question.” The dinner question is described, not quoted in full, but the comparison is explained. |
| Why that matters for the first prediction | RICH | 1:33.02–1:39.00: “Why is this important?” followed by the required first-token explanation. The transcript shows about 1.26 seconds between the question and answer. |
| Prediction repeats using the growing context | TAUGHT | 1:39.52–1:46.86: adds the chosen token to context, predicts the next one, using “your question and the answer so far.” |
| First distribution | TAUGHT | 1:47.72–2:01.46: empty answer; You 18%, A 14%, Great 9%, other tokens 59%. All values match. |
| You becomes the last token and carries answer context | RICH | 2:01.46–2:23.08 selects You, identifies it as the last token, says the context includes part of the answer, and explicitly explains “the question plus the one-word answer, You.” |
| Add could, name, him separately | TAUGHT | 2:23.98–2:33.68 narrates all three additions individually. |
| Each addition becomes context | TAUGHT | 2:34.22–2:36.08: “Each added token becomes part of the context.” |
| Him reflects question plus all four answer words | RICH | 2:37.08–2:43.20: “Him is now the last token” and its updated vector reflects the question “plus all four answer words.” This is the important explanation missing from earlier wording. |
| Name distribution | TAUGHT | 2:43.74–2:55.08: a dog name is likely; Spot 22%, Max 17%, Buddy 14%, other tokens 47%. All values match. |
| Select Spot; another result is possible | TAUGHT | 2:55.08–3:03.68 selects Spot, explicitly allows another name on another run, and reads “You could name him Spot.” |
| Period and stopping signal | TAUGHT | 3:04.68–3:12.68 adds a period and explains the special end-of-answer token. |
| One token at a time; inference | TAUGHT | 3:13.78–3:18.84 gives both closing lines, in order. |

## Required wording

| Required line | Transcript finding |
| --- | --- |
| AI uses the final token’s updated vector to predict the first token of its answer. | MET, 1:35.08–1:39.00. |
| “You” is now the last token. | MET, 2:03.66–2:05.38. |
| The last token’s updated vector reflects both your question and everything AI has written so far. | Meaning taught at 2:06.34–2:11.38. Literal compliance unresolved: small.en returns “everything the AI”; medium.en returns “everything that AI.” Direct listening is needed to resolve the extra word. |
| Each added token becomes part of the context. | MET, 2:34.22–2:36.08. |
| A special end-of-answer token signals that the reply is complete. | MET, 3:09.58–3:12.68. |
| Every answer is built one token at a time. | MET, 3:13.78–3:16.22. |
| The whole run is called inference. | MET, 3:16.22–3:18.84. |

MET here means transcript wording matches, ignoring punctuation and case, not a direct-listening certification. Under the strict narration-review gate, final KEEP remains pending the unresolved literal line and listening. No verified repair or graft is claimed.

## Clarity and editorial opportunities

1. **Remove the generic opening and duplicate simplification if this audio is used.** The 0:00–0:07.36 passage starts “Welcome to this explainer” and introduces the words-as-tokens simplification. Starting at the complete sentence at 0:08.20 preserves the hook and the clearer simplification at 0:16.52. This is a proposed cut, not an auditioned edit.
2. **Keep the concrete You explanation.** The general context statement at 2:06.34–2:11.38 is immediately restated specifically at 2:15.14–2:19.34. The specific explanation is valuable. If tightening, consider moving the general sentence to a later recap, as in the narration draft, rather than deleting the concrete question-plus-You connection. Do not authorize a move until the cinematic versions and joins are reviewed.
3. **Prefer “predict what comes next” over “predict exactly what comes next.”** “Exactly” at approximately 2:19.70–2:23.08 adds an unnecessary impression of certainty. This is a wording concern, not evidence that the narration teaches deterministic selection; it later explicitly allows a different name. The second recognizer also mis-transcribes predict as protect here, so audition before editing.
4. **Prefer “different updated vector” over “completely different updated vector.”** At 1:27.10–1:30.58, completely adds emphasis without helping explain the relationship. It is not necessary to imply every number changes. Optional cleanup, not a missing concept.

The essential arc is intelligible from the transcript alone: prepare the question, contextualize the question mark, explain its predictive role, select You, expand the answer, explain him’s context, predict a name, then finish. The new spoken signposts address the user's main clarity concern. No temperatures, sampling lesson, essay analogy, or perfect-storage claim is introduced.

## What to compare in the cinematic rolls

Preserve or improve these whole explanatory passages:

- 1:10.32–1:39.00: same token comparison and the spoken why.
- 2:12.36–2:23.08: context now includes the answer, specifically You, and supports the next prediction.
- 2:34.22–2:43.20: each token becomes context; him reflects the question plus four answer words.
- 2:55.08–3:18.84: another name is possible, the response finishes, and the exact close.

These are comparison candidates, not approved or verified audio donors. Voice continuity and complete joins must be listened to before grafting. No visual plan is proposed for this explainer, honoring the request to evaluate narration while cinematic rolls are still generating. No source material, lesson, or video was changed during this review.
