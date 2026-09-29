# Art of Prompting v9 — narrow visual repair, September 29, 2026

Built on David's “build it please,” approving the preceding live evaluation. Candidate only; no local installation, commit, push, or publication.

- Candidate: `Prompts/art-of-prompting-v9.mp4`.
- Source: `Prompts/art-of-prompting-v8.mp4`, verified against the public video during the evaluation. SHA-256 `9805eddcd0e97de5a683c2751034e3a7c44a81d13d91a11e1543b1eda6414ad6`.
- Candidate SHA-256: `01be5736ad8b3eba49c5e0156b048934e42abe6ecc7f920ac0f3aef55027fa58`.
- Runtime: **3:51.20**, 6,936 frames, 30 fps, 1280×720.
- Build: `.video-venv/bin/python scripts/video/build_art_of_prompting_v9.py`.
- QA: `.video-venv/bin/python scripts/video/qa_art_of_prompting_v9.py`.

## Approved changes

| Output span (half-open frames) | Change |
|---|---|
| 1:54.900–2:04.333, [3447,3730) | Removed the three malformed handwritten margin notes from the document drawing. Preserved the paper, meaningful “reference photo” label, arrows, highlighting, and source motion. Text masks follow each frame using feature tracking; minimum 1,875 homography inliers. |
| 2:23.467–2:29.633, [4304,4489) | Removed the stray cursor-like mark using adjacent same-frame paper. Added “WEAK PROMPT” during the lead-in, then the exact sentence “Write a caption for our lacrosse championship photo.” at 2:26.400 with a six-frame fade. Text follows the paper movement; minimum 1,529 tracking inliers. |
| 3:35.567–3:51.200, [6467,6936) | Replaced the old tinted close with the page's canonical white JPG, composed through `make_close_board.py --lesson prompting`. Preserved 48-frame initial hold, 150-frame push to 1.2×, settled final hold, and exact wording. |

No narration cuts, grafts, level changes, pauses, or timing changes. AAC is copied directly. The teaching-board appearances and their approved framing/highlights remain as in v8. The longest uninterrupted board run remains 22.767 seconds. The better-caption animation, including its final senior-voice panel, remains intact.

Only the finished v8 source survives locally; the original raw generations were removed previously. This candidate uses one further H.264 picture encode at CRF 16. No intermediate lossy render was used. Hashes bind the source and canonical close in `manifest.json`.

## Review limitations

The previous evaluation's narration KEEP verdict remains applicable because the audio is copied, but no listening or real-time end-to-end audiovisual pass was performed here. The old audio joins at 0:48.5–0:50.5 and 3:14.0–3:16.5 still warrant listening. This is a narrow candidate for review, not a whole-file shipping certification.

The original scope, teaching review, board plan, and pre-existing limitations are in `../art-of-prompting-live-review-2026-09-29/REVIEW.md`. No unrelated course files or tracker status were changed.

## Encoded candidate verification

- Full sequential comparison decoded exactly 6,936 frames in both v8 and v9; 30 fps and 231.2-second timeline retained.
- All **10,840 AAC packets and their PTS/durations are identical**. Packet-byte SHA-256: `f0f517593fad120072f6b1919ad3acd7b20f57ec6fdbeaa61fbc5a18f4f2a5eb`.
- Every frame outside the three edited intervals was compared at 160×90. Maximum mean absolute channel difference was 2.812/255, consistent with the disclosed additional encode; no timeline shift.
- Transition guard passed all **15** declared boundaries. The five boundaries entering/leaving changed spans were visually inspected as every-frame strips; each has the intended destination on its first frame, with no stale picture flash.
- Encoded start/middle/end samples of both repaired scenes were inspected. The malformed notes are gone, the prompt fits, and the later better-caption final state is intact at frame 4888.
- Encoded close retains 720 → 864 px pill width, exactly 1.2×, and remains the literal final frame. The source canvas is RGB 255/255/255; encoded audit samples are approximately RGB 252/254/251, a small lossy color-conversion/quantization deviation.
- Both the v8 review source and the canonical live file still match the original hash. No installation or publication occurred.

Evidence: `manifest.json`, `verification.json`, `encoded/`, `encoded-sheet-*.jpg`, and `guard/transition-guard.md`. Visual checks above do not substitute for the unperformed listening and continuous playback noted earlier.

## Shipped locally — September 29, 2026

David: “ship it,” following the candidate delivery and disclosed listening limitation. Installed v9 byte-identically at the canonical path; updated only its page cache key (`20260929ship17`) and manifest hash/bytes. Duration label stays “4 min.” Local commit **1264d391c91162d2c92ba16e6594729db2ef3378** contains only those three release files. No push or Vercel deployment. **Queued for batch deployment.** Listening remains unperformed; no new audio-quality certification is implied. Scoped render-scratch cleanup completed with zero matching files. Candidate and audit evidence retained.
