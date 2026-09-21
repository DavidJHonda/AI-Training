# Shared video workflow

Current instructions, consolidated 2026-09-15. Start here for each video task.
Read the task-specific reference below; do not load every technical recipe for a
routine edit. User instructions and already-approved plans take precedence.

## Which instructions to read

| Task | Read after this page |
|---|---|
| Prepare Markdown, prompt, or upload bundle | [Prompts guide](../../Prompts/README.md) |
| Stage a lesson's uploads in one folder | `sync_gemini_notebook.py` builds `gemini-notebook/<slug>/` from `Prompts/upload-sets.json` |
| Evaluate narration or compare generations | [Narration Review](NARRATION-REVIEW.md) |
| Build or repair a video | [Edit Spec](EDIT-SPEC.md) |
| Replace course-board visuals | [Board Retrofit](RETROFIT-PLAYBOOK.md), plus Edit Spec |
| Diagnose rendering, timing, or audio seams | Relevant section of [Technical Recipes](TECHNICAL-RECIPES.md) |
| Publish an approved candidate | Ship checklist and shipping rules below |

Edit Spec owns scope and visual/audio treatment. Narration Review owns teaching
verdicts. The Prompts guide owns generation materials. Technical recipes explain
implementation; old example paths, timings, and treatments do not override these
current rules. A lesson-specific kit supplies that lesson's details, not a second
set of global production rules.

## Current files and status

- `index.html` is the current lesson content authority. `LESSON_VIDEOS` identifies
  the standard videos offered by the course; verify the entry rather than inferring
  status from filenames. Lesson IDs, source slugs, and asset folder names can differ.
- Current boards and illustrations are canonical JPGs in `course-assets/<lesson>/`.
  Use the exact assets referenced by the lesson, preserving dimensions and layout.
- Current upload text lives in `lessons/`; prompts and raw generations in `Prompts/`.
  Raw rolls commonly use `<slug>-reroll.mp4` and `<slug>-reroll-2.mp4`.
- Review candidates stay in `Prompts/<lesson>-vN.mp4`. Never overwrite a candidate
  the owner may have open; give each rebuild a new version.
- Finished videos live beside boards as `course-assets/<lesson>/<lesson>.mp4`.
- Retained `video-audit/<slug>-repair-<date>/REVIEW.md` records support active work.
  An old review is not evidence that a newer file passed.
- David maintains the [Video Tracker](https://docs.google.com/spreadsheets/d/16RXfX9awLA8Idu83OBN97bCrMiTzyEOFO4MBpvPWXO8/edit).
  It governs workflow status; do not draft or post tracker rows. If unavailable,
  state that limitation and use verified local artifacts without inventing status.
- `ai-brain-break.mp4` is an activity inside Layers, not a standard lesson overview; it and its seven cards live in `course-assets/ai-brain-break/`.
  Its deliberately false claims support a debunking exercise; it is exempt from
  the standard close and standard source bundle.

## Workflow

1. **Confirm the task and sources.** Read the current lesson, identify the exact
   candidate/source files, and check the latest relevant review. Distinguish a
   full production pass from a narrow repair; see Edit Spec section 1.
2. **Prepare only what is needed.** For generation, use current Markdown, selected
   JPGs, and a self-contained prompt. For an existing-video repair, do not regenerate
   materials or reroll solely because a visual needs fixing.
3. **Evaluate the teaching.** Use KEEP / REPAIR / REROLL from Narration Review.
   Good narration with repairable visuals is useful. Compare multiple rolls by
   teaching point, preserving the best explanations, examples, and conclusions.
4. **Plan the edit.** Record source/output spans, current board paths, source hashes,
   and intended replacements. Present proposed narration cuts/grafts with exact
   words and timestamps. Include a board-by-board highlighting and camera table
   with the evaluation: whole-card versus section highlights, full-view versus
   complete-card zoom, and any unusual treatment (Edit Spec section 1b). Propose
   pauses only where students need breathing room, including existing and target
   total gaps. Present these together as one plan for approval before the first
   build. Reuse approval already given; return only for material plan changes.
5. **Build the candidate.** Preserve useful Notebook drawings. Use exact current
   lesson boards, the prescribed highlights, and the standard close. Rebuild from
   pristine sources in one assembly where available; do not stack lossy repairs.
   If only a finished video survives, disclose that source limitation.
6. **Verify and report.** Check the actual encoded candidate, not just the plan.
   Report completed work, remaining defects, and unperformed checks. A narrow
   repair can be ready for review without being ready to ship.
7. **Ship only when authorized.** Approval to build is not approval to publish.
   Follow the checklist below and honor any instruction to leave deployment to
   another task.

## Ship checklist (editor's verification of the finished file)

Before shipping a standard lesson video:

- Narration on the exact candidate earns KEEP under Narration Review. Watch/listen
  to the finished video end to end; do not claim completion from a transcript alone.
- Boards match current lesson assets and wording. Compact/dense framing, full-view
  openings, spoken highlight onsets, and constant 5px outline rings meet Edit Spec.
  No Notebook recreation/highlighting remains on course boards.
- Kept drawings support the narration. No unlicensed/watermarked stock photographs,
  legible profanity, or inappropriate source imagery remains. Apply Edit Spec's
  stock-photo and engine-corner-mark treatment, and inspect its results.
- The standard close is the literal final frame and has the prescribed motion.
- Declare every splice on the output timeline. Run `transition_guard.py` and
  inspect boundary strips: no stale frames, clipped words, clicks, or noise-floor
  cliffs. Automated detection alone does not certify a clean transition.
- Measure edited pauses against the approved selective-pause plan and listen for
  natural pacing. No automatic one-second minimum applies.
- Listen to every audio graft for wording, pronunciation, cadence, levels, and
  voice continuity. List any joins still requiring David's listening review.
- Decode to verify frame counts/timing. Visual-only repairs preserve source FPS,
  duration, decoded frame count, and the copied audio stream. Audio-changing builds
  must match their planned output duration and frame count instead.
- Confirm the website's intended file path and that no unresolved issue or missing
  verification is being presented as a pass. Full shipping checks do not authorize
  unrelated changes outside an approved narrow repair.

## Shipping filename convention

After approval and verification, replace the canonical unsuffixed MP4 with the
approved candidate. Verify that file and the lesson reference before removing the
superseded candidate. The website must not depend on a review-stage `-vN` path.
Do not delete raw generations when shipping; they may be needed for a later repair.

## Asset retention and safe preparation

Keep current boards in `course-assets/`, Markdown in `lessons/`, and active sources
and candidates in `Prompts/`. Do not recreate `archive/`, `illustrations/`, or
`video-audit-current/`, or retain obsolete boards solely for old video plans.
Remove superseded material only within David's authorized cleanup scope, after
checking replacements and active dependencies. Keep raw rolls until he authorizes
their removal; many are gitignored and cannot be recovered from Git.

Temporary render frames, lossless intermediates, and explicitly selected donor
snapshots may support an active edit. Record source hashes and protect those files
while needed. Do not bind donor frame numbers to a live MP4 that can be overwritten
on the next ship, or build a permanent library of rejected rolls.

Do not run `scripts/make-lesson-texts.sh` over hand-edited upload Markdown merely to
read a lesson; its ID filter can match multiple lessons. Read the page directly,
or use an isolated temporary export. Never restore tracked files as a cleanup
shortcut that could discard the user's uncommitted changes.

## Handoff

Record candidate path, source/donor paths and hashes, manifest, build and QA commands,
approved scope, tests/listening completed, remaining issues, and shipping approval
status in the active review. Keep the user-facing update concise and link to it.
