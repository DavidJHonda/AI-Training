# Vector Space — three September 28 rerolls versus the live video

**Recommendation: use Roll 3 as the narration base for an edited replacement, with selected complete example sentences from Roll 1. Keep Roll 2 only as an opening donor option. None should replace the live MP4 unchanged.**

The largest improvement is the lesson's opening argument. The live narration asks how changing numbers “preserves” the original meaning. The current lesson asks how numbers that no longer match any token's starting embedding can still represent meaning, and answers that question through relationships. Rolls 2 and 3 actually teach that question and answer. Roll 3 also explicitly connects cities to drink vectors, says embeddings are learned during training, and returns to the updated embedding at the end.

This is an evaluation and proposed edit plan, not a finished candidate or shipping approval. No live video, course page, board, upload material, or tracker was changed.

## Evidence and limits

- Read the current `VectorSpaceSection` in `index.html`, `lessons/vector-space.md`, the current generation prompt, and the repository's Narration Review and Edit Spec. Inspected all seven current JPGs; hashes are in `board-sources.json`.
- Generated and read complete fresh `small.en` transcripts with word timestamps for all four MP4s. Sequentially decoded every video and inspected 8-second contact sheets, plus 1-second samples of two possible drawing donors. This is sampled visual review, not continuous viewing.
- Cross-checked Roll 2's suspicious numbers with `medium.en` on isolated audio excerpts. Both models transcribe Dallas as **93 west** and the Citrus gap as **0.1**. The lesson says **97 west** and **1**. These are strongly supported ASR flags, not a claim of direct listening.
- **Direct listening, voice/cadence assessment, and contextual graft auditions were not performed.** Quoted speech below comes from ASR. Word times are editorial locators, not certified cut points. ASR spellings such as “Coffey” and “called in embedding” are not treated as pronunciation defects.
- The local live MP4's SHA-256 exactly matches the published-byte verification retained from September 27. This review did not fetch the remote video again. `index.html` still selects `vector-space.mp4?v=20260917ship1`.
- The Video Tracker was not accessed or changed; no workflow status is inferred.

## Sources

| Version | File | Runtime | SHA-256 |
|---|---|---:|---|
| Live | `course-assets/vector-space/vector-space.mp4` | 3:52.90 | `4873fac38f54ff14ebaff06b0787a8922e9e15bb99712b0332d767ad41f5b563` |
| Roll 1 | `Prompts/vector-space-1.mp4` | 3:49.23 | `3df4bc45f7b01223bfd7ed8892c0ddae6f68549482f705c3834a11c6984a56b5` |
| Roll 2 | `Prompts/vector-space-2.mp4` | 3:00.87 | `0b4be8e5b296653dbb313a53c41f7347d40b2544c5dc458e5a3a5625acf1012a` |
| Roll 3 | `Prompts/vector-space-3.mp4` | 3:28.00 | `6540e2fa2c8a67753efecaaf7d7a9612e82c812209141f44893ca72acf29e198` |

The September 22 reviews of filenames `vector-space-1` and `vector-space-2` describe older files. They were not reused as evidence for these new uploads.

## Per-version assessment

The teaching-point table below supplies the complete comparison for each version. Two prompt-verbatim passages are absent from every new roll; see the hard-requirements table. Under the repository's strict KEEP / REPAIR / REROLL rule, none earns KEEP, and a fully compliant REPAIR cannot yet be certified: exact donor wording for those two passages is unavailable, and joins have not been auditioned. **Strict verdict: REROLL for the unmet literal requirements. Editorial recommendation: develop the identified composite before requesting another generation, if the adequately taught paraphrases are acceptable.** This distinction prevents a promising edit from being mislabeled as an already verified repair.

