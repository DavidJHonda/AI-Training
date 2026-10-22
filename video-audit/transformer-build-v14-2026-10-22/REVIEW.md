# Transformer v14 — built for review

2026-10-22. User approved the combined edit plan with **“Build it please.”**
Candidate: `Prompts/transformer-v14.mp4`, **3:58.767**, 7,163 frames at 30 fps,
1280 × 720, H.264/AAC. No installation, commit, push or tracker change.

[Play the candidate](http://127.0.0.1:8765/video-audit/transformer-build-v14-2026-10-22/review.html).

## Completed changes

The build uses the four approved whole-passage narration replacements from
`Prompts/transformer-2.mp4`, with the exact preview insert hashes verified before
assembly. No added pause, time-stretched speech or global audio normalization.
The opening/return examples, tired-CAT sequential sentence and parallel-processing
passage now match the current lesson. The useful pre-existing explanations and
closing are retained.

| Changed section | Output audio span | Visual treatment |
|---|---|---|
| Opening examples | 33.833–47.267 | Current context-problems board, full opening, complete-card camera moves and sentence/answer highlights |
| Sequential reading | 57.900–65.700 | Current earlier-AI board; highlights include TIRED and follow the complete narrated sentence |
| Parallel processing | 89.100–108.133 | Current Transformer-reading board; whole message then IT and earlier CAT |
| Return to examples | 156.667–175.100 | Current resolves-meaning board; full sentences, EMPTY clue and cat/milk referents |

The paper inside the brain scene is corrected to “The tired CAT sat on the mat.
IT soon fell asleep.” Only the paper interior is composited; original motion and
surrounding pixels remain. The full rainstorm sentence is spoken and appears on
the subsequent lesson boards. The built-in ImageGen tool created the corrected
paper; `scripts/video/assets/transformer-v14/README.md` records the exact prompt
and saved asset. Tracking covers all 238 frames with the existing validated
optical-flow algorithm. Its metrics are retained in `edit-manifest.json`.

## Boards and supporting scenes

| Board | Output span | Continuous duration / treatment |
|---|---|---|
| Two Problems Context Must Solve | 23.567–49.900 | Broken by the retained cat/IT/glass scene at 36.900–40.733; longest visit 13.333 s |
| How Earlier AI Read Text | 57.833–78.933 | 21.100 s; approved complete sentence walkthrough at full view |
| How a Transformer Reads a Sentence | 89.067–108.233 | 19.167 s; full view |
| How Context Changes the Numbers | 117.533–139.133 | 21.600 s; inherited treatment |
| How the Transformer Resolves Meaning | 151.100–179.433 | **28.333 s**, longest unbroken board; approved worked-example walkthrough and complete-card camera moves |
| How a Transformer Keeps Words in Order | 205.200–228.767 | 23.567 s; inherited treatment |
| Standard close | 228.767–238.767 | Retained motion and literal final frame |

Supporting scenes retained: opening laptop/tokens/bank/river/water (0–23.567),
cat/IT/glass (36.900–40.733 and 108.233–117.533), repaired brain/computer
(49.900–57.833), paper/architecture/ChatGPT-T (78.933–89.067), active-data bars
(139.133–151.100), brightness/sarcasm/placeholder IT (179.433–approximately
196.74), and ordered/scattered blocks (approximately 196.74–205.200).
No new decorative cutaways or stock imagery.

## Verification

- Full encoded file decoded sequentially: expected frame count, FPS and duration.
- Fresh small.en transcript of the **encoded candidate**, with word timestamps;
  complete transcript read. All four revised worked examples, revised full tired-cat
  sentence, parallel statement, attention/transformation definitions, fixed-weights
  distinction, word-order explanation and both closing lines are present.
- Prepared camera/highlight states and full-video five-second contact sheets
  inspected. Every declared boundary strip inspected. The three automatic
  transition flags at f1107, f1418 and f5253 are planned camera movement, not stale
  intermediate visuals. Raw flags are preserved in `transitions/`.
- Four-pixel rings are drawn after cropping by the shared rasterizer. The generic
  detector also counts baked-in token outlines and reports only solid color cores;
  its 2–4 px histogram is not a measurement of policy width on every added ring.
  `verification.json` includes rendered-state comparisons and contrast-based
  effective stroke measurements on added rings.
- All four donor inserts are byte-identical to their approved contextual previews
  before AAC encoding. Encoded audio decoded to finite samples.
- Review page loads and plays; all six section buttons successfully seek and play.
  Chrome reports no page errors. This is a playback-function test, not listening.
- Protected source videos, current lesson and all seven canonical JPGs remain
  unchanged. No website reference was changed.

**Remaining review:** no direct perceptual listening or continuous end-to-end
watching is claimed. Listen to the four voice joins and watch the full candidate
before shipping. No verified KEEP verdict or ship-checklist pass is claimed solely
from transcripts, measurements and stills. The candidate is ready for review.

## Source and reproducibility notes

Audio base is stable `Prompts/transformer-v13.mp4`. Visual base is retained
`Prompts/transformer-v12.mp4`, which has the same narration/timeline before the
paper-only v13 repair. Using it avoids an extra lossy generation. New boards render
directly from the current canonical JPGs. The raw roll and temporary v11 snapshot
no longer exist; unchanged visuals therefore receive an additional encode.
All source hashes, exact donor bounds, output mappings, board hashes, camera/ring
specifications, protected hashes and candidate hash are in `edit-manifest.json`.

Build: `.video-venv/bin/python scripts/video/build_transformer_v14.py`.
The script refuses to overwrite an existing candidate. Audit-only preparation:
`--prepare-only` (also refuses if that candidate already exists).

The approved comparison and full prior plan are in
`video-audit/transformer-context-review-2026-10-22/REVIEW.md`.

Final candidate SHA-256: `028b68601d2c247da71701703883785c98817ed9432be08277810bfad385e769`. All 157 prepared-state comparisons passed (maximum mean RGB error 3.164/255); median contrast-based added-ring width is 4.196 px after encoding. Encoded audio has 11,461,632 samples, including AAC packet padding beyond the planned 11,460,800 sample timeline. Browser duration remains 238.766667 s.
