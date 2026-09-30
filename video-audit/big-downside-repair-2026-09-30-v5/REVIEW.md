# Big Downside v5 — approved repairs, September 30, 2026

Review candidate: `Prompts/big-downside-v5.mp4`, 10,114 frames at 30 fps, **5:37.13**. Approval: “Make the repairs please,” following the live evaluation in `../big-downside-live-review-2026-09-30/REVIEW.md`. This authorizes the repairs, not installation or publication.

## Completed edit scope

1. **Callback correction, around 3:00.43.** Delete “The only defense is,” retaining “Step four. Hang up and call the person back on the real number.” Source audio deletion: **3:00.433333–3:01.600000**, exactly 35 frames / 1.166667 seconds. No new speech, voice cloning, or substitute voice. The voice-clone board is rebuilt from the canonical JPG at full view, with the four full-height column outlines; its Call Back outline follows the repaired step-four onset. New outlines use the current fixed 4-pixel stroke at 720p.

2. **Historical-safety introduction, new 4:10.10–4:16.67** (old 4:11.27–4:17.83). Replace the unrelated AI architecture diagram with a purpose-generated museum-style display of an early touring car, biplane, and smartphone. Separate video text first reveals “New technology arrives.” and then “Safeguards follow.” The following canonical timeline remains intact. The generated image is illustrative, not an archival photograph.

All other picture content follows the original frames, shifted by the single deletion after 3:00.43. Other decoded audio is retained exactly in the assembly, except 5-millisecond ramps at the one edit. No additional pauses, general audio cleanup, or unrelated visual changes. The standard close and its existing motion are preserved; the close now starts at **5:26.77**.

The voice-clone board now runs **22.60 seconds**. The previous documented exception remains; no decorative cutaway was added. Other boards and their previously approved treatments are unchanged.

## Source limitation and unresolved details

The four original rolls identified in the older review no longer exist at their recorded paths. A filename search of this repository and the user's Downloads, Desktop, Documents, Developer, and accessible Trash returned only the canonical finished video. Their old transcripts survive but are not audio sources. Asked the user asynchronously for their current location; none has been supplied as of this record.

Consequently the build uses the exact finished source recovered from Git into `/private/tmp/big-downside-83ecf2e1-source.mp4`, with asserted SHA-256 **83ecf2e1a9de491260981d6048ce792657a478cfcfe6be13ad71d4314fc902d4**, matching the verified public video. This entails one additional H.264/AAC encode. It does not rebuild from v4.

The missing spoken historical dates, Policy Puppetry's tested-model breadth, the omitted “the” in the goal takeaway, and the pacing statement's conditional phrase **remain unresolved**. They cannot be restored from absent donor files or from on-screen text. No formal KEEP or whole-file shipping sign-off is claimed.

## Audio boundary refinement

The first v4 trial cut too early and retained “is” before “step four.” Automatic transcription caught it. v4 is superseded and should not be reviewed or shipped. Further source waveform inspection, source word timestamps from base.en and medium.en, and three short cut trials located a later boundary. The earliest trial that removed “is” while retaining “Step four” was selected for v5. ASR and waveform checks are evidence, not a substitute for listening.

## Verification

- Final decode: **10,114 frames, 30 fps, 337.133333 seconds**.
- PCM outside the single deletion and its 5-ms ramps is exactly preserved. Encoded audio correlation with the assembly: **0.999978**.
- 155 unchanged-picture samples matched their mapped source frames within expected re-encoding differences (maximum mean absolute pixel difference 2.784/255).
- Transition guard: **5 boundaries passed, 0 failed**. Manually inspected all five every-frame boundary strips; no stray frames, visual flashes, or unintended scene islands were observed.
- Inspected encoded board/highlight previews, the historical insert with both text lines, and the literal final frame. Framing and overlays are intact.
- Final encoded callback ASR reads: “They create immediate panic, demanding money. Step 4, hang up and call the person back on the real number.” The removed “only defense” wording is absent.
- Exact source and published local-file checksums remain unchanged. Detailed numeric results: `qa.json`; transition evidence: `transitions/transition-guard.md`.

**Listening and continuous audiovisual playback have not been performed.** ASR does not establish natural cadence or the absence of an audible splice; the final callback join still needs a listening review.

## Reproduction and artifacts

- Build: `.video-venv/bin/python scripts/video/build_big_downside_v5.py` (imports the shared narrow-repair implementation in `build_big_downside_v4.py`). Existing candidates are never overwritten.
- QA: `.video-venv/bin/python scripts/video/qa_big_downside_v5.py`.
- Exact source/output spans and checksums: `edit-manifest.json`.
- Image: `scripts/video/assets/big-downside-history-2026-09-30/technology-history.png`.
- Full generation prompt and provenance: adjacent `PROMPT.txt`. Created with the built-in **image_gen** tool under the **imagegen** skill. The original generated raster is unchanged; labels are separate video overlays.
- Source, intermediate, and final callback transcripts are retained in the v4/v5 audit folders. Only the final encoded transcript is evidence for the delivered candidate.

No live file, course reference, tracker row, or generation materials have been changed. Not installed, committed, pushed, or deployed.
