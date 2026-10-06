# Vector Space versions 7 8 and 9

**Use version 8 as the base and repair it with two short passages from version 9. Do not request another full reroll now.** Version 8 restores all 17 required passages, all four comparison questions, the named mystery-drink values, training, the return to the opening question, and the separate IT token. It is a substantial improvement over version 6.

Two fixes remain in the core narration: define embedding at the opening and correct the base Pepsi vector. Version 8 also adds an inaccurate absolute claim after the required close; remove that sentence. Version 9 contains the complete opening and correct Pepsi passage. No new narration needs to be invented for this plan.

| Raw candidate | Runtime | Recommendation |
| --- | --- | --- |
| 7 | 4:40 | Reject as the base. Omits the drink numbers, says Coke/Pepsi scores are identical, includes a production direction, and rewrites the close. |
| 8 | 5:25 | **Recommended repair candidate.** Strong teaching coverage and all locked passages. Two whole-beat donors plus removal of the final added claim address the identified core failures. |
| 9 | 4:47 | Keep as the opening and Pepsi donor. Correct numerical examples, but several required conclusions are paraphrased or absent and physical-change language returns. |

**Review status:** Version 8 is not KEEP as delivered. A complete repair is identified in text and short joined-audio previews have been prepared, but it is **not a verified REPAIR verdict yet**: the course rule requires direct listening and audition of the joins. Versions 7 and 9 are not KEEP either. Their standalone failures would require extensive repair or a reroll; using 8 avoids that work. The production recommendation is targeted repair, not another blind generation.

## Evidence and limits

Read the current lesson and interaction data in `index.html`, the complete narration source, the revised customization prompt, and the production storyboard. Reviewed complete small.en transcripts of all three files, with independent base.en transcripts for all three. The two passes agree on version 8’s Pepsi citrus 1, version 7’s “Deliberate pacing,” and the material closing/physical-language problems. They also agree that version 9 gives Pepsi citrus 10.

This is a complete transcript and sampled-frame comparison. **No direct audio listening or real-time motion assessment is claimed.** Raw clips and draft joins are available below for audition; voice continuity, pronunciation, breaths, and exact cut edges remain unverified. ASR spelling of Its versus IT’s is a homophone and is not a narration error.

Visual evidence comes from sequential decoding: one sample every 12 seconds throughout each video, plus denser samples around version 8’s reveals and other selected scenes. Useful generated visuals remain provisional until watched with the narration. These are raw-roll evaluations, not finished-video shipping reviews.

- [Source files and hashes](sources.json) and [lesson/prep hashes](review-source-hashes.json)
- Complete transcripts: [7](transcripts/vector-space-7.txt), [8](transcripts/vector-space-8.txt), [9](transcripts/vector-space-9.txt)
- Independent transcript checks: [7](crosscheck/vector-space-7.txt), [8](crosscheck/vector-space-8.txt), [9](crosscheck/vector-space-9.txt)
- [Required-passage match data](required-passages.json); punctuation, capitalization, and apostrophe typography normalized, wording preserved

No lesson, prep, raw video, installed video, or tracker was changed during this evaluation. Only audit evidence and listening previews were created.

## Teaching comparison

RICH and TAUGHT pass teaching coverage. THIN, MISSING, and WRONG indicate inadequate explanation, omission, or a material misleading statement. Verbatim compliance is separate from conceptual coverage. All quotations below come from the primary ASR and use raw source time.

### 1 Embedding and layer updates

- **7 — RICH:** 0:00.00–0:11.82 “Every word or token you feed into an AI starts as a specific row of numbers called an embedding. But as the AI processes your message, its layers change those numbers to reflect the surrounding context.”
- **8 — THIN:** 0:00.00–0:06.58 “As an AI processes your message, its layers analyze the context and change the embedding numbers for each token.” Names embedding numbers without defining the row of numbers. Use 9’s complete opening.
- **9 — RICH:** 0:00.00–0:09.70 “Each AI token starts with a row of numbers called an embedding. As the AI processes your message, its layers change those numbers to reflect the surrounding context.”

**Best-of choice:** 9 opening, then 8 from the opening question onward.

### 2 Unmatched numbers and opening question

- **7 — TAUGHT:** 0:15.08–0:23.94 “After the layers update the numbers, they might not match the starting embedding for any known word. How does the AI still retain meaning if the numbers don't match exactly?” Paraphrases the required passages.
- **8 — RICH:** 0:07.28–0:12.70 “But those new numbers might not match the starting numbers for any token. How can they still represent meaning?”
- **9 — TAUGHT:** 0:10.64–0:16.34 “But those new numbers might not match the starting numbers for any existing token. How can they still represent meaning?” Adds existing to a locked sentence.

**Best-of choice:** 8 preserves the approved question.

### 3 Relationships explain why exact matching is unnecessary

