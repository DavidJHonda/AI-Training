# Embrace the Future: illustration video updates

Status: All four illustration updates are approved and shipped, including Big Downside v2 with the stray sound removed. index.html was not modified.

Four live videos use the replaced Nate/Luke artwork. Big Upside was scanned and visually reviewed but uses Notebook protein graphics, not its Nate illustration, so it remains unchanged.

| Video | Full-video range included in clip | Short review | Complete video |
| --- | --- | --- | --- |
| big-downside | 1:37.4–1:57.4 | [Review clip](/Users/davidobrien/Developer/AI-Training/video-audit/embrace-illustration-sync-2026-09-08/build/big-downside/approved-review-reel.mp4) | [Full candidate](/Users/davidobrien/Developer/AI-Training/videos/big-downside.mp4) |
| opener-embrace | 0:50.5–1:17.4 | [Review clip](/Users/davidobrien/Developer/AI-Training/video-audit/embrace-illustration-sync-2026-09-08/build/opener-embrace/approved-review-reel.mp4) | [Full candidate](/Users/davidobrien/Developer/AI-Training/videos/opener-embrace.mp4) |
| rise-of-agents | 0:29.7–0:40.4 | [Review clip](/Users/davidobrien/Developer/AI-Training/video-audit/embrace-illustration-sync-2026-09-08/build/rise-of-agents/approved-review-reel.mp4) | [Full candidate](/Users/davidobrien/Developer/AI-Training/videos/rise-of-agents.mp4) |
| work-changes | 1:37.1–3:05.9 | [Review clip](/Users/davidobrien/Developer/AI-Training/video-audit/embrace-illustration-sync-2026-09-08/build/work-changes/approved-review-reel.mp4) | [Full candidate](/Users/davidobrien/Developer/AI-Training/videos/work-changes.mp4) |

## Scope and checks

- Replacement source: the approved lesson JPEGs installed under existing filenames. Their hashes and original live-video hashes are recorded in replacement-plan.json and each build manifest.
- Narration, original frame counts, and pauses are unchanged. Audio payloads were preserved for the illustration updates; Big Downside v2 additionally removes the approved stray sound described below. All candidates and clips passed native macOS playback and first-frame decoding checks.
- Opener preserves its existing full view, monster zoom, and island pan using measured source-camera tracking.
- Big Downside retains its title and sign highlight sequence with remeasured artwork coordinates.
- Rise of Agents stays full-board. Four inherited blank lavender frames immediately before the old board are now covered by the replacement (frames 950–953); audio and timing did not change.
- Work Changes retains its sequence and pans. Purple left / amber right highlights follow the full card boundaries, with vertical extents measured on the new artwork.
- Reviewed every transition-guard contact strip: 25 consecutive frames centered on each of 24 boundaries. Automatic flags were smooth pans/zooms, not transient old graphics. Settled states were also visually checked.
- Outside replacement spans, sampled candidate-versus-live image differences stayed below 2.0 levels out of 255 (lossy re-encoding). Frame counts matched exactly; audio payloads matched before the subsequently approved Big Downside audio repair.

## Reproducibility

Builder: scripts/video/build_embrace_character_sync.py. It refuses to overwrite existing candidates/audit runs. Start only from the original live baselines recorded in the scan manifests, never from a previously patched candidate.

The review clips contain two seconds of unchanged context before and after each replacement. Their time mapping is also recorded in each manifest's reel_timeline. Approved live videos are in videos. Their previous live files and approved review copies are preserved in their build audit folders, with shipping-receipt.json records. Big Downside v2 is also shipped; its original live video, approved copies, and pre-audio-repair copies are preserved in build/big-downside.

## Big Downside v2 audio repair

Removed an isolated sound in the pause after “system” and before “Our third idea…”, at 99.350–99.800 seconds in the complete video. Used adjacent room tone with 8 ms fades; no ripple edit. Video packets and all 8,560 frames are unchanged. Both complete words are retained. Native playback verified for the full candidate and review clip. See build/big-downside/audio-repair-v2.json. The original visual-only candidate is retained as pre-audio-repair-candidate.mp4 in this audit folder. Big Downside v2 is now approved and shipped; shipping-receipt.json records the verified live hash.
