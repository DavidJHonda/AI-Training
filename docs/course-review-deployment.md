# Deploy the course review form and public list

The local form in `index.html` now asks for a required five-star usefulness rating, an optional written review, and optional private improvement feedback. The notice above Submit says: “Your review will appear publicly with your first name or nickname. Your suggestions for improvement stay private.” Submitting nonempty review text records `first_name` permission and the student’s saved first name or nickname. If no name is saved, the form asks for one. Rating-only submissions record `none`. Draft saving and submission retry remain available. The thank-you screen offers **Write another review**, which opens a blank form with a fresh review ID. There is no edit option. A scrollable **Student Reviews** list appears below both the form and the thank-you screen.

## Latest form update

The three-option permission section has been replaced by the publication notice. Keep **Quote Permission** and **Quote First Name** in the spreadsheet. They retain historical private/anonymous choices and keep the public feed correctly filtered. Existing records are unchanged when a student starts another review. Each new review is stored separately and contributes another rating to the average. Retrying the same submission reuses its ID so a lost response does not create duplicate rows. A draft retains its ID across reloads; choosing **Write another review** resets the stars and written fields and generates a fresh ID. The page no longer offers editing or withdrawal controls.

This form change uses the existing payload and does **not** require an Apps Script redeployment or a spreadsheet migration if the current public-list/average-rating script is already deployed. Publish the updated `index.html`. The full script deployment instructions below apply when setting up or updating an older backend.

## Update the existing Apps Script deployment first

1. Open the Google Apps Script project currently receiving course registrations, certificates, and reviews. If it is bound to the response spreadsheet, open that spreadsheet and choose **Extensions → Apps Script**.
2. Replace the contents of the existing handler file (usually `Code.gs`) with the complete contents of this project's `google-apps-script.gs`. Replace the handler rather than adding a second copy of `doPost` or `doGet`. Save the project.
3. Choose **Deploy → Manage deployments**. Select the active web app whose URL matches `SIGNUP_ENDPOINT` in `index.html`.
4. Click **Edit** (pencil). Under **Version**, choose **New version**, add a description such as “Student reviews with average rating and total ratings,” and click **Deploy**. The web app must execute as the course account that can read **Course Users** and allow **Anyone** to access the endpoint. Keep these settings if they are already configured. Keep the **Course Users spreadsheet itself private**; do not publish or share the spreadsheet publicly.
5. Keep the existing web app URL in `index.html`. Editing the existing deployment to use a new version preserves its URL; creating a separate deployment is unnecessary. Saving the source alone does not update the deployed version.
6. After deploying the script, open the **Reviews** tab and select the four original columns **G–J** together: **Confidence Before**, **Confidence After**, **Most Useful**, and **What Changed**. Right-click and choose **Delete columns G–J**. Delete the columns, rather than just clearing their contents. If G is already **Improvement** and J is **Quote First Name**, the sheet is already compact; skip this step.
7. Publish the updated `index.html` through the course's normal website deployment process if it has not already been published.

Google documents this workflow in [Create and manage deployments](https://developers.google.com/apps-script/concepts/deployments#edit_a_versioned_deployment).

## Existing spreadsheet data

The final Reviews layout has 10 columns, A–J:

| Column | Behavior |
| --- | --- |
| A: Submitted At | Set for a new row; untouched on submission retries. |
| B: Updated At | Refreshed on every accepted submission. |
| C: Review ID | Unique per review; matches retries to the same row. |
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

Above the scrolling list, the page displays the average star rating to one decimal place and a count labeled **ratings** (or **rating** for one). The average includes every valid submitted 1–5 rating, including private reviews and submissions without written text. Another review creates a new row and increases the rating count, including when the same student submits again. Retries keep the same ID and do not increase the count twice. With zero ratings, the page shows **No ratings yet** and **0 ratings**. Invalid rating cells are ignored.

The JSON response includes `ratingSummary: { average, total }`, computed from the full sheet rather than the current batch; `average` is `null` when `total` is zero. Only the aggregate is exposed for private/rating-only submissions. Each written-review entry contains only `rating`, `text`, `submittedAt`, and `name`. Only nonempty written reviews with `anonymous` or `first_name` permission are returned, including one-star ratings. Anonymous permission always hides the stored name. Improvement feedback, review IDs, student IDs, course versions, updated timestamps, and other private data are excluded from the response. Text is rendered as text, not HTML.

Reviews sort by **Submitted At**, newest first. Another review gets its own submission date. Retries preserve the existing row’s original date. Changes made by the course owner in the sheet are reflected on refresh without changing the original ordering. The response contains up to 20 entries and a continuation cursor; the list loads older batches as the student scrolls and also offers a **Load older reviews** button. The cursor contains no private identifiers, and its revision covers both the public written reviews and the rating summary. If the public data changes between batches, pagination restarts against the current public data to avoid duplicates, omissions, and withdrawn reviews remaining in the list.

The list refreshes after successful form submissions, on returning to the page, and every 60 seconds while the page is visible. Reviews are not cached in browser storage. A failed refresh clears the displayed entries and offers retry. Before any publishable reviews exist it shows **No student reviews yet.** No sample reviews are included in the course.

The script reads and filters the sheet server-side for each request, returning only a 20-review batch to the browser. The UI refreshes all batches already loaded so edits and withdrawals affect older displayed reviews too. This is polling, not an instant push to other students' open browsers.

Google documents JSON output and redirect behavior in [Content Service](https://developers.google.com/apps-script/guides/content) and execution/access settings in [Web Apps](https://developers.google.com/apps-script/guides/web).

## Verification

Run `node scripts/test_course_reviews.cjs` from the project directory. Tests exercise the real form, public-list component, and Apps Script handler with in-memory fixtures and mocked Google services. Coverage includes:

- All-rating permission filtering, anonymous names, and an explicit public-field allowlist.
- Whole-sheet averages including private and rating-only submissions, edits without duplicate counting, and zero/single-rating states.
- Newest-first ordering across three batches; edits retaining their original position.
- Permission withdrawal and pagination resets when the public data changes.
- Scroll loading, retry, refresh after edits, periodic refresh, and the empty state.
- Draft restoration, rating-only submission, blank-form reset, new review IDs across reloads, and response-loss retries without duplicate rows.
- Notice placement, first-name/nickname publication on explicit submission, legacy drafts not publishing on page load, and recovery when a saved name is missing.
- Compact and legacy sheet layouts, unchanged Submitted At, registration, and completion updates.

These tests do not write to the live spreadsheet or send email. Desktop and narrow browser previews confirm the list's placement and retry state. Live data loading remains unverified until the new Apps Script version is deployed.

After deployment, open the web app URL with `?action=public_reviews` and confirm it returns JSON with `reviews`, `ratingSummary`, `nextCursor`, and `reset`. If it displays an authorization page, check the web app access settings; do not change spreadsheet sharing. If it returns an unknown-function page, check that the active deployment uses the new version containing `doGet`.

Deploy the new script version before the updated page; the former public endpoint does not include `ratingSummary`.

On the course page, confirm the average and **ratings** count appear above the list. Submit a rating without written text, then choose **Write another review**: confirm the new form is blank. Submit another rating and confirm it creates a separate row, increases the count by one, and leaves the original row unchanged. Confirm the list appears below the form and thank-you message. An empty published list should show **No student reviews yet.** When an existing permitted review is edited, confirm its text/rating update while its position stays tied to Submitted At. Clearing the written-review text and resubmitting should remove it and from other visible pages on their next refresh. Improvement feedback must never appear in the list or JSON.

The live Apps Script and website deployments have not been updated by this change.
