# Course Completions Country migration — local changes, not deployed

The completion record keeps the fields needed to prove a pass and reproduce the certificate name. Its compact layout is:

| A | B | C | D | E | F | G | H |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Completed At | Student ID | First Name | Last Name | Country | Final Score | Completion ID | Course Version |

**First Name** and **Last Name** are the certificate name the student confirms after passing. Keeping both is useful when a certificate is corrected later. **Student ID** connects the completion to the same browser profile used for registration and reviews. **Completion ID** prevents duplicate completion rows. **Final Score**, **Completed At**, and **Course Version** preserve the evidence associated with the pass.

Historical City and State values are preserved in the backup but are not converted into Country. Historical Country cells therefore remain blank unless that student's browser later sends a valid saved country. A returning student who predates Country can still receive and edit a certificate; a missing historical country does not block completion.

## Safe rollout order

The page and Apps Script changes are local. Do not remove City or State manually.

1. In the Apps Script project attached to **Course Users**, replace the current handler with the complete contents of `google-apps-script.gs` and save.
2. Choose **Deploy → Manage deployments**, edit the active web app, select **New version**, and deploy it with the existing execute-as and access settings. Updating the existing deployment keeps its web app URL.
3. Return to the editor. Select **migrateCompletionSheet** in the function dropdown beside **Run**, then click **Run**. Do not select `doGet` or `doPost` for this step.
4. The migration first creates **Course Completions backup [timestamp]**. It then adds Country if necessary and removes City and State from the active **Course Completions** tab. If the backup cannot be created or the headers are unexpected, it stops before deleting columns.
5. Confirm that the active tab has the eight headers shown above. Keep the backup until the new flow has been verified.
6. Publish the updated `index.html` after the Apps Script deployment. The page will send Country with future completion and certificate-name updates.
7. In a fresh browser profile, register with a Country, pass the final with at least 80%, enter a certificate first and last name, and confirm one completion row contains the Country. Edit the certificate name and confirm the same row changes without changing its Completed At, Final Score, Completion ID, or Course Version.

The deployed backend can safely run before the page is published. During that interval it accepts the previous completion payload and leaves Country blank. It also supports the old City/State sheet layout until the migration runs.

## Verification performed locally

```sh
node scripts/test_completion_country.cjs
node scripts/test_country_registration.cjs
node scripts/test_course_reviews.cjs
node scripts/test_review_loading_failures.cjs
```

The completion tests cover new and existing layouts, one-row deduplication, certificate-name edits, Country backfills, blank legacy retries, passing-score validation, full backup preservation, repeat migration, backup failure, malformed headers, and a browser retry race between old and Country-aware completion payloads.
