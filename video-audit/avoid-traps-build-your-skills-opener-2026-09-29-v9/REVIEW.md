# Avoid Traps opener v9 — approved visual refresh

**Shipped locally; queued for batch deployment.** Installed v9 at `course-assets/avoid-traps-opener/avoid-traps-opener.mp4` in commit `44d04064a01a2adc9a97a4cb89cae76207378ace`. Review candidate retained at `Prompts/avoid-traps-opener-v9.mp4`.

## Approved scope and result

David approved the September 29 evaluation, including its optional panel label. This is a visual-only repair of the verified live v7. The narration, pauses, runtime, opening, Read the Water camera walk, binoculars, short map-banner return, and standard closing sequence are retained.

| Output | Change | Source / treatment |
|---|---|---|
| 1:32.567–1:40.633 | Add “Looks helpful. Hides the risk.” inside the blank yellow panel | Original drawn scene retained. Two-line navy text tracks its camera movement through all 242 frames. |
| 2:04.333–3:08.867, excluding cutaways | Refresh the current canonical roadmap with fixed 4 px outlines | Full board; purple, blue, then teal rows at the original spoken onsets. No zoom. |
| 2:16.000–2:22.000 | First cutaway: plausible false fact | V7 picture from 0:36.867–0:42.867; original motion, semantic-failure reveal, and final state retained at normal speed. |
| 2:42.000–2:49.000 | Second cutaway: relaxed computer user | V7 picture from 0:42.900–0:49.900; normal-speed motion, no still extension. |

The first cutaway returns to an unmarked map for two seconds before resuming its first-row outline. The second returns 1.5 seconds before the third category is named; that ring appears at its original onset. The roadmap's three uninterrupted runs are **11.667, 20.000, and 19.867 seconds**, reduced from **64.533 seconds**. The Read the Water span is 18.833 seconds; no other retained board run exceeds 20 seconds.

The raw alternate roll mentioned in the evaluation is no longer present in the workspace. This build uses the live video's relaxed-computer-user scene, the evaluation's explicit fallback. Its timing was refined to the seven-second source span so the motion stays intact. The only available source is the finished v7; this candidate therefore has one additional video encoding generation. Its original AAC audio is copied, not re-encoded.

## Boards

- **THE TRAPS AHEAD:** preserve existing 0:00–0:13.100 full-board gold line outlines.
- **Read the Water:** preserve existing 1:13.733–1:32.567 full-view opening and illustration walk, unmarked.
- **Avoid Traps:** current page JPG, compact full-frame treatment, current fixed-width outlines, two cutaways above. Preserve the existing short 3:16.467–3:19.400 banner return.
- **When AI fails, nothing looks broken.:** preserve existing canonical close from 3:25.333 through the literal final frame, including the standard 1.2× push and settled hold.

Older opening/banner ring widths and the opening's pre-existing first-frame outline remain outside this narrow repair. The September 26 rule does not require rebuilding older shipped footage solely for stroke width. No narration cuts, grafts, new pauses, new generated imagery, or unrelated source edits were introduced.

## Narration

The prior evaluation's provisional KEEP carries forward because the full audio is unchanged. All essential teaching, the three-category map, and both closing lines remain. The prior wording cautions and listening limitation remain; this visual build neither edits nor newly certifies the inherited voice graft at 2:04.333–2:07.667.

## Verification

**PASS for the approved visual repair's encoded checks.**

- Complete sequential decode: **6,458 frames, 30 fps, 215.267 seconds**, unchanged from v7.
- Original AAC bytes, decoded PCM, and all **10,092 audio packet payloads/timestamps/durations are identical** to v7. No audio seam was introduced.
- Protected source video, four canonical JPGs, and lesson Markdown remain unchanged.
- Frame comparisons: 122 retained samples, 19 cutaway samples mapped to their exact source frames, five tracked-label samples, and 54 roadmap samples all passed their encoding-tolerance check. Maximum mean pixel difference was under 3 on the 0–255 scale in each group.
- All three rebuilt row colors measure **4 solid pixels** in the encoded video; purple was checked both before and after the first return.
- The transition guard passes **all 14 declared boundaries**. Five-frame strips immediately around every boundary were visually inspected, along with all five full-timeline contact sheets and the selected panel/map states. No stale-frame flash or cropped active card was found in these inspections.
- Label tracking succeeded through all 242 frames; minimum 2,372 matched inliers. It remains centered within the highlighted panel.
- The original canonical closing card is the final frame.

**Listening and continuous audiovisual review:** not performed. Audio identity proves preservation, not an auditory review of the inherited narration. Existing audio-graft and wording caveats from the live evaluation remain. These checks do not constitute a new auditory certificate. David subsequently explicitly approved shipping this disclosed candidate; the preserved audio and the recorded verification limits remain unchanged.

Candidate SHA-256: `3d86eeefdc8d99b0dc369b2ddb5e78d785da44146c4c7a5eb17bce2022d470f6`.

## Reproduction and status

Build: `.video-venv/bin/python scripts/video/build_avoid_traps_opener_v9.py`

QA: `.video-venv/bin/python scripts/video/qa_avoid_traps_opener_v9.py`

The manifest records the source/candidate hashes, protected assets, cutaway source/output frame ranges, exact board states, and declared boundaries. `label-tracking.json` records the per-frame transforms. Source previews, encoded frames, QA contact sheets, and boundary strips support inspection. V8 was superseded before delivery after its nominal 4 px rings measured only 3 solid pixels; v9 aligns the outlines to output chroma pairs so they retain four solid pixels in 4:2:0 delivery. At build time, the canonical video and website references were unchanged. The local shipping step below then installed the approved candidate.


## Local release — September 29, 2026

- Authorization: David's “ship it” after the v9 build report.
- Commit: `44d04064a01a2adc9a97a4cb89cae76207378ace` — only the canonical MP4 and its single `index.html` reference line.
- Cache key: `20260929ship1`; runtime pill remains `4 min` for the 3:35 video.
- Installed, candidate, and committed MP4 SHA-256 all match: `3d86eeefdc8d99b0dc369b2ddb5e78d785da44146c4c7a5eb17bce2022d470f6`.
- Verified the committed lesson reference and clean working/index state for both release paths. Other lesson work and audit/build files were excluded from the commit.
- Deployment: **pending the separately requested batch publication**. No GitHub push or Vercel deployment was performed, and public v9 availability is not claimed.
- Cleanup: removed the two regenerable roadmap canvases in this task's v8/v9 audit folders. Retained review evidence, candidate videos, and build scripts.
- Historical v7 source is recoverable from `44d04064^:course-assets/avoid-traps-opener/avoid-traps-opener.mp4` if a rebuild needs its pinned input.