- **7 — TAUGHT:** 0:24.66–0:36.66 “The answer is that an exact numerical match isn't necessary. The AI evaluates the relationships between the numbers, and we can visualize those relationships as a position in a mathematical space called vector space.” Nearby/similar relationship is not explicit in this opening.
- **8 — RICH:** 0:13.90–0:27.42 “An exact match isn't necessary. The relationships between the numbers matter, too. We can picture those relationships as positions on a map, where nearby positions can represent similar meanings. That's the idea behind vector space.”
- **9 — TAUGHT:** 0:17.04–0:30.16 “An exact match isn't necessary. The relationships between the numbers matter, too. We can picture those relationships as positions on a map, where nearby positions represent similar meanings. That is the core idea behind vector space.” Drops can and rewrites the vector-space sentence.

**Best-of choice:** 8 keeps the complete answer and its qualifier.

### 4 Latitude and longitude and all three city coordinates

- **7 — RICH:** 0:37.44–0:57.98 “A map uses two numbers, latitude and longitude, to build intuition for distance. Let's start with Dallas at 32.78 degrees north, 96.80 degrees west. Next, we add Mountain View at 37 degrees north, 122 degrees west. Finally, we plot New York City at 41 degrees north, 74 degrees west.”
- **8 — RICH:** 0:28.20–0:47.86 “This map uses latitude and longitude to describe position. Let's add Dallas with its coordinates 32.78 degrees north, 96.80 degrees west. Next, add Mountain View at 37 degrees north, 122 degrees west. Then New York City at 41 degrees north, 74 degrees west.”
- **9 — RICH:** 0:31.32–0:51.04 “Looking at this map, we use two numbers to describe a position. Latitude and longitude. Let's add Dallas at 32.78 degrees north, 96.80 degrees west. Next, Mountain View sits at 37 degrees north, 122 degrees west. And finally, New York City goes at 41 degrees north, 74 degrees west.”

**Best-of choice:** All teach correct coordinates. Keep 8 to preserve continuity.

### 5 First mystery city and Mountain View

- **7 — RICH:** 1:09.86–1:30.16 “Now, let's give you a new set of coordinates, 38 degrees north, 120 degrees west. These numbers don't perfectly match our existing cities. Using relative distance, which of our three established cities is closest to this new point? This map shows the new coordinate represented by a diamond, revealing Mountain View is closest, even without an exact match.”
- **8 — RICH:** 0:48.80–1:04.10 “Now you get coordinates that don't match one of our existing cities. The first is 38 degrees north, 120 degrees west. Let's add that position to the map. Which of our three cities is closest? Mountain View is closest, even without an exact match.”
- **9 — RICH:** 1:01.00–1:14.22 “Now, you receive a new set of coordinates that do not match our baseline. 38 degrees north, 120 degrees west. Which of our three cities is the closest? The diamond marks the new position, and the short connection joins it to Mountain View.”

**Best-of choice:** 8 has clear setup, question, and answer.

### 6 Second mystery city and New York City

- **7 — TAUGHT:** 1:30.96–1:38.74 “Let's try a second mystery coordinate at 40 degrees north, 76 degrees west. Checking the map, we find this point is closest to New York City.” Gives the answer without the required question.
- **8 — RICH:** 1:05.10–1:14.80 “Next, try 40 degrees north, 76 degrees west. Let's add this second diamond. Which city is closest? New York City is closest to the second point.”
- **9 — RICH:** 1:14.92–1:25.14 “Next, try a second mystery coordinate at 40 degrees north, 76 degrees west. Which city is closest this time? The new connection identifies New York City as the nearest location.”

**Best-of choice:** 8; 9 also preserves a question and answer.

### 7 No exact match conclusion and bridge to seven dimensions

- **7 — TAUGHT:** 1:39.74–1:57.06 “When exact numerical matches fail, calculating the shortest distance is a reliable mechanism for finding the closest relative match. We can transition this logic from physical geography to abstract meaning. Imagine evaluating drinks on seven specific characteristics, generating a seven-number vector for each one.” Uses abstract wording rather than the source’s concise city conclusion.
- **8 — RICH:** 1:15.54–1:43.68 “The coordinates didn't match either city exactly, but distance helped us find the closest match. By calculating distance, we can find the closest relational match, even when the new coordinates don't perfectly align with any known point on our map. A map uses two numbers to describe a position, but we can do the same with more than two numbers. Imagine a taste test, where you rate drinks on seven characteristics. We can't draw all seven dimensions, but a simplified picture shows which drinks are closest.” The extra recap at 1:21.28–1:28.60 is optional excess.
- **9 — TAUGHT:** 1:25.14–1:49.92 “Though the coordinates didn't match perfectly, distance calculations allowed us to find the closest match. A physical map uses two numbers. We can apply this exact same logic using more than two numbers. Imagine a taste test where you rate Coke, Pepsi, and hot coffee across seven characteristics – sweetness, bitterness, fizz, heat, caffeine, darkness, and citrus. These seven numbers act as abstract coordinates.” Bridge is clear, but exact city conclusion is paraphrased.

**Best-of choice:** 8, with optional removal of its redundant recap.

### 8 Simplified picture cannot draw seven dimensions

