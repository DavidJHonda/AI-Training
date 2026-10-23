# Loudest Voices v11 — earlier two-expert board

David spotted the independent Notebook graphic that still branched into Optimist, Doubter, and Worrier near 0:22 in v10. That supporting scene was missed in the previous removal pass.

The canonical two-expert board now enters at **0:19.900**, on “Same field, same evidence, very different bets,” before any three-way split. It remains at full, unmarked view until the existing Dario introduction at 0:29.100. This preserves the existing highlight sequence and gives students time to see the two experts together.

Candidate: `Prompts/loudest-voices-v11.mp4` — **4:41.933**, 8,458 frames, 1280×720, 30 fps. Review only; installed course video unchanged. Opener v6 unchanged.

Only frames 597–711 change their visual content. To keep the rest byte-identical, the GOP-aligned span 369–711 was encoded using the earlier v8 source for unchanged frames, then joined to v10's untouched packets. All **8,115 unaffected video packets** and **13,217 audio packets**, including their timestamps, match v10 exactly. Narration, pauses, total runtime, the 1:14 flash repair, and In Your Hands ending are preserved.

Verified every frame of the continuous two-expert board from frame 597 through 872 against its native rendering. Inspected the opening contact sheet across the transition and old split. Transition guard passed at frames 369, 597, 619, 712, and 873, with no transient islands. The candidate retains exactly 8,458 video presentation timestamps. Audio is copied bit-for-bit, so no new audio edit or transcription was needed.

Build: `scripts/video/fix_loudest_opening_v11.py`.
Verification: `scripts/video/qa_loudest_opening_v11.py`; `qa.json`; `transitions/`.

[Open the combined review page](../remove-doubter-2026-10-22/review.html). Use “Earlier board entrance · 0:17” to review the change. The listening review of the earlier v10 narration joins remains outstanding; this visual-only repair does not alter them.
