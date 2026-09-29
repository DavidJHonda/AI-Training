# Beyond the Average v10 — review candidate

Built 2026-09-29 following the owner's “Agree. Built it please.” Approval applies to the narrow visual plan in `../beyond-the-average-current-spec-review-2026-09-29/NOTEBOOK-GRAPHICS-REASSESSMENT.md`.

Candidate: `Prompts/beyond-the-average-v10.mp4` (1280×720, 30 fps, 4,984 frames, 2:46.133). Ready for owner playback review; not shipped or published.

## Result

The original Notebook teaching sequences, progressive reveals, illustrative percentages, independent diagrams, and changing technology labels remain in their original positions. No broad Notebook graphics replacement was made. The Same Tool board remains unchanged.

The What to Start Building Today board retains its complete-card framing, spoken order, and full unmarked opening. Three existing Notebook drawings interrupt the long board run. Its longest uninterrupted exposure drops from 53.700 to **15.400 seconds**; total main-board exposure is 42.633 seconds. The final main-board-plus-close run is 19.833 seconds.

| Insert | Candidate interval (exclusive end) | Source frames (exclusive end) | Purpose |
|---|---|---|---|
| Microscope | 1:52.000–1:56.100 | 2595–2718 | Deep subject knowledge |
| Model construction | 2:03.933–2:06.600 | 2430–2473 | Turn knowledge into work you are proud of |
| Meeting | 2:22.000–2:26.300 | 2473–2588 | Communication, trust, and team action |

The originally provisional writing/model/math montage was reduced to one model shot because the spoken list was too fast for three readable cuts. The approved plan explicitly permitted adjusting the selection and length. Source motion is retained by temporal resampling; there are no added single-frame freezes. The microscope runs at source speed; model and meeting shots are slowed to fit their intervals.

Five rebuilt course rings use the current fixed 4 px at 720p policy. An existing supersampled outer-minus-inner renderer avoids OpenCV's nominal 4 px stroke painting five solid pixels. The white canonical closing asset replaces the old close background with the same 48-frame hold, 150-frame push to 1.2×, and 162-frame settle.

## Validation and limits

- Full decode succeeds: 4,984 frames, 30 fps, 1280×720.
- Original audio packet payload is identical; narration, pauses, and duration are unchanged. The prior KEEP recommendation and recorded owner exceptions still apply.
- Automated transition guard passes at all eight changed boundaries. All 25-frame strips were visually inspected: clean cuts and returns, no stray scene fragments or transient flashes.
- Fourteen encoded keyframes inspected across all changed cards, supporting shots, board return, banner, and close. Complete active cards and closing copy are visible. Adjacent cards may extend outside the frame during intentional dense-board dives.
- Native renderer verification measures exactly 4 px on all four straight sides. The encoded half-second scan finds predominantly 3–4 solid-colour pixels at its strict threshold; this is a colour-threshold diagnostic after compression, not a different stroke policy. See `ring-native-verification.json` and `rings/ring-stroke.json`.
- Source video and canonical future/close artwork hashes remain unchanged. The live lesson reference was not edited.
- **No continuous playback with audible narration was performed.** Frame inspection, transcript alignment, and identical audio do not certify perceived motion pacing or audiovisual synchronization. Owner viewing/listening review remains outstanding; no final audiovisual or shipping pass is claimed.

## Provenance

Built directly from the hash-pinned shipped v8 because pristine source rolls were unavailable. The assembly uses a temporary source copy that is removed after completion. v10 does not use v9 as input; v9 is a superseded first build with an over-thick rasterized ring.

- Source SHA-256: `b50c3baa71e04088adb40898b73758acab11f3f2f0a34645c767ac82416c453a`
- Candidate SHA-256: `646b062e8b2f59d62a241e47f606c6765f1f71a698cc49d6e205b129e93d41a9`
- Audio payload SHA-256: `a912bfe9764fe298f7caa3a327abbf834035f70f47b42c184d4084c0eca335c7`

Build entry point: `.video-venv/bin/python scripts/video/build_beyond_the_average_v10.py` (imports the local v9 assembly implementation and existing renderer helpers). See `edit-manifest.json` for all frame boundaries and protected asset hashes; `guard/transition-guard.md`, `encoded/`, and `picture-qa-*.jpg` retain inspection evidence.

## Local shipping — 2026-09-29

Owner explicitly requested the directory/video rename and shipping v10. Shipped locally in commit `e61c36e759c700fe82071d424399bcce99adc5b0`; queued for batch deployment. No GitHub push or Vercel deployment was performed.

Installed: `course-assets/beyond-the-new-average/beyond-the-new-average.mp4`, cache key `20260929ship10`. SHA-256 remains `646b062e8b2f59d62a241e47f606c6765f1f71a698cc49d6e205b129e93d41a9`, verified both on disk and in the committed Git blob. Candidate renamed to `Prompts/beyond-the-new-average-v10.mp4`. All three board filenames and their directory were renamed consistently; their bytes are unchanged. The original audit directory and provenance paths are retained as historical records.

The shipping guard decodes all 4,984 frames and passes all 14 declared boundaries, including retained edits; boundary strips were reviewed. Page links resolve, inline JavaScript compiles, and legacy slug aliases resolve to the renamed video. The design check has two pre-existing baseline flags (font declarations and em-dash count), unchanged by this release.

The previously disclosed continuous viewing/listening check remains unperformed; the owner subsequently authorized shipping this exact candidate. This record does not claim an independent full audiovisual pass.
