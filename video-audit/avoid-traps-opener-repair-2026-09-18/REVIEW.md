# Avoid Traps opener v4 — current boards + canonical close, opening sentence cut (2026-09-18)

Status: **SHIPPED 2026-09-18** on David's approval ("ship it"): v4 copied to `course-assets/avoid-traps-opener/avoid-traps-opener.mp4` (SHA-256 verified before and after the copy, `6e99f883…`), the v4 candidate removed (v3 was superseded earlier the same day), `index.html` cache key `?v=2` → `?v=20260918ship1`, `course-assets/manifest.json` entry updated, page paragraph edit committed alongside. See `shipping-receipt.json`.

- Candidate (now live): `Prompts/avoid-traps-opener-v4.mp4`, 2:42.55, 4876 frames at 30 fps (live is 5070; 194 frames cut at the head).
- SHA-256: see `edit-manifest.json` → `render_sha256`.
- **Head cut (owner call 2026-09-18):** the opening sentence "You just spent a section under the hood, observing the mechanics that make artificial intelligence possible." (0.00–5.90 s) is removed so the lesson stands alone. The file starts at 6.467 s, a quarter second of room tone before "The same machinery…" (first word 6.76 s by Whisper). Audio from that point is the shipped audio with a 10 ms fade-in, re-encoded once (aac 192k); every board junction moves earlier by 194 frames. The lesson page's first paragraph was cut to match (`index.html` and `lessons/Opener-Avoid.md`).
- Base: the shipped file (`course-assets/avoid-traps-opener/avoid-traps-opener.mp4`, sha `35493525…`: the 2026-09-08 patch plus the illustration sync), taken as the picture source because its raw roll no longer exists. Same shape as the Vector Space, How AI Answers and One More Thing retrofits.
- Build: `.video-venv/bin/python scripts/video/build_opener_avoid_v3_retrofit.py`. It reuses the shipped patch script's own leg renderer and splicer (`build_opener_avoid_patch.py` → `build_jpg_highlight_states.py` + `ken_burns_path.py`) with the shipped plan files from `scripts/video/paths/`, image paths pointed at the current course assets (copies in `plan-*.json`).
- Audio: shipped audio from 6.467 s on, re-encoded once. Decoded PCM vs the shipped file's audio from the same point: correlation 0.99998; the new head is silent (peak 29 of 32767 in the first 10 ms) before the first word.

## What changed

Output frames below are on the trimmed timeline (shipped frame − 194).

| Span (output frames) | Picture | Change |
|---|---|---|
| 0–1209 | Notebook opening from 6.467 s (shipped picture; the network drawing is mid-animation at the new first frame) | first 194 frames cut |
| 1209–1989 | The Traps Ahead creed card: 4 ring states at the shipped junctions (false fact 1502, flattery 1574, fake 1602, inside 1931), gold `#f2cf5b` | card JPG byte-identical to the ship; leg re-rendered from its plan (mean diff 0.2 vs shipped) so its first state can start at 1403 and cover a pre-existing two-frame leak (1403–1404) of Notebook's own pale rendering of the card |
| 1989–3049 | Notebook river / waves / shoreline / lifeguard (shipped picture) | none |
| 3049–3216 | Read the Water photo board (shipped picture) | none: the JPG is byte-identical to the ship, and the shipped leg came from the 2026-09-08 illustration-sync compositor, so the shipped picture is kept rather than re-composed from the plan |
| 3216–3426 | Notebook red T figure (shipped picture) | none |
| 3426–4541 | Avoid Traps section map: whole board, then Traps in the Answer (purple), Traps in You (blue), Traps from the World (teal), takeaway banner (neutral purple) at the shipped junctions (3545 / 3870 / 4090 / 4323) | **new title-banner version of the map** (same 1600×871, shipped rects verified on it) |
| 4541–4876 | Close: 135-frame hold, 120-frame push (3840→3260), 80-frame settle, as shipped | **canonical close** `avoid-traps-opener-close.jpg` via `make_close_board.py --lesson openerprotect` replaces the archived 3840×2160 capture |

Ring treatment is the shipped one (6 px rounded outline in board pixels, camera push 1600→1572 across the states, board padded on the lavender stage).

## Checks

- Decoded frames 4876 = 5070 − 194, as planned.
- Frame-by-frame vs live shifted by 194: Notebook spans mean |diff| 0.7 (re-encode only); creed 0.5 (max 70 on the two covered frames); map 1.7 (title banner); close 9.7 (canonical board).
- `transition_guard.py`: 17 boundaries (leg ins/outs, every ring junction, close junctions, kept water span), 0 failures. Strips inspected on the v3 build (same legs, same seams, shifted): first frame after each boundary is the destination shot; the leaked creed island is gone. First frame of v4 inspected.
- Not auditioned: the new head (waveform is silent to the first word) and the rest is the shipped narration.
- Ring states inspected (`v3-states-sheet.jpg`): complete row / banner inside each ring; canonical close hold, push and last frame correct.
- Protected files (live video, close JPG, three boards) unchanged through the render.

## Still open

- (done) David approved 2026-09-18.
- (done) shipped 2026-09-18; see above.
