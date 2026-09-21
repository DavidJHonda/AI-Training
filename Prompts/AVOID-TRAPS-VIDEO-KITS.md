# Avoid Traps Video Kits

Initially prepared against the lesson pages on 2026-09-04; individual kits are updated as reviewed. Each has one canonical Markdown, one prompt under 500 words, and the current JPG sources. The seven trap lessons and Hallucination were rebuilt to the 2026-09-10 materials spec on 2026-09-18; each has an upload checklist. Follow each lesson's current checklist rather than the original batch counts. Numbering follows teaching order; gaps in the upload list are intentional.

Upload sets for all nine lessons live in `Prompts/upload-sets.json`; `scripts/video/sync_gemini_notebook.py` stages each lesson's uploads in `gemini-notebook/<slug>/upload/` with the prompt beside them and regenerates the checklists below from the same registry (2026-09-20).

`Master Prompt.md` is retired and is never uploaded. Each prompt below is self-contained. Upload only the lesson Markdown and the files listed under **Notebook sources**. Files under **Post-production boards** are exact current lesson boards, but they contain visible faces and must not be uploaded to Gemini Notebook. Each prompt reserves an uninterrupted narration span for those boards so they can be inserted exactly in post-production.

Paste the prompt into Notebook's video customization box; it is not an extra source document. Use the Markdown, not the older lesson PDF. Do not upload this checklist, the manifest, or archived variants. Before generation, turn Visible watermarking off as described in Edit Spec section 8. Save new raw videos to `Prompts/<slug>-reroll.mp4`, or the next unused numbered reroll filename. Do not overwrite existing raw rolls or the live video.

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

**v6 SHIPPED 2026-09-21** (cache key 20260921ship1, pill 4 min): roll 2 of 2026-09-21 as the whole narration, no grafts; canonical Traps Ahead (gold text-tight rings), Read the Water walk from "Survival…", section map with row rings and roll 1's binoculars interleave, standard close. Review: `video-audit/avoid-traps-opener-comparison-2026-09-21/`.

- Prompt: `Prompts/opener-avoid-video-prompt.txt`
- Markdown: `lessons/Opener-Avoid.md`
- Notebook sources:
  1. `course-assets/avoid-traps-opener/avoid-traps-opener-traps.jpg`
  2. `course-assets/avoid-traps-opener/avoid-traps-opener-section-map.jpg`
  3. `course-assets/avoid-traps-opener/avoid-traps-opener-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/avoid-traps-opener/avoid-traps-opener-read-the-water.jpg`

## Hallucination

**v11 SHIPPED 2026-09-21** (cache key 20260921ship2, pill 5 min): roll 1 of 2026-09-21 as the whole narration (two cuts: a 'banner' lead-in and a post-close sentence); canonical Boards 1, 2, 4 with full-height card rings; the post-only pizza board walked twice (also covers Notebook's fabricated Reddit screenshots); Why board's arrows changed to the Check the Claim style. Review: `video-audit/hallucination-comparison-2026-09-21/`.

Reviewed against the current page and all five canonical JPGs on 2026-09-18. Corrected Markdown links and the manifest; added the spoken application of all three source-check steps to both examples. The fake study is a deliberately invented example; a failed search alone does not prove a real-world claim false. Removed unsupported blanket claims about AI's intent from the prompt. Pauses remain selective editing decisions.

Scene directions: draw the opening chat before revealing Board 1; leave it for the definition. Teach Board 2's four explanations in order. Reserve one continuous Board 3 span for the pizza question, mistaken answer, real joke, and takeaway. Use the brief checking-mindset scene before Board 4, then narrate the named checks and both applications. Finish on the supplied close with its two lines verbatim. Review changed scene directions before generation and the highlighting plan before first edits. This prep review does not establish a verdict on any existing video.

- Prompt: `Prompts/hallucination-video-prompt.txt`
- Markdown: `lessons/hallucination.md`
- Upload checklist: `Prompts/hallucination-upload-files.txt`
- Notebook sources:
  1. `course-assets/hallucination/hallucination-example.jpg`
  2. `course-assets/hallucination/hallucination-why-ai-makes-things-up.jpg`
  3. `course-assets/hallucination/hallucination-check-claim.jpg`
  4. `course-assets/hallucination/hallucination-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/hallucination/hallucination-glue-on-pizza.jpg` (faces; Board 3 narration reserved in the Markdown)

## Training Bias

**v6 SHIPPED 2026-09-21** (cache key 20260921ship3, pill 4 min): roll 6 of 2026-09-21 as the whole narration, no grafts, no cuts; post-only Wrong Pattern board as an illustration walk; canonical Boards 2-5 with card-hugging rings (separate-card rule) and bubble rings; standard close. Review: `video-audit/training-bias-comparison-2026-09-21/`.

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; Scene markers so the prose runs leave the boards).

