# Build Your Skills — Learning Illustration Pass

Scope: three approved visual-only scene replacements. Owner said “ship them” on the refreshed three-proposal review, October 8, 2026. The assistant explained that the new scenes would first be built, verified and locally installed. This authorization covers the concrete proposals, not new narration or other lessons.

## Finished changes

| Lesson | Candidate | Changed frames (half-open, 30 fps) | Treatment |
|---|---|---|---|
| People Skills | `Prompts/people-skills-v7.mp4` | [0,798), 0:00–0:26.60 | Same four students through project completion, Maya contributing, interruption and withdrawal. Quotes appear at frames 387 and 419. Returns to the existing Your Next Move board. |
| Curious and Flexible | `Prompts/curious-and-flexible-v11.mp4` | [0,911), 0:00–0:30.37 | Same players and court; defender closes familiar lane. Open receiver highlights at frame 593; captain changes pass at 719. Curious and Flexible labels appear on matching cues. |
| Make Your Move | `Prompts/make-your-move-v10.mp4` | [8167,8343), 4:32.23–4:38.10 | Student coordinator checks progress while teammates hand off a box of supplies; restrained push toward the result. |

1,885 changed frames, 62.83 seconds total. All other video frames and packets are exact copies. Original AAC packets, timestamps, and decoded PCM are identical. Frame counts and durations remain 3,830 / 127.6667 seconds; 6,376 / 212.5333 seconds; 8,825 / 294.1667 seconds, respectively. Every source is 1280×720 at 30 fps.

## Style and source records

The built-in imagegen tool produced eight photographic assets. Complete prompts, exact generated paths, reference/edit dependencies and workspace hashes are in `assets/prompts.json`; all consumed images are saved in `assets/`. Why Learn AI? supplied the photographic style reference; People Skills’ canonical Your Next Move board supplied Maya and her classmate’s likeness and wardrobe. Related scenes were edited from the same base to preserve continuity. Text and the receiver highlight are rendered separately. No new course boards were created.

The basketball v10 was an internal intermediate without the receiver highlight; v11 is the final candidate. The eight assets are unchanged between those encodes.

The source identities and protected board/lesson hashes are recorded in each `*-manifest.json`. Finished installed sources were used. New visual intervals align exactly to existing keyframes, so only those intervals are encoded; no unaffected board or closing frame underwent another encode. Historical sources remain recoverable from pre-shipping Git HEAD `d243b5efe916c4b61669758b53e275993afc49b1` and matching retained production records. The builder requires the recorded source hash rather than silently accepting a later shipped file.

## Verification and limits

- Full sequential decode and render-state comparison passed for every candidate.
- Every unaffected decoded frame and video packet is identical to its source.
- Every AAC packet (including timestamps) and the complete decoded PCM stream matches its source.
- All 12 declared visual state/entry/exit boundaries pass transition_guard; all 12 boundary strips were visually inspected. No stale frame observed. Text and open-receiver highlight inspected in encoded frames.
- Literal final frames inspected; the existing closes are retained byte-for-byte in the unaffected region.
- Canonical board images and lesson files unchanged.
- This is a narrow illustration pass. It retains the previously approved People Skills omissions and all existing narration. Relevant prior reviews: People Skills current review Sept 30; Curious and Flexible v9; Make Your Move title v9. The opener is outside scope.
- No new end-to-end listening pass is claimed. Audio identity proves preservation, not a new listening certification. Browser playback checks and visual review are recorded separately.
- Video Tracker was not accessed or edited. Local shipping does not publish to Vercel; deployment awaits the separately authorized batch.

Build: `.video-venv/bin/python scripts/video/build_skills_illustrations.py --build <slug>`.
QA: `.video-venv/bin/python scripts/video/qa_skills_illustrations.py <slug>`.
Review page builder: `.video-venv/bin/python video-audit/build-your-skills-illustration-updates-2026-10-08/build_review.py`.

## Release status

Shipped locally in commit `3a361cd03d323f13d0da07087e95ff8cff737573`. Only three canonical MP4s and three registry cache keys were committed. Installed, committed and HTTP-served video hashes match the verified candidates; all local video requests return HTTP 200 and the served lesson references match. Queued for batch deployment; no push performed. See `local-install.json`. Browser playback reached readyState 4 for all three updated excerpts. No direct listening is claimed.
