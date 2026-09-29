Video preparation — one folder per lesson

Each lesson owns its editable PROMPT.txt, upload variants in assets/, and any prep
notes or alternate kits. These are source material and belong in Git. The registry
is upload-sets.json. Canonical teaching stays in lessons/ and boards in course-assets/.

For a registered lesson:
  1. Edit its prompt, sources, or registry entry as needed.
  2. Run .video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson <slug>
  3. Run the same command with --check.
  4. Upload everything in the lesson's upload/ folder, paste PROMPT.txt into video
     customization, and save the raw result in Prompts/ as its README.txt directs.

Only upload/, the generated per-lesson README.txt, and root MANIFEST.json are derived
and gitignored. Sync preserves prompts, assets, notes, and alternate kits. Never edit
upload/ copies; change their sources. Never use upload/ copies as registry sources.

Current prompts only. The registry's lessons list contains standard kits available
for sync. needs_preparation lists lessons whose legacy prompts were removed; prepare
a fresh kit from the current lesson before generating. retired_kits records abandoned
experiments without retaining their prompts. Old section notes are historical context,
not upload instructions. Sync rejects prompts without the current four ordered blocks.

AI Brain Break retains a purpose-specific activity prompt and source outside the
standard lesson registry. Tail of Hanoi is part of its core lesson video; its
standalone prep has been removed.

Shared preparation rules: scripts/video/PREPARATION.md
Production and shipping: scripts/video/README.md
Historical/current section context: scripts/video/kits/
Raw rolls, audio repair sources, and video candidates: Prompts/
