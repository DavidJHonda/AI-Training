# Document Trap: remove pause-video instruction

Shipped September 6, 2026: `videos/document-trap.mp4`.
Approved review candidate was moved from `Prompts/document-trap-patched.mp4` into the existing live filename. SHA-1 verified unchanged: `172a8292130209aea9322485f7e7b846f88fadb9`.

The previous live video and unused reroll were moved to recoverable Trash:
`/Users/davidobrien/.Trash/AI-Training-document-trap-unused-20260906-vayRxd/`.
No `index.html` changes were made during shipping.

- Removed pristine reroll frames [6254,6332), 3:28.467–3:31.067: “Take a moment and pause this video,” including the surrounding breaths.
- The new join is at final 3:01.500. Retains the complete preceding “original text” and the following “Think of a long, complex document…” sentence.
- Held the full quote card through the preceding sentence, then cut directly to the existing document graphics. Removed the otherwise split-second takeaway state created by shortening this span.
- Rebuilt from pristine sources; no stacked video patch. New duration: 6,734 frames / 30 fps = 3:44.467 (2.6 seconds shorter).
- All 10 output transition checks passed. Inspected the new join and the shifted downstream cut and closing strips: no intermediate old graphics.
- Final-output audio-cut-5 speech recognition confirms complete wording on each side, with the pause instruction absent. The 20ms join window measures -60.0 dBFS, with a 0.00081 sample discontinuity. These are computational audio checks, not a human listening review.
- Source reroll, live video, and lesson page remain unchanged.

Exact timing and final QA: `manifest.json`, `qa/`, and `transitions/`.
