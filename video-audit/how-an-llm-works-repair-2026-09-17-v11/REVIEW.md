# How an LLM Works — v11 narrow visual repair

Scope: implement the owner's explicit request to highlight only jelly during the 4:36 comparison. Investigate the question about available graphics for 2:21–2:46, without treating that question as selection of a replacement. No narration, timing, pause, lesson, live video, or deployment changes.

Candidate: [how-an-llm-works-v11.mp4](../../Prompts/how-an-llm-works-v11.mp4). Same 6:22.933, 1280×720, 30 fps timeline as v10. The previous candidate remains intact.

## Implemented treatment

| Board | Changed output interval | Highlight | Camera |
|---|---|---|---|
| Same Word. Different Odds. | 4:35.800–4:42.500, frames [8274,8475) | Replace the two whole-card rings with complete jelly-row rings: label, bar and percentage. Purple on both rows, matching jelly's accent. | Existing full-board comparison view, unchanged. |

Source JPG rectangles, in xyxy pixels: left jelly [62,368,756,445]; right jelly [842,671,1536,754]. Both are inside the card rails and clear of row dividers. Post-crop outlines remain 5 px. Earlier prompt/table outlines, the following takeaway banner, and every other frame treatment remain as in v10.

Rendered from the pristine source rolls and canonical canvases, not by re-encoding v10's video pictures. The delivery AAC is stream-copied directly from v10, without gain, resampling, cuts or encoding. The v10 render helper gained an optional audio-stream-copy input; its default original-build behavior is unchanged. No shared production helper was edited.

## Graphics investigation — not implemented

The board remains highlighted through approximately 2:22.67; the unmarked hold is 2:22.67–2:46.80. At that point the narration has moved from nursery-phrase examples to broader structures, explanation/problem solving/misspellings, then the fact that patterns arise during training. V10 kept the whole board unmarked because those new ideas are not specific to either illustrated phrase card. The result is a roughly 24-second inactive-looking board.

Available donor options were visually inspected at one-second intervals, with representative labels checked at full resolution:

- `Prompts/how-an-llm-works-reroll-2.mp4`, approximately 1:34–1:38: a structural/problem-solving sequence. Could cover the broader-pattern discussion, roughly output 2:23–2:35. Its wording is more technical than the narration (“Decompose Problem,” “Deduce Relations,” “Synthesize Solution”); it is an optional supporting illustration, not another spoken lesson requirement. Exclude the subsequent fabricated misspelling-percentage chart.
- `Prompts/how-the-model-learns-2.mp4`, approximately 2:45–2:49: an animated network of changing numerical values. Could support the training/patterns relationship, roughly output 2:36–2:46. The small “WEIGHT TENSOR MATRIX” label adds unspoken jargon; this is not a perfectly clean beginner visual. Exclude the later “optimized” label and biological-neuron illustration.
- Learns-2 around 2:32–2:44 also moves from a phrase to premise/evidence/conclusion, program syntax and conceptual themes. Do not drop this entire sequence in indiscriminately: its coding labels and snippet-like text add an unnecessary detour.

There is no verified clean 25-second continuous donor sequence. A two-illustration treatment could replace the hold, but would need selected source endpoints and some clean-state holds. These drawings are proposals only; the 2:21–2:46 section is unchanged in v11.

## Verification

The manifest is [edit-manifest.json](edit-manifest.json). Source, canonical asset, live file and v10 hashes are recorded there. A comparison of both manifests confirms that all visual rows, board assets, camera beats and other ring states are unchanged; only probability-board rings 7 and 8 differ.

Encoded-file results are recorded in [encoded-checks/verification.json](encoded-checks/verification.json), with the affected boundary strips in [transitions/transition-guard.md](transitions/transition-guard.md).

Final checks passed: all 11,488 frames decoded at 1280×720/30 fps, and the AAC bitstream hash is identical to v10. Both changed boundaries passed transition guard with no transient pairs or spike frames. The encoded jelly comparison, following takeaway state, final close frame, and both 25-frame boundary strips were visually inspected; the jelly rings enclose only their respective complete rows and switch cleanly to the existing takeaway treatment.

This is a narrow repair, not a new full narration evaluation. No literal listening or continuous end-to-end viewing was performed. V10's outstanding human listening review still applies, although no audio has changed here. No tracker update or publication was performed.

## Commands

```sh
.video-venv/bin/python scripts/video/prepare_how_an_llm_v11.py
.video-venv/bin/python scripts/video/build_how_an_llm_works_v11_review.py --prepare-only
.video-venv/bin/python scripts/video/build_how_an_llm_works_v11_review.py
```

The builder verifies the previous/source hashes, encodes once, checks copied audio hashes, decodes the complete output, extracts affected frames, and runs transition guard at the two changed boundaries. It refuses to overwrite an existing candidate.