- **7 — MISSING:** Not spoken.
- **8 — RICH:** 1:39.20–1:43.68 “We can't draw all seven dimensions, but a simplified picture shows which drinks are closest.”
- **9 — WRONG:** 2:41.86–2:50.12 “While we cannot physically draw all seven dimensions on a flat screen, projecting them into neighborhoods visually proves which concepts are closest in meaning.” Acknowledges the drawing limit, then says a projection visually proves closest meaning; the source describes a simplified illustration.

**Best-of choice:** 8’s exact caveat.

### 9 Coke vector with seven named dimensions

- **7 — THIN:** 1:57.84–2:00.26 “This chart plots Coke using seven specific ratings.” No values or dimension names read.
- **8 — RICH:** 1:44.58–1:54.50 “Let's add Coke to the map. Its coordinates are Sweetness 9, Bitterness 1, Fizz 10, Heat 2, Caffeine 3, Darkness 8, and Citrus 1.”
- **9 — RICH:** 1:50.66–1:59.92 “Let's plot Coke. Its coordinates are sweetness 9, bitterness 1, fizz 10, heat 2, caffeine 3, darkness 8, and citrus 1.”

**Best-of choice:** 8; 9 is equally complete.

### 10 Pepsi vector and its relationship to Coke

- **7 — WRONG:** 2:01.22–2:07.94 “Next, we add Pepsi. Because their scores are identical, they group together in a distinct soft drinks neighborhood.” Says the scores are identical; their citrus scores differ.
- **8 — WRONG:** 1:55.20–2:10.22 “Next, add Pepsi. Its coordinates are Sweetness 9, Bitterness 1, Fizz 10, Heat 2, Caffeine 3, Darkness 8, and Citrus 1. Pepsi's scores are close to Coke's, so it sits near Coke in the soft drinks neighborhood.” Both ASR passes say citrus 1 in the base vector, then correctly say Pepsi 10 in the later comparison. Source value is 10. Direct listening still required.
- **9 — RICH:** 2:00.72–2:19.50 “Next is Pepsi. Its coordinates are sweetness 9, bitterness 1, fizz 10, heat 2, caffeine 3, darkness 8, and citrus 10. Because Pepsi's scores are very close to Coke's, it drops into the exact same area, forming a soft drinks neighborhood.” All seven values correct, including citrus 10.

**Best-of choice:** 9’s complete Pepsi introduction and coordinate sentence, then 8’s neighborhood explanation.

### 11 Hot coffee vector and separate neighborhood

- **7 — THIN:** 2:08.96–2:17.96 “Now, we plot Hot Coffee. Its ratings differ significantly from the sodas, so it lands far away, defining a separate coffee and tea neighborhood.” Neighborhood named but no values.
- **8 — RICH:** 2:11.08–2:28.80 “Now add Hot Coffee. Its coordinates are Sweetness 1, Bitterness 9, Fizz 0, Heat 9, Caffeine 8, Darkness 10, and Citrus 0. Hot Coffee's scores differ more from Coke's and Pepsi's, so it sits farther away in the coffee and tea neighborhood.”
- **9 — RICH:** 2:20.38–2:40.92 “Now consider hot coffee. Its coordinates are sweetness 1, bitterness 9, fizz 0, heat 9, caffeine 8, darkness 10, and citrus 0. These extreme differences – high bitterness and heat, zero fizz, and citrus – place it far away in its own isolated coffee and tea neighborhood.” Adds a useful high-bitterness/high-heat contrast; not needed as a graft.

**Best-of choice:** 8 is complete. 9 is richer in the trait contrast but adds no missing teaching.

### 12 Mystery Drink A and citrus gaps 1 versus 8

- **7 — THIN:** 2:19.06–2:40.10 “Let's introduce mystery drink A and its seven numbers. Notice that its first six numbers exactly match the sodas. To determine if it belongs closer to Coke or Pepsi, we check the final number, Citrus. This diagram reveals that Pepsi is the closest match. The numerical gap in that single, differing citrus dimension is the smallest.” Names the comparison but omits actual values, gaps, and the question.
- **8 — RICH:** 2:41.20–3:10.54 “Let's add Mystery Drink A. Its coordinates are Sweetness 9, Bitterness 1, Fizz 10, Heat 2, Caffeine 3, Darkness 8, and Citrus 9. Mystery Drink A is near Coke and Pepsi. Its first six numbers match both. Compare the last number, Citrus. Mystery Drink A is 9, Coke is 1, and Pepsi is 10. Which is closest? Pepsi is closest. The Citrus gap is only 1, compared with 8 for Coke.” Reads all seven named values and both numerical gaps.
- **9 — RICH:** 2:51.10–3:19.10 “This vector space diagram plots mystery drink A. Its coordinates are 9, 1, 10, 2, 3, 8, and 9. Its first six numbers match both Coke and Pepsi exactly. To find the closest match, we compare the final citrus number. Mystery drink A is 9, Coke is 1, and Pepsi is 10. Which is closest? Pepsi is the closest match. The numerical gap for citrus is only 1, compared to a distance of 8 for Coke.” Reads the full vector after establishing dimension order, but does not repeat every dimension name as requested.

