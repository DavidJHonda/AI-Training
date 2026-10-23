# Work With AI Video Kits

Prep status is controlled by `gemini-notebook/upload-sets.json`. Any lesson listed in
`needs_preparation` requires a fresh kit; older “materials ready” or upload directions
below describe historical work and do not authorize reuse.

> **Method note (2026-09-21):** per-lesson entries below dated before 2026-09-20 describe the previous preparation method (Scene/Takeaway labels, withheld face boards with "reserved" narration, prompts without a verbatim list, beat spine, or VOICE block). Rebuild a lesson's Markdown and prompt to the "Prepare a new lesson" procedure in `scripts/video/PREPARATION.md`, add it to `gemini-notebook/upload-sets.json`, and run the sync before rolling it. Entries that say they are on the 2026-09-20 recipe are current.

Rebuilt 2026-09-14 under the speak-the-answers method (see `scripts/video/README.md`, "Speak the answers", and `EDIT-SPEC.md`). Every Markdown was rewritten from the live page and the boards as they render today, with each board's text written out as prose beneath its image; every upload copy in `lessons/` is byte-for-byte the page asset, renumbered in page order. Each prompt is self-contained and under 500 words. Boards with visible faces are never uploaded; the prompt reserves their narration and the real board is inserted in editing. Close copies were rendered fresh from the page's CLOSE_BOARDS (`make_close_board.py --lesson <id>`). Per-lesson upload checklists: `gemini-notebook/<slug>/README.txt` (registered lessons) or `UPLOADS.txt` (manual kits).

| Lesson | Markdown | Prompt | Notebook sources | Post-production only (faces) | Status |
|---|---|---|---|---|---|
| Opener | `lessons/Opener-Work.md` | `gemini-notebook/work-with-ai-opener/PROMPT.txt` | current refrain, same-tool faceless stand-in, section map, close | canonical same-tool board | Rebuilt 2026-09-26 on current recipe; one full Notebook reroll prepared. Upload from `gemini-notebook/work-with-ai-opener/upload/`. Compare narration with original live video before editing. |
| AI Is Different | `lessons/ai-is-different.md` | `gemini-notebook/ai-is-different/PROMPT.txt` | password rules, cooking analogy (text-only upload variant), current close | canonical illustrated cooking board | Rebuilt 2026-10-09 for a complete reroll from the revised page. Four upload files: Markdown plus three boards. See `gemini-notebook/ai-is-different/PREP-NOTES.md`. Installed video unchanged; no new generation yet. |
| Where AI Works Best | `lessons/where-ai-works-best.md` | `gemini-notebook/where-ai-works-best/PROMPT.txt` | face-free course-building comparison, two canonical EE-2FB strength boards, close | canonical course-building board | Updated 2026-10-23: approved shorter explanations and two examples per strength. v11 shipped locally, pending batch deployment: 2:53.8 with stationary boards and section highlights. Upload from `gemini-notebook/where-ai-works-best/upload/`. |
| Your Home Base (retitled from Which App? 2026-09-15; kit files keep the which-app slug for now) | `lessons/which-app.md` | **retired; fresh prep required** | which-app-1-big-three, which-app-3-how-we-used, which-app-4-close | which-app-2-home-base | materials ready, roll pending |
| Questions Matter | `lessons/questions-matter.md` | **retired; fresh prep required** | questions-matter-2-value-lives, questions-matter-3-four-qualities, questions-matter-4-close | questions-matter-1-answers-faster | materials ready, roll pending |
| Prompting Matters | `lessons/prompting-matters.md` | **retired; fresh prep required** | art-of-prompting-1-good-question, art-of-prompting-2-four-moves, art-of-prompting-3-close | none | materials ready, roll pending |
| Context Matters | `lessons/context-matters.md` | `gemini-notebook/context-matters/PROMPT.txt` | context-window-same-question-faceless and context-window-five-sources-faceless (gemini-notebook/context-matters/assets/), context-window-head-start, context-window-outside-the-window, context-window-close | context-window-same-question, context-window-five-sources (canonical boards replace the faceless variants in post) | **v4 SHIPPED 2026-09-21** (cache key 20260921ship6, pill 4 min): roll 2 of 2026-09-21 as the whole narration, plus roll 1's why-beat and the live v3's Saved Memory word, both grafted; the Same Question board leaves at 0:57 and the live v3's own footage carries the stretch after it; canonical Boards 1-4, the five-sources board as an illustration walk, Head Start and Outside the Window dense with section rings and zoom-and-pan; standard close. Review: video-audit/context-window-reroll-2026-09-21/ |
| Evaluation Matters | `lessons/evaluation-matters.md` | `gemini-notebook/evaluation-matters/PROMPT.txt` | current Markdown plus five canonical boards | none | Complete reroll ready 2026-10-23. Current live video remains an editing donor. See `gemini-notebook/evaluation-matters/PREP-NOTES.md` and `DONOR.json`; these supersede historical instructions below. |
| Critical Thinking | `lessons/critical-thinking.md` | **retired; fresh prep required** | critical-thinking-1-equation, critical-thinking-3-five-habits, critical-thinking-4-close | critical-thinking-2-two-reactions | materials ready, roll pending |