- Prompt: `Prompts/training-bias-video-prompt.txt`
- Markdown: `lessons/training-bias.md`
- Upload checklist: `Prompts/training-bias-upload-files.txt`
- Notebook sources:
  1. `course-assets/training-bias/training-bias-how-bias-happens.jpg`
  2. `course-assets/training-bias/training-bias-questions-to-ask.jpg`
  3. `course-assets/training-bias/training-bias-stale.jpg`
  4. `course-assets/training-bias/training-bias-rag.jpg`
  5. `course-assets/training-bias/training-bias-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/training-bias/training-bias-wrong-pattern.jpg` (faces; Board 1 cow-story narration reserved in the Markdown)

## Document Trap

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; Scene labels move the rulebook-mistake, retrieval, and leases passages off the boards).

- Prompt: `Prompts/document-trap-video-prompt.txt`
- Markdown: `lessons/document-trap.md`
- Upload checklist: `Prompts/document-trap-upload-files.txt`
- Notebook sources:
  1. `course-assets/document-trap/document-trap-flow.jpg`
  2. `course-assets/document-trap/document-trap-moves.jpg`
  3. `course-assets/document-trap/document-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/document-trap/document-trap-uploaded.jpg` (faces; Board 1 narration reserved in the Markdown)

## Mind Trap

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; the comparison board's narration reserved for post-production).

- Prompt: `Prompts/mind-trap-video-prompt.txt`
- Markdown: `lessons/mind-trap.md`
- Upload checklist: `Prompts/mind-trap-upload-files.txt`
- Notebook sources:
  1. `course-assets/mind-trap/mind-trap-eliza.jpg`
  2. `course-assets/mind-trap/mind-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/mind-trap/mind-trap-comparison.jpg` (faces; Board 1 narration reserved in the Markdown)

## Flattery Trap

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; the Gatsby comparison's narration reserved for post-production, a Scene label moves the rollback passage off the sycophancy board).

- Prompt: `Prompts/flattery-trap-video-prompt.txt`
- Markdown: `lessons/flattery-trap.md`
- Upload checklist: `Prompts/flattery-trap-upload-files.txt`
- Notebook sources:
  1. `course-assets/flattery-trap/flattery-trap-cycle-of-praise.jpg`
  2. `course-assets/flattery-trap/flattery-trap-sycophancy.jpg`
  3. `course-assets/flattery-trap/flattery-trap-five-moves.jpg`
  4. `course-assets/flattery-trap/flattery-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/flattery-trap/flattery-trap-comparison.jpg` (faces; Board 1 narration reserved in the Markdown)

## Engagement Trap

Revised on 2026-09-19 to add the verified Meta teen-safety settlement and the native-rendered stopping-points board. The illustrated AI stopping-point board remains reserved for post-production.

- Prompt: `Prompts/engagement-trap-video-prompt.txt`
- Markdown: `lessons/engagement-trap.md`
- Upload checklist: `Prompts/engagement-trap-upload-files.txt`
- Notebook sources:
  1. `course-assets/engagement-trap/engagement-trap-comparison.jpg`
  2. `course-assets/engagement-trap/engagement-trap-scroll.jpg`
  3. `course-assets/engagement-trap/engagement-trap-stopping-points.jpg`
  4. `course-assets/engagement-trap/engagement-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/engagement-trap/engagement-trap-stopping-point.jpg` (faces; Board 3 narration reserved in the Markdown)

