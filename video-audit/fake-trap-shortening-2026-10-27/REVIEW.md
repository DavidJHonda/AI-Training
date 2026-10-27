# Fake Trap v12 — two approved lesson-alignment cuts

Status: **shipped locally; queued for batch deployment**. Owner approved local shipping after review; see release record below.

Candidate: `Prompts/fake-trap-v12.mp4`, **4:03.167**, 7,295 frames at 30 fps, 1280×720. Exactly 12 seconds removed from v11. SHA-256: `2c81b44a5d6c9f43fbbb79054778d750c0453038c65671e05850b5e0388ed702`.

## Authorization and scope

User: “Go ahead and make those two cuts. Keep the detector explanation and the earlier shortening decisions, then check the joins.”

Narrow repair. Retains the complete detector explanation, prior school-walkthrough and eyes/lie-detector shortening, the repost distinction, all safety guidance, v11's callback illustration, and the complete closing sequence. No new narration, pauses, fades, speed changes, or board treatment. The course video, page, lesson text, and assets are unchanged.

Source: `Prompts/fake-trap-v11.mp4`, SHA-256 `7614d463682dff720a84b84561bb97ac02e0e9eb71192bcfd134bc849b827664`, matching the installed video at build time. This is an existing finished video; picture and audio were encoded once for this edit. Earlier raw generations are absent.

## Exact cuts

Source and output intervals are frame-accurate, half-open. Audio cuts use the same spans, at 1,600 samples per frame / 48 kHz.

| Cut | Source frames | Source time | Output join |
|---|---|---|---|
| “Imagine how this plays out.” | 546–615 | 0:18.200–0:20.500 | 0:18.200 |
| “To find the truth, you have to move the test off the image itself. Check the source, not the pixels. Shift your focus away from appearance and toward independent evidence.” | 4123–4414 | 2:17.433–2:27.133 | 2:15.133 |

The second cut removes the entire “Check the Source, Not the Pixels” board, starting on its first frame and ending at the emotional-cue scene's first frame. All other board framing, highlights, camera motion, and supporting scenes retain their original timing relative to narration. The three-check board remains. The standard close retains all 274 original frames.

## Verification on the encoded candidate

- Full decode confirms 7,295 frames, 30 fps, correct dimensions, and continuous timestamps.
- Every encoded frame compared against its intended v11 source frame at 80×45. Maximum mean absolute RGB error: 0.432/255. Both removed intervals are absent. Every closing frame is mapped to its original source frame.
- Transition guard passes both boundaries. Agent inspected every frame in both 25-frame boundary strips: direct arrival at the destination scene, no stale board frames or brief intermediate scenes.
- Encoded audio correlates 0.999846 with the precise retained source assembly. No additional silence or processing was applied before encoding.
- At 0:18.200, the measured quiet gap is 0.48 s (17.88–18.36 at −40 dBFS); 10 ms levels either side are −63.3 / −57.3 dBFS.
- At 2:15.133, the measured quiet gap is 0.67 s (134.60–135.27 at −40 dBFS); 10 ms levels either side are −64.4 / −60.5 dBFS.
- Fresh whole-file ASR confirms the removed lines are absent; the detector explanation, emotional cue, three checks, repost distinction, verification rule, safety guidance, and closing lines remain. “Check the source, not the pixels” occurs only at the close. Source-to-output audio comparison supports preservation beyond ASR wording.
- Protected source, installed video, page, lesson Markdown, and lesson assets retain their hashes.

## Listening and review limits

No perceptual listening or continuous audiovisual playback was performed by the agent. Waveform measurements, frame inspection, and ASR cannot certify cadence or the absence of audible artifacts. Both joins are supplied as 12-second encoded review clips, with the join five seconds into each:

- `qa/opening-join.mp4`
- `qa/detector-to-emotions-join.mp4`

This is ready for listening review, not a whole-file shipping certification. Previously accepted narration paraphrases and board treatments outside these two cuts remain. The Video Tracker was not accessed or updated.

## Reproduction and evidence

- Build: `.video-venv/bin/python scripts/video/build_fake_trap_v12.py`
- QA: `.video-venv/bin/python scripts/video/qa_fake_trap_v12.py`
- `manifest.json`: approved scope, exact source/keep spans, hashes, and encode command.
- `qa/summary.json`, `qa/transcript.json`, `qa/transcript.txt`, `qa/transitions/`: verification evidence.

An initial encode was interrupted after detecting an incorrect inferred output rate. The final build explicitly requests 30 fps; its complete timestamps and mapping passed the independent checks above. The interrupted file and temporary source PCM were discarded after verification.

## Local release — 2026-10-27

Owner: “Looks good. Ship v12 locally.” Installed the exact reviewed v12 at `course-assets/fake-trap/fake-trap.mp4`, verified SHA-256 `2c81b44a5d6c9f43fbbb79054778d750c0453038c65671e05850b5e0388ed702`, and changed only its video cache key to `20261027ship12` (display remains `4 min`; actual 4:03.167). Inline JavaScript syntax passed. Commit `00fc5f1831894a0bf5294e859f15589ef405c65a` contains only the video and the single video-reference line. Committed asset hash and reference verified. Existing lesson edits and all unrelated working changes remain intact. Prior candidate verification applies to the byte-identical installed file; owner shipping approval does not constitute agent listening certification. No push or deployment performed. Scoped render-scratch cleanup found no remaining disposable files.
