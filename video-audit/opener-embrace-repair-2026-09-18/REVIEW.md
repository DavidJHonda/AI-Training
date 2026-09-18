# Embrace the Future opener — v3 production review

## Status

- Candidate: `Prompts/opener-embrace-v3.mp4`
- SHA-256: `83e97ae29f8ad80b66fc393f11dbb699bc460e7e9474e301091c2ea139b81c45`
- Scope: full production pass, visual-only. No narration edits, audio grafts, cuts, or added pauses.
- Narration verdict inherited from the selected roll: **KEEP**, with the pronunciation/listening gate below still open.
- Candidate status: ready for David's review; **not cleared to ship or publish**.
- Superseded review renders: `Prompts/opener-embrace-v1.mp4` and `Prompts/opener-embrace-v2.mp4`. They were retained and must not be mistaken for the selected candidate.

## Sources

| Role | File | SHA-256 |
|---|---|---|
| Narration and timing base | `Prompts/opener-embrace-4.mp4` | `90307f27c1e1b357a13bd3d5b4cb5add68482e38fa9d07e9330a96c4709f73b4` |
| Early Notebook drawing donor | `Prompts/opener-embrace-3.mp4` | `ae2bc089f39db8eeb3f94c8f380a0ebb693762f6fe531b16287ae1aeb501ed9b` |

The Magellan drawing is a clean crop from source-roll frame 1950. Canonical course assets and hashes are recorded in `manifest.json`.

## Narration review of the exact candidate

The candidate audio is bit-identical to the selected roll, and its complete timestamped transcript is retained at `candidate-bundle/opener-embrace-v3/transcript.txt`.

| Essential teaching | Result | Candidate evidence |
|---|---|---|
| Four competing AI claims; nobody knows who is right | RICH | 0:00.00–0:10.36 |
| Student already knows how to use AI and understand the engine; goal is to be smarter than the tool | TAUGHT | 0:10.36–0:21.04 |
| Optimist, Worrier, and Doubter positions | RICH | 0:21.04–0:42.20 |
| Honest conclusion: nobody knows, including AI builders | RICH | 0:42.20–0:47.76 |
| Old mapmakers filled unknown water with monsters | RICH | 0:47.76–1:00.36 |
| Worriers see destructive monsters; Optimists see easy open water | RICH | 1:00.36–1:11.88 |
| Sailors usually found the unexpected; Magellan example and outcome | RICH | 1:11.88–1:27.84 |
| Take both views seriously; AI is here to stay, not guaranteed to improve forever | RICH | 1:27.84–1:39.88 |
| Section map: The Argument; Monsters and Open Water; Where It Lands on You | RICH | 1:39.88–2:04.48 |
| Required two-line close, in order, with no later narration | MET | 2:04.48–2:09.40 |

Source QA: PASS. The current `index.html` lesson and `lessons/Opener-Embrace.md` agree on the essential teaching.

### Remaining narration/listening gate

Direct audio monitoring is unavailable in this environment, so I could not personally hear the finished file end to end. Two ASR passes render the required term **Worrier** as “warrior” at approximately 0:34.76–0:37.44 and the plural as “warriors” at 1:00.36–1:02.60. Context and visuals are correct, but David must listen to those two passages and confirm the spoken vowel/word before shipping. Because the candidate copies the source AAC packets unchanged, this is the same unresolved pronunciation check as source roll 4, not a new edit seam.

## Finished visual treatment

| Output span | Treatment |
|---|---|
| 0:00.00–0:10.42 | Current `WHAT EVERYONE'S SAYING` asset. Complete unmarked board for 2.00 seconds, then a purple whole-card outline. |
| 0:10.42–0:47.50 | Six clean Notebook line-art crops supporting use AI, understand the engine, uncertain future, Optimist, Worrier/Doubter, and the honest conclusion. No stock photography, course-board recreation, or visible engine corner mark. |
| 0:47.50–1:19.00 | Current `The Edge of the Map` asset at full view. Red outline on the stormy half at the Worrier explanation; teal outline on open water at the Optimist explanation. |
| 1:19.00–1:28.08 | Notebook's ship-and-Magellan drawing for the Magellan example. |
| 1:28.08–1:39.62 | Return to the unmarked current edge illustration for the two-views/AI-is-here-to-stay conclusion. |
| 1:39.62–2:04.33 | Current `Embrace the Future` section map, full view. Unmarked opening, then one outline at a time on the three rows and takeaway banner at their spoken onsets. |
| 2:04.33–2:12.54 | Canonical standard close with 24 fps-equivalent hold/push/settle motion; it is the literal final frame. |

Longest unbroken course-board run: 44.46 seconds, from the edge-board return at 1:28.08 through the close. Notebook spans used: 0:10.42–0:47.50 and 1:19.00–1:28.08.

## Technical verification

- Source and candidate: 1280×720, 24 fps, 3,181 decoded frames, 2:12.61 container duration, 12,288 video timebase.
- Copied AAC packet MD5: `8ed09032c56e4cd2514e059580492904` for both source and candidate.
- Decoded PCM MD5: `a2de3797e3630b3d9fdea95032a774a9` for both source and candidate.
- Transition guard: PASS at all 11 declared visual splices; all boundary strips were manually inspected. Report: `transition-guard-v3/transition-guard.md`.
- Full-file visual pass: all three four-second contact sheets were inspected. Files: `final-frames-v3/`.
- Exact-candidate transcript/scenes/holds bundle: `candidate-bundle/opener-embrace-v3/`.
- No pause changes to measure; no audio joins or grafts to inspect.

## Reproduction

```sh
.video-venv/bin/python scripts/video/build_opener_embrace_v3_review.py
.video-venv/bin/python scripts/video/transition_guard.py Prompts/opener-embrace-v3.mp4 \
  --boundary 250:opening-to-use-ai --boundary 420:use-ai-to-engine \
  --boundary 507:engine-to-uncertain --boundary 672:uncertain-to-optimist \
  --boundary 835:optimist-to-worrier --boundary 1014:worrier-to-honest \
  --boundary 1140:notebook-to-edge --boundary 1896:edge-to-magellan \
  --boundary 2114:magellan-to-edge --boundary 2391:edge-to-map \
  --boundary 2984:map-to-close \
  --outdir video-audit/opener-embrace-repair-2026-09-18/transition-guard-v3
.video-venv/bin/python scripts/video/frames.py Prompts/opener-embrace-v3.mp4 \
  video-audit/opener-embrace-repair-2026-09-18/final-frames-v3 --sheet
```

Publishing was not authorized. The live lesson video and lesson materials were not changed.
