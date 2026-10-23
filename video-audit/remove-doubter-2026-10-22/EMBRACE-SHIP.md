# Embrace the Future opener v6 — shipped locally

David explicitly approved shipping this candidate on 2026-10-22: “Ship Embrace the Future Opener.”

- Local commit: `93b4e4e19c450f0ea3659a7ac85860f5e7fa1736`.
- Installed file: `course-assets/embrace-the-future-opener/embrace-the-future-opener.mp4`.
- SHA-256: `f58c28af2ef8773a38f90e75482cb416a566ee933641a6481faf8b1f3c270944`.
- Runtime: 3:17.300; 5,919 frames at 30 fps; 1280×720.
- Course cache key: `20261022v6`; existing “3 min” display retained.
- Status: **shipped locally; queued for batch deployment**. No push or public deployment performed.

Verified the installed file hash against the approved candidate, decoded all 5,919 frames, and verified the locally served video hash and updated course reference over HTTP. Prior frame mapping, audio analysis, transcription, and transition-strip checks are recorded in the candidate QA. Prep sync and staged diff checks passed.

David's explicit shipping approval supplies owner acceptance after the review handoff. Independent end-to-end editor listening was not performed, and is not claimed here; technical checks alone were not treated as a listening pass.

The commit includes only the opener's video, matching written lesson, prompt, course reference, asset metadata, and prep status. Loudest Voices remains unshipped and uncommitted. Shared-file staging preserved those pending edits.

Cleanup removed only the opener's regenerable audio WAV (about 38 MB). Candidate, stable source snapshot, transcripts, manifests, visual evidence, and active Loudest Voices scratch remain available.
