# Source artwork and intermediate files: review list

Prepared September 15, 2026. **The six confirmed sources in section 1 were deleted with approval. All other candidates remain for review.**

This inventory covers the managed `course-assets/` and `scripts/video/assets/` folders. It lists exact files, not entire folders for deletion. Archived backups, video-audit captures, review output folders, finished videos, fonts, lesson text, and executable scripts are outside this deletion list.

Items are not automatically safe to delete just because they are absent from the website. The component artwork and confirmed source pairs can be retired under your finished-boards-only approach; associated build steps would then need to be retired or updated. Older/supporting boards require your visual review because some have their own video use.

**Correction: Keep `make-your-move-1-note.jpg`. It is used by the video builder and, from September 15, the website. The superseded `make-your-move-note-v1.png` was removed with approval.**

**Welcome pilot: Keep `welcome-1-why-go-deeper.jpg`; the website and video now share this unchanged image.**

## 1. Completed: confirmed source-to-finished pairs

6 source files deleted September 15, 2026. Finished files on the right were preserved byte-for-byte. The legacy build scripts now verify and report the finished files.

| Deleted source | Keep finished board | Build script |
| --- | --- | --- |
| `course-assets/finish-smarter-opener/five-big-ideas-keepsake-art-clean.png` | [five-big-ideas-keepsake.png](/Users/davidobrien/Developer/AI-Training/course-assets/finish-smarter-opener/five-big-ideas-keepsake.png) | [build-five-big-ideas-keepsake.py](/Users/davidobrien/Developer/AI-Training/scripts/build-five-big-ideas-keepsake.py) |
| `course-assets/understand-ai-opener/opener-understand-under-hood-art-v3.png` | [opener-understand-under-hood-v3.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/understand-ai-opener/opener-understand-under-hood-v3.jpg) | [render_under_the_hood_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_under_the_hood_board.py) |
| `course-assets/honesty-and-privacy/privacy-how-much-share-v5.png` | [honesty-and-privacy-3-privacy.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-and-privacy-3-privacy.jpg) | [render_privacy_how_much_share.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_privacy_how_much_share.py) |
| `course-assets/honesty-and-privacy/privacy-whole-photo.png` | [honesty-and-privacy-4-share-only.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-and-privacy-4-share-only.jpg) | [render_honesty_privacy_supporting.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_honesty_privacy_supporting.py) |
| `course-assets/honesty-and-privacy/honesty-use-ai-help-follow-rules.png` | [honesty-and-privacy-1-school.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-and-privacy-1-school.jpg) | [render_honesty_privacy_supporting.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_honesty_privacy_supporting.py) |
| `course-assets/your-choices/your-choices-choose-tool-v3.png` | [your-choices-1-choose-tool.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-1-choose-tool.jpg) | [render_your_choices_tool.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_your_choices_tool.py) |

## 2. Component artwork in the build-assets folder

92 images: art sheets, panels, comparison artwork, base images, and character references. These are not directly displayed by the course website. A finished replacement has not been independently matched for every item in this section; use the linked images and build references to review them.

### scripts/video/assets

- [ ] [does-ai-think-compare-clean.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/does-ai-think-compare-clean.png) — build references: [render_work_with_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_work_with_ai_retrofit_review.py), [prepare_avoid_traps_generated_art.py](/Users/davidobrien/Developer/AI-Training/scripts/video/prepare_avoid_traps_generated_art.py), [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py) (additional references in the JSON inventory)

### scripts/video/assets/does-ai-think-unified

- [ ] [what-ai-does.jpg](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/does-ai-think-unified/what-ai-does.jpg) — build references: [render_does_ai_think_unified_comparison.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_does_ai_think_unified_comparison.py)
- [ ] [when-you-think.jpg](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/does-ai-think-unified/when-you-think.jpg) — build references: [render_does_ai_think_unified_comparison.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_does_ai_think_unified_comparison.py)

### scripts/video/assets/editorial-avoid-traps

- [ ] [engagement-approved-stop-art.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/engagement-approved-stop-art.png) — build references: [prepare_avoid_traps_generated_art.py](/Users/davidobrien/Developer/AI-Training/scripts/video/prepare_avoid_traps_generated_art.py), [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py), [render_engagement_stop_frame.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_engagement_stop_frame.py) (additional references in the JSON inventory)

### scripts/video/assets/editorial-avoid-traps/bias-mechanisms

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/bias-mechanisms/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/bias-mechanisms/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/bias-questions

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/bias-questions/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/bias-questions/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/characters

- [ ] [luke-reference.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/characters/luke-reference.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [nate-reference.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/characters/nate-reference.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/comparisons

- [ ] [fake-two-tests.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/comparisons/fake-two-tests.png) — build references: [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py), [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)
- [ ] [flattery-vs-feedback.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/comparisons/flattery-vs-feedback.png) — build references: [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py), [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)
- [ ] [human-vs-ai.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/comparisons/human-vs-ai.png) — build references: [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py), [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)
- [ ] [stop-vs-engagement.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/comparisons/stop-vs-engagement.png) — build references: [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py), [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)
- [ ] [support-words-vs-action.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/comparisons/support-words-vs-action.png) — build references: [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py), [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)

### scripts/video/assets/editorial-avoid-traps/document-flow

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/document-flow/art-sheet.png) — build references: [render_document_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_document_trap_boards.py)
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/document-flow/source-grid.png) — build references: [render_document_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_document_trap_boards.py)

### scripts/video/assets/editorial-avoid-traps/document-moves

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/document-moves/art-sheet.png) — build references: [render_document_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_document_trap_boards.py)
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/document-moves/source-grid.png) — build references: [render_document_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_document_trap_boards.py)

### scripts/video/assets/editorial-avoid-traps/engagement-scroll

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/engagement-scroll/art-sheet.png) — build references: [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)

### scripts/video/assets/editorial-avoid-traps/fake-checks

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/fake-checks/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/fake-checks/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/fake-reasons

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/fake-reasons/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/fake-reasons/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/hallucination-types

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/hallucination-types/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/hallucination-types/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/hallucination-why

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/hallucination-why/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/hallucination-why/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/mind-eliza

- [ ] [art-sheet-ai-first.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/mind-eliza/art-sheet-ai-first.png) — build references: [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)
- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/mind-eliza/art-sheet.png) — build references: [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/mind-eliza/source-grid.png) — build references: [render_mind_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_mind_trap_boards.py)

