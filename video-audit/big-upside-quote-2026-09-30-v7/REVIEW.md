# Big Upside v7 — Hassabis quotation

Status: shipped locally; queued for batch deployment. Owner authorized “ship it” after v7 delivery.

User request: “1:32. I think we should add a graphic to show the quote.” This is a narrow visual repair retaining all v6 edits.

## Treatment

At 1:32, the timeline cuts to a full-screen quotation with Demis Hassabis's name. Large Plus Jakarta Sans type matches the course; the concluding phrase is purple and bold. The whole quote is visible from the beginning and holds still for reading. At 1:41.633, the original full-view health board begins at its existing frame. No narration, audio, pauses, frame count or timing changes.

| Graphic | Emphasis | Camera | Output span | Purpose |
|---|---|---|---|---|
| Hassabis quotation | Purple final phrase: improve the lives of billions of people | Static full frame | [2760,3049), 1:32–1:41.633 | Makes the spoken statement readable and gives its attribution while the narration explains his motivation. |

The source-roll transcript locates “When he won…” at 1:50 and the quote at 1:52; subtracting the preceding 535 removed frames maps them to approximately 1:32.17 and 1:34.17. The fresh full-video ASR places those sentences roughly half a second later. The graphic arrives before either estimate and ends at the existing health-board cut. No new audio cut is introduced.

Wording matches the current lesson and [DeepMind's October 9, 2024 announcement](https://deepmind.google/blog/demis-hassabis-john-jumper-awarded-nobel-prize-in-chemistry/). The footer identifies this as his statement on receiving the award.

V6's supporting scenes remain at 2:03–2:11 (scan review), 2:25–2:30 (antibiotic laboratory), 2:51–2:57 (reading a menu), and 3:17–3:22 (targeted weed spraying). Its replacement everyday takeaway hold remains at 3:29.93–3:31.63. The new quote reduces the longest consecutive course-board run to 24 seconds, the unchanged first timeline span.

## Reproducibility

- Candidate: `Prompts/big-upside-v7.mp4`.
- New asset: `scripts/video/assets/big-upside-quote-2026-09-30/hassabis-quote.png`; details in its README.
- Build: `.video-venv/bin/python scripts/video/build_big_upside_v7.py`.
- QA: `.video-venv/bin/python scripts/video/qa_big_upside_v7.py`.
- Builds directly from the verified v5 source, canonical boards and original v6 generated images. V6 is a comparison reference, not the encode source. No additional lossy generation is stacked on v6.
- Raw rolls remain unavailable. The surviving v5 source is `course-assets/big-upside/big-upside.mp4`, SHA-256 `a7d56ee3a5a5f4e4968c125719077130c7317f31872fc1c52d3ce22ecffb4c06`; picture receives one encode and AAC is copied.
- `edit-manifest.json` records source hashes, frame ranges and boundaries.

## Verification and limits

The typography preview and encoded quote have been inspected at 1280×720: full quote, correct attribution, clear emphasis and no clipped text. Both affected every-frame transition strips were visually inspected: the timeline cuts directly to the quote at frame 2760, and the quote cuts directly to the unmarked health board at frame 3049. The literal final frame remains the standard close.

Completed encoded checks in [verification.json](verification.json):

- 7,719 frames, 30 fps, 1280×720, 4:17.30.
- Compressed AAC and decoded PCM are bit-identical to the source.
- All 28 [transition checks](guard/transition-guard.md) pass, with zero flagged short visual islands. The two quote-boundary strips were inspected visually; the other strips were generated but not re-inspected for this narrow addition.
- Every one of the 289 quote frames matches the intended asset within encoding tolerance; maximum mean absolute channel error is 3.074 on the 0–255 scale.
- All 36 encoded preview comparisons pass, maximum error 3.441.
- All 7,430 frames outside the quote were compared with v6. Maximum per-frame mean absolute error is 0.00736, confirming preservation of its visuals, cutaways and close.
- Protected source video, lesson, canonical JPGs, generated assets and font retain their hashes.

Candidate SHA-256: `9bfd4f0e6dd7f051e4e70ebeba0923ce896484867a2503d06c18e096a2b61c50`.

Direct listening and continuous end-to-end audiovisual playback are not completed. The existing Hassabis/abaucin pronunciation questions and older donor-audio join at 3:31.63–3:38.43 remain for listening review. This addition introduces no audio join. These limitations were disclosed before the owner authorized shipping; no new agent listening certification is claimed.

## Local release

Installed v7 at `course-assets/big-upside/big-upside.mp4` and updated only its video cache key to `20260930ship1`. The displayed duration remains `4 min` for the unchanged 4:17.30 runtime. Commit `3020cdc1e1b5736452ca82bd302bb74683fe64df` contains exactly the video and its isolated `index.html` entry. Installed and committed MP4 hashes both match the verified candidate.

No push or deployment was performed. Other working changes, candidate files, source illustrations and audit records remain separate. The original v5 input is recoverable from Git at `3d187436583b896a807432fa0e8572d73d8b23fd:course-assets/big-upside/big-upside.mp4`. Release details are in `local-release.json`.

Post-commit cleanup removed four regenerable `canvas-*.png` files from the v6/v7 audit folders only. Candidates, assets, transcripts, encoded previews and transition strips were retained.
