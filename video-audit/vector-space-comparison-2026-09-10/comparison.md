# Vector Space: two-roll evaluation

Date: 2026-09-10. Decision: **use Version 1 as the repair base**. This is a narration-intake and visual-repair assessment, not a finished-video ship certification. No video, lesson, prompt, or live registry was modified.

## Evidence and scope

- Version 1: `Prompts/vector-space-1.mp4`, 3:50.033.
- Version 2: `Prompts/vector-space-2.mp4`, 3:43.233.
- Source hashes and exact durations: `sources.json`.
- Both complete timestamped small.en transcripts reviewed; all ten 4-second contact sheets reviewed. Manual section allocations, detector scene lists, and narration-paired holds are saved per version.
- Selected full-resolution frames at Version 1 2:08 and 2:44 inspected for numerical/visual contradictions. Sampled blank or partly drawn animation frames were not classified as broken graphics. Board zooms/pans were not treated as missing content merely because one sample cropped it.
- Current source: `lessons/vector-space.md` and `VectorSpaceSection` in `index.html`. Current illustration assets were identified from the live component. The source taste table was viewed directly.
- This is transcript-based narration assessment plus sampled visual review. Continuous audio listening, delivery/prosody certification, and every-frame edit-boundary checks were not performed. Exact proposed audio cuts remain subject to listening and splice checks during a build.

## Why Version 1 wins

1. **0:00–0:24:** establishes embeddings, changing numbers, and the question the lesson answers. Version 2 spends the same opening duration on an itinerary, with neither the embedding definition nor the motivating question.
2. **0:44–0:59:** reads both new coordinate pairs. Version 2 discusses new coordinates generically.
3. **1:19–1:25:** explicitly calls the row of seven numbers a vector. Version 2 uses vector terminology later without this clear definition.
4. **2:10–2:48:** reads the mystery vector, compares matching positions, and explains the decisive Citrus gap: 1 to Pepsi, 8 to Coke. This is the strongest passage in either roll. Version 2 asks viewers to pause at 2:26 but then only announces Pepsi at 2:39–2:42. It does not work through the difference.
5. **2:58–3:10:** reads the complete CAT/IT sentence. Version 2 says only “a sentence involving a cat” at 3:18–3:21. That does not supply enough context to teach the reference.
6. **2:49–2:58:** explicitly bridges seven dimensions to thousands in AI. Version 2 only says “massive high-dimensional semantic space.”

Version 1 is seven seconds longer, with considerably more essential explanation. There is no reason to impose a major runtime reduction. Preserve its city-to-drinks-to-context progression.

## Version 1: narration corrections

| Source time | Finding | Proposed treatment |
|---|---|---|
| 0:32–0:43 | The city coordinates are rounded, but the narration calls coordinates “exact” and “precise.” | Small wording repair: these two numbers describe a position; city values are approximate. Avoid adding a geography detour. |
| 0:54–0:59 | “Which city they belong to” confuses closest-city comparison with identification. | Change to “which of these three cities is closest.” Neither roll narrates the two actual city answers; naming Mountain View and New York City would complete the example. |
| 1:26–1:32 | Coke and Pepsi's named scores are described as “almost identical,” although those selected columns match exactly. | Prefer “the same”; preserve the useful contrast with coffee. Minor precision, not a reason to reject the roll. |
| 2:00–2:09 | “Physical location is a direct expression of statistical similarity” and automatic clustering turn the useful map analogy into a universal rule. | These two sentences can be removed together. The preceding neighborhood explanation already teaches the point, and the next sentence introduces the mystery drink coherently. |
| 3:23–3:35 | “Parking it ... right next to cat” followed by “The model determines context through this movement” presents the illustration too literally and suggests the movement is the mechanism that discovers context. | Keep the preceding explanation that layers update the numbers using surrounding context. Prefer a replacement explaining that changed numbers change the position and reflect IT's connection to CAT. Version 2 3:34.66–3:39.70 supplies: “The layers update the numbers. Its new position reflects its connection to cat in this sentence.” Review a coherent graft, not merely a visual swap. |
| 3:44.82–3:46.58 | “Similar meanings will always sit close together.” | Must restore the approved “Similar meanings usually sit close together.” A visual caption cannot correct the spoken absolute. No exact donor line was found in Version 2. |

A brief reminder that AI learns its embedding values is absent from both rolls (lesson line 133); it is a minor gap that can fit naturally in the scale bridge if new narration is being recorded. Do not use this to justify an additional tutorial or large rewrite.

## Version 2: useful material and weaknesses

