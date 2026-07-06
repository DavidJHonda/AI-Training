# Video Production — Prompts Directory

How to generate a lesson video in NotebookLM (system settled 2026-07-04 after the Welcome A/B and illustration tests):

1. **Notebook sources** (per lesson):
   - `Master Prompt.md` — the master rules. Re-upload whenever it changes; sources are static snapshots.
   - `lessons/<slug>.pdf` — the lesson itself (narration grounding).
2. **Prompt box**: paste the full text of `<slug>-video-prompt.txt`. The prompt is the spec — never lighten it. All prompts are kept under NotebookLM's 5,000-character box limit.
3. After generating: save the video as `videos/<slug>.mp4` and check its `LESSON_VIDEOS` entry in index.html (filename + duration label).
4. Once the video passes review and is committed: delete the NotebookLM notebook and any review copy of the video, but KEEP the prompt. The notebook is disposable because the repo can rebuild it; the prompt is what makes that true. Videos can't be edited, so every future change to a lesson means regenerating its video — and the prompt is the source you'll tweak to do it. When a lesson changes substantially, update its prompt in the same pass so they stay in sync.

## Start Smarter (8 lessons)

welcome, why-learn-ai, what-is-ai, how-an-llm-works, does-ai-think, what-you-can-control, does-school-matter, learn-with-ai — one `<slug>-video-prompt.txt` each.

## Work With AI (8 lessons)

opener-work (the section opener, 2–2.5 min), ai-is-different, where-ai-works-best, which-app, questions-matter, art-of-prompting, context-window, evaluate-the-results, critical-thinking — one `<slug>-video-prompt.txt` each. The opener's lesson PDF is `lessons/Opener-Work.pdf`.

## Rules learned the hard way

- The **prompt box is the high-authority channel**; source documents are treated as content. Never move the script into a source (tested: it leaks — the video illustrates the spec).
- **Illustration-as-source works on the new engine, full-bleed only** (does-ai-think canary, 2026-07-06; supersedes the Jul-4 "four tests, four redraws" finding). Referencing an attached illustration by filename reproduces it with near-perfect fidelity and no leakage into other scenes — but always full-frame: "framed inset on light canvas" and added-label instructions are ignored, and the 3:2 image is cropped to 16:9, clipping edge text mid-word. If an illustration will be a video source, keep critical text out of the outer ~15% or export a 16:9 variant, and put any required caption in the narration, not the scene spec.
- **Never embed style-reference frames or illustration images in any source**; they get re-rendered as content scenes (a style frame from another lesson showed up mid-video) and induce fake "reference sheet" annotations.
- **Never ask for text inside a drawing** — it renders as gibberish handwriting. Verbatim text goes in separate pills, stickies, or black-ink printed labels.
- On-screen text specs are directional: the generator paraphrases labels even when told "verbatim." The narrative arc carries the exact content.
- Prefer static scenes over timed reveals: draw complex layouts complete and let narration walk them.
