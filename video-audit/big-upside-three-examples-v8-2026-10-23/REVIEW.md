# Big Upside v8: three-example lesson

Status: shipped locally; queued for batch deployment. Owner approved v8 and explicitly requested “Ship Big Upside v8 locally.” The previously disclosed lack of agent direct listening and continuous audiovisual playback remains documented; no new listening certification is claimed. Video Tracker was not accessed or changed.

Candidate: `Prompts/big-upside-v8.mp4`, 3:19.567 (5,987 frames at 30 fps, 1280×720). Reduced from 4:17.300 by 57.733 seconds.

Source: stable `Prompts/big-upside-v7.mp4`, byte-identical to the installed video before this release. Original raw rolls are unavailable. The first 3,049 video frames (through 1:41.633) are packet- and pixel-identical. The remaining picture is encoded once from that source plus the current board and retained illustration. The source narration is trimmed and encoded once; no generated speech, speed changes, gain changes, or added pauses.

## Authorized content edit

Retain AlphaFold, the Hassabis story and quotation, the personal connection, and the standard closing. Remove Urgent Scans, New Antibiotics, Targeted Spraying, the former health-board introduction and health banner, and the redundant everyday-board introduction. Move the original daily-routines bridge before Finding Cancer. Move “The doctor evaluates the scan and decides what care is needed” immediately after the Swedish trial. Remove “In the middle column” so Flood Warnings matches its new right-hand position. The original same-speaker line now begins “We have flood warnings.”

The revised cancer board says “Doctors review the breast scans and decide what care is needed”; retained narration uses the equivalent original sentence about the doctor evaluating the scan. The Swedish trial qualification stays intact. Flood warnings remain assistance, not a guarantee. No other examples are introduced.

## Output edit map

| Output | Source v7 | Retained material |
|---|---|---|
| 0:00–1:41.633 | 0:00–1:41.633 | AlphaFold, Hassabis and quotation |
| 1:41.633–1:45.533 | 2:37.300–2:41.200 | Daily-routines bridge |
| 1:45.533–1:57.600 | 1:45.233–1:57.300 | Finding Cancer and Swedish trial |
| 1:57.600–2:01.300 | 2:11.667–2:15.367 | Doctor evaluates and decides care |
| 2:01.300–2:13.600 | 2:45.200–2:57.500 | Reading Aloud |
| 2:13.600–2:24.800 | 2:58.700–3:09.900 | Flood Warnings |
| 2:24.800–3:19.567 | 3:22.533–4:17.300 | Takeaway, personal connection, standard close |

## Board and camera plan, verified on the encode

| Board | Highlights | Camera | Screen time / break |
|---|---|---|---|
| Helping People Live Better | Cancer at its spoken title, Reading Aloud at its title, Flood Warnings at its title, then gold takeaway | Complete unmarked board for 3.9 seconds; uniform complete-card dives; widen before Flood Warnings so its ring stays visible; return to full view for takeaway | 1:41.633–2:33.900, with existing menu-reading illustration at 2:03.500–2:12.400 |

Exact asset: `course-assets/big-upside/big-upside-examples.jpg`. Complete card edges are (40,127)–(525,815), (557,127)–(1043,815), and (1075,127)–(1560,815). All changed highlights use the fixed 4 px stroke at 720p, teal/teal/blue, and purple for the takeaway. Unchanged boards retain their shipped treatment. Longest uninterrupted changed-board run is 21.867 seconds; the second is 21.500. Both stay on the spoken examples and are separated by the relevant menu scene. No decorative filler was added.

The menu-reading illustration is the existing purpose-generated asset from v6/v7, gently pushed for 8.9 seconds under the menu/phone explanation. The brain-scan, antibiotic-lab, and weed-spraying cutaways are removed with their topics. The brain-scan illustration was not reused for breast cancer.

## Verification

- Sequentially decoded all 5,987 frames; frame count, constant 30 fps timestamps, dimensions, and duration match the plan.
- All 3,049 opening video packets and decoded pixels match v7 exactly. All 1,370 retained ending frames match their proper source frames within one encode (maximum mean pixel error 2.669/255).
- Six audio joins fall in measured quiet endpoints (-64.6 to -90.1 dBFS); only a 5 ms fade at each quiet edge. Encoded join correlations against edited PCM exceed 0.99997.
- Fresh ASR of the encoded candidate confirms the three retained examples, the moved human-judgment sentence, and the corrected flood introduction; deleted examples and “middle column” are absent. ASR is not proof of pronunciation or natural cadence.
- Inspected actual encoded settled-card frames, the full board, menu cutaway, and every transition strip. Complete cards and all rings remain inside the frame.
- Transition guard automatically passed 7/9 boundaries. Its flags at output frames 4008 and 4344 are intentional smooth pullbacks. Every-frame strip review and 62 frame-to-planned-render comparisons resolve them as camera motion, with no stale frames. Raw automatic results remain untouched in `transitions/`; the hash-bound manual disposition is `transition-review.json`.
- Source video, installed video, lesson text, page, board and illustration hashes are unchanged by this video build. No deployment.

## Listening still required

New joins are at 1:41.633, 1:45.533, 1:57.600, 2:01.300, 2:13.600, and 2:24.800. `join-review.wav` contains two seconds either side of each, in that order, separated by half a second of silence. The half-second separators are only in this review reel, not in the candidate.

Direct listening and continuous audiovisual playback have not been performed. Confirm natural cadence and complete word attacks at the six joins before shipping. Prior v7 notes also leave Hassabis pronunciation and an older question-line graft for listening; this narrow edit preserves those areas. The older question graft is now around 2:33.9–2:40.7.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_big_upside_v8.py` (refuses to overwrite an existing candidate).

QA: `.video-venv/bin/python scripts/video/qa_big_upside_v8.py`.

Fresh ASR: `.video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/big-upside-v8.mp4 --output-dir video-audit/big-upside-three-examples-v8-2026-10-23/transcripts`.

Source/output spans, hashes, geometry, and visual runs: `edit-manifest.json`. Mechanical checks: `qa.json`. Candidate transcript: `transcripts/big-upside-v8.txt`.

## Local release

Installed the approved v8 at `course-assets/big-upside/big-upside.mp4`. Updated its cache key to `20261023v8` and displayed duration to `3 min`. Commit `d493e4f90b18c300f6ae78cc6c146cbc53e1a81f` contains only the MP4 and that one `index.html` entry. Installed and committed video hashes match the approved candidate. No push or deployment was performed.

Post-commit cleanup removed the two untracked regenerable WAV files, including the listening reel. Candidate, raw source, audit records, transcripts, and encoded previews remain.