### scripts/video/assets/editorial-avoid-traps/praise-flow

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/praise-flow/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/praise-flow/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/rag-limits

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/rag-limits/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/rag-limits/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/support

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/support/art-sheet.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [source-grid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/support/source-grid.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-avoid-traps/support-danger

- [ ] [01-leave-chat.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/support-danger/01-leave-chat.png) — build references: [prepare_avoid_traps_generated_art.py](/Users/davidobrien/Developer/AI-Training/scripts/video/prepare_avoid_traps_generated_art.py)
- [ ] [02-do-it-now.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/support-danger/02-do-it-now.png) — build references: [prepare_avoid_traps_generated_art.py](/Users/davidobrien/Developer/AI-Training/scripts/video/prepare_avoid_traps_generated_art.py)
- [ ] [03-safety-rule.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/support-danger/03-safety-rule.png) — build references: [prepare_avoid_traps_generated_art.py](/Users/davidobrien/Developer/AI-Training/scripts/video/prepare_avoid_traps_generated_art.py)
- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-avoid-traps/support-danger/art-sheet.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/editorial-embrace/big-downside-guardrails

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/big-downside-guardrails/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/big-downside-voice-clone

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/big-downside-voice-clone/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/big-upside-discovery

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/big-upside-discovery/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/big-upside-help

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/big-upside-help/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/data-footprint

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/data-footprint/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/pace-accelerants

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/pace-accelerants/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/pace-ai-capability

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/pace-ai-capability/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/pace-ai-improvement

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/pace-ai-improvement/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/rise-agents-rogue

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/rise-agents-rogue/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/work-automate-augment

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/work-automate-augment/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/work-four-shapes

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/work-four-shapes/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-embrace/work-what-changes

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-embrace/work-what-changes/art-sheet.png) — build references: [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/editorial-flow/honesty-integrity

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-flow/honesty-integrity/art-sheet.png) — build references: [render_honesty_integrity_flow.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_honesty_integrity_flow.py)

### scripts/video/assets/editorial-flow/rise-of-agents

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-flow/rise-of-agents/art-sheet.png) — build references: [render_editorial_flow.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_flow.py)

### scripts/video/assets/editorial-full-bleed/be-curious-four-ways

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/be-curious-four-ways/art-sheet.png) — build references: [render_editorial_full_bleed_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_full_bleed_batch.py)

### scripts/video/assets/editorial-full-bleed/be-flexible-four-steps

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/be-flexible-four-steps/art-sheet.png) — build references: [render_editorial_full_bleed_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_full_bleed_batch.py)

### scripts/video/assets/editorial-full-bleed/context-window-head-start

- [ ] [personalization.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/context-window-head-start/personalization.png) — build references: [render_context_window_head_start.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_context_window_head_start.py)
- [ ] [projects.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/context-window-head-start/projects.png) — build references: [render_context_window_head_start.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_context_window_head_start.py)
- [ ] [saved-memory.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/context-window-head-start/saved-memory.png) — build references: [render_context_window_head_start.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_context_window_head_start.py)

### scripts/video/assets/editorial-full-bleed/creative-thinking-practice

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/creative-thinking-practice/art-sheet.png) — build references: [render_editorial_full_bleed_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_full_bleed_batch.py)

### scripts/video/assets/editorial-full-bleed/creative-thinking-professions

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/creative-thinking-professions/art-sheet.png) — build references: [render_editorial_full_bleed_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_full_bleed_batch.py)

### scripts/video/assets/editorial-full-bleed/make-your-move-actions

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/make-your-move-actions/art-sheet.png) — build references: [render_editorial_full_bleed_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_full_bleed_batch.py)

### scripts/video/assets/editorial-full-bleed/make-your-move-skills

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/make-your-move-skills/art-sheet.png) — build references: [render_editorial_full_bleed_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_full_bleed_batch.py)

### scripts/video/assets/editorial-full-bleed/people-skills-why-matter

- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/editorial-full-bleed/people-skills-why-matter/art-sheet.png) — build references: [render_editorial_full_bleed_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_full_bleed_batch.py)

### scripts/video/assets/evaluate-results

- [ ] [decide-base.jpg](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/evaluate-results/decide-base.jpg) — build references: [render_evaluate_results_dig.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_dig.py), [render_evaluate_results_quick_pass.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_quick_pass.py), [render_evaluate_results_move.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_move.py) (additional references in the JSON inventory)
- [ ] [dig-base.jpg](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/evaluate-results/dig-base.jpg) — build references: [render_evaluate_results_dig.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_dig.py), [render_evaluate_results_quick_pass.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_quick_pass.py), [render_evaluate_results_move.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_move.py) (additional references in the JSON inventory)
- [ ] [move-base.jpg](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/evaluate-results/move-base.jpg) — build references: [render_evaluate_results_dig.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_dig.py), [render_evaluate_results_quick_pass.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_quick_pass.py), [render_evaluate_results_move.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_move.py) (additional references in the JSON inventory)
- [ ] [quick-pass-base.jpg](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/evaluate-results/quick-pass-base.jpg) — build references: [render_evaluate_results_dig.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_dig.py), [render_evaluate_results_quick_pass.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_quick_pass.py), [render_evaluate_results_move.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_evaluate_results_move.py) (additional references in the JSON inventory)

### scripts/video/assets/mind-trap

- [ ] [eliza-vignette-v1.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/mind-trap/eliza-vignette-v1.png) — build references: [build_mind_trap_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_mind_trap_review.py)

### scripts/video/assets/people-skills-ee4fb

- [ ] [art-sheet-v2.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/people-skills-ee4fb/art-sheet-v2.png) — build references: [render_people_skills_ee4fb.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_people_skills_ee4fb.py)
- [ ] [art-sheet.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/people-skills-ee4fb/art-sheet.png) — build references: [render_people_skills_ee4fb.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_people_skills_ee4fb.py)
- [ ] [notice-unsaid.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/people-skills-ee4fb/notice-unsaid.png) — build references: [render_people_skills_ee4fb.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_people_skills_ee4fb.py)

### scripts/video/assets/start-smarter/types-of-ai

- [ ] [generative-ai.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/start-smarter/types-of-ai/generative-ai.png) — build references: [render_two_kinds_example_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_two_kinds_example_review.py), [render_types_of_ai_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_types_of_ai_review.py)
- [ ] [recommendation-ai.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/start-smarter/types-of-ai/recommendation-ai.png) — build references: [render_two_kinds_example_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_two_kinds_example_review.py), [render_types_of_ai_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_types_of_ai_review.py)

### scripts/video/assets/start-smarter/why-learn-ai-thrive

- [ ] [nothing-to-unlearn.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/start-smarter/why-learn-ai-thrive/nothing-to-unlearn.png) — build references: [render_why_learn_ai_thrive_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_why_learn_ai_thrive_board.py)
- [ ] [this-is-your-time.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/start-smarter/why-learn-ai-thrive/this-is-your-time.png) — build references: [render_why_learn_ai_thrive_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_why_learn_ai_thrive_board.py)
- [ ] [youll-move-faster.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/start-smarter/why-learn-ai-thrive/youll-move-faster.png) — build references: [render_why_learn_ai_thrive_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_why_learn_ai_thrive_board.py)