**Roll 1:** Strong example donor. It speaks all three cities' coordinates, all three drink vectors, the mystery vector, and the correct Citrus calculation. Its opening incorrectly changes “might not match” into “they stop matching”; it omits learning during training; at 2:19.62 it says “Physical gaps perfectly measure these numerical differences”; at 3:05.42 it calls the process “physical movement.” It also tells the viewer to “take a moment and guess” at 2:32.94. Those are reasons not to use it as the base. Close: both exact closing lines present. Listening: transcript only.

**Roll 2:** Useful opening, weak remainder. It has the complete question and immediate answer at 0:12.04–0:31.60. Both ASR passes flag Dallas's longitude and the Citrus calculation. It never defines a vector clearly as a row of numbers, does not speak the mystery vector or Coke's gap of eight, omits learning during training, and retains “physically moves” at 2:47.32. Its short duration comes partly from omitted explanation. Close: both exact closing lines present, although its picture does not use the standard close. Listening: transcript plus independent ASR checks, no direct audition.

**Roll 3:** Best lesson arc. It preserves the complete opening, the explicit latitude/longitude-to-seven-ratings bridge, the correct Citrus comparison, learning during training, and an ending that revisits the changed embedding. Its omissions are identifiable: Mountain View/New York's original coordinates, the map's numerical rows, and the mystery vector. Its “find its identity” at 2:02.04 is stronger than finding the nearest of the three examples; replace that introduction with Roll 1's ratings introduction. At 2:55.42 it says “physical update path,” and at 3:11.28 says the schematic “perfectly represents” updated meaning. Those literal/absolute words should be removed or the sentences replaced. Close: both exact closing lines present. Listening: transcript only.

**Live:** The city answers and mystery-drink comparison remain useful. Its opening is now materially out of step with the current lesson, it omits the learned-during-training point, and it repeatedly literalizes the map. It also contains invented radar/scatter graphics and placeholder text. Repairing only its pictures would leave the opening problem unresolved. Its exact close and useful “CALCULATED GAP” drawing can be retained if helpful.

**SOURCE_QA: PASS for the worked values and comparisons against the current page and boards.** Mystery versus Pepsi is a Citrus difference of 1; versus Coke it is 8. The visual neighborhoods are schematic, not measured physical distances or an actual plot of a model's hidden states. No new source contradiction was established. This is not a general technical validation of the lesson's simplified account of representations. Keep the lesson's qualified “can” and “usually”; do not turn its map analogy into a physical mechanism.

## Teaching-point comparison and best-of choices

Times refer to each source's own timeline. Quotes are ASR excerpts; an ellipsis indicates omitted words, not an audio edit. “TAKE 3” selects the narration for a proposed composite, not its raw visuals.

