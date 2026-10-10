# The Next Token — v3 narrow repair

Candidate: `Prompts/the-next-token-v3.mp4` · 3:21.10 · 1280×720 · 30 fps.

User request: “At :15, highlight sampling and temperature as spoken.”

## Changed span

The existing opening diagram stays at full view. A 4 px purple outline follows the full Sampling label card from frame 432 (0:14.40) to frame 458. It switches to the Temperature label card at frame 459 (0:15.30, nearest frame to the 0:15.28 word timestamp), holding through frame 485. The next scene still starts at 0:16.20. All other visuals and timing follow v2; narration and duration are unchanged. Rebuilt from original sources, preserving v2.

## Verification

Encoded QA passed all 22 declared boundaries and decoded all 6,033 frames. Both settled highlight states were inspected at full resolution in the encoded candidate. The first 486 pre-encode opening frames were compared with v2: only the intended 54 frames differ, exclusively within the selected label border. The assembled PCM and decoded AAC audio are byte-identical to v2. Runtime remains 201.10 seconds. Protected source and course files are unchanged. Detailed results are in `qa.json` and `unchanged-checks.json`. Timing uses the retained word timestamps; direct listening has not been performed. Existing v2 listening-review limitations remain, especially the donor joins at 2:58.33 and 3:06.27, and the retained “would become ... repetitive” wording. The owner subsequently approved shipping with “ship it”; see the local release record below.

Build: `scripts/video/build_the_next_token_v3.py`. Full source identities and repair coordinates are in `edit-manifest.json`.

## Local release — 2026-10-09

User approved v3: “ship it.” Installed at `course-assets/the-next-token/the-next-token.mp4`; lesson `inference` uses cache key `20261009ship3` and the existing 3 min runtime label (exact duration 3:21.10).

Commit: `530e970dc77e5be28d45b6ebe43fd908aed69922` — Ship The Next Token video v3 locally.

Installed SHA-256: `b68eaf70af2c11a4e8c4d751af283b988e36f90a3231b89a174d44cc6ecddec9`.

Candidate identity and all protected source/board/lesson hashes were verified before installation. All four v3 transition boundary summary sheets were visually inspected; the existing encoded QA passes all 22 boundaries and 6,033 frames. Installed hash and committed paths were verified after the commit. Direct listening and continuous audiovisual review were not performed by the assistant; the earlier disclosed limitation remains, not a claimed pass. No new narration assessment was inferred from the shipping instruction.

Status: **shipped locally; queued for batch deployment**. No push or deployment was performed. Removed 53 regenerable scratch files (approximately 0.22 GB) from this lesson's build audit folders only. Raw generations, candidates, captures, scripts, transcripts, QA records, and review evidence were retained. Future rebuilds require re-extracting the cleaned source WAVs from the retained MP4 rolls.
