# Hallucination v4 review candidate

Status: **REVIEW CANDIDATE — not shipped**

## Deliverable

- Candidate: `Prompts/hallucination-v4.mp4`
- SHA-256: `9c75c1ce9c123bd0b56dc83bf2239545e685b80f5f30a2ecd0c512e068db009e`
- Runtime: 5:43.33
- Video: 1280×720, 30 fps, H.264
- Audio: 48 kHz mono AAC
- Build script: `scripts/video/build_hallucination_v4_review.py`

## Edit

- Uses `Prompts/hallucination-2.mp4` as the narration and Notebook-animation spine.
- Replaces the grammatically faulty pizza-question beat with one complete beat from the live Hallucination-1 video.
- Graft output span: 3:28.83–3:41.03. The finished transcript reads: “When users searched for a way to keep cheese from sliding off a pizza, an AI tool provided a very specific solution. Mix about one-eighth of a cup of non-toxic glue into the tomato sauce.”
- The donor was raised 0.728 dB and joined inside existing quiet windows with 5 ms transitions to matched room tone. No teaching pause was added.
- Inserts the four current course boards with the approved full-view, zoom, and ring treatments.
- Removes the generated engine outro and ends on the canonical two-line close with a restrained 1.2× push and settled hold.
- Cleans the Notebook corner mark on all retained Notebook frames. No cleanup frame was declined.

## Verification completed

- Full file decoded successfully: 10,300/10,300 frames and the complete audio stream.
- Complete output transcript reviewed against `lessons/hallucination.md` and the current Hallucination lesson in `index.html`.
- The repaired pizza wording appears once; “Yeah, glue” appears once after it.
- Both closing lines are present verbatim.
- All eight four-second contact sheets were visually inspected end to end.
- All ten requested edit-boundary strips passed `transition_guard.py` and were visually inspected.
- The literal ending is the canonical close; no generated engine outro remains.
- Objective audio checks at the two graft joins found quiet boundaries and no sample discontinuity:
  - 3:28.83: 0.001394 sample step, −55.45 dBFS over the surrounding 20 ms.
  - 3:41.03: 0.000065 sample step, −50.48 dBFS over the surrounding 20 ms.
- Peak decoded audio level is 0.987933, below clipping.
- No added instructional pauses. The only silence longer than one second is the intended 4.36-second settled closing hold.
- Source video, live course video, lesson Markdown, and all board assets retained their pre-build hashes.

## Human listening still required

This environment cannot audition audio. Before shipping, listen in headphones across both narration joins at **3:28.83** and **3:41.03** for voice-match, cadence, room tone, and any perceptible seam. The transcript and waveform checks pass, but they do not replace listening.

## Audit artifacts

- Edit manifest: `edit-manifest.json`
- Timestamped transcript: `verification-transcripts/hallucination-v4.json` and `.txt`
- Full contact sheets and scene/hold reports: `verification/hallucination-v4/`
- Transition report and strips: `transitions/`
- Audio-gap candidates: `audio-gap-review/`

No live lesson file, existing video candidate, or deployed asset was changed.
