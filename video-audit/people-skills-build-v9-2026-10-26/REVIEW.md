# People Skills v9 — review candidate

Built 2026-10-26 from the approved plan. Output: `Prompts/people-skills-v9.mp4`, 2:22.833, 1280×720, 30 fps, 4,285 frames. Candidate SHA-256: `2f19e6f8c345646eba11fb058f228790fbffdf655b6c9df5bc35890f1b969d1a`.

Roll 5 supplies the narration. Roll 7 supplies the invitation and acknowledgment at output 0:23.967–0:32.500 (source 0:36.900–0:45.433), lowered 0.75 dB to match the measured base loudness. The approved redundant summaries were removed. The Maya credit question has approximately 3.12 seconds of quiet before the close, including 65 added frames of room tone.

All picture material comes from the installed video's existing artwork/footage, current canonical lesson boards, and the standard closing board. The original opening photos were retimed to the new narration. Retained live scenes include Maya discussing the project, the team in the hallway, the nonverbal-cues diagram, and the challenge-the-idea diagram. Updated practice cards keep their complete artwork and text in frame, including the new concern-and-solution example. The raw rerolls' comic-style opening footage is not used.

## Verification

- Decoded all 4,285 frames; cadence is consistently 30 fps.
- Compared encoded frames with the planned source picture at edit boundaries, highlight onsets, and periodic samples: minimum PSNR 35.02 dB.
- Compared decoded audio with the assembled master: 46.01 dB SNR; peak −1.98 dBFS; no clipping.
- Read the complete fresh encoded-file transcript against the live lesson in `index.html` and its Markdown source. All essential teaching points remain, as detailed below.
- Inspected all three full-video contact sheets and all 30 every-frame transition strips. The guard flagged three camera moves at frames 2530, 2811, and 3378; strip review shows continuous planned movement across the same practice board, without stale-image flashes. Raw results and the hash-matched review are retained separately.
- Inspected the full-size worked-example frame and final frame for framing and readability.
- Protected source media, installed video, boards, photos, and lesson Markdown match their prebuild hashes.

## Narration coverage

These are transcript-based findings, not a claim of direct listening or full playback. The career lab remains a separate post-overview activity, consistent with the approved prep.

| Teaching point | Encoded time | Coverage |
| --- | --- | --- |
| Finished project; Maya proposes a change and is interrupted | 0:00–0:17 | RICH — scenario and both interruption lines retained |
| Notice expression/body language; she seems hurt; choose a response | 0:17–0:24 | RICH |
| Invite her to finish and show her input matters | 0:24–0:32 | RICH — roll 7's complete invitation and acknowledgment |
| Third example violates instructions; group can improve | 0:32–0:44 | RICH |
| Her idea deserves hearing even if unused | 0:44–0:48 | TAUGHT |
| Bridge beyond the project | 0:48–0:55 | TAUGHT |
| Stand out as polished AI work becomes expected | 0:55–1:04 | RICH |
| Trust: listen, keep promises, treat others well | 1:04–1:12 | RICH |
| Connection: people need to feel heard, understood, valued | 1:12–1:19 | RICH |
| Start today; listen before planning replies; ask a follow-up | 1:19–1:33 | RICH |
| Notice tone, hesitation, enthusiasm, behavior; ask when unsure | 1:33–1:44 | RICH |
| Remember, appreciate specifically, give credit | 1:44–1:52 | RICH |
| Challenge ideas calmly, explain concern, suggest a way forward | 1:52–2:00 | RICH |
| “This example doesn’t match the instructions. Could we try another?” | 2:00–2:03 | RICH — complete worked example |
| Group fixes problem; ask learner how to give Maya credit | 2:03–2:08 | RICH, followed by thinking time |
| Both required closing lines | 2:10–2:18 | MET, followed by settled hold |

The base recognizer wrote “hurt” in the conditional sentence and omitted the article in “suggest a way forward.” A fresh medium.en check of the encoded audio transcribes “heard” and the complete phrase correctly; see `encoded-word-checks-medium.json`. The source roll had the same base-model ambiguity and was also checked with medium.en before assembly.

## Review status

The requested candidate is built and ready for playback review. Direct listening and continuous end-to-end playback have **not** been performed; subjective voice continuity at the graft remains to be auditioned. Therefore this is not a final shipping KEEP verdict. The installed course video has not been replaced.

Build script: `scripts/video/build_people_skills_v9.py`. Reproducible technical checks: `scripts/video/qa_people_skills_v9.py`. Detailed timing, cuts, source hashes, and board states: `edit-manifest.json`. Raw transition-gate output: `transitions/transition-guard.json`. Resolved visual findings: `manual-visual-review.json`.
