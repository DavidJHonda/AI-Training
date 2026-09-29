# Hallucination v14 — review candidate

Built on 2026-09-29 under David's “Agree. Build it please.” approval of the live-video evaluation. **Narrow repair: two narration cuts and supporting scenes in Check the Claim.** Candidate only; no installation, commit, push, or deployment. The source is the finished public-identical v12 because the raw generation is no longer present locally.

Candidate: [Hallucination v14](../../Prompts/hallucination-v14.mp4), **4:25.33**, 1280×720, 30 fps, 7,960 frames. It is 15.07 seconds shorter than v12.

## Completed changes

| Change | Original timeline | Candidate timeline |
|---|---|---|
| Remove “A hallucination rarely makes up the entire response. Instead,” | Cut frames 1451–1554, 0:48.367–0:51.833 | Join at **0:48.367**: “…sounds completely true, but isn't. It embeds a fabricated detail…” |
| Remove grammar guarantee and redundant “structurally perfect” sentence | Cut frames 3490–3837, 1:56.333–2:07.933 | Join at **1:52.867**: “…is a factual truth. People often use the term hallucination…” |
| Prevent the discarded monitor illustration from flashing after the second cut | Replace the retained nine frames at source 3838–3846 with frame 3847 | 1:52.867–1:53.167; immediately land on crossed-out ALL ERRORS = INVENTIONS |
| Break the Stanford application with the existing disappearing-paper/laptop illustration | Source narration 3:23.40–3:30.40; picture from 0:40.30–0:47.30 | **3:08.333–3:15.333** |
| Extend UNVERIFIED ≠ FACT over the verification explanation | Source narration 3:49.667–4:03.167; picture from source 3:59.467–4:03.167, retimed visually | **3:34.600–3:48.100** |

No new teaching pauses. Audio joins sit in measured quiet troughs; a four-millisecond interpolation spans each seam without changing duration or touching speech. Other retained narration is preserved, followed by one AAC encode. No voice generation or donor narration.

The completed Check the Claim board runs are now **11.23 seconds and 19.27 seconds**, replacing the 47.30-second uninterrupted run. The earlier Why Hallucinations Happen walk remains approximately 44.6 seconds; the exploratory wider board changes in the evaluation were not part of these concrete cutaways. Existing board artwork, framing, and rings remain untouched. The current ring-width rule does not require rebuilding previously shipped spans merely to change stroke width.

## Refinements made during verification

The initially proposed hallucination-blueprint cutaway contains **18.4%** and **undergraduate students**. Reusing it while the narrator explicitly says **18%** and **high-school students** would introduce a mismatch. The disappearing-paper drawing supports the invented-source point without that conflict. The blueprint's original appearance remains outside this narrow repair; it illustrates invented academic-looking details there and has not been presented as authentic evidence.

v13 was the first internal render. Its automatic transition guard passed, but inspection of the actual frame strips found a **single-frame Check the Match ring** immediately before the second cutaway. v14 starts that cutaway one frame earlier, covering the ring change. v13 was not overwritten and is superseded.

## Teaching and listening status

All essential teaching from the prior evaluation is retained: playlist question and exact fake-study numbers, invented detail among real facts, four mechanisms, real-source misinterpretation versus invented evidence, both checking applications, the unverified-versus-false distinction, and both closing lines. The two flagged overstatements are removed.

ASR on v13's encoded joins verifies the intended words and both closing lines. In particular, the first join retains **“It embeds a fabricated detail…”** and the second proceeds directly to **“People often use the term hallucination…”**. The recognizer writes “masks the air” where the retained source transcript also has that ambiguity; this repair did not change that phrase. ASR is a wording check, not a listening certification.

**Listening remains outstanding:** no subjective audition of the two joins, no real-time end-to-end watch/listen, and no full animation approval is claimed. Review the candidate around **0:48** and **1:53**, plus the checking sequence at **3:08–3:48**. Contextual WAVs are retained beside the manifest. This is ready for the owner's review, not a KEEP/ready-to-ship certification.

## Evidence and reproduction

- Build: `.video-venv/bin/python scripts/video/build_hallucination_v14.py`
- Encoded-file QA: `.video-venv/bin/python scripts/video/qa_hallucination_v14.py`
- Source SHA-256: `1c7189c1aedafb057d1740e60d469a55209c3350ad3de504dc363f3bcf44c253`.
- `edit-manifest.json` contains the candidate hash, source and output frame mappings, narration deletions, visual donors, and protected-file hashes.
- `verification.json` records full decoded frame count, audio comparison, sample discontinuities at the joins, visual comparison, and final-frame mapping.
- `transitions/` contains every-frame strips and the guard report for all seven declared boundaries.
- `candidate-sheet-*.jpg` contains fresh candidate frame samples across the whole file.
- The source MP4, index.html, lesson Markdown, and canonical board JPGs are hash-protected and unchanged by the build. No tracker status was changed.

## Final verification results

- Full encoded-file decode: **7,960 frames**, 4:25.333, no decoder errors.
- Seven declared transition boundaries: **7/7 guard passes**. Reviewed the original seven boundary strips, the corrected v14 cutaway strip, and full-size v14 join/cutaway/closing frames. The single-frame ring flash is gone.
- Compared **259** mapped video samples with their actual source frames: maximum mean absolute difference **0.662/255**, consistent with re-encoding. Retimed cutaway frames are excluded from this direct one-to-one comparison.
- Decoded AAC compared with the exact edited PCM: **43.34 dB** signal-to-error ratio at the same sample alignment; correct **12,736,000** planned samples.
- v14 and the transcribed v13 have **identical encoded audio packet hashes**, recorded in `audio-payload-verification.json`; the successful v13 encoded-join and close transcripts therefore apply exactly to v14.
- Final encoded quiet gaps around the joins: **0:48.207–0:48.392 (0.185 s)** and **1:52.630–1:53.185 (0.554 s)** at the diagnostic −35 dB threshold. No additional pause was inserted.
- Join-local peaks are approximately −55.7/−56.2 dBFS. These signal measurements do not substitute for listening.
- Literal final decoded frame maps to source frame **8411**, with the exact canonical closing message. Inspected full-size.
- Candidate SHA-256: `641304fa81138a2b7c0f1b384413144960cb0c74d2ebfe71be7b470beced3637`.
- Source video, current lesson, index.html, and canonical JPG hashes rechecked unchanged after QA.

**Status: built and technically checked; owner audiovisual review pending. Not shipped or published.**
