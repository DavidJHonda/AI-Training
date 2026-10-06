# Vector Space video comparison

**Version 6 is the strongest teaching base. Version 4 is the best numerical donor. Version 5 has the best opening but compresses the examples too much to carry the lesson. None is ready to use unchanged.**

The recommendation is to retain version 6 and the useful donor passages, then obtain corrected narration for the remaining gaps before the final map edit. Replacing the pictures alone will not fix the spoken physical-movement claims. Version 6 also contains four instances transcribed as “Brief pause,” confirmed by a second local ASR pass.

| Candidate | Runtime | Best use | Narration verdict under the course rules |
| --- | --- | --- | --- |
| 4 | 4:24 | Complete base-drink vectors, citrus arithmetic, distance conclusion, clean CAT connection sentence | **REROLL** — missing required wording and distinctions; no complete verified repair from these three files |
| 5 | 3:33 | Opening through 0:31.52 | **REROLL** — thin numerical teaching, unsupported claims, missing required wording |
| 6 | 5:00 | Main teaching sequence, especially both mystery drinks | **REROLL** — strongest repair candidate, but remaining audio gaps prevent a verified REPAIR verdict |

Here REROLL is the course’s formal narration status, not a recommendation to discard all existing footage. An edited combination is promising, but the available donors do not supply every missing explanation or locked sentence. No edits, new generation, installation, or tracker updates have been made.

## Review evidence and limits

Compared the complete transcripts against the live Vector Space section and interaction data in `index.html`, `lessons/vector-space.md`, and the current prep prompt and storyboard. Source filenames, durations, and SHA-256 hashes are in [sources.json](sources.json). Full timestamped transcripts are in [version 4](transcripts/vector-space-4.txt), [version 5](transcripts/vector-space-5.txt), and [version 6](transcripts/vector-space-6.txt).

**Listening:** This is a transcript and sampled-frame evaluation, not an end-to-end listening or motion review. Local small.en ASR covered every file; independent base.en checks covered version 6 and selected material claims in 4 and 5. Audio delivery, pronunciation, edit boundaries, and donor joins remain unauditioned. Do not interpret quoted ASR as a claim of direct listening. “Koch” in version 4 is retained in quoted transcript evidence; it is not sufficient evidence of a pronunciation error.

Visual sampling used sequential decoding at 12-second intervals, with two-second samples around selected reveals. These establish incorrect values, crops, and premature answers in the inspected frames; they do not certify transition quality or animation timing between samples. The formal narration verdicts remain separate from visual defects.

## Teaching comparison in lesson order

RICH and TAUGHT pass concept coverage. THIN means insufficient explanation; MISSING means no spoken explanation; WRONG identifies a substantive misleading claim. Verbatim compliance is checked separately below.

### 1 Embedding and layer updates

| Version | Evidence |
| --- | --- |
| 4 | **THIN** — 0:00.00–0:10.86 “In artificial intelligence, every token starts as a specific row of numbers, but as the neural network layers process your message, those numbers are continuously updated.” Explains the numbers and updates, but never names embedding. |
| 5 | **RICH** — 0:00.00–0:10.08 “Each token starts with a row of numbers, called an embedding. As an AI processes your message, the layers constantly change those numbers to reflect the context.” |
| 6 | **RICH** — 0:00.00–0:11.10 “Every token an AI processes starts as a row of numbers, known as an embedding. As the AI reads your message, its layers update and change those numbers to reflect the surrounding context.” |

**Best-of choice:** 5: concise definition and reason for updates.

### 2 No exact token match and the opening question

| Version | Evidence |
| --- | --- |
| 4 | **TAUGHT** — 0:18.44–0:24.08 “But those new numbers might not match the starting numbers for any token. How can they still represent meaning?” The preceding 0:11.74 claim unnecessarily makes nonmatching inevitable. |
| 5 | **RICH** — 0:10.78–0:16.28 “But those new numbers might not match the starting numbers for any token. How can they still represent meaning?” |
| 6 | **TAUGHT** — 0:14.32–0:24.06 “By the time the layers finish processing, those new numbers might not exactly match the starting numbers for any individual token in the system. How can they still represent meaning?” |

**Best-of choice:** 5: direct question without the extra restart.

### 3 Relationships and nearby positions explain the answer

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 0:24.90–0:39.02 “An exact match isn't necessary. The relationships between the numbers matter too. We can picture those relationships as positions on a map, where nearby positions can represent similar meanings. That's the idea behind vector space.” Later contradicted by the physical-distance addition at 0:46.64. |
| 5 | **RICH** — 0:17.18–0:31.52 “An exact match isn't necessary. The relationships between the numbers matter, too. We can picture those relationships as positions on a map, where nearby positions can represent similar meanings. That's the idea behind vector space.” Stop before the unsupported entirely-by-neighbors claim. |
| 6 | **TAUGHT** — 0:24.88–0:41.14 “The answer is that an exact match isn't necessary. The relationships between the numbers matter too. We can picture those numerical relationships as positions on a physical map, where nearby positions represent similar meanings. That is the foundational idea behind vector space.” Drops the source qualifier can before represent similar meanings. |

