# Layers v7 — owner review candidate

Built 2026-09-28 from the published Layers file, following the approved Layers repair plan. Not published.

Candidate: `Prompts/layers-v7.mp4` — 198.8 seconds, 5964 frames, 30 fps, 1280×720.
SHA-256: `90e4142e9e40c852d0e172685d2490d4cbdd383f4ad73366e9a2a5f4c2fc72db`.

## Repairs in output time

- 0:05.167–0:45.300: Show the full horse board, zoom to each complete column and pan First Read → More Reads → Meaning Clicks, then pull back for the takeaway. The active column retains its heading, text, and illustration. Continuous board exposure remains 40.133 seconds across all camera moves: the deliberate exception in the approved plan.
- 1:04.100–1:42.633: Keep the canonical numbers board; improve diagram, number-card and takeaway highlights. Reuse the original line-of-layers illustration at 1:15.300–1:20.300, returning before the starting-number explanation. Continuous board runs are 11.2 and 22.333 seconds.
- 1:48.000–1:52.100: Add the complete cat sentence before “At the start…”, using the approved published Vector Space donor (source 3:21.233–3:25.333). Highlight only the sentence while it is read, then only the active stage. The insert adds 4.1 seconds; original narration remains.
- 1:48.000–2:32.467: Keep all five IT/CAT stages visible. Reuse the line-of-layers illustration at 2:15.200–2:22.633. Repeat is highlighted briefly before the drawing. Continuous board runs are 27.2 seconds, including the added reading, and 9.833 seconds after the drawing.
- 2:32.467–3:18.800: Preserve the existing late illustrations and standard closing sequence.
- Rebuilt highlights use fixed 4 px strokes at 720p, applied after camera transforms.

## Verification

- Decoded all 5964 frames. Compared 2270 original-graphics/close frames, 373 reused-drawing frames, and 355 rendered-board samples against their expected sources/references. Maximum mean absolute pixel difference: 3.341/255 after encoding.
- Inspected all four prepared contact sheets, all six encoded contact sheets, and all eight transition guard sheets. Active horse columns are complete; board cards and highlights fit. No unexpected stale-frame flash was observed in the sampled boundaries.
- Automated transition guard passed 21 of 22 boundaries. The flag at frame 302 (0:10.067) is expected horse-board zoom motion; manually inspected and cleared. The original automated result remains retained.
- Measured 239 encoded ring sides: median effective width 4.198 px; range 4.073–4.467 px including antialiasing and compression.
- Original PCM is exact outside the 5 ms join ramps. Donor PCM matches the level-adjusted donor outside those ramps. AAC correlation to edited PCM is 0.999971; SNR 42.30 dB.
- Donor active-speech level is within 0.243 dB of neighboring narration after gain and limiting. Join quiet spans are 0.241 and 0.327 seconds. No extra pause was inserted.
- ASR confirms the complete new sentence between the original introduction and “At the start…”. The encoded listening excerpt is `join-review.mp3` (output 1:42–1:58).
- Published Layers source, donor video, lesson text, prompt, canonical board images, and index remained unchanged.

## Checks not performed

Actual listening and voice-identity/naturalness audition, continuous real-time playback, and mobile/public-player playback were not performed. Signal and transcript checks do not establish a seamless voice match. Owner should review 1:42–1:56, especially 1:48–1:52, before shipping. No publication or deployment was attempted.
