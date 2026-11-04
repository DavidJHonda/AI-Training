# Beyond the First Answer v6: align with the shortened lesson

Review candidate: `Prompts/beyond-the-first-answer-v6.mp4`.

**3:26.167**, down from **4:17.867**, saving **51.7 seconds**.
6,185 frames, 30 fps, 1280 x 720, H.264/AAC.

Scope: the owner approved the five-cut/two-visual-repair plan with “Build it please.”
This is a narrow repair, not a full production pass or a shipping authorization.
The installed course video and lesson assets were not changed. No publication,
tracker update, or local release commit was performed.

## Source identity

Stable source: `Prompts/beyond-the-first-answer-v5.mp4`, verified byte-identical to
the installed `course-assets/beyond-the-first-answer/beyond-the-first-answer.mp4`.

- Source SHA-256: `1ba3e2d0129424a59eb8bc5cddab83ec070af86efbaeaf622f7ca15b6e192261`
- Candidate SHA-256: `a1d41d623050fa713d807d3e584958bac9b732d1f960adf03168c7f2829df76b`
- Current teaching authority: `AITipsSection` in `index.html` and the current
  `lessons/beyond-the-first-answer.md`, including the four numbered moves.

The accepted v5 master supplies all audio and visuals. Raw rolls remain available;
rebuilding their unrelated treatments would expand the approved narrow repair.
This adds one YUV-preserving video encode and one audio encode.

## Implemented cuts

All source ranges refer to v5 and are half-open. The exact frame map and protected
asset hashes are in `edit-manifest.json`.

| Cut | Source seconds | Source frames | Output join | Removed narration |
|---|---|---|---|---|
| Thought Partner history callback | 42.567-50.767 | 1277-1523 | 0:42.567 | “Just like in that history project” through “decide what works.” |
| Learn history callback | 86.200-97.267 | 2586-2918 | 1:18.000 | Unequal subject knowledge, asking the group, and “Work with AI in the same way.” |
| Start history callback | 145.033-154.633 | 4351-4639 | 2:05.767 | Civil War assignment through “real life isn't always that clear.” |
| Iterate history callback | 183.767-195.400 | 5513-5862 | 2:34.900 | Four-week project becoming a masterpiece. |
| Iterate repeated explanation | 200.967-212.167 | 6029-6365 | 2:40.467 | “Working with AI follows the exact same pattern” through “question, evaluate, and improve.” |

The opening analogy remains because the current lesson retains it. There is no
new narration, audio speed change, added pause, or removal from the four examples.

## Visual repairs and preserved board treatment

1. Source frames 1523-1528 are a six-frame remnant of the history photograph.
   They now show clean destination frame 1529; its original motion then resumes.
   The output repair spans frames 1277-1282, with motion resuming at 1283.
2. Source frames 5862-6028 now use the existing versions animation from source
   frames 5896-6028. Its 133 frames are distributed across 167 output frames,
   slightly slowing only the picture. The old four-week timeline and its dissolve
   are completely removed. The diagram's reveal remains, followed directly by the
   business-plan example. Output span: frames 4647-4813, 2:34.900-2:40.467.

Current canonical board assets and their approved v5 treatment are preserved.
Only their positions on the shorter timeline change. The iteration example begins
one frame into its existing full-board opening because the audio cut ends there.

| Board | Output topic span | Highlight/camera treatment | Supporting break |
|---|---|---|---|
| Starting a Summer Business | 0:46.833-1:16.333 | Existing full opening, speech-bubble rings, approved zoom/pan and pullback | Tutoring illustration, 0:57.767-1:04.433 |
| Understanding Profit | 1:33.100-2:03.900 | Existing full-board push and student/AI rings | Existing money-flow animation, 1:45.900-1:59.533 |
| Thinking About College | 2:15.800-2:33.000 | Existing full-board push and student/AI rings | None; 17.2 seconds uninterrupted |
| From Idea to Business Plan | 2:40.467-3:15.367 | Existing full opening, early/later speech-bubble rings, approved zoom/pan and pullback | Lawn-planning illustration, 2:55.967-3:06.967 |
| Closing Message | 3:15.367-3:26.167 | Existing canonical close and motion | None |

Longest uninterrupted example-board run is 17.2 seconds (college). The original
opening graphics, AI-learning exchange, real-world decision/question scene,
tutoring illustration, money-flow animation, and lawn-planning illustration remain.
No new illustrations or redesigned boards were introduced.

## Teaching coverage in the encoded candidate

