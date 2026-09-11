# Next Level Moves — EDIT-SPEC candidate from reroll 2 (2026-09-11)

Status: **built for David's review, not shipped.** Live `videos/next-level-moves.mp4` and the lesson are unchanged.

- Candidate: `videos/next-level-moves-v2.mp4`, 3:15.00, 5850 frames at 30 fps.
- SHA-256: `5b20e470e7fbb64b621da01943b3c00f3df182e38f5edc54b0bddbc3159c25d8`.
- Base roll: `Prompts/next-level-moves-reroll-2.mp4` (3:07; narration verdict KEEP: four moves named, all four takeaways and both closing lines verbatim). No narration cut or grafted.
- Build: `.video-venv/bin/python scripts/video/build_next_level_moves_review.py` (shared `editspec_build.py`).

## Boards (each from the roll's own cut, carried through its spoken takeaway)

| Board | Source span | Density | Rings |
|---|---|---|---|
| Starting a Summer Business | 1499–2171 (0:50.0–1:12.4) | dense | You 0:51, AI 0:56, You 1:02, AI 1:03 (bubble dives), pull back and banner 1:09 |
| Understanding Profit | 2545–3359 (1:24.8–1:52.0) | dense | You 1:26, AI 1:31, banner 1:45 |
| Thinking About College | 3679–4303 (2:02.6–2:23.4) | compact | You 2:05, AI 2:12, banner 2:19 |
| From Idea to Business Plan | 4606–5288 (2:33.5–2:56.3) | dense | early You 2:35, early AI 2:36, later You 2:39, later AI 2:47, pull back and banner 2:53 |

Each board arrives on its cut and is held unmarked by a one-second pause before the first ring, so every full-view open exceeds two seconds. Notebook's own paraphrase cards ("Provide Context First", "Use Familiar Scenarios", "Request the First Step", "Detail Drives Quality") are replaced by the real board with its banner ringed while the takeaway is spoken. Rings are neutral purple (chat boards carry no locked accent).

## Photographs replaced

Three Notebook spans were archival photographs of real people (a 1950s classroom at 0:08–0:13 and 1:52–1:55, a 1970s campus group at 0:36–0:42). The ship checklist forbids them. Each is covered by a still taken from the roll's own next drawn scene ("The Iterative Process", the You/AI partner diagram, the student-and-decision diagram), corner-cleaned and held with the slow push. Stills are `still-420.png`, `still-1300.png`, `still-3500.png`.

## Pauses, corner mark, close

- Eight one-second pauses: on arrival of each board (four) and at the section boundaries into learning, finding a start, iteration, and the close. Measured in the final file: 1.52, 1.40, 1.31, 1.58, 1.69, 1.81, 1.60, 1.56 s.
- Corner mark: 1911 frames paper-cloned, 195 inpainted, 0 declined; `corner-check.jpg` sampled across paper, illustration, stills, and boards.
- Standard close from `CLOSE_BOARDS[aitips]` at the engine close's arrival cut (2:56.3), 48-frame hold, push to 1.2x, settle; outro removed.

## Checks

- Decoded frames 5850 = plan; seven legs decode their spans.
- `transition_guard.py`: 30 boundaries, 0 failures; `review-strip.jpg` inspected.
- Output audio vs edit master correlation 0.99995.
- Settled ring frames inspected (`states-*.jpg`).

## Still open

- Listening: the eight pause joins and the close. Two transcript oddities to hear: 1:33 ("Mode lawns", likely "Mowed lawns") and 2:27 ("in versions").
- The conversations are summarized rather than read in full; the boards carry the dialogue and every takeaway is spoken. Accepted at review.
