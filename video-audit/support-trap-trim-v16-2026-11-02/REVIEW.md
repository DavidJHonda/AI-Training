# Support Trap v16 — five approved cuts

Review candidate: `Prompts/support-trap-v16.mp4`.

Runtime **3:36.933**, down from **4:27.700**. Removed **50.767 seconds** (19%). The earlier 47-second estimate used approximate editorial timestamps; the build uses measured quiet sentence boundaries.

The user approved the suggested cuts except the safety-board introduction at approximately 3:25–3:33, then requested “Build it please.” That introduction is retained in full. No course installation, on-page edits, commit, or publishing is included.

## Deletions

Times below refer to the installed v15 source. Frame ranges are half-open at 30 fps.

| Source range | Frames | Removed content | New join |
|---|---|---|---|
| 1:01.300–1:23.600 | 1839–2508 | “So what is AI actually good for…” through “…check on you tomorrow.” | 1:01.300 |
| 2:17.367–2:25.067 | 4121–4352 | “If someone requires immediate, real-world help…” through “…time they do not have.” | 1:55.067 |
| 2:53.467–2:58.633 | 5204–5359 | “But it existed entirely in the digital space, lacking any real-world agency.” | 2:23.467 |
| 3:50.600–3:57.767 | 6918–7133 | “A chatbot cannot call anyone…” through “…zero real-world responsibility.” | 3:15.433 |
| 4:08.500–4:16.933 | 7455–7708 | “The protocol comes down to this single directive…” through “…a real person who can act.” | 3:26.167 |

## Picture and audio treatment

The original comparison, emotional-support and safety boards retain their existing framing, highlights and motion. The three preparation examples, story, warning and its breathing room, safety instructions, and canonical closing remain.

Two seven-frame holds prevent visual fragments from flashing at the edits:

- Hold source frame 1831 over frames 1832–1838. This keeps the comparison board through the end of “support” without briefly showing the phone illustration belonging to deleted narration.
- Hold source frame 5203 over retained source frames 5359–5365. This bridges directly from the existing diagram state to the family illustration without flashing the final diagram state from the deleted explanation.

No new narration, added pauses, global gain changes, or changed playback speed. Each audio splice falls in measured quiet shoulders, with five-millisecond fades at its edges. The complete closing sequence and literal final frame are retained.

## Verification

All 6,508 encoded frames match the planned source mapping, including the two short holds; presentation times are uniform. All 28 automated transition checks pass. Inspected the five joins, repaired boundary strips, preserved safety-board entry, overview sheets and final frame. Encoded audio correlation with the planned edit is 0.999990; the five joins fall in quiet intervals of 0.43–0.71 seconds. Full encoded transcription confirms the approved deletions and retained safety-board introduction. Protected source and installed course files are unchanged.

See `qa/results.json` for the final candidate hash and checks, `qa/transcript.txt` for transcription of the encoded candidate, and `qa/transitions/` for frame-by-frame boundary strips.

Build: `.video-venv/bin/python scripts/video/build_support_trap_v16.py`

QA: `.video-venv/bin/python scripts/video/qa_support_trap_v16.py`

The hash-verified finished v15 is the edit source, with one additional H.264/AAC encode. Original raw generations remain available. Retained narration has not been rewritten or fact-checked in this edit. Automated transcription and waveform checks do not certify perceptual audio quality; listening and continuous playback have not been performed.

Status: review candidate only; not installed or published.

## Local release — November 2, 2026

Owner approval: “ship it”. Installed v16 at `course-assets/support-trap/support-trap.mp4`, updated the cache key to `20261102ship16`, changed the rounded duration label to 4 min, and updated manifest hash, size and approved version.

Commit: `256e7344547847f8be953be36c37e633d2fb8956`. Exactly three production files committed; unrelated working edits preserved. The committed and installed video hashes match the approved candidate. Two inline scripts parse and the current asset verifier passes.

**Shipped locally; queued for batch deployment.** No push or public deployment performed. See `local-release.json`.