### scripts/video/assets/work-with-ai

- [ ] [where-ai-works-best-titleless-v2.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/where-ai-works-best-titleless-v2.png) — build references: [render_work_with_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_work_with_ai_retrofit_review.py), [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/work-with-ai/card-illustrations

- [ ] [books.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/card-illustrations/books.png) — build references: [render_work_with_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_work_with_ai_retrofit_review.py), [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)
- [ ] [reasoning.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/card-illustrations/reasoning.png) — build references: [render_work_with_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_work_with_ai_retrofit_review.py), [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)
- [ ] [transform.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/card-illustrations/transform.png) — build references: [render_work_with_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_work_with_ai_retrofit_review.py), [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)
- [ ] [variation.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/card-illustrations/variation.png) — build references: [render_work_with_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_work_with_ai_retrofit_review.py), [render_embrace_editorial_batch.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_batch.py)

### scripts/video/assets/work-with-ai/how-ai-learns-patterns

- [ ] [one-familiar-pattern.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/how-ai-learns-patterns/one-familiar-pattern.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [patterns-everywhere.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/how-ai-learns-patterns/patterns-everywhere.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/work-with-ai/how-training-works

- [ ] [check.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/how-training-works/check.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [corrects.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/how-training-works/corrects.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [guesses.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/how-training-works/guesses.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [reads.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/how-training-works/reads.png) — no literal reference found; may be selected dynamically by a build script

### scripts/video/assets/work-with-ai/whats-an-llm

- [ ] [language.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/whats-an-llm/language.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [large.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/whats-an-llm/large.png) — no literal reference found; may be selected dynamically by a build script
- [ ] [model.png](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/work-with-ai/whats-an-llm/model.png) — no literal reference found; may be selected dynamically by a build script

## 3. Older or supporting images beside current boards

137 files. These are not direct website references. **They are not all confirmed source parts or duplicates.** Some are complete boards, numbered video versions, or alternate lesson imagery. Review each against the current lesson assets listed for that folder before deciding.

### course-assets/ai-is-different

Current website assets: [ai-is-different-1-rules.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-1-rules.jpg), [ai-is-different-2-learn-once.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-2-learn-once.jpg), [ai-is-different-3-rules-vs-patterns.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-3-rules-vs-patterns.jpg), [ai-is-different-4-structured.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-4-structured.jpg), [ai-is-different-5-kryptonite.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-5-kryptonite.jpg)

- [ ] [ai-is-different-kryptonite.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-kryptonite.jpg) — 2 build/reference file(s); e.g. [render_ai_is_different_kryptonite_board.sh](/Users/davidobrien/Developer/AI-Training/scripts/video/render_ai_is_different_kryptonite_board.sh)
- [ ] [ai-is-different-learn-once.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-learn-once.jpg) — 3 build/reference file(s); e.g. [build_ai_is_different_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_ai_is_different_review.py)
- [ ] [ai-is-different-side-by-side.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different-side-by-side.jpg) — 1 build/reference file(s); e.g. [ai-is-different-side-by-side-highlights.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/ai-is-different-side-by-side-highlights.json)
- [ ] [ai-is-different.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-different/ai-is-different.jpg) — 1 build/reference file(s); e.g. [ai-is-different.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/ai-is-different.json)

### course-assets/ai-is-math

Current website assets: [ai-is-math-conditional-probability-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-conditional-probability-editorial.jpg), [ai-is-math-the-math-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-the-math-editorial.jpg), [ai-is-math-two-coins-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-two-coins-editorial.jpg), [ai-is-math-what-comes-next-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-what-comes-next-editorial.jpg)

- [ ] [ai-is-math-1-formula.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-1-formula.jpg) — 2 build/reference file(s); e.g. [render_ai_is_math_board_alternatives.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_ai_is_math_board_alternatives.py)
- [ ] [ai-is-math-1.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-1.jpg) — 1 build/reference file(s); e.g. [ai-is-math-pascal-fermat.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/ai-is-math-pascal-fermat.json)
- [ ] [ai-is-math-2-one-coin.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-2-one-coin.jpg) — 2 build/reference file(s); e.g. [render_ai_is_math_board_alternatives.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_ai_is_math_board_alternatives.py)
- [ ] [ai-is-math-2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-2.jpg) — no literal build reference found
- [ ] [ai-is-math-3-two-coins.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-3-two-coins.jpg) — 1 build/reference file(s); e.g. [ai-is-math-3-two-coins-highlights.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/ai-is-math-3-two-coins-highlights.json)
- [ ] [ai-is-math-4-update.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-4-update.jpg) — 1 build/reference file(s); e.g. [ai-is-math-4-update-highlights.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/ai-is-math-4-update-highlights.json)
- [ ] [ai-is-math-5-autoregressive.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/ai-is-math/ai-is-math-5-autoregressive.jpg) — 2 build/reference file(s); e.g. [render_ai_is_math_board_alternatives.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_ai_is_math_board_alternatives.py)

### course-assets/avoid-traps-opener

Current website assets: [opener-avoid-3-map.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/avoid-traps-opener/opener-avoid-3-map.jpg), [opener-avoid.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/avoid-traps-opener/opener-avoid.jpg)

- [ ] [opener-avoid-1-traps.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/avoid-traps-opener/opener-avoid-1-traps.jpg) — 2 build/reference file(s); e.g. [capture-page-boards.js](/Users/davidobrien/Developer/AI-Training/scripts/capture-page-boards.js)
- [ ] [opener-avoid-2-read-water.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/avoid-traps-opener/opener-avoid-2-read-water.jpg) — 1 build/reference file(s); e.g. [opener-avoid-read-water-current.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/opener-avoid-read-water-current.json)

### course-assets/beyond-the-average

Current website assets: [does-school-matter-1-same-tool.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/beyond-the-average/does-school-matter-1-same-tool.jpg), [does-school-matter-2-future.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/beyond-the-average/does-school-matter-2-future.jpg)

- [ ] [does-school-matter-two-skills.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/beyond-the-average/does-school-matter-two-skills.jpg) — 5 build/reference file(s); e.g. [normalize_alternative_board_titles.sh](/Users/davidobrien/Developer/AI-Training/scripts/video/normalize_alternative_board_titles.sh)
- [ ] [does-school-matter.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/beyond-the-average/does-school-matter.jpg) — 1 build/reference file(s); e.g. [does-school-matter-google.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/does-school-matter-google.json)

### course-assets/big-downside

Current website assets: [big-downside-1-guardrails.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-1-guardrails.jpg), [big-downside-2-jailbreak.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-2-jailbreak.jpg), [big-downside-3-policy-puppetry.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-3-policy-puppetry.jpg), [big-downside-4-voice-clone.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-4-voice-clone.jpg), [big-downside-5-goal-test.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-5-goal-test.jpg), [big-downside-6-safety-timeline.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-6-safety-timeline.jpg)

- [ ] [big-downside-2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-2.jpg) — 1 build/reference file(s); e.g. [render_embrace_editorial_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_review.py)
- [ ] [big-downside-guardrails.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-guardrails.jpg) — 2 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)
- [ ] [big-downside-voice-clone.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-downside/big-downside-voice-clone.jpg) — 1 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)

### course-assets/big-upside

Current website assets: [big-upside-1-protein.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-upside/big-upside-1-protein.jpg), [big-upside-2-discovery.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-upside/big-upside-2-discovery.jpg), [big-upside-3-help.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-upside/big-upside-3-help.jpg), [big-upside-hassabis-timeline.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-upside/big-upside-hassabis-timeline.jpg)

- [ ] [big-upside-discovery.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-upside/big-upside-discovery.jpg) — 2 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)
- [ ] [big-upside-help.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/big-upside/big-upside-help.jpg) — 2 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)

### course-assets/build-your-skills-opener

Current website assets: [opener-build-2-map.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/build-your-skills-opener/opener-build-2-map.jpg)

- [ ] [opener-build-1-creed.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/build-your-skills-opener/opener-build-1-creed.jpg) — 1 build/reference file(s); e.g. [build_opener_build_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_opener_build_review.py)

### course-assets/context-window

Current website assets: [context-window-1-same-question.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/context-window/context-window-1-same-question.jpg), [context-window-2-five-sources.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/context-window/context-window-2-five-sources.jpg), [context-window-3-head-start.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/context-window/context-window-3-head-start.jpg), [context-window-4-outside.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/context-window/context-window-4-outside.jpg)

- [ ] [context-window-2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/context-window/context-window-2.jpg) — no literal build reference found
- [ ] [context-window-luke-nate-ai.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/context-window/context-window-luke-nate-ai.jpg) — 1 build/reference file(s); e.g. [context-window-luke-nate-highlights.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/context-window-luke-nate-highlights.json)
- [ ] [context-window-outside.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/context-window/context-window-outside.jpg) — 3 build/reference file(s); e.g. [board-retrofits-start-work.json](/Users/davidobrien/Developer/AI-Training/scripts/video/board-retrofits-start-work.json)

### course-assets/creative-thinking

Current website assets: [creative-thinking-1-professions.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/creative-thinking/creative-thinking-1-professions.jpg), [creative-thinking-2-practice.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/creative-thinking/creative-thinking-2-practice.jpg)

- [ ] [creative-thinking-practice.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/creative-thinking/creative-thinking-practice.jpg) — no literal build reference found
- [ ] [creative-thinking-professions.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/creative-thinking/creative-thinking-professions.jpg) — no literal build reference found

### course-assets/curious-and-flexible

Current website assets: [curious-and-flexible-1-stay-curious.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/curious-and-flexible/curious-and-flexible-1-stay-curious.jpg), [curious-and-flexible-2-be-flexible.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/curious-and-flexible/curious-and-flexible-2-be-flexible.jpg)

- [ ] [be-curious-four-ways.png](/Users/davidobrien/Developer/AI-Training/course-assets/curious-and-flexible/be-curious-four-ways.png) — no literal build reference found
- [ ] [be-flexible-four-steps.png](/Users/davidobrien/Developer/AI-Training/course-assets/curious-and-flexible/be-flexible-four-steps.png) — no literal build reference found

### course-assets/data-centers

Current website assets: [data-centers-1-data-center.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/data-centers/data-centers-1-data-center.jpg), [data-centers-2-footprint.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/data-centers/data-centers-2-footprint.jpg)

- [ ] [data-centers-footprint.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/data-centers/data-centers-footprint.jpg) — 1 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)

### course-assets/document-trap

Current website assets: [document-trap-1-uploaded.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap-1-uploaded.jpg), [document-trap-2-flow.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap-2-flow.jpg), [document-trap-3-moves.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap-3-moves.jpg)

- [ ] [document-trap-flow-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap-flow-v2.jpg) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [document-trap-moves-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap-moves-v2.jpg) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [document-trap-uploaded-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap-uploaded-v2.jpg) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [document-trap-uploaded-v3.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap-uploaded-v3.jpg) — 3 build/reference file(s); e.g. [render_document_trap_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_document_trap_boards.py)
- [ ] [document-trap.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/document-trap/document-trap.jpg) — 2 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)

### course-assets/does-ai-think

Current website assets: [does-ai-think-1-chinese-room.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/does-ai-think/does-ai-think-1-chinese-room.jpg), [does-ai-think-2-side-by-side.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/does-ai-think/does-ai-think-2-side-by-side.jpg)

- [ ] [does-ai-think-rulebook.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/does-ai-think/does-ai-think-rulebook.jpg) — 8 build/reference file(s); e.g. [normalize_alternative_board_titles.sh](/Users/davidobrien/Developer/AI-Training/scripts/video/normalize_alternative_board_titles.sh)

### course-assets/embeddings

Current website assets: [embeddings-inside-real-model-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-inside-real-model-editorial.jpg), [embeddings-meaning-row-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-meaning-row-editorial.jpg), [embeddings-new-dimension-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-new-dimension-editorial.jpg), [embeddings-student-id-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-student-id-editorial.jpg), [embeddings-taste-test-to-ai-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-taste-test-to-ai-editorial.jpg)

- [ ] [embeddings-2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-2.jpg) — no literal build reference found
- [ ] [embeddings-student-id-notebook.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-student-id-notebook.jpg) — 1 build/reference file(s); e.g. [render_embeddings_student_id_notebook.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embeddings_student_id_notebook.py)
- [ ] [embeddings-taste-three.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-taste-three.jpg) — 2 build/reference file(s); e.g. [render_embeddings_vector_alternative.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embeddings_vector_alternative.swift)
- [ ] [embeddings-taste-two.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings-taste-two.jpg) — 2 build/reference file(s); e.g. [render_embeddings_vector_alternative.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embeddings_vector_alternative.swift)
- [ ] [embeddings.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/embeddings/embeddings.jpg) — no literal build reference found

### course-assets/engagement-trap

Current website assets: [engagement-trap-1-comparison.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/engagement-trap/engagement-trap-1-comparison.jpg), [engagement-trap-2-scroll.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/engagement-trap/engagement-trap-2-scroll.jpg), [engagement-trap.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/engagement-trap/engagement-trap.jpg)

- [ ] [engagement-trap-3-stop.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/engagement-trap/engagement-trap-3-stop.jpg) — 1 build/reference file(s); e.g. [render_engagement_stop_frame.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_engagement_stop_frame.py)

### course-assets/evaluate-the-results

Current website assets: [evaluate-the-results-1-quick-pass.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/evaluate-the-results/evaluate-the-results-1-quick-pass.jpg), [evaluate-the-results-2-decide.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/evaluate-the-results/evaluate-the-results-2-decide.jpg), [evaluate-the-results-3-dig.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/evaluate-the-results/evaluate-the-results-3-dig.jpg), [evaluate-the-results-4-move.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/evaluate-the-results/evaluate-the-results-4-move.jpg), [evaluate-the-results-5-check-before-use.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/evaluate-the-results/evaluate-the-results-5-check-before-use.jpg)

- [ ] [evaluate-the-results.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/evaluate-the-results/evaluate-the-results.jpg) — no literal build reference found

### course-assets/fake-trap

Current website assets: [fake-trap-1-comparison.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-1-comparison.jpg), [fake-trap-2-reasons.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-2-reasons.jpg), [fake-trap-4-checks.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-4-checks.jpg), [fake-trap.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap.jpg)

- [ ] [fake-trap-3-source.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-3-source.jpg) — no literal build reference found
- [ ] [fake-trap-comparison-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-comparison-v2.jpg) — 3 build/reference file(s); e.g. [build_fake_trap_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_fake_trap_review.py)
- [ ] [fake-trap-four-reasons-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-four-reasons-v2.jpg) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [fake-trap-four-reasons-v3.png](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-four-reasons-v3.png) — 2 build/reference file(s); e.g. [build_fake_trap_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_fake_trap_review.py)
- [ ] [fake-trap-four-reasons.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-four-reasons.jpg) — 3 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)
- [ ] [fake-trap-three-checks.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/fake-trap/fake-trap-three-checks.jpg) — 3 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)

