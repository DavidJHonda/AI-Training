# What Is AI? — donor graphics for the live board stretch, 2026-09-26

Scope: find Notebook drawings in `Prompts/what-is-ai-1.mp4` (2:53.57) and `Prompts/what-is-ai-2.mp4` (3:16.80)
that can break the live video's back-to-back board run (Two Ways 1:05.0–2:00.5, One Picks 2:00.5–2:45.0).
Narration verdicts on the rolls were NOT in scope. Live timings are from `video-audit/what-is-ai-live-review-2026-09-25/REVIEW.md`.
Frames checked at full resolution: `frames/`.

## Usable

| Donor | Source span | What it shows | Live placement | Notes |
|---|---|---|---|---|
| R1 Maya/Leo card | 2:26.2–2:36.4 (10.2 s) | Handwritten card, purple highlighter, the three lines exactly as printed on Board 3 | 2:27.4–2:34.6 under the Maya/Leo reading; back to the board for "It generated a scene" ring | Best find. Text verbatim. Two small drawn avatar icons (Maya, Leo): owner call on the no-people rule |
| R1 Rec/Gen card diagram | 0:57.0–1:02.1 (~5 s, clean; earlier frames carry an "AI TOOL" overlay) | "1. Recommendation AI — Ranks & selects existing items: ★ #1 Top Recommendation / Catalog Option B / C"; "2. Generative AI — Creates & synthesizes new content: Prompt: 'Draft an essay…' → New Synthetic Output" | (A) push in on left card at 1:14.4–1:19.6 "ranking … best match"; (B) push in on right card at 1:37.7–1:46.7 prompt definition (hold/slow-push, donor is shorter than the beat) | No people, no typos. Off-voice words on screen: "synthesizes", "content", "Synthetic" |
| Live's own catalog-grid drawing | live 0:57–1:04 | (per 9/25 review) film-strip tiles + empty prompt box, no text | (C) 2:08.6–2:12.4 "find a movie … from an existing catalog" | Already proposed 9/25 as (c) |

## Maybe

| Donor | Source span | Issue |
|---|---|---|
| R2 Home Theater / Workstation, right half only | 2:19.9–2:23.5 | Right half (blank doc + cursor, sticky notes) fits "write a scene" 2:21.9–2:26.9 and leads into the Maya card. Left half has the Superman logo, so crop is mandatory; half-frame crop is a ~2x upscale, likely soft |

## Rejected

| Donor | Source span | Why |
|---|---|---|
| R1 Avengers home-screen grid | 2:07.1–2:14.5 | Real Avengers poster art (not Civil War); gibberish caption "IS LEPTHS FROM THE TO DIE TO HAND" |
| R1 two-panel catalog/prompt diagram | 2:36.4–2:42.0 | Invented "Match: 98%"; "Synthesizes novel artifacts"; off-lesson prompt "Write a story of the stars…" with half-faded gibberish lines |
| R1 man on couch with TV | 1:47.6–1:50.2 | Drawn person; gibberish labels ("LEAST TANGIRE TV", "FLIT-OFF THE LOGO", "DROP SHADORS") |
| R1 face close-up | 1:50.2–1:53.4 | Drawn person, no teaching |
| R2 "AI TOOL: Utilitarian Task Engine" + two category cards | ~1:20–1:32 | Jargon ("Executing specialized human tasks at scale"); cards nearly empty |
| R2 Home Theater, left half | 2:19.9–2:23.5 | Superman logo (trademark, and the wrong hero) |

## Resulting board runs (with A, B, C, Maya card)

Two Ways: 1:05.0–1:14.4 (9.4 s) / 1:19.6–1:37.7 (18.1 s) / 1:46.7–2:00.5 (13.8 s).
One Picks: 2:00.5–2:08.6 (8.1 s) / 2:12.4–2:27.4 (15.0 s) / 2:34.6–2:45.0 (10.4 s).
Longest run 18.1 s, down from 111.6 s unbroken.

## Side observations (not in scope, noted for the next roll)

- Both rolls spoke stage directions aloud: R1 "Pause." (0:08.92) and "Normal pace." (0:31.40); R2 "Pause for effect." (0:13.46).
- Both rolls drew stock photographs in the history list (R1 Egyptian relief, moon landing, suffrage photo; R2 camels, factory, early airplane).
- R1 spoke all four verbatim lines exactly, including both closing lines.

---

## Build: `Prompts/what-is-ai-v6.mp4` (2026-09-26, David: "build it with A, B, C and Maya")

