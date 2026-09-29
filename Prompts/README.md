# Video production workspace

Keep raw video generations and versioned review candidates here. Use the next unused
filename for every roll or rebuild. Approved videos ship to
`course-assets/<lesson>/<lesson>.mp4` under the shared workflow.

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