| Teaching point | Live | Roll 1 | Roll 2 | Roll 3 | Best-of choice |
|---|---|---|---|---|---|
| Embedding = row; layers change numbers for context | TAUGHT 0:00–0:12, “rows of numbers…embeddings”; context explained later | TAUGHT 0:00–0:16, “alter those numbers to reflect the context” | TAUGHT 0:00–0:11, “reflect the surrounding context” | TAUGHT 0:00–0:12, “layers change those numbers” | TAKE 3 |
| Changed numbers may match no token's starting embedding | MISSING; 0:12–0:24 substitutes “hold on to the original meaning” / “preserves meaning” | WRONG qualifier 0:16.78–0:21.28, “they stop matching…any known token” | TAUGHT 0:12.04–0:15.22, exact “might not match” sentence | TAUGHT 0:12.60–0:15.72, same exact sentence | TAKE 3; 2 is a complete alternative opening |
| Question immediately answered by relationships/map/vector space | THIN 0:19–0:24, only “look at a concept called vector space” | RICH 0:21.90–0:37.98, “An exact match isn't necessary…relationships…positions on a map” | RICH 0:15.80–0:31.60, same explanation | RICH 0:16.30–0:31.08, same explanation | TAKE 3; this is the main improvement |
| Two dimensions and three city coordinates | TAUGHT concept; only Mountain View's pair spoken, 0:25.98–0:45.16 | RICH 0:38.80–0:56.46: Dallas 33/97, Mountain View 37/122, New York 41/74 | WRONG 0:41.50–0:45.98, “33…93”; other city pairs MISSING | TAUGHT two dimensions and Dallas 33/97, 0:32.26–0:45.82; other city pairs MISSING | TAKE 3 introduction/Dallas, 1's Mountain View + New York sentences |
| New positions and nearest-city answers | RICH 0:46.04–1:05.14, “first…Mountain View…second…New York City” | RICH 0:57.34–1:22.86, reads both pairs and answers explicitly | TAUGHT 1:01.42–1:18.44, both pairs and correct answers | TAUGHT 0:46.90–0:57.98, “38…120…Mountain View”; “40…76…New York” | TAKE 3; 1 is richer but repeats the two pairs |
| No exact city match still conveys position/nearby city | TAUGHT 0:57–1:12, “Neither matches exactly…distance…closest” | RICH 1:23.62–1:35.92, “relative position still tells us…which city” | TAUGHT 1:08.14–1:20.64, “Neither perfectly matches…closest match” | TAUGHT 0:58.78–1:04.44, “When nothing matches exactly…” then “which city they're near” | TAKE 3; literal required paragraph absent in all |
| Seven common characteristics; each row a vector | RICH 1:25.18–1:36.44, 0–10 scale and “entire row…called a vector” | TAUGHT 1:36.82–1:46.14, “seven characteristics…row…vector” | THIN 1:24.96–1:40.72: seven characteristics, no explicit row/vector definition | TAUGHT 1:05.46–1:17.90, “row…called a vector…seven characteristics” | TAKE 3. Live's scale explanation is an optional richer donor; no essential advantage over 3's flow |
| Compare Coke/Pepsi to coffee | RICH 1:37.24–1:50.78: sweet 9/fizz 10 versus coffee 1/0 | TAUGHT 1:47.10–1:50.56, “nearly identical…differ completely” | TAUGHT 1:30.88–1:36.64, “nearly identical…differ widely” | TAUGHT 1:18.76–1:28.62, “almost every column” and exact comparison takeaway | TAKE 3; retain its more careful wording |
| Explicit city-to-seven-dimensional-position bridge | TAUGHT 1:13.80–1:24.34, “same logic…beyond two…seven-dimensional” | TAUGHT 1:51.44–1:55.10, “seven ratings…seven-dimensional vector space” | TAUGHT 1:37.40–1:44.82, “seven ratings…position…seven-dimensional vectors” | RICH 1:29.62–1:37.62, exact “Just as latitude and longitude…” explanation | TAKE 3 |
| Neighborhoods, closer similarities, farther differences | WRONG literalization within otherwise taught comparison, 2:00.30–2:28.34, “physical position…physical distance” | WRONG overstatement 2:19.62–2:22.50, “Physical gaps perfectly measure…” | TAUGHT schematic comparison 1:41.30–1:58.52, “lines…long”; physical-gap wording needs care | TAUGHT 1:38.38–1:56.68, “numbers…right next to each other…different area” | TAKE 3; display canonical schematic |
| Read map's Coke, Pepsi, coffee vectors | MISSING complete rows | RICH 2:04.06–2:18.88, “9,1,10,2,3,8,1”; “…10”; “1,9,0,9,8,10,0” | MISSING | MISSING | TAKE 1 under neighborhood board if preserving complete upload-script numerical coverage |
| Read mystery ratings; choose nearest Pepsi | TAUGHT nearest/first-six/Citrus; full ratings MISSING 2:29.84–3:00.18 | RICH 2:23.68–2:32.10 reads 9,1,10,2,3,8,9; 2:37.62–2:40.38 “closest to Pepsi's” | THIN 1:59.46–2:06.58, no ratings; “maps right next to Pepsi” | TAUGHT answer 2:09.30–2:12.08; full ratings MISSING; “find its identity” at 2:02 is misleading | TAKE 1 introduction/ratings, then 3 answer/calculation |
| First six match; Citrus 9 vs 10 = 1, vs Coke 1 = 8 | RICH 2:41.30–3:00.18, both gaps correct | RICH 2:40.76–2:53.84, both gaps correct | WRONG 2:11.58–2:15.76, “gap of just 0.1”; Coke comparison MISSING | RICH 2:12.50–2:23.70, “gap of just one…gap is eight” | TAKE 3 |
| Compare matching dimensions; smaller gaps mean closer | RICH 3:01.26–3:05.52, “numerical gaps in matching positions” | TAUGHT through Citrus + exact takeaway 2:54.56–2:56.14 | THIN overall because example is wrong, though takeaway exact at 2:16.36 | TAUGHT through first-six/Citrus + exact takeaway 2:24.64–2:26.36 | TAKE 3 |
| Thousands of dimensions, values learned during training | THIN 3:06.68–3:13.90, thousands but learning MISSING | THIN 2:57.46–3:04.30, thousands but learning MISSING | THIN 2:19.60–2:23.68, thousands but learning MISSING | RICH 2:31.18–2:38.66, “During training, it learns embeddings with thousands of dimensions” | TAKE 3 |
| Read CAT/IT sentence and establish ambiguity | TAUGHT 3:21.38–3:29.14, sentence + “ambiguous word” | TAUGHT 3:10.38–3:18.50, full sentence + ambiguity | TAUGHT 2:26.18–2:33.90, full sentence + ambiguity | TAUGHT 2:42.04–2:49.04, full sentence + ambiguity | TAKE 3; 1's drawing is a possible picture donor |
| Layers update IT's numbers and contextual connection | WRONG physical movement 3:33.62–3:36.34; underlying link taught | TAUGHT 3:19.30–3:39.94, starting/ending example numbers and CAT link; earlier physical setup at 3:05 must be excluded | WRONG physical movement 2:47.32–2:51.94 | WRONG literal qualifier 2:55.42–3:04.00, “physical update path”; otherwise detailed numbers and CAT link | KEEP 3 after auditioning deletion of “physical”; fallback complete Roll 1 board walk |
| Return to original no-exact-match question | THIN, no explicit return | THIN, ends at CAT link | THIN, ends at CAT link | RICH structure 3:07.82–3:19.30, “no longer match the original embedding…relationship to…concepts”; remove “perfectly” overclaim | TAKE 3 after wording repair |
| Exact two-line close | TAUGHT 3:43.98–3:48.76 | TAUGHT 3:41.14–3:45.80 | TAUGHT 2:52.70–2:57.46 | TAUGHT 3:20.00–3:24.54 | TAKE 3, standard canonical close picture |

