# Support Trap narrow narration repair

## Status

- Candidate: `Prompts/support-trap-v1.mp4`
- Candidate SHA-256: `0b47758cda842340feaeb77ceb4d45575ee1e32bac6812467a0cea936c0eca38`
- Runtime: 219.467 seconds (6,584 decoded frames at 30 fps)
- Scope: approved narrow A/V graft only; live file, lesson, boards, and tracker unchanged
- Narration content verdict on the finished transcript: KEEP
- Shipping status: review candidate only; not published

## Protected sources

- Base/live: `course-assets/support-trap/support-trap.mp4`
  - SHA-256: `48ad17d38fbeee9e0eb9cf521c86922d85d67c234ce61d5385885afc322289ec`
- Donor: `Prompts/support-trap-1.mp4`
  - SHA-256: `e37c32e3acc1eaffb5ebdfa2a001e2f3ce0b26fdc06b12f97a88f8358fceec40`

Both hashes were checked before and after the build.

## Approved change

The live file's frames 4505–4725 (2:30.167–2:37.500) were replaced by roll 1
frames 5182–5674 (2:52.733–3:09.133). The donor is a complete scene-cut-to-scene-cut
beat, and both cuts sit inside narration silence.

Donor passage:

> After Sophie passed away, her mother described those chat logs as a black box.
> The AI offered empathetic words. But because those chats held crucial hidden
> details, they masked the severity of her distress from the physical people
> around her who could have intervened.

Output graft span: frames 4505–4997 (2:30.167–2:46.567). The unchanged live video
resumes at output frame 4997, so everything after the repair moves 272 frames
(9.067 seconds) later.

The donor's own Notebook drawings travel with its narration so the longer beat has
no orphan visual. All 492 donor frames had the engine corner mark removed with the
same-frame paper-clone method; none were declined. No photographs were introduced.

No pause was added. Donor gain is 0.0 dB: the measured donor passage is -17.4 LUFS,
between the adjacent live speech at -18.8 and -16.7 LUFS.

## Board and camera treatment

The existing finished live treatment is unchanged:

| Board | Highlight/camera treatment |
|---|---|
| Supportive Words versus Support | Full board, sister card, chatbot card, takeaway; complete-card views preserved |
| Use AI to Get Ready for People | Full board, What Can Be Real, Notebook examples, What Is Missing, takeaway; existing camera preserved |
| If Someone May Be in Immediate Danger | Full board, Leave the Chat, Do It Now, Tell Anyway, takeaway; existing complete-card views preserved |
| Closing Message | Existing standard hold/push/settle; canonical close remains the literal final frame |

## Build and QA

Build command:

```text
.video-venv/bin/python scripts/video/build_support_trap_v1_review.py
```

Completed checks:

- Whole candidate decoded cleanly with both audio and video streams.
- Exact decoded count: 6,584 frames, matching the planned assembly.
- `transition_guard.py` passed both declared boundaries; both every-frame strips
  were inspected and show one clean cut with no intermediate visual island.
- Output seam 1: 2:30.167 inside measured silence 2:29.542–2:30.258.
- Output seam 2: 2:46.567 inside measured silence 2:45.831–2:46.823.
- Five-millisecond waveform review found no click-sized discontinuity. Seam jumps
  were 0.000845 and 0.000035, no larger than local high-percentile sample changes.
- Unchanged audio before and after the graft correlates with the decoded live audio
  at 0.99999483 and 0.99998613 respectively; differences are AAC codec noise.
- Full timestamped output transcript confirms the donor starts with “After Sophie
  passed away…” and ends before the live “This panel outlines…” sentence. No next-
  sentence donor audio leaked into the result. The 988 and 911 instructions remain intact.
- Whole-file contact sheets were inspected. Course boards and the live close remain
  unchanged; the donor visuals contain no visible engine corner mark.
- The last candidate frame matches the live canonical close composition (mean pixel
  difference 2.98 from the expected single re-encode).

QA artifacts:

- `manifest.json`
- `transitions/transition-guard.md` and its two boundary strips
- `qa/contact-sheets/`
- `verification-transcript/support-trap-v1.txt`
- `qa/join-1-live-to-donor.wav`
- `qa/join-2-donor-to-live.wav`

## Listening still required

Direct audio playback was unavailable in the build environment. David must listen
to both contextual join WAVs and the complete candidate before shipping, checking
voice identity, cadence, levels, noise-floor continuity, and the wording/delivery
of “physical people around her.” Automated waveform and transcript checks do not
certify those qualities.

The live video, lesson materials, tracker, and deployed site were not changed.
