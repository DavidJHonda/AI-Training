# Avoid Traps Video Kits

Prepared against the current lesson pages on 2026-09-04. All nine lessons are being rerolled at the owner's request. Each has one canonical Markdown, one prompt under 500 words, and the exact current JPG sources. There are 39 JPGs: **29 for Notebook upload and 10 for post-production only**. Numbering follows teaching order; gaps in the upload list are intentional.

Do not upload `Prompts/Master Prompt.md`. Each prompt below is self-contained. Upload only the lesson Markdown and the files listed under **Notebook sources**. Files under **Post-production boards** are exact current lesson boards, but they contain visible faces and must not be uploaded to Gemini Notebook. Each prompt reserves an uninterrupted narration span for those boards so they can be inserted exactly in post-production.

Paste the prompt into Notebook's video customization box; it is not an extra source document. Use the Markdown, not the older lesson PDF. Do not upload this checklist, the manifest, or archived variants. Save new raw videos to `Prompts/<slug>-reroll.mp4` for evaluation; do not overwrite the live video before approval.

## Scene plan for review

| Lesson | Teaching sequence |
| --- | --- |
| Opener | Normal-looking failures → rip-current analogy → three groups of traps → close |
| Hallucination | Fabricated study reveal → four reasons → real Reddit joke misread → trace the source → close |
| Training Bias | Cow/grass shortcut → three distortions → three questions → historical stale-data chat → RAG → close |
| Document Trap | Tournament exception → split/search/load → RAG → four retrieval moves applied to the rulebook → close |
| Mind Trap | Mom versus chatbot college advice → brief ELIZA → why human language feels human → keep the decision → close |
| Flattery Trap | Gatsby feedback comparison → human-feedback training → brief historical sycophancy failure → five usable feedback moves → close |
| Engagement Trap | Slope question, two endings → infinite scroll removes a decision → deliberately stop or continue → close |
| Support Trap | Sister versus chatbot at lunch → useful preparation versus missing real support → content note and Sophie story → urgent human-help actions → close |
| Fake Trap | School-closure clip → harmless versus harmful fakes → four motives → detector limits → independent source checks → help if targeted → close |

## Opener

- Prompt: `Prompts/opener-avoid-video-prompt.txt`
- Markdown: `lessons/Opener-Avoid.md`
- Notebook sources:
  1. `lessons/opener-avoid-1-traps.jpg`
  2. `lessons/opener-avoid-3-map.jpg`
  3. `lessons/opener-avoid-4-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/opener-avoid-2-read-water.jpg`

## Hallucination

- Prompt: `Prompts/hallucination-video-prompt.txt`
- Markdown: `lessons/hallucination.md`
- Notebook sources:
  1. `lessons/hallucination-1-example.jpg`
  2. `lessons/hallucination-2-why.jpg`
  3. `lessons/hallucination-4-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/hallucination-3-real-text.jpg`

## Training Bias

- Prompt: `Prompts/training-bias-video-prompt.txt`
- Markdown: `lessons/training-bias.md`
- Notebook sources:
  1. `lessons/training-bias-2-mechanisms.jpg`
  2. `lessons/training-bias-3-questions.jpg`
  3. `lessons/training-bias-4-stale.jpg`
  4. `lessons/training-bias-5-rag.jpg`
  5. `lessons/training-bias-6-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/training-bias-1-wrong-pattern.jpg`

## Document Trap

- Prompt: `Prompts/document-trap-video-prompt.txt`
- Markdown: `lessons/document-trap.md`
- Notebook sources:
  1. `lessons/document-trap-2-flow.jpg`
  2. `lessons/document-trap-3-moves.jpg`
  3. `lessons/document-trap-4-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/document-trap-1-uploaded.jpg`

## Mind Trap

- Prompt: `Prompts/mind-trap-video-prompt.txt`
- Markdown: `lessons/mind-trap.md`
- Notebook sources:
  1. `lessons/mind-trap-2-eliza.jpg`
  2. `lessons/mind-trap-3-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/mind-trap-1-comparison.jpg`

## Flattery Trap

- Prompt: `Prompts/flattery-trap-video-prompt.txt`
- Markdown: `lessons/flattery-trap.md`
- Notebook sources:
  1. `lessons/flattery-trap-2-praise-loop.jpg`
  2. `lessons/flattery-trap-3-sycophancy.jpg`
  3. `lessons/flattery-trap-4-five-moves.jpg`
  4. `lessons/flattery-trap-5-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/flattery-trap-1-comparison.jpg`

## Engagement Trap

- Prompt: `Prompts/engagement-trap-video-prompt.txt`
- Markdown: `lessons/engagement-trap.md`
- Notebook sources:
  1. `lessons/engagement-trap-1-comparison.jpg`
  2. `lessons/engagement-trap-2-scroll.jpg`
  3. `lessons/engagement-trap-4-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/engagement-trap-3-stop.jpg`

## Support Trap

- Prompt: `Prompts/support-trap-video-prompt.txt`
- Markdown: `lessons/support-trap.md`
- Notebook sources:
  1. `lessons/support-trap-2-role.jpg`
  2. `lessons/support-trap-3-danger.jpg`
  3. `lessons/support-trap-4-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/support-trap-1-comparison.jpg`

## Fake Trap

- Prompt: `Prompts/fake-trap-video-prompt.txt`
- Markdown: `lessons/fake-trap.md`
- Notebook sources:
  1. `lessons/fake-trap-2-reasons.jpg`
  2. `lessons/fake-trap-4-checks.jpg`
  3. `lessons/fake-trap-5-close.jpg`
- Post-production boards — **do not upload to Gemini Notebook:**
  - `lessons/fake-trap-1-comparison.jpg`
  - `lessons/fake-trap-3-source.jpg`

## Provenance, cleanup, and post-production

- `Prompts/AVOID-TRAPS-SOURCE-MANIFEST.json` records the exact lesson asset, hashes, dimensions, upload status, and prompt word count. Current JPG originals are copied byte-for-byte; Fake Trap's reasons PNG is converted to a high-quality JPG at its original dimensions. Closing text comes directly from `index.html`'s `CLOSE_BOARDS`.
- Superseded video-source images move to `archive/video-materials/avoid-traps-2026-09-04/obsolete/lessons/`. `MOVED-FILES.json` records each original path for recovery. Replaced canonical images are backed up separately under `replaced/`. No live video, page, or original illustration is removed.
- Markdown includes the teaching inside boards as text. Regenerating a plain DOM export alone may omit that text or collapse list formatting; check it against the actual board before replacing these reviewed files.
- In post, insert the exact withheld face boards and replace native Notebook highlights. Highlight complete cards, bubbles, or banners at their true boundaries; subsection highlights inherit the containing box's full horizontal bounds. Use the element's locked accent, protect all text, and maintain balanced vertical clearance.
- Check every edit boundary frame-by-frame in the final render for old-graphic flashes, and listen across each audio cut for clipped words, duplicate breaths, or abrupt transitions. Report timestamps from the final candidate, not the uncut source. Follow `scripts/video/RETROFIT-PLAYBOOK.md` for the full procedure.
