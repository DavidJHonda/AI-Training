# Per-Lesson Video Overviews + Capstone Activities — Design

**Date:** 2026-06-19
**Status:** Part 1 (Watch control) **built & verified** 2026-06-19. Part 2 (capstone
activities) and video production/rollout still deferred (see Sequencing).

## The shift

Today only two lessons (`howwegothere`, `inference`) carry a video overview. The
goal is for **every teaching lesson** to offer two ways to learn the same
material:

1. **Watch** the lesson's video overview, or
2. **Read** the content on the page.

Section **openers** are the only exception — they get no video.

Because video is a *passive* medium, it removes the active engagement that
reading-and-scrolling provides. To compensate, every teaching lesson also gains
a **capstone activity** (see below).

## Part 1 — The Watch control (in-class layout)

Redesign the existing `WatchOverview` component from a full-width box on its own
line (which pushes all reading content down) into a **compact pill**.

Locked decisions:

- **Placement:** compact pill at the **top-right of the lesson title**,
  top-aligned to the title's first line so it doesn't drift when the title wraps
  to two lines (e.g. *Embeddings: Meaning as Numbers*). On **narrow / mobile**
  widths it drops to its own line under the title rather than crushing the title.
- **Label:** `▶ WATCH · 2 min` only. **No subtext** (the old
  "How four ideas became AI" teaser is dropped — the section kicker + title
  already supply context, and 54 teasers is needless copy to write and maintain).
- **Player behavior:** clicking expands the **16:9 player full content-width,
  inline, just below the title**. Reading content shifts down only when the
  student actively chooses to watch. (No modal.)
- The exact visual format (pill styling, spacing, color) is being explored
  separately in Claude Design; implementation will match whatever that produces,
  using the existing design tokens.

**As built (2026-06-19):**

- New `LESSON_VIDEOS` map (`sectionId → { src | youtubeId, duration, caption? }`)
  drives everything. Only `howwegothere` and `inference` are listed today.
- `WatchPill` (the compact pill) and `WatchPlayer` (inline 16:9 player, local mp4
  *or* `youtube-nocookie` iframe with `rel=0&modestbranding=1`) replace the old
  full-width `WatchOverview` box, which is removed.
- `LessonHeader` looks up `LESSON_VIDEOS[sectionId]`, renders the pill in a flex
  title row (`justify-content: space-between`, `flex-wrap: wrap` so it drops below
  the title on narrow widths) and the player below the title when open. Lessons not
  in the map (incl. openers, which don't use `LessonHeader` anyway) show no pill.
- The Chinese Room **audio** overview box and `videos/Chinese_room.m4a` were
  deleted.
- Verified in-browser: `validate()` clean (62 sections), pill renders top-right of
  the title, click expands the 16:9 player full-width below the title with caption.

## Part 2 — Capstone activities (two-layer model)

Engagement lives in **two distinct layers** — do not collapse them:

- **Inline aids** (charts, guides, small illustrative TRY ITs) stay **contextual**
  — next to the concept they reinforce. In-context practice lands harder than
  deferred practice; these are not moved.
- **Capstone activity** — one "now apply what you just learned" task — lives in a
  **consistent slot at the bottom of every teaching lesson**, just above
  `KeyInsight` / `LessonRule` / `NextLessonGate`. Lesson rhythm becomes:
  *content (+ inline aids) → DO THE ACTIVITY → key insight → advance.*

Rationale for bottom placement:

1. **Consistency** — students learn the rhythm "watch or read, *then* do" and
   always know where the activity is.
2. **Restores active recall** — the precise thing video erodes. This is the
   strong justification.
3. **Pairs with the advance gate** — the recently-softened `NextLessonGate` nudge
   has a natural thing to point at.

Explicitly **not** justified by "video-watchers scroll past the charts and get
exposed" — passive scroll-past is weak learning and fast-scrollers skip it. The
capstone earns its place as active recall, not forced incidental exposure.

**"Always" = every teaching lesson, with exceptions:**

- Section **openers** (no activity, as with no video).
- Lessons that **are themselves an activity** (e.g. `keyterms` Vocab Quiz,
  `testyourself`, `headtohead` Beat the Clock) — no second activity stapled on.

## Production & hosting (deferred decisions, recorded)

- **Production method unchanged for now** (NotebookLM-generated, as the current
  two videos). Content must be **100% locked** before videos are produced — we
  are not there yet.
- **Hosting (later):** YouTube **unlisted**, embedded via privacy-enhanced
  `youtube-nocookie.com` with `rel=0` + `modestbranding` to suppress related-video
  distraction for the teen audience. Chosen because it is free with no upload caps
  and keeps the repo tiny.
- **Do not commit videos to git.** ~54 videos at 12–33 MB each ≈ ~1 GB; the repo
  `.git` is already ~267 MB with only three media files. In-repo video does not
  scale. When converting, reference videos by ID/URL, not by committed file.

## Sequencing

Implementation is **deliberately deferred** and gated on:

1. The Watch-control visual format coming back from Claude Design.
2. Lesson content being locked before any video production.

The capstone-activity rollout is a large content effort (~50 activities written
to fit each lesson), not a single code change — it proceeds lesson by lesson.

This document records the agreed direction so it survives across sessions; it is
not a green light to start building.