**Best-of choice:** 8: complete values, comparison, question, and answer in order.

### 13 Mystery Drink B and comparison across seven dimensions

- **7 — THIN:** 2:41.04–3:00.82 “Next, we get mystery drink B. Its entirely different set of seven numbers locates it firmly in the coffee and tea neighborhood. Take a look at its numbers. Which established drink is its closest match? This updated visual shows Hot Coffee is the match. The overall similarities across all seven-dimensional ratings define its closest neighbor.” No values read.
- **8 — RICH:** 3:11.28–3:35.24 “Now add Mystery Drink B. Its coordinates are Sweetness 2, Bitterness 8, Fizz 0, Heat 8, Caffeine 7, Darkness 9, and Citrus 0. Mystery Drink B is in the coffee and tea neighborhood. Compare its seven numbers with Hot Coffee's vector. Which drink is the closest match? Hot Coffee is closest to Mystery Drink B. Its ratings are similar across all seven dimensions.”
- **9 — TAUGHT:** 3:19.98–3:40.40 “Now look at the coffee and tea neighborhood. We have mystery drink B, with scores of 2, 8, 0, 8, 7, 9, and 0. Compare those seven numbers against hot coffee's vector to find the closest match. Hot coffee is the closest match. Even though the numbers are not identical, the ratings are highly similar across all seven dimensions.” Reads every number and explains similarity, but omits the requested question and named dimension/value pairs.

**Best-of choice:** 8: complete example and all four comparison questions across the lesson.

### 14 Vector definition and distance conclusion

- **7 — TAUGHT:** 1:51.72–1:57.06 “Imagine evaluating drinks on seven specific characteristics, generating a seven-number vector for each one.” Names a seven-number vector; later distance sentence at 3:17.32–3:19.54 is a paraphrase.
- **8 — RICH:** 3:36.16–3:54.84 “Each drink's seven numbers give it a position in vector space. Comparing those numbers helps us find the closest match. Comparing multiple numbers to find the smallest gaps acts as mathematical distance, positioning each complex item accurately in vector space. This is the idea behind distance. Smaller gaps mean closer positions.” Seven numbers are explicitly placed in vector space; the extra sentence at 3:42.66–3:50.30 repeats the idea.
- **9 — THIN:** 3:41.02–3:46.86 “Comparing those numbers helps us find the closest match, because smaller numerical gaps mean closer positions.” Comparison is taught, but the seven-number vector definition/conclusion is omitted.

**Best-of choice:** 8 preserves both required conclusions. Optional trim of the inserted repeat.

### 15 Learned dimensions and return to the opening question

- **7 — TAUGHT:** 3:20.36–3:36.08 “AI scales this exact seven-dimensional logic up to thousands of dimensions, using values learned during its initial training. Because of this massive dimensional map, an updated token vector doesn't need a perfect match to function. Its new spatial position represents its meaning.” Core scale, training, and unmatched-position idea present, but exact lines absent.
- **8 — RICH:** 3:55.62–4:10.66 “AI uses this idea on a much larger scale. Its embeddings have thousands of dimensions, with values learned during training. After the layers update a token's vector, it doesn't need to match another vector exactly. Its position in vector space helps represent its meaning.”
- **9 — TAUGHT:** 3:47.98–3:56.62 “AI uses this exact distance idea, but with thousands of dimensions learned during training, meaning a token's updated vector never has to match perfectly to represent meaning.” Compresses learned dimensions and unmatched-vector meaning; approved callback absent.

**Best-of choice:** 8: complete training sentence, unmatched-vector callback, and position helps represent meaning.

### 16 CAT and IT sentence and contextual updates

- **7 — TAUGHT:** 3:42.48–4:04.84 “The cat sat on the mat during the May rainstorm because it was tired. This visual map establishes the starting position of the token, it. On its own, it could refer to many things. It begins at an arbitrary starting location with coordinates starting at 0.12, negative 0.34. As the AI layers process the sentence, they connect it to cat.” Sentence is intact; contextual information is less clearly explained.
- **8 — RICH:** 4:27.74–4:42.24 “The cat sat on the mat during the May rainstorm because it was tired. On its own, it could refer to many things. As the layers process the sentence, they update its numbers to carry information connecting it to cat.”
- **9 — TAUGHT:** 4:00.00–4:12.98 “Take the sentence, the cat sat on the mat during the May rainstorm because it was tired. On its own, the word it is completely ambiguous. As the layers process this specific sentence, they update its starting” Reads the sentence and updates, but connection explanation comes later.

**Best-of choice:** 8 explains why numbers change, not just their new location.

### 17 Starting and updated numbers and separate IT token

