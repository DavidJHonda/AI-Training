# Loudest Voices v12 — shipped locally

David explicitly approved shipping the reviewed candidate on 2026-10-22: “Ship Loudest Voices.”

- Commit: `3c9d8b0bb1ec42744bcd56dcda00b570b15dd558`.
- Installed video: `course-assets/loudest-voices/loudest-voices.mp4`.
- SHA-256: `31a18fc49cc76e576ea736d23160bc516f486e9160df6557c5f0a018ad4edc37`.
- Runtime: 4:36.733; 8,302 frames; 1280×720 at 30 fps.
- Course cache key: `20261022v12`; runtime pill: 5 min.
- Status: **shipped locally; queued for batch deployment**. No push or public deployment performed.

Verified installed bytes against the approved candidate, decoded every frame, and checked the locally served video hash and updated course reference over HTTP. Prep synchronization and staged diff checks passed. Prior candidate QA covers source-packet preservation, board rendering, narration transcription, audio joins and transition strips; the final edit's checks are in `qa.json`.

David's explicit shipping instruction provides owner acceptance after review. Independent end-to-end editor listening was not performed, and is not claimed; technical checks were not represented as a listening pass.

The release commits the video, two-expert board and native renderer inputs, lesson text, matching prompt/prep status, website references, and board documentation. Build/audit records remain local as required by the repository's shipping workflow.

Removed only the regenerable v10 pre-AAC audio WAV (about 54 MB). Its hash remains in the build manifest; it can be regenerated from the retained original source spans with `build_remove_doubter.py`. Candidates, source videos, transcripts, manifests and visual evidence remain available.
