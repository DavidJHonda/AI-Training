# How an LLM Works — v12 graphics insert

Scope: approved narrow visual repair following the owner's “yes” to the two-drawing treatment for the long patterns-board hold. No narration, pacing, duration, lesson, publication or deployment changes. Retain v11's jelly-only comparison rings.

Candidate: [how-an-llm-works-v12.mp4](../../Prompts/how-an-llm-works-v12.mp4), 1280×720, 30 fps, planned 11,488 frames / 6:22.933. Previous versions and raw generations remain intact.

## Treatment

| Board / drawing | Output span | Highlighting and camera |
|---|---|---|
| How AI Learns Patterns | Existing opening through 2:25.567 | Exact canonical board, previous full-view card rings unchanged. Keep the examples visible for “Simple phrases like these make the concept visible.” |
| Structural Sequence Mapping — Notebook drawing | 2:25.567–2:35.833 | Full-frame problem-solving diagram as narration broadens to complex structures and solving problems. Keep the small animated traveling dot; stop before the engine's full-row wash. No new rings or camera moves. |
| Internal numerical network — Notebook drawing | 2:35.833–2:46.800 | Full-frame network with changing values during the reminder that patterns form during training. Stop before “optimized” appears. No new rings or camera moves. |

The existing learning-to-answering handoff resumes at 2:46.800, unchanged. Output frames [4367,5004) are the only changed visual interval.

### Exact donor spans

- `Prompts/how-an-llm-works-reroll-2.mp4`: source frames [2840,2890), **1:34.667–1:36.333**. Quarter-speed adjacent-frame blending extends the brief dot animation to 6.533 seconds, then the last selected frame holds for approximately 3.733 seconds. This excludes the later full-row wash, argument chart and invented misspelling percentages.
- `Prompts/how-the-model-learns-2.mp4`: source frames [4950,5089), **2:45.000–2:49.633**. Half-speed adjacent-frame blending extends the numerical animation to 9.200 seconds, then the last selected frame holds for approximately 1.767 seconds. This excludes preceding programming syntax, the subsequent “optimized” label, and biological-neuron illustration.

Both scenes are supporting illustrations, not new teaching requirements. Their more technical labels (“Decompose Problem,” “Deduce Relations,” “Synthesize Solution,” and the small “WEIGHT TENSOR MATRIX” caption) are retained as disclosed in the approved proposal. No new audio tries to teach this terminology. Donor audio is not used. No photographs are introduced. The engine corner mark is cleaned before retiming, using the established same-frame paper-clone/glyph-mask method.

The longest unchanged board run remains the 90.633-second probability comparison, retained under the previous approval. Existing Notebook spans outside this repair are preserved exactly in the manifest timeline.

## Sources and preservation

The [edit manifest](edit-manifest.json) records source/asset hashes, exact half-open spans, retiming, original audio metadata, and all unchanged board specs. Visuals are rebuilt from pristine raw sources and canonical JPG canvases in one delivery encode. The delivery AAC is stream-copied from v11, not re-encoded. The builder asserts that all board assets, rings, camera beats, and unaffected timeline rows match v11.

`index.html` advanced independently since v11; its current lesson was reread, and all lesson Markdown, canonical board and raw-source hashes still match v11. The current page hash is protected for this build. No other task's edits are reverted or incorporated as additional video changes.

## Verification

**Rejected intermediate, not for review or shipping.** All 11,488 frames decoded, copied AAC matched v11 bit-for-bit, and the three automated transition checks passed. However, full-resolution inspection of encoded frame 4675 revealed faint labels from the preceding donor scene behind the incoming numerical network. The contact sheets and automated checks did not reveal this sufficiently. V13 corrects the numerical source in-point to frame 4980 (2:46.000) and retimes that clean span to the same output interval. V12 is preserved, not overwritten. The problem-solving insert and jelly highlights passed the inspected visual checks.

This is not a new narration verdict or shipping approval. No literal listening or continuous end-to-end viewing is claimed. V10's outstanding human listening check remains applicable; this repair changes no audio or audio joins. No tracker update, lesson edit or deployment was performed.

## Reproduction

```sh
.video-venv/bin/python scripts/video/prepare_how_an_llm_v12.py
.video-venv/bin/python scripts/video/build_how_an_llm_works_v12_review.py --prepare-only
.video-venv/bin/python scripts/video/build_how_an_llm_works_v12_review.py
```

The builder refuses to overwrite a candidate, verifies the previous and source identities, copies the AAC stream, decodes the finished file, saves affected frames, and runs transition guard at output frames 4367, 4675 and 5004. No shared production helper was changed for v12.
