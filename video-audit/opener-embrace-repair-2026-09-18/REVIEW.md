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

## Build: v4 (2026-09-22): recaptured card and the map-transition line from the Understand opener

**Candidate:** `Prompts/embrace-the-future-opener-v4.mp4` (4995 frames, 2:46.50, sha256 9c55127bb39a0a0f…), a narrow repair of the LIVE
`course-assets/embrace-the-future-opener/embrace-the-future-opener.mp4` (0e97083bfdb7…, 5055 frames, 30 fps, 2:48.55)
(`scripts/video/build_opener_embrace_v4.py`, folder `build-v4/`, QA scratch in `build-v4/qa/`). The live's narration, drawings and
boards are kept; two changes (David, 2026-09-22):

1. **The card, at the Work With AI opener's size.** Live frames 266–991 (8.87–33.03, the live's own cuts in and out, confirmed by
   sequential scene scan) now show today's recapture `embrace-the-future-opener-voices.jpg` (1ebc08c3543f…, 1600x900, card 60,194–1539,705,
   44 px text rows) at full view, compact, no push. Gold `#f2cf5b` rings tight to each line (text extent ±18 px x, ±9 px y; the two
   rings that share the closing line meet at the word gap's midpoint, x 347, instead of overlapping each other's neighbour as the
   live's did) at the onsets the live rings, decoded from its frames and checked against small.en: the optimist pair (quotes 1 and 3)
   at 12.17 (live frame 365; "Optimists" 12.14), the worrier pair (quotes 2 and 4) at 16.63 (499; "Worriers" follows the 16.38–16.71
   silence), unmarked for the Doubters at 20.37 (611; "Doubters" 20.44), "who's right?" at 22.20 (666; "Which" 22.16), "nobody knows."
   at 27.53 (826; "Nobody" 27.36). Full view unmarked for 3.30 s before the first ring. The crowd drawing before it (0–266) stays.
2. **The map-introduction line, audio only.** The live's "Instead of historical philosophy, we need a concrete plan for your education."
   (116.84–121.50; silences 116.34–116.84 and 121.63–122.10) is replaced by the Understand AI opener's "This roadmap shows what we'll
   explore in this section." (`course-assets/understand-ai-opener/understand-ai-opener.mp4`). Donor frames 2419–2519 (80.63–83.97):
   the word actually starts at 80.94 by energy profile and silencedetect (the small.en stamp "This 80.56" is 0.4 s early), so the beat
   is taken with 0.31 s of its own lead-in and its own tail, including the narrator's complete inhale (83.68–83.90, back at the floor
   before the cut) — this is why the donor starts at 2419 rather than the ~2405 first suggested, which would have added ~0.5 s of pause.
   Live cut at 3498 (116.60, floor after "unexpected.", no breath in that gap) and resumed at 3658 (121.93, floor; the live's own inhale
   for "First," 121.66–121.85 goes with the deleted sentence, so one breath, the donor's, precedes "First,"). Quiet before "This" 0.57 s
   (the live had 0.48 before "Instead"); quiet before "First," 0.47 s (the live had 0.46). No new pauses. **Levels:** speech RMS (20 ms
   windows above −50 dBFS): live previous sentence 109.44–116.16 −16.40 dBFS, live next sentence 122.18–128.38 −16.01, donor 80.94–83.65
   −16.63; gain **+0.4 dB** (the mean of the two flanking matches, +0.23/+0.62). Finished file, volumedetect mean: live previous sentence
   −17.2 dB, donor speech −16.6, live next sentence −16.7. **Graft output span 3498–3598 (116.60–119.93)**; the donor words land at
   116.86–119.16 in the finished file and everything after the graft is 2.00 s earlier than in the live.
   **Picture under it:** our section map, re-rendered from the current `embrace-the-future-opener-section-map.jpg` (253adaa8d5b8…,
   1600x789 on the house stage, compact, no push) with the live's treatment: three row rings at the live's onsets (The Argument
   `#4f2fc4` at live 122.17 / output 120.17, Monsters and Open Water `#1652f0` at 129.07 / 127.07, Where It Lands on You `#0e8f86` at
   135.30 / 133.30), unmarked from 142.07 / 140.07 to the board's end (live 4532 / output 4472). Rects re-measured on the current JPG:
   rows x 80–1520, y 128–278 / 278–429 / 429–620 (the white card's dividers), radius 22. The live has no banner ring and none is added.
   The map now arrives at the graft start (output 3498, 116.60) instead of at 122.17, unmarked full view for 3.57 s before the first ring;
   the Notebook frames the live showed under the old sentence (live 3498–3665: the last 9 frames of the wave-and-sailors drawing and the
   whole tablet-and-map drawing 3507–3665) are not shown.

**Everything else is the live's own,** picture and audio, including its edge-of-the-map board leg (live 1575–2262, a leg of the current
asset with the live's camera moves) and its standard close from 4729 (output 4669). Board check by hash: edge-of-the-map 830c9186…,
section-map 253adaa8…, close 18044899… equal the hashes recorded for the live's build (`manifest.json` here) and the current files;
the voices JPG differs by design (a43984df… then, 1ebc08c3… today's recapture). Pixel check: the live's map frames match the current
asset (mean abs diff 4.6/255) and its edge frames match the current asset centre-cropped to 16:9 (3.6/255).

**Checks (Edit Spec 10):** decoded 4995 = plan; guard 5/5 (266 crowd→card, 991 card→ship, 3498 live→map with the graft in, 3598 graft
out — audio-only, no visual cut, the first row ring pops at 3605, 4472 map→coder drawing), strips inspected (`build-v4/guard/`), the first
frame after each boundary is the destination; ring states inspected at full resolution for both legs (`build-v4/state-*.jpg`); corner
mark on the kept Notebook frames 806 cloned, 1803 inpainted, **0 declined**; the 687 edge-board frames (live 1575–2262, no mark) were
passed through the cleaner untouched rather than inpainted (recognised by frame hash; recorded as `unmarked_board_passthrough` in
`build-v4/edit-manifest.json`); protected files unchanged (live mp4, four JPGs, donor mp4, `lessons/Opener-Embrace.md`); small.en on
the finished file: "…react to the unexpected. This roadmap shows what we'll explore in this section. First, we tackle the argument…",
card lines and close as the live speaks them, nothing after "blank space."; silences on the finished file around the graft:
116.33–116.92 (0.58), 119.81–120.10 (0.30), then 122.22–122.48 as the live's own. Live video, lesson, course-assets, index.html and the
registry untouched; nothing committed.

**Not auditioned by ear (David):** the graft in at 1:56.6 (unexpected. → This roadmap), the graft out at 1:59.9 (section. → First,) and
the level match across them; the live's card and map spans are unchanged audio.

**At ship (not authorized yet):** copy to `course-assets/embrace-the-future-opener/embrace-the-future-opener.mp4`, cache key
`?v=20260922ship1` on `openerrealworld` (index.html line 1154; the live entry currently carries no `?v=` key), pill stays "3 min" (2:46),
manifest video hash/bytes. The page card change (`?v=20260922capture1` on the voices JPG) is already on the page.