### course-assets/finish-smarter-opener

Current website assets: [five-big-ideas-keepsake.pdf](/Users/davidobrien/Developer/AI-Training/course-assets/finish-smarter-opener/five-big-ideas-keepsake.pdf), [five-big-ideas-keepsake.png](/Users/davidobrien/Developer/AI-Training/course-assets/finish-smarter-opener/five-big-ideas-keepsake.png)

- [ ] [five-big-ideas-keepsake-art.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/finish-smarter-opener/five-big-ideas-keepsake-art.jpg) — no literal build reference found

### course-assets/flattery-trap

Current website assets: [flattery-trap-1-comparison.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/flattery-trap/flattery-trap-1-comparison.jpg), [flattery-trap-2-praise-loop.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/flattery-trap/flattery-trap-2-praise-loop.jpg), [flattery-trap-3-sycophancy.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/flattery-trap/flattery-trap-3-sycophancy.jpg), [flattery-trap-4-five-moves.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/flattery-trap/flattery-trap-4-five-moves.jpg)

- [ ] [flattery-trap-comparison-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/flattery-trap/flattery-trap-comparison-v2.jpg) — 3 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [flattery-trap-praise-loop.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/flattery-trap/flattery-trap-praise-loop.jpg) — 3 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)
- [ ] [flattery-trap.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/flattery-trap/flattery-trap.jpg) — 1 build/reference file(s); e.g. [flattery-trap-feedback.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/flattery-trap-feedback.json)