**Best-of choice:** 5: strongest complete opening; 4 also preserves the required answer.

### 4 Two city dimensions and all three city coordinates

| Version | Evidence |
| --- | --- |
| 4 | **TAUGHT** — 0:53.90–1:14.62 “This map uses two numbers to describe a position. Let's place three anchor cities. First, Dallas at 32.78 degrees north, 96.80 degrees west. Next, Mountain View at 37 degrees north, 122 degrees west. Then, New York City at 41 degrees north, 74 degrees west.” Correct numbers; does not name latitude and longitude. |
| 5 | **RICH** — 0:38.74–0:58.82 “A standard map uses two numbers for a position, latitude and longitude. Let's add Dallas to the map at 32.78 degrees north, 96.80 degrees west. Next, add Mountain View at 37 north, 122 west. Then, plot New York City at 41 north, 74 west.” |
| 6 | **RICH** — 0:42.14–1:01.86 “This map shows how we use two numbers, latitude and longitude, to describe a position. We can precisely place Dallas at 32.78 degrees north, 96.80 degrees west. Mountain View sits at 37 degrees north, 122 degrees west, and New York City at 41 degrees north, 74 degrees west.” |

**Best-of choice:** 5 and 6: named dimensions and correct values.

### 5 First mystery city and Mountain View match

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 1:15.34–1:27.56 “Now we receive a new coordinate that doesn't match our existing data. 38 degrees north, 120 degrees west. Look closely at the map. Which of our three anchor cities is closest? Mountain View is the closest match.” |
| 5 | **RICH** — 1:05.58–1:24.58 “Now, suppose you receive new coordinates. 38 degrees north, 120 degrees west. Let's mark this unknown position with a diamond. Which of our three established cities is closest? Mountain View is closest. The coordinates do not match exactly, but calculating distance easily identifies the nearest city.” |
| 6 | **RICH** — 1:02.80–1:20.04 “Now, suppose you are given a new mystery coordinate, 38 degrees north, 120 degrees west. That specific location doesn't match any of our three existing cities. Based on the grid, which of our three cities is closest? Brief pause. Mountain View is the closest match.” Both ASR passes include the spoken stage direction Brief pause. |

**Best-of choice:** 6 is a usable teaching base once the stage direction is removed; 5 has the cleanest unedited wording.

### 6 Second mystery city and New York City match

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 1:28.28–1:36.14 “Let's plot a second set of numbers. 40 degrees north, 76 degrees west. Which city is closest this time? New York City is the match.” |
| 5 | **RICH** — 1:25.66–1:36.32 “Let's try a second unknown position at 40 degrees north, 76 degrees west. Looking at this second diamond, which city is closest now? New York City is the closest match.” |
| 6 | **RICH** — 1:20.78–1:31.92 “Let's plot a second set of coordinates. 40 degrees north, 76 degrees west. Which city is closest to this new point? Brief pause. New York City is the closest fit.” Spoken Brief pause interrupts this question too. |

**Best-of choice:** All three teach the correct match; 6 needs the audio cleanup.

### 7 City conclusion and bridge to more dimensions

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 1:36.66–1:48.54 “The coordinates didn't match either city exactly, but distance helped us find the closest match. Spatial proximity overrides the need for an exact mathematical match. This same logic applies to abstract traits.” The first sentence is the clean donor; trim the jargon after it. |
| 5 | **TAUGHT** — 1:37.84–1:47.56 “Distance measurements overcome the lack of an exact coordinate match. Calculating the distance between points allows the system to find the closest match, even when the raw data is imprecise.” Imprecise data is a distracting substitution for nonmatching coordinates. |
| 6 | **RICH** — 1:32.70–1:44.62 “These new coordinates didn't match perfectly, but calculating physical distance on the map helped us find the closest answer. We can apply that exact same logic to represent more abstract concepts by using more than two numbers.” |

**Best-of choice:** 4 for the exact conclusion; 6 for the bridge.

### 8 Seven characteristics and a vector as coordinates

| Version | Evidence |
| --- | --- |
| 4 | **TAUGHT** — 1:49.14–2:00.78 “Imagine rating drinks across seven characteristics. Sweetness, bitterness, fizz, heat, caffeine, darkness, and citrus. Each drink gets a seven number coordinate on this vector space map.” Names all seven in order; calls the list a vector later. |
| 5 | **THIN** — 1:48.34–1:55.10 “This diagram maps drinks on seven flavor characteristics. Let's start with Coke's seven numbers for sweetness and fizz.” Only sweetness and fizz are named here; the seven-number row is not defined as a vector. |
| 6 | **RICH** — 2:30.94–2:39.32 “These seven numbers form a vector. That vector acts as a coordinate, plotting the item into a specific semantic neighborhood based entirely on its traits.” The definition is clear, although semantic is unnecessary jargon. Names all seven dimensions with Mystery A at 2:50.82. |