All seven dimension names and the 0–10 scale are visible in the canonical table. No new roll enumerates every dimension aloud. Live speaks the scale; the new rolls explain the common seven characteristics and use Citrus explicitly. If literal narration of every printed label is required, this remains additional source coverage to resolve; it must not be silently counted as spoken teaching.

## Current prompt's hard requirements

“Met” means present in ASR with punctuation/capitalization ignored; coffee/Coffey spelling normalized. “Paraphrase” is **missed verbatim**, even where the teaching passes. Exact audio still needs listening confirmation. The live video predates this prompt and is compared for teaching above, not retroactively scored for prompt obedience.

| Required passage | Roll 1 | Roll 2 | Roll 3 |
|---|---|---|---|
| But those new numbers might not match the starting numbers for any token. | Missed; categorical rewrite 0:16.78 | Met 0:12.04 | Met 0:12.60 |
| How can they still represent meaning? | Met 0:21.90, with “So” lead-in | Met 0:15.80 | Met 0:16.30 |
| An exact match isn't necessary. | Met 0:24.44 | Met 0:17.84 | Met 0:18.46 |
| The relationships between the numbers matter too. | Met 0:26.66 | Met 0:20.26 | Met 0:20.54 |
| We can picture those relationships as positions on a map, where nearby positions can represent similar meanings. | Met 0:28.92 | Met 0:23.36 | Met 0:23.26 |
| That's the idea behind vector space. | Met 0:36.08 | Met 0:29.82 | Met 0:29.36 |
| When nothing matches exactly, distance finds the closest one. | Met 1:23.62 | Paraphrase 1:19.32 | Met 0:58.78 |
| Those coordinates don't match any of our cities. But their position still tells us something: which city they're near. | Paraphrase 1:27.90–1:35.92 | Paraphrase across 1:08.14–1:18.44 | Compressed paraphrase 0:58.78–1:04.44 |
| Coke and Pepsi have more similar profiles than either does to coffee. | Paraphrase 1:47.10–1:50.56 | Paraphrase 1:30.88–1:36.64 | Met 1:25.58 |
| Just as latitude and longitude give a city a position, a drink's seven ratings give it a position in a space with seven dimensions. That's vector space. | Paraphrase 1:51.44 | Paraphrase 1:37.40 | Met 1:29.62–1:37.62 |
| The mystery drink's ratings are closest to Pepsi's. | Met 2:37.62 | Paraphrase 2:04.78 | Met 2:09.30 |
| Smaller gaps mean closer positions. | Met 2:54.56 | Met 2:16.36 | Met 2:24.64 |
| IT's new position reflects its connection to CAT in this sentence. | Paraphrase 3:34.62–3:39.94 | Paraphrase 2:40.34–2:51.94 | Paraphrase 3:04.72–3:07.14; omits “in this sentence” |
| Meaning is a position in vector space. | Met 3:41.14 | Met 2:52.70 | Met 3:20.00 |
| Similar meanings usually sit close together. | Met 3:43.14 | Met 2:55.82 | Met 3:22.84 |

