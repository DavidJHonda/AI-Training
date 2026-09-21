# Lesson feedback

Each lesson footer has a Report a problem control beside Copyright & Permissions.
The shared modal includes the current lesson and a required message (up to 2,500
characters). It sends directly to besmarterthanthetool@gmail.com through the
existing Apps Script web app. No feedback sheet, student email, or email app is
needed. Course Reviews and its existing data flow are unchanged.

## Activate

1. Update the existing Apps Script project with google-apps-script.gs.
2. Update its existing web-app deployment to a new version, preserving the current
   URL and execution/access settings. Use the account already authorized to send
   enrollment emails; approve MailApp authorization if Google requests it.
3. Check the web-app URL with `?action=feedback_status`; it should return
   `feedback-ready`.
4. Publish index.html after the script update.
5. Submit one clearly labeled test report and confirm receipt in the mailbox.
   Then check that a normal signup and the existing review flow still work.

This work has been tested locally with mocked Google services and mocked browser
responses. Live email delivery requires the deployment and mailbox check above.
The frontend checks capability before posting, avoiding the older handler's
unknown-event enrollment fallback. A successful UI response means MailApp accepted
the send, not independent confirmation of inbox delivery.

## Limits and retries

The email recipient is fixed server-side. Validation and a hidden honeypot reject
invalid submissions. A script-property counter limits feedback to 50 emails per
UTC day and leaves at least ten recipients of the shared MailApp quota available.
A best-effort browser-ID cache limit allows five submissions per hour. This is
basic abuse protection, not authenticated user identification or a CAPTCHA.

A script lock serializes checks and sends. Script properties retain request IDs,
payload hashes, and timestamps for retry deduplication; they do not retain message
text. Receipts older than 24 hours are pruned after successful submissions. The
browser keeps the same request ID when retrying an unchanged message. As with any
email side effect, a failure after MailApp accepts a message but before recording
its receipt can still result in a duplicate. There are no automatic send retries.

A failed/unsupported request preserves the typed message. Closing and reopening
the modal on the same lesson retains an unsent draft. Navigating to another lesson
starts a new draft for that lesson. Success is displayed only for `feedback-ok`.

## Local verification

Run `node scripts/test-lesson-feedback.cjs` from the project. It mocks Apps Script
services and verifies routing, fixed recipient, validation, duplicate suppression,
failed-send retry, quota/rate limits, and existing enrollment/review/completion
routes. No real email is sent.

Browser checks covered Resources and Evaluate the Results lesson identification,
keyboard focus and Escape, reopening drafts, unsupported deployment protection,
failed submission and retry, success, and a 390px mobile viewport. All requests
were intercepted; live delivery was not exercised.