**Best-of choice:** 6 defines vector best; 4 introduces all seven characteristics earlier.

### 9 Simplified drawing cannot display all seven dimensions

| Version | Evidence |
| --- | --- |
| 4 | **MISSING** — Not spoken. |
| 5 | **MISSING** — Not spoken. |
| 6 | **MISSING** — Not spoken. |

**Best-of choice:** No complete donor identified. Add this explanation to revised narration so viewers do not mistake the picture for an exact seven-dimensional map.

### 10 Coke and Pepsi values and their shared neighborhood

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 2:01.66–2:19.10 “Koch's coordinates are 9, 1, 10, 2, 3, 8, and 1. Pepsi scores 9, 1, 10, 2, 3, 8, and 10. With identical first six scores, they sit next to each other in the soft drinks neighborhood.” Complete vectors, with named dimension order immediately before. Koch is ASR spelling, not a diagnosed pronunciation error. |
| 5 | **THIN** — 1:55.98–2:00.44 “Pepsi's numbers are nearly identical, so it plots right next to it in a soft drinks neighborhood.” States similarity but gives no complete example vector. |
| 6 | **TAUGHT** — 1:55.66–2:15.22 “Coke has seven specific coordinates, including a sweetness of 9, a fizz of 10, and a citrus score of 1. Pepsi has nearly identical scores, landing at a sweetness of 9, a fizz of 10, and a citrus score of 10. Because their overall scores align so closely, they sit side by side in a soft drinks neighborhood.” Explains selected values and proximity; omits four scores for each base drink, despite the prep request to name dimensions with values. |

**Best-of choice:** 4 supplies the complete numerical example; 6 explains the neighborhood naturally.

### 11 Hot coffee values and the farther neighborhood

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 2:20.04–2:34.44 “Now check hot coffee. Its vector is 1, 9, 0, 9, 8, 10, and 0. These values differ drastically from the soft drinks, pushing it far away into an isolated coffee and tea neighborhood.” Complete seven-number vector. |
| 5 | **THIN** — 2:01.44–2:06.04 “Hot coffee scores differ significantly, plotting far away in a coffee and tea neighborhood.” Names the neighborhood without concrete scores. |
| 6 | **TAUGHT** — 2:16.32–2:29.92 “Hot coffee, however, has completely different coordinates. It scores a 1 for sweetness, a 9 for bitterness, and an 8 for caffeine. Those drastically different numbers push it far away into a distinct coffee and tea neighborhood.” Three useful named scores; not all seven. |

**Best-of choice:** 4 supplies all values; 6 makes the contrast understandable.

### 12 Mystery A vector and citrus comparison

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 2:35.20–2:56.28 “Now we introduce mystery drink A. Its coordinates are 9, 1, 10, 2, 3, 8, and 9. The first six match Koch and Pepsi. Compare the final citrus number, 9, against Koch's 1 and Pepsi's 10. Pepsi is the closest. The gap is only one point compared to 8 for Koch.” All seven values, plus explicit gaps 1 and 8; no question before the answer. |
| 5 | **TAUGHT** — 2:15.44–2:32.44 “Let's introduce Mystery Drink A. Its first six numbers match the sodas perfectly. We compare the seventh number, citrus. Pepsi is the closest match. Mystery Drink A's citrus score is 9. The mathematical gap to Pepsi's 10 is much smaller than Coke's 1.” The numerical reason reaches the listener, but the answer precedes it and no comparison question is asked. |
| 6 | **RICH** — 2:48.70–3:21.26 “Here is mystery drink A. Its coordinates are sweetness 9, bitterness 1, fizz 10, heat 2, caffeine 3, darkness 8, and citrus 9. The first six numbers identically match both Coke and Pepsi. To find the closest match, compare the seventh dimension, citrus. Mystery drink A scores a 9, Coke is a 1, and Pepsi is a 10. Which is the closer fit? Brief pause. Pepsi is the closest match, with a gap of only 1 on that final dimension.” All seven named dimensions, comparison, question, answer. States gap 1 but leaves gap 8 implicit; includes Brief pause. |

**Best-of choice:** 6 for the sequence; 4 for the complete answer comparing gaps 1 and 8.

### 13 Mystery B vector and hot coffee comparison