Notes:
- Opener (2026-09-26): upload the current canonical refrain, map, and close plus the face-free Same Tool variant. The canonical Same Tool board contains visible faces and is inserted only during editing. The prompt requests the full lesson with exact opening, transition, approved context sentence, takeaway, and closing audio. The three external-voice repair attempts were rejected; generate a complete Notebook roll for comparison. See `gemini-notebook/work-with-ai-opener/README.txt` for the current upload and save instructions. Older preparation notes above do not govern this rebuilt entry.
- AI Is Different (2026-10-09): the current preparation supersedes the September 26 six-board kit. Upload only the four files in `gemini-notebook/ai-is-different/upload/`. The cooking board contains a visible robot face, so its same-size text-only variant is uploaded; restore the illustrated EE-2FB board during editing. Password → playlist → learned patterns → cooking → structured/unstructured data → brief downside → current close. The former mechanics, PS5, Kryptonite, scams, deepfakes, and guardrail teaching is excluded. The prompt and Markdown end with “Different jobs need different tools.” and “Choose the tool that fits the work.”
- Where AI Works Best (2026-09-26): all six boards are included; the course-building board uses a face-free A+/C-minus comparison. Require all five takeaways, the many-examples explanation, the accuracy/fit qualification, and both closing lines. Request drawings of existing examples to break the long continuous board run; final board timing is decided from the returned roll. Canonical page boards and current video are unchanged. Three rolls returned 2026-09-26 (`Prompts/where-ai-works-best-1/2/3.mp4`): none KEEP alone, roll 3 is the base with seven grafts from rolls 1-2; review + 1b plan in `video-audit/where-ai-works-best-reroll-review-2026-09-26/REVIEW.md`, plan approved 2026-09-27; review copies v6 then v7 built; v7 (`Prompts/evaluate-the-results-v7.mp4`) drops the Check Before You Use section at David's request, and the board was removed from the page the same day. Record `video-audit/evaluate-the-results-v7-2026-09-27/REVIEW.md`. SHIPPED 2026-09-27 (cache key 20260927ship2).
- Evaluation Matters (2026-09-26): current page teaching retained, with named checks and required lines separated for narration. All six boards supplied; Check Before You Use uses a face-free upload variant preserving the March 1 / February 15 evidence comparison. The prompt requests relevant drawings within the explanations to avoid another continuous board run. Existing donor material is insufficient; no external replacement voice. Returned roll must be checked for complete narration and useful visual variety before editing. Three rolls returned 2026-09-27 (`Prompts/evaluate-the-results-1/2/3.mp4`): none KEEP alone; roll 3 = narration base, pictures from rolls 1-2 break its 168 s board run; review + plan in `video-audit/evaluate-the-results-reroll-review-2026-09-27/`, plan approved 2026-09-27; review copies v6 then v7 built; v7 (`Prompts/evaluate-the-results-v7.mp4`) drops the Check Before You Use section at David's request, and the board was removed from the page the same day. Record `video-audit/evaluate-the-results-v7-2026-09-27/REVIEW.md`. SHIPPED 2026-09-27 (cache key 20260927ship2).
- Which App: the old `which-app-3-close.jpg` was actually the Pick a Home Base board (faces), mislabeled; replaced by a rendered close.
- Prompting Matters: the page now shows the four moves on one board; the old per-move captures (`-2-move-1` … `-4-move-3`) are deleted.
- Context Matters: the five-sources board (`context-window-1.jpg` on the page) has a photo-style person in profile at the left edge, so it is post-only like the car board. The old captures (`-1-luke-nate`, `-2-outside`, `-3-five-sources`) are deleted; the head-start and outside boards are the page's own `-v1`/`-v2` assets.
- Critical Thinking: the page uses the v3 equation, v2 two-reactions, and v3 five-habits boards; all earlier generations and the retired "One More" board are deleted from `lessons/`.
- Prompts say "do not narrate the TRY IT" where the lesson has one; the Markdown carries no TRY IT text.

## Prompting Matters recap layout — September 27, 2026

