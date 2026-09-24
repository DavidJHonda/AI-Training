# Embrace the Future opener v5: review candidate (2026-09-24)

Scope: full production pass on `Prompts/opener-embrace-4.mp4`, approved by David on 2026-09-24:
two cuts, no graft, photographs covered, canonical boards, section-map hold broken, outro removed.
Build: `scripts/video/build_opener_embrace_v5.py`. Output: `Prompts/embrace-the-future-opener-v5.mp4`,
6168 frames, 3:25.6. The live video, lesson, boards and index.html are unchanged (hashes verified).

## Narration
- Cut 1: source 0:00-0:04.40, "Look at this board. It shows what everyone is saying right now." The video opens 0.32 s before "It's going to cure diseases."
- Cut 2: source 1:03.07-1:06.53, "To understand this debate, look at this vintage map." The joined gap measures 0.53 s in the output (0:58.35-0:58.87).
- No grafts and no added pauses.

## Pictures (output times)
| Output | Content |
|---|---|
| 0:00-0:10.2 | What Everyone's Saying (canonical). Gold ring on each quote as it's spoken, then "who's right?", then "nobody knows." |
| 0:23.6-0:28.9 | Replaces the GOAL ACHIEVED photo with roll 1's "GOAL ACHIEVED: SMARTER THAN THE TOOL" compass drawing (its last frame holds for about 2 s) |
| 0:58.7-1:05.5 | Replaces the map scan with roll 1's Terra Incognita paper map |
| 1:05.5-1:12.8 | Replaces the sea-monster chart with roll 1's relief map, which has a serpent in it |
| 1:12.8-1:30.4 | Edge of the map (canonical), using the live video's camera: full width, then the monster on "Worriers", then the island on "optimists" |
| 1:52.8-2:08.6 | Replaces the caravel photo with roll 1's relief map showing Magellan's route from Seville |
| 2:43.2-3:17.2 | Section map (canonical), ringing rows One/Two/Three and the banner. Broken at 2:58.4-3:03.1 by roll 3's drawing of a locked monitor and a robot planting a seedling, under "the honest case for worry alongside the real-world upside" |
| 3:17.2- | Canonical close; Notebook's close card and outro removed |

Longest board run: 17.6 s (edge of the map). Section map runs: 15.2 s and 14.0 s.

## Checks
- Decoded frames match the plan (6168).
- transition_guard: 13/13 boundaries pass. The strips were not inspected individually.
- Corner mark: 3084 frames cloned, 1119 inpainted, 0 declined.
- Board rings checked on the state sheets (`build/states-*.jpg`).

## Kept, David's call
- COMPUTATIONAL ENGINE schematic (0:10-0:23)
- Three Human Archetypes drawn faces (0:40-0:51)
- 3D question mark (0:51-0:58)
- Orange X with illegible handwriting (2:08.6-2:11)

## Not auditioned
Nobody has listened to the cut-1 opening, the cut-2 join at 0:58.6, or the close.
