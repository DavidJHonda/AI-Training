# Avoid Traps Video Production Status

Updated 2026-09-21. The 2026-09-04 owner request was **fresh rerolls for all nine lessons**. All nine
are now off their pre-reroll videos: eight shipped from new rolls and one (Support Trap) shipped as a
narration repair over its live spine. Support Trap has since been rebuilt from a fresh roll too, so all
nine now run on new narration.

Document Trap is the exception to the reroll-until-it-lands method, and worth reading before the next
lesson stalls: ten rolls never landed its eleven required lines in one take (best 7 of 10), and the kit
revision aimed at the three stragglers made it worse (3 of 11). It shipped instead as a stitch of the
best take of each beat from three rolls. When a lesson has several rolls that are each strong in
different places, assembling beats the eleventh roll — see
`video-audit/document-trap-stitch-2026-09-21/REVIEW.md` and `scripts/video/build_document_trap_v1.py`.
Engagement Trap went the same way and further: five grafts, and two of them replace a course board that
the narration had already moved past with the roll's own footage of that beat.

**Read this before the next stitch.** Notebook holds its previous panel for a few frames after the audio
has moved on, so *every* picture boundary risks a stale frame at its leading edge — five instances in
Engagement Trap alone. `transition_guard` flags two visual cuts within six frames and therefore does
**not** catch the longer ones: its 1:26 leak ran nine frames, passed the gate, and was found only by
watching. Inspect the frames either side of every picture edge, not just the ones the guard flags. The
companion audio rule: a picture boundary may sit anywhere, but an audio boundary must land in a measured
silence **in the file being cut** — `keep()` crossfades its own row edges into room tone, so a split in
running speech punches a hole (a 30 dB one, in that build).

| Lesson | Live video | Kit recipe | Next step |
| --- | --- | --- | --- |
| Opener | v6 shipped 2026-09-21 (`20260921ship1`, 4 min) | 2026-09-18 | Done |
| Hallucination | v11 shipped 2026-09-21 (`20260921ship2`, 5 min) | 2026-09-18 | Done |
| Training Bias | v6 shipped 2026-09-21 (`20260921ship3`, 4 min) | 2026-09-18 | Done |
| Document Trap | v1 shipped 2026-09-21 (`20260921ship7`, 4 min) — stitched from rolls 7, 8 and 3, not won by a single roll | 2026-09-18 | Done |
| Mind Trap | v3 shipped 2026-09-21 (`20260921ship4`, 4 min) | 2026-09-18 | Done |
| Flattery Trap | v6 shipped 2026-09-21 (`20260921ship5`, 5 min) | 2026-09-18 | Done |
| Engagement Trap | v10 shipped 2026-09-21 (`20260921ship22`, 4 min) — roll 4 spine, five grafts from the live video, roll 2 and roll 1 | 2026-09-18 | Done |
| Support Trap | v4 shipped 2026-09-21 (`20260921ship28`, 4 min) — roll 1 spine, three grafts and an added pause | 2026-09-18 | **Board 2 still thin — reroll when the kit is rebuilt** |
| Fake Trap | v5 shipped 2026-09-20 (`20260920ship2`, 5 min) | **2026-09-20 (template)** | Done |

Only the Fake Trap kit is on the 2026-09-20 recipe (VOICE block, required-verbatim list, beat spine,
clean upload Markdown, faceless variants of any face board). Every other kit predates it. The eight
lessons marked Done shipped from rolls made on the older 2026-09-18 kit and won their reviews, so
their kits need rebuilding only if a reroll is ever needed. Support Trap is the one lesson with a known
reason to reroll: **no version of its Board 2 is complete.** The lesson lists three things AI can do and
four it cannot; roll 1 speaks two and three, roll 2 a different two and three, and the old live video's
sentence was broken outright ("Notice what you leave out of your prompts"). Editing cannot fix it -
rebuild that kit on the 2026-09-20 recipe and roll again when there is time. Each lesson's
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
