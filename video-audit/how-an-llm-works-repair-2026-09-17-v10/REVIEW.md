# How an LLM Works — joined two-part v10

Recommendation: **review this candidate; no new reroll is recommended from the available content evidence.** The approved REPAIR has been built. It is not certified ready to ship: literal end-to-end watching/listening and audition of the audio joins remain outstanding.

## Candidate and scope

- Candidate: [how-an-llm-works-v10.mp4](../../Prompts/how-an-llm-works-v10.mp4)
- Duration: **6:22.933**, 11,488 decoded frames, **1280×720, 30 fps**. H.264 video, AAC mono audio at 48 kHz, approximately 24 MB.
- SHA-256: `ae9ebe17821566021033b76967935d98e34f972036eb64ece29dd019d07619aa`.
- Base narration: learns-1 followed by answers-2. Part 2 starts at **2:53.200**.
- Full production candidate from pristine source rolls, using the approved two-addition plan and continuous-probability-comparison exception. No overview-map callback, intermediate close, or added teaching pauses.
- Current `index.html`, all lesson Markdown, canonical JPGs, and live MP4 are unchanged, verified by hashes. Previous candidates and raw rolls remain intact. Nothing was deployed. The tracker was not accessed or updated.

The [edit manifest](edit-manifest.json) contains source/asset hashes, exact half-open frame intervals, camera paths, ring geometry and source/output mappings. Board timing fields named `src_in`, `src_out`, and `spoken_onset_source_frame` are **output frame coordinates** in this isolated builder, not raw-roll coordinates. The audio timeline and borrowed-picture rows contain their own raw source coordinates.

## Narration and joins

The complete encoded-file [timestamped transcript](finished-review/how-an-llm-works-v10/transcript.txt) was reviewed against the current lesson and the approved comparison. Both additions are complete in the final transcript. The training example, target/guess/correction mechanism, repetition, patterns-during-training distinction, token qualification, both full probability examples, non-forced choice, context comparison, jelly → for → lunch sequence, and final two closing lines remain present. The omitted overview is intentional. No other speech was cut or reordered.

| Addition | Source selection, frame-rounded | Output | Complete words |
|---|---|---|---|
| Expand LLM | learns-2 0:19.667–0:24.167, frames [590,725) | **0:17.567–0:22.067** | “Under the hood, a large language model, or LLM, does the work.” |
| Qualify percentages | answers-1 1:00.667–1:09.167, frames [1820,2075) | **3:41.600–3:50.100** | “Keep in mind, these percentages are illustrative examples to show how the concept works. They aren't fixed mathematical constants shared by every AI model.” |

Learns-1 is retained through source 2:48.700; its remaining silent tail is omitted. Answers-2 is retained through 3:18.167, before the Notebook outro. Its final speech is intact. The sole close then finishes its prescribed settle.

All sources were level-matched using constant gain, with common peak headroom; no dynamic normalization was applied. Five narration joins and the final room-tone extension use 5 ms ramps. Visual cuts do not touch the audio. Outside those handles, the PCM master is sample-exact to the selected source PCM after the declared constant gains: zero sample error across all six retained spans. The delivery audio is necessarily AAC-encoded once. Final measured loudness is **−20.05 LUFS**, true peak **−2.35 dBTP**.

Measured final-file low-level gaps at −35 dB, minimum 0.12 s:

| Join | Actual output low-level interval | Total gap |
|---|---|---:|
| Full-term donor entrance | 0:17.247–0:17.812 | 0.565 s |
| Full-term donor exit | 0:21.735–0:22.282 | 0.547 s |
| Learning → answering | 2:52.929–2:53.502 | 0.572 s |
| Percentage donor entrance | 3:41.254–3:41.875 | 0.621 s |
| Percentage donor exit | 3:49.840–3:50.322 | 0.482 s |
| Final close tail | 6:19.673–6:22.933 | 3.261 s |

The small differences from the planning estimates reflect frame rounding, final gain, and threshold sensitivity, not newly inserted pauses. The only added duration beyond the two donors is 92 frames of matched room tone at the final close. No automatic one-second pauses were added.

**Listening required:** review 0:13–0:28, 2:46–3:05, and 3:37–3:55, then the complete 6:23 video. Voice identity, cadence, pronunciation, perceived pacing, clicks, and noise-floor continuity are not certified by ASR or waveform checks. Transcript “4” is the recognizer's spelling of the homophone “for”; the opening “end” and the wording around “patterns it learned” are also ASR uncertainties, not established spoken errors. The source word-timestamp records and previous secondary checks are retained.

## Visual and production treatment

All boards use the exact current lesson JPGs, not Notebook recreations. Compact boards remain still at full view. The dense probability board uses full view → complete left card → complete right card → full comparison. Its rings follow whole card → prompt → complete probability table, with paired whole-card outlines for the explicit 41%/2% comparison. The camera crosses to the right during the new-context introduction and pulls back before the banner is highlighted. No active ring is cropped during those moves; geometry was checked at every rendered board frame.

