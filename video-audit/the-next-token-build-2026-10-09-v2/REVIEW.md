# The Next Token — production candidate v2

**Candidate:** `Prompts/the-next-token-v2.mp4` · 3:21.10 · 1280×720 · 30 fps.

Built under the user’s “Build it please” approval of the October 9 comparison and proposed edit plan. Version 3 supplies the narration; Version 1 supplies one complete two-sentence qualification. This is a review candidate, not a release installation.

## Implemented changes

- Removed the duplicate first Spot-at-22% sentence, the “permanent context” sentence, comparison metacommentary, unsupported speed claim, and redundant final explanation.
- Added the complete Version 1 illustrative-probabilities/Other beat at 2:58.33–3:06.27, level-matched by +1.44 dB.
- Replaced the malformed opening with a token-building diagram. Retained the dog prompt, probability-versus-certainty drawings, animated variety example, Buddy/Max branching explanation, and temperature illustration.
- Used Version 2’s cleaner 100-trial animation, with no source audio from that roll.
- Inserted the canonical five-pick board and a short animation showing the same blank resetting across separate picks.
- Captured the current TemperatureScene states and revealed them at the spoken low/high-temperature cues; added explanatory concentration/spreading animations and fixed 4 px outlines.
- Retained the original learned-weight matrix with simplified labels and changing probability bars. The weights stay visually fixed.
- Installed the canonical closing image in this candidate, with a 48-frame hold, 150-frame push to 1.2×, and settled final hold. Removed the branded tail and corner marks.
- Version 2 corrects the full footer-mask bounds in the branching scene from the first render. Both candidates are retained; v2 is the intended review file.

## Audio edit locations

| Output time | Change |
|---|---|
| 0:33.53 | Duplicate Spot sentence removed |
| 1:52.10 | Permanent-context sentence removed |
| 2:50.93 | Comparison commentary removed |
| 2:58.33 | Version 1 qualification begins |
| 3:06.27 | Return to Version 3: unchanged learning |
| 3:12.20 | Redundant conclusion removed; close begins |

No midlesson silence was added. All six joins fall at measured quiet source frames and have 5 ms ramps; the standard close has three seconds of source-derived room tone after the retained speech span. Listening remains required to assess cadence and voice continuity.

## Verification

The assembled narration was fully transcribed and checked: both opening paragraphs, qualified 22-out-of-100 explanation, sampling label, five named picks, separate-attempt distinction, app setting, low/high effects, 22/36/16 comparison, illustrative qualification, unchanged-learning statement, and both closing lines remain. The flagged permanent-context and speed phrases are gone.

The retained “would become ... repetitive” wording is the editorial limitation identified in the approved comparison; this build preserves that agreed wording rather than inventing a new phrase-level audio repair.

Encoded QA results are recorded in `qa.json`; transition details are in `transitions/transition-guard.json`. Exact source hashes, audio and visual spans, capture hashes, and unchanged protected-file checks are in `edit-manifest.json`.

Completed encoded checks: all 22 transition boundaries passed; 6,033 frames decoded at 30 fps (201.10 seconds). The AAC/assembled-audio correlation is 0.999985, with no clipped samples and a −1.15 dBFS peak. All six edit joins fall within measured quiet gaps. The final frame matches the canonical closing crop within the configured tolerance. Four encoded boundary-summary sheets were visually inspected. Playback and the Temperature section jump were verified in the local review player, served with byte-range support at port 8880.

**Direct listening and continuous audiovisual review have not been completed.** ASR and waveform agreement do not certify pronunciation, donor voice continuity, or audible joins. The playback page includes section jump buttons; particularly audition the donor entrance at 2:58.33 and return at 3:06.27.

## Reproducibility

- Build: `.video-venv/bin/python scripts/video/build_the_next_token_v2.py` (refuses to overwrite a candidate).
- QA: `.video-venv/bin/python scripts/video/qa_the_next_token.py video-audit/the-next-token-build-2026-10-09-v2`.
- Source/capture/render logic: `scripts/video/build_the_next_token_v1.py`, v2 footer correction, and `scripts/video/capture_the_next_token_v1.cjs`.
- Playback: `review.html`. Prepared and encoded frames, transition strips, isolated audio join clips, and complete assembled transcript are retained here.

Course assets, lesson text, generation prompt, and source rolls are protected by hash checks. The course player, current installed video, tracker, Git release state, and publishing configuration were not changed by this build.
