# Loudest Voices v13: match the two-example lesson

**Shipped locally on David’s explicit “Ship it” approval; queued for batch deployment.** Commit `ab801cb702afcc9d963d7e06c393e38387695fdb`. See `SHIP.md`. The review below records the pre-shipping evidence and disclosed listening limitation. Video Tracker was not accessed or changed.

Candidate: `Prompts/loudest-voices-v13.mp4`, 3:56.133, 7,084 frames at 30 fps, 1280×720. This removes 40.600 seconds from v12. `changed-section.mp4` is a 50-second review excerpt beginning at candidate 1:38.

## Narrow edit

| v12 source time | Removed narration |
|---|---|
| 1:52.900–1:58.567 | “This chart looks at four major historical predictions regarding world-changing technologies.” |
| 2:07.933–2:27.867 | The complete Steve Ballmer/iPhone and Robert Metcalfe/internet-collapse examples. |
| 2:37.600–2:52.600 | “So why were they all wrong?”, the hard-to-predict explanation, the deleted banner line, and the redundant machines-versus-human-adaptation setup. |

The two retained examples lead directly to “A technology becomes the future only when people change their habits around it. Machines improve fast. Habits change at human speed.” No generated narration or new pauses.

## Board and camera treatment

| Board | Highlighting | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| This Has Happened Before | Unmarked introduction; purple whole-card outline for online shopping; amber whole-card outline for flying cars. Fixed 4px delivered strokes. | Complete compact board at full view throughout. | Candidate 1:42.133–2:12.000 (29.867 seconds), then the retained habits animation. | The new two-card page asset is legible at full view. Replaces the old four-prediction timeline as well as the old four-card board. No removed examples or banner remain visually. |

The original habits animation resumes at source 2:52.600, under the retained habits paragraph. Its motion and timing after that point are retained. The experts, In Your Hands, and closing treatments are unchanged.

## Sources and assembly

- Stable source: `Prompts/loudest-voices-v12.mp4`; SHA-256 `31a18fc49cc76e576ea736d23160bc516f486e9160df6557c5f0a018ad4edc37`.
- Canonical board: `course-assets/loudest-voices/loudest-voices-missed-predictions.jpg`, 1600×799; SHA-256 `c43b3168ec52d1b90b84dd12e4cb80dc5c6aebd75c364cbe7ff47374c57be681`.
- Candidate SHA-256: `21542eafdd39fa9ec4740b1c3d7c0cb5fad23a0d6f914c289775a3e4755751da`.
- All 6,125 unaffected H.264 packets match v12 byte for byte; timestamps after the cuts are shifted exactly. Only the changed board and its adjacent GOP tail are encoded (959 frames).
- Reconstructed the pre-AAC audio from hash-verified v8 and In Your Hands v6 donors using the retained v10/v12 assembly plans. Correlation to v12: 0.999829. The new cuts use 5ms fades in measured quiet handles and one AAC encode. Source hashes and frame mappings are in `edit-manifest.json`.

## Verification and limits

Passed: full sequential decode, exact frame count and constant presentation timing, byte identity of unaffected video packets, all 896 board frames compared with the expected canonical state, audio correlation 0.999820 to the planned edit, and transition guard at all five assembly boundaries. Visually inspected both settled ring frames at full resolution, the contact sheet, and all five every-frame boundary strips. Complete board and title remain visible; neither card is cropped.

Fresh transcription of the edited excerpt confirms both retained examples and the complete habits paragraph, with the removed examples and repeated explanation absent.

Audio cut endpoints were measured in quiet gaps. Encoded joins have 10ms RMS levels of -61.1, -77.8, and -70.8 dBFS, with negligible sample discontinuities. These measurements do not establish that the cuts sound natural.

**Listening has not been performed.** Review the three new joins at candidate **1:52.900, 2:02.267, and 2:12.000** (14.900, 24.267, and 34.000 seconds into the excerpt). At candidate handoff, full watch/listen and shipping approval were pending. David subsequently explicitly authorized shipping after that limitation was disclosed. Assistant listening was not performed; no listening pass is retroactively claimed.

Build: `.video-venv/bin/python3 scripts/video/build_loudest_voices_v13.py`.

QA: `.video-venv/bin/python3 scripts/video/qa_loudest_voices_v13.py`.

Fresh transcription: `.video-venv/bin/python3 scripts/video/transcribe_selected_videos.py video-audit/loudest-voices-two-examples-2026-11-03/changed-section.mp4 --output-dir video-audit/loudest-voices-two-examples-2026-11-03/transcripts`.