| Version | Evidence |
| --- | --- |
| 4 | **TAUGHT** — 2:56.94–3:11.08 “Next, we map mystery drink B with a completely different vector. 2, 8, 0, 8, 7, 9, and 0. Looking across all seven dimensions, which drink is the closest match? Hot coffee.” Reads the vector and asks for an all-dimension comparison, but gives only the name as its answer. |
| 5 | **THIN** — 2:33.10–2:46.06 “Now let's plot Mystery Drink B. Compare all seven of its numbers against our established drinks. Which one is the closest neighbor? Hot coffee is the match. The numerical ratings are similar across all seven dimensions.” Explains overall similarity but never supplies B’s values. |
| 6 | **RICH** — 3:22.36–3:48.62 “Now we test a second vector. Mystery drink B has coordinates of sweetness 2, bitterness 8, fizz 0, heat 8, caffeine 7, darkness 9, and citrus 0. Based on the data, which drink is closest? Brief pause. Hot coffee is the answer. Its ratings are similar across all seven dimensions, demonstrating that we can find the right match without needing any individual number to align perfectly.” Full named vector and explanation. Brief pause needs removal. Not needing any exact individual value is a general statement; B actually shares two zeros with coffee. |

**Best-of choice:** 6: most complete spoken worked example.

### 14 Distance conclusion after the examples

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 3:11.62–3:22.44 “Each drink's seven numbers gives it a position in vector space. Comparing those numbers helps us find the closest match. This is the idea behind distance. Smaller gaps mean closer positions.” Best explicit vector-space conclusion; ASR consistently gives numbers gives instead of numbers give. |
| 5 | **TAUGHT** — 2:46.78–2:53.90 “Comparing numbers across multiple dimensions finds the closest match. Smaller numerical gaps always mean closer spatial positions.” Replaces the source wording with a more absolute always claim. |
| 6 | **TAUGHT** — 3:49.62–3:55.80 “Comparing numbers across multiple dimensions helps us locate the correct match, because smaller gaps always mean closer positions.” Conveys comparison but uses always and omits the requested vector-space conclusion. |

**Best-of choice:** 4: strongest conclusion; its grammar still needs listening verification and correction if confirmed.

### 15 Thousands of dimensions and values learned during training

| Version | Evidence |
| --- | --- |
| 4 | **THIN** — 3:23.30–3:28.18 “AI systems scale this up to thousands of dimensions, but the underlying mechanics are exactly the same.” Scale is taught; learned values and training are absent. |
| 5 | **THIN** — 2:54.82–2:58.90 “Real AI scales this logic up, using thousands of dimensions to represent meaning.” Scale is taught; learned values and training are absent. |
| 6 | **TAUGHT** — 3:56.56–4:01.14 “An AI model uses this exact principle, but scaled up to thousands of learned dimensions.” Learned dimensions preserves the core learning distinction, but does not explicitly say values learned during training. |

**Best-of choice:** 6 is closest. Restore the source’s training sentence in revised narration.

### 16 Return to the unmatched vector and meaning

| Version | Evidence |
| --- | --- |
| 4 | **THIN** — 4:16.28–4:18.06 “Meaning is a position in vector space.” Only the closing slogan; no distinct pre-context callback. |
| 5 | **WRONG** — 0:32.30–0:37.52 “The system defines meaning as a relative position within a space, determined entirely by its neighbors.” The addition says meaning is determined entirely by neighbors. |
| 6 | **TAUGHT** — 4:01.64–4:05.54 “A token's position in that massive vector space is what actually represents its meaning.” Connects position to meaning, but loses the cautious helps and the approved exact sentence. |

**Best-of choice:** 6 has the callback; none supplies the exact approved line.

### 17 Full CAT and IT sentence and why context matters

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 3:34.42–3:43.68 “The cat sat on the mat during the May rainstorm because it was tired. Out of context, it could refer to the mat, the storm, or the cat.” |
| 5 | **TAUGHT** — 3:04.42–3:13.52 “The cat sat on the mat during the May rainstorm because it was tired. On its own, the ambiguous token IT starts resting at specific numerical coordinates.” |
| 6 | **RICH** — 4:13.44–4:26.04 “The cat sat on the mat during the May rainstorm because it was tired. On its own, the token IT is completely ambiguous. As the AI layers process the sentence, they update the embedding for IT.” |

**Best-of choice:** 4 and 6 retain the teaching example; 6 connects it clearly to layer updates.

### 18 Starting and updated IT numbers represent context

| Version | Evidence |
| --- | --- |
| 4 | **WRONG** — 3:44.38–4:15.52 “Notice its starting position, with coordinates beginning in 0.12, negative 0.34, grouped separately from the animals. As the neural layers process the specific context, they continuously update the token's numbers. The coordinates shift to 0.41, 0.06, physically dragging the token across the vector space map. Its new position reflects its connection to cat in this sentence. By mathematically moving closer to the cat token, it successfully acquires its contextual meaning.” Correct start/end values are undermined by physically dragging and acquiring meaning by moving closer. |
| 5 | **WRONG** — 3:14.28–3:24.62 “As AI layers process the sentence, they actively update the numbers for IT, forcing it to physically move through vector space. Its new position reflects its connection to cat.” Physically move is misleading; start/end numbers are not read. |
| 6 | **WRONG** — 4:26.60–4:50.94 “The token begins at coordinates starting with 0.12 and negative 0.34. But the math shifts those numbers, moving the token across the space to a new location starting with 0.41 and 0.06. By changing those numbers, the layers ensure the token carries specific information, connecting it to cat. Its new physical position directly reflects its contextual relationship in the sentence.” Correct numbers and a good explanation at 4:39.84–4:45.98, then new physical position. Earlier physical claim at 4:05.54 too. |

