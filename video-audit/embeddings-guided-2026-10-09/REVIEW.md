# Embeddings v14: lesson demonstration video update

Review candidate: `Prompts/embeddings-v14.mp4`. The installed course video remains
v12. No commit, installation, upload, or deployment was performed.

## Scope and result

Narrow visual update following the approved lesson changes. The first illustration
uses the exact lesson display crop, removing the yellow banner and shortening its
frame while preserving the complete title and photograph. The two static drink
boards are replaced by captures of the shared live table, with progressive rows,
term highlights, and Citrus introduced before its values.

Narration explicitly places Coke above Coffee in the first example, so the video
uses that initial order. On “This updated table,” Coffee moves above Coke before
Pepsi appears beneath it. The colas remain adjacent through the final comparison.
The live interactive's Coffee-first sequence is unchanged.

The original mystery-drink and matching-can animations remain. Visual review of
v13 found the mystery animation's inherited ten-frame dissolve briefly brought
back the retired table. V14 rerenders those first ten frames using the original
animation code, starting directly on the intended scene. All other supporting
scenes, downstream boards, narration, pauses, and the standard close remain.

## Changed spans

- 18.367–34.633: banner-free student-ID illustration.
- 64.333–86.300: table headings, Coke, Coffee, and named values.
- 86.300–86.633: repair old-board contamination at the mystery-animation opening.
- 95.900–106.500: vector, dimension, and value with the corresponding table region.
- 106.500–116.300: reordered table, Pepsi, and its first six values.
- 122.800–137.200: compare profiles, add Citrus with empty tiles, then reveal
  Pepsi 10, Coke 1, and Coffee 0 at the spoken values.

Longest changed table run: 21.967 seconds, with successive reveals and highlights.
Preserved supporting scenes and the board/camera plan are in `EDIT-PLAN.md`.
The capture script reuses the lesson's data and render function. Video-only sizing,
4 px outlines, and short term labels replace the live instruction card and buttons.

## Sources and verification

Source is the stable finished `Prompts/embeddings-v12.mp4`, matching the installed
video at the start. SHA-256:
`b6fcc8211b27ea97ab25b6dedc94eba7c692bb94ff773071aa2e7aa730e19806`.
Original raw generations are absent, so the finished source was reencoded once.
V14 was rebuilt directly from v12, not from v13.

`edit-manifest.json` records exact frame ranges, capture paths, hashes and protected
files. `verification.json` records full sequential decode, unchanged-span error,
encoded/decoded audio identity, and final candidate SHA-256. The timeline remains
7,997 frames, 30 fps, 1280×720, 4:26.567. Audio was copied without edits.

Frame captures and changed-state contact sheets were visually inspected. The
transition guard checks all declared boundaries. Its still strips support
inspection of row reveals, Citrus stages, the source cutaways, and the repaired
mystery entry. The review page includes jump controls for each changed section.

## Limits

No end-to-end listening review of the candidate was performed. Compressed AAC
and decoded PCM identity preserve the approved source audio, but are not a new
listening verdict. Full-file narration and production checks outside the changed
spans were not repeated. This is a review candidate, not a shipping sign-off.

The lesson Markdown and Notebook upload bundle were not regenerated: this is an
existing-video visual repair, not preparation for a new narrated roll.

Final v14 checks passed: 7,997 decoded frames; 2,201 changed and 5,796 retained
frames; compressed audio and decoded PCM identical; 38 declared-boundary checks
passed with zero failures. The repaired mystery entry strip was inspected and
contains no retired board. Candidate SHA-256:
`092325b3ce30c4508f7ad280018b1e06b93ed27953e2d686d45eeef5e86a7c61`.

Browser metadata, playback, and the Citrus timestamp control passed. The ordinary
Python preview server did not support seeking, so the review runs through the
local range-capable server at port 8766. Review URL:
http://127.0.0.1:8766/video-audit/embeddings-guided-2026-10-09/review.html
