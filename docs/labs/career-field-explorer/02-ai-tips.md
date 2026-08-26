# Lab 2: Make the first draft editable

**Lesson:** AI Tips  
**Time:** 12–15 minutes  
**Starter:** `01-your-choices-recovery.html` or the student's working file  
**Recovery:** `02-ai-tips-recovery.html`

## Build

Add one edit control to each career card. It should open a clear form, load that
field's current content, save the changes, and close without changing anything when
the student cancels.

## Prompt to use with AI

> Before changing the file, ask me up to three questions about how the editor should
> work, one question at a time. Then add an Edit control to every career card. Use one
> accessible dialog for all three cards. It must load the selected card's current
> content, save edits back to that card, and support Cancel and Close without saving.
> Keep the existing design and text sizes. Do not add a framework or external code.

If the first result misses, students should name the miss instead of typing “try
again”: “Keep the card layout. The edit form is too dense. Group the fields, preserve
the existing values, and make Cancel leave the card unchanged.”

## Test before finishing

- Editing field 2 changes field 2, not field 1.
- Cancel leaves the content unchanged.
- Save updates the card immediately.
- The editor works by keyboard as well as by mouse.

## What this lab teaches

Good users give context, make AI ask questions, and aim the retry at the actual miss.
