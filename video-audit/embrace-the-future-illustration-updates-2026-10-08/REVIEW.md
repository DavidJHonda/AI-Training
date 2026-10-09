# Embrace the Future — Learning Illustration Pass

2026-10-08. **Approved and shipped locally; queued for batch deployment. Commit d243b5ef.**

The owner approved the three opportunities with “agree.” This is a narrow visual-only update. The original narration, timing, course boards, highlights, camera paths and closes are retained.

## Changes

| Candidate | Replacement interval (exclusive end) | Treatment |
| --- | --- | --- |
| Rise of Agents v8 | 1:52.30–2:01.10; frames [3369,3633) | Photographic student reviewing the basketball reel. Caption emphasis at frame 3487 (1:56.23), matching “reviewing”; revision at frame 3512 (1:57.07), matching “making it better.” “Friday highlights” becomes “30 points on Friday,” using the earlier narrated scenario. The original caption remains crossed out in the magnified excerpt. |
| Data Centers v6 | 1:10.73–1:14.80; frames [2122,2244) | Generic warehouse-scale data center exterior with realistic cooling and electrical service, replacing the power-station-like drawing. Gentle 2.5% push. No named site or extra numerical claim. |
| Work Changes v6 | 5:10.53–5:20.37; frames [9316,9611) | Same student first attempting, then checking and revising algebra. At frame 9416 (5:13.87) the learner checks the distribution step; at 9480 (5:16.00) the corrected working appears. The intentionally incorrect first attempt is crossed out. The corrected solution, x = 3, is checked in the original equation. |

Total changed supporting imagery: **681 frames / 22.70 seconds**. Six other section videos remain unchanged.

P1 preserves the v7 removal of the later universal permission rule and review-button imagery. It illustrates the retained basketball evaluation example only. P2 preserves v5’s calculation captions. P3 preserves v5’s earlier source-checking photograph and augmentation animation.

## Style, assets and reproducibility

The photographic composition follows the approved Why Learn AI? student-revision reference. P1 uses the Work With AI convention of precise screen states; P3 follows Learn With AI’s matched learning states. P2 follows the realistic-setting treatment without inventing a student action for an infrastructure shot.

Five images were made with the **built-in image_gen tool**, including the matched earlier study state edited from the later one. Local originals and complete generation/edit prompts are in `assets/` and `assets/prompts.json`. The basketball footage illustration is illustrative, not a real person’s video. Caption text, highlights, editor screen and notebook working are rendered deterministically by `scripts/video/build_embrace_future_illustrations.py`.

The two study photographs preserve the learner, clothing, setting, work and camera; gaze and left-hand placement change. A magnified excerpt shows the same notebook working that is composited onto the page, making the learning action readable at 720p. These are supporting scenes, not redesigned course boards.

## Assembly and verification

- SHA-locked sources: installed Rise of Agents v7, Data Centers v5, Work Changes v5. Exact source and candidate hashes are in each manifest.
- Sources are finished approved videos; pristine raw rolls were not used. Encode only intersecting GOPs and remux the rest.
- Rise of Agents reencodes frames [3369,3869). The 236 following board frames are preserved in content using native YUV input; minimum YUV PSNR against source is 64.03 dB. All 4,612 frames outside that interval are pixel-identical.
- Data Centers reencodes only [2122,2244); 6,572 untouched frames are pixel-identical.
- Work Changes reencodes only [9316,9611); 9,553 untouched frames are pixel-identical.
- All original AAC packets, timestamps and decoded PCM hashes are identical for all three full candidates. Runtime and frame counts remain 5,112 / 6,694 / 9,848 at 30 fps and 1280×720.
- Every changed frame matches its intended rendered state; full candidate decodes pass.
- **11/11 transition boundaries pass.** All eleven every-frame strips were visually inspected, including scene entry/exit, all state changes, and Rise of Agents’ return to copied source packets. No stale intervening shot was found. Data Centers retains the original pale-paper fade into the chat diagram on exit.
- Encoded final states inspected at 1280×720: screen perspective/text, notebook correction and facility scene are intact. Source videos, lesson Markdown and canonical JPGs retain their original hashes.
- Initial assembly attempts for P1 and P3 stopped on a codec-compatibility assertion before any candidate was written. Matching the original fast encoding preset resolved the mismatch. Final candidates passed the packet/frame checks above.

`qa_embrace_future_illustrations.py`, individual `qa.json` reports, `verification.json` and transition strips retain the evidence. Original audio is copied in full candidates; short browser excerpts use reencoded AAC for convenient review.

## Scope limits and owner review

This is not a new factual or narration audit, nor a whole-file production certification. The current installed revisions and their approved exceptions are preserved. No new outside-scope defect was established by this narrow build. Continuous audible viewing/listening by the agent has not been performed; transcripts and identical audio do not establish that subjective check. Review the supplied excerpts with sound, especially 1:52–2:01 in Rise of Agents, 1:11–1:15 in Data Centers, and 5:11–5:20 in Work Changes.

The Video Tracker was not accessed or edited. At build completion, course video files and site references were unchanged; the approved local installation is recorded below. The review includes before/after excerpts, visible posters, full candidates, scene states, assets and prompts.

## Browser review delivery

All six before/after excerpts decode completely and include audio. All three updated players were exercised in the in-app browser and reached their expected ends with readyState 4 and no media error. Posters and comparison layout inspected. Review links resolve. This verifies player operation, not subjective audio listening.

## Local release — 2026-10-08

- Owner authorization: “They look great. Ship them.”
- Commit: `d243b5efe916c4b61669758b53e275993afc49b1`. Exactly three canonical MP4 files and their three cache-key updates in `index.html`.
- Installed Rise of Agents v8, Data Centers v6 and Work Changes v6; all use cache key `20261008ship1`.
- Installed and committed hashes match the reviewed candidates. Local HTTP 200 responses and the served bytes match those hashes; all three references are present in the local course.
- Audio/frame/transition checks apply to the identical installed bytes. The disclosed lack of continuous editor listening remains recorded; the owner approved shipping after reviewing the candidates.
- Previous source candidates are retained in `Prompts/` as recorded in `local-install.json`.
- Scoped cleanup dry run found zero disposable render-scratch files. Scene assets, prompts, candidates, review excerpts and verification evidence remain available.
- No push or deployment performed. Status: shipped locally; queued for batch deployment.
