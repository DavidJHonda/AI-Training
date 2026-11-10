# How AI Answers — motion-preserving edit, v19

Built the approved version-2 plan. **Review candidate: `Prompts/how-ai-answers-v19.mp4`, 2:35.367, 1280×720, 30 fps, 4,661 frames.**

The course video, lesson, canonical boards, and prep materials are unchanged. Nothing was installed, committed, pushed, or published.

## What changed

- Retained the dog illustration and original staggered token reveal. Held the intact dog drawing through the source's brief blank fade. Repaired the ambiguous first-answer-token placeholder and removed token-index clutter.
- Used the exact current Before the Answer Begins and Same Token, Different Context images, with four-pixel narration-led outlines. Neither board was recreated or reworded.
- Reconstructed the moving vector-to-prediction handoff around the dog question, replacing the unrelated story prompt. The vector moves toward the possible starts; the following demonstration supplies the percentages.
- Used the current shared demonstration captures for both probability distributions and selections. Each spoken choice and the other-token remainder receives its own cue. Selected rows retain the lesson's semantic selection border.
- Preserved the original moving token row, arrows, changing vector numbers, and vector handoffs for You/could/name/him. Added the persistent dog question, simplified labels, enlarged the useful area, and retimed the reveals to the spoken words. Removed the “1 token ahead” heading.
- Retained source word/period tiles for the finish, separated the stopping signal from the answer text, removed the extra probability chart and technical labels, and left only the completed answer after stopping.
- Used the exact canonical close, with a 48-frame hold, 150-frame push to 1.2×, and 60-frame settled hold. Removed the generated branded outro. Kept source footage has its corner mark cleaned or cropped out.

## Narration cuts and joins

All cuts use the pristine version-2 audio. No donor narration and no added pauses. Five-millisecond ramps occur only at the three joins inside measured silence. The retained PCM outside those ramps is identical to the source after sample-rate conversion.

| Removed source span | Removed teaching | Output join | Measured encoded gap below −40 dB |
|---|---|---|---|
| 0:53.400–1:03.600 | Repeated “contains … your entire request” explanation | 0:53.400 | 0.69 s |
| 1:42.367–1:53.100 | “Only ever calculates one single step ahead” claim | 1:32.167 | 0.94 s |
| 2:08.500–2:22.700 | Universal narrowing claim and repeated loop explanation | 1:47.567 | 0.74 s |

These include surrounding silence, rather than cutting exactly on ASR speech boundaries. Listening clips `join-1.wav`, `join-2.wav`, and `join-3.wav` contain context around each final join.

## Output visual sequence

| Output time | Treatment |
|---|---|
| 0:00–0:16.533 | Dog drawing, repaired first-token setup, native token reveal |
| 0:16.533–0:36.700 | Before the Answer Begins; full board, four whole-step cues |
| 0:36.700–0:53.667 | Same Token, Different Context; full view, dog then dinner card |
| 0:53.667–0:59.200 | Animated vector handoff using the dog question |
| 0:59.200–1:19.500 | Initial probabilities and spoken row cues |
| 1:19.500–1:32.167 | Selected You and updated-vector explanation |
| 1:32.167–1:47.567 | Native growing-word/vector animation with repaired labels and timing |
| 1:47.567–2:06.567 | Name probabilities and spoken row cues |
| 2:06.567–2:16.600 | Selected Spot and another-run qualification |
| 2:16.600–2:26.067 | Period, then separate stopping signal |
| 2:26.067–2:26.767 | Completed answer only |
| 2:26.767–2:35.367 | Canonical closing message |

Longest continuous board run: approximately **37.13 seconds**, comprising the recap and comparison. Longest individual still scene: approximately **20.3 seconds**, the first probability walkthrough. The animated handoff, growing reply, and finish separate the remaining board runs. No decorative footage was added.

## Verification completed

- Full encoded video/audio decode passed; frame count and duration match the plan.
- Forty encoded states compared with prepared references; largest mean pixel error 3.15/255. Inspected the encoded state sheets, all eight probability/remainder cues, word-reveal sequences, final frame, and boundary summaries. Detailed every-frame strips were also inspected at the three narration joins.
- Transition guard passed all 14 declared boundaries. `guard-final/` contains the final boundary record; two selection-boundary declarations were corrected by one frame to match their actual visual change, without changing the video.
- Full ASR of this exact candidate retains all seven required sentences, both complete probability distributions, and the qualification about another run. All three removed passages are absent. ASR writes the spoken token You as its homophone “u”; that is normalized only for the text check.
- Encoded audio correlation with the assembled reference is 0.999988, with 46.09 dB signal-to-error ratio. No unintended retained-PCM change detected.
- All protected source, page, lesson, board, and installed-video hashes match the pre-build record.
- Builder and QA scripts passed syntax checks. Internal v17/v18 candidates informed timing and transition fixes; v19 supersedes them for review.

**Not performed:** direct perceptual listening or uninterrupted audiovisual playback. Frame sequences, ASR, and signal comparisons cannot certify cadence, audible seam quality, or overall motion feel. The final listening review should include 0:53.4, 1:32.2, and 1:47.6, followed by a complete watch/listen. This is a built candidate ready for review, not a shipping verdict.

## Reproduction and provenance

Source: `Prompts/how-ai-answers-2.mp4`.

Source SHA-256: `009393ffb3e9fbcae7e0ffd463527ebee3014e7bbf712af953a09f5733d16820`.

Candidate SHA-256: `90b5fb1597b8ce95a5a4fb0792178ee39d15057be8f585f40bba74b39622285f`.

The builder's filename reflects the first build in this pass. Use a fresh `--version` for any further render; existing candidates are protected from overwrite.

```sh
.video-venv/bin/python scripts/video/build_how_ai_answers_v17.py --version 19
.video-venv/bin/python scripts/video/qa_how_ai_answers_motion.py --version 19
HF_HUB_OFFLINE=1 .video-venv/bin/python scripts/video/transcribe_selected_videos.py \
  Prompts/how-ai-answers-v19.mp4 --model small.en \
  --output-dir video-audit/how-ai-answers-motion-v19-2026-11-10/transcripts
```

See `edit-manifest.json` for source/output mapping, hashes, exact board geometry, and animation retiming; `qa.json`, `transcript-check.json`, and `guard-final/transition-guard.json` contain the verification results.
