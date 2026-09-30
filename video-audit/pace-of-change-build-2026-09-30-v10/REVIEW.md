# Pace of Change v10 — shipped locally

Built September 30, 2026, following David's approval to remove the four-idea preview while keeping the conceptual-map transition.

[Open v10](../../Prompts/pace-of-change-v10.mp4) — 4:22.40, 7,872 frames, 1280 × 720, 30 fps. Shipped locally September 30, 2026; queued for batch deployment.

## Change from v9

Removed exactly 12 seconds: original source frames 5594–5954 (3:06.467–3:18.467), corresponding to v9 2:48.967–3:00.967. This removes the four-idea introduction and its preliminary explanation of which milestones are hypothetical. The later explanation remains.

The full board still appears at 2:46.40. The retained narration is:

> AI is already helping people build better AI. Look at this conceptual map of the future. The first is automated AI research.

The new join is at 2:48.967. The existing 24-frame camera move begins there, and the Automated AI Research highlight appears at 2:49.767 as teaching begins. The complete left card is visible. No pause was added; the retained quiet gap measures 0.837396 seconds in the encoded audio.

All approved v9 repairs remain, including its earlier narration cut, three supporting visuals, and full final-board banner. Later timestamps move 12 seconds earlier. Built directly from the same finished v8 source, avoiding another generation of compression from v9. The v9 candidate is preserved byte-for-byte.

## Verification

- Full candidate decode passed: 7,872 frames, no decoding errors.
- 294 retained-frame comparisons match mapped source frames within encoding differences (maximum mean absolute difference 2.596 / 255). All 43 replacement samples match planned assets (maximum 3.722 / 255).
- The transition guard passed 24 of 25 boundaries automatically. It flagged four adjacent pairs within the existing camera zoom after the new join. Manual inspection of the every-frame strip shows continuous movement with no intermediate shot. All 27 frames spanning the join and complete camera move match their exact mapped source frames, maximum difference 2.402 / 255. The original automated FAIL is preserved; this is a documented motion false positive, not an automatic pass.
- The new transition strip and full-resolution first-highlight frame were inspected, along with the corrected final banner and final frame.
- Retained PCM is sample-identical to the source outside the two four-millisecond seam interpolations. Encoded audio matches edited PCM at 43.30 dB signal-to-error ratio. New seam peak is −55.04 dBFS.
- Speech recognition on the encoded join confirms “Look at this conceptual map of the future. The first is automated AI research. Currently, AI can write code, run experiments…” with the four-idea preview absent.
- Source MP4 and canonical boards remain unchanged. v9 SHA-256 remains `388f84fc1d76bac210de0f4d2096b0e1b9b4608d98dbe1ee1fc9e3c76f444fc5`.

Listening and continuous audiovisual playback remain unperformed. Speech recognition and waveform checks do not certify subjective cadence. Review the join around 2:49 before shipping; no final shipping certification is claimed.

Evidence: [manifest](edit-manifest.json), [verification](verification.json), [transition guard](transitions/transition-guard.md), [camera-move comparison](new-join-motion-comparison.json), [join transcript](narration-join-transcript.txt), [encoded audition clip](encoded-narration-join.wav).

Build: `.video-venv/bin/python scripts/video/build_pace_of_change_v10.py`

QA: `.video-venv/bin/python scripts/video/qa_pace_of_change_v10.py`

Candidate SHA-256: `205bbf7c816b901ff42a46ad9f87e67aaf3cf46b252e671a83f0e2469d4d73c7`.

## Local shipping — September 30, 2026

David explicitly requested “ship it” after the listening limitation was disclosed. Installed the approved candidate at `course-assets/pace-of-change/pace-of-change.mp4`; its SHA-256 remains `205bbf7c816b901ff42a46ad9f87e67aaf3cf46b252e671a83f0e2469d4d73c7`. No claim of performed listening or continuous playback is added by shipping approval.

Local commit: `b1c76e989336f28be73e8ff6bc38bfae83501e09`. Five release files only: canonical MP4, this lesson's two index.html changes, Markdown, prompt, and Pace of Change section of the lesson kit. Unrelated work remains unstaged. Course cache key: `20260930ship10`; displayed runtime: 4 min; exact runtime: 4:22.40. Verified both the installed and staged asset hashes, local course reference, and release scope before committing. Upload sync check passes.

Status: **shipped locally; queued for batch deployment**. No push, deployment, public-live verification, or tracker update performed.

After commit, the scoped cleanup removed 11 regenerable WAV/canvas files (0.11 GB) from this lesson's v9/v10 audit directories. The linked audition WAV above is now cleaned scratch; transcript, comparisons, manifests, contact sheets, transition strips, and candidate MP4s remain. The original v8 source can be recovered from Git commit `dff28c5b066ccb59824fc436577a89ed76c06c3c`; builder/QA source paths require that historical source rather than the newly installed canonical MP4.