LLM highlights: app/engine banner, unmarked full-term donor, Large, Language, Model. Training: complete Read, Guess, Check, Adjust sections. Patterns: familiar-pattern card, then broader phrase-pattern card; unmarked for the extended explanation. Prediction: complete first, second, third cards, then full-width takeaway. All rings are post-crop 5 px outlines. Board arrivals are unmarked full views; the shortest item-led opening is 3.033 s for prediction. The standard close begins at **6:13.333**, holds 48 frames, pushes for 150 frames to 1.2×, then settles for 90 frames. It is the literal final frame.

**Longest continuous board run: 90.633 s, 3:19.400–4:50.033**, the approved probability-comparison exception. This is longer than the preliminary ~84 s estimate because the canonical comparison also covers the source's “SHAPING THE ODDS” title. No extra narration or pause was added. A reuse of the approved prediction-loop drawing under the phone analogy separates this comparison from the next board. The longest learning board run is 56.300 s.

Retained/retimed Notebook pictures (audio remains on the independent narration timeline):

| Output | Picture source | Treatment |
|---|---|---|
| 0:00.000–0:08.467 | learns-1 0:00.000–0:08.467 | Peanut-butter opening |
| 0:46.667–0:52.100 | learns-1 0:43.000–0:48.433 | Established training loop; skip blank animation opening |
| 1:41.500–1:50.500 | learns-1 0:43.000–0:50.733 | Repeat loop; final clean state holds 1.267 s |
| 2:46.800–2:53.200 | learns-2 2:57.000–3:01.433 | Internal patterns/application handoff; final state holds 1.967 s |
| 3:06.000–3:10.233 | answers-1 0:19.000–0:23.233 | Incremental pieces |
| 3:10.233–3:19.400 | answers-1 0:24.000–0:28.533 | Whole words → fragments; holds 4.633 s before fabricated IDs appear |
| 4:50.033–5:01.300 | answers-2 2:40.000–2:51.267 | Predict/select/update loop under phone analogy and loop introduction |
| 5:39.567–5:58.867 | answers-2 2:40.000–2:55.033 | Same loop for paragraph generation; holds clean state 4.267 s before “FLUID THOUGHT EMERGENCE” |
| 5:58.867–6:13.333 | answers-2 2:57.167–3:11.633 | Training versus answering drawings |

The last answering diagram animates the selected word back into context; it is a feedback illustration, not another worked numerical example. Schematic weights and small labels remain in the handoff/loop drawings; they are not required for understanding the narration. No standalone stock-photo span was identified in the inspected kept scenes. Engine corner marks were cleaned on 2,440 frames by same-frame paper cloning and 192 by glyph inpainting; no frames were declined. Generated token IDs, the “fluid thought” label, and Notebook end cards are excluded.

## Verification and remaining limits

- Full sequential candidate decode: 11,488 frames, planned resolution/FPS/duration.
- [Transition guard](transitions/transition-guard.md): **21/21 PASS**. Every-frame strips around all declared visual/audio boundaries were visually inspected; destination scenes start on the declared frame without old-board flashes.
- All distinct settled ring states inspected from the encoded candidate at 1280×720; full-card framing, section bounds, colors, and constant strokes confirmed. Full-view openings and the final close inspected.
- All retained Notebook spans inspected at one-second intervals plus boundary/end frames; source labels additionally inspected at full resolution. This is not continuous playback or a claim that every image frame was visually read.
- Complete 82-segment final ASR transcript reviewed. Exact PCM source-preservation checks and encoded loudness/gap measurements passed. [Machine-readable verification](encoded-checks/verification.json).
- Protected source, lesson, canonical board and live-video hashes remain unchanged.
- **Not performed:** literal audio audition, continuous end-to-end watch/listen, perceptual seam/pacing certification, tracker update, publishing. Those prevent a shipping-ready KEEP certification.

## Build and QA commands

```sh
.video-venv/bin/python scripts/video/prepare_how_an_llm_split_v10.py --words
.video-venv/bin/python scripts/video/prepare_how_an_llm_split_v10.py --loudness-only
.video-venv/bin/python scripts/video/build_how_an_llm_works_v10_review.py --prepare-only
.video-venv/bin/python scripts/video/build_how_an_llm_works_v10_review.py
.video-venv/bin/python scripts/video/verify_how_an_llm_split_v10.py
.video-venv/bin/python scripts/video/grade_bundle.py video-audit/how-an-llm-works-repair-2026-09-17-v10/finished-review Prompts/how-an-llm-works-v10.mp4
```

The builder deliberately refuses to overwrite an existing candidate. Any rebuild needs a new version. Shared rendering-helper changes already present in the worktree were not edited; the helper hash used by this build is recorded in the manifest. The source identities and approved comparison remain in [the split review](../how-an-llm-works-split-comparison-2026-09-17/REVIEW.md).
