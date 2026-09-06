# Hallucination reroll materials

Prepared September 5, 2026 after approval of the lesson arc and the new EE-FLOW board.

## Upload to Notebook

- `lessons/hallucination.md`
- `lessons/hallucination-1-example.jpg`
- `lessons/hallucination-2-why.jpg`
- `lessons/hallucination-4-check-claim.jpg`
- `lessons/hallucination-5-close.jpg`

Paste `Prompts/hallucination-video-prompt.txt` into the video customization field. It is 458 whitespace-delimited words, below the 500-word limit.

Do not upload `hallucination-3-real-text.jpg`, which contains Nate and Luke's faces. Keep it for post-production. Do not upload the PDF, the old candidate, or Master Prompt.md. The existing PDF is not part of this reroll packet.

## Teaching requirements

1. The invented Stanford study makes fabricated precision concrete. Define hallucination and explain the four mechanisms on the existing board.
2. The real Reddit joke illustrates a different error: misinterpreting genuine source text.
3. Explicit bridge: a source can be invented, or a real source can be misread. Check for both.
4. Reserve about 40–50 seconds for a spoken walkthrough of Notice the Claim, Find the Source, and Check the Match, with the corresponding example for each. Merely showing the board or advising general skepticism does not satisfy this requirement.
5. Exact two-line course close, with a pause and no added outro.

Target duration is 3:30–4:00; do not rush the checking instruction to meet it. The expanded Markdown explains the existing lesson and board, rather than adding a new framework. These narration expansions are intentionally in the video-prep Markdown; a fresh plain lesson export would lose them.

## Validation

- All four on-page teaching-board assets and their prep copies are byte-identical. No new JPG render was needed.
- JPGs are numbered 1–5, with the face-containing third board intentionally absent from the upload list.
- The current patched video remains available as source footage for a hybrid edit if the reroll has a better ending but weaker earlier sections.
- No video, lesson-page code, or live media was changed while preparing this packet.
- `node scripts/test_hallucination_check_claim.cjs` and `git diff --check` pass.
