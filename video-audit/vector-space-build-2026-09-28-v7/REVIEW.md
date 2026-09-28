# Vector Space v7 — review candidate

Built September 28, 2026, following approval of the reroll evaluation. **3:42.83, 1280 × 720, 30 fps, 6,685 frames.**

[Play the candidate](/Users/davidobrien/Developer/AI-Training/Prompts/vector-space-v7.mp4)

Roll 3 supplies the main explanation. Roll 1 supplies Mountain View and New York coordinates, all three complete drink vectors, the mystery drink ratings, and the complete contextual-update explanation. The canonical lesson boards and two-line close are preserved. New paper-style opening and return diagrams use only the lesson's illustrative values: .12, −.34 and .41, .06.

The contextual passage uses the approved complete-sentence fallback to avoid the word “physical.” The overclaim about perfectly preserving meaning is replaced by Roll 3's complete sentence, “The relationships between the numbers matter too.” This returns to the opening question. No cuts inside words remain in the final edit. V6 is superseded and retained unchanged.

## Review focus

The candidate is built and technically checked, but **direct listening and continuous real-time playback were not performed**. ASR, signal checks, and still-frame review cannot certify voice continuity or cadence. Listen especially at the Roll 1/Roll 3 joins:

- [Cities, 0:38–0:55](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v7/audition/cities.mp4)
- [Drink values and mystery example, 1:58–2:33](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v7/audition/drink-values-and-mystery.mp4)
- [Context and ending, 3:03–end](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v7/audition/context-and-ending.mp4)

The complete transcript from the encoded candidate is in [transcript.txt](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v7/transcript.txt). It confirms the intended numeric examples and ending; it is machine transcription, not a certified verbatim transcript.

## Pacing exceptions retained from the approved plan

The drink sequence remains a continuous 94.4-second run of canonical boards, from 1:09.53 to 2:43.93. Its changing highlights follow the narration; no filler is inserted to interrupt the explanation. Four individual boards exceed 20 seconds:

| Board | Start | Duration |
| --- | --- | --- |
| Seven drink dimensions | 1:09.53 | 33.07 s |
| Drink neighborhoods and spoken vectors | 1:42.60 | 34.33 s |
| Mystery drink comparison | 2:16.93 | 27.00 s |
| Context changes IT | 3:06.90 | 21.53 s |

All six explanatory boards stay in complete view, with at least two seconds before the first highlight. This prioritizes reading the full board and the approved spoken detail. The two narration paraphrases identified in the comparison remain accepted semantic equivalents rather than exact required wording. The maps are teaching schematics, not literal projections of a model's learned dimensions.

## Validation

- Full sequential decode: 6,685 frames at 30 fps, all 1280 × 720; no decode failure.
- Transition guard: 19 boundaries, zero flagged short visual islands. Every-frame strips covering ±12 frames at all boundaries were visually inspected; no stray or stale frames were observed.
- Fresh eight-second contact sheets, board highlight states, changed ending, and literal final frame inspected. The final frame is the canonical two-line close.
- All 30 sampled native ring states measure 4 opaque pixels across each straight side. Encoded YUV color thresholds can read thinner because of chroma filtering; the native raster measurement is recorded in `ring-native-verification.json`.
- Canonical close: 48-frame initial hold, 150-frame push to 1.2×, 42-frame settled hold.
- Fresh full-file ASR confirms Dallas 33° N / 97° W, Mountain View 37° N / 122° W, New York 41° N / 74° W; Coke 9/1/10/2/3/8/1; Pepsi 9/1/10/2/3/8/10; coffee 1/9/0/9/8/10/0; mystery 9/1/10/2/3/8/9; citrus gaps 1 and 8; and the intended complete-sentence ending.
- Roll 1 gain matched to Roll 3 at −0.8325 dB. Four-millisecond ramps at sentence boundaries; zero added pauses. Encoded audio peak 27,960 on the 16-bit scale (about −1.38 dBFS), no sample clipping; decoded AAC/reference SNR 44.72 dB. AAC decode includes 704 trailing padding samples.
- Protected source videos, live video, lesson Markdown, and all seven canonical JPGs retain their pre-build hashes.

Evidence: `qa.json`, `edit-manifest.json`, `guard/transition-guard.json`, `guard-sheet-*.jpg`, `encoded-sheet-*.jpg`, `encoded/`, `silence-detect.txt`, and `transcript.json` in this directory. The manifest records exact source/output frame mappings, highlight geometry, gain, and source hashes.

## Artifact identity and build

Candidate SHA-256: `c6a02f73dfc431965fae48f4cc608599b8affe691dc1a9b0adf0e03a62d6be69`

| Source | SHA-256 |
| --- | --- |
| Roll 1 | `3df4bc45f7b01223bfd7ed8892c0ddae6f68549482f705c3834a11c6984a56b5` |
| Roll 3 | `6540e2fa2c8a67753efecaaf7d7a9612e82c812209141f44893ca72acf29e198` |
| Local live | `4873fac38f54ff14ebaff06b0787a8922e9e15bb99712b0332d767ad41f5b563` |

Build entry point: `scripts/video/build_vector_space_v7.py`, using the shared composition in `build_vector_space_v6.py`. It refuses to overwrite the candidate and reuses the v6 audit's clean donor excerpts. Validation command from the repository root:

```sh
.video-venv/bin/python scripts/video/qa_vector_space_v6.py --version 7
```

Review candidate only. No publication, live asset replacement, lesson/index update, or commit was performed.
