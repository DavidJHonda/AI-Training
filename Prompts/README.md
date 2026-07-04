# Video Production — Prompts Directory

How to generate a lesson video in NotebookLM (system settled 2026-07-04 after the Welcome A/B and illustration tests):

1. **Notebook sources** (per lesson):
   - `NotebookLM Task-Master Video Guidelines.md` — the master rules. Re-upload whenever it changes; sources are static snapshots.
   - `lessons/<slug>.pdf` — the lesson itself (narration grounding).
2. **Prompt box**: paste the full text of `<slug>-video-prompt.txt`. The prompt is the spec — never lighten it. All prompts are kept under NotebookLM's 5,000-character box limit.
3. After generating: save the video as `videos/<slug>.mp4` and check its `LESSON_VIDEOS` entry in index.html (filename + duration label).
4. Once the video passes review and is committed: delete the NotebookLM notebook and any review copy of the video, but KEEP the prompt. The notebook is disposable because the repo can rebuild it; the prompt is what makes that true. Videos can't be edited, so every future change to a lesson means regenerating its video — and the prompt is the source you'll tweak to do it. When a lesson changes substantially, update its prompt in the same pass so they stay in sync.

## Start Smarter (8 lessons)

welcome, why-learn-ai, what-is-ai, how-an-llm-works, does-ai-think, what-you-can-control, does-school-matter, learn-with-ai — one `<slug>-video-prompt.txt` each.

## Rules learned the hard way

- The **prompt box is the high-authority channel**; source documents are treated as content. Never move the script into a source (tested: it leaks — the video illustrates the spec).
- **The generator cannot show a source image as-is.** Four tests, four redraws, under every instruction phrasing including "display AS-IS, do NOT redraw." Don't reference course illustrations at all: DESCRIBE the wanted scene in the prompt (cast, setting, key props) and let it draw fresh.
- **Never embed style-reference frames or illustration images in any source**; they get re-rendered as content scenes (a style frame from another lesson showed up mid-video) and induce fake "reference sheet" annotations.
- **Never ask for text inside a drawing** — it renders as gibberish handwriting. Verbatim text goes in separate pills, stickies, or black-ink printed labels.
- On-screen text specs are directional: the generator paraphrases labels even when told "verbatim." The narrative arc carries the exact content.
- Prefer static scenes over timed reveals: draw complex layouts complete and let narration walk them.
