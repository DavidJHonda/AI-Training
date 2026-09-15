# Course assets

Boards and illustrations are grouped by lesson. Lesson text stays in `lessons/`; LAB packets stay in `packets/`.

- Approved website credits are part of the standard JPG. There are no separate `-attributed` files or uncredited originals for these boards.
- Do not recreate `source-illustrations` folders. Removed source records remain in the manifest for historical reference.
- Keep filenames, dimensions, and teaching-content positions stable. Video highlights depend on that geometry.
- Shared lesson filenames remain separate; byte-identical copies of upgraded boards carry the same website credit.
- `manifest.json` maps every original path to its current canonical file. It records current hashes, original migration hashes, deduplication history, and credited-file renames.

## Generating boards

Python image writers use `scripts/video/course_credit.py`'s `save_course_image` in place of Pillow `save` for outputs in this folder. Unapproved or non-course outputs pass through unchanged. The approved footer patch is reset before drawing, so credit text does not accumulate. Unexpected dimensions fail rather than moving the footer or teaching content.

Native and shell generators call `bash scripts/finalize-course-asset.sh PATH` immediately after writing an output. Already credited canonical bytes and stamped exports are skipped. `COURSE_ASSET_PYTHON` can select a Python interpreter with Pillow; the default uses `.video-venv/bin/python3` when present.

Footer placement/background recipes live in `scripts/video/course-credit-policy.json`. They contain only the small reserved footer background patches, not copies of the teaching boards. Update the recipe intentionally if a board's canvas or footer design changes.

`render_selected_board_attributions.py` is retained as a compatibility command. It finalizes standard filenames in place and does not create derivatives.

## Verification

`python3 scripts/verify-course-assets.py --migration-hashes` verifies the current approved canonical hashes and every website image/PDF path. The option name is retained for existing workflows; `migration_sha256` in the manifest preserves the original pre-credit hash where different. Historical audit records may still name removed originals or attributed files.
