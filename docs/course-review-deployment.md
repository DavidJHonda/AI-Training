# Deploy the course review form and public list

The local form in `index.html` now asks for a required five-star usefulness rating, an optional written review, and optional private improvement feedback. The notice above Submit says: “Your rating counts toward the course average. Your written review will appear publicly with your first name or nickname. Your suggestions for improvement stay private.” Whenever a student enters written review text, an editable **Your first name or nickname** field appears, initially filled with their registration first name. A saved choice survives reloads and editing. Submitting nonempty review text records `first_name` permission and the value shown in that field; an empty name must be filled before publishing. Rating-only submissions record `none`. The button reads **Post my review** when written review text is present, or **Submit my rating** for stars only, including submissions with private improvement feedback. Whitespace-only review text counts as empty. Draft saving and submission retry remain available. The thank-you screen offers **Edit my review**, which reopens the saved rating and written responses. Resubmission updates the same review ID and row. A scrollable **Student Reviews** list appears below both the form and the thank-you screen.

## Loading reliability update — September 14, 2026

This update **requires a new version of the existing Apps Script deployment** and the updated `index.html`. No sheet-column changes are needed. Public-list reads no longer wait on the shared write lock. Review edits write their changed fields together and flush before releasing the write lock. Each loaded page now gets its own 20-second timeout. Safe error codes identify the phase of a future server failure. The current design and one-minute refresh schedule are unchanged; caching has not been added.

See [the diagnosis and verification report](course-review-loading-diagnosis.md) for the observed live failure, controlled before/after reproductions, limitations, and caching assessment.

## Previous form update

The three-option permission section has been replaced by the publication notice. Keep **Quote Permission** and **Quote First Name** in the spreadsheet. They retain historical private/anonymous choices and keep the public feed correctly filtered. Existing records are unchanged until the student explicitly resubmits. **Edit my review** preserves the saved answers and review ID; the server updates the existing row without increasing the rating count. Retries also reuse that ID so a lost response does not create duplicates. Submitted At stays unchanged, while Updated At and the public rating/text reflect the edit. Clearing the written review and resubmitting removes it from the public list while keeping the rating and private improvement feedback.

The previous form-only changes used the existing payload. The loading reliability update above also changes the backend, so follow the deployment steps below even if the public-list/average-rating script is already deployed.

## Update the existing Apps Script deployment first

1. Open the Google Apps Script project currently receiving course registrations, certificates, and reviews. If it is bound to the response spreadsheet, open that spreadsheet and choose **Extensions → Apps Script**.
2. Replace the contents of the existing handler file (usually `Code.gs`) with the complete contents of this project's `google-apps-script.gs`. Replace the handler rather than adding a second copy of `doPost` or `doGet`. Save the project.
3. Choose **Deploy → Manage deployments**. Select the active web app whose URL matches `SIGNUP_ENDPOINT` in `index.html`.
4. Click **Edit** (pencil). Under **Version**, choose **New version**, add a description such as “Fix public review loading and save edits in one range update,” and click **Deploy**. The web app must execute as the course account that can read **Course Users** and allow **Anyone** to access the endpoint. Keep these settings if they are already configured. Keep the **Course Users spreadsheet itself private**; do not publish or share the spreadsheet publicly.
5. Keep the existing web app URL in `index.html`. Editing the existing deployment to use a new version preserves its URL; creating a separate deployment is unnecessary. Saving the source alone does not update the deployed version.
6. **Only for a previously requested migration from the original 14-column layout:** open the **Reviews** tab and select the four original columns **G–J** together: **Confidence Before**, **Confidence After**, **Most Useful**, and **What Changed**. Right-click and choose **Delete columns G–J**. Delete the columns, rather than just clearing their contents. If G is already **Improvement** and J is **Quote First Name**, the sheet is already compact; skip this step.
7. Publish the updated `index.html` through the course's normal website deployment process if it has not already been published.