Script: `scripts/video/build_what_is_ai_donor_breaks.py`. Base = the live file frozen as `baseline-live-2026-09-21.mp4`
(sha 954c22da…). Picture-only; hard cuts out of and back into the board; rings, narration and close untouched.

| Cut | Output frames | Time | Picture |
|---|---|---|---|
| A | 2280–2386 | 1:16.00–1:19.53 | R1 diagram (1:00.00 still, corner-cleaned), push full view → Recommendation card (1.42x) |
| B | 2925–3201 | 1:37.50–1:46.70 | same still, slow push full view → Generative card (1.42x) |
| C | 3906–3978 | 2:10.20–2:12.60 | live's own film-strip grid, live frames from 0:57.50 |
| M | 4431–4638 | 2:27.70–2:34.60 | R1 Maya/Leo card from 2:26.40, corner-cleaned |

Each cut lands after the matching ring has been on screen 1.5–3.4 s (M: 0.7 s); the ring is still up on return.
Board runs now: 1:05.0–1:16.0 (11.0 s), 1:19.5–1:37.5 (18.0), 1:46.7–2:00.5 (13.8), 2:00.5–2:10.2 (9.7), 2:12.6–2:27.7 (15.1), 2:34.6–2:45.0 (10.4).

Verification: 5298 frames at 30 fps (= baseline); audio packet payload identical to the baseline; transition guard PASS on
all 8 boundaries (single clean cut each, strips in `transitions/`); corner mark cloned on all 208 roll-1 frames, 0 declined,
corners inspected (`corner-check.jpg`); boundary frames inspected (`state-boundaries.jpg`). Not done: a full watch by ear
(audio is bit-identical, so nothing new to hear). Upscale on A/B at 1.42x is slightly soft; text stays readable.
Not shipped; live file untouched.

---

## v7: `Prompts/what-is-ai-v7.mp4` — board walk + fixed ring width (2026-09-26)

David: "zoom and pan between elements to be consistent with other videos" on the 1:05 and 2:00 boards; "the highlights look
too thick"; then "Replace the 9/21 scaling rule with a fixed 6 px on-screen highlight at 1080p, regardless of board zoom.
Apply this to 'What is AI?' and the shared tool for future builds. Other shipped videos don't need rebuilding."

Shared tool: `ken_burns_path.ring_px(out_h)` now returns 6 px x out_h/1080 (4 px at 720p) at any zoom; `RING_PX` = 4 in
ken_burns_path and editspec_build (camera fit margins); Edit Spec §5 and the Retrofit Playbook updated.

Script: `scripts/video/build_what_is_ai_board_walk.py` (reuses `build_what_is_ai_donor_breaks.prepare_donors`). Same frozen
baseline. Both board legs re-rendered dense with the house dive pattern (In Your Hands v4): full view through the intro,
24-frame move onto the Recommendation card's text section at its title onset, v5's row rings in turn, pan to the Generative
card at its title onset, its row rings, 30-frame pull-back at the banner onset. v5 ring rects/colours/onsets verbatim, remapped
onto the current canvas (4% tall-board margin). One Picks keeps the scenario ring at full view before the dive. v6's four
cutaways laid over unchanged.

| Board | Output frames | Dive (Rec / Gen) | Pull-back |
|---|---|---|---|
| Two Ways | 1947–3612 | 1:07.47 / 1:26.87 | 1:53.57 |
| One Picks | 3612–4941 | 2:07.03 / 2:19.20 | 2:38.47 |

Verification: 5298 frames at 30 fps; audio packets identical to the baseline; corner mark cloned on all 208 roll-1 frames.
Transition guard: the cutaway and ring boundaries pass; four flags (f2024, f3407, f3811, f4754) are the dive / pull-back moves
themselves (smooth per-frame motion, strip `transitions-v7/boundary-003811-*` inspected, no stale frames). Settled states
inspected (`v7-states.jpg`): text sharp and whole in every dive, rings 4 px throughout, banner ring at full view.
Not shipped; v6 superseded by v7.

**SHIPPED 2026-09-26** (David: "ship it"). v7 copied to `course-assets/what-is-ai/what-is-ai.mp4` (sha 4500df2e…, 19,858,688 bytes,
2:56.60, verified byte-identical to the candidate and served 200 over http); cache key `20260921ship9` → `20260926ship2` on the
`llms` entry; duration pill unchanged (3 min); `course-assets/manifest.json` entry updated. Candidates v6 and v7 removed from
`Prompts/`; raw rolls `what-is-ai-1.mp4` / `-2.mp4` kept (roll 1 is the donor source).
