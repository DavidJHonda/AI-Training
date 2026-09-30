# Training Bias v9: approved narration cuts

Candidate: `Prompts/training-bias-v9.mp4`. Narrow repair, ready for owner review; not installed, committed, or published. Runtime **217.433 seconds (3:37.43)**, down from 261 seconds. **43.567 seconds removed.**

User authorization: “Now, let's make the cuts from the video please.” This follows approval to remove the repeated explanation around :46–:56 and the Cooper Flagg demonstration plus its cause caveat around 2:38–3:12. The written lesson was updated separately before this build.

## Cuts and joins

All source times refer to the original v7/v8 timeline. Frame ranges are half-open at 30 fps; audio uses matching 48 kHz sample boundaries, inside measured quiet gaps.

| Source removed | Frames | Removed narration | New output join |
|---|---|---|---|
| 0:45.500–0:55.500 | 1365–1665 | “An AI model repeats the shape of its training data. When a data set only captures a narrow slice of reality, the model interprets that limited view as the entire world.” | 0:45.500: “…an old picture.” → “This diagram shows how skewed data…” |
| 2:38.133–3:11.700 | 4744–5751 | “Let's look at this chat interface…” through “…stale information from a hallucination or another error.” | 2:28.133: “…missing from its worldview.” → “This illustrates a vital rule for any fact check.” |

The current-source verification rule, all three questioning prompts, RAG explanation, and closing message remain. No new narration, voice grafts, or pauses were added.

## Visual treatment

| Affected visual | Treatment |
|---|---|
| How Skewed Data Distorts the Picture | Bring the complete unmarked destination board forward five source frames (1665–1670) to the audio join. Preserve v8's subsequent highlights and cutaways. |
| Stale Information in Real Life | Remove the entire Cooper Flagg board, including its introduction and associated cause diagram. |
| Verify Dates supporting drawing | Bring its first frame (source 5764) forward thirteen frames to source 5751, covering the deleted cause diagram until the retained animation resumes. |

All other v8 visuals retain their source-relative timing, framing, highlights, and motion. Source material reused in v8's later cutaways remains, including the data/worldview illustration during Defaults. The canonical closing image remains the final frame.

## Source and reproducibility

Recreated the v8 visual treatment from its SHA-locked finished v7 source `/private/tmp/training-bias-v7-0423a1b5f343.mp4`, rather than re-encoding v8. Raw generations are unavailable. This is one video re-encode from v7; trimmed source audio is encoded once to AAC.

- Source SHA-256: `0423a1b5f34337d130fbb1ff9392fa45ffab98d09426b47da68c8b99bc9917cd`.
- Candidate SHA-256: `a4f6a71c0d27b179f402ccc6cb20a99f803d9bf0e095c03f336e6e70a4f8b1db`.
- Build: `.video-venv/bin/python scripts/video/build_training_bias_v9.py`.
- QA: `.video-venv/bin/python scripts/video/qa_training_bias_v9.py`.
- Exact source/output mapping, protected hashes, and all boundaries: `edit-manifest.json`.

## Completed verification

- Exactly **6,523 decoded frames**, 1280×720 at 30 fps, uniformly spaced video timestamps.
- **25/25 declared transition checks passed**, including inherited v8 boundaries. Both new join strips and their first destination frames were visually inspected, along with the final frame; no remnants of deleted shots appeared at the joins. Inherited boundary strips are retained but were not all manually re-inspected in this narrow pass.
- Retained visuals sampled once per second against mapped v8 frames: mean absolute channel difference 0.030/255, maximum sampled frame mean 1.334/255.
- Encoded audio matches the planned trimmed source timeline, with 44.38 dB signal-to-error ratio after AAC encoding. Source cut-point RMS levels over 40 ms are below −56 dBFS. Encoded seam RMS levels over 20 ms are −59.70 and −61.34 dBFS.
- The encoded second join has a continuous 0.565-second quiet gap at −38 dB. The first has about 0.511 seconds of near-contiguous quiet at the same threshold, interrupted by a sub-millisecond threshold crossing; the splice itself falls in its final 0.409-second quiet interval. No digital silence was inserted.
- Fresh word-level source transcripts checked the four cut endpoints. Fresh encoded join transcripts retain the expected complete surrounding sentences. ASR reads the retained date rule as “Whenever a specific date matters…”; this is supporting evidence, not an auditory verdict.
- Hashes confirm v8, the installed video, all canonical JPGs, the edited lesson source, and `index.html` remained unchanged during this build.

## Review limitations and remaining work

No actual audio audition or continuous full-video watch was performed. Listen at **0:45.50** and **2:28.13** for cadence, breaths, clipped phonemes, and clicks. Contextual audio clips are `join-1365.wav` and `join-4444.wav`. Waveforms, transcripts, and correlation do not certify a listening pass.

This cut-only candidate retains the previously noted early graphic headed “Training Bias” above both skewed and stale data. Its framing ambiguity was corrected in the written lesson, but neither this graphic nor the surrounding narration was rewritten in this cut pass. The earlier RAG-pronunciation listening check also remains. This is not a full production or shipping approval.
