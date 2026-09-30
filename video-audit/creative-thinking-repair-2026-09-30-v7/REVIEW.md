# Creative Thinking repair candidate

Built September 30, 2026 following the user's “Build please” approval. Candidate: `Prompts/creative-thinking-v7.mp4`, **2:47.37**, 1280×720, 30 fps, 5,021 frames. Ready for review of the targeted changes; not installed, committed, or published.

Candidate SHA-256: `8b59d4b7e1b181f47a3fd53b8ed887ccb4f39de165522d39ac9664b2ea70606f`.

Source: `course-assets/creative-thinking/creative-thinking.mp4`, SHA-256 `7c457ead1ec33f4a3239a3b925e5ba4cd552378cede06927d267ecf6d0cfa55f`. Only the finished source survives locally; this candidate is one encode from that source, not a chain of encodes through the intermediate candidates.

## Changes

- Removed source **1:37.667–1:43.067**, “and everyone using the same AI gets similar answers. With the baseline equalized,” and **1:44.800–1:45.600**, “entirely.” Total removal: 6.2 seconds. The retained sentence is: “Today, AI gives polished answers in seconds. The professional advantage moves to the person who can notice what is missing, connect ideas from different places, and choose the better direction.”
- Corrected the surviving AI diagram's title to “AI gives polished answers.” The “Identical Outputs (Zero Variance)” section falls within the removed footage. The later missing-angle animation starts after an inherited dissolve that otherwise briefly exposed “EQUALIZED BASELINE” and “Parity: 100%.” Its useful motion and final unique-angle state remain.
- Preserved picture continuity across the “entirely” cut by retiming the missing-angle sequence. Source frames 3135–3251 map to output frames 2930–3065; the later hands illustration remains at the original relative narrative position.
- Inserted the proposed hands/gear/leaf drawing at output **2:16.80–2:20.80**, under “borrow a pattern, feature, or approach…” It combines elements from different domains. The practice board returns 1.47 seconds before the next card's camera move. Source drawing: frames 3252–3371, or 1:48.40–1:52.40 of the original file.
- Replaced the old tinted close with the canonical white JPG, beginning at output **2:38.467**. Verified 48-frame opening hold, 150-frame push, 69-frame settled hold, and 1.2× enlargement. The course close is the literal final frame.

No extra pauses were added. Audio outside the two cuts and their four 4 ms shoulders is sample-identical in the intermediate PCM: 8,032,832 unchanged samples verified. Shoulders fade into room tone taken from the source gap. The first cut retains approximately 0.28 seconds between the end of “seconds” and the next sentence's onset. The “entirely” cut uses low-energy shoulders identified with the waveform and two ASR passes. Neither join has been heard by ear.

## Teaching review

**Content assessment: KEEP on transcript evidence, pending listening.** The specific inaccurate AI premise is removed. Full candidate narration was transcribed and read; the following remain:

| Teaching point | Assessment | Output evidence |
|---|---|---|
| Good-idea hook, missed connections, better approach | RICH | 0:00–0:14 |
| Definition of creative thinking | RICH | 0:14.64–0:22.40 |
| Creativity beyond artists, writers, musicians | RICH | 0:23.76–0:34.74 |
| Jobs: simpler, more personal, easier-to-use computers | RICH | 0:35.18–0:53.92 |
| Lawyer: same facts and laws, different strategy | RICH | 1:02.26–1:09.22 |
| Entrepreneur: overlooked need, new approach | RICH | 1:10.04–1:14.58 |
| Engineer: solve what the standard approach cannot | RICH | 1:15.28–1:18.96 |
| Doctor: same symptoms, missed diagnosis | RICH | 1:18.96–1:23.76 |
| Creativity as a habit beneath many jobs | RICH | 1:24.78–1:32.88 |
| Polished AI answers; human noticing, connecting, choosing | TAUGHT | 1:34.30–1:45.72; both unwanted assertions absent |
| Habits can improve | TAUGHT | 1:47.22–1:50.44 |
| Generate Before You Judge, including bad/obvious ideas | RICH | 1:55.80–2:05.20 |
| Ask What If, change assumptions, consider the opposite | RICH | 2:06.42–2:12.68 |
| Connect Unrelated Things, borrow and apply | RICH | 2:13.68–2:21.40 |
| Step Away, Then Return, allow new connections | RICH | 2:22.24–2:31.90 |
| Habits widen options; judgment selects | RICH | 2:32.76–2:36.78 |
| Both closing lines, nothing afterward | RICH | 2:38.62–2:42.54 |

