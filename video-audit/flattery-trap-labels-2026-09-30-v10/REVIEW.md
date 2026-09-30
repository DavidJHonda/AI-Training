# Flattery Trap v10 — two title corrections

Built 2026-09-30. Narrow repair requested by David: change “FALSE PRAISE” at
approximately 0:13 to “FLATTERY TRAP,” and “ARTIFICIAL PRAISE” at approximately
1:53 to “SYCOPHANCY.” No other editorial changes.

Candidate: `Prompts/flattery-trap-v10.mp4` (1280×720, 30 fps, 9,431 frames,
5:14.3667). SHA-256: `db9c8139d51ab6e00c30315346f6078822496c83a97a738737454c802657db50`.

Source: `Prompts/flattery-trap-v9.mp4`, SHA-256
`26a48f97db2ece2374d2849ac7730d39c68d19fe083f6cb709bc450d0ce5f4f0`.
The finished v9 is the repair source; original raw rolls are unavailable locally.
Only the two affected complete H.264 GOPs were encoded. All other video packets
and all audio packets were remuxed unchanged, avoiding further generation loss
outside these two scenes. Source and replacement SPS/PPS are identical.

| Graphic | Output frames (end exclusive) | Exact time | Treatment |
|---|---|---|---|
| FLATTERY TRAP | 396–463 | 0:13.200–0:15.433 | Replace words on the yellow note; retain original paper edges and background. |
| SYCOPHANCY | 3385–3608 | 1:52.833–2:00.267 | Replace heading only; retain dictionary body, paper, backing, and background. |

Both are independent supporting drawings, not replacements of canonical course
boards. Original full-view framing and unmarked treatment remain. Source spans
are stationary holds with minor compression variation. Generated text regions
were composited over each original frame; timing and surrounding scenes remain.

## Verification

- Entire candidate decoded: 9,431 frames at 30 fps, matching v9.
- All 9,141 frames outside the two scenes are pixel-identical to v9.
- All unaffected compressed video packets are identical, including timestamps.
- All 14,737 AAC packets, timestamps, and durations are identical. Decoded audio
  bytes and SHA-256 also match: `2d362b336647ba5f2be84c991316af7b7666d1c1d57a5824f196527f2f7b90b2`.
- Actual encoded titles inspected at native resolution: exact spelling, readable,
  no clipping or leftover original heading text.
- Transition guard passed all four boundaries (396, 463, 3385, 3608).
  All four every-frame boundary strips inspected: clean destination frames,
  no stale title flashes. The existing diagram reveal after frame 463 remains.
- No new audio joins or pauses. No direct listening or continuous audiovisual
  playback performed during this title-only repair. Earlier v9 listening gaps
  remain, including the prior edits around 2:41 and 2:45 and the donor voice join
  around 2:37–2:41. This is a review candidate, not whole-file ship certification.
- Course asset and site reference were not modified; no shipping or deployment.

## Reproducibility and assets

Build: `.video-venv/bin/python scripts/video/build_flattery_trap_v10.py`

QA: `.video-venv/bin/python scripts/video/qa_flattery_trap_v10.py`

The builder intentionally refuses to overwrite an existing candidate or encoded
leg. Preserve reviewed versions and increment the version for another build.

Built-in image_gen produced the two title corrections. Final generated assets
are retained beside this review as `flattery-trap.png` and `sycophancy.png`.
Exact final prompts are in `image-prompts.json`. Local source reference frames,
encoded frame checks, `edit-manifest.json`, `qa.json`, and transition strips are
also retained here. Only the localized title regions from the generated images
are used in the candidate; the remainder comes from v9.

## Local release — 2026-09-30

David approved this candidate with “ship it” after the v10 review. Installed
`Prompts/flattery-trap-v10.mp4` at the canonical course path and committed only
the video and its single lesson cache-key update. Local commit:
`9311fe113135ab1200ca407030953076740188ba`. Cache key: `20260930ship10`.
The page's rounded “5 min” duration remains correct (actual 5:14.3667).

Installed and committed video hashes both match the reviewed candidate:
`db9c8139d51ab6e00c30315346f6078822496c83a97a738737454c802657db50`.
Existing hash-bound full decode, audio identity, and transition checks were
verified against the exact installed file. Earlier documented listening and
continuous-playback limitations remain unperformed; owner shipping approval is
not represented as a new assistant listening pass or an independently verified
whole-file audiovisual sign-off. No tracker update was made.

Status: **shipped locally; queued for batch deployment**. No GitHub push or
Vercel deployment was performed. Unrelated work was excluded from the commit.
