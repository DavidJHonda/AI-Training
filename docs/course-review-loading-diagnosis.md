# Course Reviews loading investigation — September 14, 2026

## What the live evidence establishes

The original screenshot showed the **Student Reviews** loading error below a successful submission/thank-you screen. Independent GET requests made during that incident also returned HTTP 200 with `{"error":"Student reviews could not be loaded."}` after 11.4 and 11.5 seconds. Those requests did not submit a review, edit a review, or include a pagination cursor. The Google execution screenshots showed similar 10–11-second durations, followed by a recovered 1.71-second request.

Two read-only checks during this investigation succeeded in 2.36 and 1.64 seconds. Each returned five public reviews, five total ratings, and no older-page cursor. No live reviews were added or edited for testing.

**The failing operation was the public-list read.** Loading older pages was not involved in those observed failing requests. Normal submission and editing pass the isolated tests. This does not rule out a concurrent write as a trigger for the earlier read failure.

The original server exception is unavailable. Lock contention matches the timing and reproduces the symptom, but the exact historical cause and the execution holding the lock cannot be established from these screenshots or the generic response alone. The fixes below address demonstrated code defects; they are not proof of that missing historical exception.

## Reproductions and fixes

Tests run the actual Apps Script handlers and public-list component using isolated spreadsheet fixtures, a controllable lock, and a virtual clock. The same cases were run against a saved copy of the pre-fix source and the revised source.

| Case | Before | After |
| --- | --- | --- |
| New submission, edit, then return to the page | Pass; same row, original Submitted At, count unchanged on edit | Pass |
| Public-list read while another execution holds the script lock | Lock timeout becomes the displayed loading error | Read succeeds without acquiring that lock |
| Refresh 45 already-loaded reviews, with each of three page requests taking 8 seconds | Shared 20-second deadline aborts the healthy third request | All 45 reviews return; each request has its own 20-second deadline |
| One page takes longer than 20 seconds | Times out | Still times out |
| Unmount while loading, then return | Cancelled request does not populate the new component | Pass |
| Read at an edit's write boundary | Read waits on writer; edit uses two range writes | Edit uses one range write; reader sees the changed fields together |
| Publication withdrawal during an edit | Existing privacy tests pass | Read at the write boundary excludes the private text; rating remains counted |
| Two writes targeting the same review ID | Existing upsert tests pass | Write lock still prevents overlapping writes; retry updates one row |

Public reads no longer use the script-wide lock shared with review writes and certificate processing. Review writers still acquire that lock. An edit now writes all mutable review fields in a single contiguous range operation, preserving Submitted At and the values of retired columns in the legacy layout. `SpreadsheetApp.flush()` commits the write before releasing the lock. Public responses still contain only the allowed review fields and aggregate rating data.

The frontend change only moves the deadline from the entire refresh to each individual page request, and discards cancelled responses before processing another page. The page design, form, thank-you screen, Google Sheet, and refresh schedule are unchanged.

## Diagnostics for a future failure

The public endpoint now adds a non-sensitive `code` to an error response:

- `REVIEWS_REQUEST_FAILED`: request or cursor processing.
- `REVIEWS_LAYOUT_FAILED`: obtaining/validating the supported sheet layout.
- `REVIEWS_READ_FAILED`: obtaining the sheet or reading its review data.
- `REVIEWS_FORMAT_FAILED`: filtering, sorting, calculating, or formatting the response.

These identify the phase where the exception occurred, not necessarily its ultimate cause. The server log also records elapsed time and the exception. Exception text, spreadsheet identifiers, and private review fields are never returned to the browser. The error displayed on the course page remains unchanged. These codes become available only after redeployment.

## Verification

Run from the repository root:

```sh
node scripts/test_course_reviews.cjs
node scripts/test_review_loading_failures.cjs
git diff --check
```

All checks passed. Coverage includes compact and legacy layouts, new submissions, editable names, edits, lost-response retries, ordering, pagination resets, publication withdrawals, privacy filtering, average/count updates, registration, and certificates. The new reproduction suite covers lock contention, slow multi-page refreshes, stalled requests, cancellation, and safe error codes.

The 1,000-review fixture returns 50 pages of 20 reviews with no omissions or duplicates and no private fields. That run makes 150 sheet-range reads (headers, layout discriminator, and review data per page), down from 50 read-lock acquisitions to zero. This is a functional/service-call-count test using mocked Google services, **not a Google latency or concurrent-traffic benchmark**.

## Caching and refresh assessment

Caching is worthwhile if traffic grows: pagination currently rereads and processes the whole sheet for each 20-review page. A short-lived cache of the public fields and rating summary would reduce this work. It should be versioned and invalidated on accepted submissions/edits, split into entries within Google's 100 KB cache-value limit, tolerate early eviction, and expire promptly so direct sheet changes are reflected. Cache construction and invalidation must be designed to avoid serving a stale publication permission after an edit.

Reducing redundant automatic refreshes is also worthwhile, but lower priority at current volume. Focus and visibility events can each cause a refresh if the previous request has already completed; a short freshness window can suppress that duplication. A lightweight version check could avoid refetching all loaded pages when nothing changed. Immediate refresh after submission/edit should remain. Simply lengthening the one-minute poll trades fewer reads for slower appearance of edits and withdrawals.

Neither caching nor the refresh schedule was changed in this fix. First deploy and observe these corrections. They remove the reproduced read-lock dependency and multi-page deadline failure without adding cache consistency concerns.

## Deployment and remaining limitation

Replace the existing Apps Script handler with `google-apps-script.gs`, then use **Deploy → Manage deployments → Edit → New version → Deploy**, retaining the existing URL and access settings. Publish the revised `index.html` through the existing website process. No spreadsheet column changes are required. Detailed instructions are in [course-review-deployment.md](course-review-deployment.md).

The code is verified locally. The course account's deployment is not accessible in the connected browser, so this investigation has **not deployed or verified the fixes against live Google services**. After deployment, verify a genuine submission, an edit, and returning to the page. Older-page behavior can be tested against a private staging sheet with fixtures rather than adding sample reviews to the production sheet.

References: [Google's lock and flush guidance](https://developers.google.com/apps-script/reference/lock/lock#releaselock), [batch-operation best practices](https://developers.google.com/apps-script/guides/support/best-practices), and [CacheService limits and behavior](https://developers.google.com/apps-script/reference/cache/cache).
