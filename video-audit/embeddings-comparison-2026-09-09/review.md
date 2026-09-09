# Embeddings: raw-roll comparison

Reviewed September 9, 2026. **Recommendation: use version 2 as the repair base. Keep version 1 as a possible closing-narration donor.** Neither raw file is ready to ship.

This is a narration intake and visual-repair inventory under rubric r5, not a finished-video numerical grade. No lesson, prompt, source video, or live video was changed.

## Why version 2

Version 2 (4:19) gives the stronger standalone explanation. Its taste-test walkthrough clearly separates a vector, a dimension, and a value. Its comparison with AI explicitly says the numbers are learned during training, describes patterns in how words are used together, and explains that the unlabeled values work together to represent meaning. It names the embedding before walking through the lookup table. These are useful explanations, not padding.

Version 1 (3:19) is a credible fallback, not a failed lesson. It preserves the examples and explains ID lookup well. However, it compresses the AI comparison, never explicitly places learning during training in the narration, and delays naming the embedding until the end of the table walkthrough. It also says the taste test and AI have an identical underlying mechanism. Both use numerical representations, but their values are obtained differently. That sentence should be cut if version 1 is used.

Version 2's questionable statements are removable additions. Cutting them leaves the essential teaching intact. This is a repair opportunity rather than a reason to reroll.

## Teaching coverage

| Beat | Version 1 | Version 2 |
|---|---|---|
| Student ID identifies but does not describe | Clear, 0:15–0:35 | Clear, 0:19–0:43 |
| Coke/coffee numerical profiles | Good, 0:45–1:15 | Strong, 0:50–1:18 |
| Vector, dimension, value | Taught briefly, 0:55–1:02 | Deliberate definitions, 1:18–1:31 |
| Identical first six scores; Citrus captures a difference | Clear, 1:15–1:33 | Clear worked problem, 1:32–2:05 |
| Every token; thousands of dimensions | Covered, 1:42–1:52 | Covered, 2:28–2:45 |
| Learned values, including negatives and decimals | Covered, 1:53–1:59; training timing implicit | Explicitly learned during training, 2:46–2:53 |
| No human dimension labels; values work together | No labels and patterns covered, 1:59–2:08 | Both points explicit, 2:54–3:07 |
| Embedding = complete row | Named near 2:51 | Named at 3:07 before table walkthrough |
| Cat → ID → embedding-table row | Clear, 2:21–2:39 | Clear, 3:17–3:33 |
| Dimension columns and parameter value | Covered, 2:39–2:50 | Covered, 3:34–3:45 |
| Pieces of words receive embeddings | Covered, 2:56–3:09 | Covered, 3:55–4:07 |
| Exact approved close | Present, approximately 3:09–3:15 | Meaning preserved, wording expanded, 4:07–4:15 |

The student-ID example and both drinks boards are meaningfully narrated in both versions. Neither needs to read all cells aloud. Omitting the on-page interactive club exercise does not impair this explanatory video.

## Version 2: proposed narration edits

Times refer to the original upload and are approximate; final edit boundaries require audio checks.

1. **0:12–0:18:** remove “random” from “that ID is just a random number,” if the join is clean. An ID is an assigned identifier, not a fresh random number generated for each occurrence. The subsequent catalog-number explanation is good.
2. **1:43–1:45:** optionally remove “Take a moment and consider.” Keep the actual question and its answer; they make the added-dimension example work.
3. **2:05.7–2:14.1:** cut the repeated generalization after Citrus has already resolved the problem. This also removes the generated vector-space detour.
4. **2:19.6–2:22.9:** cut “A row of numbers represents an exhaustive list of characteristics.” The taste test itself shows why a finite profile need not capture everything. AI embeddings are learned representations, not exhaustive definitions.
5. **3:49.6–3:54.2:** cut “its unique mathematical definition based on its relationship to every other token.” End the preceding sentence at “the token's embedding,” then move to the word-piece example. The stronger explanation already given is that values capture patterns of use and work together.
6. **Closing:** version 2 paraphrases the approved lines. Version 1 contains the exact close and is a possible short donor. Audition voice/tone compatibility before committing; do not assume two rolls will splice naturally. A clean edit of version 2's wording may also be possible, but should not leave audible word-level joins.
7. Add roughly one-second teaching pauses at the main transitions where needed, especially into the AI comparison and the lookup-table walkthrough. Preserve ongoing explanatory narration.

