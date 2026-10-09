# Shared video workflow

Current instructions, updated 2026-10-08. Start here for each video task.
Read the task-specific reference below; do not load every technical recipe for a
routine edit. User instructions and already-approved plans take precedence.

## Which instructions to read

| Task | Read after this page |
|---|---|
| Prepare Markdown, prompt, or upload bundle | [Preparation guide](PREPARATION.md) |
| Stage a lesson's uploads in one folder | `sync_gemini_notebook.py` builds `gemini-notebook/<slug>/` from `gemini-notebook/upload-sets.json` |
| Evaluate narration or compare generations | [Narration Review](NARRATION-REVIEW.md) |
| Build or repair a video | [Edit Spec](EDIT-SPEC.md) |
| Improve learning with supporting scenes and timed illustrations | [Learning Illustration Pass](LEARNING-ILLUSTRATION-PASS.md), plus Edit Spec sections 8–8d |
| Replace course-board visuals | [Board Retrofit](RETROFIT-PLAYBOOK.md), plus Edit Spec |
| Diagnose rendering, timing, or audio seams | Relevant section of [Technical Recipes](TECHNICAL-RECIPES.md) |
| Ship an approved candidate locally | Ship checklist and local shipping rules below |
| Publish a batch to Vercel | Batch deployment rules below |

Edit Spec owns scope and visual/audio treatment. Narration Review owns teaching
verdicts. The Preparation guide owns generation materials. Technical recipes explain
implementation; old example paths, timings, and treatments do not override these
current rules. A lesson-specific kit supplies that lesson's details, not a second
set of global production rules.

## Current files and status

- `index.html` is the current lesson content authority. `LESSON_VIDEOS` identifies
  the standard videos offered by the course; verify the entry rather than inferring
  status from filenames. Lesson IDs, source slugs, and asset folder names can differ.
- Current boards and illustrations are canonical JPGs in `course-assets/<lesson>/`.
  Use the exact assets referenced by the lesson, preserving dimensions and layout.
- Current upload text lives in `lessons/`. Editable generation prompts, upload variants,
  and lesson prep notes live in `gemini-notebook/<lesson>/`; its registry is
  `gemini-notebook/upload-sets.json`. Only upload copies, generated lesson READMEs,
  and sync metadata are derived. Shared prep rules and section kits live here in
  `scripts/video/`. Raw generations stay in `Prompts/` and commonly use `<slug>-reroll.mp4` and `<slug>-reroll-2.mp4`.
- Review candidates stay in `Prompts/<lesson>-vN.mp4`. Never overwrite a candidate
  the owner may have open; give each rebuild a new version.
- Finished videos live beside boards as `course-assets/<lesson>/<lesson>.mp4`.
- Retained `video-audit/<slug>-repair-<date>/REVIEW.md` records support active work.
  An old review is not evidence that a newer file passed.
- `board_spans.py` measures when each course board is on screen in a finished
  video (ORB feature match against the lesson's JPGs every 0.5 s, sequential decode,
  survives zooms and pans): `.video-venv/bin/python scripts/video/board_spans.py
  course-assets/<slug>/<slug>.mp4 course-assets/<slug> <review-dir>` writes
  `board-spans.txt`. Added 2026-09-25 for the Start Smarter live reviews; a span
  is judged under Edit Spec 8b (walking the board is free, narration past it is not).
