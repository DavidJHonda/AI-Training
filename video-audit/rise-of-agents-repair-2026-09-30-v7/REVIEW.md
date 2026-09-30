# Rise of Agents v7 — compact board and closing advice

Built `Prompts/rise-of-agents-v7.mp4`: **2:50.40**, 5,112 frames, 30 fps, 1280×720. **Shipped locally in commit `20f7fc81`; queued for batch deployment.**

## Authorized changes

The user requested removal of “AI should not send, spend, submit, delete, or post without you reviewing first.” from lesson and video, and incorporation of the redesigned Rogue Agents box.

- Removed the sentence from `index.html`, lesson Markdown, generation prompt and active kit instructions. Synced the upload bundle.
- Cut source frames [4901, 5088), **2:43.367–2:49.600**, removing 6.233 seconds. Output join: **2:32.200**. The warning now leads into “Treat agents as advanced tools.”
- Removed the review-button and eye-button imagery in full. The preceding warning holds for two extra frames in the retained quiet gap; the advanced-tools scene starts seven frames early in the following quiet gap, then resumes its original motion.
- Inserted the exact current compact Rogue Agents JPG at both board appearances. The inner title is gone, the date pill is above the right-hand paragraph, and the quote appears once in the gold banner.
- Board treatment: compact, full view, no crop or zoom. Scale 0.775, offset (20, 96), 1240×527 inside 1280×720. Quote banner ring is fixed 4 px, #6e51ff, at the quotation introduction. Board spans: 2:01.10–2:09.50 and 2:22.767–2:27.467.
- Preserved the previously approved Gemini removal, PocketOS label corrections, other teaching and standard close. Rebuilt from verified finished v4 with one final encode; v6 was not used as a lossy intermediate. Raw rolls are unavailable.

## Verification

- Decoded the actual encoded file to exactly 5112 frames and 170.4 seconds.
- Transition guard passed all seven boundaries. Inspected the every-frame strips, new join frame, board preview and literal final close.
- Compared all 393 board frames against their intended canonical render; maximum mean channel error 2.7852/255.
- Compared 4312 unaffected frames against v4; maximum mean channel error 2.7919/255.
- Retained PCM is exact outside the two 4 ms splice bridges. The new splice endpoints are in measured quiet intervals around −68 dBFS; no added pause or gain change. Encoded AAC correlation with intended PCM: 0.999990024.
- Transcribed the actual encoded ending with medium.en. It contains the quotation, goal warning, “Treat agents as advanced tools,” ChatGPT advice and close, with neither removed sentence. See `transcript/encoded-ending.txt`; timestamps are relative to output 2:20.
- Upload sync and scoped whitespace checks pass. Canonical video remains unchanged.

## Review limits

The new audio join has not been directly auditioned. Listen around **2:32.20** for cadence; `encoded-join-4566.wav` provides context. Automated transcription and sample checks do not replace listening. No full-motion, end-to-end audiovisual shipping certification is claimed. Previously documented opening wording and delayed-discovery omission remain outside this narrow repair.

Build: `.video-venv/bin/python scripts/video/build_rise_of_agents_v7.py`

QA: `.video-venv/bin/python scripts/video/qa_rise_of_agents_v7.py`

Candidate SHA-256: `c7377765375cf8092f1ef45a4c76b6db8513d287edd556835f9a2a2f95eb03b4`

Source SHA-256: `d27f50d630ccae490c6d6c9511d6694d638e65dc073e8dd4ff9a4887ebfe8dcd`

Board SHA-256: `a95dbe1799a2aff7798a520f3653715e14caa2bc20be922b8d3a3ccba3511e46`

Records: `edit-manifest.json`, `qa.json`, `transitions/transition-guard.md`, `transitions-overview.jpg`.

## Local shipping

User approved v7 with “ship it” after the listening limitation was disclosed. Installed the exact verified candidate at `course-assets/rise-of-agents/rise-of-agents.mp4`; SHA-256 is unchanged. Updated `LESSON_VIDEOS.agents` to cache key `20260930ship1`; the 3 min pill remains appropriate for 2:50.40. Committed the video, redesigned board, lesson text and supporting source changes in `20f7fc81b6011e765a1fca0d9c24af0f48bfb187`. Unrelated work remains untouched. No push or deployment performed.

Removed 12 regenerable WAV scratch files from this task’s v5/v6/v7 audit folders (~0.07 GB) after commit. Encoded MP4s, transcripts, manifests, checks and frame strips remain. Audio contexts can be extracted again from the retained candidate. The old finished v4 source is recoverable from the pre-release commit and blob recorded in `shipping.json`.
