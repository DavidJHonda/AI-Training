# When You Need More — v8 review build

Built November 7, 2026 on the owner's “agree. Build the video please.” following the donor-graphics review. This is a narrow visual-only engagement repair. Candidate: `Prompts/when-you-need-more-v8.mp4` (168.97 seconds, 1280×720, 30 fps). It is built for review; the installed v7, page, narration, source rolls, canonical assets, and lesson remain unchanged.

## Result

Two animated donor inserts and the previously approved college comparison illustration replace 26.6 seconds of comparison-board footage. The longest uninterrupted board hold falls from 37.23 seconds to 18.37 seconds. Total time on the three comparison boards falls from 82.63 seconds to 56.03 seconds. Runtime and audio are unchanged.

| Current output | New picture | Source and treatment |
|---|---|---|
| 1:37.00–1:46.90 | Steps develop, rearrange, and lead to an answer | Roll 7, 1:59.00–2:08.90, native speed. Native boxes, connections, reveals, and answer lines remain. Moving labels become Steps / Options / Weigh / Check. Main labels become Your task / More thinking / An answer. “Verified Output” is removed and replaced with “Review before using.” |
| 2:22.00–2:28.33 | Highlighted passages from websites feed into a report | Roll 9, 3:05.50–3:11.83, native speed. Preserves the moving cursor, highlights, page changes, and report reveal. Ends before the donor's generated course board. |
| 2:28.33–2:38.70 | Texas A&M versus UT Austin physics comparison | Approved illustration from the October 8 v3 edit. Gentle 3.5% push, keeping university names and comparison categories in frame. Returns to the current board for costs and “Show your sources.” |

The scheduling donor remains a possible later adaptation: its existing three-track technical workflow does not depict this lesson's four people, one week, and two video editors. The present build uses the direct-fit research footage and college illustration, plus the successfully repaired thinking animation.

## Board and camera treatment

The original current JPGs and v7 highlighting are preserved. All comparison boards remain compact/full view, with no new pauses or zooms. The normal closing hold/push/settle remains.

| Board | Highlighting | Onscreen / break |
|---|---|---|
| Which Model? | Existing complete-card and example outlines, unchanged | 0:46.10–1:01.73; 15.63-second hold |
| How Much Thinking? | Existing Less Thinking description and example, then More Thinking description and example | 1:18.63–1:37.00, animation until 1:46.90, board through 1:55.87. Longest hold: 18.37 seconds. |
| How Much Research? | Existing Regular Chat description/example and Deep Research description/example | 2:11.53–2:22.00, animation then college illustration through 2:38.70, board until 2:41.30. Longest hold: 10.47 seconds. |

Pristine donor visuals and the existing build recipe were used for one final visual encode. The installed v7 AAC stream was copied directly; no new audio encode, edit, splice, or pause was introduced. The generated WAV in the build scratch is not the candidate's audio source.

## Verification

- All 5,069 encoded frames decode, with continuous 30 fps timestamps and the expected resolution.
- AAC packet bytes **and packet timestamps/durations** match installed v7 exactly. Audio SHA-256: `e30f800289549c353ea1008d26331406d0a3b973148a0d7593745d7cf04ad4a7`.
- All 17 declared boundaries pass the transition guard. Encoded before/after boundary frame sequences were visually inspected; no leaked donor board is visible.
- Encoded insert sequences, repaired labels, answer-panel reveal, report final state, college framing, and literal closing frame were inspected. The moving labels are tracked to their native boxes.
- Every retained frame was compared against installed v7 after reduction to 320×180. Mean absolute error averaged 0.026/255; maximum 0.826/255. This is consistent with re-encoding, with no identified unintended picture change.
- All protected hashes match. Corner cleanup declined no retained donor frames: 297 cloned and 190 glyph-inpainted insert frames.
- Candidate SHA-256: `00c4017e56f02002441fbe5c55dfee5759a013a201b476a47a72f07b7b49445b`; 28,377,902 bytes.

Evidence: `qa.json`, `edit-manifest.json`, `label-tracking.json`, `encoded/`, `encoded-inserts-*.jpg`, `boundary-review-*.jpg`, `answer-reveal-check.jpg`, and `transitions/`.

Limitations: no continuous audiovisual listening pass was completed. Browser playback verification was unavailable: the sandbox disallowed a local HTTP listener and browser policy rejected the local-file URL. No workaround was attempted. Complete file decoding and visual frame-sequence inspection are reported separately from playback/listening. Video Tracker was not accessed or changed.

## Review artifacts

- Full candidate: `../../Prompts/when-you-need-more-v8.mp4`.
- `before-left-after-right.mp4`: 41-second comparison with installed v7 on the left and v8 on the right. Covers 1:32–1:50 and 2:19–2:42; audio is from the candidate. This comparison is a review excerpt, not the delivery video.
- Builder: `../../scripts/video/build_when_you_need_more_v8.py`.
- Verification: `../../scripts/video/qa_when_you_need_more_v8.py`.

Status: **built and technically verified for review; not installed or published**.
