# When You Need More — shortened v4

2026-10-22. Built on the owner's approval of the three-cut plan and burger-flash repair. Shipped locally after owner approval; queued for batch deployment. See SHIP.md. No push or public deployment.

Candidate: `Prompts/when-you-need-more-v4.mp4`, 3:48.000, 6,840 frames at 30 fps, 1280 × 720. Removes 35.633 seconds from the installed 4:23.633 version.

## Source and scope

Stable source: `Prompts/when-you-need-more-v3.mp4`, identical to the installed video at review time. SHA-256: `42612126a609f966c3581726c76d65b615f93e135beee722183a57e487ec7f5b`. One additional encode from the finished v3 preserves its approved visual production. Candidate and protected-file hashes are in edit-manifest.json.

All three boards, their illustrations, examples, card and banner highlights, supporting cutaways, and the complete canonical closing retain their original internal timing and pictures. Existing explanatory additions outside the three approved cuts remain. The lesson, TRY IT, installed video and canonical JPGs are unchanged by this build.

## Edit map

Half-open frames at 30 fps:

| Source kept | Output frames |
| --- | --- |
| 0–1574 | 0–1574 |
| 1666–2999 | 1574–2907 |
| 3438–5285 | 2907–4754 |
| 5823–7909 | 4754–6840 |

Three narration joins:

- **0:52.467:** “Different models have different capabilities.” → “This board lays out the first choice.” Removes the repeated model-benefit sentence.
- **1:36.900:** “Thinking changes how much time AI spends working through your task.” → “AI isn't thinking the way you do…” Removes the English-exam analogy and its dependent transition.
- **2:38.467:** “There's one more option to consider, research.” → “It gathers information from different websites…” Removes the cheeseburger/first-house comparison and “AI's research mode helps with that kind of work.”

Cuts are in measured silence. Five-millisecond ramps are confined to the cut edges; no gain change or new pause. The mono source was decoded to 48 kHz for exact 1,600-sample-per-frame cuts and encoded to AAC at 192 kbps.

## Burger-flash repair

The deleted topic appears visually before its narration: the little burger/comparison panel reveals before the full burger-and-house cutaway. Source frames 5260–5285 (2:55.333–2:56.167) are replaced with source frame 5823, the retained clean research-mode graphic. On the output timeline this is frames 4729–4754, or **2:37.633–2:38.467**. The original animation resumes at the same donor frame at the audio join, so there is no jump back to the deleted topic.

This 25-frame hold is entirely inside the approved repair area and does not lengthen the video. The source graphic that follows develops into the existing website/source-comparison animation.

## Verification and limits

- Four declared audio/visual boundaries passed transition_guard.py. Inspected all four encoded boundary strips; no stale burger or house frame appears at the repaired transitions.
- Decoded all 6,840 frames with continuous 30 fps presentation timestamps. Every frame matches its planned retained source or donor frame within encoding error (maximum frame mean absolute error 3.049/255). Encoded audio correlation against the edited PCM is 0.999985. All protected hashes remain unchanged; results are in qa.json.
- Encoded speech gaps at the three joins measure 0.434, 0.518, and 0.595 seconds. No new pause was added.
- Inspected the repaired research sequence and the full-resolution final frame. The complete canonical close remains the literal final frame.
- Encoded preview frames and the repaired research sequence are saved in preview/. The review page includes jump buttons just before all three joins.
- Read the complete fresh exact-candidate transcript (632 words), saved in transcripts/when-you-need-more-v4.txt and .json. All three planned joins retain complete wording, the removed analogies and repeated sentence are absent, all six board examples and three takeaways remain, and both exact closing lines are retained. Transcript-based coverage passes the current lesson; listening remains unverified as stated below.

No independent direct listening audition or continuous audiovisual playback has been performed. The three joins at **0:52, 1:37, and 2:38** need owner listening review. Technical and ASR checks do not certify audible cadence. This is a review candidate, not a shipping pass.

## Reproduction

Build: `.video-venv/bin/python scripts/video/cut_when_you_need_more_v4.py` (refuses to overwrite an existing candidate).

Verify: `.video-venv/bin/python scripts/video/qa_when_you_need_more_v4.py`.

Transcribe: `.video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/when-you-need-more-v4.mp4 --output-dir video-audit/when-you-need-more-build-v4-2026-10-22/transcripts --model small.en`.
