# Unexpected Results v4: two-example lesson

**Reroll requested, 2026-10-23:** the owner likes the rat section but finds narration mis-speaks weak. A fresh complete narration is now the production path; updated preparation emphasizes Hanoi as the main unexpected-result story and texting/cane toads as two further examples. v4 is retained for reference and is not approved for shipping.

Status: review candidate; not installed, committed, or published. Owner requested the two-example
update. This is a narrow content edit. No Video Tracker access or change is claimed.

Candidate: [unexpected-results-v4.mp4](../../Prompts/unexpected-results-v4.mp4), **2:48.033**,
1280×720 at 30 fps, 5,041 frames. Removed **1:11.033** from the 3:59.067 source.

## Changes

Keep the rat story and moral, texting, cane toads, and the ending. Remove GPS, highways, the extra
traffic explanation, and both lines that announce or summarize four examples. Replace the old
four-example graphic everywhere it would remain with the current two-example asset. Highlight the
complete active card at full view. Retain the existing texting animation. Longest uninterrupted
changed board run: **14.1 seconds**.

The source SMS narration explains a secondary short-message feature becoming everyday communication.
It does not repeat the newly revised page word for word, and the new youth-adoption detail is not
spoken. That detail is supplementary to the lesson's central point about unexpectedly large effects.
No new speech, voice change, or carrier-to-customer origin claim is introduced.

The existing close and rat-story label repairs are preserved. No new pauses or speed changes.
The former road-to-AI visual overlap is covered through the source's actual next-scene cut, avoiding
stale highway frames at the final audio join.

## Source and method

Stable source: `Prompts/unexpected-results-v3.mp4`, byte-identical to the installed file at build time.
SHA-256: `051361422c95c73c7d7127cc5b9908f8652f9b4b8b1a068bb1300c5a5f5bffdc`.
Original raw rolls are unavailable. The first 2,469 video frames (1:22.300) are copied as original
H.264 packets. The rest is encoded once from that source and the canonical board. Retained audio
is trimmed at measured quiet endpoints and encoded once. Five-millisecond edge tapers only reduce
click risk; no direct listening certification follows from these measurements.

See [edit plan](EDIT-PLAN.md) for exact source spans and retained words, `edit-manifest.json` for
output spans, hashes, board geometry, and visual runs, and `qa.json` for encoded-file checks.

## Narration assessment

The retained source teaches the core arc: confident predictions can miss large effects; rat-tail
payments rewarded keeping rats alive; texting grew beyond its modest role; cane toads backfired;
AI may have important effects nobody anticipates; stay curious and build durable skills.
The rat story is RICH; both retained examples and the closing uncertainty/skills takeaway are TAUGHT.
The new youth-adoption detail is MISSING from speech but appears on the current canonical graphic;
this candidate does not claim a verbatim narration update. The rat-story opening uses the existing
“a true story from 1902 Hanoi” instead of the preparation prompt's exact “a true story about rats.”
That is inherited from the approved source, not newly rewritten audio.

Final KEEP/ship certification is withheld pending direct listening and continuous audiovisual review.
ASR and numerical audio checks cannot verify cadence, pronunciation, or perceptual smoothness.

## Verification

- Full sequential decode: 5,041 frames at 30 fps with uniform timestamps.
- Opening 2,469 frames are packet- and pixel-identical to v3.
- All 1,824 retained, re-encoded native frames were compared to their mapped source frames;
  maximum mean absolute pixel error was 2.787/255.
- All eight cut endpoints measured below -61 dBFS. Encoded audio correlations around the four
  joins exceed 0.99998 against the planned edited PCM.
- Transition guard: nine checked boundaries, zero failures. All nine every-frame strips inspected.
  No stale GPS/highway frames appeared at the edits.
- Full candidate ASR transcript reviewed: texting and cane toads remain; GPS, highways, the road
  explanation, and four-example announcements are absent. ASR writes “warriors” for the existing
  “Worriers” references; this is unverified transcription/pronunciation ambiguity, not a claimed fix.
- Whole-video six-second contact sheet, edited-middle frames, complete-card outline previews,
  and final closing frame inspected. This is sampled visual review, not continuous playback.
- Source v3, installed video, and canonical board hashes are unchanged by the build and QA.

Direct listening and continuous audiovisual playback have not been performed. The four audio joins
are at **1:30.533, 1:51.767, 2:00.367, and 2:02.333**. These need perceptual review before shipping.
Candidate SHA-256: `523d86b547a86fbe0e0403fa78a1db1dad2fb33c1435f4ff0fa915151a687d13`.

Build and checks:

```sh
.video-venv/bin/python scripts/video/build_unexpected_results_v4.py
.video-venv/bin/python scripts/video/qa_unexpected_results_v4.py
HF_HUB_OFFLINE=1 .video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/unexpected-results-v4.mp4 --output-dir video-audit/unexpected-results-two-examples-v4-2026-10-23/transcripts
```
