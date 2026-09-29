# Embeddings — current site-referenced video evaluation

Reviewed September 29, 2026. Evaluation only; no video, lesson, or site changes.

**Recommendation: retain the narration; make targeted visual repairs.** The transcript supports a provisional KEEP for teaching. This is not a completed perceptual review or a new shipping certification: no end-to-end listening or motion playback was available.

## Exact source and evidence

- `index.html:1123` references `course-assets/embeddings/embeddings.mp4?v=20260927ship1`.
- Duration 4:26.567; sequentially decoded all 7,997 frames, 30 fps, 1280 × 720.
- Current file SHA-256: `14d9ba4b66ee5a698eaa5845e7ec08b931d5de33f93a5d798c92a486637dca94`, identical to the September 27 v7 candidate and shipping receipt.
- Read the full current lesson in `index.html`, upload Markdown, current Narration Review and Edit Spec, and the prior v7 record.
- Read the complete timestamped ASR transcript from that identical candidate; copied it to `transcript.txt`. ASR is evidence of wording, not a listening pass.
- Fresh sequential frame samples every four seconds span the entire file in `sheet-00.jpg` through `sheet-05.jpg`. Inspected additional full-resolution frames, including the literal final frame. All five current canonical board assets match the hashes used in the shipped build.
- The browser security policy blocked opening the existing local-file page. This review establishes the local site reference and exact local media identity, not the currently deployed public bytes or live-player behavior.
- No direct audio audition or continuous motion viewing occurred. Pronunciation, cadence, fades, brief between-sample artifacts, and the two audio joins remain unverified. Prior signal/transition checks are recorded evidence for the identical file, not newly performed perceptual checks.

## Teaching evaluation

LESSON: embeddings. CANDIDATE: the file above. VERDICT: **provisional KEEP from transcript; listening still outstanding**.

| Essential teaching point | Assessment | Evidence on output timeline |
|---|---|---|
| Text becomes tokens with unique IDs; ID is identification rather than meaning | RICH | 0:00–0:17.88; distinction explicitly explained |
| Student-ID analogy and fries example | RICH | 0:18.50–0:33.96; identifies students but does not describe personality or behavior |
| Bridge from an ID to numerical characteristics | TAUGHT | 0:34.76–0:48.26; an ID alone is insufficient to process meaning |
| Six taste dimensions and the 0–10 scale | RICH | 0:49.20–1:03.88; all six traits named and scale explained |
| Ordered drink profiles | RICH | 1:04.46–1:25.78; Coke's complete 9, 1, 10, 2, 3, 8 row read; coffee described as different; fixed positional meanings explained |
| Identify Coke from Sweet 9, Bitter 1, Fizz 10 | RICH | 1:26.50–1:35.18; question and answer both spoken |
| Vector, dimension, value | TAUGHT | 1:35.98–1:46.10; row, position, and number distinguished |
| Matching Coke/Pepsi profiles cannot distinguish them | RICH | 1:46.68–2:02.40; reason for adding information is explicit |
| Seventh Citrus dimension separates them | RICH | 2:03.08–2:16.72; Pepsi 10, Coke 1, coffee 0, followed by the takeaway |
| Bridge to AI; embedding is a row of numbers | TAUGHT | 2:23.64–2:34.80 |
| Every vocabulary token gets a row; typically thousands of dimensions | TAUGHT | 2:35.26–2:48.14 |
| Learned values rather than human scores; signed decimal values | TAUGHT | 2:48.98–2:58.82 |
| Learned usage patterns, no human semantic dimension labels | TAUGHT | 2:59.40–3:17.04; comparison and overall purpose explicitly explained |
| Cat ID 4719 selects a row in the embedding table | RICH | 3:17.74–3:36.36; lookup and neighboring tokens explained |
| Table columns versus dimensions; learned value/parameter versus whole embedding | TAUGHT | 3:36.84–3:58.24; d1–dn, 0.45, parameter and complete row distinguished |
| Subword pieces also get embeddings | RICH | 3:58.76–4:13.98; unbelievable → un, belie, vable, each with its own row |
| Required two-line close | TAUGHT / MET | 4:14.92–4:20.98; both lines verbatim |

The arc works: identification is insufficient → describe drinks with numbers → add a distinguishing characteristic → transfer to learned token representations → show lookup → include word pieces. No essential spoken bridge is missing. Reading every coffee value or every decimal in cat's row is unnecessary to teach the current page's point; the relevant comparisons and definitions are spoken.

HARD REQUIREMENTS: vector, dimension, value, embedding and parameter are explained; both closing lines are present. The removed “individual syllables” phrase is absent. ERRORS: no material narration error established from the transcript. SOURCE_QA: no blocking contradiction found in the current lesson's intended illustrative explanation.

ADDITIONS: the generalized dimension example around 2:17 and the human-rating/AI-vector illustration around 3:13 support the subject. Their visuals need separate assessment below. “Complex decimals” at 2:54 is loose wording, but does not by itself assert mathematical complex-valued embeddings. Not a reason to reroll.

