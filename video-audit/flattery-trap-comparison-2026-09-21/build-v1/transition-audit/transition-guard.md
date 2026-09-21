# Transition guard

- Result: FAIL
- Video: `Prompts/flattery-trap-v1.mp4`
- Decoded frames: 9865
- Short visual-island limit: 6 frames
- Manual every-frame strip review: REQUIRED

## Boundaries

- PASS — f690 `source-to-compare-board` — [`boundary-000690-source-to-compare-board.jpg`](boundary-000690-source-to-compare-board.jpg)
- PASS — f2487 `compare-to-cycle-board` — [`boundary-002487-compare-to-cycle-board.jpg`](boundary-002487-compare-to-cycle-board.jpg)
- FAIL — f3385 `cycle-board-to-notebook` — [`boundary-003385-cycle-board-to-notebook.jpg`](boundary-003385-cycle-board-to-notebook.jpg)
  - Possible stale visual: f3385 to f3390 (5 frames)
- PASS — f4000 `notebook-to-syco-board` — [`boundary-004000-notebook-to-syco-board.jpg`](boundary-004000-notebook-to-syco-board.jpg)
- PASS — f4317 `syco-board-to-notebook` — [`boundary-004317-syco-board-to-notebook.jpg`](boundary-004317-syco-board-to-notebook.jpg)
- PASS — f4717 `notebook-to-graft` — [`boundary-004717-notebook-to-graft.jpg`](boundary-004717-notebook-to-graft.jpg)
- PASS — f4814 `graft-to-notebook` — [`boundary-004814-graft-to-notebook.jpg`](boundary-004814-graft-to-notebook.jpg)
- PASS — f5067 `notebook-to-moves-board` — [`boundary-005067-notebook-to-moves-board.jpg`](boundary-005067-notebook-to-moves-board.jpg)
- FAIL — f8265 `moves-board-to-notebook` — [`boundary-008265-moves-board-to-notebook.jpg`](boundary-008265-moves-board-to-notebook.jpg)
  - Possible stale visual: f8265 to f8269 (4 frames)
- PASS — f8475 `notebook-to-moves2` — [`boundary-008475-notebook-to-moves2.jpg`](boundary-008475-notebook-to-moves2.jpg)
- FAIL — f8991 `moves2-to-notebook` — [`boundary-008991-moves2-to-notebook.jpg`](boundary-008991-moves2-to-notebook.jpg)
  - Possible stale visual: f8991 to f8996 (5 frames)
- PASS — f9362 `notebook-to-moves3` — [`boundary-009362-notebook-to-moves3.jpg`](boundary-009362-notebook-to-moves3.jpg)
- PASS — f9572 `moves3-to-close` — [`boundary-009572-moves3-to-close.jpg`](boundary-009572-moves3-to-close.jpg)
