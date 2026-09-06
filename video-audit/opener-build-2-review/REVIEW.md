# Opener Build 2 — review candidate

Built from `Prompts/opener-build-2.mp4`; no live video or lesson HTML changed.

## Approved changes

- Preserved the original 0:59–1:14 passage, including its visuals and narration.
- Removed 0:12.400–0:26.500: coworker/competitor/client, value falling to zero, and the discarded answer setup.
- Removed 2:47.700–3:09.000: the post-roadmap portfolio claim and repeated same-AI setup.
- Ended narration at 3:25.800, after the complete “belong entirely to you” sentence. Added 1.2 seconds of matched source room tone under the close.
- Replaced the creed and roadmap with the supplied current lesson boards, full-width highlights, and locked local accents. The compact roadmap stays completely visible.
- Replaced the engine close with the course close and its standard 1.2× push/settle. Kept the approved narration paraphrase; no fabricated or regenerated voice.

## Finished timeline

| Time | Event |
| --- | --- |
| 0:12.400 | Opening cut; resumes “True lasting value…” |
| 0:16.800–0:35.700 | Creed board and full-width gold highlights |
| 0:44.900–0:59.900 | Original 0:59–1:14 passage, preserved |
| 2:14.300–2:33.600 | Roadmap; full rows highlighted purple, blue, then teal |
| 2:33.600 | Cut to “When you sit down to work…” |
| 2:40.533 | Standard close begins |
| 2:50.400–2:51.600 | Room-tone closing hold |

## Verification

- Sequentially decoded all 5,148 finished frames at 30 fps: 2:51.600.
- Transition guard passed all 16 declared picture, highlight, and audio-tail boundaries.
- Visually inspected all 16 every-frame boundary strips. No discarded source-picture islands at the cuts or board replacements.
- Inspected settled frames for the creed, all three full-width roadmap rows, and the final close. No clipped text, inset row rings, white corner brackets, or cropped closing copy.
- Re-transcribed the final render: both joins retain complete intended sentences; the ending retains “belong entirely to you.” The requested passage is present in full.
- Audio edits use measured silent shoulders and 5 ms endpoint fades. Breath cleanup does not ripple the timeline. No additional breath removals were performed.
- Original upload SHA-256 verified unchanged after rendering; exact source and board hashes, geometry, colors, and frame mappings are in `edit-manifest.json`.

The transcript and signal checks support word/cut integrity; they are not a claim of a separate human listening review. Owner approved playback and shipping after the final-line correction below.

## Final-line highlight correction

The creed's smaller closing line now uses source bounds `(72, 575, 1528, 630)` instead of `(72, 580, 1528, 638)`. The measured glyphs span y=587–618, giving 12px of vertical clearance on each side. Full component width and highlight timing are unchanged. The rebuilt render passed all 16 transition checks; the changed highlight's boundary strip and settled frame were visually inspected. Duration remains 5,148 frames, and decoded audio is bit-identical to the preceding candidate (SHA-256 `49c6cbf5e06906f9d423e1701547eb611e813e9cb46aa21edd39db569067beeb`).

## Shipped September 5, 2026

- Approved candidate moved to `videos/opener-build.mp4`; file SHA-256 verified identical before and after: `bfc94366ed51bc871d4516fddd21eba16941cf057812dcfcefd793543e541dcd`.
- Changed only the `openerskills` video entry in `index.html` from coming-soon to the shipped source, with a 3-minute label and section-map CTA. Preserved unrelated in-progress edits.
- Removed three unused uploads from Prompts: `opener-build.mp4`, `opener-build-reroll.mp4`, and `opener-build-2.mp4`. They are recoverable in `/Users/davidobrien/.Trash/AI-Training-opener-build-unused-20260905-ship/`.
- Kept the prompt, lesson markdown, boards, and audit/build records. The historical build requires restoring its original source from Trash if another repair is needed.
