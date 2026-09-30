# Support Trap v8 — requested repairs

Candidate: `Prompts/support-trap-v8.mp4`. Duration **4:19.13**, 7,774 frames at 30 fps, 1280×720. Review candidate only; not installed or published.

- **0:40.33:** The gold outline moves from the complete chatbot card to its quoted response as the narration begins. The camera retains the complete active card. The outline moves to “Caring words” at the existing cue.
- **2:21.63–2:24.00:** Replaced the leaked “Direct Human Intervention” graphic and intervening fade with the settled “When Does Chat Become Dangerous?” diagram. Original diagram motion resumes at 2:24.00. Narration timing is unchanged here.
- **Original 3:30.70–3:31.87:** Removed the second, standalone “Leave the chat.” The retained sentence now leads into “Tell a trusted adult or school counselor.” Removed 35 frames / 1.1667 seconds, cutting at measured quiet troughs with 5 ms fades. The safety card highlight begins on the retained instruction at 3:28.33. All later material moves earlier by 35 frames.

Rendered from original source assets with the v7 recipe, preserving the previous lunch-transition and later urgency repairs. The source PCM is identical outside the deletion and its 5 ms seam edges. No global gain or narration replacement.

Validation: full export decodes to 7,774 frames with uniform 30 fps timestamps. All 30 transition checks pass. Inspected exported frames and every-frame strips at the repaired transitions. Unchanged regions agree with v7 within re-encoding variation (maximum sampled frame mean difference 0.222/255). Encoded audio correlation with planned PCM is 0.999987. The encoded safety passage transcript confirms one retained “leave the chat” instruction followed by the trusted-adult instruction; 988 and 911 remain present. Closing frame and 48/150/30-frame closing treatment are preserved.

Perceptual audio listening remains pending; waveform and transcript checks do not certify spoken cadence. No claim of a complete audiovisual playback review.

SHA-256: `9ef0eed0c12ca2686959b6e094d8e7db35162bc1f997054115d265fd998c9794`

Evidence: `edit-manifest.json`, `qa-results.json`, `safety-transcript.txt`, `transitions/transition-guard.json`, and exported frame checks in `qa/`.
