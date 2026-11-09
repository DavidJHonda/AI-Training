# Layers v13 — shorter explanation and numeric walkthrough

Built November 9, 2026 from the installed v12. Review candidate: `Prompts/layers-v13.mp4`, **2:56.00**, 5,280 frames at 30 fps, 1280 × 720. This removes 30.10 seconds from v12's 3:26.10.

The user agreed to removing the redundant explanation around 0:55–1:05 and tightening the numeric passage around 1:19–1:39, then requested the video update. This is a narrow edit implementing that approval.

| Original span removed | Content |
|---|---|
| 55.100–65.100 | “Within each layer, steps called attention and transformation work together to update the numbers, helping the system work out what your words mean together.” |
| 79.600–99.700 | The introduction to tracking two values, their starting values, and the walkthrough ending in their final values. |

Both cuts fall in measured inter-sentence gaps. The retained explanation is: “The numbers that come out are not the numbers that went in. Attention and transformation update the numbers at each layer.” The complete four-card number row remains visible for comparison, followed by the original pullback and takeaway highlight. No new pauses or illustrations were added. The supporting illustration associated with the removed numeric introduction disappears with that passage; all other supporting scenes remain in their original sequence.

The new joins are **0:55.100** and **1:09.600**. `edited-section-preview.mp4` contains output 0:48–1:19 for convenient listening review. The rest of the lesson retains its prior treatment, including the CAT/IT example and standard close.

Verification: decoded all 5,280 frames; compared 138 encoded pictures with their mapped source frames (maximum mean pixel error 0.659/255); checked all three retained audio spans (correlations above .99998); transcribed the encoded edited region and confirmed the retained sentences without the deleted readout. Transition guard passes both new joins. Inspected every-frame strips around both joins, the numeric comparison and takeaway frames, and the literal final frame. No stale intervening picture was found.

Direct listening and continuous real-time playback were not performed. Listen at 0:55 and 1:10 to assess cadence and audio joins. This is ready for review, not a full shipping certification; broader inherited board treatments were outside this narrow edit.

Source limitation: v12's original reconstruction depends on a temporary source snapshot that no longer exists. This candidate uses one high-quality encode from the verified current v12, with no intermediate lossy renders. Source and installed-video SHA-256 remain `42fb10fd979dd5567d8a9ae2105507a87b7f7cc0610ff20e1095fbd7ce5bcbb6`.

Build: `.video-venv/bin/python scripts/video/build_layers_v13.py`. Exact mappings, source/candidate hashes and treatment are in `edit-manifest.json`; quantitative checks in `qa.json`; wording checks in `encoded-transcript.json`; visual boundary evidence in `guard/`.

The candidate was shipped locally on November 9, 2026 after the user said “ship it.” No tracker status was changed.

## Local release

Commit: `3f974f5b7c978dc1f02fb55e981eb6efc572136e`. Installed the exact approved v13 at `course-assets/layers/layers.mp4`; cache key `20261109ship-layers-v13`, duration pill 3 min. Updated the manifest SHA-256 and byte size. Committed and installed bytes verified identical to the candidate. Only the MP4, its manifest entry and its index reference were committed; unrelated working edits remain.

User approved shipping after the disclosed listening limitation. Direct listening is not claimed, nor is an explicit user report of listening. The exact reviewed file was installed unchanged. Course-reference verification passes. The full working-tree hash check reports only two pre-existing Transformer board edits; their staged/committed versions match the manifest. Layers checks pass.

**Shipped locally; queued for batch deployment.** No push or deployment performed.
