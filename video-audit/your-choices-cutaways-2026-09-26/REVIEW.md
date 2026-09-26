# Your Choices — cutaways under the board runs (2026-09-26)

Scope: narrow visual-only retrofit of the live video (`course-assets/your-choices/your-choices.mp4`, the 2026-09-25 age-rules cut). Plan approved by David 2026-09-26 ("build it"). Build: `scripts/video/build_your_choices_cutaways.py`. Candidate: `Prompts/your-choices-cutaways.mp4`. Record: `edit-manifest.json` (hashes, spans, corner-mark counts).

Every output frame is the live frame except the six spans below. Boards, rings, close, and audio are as shipped; audio packets are byte-identical to live; 4863 decoded frames (same as live).

| Output | Narration | Drawing | Source |
|---|---|---|---|
| 0:40.6–0:43.1 | "Let's look at the first two configuration choices" | four paper-cut dials | Roll 2 frames 584–657 |
| 0:49.6–0:55.6 | "Choose the app… fits the tools and workflows you use the most." | drawn monitor with app toolbar | Roll 2 2320–2516 |
| 1:10.9–1:15.6 | "Some apps offer a family of models…" | model picker (Standard 1.5 / Advanced Ultra / Compact Flash) | Roll 1 3248–3387 |
| 1:47.6–1:54.5 | "dial up this setting for math, code, planning…" | Advanced Work keys, cursor on Reasoning | Roll 2 756–965 |
| 1:54.5–1:58.3 | "Keep this at the default setting for routine…" | Routine checklist (last 18 frames held) | Roll 2 658–753 |
| 2:08.3–2:15.5 | "searches… compares various sources… cited report." | Research half of the diagram, zoomed (last 70 frames held) | Roll 2 1232–1375, crop x617–1257 y260–620 |

Longest single-board holds after the edit: Which Model? / Choose the Tool 1:15.6–1:33.9 (18.4 s); Choose How It Works 1:33.9–1:47.6 (13.7 s). Before: 53.3 s and 49.7 s.

Checks done: transition_guard 11/11 pass, strips inspected (model-picker entry); contact sheet of every span's first/middle/last frame and both neighbours; corner mark cleaned on all 861 donor frames (0 declined), corners inspected. Hard cuts, all in word gaps except 0:43.1 (mid "choices"; picture only).

Not done: no one has watched it end to end. Owner calls still open: the model picker's made-up "Advanced Ultra / Compact Flash" names; style mix (Roll 1 flat UI among Roll 2 paper-cut).

Shipped 2026-09-26 on David's "ship it": installed at course-assets/your-choices/your-choices.mp4 (sha256 af247783…, 18544138 bytes), cache key 20260926ship1, manifest video_assets updated.
