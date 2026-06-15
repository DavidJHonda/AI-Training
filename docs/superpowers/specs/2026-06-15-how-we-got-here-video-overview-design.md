# How We Got Here — NotebookLM Video Overview

**Date:** 2026-06-15
**Lesson:** Understand AI → Foundations → How We Got Here (id `howwegothere`, component `HowWeGotHereSection`)
**Status:** Approved in brainstorming; ready for implementation planning.

## Motivation

Offer an optional video-overview path to the How We Got Here lesson as an alternative learning
modality, collapsed by default so it adds no length for students who skip it (the lesson's standing
concern). The video is a NotebookLM-generated overview, so it doubles as a quiet demonstration of a
real study tool, tying to the Study with AI lesson.

## Hosting

Self-hosted. The file `videos/How_We_Got_Here.mp4` (~11 MB) is committed to the repo and served by
Vercel as a static asset at the relative path `videos/How_We_Got_Here.mp4` (same pattern as
`illustrations/*.jpg`). No third-party player, no external scripts, works offline once cached. This
is the app's first video; `videos/` is a new asset directory.

## Component: WatchOverview

A new self-contained sub-component, defined adjacent to `HowWeGotHereSection`, inserted **after the
two hook `BodyP` paragraphs and before `CoreLoopBox`**.

**Collapsed (default):** one soft, full-width clickable bar — a disclosure control:
- Content: a "🎬" mark, bold "Prefer to watch?", the text "Video overview", and a chevron "▸".
- Styling: `var(--card)` background, rounded, `var(--shadowSoft)`, matching house chrome. One short
  row of height; nothing else rendered until opened.

**Expanded (on click):** chevron flips to "▾" and reveals, below the bar:
- A native HTML5 `<video controls preload="metadata">` with a child `<source src="videos/How_We_Got_Here.mp4" type="video/mp4">`, rendered full-width and rounded (`borderRadius` ~12, `width: 100%`, `display: block`). `preload="metadata"` so the 11 MB downloads only when a student plays it; **no autoplay**.
- A small caption below the player (the NotebookLM tie-in):
  "Made with NotebookLM from this lesson's notes. You can do the same with your own class material."

**State:** open/closed is plain `useState(false)` — a disclosure, not lesson progress, so it is not
persisted and resets on navigation.

## Copy constraints

- No em-dashes (design-check expects 7 file-wide; all pre-existing). Use commas/colons/periods.
- **No duration claim** ("3-min", etc.): the file's length cannot be verified in this environment, so
  the bar says "Video overview" with no number.
- Curly punctuation (’) to match house style (e.g. "lesson’s").

## Design-system notes

- Fonts via `var(--sans)`/`var(--serif)`/`var(--mono)` only (design-check enforces).
- No hand-built counter pills, no new shadow literals (`var(--shadowSoft)`), no em-dashes.
- The `<video>` element is new to the file; design-check does not inspect it. The chevron rotation
  may use a simple inline transform; no new keyframes required.

## Code touch points

- New function `WatchOverview(props)` near `HowWeGotHereSection`.
- `HowWeGotHereSection`: insert `React.createElement(WatchOverview, null)` after the second hook
  `BodyP` and before `React.createElement(CoreLoopBox, null)`.
- Commit `videos/How_We_Got_Here.mp4` (currently untracked).

## Out of scope

- A poster/thumbnail image (none available; native first-frame is acceptable). Can add later.
- Transcript review / captions track (no transcript provided yet; a `<track>` can be added later if
  captions are produced).
- Adding the video to any other lesson, or to the print packet.
- No `briefing.md` update (within-lesson content addition; label/id/counts unchanged).

## Follow-ups

- Run `design-check.sh` (should stay PASS) and `node --check` on the inline script before committing.
- Browser-verify: the bar renders collapsed, expands/collapses on click, the player appears and the
  video plays from `videos/How_We_Got_Here.mp4` (HTTP 200 for the asset), no console errors.
- Commit the video file alongside the code change.
