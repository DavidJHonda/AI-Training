# Video production workspace

Keep raw video generations and versioned review candidates here. Use the next unused
filename for every roll or rebuild. Approved videos ship to
`course-assets/<lesson>/<lesson>.mp4` under the shared workflow.

Use the current lesson title slug for donor rolls as well as finished videos.
Retitles apply to saved local rolls and their production references. Preserve
version numbers and use `-legacy-N` to distinguish older rolls whose names collide.
The original old-to-current file map is `scripts/video/lesson-filename-migration.json`.
The November 4 retitles are recorded in
[`lesson-filename-migration-2026-11-04.json`](../scripts/video/lesson-filename-migration-2026-11-04.json).
That ledger also maps unused rolls, build scripts, audit records, and board files.

| Current lesson | Filename prefix | Installed candidate | Retained versions |
| --- | --- | --- | --- |
| Curiosity | `curiosity` | `curiosity-v3.mp4` | Raw rolls `1`–`3`; new edits `v1`–`v3`; earlier lesson edits `v6`–`v11` |
| What’s Next? | `whats-next` | `whats-next-v12.mp4` | Earlier edits `v6`–`v11` |

An unsuffixed file in `course-assets/<lesson>/` is the installed video. A numeric
suffix such as `-3` identifies a raw roll; `-v3` identifies an edited candidate.
Renaming does not update the words or boards inside older videos. Dates, source
hashes, and review decisions remain in `video-audit/`. Always check the next unused
filename rather than assuming a lower version is older content.

Lesson preparation lives in [`gemini-notebook/`](../gemini-notebook/README.txt):
editable prompts, upload variants, lesson notes, and the upload registry. Shared
rules are in the [Preparation guide](../scripts/video/PREPARATION.md) and
[video workflow](../scripts/video/README.md). Section context lives in
[`scripts/video/kits/`](../scripts/video/kits/README.md).

`narration-repairs/` retains production audio and its provenance. Keep source rolls,
repair audio, and active candidates until their removal is authorized.

Do not store new generation prompts, upload checklists, prep JPGs, or section kits
here. Old prep paths can be looked up in
[`prep-path-migration.json`](../scripts/video/prep-path-migration.json).