The lesson page and preparation asset `course-assets/prompting-matters/prompting-matters-good-question.jpg` now use the compact four-card layout with numbered circles above the headings, titled “Four Qualities of a Good Question.” All four definitions and the takeaway retain the previous board’s exact wording. Renderer: `scripts/video/render_art_of_prompting_recap.py`. The existing MP4 still contains the illustrated layout; its narration is unchanged. Any later visual sync must replace the old two-by-two camera and ring coordinates for this board.

## Evaluation Matters process reroll — September 27, 2026

David requested a full reroll because no existing version walks through the path. The current overview is “How to Evaluate an AI Answer”; the four stage boards are Quick Pass, Dig Deeper?, Dig Deeper, and Your Move. The overview includes the two short cues and the larger two-line decision label. Each stage board has its highlighted map; only the overview shows the Fix It return loop.

The Markdown now speaks the arrows as complete routes. The prompt requires this uninterrupted walkthrough before the individual stage explanations: start at Quick Pass, reach the decision diamond, follow Yes through Dig Deeper to Your Move, follow No straight to Your Move, name the three outcomes, and follow Fix It back to Quick Pass. All three route sentences are required verbatim. Hold the complete overview while narrating these paths. Later scenes can illustrate the existing examples.

Upload all seven files in `gemini-notebook/evaluation-matters/upload/`. Paste `gemini-notebook/evaluation-matters/PROMPT.txt` in the customization field. Save the returned raw video as `Prompts/evaluation-matters-reroll.mp4`, or the next unused numbered reroll filename. The removed scholarship-deadline comparison is excluded. The six boards are byte-identical to the canonical course assets. No new generation has been run and the current finished video has not been changed.

Review the returned narration first: each arrow and both routes must be spoken, the optional dig must remain optional, and only Fix It loops back. A list of stage names alone does not meet this reroll’s purpose. The new board layouts need new camera and ring coordinates during editing.

## Where AI Works Best board revision 2026-10-23

Page, lesson Markdown, and Notebook prep now use two EE-2FB boards in place of the four standalone strength boards. Each strength retains the approved explanation and two original examples. Opening comparison, vast-exposure explanation, close, and activities stay in place. Renderer: `scripts/video/render_where_ai_works_best_boards.cjs`; copy/art: `scripts/video/assets/where-ai-works-best-simplified/`. Approved v11 is installed locally (2:53.8), pending batch deployment. It uses the two boards without zoom or pan, highlighting each full card, description, then the whole Examples section. Two examples per strength; repeated explanations and spoken strength banners removed. Earlier September prep instructions above are historical.

## Evaluation Matters simplification — October 23, 2026

Current source supersedes the September reroll instructions above. Overview unchanged; Quick Pass retains all three explanations but drops its repeated banner. Dig Deeper? remains a two-card board (task and stakes), preceded by the knowledge-gap transition. Dig Deeper combines five checks into three. Your Move is short lesson text; its board is no longer displayed or uploaded. The close and TRY IT scenarios remain; TRY IT instructions match the revised criteria. Five supplied boards including close. Existing video is unchanged and awaits alignment.

### Three-step overview follow-up — October 23, 2026

The overview now reads Do a Quick Review → Does It Need a Closer Look? → Make Your Move. The middle cue says “If needed, dig deeper. Choose the checks that fit.” The diamond, Yes/No branches, outcome buttons and return loop are removed. Mini maps on the stage boards and lesson headings use the same labels; deciding and deeper checking share the middle step. Checking the revised answer remains in Make Your Move prose. Current prep supersedes all earlier flowchart narration requirements. Video remains unchanged.

### Illustrated EE-FLOW overview — October 23, 2026

How to Evaluate an AI Answer now uses Check the Claim’s shared white stage, three 16:9 illustrations, numbered markers and neutral arrows. Middle overview label: “Take a Closer Look?”; full question remains in lesson headings and small stage maps. No loop or outcome buttons. Renderer: `scripts/video/render_evaluation_flow.py`; generated panel sources and prompts: `scripts/video/assets/evaluation-flow/`. Existing video remains unchanged.

### Closer-look explanations restored — October 23, 2026

The two decision cards retain their original explanations and examples: factual answer / draft / plan, and movie / scholarship / injury. Can You Judge It? remains removed; the knowledge-gap transition stays above the board. The three-step illustrated overview and other boards are unchanged.

### Purple quick-review flow — October 23, 2026

Do a Quick Review now uses EE-FLOW: Read → Understand → Validate, with the exact existing body copy. Purple illustrations, markers and headings match the overview’s first step. No corner mini map. Renderer: `scripts/video/render_evaluation_quick_review_flow.py`; assets and prompts: `scripts/video/assets/evaluation-quick-review/`. Video remains unchanged.

