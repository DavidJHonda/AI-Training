# Does AI Think? v11 — approved three-row repair

**Review candidate:** `Prompts/does-ai-think-v11.mp4`, **3:12.20**, 5,766 frames, 1280×720, 30 fps. This is 24.00 seconds shorter than installed v10. The installed course video, lesson, prompt and board files are unchanged. No local release commit, push or deployment was performed.

**Candidate SHA-256:** `ffe56fb6651603e84229de4d9aa6c574de8740c295bf870f583a34d4fd8136c2`.

## Approved scope and result

David authorized the repair proposed in `video-audit/does-ai-think-current-review-2026-10-23/REVIEW.md`: use the current three-row board, remove the obsolete five-part introduction/numbering and Beauty passage, and retain everything else. The original Meaning and Experience explanations remain, in their original order, under one Experience and meaning highlight. Word choice and Uncertainty follow, then the takeaway. The optional uncertainty donor was not used: “You inherently notice” remains, consistent with the instruction to preserve the rest.

All four removals use measured quiet gaps, including full word tails. Medium-model word timing was checked against the decoded waveform; transcript segment boundaries were not used as cut instructions. No pause was added. Five-millisecond de-click ramps affect only the quiet audio edges.

| Removed source interval | Source frames, end exclusive | Removed material | New join | Encoded speech gap at −40 dBFS |
| --- | --- | --- | --- | --- |
| 2:07.500–2:17.200 | 3825–4116 | Five-differences introduction and “First is meaning” | 2:07.500 | 0.623 s |
| 2:23.700–2:25.667 | 4311–4370 | “Second is experience” | 2:14.000 | 0.480 s |
| 2:32.700–2:34.667 | 4581–4640 | “Third is word choice” | 2:21.033 | 0.521 s |
| 2:42.167–2:52.533 | 4865–5176 | Complete Beauty comparison | 2:28.533 | 0.555 s |

The cut handles account for the difference from the earlier approximate 23-second estimate. The four actual encoded seams measure −75.0 to −80.6 dBFS over 10 ms. These measurements support clean placement but are not a listening verdict.

## Board treatment and retained scenes

The exact current canonical JPG (`does-ai-think-side-by-side.jpg`, SHA-256 `1b33297f6eba5cb6fb6347ca4cef21a450752e4c11a3656cc58f660033b68dbf`, 1600×1310) is used without text/layout changes. A temporary padded canvas fits it to video.

| Board/state | Output timing | Treatment |
| --- | --- | --- |
| Full comparison opening | 2:05.000–2:07.733 | Complete unmarked board, 2.733 s before the first outline. As proposed, it arrives during the preceding learned-patterns explanation, replacing that animation's last 2.967 s. |
| Experience and meaning | Outline starts 2:07.733 | One green outline around both columns of the combined first row; smooth one-second move to a complete-row view. Both old explanations use this same state. |
| Word choice | Outline starts 2:21.233 | Complete second row, same zoom width, smooth move. |
| Uncertainty | Outline starts 2:28.833 | Complete third row. At the bottom of the padded canvas its camera position matches the second row, so only the outline changes. |
| Takeaway | Pullback 2:40.567; purple outline 2:41.567; board ends 2:45.900 | Smooth pullback to the full board and edge-to-edge banner outline. |
| Chinese Room | Original timing and treatment | Preserved, including the approved camera-only walk and long continuous board run. |
| Closing board | 3:04.200–3:12.200 | Original eight-second close, with its exact animation and literal last frame; shifted earlier only by the cuts. |

Every comparison outline is drawn with the shared fixed 4 px renderer. All three retained comparison cutaways remain exact copies of their encoded video packets and decoded pixels: learned network/input at 2:10.800–2:13.300, next-word prediction at 2:25.067–2:27.867, and student checking an answer at 2:34.000–2:37.500. Their corresponding audio remains aligned. The opening, Chinese Room, subsequent useful-work scenes and closing content are retained.

## Preservation and verification

Stable source is the previously approved `Prompts/does-ai-think-v10.mp4`, SHA-256 `098b77a5b70fbc9ba6bce99e6b2b2f345343792a34688c1a2d6245a29df3771f`. It matches the installed video. Using the approved finished source allows untouched video and audio packets to remain exact; only the board replacement intervals and necessary codec handles are re-encoded. The raw generations are retained but are not used to regenerate unaffected scenes.

Completed on the actual v11 encoding:

- All 5,766 frames decode at the planned timestamps; all AAC timestamps are contiguous.
- 4,502 retained video frames are pixel-identical to their mapped v10 source frames, and their encoded packets are also identical.
- 963 updated board frames match the canonical renderer, minimum PSNR 33.81 dB.
- 301 surrounding frames had to be re-encoded to preserve valid keyframe boundaries; minimum PSNR against v10 is 47.84 dB. Their content/timing is unchanged.
- 8,008 audio packets are byte-identical to their mapped original packets. Only the comparison passage between source 2:07.296 and 2:52.693 is replaced with the edited audio. Both audio replacement edges are silent AAC packet boundaries. Retained decoded audio is exactly identical outside two adjacent codec-overlap packets. The edited passage's decoded SNR against its PCM edit master is 46.26 dB.
- Inspected all 19 every-frame transition strips, each board state preview, selected full-resolution encoded frames, and the encoded last frame. The detector flags at frames 4817 and 4847 are the beginning/end of the same continuous pullback, not visual islands; raw flags are preserved with this manual resolution.
- Fresh medium-model transcription of the actual encoded 2:00–2:50 passage confirms all retained comparison explanations, the takeaway, and removal of the obsolete introduction, labels and Beauty. See `encoded-comparison-transcript.txt` and `.json`.
- Source, installed video, lesson, prompt and canonical board hashes remain unchanged. The Does AI Think page section and video entry remain unchanged. After QA, independent commit `67696d1b` shipped Unexpected Results v6 and changed only that other lesson’s index video entry; the manifest records the verified before/after index hashes and unchanged Does AI Think scope.

The prior complete transcript review still covers the unchanged opening, Chinese Room and conclusion; retained audio is computationally tied to that reviewed v10 source. No new required teaching omission was found in the changed passage. This is not a fresh whole-file KEEP/ship certification.

## Listening and remaining review

Direct listening and full real-time playback were not performed: the available tools provide transcription, image inspection and signal analysis, not audio perception. In particular, the four new joins still need a listening check for cadence. The previously disclosed 0:39 “thread/threat” ambiguity, the existing close voice graft (now 3:04.200), and “You inherently notice” are preserved outside this approved repair.

Encoded seven-second context clips are available as `join-1-encoded.wav` through `join-4-encoded.wav`; they center on the four new joins above. The candidate is ready for user review, not installed. Do not treat the numerical checks as proof that the joins were heard.

## Reproduction and evidence

- Build: `.video-venv/bin/python scripts/video/build_does_ai_think_v11.py` (refuses to overwrite v11).
- Preview first: same command with `--preview`.
- QA: `.video-venv/bin/python scripts/video/qa_does_ai_think_v11.py`.
- `edit-manifest.json`: exact mappings, asset geometry, source/candidate hashes and protected files.
- `cut-measurements.json`, `word-timing.json`: source-word and quiet-gap evidence.
- `qa.json`, `encoded/`, `transitions/`: actual encoding checks and visual review.
- `encoded-comparison-transcript.txt`: fresh transcription of the changed passage.
