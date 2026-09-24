# Rise of Agents v4: review candidate (2026-09-24)

**Candidate:** `Prompts/rise-of-agents-v4.mp4`, 3:07.8 (5634 frames at 30 fps). Review only. The live
video, v2, v3, the lesson, and the page are unchanged.

**Build:** `scripts/video/build_rise_of_agents_v4.py`, with the record in `build/edit-manifest.json`.

**Scope:** v3 (`video-audit/rise-of-agents-v3-2026-09-24/REVIEW.md`) plus the lesson's transition from
the analogy to the example: "Agents are suddenly everywhere, for the obvious reason: they do the work.
Now, let's give you an example." David noted it was missing from v3 and approved option 1 on
2026-09-24.

## The change

| Output | Source | Words | Picture |
|---|---|---|---|
| 0:38.2-0:44.0 | roll 2 18.45-24.30 | "This distinction is exactly why AI agents are suddenly everywhere. They actually do the work." | roll 2's Completed Tasks dashboard drawing ("Data Parsed / Video Trimmed / Email Sent"), from its own cut. The 18.45-18.63 frames are a Notebook board render and aren't shown |
| 0:44.0-0:46.0 | roll 1 35.00-36.95, +1.0 dB | "Let's look at a concrete example." | the dashboard drawing holds its last frame |
| 0:46.0- | roll 2 from 24.45 | "Say you scored 30 points..." | comparison board, as v3 |

Everything after this point is v3, shifted by +7.8 s.

**Gaps at the new joins**, measured on the output:
- live → roll 2: 0.49 s of silence (37.94-38.43)
- roll 2 → roll 1: 0.50 s (43.80-44.30)
- roll 1 → roll 2: 0.42 s (45.72-46.14)

**Roll 1's gain.** Its phrase measured −18.0 dBFS against roll 2's −16.6 over the neighbouring
sentence. +1.0 dB splits the difference, because a short sentence-final phrase naturally reads
quieter. Listen for it.

## Checks

- The frame count is 5634, which equals the plan. The protected files (the live video, v2, v3, roll 1,
  the boards, the lesson, and index.html) are unchanged.
- `transition_guard.py` passed all 19 boundaries. I inspected the strips at the two new boundaries
  (1146, 1379) and the rest carry over from v3.
- The corner mark was cleaned on 2055 frames, with none declined.
- The transcript (`words-medium.txt`) confirms the transition @0:38.5-0:45.7. The remaining narration
  matches v3.

## Listen at these points

- **0:38.2**: live voice into roll 2 ("...to being the supervisor." → "This distinction...").
- **0:44.0** and **0:46.0**: into and out of roll 1's "Let's look at a concrete example.", including its
  level.
- Then v3's joins, each shifted +7.8 s: 1:32.3, 1:46.9, 1:52.1, and ~2:43.

Flags carried from v3 are unchanged.

## Shipped 2026-09-24

David approved the ship ("ship it") after the v4 report. Before installing it, I checked that the file's
sha256 and decoded frame count (5634 frames, 187.8 s) match its edit manifest.

What changed:
- `course-assets/rise-of-agents/rise-of-agents.mp4` is now v4 (sha256 d27f50d630ccae49...).
- The `index.html` `LESSON_VIDEOS.agents` entry has cache key `?v=20260924ship1` and pill "3 min"
  (was "4 min").

The replaced live video (commit 6cccc758, sha256 1dac35e2393d1ae8...) is preserved as
`Prompts/rise-of-agents-live-pre-v4.mp4`, and the v3/v4 builds now read it from there. The v2/v3/v4
candidates and all raw rolls are kept.

**Not verified by listening.** No one has listened to the joins listed above. That was David's call at
ship.