### course-assets/hallucination

Current website assets: [hallucination-1-example.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-1-example.jpg), [hallucination-2-why.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-2-why.jpg), [hallucination-4-check-claim.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-4-check-claim.jpg), [hallucination-real-text-v4.png](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-real-text-v4.png)

- [ ] [hallucination-3-real-text.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-3-real-text.jpg) — 1 build/reference file(s); e.g. [build_hallucination_reroll_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_hallucination_reroll_review.py)
- [ ] [hallucination-real-text-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-real-text-v2.jpg) — 2 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [hallucination-real-text.png](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-real-text.png) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [hallucination-types-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-types-v2.jpg) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [hallucination-types.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-types.jpg) — 3 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [hallucination-why.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination-why.jpg) — 2 build/reference file(s); e.g. [render_hallucination_boards.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_hallucination_boards.swift)
- [ ] [hallucination.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/hallucination/hallucination.jpg) — no literal build reference found

### course-assets/honesty-and-privacy

Current website assets: [honesty-and-privacy-1-school.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-and-privacy-1-school.jpg), [honesty-and-privacy-2-best-practices.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-and-privacy-2-best-practices.jpg), [honesty-and-privacy-3-privacy.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-and-privacy-3-privacy.jpg), [honesty-and-privacy-4-share-only.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-and-privacy-4-share-only.jpg)

- [ ] [honesty-where-the-line-is.png](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/honesty-where-the-line-is.png) — no literal build reference found
- [ ] [privacy-how-much-share-v3.png](/Users/davidobrien/Developer/AI-Training/course-assets/honesty-and-privacy/privacy-how-much-share-v3.png) — no literal build reference found

### course-assets/how-ai-answers

Current website assets: [how-ai-answers-before-answer-begins.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-before-answer-begins.jpg), [how-ai-answers-inference-notebook.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-inference-notebook.jpg), [how-ai-answers-token-by-token.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-token-by-token.jpg), [how-ai-answers-where-answer-begins.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-where-answer-begins.jpg)

- [ ] [how-ai-answers-inference.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-inference.jpg) — no literal build reference found
- [ ] [how-ai-answers-last-token.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-last-token.jpg) — 3 build/reference file(s); e.g. [render_how_ai_answers_last_token.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_how_ai_answers_last_token.swift)
- [ ] [how-ai-answers-phone-prediction.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-phone-prediction.jpg) — no literal build reference found

### course-assets/how-an-llm-works

Current website assets: [how-an-llm-works-1-llm.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-an-llm-works/how-an-llm-works-1-llm.jpg), [how-an-llm-works-2-learn-once.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-an-llm-works/how-an-llm-works-2-learn-once.jpg), [how-an-llm-works-3-training.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-an-llm-works/how-an-llm-works-3-training.jpg), [how-an-llm-works-4-patterns.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-an-llm-works/how-an-llm-works-4-patterns.jpg)

- [ ] [how-an-llm-works.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/how-an-llm-works/how-an-llm-works.jpg) — no literal build reference found

### course-assets/layers