**Best-of choice:** 6 for numbers and the information-carrying explanation; 4 at 4:06.14–4:09.92 for the clean final connection sentence.

### 19 IT remains a separate token near CAT

| Version | Evidence |
| --- | --- |
| 4 | **MISSING** — Not spoken. Connection wording is present but this distinction is not explicit. |
| 5 | **MISSING** — Not spoken. |
| 6 | **MISSING** — Not spoken. |

**Best-of choice:** No explicit donor identified. Preserve this distinction in revised narration and the complete context illustration.

### 20 Both closing lines

| Version | Evidence |
| --- | --- |
| 4 | **RICH** — 4:16.28–4:20.48 “Meaning is a position in vector space. Similar meanings usually sit close together.” |
| 5 | **RICH** — 3:25.46–3:29.64 “Meaning is a position in vector space. Similar meanings usually sit close together.” |
| 6 | **RICH** — 4:51.94–4:56.68 “Meaning is a position in vector space. Similar meanings usually sit close together.” |

**Best-of choice:** All three meet the spoken close. Replace the generated ending with the canonical board during editing.

## Required wording

The prep prompt locks these passages. Punctuation and capitalization differences are ignored; an added introduction is acceptable when the complete required sentence is present. A paraphrase may teach the concept and still miss the required wording.

| Required passage | Version 4 | Version 5 | Version 6 |
| --- | --- | --- | --- |
| “But those new numbers might not match the starting numbers for any token.” | MET 0:18.44–0:21.88 | MET 0:10.78–0:14.32 | MISSED 0:14.32–0:21.66, rewritten |
| “How can they still represent meaning?” | MET 0:22.60–0:24.08 | MET 0:14.92–0:16.28 | MET 0:22.44–0:24.06 |
| “An exact match isn’t necessary.” | MET 0:24.90–0:26.56 | MET 0:17.18–0:19.00 | MET within 0:24.88–0:27.94, prefixed “The answer is that” |
| “The relationships between the numbers matter too.” | MET 0:27.02–0:29.50 | MET 0:19.62–0:21.90 | MET 0:27.94–0:30.80 |
| “We can picture those relationships as positions on a map, where nearby positions can represent similar meanings.” | MET 0:30.24–0:36.46 | MET 0:22.80–0:28.76 | MISSED 0:31.60–0:37.98, modified and can omitted |
| “That’s the idea behind vector space.” | MET 0:37.20–0:39.02 | MET 0:28.76–0:31.52 | MISSED 0:38.56–0:41.14, modified |
| “The coordinates didn’t match either city exactly, but distance helped us find the closest match.” | MET 1:36.66–1:41.56 | MISSED 1:37.84–1:47.56, different wording | MISSED 1:32.70–1:38.46, different wording |
| “Each drink’s seven numbers give it a position in vector space. Comparing those numbers helps us find the closest match.” | MISSED provisionally 3:11.62–3:17.98: two ASR passes say gives; listen before treating this as a confirmed one-word error | MISSED; no complete line | MISSED; no complete line |
| “This is the idea behind distance: smaller gaps mean closer positions.” | MET 3:18.68–3:22.44; spoken as two sentences | MISSED 2:46.78–2:53.90, different wording | MISSED 3:49.62–3:55.80, different wording |
| “Its position in vector space helps represent its meaning.” | MISSED | MISSED | MISSED 4:01.64–4:05.54, stronger different wording |
| “IT’s new position reflects its connection to CAT in this sentence.” | MET 4:06.14–4:09.92; ASR renders homophone Its | MISSED 3:22.12–3:24.62, ends at cat | MISSED 4:46.66–4:50.94, physical/contextual relationship rewrite |
| “Meaning is a position in vector space.” | MET 4:16.28–4:18.06 | MET 3:25.46–3:27.22 | MET 4:51.94–4:54.10 |
| “Similar meanings usually sit close together.” | MET 4:18.96–4:20.48 | MET 3:28.08–3:29.64 | MET 4:55.02–4:56.68 |

Other prep requirements: version 4 omits the word embedding. Versions 4 and 5 omit the Mystery A comparison question. Version 6 supplies all four questions but reads the pause directions. Version 4 reads all three base-drink vectors following a dimension list; version 6 reads selected base-drink values, then names every dimension with both mysteries; version 5 never teaches a complete seven-number worked example. All three violate the no-literal-movement instruction. None explicitly explains the limitation of the simplified seven-dimensional drawing or that IT remains a separate token. Version 6 uses the discouraged word semantic at 2:33.30.

## Per version findings

### Version 4

