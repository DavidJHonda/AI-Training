# Layers v8 — built for owner review

Candidate: `Prompts/layers-v8.mp4` — **3:23.367**, 6101 frames, 30 fps, 1280×720.
SHA-256: `4d2581ea0c1bb01157f13fbd5a0d3406c072d91245acdb97008fab1e479990ca`.

Built after David approved the September 28 three-reroll review: “Agree. Build it please.” This is the recommended **v7 base plus roll 3's explicit bridge**, with the proposed picture treatment. Review candidate only; not published.

## What changed

- **0:45.167–0:49.733:** insert “AI does something similar. It builds meaning through repeated updates.” from `Prompts/layers-3.mp4`, source **0:55.167–0:59.733**. It follows the horse takeaway and precedes “AI doesn't read your message the way you do.” The insert is 137 frames (4.567 s); the proposal's 4.56 s was aligned to whole frames without moving either edge out of its measured silence.
- **0:31.700–0:38.133:** use roll 1's independent horse drawing, source 0:36.000–0:42.433, during the resolved horse example. Return to the complete Meaning Clicks column before the repeated-pass takeaway. The horse-board continuous hold drops from 40.13 s to 26.53 s.
- **0:45.167–0:47.533:** use roll 1's horse drawing, source 0:39.000–0:41.367, for “AI does something similar.” Cut to the retained stack illustration as “It builds meaning…” starts.
- **0:47.533–0:55.367:** show the retained layer-stack drawing for repeated updates, the human/AI distinction and introducing layers. This also covers the four old horse-board frames that would otherwise have reappeared after the audio insert.
- **0:55.367–1:04.667:** use the inspected ACTIVE DATA drawing from the current Transformer video, source **2:17.000–2:26.300**, for attention/transformation updating the numbers. Return to the original stack before the neural-network definition. All selected Transformer frames are within the illustration, not the preceding board.
- **0:07.167–0:09.333:** add the requested complete horse-sentence outline in purple, fixed 4 px at 720p. The earlier review assumed this was already in v7, but its actual manifest contained only column/banner outlines. The board opens unmarked for two seconds before this title outline; it clears before First Read.
- Preserve the remaining v7 narration, boards, highlighting, cameras, diagram breaks, late illustrations and standard close. No extra pause was added. All later material shifts by 4.567 s.

## Source and assembly record

The build does **not** re-encode the v7 MP4 as its picture/audio source. It uses v7's retained original Layers snapshot, canonical JPG board renders and assembled pre-encode PCM. Earlier raw source rolls were unavailable; the original snapshot is the published edit from which v7 was built. The preserved cat-sentence graft is already in that assembled PCM.

Source/donor hashes, exact frame mappings, camera/ring specifications, protected-file hashes and picture spans are in `edit-manifest.json`. Reproducible implementation: `scripts/video/build_layers_v8.py`; verification: `scripts/video/qa_layers_v8.py`. These scripts refuse to overwrite the review candidate.

The new spoken bridge is gain-matched by **+3.043 dB**, placing active speech within **0.189 dB** of the surrounding narration. Its peak is **−0.967 dBFS**; no new limiter was necessary. Five-ms fades meet local room tone only inside the measured silence. Original PCM is unchanged outside those two short fade windows. The base's 24 full-scale PCM samples remain 24; none was introduced by the new donor.

All 264 frames borrowed from raw roll 1 had their corner glyphs removed with the existing mask/inpaint method; no frame was declined. The selected Transformer illustration was already clean. The course video, all raw rerolls, v7, Transformer, lesson, prompt, index and canonical boards retained their hashes.

## Narration assessment

**Teaching coverage supports KEEP; direct listening remains outstanding.** This is a transcript-grounded assessment of the encoded candidate, not a whole-file acoustic or shipping sign-off. Read the fresh complete 58-segment transcript from the actual v8 file. Together with preservation of the original PCM, it supports the following:

