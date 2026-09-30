# Support Trap v9 — live-ending hybrid

Approved scope: v8 opening and expanded teaching, followed by the live narration from its 2:14 warning through the close, with v8's visual interruptions around the safety board. Review candidate only; not installed or published.

Candidate: `Prompts/support-trap-v9.mp4`, **4:45.50**, 8,565 frames at 30 fps, 1280×720.

## Narration

The first 2:36.03 retains v8's assembled PCM. At 2:36.03 the recording changes to the stable live snapshot, source 2:14.20 through 4:23.67. That complete ending plays in source order and at original speed, with one constant −5.4 dB gain adjustment and a 5 ms matched-room-tone entry ramp. There are no internal word cuts, new pauses, or narrator grafts in the live ending. The live warning's breathing room is preserved.

The adjacent v8 passage measured −22.38 LUFS; the first live passage measured −16.78 LUFS before adjustment (−22.18 after the selected gain). These measurements support the level choice; they do not establish perceptual matching.

The live wording is deliberately retained to preserve the delivery David preferred. It says the chatbot “consistently responded with warmth and encouraged her to seek professional help.” The lesson includes “sometimes” before encouraged. That qualifier has not been inserted with another voice or a word-level graft; it remains a wording difference for review. The careful live death/black-box account and all three safety steps remain intact.

## Pictures and board treatment

V8's early visual work remains: cafeteria action insert, empty-chair contrast, corrected three-jobs diagram, response-text outline at 0:40.33, and the repaired tool-versus-trap transition. The live story pictures run in their original timing from the warning through the black-box account. No earlier live teaching or faulty earlier diagram is imported.

| Output | Picture and purpose |
|---|---|
| 2:36.03–2:43.93 | Live warning and original pause |
| 2:43.93–2:50.67 | Live story attribution and restrained chair illustration |
| 2:50.67–2:59.40 | Live private-chat illustration |
| 2:59.40–3:16.93 | Live family/therapist limits and lack of physical intervention |
| 3:16.93–3:35.43 | Live black-box account |
| 3:35.43–3:59.23 | Current safety board, unmarked introduction followed by Leave the Chat and Do It Now outlines |
| 3:59.23–4:08.73 | V8 urgency drawing under “one more message” and inability to call/protect/take responsibility |
| 4:08.73–4:27.90 | Safety board returns for Tell Anyway and the takeaway banner |
| 4:27.90–4:34.73 | V8 chat-to-person drawing under knowing when to leave |
| 4:34.73–4:45.50 | Canonical closing graphic under live closing narration |

Safety board: exact current `course-assets/support-trap/support-trap-danger.jpg`, compact full view, no camera dive, fixed 4 px outlines. Spoken target onsets in source-live time are 3:23.23 Leave the Chat, 3:36.23 Do It Now, 3:47.97 Tell Anyway, and 4:00.80 takeaway. The first safety run is 23.80 seconds because it includes the complete spoken board introduction and first card; the insert follows the second-card label, then the 19.17-second return covers the third card and conclusion. These runs follow explained board content rather than unrelated narration.

The close holds 48 frames, pushes to 1.2× over 150 frames, then retains the live ending's settled hold through the literal final frame. No closing narration or source tail is shortened.

## Sources and reproduction

The live donor is the stable snapshot `video-audit/support-trap-build-2026-09-30-v5/donor-3bf1658e.mp4`, SHA-256 `3bf1658e980395f5d688b1c58cd39550c92378e2421644740611c7aaec3c23ab`. The September 30 raw rolls and current JPGs are verified before rendering. Original assets are rendered in one assembly; the surviving live video is necessarily the source for its ending. Earlier candidates and installed assets are protected from writes.

Build: `.video-venv/bin/python scripts/video/build_support_trap_v9.py`

QA: `.video-venv/bin/python scripts/video/qa_support_trap_v9.py`

The manifest records exact source/output frame spans, source hashes, board geometry, gain and closing treatment. Full playback and listening are not performed by these tools. David's listening checkpoints are the narration handoff at 2:36.03 and the uninterrupted live ending thereafter. This candidate is not a certified shipping pass.

## Final encoded checks

- All 8,565 frames decode at uniform 30 fps; duration 285.50 seconds.
- At the narration handoff, the measured quiet gap is 0.497 seconds (2:35.712–2:36.209). The preserved warning pause measures 4.005 seconds (2:40.196–2:44.201) at −35 dB. No added pause was applied.
- All 25 declared transition checks pass. Inspected the changed handoff, safety-board/insertion/closing boundaries and encoded ring states. The original live scene sequence remains in source sync.
- The first 2:36.03 has zero sampled pixel difference from v8, and its assembled PCM is bit-identical.
- The complete live ending PCM is identical to the source after the single −5.4 dB gain change, except its initial 5 ms entry ramp. Encoded audio correlation to planned PCM: 0.9999863.
- Delivered loudness: −20.97 LUFS integrated, −1.69 dBTP true peak. The loudness command was a measurement only; no dynamic normalization was applied.
- Encoded ending transcript confirms the complete warning, story, three safety steps, 988 and 911, and both closing lines. No repeated standalone “Leave the chat” from v8's former donor join remains.
- Canonical closing image is the final frame. Settled hold lasts 125 frames after the 48-frame prehold and 150-frame push.

Candidate SHA-256: `1f319094ba354c2048d900c8f3c62068b9f43c39971ee378f879588d9320137b`.

Full listening and continuous audiovisual playback remain pending. Build and technical QA completion do not certify the audible handoff or authorize installation/publication.