**LESSON:** vector-space. **CANDIDATE:** `Prompts/vector-space-4.mp4` (4:24). **VERDICT:** REROLL. Teaching points and required lines are evaluated above.

**ERRORS:** At 0:46.64–0:53.24, “physical distance between numbers” is presented as how the system finds a token’s meaning. At 4:02.90–4:05.58, the token is “physically dragging” across the map. At 4:10.50–4:15.52, moving closer to CAT is described as how it acquires contextual meaning. The lesson instead says layer updates carry contextual information and the illustrated new position reflects that connection. The 0:11.74–0:17.70 claim makes an inevitable outcome out of the lesson’s might.

**ADDITIONS:** The cartographer analogy and “spatial proximity overrides” language add length without making the lesson easier for its audience. The complete citrus gap comparison is useful and follows the source.

**REPAIR PLAN:** Proposed opening donor: version 5 at 0:00–0:31.52, replacing version 4 at 0:00–0:53.24. A clean context sentence exists in this candidate at 4:06.14–4:09.92. Cutting the physical clause and the following acquiring-meaning sentence would leave correct numbers and the connection, subject to audition. These fixes do not fill all missing explanations or the approved meaning callback, so they do not establish REPAIR.

**EDITING NOTES:** City and drink reference boards show completed information too early in sampled frames. Use the approved staged maps. Retain only verified useful supporting drawings. The useful opening token drawing is a provisional visual donor, not motion-approved.

**SOURCE_QA:** PASS for this comparison; the identified physical-movement assertions were added by the roll and are not in the source. **LISTENING:** Not directly auditioned; full ASR and selected independent cross-checks only.

### Version 5

**LESSON:** vector-space. **CANDIDATE:** `Prompts/vector-space-5.mp4` (3:33). **VERDICT:** REROLL. Teaching points and required lines are evaluated above.

**ERRORS:** At 0:32.30–0:37.52, meaning is “determined entirely by its neighbors,” overstating the analogy. At 1:41.48–1:47.56, the lesson’s nonmatching point becomes “imprecise” raw data. At 3:19.22–3:21.42, the token is forced to “physically move through vector space.”

**ADDITIONS:** The opening through 0:31.52 is a useful concise rendering of the source. “Seven numbers for sweetness and fizz” at 1:52.50–1:55.10 obscures the other characteristics instead of explaining them.

**REPAIR PLAN:** Retain the opening as a potential donor, stopping before the unsupported neighbors sentence. Versions 4 and 6 supply much richer worked examples, but replacing most of the rest would defeat the point of choosing 5 as the base. Missing exact wording remains unresolved in the available files.

**EDITING NOTES:** The shorter runtime comes partly from missing teaching, not just efficiency. Premature answer rings and crops still need correction. A relational sketch around 0:32–0:38 could potentially support different audio, but its associated narration must not stay.

**SOURCE_QA:** PASS for this comparison. **LISTENING:** Not directly auditioned; full ASR and selected independent cross-checks only.

### Version 6

**LESSON:** vector-space. **CANDIDATE:** `Prompts/vector-space-6.mp4` (5:00). **VERDICT:** REROLL under the current locked requirements; retain as the strongest base for a corrected composite. Teaching points and required lines are evaluated above.

**ERRORS:** “Context physically changes a token’s position” at 4:05.54–4:11.00 and “new physical position” at 4:46.66–4:50.94 turn a representation into literal motion. Both ASR passes also transcribe “Brief pause” at about 1:17, 1:29, 3:16, and 3:38. These are production directions, not lesson content.

**ADDITIONS:** All seven dimensions are paired with values for both mysteries. The Mystery A comparison comes before the question, which supports the intended reveal. The later explanation that layer updates make IT carry information connecting it to CAT is useful and should remain. “Mathematical problem,” “semantic neighborhood,” and “based entirely” are unnecessary elaborations.

**REPAIR PLAN:** See the proposed composite below. Identified donors resolve several issues, but no available roll supplies the exact approved position/meaning callback, the simplified-drawing caveat, or the explicit separate-token distinction. The vector-conclusion donor also needs a word-level listening check. Complete and verified repair is therefore not established.

**EDITING NOTES:** Replace the invented drink-number table, answer-revealing boards, inconsistent dimension-count drawing, and cropped context illustration. These are concrete teaching defects, not simply a preference for custom assets.

**SOURCE_QA:** PASS for this comparison. **LISTENING:** Complete small.en and base.en transcripts agree on the stage directions and physical wording. No direct listening, motion audition, or joined-audio verification.

## Proposed composite and remaining narration

**BASE:** `Prompts/vector-space-6.mp4`, for its lesson order, explanations of both mystery drinks, correct named values, and contextual-information explanation. This is a proposal, not an assembled or approved edit.

