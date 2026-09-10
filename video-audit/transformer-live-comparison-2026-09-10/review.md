# Live Transformer vs current lesson and v5

Live: videos/transformer.mp4, 271.3 seconds. Latest review: videos/transformer-v5.mp4, 251.133 seconds. Read current index.html HowAIReadsSection and lessons/transformer.md, full newly generated live small.en transcript, previous full candidate transcript with v4/v5 correction manifests, and all three live contact sheets. This is a narration-content and sampled-visual comparison, not uninterrupted listening. No media or lesson changed.

Verdict: live has stronger explanatory pacing for positional encoding, but is not a better as-is match for the current lesson overall. Recommend preserving v5 as the main edit and adapting the live word-order teaching sequence, subject to a concrete edit plan and clean audio joins. The user has requested evaluation only, not a new build.

Live strengths:
- 0:37–0:47 reads both complete cat/milk sentences and makes the one-word change explicit.
- 0:55–1:29 explains sequential processing with a familiar typewriter image, though it overstates inevitable forgetting.
- 3:28–4:20 develops DOG BITES MAN, the identical tokens in another order, and position information as the solution. Around 4:00, numbered tokens provide a concrete visual link to the position-stamp metaphor. V5 gives the same topic only about 23.4 seconds at 3:39–4:02, so its explanation feels compressed.

Current lesson alignment favors v5:
- Live opener uses mathematical vectors without defining embeddings. V5 explains the starting row of numbers.
- Live 2:15–2:34 separates attention as choosing relevance and transformation as updating the representation. V5 explicitly says attention blends information into the numbers before transformation. This matches the revised lesson and original Transformer paper section 3.2.
- Live 3:06–3:11 directly links IT to later thirsty/fresh through attention. The revised lesson deliberately uses complete-sentence interpretation rather than claiming causal attention can look forward.
- Live uses retired lesson boards, including the old two-operations presentation and old closing. This is repairable visually, not a narration-selection reason by itself.

Position passage should not be copied verbatim:
- 3:20.98–3:27.88 says simultaneous reading inherently destroys chronology. Keep the conditional explanation of what is missing WITHOUT positional information instead.
- 3:44.94–3:50.38 says the positional step happens before the first layer. 3:51–3:55 says a sequence number is mixed directly into every token; 4:05.58–4:12.24 says position is hard-coded into tokens. These describe an overly literal universal implementation; the current lesson uses a position-stamp metaphor. Different positional schemes exist, including rotary attention representations.
- Most useful narrative material: 3:28.56–3:44.28 (DOG/MAN comparison), 3:55.84–4:05.58 (position-stamp metaphor and name), 4:13.16–4:19.72 (benefit). Exact edit points require waveform review; these are transcript ranges, not approved cut boundaries. A short bridge from existing new narration may make the metaphor coherent without literal implementation claims.

Technical references: https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf (attention weighted sum, decoder masking, positional encoding); https://huggingface.co/docs/transformers/model_doc/roformer (rotary positional representations).
