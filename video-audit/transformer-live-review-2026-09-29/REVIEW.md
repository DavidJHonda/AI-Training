# Transformer — public video evaluation, September 29, 2026

**Recommendation: retain the narration and overall edit; repair one distracting visual.** The content earns a provisional **KEEP** recommendation from the complete fresh transcript. This is not an end-to-end audiovisual signoff: no perceptual listening or continuous playback was available. Visual findings below come from contact sheets covering the full duration and selected full-resolution frames.

## Verified source

- Public video: https://besmarterthanthetool.com/course-assets/transformer/transformer.mp4?v=20260928ship1
- Local equivalent: `course-assets/transformer/transformer.mp4`, the shipped v12 candidate.
- Public and local SHA-256: `0a972235e9fcaf619d8db34715243a7812a87569091e87092f866666586376b5`.
- Runtime: **3:54.867**, 7,046 frames, 30 fps, 1280 × 720.
- Retrieved public page references that exact cache key. Its Transformer lesson function matches the current local `index.html` lesson. Every board asset in the v12 manifest still matches its recorded hash.
- Scope: evaluation only. No lesson, video, prompt, tracker, or release change.

## Main findings

1. **Should fix — 0:54.967–1:02.900: a large gibberish paragraph sits over the brain.** At normal delivery resolution, it looks like text the student is meant to read, but it is visibly nonsensical. This distracts precisely when the narration contrasts human comprehension with earlier sequential AI. Preserve the brain/computer comparison and its existing animation; replace only the paper's contents with a meaningful, minimal visual, for example the existing CAT … IT sentence connection. Inspect the full span to ensure the repair follows any movement. Evidence: [frame at 0:58](frames/58.jpg).
2. **The worked-example return is worth keeping.** At 2:26.767–2:55.533, the video rereads all four sentences, then explains “turn on,” “carry,” “thirsty,” and “fresh.” This is useful progression from posing the ambiguity to explaining its resolution. It is not empty repetition. The sentence/clue outlines and complete-card views support the spoken explanation.
3. **The strongest conceptual beat is 2:14.88–2:26.80.** It clearly separates fixed learned weights from the changing token representations. Preserve it, along with the attention/transformation explanation immediately before it.

## Narration review

LESSON: Transformer (`attention`)

CANDIDATE: verified public v12, 3:54.867

VERDICT: **KEEP recommendation, provisional pending listening**. No material narration cut or graft is indicated by the transcript. No reroll is recommended from the available evidence.

| Teaching point, in lesson order | Assessment | Evidence from the fresh transcript |
| --- | --- | --- |
| Text becomes tokens; embeddings are rows of numbers representing starting meaning | TAUGHT | 0:00–0:15.78 explicitly defines both terms. |
| Surrounding words provide context | TAUGHT | 0:15.78–0:23.48 connects context to interpreting token meaning. |
| LIGHT can mean brightness or not heavy | RICH | 0:26.68–0:39.08 reads both sentences and explains both meanings. |
| IT can point to the cat or milk | RICH | 0:39.08–0:52.40 reads both complete sentences and identifies each referent. |
| Earlier sequential models struggled with distant connections | RICH | 0:55.04–1:23.36 walks THE → CAT → SAT, then explains the distance between CAT and IT. The complete long example is shown; the narration teaches its relevant relationship rather than rereading every intervening word. |
| 2017 paper, Transformer architecture, T in ChatGPT | TAUGHT | 1:23.44–1:33.44 names the year, Google, paper, architecture, and acronym link. The exact count of researchers is incidental background, not a missing mechanism. |
| Whole-message processing permits a direct connection back to CAT | TAUGHT | 1:33.44–1:43.88 connects the processing change to the same example. |
| Having the words available is only the start; relevant information must update token numbers | TAUGHT | 1:43.88–1:53.16 explicitly provides this bridge. |
| Attention weighs relevant information and blends it into token numbers | TAUGHT | 1:55.48–2:01.88 states the operation. |
| Transformation further processes those numbers using learned patterns | TAUGHT | 2:01.88–2:14.88 explains its role and the two steps working together. |
| Weights stay fixed; token representations change | RICH | 2:14.88–2:26.80 directly contrasts what stays fixed with what updates. |
| Return to LIGHT: turn on / carry supply the clues | RICH | 2:26.80–2:37.20 rereads each sentence, then explains its clue. |
| Return to IT: thirsty / fresh supply the clues | RICH | 2:37.20–2:51.16 rereads each sentence, then identifies the referent using its clue. |
| Sarcasm, idioms, and placeholder IT | TAUGHT, briefly | 2:55.56–3:12.84 names these applications and gives “It was a cold day” as a placeholder example. Optional clarity improvement in a future narration pass: say that this IT does not refer to a particular thing. No unsupported claim that a replacement donor has been identified. |
| Parallel processing needs position information | TAUGHT | 3:12.84–3:21.12 introduces the order problem. |
| Dog bites man / man bites dog; same tokens, different events | RICH | 3:21.12–3:34.88 reads both versions and explains why positions matter. |
| Position stamps / positional encoding preserve each token's place | TAUGHT | 3:34.88–3:44.84 names and explains the solution. The literal 1, 2, 3 labels are illustrative positions, not omitted consequential values. |
| Closing takeaway | TAUGHT | 3:44.84–3:50.84 delivers both required lines. |

HARD REQUIREMENTS: **MET in transcript** — “Attention Is All You Need,” Transformer, the T in ChatGPT, positional encoding, and both canonical closing lines: “Attention is all you need.” / “AI uses relationships between words to help interpret your message.”

