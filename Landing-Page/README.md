# Course landing page plan

Last updated: October 7, 2026

Status: landing page and course entry flow implemented for release. The lesson source remains in `index.html`; production URLs are served through `vercel.json` rewrites.

## Current implementation

- `/` serves `landing.html`, styled by `landing.css`, with public reviews from `landing.js`.
- `/course` serves the existing course application. Existing storage keys and schemas are unchanged.
- `/course/why-learn-ai` renders the real Why Learn AI lesson in guest mode, including video, image enlargement, and the activity. Guest visits do not change the learner’s saved course position or completion record.
- Start buttons on the landing page and sample use `start-course.js` to open an accessible native dialog. It embeds the actual course entry form, so country validation and enrollment delivery remain in one implementation. `entry-flow.css` styles the dialog, compact standalone entry, and sample shell.
- Recognized learners bypass the dialog. New learners enter Welcome; returning learners keep their saved lesson and progress.
- `/index.html`, root `?print=` links, and root `?review=closing-boards` links still serve the course. Asset URLs resolve from the site root.
- The two current sample reviews remain by David’s request. He plans to replace them. Reviews show source submission dates in a scrollable region, with older-page loading when needed.
- The saved creator illustration is used. The introduction video remains a future addition.
- Existing search-engine noindex settings are preserved.

## Local evaluation

From the repository root, run `python3 scripts/serve-site.py --port 8878`, then open <http://127.0.0.1:8878/>. This server reads the same exact URL rewrite rules as Vercel. A generic static server does not implement the new URLs.

The earlier `preview.html`, `sample.html`, and `entry.html` files are design drafts; edit the root-level production files for the current implementation. Localhost browser storage is separate from the public site’s storage.

## Verification

- New-learner dialog: required fields, valid country selection, and entry into Welcome passed on an isolated local server that intercepted enrollment POSTs.
- Returning learner: seeded a saved Tokens lesson with two completed lessons, visited the sample, then entered `/course`; the saved progress record remained byte-for-byte unchanged and no enrollment was sent.
- Guest sample: renders without enrollment, opens the video, and runs the activity selection. Its Start button opens the same dialog.
- Dialog: mobile layout and Escape from inside the embedded form verified; focus returns to the Start link.
- Legacy print URL, route compatibility, script syntax, and whitespace checks passed.
- `design-check.sh` reports the same two pre-existing baseline mismatches as before these changes: two off-allowlist fonts and five em dashes versus an expected six. No new mismatch was introduced.

## Purpose

Give a new visitor a clear reason to begin Be Smarter Than the Tool. The page should work for students arriving from a newsletter, a shared link, or a YouTube video, as well as teachers and club leaders considering the course for a group.

Start with the existing course entry page as the design and content foundation. Preserve its clarity, student voice, branding, and straightforward invitation to start.

## What makes the course different

- Built by high school students, for high school students. Nate and Luke started an AI club at their high school.
- Goes beyond prompting: how AI works, when to trust it, how to think for yourself, and what AI means for school, work, and the future.
- Builds understanding and confidence through clear explanations, practical examples, and opportunities to try things.
- Free and self-paced, with no prior AI knowledge required.
- Students can watch a lesson or read it. Videos are an alternative to reading the lesson, not an additional requirement.
- TRY ITs and LABs let students put ideas into practice. Optional group exercises support clubs and classes.
- No email address or account required. The current entry flow asks for a first name or nickname and country.

Describe these strengths positively. Do not claim this is the best or only course of its kind, or broadly criticize other courses.

## Working page outline

This is the proposed structure for the eventual build, not a finished design.

1. **Course introduction.** Keep the course name, student-built positioning, a clear description of its purpose, and a prominent “Start the course” button.
2. **Nate and Luke's short introduction video.** Let each introduce himself. Explain the questions that inspired the course and what students can expect. Working script: [intro-video-script.md](intro-video-script.md).
3. **What students will gain.** Use the current entry page's five benefits as the starting point: Get Results, Get Smart, Get Wise, Get Prepared, and Get Ahead. Refine wording to emphasize understanding, judgment, confidence, and preparing for the future.
4. **How to use the course.** Watch or read, then try things. Learn at your own pace. Mention group exercises for clubs and classes without making individual learners feel they need a group. A computer works best for hands-on labs.
5. **Certificate.** Retain the current sample certificate and explain that passing the final exam earns a certificate of completion.
6. **Start or return.** Offer a clear route into the course and make returning to saved work easy. Keep any enrollment information minimal.

A future “For Teachers” area or workbook remains a separate, later idea. It is not a requirement for this landing page.

## Entry flow and saved progress

Agreed direction: a public landing page separate from the course application. Clicking “Start the course” takes the learner to the course at a different URL on the same site.

One proposed implementation is a public `index.html` landing page with the existing course moved to `course.html`. Final filenames and routing are still to be selected. `Landing-Page` is the planning directory; it does not establish the eventual public URL.

The current application and its entry screen both live in `index.html`. Its learner information and progress use browser local storage. During the build:

- Keep the course on the same origin, including protocol and hostname, and preserve existing storage keys and stored-data formats.
- Returning learners should retain their saved progress in the same browser/profile and device, assuming their browser data remains available.
- Starting from the landing page must not reset enrollment, lesson progress, exercise state, or final-exam records.
- Provide a clear return/continue route for existing learners.
- Decide where the current first-name-or-nickname and country form belongs. Avoid making existing learners enroll again.
- Check existing bookmarks, lesson links, print links, group-exercise return links, asset paths, and download links before moving the application.
- Verify progress with a populated browser profile as well as a fresh visitor. Local `file://` tests are not enough to establish same-origin behavior on the published site.

This plan preserves the current local saved-progress approach. It does not add accounts, email collection, or cross-device synchronization.

## Launch context

We discussed direct outreach to relevant newsletters, sharing lesson videos on YouTube, and letting early use build awareness. The landing page should give those visitors a useful introduction and a simple path to start. Distribution partnerships can be explored separately; they are not a prerequisite for building this page.

## Decisions still open

- Final page copy and visual layout, based on the current entry page.
- Final landing-page and course URLs, including compatibility with existing links.
- Exact placement of the enrollment form and returning-learner controls.
- Final introduction script, recorded video, captions, and hosting.
- Whether to add student feedback or testimonials later. Do not add old course reviews automatically.

## When we are ready to build

Re-read this plan and inspect the current entry page before implementation. Finalize the copy and entry flow, build the separate page, and verify navigation and progress preservation before publishing. No page build or deployment has been requested as part of creating this planning directory.

## Saved illustration

The previous Welcome illustration of Nate and Luke is preserved as [nate-and-luke-building-the-course.jpg](nate-and-luke-building-the-course.jpg) for the public rollout. Welcome now uses a people-free workspace. See [illustration-notes.md](illustration-notes.md) for the preservation record and replacement prompt.