## Support Trap

Rebuilt to the 2026-09-10 materials spec on 2026-09-18 (Board sections with teaching content and takeaways; Speak the Answers prompt; the lunch comparison's narration reserved for post-production; the activity’s three-way distinction is included before the serious story).

- Prompt: `Prompts/support-trap-video-prompt.txt`
- Markdown: `lessons/support-trap.md`
- Upload checklist: `Prompts/support-trap-upload-files.txt`
- Notebook sources:
  1. `course-assets/support-trap/support-trap-role.jpg`
  2. `course-assets/support-trap/support-trap-danger.jpg`
  3. `course-assets/support-trap/support-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/support-trap/support-trap-comparison.jpg` (faces; Board 1 narration reserved in the Markdown)

## Fake Trap

Materials test, 2026-09-20 (owner request after the narration-source review): the kit is rebuilt on the 2026-09-11 Build Your Skills recipe that produced the shipped run. The Markdown is a clean lesson (Board / Image file / Teaching content only; no Scene, Takeaway, or post-production labels; banner lines carried as plain sentences). The prompt carries the VOICE block, a required-verbatim list, and a beat spine. Both face boards are uploaded as text-only variants (photo panels removed) so their teaching sits on a picture instead of an invented scene; the canonical boards replace them in post. Baseline for the comparison: `Prompts/fake-trap-v3.mp4`, reviewed in `video-audit/fake-trap-materials-test-2026-09-20/REVIEW.md`. RESULT: the recipe won (roll 2 base, one roll-1 graft); **v5 SHIPPED 2026-09-20** (cache key 20260920ship2, pill 5 min). Use this kit as the template for the remaining Avoid Traps lessons.

- Prompt: `Prompts/fake-trap-video-prompt.txt`
- Markdown: `lessons/fake-trap.md`
- Upload checklist: `Prompts/fake-trap-upload-files.txt`
- Notebook sources:
  1. `Prompts/fake-trap-comparison-faceless.jpg` (upload variant of the Board 1 comparison board, photos removed)
  2. `course-assets/fake-trap/fake-trap-reasons.jpg`
  3. `Prompts/fake-trap-follow-the-source-faceless.jpg` (upload variant of the Board 3 board, photo removed)
  4. `course-assets/fake-trap/fake-trap-checks.jpg`
  5. `course-assets/fake-trap/fake-trap-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `course-assets/fake-trap/fake-trap-comparison.jpg` (faces; replaces the faceless variant in the edit)
  - `course-assets/fake-trap/fake-trap-follow-the-source.jpg` (faces; replaces the faceless variant in the edit)

## Provenance, cleanup, and post-production

- `Prompts/AVOID-TRAPS-SOURCE-MANIFEST.json` records the exact lesson asset, hashes, dimensions, upload status, and prompt word count. Current JPG originals are copied byte-for-byte; Fake Trap's reasons PNG is converted to a high-quality JPG at its original dimensions. Closing text comes directly from `index.html`'s `CLOSE_BOARDS`.
- Use the current lesson boards in `course-assets/` and current Markdown in `lessons/`. Remove superseded materials within owner-authorized cleanup scope; do not create archive copies. Historical move records in the source manifest describe removed files, not available upload sources. The old `prepare_avoid_traps_kits.py` workflow is retired because its source mappings and archive behavior are obsolete.
- Markdown includes the teaching inside boards as text. Regenerating a plain DOM export alone may omit that text or collapse list formatting; check it against the actual board before replacing these reviewed files.
- In post, insert the exact withheld face boards and replace native Notebook highlights. Highlight complete cards, bubbles, or banners at their true boundaries; subsection highlights inherit the containing box's full horizontal bounds. Use the element's locked accent, protect all text, and maintain balanced vertical clearance.
- Check every edit boundary frame-by-frame in the final render for old-graphic flashes, and listen across each audio cut for clipped words, duplicate breaths, or abrupt transitions. Report timestamps from the final candidate, not the uncut source. Follow `scripts/video/RETROFIT-PLAYBOOK.md` for the full procedure.
