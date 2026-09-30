# Avoid Traps Video Kits

Prep status is controlled by `gemini-notebook/upload-sets.json`. Any lesson listed in
`needs_preparation` requires a fresh kit; older “materials ready” or upload directions
below describe historical work and do not authorize reuse.

> **Method note (2026-09-21):** per-lesson entries below dated before 2026-09-20 describe the previous preparation method (Scene/Takeaway labels, withheld face boards with "reserved" narration, prompts without a verbatim list, beat spine, or VOICE block). Rebuild a lesson's Markdown and prompt to the "Prepare a new lesson" procedure in `scripts/video/PREPARATION.md`, add it to `gemini-notebook/upload-sets.json`, and run the sync before rolling it. Entries that say they are on the 2026-09-20 recipe are current.

Initially prepared against the lesson pages on 2026-09-04; individual kits are updated as reviewed. Each has one canonical Markdown, one prompt under 500 words, and the current JPG sources. The seven trap lessons and Hallucination were rebuilt to the 2026-09-10 materials spec on 2026-09-18; each has an upload checklist. Follow each lesson's current checklist rather than the original batch counts. Numbering follows teaching order; gaps in the upload list are intentional.

**Current prep status (2026-09-29):** use `gemini-notebook/upload-sets.json` for the active kit list. Support Trap now has a rebuilt full-video reroll kit. Retired entries still require fresh prep from the current page under `scripts/video/PREPARATION.md`; historical lists below do not override the registry.

The source lists and reserved-narration directions below document previous productions. They are not current upload instructions. Preserve useful review and editing history, but do not recreate a legacy prompt from these notes. Current bundles come only from `gemini-notebook/upload-sets.json`.

## Scene plan for review

| Lesson | Teaching sequence |
| --- | --- |
| Opener | Normal-looking failures → rip-current analogy → three groups of traps → close |
| Hallucination | Drawn chat → fabricated study reveal → definition scene → four explanations → uninterrupted pizza/Reddit example → checking mindset → three source-check steps applied to both examples → exact close |
| Training Bias | Cow/grass shortcut → three distortions → three questions → historical wrong-answer chat and current-source correction → RAG → close |
| Document Trap | Tournament exception → split/search/load → RAG → four retrieval moves applied to the rulebook → close |
| Mind Trap | Mom versus chatbot college advice → brief ELIZA → why human language feels human → shared context versus shared experience → movie versus college → keep the decision → close |
| Flattery Trap | Gatsby feedback comparison → human-feedback training → brief historical sycophancy failure → five demonstrated feedback moves with explanations and limits → close |
| Engagement Trap | Slope question, two endings → infinite scroll removes a decision → Meta settlement restores limits and pauses → deliberate stopping in AI chat → close |
| Support Trap | Sister versus chatbot at lunch → venting, preparation followed by action, and danger needing a person → content note and Sophie story → urgent human-help actions → close |
| Fake Trap | School-closure clip → harmless versus harmful fakes → four motives → detector limits → three source checks applied to the school-closure clip → help if targeted → close |

## Opener


**v7 SHIPPED 2026-09-22** (cache key 20260922ship3, pill 4 min, 3:35): v6 with the map-introduction sentence replaced by the Understand opener's "This roadmap shows what we'll explore in this section." (audio-only graft, +0.69 dB) and the section map arriving on it. Review: `video-audit/avoid-traps-opener-comparison-2026-09-21/` (Build v7 section).
**v6 SHIPPED 2026-09-21** (cache key 20260921ship1, pill 4 min): roll 2 of 2026-09-21 as the whole narration, no grafts; canonical Traps Ahead (gold text-tight rings), Read the Water walk from "Survival…", section map with row rings and roll 1's binoculars interleave, standard close. Review: `video-audit/avoid-traps-opener-comparison-2026-09-21/`.

- Prompt: **retired; fresh prep required**
- Markdown: `lessons/Opener-Avoid.md`
- Notebook sources:
  1. `course-assets/avoid-traps-opener/avoid-traps-opener-traps.jpg`
  2. `course-assets/avoid-traps-opener/avoid-traps-opener-section-map.jpg`
  3. `course-assets/avoid-traps-opener/avoid-traps-opener-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/avoid-traps-opener/avoid-traps-opener-read-the-water.jpg`

