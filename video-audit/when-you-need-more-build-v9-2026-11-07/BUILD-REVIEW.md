# When You Need More — v9 review candidate

Built November 7, 2026 following the user's “Agree.” to matching the successful
Your Home Base illustration treatment. Full candidate:
`Prompts/when-you-need-more-v9.mp4`, 168.9667 seconds, 1280×720, 30 fps.

## Changes

- 1:01.733–1:18.633: a student works through a summer-business plan with an AI
  assistant, a costs/pricing/customers notebook, calculator and planning papers.
  Replaces the hourglass/gears and clock passages.
- 1:55.867–2:11.533: the same student compares university source pages and records
  physics-program research, admissions and cost questions in a notebook.
  Replaces the documents/network and web-lookup drawings.
- Both illustrations use a two-second wide hold, a gentle four-percent camera
  push and a two-second closer hold. These are photographic illustrations with
  camera motion, not character animation. No facts or numerical comparisons are
  invented in the university materials.

The exact shot boundaries encompass the user's rounded times. The existing
teaching-board entries, narration, duration and all v8 animation improvements
remain intact. Canonical JPGs and installed v7 remain unchanged. Unaffected
pictures were rebuilt from pristine sources with the existing renderers; audio
was copied directly from v8 without re-encoding.

Illustrations were generated using built-in `image_gen.imagegen`, with
`scripts/video/assets/your-home-base-scenes-2026-11-07/chatgpt-art-night.png` as
the identity/style/location reference. Final PNGs and exact prompts are saved
under `scripts/video/assets/when-you-need-more-scenes-2026-11-07/`.
The scene keeps the same learner, jersey, warm study room and task-focused
composition. Text and safe margins were inspected at the final 720p framing.

## Verification

- All 5,069 frames decode; video timestamps are continuous at 30 fps.
- AAC packet bytes, timestamps and durations match v8 exactly. Audio SHA-256:
  `e30f800289549c353ea1008d26331406d0a3b973148a0d7593745d7cf04ad4a7`.
- All 15 declared boundaries pass the transition guard. Encoded frames on both
  sides of every seam were visually inspected, including all four new entry/exit
  cuts. No intervening old graphic was observed.
- New scenes were inspected at half-second sampling throughout, alongside
  full-size endpoint previews and the literal encoded closing frame.
- Every retained frame was compared against v8 at 320×180: maximum mean absolute
  error 0.212/255, average 0.00169/255, consistent with re-encoding.
- All protected hashes match; source cleanup declined zero frames. V8's donor
  inserts retain the same repaired text and native motion.
- Candidate SHA-256:
  `8ae33c72486e5bfaaf8b2fe554a6fabec725c52374b3263b1e8325f0173f11e6`.
  File size: 40,564,862 bytes.

Technical and frame-sequence checks are complete. No continuous audiovisual
playback/listening pass was completed. Browser playback was unavailable under
the previously encountered local-serving and file-URL restrictions; no workaround
was attempted. Review candidate only: not installed, committed or published.

## Review files

- `../../Prompts/when-you-need-more-v9.mp4`: full candidate.
- `before-left-after-right.mp4`: 39-second comparison, v8 left / v9 right, with
  candidate narration; covers 1:00–1:20 and 1:54–2:13. All 1,170 frames decode.
- `PLAN.md`: approval, timing and teaching purpose.
- `edit-manifest.json`, `qa.json`, `comparison-qa.json`: technical evidence.
- `encoded-scenes-*.jpg`, `boundary-review-*.jpg`, `encoded/`, `transitions/`:
  visual review evidence.
- `../../scripts/video/build_when_you_need_more_v9.py`: reproducible builder.
- `../../scripts/video/qa_when_you_need_more_v9.py`: full candidate checks.

## Local shipping — November 7, 2026

User authorized: “ship it” after the review disclosure. Installed approved v9 at
`course-assets/when-you-need-more/when-you-need-more.mp4` and verified exact
candidate hash and 40,564,862-byte size. Updated the lesson cache key to
`20261107ship9`, retained the correct “3 min” display, and updated only the
video manifest row (version 9, hash, bytes). Migration-hash verification passed
for 248 assets, 519 mappings, 263 references and 55 videos.

Local commit: `694ff9772ac7ca10c6162546434aa303d5a1d839`. Its only files are the canonical video,
`index.html` and `course-assets/manifest.json`; unrelated working changes remain
uncommitted. Review/build assets are retained locally. Independent continuous
listening remains unperformed, as disclosed before shipping authorization.
Video Tracker was not accessed or changed.

**Shipped locally; queued for batch deployment.** No push or deployment performed.

Post-commit cleanup removed 12 regenerable scratch files (0.11 GB), scoped to
the v8/v9 build folders. Candidates, PNG assets, prompts and review evidence remain.
