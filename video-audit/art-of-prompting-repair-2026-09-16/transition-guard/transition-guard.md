# Transition guard

- Result: FAIL
- Video: `Prompts/art-of-prompting-v1.mp4`
- Decoded frames: 7179
- Short visual-island limit: 6 frames
- Manual every-frame strip review: REQUIRED

## Boundaries

- PASS — f177 `photo-cover-to-base` — [`boundary-000177-photo-cover-to-base.jpg`](boundary-000177-photo-cover-to-base.jpg)
- PASS — f545 `base-to-gibberish-cover` — [`boundary-000545-base-to-gibberish-cover.jpg`](boundary-000545-base-to-gibberish-cover.jpg)
- PASS — f797 `to-good-board` — [`boundary-000797-to-good-board.jpg`](boundary-000797-to-good-board.jpg)
- PASS — f932 `to-roll2-definitions` — [`boundary-000932-to-roll2-definitions.jpg`](boundary-000932-to-roll2-definitions.jpg)
- PASS — f1203 `to-on-target-donor` — [`boundary-001203-to-on-target-donor.jpg`](boundary-001203-to-on-target-donor.jpg)
- FAIL — f1342 `to-open-ended-donor` — [`boundary-001342-to-open-ended-donor.jpg`](boundary-001342-to-open-ended-donor.jpg)
  - Possible stale visual: f1351 to f1352 (1 frames)
  - Possible stale visual: f1352 to f1353 (1 frames)
  - Possible stale visual: f1353 to f1354 (1 frames)
- FAIL — f1472 `resume-base-good-board` — [`boundary-001472-resume-base-good-board.jpg`](boundary-001472-resume-base-good-board.jpg)
  - Possible stale visual: f1477 to f1478 (1 frames)
  - Possible stale visual: f1478 to f1479 (1 frames)
  - Possible stale visual: f1479 to f1480 (1 frames)
  - Possible stale visual: f1480 to f1481 (1 frames)
  - Possible stale visual: f1481 to f1482 (1 frames)
  - Possible stale visual: f1482 to f1483 (1 frames)
  - Possible stale visual: f1483 to f1484 (1 frames)
- PASS — f1648 `board-to-notebook` — [`boundary-001648-board-to-notebook.jpg`](boundary-001648-board-to-notebook.jpg)
- PASS — f1948 `to-move1-board` — [`boundary-001948-to-move1-board.jpg`](boundary-001948-to-move1-board.jpg)
- PASS — f2436 `board-to-example` — [`boundary-002436-board-to-example.jpg`](boundary-002436-board-to-example.jpg)
- PASS — f2753 `to-move2-board` — [`boundary-002753-to-move2-board.jpg`](boundary-002753-to-move2-board.jpg)
- PASS — f3290 `board-to-notebook` — [`boundary-003290-board-to-notebook.jpg`](boundary-003290-board-to-notebook.jpg)
- PASS — f3423 `to-muted-paragraph` — [`boundary-003423-to-muted-paragraph.jpg`](boundary-003423-to-muted-paragraph.jpg)
- PASS — f3437 `mute-to-source` — [`boundary-003437-mute-to-source.jpg`](boundary-003437-mute-to-source.jpg)
- PASS — f3517 `to-muted-question` — [`boundary-003517-to-muted-question.jpg`](boundary-003517-to-muted-question.jpg)
- PASS — f3528 `mute-to-source` — [`boundary-003528-mute-to-source.jpg`](boundary-003528-mute-to-source.jpg)
- PASS — f3898 `to-continued-board` — [`boundary-003898-to-continued-board.jpg`](boundary-003898-to-continued-board.jpg)
- PASS — f4119 `board-to-move3-drawing` — [`boundary-004119-board-to-move3-drawing.jpg`](boundary-004119-board-to-move3-drawing.jpg)
- PASS — f5057 `to-move4-board` — [`boundary-005057-to-move4-board.jpg`](boundary-005057-to-move4-board.jpg)
- PASS — f5392 `board-to-move4-drawing` — [`boundary-005392-board-to-move4-drawing.jpg`](boundary-005392-board-to-move4-drawing.jpg)
- PASS — f5997 `overclaim-cut-resume` — [`boundary-005997-overclaim-cut-resume.jpg`](boundary-005997-overclaim-cut-resume.jpg)
- PASS — f6001 `resume-destination-drawing` — [`boundary-006001-resume-destination-drawing.jpg`](boundary-006001-resume-destination-drawing.jpg)
- PASS — f6710 `to-close` — [`boundary-006710-to-close.jpg`](boundary-006710-to-close.jpg)
- PASS — f7059 `to-close-tail` — [`boundary-007059-to-close-tail.jpg`](boundary-007059-to-close-tail.jpg)
