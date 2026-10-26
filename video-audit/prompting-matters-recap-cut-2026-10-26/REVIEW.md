# Prompting Matters: remove the four-qualities recap

October 26, 2026. Narrow edit authorized by David: “Now, let's edit the video to match the lesson,” following approval to remove the recap and keep the weak/better examples unchanged.

Candidate: `Prompts/art-of-prompting-v12.mp4`. Build: `.video-venv/bin/python scripts/video/build_prompting_matters_v12.py`. Verification: `.video-venv/bin/python scripts/video/qa_prompting_matters_v12.py`.

## Source and edit

Use the current canonical `course-assets/prompting-matters/prompting-matters.mp4`, SHA-256 `0c3e63b271877b449c6aca57bea490a9ddbf5c6bf7c76e5236ab33cdc2986d1f`. This differs from the retained v10 candidate, so the canonical file is the source of truth. Raw generation sources are unavailable; one further H.264 CRF16 encode and AAC encode are required for this edit. The source hash is checked before and after the build.

Remove source frames [797,1480), or 0:26.567–0:49.333. Removed narration begins “A good question is always the foundation. Prompting adds the instructions,” covers the four qualities, and ends “leaving room for an unexpected answer.” Retain source [0,797) and [1480,6936). The new join at 0:26.567 connects “We call that prompting” to “Packaging your question for AI comes down to four specific moves.” Both edit points are in existing room tone. No additional pauses, words, or grafts.

| Affected board | Treatment | Camera/highlights | Result |
|---|---|---|---|
| Four Qualities of a Good Question | Remove the complete recap board and its narration | Removed with the segment | No recap remains |

All other visuals, four weak/better examples, source-relative timing, board treatments, and closing motion are retained. The cut removes 683 frames / 22.767 seconds. Planned candidate: 6,253 frames at 30 fps, 3:28.433, from 3:51.200.

## Verification and limitations

The initial v11 encode was rejected for fractional frame-rate metadata after FFmpeg concat. It is not the review candidate. V12 explicitly sets 30 fps CFR and a 90 kHz video track timebase. Its build still starts directly from the canonical source, not v11.

Encoded QA results are recorded in `verification.json`; the declared join is audited in `guard/`. Review scope is the removed segment and affected join, with full retained-frame/audio comparisons. This does not certify a new whole-file production pass. No subjective audio audition or continuous end-to-end playback has been performed. The new join at 0:26.567 is supplied in `join-preview.mp4` for listening review. Previous source-review limitations outside this narrow edit remain outside scope.

Review candidate only. The installed canonical video, page video reference, Git history, and deployment are unchanged.

### Completed encoded checks

- Candidate SHA-256: `22f72b3820d15c29f2b2c64fa626ae9d06fa14fffe2079aef633e6cfc2fb0b77`.
- Decoded 6,253 frames, exactly 30 fps and 1280×720. Timeline is 208.433 seconds.
- Compared every retained frame to its mapped source frame. Maximum mean absolute difference at 160×90 is 0.680/255, consistent with the additional encode. All four prompt examples and the close retain their source frames.
- Decoded audio correlation against the exact retained source PCM is 0.999984. Join sample discontinuity is only 3/32768; the 20 ms handles peak at 63 and 65/32768, confirming the splice is in room tone.
- Transition guard passed the sole new boundary. Its every-frame strip was visually inspected: the recap does not flash, and the preserved four-moves animation starts at its original first frame.
- Local speech recognition of the encoded join confirms “We call that prompting. Packaging your question for AI comes down to four specific moves.” Transcript is in `join-transcript.json`. This wording check does not substitute for subjective listening.
- Canonical source hash remains unchanged. No local installation or publication.

## Shipped locally — October 26, 2026

David approved the delivered candidate: “Looks good. Ship it locally.” Installed v12 byte-identically and committed only the video, its manifest entry, its page reference, and the approved lesson recap removal. Local commit `d9dcb3fafa9ff905904ffb1c5a1ae72251feefab`. Installed SHA-256 `22f72b3820d15c29f2b2c64fa626ae9d06fa14fffe2079aef633e6cfc2fb0b77`. Cache key `20261026ship12`; rounded runtime label “3 min.” Existing design flags (2 raw fonts and 9 em-dashes) are unchanged from HEAD; JavaScript syntax and staged whitespace checks passed. The owner reviewed the candidate; no additional agent listening is claimed.

The previous canonical source is retained at `Prompts/art-of-prompting-recap-source-20261026.mp4`; the builder now points to this hash-pinned source for reproducibility. Scoped cleanup removed three regenerable WAV files; review media and evidence remain. No push or deployment. **Shipped locally; queued for batch deployment.**