- **7 — WRONG:** 3:53.28–4:23.74 “It begins at an arbitrary starting location with coordinates starting at 0.12, negative 0.34. As the AI layers process the sentence, they connect it to cat. The token travels across the map, arriving at a newly updated coordinate position starting with 0.41, 0.06. It remains a completely separate token, but its new coordinate position now physically embeds its contextual connection to the cat.” Numbers correct and token stays separate, but physically embeds makes the representation literal.
- **8 — RICH:** 4:42.24–5:01.42 “Its starting position has numbers beginning 0.12 minus 0.34. The layers update the numbers to 0.41, 0.06. It remains a separate token, now near cat. Its new position reflects its connection to cat in this sentence.” Correct .12/−.34 and .41/.06; separate token and contextual relationship explicit.
- **9 — WRONG:** 4:12.98–4:37.22 “coordinates, beginning at 0.12, negative 0.34, and shift them to new coordinates, 0.41, 0.06. This physical change in the numbers moves its position in vector space. It remains a separate token, but is now near cat. Its new position reflects its connection to cat in this specific sentence.” Correct numbers and separation, but physical change is added at 4:23.50–4:27.72.

**Best-of choice:** 8 without a graft. Retain all three distinct statements: changed numbers, separate token, connection to CAT.

### 18 Exact close with no added claim afterward

- **7 — WRONG:** 4:24.68–4:36.04 “This final banner shows exactly how the system maps human language. Meaning is defined by a position in vector space, where concepts with similar meanings sit physically close to one another.” Rewrites both lines, narrates final banner, and says meanings sit physically close.
- **8 — WRONG:** 5:11.20–5:21.18 “Meaning is a position in vector space. Similar meanings usually sit close together. In AI, mathematical closeness directly equals conceptual similarity.” Both correct lines are present, followed by mathematical closeness directly equals conceptual similarity. Remove the added sentence.
- **9 — RICH:** 4:38.30–4:43.26 “Meaning is a position in vector space. Similar meanings usually sit close together.”

**Best-of choice:** 8’s own two-line close, ending after 5:16.16. No close donor needed.

## Required wording

Version 8 contains every required passage. A correct sentence does not cancel a contradiction elsewhere: its Pepsi error and added closing claim still need repair. The table is compliance evidence, not a numeric quality score. “MISSED” means not present verbatim, not necessarily missing conceptually; see the teaching comparison.

| Required passage | Version 7 | Version 8 | Version 9 |
| --- | --- | --- | --- |
| But those new numbers might not match the starting numbers for any token. | MISSED | MET 0:07.28–0:10.52 | MISSED |
| How can they still represent meaning? | MISSED | MET 0:11.28–0:12.70 | MET 0:14.92–0:16.34 |
| An exact match isn’t necessary. | MISSED | MET 0:13.90–0:15.60 | MET 0:17.04–0:18.52 |
| The relationships between the numbers matter too. | MISSED | MET 0:16.22–0:18.12 | MET 0:19.04–0:20.96 |
| We can picture those relationships as positions on a map, where nearby positions can represent similar meanings. | MISSED | MET 0:19.08–0:24.76 | MISSED |
| That’s the idea behind vector space. | MISSED | MET 0:25.64–0:27.42 | MISSED |
| The coordinates didn’t match either city exactly, but distance helped us find the closest match. | MISSED | MET 1:15.54–1:20.52 | MISSED |
| We can’t draw all seven dimensions, but a simplified picture shows which drinks are closest. | MISSED | MET 1:39.20–1:43.68 | MISSED |
| Each drink’s seven numbers give it a position in vector space. Comparing those numbers helps us find the closest match. | MISSED | MET 3:36.16–3:41.98 | MISSED |
| This is the idea behind distance: smaller gaps mean closer positions. | MISSED | MET 3:50.96–3:54.84 | MISSED |
| Its embeddings have thousands of dimensions, with values learned during training. | MISSED | MET 3:58.56–4:02.34 | MISSED |
| After the layers update a token’s vector, it doesn’t need to match another vector exactly. | MISSED | MET 4:02.96–4:07.36 | MISSED |
| Its position in vector space helps represent its meaning. | MISSED | MET 4:07.98–4:10.66 | MISSED |
| IT remains a separate token, now near CAT. | MISSED | MET 4:54.02–4:57.10 | MISSED |
| IT’s new position reflects its connection to CAT in this sentence. | MISSED | MET 4:57.98–5:01.42 | MISSED |
| Meaning is a position in vector space. | MISSED | MET 5:11.20–5:13.36 | MET 4:38.30–4:40.40 |
| Similar meanings usually sit close together. | MISSED | MET 5:14.46–5:16.16 | MET 4:41.40–4:43.26 |

Additional instructions: version 8 asks all four questions and supplies the next answer without spoken timing directions. Version 7 omits the second-city and Mystery A questions; version 9 omits the Mystery B question. Versions 8 and 9 say all seven base-drink dimension/value pairs, but version 8’s Pepsi citrus value conflicts with the source. Version 8 reads the names and values for both mysteries; version 9 reads their numbers using the previously established order. Version 8’s opening mentions embedding numbers but does not define embedding as a row of numbers; version 9 supplies that definition.