Hard requirements are present in the transcript. No material content error identified after the cuts. Current lesson source remains consistent; no lesson or board copy changed. The retired generation prompt's additional verbatim sentence is not treated as an active requirement. Full-file ASR writes “A professional advantage”; the short join transcription writes “The professional advantage,” consistent with the preserved source. This minor ASR disagreement is not a confirmed spoken defect.

## Visual scope and remaining limitations

The two existing dense-board treatments remain: full unmarked opening, complete-card zooms, whole-card rings, and full-view summaries. Unaffected source drawings remain. This targeted candidate does not redesign the boards or add unspecified illustrations.

The longest course-board run remains **40.4 seconds** at 0:54.40–1:34.80. The first practice-board run is now 29.43 seconds at 1:47.37–2:16.80; the later practice board and close run for 26.57 seconds after the cutaway. These are still longer than the broader visual-refresh guideline. No additional meaningful illustration was established in the approved plan, so that broader refinement remains open.

The pre-existing Macintosh photograph at 0:35.33–0:46.17 remains outside this repair. Inspection of the earlier builder establishes that it was taken from the original Notebook roll, so its provenance still needs resolution or replacement before a full production sign-off. Inherited ring widths and optional “rule-bound professions” wording also remain. This candidate is not labeled ready to ship.

## Verification

Completed on the final v7 encode:

- Full sequential decode: 5,021 frames, 167.3667 seconds; expected reduction of 186 frames.
- All seven declared edit boundaries passed `transition_guard.py`; every boundary strip and the encoded overview were visually inspected. No stale-frame island found at those boundaries.
- Final-file AAC payload hash equals the fully transcribed v5 candidate's payload hash: `f6e72fe2dd6fb71b40498c0b6b00f7c2521320111337ba7a3d932a66883fb546`. Thus the full candidate transcript applies exactly to v7; the subsequent changes were visual only.
- Canonical close background is neutral white: encoded limited-range YUV 235/128/128, RGB 255/255/255. Pill width is 720 px at opening and 864 px settled, exactly 1.2×. Final frame remains the close.
- Source video, lesson Markdown, and all three canonical JPG hashes remain unchanged. Website files were not edited.

**Listening remains unperformed**, including output joins at **1:37.667 and 1:39.400**. Transcript recognition, waveform analysis, and visual guards do not certify pronunciation, clicks, cadence, or voice continuity. A short listening clip is saved as `listen-1m34-to-1m48.wav`. Real-time end-to-end audiovisual playback and whole-file shipping checks remain outstanding.

Builder: `scripts/video/build_creative_thinking_v7.py`. QA: `scripts/video/qa_creative_thinking_v7.py`. Supporting records: `edit-manifest.json`, `verification.json`, `candidate-transcript.txt`, `audio-preservation-qa.json`, `encoded-overview.jpg`, and `transitions/`.

Build and QA commands:

```sh
.video-venv/bin/python scripts/video/build_creative_thinking_v7.py
.video-venv/bin/python scripts/video/qa_creative_thinking_v7.py
```

The builder refuses to overwrite an existing candidate. V5 and v6 remain intermediate review artifacts; **v7 is the delivered candidate**. No shipping or publishing authorization was inferred from “Build please.”
