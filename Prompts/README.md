# Video Production — Prompts Directory

How to generate a lesson video in NotebookLM (system settled 2026-07-04 after the Welcome A/B test):

1. **Notebook sources** (per lesson):
   - `NotebookLM Task-Master Video Guidelines.md` — the master rules. Re-upload whenever it changes; sources are static snapshots.
   - `lessons/<slug>.pdf` — the lesson itself (narration grounding).
   - `<slug>-illustrations.pdf` — ONLY if the lesson has one (see table). Contains the course illustrations to reproduce, captioned by scene.
2. **Prompt box**: paste the full text of `<slug>-video-prompt.txt`. The prompt is the spec — never lighten it. All prompts are kept under NotebookLM's 5,000-character box limit.
3. After generating: save the video as `videos/<slug>.mp4` and check its `LESSON_VIDEOS` entry in index.html (filename + duration label).

## Start Smarter (8 lessons)

| Lesson | Prompt | Illustration appendix |
|---|---|---|
| Welcome | welcome-video-prompt.txt | welcome-illustrations.pdf |
| Why Learn AI | why-learn-ai-video-prompt.txt | why-learn-ai-illustrations.pdf |
| What Is AI? | what-is-ai-video-prompt.txt | — |
| How an LLM Works | how-an-llm-works-video-prompt.txt | — |
| Does AI Think? | does-ai-think-video-prompt.txt | does-ai-think-illustrations.pdf |
| What You Can Control | what-you-can-control-video-prompt.txt | — |
| Does School Matter? | does-school-matter-video-prompt.txt | does-school-matter-illustrations.pdf |
| Learn with AI | learn-with-ai-video-prompt.txt | — |

## Rules learned the hard way

- The **prompt box is the high-authority channel**; source documents are treated as content. Never move the script into a source (tested: it leaks — the video illustrates the spec).
- **Never embed style-reference frames** in any source; they get reproduced as scenes. Style steering lives in prompt language only.
- **Content illustrations DO reproduce faithfully** when embedded in an appendix source with a "reproduce in Scene N" caption.
- On-screen text specs are directional: the generator paraphrases labels even when told "verbatim." The narrative arc carries the exact content.
- Prefer static scenes over timed reveals: draw complex layouts complete and let narration walk them.

The `*-illustrations.html` files are the editable sources for the appendix PDFs. To regenerate one:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="Prompts/<slug>-illustrations.pdf" \
  "http://127.0.0.1:8753/Prompts/<slug>-illustrations.html"
```

(Serve the repo root first: `python3 -m http.server 8753 --bind 127.0.0.1`.)
