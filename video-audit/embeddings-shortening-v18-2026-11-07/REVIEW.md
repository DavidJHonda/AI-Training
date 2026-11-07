# Embeddings v18: requested shortening

Scope: remove badge-number enumeration, coffee and Coke score readouts, and the entire embedding-table walkthrough. Build authorization: user requested these four changes. This is a review candidate, not an installed release.

Runtime: 3:47.93 → 3:10.73; 37.2 seconds removed.

## Cuts

| Passage | Installed v16 interval | New join | Result |
|---|---|---|---|
| badge-numbers | 0:23.13–0:28.17 | 0:23.13 | If four students are wearing badges, those numbers tell us who is who. |
| coffee-readout | 1:07.57–1:15.67 | 1:02.53 | Let’s put those ratings in the table. Next, you taste Coke, and rate it on the same six characteristics. |
| coke-readout | 1:19.87–1:28.27 | 1:06.73 | …the same six characteristics. Which drink scores nine for sweet, one for bitter, and ten for fizz? |
| model-table | 3:10.57–3:26.23 | 2:49.03 | Both use a row of numbers to describe something. Even word fragments get their own embeddings. |

## Picture treatment

| Board | Treatment | Timing |
|---|---|---|
| An ID Identifies You. It Doesn’t Describe You. | Preserve full, unmarked illustration; the badge values stay visible. | Remove the spoken enumeration only. |
| Coffee ratings | Reveal the complete coffee row during “Let’s put those ratings in the table.” No individual value outlines. | 2.1 seconds before Coke appears. |
| Coffee and Coke ratings | Reveal Coke during “Next, you taste Coke”; preserve the table and later recognition-question highlights. | 3.9 seconds of the introductory sentence, then the question. |
| From Taste Ratings to AI Embeddings | Preserve paired-row highlights and takeaway. | Cut from its complete takeaway directly to word pieces. |
| Inside a Real Model | Remove the entire illustration and its narration. | 0 seconds in candidate. |

No new narration or pauses. Use the existing source gaps with five-millisecond edge fades. Preserve the v16 timing and camera treatment elsewhere. Rebuild from pristine embeddings-2.mp4, using retained v16 captures and word-piece artwork.

## Badge boundary repair

The first draft cut at source 22.900s and clipped the final syllable of “badges.” V18 cuts at 23.133s, after the final fricative and before “numbered.” The 5ms spectral profile, rather than the original transcript word timestamps, determines the boundary. Probe evidence is retained in ../embeddings-shortening-v17-2026-11-07/badge-probes.json.

## Review limits

Direct listening and continuous-motion review remain outstanding. The pre-existing word-piece limitation remains: un / belie / vable are shown but not individually spoken. The installed course video and generation source documents are unchanged.

## Completed verification

- All 5,722 encoded frames decode at 1280 × 720, 30 fps.
- 121 sampled frames match the intended render. Unchanged visuals match v16 with maximum mean pixel difference 0.044 on the 0–255 scale.
- All 27 declared boundaries pass transition_guard; badge, drink reveal, and table-removal strips were visually inspected.
- Encoded audio correlations exceed 0.999 across sampled windows and all splice neighborhoods.
- Transcription of each encoded join preserves the intended words, including the full word “badges.”
- Browser check passed: video duration, four seek controls, four playable excerpt URLs, mobile fit, and no runtime errors.
- Source, installed v16 video, on-page lesson, and Markdown source hashes remain unchanged by the video build.

## Local release

Approved by the user with “ship it.” Installed at course-assets/embeddings/embeddings.mp4 with cache key 20261107ship18 and displayed runtime 3 min. Local commit 1728d93ea4d0d2943265c91920b1f5478028747d. Full asset integrity check and local served-file hash verification pass. Shipped locally; queued for batch deployment. No push or deployment performed. Direct listening remains unperformed by the agent, as disclosed before approval. Regenerable WAV scratch was removed; review excerpts remain as M4A.
