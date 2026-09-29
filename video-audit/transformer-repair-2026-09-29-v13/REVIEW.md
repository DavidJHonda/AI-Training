# Transformer v13 — narrow visual repair

**Status: shipped locally; queued for batch deployment.** David approved the build and then shipping with “ship it.”

## Scope

Repair the gibberish paragraph over the brain at **0:54.967–1:02.900** (frames 1649–1886 inclusive). The cream paper now reads “The CAT sat / on the mat / because IT / was tired.” Matching blue highlights connect CAT and IT. The original brain drawing, computer, scene framing, and movement are retained. No narration, pause, board, camera, or closing changes.

Candidate: `Prompts/transformer-v13.mp4`.

Source: stable `Prompts/transformer-v12.mp4`, SHA-256 `0a972235e9fcaf619d8db34715243a7812a87569091e87092f866666586376b5`, verified equivalent to the public video during the preceding evaluation. The pristine raw roll is unavailable; this repair uses the finished v12 and adds one video encode. Its AAC audio stream is copied directly.

Generated asset: `scripts/video/assets/transformer-v13/brain-paper-imagegen.png`. Built-in ImageGen created the paper repair; the complete prompts and generation lineage are in that directory's `README.md`. Only the paper interior is used, with a two-pixel inward feather; no generated surrounding scene replaces the original.

Build: `.video-venv/bin/python scripts/video/build_transformer_v13.py`.

The build sequentially decodes the source, tracks the paper against frame 1740, and verifies that every pre-encode pixel outside the compositing mask is unchanged. The maximum median tracking residual across all 238 repaired frames is 0.0077 pixels. First/middle/last prepared frames were visually inspected. The full manifest records every frame's transform and input identities.

## Remaining review limits

No new perceptual listening or continuous whole-video playback. The earlier review's listening questions at 0:46–0:52 and 2:44–2:48 remain outside this narrow repair. The original 28.767-second worked-example board run and 33.567-second board/close chain remain unchanged. Whole-file shipping certification and shipping approval are separate from this build.

## Encoded verification — PASS

- Candidate SHA-256: `fea9e90451f29da642ad2e3fc51b8249a1e1ef7c265a4f33724c216e198aba0f`.
- Exactly 7,046 decoded frames at 30 fps; runtime remains **3:54.867**. Video and audio stream durations, timebases, frame counts, and rates match v12.
- Copied AAC payload hash matches exactly: `0dd13d6abffcf7734cc683e8d2fb0514`. No new audio splice exists.
- Both declared boundaries passed transition guard. Every-frame strips at frames 1649 and 1887 were inspected: the first frame of the brain scene is repaired, the last remains repaired, and the following board starts cleanly. No stale paragraph flash or intermediate frame was found.
- All 238 repaired frames passed the paper-content check; maximum mean error against the prepared paper is 2.930/255. Unchanged scene surroundings have maximum mean error 2.529/255, consistent with the additional video encode.
- Full-file source comparison found no unauthorized visual changes and no short source-frame islands. Outside-span downsampled mean error p99 is 2.580/255.
- Inspected the encoded repair sheet and literal last frame. Text fits, CAT and IT are clearly marked, no gibberish remains in the repaired paper, and the canonical close remains the ending.
- Source candidate and installed course video retain their original hash. The public site has not been replaced by this build.

Verification commands:

```sh
.video-venv/bin/python scripts/video/splice_integrity.py Prompts/transformer-v12.mp4 Prompts/transformer-v13.mp4 --span 1649:1887 --outdir video-audit/transformer-repair-2026-09-29-v13/integrity
.video-venv/bin/python scripts/video/transition_guard.py Prompts/transformer-v13.mp4 --boundary 1649:enter-repaired-brain --boundary 1887:leave-repaired-brain --outdir video-audit/transformer-repair-2026-09-29-v13/guard
.video-venv/bin/python scripts/video/qa_transformer_v13.py
```

Evidence: `edit-manifest.json`, `encoded-verification.json`, `stream-metadata.json`, `integrity/splice-integrity.json`, `guard/transition-guard.json`, `encoded-repair-sheet.jpg`, and `last-frame.jpg`.

[13-second contextual preview](repair-preview.mp4) covers full-video 0:52–1:05. This convenience excerpt is re-encoded separately; the full candidate is the release-review artifact.

[ImageGen asset and exact prompts](../../scripts/video/assets/transformer-v13/README.md).

## Local shipping — September 29, 2026

Installed the exact approved v13 at `course-assets/transformer/transformer.mp4`, updated its manifest hash/size and cache key to `20260929ship1`, and verified installed and committed bytes against the reviewed candidate. Displayed duration remains 4 min for the 3:54.867 file.

Local commit: `8c2ed0cd989d06eecde24f924232259ece454d6a`. Only the Transformer MP4 and its entries in `index.html` and `course-assets/manifest.json` were committed. Audit/build records remain local. Previously disclosed listening limitations remain recorded; no new listening claim is made.

No push or deployment was performed. This release is **queued for batch deployment**. Scoped scratch cleanup found no eligible files; review artifacts and source candidates are retained.
