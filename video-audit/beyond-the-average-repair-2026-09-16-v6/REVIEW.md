# Beyond the Average v6 — narrow narration repair

**Candidate:** `Prompts/beyond-the-average-v6.mp4`  
**Source:** `Prompts/beyond-the-average-v5.mp4` (`56e10d9067e5e662de1dde7b74aab421638c665d3527474c61d1b3403895d493`)  
**Output:** 2:47.13, 5,014 decoded frames, 30 fps, 1280×720, AAC mono 48 kHz  
**Output SHA-256:** `a86b7068fe6f28d302628d1161e71beded50b235096b1dc5c6de479ddf6860a4`  
**Scope:** approved narrow repair only; review candidate, not published.

## Approved change

Removed the complete v5 narration sentence at 0:50.58–0:54.04:

> The work only becomes valuable when you find a way to take it further.

The sentence incorrectly changed “the common AI output is not a differentiating
advantage” into “the output has no value.” No replacement narration was needed.
The repaired sequence is:

> “…the software itself offers no competitive advantage.” → pause → “The
> difference is what you add.”

Audio 0:50.1667–0:55.0000 and visual frames 1505–1658 from v5 were removed.
The removed Notebook handwriting scene was replaced by a 16-frame hold on the
preceding data-center frame. The hold uses 0.5333 seconds of matched nearby room
tone from v5 0:54.090–0:54.633, joined with 5 ms crossfades. The existing Same
Tool board begins at output frame 1521, with nine cloned full-board frames so the
board is already visible while the preserved audio approaches “The difference.”

## Affected board plan

| Board | Highlighting | Camera | Reason |
| --- | --- | --- | --- |
| Same Tool. Different Advantage. | Unmarked throughout | Complete full board, still | The narration teaches one whole-board point. v6 brings the already-approved board in directly after the repaired pause; no later treatment changes. |

All later visuals and their relationship to narration retain v5's timing. The
dense What to Start Building Today board, its four complete-card dives and rings,
its takeaway pullback, and the standard close are unchanged except for the global
4.3-second timeline shift caused by this deletion.

## Verification

- Full sequential decode: 5,014 frames, matching plan; exact 30 fps and 1280×720.
- Fresh complete transcript: the rejected sentence is absent, no neighboring word
  is missing, and the intended join is present.
- Repaired pause measured with `silencedetect` at −35 dB: 0:50.1576–0:51.3705,
  **1.2129 seconds**, matching the approved approximately 1.2-second target.
- `transition_guard.py`: PASS at all eight declared boundaries. Manual inspection
  of every strip confirms the pause is a continuous held data-center frame; frame
  1521 is already the complete Same Tool board; no stale handwriting frames or
  short visual islands remain. The retained downstream board and close seams also
  remain clean.
- Fresh full-file transcription retains every previously approved teaching beat
  and both closing lines. Narration content verdict after the repair: **KEEP**.
- v5 remains unchanged. The canonical live video, lesson Markdown, current board
  assets, and `index.html` were not edited. v6 was not deployed.

## Listening limitation

This environment did not expose audible playback. ASR, word timestamps, signal
measurements, and visual strips verify the edit structurally, but they do not
certify cadence, a click-free audio crossfade, or voice continuity by ear. Before
shipping, David should listen to roughly 0:49.5–0:52.5, especially the pause and
the onset of “The difference is what you add.” The rest of the candidate inherits
v5's previously listed listening requirements.

## Build and QA

- Build: `PYTHONDONTWRITEBYTECODE=1 .video-venv/bin/python scripts/video/build_beyond_the_average_v6.py`
- Manifest: `edit-manifest.json`
- Transition report: `guard/transition-guard.md`
- Fresh transcript bundle: `/tmp/beyond-average-v6-final-review/beyond-the-average-v6/`