Current website assets: [layers-3-resolves-it.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/layers/layers-3-resolves-it.jpg), [layers-horse-three-reads-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/layers/layers-horse-three-reads-editorial.jpg), [layers-inside-layer-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/layers/layers-inside-layer-editorial.jpg), [layers-why-dozens.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/layers/layers-why-dozens.jpg)

- [ ] [layers-inside.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/layers/layers-inside.jpg) — 2 build/reference file(s); e.g. [render_layers_vector_rail.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_layers_vector_rail.swift)
- [ ] [layers-three-reads.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/layers/layers-three-reads.jpg) — 2 build/reference file(s); e.g. [render_layers_remaining_boards.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_layers_remaining_boards.swift)
- [ ] [layers.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/layers/layers.jpg) — no literal build reference found

### course-assets/learn-with-ai

Current website assets: [learn-with-ai-1-study-tools.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/learn-with-ai/learn-with-ai-1-study-tools.jpg), [learn-with-ai-2-how-it-works.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/learn-with-ai/learn-with-ai-2-how-it-works.jpg), [learn-with-ai-3-four-moves.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/learn-with-ai/learn-with-ai-3-four-moves.jpg)

- [ ] [learn-with-ai-study-tools.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/learn-with-ai/learn-with-ai-study-tools.jpg) — 6 build/reference file(s); e.g. [normalize_alternative_board_titles.sh](/Users/davidobrien/Developer/AI-Training/scripts/video/normalize_alternative_board_titles.sh)
- [ ] [learn-with-ai.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/learn-with-ai/learn-with-ai.jpg) — no literal build reference found

### course-assets/loudest-voices

Current website assets: [loudest-voices-1-experts.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/loudest-voices/loudest-voices-1-experts.jpg), [loudest-voices-2-missed-predictions.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/loudest-voices/loudest-voices-2-missed-predictions.jpg)

- [ ] [loudest-voices.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/loudest-voices/loudest-voices.jpg) — no literal build reference found

### course-assets/make-your-move

Current website assets: [make-your-move-2-careers-a.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/make-your-move/make-your-move-2-careers-a.jpg), [make-your-move-2-careers-b.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/make-your-move/make-your-move-2-careers-b.jpg), [make-your-move-3-skills.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/make-your-move/make-your-move-3-skills.jpg), [make-your-move-4-actions.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/make-your-move/make-your-move-4-actions.jpg), [make-your-move-note-v1.png](/Users/davidobrien/Developer/AI-Training/course-assets/make-your-move/make-your-move-note-v1.png)


### course-assets/mind-trap

Current website assets: [mind-trap-1-comparison.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap-1-comparison.jpg), [mind-trap-2-eliza.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap-2-eliza.jpg)

- [ ] [mind-trap-comparison-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap-comparison-v2.jpg) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [mind-trap-comparison-v3.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap-comparison-v3.jpg) — 3 build/reference file(s); e.g. [prepare_avoid_traps_kits.py](/Users/davidobrien/Developer/AI-Training/scripts/video/prepare_avoid_traps_kits.py)
- [ ] [mind-trap-eliza-effect-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap-eliza-effect-v2.jpg) — 1 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [mind-trap-eliza-effect-v3.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap-eliza-effect-v3.jpg) — no literal build reference found
- [ ] [mind-trap-eliza-effect.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap-eliza-effect.jpg) — 3 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)
- [ ] [mind-trap.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/mind-trap/mind-trap.jpg) — no literal build reference found

### course-assets/one-more-thing

Current website assets: [one-more-thing-1-draws.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/one-more-thing/one-more-thing-1-draws.jpg), [one-more-thing-2-temperature.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/one-more-thing/one-more-thing-2-temperature.jpg), [one-more-thing-3-bill.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/one-more-thing/one-more-thing-3-bill.jpg)

- [ ] [one-more-thing-memory-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/one-more-thing/one-more-thing-memory-v2.jpg) — 1 build/reference file(s); e.g. [render_one_more_thing_memory_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_one_more_thing_memory_board.py)
- [ ] [one-more-thing-temperature.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/one-more-thing/one-more-thing-temperature.jpg) — 2 build/reference file(s); e.g. [render_your_choices_temperature.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_your_choices_temperature.py)
- [ ] [one-more-thing.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/one-more-thing/one-more-thing.jpg) — no literal build reference found

### course-assets/pace-of-change

Current website assets: [pace-of-change-1-three-years.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change-1-three-years.jpg), [pace-of-change-2-accelerants.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change-2-accelerants.jpg), [pace-of-change-3-future-research.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change-3-future-research.jpg), [pace-of-change-4-future-capability.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change-4-future-capability.jpg)

- [ ] [pace-of-change-accelerants.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change-accelerants.jpg) — no literal build reference found
- [ ] [pace-of-change-future-capability.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change-future-capability.jpg) — no literal build reference found
- [ ] [pace-of-change-future-research.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change-future-research.jpg) — no literal build reference found
- [ ] [pace-of-change.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/pace-of-change/pace-of-change.jpg) — no literal build reference found

### course-assets/people-skills

Current website assets: [people-skills-1-why-matter.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/people-skills/people-skills-1-why-matter.jpg), [people-skills-2-four-ways.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/people-skills/people-skills-2-four-ways.jpg)

- [ ] [people-skills-luke-nate.png](/Users/davidobrien/Developer/AI-Training/course-assets/people-skills/people-skills-luke-nate.png) — no literal build reference found
- [ ] [people-skills-why-matter.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/people-skills/people-skills-why-matter.jpg) — no literal build reference found

### course-assets/questions-matter

Current website assets: [questions-matter-1-answers-faster.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/questions-matter/questions-matter-1-answers-faster.jpg), [questions-matter-2-value-lives.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/questions-matter/questions-matter-2-value-lives.jpg), [questions-matter-3-four-qualities.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/questions-matter/questions-matter-3-four-qualities.jpg)

- [ ] [questions-matter-answers-cheap.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/questions-matter/questions-matter-answers-cheap.jpg) — 3 build/reference file(s); e.g. [normalize_alternative_board_titles.sh](/Users/davidobrien/Developer/AI-Training/scripts/video/normalize_alternative_board_titles.sh)
- [ ] [questions-matter-value-shift.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/questions-matter/questions-matter-value-shift.jpg) — 2 build/reference file(s); e.g. [render_questions_matter_value_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_questions_matter_value_board.py)
- [ ] [questions-matter.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/questions-matter/questions-matter.jpg) — no literal build reference found

### course-assets/rise-of-agents

