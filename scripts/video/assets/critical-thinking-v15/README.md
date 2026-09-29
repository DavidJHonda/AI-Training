# Critical Thinking v15 visual-repair assets

Approved by David's “Build it” following the September 29 evaluation.

`annotated-paper-corrected.png` was created using the built-in imagegen tool in edit mode. Target was the installed v14 frame at 1:49, inspected before editing. It replaces only the annotated-article scene at frames 3198–3467; the video renderer applies a restrained pullback. The output preserves the paper/pen composition and removes all nonsense writing. It is not a new canonical course board.

Original tool output: `/Users/davidobrien/.codex/generated_images/01a0ee25-cdf0-7b83-8f93-425eaf46a32f/exec-d0016fbb-32b5-461e-b3a7-3a89bcf0dd31.png`.

## Exact generation prompt

Use case: text-localization. Edit target: this exact 16:9 illustrated torn-paper article with red pen. Repair only the writing on the paper for a high-school critical-thinking video. Preserve the exact paper position, perspective, torn edges, pen, blue backing paper, yellow/red highlights, lighting, illustration style, framing and surrounding background. Remove ALL existing words including headings and gibberish. Replace them with three beautifully clear handwritten question blocks laid out on the paper, keeping each completely readable within frame and away from the pen: upper left 'What evidence supports this?'; upper right 'What is missing?'; lower left 'What else could explain it?'. Use these exact three questions and no other text. Tasteful red circles or underlines may mark 'evidence', 'missing', and 'explain'. Keep ample whitespace instead of invented filler text. Critical invariant: same composition and perspective, no extra props, no logo, no watermark, no new student, no redesign, no pseudo-text. Output landscape 16:9.

## Other graphics

The revised statistical diagram is deterministic vector-style video graphics rendered by `scripts/video/build_critical_thinking_v15.py` over the original scene's blank opening background. It preserves the staged reveal and narrated timing, with 15 participant nodes, 18 measurement nodes, a single highlighted outcome and a qualified conclusion. It avoids depicting one participant/measurement edge as a statistical correlation.

The study heading is a local video text overlay. Its opacity is measured from the original title on each frame, retaining the original panel and all surrounding animation.
