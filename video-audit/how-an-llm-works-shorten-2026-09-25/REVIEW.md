# How an LLM Works — shortened candidate (10 sentence cuts) — 2026-09-25

Candidate: `how-an-llm-works-shortened.mp4`, 9,114 frames / 5:03.80 (was 11,488 / 6:22.93; −79.13 s).
SHA-256 `cee726d43be1f24e7a330daedbac366d3aa0ae0cdc06e637180068e8df09099e`. Not shipped; live file untouched.
Source backup: `archive/how-an-llm-works/how-an-llm-works-before-shorten-20260925.mp4` (sha 5f3f2674…, = shipped v13).
Build: `.video-venv/bin/python scripts/video/cut_how_an_llm_works_shorten.py` (refuses to overwrite).

Checks done:
- Full decode 9,114 frames = expected.
- Re-transcribed output (`transcript-shortened.txt`, faster-whisper medium.en): all ten sentences absent, every retained sentence complete, no clipped words.
- Every audio join sits inside a measured pause; 200 ms RMS across each join −60 to −72 dBFS.
- Picture joins (`joins/output-joins-*.jpg`): clean single-frame cuts, no flash frames. Cuts 4 and 10 remove exactly the numerical-network and training-vs-answering drawings. Cut 5 shows Same Word. Different Odds. in full view ~1.2 s before the left-card zoom.

Not done: human listening of the ten joins (especially 1, 5, 10), cache key / duration pill / manifest updates.

## v2 (after owner review)
- `how-an-llm-works-shortened-v2.mp4`, sha 45b48a41a26a…; same length and audio join points as v1.
- Owner: banner highlighted at 3:53 but not spoken. Its highlight began at source frame 8475 for the deleted cut-8 sentence. Output frames 6995–7011 now hold source frame 8474 (jelly rings only). Only those 17 frames differ from v1.
- Owner: audio glitch at 0:46 (cut 1). Signal check: output matches the intended splice sample-for-sample, and there is no click or level step in the -66 dBFS pause. The cause is not yet identified and the join is unchanged.

## Shipped 2026-09-25
Shipped v2 on David's call. It's now `course-assets/how-an-llm-works/how-an-llm-works.mp4` (sha256 45b48a41a26a…, 18,201,294 bytes, 9,114 frames / 5:03.80).
Cache key 20260917ship1 → 20260925ship13, pill 6 → 5 min, manifest `video_assets` sha/bytes refreshed.
Pre-shorten v13 is kept at `archive/how-an-llm-works/how-an-llm-works-before-shorten-20260925.mp4`.
The 0:46 join was shipped unchanged. The owner's glitch report there was not resolved. Not committed or deployed.