| Change | Raw version 6 target | Identified existing donor and exact spoken beat | Status |
| --- | --- | --- | --- |
| Concise opening | 0:00–0:41.14 | Version 5, 0:00–0:31.52; complete opening from “Each token starts with a row of numbers, called an embedding” through “That’s the idea behind vector space.” | Best donor; stop before 0:32.30. Join to the city introduction not auditioned |
| Exact city conclusion | 1:32.70–1:38.46 | Version 4, 1:36.66–1:41.56: “The coordinates didn’t match either city exactly, but distance helped us find the closest match.” | Retain version 6 bridge at 1:39.14; join not auditioned |
| Explain both citrus gaps | 3:17.88–3:21.26 | Version 4, 2:51.98–2:56.28: “Pepsi is the closest. The gap is only one point compared to 8 for [Coke].” | Whole answer beat; ASR spells Koch; pronunciation and join unverified |
| Exact distance explanation | 3:49.62–3:55.80 | Version 4, 3:18.68–3:22.44: “This is the idea behind distance. Smaller gaps mean closer positions.” | Join to scale explanation not auditioned |
| Remove literal-motion introduction | 4:05.54–4:11.00 | Cut this whole sentence; proceed from a corrected meaning callback to “Consider the sentence” at 4:11.84 | Needs the missing callback first |
| Clean contextual conclusion | 4:46.66–4:50.94 | Version 4, 4:06.14–4:09.92: “IT’s new position reflects its connection to CAT in this sentence.” | Follows version 6’s information-carrying explanation; join not auditioned |

**GRAFTS:** Five proposed complete beats, all under course-controlled visuals. No donor splice is verified. Do not splice individual words merely to reconstruct locked sentences.

Optional richer material: version 4 at 1:49.14–2:34.44 introduces all dimensions and reads every base vector. This is more complete numerically than version 6’s base-drink sequence, but less natural than pairing each label with its value. Do not automatically graft the entire passage; revised narration using the prepared source would better match the requested presentation.

A new or corrected narration pass still needs to supply these complete ideas:

- “We can’t draw all seven dimensions, but a simplified picture shows which drinks are closest.”
- Complete dimension/value pairs for Coke, Pepsi, and hot coffee, using the unchanged source data. Keep version 6’s complete mystery examples.
- “Each drink’s seven numbers give it a position in vector space. Comparing those numbers helps us find the closest match.” Version 4 is nearly a donor, but the apparent gives needs direct confirmation.
- “Its embeddings have thousands of dimensions, with values learned during training.”
- “After the layers update a token’s vector, it doesn’t need to match another vector exactly. Its position in vector space helps represent its meaning.” This explicitly reconnects the lesson to its opening question.
- “IT remains a separate token, now near CAT.” Preserve the source’s meaning as representation; no physical movement or nearest-word lookup claims.

Retain the two closing lines unchanged. Stage directions must not appear in spoken narration. No new lesson source edits are needed for these corrections; the current upload source already contains these explanations.

## Proposed visual treatment

The map-only format, accumulated points, short comparison pauses, restored static context illustration, and canonical close were already approved in the prep discussion. The source-timed plan below is provisional because corrected narration will change the timeline. Times refer to unedited version 6.

| Raw source span and cue | Board and highlight sequence | Camera and reason |
| --- | --- | --- |
| 0:00–0:41, opening | Supporting token and changing-number drawing; preserve the complete question and answer. Avoid new readable example vectors | Retain useful generated drawings where accurate; motion review pending. If using version 5 audio, retime the drawing to that full beat |
| 0:42.14, two dimensions | `cities-0.png` | Full map, fixed camera |
| 0:47.46 Dallas; 0:53.38 Mountain View; later New York clause before 1:01.86 | `cities-1`, `cities-2`, `cities-3`; reveal marker, label, coordinates together | Same framing. Final NYC onset needs a word-level timing check |
| 1:02.80 new coordinate; 1:13.34 question; 1:18.70 answer | `cities-4` through question; `cities-5` at Mountain View answer | All three cities remain visible. No answer ring before the answer |
| 1:20.78 setup; 1:22.54 second coordinates; 1:30.48 answer | `cities-6`, then `cities-7` at New York City | Hold complete map through the city conclusion |
| 1:39.14 bridge; 1:45.46 taste test | `drinks-0` | Full panel with both neighborhoods. Narration supplies instructions |
| 1:55.66 Coke; 2:02.94 Pepsi; 2:16.32 coffee | `drinks-1`, `drinks-2`, `drinks-3` | Reveal each complete label/vector/point. No card text, buttons, or vector-order key |
| 2:40.20–2:47.92 new-item setup | Hold `drinks-3` | Replace the unrelated generated P/Coke example; do not introduce a second numeric story |
| 2:48.70 Mystery A through 3:15.36 question | `drinks-4`; highlight first six entries together, then citrus 9, 1, 10 as narrated | Full panel preferred. Any closer view must preserve complete labels/vectors and both soda candidates. Replace the 3:02–3:04 invented-value table |
| 3:17.88 Pepsi answer | `drinks-5`, ring and short match line; emphasize citrus values | Reveal on spoken Pepsi. Optional correct citrus number line only after the question; see retention notes |
| 3:22.36 setup, 3:24.62 B values, 3:35.18 question | `drinks-6` | Keep coffee and B vectors complete, along with accumulated points. B label connector is not an answer line |
| 3:39.64 coffee answer through distance recap | `drinks-7`, ring and short match line | Hold the completed map. Do not show coffee ring early |
| 3:56.56 scale and meaning callback | Supporting drawing indicating many dimensions without an invented fixed count | Replace the sampled 4:00 graphic with conflicting 1502/1536 counts |
| 4:13.44 sentence; 4:18.14 context | Canonical `vector-space-meaning-map.jpg`; complete sentence and diagram | Full image, no crop that hides either IT position |
| 4:26.60 starting numbers; 4:30.86 update; 4:39.84 connection | Highlight starting coordinate group, purple path, updated coordinate group, then IT and CAT | Keep the complete illustration visible. Do not animate physical token travel or merge IT into CAT; intermediate dots do not specify a number of layers |
| 4:51.94 close | Canonical `vector-space-close.jpg`, both lines | Complete uncropped board; remove generated branding/outro after the final line |

