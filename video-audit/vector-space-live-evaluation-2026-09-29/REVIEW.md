# Vector Space — live evaluation, September 29, 2026

**Recommendation: keep the current version; make a targeted visual improvement if revisiting it.** The city → drink → contextual meaning progression is coherent, the numerical comparison is correct, and the ending answers the opening question. The main weakness is the long drink-board sequence. This is a transcript-and-sampled-frame evaluation, not an end-to-end audiovisual certification.

## Verified live version

The public page selects `course-assets/vector-space/vector-space.mp4?v=20260928ship1`. Fresh streaming SHA-256 matches the installed v9 exactly: `53a9bb18646f9160e91291c9957a00751edf15285fd548919c9d7a6ab7b4dd25`, 11,574,033 bytes. The September 28 record's pending-deployment note is therefore superseded by this observation. Runtime is **3:25.13**, 6,154 frames, 30 fps, 1280 × 720. The site's “3 min” follows its rounded-minute convention.

The public and local `VectorSpaceSection` are identical. All six teaching-board assets still match the v9 manifest hashes. Public video bytes were hashed without retaining another MP4. Fresh sequential decoding completed with no near-black frames. See `public-verification.json`, `board-identity.json`, and `decode.json`.

V9's compressed audio hash is identical to v8: `889c4e61c1fe094978caffb6364dd913eee07186f0bcc93bf15becc1e01758cb`. The complete v8 encoded transcript was therefore reused with evidence of audio identity, not filename inference. Inspected fresh four-second contact sheets across the entire file, selected 720p frames, and the literal final frame. The direct public MP4 rendered a city-board frame in the browser. The course UI stopped at its entry form; no registration was submitted. This does not establish embedded-player behavior or mobile usability.

## Narration review

LESSON: vector-space

CANDIDATE: verified public v9, 3:25.13

VERDICT: **KEEP within the previously approved simplified teaching scope**, provisional on listening. No new essential omission identified. The wording cautions below merit refinement, but do not justify throwing away this composite.

| Teaching point in lesson order | Assessment | Transcript evidence |
|---|---|---|
| Token begins as an embedding; layers update it for context | TAUGHT | 0:00–0:11.84: row of numbers, embedding, surrounding context. ASR's “called in embedding” is not evidence of an audible error. |
| Changed numbers might match no starting token; why can they still mean something? | RICH | 0:12.60–0:17.52 poses the actual problem. |
| Exact match unnecessary; relationships and positions convey meaning | RICH | 0:18.46–0:31.08 provides the answer and map intuition. |
| Transition into familiar coordinates | TAUGHT | 0:32.14–0:40.80 introduces a geographic map and latitude/longitude. |
| All three city coordinate pairs | RICH | 0:41.44–0:53.82: Dallas 33/97, Mountain View 37/122, New York 41/74. |
| Both new positions and nearest-city answers | RICH | 1:00.04–1:05.70: 38/120 → Mountain View; 40/76 → New York. |
| A nonmatching position still tells us something | TAUGHT | 1:06.42–1:12.20: distance finds the closest one; position tells which city is near. |
| Vector is a row; seven comparable drink characteristics | TAUGHT | 1:13.16–1:25.68 connects positional logic to drinks, defines vector, and names seven characteristics with examples. Full label recital and full-row readings are unnecessary under the approved cuts. |
| Coke/Pepsi more similar than coffee | RICH | 1:26.58–1:36.24 compares rows and states the relationship. |
| Two geographic dimensions → seven rating dimensions | RICH | 1:37.38–1:45.34 explicitly explains why the ratings specify a position. |
| Nearby soft drinks, distant coffee | TAUGHT | 1:46.08–2:04.42 explains the diagram's groups and gaps. |
| Mystery closest to Pepsi; compare matching positions | RICH | 2:05.22–2:25.96: first six match; Citrus 9 versus 10 gives 1, versus Coke's 1 gives 8. Approved removal of full-vector recitals preserved the calculation. |
| Embeddings learned in training; larger dimensionality | TAUGHT | 2:27.00–2:38.28: training and thousands of dimensions; see wording caution below. |
| Full CAT/IT sentence and ambiguity | RICH | 2:39.20–2:48.74 reads the sentence and explains IT alone is ambiguous. |
| Context changes numbers, hence position and connection to CAT | RICH | 2:49.46–3:10.08: starting values, layer updates, updated values, explicit CAT connection. |
| Return to opening question | TAUGHT | 3:10.86–3:16.52: updated numbers differ from the original; relationships matter. |
| Two-line close | TAUGHT | 3:17.24–3:21.66: both prescribed lines, including “usually.” |

HARD REQUIREMENTS: Both closing lines are verbatim in the transcript and visible in the final frame. Two earlier prompt-verbatim passages remain accepted semantic equivalents under the September 28 approval; this review does not reinstate those retired objections or the deliberately removed numeric recitals. The optional on-page 2048 activity is not presented as necessary spoken teaching.

ERRORS: No wrong city coordinate or mystery-drink arithmetic identified. “Exact mechanism” and schematic-map phrasing warrant the caution below. The 0–10 rating scale is visible but not spoken; the worked differences remain understandable without a separate scale recital.

SOURCE_QA: Worked values and relationships agree with the current page. The drink scores and maps serve as illustrative examples. No claim of empirically measured beverage properties is required for the comparison. The map is an analogy for relationships, not a literal two-dimensional plot of a model's internal state.

ADDITIONS: The geographic-map bridge and the final return to the original question improve continuity.

REPAIR PLAN: No required narration splice proposed. No donor has been auditioned for the optional wording improvement. No pause changes proposed.

