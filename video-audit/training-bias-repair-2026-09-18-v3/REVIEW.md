# Training Bias v3 — build review

## Recommendation

**KEEP for final human headphone review.** This review candidate implements the approved live-base repair and is not published. The lesson, live video, donor roll, current board JPGs, `index.html`, and upload Markdown remain byte-for-byte unchanged.

- Candidate: `Prompts/training-bias-v3.mp4`
- Runtime: 4:54.47 (8,834 frames at 30 fps)
- SHA-256: `7ea2f7c3401558396622b85adeb82160603be8257dbda222ebcd909ecc3159d9`
- Build script: `scripts/video/build_training_bias_v3_review.py`
- Exact manifest: `edit-manifest.json`

## Narration repair

The live narration remains the spine. Two complete beats from `Prompts/training-bias-2.mp4` replace weaker live passages:

1. **Exact student prompts**
   - Donor: 2:48.958–3:21.042
   - Replaces live: 2:01.20–2:21.50
   - Output: 2:01.20–2:33.30
   - Restores the key distinction that the model may already contain more of the picture but not lead with it, then gives the three prompts verbatim.

2. **Cooper Flagg example, causal caveat, and RAG lead-in**
   - Donor: 3:45.833–5:02.083
   - Replaces live: 2:42.80–3:26.00
   - Output: 2:54.60–4:10.87
   - Restores the worked conversation, avoids claiming that the chat proves stale training was the root cause, requires current-source verification when dates matter, and introduces RAG accurately.

The return cuts were verified against word-level timing. The first returns after the complete word “examples”; the second enters only after “creating an outdated picture” and returns after the complete original “RAG.” No teaching pauses were added. The base recognizer printed a zero-duration “Pause/Pulse” hypothesis in the silence after the first graft; a targeted `small.en` word-level pass found no spoken word there.

## Visual and production result

- Rebuilt all five lesson boards from the current canonical JPGs.
- Kept every board at a static, readable full view; no zoom or pan.
- Rings follow the spoken points on Defaults, Blind Spots, Wrong Patterns; the three exact prompts; all four chat bubbles; Retrieve, Add to Context, Generate; and the RAG caveat.
- Kept the stale-information chat full frame.
- Used the donor’s current-source and outside-information Notebook drawings after the chat, then held the last clean drawing instead of showing its obsolete embedded RAG board.
- Cleaned the Gemini Notebook corner mark from every retained live and donor Notebook frame. The build reports 909 live clones, 1,504 live inpaints, 1,246 donor clones, and zero declined frames.
- Used the current close JPG with the standard 48-frame prehold, 150-frame push to 1.2×, and a 57-frame settled hold. The close is the literal final image.
- No stock photographs and no engine outro.

Board spans in the output:

- Wrong Pattern: 0:15.10–0:28.47
- How Skewed Data Distorts the Picture: 0:59.37–1:39.47
- Three Questions That Reveal Bias: 1:53.47–2:34.17
- Stale Information in Real Life: 2:54.60–3:29.33
- How RAG Works: 4:10.87–4:45.97
- Standard close: 4:45.97–4:54.47

## Verification

- Full candidate transcript reviewed; all essential lesson teaching is present and the two earlier boundary repetitions are absent.
- Full 4-second contact sheets reviewed from beginning through the literal final frame.
- Transition guard passed all 12 declared visual/audio boundaries; every strip was also visually inspected.
- Video decodes to exactly 8,834 frames at 1280×720 and 30 fps.
- Candidate integrated loudness measured -17.69 LUFS with -0.04 dBTP after AAC encoding.
- Donor speech was matched to the surrounding live speech: graft 1 measures -18.05 LUFS versus -17.95 LUFS live; graft 2 measures -17.10 LUFS versus -16.93 LUFS live. Peak-safe limiting was applied only to the grafts.
- Sample discontinuities at all four audio joins are far below the candidate’s ordinary 99.9th-percentile sample change; no objective click spike was detected.
- Current source and lesson hashes all rechecked unchanged after render.
- See `verification/training-bias-v3/`, `transitions/`, and `qa-objective.json` for evidence.

## Remaining human check

This environment cannot audition audio. Before shipping, listen on headphones to the four joins at 2:01.20, 2:33.30, 2:54.60, and 4:10.87 and confirm perceived voice, room tone, cadence, and breaths. Objective level, peak, waveform, transcript, and visual checks pass, but they do not replace that listening pass.

The candidate has not been copied to `course-assets`, referenced from the lesson, or deployed.
