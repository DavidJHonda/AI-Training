# Unexpected Results v3 — approved label repair

**Shipped locally, September 30, 2026; queued for batch deployment.**

David approved local shipping with “ship it.” Commit `78fa9efdc3f0d5e6d180e18ef50decbaf70a1dd3` installs the exact reviewed v3 at `course-assets/unexpected-results/unexpected-results.mp4`, updates its manifest hash/size and cache key to `20260930ship3`, and retains the `4 min` display. Only those three release files were committed. No push or deployment performed; the published site was not reverified or claimed updated.

Installed SHA-256: `051361422c95c73c7d7127cc5b9908f8652f9b4b8b1a068bb1300c5a5f5bffdc` (30,977,994 bytes), verified after commit. The prior build's audio, frame-identity and transition checks remain tied to these exact bytes. No new listening pass is claimed; shipping follows the owner's approval of the reviewed narrow repair.

The broad `verify-course-assets.py` check reports unrelated existing failures: retired-name records for In Your Hands and malformed extracted paths for two Where's the Line boards. The scoped Unexpected Results file, manifest entry, references and Git diff checks pass. Those unrelated findings were not changed or included in this release.

Post-commit scratch cleanup was scoped to this build. The standard cleaner found no matching leftovers; the untracked, regenerable `leg-labels.mp4` intermediate was removed separately. Candidate, code, manifests, encoded review frames and transition evidence are retained. See `local-release.json`.

Candidate: [unexpected-results-v3.mp4](../../Prompts/unexpected-results-v3.mp4), **3:59.07**, 1280×720, 30 fps, 7,172 decoded frames.

David's “Build it please” approved the two visual corrections from the [live evaluation](../unexpected-results-live-review-2026-09-30/REVIEW.md). This is a narrow visual repair. Narration, pauses, board treatment, closing card, and timeline are preserved.

## Changes to review

| Output time | Correction | Preserved |
|---|---|---|
| 0:32.40–0:40.17 | Ledger heading becomes **Rat tails collected**; erroneous 2023 date becomes **Hanoi, 1902** | Ledger paper, bars, green check, scene timing |
| 0:47.77–0:53.20 | **Can survive / Can keep breeding** replaces the absolute lifespan statement | Original box, rat/offspring reveal, arrow, labels, and source fade-in/fade-out |

The breeding correction starts with the original text's visible fade at frame 1433 and ends with that scene at frame 1596 exclusive. Its opacity is measured from the original text rather than introducing a new animation schedule. Full-resolution encoded examples: `encoded-01080.png` (0:36), `encoded-01560.png` (0:52), and `encoded-01595.png` (exit fade).

## Source and method

The raw generations are absent. The repair uses the verified published v2 file at `course-assets/unexpected-results/unexpected-results.mp4`, locked to SHA-256:

`1aadfdf5f509be580e4ceb70789a52da017474a1c9cda00b2be6dc0b12a5730a`

Only complete H.264 groups covering frames **972–1595** were encoded again, once from that source. This 20.8-second encoding span includes the unchanged intervening rat scene because the second label begins between source keyframes. All compressed video outside that span and every original AAC packet were copied unchanged. The source and replacement decoder configurations match exactly.

Label cleanup removes the original glyphs and draws the corrected typography; no supporting scene was replaced by a still. The source canonical video, lesson Markdown and JPGs passed unchanged-hash assertions. No website, tracker, release commit, or deployment changes were made.

Candidate SHA-256:

`051361422c95c73c7d7127cc5b9908f8652f9b4b8b1a068bb1300c5a5f5bffdc`

Build: `scripts/video/build_unexpected_results_v3.py`.

## Verification

- Whole-file sequential decode: **7,172 frames**, **30 fps**, **239.0667 seconds**, matching source video and audio stream start times/durations.
- **6,548 untouched frames are pixel-identical**, and their compressed packets/timestamps are identical. This includes all course boards and the final closing frame.
- **All 11,208 AAC packets and timestamps are identical**. Decoded PCM also matches exactly: 22,951,936 bytes, SHA-256 `5ebad73a70a896e05fb017dfb874806de6c079eab37a4370d8a2fdc0d8cb0796`.
- `transition_guard.py`: **4 boundaries, 0 failures**. All four every-frame strips inspected: ledger enters already corrected, ledger exits directly to the original next scene, the breeding label follows the reveal, and the original exit dissolve remains intact.
- Full-resolution encoded labels inspected at settled states and partial fades; no old-word remnants visible in those checks.
- The visual changes are ready for review. Direct audio listening and continuous whole-file viewing were not performed; no new audio edit or splice was introduced. This is not a new whole-file narration/shipping sign-off. The earlier review's optional polish and pre-existing broader verification limits remain outside this repair.

Evidence: `edit-manifest.json`, `qa.json`, `label-opacity.json`, `transitions/transition-guard.md`, and `encoded-*.png`.

Commands:

```sh
.video-venv/bin/python scripts/video/build_unexpected_results_v3.py --preview
.video-venv/bin/python scripts/video/build_unexpected_results_v3.py
.video-venv/bin/python scripts/video/qa_unexpected_results_v3.py
.video-venv/bin/python scripts/video/transition_guard.py Prompts/unexpected-results-v3.mp4 --boundary 972:ledger-in --boundary 1205:ledger-out --boundary 1425:breeding-label-fade --boundary 1596:breeding-out --outdir video-audit/unexpected-results-labels-2026-09-30-v3/transitions
```

The guard was run through a `runpy` wrapper setting OpenCV processing and video-decoder threads to one. The checker and thresholds were unchanged.

Shipping authorization came from the subsequent explicit “ship it,” not the earlier build request.
