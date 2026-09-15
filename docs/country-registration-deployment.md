# Country registration and enrollment cleanup

The splash now requires a first name or nickname and a country selected from the searchable list. It starts with “Select your country” and no selection. United States appears once, first; the remaining entries are alphabetized. Typing alone does not count as a selection. The list includes the 249 ISO 3166-1 countries and territories, using English display names from Unicode/ICU. The code list comes from the public-domain IANA `iso3166.tab`; [ISO explains the country-code standard](https://www.iso.org/iso-3166-country-codes.html).

`country-select.js` contains the list and accessible combobox. The matching allowlist is included in `google-apps-script.gs`, so that file remains a complete replacement for the deployed script. A regression test verifies that the two lists match.

## Google Sheet

Keep **Course Users** private and keep its enrollment tab first. The target registration layout is:

| A | B | C | D |
| --- | --- | --- | --- |
| Timestamp | First Name | Student ID | Country |

The long values under the old **Certificate?** heading are student IDs. They connect a browser's registration, reviews, and completions; they do not indicate whether a certificate was earned. Actual completion records live in **Course Completions**.

The revised script finds enrollment columns by header, supports the old **Certificate?** label, and works before and after cleanup. Normal registrations rename that heading to **Student ID** and add **Country** if it is missing. New registration payloads and signup emails no longer collect Last Name, Email, City, or State.

The editor function **migrateEnrollmentSheet** makes a complete backup tab named **Enrollment backup [timestamp]**, then removes **Last Name**, **Email**, **City**, and **State** from the active enrollment tab. It preserves timestamps, first names, IDs, and any existing countries. Unrelated custom columns remain. It refuses to remove anything if backup creation fails, and it is safe to run again.

**Deploy this script version before running cleanup.** Older deployed scripts write to fixed column positions and would misfile registrations after columns are deleted. Do not delete the columns manually first.

**Reviews** remain unchanged. **Course Completions** keeps the first and last name used on the certificate and replaces its City/State snapshot with Country in a separate, backup-first migration. See `docs/completion-country-deployment.md` for that rollout. Removing the enrollment Last Name field does not remove certificate names or alter certificate tracking.

Missing historical countries are not inferred from City/State or IDs and will not fill retroactively. If the older deployed script discarded a submitted country, adding a header cannot recover that value from the sheet. The page permits entry even if logging fails, so entering the course alone does not confirm a successful spreadsheet write.

## When ready to deploy

Deploy the backend before publishing the new page so country data can be stored from the first signup.

1. Open the existing Apps Script project attached to Course Users.
2. Replace the current handler code with the complete contents of `google-apps-script.gs` and save. Do not append a second copy of the handler functions. The country list is already included in this file.
3. Choose **Deploy → Manage deployments**, select the active web app, then click the pencil/Edit icon.
4. Select **New version**, optionally describe it as “Country registration and enrollment cleanup,” and click **Deploy**. Retain the current execute-as and access settings. Editing the existing deployment keeps the web app URL unchanged. See [Google’s deployment instructions](https://developers.google.com/apps-script/concepts/deployments#edit_a_versioned_deployment).
5. After the deployment succeeds, return to the editor. In the function dropdown beside **Run**, select **migrateEnrollmentSheet**, then click **Run**. Approve Google authorization if prompted. Do not run `doGet` or `doPost` from that dropdown for this step.
6. Check the first sheet: the screenshot's layout becomes **Timestamp | First Name | Student ID | Country**. A backup tab contains the full original data, including the removed columns. No Country column needs to be added by hand.
7. Publish the website changes together when ready, including `index.html`, `country-select.js`, and `course-assets/the-final/course-certificate-sample.png` if not already published. The backend also accepts the earlier country form, so it can be updated before the website.
8. Using a fresh browser profile, select a country and enter a name, then verify that the new row has its Student ID and Country in the correct columns. Confirm returning students still enter directly.

The script accepts older queued enrollment payloads without a country, ignoring their obsolete registration fields. New payloads carry `registrationVersion: 2`, which requires both name and a valid country on the server. This keeps old clients compatible while validating the new form.

## Local verification

All tests use local fixtures or intercept requests; they do not write to Google Sheets or send email.

```sh
node scripts/test_country_registration.cjs
node scripts/test_course_reviews.cjs
node scripts/test_review_loading_failures.cjs
```

Browser checks covered 1440px, 390px, and 320px layouts; search, ordering, exact-text-without-selection rejection, empty-name rejection, arrow keys, Enter, Escape, touch/click selection, signup payloads, local profile persistence, and returning-student access. Backend checks cover both enrollment layouts, the screenshot's Certificate? heading, automatic Country creation, complete backups, preserved historical IDs/timestamps/countries, repeated cleanup, custom columns, failed backups, invalid layouts, legacy enrollments, review edits/loading, and certificate tracking.

The user deployed the Country-aware Apps Script as Version 9 on September 14, 2026. The backup migration and live-sheet verification remain manual steps in the Apps Script editor and Google Sheet.