The two universally missing exact passages are semantically taught in Roll 3. My editorial preference is to accept those paraphrases instead of generating again just for their wording. That is a proposed relaxation of the current prompt requirements, not an automatic KEEP verdict.

## Proposed narration edit

**BASE: Roll 3. Three proposed complete-beat donor insertions from Roll 1; two small wording deletions to audition. No Roll 2 audio needed unless its opening proves audibly better.**

| Target in Roll 3 | Identified source and exact words | Purpose / status |
|---|---|---|
| Replace 0:42.40–0:45.82, “New York City and Mountain View have their own coordinates…” | Roll 1, 0:48.92–0:56.46: “Mountain View is at 37 degrees north, 122 degrees west. And New York City is at 41 degrees north, 74 degrees west.” | Restores city values under Three Cities. Keep Roll 3's preceding Dallas sentence and following new-positions introduction. Whole sentences; surrounding gaps exist in ASR; joins not auditioned. |
| Insert after neighborhood explanation ending 1:56.68 | Roll 1, 2:04.06–2:18.88: “Coke is 9, 1, 10, 2, 3, 8, 1. Pepsi is 9, 1, 10, 2, 3, 8, 10. Coffee is 1, 9, 0, 9, 8, 10, 0.” | Restores upload-script map values. Keep the map visible and highlight rows as spoken. Optional compression choice: omit this addition if complete row recitation is judged unnecessary; do not claim full source coverage if omitted. |
| Replace 1:57.46–2:08.62, from “Now, we introduce…” through “far right” | Roll 1, 2:23.68–2:32.10: “Now, suppose you are given the ratings for a mystery drink. The numbers are 9, 1, 10, 2, 3, 8, 9.” | Supplies the actual vector and removes “find its identity.” Return to Roll 3's exact Pepsi answer at 2:09.30. Exclude Roll 1's next sentence, “Take a moment and guess…” |
| 2:55.42–3:04.00 context sentence | Remove “physical,” ASR locator 2:56.24–2:56.68, leaving “We trace its update path…” | Word deletion is a proposed audition, not a certified splice. Preserve the complete starting/ending values. If deletion sounds unnatural, use Roll 1's complete board walk 3:19.30–3:39.94, replacing Roll 3 2:50.04–3:07.14; inspect “neutral token” wording and avoid duplicating the CAT conclusion. |
| 3:11.28–3:19.30 return to meaning | Remove “perfectly,” ASR locator 3:13.24–3:13.82 | Keeps the useful explicit return to relationships without claiming the drawing is exact. If an invisible join is unavailable, omit this whole sentence; the opening answer and preceding CAT connection still carry the lesson, but the ending becomes less explicit. |