The complete fresh transcription is in `qa/transcript.txt` and
`qa/transcript.json`. The following assessment is based on that transcript and
source/frame preservation, not a claimed listening pass.

| Teaching point | Assessment | Encoded-video evidence |
|---|---|---|
| One perfect prompt is only the start | TAUGHT | 0:00-0:10 |
| Opening group-project analogy and two-way conversation | RICH | 0:11-0:31 |
| Four moves orient the viewer | TAUGHT | 0:32-0:38 |
| Thought partner; you make final decisions | TAUGHT | 0:39-0:47 |
| Summer-business example uses strengths and asks the student to choose | RICH | 0:49-1:15 |
| Learn through follow-ups, familiar ideas, and explaining back | RICH | 1:18-1:32 |
| Profit example connects explanation to a familiar business | TAUGHT | 1:36-2:03; sales $300, costs $150, profit $150, and Sales minus Costs equals Profit |
| Find a starting point when a decision is unclear | TAUGHT | 2:04-2:16 |
| College example asks one question at a time and postpones recommendations | RICH | 2:16-2:32 |
| Iteration means versions improving the next | TAUGHT | 2:33-2:40 |
| Generic versus specific business plan; pressure-testing weaknesses | RICH | 2:41-3:15 |
| Both closing lines | MET | 3:15.54-3:21.16 |

No new factual contradiction or broken verbal reference was found in the full
transcript. “To iterate means to build something in versions” is transcribed
correctly in v6. The old v5 transcript's “inversions” is not a new content edit.

Pre-existing approved v5 compression remains: the spoken examples omit some
background/filler, detailed profit arithmetic, two final pressure-testing questions,
and spoken takeaway banners. The printed boards retain those details. These were
not removed by this build, and this is not a word-for-word reading of the lesson.

Formal narration/whole-file shipping sign-off remains pending listening. The
candidate is ready for owner review, not declared ready to ship.

## Verification

- Sequentially decoded and compared all 6,185 encoded frames to their expected
  retained source or visual donor frames. No frame mapping errors; maximum sampled
  YUV mean absolute error 0.616 or less on a 0-255 scale. All presentation timestamps
  are continuous at 30 fps, and the final canonical closing frame is retained.
- Encoded audio correlation to the planned edit: 0.9999874. Peak: -1.65 dBFS.
- All ten source cut endpoints are within measured low-energy speech gaps.
  Five-ms edge ramps were applied inside those gaps. No audio speed change.
- Final measured silence across the five joins: 0.641, 0.609, 0.716, 0.763,
  and 0.754 seconds. No extra pauses were added.
- `transition_guard.py`: all six declared edit boundaries pass, with no short
  intermediate-shot alerts. All six every-frame transition strips and all four
  whole-video sample sheets were inspected. The photo remnant and four-week
  timeline are absent from the edited spans.
- Fresh automatic transcription of the actual encoded MP4 reviewed in full:
  all five removed passages are gone, and the retained explanations/examples and
  closing lines are present.
- Source master, installed course video, current lesson Markdown, and canonical
  board hashes are unchanged from the build snapshot.

**Listening limitation:** no direct audio audition or continuous audiovisual
viewing was performed. Signal checks do not certify cadence, pronunciation, or
subjective seam quality. Review the five joins at 0:42.57, 1:18.00, 2:05.77,
2:34.90, and 2:40.47 when listening. This narrow pass does not claim a fresh
whole-file production audit of unchanged board framing or artwork.

Build and verification:

```sh
.video-venv/bin/python scripts/video/build_beyond_the_first_answer_v6.py
.video-venv/bin/python scripts/video/qa_beyond_the_first_answer_v6.py
.video-venv/bin/python scripts/video/qa_beyond_the_first_answer_v6.py --transcribe
```

The build refuses to overwrite v6. Use a new version number for any subsequent
candidate so an open player never changes underneath the reviewer.

## Local shipping: November 4, 2026

Owner approved with “ship it” after the listening limitation was disclosed.
Installed the exact v6 bytes, updated the course cache key to
`20261104ship-beyond-v6`, changed the displayed duration to `3 min`, and
updated the video manifest hash and byte size. Full asset hash verification passed.

Commit: `181e5b802f37aa9b34195d8d75696d3ad715142b`. Only the canonical MP4 and its release metadata
were committed. Unrelated lesson and asset work remains in the working tree.

**Shipped locally; queued for batch deployment.** No push, public deployment,
tracker update, or additional listening pass is claimed. See `shipping-receipt.json`.