## Per candidate disposition

### Version 7

**LESSON:** vector-space. **CANDIDATE:** `Prompts/vector-space-7.mp4`. **VERDICT STATUS:** Not KEEP; reject as base. No verified repair proposed for this raw roll. A standalone replacement would require extensive repair or REROLL.

**ERRORS:** 2:02.80–2:07.94 says Coke and Pepsi’s scores are identical; the source gives citrus 1 versus 10. 3:12.94–3:13.44 transcribes as “Deliberate pacing” in both passes. 4:15.30–4:23.74 says the new coordinate physically embeds its connection. 4:29.08–4:36.04 rewrites the close and again makes proximity physical. The worked drink values and numerical gaps are missing throughout.

**ADDITIONS:** The early city-to-token comparison at 1:03.34–1:09.04 is understandable, but version 8 already carries the necessary bridge. No unique donor is needed. “Arbitrary starting location” at 3:53.28–3:59.88 is less careful than the source’s starting position.

**REPAIR PLAN:** Replacing most of the drinks, conclusions, and closing section with 8 would effectively substitute another base. Prefer 8 directly. **EDITING NOTES:** The radar chart at approximately 1:48–2:24 changes the dimensions to include Caloric and Coldness; it is not the source example. Generated city maps add cities and change displayed coordinates. Restore exact maps if any visual material is reused.

**SOURCE_QA:** PASS for the identified issues; these errors were added by the roll. **LISTENING:** ASR comparison only; no direct listening.

### Version 8

**LESSON:** vector-space. **CANDIDATE:** `Prompts/vector-space-8.mp4`. **VERDICT STATUS:** Proposed REPAIR, not yet certified; complete identified text-level plan below, with audio audition pending.

**ERRORS:** 1:57.26–2:05.12 ends the Pepsi vector with “Citrus 1,” according to both passes. At 3:00.28–3:04.48 the narrator correctly says Pepsi is 10, so the unedited recording contradicts itself. The source and displayed vector use 10. At 5:16.84–5:21.18, “In AI, mathematical closeness directly equals conceptual similarity” removes the source’s usually/can qualification and comes after the required close. Cut it.

**ADDITIONS:** Short extra recaps after the cities, neighborhoods, vector conclusion, learned-dimensions callback, and CAT example repeat ideas the source already explains. They are generally unnecessary rather than all being factual errors. Optional whole-sentence trims are listed separately from required fixes.

**REPAIR PLAN:** Use 9’s opening and Pepsi sentences, remove the extra final claim. No other donor is required. **EDITING NOTES:** Exact staged maps still need to replace premature answers and generated geography. The current context illustration replaces invented coordinates and the generated context remake. Visual repairs do not cause the narration disposition.

**SOURCE_QA:** PASS. **LISTENING:** Full independent ASR passes; raw audio clips and joined previews prepared, not auditioned.

### Version 9

**LESSON:** vector-space. **CANDIDATE:** `Prompts/vector-space-9.mp4`. **VERDICT STATUS:** Not KEEP; retain donor beats, not this base. No verified complete repair proposed for this raw roll.

**ERRORS:** 2:41.86–2:50.12 says projecting seven dimensions into neighborhoods visually proves which concepts are closest in meaning. The lesson calls it a simplified picture, not a proof. 4:23.50–4:27.72 says “This physical change in the numbers moves its position in vector space.” The source describes contextual numerical updates and their representation. Several exact conclusions are absent; the drink vector definition is thin.

**ADDITIONS:** The hot-coffee comparison explicitly names high bitterness/heat and zero fizz/citrus; this supports the source. It is richer than 8’s comparison but not necessary to repair it. The opening definition and Pepsi coordinate sentence are the useful donors.

**REPAIR PLAN:** Borrow these two complete beats for 8. Replacing 9’s multiple missing locked passages and correcting the extra claims would involve more work than repairing 8. **EDITING NOTES:** Generated base-drink scenes have useful correct values in samples; retain only if they fit the approved map treatment after motion review. City/mystery answers appear before their intended reveals, and the context image is cropped.

**SOURCE_QA:** PASS for this evaluation. **LISTENING:** Full independent ASR passes; no direct listening or motion certification.

## Proposed repair using version 8

**BASE:** version 8. **GRAFTS:** two whole narration beats from version 9. No individual word assembly, synthesized replacement, or donor from versions 4–6 is needed. All times below are raw source times; finalize cut edges at nearby silence after listening.

