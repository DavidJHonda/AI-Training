# Work With AI illustration pilot — 2026-10-08

Narrow visual-only build under the approved three-insert proposal. Owner approved all three candidates and requested shipping. Installed and committed locally as 4070c1c6; queued for separate batch deployment. Existing narration and timeline unchanged. Sources are the approved finished local videos, each reencoded once at H264 CRF16 with its original AAC stream copied.

| Lesson | Source → candidate | Replaced frames (end exclusive) | Output time | Screen state change |
|---|---|---|---|---|
| Art of Prompting | v9 → v10 | 3447–3730 | 114.900–124.333 s | 118.400 s: focused feedback request appears |
| Context Window | v6 → v7 | 5844–5980 | 194.800–199.333 s | 196.800 s: assignment appears in chat |
| Evaluate the Results | v8 → v9 | 5106–5277 | 170.200–175.900 s | 172.233 s: emphasis moves to source |

Exact cut boundaries were determined from sequential source frames. These replace the complete existing supporting shots while preserving adjacent boards, rather than using rounded provisional proposal times. P2 uses the shorter true 4.53-second window; P3 uses the proposal's side-by-side option to maximize reading time.

## Board treatment retained

- Art of Prompting: preserve both Four Moves boards, full introductions, every existing highlight and camera, and the preceding paragraph/question reveal. Return to the existing continued board at frame 3730.
- Context Window: preserve the Outside the Window board, all four card views and highlights, its Files on Your Computer initial view and return, and the transition to Other Apps and Tabs. Preserve the accepted desk scene, five-source tray, and long-chat mechanics sequence.
- Evaluate the Results: preserve the continuous evaluation flowchart, Quick Pass, Dig Deeper?, all five Dig Deeper cards, and Your Move. Preserve the Check the Sources card before and after the insert.
- No board redraws, narration cuts, audio grafts, pause edits, or closing-frame changes.

## Checks and limitations

See verification.json for source/candidate hashes, complete decoded frame counts, identical audio payload checks, intended-state comparisons across all edited frames, and per-second retained-frame comparisons. Each transitions-* folder contains the transition-guard record and every-frame boundary strips, including screen-state changes.

Encoded screen states and all nine transition strips were inspected before delivery. Continuous listening and audiovisual playback review are unperformed; the owner should audition all three contextual excerpts. This narrow visual repair is not a new verdict on full-video teaching, narration, or ship readiness. At build verification the prior sources remained installed. Shipping replaced them with the exact approved candidate hashes; see local-install.json. Video Tracker and public deployment status were not checked.

## Assets and reproducibility

Photographs were generated with the built-in image_gen tool. Original scene and targeted draft-paper correction prompts are in assets/generation-record.json. Final selected photographs are assets/draft.png, assets/file.png, and assets/source.png. The script renders exact instructional screen text separately and composites it into the display quadrilaterals.

Build: scripts/video/build_work_with_ai_illustration_pilot.py. Verification and review assembly scripts live beside this record. The three lesson manifests record source identities and output hashes. Full candidates are in Prompts/art-of-prompting-v10.mp4, Prompts/context-window-v7.mp4, and Prompts/evaluate-the-results-v9.mp4.
