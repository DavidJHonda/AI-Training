# Lab 09 facilitator note: Build Your Course Notebook

For whoever is running the session (Nate / Luke). The lab lives at the end of the
**Learn with AI** lesson in the app; students follow its nine steps on their own
laptops. This note covers the session around it. The live lesson in `index.html` is
authoritative if these notes ever disagree with the student-facing steps.

## Before the session

- Verify that a school Google account can open Gemini Notebook at
  `notebook.google.com`. If access is blocked by the school's Workspace settings,
  choose an approved fallback before students arrive; do not improvise account policy
  during the session.
- Run the current path once: open the packet in a new tab from step 1, download
  `Start Smarter.pdf` from step 2, create a fresh notebook, upload the PDF, send the
  exact quiz prompt from step 6, answer the quiz, and open a citation.
- Make sure `packets/start-smarter.pdf` reflects the seven current Start Smarter
  learning lessons. Welcome is intentionally excluded so the quiz tests AI concepts,
  not course orientation. It is a static export, so regenerate it with
  `bash scripts/make-packet.sh` after relevant lesson changes.

## The 30-minute session

| Time | What happens |
|------|--------------|
| 0–3 | Everyone opens Learn with AI, scrolls to LAB 09, and signs into Gemini Notebook. |
| 3–8 | **Demo on the shared screen:** run steps 1–6 once (open, download, sign in, notebook, source, quiz) while emphasizing that the answers should come from the uploaded course packet. |
| 8–26 | **Everyone builds:** students work through the nine live steps on their own machines. Circulate. |
| 26–30 | If time remains, ask two volunteers to share one quiz question and how they did. Keep it informal. |

## Common stalls

- **The packet seems missing.** Check the browser's Downloads list and confirm that
  downloads are allowed. Step 1 opens the prepared PDF in a new tab and step 2
  downloads it; neither uses a print dialog.
- **The source is still processing.** Wait for the uploaded source to become available
  before generating the quiz, especially on school Wi-Fi.
- **The quiz shows answers immediately.** Re-send the exact step 6 prompt, including
  “Don’t show the answers yet. Wait for mine, then grade me.”
- **A student finishes early.** Send them to step 9: start a second notebook for the
  class with their next test and add the real materials their teacher provided.

## What done looks like

A student leaves with a **Be Smarter Than the Tool** notebook containing the Start
Smarter packet, a completed and graded 10-question quiz, and at least one citation
opened back to the source. Step 9 is the transfer challenge they can begin in the
session and continue afterward.
