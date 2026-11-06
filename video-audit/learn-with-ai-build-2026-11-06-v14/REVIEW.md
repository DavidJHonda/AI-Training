# Learn with AI — v14 build review

Built November 6, 2026 at the owner's request. Candidate: `Prompts/learn-with-ai-v14.mp4`, **4:06.200**, 7,386 frames, 1280 × 720, 30 fps, H.264 CRF 18 / AAC 192 kbps; 23,911,981 bytes. SHA-256: `db81af919cbcb591a375a48dad1478b4302236fae95d06abb3dfa04713669212`.

**Built for owner review. Not installed, committed, or deployed.** Transcript, signal, frame-timing, and sampled visual checks passed. Direct listening and a full-speed audiovisual review were not performed and remain outstanding; the donor's voice/cadence continuity is not certified by ASR or level matching.

## Narration assembly

Original `learn-with-ai-3.mp4` is the base. `learn-reroll-2.mp4` supplies one complete sentence enumerating quizzes, flashcards, study guides, audio and video overviews, mind maps, and more. Exact source hashes and frame boundaries are in `edit-manifest.json`. Sources, canonical JPGs, and lesson Markdown remain hash-identical.

| Output span | Content |
| --- | --- |
| 0:00–2:25.000 | Original base through upload types |
| 2:25.000–2:34.333 | Donor 2's complete output sentence |
| 2:34.333–2:37.333 | Base's exact materials-to-tools takeaway |
| 2:37.333–3:24.600 | Base four moves, following removal of the hallucination/test-relevance guarantee |
| 3:24.600–4:06.200 | Learning coach and current close, following removal of the memory-guarantee summary |

No synthetic speech or additional pauses. The donor is lowered 3.241 dB to match adjacent base speech using median voiced-window RMS. Eight-millisecond ramps apply only at real audio edits; visual changes do not introduce audio fades. All four encoded joins fall inside measured quiet intervals at a −40 dB threshold; context WAVs are in `qa/`.

Fresh ASR of the finished MP4 contains 725 words and all six required passages (punctuation normalized), including the two exact closing lines. It preserves the history/math example, all four moves, complete ten-question quiz instruction with answers withheld and grading, citation verification, and learning-coach process. Both removed guarantee passages are absent. See `encoded-transcript/learn-with-ai-v14.txt` and `qa/required-passages.json`.

This remains the reviewed roll-3 narration with the scoped repairs, not a new verbatim reading of every lesson sentence. Existing paraphrases and the short facts-versus-theory explanation remain. The upload enumeration says websites without separately saying articles, as in the accepted base; the current board displays both. ASR renders a few unchanged words imperfectly (for example “You've one” for the first move), so transcript evidence is not a substitute for listening.

## Visual treatment

All three teaching boards use current canonical JPGs. Each first appears complete and unmarked. Dense boards move to complete active cards, with fixed 4-pixel outlines at 720p; descriptions and the shared check banner receive timed emphasis. The compact input/output board stays in full view. Supporting drawings interrupt long board runs.

| Board | Total display | Longest uninterrupted run |
| --- | ---: | ---: |
| Which Study Tool for the Job? | 37.900 s | 19.300 s |
| How Gemini Notebook Works | 20.033 s | 12.333 s |
| Your Four Moves | 38.267 s | 20.000 s |

Preserved source illustrations include the crowded schedule, patient late-night tutor, alternate explanation, class-materials student, and confused learner. Retained generated diagrams include ordinary chat versus study tools, facts versus theory, and the coaching process. Reused illustrations replace photographic cutaways and a garbled coach illustration. The opening's corrupt label is repaired to “MORE WORK,” tracked only through its actual shot. A simple citation-to-original-material diagram supports the verification explanation. Engine corner marks are cleaned from retained source frames.

The standard canonical close begins at frame 7,021 (3:54.033): 48-frame full hold, 150-frame push to 1.2×, then 167-frame settled hold. The final encoded frame visibly retains both current closing lines. No added third closing line or recreated typography.

## Finished-file checks

- Independent sequential PyAV decode: exactly 7,386 frames; uniform PTS increments of 512 at a 1/15360 time base; no frame-count or cadence mismatch.
- AAC duration 246.208 seconds, 8 ms longer than video; PCM correlation with the intended audio assembly 0.999985. Encoded peak −1.513 dBFS; no sample clipping.
- All 23 declared visual boundaries pass `transition_guard.py`; every-frame boundary strips inspected, including board entrances, cutaways, donor joins, coach bridge, opening repair endpoint, and close. No stale one-to-six-frame visual islands observed.
- Encoded eight-second overview samples, board states, full openings, citation scene, and final frame inspected. Pre-encode full-size board framing and outlines were also inspected. These checks do not constitute full-speed motion playback.
- Protected input and asset hashes all pass. Evidence: `qa/verification.json`, `qa/transitions/`, `qa/silence.log`, and encoded transcript.

Reproduction: `.video-venv/bin/python scripts/video/build_learn_with_ai_v14.py`. Verification: `.video-venv/bin/python video-audit/learn-with-ai-build-2026-11-06-v14/verify_candidate.py`. The builder refuses to overwrite an existing finished candidate; preserve v14 if revising.
