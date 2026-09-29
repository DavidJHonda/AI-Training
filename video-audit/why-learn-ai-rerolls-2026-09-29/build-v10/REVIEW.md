# Why Learn AI? v10 — shipped locally; queued for batch deployment

Owner correction, September 29, 2026: the four new custom graphics in v9 were
too cartoonish. This revision uses photographic images, with realistic
high-school-age students in the chatbot and project-feedback scenes.

[Review video](/Users/davidobrien/Developer/AI-Training/Prompts/why-learn-ai-v10.mp4)

| Finished-video time | Replacement and teaching purpose |
|---|---|
| 1:10.30–1:13.30 | Realistic smartphone navigation screen: route and traffic assistance. |
| 1:31.80–1:37.30 | High school student using a chatbot at a library desk. |
| 2:48.20–2:53.20 | High school student using feedback to revise a school project. |
| 3:29.40–3:40.70 | Photographic illustrative strategy-document cover; title and date support the quotation. |

All four inserts retain their exact v9 spans and gentle 2.5% camera push. The
student images are purpose-generated, not photographs of identified people.
The document is an illustrative prop, not a reproduction of an official cover.
Existing Notebook drawings and animations, both owner-approved numerical charts,
canonical course boards, narration, and total timing remain as in v9.

## Build and verification

The video is rendered from pristine source footage and canonical board assets,
with v9's AAC stream copied directly. The build verifies matching audio packet
hashes and the same 7,075-frame visual timeline (3:55.83 at 30 fps, 1280×720).
Source videos, live course MP4, lesson, canonical boards, and v9 are protected.
The owner authorized shipping with “ship it.” The candidate is installed at the
canonical course path and committed locally. Public deployment remains pending.

All eight changed boundaries passed the transition guard and visual inspection.
The encoded first/middle/last frames of all four inserts passed crop and
readability review. Samples from every untouched span were pixel-identical to
v9. The audio packet hash is identical. Verification results are in
`checks.json`, `edit-manifest.json`, and `guard/`.
The targeted visual review covers the first, middle, and last frame of each
replacement and every frame around all eight changed boundaries. Samples from
every unaffected scene are compared against v9. Audio wording and earlier
listening limitations carry forward from the [v9 review](/Users/davidobrien/Developer/AI-Training/video-audit/why-learn-ai-rerolls-2026-09-29/build-v9/REVIEW.md);
direct listening and continuous real-time playback have not been performed.

## Saved images and prompts

Created with the built-in image_gen tool using the imagegen skill; each image
was generated separately in photographic style.

- [Navigation](/Users/davidobrien/Developer/AI-Training/video-audit/why-learn-ai-rerolls-2026-09-29/build-v10/assets/navigation.png)
- [Chatbot student](/Users/davidobrien/Developer/AI-Training/video-audit/why-learn-ai-rerolls-2026-09-29/build-v10/assets/chatbot.png)
- [Project-feedback student](/Users/davidobrien/Developer/AI-Training/video-audit/why-learn-ai-rerolls-2026-09-29/build-v10/assets/feedback.png)
- [Illustrative strategy document](/Users/davidobrien/Developer/AI-Training/video-audit/why-learn-ai-rerolls-2026-09-29/build-v10/assets/document.png)
- [Exact prompt set and generation record](/Users/davidobrien/Developer/AI-Training/video-audit/why-learn-ai-rerolls-2026-09-29/build-v10/assets/generation-record.json)
- [Build script](/Users/davidobrien/Developer/AI-Training/scripts/video/build_why_learn_ai_v10.py)

Rule 8d in [EDIT-SPEC.md](/Users/davidobrien/Developer/AI-Training/scripts/video/EDIT-SPEC.md)
now records the owner's photographic preference for new custom supporting images.
It preserves useful existing Notebook animation and retains the separate
restriction on unknown-source Notebook stock photographs.

## Local shipping record

Commit: `f9da557aa45a8c9167e9b1454c725c99a7fae85d`. Installed SHA-256: `f7cab5a37d9c1f8ae141f1f2bcfadb441dd4341dedad782eb1684b63e9c6bd79`.
The release commit contains only the canonical MP4 and the lesson cache-key
update to `20260929ship10`; displayed runtime remains 4 min. Installed and
committed video hashes match the approved candidate. Full decode succeeded,
and the shipping guard passed all 28 declared visual/audio boundaries.

No GitHub push or deployment was triggered. Direct listening was not performed;
the earlier limitation remains recorded, with the owner’s subsequent shipping
authorization. Regenerable scratch was cleaned only from this lesson’s v9/v10
build folders (20 files, approximately 0.25 GB).
