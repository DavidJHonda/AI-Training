# Pace of Change v9 — review candidate

Built September 30, 2026, following David's “Agree. Build it please.” approval of the live-video evaluation. **Built for review; not shipped, committed, or published.**

[Open v9](../../Prompts/pace-of-change-v9.mp4) — 4:34.40, 8,232 frames, 1280 × 720, 30 fps.

## Changes

- Removed the overbroad model-replacement passage and “stop judging AI by its temporary flaws.” Source frames 3291–3816 (1:49.700–2:07.200), 525 frames / 17.5 seconds removed.
- Added three approved supporting visuals under unchanged narration. These reduce the longest board-only stretch from 92.2 seconds to 23.3 seconds.
- Restored the full How Far Can AI Go? board before its final uncertainty sentence. The gold banner is fully visible and receives a 4 px purple outline at 4:15.47 in the candidate. The framing reset occurs behind the preceding ASI insert; the return is already settled.
- Preserved the approved 2023–2026 animation, remaining original scenes, board timing relative to narration, and standard close. Other existing outlines are preserved under the grandfathering rule.
- Updated the local lesson page, Markdown, prompt, upload copy, and lesson-kit wording to qualify new-model improvements rather than claim every release replaces the prior model. The public site and its video reference are unchanged.

## Candidate timestamps

| Candidate span | Picture / action |
|---|---|
| 1:49.70 | Narration join: “...every couple of months.” → “A limitation can disappear quickly...” |
| 3:04.50–3:12.10 | Human-directed research: goals, code, experiments/results, verification |
| 3:33.50–3:42.60 | Human-directed work today versus hypothetical self-improvement loop |
| 4:05.90–4:14.00 | Clearly hypothetical superintelligence across cognitive fields |
| 4:14.00–4:18.60 | Complete final board; ASI card then full gold banner |
| 4:15.47 | “Nobody knows whether AI will reach either milestone” banner highlight |
| 4:18.60–4:25.20 | Preserved forked uncertainty graphic |
| 4:25.20–4:34.40 | Preserved canonical close |

Board treatment remains the approved plan: canonical comparison overview followed by its approved animation; Why So Fast? at full view with its existing three card highlights and two breaks; Could AI Improve Itself? with complete-card views and banner plus two new breaks; How Far Can AI Go? with the existing AGI/ASI views, new ASI break, then corrected full-board takeaway. No new pauses were added. The second insert runs to the next board cut, avoiding an unnecessary one-second return to the previous board.

## Audio and source limitations

Only the finished v8 survives locally. Source SHA-256: `4cce8f2cb230d865ad54e6ff165a603fc779c6180514bd83bb8965cc8f6680d7`, previously verified identical to the public video. This is one new encode from that finished source; no raw generation was available.

The source cut boundaries sit in measured quiet gaps: 109.467–109.982 and 126.989–127.412 seconds. The encoded joined gap is 0.44446 seconds, agreeing with the expected 0.44467 seconds. A four-millisecond interpolation smooths the quiet seam. Retained PCM outside that seam is sample-identical to the original decoded source. There are no audio changes at visual insert boundaries and no global level adjustment.

The isolated join transcription reads:

> pushing them to release new models every couple of months. A limitation can disappear quickly, so today's no is not necessarily permanent. This diagram outlines

[Encoded join audition clip](encoded-narration-join.wav).

**Listening remains unperformed.** Speech recognition and waveform checks do not certify cadence or subjective audio quality. Listen around 1:49–1:52 before shipping. Continuous audiovisual playback of the entire candidate also remains unperformed; no final KEEP or shipping certification is claimed. The retained lesson coverage from the full v8 transcript is preserved except for the approved deletion; both closing lines remain intact.

## Verification completed

- Entire encoded candidate decoded without errors: 8,232 frames / 274.40 seconds.
- All 24 declared transition boundaries passed `transition_guard.py`; inspected every-frame strips for all eight changed or adjacent visual boundaries.
- Compared 303 retained-frame samples to their mapped source frames; maximum mean absolute pixel difference 2.596 / 255 after encoding.
- Compared 43 replacement-frame samples against the planned artwork / canonical board; maximum difference 3.722 / 255.
- Compared complete decoded AAC to the approved edited PCM: signal-to-error ratio 43.21 dB. Join-local peak −56.68 dBFS.
- Inspected the three new inserts and corrected full-board banner in full-resolution frames extracted from the actual encoded candidate. Labels are readable and the full gold banner is inside the frame.
- Final decoded frame maps to the original canonical close. The source MP4 and all canonical board hashes remain unchanged.
- `sync_gemini_notebook.py --lesson pace-of-change --check` passes.

Evidence: [manifest](edit-manifest.json), [verification](verification.json), [transition results](transitions/transition-guard.md), [corrected banner](encoded-007679.jpg).

## Artwork and reproducibility

Three project assets were generated with the **built-in image_gen tool**. Their prompts and originals are retained:

- [Research workflow](../../scripts/video/assets/pace-of-change-cutaways-2026-09-30/research.png)
- [Human-directed / hypothetical loop contrast](../../scripts/video/assets/pace-of-change-cutaways-2026-09-30/contrast.png)
- [Hypothetical ASI](../../scripts/video/assets/pace-of-change-cutaways-2026-09-30/asi.png)
- [Exact prompt set](../../scripts/video/assets/pace-of-change-cutaways-2026-09-30/prompts.json)

New images are static cutaways, with no added camera motion or narration. They are purpose-generated imagery; source Notebook stock photographs were not introduced. All speculative visuals explicitly say hypothetical.

Build: `.video-venv/bin/python scripts/video/build_pace_of_change_v9.py`

QA: `.video-venv/bin/python scripts/video/qa_pace_of_change_v9.py`

Candidate SHA-256: `388f84fc1d76bac210de0f4d2096b0e1b9b4608d98dbe1ee1fc9e3c76f444fc5`.

The builder intentionally refuses to overwrite this candidate. Any requested revision should use a new version. No tracker row was changed. No Git commit, push, or deployment was performed.
