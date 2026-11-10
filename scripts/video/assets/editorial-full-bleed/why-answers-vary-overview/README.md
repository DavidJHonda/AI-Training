# Why Answers Vary overview artwork

Format: Editorial Explainer Three-Card Full-Bleed (EE-3FB).

`art-sheet.png` is purpose-built soft 3D editorial artwork generated on November 10, 2026. Its three horizontal bands supply the art for three cards rendered from left to right. Teaching copy is added deterministically by `scripts/video/render_why_answers_vary_overview.py`, using the shared EE-3FB renderer.

- Model & Thinking: blue `#1652f0`. Two different model metaphors produce different outputs from matching input symbols.
- What AI Receives: teal `#0e8f86`. Extra context accompanies a prompt and changes the output.
- AI’s Choices: purple `#4f2fc4`. One input and candidate pool branch to different possible choices.

These are visual metaphors, not literal model architecture or extra narrated facts. The generated art has no essential text. The renderer crops the sheet at its native color boundaries, then cover-fills the canonical 485/486-by-273-pixel frames. It adds the standard accent washes, outlines, typography, and course credit. Board height follows the longest card copy.

Canonical page and upload asset: `course-assets/why-answers-vary/why-answers-vary-overview.jpg`. Run the renderer, refresh its generated-assets manifest entry, then sync the lesson upload bundle after changes.
