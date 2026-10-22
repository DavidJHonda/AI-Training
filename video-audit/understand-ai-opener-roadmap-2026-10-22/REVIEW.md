# Understand AI opener — roadmap consistency check

Date: 2026-10-22. Scope: update the lesson after One More Thing became The Next Token, and check the current video for the removed math-workload promise.

## Lesson update

The fifth roadmap explanation now reads: “How AI builds an answer and why answers vary.” Updated `index.html`, `lessons/Opener-Understand.md`, the canonical roadmap JPG, and its renderer. Bumped only the roadmap image cache key. Synced the Understand AI opener upload bundle; its scoped `--check` passes. Inspected the rendered 1600 × 1091 board; all five rows and the takeaway remain readable.

## Video finding

The course entry `LESSON_VIDEOS.openerfoundations` points to `course-assets/understand-ai-opener/understand-ai-opener.mp4?v=20260929ship1`.

Current MP4 SHA-256: `e914ab971a630018a2c92edb67d19ddfb4a97c38f52cfbee6194ef2975e77f79`. This exactly matches the source recorded in `video-audit/understand-ai-illustration-opportunities-2026-10-08/sources.json`, establishing that the existing full transcript applies to this file.

- 2:13.04–2:16.60: “We look at the final construction process, why the answers vary,”
- 2:16.96–2:18.60: “and just how much math goes into it.”
- 2:19.78: closing narration begins, “The machine won't feel like magic anymore.”
- The decoded frame at 2:16 visibly contains the old fifth-row text. Evidence: `current-video-2m16.jpg`. The roadmap remains outdated wherever that embedded board appears, even before the fifth row is highlighted.

The video needs a narrow repair: replace the embedded roadmap wherever visible, preserving its framing and highlight sequence, and remove the obsolete narration clause. Listed timestamps are word-alignment evidence, not approved edit boundaries. Determine a cut in silence and audition the cadence into the close before finalizing a build.

## Verification limits and status

The initial check used the complete existing transcript, a matching source hash, and a decoded video frame. The user subsequently authorized the repair below. No full KEEP / REPAIR / REROLL verdict is claimed.

## Authorized repair — v14

User authorization: “Fix the video too. Remove that clause and replace the roadmap with the updated version.”

Candidate: `Prompts/understand-ai-opener-v14.mp4`, 2:26.033 (4,381 frames at 30 fps, 1280 × 720). SHA-256: `9a1cff435896a2982502eaf3f4cce6990f151a481a46ec79f3a4746bbcc83f2b`.

Source: `Prompts/understand-ai-opener-v13.mp4`, matching the installed source hash above. The original raw generation is unavailable; this repair uses the finished v13 and re-encodes retained picture and audio once.

| Board | Highlighting | Camera | Output spans | Treatment |
|---|---|---|---|---|
| Understand AI | Preserve all five existing row onsets and fixed 4 px outlines | Existing static full view, compact | 1:20.767–1:47.833 and 1:58.700–2:17.133 | Replace with the exact current canonical JPG; preserve the intervening text/token/number animation |

Longest unbroken map run remains 27.067 seconds, retaining the previously approved pacing exception. The later map run is now 18.433 seconds. The token animation at 1:47.833–1:58.700 and the closing scene retain their source frames and timing relative to their narration.

Removed source frames 4106–4165: 2:16.867–2:18.867, exactly two seconds, bracketing “and just how much math goes into it.” Both cut points fall in quiet audio. A 5 ms blend joins the quiet handles without changing the planned duration. No pause was inserted. The final encoded gap between the speech release after “vary” and the closing sentence measures 1.222 seconds at a −40 dBFS silence threshold (2:16.807–2:18.029). This acoustic measurement differs slightly from the transcript's approximate word boundaries.

### Verification

- Fully decoded and compared every output frame with either its corresponding source frame or intended updated roadmap state. Exactly 4,381 frames; maximum per-frame mean absolute channel difference is 3.246/255 for retained footage and 3.020/255 for updated roadmap frames, consistent with re-encoding. The source is unchanged.
- Fresh transition guard passed all five declared boundaries; visually inspected all five every-frame strips. No stale-frame island found. The audio cut is beneath an unchanged roadmap state.
- Inspected all five settled encoded row highlights at full resolution, plus the unmarked replacement preview. All content and complete row outlines remain visible.
- Fresh local Whisper small.en transcription of the encoded ending reads: “We look at the final construction process, why the answers vary.” It then contains both closing sentences, with no math clause.
- Decoded output audio correlates 0.999995 with the intended source cut. Peak audio within 10 ms of the edit is −53.2 dBFS. These are technical checks, not a listening certification.
- `git diff --check` passes.

Build: `.video-venv/bin/python scripts/video/build_understand_ai_opener_v14.py`. Detailed source identity, timeline, board treatment, and encode command: `edit-manifest.json`. Results: `verification.json`, `ending-transcript.json`, `ending-silence-check.txt`, and `guard/transition-guard.md`. Convenience review clip: `ending-preview.mp4`, starting at full-video 2:09.

### Review status

The requested narrow repair is complete as a review candidate. No real-time listening or full audiovisual review was performed; the spoken cadence through the edit at approximately 2:17 remains for listening review. Prior unrelated narration differences documented in the v13/source reviews were preserved; no whole-video shipping verdict is claimed. The installed course MP4 and its page reference remain unchanged. No local release commit or publication was performed.

## Local release — 2026-10-22

Shipped locally; queued for batch deployment. David reviewed the candidate and authorized shipping: “Looks good. Ship it.” Installed v14 at the canonical course path and verified its SHA-256 exactly matches the approved candidate. Updated its video cache key to `20261022ship1`, the roadmap cache key and wording, lesson Markdown, renderer, and the three affected asset-manifest records. The existing rounded runtime label remains “2 min”; exact duration is 2:26.033.

Local commit: `7f13d1838866e7f8fd50c659be810ea0a6aa662a`. The six-file commit contains only this release. Build and audit records remain local. The global asset verifier reports the same seven pre-existing issues before and after installation, with zero new issues. The scoped upload check and Git whitespace check pass. User review and shipping authorization supersede the prior pending-review status; the agent has not added a full audiovisual listening claim. No push or Vercel deployment was performed.
