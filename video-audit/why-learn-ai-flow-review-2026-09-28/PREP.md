# Why Learn AI? preparation handoff — September 28, 2026

User requested the video prep materials after the teaching-flow review. Preparation is complete; generation, editing, and publication were not performed.

- Narration source: `lessons/why-learn-ai.md`.
- Prompt: `Prompts/why-learn-ai-video-prompt.txt`, 454 words, four current-format blocks.
- Registry entry: `why-learn-ai` in `Prompts/upload-sets.json`.
- Staged bundle: `gemini-notebook/why-learn-ai/`; upload exactly the five files in `upload/`, then paste `PROMPT.txt` into customization.
- Raw output: `Prompts/why-learn-ai-reroll.mp4`, or next unused numbered name.
- Current section-kit entry: `Prompts/START-SMARTER-VIDEO-KITS.md`.

The narration keeps page order and essential content. Added connective sentences explicitly map the printing-press choice to AI, familiar use to deliberate practice, desktop publishing to learning by making with AI, and the examples to the historical pattern. Missing teaching is protected as standalone required speech. The source does not repeat the old video's unsupported narrow-task historical contrast. The live lesson and video were not edited in this preparation task.

The press upload is a text-only native-layout rendering, `Prompts/why-learn-ai-press-faceless.jpg`, created with `render_why_learn_ai_opener_board.py --upload-variant`. It preserves the 1600 × 1150 dimensions, title, and banner, with no artwork loaded. Visually inspected. The registry maps it to the canonical illustrated press board for replacement in the eventual edit. The remaining three JPG uploads are canonical assets copied without modification.

Verification completed:

- `sync_gemini_notebook.py --lesson why-learn-ai --check`: OK.
- All 14 required quoted entries match standalone narration lines (quotation marks excluded for comparison).
- All Markdown image references resolve inside the five-file upload folder; prompt copy matches source.
- The two closing lines remain exact and last.
- Prompt is under 500 words; no checklist, prompt, or review document is inside upload/.
- Other registry entries were unchanged.
- Live video SHA-256 still matches the reviewed file: `6628a10f654e3f4e093ae13a9a060de73a3151ea456cc417271156c5973fae1e`.

Review the resulting roll against the revised source before finalizing the provisional production plan in REVIEW.md. No new narration has yet been generated or listened to.
