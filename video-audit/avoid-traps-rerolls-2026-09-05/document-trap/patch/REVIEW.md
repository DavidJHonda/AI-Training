# Document Trap review candidate

Status: ready for user review, not shipped. Built September 5, 2026.

Output: `Prompts/document-trap-patched.mp4` (6,812 frames at 30 fps, 3:47.067).

## Opening and board correction

- Replaced the reroll's first 1:07.500 with live narration from 0:00 to 1:05.533. The live opening establishes the season-end tournament before asking the foul-limit question, then shows five fouls for the regular season and six for tournament play.
- Preserved the live footage through 0:57.800. From there, the current uploaded-file illustration replaces the old system-error title, which starts at live frame 1751 (0:58.367). Its full takeaway banner is highlighted at 1:00.200.
- At final 1:05.533, resume reroll source 1:07.500 and the flow walkthrough.
- Confirmed `index.html` uses `illustrations/document-trap-flow-v2.jpg`. The flow image already matched the lesson; removed the two video-only caption lines below it and restored the full-board opening view. No lesson files changed.

## Approved repairs

- Replaced uploaded-file illustration, processing flow, and four prompting moves with current lesson assets. Used full-card and full-banner border highlights, accent-matched colors, and zoom/pan walkthroughs.
- Removed the previous candidate's on-screen qualification at the user's request. Use the current lesson flow asset without added copy.
- Removed the universal processing extension, keyword-only explanation, promise that selecting pages removes search guesswork entirely, and guarantee about never missing details.
- Preserved the document/contract examples and reflection break.
- Replaced the ending with the current lesson's standard close.

## Audio cuts

| Source range removed | Join in final video |
| --- | --- |
| Reroll opening 0:00–1:07.500 replaced with live 0:00–1:05.533 | 1:05.533 |
| 2:10.667–2:22.967 | 2:08.700 |
| 2:26.433–2:36.000 | 2:12.167 |
| 3:16.500–3:19.633 | 2:52.667 |
| 3:59.633–4:05.833 | 3:32.667 |

## Verification

- Final transition guard: all 10 boundaries passed. Visually inspected all 10 new consecutive-frame transition strips; no old-graphic flashes appeared in those windows. Older strips remain as audit history; the current guard report identifies the current files.
- Inspected updated opening and flow state sheets. Both foul limits are present; the flow has no added captions. The remaining card walkthroughs and closing treatment are unchanged apart from their new output times.
- Rechecked all five joins using waveform/sample-discontinuity checks. Join-window levels range from about -57 to -67 dBFS. Speech recognition on the new live-to-reroll join confirms “...the system reading it. To avoid getting caught in the document trap...” with complete wording. Previously checked later cuts are unchanged. This is computational audio QA, not a human listening review.
- The combined audio-review reel contains overlapping excerpts from the two nearby RAG cuts; repeated words in that reel are not duplicated in the video.
- Build asserted that both source and live video hashes were unchanged. No index.html or lesson content changes were made for this candidate.

Reproduce with `scripts/video/build_document_trap_review.py`; refresh inspection assets with `scripts/video/qa_document_trap_review.py`. Exact timings and highlight geometry are recorded in `manifest.json`.
