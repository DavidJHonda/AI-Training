# What is AI? v14 — shipped locally

Owner approved shipping the reviewed candidate on 2026-10-22: “Ship What is AI?”

- Commit: `375353da9cf9521e4d95d943ca79cd08194839bd`.
- Installed path: `course-assets/what-is-ai/what-is-ai.mp4`.
- SHA-256: `738113d2f4bcb6d805960fc0405e042dafcf90ea29809356e66e856ff83315af`.
- Runtime: 2:46.5; 4,995 frames; 1280 × 720 at 30 fps.
- Course cache key: `20261022v14`; rounded runtime label remains 3 min.
- Status: **shipped locally; queued for batch deployment**. No push or public deployment performed.

Installed bytes match the exact approved candidate and its prior QA manifest. Verified the locally served video SHA-256 and updated lesson reference over HTTP. Staged diff checks passed; the commit includes only the installed video and its one-line course reference update. Existing untracked prep, build, and audit work was preserved.

The exact candidate already passed every-frame source/render comparison, frame/timestamp verification, audio correlation, fresh transcription, all 12 transition gates, inspected transition strips and board/closing frames, and measured additional pause. See REVIEW.md and qa.json. The 4 px outline implementation follows the current Edit Spec over the older 5 px wording still in the general checklist.

The owner's shipping instruction supplies acceptance after review. Independent end-to-end editor watching/listening was not performed and is not claimed. The prior disclosure about direct listening remains in the review record. The external Video Tracker was not accessed or modified.

After committing, removed 12 regenerable scratch files (approximately 0.09 GB) only from this lesson's v12, v13, and v14 audit folders. Candidates, raw source rolls, scripts, manifests, transcripts, and visual evidence remain available. Scratch can be regenerated from retained source files and builder scripts.
