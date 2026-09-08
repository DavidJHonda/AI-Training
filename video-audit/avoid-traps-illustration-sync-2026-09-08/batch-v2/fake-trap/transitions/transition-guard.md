# Transition guard

- Result: FAIL
- Video: `/Users/davidobrien/Developer/AI-Training/Prompts/fake-trap-illustrations-patched-v2.mp4`
- Decoded frames: 6601
- Short visual-island limit: 6 frames
- Manual every-frame strip review: REQUIRED

## Boundaries

- PASS — f402 `illustration-start` — [`boundary-000402-illustration-start.jpg`](boundary-000402-illustration-start.jpg)
- PASS — f573 `appearance-test` — [`boundary-000573-appearance-test.jpg`](boundary-000573-appearance-test.jpg)
- FAIL — f915 `source-trail-test` — [`boundary-000915-source-trail-test.jpg`](boundary-000915-source-trail-test.jpg)
  - Possible stale visual: f922 to f923 (1 frames)
  - Possible stale visual: f923 to f924 (1 frames)
  - Possible stale visual: f924 to f925 (1 frames)
  - Possible stale visual: f925 to f926 (1 frames)
  - Possible stale visual: f926 to f927 (1 frames)
- PASS — f1296 `illustration-end` — [`boundary-001296-illustration-end.jpg`](boundary-001296-illustration-end.jpg)
- PASS — f3581 `illustration-start` — [`boundary-003581-illustration-start.jpg`](boundary-003581-illustration-start.jpg)
- PASS — f4203 `illustration-end` — [`boundary-004203-illustration-end.jpg`](boundary-004203-illustration-end.jpg)
