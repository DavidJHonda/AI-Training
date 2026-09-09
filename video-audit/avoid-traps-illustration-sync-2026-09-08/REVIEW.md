# Avoid Traps illustration updates — shipping status

Opener, Hallucination, Training Bias, Document Trap, Mind Trap, Engagement Trap, and Fake Trap are now approved and shipped. Support Trap was already shipped. Flattery Trap revision v3 is now approved and shipped, completing all nine Avoid Traps illustration updates. It keeps the full board visible during the scenario highlight. No index.html or lesson writes. Shipped originals and review copies are recoverable in the audit folders; each has a shipping-receipt.json.

Start with the short reels. Each includes two seconds before and after the updated segment. Mind Trap and Fake Trap reels contain two separate segments; exact reel-to-full-video mappings are in each manifest.

| Video | Review reel | Full candidate | Changed times in full video |
| --- | --- | --- | --- |
| Opener | [10 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch/opener-avoid/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/opener-avoid.mp4) | 1:48–1:54 |
| Hallucination | [12 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch/hallucination/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/hallucination.mp4) | 2:04–2:12 |
| Training Bias | [17 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch/training-bias/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/training-bias.mp4) | 0:15–0:28 |
| Document Trap | [12 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch/document-trap/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/document-trap.mp4) | 0:58–1:06 |
| Mind Trap | [47 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch/mind-trap/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/mind-trap.mp4) | 0:25–0:36; 0:41–1:09 |
| Flattery Trap | [51 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch-v3/flattery-trap/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/flattery-trap.mp4) | 0:29–1:16 |
| Engagement Trap | [27 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch/engagement-trap/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/engagement-trap.mp4) | 3:32–3:55 |
| Fake Trap | [59 sec](/Users/davidobrien/Developer/AI-Training/video-audit/avoid-traps-illustration-sync-2026-09-08/batch-v2/fake-trap/approved-review-reel.mp4) | [Full video](/Users/davidobrien/Developer/AI-Training/videos/fake-trap.mp4) | 0:13–0:43; 1:59–2:20 |

## Verification

- Approved live audio packet payload is byte-identical in all eight full candidates. Reels are preview extracts and re-encode their excerpt audio.
- Exact decoded frame counts and 30 fps preserved: Opener 5070; Hallucination 7018; Training Bias 7488; Document Trap 6734; Mind Trap 5820; Flattery Trap 10999; Engagement Trap 7265; Fake Trap 6601.
- Native macOS playback and first-frame decoding passed for all eight full candidates and all eight reels.
- Inspected all 37 entry, state-change, and exit boundary strips, including every frame within twelve frames on each side. No stale-illustration flashes found. Automatic guard passed 32 boundaries; its five flags were continuous camera moves, manually reviewed: Flattery Trap frames 984, 1275, 1788, 2010; Fake Trap frame 915. Raw flags remain in audit reports.
- Compared 1,949 sampled frames outside replacement intervals, including every nearby outside boundary frame. Maximum mean absolute RGB difference was 1.586/255, consistent with single-pass codec changes, not altered content. Rendered highlight-state frames were compared with the final encoded frames and visually inspected.
- Preserved source gaps, closing shots, pauses, and all narration. Nate appears in both Mind Trap comparison panels. Fake Trap retains its gentle 3.5% illustration push while keeping the replacement title and banner visible.
- No index.html or lesson writes. All eight original live hashes and replacement-asset hashes rechecked; the shipped Support Trap pilot remains unchanged.
- Four superseded Flattery/Fake internal previews were moved out of Prompts to recoverable `batch/<slug>/superseded-*.mp4` audit files. Only final deliverables remain in Prompts.

## Build records

Final manifests and fidelity results are in `batch/<slug>/` for the first six applicable builds and `batch-v2/flattery-trap/`, `batch-v2/fake-trap/` for the refined pair. Those final manifests include approved-baseline and output hashes, frame spans, measured box bounds, inherited highlight colors, audio payload hashes, and reel timestamp mappings.

Builder: `scripts/video/build_avoid_illustration_sync.py`. It uses the visual-only retrofit procedure: one concat encode from each frozen approved live baseline plus lossless replacement legs; approved audio is stream-copied, and candidates are never used as new baselines. The first six were built with base revision; the refined pair uses `--revision v2 --slugs flattery-trap fake-trap`. Existing outputs are deliberately protected from overwrites.

## Flattery Trap v3 follow-up

Removed scenario camera zoom and masking at full-video 0:32.800 (review reel 0:06.300). The full board remains visible with a full-width scenario highlight. Later card highlights and approved audio are preserved. Frame count 10,999, audio packet payload identical. Native playback passes for the full video and reel. Compared 344 outside-span frames; maximum mean RGB difference 1.002/255. Manually inspected all nine every-frame boundary strips: no stale-graphic flashes. Two automated flags at frames 1788 and 2010 are continuous approved camera moves. The scenario and following transition both pass automatically. Flattery Trap v3 is approved and shipped. The previous live video and approved review copies are preserved in batch-v3/flattery-trap; shipping-receipt.json records the verified live hash. Superseded v2 review files are recoverable in batch-v2/flattery-trap.
