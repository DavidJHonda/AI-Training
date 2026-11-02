# Does School Matter? — Skills update v13

Shipped locally November 2, 2026 following “ship it.” Local commit `cfd1784781b5c032a74e0573e0312c3cd753adf4`. Queued for batch deployment; not pushed or published.

## Result

Installed `Prompts/does-school-matter-v13.mp4` at `course-assets/does-school-matter/does-school-matter.mp4`. Runtime 148.6 seconds, 4458 frames at 30fps, 1280×720. The previous 141.7-second video is preserved as `Prompts/does-school-matter-v12.mp4`. The full revised lesson is 6.9 seconds longer than v12 because the Skills explanation now includes critical thinking.

Keep the original “Second, develop strong skills,” then use 22.3 seconds of roll 4. Remove roll 4's board-reference introduction, both abstract explanatory passages, “Once those basics are in place,” and “The first mechanical step of that process is to.” Return to the original school takeaway and complete closing. No added pauses. The encoded transcript confirms questioning claims, weighing evidence and making informed decisions, with none of the removed wording and only one school takeaway.

## Visual treatment

| Board | Highlight sequence | Camera | Supporting scenes |
|---|---|---|---|
| What School Helps You Build | Full board, Knowledge card, Skills card, full takeaway banner | Complete current 1600×917 asset fitted to 1280×720 with white side bars; 4px outlines | Existing microscope at 105.27–109.37; model-building at 114.20–116.87; teamwork at 119.00–123.30 |

Longest continuous run of this board is 15.4 seconds, from 123.30 to the existing close at 138.70. Updated complete-card bounds are measured from the current asset. The original opening, earlier lesson visuals, Knowledge audio and closing are retained. The drawing clips retain their motion and are retimed to the relevant Skills sentences.

## Validation

- All 4458 encoded frames decoded, with continuous timestamps and expected source/board correspondence; maximum mean absolute frame error 3.13 from normal compression.
- Existing body and closing PCM preserved except 5ms seam ramps. Encoded audio correlation with the assembly: 0.999992.
- Roll 4 loudness matched by +4.8 dB with a latency-compensated peak limiter. The existing source has seven tiny AAC decoded overshoots; float PCM avoids adding integer clipping during assembly.
- All four audio joins fall inside measured quiet gaps, lasting 0.347, 0.461, 0.369 and 0.376 seconds.
- Encoded replacement transcription confirms the full critical-thinking sequence and removal of the unwanted wording.
- Transition guard passed all 15 unique boundaries. Encoded contact sheet and the question-join frame strip visually inspected. Full-frame comparisons cover every frame; not all transition strips were manually viewed.
- Asset verifier passed: 244 retained assets, 515 original path mappings, 263 current references and 54 finished videos.
- In-app browser loaded the installed MP4 at the new cache URL: 148.6 seconds, 1280×720, readyState 4, no playback error. The course entry form was not submitted.
- `index.html` cache key updated to `20261102v13`; video manifest SHA-256, size and version updated. Other working changes left intact.

## Limitations

Direct listening was unavailable. Wording, silence boundaries, gain, frame continuity and browser media loading were checked; pronunciation, perceived voice continuity and listening comfort remain unverified. This is a local requested update, not a claim of completing the full listening-based shipping checklist. The user subsequently authorized local shipping after this limitation was disclosed. The six-file release is committed locally; no GitHub push, Vercel deployment or tracker update was performed.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_does_school_matter_v13.py`

QA: `.video-venv/bin/python scripts/video/qa_does_school_matter_v13.py`

The build protects existing candidates and refuses to overwrite v13. Use a new candidate version for any further edit. The QA source-protection check captures the pre-install state; the installed file and index intentionally differ after local installation.
