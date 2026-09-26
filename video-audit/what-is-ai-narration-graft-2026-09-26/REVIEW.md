# What Is AI? — v8 review cut: roll 1's verbatim lines grafted into the live video, 2026-09-26

David: "build the review cut" (plan: definition, comparison takeaway and closing from roll 1; Ask the Desk board held
through the definition with its banner ringed; everything else as shipped). **Review only; not shipped. Live file untouched.**

- Candidate: `Prompts/what-is-ai-v8.mp4` — 5156 frames, 30 fps, 2:51.87 (live 2:56.60)
- Base: live 20260926ship2 (v7), frozen as `baseline-20260926ship2-live.mp4` (sha 4500df2e…)
- Donor: `Prompts/what-is-ai-1.mp4` (sha 483da7e4…)
- Script: `scripts/video/build_what_is_ai_v8_narration.py`; manifest `edit-manifest.json`
- Source limitation: base is the finished live file (already corner-cleaned), so the picture is one extra encode generation,
  and kept live audio is decoded AAC re-encoded once.

## Splices (output timeline)

| Output | What | Source |
|---|---|---|
| 0:00.00–0:21.90 | Live hook, desk, "ask AI", the list | live 0:00.00–0:21.90 |
| 0:12.33–0:26.10 | Ask the Desk board, still full view, shipped framing (2044x1150 canvas); banner ring from 0:22.40 | desk leg (was 0:12.33–0:19.13 then the invented-dates timeline) |
| 0:21.90–0:26.10 | **"AI is software built to do things that used to take a human brain."** (0 dB) | roll 1 0:36.10–0:40.30 |
| 0:26.10–2:35.87 | Live: four examples → "It generated a completely original scene…" | live 0:28.63–2:38.40 |
| 2:35.87–2:41.07 | **"One helps you find something to watch. The other helps you create a story of your own."** (+2.0 dB), live picture continues (banner ring lands on "One") | roll 1 2:36.00–2:41.20 |
| 2:41.07–2:42.07 | Live silence under the One Picks banner | live 2:43.60–2:44.60 |
| 2:42.07–2:47.87 | Standard close; **"Two kinds. One picks, one creates. This course is about the one that creates."** (+3.5 dB) | roll 1 2:44.46–2:50.27 |
| 2:47.87–2:51.87 | Settled close hold (120 frames, matched room tone) | — |

Replaced live wording: "That happens because AI is software built to perform tasks that used to require a human brain." /
"One tool helps you … a completely original story." / "There are two kinds of AI. One picks and one creates. This course is
exclusively about the AI that creates." Every cut sits in measured silence (20 ms RMS profiles; medium.en word onsets).
Gaps vs live: into the definition 1.36 s (live 1.52 to "That"), out of it 0.34+0.27 s (live 0.64), into the comparison 0.84 s
(live 0.84), comparison → "Two kinds" 1.44 s (live 1.46).

## Verification

- Decoded 5156 frames at 30 fps = planned total.
- medium.en on the candidate: all three roll-1 lines verbatim; "Berlin Wall." → "AI is software…" and "…human brain." → "It can understand…" intact.
- Speech level: 72.0 / 72.0 / 72.1 dB around and through the definition; 74.4 / 74.0 / 74.2 dB before, through and in the close.
  15 samples at ≥32000 in the boosted grafts (live has 17 elsewhere); not audible-risk but noted.
- `transition_guard.py`: 5/6 pass. The flag at 4676 (frames 4685–4688) is the live v7 pull-back onto the One Picks banner — continuous
  live frames under an audio-only graft; strip inspected. Desk→drawing (783) and board→close (4862) are single clean cuts, strips inspected.
- Desk states inspected (`states-desk.jpg`): banner ring 4 px, whole banner, board edge-to-edge as shipped.

## Not done / open

- **No listening by ear.** David to listen at 0:21–0:27 (live → roll 1 → live voice), 2:35–2:42, and the close — voice continuity is the open question.
- Not touched (outside this plan): after the desk board the live picture resumes on Notebook's "AI: Software Emulating Intelligence" chip
  (gibberish code props) and the "Key AI Capabilities" four-panel (invented examples, banned word "Capabilities"), 0:26.1–~0:33.6.
  Also still live: "suggest ideas for your homework" (lesson: "for a history project").

**SHIPPED 2026-09-26** (David: "ship it"). v8 copied to `course-assets/what-is-ai/what-is-ai.mp4` (sha d3dc0512…, 17,575,182 bytes,
2:51.87, byte-identical to the candidate, served 200 over http); cache key `20260926ship2` → `20260926ship5` on the `llms` entry;
duration pill unchanged (3 min); `course-assets/manifest.json` entry updated. Candidate removed from `Prompts/`; raw rolls kept.
