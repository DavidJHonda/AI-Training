# Training v9: review candidate (2026-09-27)

[Candidate](../../Prompts/training-v9.mp4) · [transcript](transcripts/training-v9.txt) · [edit manifest](edit-manifest.json) · build `scripts/video/build_training_v9.py`

**4:06.07, 7,382 frames, 1280x720 at 30 fps.** Not shipped; the live video is unchanged.

Plan: `../training-reroll-review-2026-09-27/` (REVIEW.md, edit-plan.csv). David's calls on 2026-09-27:
- graft C dropped
- join B approved
- roll 3's "Repeat." is not cut off, so roll 3's own close is kept
- paper-craft drawings and the frustrated-student cutaway: agreed

## Narration (fresh small.en transcript of the candidate)
- Base is roll 3.
- Graft A = roll 1 0:20.00-1:00.90 (output 0:23.30-1:04.20): Before Training Starts word for word with all seven data kinds, plus the three phase names and roles. Gain 0 dB (both rolls measure -19.7 dBFS).
- Cut B = roll 3 2:03.45-2:19.30. The pretraining quote now reads "...in the sport. / In this guide, we will cover..." (output 2:04.9-2:09.7).
- All 9 required lines are present, and all three sample answers are read in full. Closing lines at 3:56-4:01.
- Every row edge sits inside a measured silence (0.52-1.39 s; the 1.39 s at 0:45 is roll 1's own gap after "curriculum.").

## Pictures
Longest single board run: The Training Loop, 23.6 s (0:59.8-1:23.4, one worked example with Guess / Check / Adjust rings). Every other run is 21.7 s or less. The old roll had 128 s of boards straight.

| Output | Picture | Source |
|---|---|---|
| 0:00-0:23.3 | flask/code/essay, player, shot, ball rack | roll 3 own |
| 0:23.3-0:45.0 | Before Training Starts (compact, two card rings) | board |
| 0:45.0-0:48.5 | desk + court split drawing | roll 2 0:05.9 |
| 0:48.5-1:04.2 | Three Phases (question ring, then Phase 1/2/3) | board |
| 1:04.2-1:14.8 | Aim & Force basketball drawing | live 0:10.9 |
| 1:14.8-1:38.4 | The Training Loop | board |
| 1:38.4-1:41.1 | ball rack (second showing) | roll 3 own |
| 1:41.1-1:45.5 | control panel (paper-craft) | roll 3 own |
| 1:45.5-2:00.3 | 1 · Pretraining: full view, dive to What Pretraining Builds | board |
| 2:00.3-2:04.6 | ball off the rim | roll 2 0:09.4 |
| 2:04.6-2:10.3 | 1 · Pretraining: answer section | board |
| 2:10.3-2:15.3 | frustrated student at scrambled screen | roll 1 4:01.3 |
| 2:15.3-2:24.0 | Internal Weights diagram (v8 precedent) | live 0:25 |
| 2:24.0-2:37.8 | 2 · Instruction Tuning: Learn to Follow Instructions | board |
| 2:37.8-2:41.7 | shot into hoop (second showing) | roll 3 own |
| 2:41.7-2:54.1 | 2 · Instruction Tuning: answer, then What Still Needs Work | board |
| 2:54.1-3:01.0 | student thinking at desk | roll 2 0:00 |
| 3:01.0-3:17.0 | 3 · Preference Tuning: Learn from Feedback | board |
| 3:17.0-3:20.3 | smiling student at laptop | roll 1 5:01.5 |
| 3:20.3-3:41.3 | 3 · Preference Tuning: answer, then What Still Needs Work | board |
| 3:41.3-3:55.8 | student at laptop, laptop, hands typing a chat | roll 3 own |
| 3:55.8-4:06.1 | standard close | |

## Verification
- **Transition guard:** 23/23 boundaries pass. I looked at all 23 strips: no stale frames, and board returns land settled (camera_at set to the return frame). The close card is the final frame.
- **Sub-second scenes:** none. The shortest scene is 2.7 s (the ball rack).
- **Corner mark:** 1,869 frames cloned, 865 inpainted, 0 declined. Protected files are unchanged.
- **Ring stroke (`ring-stroke.txt`):** blue and purple read 4-4.5 px; teal and green read 5 px. This is the known house `draw_ring` behavior flagged 2026-09-27 (Where AI Works Best); I have not fixed it.
- **Not done:** listening by ear to the whole file or to the joins (0:23.3, 0:45.0, 0:48.5, 1:04.2, 2:04.6/2:08.2), or checking playback on a phone.
