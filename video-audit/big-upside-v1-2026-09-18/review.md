# Big Upside v1 production review

## Result

- Candidate: `Prompts/big-upside-v1.mp4`
- Source narration roll: `Prompts/big-upside-4.mp4`
- Scope: visual-only production pass
- Narration verdict carried forward: **KEEP**
- Audio edits, pauses, and narration grafts: none

## Visual work

- Replaced the protein explanation span with the canonical protein board and
  narration-timed, complete-component camera views for the string, shape and
  function, disease/drug, fold-space, and known-versus-unknown teaching beats.
- Replaced the Hassabis biography span with the canonical seven-row timeline;
  each complete row is ringed when its teaching point begins.
- Replaced the scientific-discovery and practical-help spans with their
  canonical three-card boards; complete cards and takeaway banners are ringed
  at the relevant narration onsets.
- Replaced the source close and black tail with the canonical standard close.
  At 24 fps, the house motion is adapted to a 38-frame hold, a 120-frame smooth
  push to 1.2x, and a settled final frame.

## Timing and media verification

- Source and output: 1,280 × 720, 24 fps, 8,147 decoded frames,
  339.458333 seconds of video.
- Source/output AAC packet MD5:
  `15b58a6b15b6ff2dbfd8e5546e982810` (exact match).
- One H.264 encode: CRF 18, medium preset, yuv420p. Audio is stream-copied.
- Sequential transition guard: PASS at all seven declared visual boundaries.
- Manual review: every transition strip is clean; no stale intermediate frame.
- Board state sheets: all complete components remain visible, ring strokes are
  5 px on delivery frames, and no ring covers instructional text.
- Full-output black detection: no black interval reported.
- Final output frame: canonical close, not black.

## Audit artifacts

- `manifest.json`: source/output hashes, media metadata, canonical asset hashes,
  replacement spans, and audio proof.
- `*-states.jpg`: board and close state sheets.
- `transitions/`: every-frame seam strips and the transition-guard report.
- `final-output-frame.png`: decoded literal last frame of the candidate.

The earlier first render stopped before the source audio's final packets. It is
preserved as `failed-audio-truncated.mp4` for traceability and is not the
candidate.
