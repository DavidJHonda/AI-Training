# When You Need More — shipped locally

Date: 2026-11-03. Authorization: owner said “ship it” after reviewing the delivered v7 candidate and disclosure that direct listening was unavailable. This authorizes shipping; it is not evidence of an independent end-to-end listening pass.

- Local commit: `b4993f70fceb7cb65bb1af627e7b418c68322afa`.
- Approved candidate: `Prompts/when-you-need-more-v7.mp4`.
- Installed: `course-assets/when-you-need-more/when-you-need-more.mp4`.
- SHA-256: `ae5499e7373e2cbd5231c4cebbdd1b3df3a5814c1e540729b427ba9a0cb8eaf3`.
- Bytes: 12018364.
- Duration: 168.966667 seconds; page label 3 min.
- Cache: `20261103ship7`; lesson ID `choosemodel`.
- Status: **shipped locally; queued for batch deployment**. No push or deployment performed.

The commit includes the approved current lesson, three banner-free boards, eight-step Career Explorer project setup and follow-on project wording, preparation sources, video, and scoped manifest metadata. Unrelated Big Upside/Big Downside work remains unstaged.

Verification: installed bytes equal the reviewed candidate; asset migration/hash verifier passes (248 assets, 519 mappings, 263 website references, 55 videos); staged inline JavaScript parses; staged diff passes whitespace and scope checks. Local browser opens the actual lesson player and reports the new cache URL, 168.966667 seconds, 1280 × 720, no media error, and no JavaScript errors. Page shows 3 min and the project setup step. See `local-browser-qa.json` and `shipped-local-page.png`.

Encoded candidate checks are recorded in `BUILD-REVIEW.md`, `encoded-qa.json`, and `transitions/`. Owner shipping approval follows the stated listening limitation; no automated or transcript check is represented as direct listening. The Video Tracker was not accessed or updated; David maintains it.

Regenerable render scratch is removed only within When You Need More audit folders after this commit; review records, transcripts, images, source rolls, and candidates are retained.