Google documents this workflow in [Create and manage deployments](https://developers.google.com/apps-script/concepts/deployments#edit_a_versioned_deployment).

## Existing spreadsheet data

The final Reviews layout has 10 columns, A–J:

| Column | Behavior |
| --- | --- |
| A: Submitted At | Set for a new row; untouched on edits and submission retries. |
| B: Updated At | Refreshed on every accepted submission. |
| C: Review ID | Matches edits and retries to the same row. |
| D: Student ID | Identifies the student. |
| E: Course Version | Records the submitted course version. |
| F: Usefulness Rating | Required whole number from 1 to 5. |
| G: Improvement | Private improvement feedback. Never covered by publication permission. |
| H: Testimonial | Optional written review. |
| I: Quote Permission | Permission for column H only. |
| J: Quote First Name | Attribution for the written review. |

Deleting the four retired columns removes their historical answers. All remaining columns and their data shift left together. The script does not delete columns itself.

Deploy the script before deleting the columns. It supports both the original 14-column layout and the final 10-column layout, detecting which to use from the headers. It preserves retired answers while the original columns still exist and creates new Reviews tabs with only the 10 current columns. A partial deletion or unexpected header layout is rejected before writing review data. Registration and course-completion handling are unchanged.

## Public review feed

The updated script serves JSON at the existing web app URL plus `?action=public_reviews`. It reads the **Reviews** tab in the same spreadsheet used by registration and completion handling. No new sheet, spreadsheet sharing, or website endpoint URL is needed.

Above the scrolling list, the page displays the average star rating to one decimal place and a count labeled **ratings** (or **rating** for one). The average includes every valid submitted 1–5 rating, including private reviews and submissions without written text. Editing a rating changes the average without increasing the count. Edits and retries keep the same review ID. With zero ratings, the page shows **No ratings yet** and **0 ratings**. Invalid rating cells are ignored.

The JSON response includes `ratingSummary: { average, total }`, computed from the full sheet rather than the current batch; `average` is `null` when `total` is zero. Only the aggregate is exposed for private/rating-only submissions. Each written-review entry contains only `rating`, `text`, `submittedAt`, and `name`. Only nonempty written reviews with `anonymous` or `first_name` permission are returned, including one-star ratings. Anonymous permission always hides the stored name. Improvement feedback, review IDs, student IDs, course versions, updated timestamps, and other private data are excluded from the response. Text is rendered as text, not HTML.

Reviews sort by **Submitted At**, newest first. Edits and retries preserve the existing row’s original date. Changes made by the course owner in the sheet are reflected on refresh without changing the original ordering. The response contains up to 20 entries and a continuation cursor; the list loads older batches as the student scrolls and also offers a **Load older reviews** button. The cursor contains no private identifiers, and its revision covers both the public written reviews and the rating summary. If the public data changes between batches, pagination restarts against the current public data to avoid duplicates, omissions, and withdrawn reviews remaining in the list.

The list refreshes after successful form submissions, on returning to the page, and every 60 seconds while the page is visible. Reviews are not cached in browser storage. A failed refresh clears the displayed entries and offers retry. Before any publishable reviews exist it shows **No student reviews yet.** No sample reviews are included in the course.

The script reads and filters the sheet server-side for each request, returning only a 20-review batch to the browser. The UI refreshes all batches already loaded so edits and withdrawals affect older displayed reviews too. This is polling, not an instant push to other students' open browsers.

Google documents JSON output and redirect behavior in [Content Service](https://developers.google.com/apps-script/guides/content) and execution/access settings in [Web Apps](https://developers.google.com/apps-script/guides/web).

## Verification

Run `node scripts/test_course_reviews.cjs` and `node scripts/test_review_loading_failures.cjs` from the project directory. Tests exercise the real form, public-list component, and Apps Script handler with in-memory fixtures and mocked Google services. Coverage includes:

- All-rating permission filtering, anonymous names, and an explicit public-field allowlist.
- Whole-sheet averages including private and rating-only submissions, edits without duplicate counting, and zero/single-rating states.
- Newest-first ordering across three batches; edits retaining their original position.
- Permission withdrawal and pagination resets when the public data changes.
- Scroll loading, retry, refresh after edits, periodic refresh, and the empty state.
- Draft restoration, rating-only submission, editing saved answers, unchanged review IDs and rating counts, and response-loss retries without duplicate rows.
- Notice placement, editable public names prefilled from registration, nickname persistence and publication, empty-name validation, and legacy drafts not publishing on page load.
- Compact and legacy sheet layouts, unchanged Submitted At, registration, and completion updates.

These tests do not write to the live spreadsheet or send email. Desktop and narrow browser previews confirm the list's placement and retry state. The currently deployed feed was checked read-only and returned five reviews. The reliability fixes still require deployment and live verification.

After deployment, open the web app URL with `?action=public_reviews` and confirm it returns JSON with `reviews`, `ratingSummary`, `nextCursor`, and `reset`. If it displays an authorization page, check the web app access settings; do not change spreadsheet sharing. If it returns an unknown-function page, check that the active deployment uses the new version containing `doGet`.

Deploy the new script version and publish the updated page so both reliability fixes are active. Older backends without `ratingSummary` must be updated before publishing this page.

On the course page, confirm the average and **ratings** count appear above the list. Submit a rating, then choose **Edit my review**: confirm the saved rating and text are restored. Change the rating and resubmit; confirm the same row updates, the total count stays unchanged, and the average reflects the change. Confirm the list appears below the form and thank-you message. An empty published list should show **No student reviews yet.** When an existing permitted review is edited, confirm its text/rating update while its position stays tied to Submitted At. Clearing the written-review text and resubmitting should remove it from the public list and other visible pages on their next refresh. Improvement feedback must never appear in the list or JSON.

The live Apps Script and website deployments have not been updated by this change.
