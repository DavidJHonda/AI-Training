# Trap Lesson Playbook

Distilled from the Mind Trap rebuild (2026-07-21). The standard for every Avoid Traps lesson. Mind Trap (`MindTrapSection` in index.html) is the reference implementation.

## Structure, in order

1. **Opener** — one or two short paragraphs. May carry the section-position bridge. No cross-references to other lesson titles. Ends by promising what this lesson explains.
2. **Demonstration** — ONE concrete worked example the reader can see, early. Prefer a comparison or demo box (tinted-panel format) where the contrast IS the lesson. A box must demonstrate, never restate.
3. **Thesis** — one bolded sentence in plain behavioral language: "X Trap is [verb]-ing ..." Names the mistake as an action. Shorter is better; Mind Trap's is seven words. Sits directly after the demonstration.
4. **Illustration** — if one exists, it goes after the thesis.
5. **History or evidence beat** (optional) — one short kickered body-text beat (the ELIZA pattern). Body text, not a card.
6. **Mechanism** — ONE box explaining why the trap works. Two or three cards max. No duplicate lists across cards. Kicker optional.
7. **Advice** — a KeyInsight with a behavioral rule ("Don't ..."), including what AI IS still good for. Instruction, not restatement.
8. **Close board** — carries the landing. The KeyInsight must not restate it.
9. **TRY IT** — drills the ONE core rule. Same simple question repeated across escalating stakes; wrong answers punish over-trust AND overcorrection; include one rep that defines the rule's boundary (where the trap does NOT apply). No orphaned vocabulary from cut content.
10. **Gate** — no end-of-lesson handoffs; the next lesson's opener owns bridges.

## Cut list (delete on sight)

- Boxes that restate what prose or another box already showed
- Vocabulary detours: terms defined but never used again in the course
- Mid-lesson pre-runs of other lessons' material (each trap owns its territory; at most one teaser sentence, ideally none)
- "Don't overcorrect" hedge sections — overcorrection teaching lives in TRY IT wrong-answer feedback
- KeyInsights that restate the close board
- Any concept stated three or more times: cut the weakest instance, keep the demonstration
- Stale references: audit every TRY IT hint, feedback, and headline for terms and framing from content that was cut

## Copy rules

- David's voice: short sentences, colon setups, balanced contrast, no em dashes, no exclamation points outside quoted AI speech
- AI's answer in any demonstration is UNGROUNDED, not wrong: polished, confident, could have been written for anyone. Never "AI gives bad advice"
- Human answers in demonstrations contain knowledge no typed question holds (failure modes, watched history, stakes) plus concrete grounding
- Numbers: only the lesson's own; never invented stats

## Process per lesson

1. Fresh-eyes deep eval: redundancy map, staleness and orphans, TRY IT alignment with the current thesis, cross-lesson overlap, flow seams, voice nits
2. Edit plan: cuts, rebuilds, and at most four judgment calls reserved for David
3. Execute only after approval; then syntax check, design-check.sh, validate(), and re-export the lesson's .md and .pdf
4. Verify the kicker carries the trap's angle and the close board is the landing
