# Hallucination v15 — Check the Match cue

Approved follow-up to v14: make the third step visible and explicitly name it during the pizza application. Candidate only; no installation, commit, or publication. Built directly from the public-identical finished v12 because the pristine generation is absent locally. The prior v14 narration cuts and other repairs are retained.

Candidate: `Prompts/hallucination-v15.mp4`, 7,999 frames, 30 fps, 1280×720, **4:26.633** (1.3 seconds longer than v14).

## Changes

| Change | Original source | Candidate |
|---|---|---|
| Restore Check the Match highlight during Stanford verification | 3:49.667–3:54.900 | 3:34.600–3:39.833 |
| Retain UNVERIFIED ≠ FACT for the conclusion | 3:54.900–4:03.167 | 3:39.833–3:48.100 |
| Show full Check the Claim board before the pizza cue | 4:16.000 onward | 4:00.933–4:03.300 unmarked |
| Insert “and check the match” from this narrator’s earlier introduction | Donor 3:19.700–3:21.000, inserted at source 4:18.000 | Donor window 4:02.933–4:04.233 |
| Highlight third column at spoken “check” and retain through the source-support explanation and Reddit-joke conclusion | Source resumes at 4:18.000 through 4:29.500 | Ring 4:03.300–4:15.733 |
| Preserve original standard close | 4:29.500–4:40.400 | 4:15.733–4:26.633 |

The donor says **“and check the match”**, using the existing voice, rather than synthesizing “Third.” The visible numbered third column identifies its place in the sequence. This phrasing choice was communicated during the build. The teaching now explicitly names the step before explaining that finding text is insufficient: the source must actually support the claim, and a Reddit joke does not.

## Board treatment

**Check the Claim** uses the current canonical `course-assets/hallucination/hallucination-check-claim.jpg`, unchanged. Compact board, full view throughout. The teal `#0e8f86` outline encloses the entire third column of the shared white box; fixed 4 px delivery stroke drawn after resizing by `ken_burns_path.py`. The Stanford highlight continues an established board sequence. The returning pizza board is unmarked for 2.367 seconds before its ring appears. No zooms or new reading pauses.

The Stanford board run is now 24.5 seconds while narration walks steps 2 and 3; the pizza return lasts 14.8 seconds and stays on the source-support teaching. Earlier pizza illustrations remain. The returning board replaces the final illustrative source walk specifically to connect that explanation to the named third step.

## Verification status

Encoded-file checks passed. The added phrase joins are in measured quiet gaps; 4 ms interpolation at the seams preserves timing and speech. No synthetic voice. `edit-manifest.json` records source/output ranges and protected-file hashes.

Listening is outstanding: no subjective audition or real-time end-to-end watch/listen is claimed. Review the new cue and its context around **4:00–4:16**, plus the restored Stanford highlight around **3:34–3:40**. ASR and signal checks do not certify delivery or intonation. This is a narrow review candidate, not a whole-video ready-to-ship certification. Earlier out-of-scope board treatments remain as described in the v14 review.

Reproduce with `scripts/video/build_hallucination_v15.py`; encoded checks use `scripts/video/qa_hallucination_v15.py`. Candidate filenames are immutable.

## Completed verification

- Full decode: **7,999 frames**, **266.633 seconds**, no decoder errors.
- Automatic transition guard: **13/13 boundaries passed**, no brief intermediate scene detected.
- Inspected every-frame strips at the restored Stanford highlight, its exit, the pizza-board entrance, cue-ring onset, audio-insert exit, and standard-close entrance. The intended rings appear cleanly without a stray prior state. Full-resolution cue and closing frames inspected.
- Compared **246** retained-picture samples against mapped original frames; maximum mean absolute difference **0.662/255**. Compared **24** board samples to the lossless board legs; maximum **2.109/255**.
- Exact PCM assembly versus decoded AAC: **43.33 dB** signal-to-error ratio, **12,798,400** planned audio samples. Added joins have local peaks near **−60.5/−59.9 dBFS**.
- Fresh ASR of the encoded example confirms “and check the match,” “Finding the text is only part of the process,” and the explanation that the source must support the claim and the Reddit thread was a joke. `encoded-match-transcript.json` retains the recognizer output; its punctuation and approximate timestamps are not an audition or word-boundary guarantee.
- Literal final frame maps to original frame **8411**. Canonical source, index.html, lesson text, and JPG hashes verified unchanged after QA.
- Candidate SHA-256: `dc225c0e4c07c9292e7b852fdafb831dd2e63027ead3ec08668b7415a8e34cb2`.
- Detailed checks: `scripts/video/qa_hallucination_v15_details.py`; evidence beside this review includes encoded-audio WAV, source/output manifest, comparison reports, fresh frame sheets, and transition strips.

**Status: built and technically checked; listening review pending. Not shipped or published.**
