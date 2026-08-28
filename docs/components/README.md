# Course Visual System

This directory documents the visual language students see in the live course.
It separates three surfaces that used to be treated as one component library:

1. **Page components** are React layouts rendered by `index.html`.
2. **Boards** are static 16:9 teaching graphics shared by lesson pages and video
   preparation materials.
3. **Utility formats** are openers, closing cards, worked examples, activities,
   assessments, quotations, and other purpose-built exceptions.

The governing principle is **one course shell, two primary board families**. The
shell makes the course recognizable. The two families let the visual tone match the
teaching job instead of forcing every idea into the same template.

## Current documentation

- [Page components](page-components.md) explains the roles of the live React
  components. `index.html` remains authoritative for implementation details.
- [Board system](boards/README.md) defines the shared shell, the Friendly Schematic
  and Editorial Explainer families, the named `EE-2FB` and `EE-3FB` full-bleed card
  formats, utility exceptions, accessibility rules, and the production workflow.
- [Board inventory](boards/BOARD-INVENTORY.md) classifies current lessons as Keep,
  Normalize, Redesign, or Exception before any broad visual retrofit.

## Source of truth

- Live page behavior: `index.html`
- Current lesson architecture and working agreements: `briefing.md`
- Canonical on-page board assets: `illustrations/`
- Canonical video-prep boards: `lessons/`
- Board/video synchronization: `board-review-first-four/VIDEO-EDIT-TRACKER.md`

When the same board appears on the page and in video preparation, both copies should
be byte-identical. The course should never maintain two visually different versions
of the same teaching beat.

## Course tokens

- Page background: `#f6f5fb`
- Standard outer component and board shade: `#f7f4ff`
- Primary content surface: white
- Primary accent: the live `--primary` token
- Primary ink: the live `--ink` token
- Standard page block gap: the live `--blockGap` token

Do not revive `#eeeaff` as the standard board canvas. It belongs to an older board
specification and does not match the live `--primaryFaint` course shade.

## Archived screenshots

The PNG files directly in this directory are historical component screenshots. They
remain useful as visual references, but they are not behavioral or production
specifications. Many were captured before the current course structure, spacing,
activity patterns, and board system were established.

Do not copy a screenshot without checking its live implementation and the current
documentation above.