| Required edit | Target in version 8 | Source words and donor | Join and visual treatment |
| --- | --- | --- | --- |
| Define embedding before the opening question | Replace 0:00–0:06.58 | Version 9, 0:00–0:09.70: “Each AI token starts with a row of numbers called an embedding. As the AI processes your message, its layers change those numbers to reflect the surrounding context.” | Then 8 at 0:07.28: “But those new numbers…” Clear referent, no duplicated opening. Use an accurate supporting drawing; original 8 opening has gibberish tokens. |
| Correct Pepsi’s base vector | Replace 1:55.20–2:05.12 | Version 9, 2:00.72–2:11.86: “Next is Pepsi. Its coordinates are sweetness 9, bitterness 1, fizz 10, heat 2, caffeine 3, darkness 8, and citrus 10.” | Keep 8’s preceding complete Coke beat and following 2:05.92 neighborhood explanation. Under the full drink map; adjust reveal onset and hold length to the donor. |
| End with the approved close | Remove 5:16.84–5:21.18 and subsequent engine outro | Keep 8’s own 5:11.20–5:16.16 two-line close. | End on the canonical close board. Final tail and room tone checked in the actual build. |

Draft listening previews:

- [Opening joined to version 8’s question and answer](audio-checks/proposed-opening-join.wav)
- [Coke, corrected Pepsi, and the neighborhood explanation](audio-checks/proposed-pepsi-joins.wav)
- [Original version 8 Pepsi passage](audio-checks/8-pepsi-and-neighborhood.wav)
- [Original version 8 close and added claim](audio-checks/8-close-and-extra-claim.wav)

The joins are preliminary concatenations with source silence, not finished audio. No normalization or final crossfades were applied. Verify the wrong value directly, listen to each donor in context for voice/cadence/level continuity, and finalize breath-safe boundaries before declaring REPAIR. If the Pepsi recording actually says 10, drop that graft; both ASR passes currently support 1. These are narrow checks with identified material, not reasons to commission another full video.

### Optional tightening

The following complete added recaps can be removed without losing source teaching. These cuts are proposed, not performed or approved. Do not confuse shorter runtime with a required teaching repair.

| Raw version 8 span | Words identifying the complete beat | Reason |
| --- | --- | --- |
| 1:21.28–1:28.60 | “By calculating distance, we can find the closest relational match…” | Immediately repeats the exact city conclusion. |
| 2:29.60–2:36.90 | “Grouping objects by multiple numeric attributes…” | Restates the neighborhood explanation before introducing Mystery A. |
| 3:42.66–3:50.30 | “Comparing multiple numbers to find the smallest gaps…” | Sits between the clear vector conclusion and clear distance definition. |
| 4:11.44–4:20.74 | “Across thousands of dimensions, a token’s position holds so much relational data…” | Repeats the concise approved position/meaning callback. |
| 5:02.40–5:10.48 | “Updating a word’s coordinates based on surrounding text…” | Repeats the contextual-connection takeaway immediately before the close. |

Keep all city values, all five full drink vectors, both neighborhoods, both gap calculations, both mystery answers, training, the drawing caveat, and IT/CAT distinctions. Runtime after edits must be measured, not promised from these approximate sentence boundaries.

## Board and camera plan

The map-only progressive reveal format, four short comparison pauses, static context illustration, and canonical close are already approved in the lesson’s prep plan. The source-specific donor edits and optional cuts above are new proposals. The table below uses version 8’s unedited time; all timings must move with the audio edit.

| Board | Highlighting sequence | Camera | On screen and breaks | Reason or exception |
| --- | --- | --- | --- | --- |
| Opening supporting drawing | Row of numbers, layer updates, then nearby relationships; no answer-map board | Complete drawing | 0:00–0:27.42, adjusted to opening donor | Replace gibberish at 0:00. Potentially retain the animals/vehicles relationship sketch near 0:19–0:27 after motion review. |
| Three Cities | Empty map → Dallas → Mountain View → New York City; reveal each label and coordinate pair with its marker | Fixed full map, all three retained | Two dimensions 0:28.20; Dallas 0:32.18; Mountain View 0:38.80; NYC 0:44.16 | Prepared `cities-0` through `cities-3` replace generated geography and non-source city labels. |
| The First New Position | Diamond at 38 N/120 W; hold unanswered through question; ring and connection on “Mountain View” | Same fixed map | Point 0:52.44; question 0:59.16–1:00.38; answer 1:01.70 | Use `cities-4`, then `cities-5`. Sample at 0:52 already shows the answer; retiming is essential. |
| The Second New Position | New diamond at 40 N/76 W; keep first answer; reveal NYC connection/ring only at answer | Same fixed map | Point 1:05.10; question 1:11.08–1:11.94; answer 1:13.00; hold through conclusion at 1:20.52 | `cities-6`, then `cities-7`; generated regional map does not show the intended comparison. |
| Three Drinks | Empty neighborhoods → Coke → Pepsi → coffee, each with full vector; brief emphasis on newly narrated object | Full map; keep earlier objects and both neighborhoods visible | Bridge 1:29.62; caveat 1:39.20; Coke 1:44.58; Pepsi donor in target 1:55.20; coffee 2:11.08; neighborhood finish 2:28.80 | `drinks-0` through `drinks-3`. Generated trait scene is potentially useful but differs from approved map-only treatment; do not add it automatically. |
| Mystery Drink A | Add A and vector; first-six comparison, then citrus 9/1/10; answer ring on Pepsi | Full panel; any comparison view must retain complete vectors | Setup 2:37.66; A 2:41.20; question 3:05.08–3:05.58; answer 3:06.38; gaps finish 3:10.54 | `drinks-4` through question, then `drinks-5`. In the raw sample the Pepsi ring is already visible at 2:48. |
| Mystery Drink B | Add B with label connector; hold candidates; coffee ring only on answer | Both coffee and B readable; retain accumulated points | B 3:11.28; question 3:28.48–3:29.80; answer 3:30.50; conclusion 3:36.16–3:41.98 | `drinks-6`, then `drinks-7`. Label connector and answer connection must remain distinct. Raw ring is already visible at 3:12. |
| Distance and learned dimensions | Completed drink map for recap, then a supporting drawing for scale/callback | Readable complete scene | Distance 3:50.96; scale 3:55.62; callback through 4:10.66 | Do not hold a map through unrelated prose. Remove exact d=1536 label from a retained scale drawing; the source teaches thousands, not one fixed count. |
| How Context Changes IT’s Position | Full sentence and illustration → starting numbers → update path → updated numbers → separate IT beside CAT | Complete canonical image; both positions remain visible | Context intro 4:21.38; sentence 4:27.74; starting numbers 4:42.24; update 4:49.18; separate token 4:54.02; connection 4:57.98–5:01.42 | Replace generated remake and invented-coordinate sketch with `vector-space-meaning-map.jpg`. Keep this an explanatory illustration, not literal physical travel. |
| Meaning is a position in vector space | Canonical two-line close | Full board, standard closing motion | 5:11.20–5:16.16 plus appropriate finished hold | `vector-space-close.jpg`; cut extra sentence and engine outro. |

