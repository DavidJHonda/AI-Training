# Video Production — Prompts Directory

How to generate a lesson video in NotebookLM (system settled 2026-07-04 after the Welcome A/B and illustration tests):

1. **Notebook sources** (per lesson):
   - `Master Prompt.md` — the master rules. Re-upload whenever it changes; sources are static snapshots.
   - `lessons/<slug>.md` — the lesson itself (narration grounding). Use the plain-text `.md` export, NOT the `.pdf`: the PDF is a styled page render the video generator can screenshot into blurry document b-roll; the `.md` is content only, so there's nothing to mis-render. (`scripts/make-lesson-texts.sh` regenerates the `.md` files.)
2. **Prompt box**: paste the full text of `<slug>-video-prompt.txt`. The prompt is the spec — never lighten it. All prompts are kept under NotebookLM's 5,000-character box limit.
3. After generating: save the video as `videos/<slug>.mp4` and check its `LESSON_VIDEOS` entry in index.html (filename + duration label).
4. After downloading the video, delete that lesson's notebook right away — one notebook per lesson, gone as soon as its video is saved, so the NotebookLM workspace stays controllable. Nothing is lost: the repo rebuilds any notebook from `Master Prompt.md` + the lesson `.md` (+ illustration jpg if the prompt calls for one), which a re-roll does anyway. KEEP the prompt while the video is flagged or pending. When a video fails review, update its prompt against the observed failure modes in the same pass, before regenerating. The notebook is disposable because the repo can rebuild it; the prompt is what makes that true. Videos can't be edited, so every future change to a lesson means regenerating its video — and the prompt is the source you'll tweak to do it. When a lesson changes substantially, update its prompt in the same pass so they stay in sync.
5. **Retirement (owner policy, 2026-07-07)**: once a video is Live with NO flag, its NotebookLM sources are deleted — the lesson `.md`, its board jpgs in `lessons/`, and its `<slug>-video-prompt.txt`. The lesson `.pdf` stays. Everything is recoverable from git history; the `.md` also regenerates via `scripts/make-lesson-texts.sh` and boards recapture via `scripts/capture-board.sh`. Flagged videos keep their full source sets until their re-roll ships clean.

## Prompts on hand

- **Start Smarter**: complete — all 8 live, no flags, sources retired.
- **Work With AI**: context-window (flagged), evaluate-the-results (rejected v1 — regenerate).
- **Understand AI** (prompt ready, pending scene review): opener-understand, vector-space, ai-is-math, tokens, embeddings, transformer, layers.

Retired after shipping clean (recover from git history if a lesson changes): does-ai-think, what-you-can-control, does-school-matter, learn-with-ai, opener-work, where-ai-works-best, questions-matter, critical-thinking, what-is-ai, ai-is-different, which-app, why-learn-ai, art-of-prompting, welcome, how-an-llm-works.

## Status tracking

Per-video status lives in the shared Google Sheet "AI-Training — Video Tracker"
(https://docs.google.com/spreadsheets/d/16RXfX9awLA8Idu83OBN97bCrMiTzyEOFO4MBpvPWXO8/edit).
The sheet is the dashboard; the repo and intake commit messages remain the source of
truth. Update the sheet at every intake decision. Workflow: Claude reads the sheet
directly (Google Drive connector, read-only) and drafts paste-ready updated rows;
David pastes them into the sheet.

## Rules learned the hard way

- **The per-lesson .md is REQUIRED — never drop it from the sources** (A/B test, how-an-llm-works, 2026-07-07). Without it the engine backfills vocabulary from its own ML knowledge ("N-Gram Association Map", "Hypothesis/Validation/Adjustment", "Prior Tokens/Context Trigger") and invents MORE statistics, and the video ran longer, not shorter. The .md is what grounds narration in the lesson's vocabulary; repetition is fixed by fewer, longer-held board scenes, not by removing sources.

- **BOARDS BEAT SKETCHES — use as many lesson-box jpgs as the lesson supports** (owner directive, 2026-07-07). Every intake confirms the split: board scenes reproduce verbatim (often with narration-synced highlights for free), while freeform sketch scenes are where the engine drifts — welcome's invented chapter card + b-roll, why-learn-ai's 1:43 morph, critical-thinking's muddled drawn close all happened in non-board scenes. Default scene plan: sketch for the hook, a board for every teaching beat (capture one with `scripts/capture-board.sh` if it doesn't exist), pills/stickies for the close. For a verbatim-critical beat that exists as no lesson element (a course-name close, a tools list), COMPOSE a one-off board on a standalone page in the app's fonts and reproduce that — prose EXACT anchors get paraphrased even in the close position; composed boards land verbatim (welcome v3, 2026-07-08: statement-card close + tools pills both held, after two rolls of prose anchors failing).

