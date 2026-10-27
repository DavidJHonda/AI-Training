# Engagement Trap v15 — October 27 lesson update

Built after David approved the measured plan: “Approved. Build the updated video.”
This is a narrow repair matching the lesson deletions, ready for owner review.

Candidate: `Prompts/engagement-trap-v15.mp4` — **3:58.27**, 1280×720, 30 fps,
7,148 frames. It is **22.8 seconds shorter** than installed v14. The installed
video and website reference have not been changed; no commit or deployment was made.

## Changes

| Installed v14 span | Change | v15 result |
|---|---|---|
| 0:04.667–0:20.167 | Remove the quick-question opening example, from “You ask an AI a quick question…” through “…the reply invites you to stay.” | Opening joins directly to “This extra help may be useful…” at 0:04.667 |
| 2:31.200–2:38.500 | Remove “Successfully using AI requires the active skill of recognizing the exact moment you have obtained the information you originally came for.” | “The system instantly generates a follow-up task” joins to “Engagement is an engineered outcome” at 2:15.700 |
| 2:21.033–2:31.200 | Preserve the missing-page-break narration; replace its pictures with the existing opening chat/follow-up animation | Animation runs at 2:05.533–2:15.700 |

The deleted **AI Won’t Quit for You** illustration and its takeaway ring are absent
from every output frame. The complete donor chat reveal uses source frames 143–510,
retimed from 12.27 to 10.17 seconds. Its reaction shot begins at frame 511 and is
excluded. The original canvas and animated answer/follow-up sequence are retained;
there are no new course-board highlights or camera treatments.

At the first audio cut, the opening picture holds for seven additional frames until
the source's next visual cut. This prevents a 0.233-second flash of the deleted
reaction scene. It does not change audio timing or add a pause.

All other pictures follow the installed source timeline, including the approved
first-board zoom/pan, timer diagram, pause prompt, remaining boards and standard
close. The previous 19.33-second longest uninterrupted board run remains unchanged;
the changed span is a 10.17-second supporting animation, not a course-board hold.

## Verification

- Fully decoded all **7,148 frames**, with regular 1/30-second timestamps and the
  planned duration. Compared every output frame against its declared source frame
  at thumbnail resolution; maximum mean channel difference was 2.658/255.
- Verified that none of the deleted illustration's source frames enter the output.
  The literal final frame maps to the installed video's final closing frame.
- Transition guard passed **4/4** declared boundaries. Inspected all four
  every-frame strips, both animation progression sheets and four overview sheets.
  No residual reaction flash, stale illustration or unexpected visual was found.
- Encoded audio matches the planned edited PCM with correlation **0.999978**.
  Both cuts land within measured quiet intervals. Five-millisecond room-tone blends
  protect the endpoints; no pause or duration was added.
- First join: quiet from **0:04.405 to 0:04.973** (0.569 seconds).
  Second join: quiet from **2:15.539 to 2:15.784** (0.245 seconds).
- Transcribed the actual encoded candidate. Both removed passages are absent;
  the opening continuation, missing-page-break explanation, follow-up-task sentence,
  engagement section, settlement section, stopping-points teaching and closing lines
  remain. Automated transcription supports wording checks, not listening quality.
- Protected source video, current lesson Markdown and all canonical JPG hashes
  remained unchanged.

## Listening review and limits

No perceptual listening or continuous motion playback was performed by the agent.
Review the joins at **0:04.667** and **2:15.700**, using the full candidate or the
encoded excerpts `qa/opening-join.mp4` and `qa/retained-ai-bridge-and-join.mp4`.
The source's previously documented limitation remains: the slope definition is
visible but not fully spoken. This work does not claim a fresh whole-file shipping
sign-off or new verification of pre-existing factual claims.

The original raw rolls were absent during the prior production. This build uses
the verified installed v14, with one additional video/audio encode. No synthesized
voice or new image was introduced.

## Provenance and reproduction

- Source: `course-assets/engagement-trap/engagement-trap.mp4`
- Source SHA-256: `88f2f67a4958bd2aa7dc135307f8c4150fc4dd94518fb6cc6c1a50932949e42e`
- Candidate SHA-256: `2dc69c8a233762e5b6272111432f362d05450bec0931a7ee69adcca388b90a15`
- Build: `.video-venv/bin/python scripts/video/build_engagement_trap_v15.py`
- QA: `.video-venv/bin/python scripts/video/qa_engagement_trap_v15.py`
- Plan: `edit-plan.json`; source/output maps and approval: `edit-manifest.json`.
- Actual encoded checks: `qa/summary.json`, `qa/transcript.txt`, `qa/silences.txt`,
  and `qa/transitions/transition-guard.json`.

The builder refuses to overwrite v15. Any rebuild must use the next unused version.
Installation and local shipping remain pending owner review and authorization.

## Local shipping — October 27, 2026

David accepted v15 with “Looks good. Ship it.” Installed the exact approved bytes
at `course-assets/engagement-trap/engagement-trap.mp4`, updated the cache key to
`20261027ship15`, retained the four-minute display, and refreshed the manifest hash,
size and candidate version. The installed file fully decoded and its SHA-256 matches
both v15 and the committed MP4. The prior listening/playback limitations remain
documented; no new agent listening claim is made.

Local commit: `8ebf603c80b32e93adb1a23b8edb7ce3008afd73`. Only the canonical video, its manifest entry,
and its single `LESSON_VIDEOS` line were committed. Other working edits, including
the lesson text edits, remain in the working tree.

The repository-wide reference check reported existing retired filenames in
`course-assets/in-your-hands/` (`in-or-out`, `three-choices`, and `close`).
Targeted Engagement Trap installation and reference checks passed.

**Shipped locally; queued for batch deployment.** No push or deployment was run.

After the commit, scoped scratch cleanup removed only the regenerable `edited.wav`
(22.9 MB). Candidates, owner-review clips, prior v14 and audit evidence were retained.
