# Big Downside v6 — September 30, 2026

Narrow review candidate: `Prompts/big-downside-v6.mp4`, 10,114 frames at 30 fps, 5:37.13. User requested repairs to an audio glitch around “can point” at 0:38, another around 2:57, and a canonical board when the narration says “This chart…” around 1:16. This authorizes these repairs, not installation or publication.

## Changes

- **0:38.60–0:39.00:** Localized de-clicking around “can point.”
- **2:57.00–2:57.35:** Localized de-clicking around “fake call.”
- **1:15.40–1:17.77, frames [2262,2333):** Extend the first unmarked frame of the existing canonical **The Guardrail Challenge Gets Harder** board over the Notebook pipeline graphic. This makes “This chart…” refer to the board immediately. The current canonical JPG hash matches the original build's protected asset. Full-board framing; subsequent existing camera motion and the Changes Itself / Matches People / Surpasses People highlights remain unchanged. Total board span is now 23.37 seconds, covering the chart introduction and its explanation.

The source waveforms contain brief impulses at both reported locations; the automatic de-click detector identified samples there. Repairs use `adeclick=t=4:b=2:a=2` with surrounding context, then apply only the two specified windows with 5-ms edge blends. This removes detected impulsive noise without replacing words, adding pauses, or changing duration. The filter can alter consonant transients, so listening review remains necessary. An asynchronous question about the perceived glitch type was sent; no answer was available when these conservative patches were prepared.

The v5 callback wording correction, rebuilt voice-clone board, and historical-technology insert are retained. This is rebuilt from the hash-pinned finished source, not by re-encoding v5: `/private/tmp/big-downside-83ecf2e1-source.mp4`, SHA-256 `83ecf2e1a9de491260981d6048ce792657a478cfcfe6be13ad71d4314fc902d4`, Git revision `a81bf97a`.

## Verification

Encoded checks passed: 10,114 decoded frames, 30 fps, 337.133333 seconds. PCM outside the declared callback edit and two de-click windows matches the finished source exactly. The two de-click patches change 103 and 74 PCM samples respectively. Encoded audio correlation with the assembly is 0.999978. All 154 sampled unchanged visual frames remain within the expected additional encoding difference (maximum mean absolute pixel difference 2.784/255). Video and audio packet DTS increments are constant, with no timestamp jitter. The exact finished source and installed video hashes remain unchanged.

Transition guard passed all seven declared boundaries. All seven every-frame strips were visually inspected; the earlier board starts cleanly, joins the existing board motion without a flash, and prior repaired transitions remain clean. The new board opening was also inspected at full encoded resolution. Listening and continuous audiovisual playback have not been performed. Signal analysis and transcription cannot certify the audible result. Review the two repaired spots and the previous callback join around 3:00.

## Remaining scope limits

The four original rolls remain unavailable. Previously documented omitted spoken dates, Policy Puppetry tested-model scope, the missing goal-line article, and pacing-statement qualification are unresolved. No whole-file KEEP or shipping sign-off is claimed.

Build: `.video-venv/bin/python scripts/video/build_big_downside_v6.py` (imports the v5 configuration and v4 rendering implementation). QA: `.video-venv/bin/python scripts/video/qa_big_downside_v6.py`. `edit-manifest.json` records repair spans, source identity, hashes and filter parameters; before/after and encoded WAV excerpts support review.

No live video, course reference, tracker, or generation material changed. Not installed, committed, pushed, or published.

## Local release

User explicitly approved v6 with “ship it” after the review handoff. Installed and committed locally as `3d187436583b896a807432fa0e8572d73d8b23fd`. Cache key: `20260930ship1`. Runtime: 5:37.13; the existing rounded `6 min` pill remains accurate. Installed file and committed blob both match the approved candidate SHA-256 `048387bd5d140cccbb6e99bafc2c24c87ff2d30412f6005932675822755fd5d6`. Commit includes only the canonical video and its single course-reference update; unrelated working edits were preserved.

**Shipped locally; queued for batch deployment.** No push or deployment was performed. The owner’s shipping instruction is recorded as release approval; it does not imply that the assistant performed listening or whole-file audiovisual review. The previously documented source limitations remain on record.

Post-commit scratch cleanup removed 41 regenerable files (0.26 GB) from this lesson’s v4–v6 repair audit folders. Reports, manifests, transcripts, preview/transition images, source image, and candidate MP4s remain.
