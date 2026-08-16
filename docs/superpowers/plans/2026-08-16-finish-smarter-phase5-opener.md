# Finish Smarter Phase 5 — Opener Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the Finish Smarter opener (`openerskills`) as the section's real front door — mirroring Start Smarter's more-than-an-intro intent — and clean up the opener plumbing (PDF slug, dead card-render path).

**Architecture:** The opener is a thin wrapper passing content props to the shared `OpenerSection`. This phase rewrites the wrapper's CONTENT (whyThisMatters paragraphs, featured/common-mistake/question beats, overview bridges polish) and fixes two pieces of plumbing: `OPENER_PDF_NAMES.openerskills` ("Opener-Build" → "Opener-Finish") and the dead `renderCard`/`renderCardGrid` path in `OpenerSection` (flagged by the phases-1-2 final review as the blind spot that let a stale-bridge bug hide).

**Tech Stack:** React.createElement inline; `my-writing-style` skill for all copy.

## Global Constraints

- **Voice:** David's — short sentences, colon setups, NO em-dashes, no exclamation points. Load `my-writing-style` before writing.
- **Intent (from the spec):** "the course is done teaching you the tool; this section is about what you do with that." Mirror of Start Smarter at the intent level (that section is more than an intro; this one is more than an outro) — NOT a structural copy of any other opener, but it must use the standard `OpenerSection` slots like its four siblings.
- **The four beats stay** (THE LAST OF THE AI / SKILLS AI WON'T REPLACE / STAY SHARP / LAND IT) with their current lesson membership; bridges may be polished but must stay truthful to the routed 10 lessons ending in The Final + certificate.
- **Opener rules:** no cross-references to other lesson titles inside opener prose (beat bridges name lessons via their cards/labels — that is the existing convention and fine); transitions live at the beginning; the opener is the section's title page (never Draft).
- **Verification cycle:** node --check (awk -v recipe); serve 8754 + Chrome MCP validate() = 55; chain trace (last `whatyoulearned` → `"welcome"`); design-check PASS; screenshots; kill server.
- **Commit style:** imperative subject; `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` trailer. Never commit owner's unrelated uncommitted work or memory files.
- **Editing gotcha:** `\uXXXX`-plus-unicode lines defeat the Edit tool; sed/python there.

---

### Task 1: Rewrite the opener; fix slug and dead path

**Files:** Modify `index.html`, `briefing.md` (if it names the opener's content), `lessons/` (export); memory files at the end (uncommitted).

- [ ] **Step 1 — Study.** Read the current `openerskills` wrapper fully, the shared `OpenerSection` (all slots + which render), one strong sibling opener (e.g. `openerrealworld` for Embrace the Future) as the quality bar, and the section's 10 lessons' openers/close boards enough to write truthful framing. Verify which overview data renders (kicker + bridge) and which is dead (`renderCard`/`renderCardGrid` + per-lesson `questions` cards — confirm dead by tracing `renderOverview`).
- [ ] **Step 2 — Rewrite the content props** in David's voice:
  - `whyThisMatters` paragraphs: the pivot framing — every section before this taught the tool (use it, understand it, protect yourself from it, face what's coming); this one is about the person holding it. What's left to learn is the part AI can't take. End by setting up the arc: the last of the AI, then the skills that stay yours, then your move, then prove it.
  - Common-mistake beat: the mistake is treating the end of the course as the end of the work (or the designer's sharper alternative — one mistake, stated plainly).
  - `question` prop ("Keep this question in mind"): one durable question for the section (e.g. what do I bring that the tool doesn't — designer's call, one question).
  - Beat bridges: polish pass only where wording can tighten; must remain truthful; LAND IT should land on prove-it-and-certificate without hype.
- [ ] **Step 3 — Plumbing.**
  - `OPENER_PDF_NAMES.openerskills` → `"Opener-Finish"`; regenerate the export under that name; delete stale `lessons/Opener-Build.md`/`.pdf`. (This also clears the last "BUILD YOUR SKILLS"-header stale export for THIS lesson; the unrelated stale exports (`be-curious`, `tune-the-model`) are the separate regen batch — leave them.)
  - Dead path: if Step 1 confirms `renderCard`/`renderCardGrid` and the per-lesson `questions` card data are unrendered across ALL openers, DELETE the dead functions and the `questions` arrays from all five opener wrappers (house rule: delete verified dead code; the kicker+bridge reality stays). If anything turns out live, leave it and flag in the report.
- [ ] **Step 4 — Sweep.** Grep for "Opener-Build" (0 expected after the change, outside historical docs); briefing.md mentions of the opener's content or the dead-card convention (fix if it lies).
- [ ] **Step 5 — Verify.** Full cycle; screenshots: the rewritten opener top-to-bottom; `?print=lesson:openerskills` renders; the download link resolves to `Opener-Finish.pdf`. Confirm the four sibling openers still render correctly after the dead-code deletion (screenshot one).
- [ ] **Step 6 — Memory + commit.** Memory: phase 5 complete; the restructure's five phases all done; remaining = editorial pass + export regen batch + tracker rows + graduation of Draft labels. MEMORY.md hook updated. Commit repo changes.

---

## Self-review notes (applied)

- Single task: content + plumbing share every file and verification run; splitting would double overhead for no isolation gain. The one review doubles as the branch review.
- The dead-code deletion touches all five openers — the verification step explicitly re-checks a sibling.
