# Transition guard

- Result: FAIL
- Video: `Prompts/loudest-voices-v4.mp4`
- Decoded frames: 7047
- Short visual-island limit: 6 frames
- Manual every-frame strip review: REQUIRED

## Boundaries

- PASS — f789 `source-to-experts` — [`boundary-000789-source-to-experts.jpg`](boundary-000789-source-to-experts.jpg)
- PASS — f1061 `dario-graft-start` — [`boundary-001061-dario-graft-start.jpg`](boundary-001061-dario-graft-start.jpg)
- FAIL — f1888 `dario-graft-end` — [`boundary-001888-dario-graft-end.jpg`](boundary-001888-dario-graft-end.jpg)
  - Possible stale visual: f1876 to f1877 (1 frames)
  - Possible stale visual: f1877 to f1878 (1 frames)
  - Possible stale visual: f1878 to f1879 (1 frames)
  - Possible stale visual: f1879 to f1880 (1 frames)
  - Possible stale visual: f1880 to f1881 (1 frames)
  - Possible stale visual: f1881 to f1882 (1 frames)
  - Possible stale visual: f1882 to f1883 (1 frames)
  - Possible stale visual: f1883 to f1884 (1 frames)
- PASS — f2089 `experts-to-hinton-drawing` — [`boundary-002089-experts-to-hinton-drawing.jpg`](boundary-002089-experts-to-hinton-drawing.jpg)
- FAIL — f2267 `hinton-drawing-to-experts` — [`boundary-002267-hinton-drawing-to-experts.jpg`](boundary-002267-hinton-drawing-to-experts.jpg)
  - Possible stale visual: f2267 to f2268 (1 frames)
- PASS — f3943 `experts-to-predictions` — [`boundary-003943-experts-to-predictions.jpg`](boundary-003943-experts-to-predictions.jpg)
- PASS — f6269 `predictions-to-notebook` — [`boundary-006269-predictions-to-notebook.jpg`](boundary-006269-predictions-to-notebook.jpg)
- PASS — f6668 `notebook-to-close` — [`boundary-006668-notebook-to-close.jpg`](boundary-006668-notebook-to-close.jpg)
- PASS — f6927 `close-settle` — [`boundary-006927-close-settle.jpg`](boundary-006927-close-settle.jpg)
