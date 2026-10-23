# Loudest Voices v9 — built for review

October 22, 2026. David approved the complete splice plan with “Yes, build it.” Candidate: `Prompts/loudest-voices-v9.mp4`, 1280×720, 30 fps, 9,380 frames, **5:12.667**. SHA-256: `8f3e1a3304accf690df5456ae6cf4686e00dd612dd764d92884bfc87c92ecdd6`.

## Result

Retains Loudest Voices through “Machines improve fast. Habits change at human speed.” Adds the complete In Your Hands comparison and energy-allocation takeaway, followed by its closing narration with the current canonical Loudest Voices closing JPG. The old Loudest Voices close, the donor's introduction, and Three Moves Worth Your Energy are omitted.

The existing expert and predictions boards, camera paths, highlights, Notebook animations, and useful donor illustrations are preserved. No new narration, extra silence, speed changes, or loudness processing. The two new audio joins have 5 ms fades inside the approved quiet handles. Candidate audio and video were each encoded once from the two finished approved source versions; pristine raw recordings are unavailable. Source hashes are asserted by the builder. The interrupted first assembly was retained as an incomplete scratch file after an encoder frame-rate warning; the final assembly explicitly sets 30 fps and passes decoded timing checks.

| Output | Source |
|---|---|
| 0:00–3:36.267 | Loudest Voices v8, 0:00–3:36.267 |
| 3:36.267–4:56.367 | In Your Hands v6, 0:35.800–1:55.900 |
| 4:56.367–5:12.667 | In Your Hands v6 audio, 2:47.300–3:03.600; current Loudest Voices closing artwork |

## Verification of the actual candidate

- Complete sequential decode: **9,380 frames**, expected runtime, dimensions, and 30 fps. Uniform timestamp steps verified.
- **All 8,891 retained video frames** compared with the exact mapped source frames. Mean pixel difference 0.243/255, maximum frame mean 1.434/255 at half resolution; consistent with a single encode and correct source alignment.
- Audio checked against the exact source-sample assembly with the intended quiet-handle fades: correlation **0.999981**, RMS difference 0.000862. Both splice sample discontinuities are below 0.000033 full scale; this is a numeric check, not a listening verdict.
- **2/2 transition-guard checks passed.** All 25 frames around each new splice were visually inspected. No old closing frame or Three Moves image leaks into either join.
- Sampled encoded frames inspected across the existing expert/prediction walkthroughs, comparison, both donor cutaways, and final close. Existing approved column-framing exceptions remain as planned.
- The final close has a 48-frame hold, 150-frame push to 1.2×, and 291-frame settled hold. Encoded beginning/push/end samples inspected; the literal final frame is the correct current closing board.
- Final join gaps measured at −35 dB: **1.161 seconds** and **1.596 seconds**, matching the approved preview plan. No additional silence was inserted.
- Fresh complete 845-word candidate transcript reviewed against the current lesson and the approved reuse plan. All essential teaching is present: opinions and expert disagreement; all three experts with backgrounds, predictions and admissions; all four missed predictions; people/habits; all five out-of/in-your-hands points; energy allocation; and the closing meaning. The approved donor paraphrases remain, including “the technology” for “AI” in the spoken close. No Three Moves narration or old sign-off appears.
- Existing name spellings and “warrior” in automatic transcription are not treated as new verified pronunciation errors; the source audio matches the already approved versions.
- Canonical installed videos, index.html, lesson Markdown, and closing JPG hashes remain unchanged.

## Review limits and next step

**Built for review; not installed or shipped.** Textual coverage and technical checks pass. Direct listening for voice continuity, pronunciation, cadence, and continuous audiovisual playback were not performed; no full KEEP/ship certification is claimed. The review page provides the complete candidate and jump buttons before the two joins at 3:36 and 4:56. Local workflow status is based on verified artifacts; the external Video Tracker was not inspected or changed.

Build: `scripts/video/build_loudest_voices_v9.py`. QA: `scripts/video/qa_loudest_voices_v9.py`. Evidence: `edit-manifest.json`, `qa.json`, `transitions/`, `join-silence.json`, `transcripts/loudest-voices-v9.txt`, and `encoded-contact-sheet.jpg`.
