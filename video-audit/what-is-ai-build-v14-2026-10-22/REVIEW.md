# What is AI? — v14 donor repair

Review candidate: `Prompts/what-is-ai-v14.mp4`, **2:46.5**, 4,995 frames at 30 fps, 1280 × 720. Shipped locally on owner approval; see SHIP.md. Queued for batch deployment.

The owner explicitly asked to use roll 6's prompt explanation and edit the closing from roll 7 rather than reroll. This approves the paraphrased explanation and the within-sentence trim needed for the second closing line. The previous assessment of the unedited rolls does not prohibit this newly authorized repair.

## What changed

- Retained the opening, definition, AI Is Everywhere, recommendation explanation, generative job, examples, and exact course-focus takeaway from the existing assembly's source footage.
- Added exactly 30 frames (1.000 second) of matched room tone at the end of AI Is Everywhere, holding its last board frame. In the encoded output, the measured silence is **1:44.166–1:45.588 (1.421 seconds)**. The previous actual signal-level gap was approximately 0.421 seconds; the earlier 0.82-second estimate came from ASR timestamps. The added duration is exactly the approved extra second.
- Replaced the disconnected prompt definition with roll 6's complete two-sentence explanation, source **0:30.700–0:39.400**: “The engine behind this creation process is something called a prompt. That's simply the specific question or set of instructions you type into the system.” It follows the generative job and precedes the existing examples.
- Closing line one is roll 7 source **2:37.200–2:39.100**. Closing line two is source **3:01.100–3:03.400**, removing “you need to” and retaining “Start with something you want to do.” The intervening toolbox/workflow narration and the subsequent extra ending are excluded.
- The first closing line ends naturally. For the second, signal inspection locates the initial /s/ after the preceding “to”; the chosen cut preserves approximately 0.11 seconds of that fricative before the /t/. A 2 ms ramp avoids a hard edge. Earlier test cuts at 3:01.000 and 3:01.040 retained “to” in fresh ASR; a later test and the final assembly transcribe the required line without it.
- Used the exact current types and closing JPGs. The closing uses a 48-frame hold, 150-frame smooth push to 1.2×, and 48-frame settled hold. The canonical closing is the literal final frame.

## Narration result

The complete fresh candidate transcript was read. The repaired passage now teaches the creation/prompt relationship before the definition, names all six output examples, retains the course-focus takeaway, and speaks both current closing lines in order. The owner-approved explanatory wording differs from the original verbatim generation request. It does not include learned patterns, the originality overclaim from roll 6, or the extra technical claims from roll 7.

| Beat | Encoded narration |
|---|---|
| Generative AI job — TAUGHT | 2:11.16–2:15.46, “Then there is generative AI. Its job is to make something that didn't exist.” |
| Prompt connection and definition — TAUGHT | 2:16.08–2:24.22, roll 6's two complete sentences quoted above. |
| Six examples — TAUGHT | 2:25.08–2:31.26, email, essay, image, website, song, video. |
| Takeaway — MET | 2:32.32–2:37.62, “AI can recommend, AI can create. This course focuses on generative AI.” |
| Closing — MET | 2:38.48–2:42.02, “You've got a tool that can help. Start with something you want to do.” |

Content check passes for the authorized repair. Direct listening was unavailable, so voice continuity, cadence and the perceptual quality of the edited initial consonant remain for listening review. This is not a claim of an end-to-end audiovisual audition or shipping readiness.

## Visual treatment

| Board | Treatment |
|---|---|
| Where AI Already Lives | Preserve previous framing and highlighting; hold its final frame for the additional second. |
| Two Types of AI | Preserve existing recommendation treatment. Generative return opens whole, then uses a complete-card zoom with job, mechanism/definition, and examples outlined at their spoken onsets. Return whole for the takeaway and banner highlight. Fixed 4 px outlines; original canonical JPG unchanged. |
| You've got a tool that can help. | Exact current close board, unmarked, standard 48/150/48-frame motion. |

The donor audio is placed under course boards. Their generated diagrams and overlong visual sequences are not inserted. The existing opening and recommendation example animation remain.

## Verification

- Every encoded frame compared against its selected source or board render: maximum frame mean absolute error **3.081/255**; no mapping mismatch.
- 4,995 decoded frames, continuous timestamps, 30 fps.
- Encoded audio correlation to intended PCM: **0.999982**.
- All **12 transition gates pass** at the stricter 12-frame visual-island threshold. Every-frame transition strips and encoded board/closing samples were inspected.
- One-second added hold verified by the frame/sample plan and measured encoded silence.
- Fresh `small.en` transcription verifies the repaired explanation and both closing lines, including “Start” without “you need to.”
- Source and protected course-file hashes unchanged. Gains applied only to the new donors to approximately match active speech RMS: prompt +1.7 dB; closing line one −1.3 dB; closing line two +3.9 dB. No clipping in intended PCM.
- Reassembled from the same finished v11/Why Learn v10 source files plus raw rolls 6/7, avoiding a further encode of v13. One additional encode of the finished base footage remains a source limitation.

Reproduction: `scripts/video/build_what_is_ai_v14.py`, `scripts/video/qa_what_is_ai_v14.py`; source hashes and exact timeline are in `edit-manifest.json`. Results are in `qa.json`, `encoded-silences.txt`, `transitions/`, and `transcripts/`.
