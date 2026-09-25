# Course landing page plan

Last updated: September 25, 2026

Status: planning only. This directory holds the page plan, copy, scripts, and future design references until we build the page. Creating these documents does not change the current course entry page, URLs, or saved progress.

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
