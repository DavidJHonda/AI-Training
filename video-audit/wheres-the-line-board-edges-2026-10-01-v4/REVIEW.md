# Where’s the Line v4 — illustration edge repair

Updated both canonical lesson boards and rebuilt the approved v3 video assembly using them. The user authorized: “Update the boards, and use them in the video, please.” This is a narrow visual repair.

Candidate: [wheres-the-line-v4.mp4](../../Prompts/wheres-the-line-v4.mp4), 1280×720, 30 fps, 6,059 frames, 3:21.97.

SHA-256: `d4717575e5acbe4beecd64e9347a1aef89197a31a0bc3944e9de982b2c03019f`.

## Repair

The source artwork sheets contain white dividers. Their former crops included a few pixels of the divider at the right of left-hand cards and left of right-hand cards. The native board renderer now displays the sheets at 1504px wide instead of 1488px, with right-hand crops starting at -760px instead of -744px. Each 744px illustration window therefore has 8px of clearance from the sheet midpoint. Original vertical scaling and offsets are preserved.

All six illustrations fill their card windows. Board dimensions remain 1600×967 and 1600×1381. Text, card geometry, highlight bounds, camera paths, timing, cutaways, and audio are retained. Before/after pixel comparison confirmed identical pixels outside the illustration regions and adjacent JPEG blocks. [Edge comparison](board-edge-comparison.jpg).

The changed video spans are the visible board portions of frames 2898–3915 and 4370–5798, preserving the four existing cutaways. The longest uninterrupted board run remains 15.27 seconds. The video is rebuilt from the same frozen original source and v3 creative assets in one encode, avoiding another encode of v3.

## Verification

- Sequential decode: 6,059 frames at 30 fps; frame timestamp spacing matches 1/30 second.
- Encoded AAC packets and decoded PCM are hash-identical to the original source, as in v3.
- All eight encoded highlight states inspected at full resolution. All six illustration edges fill cleanly; full active cards and the two outcome highlights remain visible.
- Both full-board openings and every-frame strips for all 14 declared transitions inspected; transition guard passed 14/14.
- Source, installed video, index, lesson text, and creative assets unchanged during the build. The two canonical JPGs were deliberately updated before building.
- No direct audio audition or continuous audiovisual playback performed. The previously identified narration wording around 2:22 remains unchanged and unresolved; see the [v3 review](../wheres-the-line-repair-2026-09-30-v3/REVIEW.md).

Status: shipped locally; queued for batch deployment. User approved shipping with “ship it” after disclosure of the unchanged narration issue. Installed file and committed file each match candidate SHA-256. Local commit: `238d0bf0122b37ffa64b0d9be756ba6459cad38d`. Video cache key `20261001ship4`; both board cache keys `20261001edges4`. No push or deployment performed. V3 and V4 candidates remain available. The listening limitation above remains unverified, not a passed check.

## Reproduction and evidence

- [Board renderer](../../scripts/video/render_wheres_the_line_boards.cjs)
- [V4 build wrapper](../../scripts/video/build_wheres_the_line_v4.py), reusing the v3 assembly
- [V4 QA wrapper](../../scripts/video/qa_wheres_the_line_v4.py)
- [Manifest](edit-manifest.json), [encoded QA](qa.json), [board QA](board-qa.json), [transitions](transitions/transition-guard.md)

Commands from repository root:

```sh
node scripts/video/render_wheres_the_line_boards.cjs
.video-venv/bin/python scripts/video/build_wheres_the_line_v4.py --prepare-only
.video-venv/bin/python scripts/video/build_wheres_the_line_v4.py
.video-venv/bin/python scripts/video/qa_wheres_the_line_v4.py
```
