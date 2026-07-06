# Video Production — Prompts Directory

How to generate a lesson video in NotebookLM (system settled 2026-07-04 after the Welcome A/B and illustration tests):

1. **Notebook sources** (per lesson):
   - `Master Prompt.md` — the master rules. Re-upload whenever it changes; sources are static snapshots.
   - `lessons/<slug>.md` — the lesson itself (narration grounding). Use the plain-text `.md` export, NOT the `.pdf`: the PDF is a styled page render the video generator can screenshot into blurry document b-roll; the `.md` is content only, so there's nothing to mis-render. (`scripts/make-lesson-texts.sh` regenerates the `.md` files.)
2. **Prompt box**: paste the full text of `<slug>-video-prompt.txt`. The prompt is the spec — never lighten it. All prompts are kept under NotebookLM's 5,000-character box limit.
3. After generating: save the video as `videos/<slug>.mp4` and check its `LESSON_VIDEOS` entry in index.html (filename + duration label).
4. After downloading the video, delete that lesson's notebook right away — one notebook per lesson, gone as soon as its video is saved, so the NotebookLM workspace stays controllable. Nothing is lost: the repo rebuilds any notebook from `Master Prompt.md` + the lesson `.md` (+ illustration jpg if the prompt calls for one), which a re-roll does anyway. KEEP the prompt. When a video fails review, update its prompt against the observed failure modes in the same pass, before regenerating. The notebook is disposable because the repo can rebuild it; the prompt is what makes that true. Videos can't be edited, so every future change to a lesson means regenerating its video — and the prompt is the source you'll tweak to do it. When a lesson changes substantially, update its prompt in the same pass so they stay in sync.

## Start Smarter (8 lessons)

welcome, why-learn-ai, what-is-ai, how-an-llm-works, does-ai-think, what-you-can-control, does-school-matter, learn-with-ai — one `<slug>-video-prompt.txt` each.

## Work With AI (8 lessons)

opener-work (the section opener, 2–2.5 min), ai-is-different, where-ai-works-best, which-app, questions-matter, art-of-prompting, context-window, evaluate-the-results, critical-thinking — one `<slug>-video-prompt.txt` each. The opener's lesson file is `lessons/Opener-Work.md`.

## Status tracking

Per-video status lives in the shared Google Sheet "AI-Training — Video Tracker"
(https://docs.google.com/spreadsheets/d/16RXfX9awLA8Idu83OBN97bCrMiTzyEOFO4MBpvPWXO8/edit).
The sheet is the dashboard; the repo and intake commit messages remain the source of
truth. Update the sheet at every intake decision.

## Rules learned the hard way

- The **prompt box is the high-authority channel**; source documents are treated as content. Never move the script into a source (tested: it leaks — the video illustrates the spec).
- **NotebookLM rejects photoreal-people image sources.** Of the staged illustrations, the two painterly ones (chinese-room, context-window-window) uploaded fine; the photorealistic ones with visible faces and brand marks were refused (content filter, not format — the files are byte-identical in structure). Illustrations meant for video sourcing must be drawn/painterly, faces stylized or from behind, no real logos or trade dress. The four affected prompts (questions-matter, ai-is-different, where-ai-works-best, which-app) run in describe-the-scene mode until ChatGPT re-dos exist.
- **Lesson-box jpgs are the best video source yet** (questions-matter pilot, 2026-07-06): a 1600x900 capture of a lesson card grid, composed on the page-background color with text clear of the 16:9 crop zone, reproduced pixel-crisp — and the engine added narration-synced highlight sweeps over the static grid on its own. Use this for any verbatim-critical scene; capture via headless browser at 2x zoom.
- **The engine can insert Getty stock photos despite the master-prompt ban.** When narration names real people or places (Socrates, Einstein, Athens), it may cut to watermarked archival photographs. Reinforce per-prompt: name the figures and require they be drawn.
- **Illustration-as-source works on the new engine, full-bleed only** (does-ai-think canary, 2026-07-06; supersedes the Jul-4 "four tests, four redraws" finding). Referencing an attached illustration by filename reproduces it with near-perfect fidelity and no leakage into other scenes — but always full-frame: "framed inset on light canvas" and added-label instructions are ignored, and the 3:2 image is cropped to 16:9, clipping edge text mid-word. If an illustration will be a video source, keep critical text out of the outer ~15% or export a 16:9 variant, and put any required caption in the narration, not the scene spec.
- **Never embed style-reference frames or illustration images in any source**; they get re-rendered as content scenes (a style frame from another lesson showed up mid-video) and induce fake "reference sheet" annotations.
- **Never ask for text inside a drawing** — it renders as gibberish handwriting. Verbatim text goes in separate pills, stickies, or black-ink printed labels.
- On-screen text specs are directional: the generator paraphrases labels even when told "verbatim." The narrative arc carries the exact content.
- Prefer static scenes over timed reveals: draw complex layouts complete and let narration walk them.