No essential lesson beat is lost by the proposed cuts. The finished video should remain around four minutes; runtime is not the selection criterion.

## Visual repairs, kept separate from narration quality

Both videos use all five current source-board slots, including the approved faceless student-ID variant. Notebook's temporary yellow highlighting is expected raw material. It is editing work, not a reason to reroll.

For version 2:

- **0:00–0:19:** generated token IDs differ from the verified course examples. Preserve an engaging opener, but use consistent IDs if numbers are displayed. The narration does not require reading them.
- **0:19–0:39:** use the current course student-ID illustration where it supports the narration, with a full view that includes the IDs. The line about four cards may fit the faceless board more literally; choose the framing during editing rather than forcing a visual mismatch.
- **2:05.5–2:23.8:** generated diagrams add terminology and a rewritten drinks table. The settled frame at 2:12 gives Coke and Pepsi Sweet 8, Bitter 2, Fizz 7, Heat 0, Caffeine 6, Dark 9, contradicting the lesson's 9, 1, 10, 2, 3, 8. The proposed cut removes most of this span. Use a short appropriate bridge for the remaining transition into the AI comparison.
- **3:12–3:54:** retain the actual Inside a Real Model board, but rebuild the camera and highlight sequence to show complete spoken components. Around 3:39–3:45, the narration discusses a learned value while the generated arrow remains on dimension headings. This is a synchronization repair.
- **3:55–4:07:** replace the generated subword diagram. At 4:05, it assigns ID 4719 to `un`, even though this same video just used 4719 for `cat`. It also supplies other invented IDs. A clean three-row illustration can retain the useful narration. Use the verified token IDs if included: un 359, belie 32898, vable 24694. Do not imply its sample embedding values were measured from a named model.
- Replace the closing visuals and engine outro with the standard course close. Keep appropriate Notebook graphics elsewhere, including the numerical-row visual near 3:07, rather than turning the entire video into uninterrupted boards.

For version 1, the main visual repair spans are the invented introductory token split at 0:06–0:15, the unnecessary dimensionality sketch at 1:33–1:41, the course-board camera/highlights, the word-piece narration still over the cat table at 3:01–3:09, and the close. These do not outweigh version 2's stronger comparison explanation.

## Source and verification

Current grounding: `lessons/embeddings.md`, the Embeddings section of `index.html`, and the current five referenced course boards. The Notebook student-ID board is an approved upload substitute for the face illustration, not a retired board.

Source QA found no material contradiction in the core teaching: a vector is a row of values, its positions are dimensions, token IDs select embedding rows, and the embedding-table values are learned parameters. The drink ratings are explicitly a taste-test example, not measured beverage facts. The model table's sample numbers illustrate lookup, not an asserted dump of a named model. [PyTorch's Embedding documentation](https://docs.pytorch.org/docs/2.14/generated/torch.nn.modules.sparse.Embedding.html) documents the lookup-table structure, vocabulary size, embedding dimension, and learnable weight matrix.

Both full base.en transcripts and independent small.en transcripts were read. All eleven contact sheets were inspected (five for version 1, six for version 2), along with the scene and hold inventories and targeted full-resolution frames. Manual section maps and source metadata/hashes are retained. Board pans were considered across neighboring frames; partial sampled crops were not treated as standalone content errors.

ASR disagrees about pronunciation/spelling of the fragments in version 1; the second pass recognizes the intended three pieces. No pronunciation defect is asserted from the first transcript alone. There was no complete real-time listening pass, and the proposed audio joins and donor compatibility remain build-stage checks. This report does not certify shipping audio, transition integrity, or final ship gates.

Tracker-ready disposition: **Embeddings — select version 2 for repair; version 1 retained as possible exact-close donor; no shipping approval yet.**
