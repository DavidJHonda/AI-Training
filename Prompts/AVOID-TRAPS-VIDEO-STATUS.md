# Avoid Traps Video Production Status

Updated 2026-09-21. The 2026-09-04 owner request was **fresh rerolls for all nine lessons**. Five have
since shipped from new rolls, one shipped as a narration repair over its live spine, and three are
still on their pre-reroll videos with rolls waiting to be reviewed.

| Lesson | Live video | Kit recipe | Next step |
| --- | --- | --- | --- |
| Opener | v6 shipped 2026-09-21 (`20260921ship1`, 4 min) | 2026-09-18 | Done |
| Hallucination | v11 shipped 2026-09-21 (`20260921ship2`, 5 min) | 2026-09-18 | Done |
| Training Bias | v6 shipped 2026-09-21 (`20260921ship3`, 4 min) | 2026-09-18 | Done |
| Document Trap | Pre-reroll (2026-09-08) | 2026-09-18 | Review `document-trap-1…6` |
| Mind Trap | v3 shipped 2026-09-21 (`20260921ship4`, 4 min) | 2026-09-18 | Done |
| Flattery Trap | Pre-reroll (2026-09-08) | 2026-09-18 | Review `flattery-trap-1`, `-2` |
| Engagement Trap | Pre-reroll (2026-09-08) | 2026-09-18 | Review `engagement-trap-1`, `-2` |
| Support Trap | v2 shipped 2026-09-20 (`20260920ship1`, 4 min) — a narration repair over the live spine, not a fresh roll | 2026-09-18 | Rebuild the kit, then reroll |
| Fake Trap | v5 shipped 2026-09-20 (`20260920ship2`, 5 min) | **2026-09-20 (template)** | Done |

Only the Fake Trap kit is on the 2026-09-20 recipe (VOICE block, required-verbatim list, beat spine,
clean upload Markdown, faceless variants of any face board). Every other kit predates it. The five
lessons marked Done shipped from rolls made on the older 2026-09-18 kit and won their reviews, so
their kits need rebuilding only if a reroll is ever needed; the three pre-reroll lessons and Support
Trap should be rebuilt on the 2026-09-20 recipe before anything new is generated. Each lesson's
`Prompts/<slug>-upload-files.txt` carries its own Status line, generated from
`Prompts/upload-sets.json`; edit the registry, not the checklist.

Use [AVOID-TRAPS-VIDEO-KITS.md](AVOID-TRAPS-VIDEO-KITS.md) for the scene plan, the exact
upload/post-production lists, and the shipped-build note for each lesson. Every shipped build keeps its
review in `video-audit/<slug>-*-2026-09-*/REVIEW.md`. No external tracker update is implied by this
status.

Review the teaching first. Notebook-native highlighting and generated closing visuals are expected
post-production replacements, not reasons to reject a good narration. Preserve useful generated
graphics between board scenes. After editing, verify actual card/bubble/banner boundaries, accent
colors, narration alignment, and all transition frames and audio joins before asking for human review.

Earlier audit timestamps referred to older video versions and are intentionally not carried forward as
current defects. Re-evaluate the actual new candidate and report its own timestamps.