These are source speech extents. Final cuts must be found in actual silence/waveforms; do not cut on ASR boundaries mechanically. Approximate resulting runtime with all three additions is around **3:44**, before final silence decisions. It is not a promised encoded duration.

No new pause is proposed. Preserve natural gaps. Relevant existing Roll 3 ASR inter-speech gaps are 1.18s before cities (0:31.08→0:32.26), 1.02s before drinks (1:04.44→1:05.46), 1.08s before the AI-scale beat (2:26.36→2:27.44), 0.94s before the CAT setup (2:38.66→2:39.60), and 0.70s before the close (3:19.30→3:20.00). Target is the existing gap, **added time 0**. These are ASR gaps, not measured noise-floor silence; remeasure if a cut touches them.

## Visual findings and useful donors

**Do not retain the rerolls' generated diagrams by default.** Roll 1 invents embedding values, a reference dictionary, distance examples, a formula, and a “1,536 dimensions” label. Roll 2's opening map contains questionable geographic labeling, and its AI diagram adds “d = 4,096.” Roll 3 invents initial embedding values, a numeric mismatch collage, and “d = 1,536” at about 2:28–2:40. The absence of a narration error does not make those pictures valid.

All generated course-board views need replacement with the exact current JPGs: the raw rolls crop titles/rows and add Notebook highlights. Roll 3's ending uses the right closing text but still requires the standard closing treatment. Remove engine corner marks in production.

Two concrete drawing candidates were inspected more closely:

- **Roll 1 around 3:10–3:18:** IT with arrows to a cat, mat, and cloud. This is a useful visual for ambiguity before context resolves it, and is much clearer than the live placeholder scene. Use only the actual CAT/IT illustration; the preceding quotation-mark collage has visible art-production labels such as “cardstock” and “fineliner” and should not be carried over. Inspected 1-second samples; exact entrance/exit and full motion still need previewing.
- **Live around 1:06–1:13:** two drawn discs connected by a dashed “CALCULATED GAP” line. Useful for the distance principle or the short transition into it. Avoid extending into the invented taste-axis graphic that follows. Inspected 1-second samples; exact full-span verification still required.

Roll 1's mystery-drink question-mark drawing has production-label text and is not an approved donor as-is. Roll 3's generic word-neighborhood diagram is a possible alternative, but it is not a new explanatory illustration for each long board walk. I found **no verified clean drawing set that solves all board-hold problems**. Do not promise a fully animated replacement from these sources alone.

## Board, highlighting, and camera proposal

This is the proposed full replacement's board treatment. Timings below are **Roll 3 source windows**, with estimated added donor speech; they are not final output timestamps. Actual visual cuts and final narration assembly must govern the build. Start each board complete and unmarked; use fixed 4px outlines at 720p after camera transforms, following actual spoken onsets. Keep all numeric rows legible. Canonical board imagery, including the existing tabletop map, is preserved.

