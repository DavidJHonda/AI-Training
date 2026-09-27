# Critical Thinking v14 — review candidate

Built September 27, 2026. **Shipped to the canonical course file September 27, 2026, with David’s explicit approval.**

Output: `Prompts/critical-thinking-v14.mp4` — 3:06.43, 1280×720, 30 fps.

## Approved edits

- Removed the first 12 seconds of generic setup. Opens with “Look at the left side. Knowledge forms your baseline.”
- Retained the exact owner-approved “explanations” repair from the earlier listening preview. Added 0.6 seconds of picture hold so the complete word fits. No generated narration.
- Added the existing Flawed Design drawing at 2:05.60–2:10.73 during evidence checking.
- Added the existing chocolate newspaper drawing at 2:28.47–2:34.47 during “Why am I convinced?”
- Preserved the chocolate-study story, all five habits, AI discussion, closing lines, and earlier whistle repair.

## Continuous board appearances

Exact frame-map durations; the independent half-second board scan agrees within its sampling resolution.

| Board | Before | After |
|---|---:|---:|
| What You Know. How You Think. | 47.23 s | 35.23 s |
| Same Claim. Different Thinking. | 20.17 s | 20.17 s |
| Five Habits of Critical Thinking | 53.77 s | 10.00 / 17.73 / 15.50 s |
| Closing message | 8.70 s | 8.70 s |

The opening remains longer than the approximately 20-second target; this build implements the approved 12-second trim and preserves the remaining explanation. The reactions board is slightly over 20 seconds. Existing board images, camera treatment, and legacy ring widths are retained; this is not a course-wide visual-spec retrofit.

## Verification

- All 5,593 output frames decoded and matched to the intended source-frame map. Mean thumbnail pixel difference 2.34/255; maximum 2.79/255 after encoding.
- Full FFmpeg decode completed without reported errors.
- The approved word-repair preview is bit-identical in the assembled PCM timeline.
- The prior whistle-repair region is bit-identical before AAC encoding. Output uses 256 kbps AAC with PNS and TNS disabled, matching the previous repair approach.
- Encoded audio correlation to the assembled PCM: 0.999983.
- All 16 boundary strips visually inspected. Automated guard passed 15 and flagged the existing horizontal pan after the word hold. Manual inspection and source-frame mapping confirm continuous source motion, with no intervening shot. The raw warning is retained in `transitions/transition-guard.json`; disposition is in `transitions/manual-review.json`.
- Protected live video, page, and asset hashes remained unchanged.
- Build and verification Python files pass syntax compilation; `git diff --check` passed.
- The completed-video transcript confirms the new opening, the full chocolate-study story, all five habits, and both closing lines. ASR renders the repaired word as singular “explanation”; the audio remains the exact owner-approved preview, so this transcript is a content check rather than a new phonetic judgment.

Full end-to-end listening is not available in this environment. The owner approved the repair preview; the completed encoded video still needs owner playback review. This report does not claim a new auditory approval or publication.

## Evidence

`edit-manifest.json`, `verification.json`, `board-measurement/board-spans.txt`, `keyframes.jpg`, and `transitions/` retain the timing, frame, audio, and boundary checks. `verify.py` reproduces the automated verification; its transition guard intentionally retains the raw warning described above.

## Shipping — September 27, 2026

David authorized “ship the video please.” Installed the exact reviewed bytes as `course-assets/critical-thinking/critical-thinking.mp4`, updated the manifest hash/size and lesson cache key to `20260927critical14`. The duration label remains “3 min.” The previous file is recoverable from Git. Earlier validation limits and retained legacy visual treatment above still apply; no additional listening is claimed. See `shipping-receipt.json`.
