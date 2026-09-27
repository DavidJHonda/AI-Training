# 06. Transformer — published-video review

**Recommendation: REROLL after a source correction — the central mechanism needs clearer scope.**

Reviewed Sept. 27, 2026. Runtime **3:46.27**. Published version `course-assets/transformer/transformer.mp4?v=20260922ship6`.

## Narration and teaching

The two ambiguity examples, earlier sequential models, attention/transformation, frozen weights, and positional information are all covered. Most of this is useful teaching. The material issue is the move from “the T in ChatGPT” (1:27–1:31) to whole-message access and updating token meanings (1:32–2:12), illustrated with later words “carry,” “thirsty,” and “fresh” (2:29–2:42). This blurs parallel processing with unrestricted attention. In a causal decoder, an earlier token cannot attend to later positions even when the prompt is processed in parallel. A later/final position can use the full preceding context to resolve the interpretation. Bidirectional encoder attention is different. The original paper explicitly distinguishes these cases: [Attention Is All You Need, §§3.1 and 3.2.3](https://arxiv.org/html/1706.03762v7).

Recommendation: correct the source and affected boards first, then generate replacement narration for the causal-attention explanation. No verified existing donor contains the necessary qualification. Calling this a feasible audio REPAIR would overstate the available evidence. A reroll should preserve the strong examples and frozen-weights explanation; it is not needed for the existing ring widths or pacing. If the owner chooses to teach a generic bidirectional transformer instead, explicitly state that scope and distinguish it from the later autoregressive chat example.

## Timestamped findings and proposed fixes

| Current timestamp | Finding | Proposed action |
|---|---|---|
| 1:31.96–1:51.12; 2:25.48–2:46.14 | Whole-message availability is conflated with what each token is allowed to attend to; right-side clues are used to explain an earlier token. | Proposed replacement concept: “The prompt can be processed in parallel. In a GPT-style model, each position uses itself and earlier positions. By the end of the prompt, later positions can use the whole sentence to help predict the reply.” Use an earlier-context example, or demonstrate resolution at the final position. Revise the current page boards consistently before a reroll. |
| 0:23.57–0:39.03; 0:42.87–0:53.67; 2:25.47–2:46.93 | The two tall photo/text cards remain full view; their smallest sentences are less comfortable at 720p. | Try a complete-card zoom in an approved preview, including photo, title, sentences and bottom clue section. Tall cards may gain little; do not promise a readability improvement or crop inside them. |
| 3:12.70–3:36.27 | Word-order board lasts 23.57s, the longest actual board run. | KEEP the compact full view and complete comparison as a short exception. The lesson already alternates short boards and drawings well. |

## Current board durations and proposed board plan

Longest continuous teaching-board chain: **23.57s**. Including a directly adjacent standard closing card, longest board-to-board exposure is **33.57s**. These counts include camera movements and silence holding the image; the close is also listed separately below.

| Exact board title | Current output span | Continuous time | Highlighting / camera plan | Break or exception |
|---|---|---:|---|---|
| Two Problems Context Must Solve | 0:23.57–0:39.03 | 15.47s | Full board first; blue different-meanings card then named sentences. | 15.47s, then drawing break. |
| Two Problems Context Must Solve | 0:42.87–0:53.67 | 10.80s | Return full view; green pronouns card/sentences then banner. | 10.80s; source correction affects examples. |
| How Earlier AI Read Text | 1:01.60–1:21.97 | 20.37s | Full view; whole sequence then distant CAT/IT relationship. | 20.37s, minor exception. |
| How a Transformer Reads a Sentence | 1:32.10–1:42.60 | 10.50s | Full view; complete sentence. | 10.50s; correct causal-attention scope. |
| How Context Changes the Numbers | 1:51.90–2:13.50 | 21.60s | Full view; Attention → Transformation → banner. | 21.60s, minor exception. |
| How the Transformer Resolves Meaning | 2:25.47–2:46.93 | 21.47s | Full opening; complete active card if useful; clues then banner. | 21.47s; source correction before new timing. |
| How a Transformer Keeps Words in Order | 3:12.70–3:36.27 | 23.57s | Full view; same tokens → absent positions → position stamps → banner. | 23.57s, explicit exception. |
| Attention is all you need. / AI uses relationships between words to help interpret your message. | 3:36.27–3:46.27 | 10.00s | Standard close. | 10.00s; reconsider wording if source scope changes. |

## Rings, framing and transitions

Current outlines vary about 4–7px; the detected 2px IT box is part of the board art, not a generated highlight. Apply 4px in any new build.

Most boards are compact. Preserve the useful Notebook interleaving; do not lengthen holds or add pauses just for camera changes.

Fresh automated transition guard: **PASS at 17 declared boundaries**. This detects short visual islands near declared edits; it does not prove all animation, audio, or natural source transitions are good.



## Evidence and limits

No build, reroll, course edit, tracker write, or publication was performed. Proposed edit times refer to the current published output; source reuse references refer to that same MP4 unless explicitly stated. Proposed future cut points are editorial targets, not auditioned frame-accurate audio joins.

The current published MP4 and all checked page JPGs match local SHA-256 hashes. The retained build manifest also exactly matches this MP4 hash. Board spans below therefore use the finished output timeline, verified against sequentially decoded visual samples. Pauses, zooms, pans and changed rings remain inside the same continuous board span. Adjacent different canonical boards count together for a board-chain duration. Time ranges are half-open at the outgoing cut.

The current ring rule is fixed **4px at 720p**, drawn after camera transforms (Edit Spec §5, Sept. 26). Older shipped ring widths are explicitly grandfathered. They are not standalone reroll/rebuild reasons. Reported widths are sampled solid-pixel estimates; anti-aliasing adds an edge and artwork can cause false detections.

Checks not completed: real-time end-to-end listening/viewing, narrator warmth/prosody/pronunciation, audible splice quality, loudness/noise-floor continuity, and phone/player readability or streaming behavior. Fresh word-timestamp ASR supports content review, but does not certify any of those listening checks. Original raw rolls/donor candidates cited in older reports are missing from this checkout, so proposed donor availability is restricted to current published pictures. The Google Sheet Video Tracker returned HTTP 401; workflow status was not verified or changed. No full independent audit of every tokenizer ID, model-specific vocabulary claim, or toy embedding value was completed. Page boards were inspected as current image assets and page content, not as an interactive browser playback session.

All ten lesson videos were sequentially decoded end to end and passed fresh automated transition guards at the declared seams. Only Opener’s complete seven seam strips were manually inspected in this pass; other videos received scene/interval contact-sheet review plus selected full-resolution frames, not manual inspection of every transition-strip frame. The guard result is a limited visual check, not a shipping certification. Original half-second ORB span scans were stopped after false positives; exact hash-matched output manifests plus decoded frames were used instead. Ring sampling was 4 seconds for other lessons and 1 second for Opener, not an exhaustive per-frame width measurement.

The 20-second single-board and 60-second chain thresholds are editorial triggers, not reasons to insert filler. A proposed reuse below is not certified until the complete selected span is previewed. Where no relevant compliant drawing is verified, that limitation or a remaining pacing exception is stated rather than hidden. Keep canonical JPGs intact; source-board revisions require a separate approved source change.


- [Current video](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer.mp4)
- [Current boards inspected](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-section-review-2026-09-27/transformer/current-boards.jpg)
- [Fresh transcript](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-section-review-2026-09-27/transcripts/transformer.txt)
- [Retained matching manifest](/Users/davidobrien/Developer/AI-Training/video-audit/transformer-comparison-2026-09-22/build-v10/edit-manifest.json)
- [Fresh transition report](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-section-review-2026-09-27/transformer/guard/transition-guard.md)
- [Measured ring samples](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-section-review-2026-09-27/transformer/ring-stroke.txt)
- [Public/local byte verification](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-section-review-2026-09-27/published-byte-verification.json)

SHA-256: `d55f0000452087fb4b7993b2e79e06759ef263e147362cbd744a3c44883d9eb6`.
