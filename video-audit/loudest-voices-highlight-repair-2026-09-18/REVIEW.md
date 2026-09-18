# Loudest Voices — highlight and camera correction

## Recommendation

**KEEP the corrected visual candidate for owner review.** The highlight geometry and camera emphasis now follow the spoken structure. This remains a review candidate and was not published.

## Candidate

- Video: `Prompts/loudest-voices-v5.mp4`
- Duration: 3:54.90 at 30 fps
- Planned and decoded frames: 7,047
- SHA-256: `d77eae1ee7766b03d6119ae39113f6912c732f1605145ea40891fcfc3abda23b`
- Base and donor narration, lesson text, course boards, and close asset are unchanged.

## Corrections made

- Audited all nine expert-board highlight states and all five prediction-board states.
- Each expert introduction now remains on the complete three-person board and rings that expert's full card.
- Each `SAYS` and `BUT ADMITS` passage now has its own section-level crop.
- Every section ring includes the section heading and the complete quotation. No ring stroke crosses `SAYS`, `BUT ADMITS`, or quotation text.
- Camera moves complete at the corresponding spoken onset rather than beginning after the words start.
- The LeCun `SAYS` passage is now shown and highlighted on the course board. The former `A DEAD END` Notebook interruption was removed because it hid that spoken section.
- The Hinton board return now lands on a settled crop before the spoken-section ring appears.
- The four historical examples retain complete-card zooms and rings; their camera moves now also land at spoken onset.
- The prediction takeaway returns to the full board and highlights the complete banner.
- No teaching pauses or narration edits were added.

## Verification

- Transition guard: **PASS**, 7/7 actual visual splices, 0 failures.
- Manual every-frame strips: inspected for all seven visual splices; no stale visual islands or one-frame leaks found.
- Expert and prediction state sheets: inspected at every ring state.
- Full 4-second contact-sheet pass: inspected from opening through settled close; no incorrect ring, broken crop, blank frame, or unexpected photograph found.
- Full candidate transcript: teaching content unchanged and complete.
- Protected source, lesson, and board hashes: unchanged.

## Review artifacts

- `states-experts.jpg`: all expert introduction and subsection states.
- `states-predictions.jpg`: all historical-example and takeaway states.
- `transitions-v5/transition-guard.md`: final automated transition result.
- `edit-manifest.json`: output timeline, target geometry, camera beats, hashes, and render metadata.

## Scope note

The previous candidate was not overwritten. `loudest-voices-v5.mp4` is the corrected version to review. Nothing was deployed or copied over the live course video.


## Shipped

**SHIPPED 2026-09-18** on David's approval ("Ship loudest-voices-v5"): v5 copied to `course-assets/loudest-voices/loudest-voices.mp4` (SHA-256 verified before and after the copy, `d77eae1e…`), v3/v4/v5 candidates removed, `index.html` video src given cache key `?v=20260918ship1` and the pill 5 min → 4 min, `course-assets/manifest.json` entry updated. See `shipping-receipt.json`.
