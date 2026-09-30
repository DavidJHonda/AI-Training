# Loudest Voices v8

Approved September 30, 2026: David confirmed the Worrier pronunciation is correct and requested a build of the suggested visual improvements. This is a narrow visual repair, with no narration, timing, or pause changes. The initial request authorized a candidate build. David subsequently approved shipping with “ship it”; the local release is recorded below.

## Changes

- **Expert-board framing:** unmarked full-board opening, then the complete active expert card at left and a magnified viewport of its current source section at right. The original illustration, name, background, both quotations, and card bottom remain visible throughout each expert's discussion. Text is sampled directly from the canonical JPG, with no retyping, reflow, or canonical-file modification. At synthesis, return to the full board and retain the approved three-card highlight sequence.
- **Fixed highlights:** 4-pixel outlines drawn after scaling, including full-board synthesis. The historical-predictions board is not rebuilt.
- **Habits animation:** replace the three hard-to-read labels with “Machines improve fast,” “Habits change more slowly,” and “Adoption takes time.” Keep the original moving markers, bars, connecting line, badge, timing, and fade progression. Stationary source paper clears the old top/bottom labels; the central label uses a small glyph mask. A small symmetrical corner sample preserves the later badge where it overlaps the former title.
- **Preserved:** all narration including “Worrier,” runtime, existing pauses, opening graphics, building/Flawed Approach cutaways, historical chart, predictions-board walkthrough, synthesis wording, and canonical close.

## Board treatment and timing

| Board | Highlight sequence | Framing | Output spans |
|---|---|---|---|
| Even the Experts Don’t Know | Whole active card for identity, then its SAYS and BUT ADMITS section; three cards as named in synthesis | Full unmarked introduction; complete active card plus magnified source detail; full board for synthesis | 0:23.73–1:09.33, 1:14.13–1:37.67, 1:40.17–2:18.07 |
| This Has Happened Before | Existing four cards, then takeaway | Preserved exactly | 2:29.40–3:22.30 |
| Where AI will be in ten years is a bet. / Which voice you listen to is your call. | None | Preserved exactly, including original motion and final hold | 3:36.70–3:49.47 |

**Framing choice:** a single complete-card zoom cannot materially enlarge these 1,395-pixel-tall cards within a 720-pixel-high delivery frame. The dual viewport is a deliberate treatment of that constraint: the complete source card provides attribution/context, while a second viewport makes the active text readable. Unlike the old section-only view, the full card remains on screen. This unusual treatment was communicated during the build; it implements the approved readability and attribution improvement without redesigning a course asset.

Longest unchanged board runs: 45.6 seconds for the first expert span, 37.9 seconds for the last expert span, and 52.9 seconds for predictions. The earlier owner-directed extended holds are preserved. No new decorative cutaway is inserted.

## Source and method

- Base: canonical `course-assets/loudest-voices/loudest-voices.mp4`, verified v7 hash `e671f6bceff6b2e31d1dee294c638c437e951d7cb99a708ffd981ae812f16391`.
- Stable active-build snapshot: `source-v7.mp4` in this folder. Raw Notebook rolls are no longer present, so no pristine raw source is claimed.
- Candidate: `Prompts/loudest-voices-v8.mp4`.
- Re-encode only changed complete GOP ranges: `[712,2080)`, `[2224,2930)`, `[3005,4142)`, `[6069,6501)`.
- Remux all other video packets and every AAC packet unchanged. No new audio splice or encode.
- 6,884 frames, 30 fps, 1280 × 720, 3:49.467.
- Build script: `scripts/video/build_loudest_voices_v8.py`; QA: `scripts/video/qa_loudest_voices_v8.py`.
- Geometry, spoken onsets, source/asset hashes, boundaries, and candidate hash are retained in `edit-manifest.json`.

## Verification

**Approved and shipped locally; queued for batch deployment.** Candidate SHA-256: `d553d341c258f1420b8a5927f6a6cdd2652a12b1f0d6fafe5d55f66089b497a4`.

- Sequential decoded frame count: **6,884**, 30 fps, 3:49.467, matching the source exactly.
- All **10,758 AAC packets**, their timestamps, and the decoded PCM are identical. PCM SHA-256: `86bff45f3d2f7e40a070dd5c144aafb6f7c062f5f3f5ae8d7ef73abba3aded19`.
- All **3,241 frames outside the edited ranges are pixel-identical**; unaffected compressed video packets also match. This includes the complete predictions-board sequence and canonical close.
- **23/23 transition checks passed.** All generated every-frame boundary strips inspected in `boundary-review-00.jpg` through `boundary-review-07.jpg`; no stale-frame flash found. These include each expert-section change and synthesis highlight, not only the four replacement-range boundaries.
- Encoded identity/SAYS/BUT ADMITS states for all three experts inspected at delivery resolution: full context card visible, no clipped quotation or ring, appropriate accent colors. Full-view open and synthesis states checked separately.
- Habits-label previews and encoded states checked before reveal, during the marker progression, and at the final badge state. Old labels are removed, new wording is readable, and the original diagram continues through its final state.
- At build completion, canonical source video, current boards, and lesson hashes were unchanged, and the site reference had not been edited. Local installation is recorded below.

The first assembly attempt correctly stopped before writing a candidate because the replacement codec's picture-parameter set differed when encoded at CRF 17. Encoding the changed ranges at the source's CRF 18 produced matching codec configuration, enabling exact remuxing of unaffected spans. The final candidate above passed the actual decode and packet comparisons.

No direct continuous audiovisual playback or listening is claimed. The user has resolved the pronunciation concern. Audio preservation is checked by packet bytes/timestamps and decoded PCM identity; these establish no audio change, not a new subjective listening evaluation.

The candidate build left the canonical video, boards, lesson, and site reference unchanged. The subsequent local release replaces only the canonical video and its cache key. Unrelated workspace edits belong to other work and are preserved.


## Local release — September 30, 2026

- Authorization: David said “ship it” after reviewing the v8 build.
- Status: **shipped locally; queued for batch deployment**. No push or deployment performed.
- Local commit: `91ff099a2185b02f9a33645727a09454e1eda0f5` — Ship Loudest Voices v8 readability improvements.
- Installed: `course-assets/loudest-voices/loudest-voices.mp4`.
- Installed and committed SHA-256, both verified against the approved candidate: `d553d341c258f1420b8a5927f6a6cdd2652a12b1f0d6fafe5d55f66089b497a4`.
- Course entry: `whatpeoplesay`, cache key `20260930ship1`, displayed runtime remains `4 min`.
- Commit contains exactly the canonical video and this one-line course-reference update. Audit/build records remain local.
- Prior candidate checks apply to the identical installed bytes: 6,884 decoded frames, unchanged runtime/audio, 3,241 untouched frames pixel-identical, 23 passing transition checks. The direct continuous playback/listening limitation above remains accurately recorded.
- Scoped render-scratch cleanup completed after commit: dry run, then delete for these two Loudest Voices audit folders only; three diagnostic WAV files removed. Candidate, stable source snapshot, build records, visual evidence, and unrelated builds retained.
