# Big Upside v12 — built for review

November 3, 2026. Implements the approved production plan in the [source comparison](../big-upside-comparison-2026-11-03/REVIEW.md).

**Candidate:** [big-upside-v12.mp4](../../Prompts/big-upside-v12.mp4), 3:32.500, 1280×720, 30 fps, 6,375 frames. SHA-256: `fa1cda4fd1caa483fb059bfbd506c5ce0392501ad07e802aaa55c95e0a14248d`.

**Status: shipped locally; queued for batch deployment.** After the listening and continuous-playback limitations were disclosed, David explicitly instructed “ship it.” V12 is installed and committed locally. Assistant direct listening and continuous audiovisual playback remain unperformed; neither is represented as passed. The lesson, raw sources, and canonical boards are unchanged by this shipment.

## Narration

Roll 1 supplies the complete lesson arc. Its protein caveat is replaced by the complete roll 3 passage: “But remember, a prediction isn't a finished medicine. Scientists still have to test ideas and do the research.” The categorical roll 1 sentence “That early warning translates directly into safety” is removed. The explanation about preparing or moving before the water arrives remains.

The frame-aligned source assembly is authoritative in `edit-manifest.json`:

| Source | Source interval | Output interval |
|---|---|---|
| Roll 1 | 0–72.7667 s | 0–72.7667 s |
| Roll 3 | 61.0667–67.8333 s | 72.7667–79.5333 s |
| Roll 1 | 80.9333–172.4667 s | 79.5333–171.0667 s |
| Roll 1 | 175.9667–217.4000 s | 171.0667–212.5000 s |

The donor receives +0.0684 dB gain. Five-millisecond ramps affect only quiet endpoints at the three joins. No internal pauses, narration generation, or speed changes were added. Review audible continuity near **1:12.77, 1:19.53, and 2:51.07**.

All eight required word sequences appear in fresh ASR, allowing punctuation, case, and brief lead-ins. The removed safety claim is absent. The transcript was generated from v11; all v12 AAC packets are byte-identical, verified independently. See `narration-checks.json`, `transcripts/PROVENANCE.json`, and `packet-verification.json`. ASR does not certify pronunciation, cadence, or smooth joins.

## Picture

The five exact current lesson JPGs replace generated board approximations. Teaching boards remain complete and static, with 4 px outlines in the 720p output. Their intervals are:

| Board | Output interval |
|---|---|
| Protein | 0:57.367–1:16.400 |
| Cancer, setup | 1:19.967–1:29.267 |
| Cancer, explanation | 1:38.000–1:54.000 |
| Reading | 2:08.967–2:22.833 |
| Flood | 2:42.800–2:58.233 |
| Close | 3:23.867–3:32.500 |

Roll 2 supplies the community scene and laboratory scenes. Its community scene starts after the incoming cut and holds its final safe frame briefly to fill the approved interval. The laboratory continues cleanly through the caveat's outgoing audio join. The live video's provenance-known, purpose-generated menu-reading asset supplies the 1:54.000–2:01.933 cutaway.

The “Impact Today” chapter card, unsupported 1–5-year experiment graphic, and anatomical cancer setup are replaced. The retained qualitative Swedish-trial comparison supports the narration. The animated forecast graphic now reads “EARLY FLOOD WARNING / DAYS AHEAD,” removing its fixed five-day promise. Supporting source animations remain, with engine-corner cleanup. The close has a 48-frame hold, 150-frame push to 1.2×, and 61-frame settle; its literal final frame is the current close.

The approved menu donor is photorealistic and the production outlines are added despite the raw-generation prompt's no-photo/no-highlight instructions; these follow the approved edit plan and production specification. No unknown stock imagery was introduced.

## Verification

- Sequentially decoded the actual candidate: all 6,375 frames, correct dimensions, exact 30 fps presentation timestamps, and 212.5-second picture duration.
- Checked 90 encoded board frames against the intended canonical compositions; maximum mean absolute channel difference 2.63/255, within the compression tolerance.
- Encoded audio measures 45.39 dB signal-to-error ratio against the intended PCM. Pre-encode samples outside the donor gain and join handles match the approved source assembly exactly.
- Transition guard passes all 40 boundaries. Visually inspected all 40 every-frame boundary strips, all 11 sampled-file sheets, all six seam summaries, and the full-resolution final frame. No stale-picture flashes found in those checks.
- Protected-file SHA-256 checks pass, including all three raw rolls, installed video, lesson, index, current boards, and menu donor.

Evidence: `verification.json`, `board-comparison.json`, `packet-verification.json`, `transition-guard/`, `qa-sheet-*.jpg`, and `seam-summary-*.jpg`.

**Unperformed:** direct listening and uninterrupted audiovisual playback. Voice matching, click-free joins by ear, and real-time motion/narration quality remain uncertified. The sampled stills and numeric checks do not substitute for that review.

## Build provenance

`scripts/video/build_big_upside_v12.py` defines the final assembly; its `--full` path renders from pristine sources. The delivered file preserves already-valid encoded packets and replaces only affected GOPs with fresh renders from original sources, avoiding an additional lossy generation of the rest. The audio is copied unchanged during picture repairs.

v9 and v11 are superseded internal candidates. v10 is rejected because its repair had incorrect timestamps. v12 fixes the laboratory return and community incoming-cut defects and passes fresh encoded-file checks. Earlier candidates remain available solely as build history.

## Local shipment

User authorization: “ship it.” Installed at `course-assets/big-upside/big-upside.mp4`; SHA-256 matches the candidate above, 24,583,028 bytes. Cache key `20261103ship12`; rounded displayed runtime 4 min (actual 3:32.500). Local commit `50784bfbe9b3b62b9db861a7447660a189cd2ba1`. The commit contains only the video, its LESSON_VIDEOS entry, and its video manifest hash/size. Existing lesson and board work remains unstaged.

`python3 scripts/verify-course-assets.py --migration-hashes` passed: 248 retained assets, 519 original path mappings, 263 current website references, and 55 finished videos. The staged video hash and exact shared-file scope were independently checked. No push or deployment performed; public serving remains unverified.

Post-commit cleanup removed 35 regenerable scratch files (0.24 GB) only from this Big Upside build/comparison series. Raw rolls, candidates, reports, transcripts, manifests, and visual review evidence were retained.