Current website assets: [rise-of-agents-1-gps.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/rise-of-agents/rise-of-agents-1-gps.jpg), [rise-of-agents-2-chatbot-vs-agent.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/rise-of-agents/rise-of-agents-2-chatbot-vs-agent.jpg), [rise-of-agents-3-loop.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/rise-of-agents/rise-of-agents-3-loop.jpg), [rise-of-agents-4-rogue.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/rise-of-agents/rise-of-agents-4-rogue.jpg)

- [ ] [rise-of-agents-loop.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/rise-of-agents/rise-of-agents-loop.jpg) — no literal build reference found
- [ ] [rise-of-agents.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/rise-of-agents/rise-of-agents.jpg) — 1 build/reference file(s); e.g. [render_embrace_editorial_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_review.py)

### course-assets/shared

Current website assets: [your-edge.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/shared/your-edge.jpg)

- [ ] [when-ai-judges-you.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/shared/when-ai-judges-you.jpg) — no literal build reference found

### course-assets/support-trap

Current website assets: [support-trap-1-comparison.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/support-trap/support-trap-1-comparison.jpg), [support-trap-2-role.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/support-trap/support-trap-2-role.jpg), [support-trap-3-danger.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/support-trap/support-trap-3-danger.jpg)

- [ ] [support-trap-1-comparison-notebook.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/support-trap/support-trap-1-comparison-notebook.jpg) — 1 build/reference file(s); e.g. [prepare_support_trap_reroll.py](/Users/davidobrien/Developer/AI-Training/scripts/video/prepare_support_trap_reroll.py)
- [ ] [support-trap-comparison-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/support-trap/support-trap-comparison-v2.jpg) — 5 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [support-trap-real-vs-missing.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/support-trap/support-trap-real-vs-missing.jpg) — 4 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)

### course-assets/tokens

Current website assets: [tokens-building-blocks-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-building-blocks-editorial.jpg), [tokens-cat-token-id-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-cat-token-id-editorial.jpg), [tokens-how-ai-splits-text-verified-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-how-ai-splits-text-verified-editorial.jpg), [tokens-how-tokenization-works-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-how-tokenization-works-editorial.jpg), [tokens-using-ai-feels-like-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-using-ai-feels-like-editorial.jpg)

- [ ] [tokens-3-cat.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-3-cat.jpg) — 2 build/reference file(s); e.g. [render_tokens_cat_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_tokens_cat_board.py)
- [ ] [tokens-building-blocks-notebook.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-building-blocks-notebook.jpg) — 1 build/reference file(s); e.g. [render_tokens_building_blocks_notebook.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_tokens_building_blocks_notebook.py)
- [ ] [tokens-verified.png](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens-verified.png) — no literal build reference found
- [ ] [tokens.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/tokens/tokens.jpg) — 1 build/reference file(s); e.g. [render_understand_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_understand_ai_retrofit_review.py)

### course-assets/training

Current website assets: [training-before-starts-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training/training-before-starts-editorial.jpg), [training-instruction-tuning-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training/training-instruction-tuning-editorial.jpg), [training-loop-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training/training-loop-editorial.jpg), [training-preference-tuning-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training/training-preference-tuning-editorial.jpg), [training-pretraining-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training/training-pretraining-editorial.jpg)

- [ ] [training-loop.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training/training-loop.jpg) — 4 build/reference file(s); e.g. [render_understand_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_understand_ai_retrofit_review.py)
- [ ] [training.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training/training.jpg) — 3 build/reference file(s); e.g. [render_understand_ai_retrofit_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_understand_ai_retrofit_review.py)

### course-assets/training-bias

Current website assets: [training-bias-1-wrong-pattern.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-1-wrong-pattern.jpg), [training-bias-2-mechanisms.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-2-mechanisms.jpg), [training-bias-3-questions.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-3-questions.jpg), [training-bias-4-stale.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-4-stale.jpg), [training-bias-5-rag.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-5-rag.jpg)

- [ ] [training-bias-mechanisms.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-mechanisms.jpg) — 3 build/reference file(s); e.g. [render_training_bias_boards.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_training_bias_boards.swift)
- [ ] [training-bias-pattern-v2.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-pattern-v2.jpg) — 3 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)
- [ ] [training-bias-questions.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias-questions.jpg) — 2 build/reference file(s); e.g. [render_training_bias_boards.swift](/Users/davidobrien/Developer/AI-Training/scripts/video/render_training_bias_boards.swift)
- [ ] [training-bias.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/training-bias/training-bias.jpg) — 2 build/reference file(s); e.g. [render_avoid_traps_editorial.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_avoid_traps_editorial.py)

### course-assets/transformer

Current website assets: [transformer-attention-transformation-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-attention-transformation-editorial.jpg), [transformer-before-transformers-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-before-transformers-editorial.jpg), [transformer-context-problems-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-context-problems-editorial.jpg), [transformer-how-transformer-reads-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-how-transformer-reads-editorial.jpg), [transformer-resolves-meaning-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-resolves-meaning-editorial.jpg), [transformer-word-order-editorial.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-word-order-editorial.jpg)

- [ ] [transformer-1-before.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-1-before.jpg) — 6 build/reference file(s); e.g. [build_prompts.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_prompts.py)
- [ ] [transformer-2-now.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-2-now.jpg) — 3 build/reference file(s); e.g. [render_transformer_reading_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_transformer_reading_boards.py)
- [ ] [transformer-attention-transformation-page.png](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-attention-transformation-page.png) — no literal build reference found
- [ ] [transformer-attention-transformation-video.png](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-attention-transformation-video.png) — 1 build/reference file(s); e.g. [transformer-attention-transformation-highlights.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/transformer-attention-transformation-highlights.json)
- [ ] [transformer-reading-comparison.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-reading-comparison.jpg) — 6 build/reference file(s); e.g. [build_prompts.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_prompts.py)
- [ ] [transformer-solutions-page.png](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-solutions-page.png) — no literal build reference found
- [ ] [transformer-solutions-video.png](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer-solutions-video.png) — 1 build/reference file(s); e.g. [transformer-solutions-highlights.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/transformer-solutions-highlights.json)
- [ ] [transformer.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/transformer/transformer.jpg) — 1 build/reference file(s); e.g. [render_transformer_reading_boards.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_transformer_reading_boards.py)

### course-assets/understand-ai-opener

Current website assets: [opener-understand-2-map.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/understand-ai-opener/opener-understand-2-map.jpg), [opener-understand-under-hood-v3.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/understand-ai-opener/opener-understand-under-hood-v3.jpg)

- [ ] [opener-understand-under-hood-art.png](/Users/davidobrien/Developer/AI-Training/course-assets/understand-ai-opener/opener-understand-under-hood-art.png) — no literal build reference found
- [ ] [opener-understand.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/understand-ai-opener/opener-understand.jpg) — no literal build reference found

