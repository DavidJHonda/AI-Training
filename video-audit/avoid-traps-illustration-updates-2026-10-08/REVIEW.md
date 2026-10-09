# Avoid Traps illustration updates — 8 October 2026

Three owner-approved illustration updates shipped locally in commit 2e638b82a6bcf6902443e6d6f19345d7c6ff7d99. Queued for batch deployment; no push or deployment performed.

| Lesson | Source | Candidate | Changed frame range (30 fps, end exclusive) |
| --- | --- | --- | --- |
| Document Trap | v3 | v4 | 5525–5930 (13.50 s) |
| Support Trap | v13 | v14 | 3506–3886 (12.67 s) |
| Fake Trap | v10 | v11 | 6068–6217 (4.97 s) |

The full source selection and hashes are in `sources.json`; individual manifests record the resulting candidate hashes. Candidates are saved under `Prompts/`. Course assets now contain the approved candidates, with cache keys 20261008ship4, 20261008ship14, and 20261008ship11. The other six Avoid Traps videos are unchanged.

## Visual treatment

- Document Trap: student checks an original rulebook beside the AI quotation. Original passage emphasis at frame 5640; the matching six-foul wording at 5732; learner responsibility at 5861. This is labeled a lesson example, without a league attribution or automated verification verdict.
- Support Trap: fixed email, parent, and study panels. Parent preparation is emphasized first; study preparation at 3572; neutral preparation at 3658; send at 3746, parent conversation at 3776, studying at 3848. Paired photographs reveal the action at the relevant narration cue.
- Fake Trap: fixed phone scene. Urgent voicemail at entry; saved contact at 6133; outgoing call at 6179. No real phone number or claim that the request is genuine.

Seven photographic assets were generated or edited with the built-in image generation tool. All are saved in `assets/`; complete prompts and source provenance are in `assets/prompts.json`. Exact text, highlights, and interface states are code-rendered. The repeatable builder is `scripts/video/build_avoid_traps_illustration_updates.py`.

## Retained material and limitations

Narration, pauses, durations, course board text, highlights, and camera paths remain. Document Trap keeps the owner-approved continuous supporting shot through the final quotation-checking line. Support Trap retains the existing cafeteria image, three-jobs boards, later story, warning, and safety guidance. Fake Trap preserves the v10 shortening and does not restore the removed school-closure walkthrough.

The existing Document Trap narration overclaims remain outside this visual-only edit; see `video-audit/document-trap-repair-2026-09-29-v2/NARRATION-NEEDED.txt`. Support Trap’s inherited story wording also remains unchanged. This is not a new narration or factual verdict.

Sources are finished approved videos reencoded once at H.264 CRF 16. Audio streams are copied into full candidates. Browser excerpts are separately encoded for review with three-second context handles.

## Verification evidence

`verify.py` performs full sequential source/candidate decoding, frame-count and frame-rate checks, identical audio payload hashing, comparisons for every inserted frame, retained-frame comparisons every second and at boundaries, and transition checks for every entry, state change, and exit. Results are recorded in `verification.json` and `transitions-*/`.

Manual encoded-state and transition-strip inspection is recorded separately in `visual-review.json`. Browser checks are recorded in `browser-checks.json`. Continuous listening and audiovisual playback assessment by the agent are not completed or claimed. The owner approved shipping after reviewing the excerpts in `review.html`.

## Preview playback follow-up

The owner reported black preview surfaces. This was reproduced in the browser despite loaded media and no media errors. The local clips decoded valid pictures, and reloading restored visible playback. All six players now have explicit poster images and load on play rather than simultaneously; starting one pauses the others. Actual playback frames were visually confirmed in all three updated excerpts. Full candidate MP4s are unchanged. The precise browser-internal cause was not established.

## Local release

Installed candidate hashes, cache keys, durations, and commit are recorded in `local-install.json`. Installed files, committed blobs, and files served through the localhost course URLs all match the approved candidates. Only the three MP4s and three `index.html` cache-key changes are committed; unrelated site work remains outside this release. Prior complete decode, audio equality, and frame/transition verification was reused because candidate hashes are unchanged.
