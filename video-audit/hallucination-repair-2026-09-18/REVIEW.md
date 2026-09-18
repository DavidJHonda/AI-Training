# Hallucination v3 — current boards + canonical close (visual-only retrofit, 2026-09-18)

Status: **REVIEW CANDIDATE — not shipped.** Live file unchanged.

- Candidate: `Prompts/hallucination-v3.mp4`, 3:53.93, 7018 frames at 30 fps (same as live).
- SHA-256: see `edit-manifest.json` → `render_sha256`.
- Base: the shipped file (`course-assets/hallucination/hallucination.mp4`, sha `0198c0dc…`: the 2026-09-06 reroll build plus the 2026-09-08 illustration sync), taken as the picture source because the raw roll (`Prompts/hallucination-reroll.mp4`) no longer exists. Same shape as the other 2026-09-18 retrofits.
- Build: `.video-venv/bin/python scripts/video/build_hallucination_v3_retrofit.py`. It reuses the shipped scripts' own leg makers and renderers (`build_your_choices_reroll_review.make_leg` with the shipped cut/pause mapping, `build_work_changes_hybrid.render_leg`, `build_avoid_illustration_sync.render_leg` for the photo board, the shipped close mover), pointed at the current course assets.
- Audio: the shipped AAC stream copied (`-c:a copy`). Verified byte-identical (stream sha `b99f2ed4…` on both files). Nothing to audition.

## What changed

All four boards changed since their ships by the website credit line only, at the same dimensions (example 1600×825, why 1600×871, check-claim 1600×778, Real Text 1387×1134 JPG replacing the synced PNG). Every shipped ring rect was drawn on the current files and frames its component; the Real Text banner rect is re-detected by the sync compositor's gold-band finder.

| Span (output frames) | Picture | Change |
|---|---|---|
| 0–1908 | Nothing Sounds Wrong: full, your prompt (30), AI bubble dive (273, camera 1180 wide), takeaway (1028), full again (1374); neutral purple | credit line |
| 1908–3208 | Why Hallucinations Happen: full, then dives to the four columns (2079 / 2325 / 2565 / 2838) in purple, blue, teal, amber; the one-second pause (3177–3207) holds the last state | credit line |
| 3208–3724 | Notebook glue-pizza drawing and search scene (shipped picture) | none |
| 3724–3974 | Real Text. Wrong Meaning. photo board: full (3724), takeaway ring (3847) | current JPG of the synced board |
| 3974–4600 | Notebook "AI Failure Modes" graphic (shipped picture) | none |
| 4600–6612 | Check the Claim: full, dives to Notice (4714, purple), Find (5252, blue), Match (5784, teal), recap pull-back (6302) | credit line |
| 6612–7018 | Close: 48-frame hold, 150-frame push to 1.2×, settle, as shipped | **canonical close** `hallucination-close.jpg` via `make_close_board.py --lesson hallucination` replaces the archived capture |

Rings are the shipped treatment: 5 px post-crop rounded outline in the locked accents, dives with 24-frame moves.

## Checks

- Decoded frames 7018 = live.
- Frame-by-frame vs live: Notebook spans mean |diff| 0.3 (re-encode only); example 0.35, why 0.55, check-claim 0.5, Real Text 1.3 (credit lines / JPG re-encode); close 9.9 (canonical board).
- `transition_guard.py`: 22 boundaries; 14 pass, 8 flagged. All 8 flags are the 24-frame camera dives on the Why and Check the Claim boards (frames 2079, 2325, 2565, 2838, 4714, 5252, 5784, 6302), where the detector reads a continuous pan as a run of cuts; the shipped 2026-09-06 review recorded the same false positive. Every strip inspected: the pans ramp smoothly, every real splice (leg ins/outs, kept audio cuts, pause end, pizza-to-search, close) lands on its destination frame with no stale island.
- Ring states inspected (`v3-states-sheet-*.jpg`): complete bubble / column / step / banner inside each ring; canonical close hold, push and last frame correct.
- Protected files (live video, lesson, five assets) unchanged through the render.

## Still open

- David's eye-test of the candidate.
- Ship step (on approval): copy to `course-assets/hallucination/hallucination.mp4`, add a cache key to the lesson's video src in `index.html` (it has none today), update the manifest entry, receipt here, remove the `-v3` candidate.
