# Make Your Move v12 — actions introduction

October 23, 2026. Fixed the visual mismatch identified by the owner near 1:44. The full current **Moves to Make** board now appears at the beginning of the action introduction, replacing the city drawing over 1:40.367–1:51.367 (frames 3011–3340). It stays unmarked during the overview; existing action highlights and camera movement continue afterward.

Candidate: `Prompts/make-your-move-v12.mp4`
SHA-256: `6f63a81571523de73159699b083c64d0b99217812deb0795ac093d9bd2f4f573`
Runtime: **3:01.03**, unchanged.

Only the 330-frame replacement span was encoded. Every original audio packet and timestamp is identical to v11. Every video packet and decoded frame outside that span is identical to v11. All 5,431 frames retain their original timestamps. Both transition-guard boundaries passed, and both every-frame strips were visually inspected, along with the full-size replacement board. The complete board remains visible and unmarked during the new introduction; no stale city frames remain in the repaired interval.

The added opening hold extends the first actions-board run to about 19 seconds, followed by its existing conversation cutaway. No narration, pacing, pauses, highlighting, or other footage changed. The canonical lesson video, page reference, and v11 remain unchanged.

Review candidate only; not installed or published. V11's outstanding continuous listening/playback review still applies; this visual-only repair does not change its narration verdict or claim a new listen-through.

Build and verification: `.video-venv/bin/python scripts/video/build_make_your_move_v12.py`. The script refuses to overwrite a candidate, locks source and board hashes, and writes `verification.json` plus transition strips.

## Local shipping — October 23, 2026

The owner reviewed v12 and explicitly approved: “Looks good. Ship this version of Make Your Move locally.” Installed the approved bytes at `course-assets/make-your-move/make-your-move.mp4`; SHA-256 matches the candidate and committed file. Updated the page cache key to `20261023ship12` and runtime to `3 min`. Matching lesson text and three-career board are included.

**Shipped locally; queued for batch deployment.** Commit: `d6df030a807420a7b4a7a03caace1600d9ee1616`. Only the nine Make Your Move release files/selected portions were committed; unrelated working changes remain. No push or deployment performed. Owner playback approval is recorded separately from automated checks; no additional assistant listening or full-playback review is claimed. Earlier “not installed” statements above describe the pre-approval review stage.

Post-commit cleanup removed the four regenerable eight-second WAV join excerpts from the v11 audit. Source videos, both candidates, transcripts, manifests, preview images, transition strips, and build scripts are retained.
