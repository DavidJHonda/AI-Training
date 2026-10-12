# Vector Space v19 — built review candidate

Approved 2026-10-10: “Build uit.” Candidate: `Prompts/vector-space-v19.mp4`.
Runtime: **4:16.43**, 7,693 frames, 1280×720, 30 fps, AAC mono 48 kHz.
SHA-256: `d9a5fb6a023340b28f75c0f22e0f3232419fcc42b7a0fe82d7d6ae572ab64704`.

## Implemented

Replaced live 212.333333–217.466667 with roll 11 audio from 220.766667–225.700000. The donor occupies output **212.333333–217.266667**. Its complete revised example is: “The tired cat sat on the mat during the May rainstorm. It soon fell asleep.” Donor gain is −0.39645 dB, matched using nearby active-speech RMS. Five-millisecond seam ramps occur inside quiet gaps; no speech stretching or added pauses.

Changed the sentence card at **206.266667–217.800000**. Preserved its typography, composition, and purple CAT/IT emphasis. All subsequent picture and audio cues shift earlier by six frames (0.2 seconds).

Reconstructed the approved v18 pictures from its native render code and original sources, avoiding re-encoding previously compressed video as the picture source. The live decoded audio supplies all unaffected narration, with one AAC encode after the splice. The canonical context board retains its unmarked full-view opening, framing, and starting-numbers → layers → updated-numbers → IT → conclusion highlights. Its continuous run remains 29.1 seconds, the existing approved treatment. No new supporting illustrations were introduced. Earlier supporting scenes and the close are preserved.

## Verification

- All 7,693 frames decoded; frame count and duration match the plan.
- All **7,347 frames outside the sentence card** compared against corresponding live frames at 160×90: maximum mean absolute pixel error 0.0364/255. No unintended reordered or changed scenes detected.
- Revised sentence card checked in six encoded frames, including both audio joins and the first/last card frames. Correct wording and unclipped layout visually confirmed. RGB-to-YUV/OpenCV conversion causes an approximately three-code-value background difference from the source PNG; initial strict RGB comparison was adjusted to allow this measured conversion error after visual inspection.
- Transition guard passed **all 10 affected boundaries**; every-frame strips inspected, with no leaked intermediate scenes. Canonical board opens unmarked; preserved focus states and final close inspected in the contact sheet. Full-resolution board opening and starting-number ring also inspected.
- Unaffected assembled PCM is sample-identical before AAC encoding. Five encoded audio comparisons covering earlier and later sections have correlations above 0.99998. Encoded audio peak is 0.86055; no clipping detected.
- ASR of the encoded 3:30–3:48 passage confirms the complete revised example and continuation into “On its own…” and the connection-to-CAT explanation. See `transcripts/v19-asr-check.txt`; timestamps there are relative to 210 seconds.
- Cut points measured before rendering in quiet gaps: approximately −63 and −60 dBFS on the base, −66 and −80 dBFS on the donor. Encoded silence detection is retained in `v19-silence.log`.
- Protected source/page/board hashes unchanged. No live installation, commit, push, or tracker change.

## Listening and scope limits

Direct listening has **not** been completed. ASR, waveforms, and correlations do not certify the voice match or subjective pacing. Listen through **3:26–3:50**, especially the joins at **3:32.33 and 3:37.27**, in `v19-review.html`. `v19-context-review.wav` contains that encoded excerpt. Full-file real-time watch/listen and broader shipping checks have not been performed; this is a narrow review candidate, not a shipping verdict.

Reproducibility: `build_v19.py`, `v19-manifest.json`, `verify_v19.py`, and `v19-verification.json`. Transition strips are in `v19-transitions/`; keyframes/contact sheet are in `v19-inspection/`.