| Exact board title | Highlight sequence | Camera | Planned exposure / break | Reason or exception |
|---|---|---|---|---|
| Three Cities, Two Coordinates Each | City positions/coordinate labels as Dallas → Mountain View → New York are spoken | Full board, no cropped city labels | Source 0:32.20–0:46.93, about 14.7s + roughly 4.1s net city donor = 18.8s | Complete donor sentences replace Roll 3's vague reference |
| Use the Map to Find the Closest City | First new position with Mountain View; second with New York; banner at takeaway | Full view | Source 0:46.93–1:05.43, about 18.5s | City pair remains a roughly 37s board chain |
| Three Drinks, Seven Dimensions Each | Whole table introduction; Coke/Pepsi comparison; coffee row; comparison banner | Full table; no dive cropping header or rows | Source 1:05.43–1:38.50, about 33.1s | Long-hold exception still unresolved: narration actively explains the rows and seven-dimension analogy; no verified relevant drink drawing available |
| A Map of Drink Similarities | Coke/Pepsi group versus coffee; then complete score rows during Roll 1 readings | Full map | Source 1:38.50–1:57.63, about 19.1s + roughly 14.8s if full rows added | About 34s if complete row reading retained; longer board chain is a real cost of restoring numerical coverage |
| Use the Map to Find the Closest Drink | Mystery row; first-six match; compare Citrus 9 with Pepsi 10, then Coke 1; Pepsi answer/banner | Full view; retain every compared value | Source 1:57.63–2:27.23, about 29.6s, shortened by roughly 2.7s with donor introduction | Roughly 27s worked example. A short live “CALCULATED GAP” insert can support “Smaller gaps…” at 2:24.64, but does not by itself solve the prior long chain |
| How Context Changes IT's Position | Starting IT/numbers → update path → ending IT/numbers beside CAT → takeaway | Full board; no zoom cutting off start/end or neighborhoods | Raw source 2:39.73–3:20.00, about 40.3s. Proposed Roll 1 IT illustration under sentence/ambiguity at roughly 2:39.60–2:49.04, then board for about 31s | Donor makes the opening clearer and shortens the hold; remaining board duration is still an explicit exception pending an additional useful drawing |
| Meaning is a position in vector space. / Similar meanings usually sit close together. | Standard close, no teaching rings | Standard restrained closing motion | 3:20.00–3:28.00 source, about 8s including end hold | Preserve both exact spoken lines and end on the canonical close |

Roll 3's raw continuous course-board chain is approximately **1:55** (0:32.20–2:27.23), counting zooms/highlights as the same board exposure. Restoring the city and vector values makes that chain longer. It exceeds the Edit Spec's roughly 60-second trigger. The table and context board also exceed the roughly 20-second trigger individually. This is not a solved pacing plan; these exceptions or additional verified picture treatments must be settled before presenting a candidate as production-ready.

The live comparison's existing board timings remain in the September 27 report. Its principal verified visual defects are still at about 1:51–2:00 (radar), 2:20–2:30 (scatter), and 3:01–3:26 (invented vector walls and placeholder sentence). Keeping the live edit and only grafting Roll 3's opening would be a smaller improvement, but would leave those defects and several weaker explanations in place.

## Practical decision

Choose **Roll 3 plus Roll 1's example details**, retain the canonical boards, and use the CAT/IT drawing for the sentence setup. Resolve the two literal-line exceptions and audition the small wording repairs before calling the composite KEEP. No new generation is needed merely to replace bad graphics. A further targeted generation is warranted only if exact omitted wording remains mandatory, the donor voice joins fail, or additional compliant explanatory drawings are desired.

The local duration label is still “3 min” for the 3:52.90 live file. A future approved replacement should set the label from its final runtime.

Evidence: each source directory here contains `source.json`, `transcript.txt`, `transcript.json`, and contact sheets. `number-crosscheck.txt` records the second ASR pass. `roll1-context-drawing/` and `live-gap-drawing/` contain the additional donor samples. `current-boards.jpg` and `board-sources.json` record this review's board inspection.
