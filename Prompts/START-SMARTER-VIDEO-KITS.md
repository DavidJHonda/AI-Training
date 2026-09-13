# Start Smarter Video Kits

Rebuilt 2026-09-12 under the speak-the-answers method (see `scripts/video/README.md`, "Speak the answers", and `EDIT-SPEC.md`). Welcome has no video by design. Every Markdown was rewritten from the live page with each board's text as prose beneath its image; every upload copy in `lessons/` is byte-for-byte the page asset (three What Is AI boards and the Where AI Already Lives board are served from `lessons/` by the page itself). Each prompt is self-contained and under 500 words. Boards with visible faces are never uploaded; the prompt reserves their narration and the real board is inserted in editing. Per-lesson upload checklists: `Prompts/<slug>-upload-files.txt`.

| Lesson | Markdown | Prompt | Notebook sources | Post-production only (faces) | Status |
|---|---|---|---|---|---|
| Why Learn Ai? | `lessons/why-learn-ai.md` | `Prompts/why-learn-ai-video-prompt.txt` | why-learn-ai-1-everyday, why-learn-ai-2-thrive, why-learn-ai-3-close | why-learn-ai-1-press | materials ready, roll pending |
| What Is Ai? | `lessons/what-is-ai.md` | `Prompts/what-is-ai-video-prompt.txt` | what-is-ai-1-types, what-is-ai-2-same-goal, what-is-ai-4-close | what-is-ai-ask-the-desk | materials ready, roll pending |
| How An Llm Works | `lessons/how-an-llm-works.md` | `Prompts/how-an-llm-works-video-prompt.txt` | how-an-llm-works-1-llm, how-an-llm-works-2-learn-once, how-an-llm-works-3-training, how-an-llm-works-4-patterns, how-an-llm-works-5-close | none | materials ready, roll pending |
| Does Ai Think? | `lessons/does-ai-think.md` | `Prompts/does-ai-think-video-prompt.txt` | does-ai-think-1-chinese-room, does-ai-think-3-close | does-ai-think-2-side-by-side | materials ready, roll pending |
| What You Can Control | `lessons/what-you-can-control.md` | `Prompts/what-you-can-control-video-prompt.txt` | what-you-can-control-1-hands, what-you-can-control-2-three-moves, what-you-can-control-3-close | none | materials ready, roll pending |
| Does School Matter? | `lessons/does-school-matter.md` | `Prompts/does-school-matter-video-prompt.txt` | does-school-matter-2-future, does-school-matter-3-close | does-school-matter-1-same-tool | materials ready, roll pending |
| Learn With Ai | `lessons/learn-with-ai.md` | `Prompts/learn-with-ai-video-prompt.txt` | learn-with-ai-1-study-tools, learn-with-ai-3-four-moves, learn-with-ai-4-close | learn-with-ai-2-how-it-works | materials ready, roll pending |

Notes:
- How an LLM Works: the "Same Word, Different Odds" table and the "One Word at a Time" walk are page components, not images; their numbers and words are in the Markdown as prose. The old odds capture and the myths board were stale and are deleted.
- Does School Matter had no close board copy; one was rendered from the page's CLOSE_BOARDS entry (`make_close_board.py --lesson whybother`).
- Stale September captures (why-learn-ai quote card, what-is-ai movie task, how-an-llm-works map/training/patterns/odds/myths, does-ai-think rulebook/compare, what-you-can-control moves, does-school-matter two-skills, learn-with-ai feed-in/habits) were deleted; the page assets in `illustrations/` and `lessons/` are the originals.
