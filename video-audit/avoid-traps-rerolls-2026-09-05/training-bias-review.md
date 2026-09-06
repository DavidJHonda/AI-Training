# Training Bias — evaluation

Source: `Prompts/training-bias.mp4` · 4:34 · September 5, 2026

**Recommendation: repair.** This is a complete, usable teaching spine. It connects biased patterns, better questions, stale information, and retrieval without dropping an entire part of the lesson.

## What works

- **0:00–0:49:** the cow/background example explains why individually real facts or images can still create a distorted picture.
- **0:59–1:39:** defaults, blind spots, and wrong patterns each receive an explanation, not just a label.
- **1:53–2:22:** all three practical questions are taught and the board supplies usable wording.
- **3:34–4:18:** retrieval, adding to context, and generation are explained, followed by the important warning that retrieval does not guarantee reliability or correct interpretation.

The cow illustration is grounded in an actual background-generalization problem, although the video simplifies it into a single shortcut. I would keep that teaching analogy rather than demand a research-methods detour. [Beery et al., Recognition in Terra Incognita](https://openaccess.thecvf.com/content_ECCV_2018/html/Beery_Recognition_in_Terra_ECCV_2018_paper.html)

## Suggested changes

1. **2:31–2:36 — Trim the claim about forcing AI to reveal “actual reality” / the rest of the picture.** Asking for missing perspectives is useful, but it does not guarantee a complete or unbiased answer. Keep the three questions themselves.
2. **3:01–3:13 — Cut the asserted diagnosis of Claude’s mistake.** The video says it did not hallucinate, its training stopped before the draft, and everything after its cutoff is missing. The supplied exchange does not establish that exact cause. A model’s explanation of its own mistake is not proof of its training cutoff. Keep the incorrect answer and the successful current-source check on either side.
3. **3:27–3:31 — Replace the graphic labeled “Knowledge cutoff 18 months ago.”** No model/version or date supports that precise duration. The narration’s broader point about checking what changed can stay.
4. **4:18–4:26 — Optional cut.** The philosophical statement that AI is “only a reflection” is weaker than the concrete explanation we just heard. Go directly to “AI repeats the shape of its data. Ask what’s missing. Check what’s changed.”

## Board and visual plan

- **0:15–0:28:** insert `training-bias-pattern-v2.jpg` for the learned-background explanation. The new narration fully supports the Nate and Luke board; no alternative upload is needed. Keep the engaging cow-on-grass/beach opening.
- **0:59–1:39:** `training-bias-mechanisms-v2.jpg`.
- **1:53–2:22:** `training-bias-questions-v2.jpg`.
- **2:49–3:25, shortened by the approved cut:** `training-bias-stale-chat-v2.jpg`, tracing full bubbles. Preserve the current-source correction, not the unsupported diagnosis.
- **3:43–4:18:** `training-bias-rag-v2.jpg`, including its full caveat banner.
- Replace the end with the current standard close.

## Source note

The current lesson’s quoted Claude response itself attributes the error to stale information (`lessons/training-bias.md:57`). It is fine to show what Claude said, but our explanatory narration should not elevate that self-report into a verified technical diagnosis. If we revise source wording later, explicitly distinguish the observed correction from the unknown internal cause. No source edits made in this evaluation.