- `ring_stroke.py` measures the on-screen stroke width of every highlight ring in a
  finished video (colour-threshold the eight Edit Spec section 5 tokens, keep the
  hollow rectangles, median run length across the four sides every 0.5 s):
  `.video-venv/bin/python scripts/video/ring_stroke.py course-assets/<slug>/<slug>.mp4
  <review-dir>` writes `ring-stroke.txt` (per-sample rows, histogram, per-run
  summary) and 4x crops of the thinnest and thickest ring found. Widths are solid
  pixels at the default threshold; the anti-aliased edge adds about half a pixel.
  Calibrated 2026-09-26 on What Is AI? (20260926ship2, the fixed-4 px reference
  reads 4.0). Added for the Work With AI live review; the target is Edit Spec
  section 5's fixed 4 px at 720p.
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
   JPGs, and a self-contained prompt. Complete the
   [lesson-arc pass](PREPARATION.md#prepare-the-lesson-arc): progression,
   essential bridges, diagram relationships, and distinct overview/detail roles.
   For an existing-video repair, do not regenerate
   materials or reroll solely because a visual needs fixing.
3. **Evaluate the teaching.** Use KEEP / REPAIR / REROLL from Narration Review.
   Good narration with repairable visuals is useful. Compare multiple rolls by
   teaching point, preserving the best explanations, examples, conclusions, and
   the connections that make them a coherent lesson.
   For isolated missing or misspoken narration, evaluate a donor from an existing
   video roll before requesting a full reroll. Verify its wording and audition
   the joins before treating it as a verified repair source.
4. **Plan the edit.** Record source/output spans, current board paths, source hashes,
   and intended replacements. Present proposed narration cuts/grafts with exact
   words and timestamps. Include a board-by-board highlighting and camera table
   with the evaluation: whole-card versus section highlights, full-view versus
   complete-card zoom, and any unusual treatment (Edit Spec section 1b). Propose
   pauses only where students need breathing room, including existing and target
   total gaps. Present these together as one plan for approval before the first
   build. Reuse approval already given; return only for material plan changes.
5. **Build the candidate.** Preserve engaging Notebook graphics and animations
   that support the lesson; consistent added examples are allowed. Judge their
   teaching value in motion with narration, and prefer targeted repairs over
   replacing effective scenes with stills (Edit Spec section 8). Use exact current
   lesson boards, the prescribed highlights, and the standard close. Rebuild from
   pristine sources in one assembly where available; do not stack lossy repairs.
   If only a finished video survives, disclose that source limitation.
6. **Verify and report.** Check the actual encoded candidate, not just the plan.
   Report completed work, remaining defects, and unperformed checks. A narrow
   repair can be ready for review without being ready to ship.
7. **Ship locally when authorized.** Approval to build is not approval to ship.
   “Ship it” means install, verify, and commit the approved video locally under
   the rules below. GitHub pushes and Vercel deployments happen only on a separate
   explicit request to publish a batch.

## Local shipping and batch deployment (owner rule, 2026-09-29)

Individual video shipping stops at a local Git commit:

1. Complete the ship checklist, then install the approved candidate at the
   canonical `course-assets/<lesson>/<lesson>.mp4` path.
2. Update that video's `LESSON_VIDEOS` reference, cache key, and displayed runtime
   in `index.html` as needed. Verify the installed file and local lesson reference.
3. Commit only the approved release changes locally. Preserve unrelated working
   changes; do not stage an entire shared file when only one entry belongs to the
   release. Keep audit/build records locally without automatically adding them to
   the release commit.
4. Record the local commit, installed file hash, and pending deployment status in
   the review. Report **shipped locally; queued for batch deployment**. Perform
   the render-scratch cleanup below after the local commit.

Do not run `git push`, trigger Vercel, wait for a deployment, or describe the video
as live during an individual ship. Local installation does not establish what is
currently served by the public site.

When David separately requests a batch deployment, inspect all outgoing commits
and confirm the batch includes only intended release changes before pushing to
the configured GitHub/Vercel deployment workflow. A push publishes all outgoing
commits on that branch, not just the latest video's commit. Use the authorization
already given for that batch; do not ask again for the same scope. After deployment,
verify the public lesson references and served video files for every included
video, then record the deployment and report which videos are live. If deployment
or verification fails, retain the pending status and report the actual result.

## Ship checklist (editor's verification of the finished file)

Before shipping a standard lesson video:

- Narration on the exact candidate earns KEEP under Narration Review. Watch/listen
  to the finished video end to end; do not claim completion from a transcript alone.
- Boards match current lesson assets and wording. Compact/dense framing, full-view
  openings, spoken highlight onsets, and constant 5px outline rings meet Edit Spec.
  No Notebook recreation/highlighting remains on course boards.
- Kept graphics and animations support the narration without contradicting the
  lesson. Check motion, reveals, labels, and final states; added examples are
  acceptable when consistent and not misleading. The review identifies useful
  scenes retained and the specific reasons for replacements (Edit Spec section 8).
  No unlicensed/watermarked stock photographs,
  legible profanity, or inappropriate source imagery remains. Apply Edit Spec's
  stock-photo and engine-corner-mark treatment, and inspect its results.
- The standard close is the literal final frame and has the prescribed motion.
- Declare every splice on the output timeline. Run `transition_guard.py` and
  inspect boundary strips: no stale frames, clipped words, clicks, or noise-floor
  cliffs. Automated detection alone does not certify a clean transition.
- Measure edited pauses against the approved selective-pause plan and listen for
  natural pacing. No automatic one-second minimum applies.
- **Cut a pause at the silence, never at a `scenes.py` cut (2026-09-22, One More
  Thing v6).** The scene cut says where the picture may change; it does not say
  where the sentence begins, and Notebook's cuts routinely land a few frames
  after the next line has started. Two pauses in that build were split on the
  picture cut and each stranded the attack of the following word in front of the
  silence - eight frames of "Not" before the closing message, which David heard
  at 4:16, and two frames of "So" at 2:06.8, which is quieter but the same bug.
  Measure the RMS either side of every planned split and move it into the gap;
  `transition_guard.py` is a picture check and will not catch this.
- Listen to every audio graft for wording, pronunciation, cadence, levels, and
  voice continuity. List any joins still requiring David's listening review.
- Decode to verify frame counts/timing. Visual-only repairs preserve source FPS,
  duration, decoded frame count, and the copied audio stream. Audio-changing builds
  must match their planned output duration and frame count instead.
- Confirm the website's intended file path and that no unresolved issue or missing
  verification is being presented as a pass. Full shipping checks do not authorize
  unrelated changes outside an approved narrow repair.

After the candidate is installed and committed, reclaim its render scratch:

    .video-venv/bin/python scripts/video/clean_video_audit.py            # dry run
    .video-venv/bin/python scripts/video/clean_video_audit.py --delete

It removes only regenerable intermediates - `leg-*.mkv`, `*.wav`, `canvas-*.png`,
and `*-live.mp4` copies - and checks every candidate against `git ls-files` first,
so the committed record (REVIEW.md, edit-manifest.json, contact sheets, transition
strips, transcripts) is never touched. Use `--skip <substr>` to spare a build still
in flight, whose legs `--render-existing` still needs.

**Why this is a ship step, not housekeeping (2026-09-21).** Nothing reclaimed this
until video-audit reached 93 GB and filled the disk mid-render: ffmpeg died with a
broken pipe, and then the harness could not write its own output, so no command
would run at all. 76 GB of it was FFV1 leg files from 85 already-shipped builds.
Legs are worth keeping only while a lesson is still being rebuilt, because
`--render-existing` reuses them; once it ships they are dead weight. Do not copy a
live video into an audit folder either - `grade_bundle.py` takes a path, so point it
at `course-assets/<slug>/<slug>.mp4` directly.

## Shipping filename convention

After approval and verification, replace the canonical unsuffixed MP4 with the
approved candidate. Verify that file and the lesson reference before removing the
superseded candidate. The website must not depend on a review-stage `-vN` path.
Do not delete raw generations when shipping; they may be needed for a later repair.

## Asset retention and safe preparation

Keep current boards in `course-assets/`, Markdown in `lessons/`, prep sources in
`gemini-notebook/<lesson>/`, and raw video/audio sources and candidates in `Prompts/`. Do not recreate `archive/`, `illustrations/`, or
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
status in the active review. Distinguish candidate, shipped locally/pending batch,
and verified live; record the local commit and file hash at shipping, and public
verification only after batch deployment. Keep the user-facing update concise
and link to it.
