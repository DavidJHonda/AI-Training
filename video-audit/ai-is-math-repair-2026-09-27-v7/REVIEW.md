# AI Is Math v7 — repaired review candidate

Built from the actual published file on 2026-09-27. **Review candidate; not published.** The owner accepted leaving the illustrative/47% explanation on screen and authorized removal of the 2:29–2:32 overstatement plus the visual repair. This replaces the earlier REROLL recommendation.

Candidate: `Prompts/ai-is-math-v7.mp4` — 3:26.13, 6,184 frames, 1280×720, 30fps. Source: `course-assets/ai-is-math/ai-is-math.mp4`, SHA-256 `de2305a0df2bd399e3316a554ad0b79c2bb11248521d6ad8912f2be36869ae0d`. Raw generations and the historical v6 candidate are absent; this repair necessarily re-encodes the surviving published video. Build uses a protected snapshot, with one final video encode.

## Narration

The only deletion is “This is exactly how large language models function.” The source-frame cut is [4452,4578), 2:28.40–2:32.60 including surrounding silence. The output join is **2:28.40**. Five-millisecond ramps sit in measured silence at the join. No new narration, graft, generated voice, extra pause, or speech gain change. PCM outside those ramps matches the kept source samples exactly before AAC encoding.

The next sentence remains “They use the sequence of a conversation to constantly update the probability of what comes next.” Review the transition at 2:28.40 for spoken flow: after deleting the preceding sentence, “They” relies on the lesson's AI context instead of an immediately preceding “large language models.” The context/prediction drawing supports the transition. No claim is made that this join has been listened to.

The dog probabilities and full repeat explanation remain. “Illustrative probabilities” and the remaining 47% are legible on the exact canonical board; omission from speech is the owner's accepted exception. Current prompt verbatim requirements remain broader than this existing narration; this repair does not claim compliance with all new-roll requirements.

## Visual changes and continuous exposure

All four teaching boards use exact current JPGs, full unmarked openings, fixed framing, and 4px post-transform highlights. Board files and lesson text are unchanged. Rings follow the formula, scenario, outcome groups, selected heads/heads result, calculations, question, reply and candidate group. The complete dog-board footnote remains visible throughout. The published eight-second standard close is retained.

| Output interval | Visual | Continuous duration |
|---|---|---:|
| 0:00–0:15.43 | Existing drawn chip/network, cropped to remove the unrelated formula | 15.43s |
| 0:15.43–0:22.37 | Existing context-to-next-word drawing, before numerical percentages appear | 6.93s |
| 0:22.37–0:44.20 | Existing drawn Pascal/Fermat scene | 21.83s |
| 0:44.20–1:01.13 | Standard Probability | 16.93s |
| 1:01.13–1:25.90 | Counting the Possibilities | 24.77s |
| 1:25.90–1:54.00 | Existing hands/coins drawing for recap and peek | 28.10s |
| 1:54.00–2:18.40 | A Clue Changes the Odds | 24.40s |
| 2:18.40–2:23.00 | Hands/coins under changed-knowledge explanation | 4.60s |
| 2:23.00–2:28.40 | A Clue Changes the Odds recap | 5.40s |
| 2:28.40–2:42.30 | Context-to-next-word drawing | 13.90s |
| 2:42.30–3:07.20 | What Comes Next? | 24.90s |
| 3:07.20–3:18.13 | Chosen word included in context and fed back to the engine | 10.93s |
| 3:18.13–3:26.13 | Original standard close | 8.00s |

Longest individual teaching-board run: **24.90s**. Longest adjacent-board chain: **41.70s**, formula into coins. Counts include all camera movement and holds; changing highlights never resets them. The ~25s numerical explanations are deliberate exceptions to the roughly 20s preference: keeping all outcomes and numbers visible is more useful than cutting away during calculation. The long original generated-board recreations are removed. The coin drawing itself has a 28.10s hold; this is disclosed, not counted as multiple breaks because of its gentle push.

The repair uses held, clean source drawings with a 2.5% push; it does not create new illustration animations. Donor source frames: chip 750 (crop x240,y110,w800,h450), context 540, history 900, hands/coins 3230, repeat 5880. These were decoded sequentially and visually inspected. The chosen context/repeat frames contain no invented numeric candidate probabilities. New footage replaces the opening phone photographs, the generated duplicate boards, the extra numerical diagrams, and the miscellaneous paper/formula shot. Full donor geometry and timing are in `edit-manifest.json`.

## Verification and limits

Verification artifacts: `verification.json`, `guard/`, `rings/`, `boards/`, `transcripts/`, `encoded/`. These cover actual-file decode/count, sampled reference comparisons, every retained close frame, protected-file identity, PCM continuity outside the approved edit, fixed-width ring sampling, feature-based board matching, the candidate transcript, and every declared visual boundary.

Not performed: real-time end-to-end watching/listening; audible seam, warmth, pronunciation or closing cadence assessment; phone/player playback testing; tracker access; new network download of the published file. No exhaustive semantic audit of every historical generated graphic is claimed. Use the candidate for review, especially the 2:28.40 join; publication requires the remaining listening review and owner approval.

Final results: all 6,184 frames decode; 279 reference comparisons (including all 240 close frames) have mean absolute pixel error below 2.85/255. All twelve transition-guard boundaries pass and all three strip sheets were visually inspected. Encoded board-state sheets and selected full-resolution frames were inspected. The candidate transcript confirms the overstatement is absent and the dog/repeat explanation and both closing lines remain.

Ring measurement caveat: the strict solid-color detector reports 2–4px cores after YUV420 video encoding, because chroma subsampling softens some edge colors. The actual renderer uses an exact 4px mask after scaling; a separate integrated-color-coverage check across 18 encoded straight-edge samples measures 4.01–4.45px including compression fringes (`rings/integrated-width.json`). This is not a claim that every encoded ring has four fully saturated pixels.

The automatic board matcher has a low-confidence false positive at 1:36–1:37.50 (37 inliers) in the hands/coins illustration. The actual frame was sequentially decoded and compared with the declared drawing; it is not a second coin-board appearance. Exact continuous durations in the table use verified edit boundaries, not rounded detector totals.