ERRORS: No material contradiction with the current lesson found in the transcript. ASR punctuation and capitalization are not treated as audio defects.

SOURCE_QA: No blocking error found for this introductory lesson. “Reads the whole message at once” describes parallel input processing; it should not be interpreted as all decoder positions seeing future tokens or the whole answer being generated simultaneously. The original paper distinguishes parallel attention, causal masking, feed-forward processing, and positional encoding: [Attention Is All You Need, sections 3.1–3.5](https://arxiv.org/html/1706.03762v7). This technical boundary is not a recommendation to add advanced machinery to the video.

ADDITIONS: The river/bank/water diagram is a useful added context example. Its illustrative vector values do not need to be presented as measured statistics. The sarcasm example “Oh, fantastic” provides a concrete visual application. These judgments concern visible content; animation quality remains provisional.

REPAIR PLAN: No narration edit proposed. The visual correction above preserves the existing audio and timing. No added pauses proposed; there is no measured or heard pacing problem justifying them.

LISTENING: None. The transcript is automated transcription of the exact encoded live-equivalent file. It does not establish voice quality, cadence, pronunciation, or smoothness of splices. The prior review particularly calls out 0:46–0:52 and 2:44–2:48; those listening checks remain open.

## Board treatment to retain

This evaluation proposes one narrow visual repair outside the boards. The table records the existing board treatment to preserve, not a new authorized build. Times derive from the exact matching v12 manifest and were checked against fresh frame samples.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
| --- | --- | --- | --- | --- |
| Two Problems Context Must Solve | Different Meanings card → individual example sentences; Pronouns card → individual sentences; summary banner | Full opening, complete LIGHT-card zoom, pan to complete pronoun card, pull back | 0:23.567–0:39.033 and 0:42.867–0:54.967; cat/IT/glass illustration between visits | Preserve the established full-sentence teaching and card framing. |
| How Earlier AI Read Text | THE → CAT → SAT → IT → CAT; takeaway | Full view, compact | 1:02.900–1:23.267, 20.367 s | The word-by-word highlights directly teach sequential traversal and the long connection. This was explicitly requested for v12. |
| How a Transformer Reads a Sentence | Whole-message orientation, then IT/CAT relationship | Full view, compact | 1:33.400–1:43.900, 10.500 s | Direct comparison to the earlier-AI board. |
| How Context Changes the Numbers | Whole Attention card → whole Transformation card → summary | Full view, compact | 1:53.200–2:14.800, 21.600 s | Two actively explained steps; the active-data illustration follows. Preserve the complete cards. |
| How the Transformer Resolves Meaning | Each full sentence followed by its clue explanation; summary banner | Full opening → complete LIGHT card → complete pronoun card → full-board takeaway | 2:26.767–2:55.533, 28.767 s | Longest unbroken teaching board. A deliberate exception to the approximately 20-second break preference: removing the sentence or clue while it is taught would weaken the approved reread sequence. No stronger, verified break is proposed. |
| How a Transformer Keeps Words in Order | Comparison, without-position card, position-stamps card, summary | Full view, compact | 3:21.300–3:44.867, 23.567 s | Short comparison followed by two explained states. Preserve the coherent walkthrough; no decorative cutaway proposed. |
| Attention is all you need. | Unmarked canonical close | Existing hold/push/settled hold | 3:44.867–3:54.867, 10.000 s | The actual last decoded-frame sample is the canonical close. |

Longest teaching-board run: **28.767 s**. Longest board/close chain: **33.567 s**. Rings and camera changes do not reset these durations. These runs are recorded openly rather than claimed to satisfy a strict 20-second cap; the current specification describes an approximate default, and the existing treatment has specific teaching value and prior approval.

## Supporting scenes

Retain, provisionally on sampled visual evidence:

- 0:00–0:23.567: typing, word/token strip, and river/bank/water embedding reveal establish words → numbers → context.
- 0:39.033–0:42.867 and 1:43.900–1:53.200: cat/IT/glass illustrates the referent problem. The later reuse is a little repetitive, but it supports the bridge to the mechanism and is not a repair blocker.
- 0:54.967–1:02.900: brain versus computer comparison; repair only the distracting fake paragraph.
- 1:23.267–1:33.400: paper/architecture/ChatGPT-T graphic provides historical orientation.
- 2:14.800–2:26.767: active-data number bars accompany the weights-versus-token-data distinction.
- 2:55.533–3:12.84 approximately: LIGHT/brightness, sarcastic “Oh, fantastic,” and placeholder-IT scenes extend the example. The individual cuts were sampled, not timed frame-exactly in this pass.
- Approximately 3:12.84–3:21.300: ordered blocks becoming scattered visually introduce the position problem.

No newly generated supporting artwork is needed for this recommendation. Keep useful animation when repairing the paper area; do not replace the whole segment with a still by default.

## Verification limits and artifacts

Performed: fetched public HTML; streamed the served MP4 for a cryptographic identity check; compared the public lesson function with local source; generated and read the complete fresh transcript; decoded the file while building scene/contact-sheet evidence; inspected all five four-second contact sheets and selected 720p frames; checked current board hashes against the exact-file build manifest; inspected the ending sample.

Not performed: continuous end-to-end playback, perceptual audio listening, a new every-boundary transition pass, motion-quality certification, or mobile/student-player testing. Existing v12 technical QA is historical evidence for this same hash, not a new listening pass.

Evidence: `public-verification.json`, `verification.json`, `transformer/transcript.txt`, `transformer/sheets/`, and `frames/`. The previous build record remains at `video-audit/transformer-repair-2026-09-28-v12/REVIEW.md`.
