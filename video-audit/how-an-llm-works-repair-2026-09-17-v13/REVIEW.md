# How an LLM Works — v13 approved graphics insert — SHIPPED 2026-09-17

Scope: narrow visual repair approved by the owner's “yes” to the two-drawing treatment for the long patterns-board hold. No narration, duration, pause, lesson, publication or deployment changes. Retain v11's jelly-only comparison rings.

Candidate: [how-an-llm-works-v13.mp4](../../Prompts/how-an-llm-works-v13.mp4), 1280×720, 30 fps, 11,488 frames / 6:22.933. Earlier candidates and raw sources remain intact. V12 was an internal QA rejection: its network entrance retained faint labels from the preceding source scene. V13 starts that donor later, on a fully clean state.

## Approved treatment

| Board / drawing | Output span | Highlighting and camera |
|---|---|---|
| How AI Learns Patterns | Existing opening through 2:25.567 | Canonical full-view board and earlier rings unchanged. Examples remain visible for “Simple phrases like these make the concept visible.” |
| Structural Sequence Mapping — Notebook drawing | 2:25.567–2:35.833 | Full-frame problem-solving illustration under broader structures/explanation/problem-solving narration. Retain the traveling dot, stop before the engine's full-row wash. No added camera movement or new rings. |
| Numerical network — Notebook drawing | 2:35.833–2:46.800 | Full-frame changing internal numbers under the reminder that patterns form during training. No programming labels at the entrance, no later “optimized” label. No added camera movement or new rings. |

Only output frames **[4367,5004)** change. The prior learning-to-answering handoff resumes at 2:46.800. V11's jelly-row highlights at 4:35.800–4:42.500 remain unchanged.

### Exact sources

- `Prompts/how-an-llm-works-reroll-2.mp4`: frames **[2840,2890)**, **1:34.667–1:36.333**. Quarter-speed linear adjacent-frame blending gives 6.533 seconds of animation, followed by approximately 3.733 seconds holding the last selected state. Excludes the later full-row wash, argument chart and invented misspelling percentages.
- `Prompts/how-the-model-learns-2.mp4`: frames **[4980,5089)**, **2:46.000–2:49.633**. One-third-speed linear adjacent-frame blending gives 10.800 seconds of animation, followed by approximately 0.167 seconds holding the final selected state. Excludes earlier programming text, “optimized,” and the biological-neuron drawing.

No donor audio is used. No photographs, new boards or new teaching requirements are introduced. As disclosed in the approved proposal, the drawings contain more technical labels than the narration: “Decompose Problem,” “Deduce Relations,” “Synthesize Solution,” and the small “WEIGHT TENSOR MATRIX” caption. They serve as supporting illustrations, not a separately taught procedure. The engine corner mark is cleaned before retiming, with the established same-frame method.

### Complete Notebook visual inventory

All previously approved drawing spans outside this repair are unchanged. Exact source frames and identities are in the manifest.

| Output seconds | Drawing |
|---|---|
| 0.000–8.467 | Peanut butter opening |
| 46.667–52.100 | Training loop introduction |
| 101.500–110.500 | Training repetition |
| 145.567–155.833 | New problem-solving insert |
| 155.833–166.800 | New internal-number insert |
| 166.800–173.200 | Learning-to-answering handoff |
| 186.000–190.233 | Incremental pieces |
| 190.233–199.400 | Whole words and fragments |
| 290.033–301.300 | Prediction loop / phone analogy |
| 339.567–358.867 | Repeated prediction loop |
| 358.867–373.333 | Training versus answering |

The longest unbroken board run is still the previously approved 90.633-second probability comparison. It is outside this narrow repair.

## Preservation and verification

The [edit manifest](edit-manifest.json) records sources, hashes, source/output spans, retiming, and every board/camera/ring specification. The builder asserts that all board specs and all unaffected timeline rows match v11. Pristine raw sources and canonical JPG canvases are assembled in one delivery encode; v11's AAC stream is copied without resampling, gain, fades, cutting or encoding.

`index.html` advanced independently since v11. Its current lesson was reread; the Markdown, canonical assets and prior raw-source hashes still match v11. Today's page hash is protected during this build, without reverting other work.

Final encoded checks passed:

- Complete decode: 11,488 frames, 1280×720, 30 fps, unchanged duration.
- AAC bitstream SHA-256 matches v11 exactly: `b50c20d1c3e38010c8f5d1c0a872f6dcd9b137ebe37f04acc32f5334bb325e8c`.
- All three changed picture boundaries passed transition guard, with only the intended cut at each boundary and no transient frame islands. All three 25-frame strips were visually inspected.
- The encoded replacement was inspected at one-second intervals, with the numerical entrance and a later network frame checked at full resolution. The old labels are absent at the entrance. The jelly-only comparison and literal final close were also checked in the encoded file.
- All 159 unique donor frames used same-frame paper cloning for the corner mark; none were declined or required glyph inpainting. All protected files remained unchanged.
- Candidate SHA-256: `5f3f2674150905c7b14d4ecf3dad2850d361ea5c4a87ff085fe47de2202d83ad`.

Evidence: [encoded verification](encoded-checks/verification.json), [transition report](transitions/transition-guard.md), and the associated frame images.

This is ready for owner review as a narrow repair, not a new narration verdict or shipping approval. No literal listening or continuous end-to-end viewing is claimed. V10's outstanding human listening check remains applicable, although the audio and all audio joins are unchanged. No tracker update or deployment was performed.

## Reproduction

```sh
.video-venv/bin/python scripts/video/prepare_how_an_llm_v12.py
.video-venv/bin/python scripts/video/build_how_an_llm_works_v13_review.py
```

The v13 wrapper uses the v12 narrow-repair builder with the corrected donor in-point and retiming rate. It refuses to overwrite a candidate. The builder verifies source identities, renders from pristine material, checks copied audio hashes, decodes the entire output, extracts affected frames, and runs transition guard at frames 4367, 4675 and 5004. No shared production helper was changed.

## Shipped

Shipped 2026-09-17 on David's call as `course-assets/how-an-llm-works/how-an-llm-works.mp4` (sha256 5f3f26741509…, 11,488 frames / 6:22.93), cache key 20260917ship1, duration pill 4 → 6 min, manifest `video_assets` hash refreshed. The v13 candidate was removed from `Prompts/`; earlier candidates, rolls, and the two-part split work were left for the session that owns them.
