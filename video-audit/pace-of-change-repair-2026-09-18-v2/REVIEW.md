# Pace of Change — repaired candidate review

## Recommendation

**Repair completed; conditional Keep after the required human listening pass.**

The repaired candidate preserves roll 2 as the base, restores the complete AGI explanation from the existing course video, uses the two exact closing lines from roll 1 without “And right now,” replaces the course-board visuals with the current canonical assets, and ends on the canonical close. Visual, transcript, timing, level, frame-count, and transition checks passed. This environment cannot directly audition audio, so the narration joins and delivery remain explicitly unverified by ear.

Candidate: `Prompts/pace-of-change-v2.mp4`

## Sources and identity

- Base: `Prompts/pace-of-change-2.mp4`
  - SHA-256: `c80f2401a71f25dddee35386588671d413cdd1347eb075bc1a944da842e49ab7`
- AGI donor: `course-assets/pace-of-change/pace-of-change.mp4`
  - SHA-256: `28efd24c23ce3a45d0d1a058f841730c97f40ef260a815a3c67965a6a9018da2`
- Closing-line donor: `Prompts/pace-of-change-1.mp4`
  - SHA-256: `bfa5ec760273799f727594eb7f36b7dd35bb69802eb0647f535cbb1d247dc6cc`
- Candidate SHA-256: `75f65a59ef5d8b44115e4cca16972d5f053388790ced701dbc27370228ee6ff9`
- Candidate length: 7,558 decoded frames at 30 fps, 251.933 seconds (4:11.93)

## Narration repairs

### Complete AGI explanation

- Original donor: frames 6,305–6,881 (3:30.17–3:49.37) from the current course video.
- Output: frames 6,281–6,857 (3:29.37–3:48.57).
- Restored teaching:
  - AGI usually means human-level ability across many kinds of cognitive work.
  - There is no agreed finish line.
  - No universally accepted definition or test proves that a system has achieved AGI.
- The transcript then continues into roll 2’s ASI definition and the conclusion that nobody knows whether either milestone will be reached.

### Exact close from roll 1

- Line 1 donor: frames 6,542–6,624 (3:38.07–3:40.80).
- Line 1 output: frames 7,296–7,378 (4:03.20–4:05.93).
- Deleted donor words: frames 6,624–6,647, “And right now.”
- Line 2 donor: frames 6,647–6,702 (3:41.57–3:43.40).
- Line 2 output: frames 7,383–7,438 (4:06.10–4:07.93).
- Final wording:
  - “AI keeps getting faster and more powerful.”
  - “Nobody is sure where it stops.”

### Selective pauses

- The pre-close extension is frames 7,286–7,296: 10 frames (0.333 seconds) of matched room tone. Combined with the source and donor silence, it gives the conclusion a deliberate transition without applying an automatic one-second pause.
- The reconstructed break between closing lines is frames 7,378–7,383: 5 frames of matched room tone, combined with donor head/tail silence.
- The earlier v1 candidate cut eight frames too early and touched the trailing sibilant in “milestones.” This v2 cut lands inside measured silence. At frame 7,286, the encoded audio measures −53.19 dBFS in the preceding 10 ms and −62.46 dBFS in the following 10 ms.

## Visual and production result

- The four current canonical course boards replace the generated board renders.
- Board emphasis follows the narration:
  - 2023 vs. 2026: Answering, Images, Context Window, Doing.
  - Why So Fast?: Better Training, More Compute, AI Helps Build AI.
  - Could AI Improve Itself?: Automated AI Research, Self-Improving AI, then the distinction banner.
  - How Far Can AI Go?: AGI, ASI, then the uncertainty banner.
- The longest uninterrupted board run is 2,554 frames (85.13 seconds), covering the two future-facing boards. This is an intentional exception: the narration actively walks the board content and the approved plan avoids tiny-text interstitials.
- The final frame is the canonical close with both conclusion lines legible.
- Corner-mark cleanup cloned 1,084 source frames; no frame required inpainting and none were declined.

## Verification performed

- Sequentially decoded all 7,558 output frames.
- Automated transition guard passed all 13 declared boundaries; every generated boundary strip was also reviewed manually.
- Whole-video contact sheets were reviewed from the opener through the settled close.
- Transcript verification confirms the essential lesson sequence, the complete AGI distinction, the ASI definition, the uncertainty conclusion, and both exact closing lines.
- Active speech RMS after encoding:
  - base before AGI: −13.56 dBFS
  - AGI donor: −13.55 dBFS
  - base after AGI: −13.35 dBFS
  - closing line 1: −14.25 dBFS
  - closing line 2: −13.56 dBFS
- All protected sources and lesson materials matched their hashes at successful render completion. A concurrent user edit to `index.html` triggered the first protection check; it was preserved untouched, and the render was rerun against its current hash.

Supporting evidence:

- `edit-manifest.json`
- `qa-metrics.txt`
- `silencedetect.txt`
- `transitions/transition-guard.md`
- `transitions/all-boundaries.jpg`

## Required listening check

This environment could analyze decoded audio, silence, levels, and speech recognition but could not directly hear the finished video. Before publishing, listen to:

1. 3:29.37 and 3:48.57 — both AGI graft joins and voice continuity.
2. 4:02.5–4:03.5 — the repaired “milestones” transition into the close.
3. 4:03.20–4:07.93 — both closing lines, their relative level, and the reconstructed break.

The candidate has not been deployed or substituted for the live course video. The superseded v1 candidate and its audit were retained rather than deleted.


## Shipped

**SHIPPED 2026-09-18** on David's approval ("ship pace-of-change-v2"): v2 copied to `course-assets/pace-of-change/pace-of-change.mp4` (SHA-256 verified before and after the copy, `75f65a59…`), v1 and v2 candidates removed, `index.html` cache key `?v=2` → `?v=20260918ship1` and the pill 5 min → 4 min, `course-assets/manifest.json` entry updated. See `shipping-receipt.json`.
