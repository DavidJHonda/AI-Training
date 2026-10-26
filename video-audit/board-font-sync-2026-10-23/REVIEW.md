# Board font synchronization — October 23, 2026

Three review candidates use the current approved board JPGs. The source highlight timing, colors, stroke weights, camera paths, cutaways, narration, duration and frame timestamps are preserved. No installed video, lesson, board asset, or index entry was changed.

| Candidate | Updated board | Board interval (30 fps, end exclusive) |
| --- | --- | --- |
| `Prompts/honesty-and-privacy-v7.mp4` | Using AI in School | 674–1676 (0:22.47–0:55.87) |
| `Prompts/wheres-the-line-v5.mp4` | How DraftKings Uses AI | 2898–3915 (1:36.60–2:10.50), excluding original cutaways |
| Same candidate | Making the Responsible Choice | 4370–5798 (2:25.67–3:13.27), excluding original cutaways |
| `Prompts/people-skills-v8.mp4` | Your Next Move | 798–1071 (0:26.60–0:35.70) |

## Validation

All three candidates have exactly the original AAC packet bytes and timestamps, identical decoded audio, and identical video frame timestamps. Resolution remains 1280×720 at 30 fps. Durations remain 230 seconds, 201.9667 seconds, and 127.6667 seconds respectively.

Every frame was decoded and checked. All video packets and decoded pixels outside the replacement GOP intervals are identical to the source: 5,657 frames for Honesty & Privacy, 4,004 for Where's the Line?, and 3,412 for People Skills. The original cutaways in Where's the Line? were copied without re-encoding.

The finished sources were frozen before editing. For clean GOP joins, 241 surrounding frames in Honesty & Privacy and 145 in People Skills required another encode; their minimum PSNR versus the original exceeds 51 dB. The original footage was retained in these handles. Every replacement frame matches the intended current-board render, with minimum RGB PSNR above 35 dB.

All highlight states and all 33 transition strips were visually inspected. The transition detector passed all boundaries in Honesty & Privacy and People Skills. In Where's the Line? it flagged five continuous camera moves (4569, 4907, 5132, 5408, 5681); every flagged strip was inspected and contains the retained pan/zoom rather than a transient old graphic. The raw detector results remain preserved, with the manual resolution recorded separately in `qa.json`.

No direct audio listening or full real-time playback was performed. Audio identity was verified computationally. These are review candidates, not a claim of a fresh full-video shipping review.

## Reproduction and evidence

`scripts/video/build_board_font_sync.py` recreates each candidate from the frozen finished source and current canonical JPGs, using the retained board camera/highlight specifications. It refuses to overwrite an existing candidate. `scripts/video/qa_board_font_sync.py` checks source preservation, all frames, audio and transition boundaries. The `--reviewed-motion-flags` option is only for the five visually inspected Where's the Line? camera-motion flags.

Each lesson folder here contains its manifest, exact candidate/source hashes, board specifications, QA results and transition evidence. The original course files remain protected by recorded hashes. No publication, installation, commit or push was performed in this pass.

## Local installation

The owner approved installing these exact three candidates. Installed and hash-verified all three canonical MP4s; updated only their cache keys in `index.html`. Local commit: `fbc174494c1eb76ea7a0122df2149d222ecc1671`. Status: **shipped locally; queued for batch deployment**. No push or deployment performed. The earlier full-playback/listening limitation remains disclosed; this release installs the approved narrow visual repair. Exact installed hashes and references are in `shipping.json`.
