# Contact form

Both landing and course footers open the shared dialog in `contact.js` and `contact.css`.
Name is optional; email and message are required. Messages are emailed to the fixed
course inbox, `besmarterthanthetool@gmail.com`, with the sender's email as Reply-To.
No spreadsheet tab is created. The direct email link remains available.

Drafts stay in memory while this page remains open, including closing and reopening
the dialog. They are not saved to browser storage. The browser saves only a random
client ID. Success requires the exact `contact-ok` acknowledgement. No message is
posted until a read-only `contact_status` request returns `contact-ready`, so an old
backend cannot mistake a contact request for enrollment.

## Activate

1. Replace the existing Apps Script handler (usually Code.gs) with the complete
   `google-apps-script.gs` in this repository and save.
2. Choose Deploy > Manage deployments > Edit > New version > Deploy. Preserve the
   existing URL and access/execution settings. Use the course's authorized account.
3. Open the existing web app URL with `?action=contact_status`. Expect `contact-ready`.
4. Test the form and confirm receipt in the course inbox. Check Reply addresses the
   visitor. Live email delivery has not been tested by the local checks.
5. Publish the website files, including contact.js and contact.css.

## Limits and checks

Server validation bounds name (100 characters), email (254), and message (5,000),
rejects email/name header injection and a honeypot. Contact sends are limited to
20 per UTC day and 3 per browser ID per hour, leaving at least 10 recipients of
shared MailApp quota. Browser IDs are a basic deterrent, not authentication.
Receipts store only request IDs, payload hashes, and timestamps, and are pruned
following successful sends after 24 hours. Retries of an unchanged payload reuse
its ID. Failure between MailApp acceptance and receipt storage can still duplicate
an email. The sender's name, address, and message remain in the receiving mailbox.

Run `node scripts/test-contact.cjs`, `node scripts/test-lesson-feedback.cjs`, and
`node scripts/test_course_reviews.cjs` for mocked backend/regression checks.
Browser checks used a separate local origin with mocked sends: landing success,
course send failure, preserved drafts, Escape/focus restoration, and prevention
of POST to an unsupported deployment. No real test emails were sent.
