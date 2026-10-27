# Training Bias v11 — shorter lesson video

Built 2026-10-27 after David approved the proposed cuts with “Sounds good. Build it please.” Review candidate: `Prompts/training-bias-v11.mp4`. Duration **2:34.400**, **48.033 seconds shorter** than installed v10. Candidate SHA-256: `d2cf348666962732470205fbfcab21d43027a0cc036744401d59c96ebb9a2bf9`.

## Local release — 2026-10-27

**Shipped locally; queued for batch deployment.** David authorized “ship it” after the build report disclosed the remaining listening review. This records owner acceptance of the exact candidate and its disclosed limitations, not completion of an additional listening pass.

- Commit: `bee39747997aa2278867ec97fc17ececc22bbf94` — `Ship shortened Training Bias v11 locally`.
- Installed at `course-assets/training-bias/training-bias.mp4`; installed and committed video match the approved candidate hash.
- Course cache key: `20261027ship11`; existing rounded `3 min` label remains correct for 154.4 seconds.
- Release includes the matching Training Bias page/Markdown cuts and existing four-step lab revision. Unrelated edits in the shared page and other lessons were excluded.
- Verified both staged and working-page inline JavaScript syntax, staged scope, whitespace, installed/staged video identity, and committed course reference.
- No push or deployment; public serving was not re-verified. See `local-release.json`.

## Approved scope and result

Narrow repair: remove the two-traps introduction and detailed RAG explanation, preserve the core bias teaching and standard close, and recover the short current-source instruction from a retained earlier version. No new narration or pauses.

| Output | Source | Treatment |
|---|---|---|
| 0:00–0:35.900 | v10 frames 0–1077 | Cow story and “This is the core of training bias.” Hold the last cow illustration frame over the 2.17-second beginning of the now-retired two-traps diagram. |
| 0:35.900–2:18.533 | v10 frames 1365–4444 | Three distortions, consequences, three questions, and the brief stale-training explanation. Original board highlights, supporting graphics, narration and timing retained. |
| 2:18.533–2:24.633 | v8 frames 5847–6030 | Restore “Whenever a specific date matters, you must verify the AI’s claim against a current external source.” Keep its original Verify Dates drawing. |
| 2:24.633–2:34.400 | v10 frames 5780–6073 | Existing standard close; extend its first frame over 13 frames of leading silence so no RAG graphic survives. Original close motion resumes unchanged. |

Source frame ranges are half-open. Exact source hashes, boundaries and output mappings are in `edit-manifest.json`. The missing temporary v7 assembly and raw generation are not reconstructed: retained finished v10 and v8 receive one additional encode (H.264 CRF 16, 1280×720, 30 fps; AAC 192 kbps).

## Board and supporting-visual treatment

| Board or scene | Highlighting | Camera and on-screen treatment |
|---|---|---|
| Wrong Pattern. Wrong Answer. | Existing treatment retained | Existing illustration walk; last cow frame held from 0:33.733–0:35.900 to cover the deleted topic diagram. |
| How Skewed Data Distorts the Picture | Existing card outlines at original spoken onsets | Full view opens at 0:35.900. Existing data-shape and cow-shortcut cutaways retained. |
| Three Questions That Reveal Bias | Existing three question outlines and takeaway | Existing full view retained, 1:38.100–2:03.400; broader-picture drawing follows. |
| Verify Dates | Unmarked supporting drawing | Original full-frame drawing retained for the 6.100-second recovered instruction. |
| AI repeats the shape of its data. | Existing standard close | First frame extended 0.433 seconds over existing silence; existing push and settled final hold preserved. Literal final frame is the close. |

The longest unbroken board run is the inherited Three Questions board at **25.3 seconds**. This pre-existing pacing exception was preserved under the approved narrow scope. Other retained supporting scenes include the opening notebook and cow drawings, the training-data/worldview comparison, cow-shortcut callback, facial-analysis and wrongful-arrest illustrations, individual-fact checking, representative-reality comparison, and training-cutoff diagram. No new illustration was created.

## Verification of the encoded candidate

- Decoded all **4,632 frames**; verified 1280×720, 30 fps and uniform presentation timestamps.
- **19/19 declared transition checks passed.** Visually inspected all three changed join strips, the sampled whole-video contact sheet and final frame. No retired diagram fragments appear at the edited joins. The inherited boundary strips were generated but not individually re-reviewed.
- Sampled mapped source-frame comparison once per second, including declared visual holds: mean absolute channel difference 2.400/255, maximum sampled frame difference 2.661/255, following the additional encode.
- Encoded audio matches the intended source assembly at **48.73 dB signal-to-error ratio**. Cuts use quiet gaps and 5 ms edge fades, without added silence. Measured quiet intervals across the three joins: **0.45, 0.48 and 0.68 seconds** at a −38 dB RMS threshold.
- Fresh full-candidate transcription confirms the early announcement and RAG explanation are absent, the recovered current-source sentence is present, and the three prompts and close remain. Automatic transcripts have minor recognition errors; source-audio matching independently verifies retained speech.
- Installed MP4, lesson Markdown, canonical JPGs, and both source candidates remain unchanged. This task did not edit `index.html` or install, commit, or publish the candidate.

## Remaining review

No subjective listening or continuous audiovisual playback was performed. At build time, the candidate was ready for David’s review, **not certified ready to ship**. The owner subsequently accepted it for local release as recorded above. Listen particularly around **0:36**, **2:19**, and **2:25** for cadence and continuity. The recovered sentence is from the same original narration as v10, but measured seams and transcription do not replace listening. Retained animation motion has not been re-evaluated continuously in this narrow pass.

Build: `.video-venv/bin/python scripts/video/build_training_bias_v11.py`

QA: `.video-venv/bin/python scripts/video/qa_training_bias_v11.py`

Full transcript: `transcripts/training-bias-v11.txt`. Numerical results: `qa.json`. Guard strips: `guard/`. Scripts intentionally refuse to overwrite existing candidates; a changed build requires a new version.
