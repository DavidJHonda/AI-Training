# Avoid Traps Video Production Status

Prep status is controlled by `gemini-notebook/upload-sets.json`. Any lesson listed in
`needs_preparation` requires a fresh kit; older “materials ready” or upload directions
below describe historical work and do not authorize reuse.

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
| Support Trap | v4 shipped 2026-09-21 (`20260921ship28`, 4 min) — roll 1 spine, three grafts and an added pause | **Rebuilt 2026-09-29** | **Full-video reroll kit ready; review new narration before selecting it for the edit** |
| Fake Trap | v5 shipped 2026-09-20 (`20260920ship2`, 5 min) | **2026-09-20 (template)** | Done |

**Support Trap update, 2026-09-29:** the full-video reroll kit is rebuilt and registered. David prefers a complete new generation as the narration source rather than an isolated passage. The missing thought-organization benefit is protected verbatim, all four limitations are kept together, and the misleading three-jobs labels are explicitly prohibited. The current video teaches “show up” elsewhere; that is not a globally missing point. See `gemini-notebook/support-trap/PREP-NOTES.md` and the verified live evaluation. New generation and audio selection remain pending; the live release is unchanged.

Kit availability comes from `gemini-notebook/upload-sets.json`; generated READMEs reflect that registry. Historical dates in this table do not establish current prep availability. No external tracker update is implied.

Review the teaching first. Notebook-native highlighting and generated closing visuals are expected
post-production replacements, not reasons to reject a good narration. Preserve useful generated
graphics between board scenes. After editing, verify actual card/bubble/banner boundaries, accent
colors, narration alignment, and all transition frames and audio joins before asking for human review.

Earlier audit timestamps referred to older video versions and are intentionally not carried forward as
current defects. Re-evaluate the actual new candidate and report its own timestamps.
