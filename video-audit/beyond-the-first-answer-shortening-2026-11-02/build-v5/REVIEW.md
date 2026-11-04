# Next Level Moves v5: shorter narration

Review candidate: `Prompts/beyond-the-first-answer-v5.mp4`.

Duration: **4:17.867**, down from **5:06.867**, saving **49 seconds (16%)**.

The approved approach keeps the existing boards, shortens the spoken chats, and omits the four spoken takeaway banners. All four moves, the history-project examples, supporting illustrations, and original closing remain. No narration was synthesized or sped up. This supersedes the earlier analogy-removal proposal in the parent folder.

| Example | Narration removed | Time saved |
| --- | --- | ---: |
| Thought Partner | Conversational filler, availability details, banner | 11.10 s |
| Learn | Extra student background, detailed arithmetic and expenses, banner | 21.23 s |
| Start | Introductory AI filler, banner | 7.00 s |
| Iterate | Final two AI questions, banner | 9.67 s |

The profit example still explains profit and gives sales of $300, total costs of $150, and profit of $150. The college prompt still asks one question at a time and says not to recommend a college yet. The iteration example retains the full specific student prompt and two pressure-testing questions.

Canonical board JPGs were reused unchanged. Camera moves and highlights follow the edited narration; the banners remain visible without a spoken-banner highlight. All unaffected visuals and the original closing use the verified live-matching v4 master. Raw source rolls remain available. This narrow edit adds one video and one audio encode.

## Verification

- All 7,736 frames decoded and compared with the expected retained source frames or retimed canonical-board renders. Maximum sampled YUV mean absolute error: 0.702 on a 0–255 scale.
- Audio matches the planned edit with correlation 0.999987. Cuts lie in measured pauses, with 5 ms ramps. No speed changes or added holds.
- All 25 transition strips and all eight frame contact sheets inspected. The automatic transition checker flagged two continuous camera pans, at frames 1,908 and 2,179. Detailed strips confirmed no stray inserted frames; the raw flags and manual disposition are both retained.
- Source video, installed course video, lesson text, and board hashes remain unchanged.
- Fresh automatic transcription of the encoded candidate is in `qa/transcript.txt` and `qa/transcript.json`.

**Listening review remains outstanding.** The agent inspected frames, transcript and audio signals but did not audition the soundtrack. This is a review candidate, not an installed or published release.

Rebuild: `scripts/video/build_beyond_the_first_answer_v5.py`; verification: `scripts/video/qa_beyond_the_first_answer_v5.py`. Detailed cuts, source hashes and output timestamps are in `edit-manifest.json`.

## Local shipping: 2026-11-02

Owner approved with “Ship it” after the listening limitation was disclosed. Installed the approved v5 bytes at `course-assets/beyond-the-first-answer/beyond-the-first-answer.mp4`, updated the cache key and displayed runtime, and updated the manifest hash and size. Full asset verification passed: 244 retained assets, 262 website references, 54 finished videos.

Commit: `272448e2280293ef0eeb30a573288ea327527910`. Installed SHA-256: `1ba3e2d0129424a59eb8bc5cddab83ec070af86efbaeaf622f7ca15b6e192261`.

**Shipped locally; queued for batch deployment.** No push or deployment was performed. No direct listening pass or tracker update is claimed. Prior review results describe the exact approved bytes.
