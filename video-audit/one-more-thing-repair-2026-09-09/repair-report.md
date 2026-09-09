# One More Thing — version 2 repair

Review output: `videos/one-more-thing-v2.mp4`

Duration: 3:36.73 (6,502 frames, 1280×720, 30 fps). Original: 4:06.13. This is a review candidate; the live lesson video has not been replaced.

## Changes

- Replaced generated teaching visuals with the three exact current lesson boards: Same Probabilities, Different Choices; How Temperature Changes the Odds; The Math Adds Up Fast.
- Added narration-timed course highlights to the active rows, comparisons, cards, and takeaways. Source timing and exact rectangles/colors are recorded in `edit-manifest.json`.
- Removed the low-temperature restatement and prediction aside, the direct-control/safe-text restatement, the duplicate two-trillion calculation, and the old-work aside.
- Preserved the probability explanation, 22-out-of-100 example, five independent tries, variety and changing context, both temperature examples, unchanged learned weights, and all three calculation totals.
- Added four one-second room-tone pauses between ideas, plus a short natural join after the repeated calculation was removed.
- Replaced the generated ending with the current standard closing board and its standard hold/push/settle treatment.

## Verification

- Finished MP4 decodes successfully. Frame count, dimensions, FPS, and encoded audio format verified.
- Original source SHA-256 matches the pre-edit manifest.
- Transcribed the final encoded MP4 and read the complete result (`final-transcript.txt`). Sentences remain complete across the cuts; the key examples and closing line remain.
- Transition guard passed all 13 declared edit/board boundaries. Inspected the every-frame boundary strips, grouped in `transition-audit/review-group-*.jpg`: no old graphic or intermediate shot appears at a join. The first destination frame is an approved board or close.
- Inspected full-resolution highlight states and the final encoded closing frame. Full boards, card edges, percentages, and banner text remain visible. Repeated states use identical visual geometry.
- Encoded state snapshots were compared with the rendered PNGs. The initial strict mean-pixel-difference threshold of 3 flagged five math states at 3.028–3.076/255. Inspection of the encoded math frame confirms the intended board and highlight; these small encoding/color differences do not indicate a wrong shot. Raw measurements are retained in `encoded-frame-check.json`.
- Measured quiet intervals in final encoded audio: before temperature 98.200–99.625 (1.425 s); before high temperature 119.815–121.139 (1.323 s); before computation 148.852–150.139 (1.288 s); before close 207.542–208.776 (1.234 s). These include the inserted one second plus adjacent source quiet. The shorter calculation join is 184.479–185.306 (0.827 s).
- Audio joins use quiet source handles, matched room tone, and 5 ms edge fades. Narration was checked through transcription and waveform analysis; a full human playback listening pass remains part of owner review. This report is a repair record, not a final ship grade.

## Reproduce

Run `.video-venv/bin/python scripts/video/build_one_more_thing_review_repair.py` from the repository root. The script preserves the original source and writes only the review candidate and audit artifacts.
