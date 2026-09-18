# Course assets

Finished videos, boards, and illustrations are grouped by lesson. Lesson text stays in `lessons/`; LAB packets stay in `packets/`.

- Approved website credits are part of the standard JPG. There are no separate `-attributed` files or uncredited originals for these boards.
- Do not recreate `source-illustrations` folders. Removed source records remain in the manifest for historical reference.
- Name lesson boards, illustrations, and downloads `<lesson-folder>-<content-description>.<extension>`, using lowercase words separated by hyphens. Omit sequence numbers and version or implementation labels. Examples: `welcome-course-toolkit.jpg`, `your-home-base-big-three.jpg`, and `context-window-close.jpg`. Meaningful words such as `four-moves` remain. Shared assets use descriptive names.
- Keep approved filenames stable after this standardization. Update all references when a rename is necessary. Never change dimensions or teaching-content positions as part of a filename cleanup; video highlights depend on that geometry.
- Shared lesson filenames remain separate; byte-identical copies of upgraded boards carry the same website credit.
- `manifest.json` maps every original path to its current canonical file. It records current hashes, original migration hashes, deduplication history, and previous filenames. Original generator aliases resolve to the current files through `scripts/video/course_asset_paths.py`.

## Videos

Each finished lesson video is `course-assets/<lesson>/<lesson>.mp4`. The Layers activity video (AI Brain Break) lives in its own folder, `course-assets/ai-brain-break/`, with the seven on-screen cards as JPGs. `index.html` defines the videos students see. Raw generations and pending candidates stay in `Prompts/`; candidates retain their version suffix until approved. The old `videos/` directory is retired.

`manifest.json` records the migrated video paths and approved hashes under `video_assets`. When an approved finished video is replaced, update its hash and size in that record.

## Generating boards

Python image writers use `scripts/video/course_credit.py`'s `save_course_image` in place of Pillow `save` for outputs in this folder. Unapproved or non-course outputs pass through unchanged. The approved footer patch is reset before drawing, so credit text does not accumulate. Unexpected dimensions fail rather than moving the footer or teaching content.

Native and shell generators call `bash scripts/finalize-course-asset.sh PATH` immediately after writing an output. Already credited canonical bytes and stamped exports are skipped. `COURSE_ASSET_PYTHON` can select a Python interpreter with Pillow; the default uses `.video-venv/bin/python3` when present.

Footer placement/background recipes live in `scripts/video/course-credit-policy.json`. They contain only the small reserved footer background patches, not copies of the teaching boards. Update the recipe intentionally if a board's canvas or footer design changes.

`render_selected_board_attributions.py` is retained as a compatibility command. It finalizes standard filenames in place and does not create derivatives.

## Verification

`python3 scripts/verify-course-assets.py --migration-hashes` verifies the current approved canonical hashes and every website image/PDF/video path and finished video hash. The option name is retained for existing workflows; `migration_sha256` in the manifest preserves the original pre-credit hash where different. Historical audit records may still name removed originals or attributed files.