LISTENING: No direct audio audition or continuous real-time viewing was performed. Voice continuity, prosody, pronunciation, audible clicks and noise-floor changes remain unassessed. Transcript coverage and audio identity do not certify these properties. Existing joins near 0:31.67, 0:35.30, 0:45.77, 0:54.33, 2:04.97, 2:08.40, 2:49.20 and 3:10.73 are useful contextual listening checkpoints.

## Highest-impact findings

1. **Drink-board pacing, 1:13.17–2:26.23.** Three consecutive boards occupy 73.07 seconds. The table alone lasts 33.07 seconds; its takeaway ring remains while the narration moves into two-versus-seven dimensions. This is the best place to improve the video. At approximately **1:37.38–1:46.23**, replace that final table stretch with a focused two-coordinate row beside a seven-rating row, using the existing dimensions and values. Keep the spoken bridge intact and cut to the existing neighborhood board at its current boundary. This would reduce the table to about 24.2 seconds and split the board chain into roughly 24.2 and 40.0 seconds. The first table hold remains an explicit pacing exception, justified by its continuous row walkthrough. This is a proposed explanatory graphic, not a verified existing donor or an authorized build.
2. **Analogy wording, 2:27–2:38.** “AI uses this exact mechanism to understand text” is stronger than the page's “AI uses this idea on a much larger scale.” The illustration supports numerical relationships; it should not imply that transformer processing is simply choosing the nearest drink/word. Prefer the page's wording in a future narration revision. Likewise retain “usually” when discussing similar meanings. Transformer attention computes weighted combinations of values using query/key relationships; it is not this particular nearest-example calculation ([original Transformer paper, §3.2](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)). Contextual representation geometry also varies across layers ([Ethayarajh, 2019](https://aclanthology.org/D19-1006/)). These sources motivate a small qualification, not a technical detour for students. The opening's “can” and closing's “usually,” plus the explicit schematic graphics, already provide context for the simplified explanation.
3. **Context-board readability, 2:49.20–3:10.73.** The main path and CAT connection are clear, but the small number plaques and “layers update” label are the weakest text at native 720p. They are much smaller than the drink values. If reframing, first test a larger view of the complete board; do not crop individual labels out of their scene. Treat a camera change as a preview decision, not a guaranteed improvement. The existing follow-up schematic at 3:10.73 makes the relationship clear and should remain.

## Board and camera recommendation

The existing board durations below come from the exact hash-matched output manifest and agree with the fresh sampled frames. Preserve approved treatment except for the optional bridge graphic. Initial unmarked full views are present in the manifest and sampled frames; exact onset verification was not repeated frame by frame.

| Board | Highlighting sequence | Camera | On screen / breaks | Recommendation |
|---|---|---|---|---|
| Three Cities, Two Coordinates Each | Dallas → Mountain View → New York | Complete full view | 0:31.67–0:54.67; 23.00 s | Keep the full map and explicit coordinate readings. Mild pacing exception; coherent walk. |
| Use the Map to Find the Closest City | Each new position paired with its nearest city → takeaway | Complete full view | 0:54.67–1:09.67; 15.00 s | Keep; paired outlines directly support the comparisons. |
| Three Drinks, Seven Dimensions Each | Whole row → Coke/Pepsi comparison → coffee → takeaway | Complete full view | 1:13.17–1:46.23; 33.07 s | Proposed graphic break for final 8.85 s at 1:37.38; retain readable full table for the row comparison. |
| A Map of Drink Similarities | Soft-drinks group → coffee group | Fixed complete-board view | 1:46.23–2:04.97; 18.73 s | Keep v9's stable framing. Do not reintroduce the push that caused the next board to jump smaller. |
| Use the Map to Find the Closest Drink | Matching rows → Citrus 9/10 → Citrus 9/1 → takeaway | Same fixed complete-board view | 2:04.97–2:26.23; 21.27 s | Keep; no extra graphic needed during the short calculation. |
| How Context Changes IT’s Position | Starting numbers → update path label → updated numbers → takeaway | Current full view; optional larger complete-board preview | 2:49.20–3:10.73; 21.53 s | Preserve the path and all neighborhoods; improve small-text legibility only if preview demonstrates it. |
| Meaning is a position in vector space. / Similar meanings usually sit close together. | Unmarked | Existing hold, push, settled hold | 3:17.13–3:25.13; 8.00 s | Keep. Literal final frame confirmed. |

Longest single teaching-board span: **33.07 s**. Longest consecutive teaching-board chain: **73.07 s**. These were disclosed in the approved v8/v9 history; they are editorial improvement opportunities rather than newly discovered release regressions.

## Supporting visuals

- 0:00–0:23.23: token-to-number schematic, changed values, and the opening problem. Keep; it explains rather than decorates.
- 0:23.23–0:31.67 and 2:26.23–2:39.37: Notebook meaning neighborhoods. Sampled stages show words becoming groups; retain provisionally for their explanatory purpose. Motion timing has not been directly assessed.
- 1:09.67–1:13.17: calculated-gap drawing, a useful short bridge out of geography. Keep.
- 2:39.37–2:49.20: IT with cat/mat/weather alternatives. Keep; it sets up the sentence's ambiguity.
- 3:10.73–3:17.13: contextual IT/CAT schematic. Keep; it returns to the initial numbers and reinforces the conclusion.

No replacement of effective animation is proposed. No stock-photo or engine-mark defect was evident in the samples; this is not an exhaustive per-frame mark audit. Existing 19-boundary transition-guard results and ring checks remain historical evidence for the hash-matched file; they were not freshly rerun or all manually inspected here. The Google Sheet Video Tracker was not accessed or changed. No video, lesson, website reference, or release commit was changed by this evaluation.