Useful possible donors:

- **0:12–0:18 visuals:** lively map/compass and drink illustrations, without replacing lesson teaching. Could be repurposed only where they fit Version 1's narration.
- **1:44–1:55 narration:** explains that we cannot draw seven dimensions but can compare the numbers. Useful if a repaired sequence needs that clarification, but it is not missing enough from Version 1 to require a graft by default.
- **3:34.66–3:39.70 narration:** the clean closing connection quoted above.

Important weaknesses:

- **0:54–1:03:** says simple coordinate subtraction “definitively proves” closest geographic locations. Differences must be combined using an appropriate distance measure; raw latitude/longitude differences are not a universal physical-distance calculation. This should not be a donor passage.
- **1:30–1:34:** “Across all seven dimensions ... nearly identical” obscures the deliberately large Citrus difference (1 versus 10).
- **2:26–2:35:** asks students to pause and compare, while the visible mystery-drink board already gives the answer. The stronger teaching is Version 1's worked explanation.
- **2:53–2:59:** generic AI scale bridge misses “thousands.”
- **2:59–3:33:** explains changing coordinates without reading the sentence, uses “physically moves,” and again literalizes the map. Do not transplant this whole passage.
- No complete approved closing message.

## Visual repair plan: preserve useful Notebook graphics

Do not replace every Notebook scene with course boards. Use the current board only over the exact table/map teaching that benefits from it; retain accurate generated diagrams and transitions.

Version 1 repairs:

- **0:25–0:59:** use current city boards when their coordinates are being taught. Restore complete board framing and native outline-only emphasis. Show the specific city/point as spoken.
- **1:10–1:33:** replace the generated/reproduced taste board with the exact current asset. The raw table at 1:12–1:32 alters coffee values: its Heat is 8 and Caffeine 9, whereas the source is Heat 9 and Caffeine 8.
- **1:33–1:42:** seven-spoke illustration may be retained as an illustrative transition; it is not a literal projection of seven independent axes onto a page.
- **1:42–2:00:** current drink-neighborhood board with complete active areas, preserving the comparison.
- **2:00–2:10:** generated clustering graphic separates Cola and Pepsi widely on Sweetness and puts Coffee between them. That contradicts the preceding lesson comparison. Removing the redundant narration above also removes this scene without losing teaching.
- **2:10–2:38:** preserve the full numerical walkthrough with the current closest-drink board. No need to shorten the 1-versus-8 explanation.
- **2:38–2:49:** generated “Conceptual Distance & Vector Gaps” changes Sweet/Fizz values (Pepsi 8/9, mystery 7/8, Coke 9/8). This contradicts the just-spoken matching first six dimensions. It must be replaced or corrected. Use the existing lesson map with precise Citrus emphasis, or repair a simple Notebook-style numerical diagram rather than inventing a new lesson board.
- **2:49–2:58:** retain usable high-dimensional Notebook illustration if detailed labels remain legible and accurate at delivery size.
- **2:58–3:07:** narration says the sentence is “mapped out here,” but the tabletop board does not display it. Show the existing on-page sentence treatment while the complete sentence is read, then reveal the illustration.
- **3:07 onward:** retain the existing tabletop illustration for the specific starting-number, layer-change, and CAT connection spans. Do not create unrelated new scenes merely to add motion. Notebook's alternate sentence at about 3:36–3:41 (“The CAT rested because IT was comfortable”) should be reconciled to the same example if that graphic is used.
- Restore native outline-only board emphasis; remove generated fill highlights during repair, not as a reason to reject narration.
- Insert the actual standard close and remove the Notebook outro. Final narration must agree with “usually.”

## Technical guardrail

The lesson deliberately uses a spatial analogy. Its teaching note (MD line 155) says movement does not mean the model identifies meaning by looking up the nearest original token embedding. That distinction should survive the video repair without adding a long caveat to student-facing narration.

Primary research confirms that contextual representations vary across contexts/layers and are poorly summarized by a static word embedding: [Ethayarajh, 2019, How Contextual are Contextualized Word Representations?](https://aclanthology.org/D19-1006/). This supports preserving context-dependent numbers rather than presenting one fixed semantic address as a universal decoder. The critique of literal nearest-token lookup is an architectural interpretation, not a direct quotation from this paper.

## Decision

**Version 1: KEEP AND REPAIR. Version 2: selective donor, not the base.**

The highest-value work is localized narration correction and selective visual repair, while preserving Version 1's full explanation. Neither raw file is approved to ship as-is. No finished-video score or passed audio-integrity gate is claimed by this intake report.