## Hallucination

**Fresh full-video reroll prep — September 30, 2026.** David chose a reroll after the v15 repair. The active instructions are now [the lesson-owned prep notes](../../../gemini-notebook/hallucination/PREP-NOTES.md), [PROMPT.txt](../../../gemini-notebook/hallucination/PROMPT.txt), and the `hallucination` entry in `gemini-notebook/upload-sets.json`.

The complete source is `lessons/hallucination.md`. The overview and both worked examples explicitly name all three checking steps. The pizza application explains why finding a real comment is not enough: a joke does not support the advice. Preserve the invented-study example, all four causes, the distinction between invention and misreading, the failed-search qualifier, and both closing lines.

Run the lesson sync and upload every file in `gemini-notebook/hallucination/upload/`: one Markdown and five JPGs. The pizza board now has a text-only upload stand-in; the canonical illustration replaces it in editing. Older directions to omit that source or reserve a continuous pizza-board span are superseded. Read the current prep notes for generation and review details.

Historical production evidence remains in `video-audit/hallucination-comparison-2026-09-21/`, `video-audit/hallucination-live-review-2026-09-29/`, and `video-audit/hallucination-v15-2026-09-30/`. The page still references the installed video with cache key `20260921ship21`; preparation does not change that release.

## Training Bias

**v6 SHIPPED 2026-09-21** (cache key 20260921ship3, pill 4 min): roll 6 of 2026-09-21 as the whole narration, no grafts, no cuts; post-only Wrong Pattern board as an illustration walk; canonical Boards 2-5 with card-hugging rings (separate-card rule) and bubble rings; standard close. Review: `video-audit/training-bias-comparison-2026-09-21/`.

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; Scene markers so the prose runs leave the boards).

- Prompt: **retired; fresh prep required**
- Markdown: `lessons/training-bias.md`
- Upload checklist: **retired; fresh prep required**
- Notebook sources:
  1. `course-assets/training-bias/training-bias-how-bias-happens.jpg`
  2. `course-assets/training-bias/training-bias-questions-to-ask.jpg`
  3. `course-assets/training-bias/training-bias-stale.jpg`
  4. `course-assets/training-bias/training-bias-rag.jpg`
  5. `course-assets/training-bias/training-bias-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/training-bias/training-bias-wrong-pattern.jpg` (faces; Board 1 cow-story narration reserved in the Markdown)

## Document Trap

Rebuilt 2026-09-21 on the 2026-09-20 recipe (the Fake Trap template) after the 9/18 and 9/20 rolls did not carry the lesson: the prompt has the VOICE block, ten required-verbatim lines (both quotes from the story, the definition, both banners, the tournament-section question, the quotation line, the close), and a beat spine under 500 words; the Markdown is Board / Image file / Teaching content only with no Scene or Takeaway labels; Board 1 uploads as a faceless variant (title and banner, photo removed) that the canonical board replaces in post. Staged in `gemini-notebook/document-trap/`.

Revised again 2026-09-21 after rolls 7 and 8: both spoke seven of the ten required lines and missed the same three — the two definition sentences and Board 1's banner — and so did all six earlier rolls, so there was nothing to repair from. Those three were the only required lines buried mid-paragraph; every line that lands is either quoted dialogue or alone on its own line. The Markdown now gives all eleven that shape (the six-foul result is the eleventh, added because it has never landed in eight rolls), the two "may" sentences are split out so the conditional wording is not buried, and the prompt names the layout and the hardenings to avoid. Review: `video-audit/document-trap-reroll-2026-09-21/`.

- Prompt: `gemini-notebook/document-trap/PROMPT.txt`
- Markdown: `lessons/document-trap.md`
- Upload checklist: `gemini-notebook/document-trap/README.txt`
- Notebook sources:
  1. `gemini-notebook/document-trap/assets/document-trap-uploaded-faceless.jpg` (upload variant of Board 1, photo removed)
  2. `course-assets/document-trap/document-trap-flow.jpg`
  3. `course-assets/document-trap/document-trap-moves.jpg`
  4. `course-assets/document-trap/document-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/document-trap/document-trap-uploaded.jpg` (faces; replaces the faceless variant in the edit)

## Mind Trap

