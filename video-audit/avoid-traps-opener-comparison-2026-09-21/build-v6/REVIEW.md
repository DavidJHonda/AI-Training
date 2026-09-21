# Avoid Traps opener v6 — build review (2026-09-21)

v6 = v5 with the Traps Ahead rings changed to the creed gold, tight to the text (David's one note on v5). Byte-identical to v5 from frame 393 on (sampled every 61st frame: zero difference outside Board 1).

Status: review candidate only. The live video, both raw rolls, the lesson Markdown, and the
four board JPGs are unchanged (protected hashes verified after render).

- Candidate: `Prompts/avoid-traps-opener-v6.mp4`
- SHA-256: `dada263ebcae82a17d3f365a92f6d1c85cab74a488647b7b6debeb8681cc8d01`
- Runtime: 6,543 frames at 30 fps (3:38.10), 1280×720
- Build: `scripts/video/build_avoid_traps_opener_v6.py`; manifest `edit-manifest.json`
- Scope: full production pass on `Prompts/opener-avoid-traps-2.mp4` under the approved plan in
  `../REVIEW.md` (David 2026-09-21: "Agree with everything"), using both recommendations: the
  Read the Water board arrives at "Survival…", and roll 1's binoculars break the section-map run.

## Narration

Roll 2 start to finish, single voice, no grafts, no cuts. The only audio change is the engine
outro removed after "water." (source 213.64 s; digital silence from 214.2 s). Rendered transcript
read in full (`verification/avoid-traps-opener-v5/transcript.txt`): every beat from the three-way
review is present, the banner is spoken, the two closing lines are the last words.

No teaching pause added. Natural gaps in the encoded file at the section boundaries: 0.53 s
(Traps Ahead → server room), 0.49 s (Read the Water → surprise box), 0.41 s (map → binoculars),
0.74 s (banner → lead-in), 0.30 s (lead-in → close). The 0.30 s before "When AI fails" is roll 2's
own pacing and reads as the narrator running the lead-in into the close; flag it on listening.

## Boards and covers

| Board / scene | Output span | Treatment |
|---|---|---|
| The Traps Ahead | 0:00–0:13.10 | Canonical board replaces Notebook's render. Compact, still. Gold (#f2cf5b) rings hugging each line's text, as on the shipped openers (David 2026-09-21; v5 had full-width purple rings). Line rings at spoken onsets: "The false fact" 0:00 (pops in the full view, spec rule 3), "The flattery" 0:02.9, "The fake" 0:04.8, "every trap looks fine" 0:09.6. |
| Read the Water (faces, post-only) | 1:13.73–1:32.57 | Inserted over Notebook's calm-channel diagram from just before "Survival…" through the lifeguard beat. Camera walk, no rings: full board, glide to the channel at "spotting it before you get your feet wet" (1:19.6), to the two figures at "Lifeguards" (1:22.5), back to the full board at "recognize the exact shape" (1:28.6). Notebook's diagram keeps the setup 0:54.7–1:13.7. |
| Avoid Traps section map | 2:04.63–3:11.70 and 3:19.30–3:22.23 | Canonical board replaces Notebook's render. Compact, still. Row rings at "The first category" 2:10.6 (purple), "Next are traps in you" 2:32.6 (blue), "The final category" 2:53.3 (teal); banner ring at "Recognizing the pattern" 3:19.6. |
| Roll 1 binoculars drawing | 3:11.70–3:19.30 | Under "Having this three-part map is your foundation. Once you know where to look…" (roll 1 frames 3891–4114, stable, corner mark cleaned). |
| Standard close | 3:28.17–3:38.10 | Canonical close from Notebook's own close cut; 48-frame hold, 150-frame push, 100-frame settle; literal final frame. |

Longest unbroken board run: 67.1 s (the map before the binoculars), 7 s over the guideline, as
approved. Notebook spans kept: server room, syntax-error cards, relaxed and wary users, the
channel diagram setup, the T-template, surprise box, paper ocean, pipe diagram, eyes, and the
server under the lead-in. No photographs, no web addresses. State sheets: `states-*.jpg`; every
settled ring inspected at full resolution.

Corner mark on every source frame: cleaned at render, 2,427 cloned, 760 inpainted, 0 declined.

## Verification

- Decoded 6,543 frames, matches the plan; 218.1 s of audio.
- `transition_guard.py`: 8 of 8 declared boundaries pass; every strip inspected, the first frame
  after each boundary is already the destination.
- Contact sheets (`verification/…/sheets/`, every 4 s) reviewed end to end.
- Protected files unchanged.

## Listening checks for David

1. 1:13.7 — the board arrives mid-sentence just before "Survival"; audio is continuous, so this is
   a visual check only.
2. 3:28 — the 0.30 s gap between "…errors will announce themselves." and "When AI fails."
3. 3:33.6–3:34.1 — the close audio ends on the sibilant of "water."; confirm no clipped tail.

## Not done

- No headphone audition. Ship on David's approval: replace the live file, cache key
  `20260921ship1`, pill 3 min → 4 min.