### course-assets/unexpected-results

Current website assets: [unexpected-results-1-plans.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/unexpected-results/unexpected-results-1-plans.jpg)

- [ ] [unexpected-results.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/unexpected-results/unexpected-results.jpg) — no literal build reference found

### course-assets/welcome

Current website assets: [welcome-2-how-to-take-course-page.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/welcome/welcome-2-how-to-take-course-page.jpg), [welcome-2-your-path.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/welcome/welcome-2-your-path.jpg), [welcome-3-course-toolkit.png](/Users/davidobrien/Developer/AI-Training/course-assets/welcome/welcome-3-course-toolkit.png), [welcome.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/welcome/welcome.jpg)

- [ ] [welcome-2-how-to-take-course.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/welcome/welcome-2-how-to-take-course.jpg) — 2 build/reference file(s); e.g. [build_prompts.py](/Users/davidobrien/Developer/AI-Training/scripts/video/build_prompts.py)
- [ ] [welcome-3-what-youll-need.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/welcome/welcome-3-what-youll-need.jpg) — 3 build/reference file(s); e.g. [capture-page-boards.js](/Users/davidobrien/Developer/AI-Training/scripts/capture-page-boards.js)

### course-assets/what-is-ai

Current website assets: [what-is-ai-1-types.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-is-ai/what-is-ai-1-types.jpg), [what-is-ai-2-same-goal.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-is-ai/what-is-ai-2-same-goal.jpg), [what-is-ai-ask-the-desk.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-is-ai/what-is-ai-ask-the-desk.jpg)

- [ ] [what-is-ai-llm.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-is-ai/what-is-ai-llm.jpg) — 7 build/reference file(s); e.g. [normalize_alternative_board_titles.sh](/Users/davidobrien/Developer/AI-Training/scripts/video/normalize_alternative_board_titles.sh)
- [ ] [what-is-ai.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-is-ai/what-is-ai.jpg) — no literal build reference found

### course-assets/what-you-can-control

Current website assets: [what-you-can-control-1-hands.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-you-can-control/what-you-can-control-1-hands.jpg), [what-you-can-control-2-three-moves.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-you-can-control/what-you-can-control-2-three-moves.jpg)

- [ ] [what-you-can-control-hands.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-you-can-control/what-you-can-control-hands.jpg) — 5 build/reference file(s); e.g. [normalize_alternative_board_titles.sh](/Users/davidobrien/Developer/AI-Training/scripts/video/normalize_alternative_board_titles.sh)
- [ ] [what-you-can-control-three-moves.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-you-can-control/what-you-can-control-three-moves.jpg) — 2 build/reference file(s); e.g. [render_what_you_can_control_three_moves_board.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_what_you_can_control_three_moves_board.py)
- [ ] [what-you-can-control.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/what-you-can-control/what-you-can-control.jpg) — no literal build reference found

### course-assets/why-learn-ai

Current website assets: [why-learn-ai-1-everyday.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/why-learn-ai/why-learn-ai-1-everyday.jpg), [why-learn-ai-1-press.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/why-learn-ai/why-learn-ai-1-press.jpg), [why-learn-ai-2-thrive.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/why-learn-ai/why-learn-ai-2-thrive.jpg)

- [ ] [why-learn-ai.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/why-learn-ai/why-learn-ai.jpg) — no literal build reference found

### course-assets/work-changes

Current website assets: [work-changes-1-strengths.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes-1-strengths.jpg), [work-changes-2-assignment.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes-2-assignment.jpg), [work-changes-3-automate-augment.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes-3-automate-augment.jpg), [work-changes-4-what-changes.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes-4-what-changes.jpg)

- [ ] [work-changes-automate-augment.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes-automate-augment.jpg) — 1 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)
- [ ] [work-changes-strengths.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes-strengths.jpg) — no literal build reference found
- [ ] [work-changes-what-changes.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes-what-changes.jpg) — 1 build/reference file(s); e.g. [render_editorial_board_refresh.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_editorial_board_refresh.py)
- [ ] [work-changes.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-changes/work-changes.jpg) — 1 build/reference file(s); e.g. [render_embrace_editorial_review.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_embrace_editorial_review.py)

### course-assets/work-with-ai-opener

Current website assets: [opener-work-2-same-tool.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-with-ai-opener/opener-work-2-same-tool.jpg), [opener-work-3-section-map.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-with-ai-opener/opener-work-3-section-map.jpg)

- [ ] [opener-work-1-refrain.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/work-with-ai-opener/opener-work-1-refrain.jpg) — 4 build/reference file(s); e.g. [capture-page-boards.js](/Users/davidobrien/Developer/AI-Training/scripts/capture-page-boards.js)

### course-assets/your-choices

Current website assets: [your-choices-1-choose-tool.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-1-choose-tool.jpg), [your-choices-2-choose-how.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-2-choose-how.jpg)

- [ ] [your-choices-choose-how-v8.png](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-choose-how-v8.png) — no literal build reference found
- [ ] [your-choices-how-works-v6.png](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-how-works-v6.png) — no literal build reference found
- [ ] [your-choices-how-works.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-how-works.jpg) — no literal build reference found
- [ ] [your-choices-temperature-v1.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-temperature-v1.jpg) — 2 build/reference file(s); e.g. [render_your_choices_temperature.py](/Users/davidobrien/Developer/AI-Training/scripts/video/render_your_choices_temperature.py)
- [ ] [your-choices-where-what.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-choices/your-choices-where-what.jpg) — no literal build reference found

### course-assets/your-home-base

Current website assets: [which-app-1-big-three.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-home-base/which-app-1-big-three.jpg), [which-app-2-home-base.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-home-base/which-app-2-home-base.jpg), [which-app-3-how-we-used.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-home-base/which-app-3-how-we-used.jpg)

- [ ] [which-app.jpg](/Users/davidobrien/Developer/AI-Training/course-assets/your-home-base/which-app.jpg) — 1 build/reference file(s); e.g. [which-app-choose.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/which-app-choose.json)

## 4. Separate video-only item

[training-server-bridge.jpg](/Users/davidobrien/Developer/AI-Training/scripts/video/assets/training-server-bridge.jpg) is referenced by [training-deleted-scene-bridge.json](/Users/davidobrien/Developer/AI-Training/scripts/video/paths/training-deleted-scene-bridge.json). It is a video image, not a confirmed component of a finished lesson illustration. Decide separately.

## Kept outside this deletion review

- 185 current website image/PDF assets.
- 43 closing-board exports, following your decision to retain the closing message with each lesson.
- Fonts and font licenses, all finished videos, lesson text, and other application files.

Counts and the classification apply to this audit date. Any approved deletion should recheck hashes and current references first.