**v3 SHIPPED 2026-09-21** (cache key 20260921ship4, pill 4 min): roll 6 of 2026-09-21 as the whole narration, no cuts, plus one graft from roll 5 (the shared-text-versus-shared-experience sentence, which roll 6 never speaks); post-only comparison board walked with section rings and returned to unmarked under the definition, which also removes the roll's chapter card; canonical Why AI Feels Like Somebody with card-hugging rings and a banner ring; the roll's 23.5 s archival mainframe photograph replaced by the previous live video's own ELIZA teletype drawing; standard close. Review: `video-audit/mind-trap-comparison-2026-09-21/`.

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; the comparison board's narration reserved for post-production).

- Prompt: **retired; fresh prep required**
- Markdown: `lessons/mind-trap.md`
- Upload checklist: **retired; fresh prep required**
- Notebook sources:
  1. `course-assets/mind-trap/mind-trap-eliza.jpg`
  2. `course-assets/mind-trap/mind-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/mind-trap/mind-trap-comparison.jpg` (faces; Board 1 narration reserved in the Markdown)

## Flattery Trap

**v6 SHIPPED 2026-09-21** (cache key 20260921ship5, pill 5 min): roll 4 of 2026-09-21 as the whole narration, no cuts, plus one audio-only graft from roll 2 ("But while the problem has improved, it has not disappeared.", the clause every other roll drops; roll 2's own picture there is an invented agreement-rate chart and never enters the build). Roll 4 is the only roll that keeps the RLHF qualification and speaks the standing instruction word for word. Post-only Flattery vs. Useful Feedback with response-quote and section rings; canonical How the Praise Got Baked In with full-box-height column rings; canonical Sycophancy with its first paragraph ringed; canonical Five Ways in five legs, dense, diving to the active row and panning between rows, broken up by three roll-3 drawings matched to the beats they cover; standard close. First build under the artwork-scaled ring rule (Edit Spec section 5). Review: `video-audit/flattery-trap-comparison-2026-09-21/`.

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; the Gatsby comparison's narration reserved for post-production, a Scene label moves the rollback passage off the sycophancy board).

- Prompt: **retired; fresh prep required**
- Markdown: `lessons/flattery-trap.md`
- Upload checklist: **retired; fresh prep required**
- Notebook sources:
  1. `course-assets/flattery-trap/flattery-trap-cycle-of-praise.jpg`
  2. `course-assets/flattery-trap/flattery-trap-sycophancy.jpg`
  3. `course-assets/flattery-trap/flattery-trap-five-moves.jpg`
  4. `course-assets/flattery-trap/flattery-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/flattery-trap/flattery-trap-comparison.jpg` (faces; Board 1 narration reserved in the Markdown)

## Engagement Trap

Revised on 2026-09-19 to add the verified Meta teen-safety settlement and the native-rendered stopping-points board. The illustrated AI stopping-point board remains reserved for post-production.

- Prompt: **retired; fresh prep required**
- Markdown: `lessons/engagement-trap.md`
- Upload checklist: **retired; fresh prep required**
- Notebook sources:
  1. `course-assets/engagement-trap/engagement-trap-comparison.jpg`
  2. `course-assets/engagement-trap/engagement-trap-scroll.jpg`
  3. `course-assets/engagement-trap/engagement-trap-stopping-points.jpg`
  4. `course-assets/engagement-trap/engagement-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/engagement-trap/engagement-trap-stopping-point.jpg` (faces; Board 3 narration reserved in the Markdown)

## Support Trap

**Full-video reroll prep rebuilt 2026-09-29.** David requested a complete new generation, then selection of its narration for the edit. The current v4 remains live (`20260921ship28`, 4:23.667). This is a current-method kit, not the retired 2026-09-18 setup. See `gemini-notebook/support-trap/PREP-NOTES.md` for the lesson arc, protected lines, source provenance, and editing handoff.

Both role-board sentences are now required verbatim: all three benefits including organizing thoughts, and all four limitations. The three jobs are Ordinary Venting, Preparation, Danger; the prompt explicitly rejects the live graphic’s Task Execution / System Collaboration / Multi-Agent Workflow labels. The warning, attributed story, distinct safety-number instructions, and closing lines remain protected. The full source includes the page activity’s plan-then-start example as teaching, without quiz instructions.

- Prompt: `gemini-notebook/support-trap/PROMPT.txt`
- Markdown: `lessons/support-trap.md`
- Generated upload checklist: `gemini-notebook/support-trap/README.txt`
- Upload the Markdown plus four boards in order:
  1. `gemini-notebook/support-trap/assets/support-trap-comparison-faceless.jpg`
  2. `course-assets/support-trap/support-trap-role.jpg`
  3. `gemini-notebook/support-trap/assets/support-trap-danger-faceless.jpg`
  4. `course-assets/support-trap/support-trap-close.jpg`
- Post-only: canonical `support-trap-comparison.jpg` and `support-trap-danger.jpg` replace their text-only upload variants in the edit. No canonical assets were changed.
- Save the complete roll as the next unused `Prompts/support-trap-reroll.mp4` / `support-trap-reroll-N.mp4` name. Compare the complete narration against v4 before selecting passages; a full reroll is not automatic approval to replace the finished video.

## Fake Trap

Materials test, 2026-09-20 (owner request after the narration-source review): the kit is rebuilt on the 2026-09-11 Build Your Skills recipe that produced the shipped run. The Markdown is a clean lesson (Board / Image file / Teaching content only; no Scene, Takeaway, or post-production labels; banner lines carried as plain sentences). The prompt carries the VOICE block, a required-verbatim list, and a beat spine. Both face boards are uploaded as text-only variants (photo panels removed) so their teaching sits on a picture instead of an invented scene; the canonical boards replace them in post. Baseline for the comparison: `Prompts/fake-trap-v3.mp4`, reviewed in `video-audit/fake-trap-materials-test-2026-09-20/REVIEW.md`. RESULT: the recipe won (roll 2 base, one roll-1 graft); **v5 SHIPPED 2026-09-20** (cache key 20260920ship2, pill 5 min). Use this kit as the template for the remaining Avoid Traps lessons.

- Prompt: `gemini-notebook/fake-trap/PROMPT.txt`
- Markdown: `lessons/fake-trap.md`
- Upload checklist: `gemini-notebook/fake-trap/README.txt`
- Notebook sources:
  1. `gemini-notebook/fake-trap/assets/fake-trap-comparison-faceless.jpg` (upload variant of the Board 1 comparison board, photos removed)
  2. `course-assets/fake-trap/fake-trap-reasons.jpg`
  3. `gemini-notebook/fake-trap/assets/fake-trap-follow-the-source-faceless.jpg` (upload variant of the Board 3 board, photo removed)
  4. `course-assets/fake-trap/fake-trap-checks.jpg`
  5. `course-assets/fake-trap/fake-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/fake-trap/fake-trap-comparison.jpg` (faces; replaces the faceless variant in the edit)
  - `course-assets/fake-trap/fake-trap-follow-the-source.jpg` (faces; replaces the faceless variant in the edit)

## Provenance, cleanup, and post-production

- `scripts/video/kits/AVOID-TRAPS-SOURCE-MANIFEST.json` records the exact lesson asset, hashes, dimensions, upload status, and prompt word count. Current JPG originals are copied byte-for-byte; Fake Trap's reasons PNG is converted to a high-quality JPG at its original dimensions. Closing text comes directly from `index.html`'s `CLOSE_BOARDS`.
- Use the current lesson boards in `course-assets/` and current Markdown in `lessons/`. Remove superseded materials within owner-authorized cleanup scope; do not create archive copies. Historical move records in the source manifest describe removed files, not available upload sources. The old `prepare_avoid_traps_kits.py` workflow is retired because its source mappings and archive behavior are obsolete.
- Markdown includes the teaching inside boards as text. Regenerating a plain DOM export alone may omit that text or collapse list formatting; check it against the actual board before replacing these reviewed files.
- In post, insert the exact withheld face boards and replace native Notebook highlights. Highlight complete cards, bubbles, or banners at their true boundaries; subsection highlights inherit the containing box's full horizontal bounds. Use the element's locked accent, protect all text, and maintain balanced vertical clearance.
- Check every edit boundary frame-by-frame in the final render for old-graphic flashes, and listen across each audio cut for clipped words, duplicate breaths, or abrupt transitions. Report timestamps from the final candidate, not the uncut source. Follow `scripts/video/RETROFIT-PLAYBOOK.md` for the full procedure.
