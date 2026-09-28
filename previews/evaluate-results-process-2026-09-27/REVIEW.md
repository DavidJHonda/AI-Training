# Evaluate the Results process layout

Added the opening “How to Evaluate an AI Answer” flowchart and rebuilt all four stage boards with small highlighted maps. The full overview shows Yes/No routing and the Fix It return loop; the small maps omit the return loop. All 14 existing definitions and four takeaways match the page copy exactly.

- Renderer: `scripts/video/render_evaluate_results_process.py`
- Page: `index.html`, lesson `evaluating`
- Source: `lessons/evaluate-the-results.md`
- Browser review: overview and all four stage boards inspected at 880 px display width; no clipping or overlap.
- Notebook preparation: synced and byte-equality check passed.
- `git diff --check`: passed.
- Global asset audit has unrelated failures for In Your Hands retired filenames and the training-path matcher applied to Where’s the Line references.
- Design check has existing raw-font and em-dash baseline flags; no shared styles or fonts were changed here.

The current MP4 was not changed. Its stage pictures and camera/ring coordinates need a separate visual sync after review of these boards; the new overview also needs placement in the video.

Overview refinement: stage subtext removed; Your Move replaces Make Your Move on all evaluation boards, mini maps, and headings. The Yes/No routes, outcome labels, and Check the fix loop remain.

Video-summary refinement: restored only two overview cues: Quick Pass = “Read. Understand. Validate.”; Dig Deeper = “Choose the checks that fit.” The decision and Your Move boxes remain label-only.
