# The Next Token and Critical Thinking — board refresh

October 23, 2026. Scope: synchronize the adjusted canonical boards into the two finished videos, retaining the existing highlighting interaction, narration, timing, cutaways and other footage. Review candidates only; the installed course videos and lesson references remain unchanged.

| Candidate | Board | Output frames (30 fps; end exclusive) |
| --- | --- | --- |
| `Prompts/the-next-token-v4.mp4` | Same Probabilities, Different Choices | 1600–2304 and 2556–2710 |
| `Prompts/critical-thinking-v16.mp4` | What You Know. How You Think. | 0–1057 |
| Same candidate | Five Habits of Critical Thinking | 3468–3768, 3922–4454, 4634–5099 |

The Next Token retains the original full-board treatment and four highlight states at their original frame positions. Its canonical board is now 40 pixels taller to accommodate the larger note. The canvas fits the whole updated board; the right-panel and note-only highlight boxes extend to board y=764 to enclose all three lines. Ring colors, stroke and onset times are unchanged.

Critical Thinking retains the original gentle opening push, each habit's pan/zoom, all highlight times and legacy stroke weight. The previous 12-second opening trim, 15-frame opening hold and 18-frame hold around the approved spoken-word repair are reproduced. Both original cutaways are packet-copied. No narration repair or timing change is introduced.

## Source preservation and evidence

Each build starts from a frozen copy of the currently installed video, with its exact source hash checked. The builder re-encodes only the required GOP intervals and copies all remaining video packets plus every audio packet. The Next Token requires two unchanged surrounding frames to be re-encoded; Critical Thinking requires 20. The frozen sources, current board JPGs, lessons, installed videos and index are protected by hashes.

Per-video `manifest.json` records source/candidate hashes, encoding intervals, prepared board specifications and the precise geometry/timeline mappings. `qa.json` records checks on the actual encoded file. `transitions/` contains raw detector results and every-frame strips. All original render and review candidates are retained.

Build scripts: `scripts/video/build_board_font_sync_round2.py` and the shared `build_board_font_sync.py`. QA scripts: `scripts/video/qa_board_font_sync_round2.py` and the shared `qa_board_font_sync.py`. Builders refuse to overwrite a review candidate.

Direct listening and full real-time playback were not performed. Computational audio identity checks establish that sound is unchanged; this pass does not claim a new end-to-end narration review.

## Completed verification

Both encoded candidates passed frame-count, timestamp, original audio packet and decoded PCM identity checks. All video packets and decoded pixels outside the replacement GOP intervals are identical to the source. The installed videos, lessons, canonical boards and index remain unchanged.

| Candidate | Updated board frames | Exact retained frames | Re-encoded handle frames | Minimum board-render PSNR | Minimum handle PSNR |
| --- | ---: | ---: | ---: | ---: | ---: |
| The Next Token v4 | 858 | 5,173 | 2 | 35.57 dB | 51.60 dB |
| Critical Thinking v16 | 2,354 | 3,219 | 20 | 34.11 dB | 49.74 dB |

All highlight states, selected full-resolution encoded frames, and every frame in the 9 Next Token and 20 Critical Thinking transition strips were visually inspected. Next Token passed the automated transition detector. Critical Thinking's flags at frames 3689, 4169 and 4373 were reviewed as continuous original camera moves, with no new visual islands or transition defects. The raw detector flags remain in the evidence; the separate visual-review result is tied to the candidate hash.

The transition checker was corrected to clamp its inspection start to frame zero for boundaries close to the beginning. Critical Thinking's frame-5 highlight now completes that check. No video rebuild was needed for this checker fix.

Both candidates are ready for user review. They have not replaced the installed course videos.

## Local installation — October 23, 2026

David explicitly approved replacing both installed videos with these reviewed candidates. Installed and byte-verified The Next Token v4 (`3692635c319e3fbf439ff676efbc4c6d452dc1013cd39968b39bda72d2b4fa57`) and Critical Thinking v16 (`7311d15693bbe2f8994d1dc9a1ce142a03b6ff0c16ace8ce2d0fd830c30c62d2`). Updated their canonical lesson cache keys to `20261023ship4` and `20261023ship16`; both displayed runtimes remain 3 min.

Local release commit: `3f89fb15437648a6e39b3abe8741489b5fc40f9c`. Only the two canonical MP4s and the two index references are included. Shipped locally; queued for batch deployment. No push or deployment was performed. The documented narrow visual/audio-identity checks apply; no new end-to-end listening pass is claimed.