- **David reviews the scene-by-scene directions before any generation.** Whenever a prompt's SCENE BREAKDOWN changes (new lesson, board swap, hardening), present the scene list for his review before he generates. This catches structural problems automation misses — e.g., a board that already contains content a later scene restates (which-app v1's repetition: the big-three board ends with the three "asks" questions, and the old Scene 3 showed the same three questions again as stickies).

- The **prompt box is the high-authority channel**; source documents are treated as content. Never move the script into a source (tested: it leaks — the video illustrates the spec).
- **NotebookLM rejects photoreal-people image sources.** Of the staged illustrations, the two painterly ones (chinese-room, context-window-window) uploaded fine; the photorealistic ones with visible faces and brand marks were refused (content filter, not format — the files are byte-identical in structure). Illustrations meant for video sourcing must be drawn/painterly, faces stylized or from behind, no real logos or trade dress. The four affected prompts (questions-matter, ai-is-different, where-ai-works-best, which-app) run in describe-the-scene mode until ChatGPT re-dos exist.
- **Lesson-box jpgs are the best video source yet** (questions-matter pilot, 2026-07-06): a 1600x900 capture of a lesson card grid, composed on the page-background color with text clear of the 16:9 crop zone, reproduced pixel-crisp — and the engine added narration-synced highlight sweeps over the static grid on its own. Use this for any verbatim-critical scene; capture via headless browser at 2x zoom. When the board IS a lesson element, `scripts/capture-board.sh` does this composition for you (run by hand, never automatic — see its header); composed variants that exist on no page still need a one-off page.
- **The engine can insert its own mid-video chapter cards** (welcome intake, 2026-07-07): an ~8s off-prompt segment — invented neural-net diagram b-roll, then a dark "Lesson 1: Architecture" title card — appeared at ~1:00, right where narration promises "the real machinery," despite NO TITLE CARD and ONLY THE SCENES LISTED. Ban it by name: rule 3 in every prompt now lists "chapter-title" among forbidden extra scenes, and rule 1 in welcome additionally bans mid-video chapter/lesson-number cards explicitly. Watch for it at topic-shift moments in narration.
- **The engine can insert Getty stock photos despite the master-prompt ban.** When narration names real people or places (Socrates, Einstein, Athens), it may cut to watermarked archival photographs. Reinforce per-prompt: name the figures and require they be drawn.
- **Illustration-as-source works on the new engine, full-bleed only** (does-ai-think canary, 2026-07-06; supersedes the Jul-4 "four tests, four redraws" finding). Referencing an attached illustration by filename reproduces it with near-perfect fidelity and no leakage into other scenes — but always full-frame: "framed inset on light canvas" and added-label instructions are ignored, and the 3:2 image is cropped to 16:9, clipping edge text mid-word. If an illustration will be a video source, keep critical text out of the outer ~15% or export a 16:9 variant, and put any required caption in the narration, not the scene spec.
- **Never embed style-reference frames or illustration images in any source**; they get re-rendered as content scenes (a style frame from another lesson showed up mid-video) and induce fake "reference sheet" annotations.
- **Never ask for text inside a drawing** — it renders as gibberish handwriting. Verbatim text goes in separate pills, stickies, or black-ink printed labels.
- On-screen text specs are directional: the generator paraphrases labels even when told "verbatim." The narrative arc carries the exact content.
- Prefer static scenes over timed reveals: draw complex layouts complete and let narration walk them.