The 2:17 statement about adding dimensions is an analogy about representational capacity, not evidence that a deployed model dynamically appends dimensions. The subsequent learned-values comparison keeps that interpretation reasonable. If revising teaching later, “more dimensions give room to capture more differences” is a useful precision improvement. Actual embedding tables have a configured dimensionality and learned weight matrix; see [PyTorch Embedding documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html). No narration edit is proposed on this basis.

REPAIR PLAN (narration): none. No donor search or graft needed based on established teaching coverage. LISTENING: unheard, including joins at 1:46.50 and 4:10.86. No new pauses proposed without listening evidence.

## Findings in priority order

1. **Content correction, 2:17.20–2:23.43: wrong values circled.** “Resolving Ambiguity with Dimensions” shows rows whose first six values match. It circles the sixth value, 0.55, in both rows while the seventh values are 0.89 and −0.74. The lower diagram correctly names Dimension 7, making the emphasis internally inconsistent. Confirmed at full resolution at 2:19 and 2:21 (`full-139.jpg`, `full-141.jpg`). Preserve the explanation and diagram; remove the two incorrect circles and emphasize the last values. Inspect the correction throughout the scene's animation before accepting it. This is a visual error, not a failed narration point.
2. **Framing repair, comparison board 2:23.43–3:12.37.** During the dive/pan the board title and then the column headings leave the frame; at 3:04 even “Your Taste Test” is visibly clipped (`full-184.jpg`). This loses useful comparison context and conflicts with complete-card framing. Reduce the crop so both complete comparison columns, headings, and bottom content remain visible. Keep the row emphasis. The initial full view is intact.
3. **Engagement opportunity: extended board holds.** Meaning in a Row holds 42.17 seconds and New Dimension 30.70 seconds consecutively: 72.87 seconds without a supporting scene. Taste/AI holds 48.93 seconds; Inside a Real Model 41.03 seconds. These are real explanatory walks, not dead silence, and were explicitly retained in the approved v7 plan. Nevertheless, useful cutaways would improve visual variety. Treat this as a separately scoped enhancement, not a retroactive claim that those approved holds alone invalidate the video. Do not add filler or cut essential narration to hit an arbitrary duration.
4. **Minor graphic cleanup, about 0:49–1:04:** the taste-test scale has a second orphan “(High)” at the far right (`full-54.jpg`). Remove the stray label while preserving the useful drinks/traits illustration. Lower priority than findings 1–2.

The full-resolution Inside a Real Model board is readable; preserve its approved full-view treatment rather than zooming solely because the contact-sheet thumbnail is small. Student-ID framing and the canonical final closing card are appropriate in sampled frames. No basis for a full reroll was found.

## Proposed visual-only plan

This is a reviewable proposal, not an executed or approved new build. Preserve narration, timing and existing pauses. Full-motion review is needed before implementing overlays on animated scenes.

| Board (exact title) | Highlighting sequence | Camera | On screen / breaks | Recommendation |
|---|---|---|---|---|
| An ID Identifies You. It Doesn’t Describe You. | Unmarked illustration, then bottom takeaway as spoken | Full view | 0:18.37–0:34.63; 16.27 s | Preserve |
| Meaning Becomes an Ordered Row of Numbers | Coke row → coffee row → positional-meaning takeaway → Coke's identifying values → full vector → dimension headings → value | Full board | 1:04.33–1:46.50; 42.17 s | Preserve for narrow repair. Optional future cutaway at the vector/dimension/value definitions would be useful only with a purpose-built explanatory scene; no donor approved or selected |
| One New Dimension Separates Similar Meanings | Pepsi → matching six values → Citrus → Pepsi 10 / Coke 1 / coffee 0 → takeaway | Full board | 1:46.50–2:17.20; 30.70 s; existing supporting scene follows | Preserve board; correct following scene's circles at 2:17.20–2:23.43 |
| From Taste Ratings to AI Embeddings | What gets a row → dimensions per row → values → usage patterns/labels → takeaway | Full view, then only a restrained crop that retains complete columns and headings | 2:23.43–3:12.37; 48.93 s; existing human-rating comparison follows | Repair crop. Optional future use of the 3:12.37–3:17.57 supporting diagram within this explanation requires motion/timing review; no additional cutaway assumed |
| Inside a Real Model | Token → ID → other rows → identifying columns → dimension columns → 0.45 → whole numerical row | Preserve full view | 3:17.57–3:58.60; 41.03 s | Preserve approved framing; the actual lookup relationships matter more than decorative movement |
| Closing message | No added rings | Preserve canonical close and existing motion | 4:14.50–4:26.57; 12.07 s | Literal last frame checked; motion itself not freshly certified |

Retain the opening token/ID sequence (0:00–0:18), the student-ID and numerical-row bridge (0:34.63–about 0:49), taste-test setup (about 0:49–1:04.33, with stray-label cleanup), the corrected dimension-separation scene (2:17.20–2:23.43), the human/AI numerical-profile comparison (3:12.37–3:17.57), and the subword-to-embedding scene (3:58.60–4:14.50). These illustrate identification, quantified traits, distinctions and lookup rather than merely decorating the narration. Retention judgments are based on sampled sequences and transcript alignment; motion quality remains provisional.

No requested work was left awaiting build approval: the request was evaluation. The report, transcript and fresh frame evidence complete the accessible analysis. A full viewing/listening pass remains necessary for a definitive audiovisual verdict.
