# How NotebookLM Works — section design

**Date:** 2026-06-09
**Lesson:** Study with AI (`studying` section in `index.html`)

## Purpose

A static diagram that shows, at a glance, how NotebookLM turns a student's
own sources into study material: many inputs flow **into** NotebookLM, which
fans **out** into study outputs. Reinforces the "START HERE / use NotebookLM
as your main study tool" recommendation that precedes it.

## Placement

Immediately after the **START HERE** recommendation, before **PICK THE
STRONGER PROMPT**. Flow of the lesson: recommend NotebookLM → show how it
works (this section) → practice prompts.

## Layout

A single lavender container (matches the lesson's box style) holding a
left-to-right flow:

```
WHAT YOU FEED IN      →   [ NotebookLM ]   →   WHAT YOU GET OUT
```

- **Left panel** — "What you feed in": vertical list of input chips.
- **Center node** — emphasized "NotebookLM" hub.
- **Right panel** — "What you get out": vertical list of output chips.
- Arrows connect inputs → hub → outputs.

Static (no interaction) — it *shows* how the tool works.

## Content (curated to what matters, not the full lists)

**Inputs:** Notes & PDFs, Slides, Images, Websites & articles, YouTube
videos, …and more.

**Outputs:** Quiz, Flashcards, Study guide, Audio overview, Mind map, Video
overview, …and more.

## Style

- Reuse the lesson's palette: inputs in the blue family (`#d6e2f4` /
  `#2f4cb8`), outputs in the purple family (`#ddd0ef` / `#5a3aa6`), hub
  emphasized with the primary color.
- Each chip: small white card with an emoji icon + label.
- Built with `React.createElement` inline, consistent with the file.

## Out of scope

- The raw NotebookLM file-type list (pdf, txt, md, …) — represented by
  "…and more".
- Outputs not core to studying (Slide Deck, Infographic, Data Table) —
  folded into "…and more".
