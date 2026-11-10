# Why Answers Vary v16

Review candidate: `Prompts/why-answers-vary-v16.mp4`, 1280×720, 30fps, 5,549 frames, **3:04.97**.

Built at David's request from the version-4 evaluation plan. The installed course video and lesson were not changed. No installation, commit, or publication is authorized by this build.

## Changes

- Version 4 supplies the opening, overview, full sampling example, temperature explanation, and exact closing lines.
- Removed the added summaries about every session changing, probability being a guide rather than a mathematical rule, mimicking human thought, and unchanged core understanding.
- Inserted complete existing narration beats explaining vocabulary-wide probabilities, the role of a changed token, the named apps, and the combined Other category. No generated voice or isolated-word splice was used.
- Replaced board recreations with the current canonical images. Highlights use fixed 4px outlines at 720p. The overview stays at full view because its complete cards are readable.
- Retained the two-chat phone illustrations, dog drawings, and branching animation. Removed the branching graphic's technical heading, preserving its reveals and continuations.
- Added the relevant weighted-draw animation from raw version 5 at **0:57.23–1:07.23**, under version 4's qualified 22/100 explanation. Its displayed 22/17/14/9/6/32 values match the lesson. This is a supporting animation, not a recreated course board.
- Temperature opens on the complete canonical board at **2:12.97**, then uses captures of the retained live component to reveal starting, low, and high probabilities. The reveals crossfade over 18 frames. All three columns and all six rows remain visible. It finishes by outlining the combined Other row and then Spot's comparison row.
- Used the canonical close, 48-frame hold, 150-frame push, and 17-frame settled hold. The final frame is the course close. Removed the Notebook outro and cleaned its corner mark from retained scenes.

The longest individual canonical-board run is **24 seconds**, the five-pick explanation. It stays together deliberately so the unchanged distribution, separate picks, and concluding observation remain available to compare. The weighted-draw animation breaks the larger sampling section. Temperature's individual reveal states run approximately 7–12 seconds before the next state or comparison changes.

## Audio grafts for listening

All times are output times. Source hashes, exact frame endpoints, donor gains, and source-to-output mappings are in `edit-manifest.json`. Contextual WAV excerpts are named `join-<output frame>.wav` in `../why-answers-vary-build-v15-2026-11-10/`; the corrected vocabulary join is `encoded-vocabulary-join.wav` in this folder.

| Output | Source | Retained teaching |
|---|---|---|
| 0:42.80–0:49.73 | Raw 3, 0:26.63–0:33.57 | “At this exact blank, the AI calculates a probability for every token in its vocabulary.” |
| 1:50.90–1:53.87 | Raw 5, 1:47.93–1:50.90 | “Choosing a different token shapes what comes next.” |
| 1:53.87–2:02.23 | Raw 3, 2:02.37–2:10.73 | A different token choice **can** send the remainder in a different direction. |
| 2:07.67–2:12.97 | Raw 6, 1:14.07–1:19.37 | Approved ChatGPT, Gemini, and Claude sentence, including “for you.” |
| 2:46.87–2:50.80 | Raw 3, 3:14.07–3:18.00 | “The other category comprises the vast remainder of the vocabulary.” |

Splice endpoints were selected in low-energy gaps. Donor gain adjustments range from approximately −0.10 to −0.52 dB. Five-millisecond transitions to source room tone protect endpoints. No midlesson pauses were inserted; two seconds of source-derived room tone extend the close. The assembled PCM has zero clipped samples and peaks at approximately −1.36 dBFS.

## Remaining issues

**This is a review build, not a shipping candidate with a KEEP verdict.**

1. At approximately **1:33.7–1:50.4**, the version-4 rationale still says choosing the most likely token makes answers repetitive and that alternatives make them feel creative. The approved lesson uses **can**. No clean complete donor with those qualifications was identified. This passage remains unchanged for review; a correct board does not repair its wording.
2. At approximately **0:29–0:34**, the techniques transition preserves the meaning but does not speak the required sentence exactly: “Two techniques help explain AI's choices: sampling and temperature.” No complete exact donor was identified.

Perceptual listening and uninterrupted audiovisual playback have **not** been performed. ASR and waveform measurements cannot certify pronunciation, voice continuity, natural cadence, or join quality. In particular, the base transcript's “tries” transcription uncertainty remains a listening check. All donor joins above need listening before shipping. Motion was inspected through sequentially decoded samples, not continuous playback with narration.

## Reproduction and checks

- Build: `.video-venv/bin/python scripts/video/build_why_answers_vary_v16.py`
- Capture source: `../why-answers-vary-build-v15-2026-11-10/capture.cjs`, using the existing temperature preview and video-only presentation CSS.
- Verification: `.video-venv/bin/python video-audit/why-answers-vary-build-v16-2026-11-10/verify.py`
- Encoded-file transcription and transition results are retained alongside this review. See `qa.json`, `transitions/transition-guard.md`, and `../why-answers-vary-build-v15-2026-11-10/transcripts/` for results.
- Protected file hashes cover raw sources, current lesson Markdown and prompt, canonical boards, and installed video. The build never writes `index.html`, which contains concurrent unrelated work.

No claim of complete audio or playback verification is made.

## Final encoded verification

- v16 removes the stray preceding word “choice” from the vocabulary donor at 0:42.80–0:43.47 using matched source room tone. The complete “At this exact blank…” sentence remains. This is an equal-duration repair; no pause or picture timing changed.
- The H.264 video stream is copied bit-for-bit from v15. The 24 inspected v15 transition strips therefore apply to the exact same encoded pictures in v16. The v16 container also passes the transition guard and complete decoding checks.
- Full v15 encoded narration was transcribed and read. The only changed v16 audio span is checked separately in `wording-check/encoded-vocabulary-join.txt`. The remaining wording issues above are still open.
- Source and installed-video protection checks pass. No perceptual listening or uninterrupted audiovisual playback was performed.
- The reproducible build uses the retained v15 candidate and original assembled PCM; v16 does not re-encode the picture or transcode the previously encoded AAC track.