| Essential point | Assessment and output evidence |
|---|---|
| English-class hook and full horse sentence | RICH, 0:00–0:09. |
| First Read, More Reads, Meaning Clicks | RICH, 0:10–0:38; ambiguity, competing interpretations, resolved events and roles of “raced”/“fell.” |
| Repeated passes and horse takeaway | TAUGHT, 0:38.62–0:44.54; exact “Each read updates the meaning until it clicks.” |
| Explicit horse-to-AI bridge in the required position | TAUGHT, 0:45.64–0:49.28; both new clauses, immediately followed by the human/AI distinction. |
| Layers, attention/transformation, contextual updates | TAUGHT, 0:49.92–1:04.38; original explanation preserved. Successive transfer/building on prior numbers is further explained in the diagram and Repeat stage. |
| Neural-network definition | TAUGHT, 1:05.24–1:07.86; exact whole-stack definition. |
| General numbers-in → layers → final-numbers process | RICH, 1:08.60–1:18.94. |
| Many-number qualifier and first/final pairs | RICH, 1:19.77–1:42.56; many numbers, two tracked; .42/−1.15 → .19/−1.12. |
| Numbers-board takeaway | TAUGHT, 1:43.12–1:46.38; exact attention/transformation sentence. |
| General process to one word and full cat sentence | RICH, 1:46.96–1:56.38; all cat/mat/May-rainstorm wording supplied before Start. |
| Start and starting values | RICH, 1:56.94–2:05.26; uncertainty and .12/−.34. |
| Layer 1, Layer 2, Repeat | RICH, 2:06.04–2:28.02; connection begins, information strengthens, more layers build on previous numbers. |
| Result values and referent | RICH, 2:28.74–2:36.20; .41/.06 and exact “AI works out that it refers to cat.” |
| Qualified layer scale | RICH, 2:36.98–2:46.22; companies may not disclose, published designs, dozens and sometimes over a hundred. |
| Horse callback and harder meaning | TAUGHT, 2:47.14–2:59.64; sarcasm, story twists and reasoning. |
| Compute/time versus benefit | TAUGHT, 3:00.36–3:12.06; cost and exact benefit sentence. |
| Two closing statements | TAUGHT, 3:12.90–3:18.84; both required lines, no extra spoken “Pause.” |

All ten current required spoken lines are present in the transcript. No material missing point or new factual addition was identified. Roll 3's physical-layer, internal-cat-definition and “slow” additions were not imported. Source QA: PASS for this narrow repair; no lesson/source change needed. ASR renders “raced” as “Race” in one inherited line and “reads” as “reeds” in another; these are not grounds to change unchanged source audio without listening.

## Actual board exposure and drawing breaks

| Board | Continuous board spans | Treatment |
|---|---|---|
| “The Horse Raced Past the Barn Fell” | 0:05.167–0:31.700 (**26.533 s**); 0:38.133–0:45.167 (**7.033 s**) | Full-view opening/title, complete-column camera and outlines, full-view takeaway. New horse drawing breaks the previous long hold. |
| How Layers Update the Numbers | 1:08.667–1:19.867 (**11.2 s**); 1:24.867–1:47.200 (**22.333 s**) | Compact full board; retained stack drawing in the five-second gap. Diagram, first pair, final pair and banner outlines retained. |
| How AI Connects ‘IT’ to ‘CAT’ | 1:52.567–2:19.767 (**27.2 s**); 2:27.200–2:37.033 (**9.833 s**) | Canonical uppercase board, complete sentence strip followed by each complete stage; retained stack drawing in the 7.433-second gap. |
| Meaning builds up, layer by layer. | 3:12.667–3:23.367 (**10.7 s**) | Canonical close and existing standard motion retained; literal final frame. |

Longest uninterrupted teaching-board exposure is **27.2 s**. The 26.533-, 22.333- and 27.2-second runs are disclosed longer worked-example runs under the approved treatment; camera movement is not counted as a break. No new board or filler graphic was made.

## Verification completed

- Sequentially decoded **all 6101 frames**, confirming dimensions, fps and planned duration.
- Compared **351 retained frames** against corresponding v7 frames; largest mean pixel difference **0.834/255**. Compared **102 encoded states** against render references; largest difference **3.262/255**, including JPEG reference and encode differences.
- Inspected all five encoded contact sheets across the file, the full-resolution title outline and literal final frame. Inspected every-frame strips at all new picture/audio boundaries and title-outline on/off boundaries.
- Transition guard checked **31 declared inherited/new boundaries**: 30 automatic passes. The only flag is inherited frame **302**, the smooth horse-board dive; inspected frames 290–314 and cleared it as camera motion, not an intermediate shot. Original automated FAIL remains in `guard/transition-guard.md`; `guard/manual-review.json` records the resolution instead of misrepresenting the detector output.
- Original PCM is exact outside the new join ramps; donor PCM matches the gain-adjusted selected source outside the ramps. Encoded AAC correlation to assembled PCM is **0.999969**, with **41.87 dB** SNR. These measurements verify preservation/encoding, not listening quality.
- Measured encoded bridge gaps at −35 dB: **0:44.832–0:45.736 = 0.904 s** before the new sentence and **0:49.608–0:49.999 = 0.391 s** before the returning v7 line. Both reflect retained natural margins; no added silence. The bridge's own clause gap is 0.533 s.
- Fresh full-file ASR confirms the inserted sentence and its preceding/following context. `bridge-encoded.mp3` is an excerpt from the actual output audio, covering **0:38–1:10**.
- Source/protected-file identities remained unchanged. No course deployment or Video Tracker update was performed.

## Listening still needed

No direct listening or real-time end-to-end playback was performed. Listen particularly at **0:42–0:53** for the new bridge's voice, cadence, pronunciation and joins. The inherited cat-sentence insert at **1:52.567–1:56.667** retains the previous listening limitation. Unchanged rings/cameras were checked through frame comparisons and sampled visual inspection, not freshly remeasured at every frame. This candidate is ready for owner review, not certified for publication.
