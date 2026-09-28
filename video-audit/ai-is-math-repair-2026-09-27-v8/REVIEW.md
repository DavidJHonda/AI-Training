# AI Is Math v8 — original graphics restored

Approved and installed for shipping: `Prompts/ai-is-math-v8.mp4`, 3:26.13, 1280×720, 30fps, 6,184 frames.

Owner direction supersedes the earlier visual-removal decisions: the live video's AI-company photographs and illustrative demonstrations are acceptable. Restore all of its graphics and animations. No blanket policy change for unrelated videos is inferred.

## Changes from v7

- Restored the full ChatGPT/Claude opening through its original scene boundary at 0:15.43, including the requested 0:00–0:13 portion.
- Restored the animated prediction/chip sequence, history transitions, letters, coin and puppy demonstrations, paper/math imagery, original hands/coins movement, generated coin diagrams, and the animated word/context/repeat sequence.
- Restored the live demonstration sequence under the repaired narration at output 2:28.40–2:43.30 (source 2:32.60–2:47.50). This includes the requested region around 2:29–2:41. Its illustration-only figures remain as authorized.
- All original graphics are used at their native frame positions after accounting for the existing narration deletion. No held replacement illustrations or new push animations from v7 remain.
- Canonical teaching boards retain the rebuilt 4px highlights and full framing, at their original published boundaries. The clue board opens unmarked for two seconds before its first outline. Its v7 drawing break is removed to restore the live sequence.
- The audio stream is copied directly from v7. The already-approved deletion of “This is exactly how large language models function” remains; no further narration edits. Source frames 4452–4577 are omitted from both picture and audio. The live file, prior candidate, canonical boards, and lesson remain unchanged.

## Continuous board durations

These counts include all zooms, pans, and holds; a highlight change does not reset them.

| Board | Output interval | Duration |
|---|---|---:|
| Standard Probability | 0:44.53–1:01.13 | 16.60s |
| Counting the Possibilities | 1:01.13–1:26.57 | 25.43s |
| A Clue Changes the Odds | 1:58.30–2:28.40 | 30.10s |
| What Comes Next? | 2:43.30–3:07.80 | 24.50s |
| Original close | 3:18.13–3:26.13 | 8.00s |

Longest canonical-board run: 30.10s. Adjacent formula/coin canonical boards: 42.03s. Including the restored coin demonstration immediately afterward, continuous formula/coin diagram exposure is 50.37s. The generated clue demonstration and canonical clue board together occupy 38.53s. These longer exposures are retained under the owner's direction to restore the live graphics; they are not falsely counted as fresh breaks merely because the renderer or camera changes.

## Verification scope

Build from the protected published-video snapshot plus canonical JPGs, with one final video encode. Exact provenance and boundaries are in `edit-manifest.json`; reproducible whole-file verification is `verify_candidate.py`. The original raw generations remain unavailable. This is a narrow restoration, not a new narration or teaching review.

Prior v7 limits remain: no real-time end-to-end listening, pronunciation/cadence assessment, or audible assessment of the 2:28.40 narration join. It still leads into “They use…” after deleting the preceding sentence. No phone/player testing, tracker access, or new public download performed. The numerical footnote remaining on-screen rather than being spoken is the owner's accepted exception. David explicitly approved publication with “Ship it.”

Verification completed: every one of the 6,184 encoded frames was compared with its expected source or rebuilt canonical-board frame, including all 3,285 retained original-graphics/close frames. Maximum per-frame mean absolute pixel error was 2.845/255. The compressed audio-stream SHA-256 exactly matches v7. Protected files are unchanged. All fifteen declared transition checks pass; all three transition sheets and five encoded sample sheets were visually inspected. The restored paper-only entrances and fades are native to the live video, not leaked old frames. The unchanged 4px rasterizer is covered by the prior integrated-width check; no new exhaustive ring-detector run or listening review is claimed.

## Shipping approval

David approved v8 with “Ship it.” Installed the exact approved bytes at the canonical unsuffixed MP4 path; updated the AI Is Math cache key and manifest hash/size only. Earlier listening limitations remain disclosed rather than represented as newly performed checks. Commit/push result is reported in the task; deployment is not awaited.

Shipping validation: approved candidate/canonical SHA-256, manifest byte count, and staged website cache key agree. `git diff --check` passes. The general asset verifier reports pre-existing In Your Hands retired-file warnings and two Training-prefixed Where’s the Line reference warnings; running the same verifier against HEAD metadata produces identical output. These are unrelated to this shipment and were not changed.