State PNGs are in `gemini-notebook/vector-space/reference-frames/`; current lesson data and the shared capture implementation govern any refreshed render. The implementation changed while other course work was active, so confirm the final state captures match the then-current lesson before building. No course code was changed by this review.

### Useful generated visuals and specific replacements

**Potential retain:** Version 8’s nearby animals and vehicles sketch near 0:19–0:27 explains similar items grouping. Its base-drink progression around 1:44–2:28 correctly displays the seven values in inspected full-size frames, including Pepsi citrus 10. It could be useful if a later decision favors named-value visuals, but the existing approved treatment is the lesson’s maps. Motion, label timing, and the unexplained distance label in its final coffee scene need inspection; sampled stills do not certify the animation. Version 9’s corresponding named-trait progression around 1:50–2:40 is another possible visual donor, not necessary to the recommended build.

**Content corrections:** Version 7’s radar chart changes the characteristics. Version 8’s generated geography does not faithfully represent the three-city comparison. Its context sketch around 4:58–5:02 displays 10.5/24.7 and 56.2/89.1 instead of the narrated example. Generated opening tokens in 8 contain nonsense words. Replace these specific scenes, not every drawing merely because custom assets exist.

**Reveal corrections:** The completed Mountain View, Pepsi, and coffee answer rings are visible before the corresponding version 8 questions. Use unanswered and answered map states separately. See [city samples](roll-8/details-0.jpg), [Mystery A samples](roll-8/details-2.jpg), and [Mystery B samples](roll-8/details-3.jpg).

**Standard cleanup:** Restore complete canonical boards, remove generated marks and the branded outro, keep labels readable, and use the course highlight treatment. Any final motion/branding decisions require inspection of the encoded result.

## Comparison pauses

The user-approved target is approximately 1.5–2 seconds total question-to-answer space. Proposed target below is 1.75 seconds. Existing quiet was measured with silencedetect at −35 dB, minimum 0.15 seconds; this is an acoustic estimate, not a listening judgment. [Measured intervals](roll-8/silences.json) are in raw version 8 time. Small differences from ASR word edges are expected.

| Question and following answer | Measured quiet interval | Existing quiet | Proposed total | Additional quiet |
| --- | --- | --- | --- | --- |
| “Which of our three cities is closest?” → Mountain View | 1:00.560–1:01.809 | 1.249 s | 1.750 s | 0.501 s |
| “Which city is closest?” → New York City | 1:12.103–1:13.133 | 1.029 s | 1.750 s | 0.721 s |
| “Which is closest?” → Pepsi | 3:05.772–3:06.382 | 0.610 s | 1.750 s | 1.140 s |
| “Which drink is the closest match?” → hot coffee | 3:29.927–3:30.534 | 0.607 s | 1.750 s | 1.143 s |

Hold the unanswered map through each gap and reveal the answer on the spoken name. Use matched room tone and finalize at actual audio silence after audition. Do not add a full pause on top of the existing gap, add pauses to every heading, or reuse version 6’s pause measurements. Recalculate output timestamps after the two donor edits and any optional trims.

## Build readiness

The next useful step is **audition the two prepared joins, confirm the Pepsi value, and build the targeted version 8 repair with the approved map treatment**. The review identifies existing audio for every required correction; another full generation is not currently justified. Certification still requires listening to the joins and reviewing the actual repaired candidate. No finished video has been rendered or approved by this evaluation.
