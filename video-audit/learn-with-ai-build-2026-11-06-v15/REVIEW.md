# Learn with AI — v15 pacing revision

**Shipped locally, November 6, 2026; queued for batch deployment.** Candidate: `Prompts/learn-with-ai-v15.mp4`, **3:51.600**, 6,948 frames at 30 fps, 1280 × 720 H.264 / AAC, 21,159,927 bytes. SHA-256: `9bb337a8add7b13288f5a0f28e5640b88f74058b0ca8def9b1c553c278f9aac7`.

This is a narrow revision of preserved v14, rebuilt from the same pristine roll 3 and donor 2 sources. The owner explicitly said “ship it” after the listening limitation was disclosed. Installed at `course-assets/learn-with-ai/learn-with-ai.mp4`, cache `20261106ship15`, with the existing 4 min label. Local commit: `c9c5be5e9779393124bbce9e3a2a637382ffa813`. The committed video and installed video are byte-identical to this candidate. No push or deployment was performed. Direct listening and full-speed audiovisual review remain outstanding, including the new narration join at 1:45.600. This report does not upgrade those checks to passes.

## Three requested changes

| V14 position | Revision | V15 position |
| --- | --- | --- |
| 1:45.600–2:00.200 | Remove the added facts-versus-theory comparison and its visual sequence. The preceding board already explains choosing between a study tool and learning coach. The teacher-check line now leads directly into “Let's focus entirely on the study tool track.” | New join at 1:45.600 |
| 2:21.000–2:25.000 | Keep How Gemini Notebook Works and its You Upload outline instead of the repeated laptop drawing. | 2:06.400–2:10.400 |
| 2:55.600–2:59.600, including 2:57 | Keep the complete Give It the Full Picture card and its outline instead of the repeated drawing. | 2:41.000–2:45.000 |

The cut removes 14.600 seconds. Neither board replacement changes audio. The source wording and exact frame plan are in `EDIT-PLAN.md`; the full assembly and protected hashes are in `edit-manifest.json`.

These continuous board views intentionally follow the owner's request. How It Works now stays visible for 24.033 seconds; Four Moves for 42.267 seconds with its introduction and successive complete-card views before the citation diagram. The first board's longest uninterrupted run remains 19.300 seconds (37.300 seconds total). No extra supporting image was introduced merely to interrupt the boards. Other v14 visual treatments remain, including the standard close, now starting at frame 6,583 / 3:39.433.

## Verification of the actual v15 file

- Full sequential decode: 6,948 frames, uniform PTS increments, correct dimensions and frame rate. Encoded audio duration 231.616 seconds, within 16 ms of video.
- Fresh encoded ASR: 682 words; both removed sentences absent; all six required passages, complete output list including audio/video overviews, history/math example, full quiz instruction, citation teaching, coach process and both closing lines remain. See `encoded-transcript/learn-with-ai-v15.txt` and `qa/required-passages.json`. ASR is wording evidence, not a listening pass.
- Pre-encode PCM is identical to v14 with the selected interval removed, except for the 8 ms ramps at the new join. The two visual-only repairs have no audio changes. See `audio-preservation.json`.
- Encoded audio correlation to the intended assembly: 0.999986; peak −1.513 dBFS. All five joins occur inside measured quiet intervals. New join quiet interval: 1:45.080–1:46.030, approximately 0.950 seconds at −40 dB. No added pause. Evidence in `qa/joins.json` and `qa/silence.log`.
- Transition guard passes all 23 declared boundaries, including the former cutaway endpoints. Every-frame strips around the new cut, its adjacent reused-scene boundary, and all four former cutaway endpoints were inspected. No leftover comparison frames or repeated-drawing flashes at the repaired spans were observed. Full-size frames on both sides of the new cut, both retained-board spans, and the final frame were inspected.
- V14, raw sources, lesson Markdown and canonical JPGs remain hash-identical. See `qa/verification.json`.

The current page's essential tool distinction is taught before the cut; the deleted comparison is additional repetition rather than a missing lesson requirement. Existing v14 narration paraphrases remain, including “websites” without separately saying “articles” in the upload list. No broader teaching rewrite or full-speed playback is claimed for this narrow repair. The external tracker was not consulted or modified.

Build: `.video-venv/bin/python scripts/video/build_learn_with_ai_v15.py`. Check: `.video-venv/bin/python video-audit/learn-with-ai-build-2026-11-06-v15/verify_candidate.py`. Preserve this candidate if further revisions are requested.

## Local shipping checks

`python3 scripts/verify-course-assets.py --migration-hashes` passed: 248 retained assets, 519 mappings, 263 website references and 55 finished videos. The commit contains only this video, its manifest hash/size, its lesson cache reference and its registry shipping status. Unrelated working changes were left outside the commit. See `shipping-verification.json`.
