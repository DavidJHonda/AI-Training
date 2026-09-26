# Transition guard

- Result: FAIL
- Video: `Prompts/what-is-ai-v8.mp4`
- Decoded frames: 5156
- Short visual-island limit: 6 frames
- Manual every-frame strip review: REQUIRED

## Boundaries

- PASS — f370 `notebook-to-desk` — [`boundary-000370-notebook-to-desk.jpg`](boundary-000370-notebook-to-desk.jpg)
- PASS — f657 `def-graft-in` — [`boundary-000657-def-graft-in.jpg`](boundary-000657-def-graft-in.jpg)
- PASS — f783 `desk-to-notebook` — [`boundary-000783-desk-to-notebook.jpg`](boundary-000783-desk-to-notebook.jpg)
- FAIL — f4676 `comp-graft-in` — [`boundary-004676-comp-graft-in.jpg`](boundary-004676-comp-graft-in.jpg)
  - Possible stale visual: f4685 to f4686 (1 frames)
  - Possible stale visual: f4686 to f4687 (1 frames)
  - Possible stale visual: f4687 to f4688 (1 frames)
- PASS — f4832 `comp-graft-out` — [`boundary-004832-comp-graft-out.jpg`](boundary-004832-comp-graft-out.jpg)
- PASS — f4862 `board-to-close` — [`boundary-004862-board-to-close.jpg`](boundary-004862-board-to-close.jpg)