All staged PNGs are under `gemini-notebook/vector-space/reference-frames/`; exact values and state definitions are in `reveal-cues.json`. Preserve the course palette and existing board geometry rather than introducing arbitrary new highlights.

### Visual evidence and graphics worth retaining

- **Content correction:** In version 6 around 3:02–3:04, the table displays first-six values 0.82, 0.45, −0.12, 0.99, −0.34, 0.55 and seventh values 0.10, −0.22, −0.88. These contradict the taste-test vectors being explained. The evidence is visible in [the reveal sheet](roll-6/reveals-1.jpg).
- **Reveal correction:** At 1:04 the Mountain View ring is already visible, before the 1:13–1:16 question. At 2:50 the Pepsi ring is visible, before the 3:14–3:15 question. At 3:37 the coffee ring appears during the B question. The prepared states solve the specific answer leak while preserving the lesson’s map design.
- **Content correction:** The generated scale graphic sampled around 4:00 combines “Learned Dimensions: 1502” with “1,536 dimensions.” Neither exact count belongs in this lesson. Keep the general scale idea without these labels.
- **Potential keep:** Version 6’s citrus number line around 3:15–3:23 correctly contrasts Coke 1, Mystery A 9, Pepsi 10, with gaps 8 and 1. It could be a useful short inset after the answer if it does not interrupt the approved map sequence. Still-frame evidence only; inspect motion and narrated timing before choosing it.
- **Potential keep:** Version 6’s hot-coffee trait drawing around 2:19–2:25 and B’s characteristic bars around 3:23–3:35 reinforce correct named values. The approved map-only treatment already carries these beats, so retaining either would be optional, not required replacement work.
- **Potential keep:** Version 4’s opening token drawing around 0:00–0:06 explains an embedding visually. Version 5’s relational sketch around 0:32–0:38 may support correct relationship audio, but its original entirely-by-neighbors narration must be removed. Both require motion inspection.
- **Standard cleanup:** Canonical closing board, removal of generated marks/outro, and readable complete-board framing. These are separate from factual corrections.

## Question pauses

Do not add a fresh two-second pause on top of existing silence. Version 6 already has enough quiet time around each spoken direction. Automated silence detection used −35 dB and a 0.15-second minimum; figures below are measured low-energy intervals, not an auditory judgment. Detailed results are in `roll-6/silences.json`. Boundaries need listening before an edit.

| Question and answer | Candidate spoken-direction interval in raw source | Existing quiet before plus after the direction | Desired final quiet | Added silence |
| --- | --- | --- | --- | --- |
| “Which of our three cities is closest?” 1:13.34–1:15.98 → Mountain View 1:18.70 | 1:17.065–1:17.553 | 0.805 + 1.040 = **1.845 s** | About 1.5–2 s | **0 s** if existing quiet is retained |
| “Which city is closest to this new point?” 1:26.34–1:28.00 → NYC 1:30.48 | 1:28.936–1:29.436 | 0.893 + 0.985 = **1.878 s** | About 1.5–2 s | **0 s** |
| “Which is the closer fit?” 3:14.52–3:15.36 → Pepsi 3:17.88 | 3:16.287–3:16.835 | 0.871 + 0.883 = **1.754 s** | About 1.5–2 s | **0 s** |
| “Based on the data, which drink is closest?” 3:35.18–3:37.06 → coffee 3:39.64 | 3:38.182–3:38.687 | 0.886 + 0.890 = **1.776 s** | About 1.5–2 s | **0 s** |

Remove each spoken direction after auditioning its edges, preserve room tone, and align the answer ring with the answer onset. Recalculate pauses and all visual cue times after any donor grafts. No audio cuts or pause insertions have been executed.
