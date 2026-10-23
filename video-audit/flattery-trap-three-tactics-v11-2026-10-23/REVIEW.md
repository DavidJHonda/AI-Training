# Flattery Trap v11: three tactics and a brief tip

2026-10-23. Narrow repair authorized by the request to match the revised lesson box. Candidate: `Prompts/flattery-trap-v11.mp4`. The installed course video remains v10 pending review and local shipping authorization. No deployment, commit, or tracker edit.

## Result

4:21.767, down from 5:14.367 (52.600 seconds shorter). 7,853 frames, 1280×720, 30 fps. All three weak/better examples remain. The opposing viewpoint stays in Ask for the Gaps. The saved-instruction tip lasts 12.900 seconds and retains the exact instruction.

The source is the verified, stable `Prompts/flattery-trap-v10.mp4`, identical to the current installed video. Original raw rolls are unavailable locally. The first 4,712 compressed video packets/decoded frames are preserved exactly. Only the edited tail is encoded; the assembled audio is encoded once. No synthetic voice or word-level grafts.

## Narration edit

All ranges are source time, half-open, cut inside measured silences. The edit preserves whole sentences, including speech tails beyond the speech recognizer's estimated word endpoints.

| Source range | Action |
|---|---|
| 0:00.000–2:40.867 | Keep opening through “it has not disappeared.” |
| 2:40.867–2:44.600 | Remove “This table outlines five ways to fight the flattery trap.” |
| 2:44.600–3:52.500 | Keep first, second, and third tactics, all weak/better examples, and rubric caveat. |
| 3:52.500–4:21.033 | Remove separate fourth tactic and its counterargument caveat; the opposing-viewpoint question remains in tactic two. |
| 4:21.033–4:27.833 | Keep “Each of these moves works because you are replacing a request for validation with a concrete standard for the AI to meet.” |
| 4:45.267–4:52.333 | Move saved-instruction explanation directly after that summary: “In applications that support it, you can save this direction to guide all future responses so you don't have to type it every time.” |
| 4:39.400–4:45.233 | Follow with the exact “Be direct with me…” instruction. |
| 5:01.067–end | Keep “Ask AI to improve the work, not approve of you” and the standard close. |

Omitted within the remaining tail: the fifth-move label, weak “be honest with me” setup, “Give it a direct instruction,” the extended standing-instruction caveat, and “All five of these moves point to a single strategy.” The original first-three-tactic explanations remain intact. No pauses were added. Five editorial joins use 5 ms fades inside existing silence; visual-only scene changes do not alter audio.

The saved-instruction sentence now introduces the quoted instruction. The board displays the instruction throughout this brief tip. The source's phrase “all future responses” is retained; the page's more qualified “if your app supports saved instructions” wording remains visible. This repair does not add an accuracy guarantee.

## Board and supporting-picture plan

| Board | Highlighting | Camera | Breaks and purpose |
|---|---|---|---|
| Three Ways to Fight the Flattery Trap | First row, second row, third row, unnumbered tip, then takeaway; teal row/tip rings and purple takeaway ring | Complete unmarked board first for two seconds; then complete-row framing. Tip returns to full view for two seconds before its dive. Takeaway is full view. Fixed 4 px on-screen rings. | Tactic-one board: 15.9 s; gaps board: 15.9 s; rubric board: 19.9 s; tip: 12.9 s; takeaway: 3.5 s. |

Exact canonical JPG: `course-assets/flattery-trap/flattery-trap-five-moves.jpg`, 1600×1101. Its legacy filename is retained. Temporary 2112×1188 canvas, JPG offset (256,43); no reflow or repainting. Complete geometry, colors, timing, hashes, and source/output mappings are in `edit-manifest.json`.

Supporting scenes retained/reused:

- Source 3:00.500–3:05.267: neutral input versus evaluation, original narration/timing.
- Source drawing 4:21.033–4:24.833 reused under source narration 3:21.200–3:25.000 (“specific targets to locate”), replacing an extended board hold. Its crossed-out thumbs-up and concrete checklist reinforce the shift from approval to specific criteria. The original summary occurrence remains.
- Complete rubric-alignment drawing from source 3:47.267–3:52.500, slowed to cover 3:44.867–3:52.500 beneath the rubric caveat. Its reveals remain in order and no speech changes.
- Source 4:21.033–4:27.833: original crossed-out thumbs-up summary.
- Original standard close and its motion retained.

The longest changed continuous board run is 19.867 seconds. Earlier unchanged board runs retain the current video's approved treatment.

## Verification

See `qa.json`, `transcript.txt`, `candidate-words.json`, `encoded-frames/`, and `transitions/` for the encoded-candidate evidence. Final verification notes follow below.

Direct listening and continuous audiovisual playback have not been performed. Transcript verification, source-gap measurements, encoded-audio comparisons, and visual frame/transition inspection do not replace a listening pass. The candidate is for review, not whole-file shipping certification. Prior v10 limitations outside the requested tactics repair remain documented in its review.

## Reproduce

- `.video-venv/bin/python scripts/video/build_flattery_trap_v11.py`
- `.video-venv/bin/python scripts/video/qa_flattery_trap_v11.py`

The builder refuses to overwrite the candidate. Increment the version before another render.

### Completed encoded-file checks

- Full decode: 7,853 frames at 30 fps; every presentation timestamp advances by exactly 512 ticks.
- First 4,712 video frames and compressed packets match v10 exactly.
- All 11 declared visual/editorial boundaries passed transition guard. Every-frame boundary strips inspected: no stale five-row board, removed fourth/fifth-row flashes, or extra intermediate scene tails.
- Encoded first/second/third/tip highlight frames inspected at 1280×720: complete active content is visible, text is readable, tip is unnumbered, and row two includes the opposing viewpoint. Full-board opening and final standard-close frame inspected.
- All 10 source audio-cut edges fall in low-level gaps (approximately −56 to −72 dB RMS). No word-level cuts. Encoded audio at each new join correlates with the assembled source PCM at 0.999985 or better.
- Full encoded candidate transcribed and read. All three weak/better examples, rubric caveat, saved instruction, opposing viewpoint, takeaway, and close remain. No “five,” “fourth move,” “fifth move,” or separate “argue the other side” remains after the introductory lesson portion.
- ASR has minor transcription errors in unchanged speech (for example “or a crest” for “a request” in the intact summary sentence). The source transcript and untouched sentence span establish the intended wording; this is not represented as an auditory verification.
- Course MP4 and LESSON_VIDEOS entry remain unchanged. This task produced a review candidate.

Candidate SHA-256: `6e89ab7e091ace7841cb71518658f01708f263ba19d3039e0e71e9ef137f0497`.

Listening review remains needed at output 2:40.87, 3:48.77, 3:55.57, 4:02.63, and 4:08.47. These are the five new narration joins. No whole-file audiovisual KEEP/shipping verdict is claimed.
