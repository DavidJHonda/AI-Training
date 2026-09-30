# Big Upside approved visual repair

User authorization: “Agree. Build it please.” This implements the live evaluation's two recommended visual changes, including its proposed supporting scenes. This is a narrow visual repair and review candidate, not shipping or deployment.

Source: verified live v5, `course-assets/big-upside/big-upside.mp4`, SHA-256 `a7d56ee3a5a5f4e4968c125719077130c7317f31872fc1c52d3ce22ecffb4c06`. Raw rolls and their render intermediates are absent. Encode the pictures once from this source, preserve its 7,719 frames at 30 fps, and copy its original AAC unchanged.

| Board | Highlighting and camera | Breaks and treatment |
|---|---|---|
| Helping People Stay Healthy | Full view; whole Finding Cancer card, Urgent Scans card, New Antibiotics card, then banner. Preserve onsets and camera path; update outlines to fixed 4px at 720p. | Show doctor reviewing a flagged scan at 2:03–2:11, laboratory testing at 2:25–2:30. Return to the same board and active card, with no restart or pause. |
| Helping People in Everyday Life | Full view; whole Reading Aloud, Flood Warnings and Targeted Spraying cards, then banner. Preserve onsets and camera path; fixed 4px outlines. | Phone reading a menu at 2:51–2:57; camera-guided weed spraying at 3:17–3:22. Hold final takeaway state over the unfinished milestones insert, 3:29.93–3:31.63. |

All other pictures, including effective Notebook sequences and the standard close, retain their source timeline. Cutaways use purpose-generated photographic-looking assets, with a restrained 2.5% push across each insert. The scan represents a possible finding for a doctor's review. The research scene represents laboratory testing, not a proven treatment. The menu scene shows the phone camera aimed at the menu. The spraying scene shows one active nozzle over a weed and inactive neighbors over crops. Keep generated assets and exact prompts in `scripts/video/assets/big-upside-cutaways-2026-09-30/`.

No narration cuts, grafts, pauses, gain changes or new audio joins. Existing listening flags carry forward: Hassabis pronunciation, abaucin pronunciation, and the 3:31.63–3:38.43 donor line.

Checks: inspect source images and pre-render framing; decode exact output frame count; compare encoded previews against intended frames; compare preserved pictures outside the edit; hash compressed and decoded audio; run transition guard on all old and new boundaries and inspect the affected strips; confirm protected assets remain unchanged.
