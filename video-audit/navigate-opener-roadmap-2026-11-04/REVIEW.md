# Navigate the Future opener — current roadmap repair

Scope: replace only the roadmap visuals with the current canonical board named in `index.html`. User requested no other changes.

Candidate: `Prompts/navigate-the-future-opener-v10.mp4`.
Source: the installed v8, retained at `Prompts/navigate-the-future-opener-v8.mp4`; its SHA-256 matches the canonical video at task start. Source and board hashes are in `edit-manifest.json`.

| Board | Highlights | Camera | Output spans |
|---|---|---|---|
| Navigate the Future | The Argument, Monsters and Open Water, Where It Lands on You, then takeaway banner; original onsets | Original full view with gentle 1600-to-1578-pixel push | Frames [3092,3555) and [3696,4117), 103.067–118.500 and 123.200–137.233 seconds |

Original 4.7-second monitor/seedling cutaway retained at frames [3555,3696). The longest continuous roadmap span is 15.433 seconds. The seven-frame opening hold is retained. The canonical JPG is placed at [0,55] on the existing 1600×900 canvas, preserving its 1600×789 dimensions. Geometry and timing come from the original map leg, traced through the v6 and v8 edit manifests and checked against the actual source frames.

Audio is copied directly. The narration still says “embrace the future” at approximately 106–107 seconds; this is deliberately outside the requested board-only repair. No cuts, pauses, new illustrations, or close changes.

Build: `.video-venv/bin/python scripts/video/build_navigate_opener_v10.py`
QA: `.video-venv/bin/python scripts/video/qa_navigate_opener_v10.py`

The first render (v9) failed the frame-count check because timestamp handling dropped six frames. It is rejected. v10 normalizes each branch to a 1/30 timebase, including the opening hold.

Verification passed on v10: 4,370 decoded frames at 30 fps (145.667 seconds); the copied AAC stream hash exactly matches v8. All 3,486 frames outside the replacement spans match source timing, with mean pixel error 0.592/255 from encoding. All four transition guards passed and their every-frame strips were visually inspected. Full-view opening, all four settled highlight states, original cutaway, and closing frames were inspected; no clipping or stale roadmap frames were found. See `qa.json`, `after-contact.jpg`, and `transitions/`. This is a narrow review candidate, not a whole-video production pass. No end-to-end listening review, installation, commit, or deployment is claimed. Video requires one encode from the surviving finished source; retained frames may have ordinary compression differences.
