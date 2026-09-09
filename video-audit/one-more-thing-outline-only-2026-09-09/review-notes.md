# One More Thing v4 — outlines only

Review candidate: `videos/one-more-thing-v4.mp4`, 3:36.73, 1280×720, 30 fps.

Removed all post-production shaded heading/label fills from all three teaching boards, including the final math board. Outline rings remain. The original board colors and backgrounds are preserved. Restored Notebook footage, narration, cuts, pauses, and standard close match v3.

Updated the current grading specification, retrofit playbook, video README, board-sync manifest, prompt README, rubric summary, and migration summary to require outline-only highlighting. The shared raster and DOM capture tools no longer add heading/text shading. Legacy raster chip fields are ignored so older plans cannot reintroduce the fills through that renderer. Historical videos and their audit records were not rebuilt.

Verification:

- All 91 heading-region comparisons across the rendered board states are pixel-identical to their clean board regions. No added shading remains.
- Inspected representative full-resolution states from every board.
- Encoded audio stream hash matches v3 exactly. Runtime remains 6,502 frames.
- Transition guard passed all 15 boundaries; inspected the every-frame strips in `transition-audit/group-*.jpg`. No stray scene appears at a handoff.
- Shared raster renderer verified with a legacy chip-containing plan: the heading region remains untouched while the outline is drawn.
- Shared DOM panel function verified to preserve heading, background, padding, and margin styles while adding the outline. JavaScript syntax and Python compilation checks pass.

Build: `.video-venv/bin/python scripts/video/build_one_more_thing_review_repair.py --engaging-visuals`

This is a review candidate. The live lesson video is unchanged.
