# Understand AI retired video boards — 2026-09-09

The owner requested that retired boards be removed from `lessons/` so they cannot be accidentally uploaded for new videos.

- `obsolete/lessons/` preserves 61 removed source images, including older standalone closing images. The ten current Markdown sources retain their closing messages; the standard closing board is inserted during editing.
- `MOVED-FILES.json` records each original path, archive path, byte count, reason, and SHA-256. To restore an image, copy it to its original path only after checking that no newer file would be overwritten.
- 42 current Understand AI board images remain in `lessons/`. The opener also references `illustrations/opener-understand-under-hood-v3.jpg`, for 43 teaching boards overall.
- All images referenced by current lesson Markdown and direct live-page image paths were protected. Other sections, lesson text, prompt TXT files, PDFs, live illustrations, review copies, and videos were outside this cleanup.

Use the board references in the current lesson Markdown to select uploads. Do not upload these archived images.

Historical rendering scripts and board specifications may still name retired source paths. This archive does not revise those historical recipes. Check the current lesson Markdown before running an older renderer or capture recipe; it may recreate superseded files in `lessons/`.