### Blue decision and deeper-check cards — October 23, 2026

Does It Need a Closer Look? now uses EE-2FB; Dig Deeper uses EE-3FB. Both use blue illustrations and headings matching the overview middle step. Exact approved explanations and banners remain. Neither has a corner flowchart, numbering, or arrows. Renderer: `scripts/video/render_evaluation_cards.cjs`; source copy, artwork, and built-in imagegen prompts: `scripts/video/assets/evaluation-blue-cards/`. This supersedes the mini-map instructions above. Existing video remains unchanged and needs new board framing when updated.

### Decision guidance integrated into Dig Deeper — October 23, 2026

Overview middle heading is Take a Closer Look (no question mark). The page kickers are Start Here and Sometimes You Dig Deeper. Do a Quick Review has a purple circle 1 next to its title, using the overview marker style. Dig Deeper now starts with an assignment-style white panel and blue left rule: What Kind of Task / How Much Is Riding on It, with the full original explanations. The separate closer-look board is removed from the lesson and prep uploads, retained on disk. Four boards remain including close. Video is unchanged.

### Numbered stage boards and Make Your Move restored — October 23, 2026

Dig Deeper is now titled Take a Closer Look, with a blue step-2 circle matching the quick-review step-1 marker. The two task-and-stakes headings now match the lower cards at 40 px bold. Make Your Move is restored as three text cards (Use It, Fix It, Walk Away) using current lesson wording, a teal step-3 title marker, and the original takeaway. No old mini flowchart. Five boards including close are displayed and prepared. Renderer: `scripts/video/render_evaluation_cards.cjs`. Existing video remains unchanged.

### Teal full-bleed Make Your Move — October 23, 2026

Make Your Move now uses EE-3FB: three 16:9 teal illustrations above Use It, Fix It, and Walk Away. The board keeps its existing text, step-3 marker and takeaway. Teal #0e8f86 matches the overview. Built-in imagegen art and prompts: `scripts/video/assets/evaluation-move/`; canonical renderer: `scripts/video/render_evaluation_cards.cjs`. The video is unchanged.

### Stage banners removed — October 23, 2026

Take a Closer Look and Make Your Move no longer have takeaway banners. Card text, illustrations and numbered title markers are preserved. The Closing Message still reads “The tool answers. You evaluate. Read. Understand. Validate.” The transition from the decision introduction to checking methods is under discussion, with no new transition added yet.

### In-board checking transition — October 23, 2026

Take a Closer Look now bridges the task-and-stakes panel and the three illustrated cards with a small blue heading, WAYS TO TAKE A CLOSER LOOK, and “Choose the checks that fit the task.” Plain text and spacing, no extra box. Both stage banners remain removed.

### Closer-look section headings enlarged — October 23, 2026

DOES IT NEED A CLOSER LOOK? and WAYS TO TAKE A CLOSER LOOK now use 40 px bold blue type matching the card titles. The supporting sentence “Choose the checks that fit the task.” is removed from the board. The overview and introductory lesson prose remain unchanged.

### Evaluation closing covers the full process — October 23, 2026

Main message remains “The tool answers. You evaluate.” Subtext is now “Review the answer. Take a closer look when needed. Decide what to do next.” Page, closing image, Markdown and Notebook prep agree. The existing video narration is unchanged and needs the updated close in the next rebuild.

### Split decision cards and connecting sentence — October 23, 2026

Take a Closer Look now presents task and stakes in two separate white cards. Between these cards and WAYS TO TAKE A CLOSER LOOK, the approved connecting line reads “The more that depends on the answer, the more carefully you should check it.” Thin rules flank the line. The existing frame, blue coloring, numbered title, illustrations and full-bleed checking cards remain. No banner. Video remains unchanged.

### Closer-look heading hierarchy — October 23, 2026

DOES IT NEED A CLOSER LOOK? and WAYS TO TAKE A CLOSER LOOK now use 28 px / 36 px blue type. Card titles remain 40 px. Copy and other layout treatments are unchanged.

### Complete Evaluation Matters reroll prepared — October 23, 2026

Current authority: `gemini-notebook/evaluation-matters/PREP-NOTES.md`, the 476-word `PROMPT.txt`, and the six generated uploads. Full narration is requested; the live 4:15.37 video is retained as an editing donor only. `DONOR.json` pins its path and hash. Fresh overview, transitions, consolidated checks and full-process close take priority; compatible old passages can repair the reroll after listening and timing verification. Current board labels, 28 px section headings, 12 px label gaps, separate decision cards, connecting sentence, and banner-free blue/teal boards are all in the upload assets. No generation, build, or shipment has occurred.
