# Work With AI opener v2: review candidate (2026-09-14, EDIT-SPEC build)

**Candidate:** `Prompts/work-with-ai-opener-v2.mp4` (2:35.1, 4652 frames, 30 fps). **Live video and lesson unchanged** (`course-assets/work-with-ai-opener/work-with-ai-opener.mp4`,
`lessons/Opener-Work.md`, both board assets and the donor roll hash-verified after the render).
**Build:** `scripts/video/build_opener_work_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration status:** roll 2 was REROLL under `video-audit/opener-work-comparison-2026-09-14/REVIEW.md` solely for the missing close lines.
The donor roll `Prompts/close-opener-work.mp4` (from `lessons/opener-work-donor.md`) supplies both; with them grafted the candidate meets
the hard requirements, and the remaining THIN points (opening refrain paraphrased as "Aim your inquiries with precision. Check every
result for accuracy. Build an active partnership with the system."; "force multiplier" for "multiplies it") stand as accepted by David
2026-09-14 ("Build it").

## Base, donor, audio

- Base: `Prompts/opener-work-2.mp4` (2:39). One narration cut, approved by David 2026-09-14: source 140.3–155.7, "You remain the ultimate
  editor. The user bears total responsibility for the final product. Focus on the instruction on the screen. Work in active partnership
  with the AI. Your personal insight provides the direction while the machine provides the scale." Invented, and the last sentence
  paraphrased the close.
- Two audio-only grafts from the donor, under the standard close board, donor raised 1.1 dB (roll 2 speech −16.7 dBFS, donor −17.8):
  - "Don't just use AI, work with it." donor 33.19–35.74 (span frames 990–1080, troughs at −69 / −65 dB).
  - "AI doesn't replace your thinking, it multiplies it." donor 65.82–68.80 (span frames 1971–2069; the "Because in the end," lead-in is
    dropped at the 65.6–65.8 trough; the donor's digital-zero tail after 69.02 is excluded). **Wording:** the lesson and the close sticky say
    "It doesn't"; the donor says "AI doesn't". David chose the line as spoken over a single-word splice.
  - A 15-frame room-tone breath sits between the two lines.
- Four one-second pauses at idea boundaries (source seams 12.6, 28.4, 72.7, 140.3): refrain → "You've met the tool"; jargon bridge →
  "This concept is visible in the results. Two people…"; camera story → section map; banner → closing lines. None inside a board.

## Boards (page assets, byte-identical to `lessons/`)

| Board | Output frames | Arrives at | Treatment | Leaves at |
| --- | --- | --- | --- | --- |
| Same Tool. Different Results. (`illustrations/opener-work.jpg`, faces; not uploaded) | 1684–2066 | "The phone hardware remained identical in both cases" (54.24), on Notebook's own cut 54.13 | Camera walk, no rings: full board, dive to the two photo panels at "The same logic applies to artificial intelligence" (57.32), back to the full board at "The quality of the output reflects the user's ability" (62.46), ends full. Notebook's phone-and-sandwich drawings stay under the camera story before it (37.5–54.1); the board covers Notebook's invented "THE TOOL IS A CONSTANT" chart (60.0–66.9) | Notebook's cut to the keyboard drawing (66.87) |
| Work With AI section map (`illustrations/opener-work-section-map.jpg`), compact | 2271–4299 | "This map outlines the structural roadmap" (73.04) | Rows ringed in their locked accents: Know What It's For (purple) at "Step one, know what it's for" (76.14), Use It Well (blue) at "step two, use it well" (97.96), Think Before You Trust (teal) at 123.80; banner at "The result depends on how you use the tool" (137.56). Row rects = number circle + title + description inside the card rails, dividers excluded (card 81–1519 × 128–702, dividers y 319 / 511) | the approved cut (140.3) |

**Longest unbroken board run (rule 8b):** the section map, 67.6 s. Notebook drew two things inside that span and neither can break it:
its diagnosis diagram (1:30.63–1:36.80) starts from a blank canvas and is complete only in its last frames, and its sticky-note monitor
(1:55.60–2:01.13) carries lorem ipsum. Notebook spans kept elsewhere: 0–12.6 (refrain diagrams), 12.6–28.4 (man at computer, keyboard),
28.4–54.1 (two phones, hands with phones, blurry and crisp sandwich shots), 66.9–72.7 (keyboard). No photographs in the roll. David can
pull any of it back.

## Verification (ship checklist)

Run on the 12:36 render.

1. Decoded frames 4652 = plan; audio 155.072 s vs 155.067 planned (one AAC frame of padding). Each leg decoded its span exactly.
2. `transition_guard.py` passed all four declared boundaries (1684, 2066, 2271, 4329); `boundary-pairs.jpg`: the first frame after each
   is already the destination (Same Tool board, keyboard drawing, section map, close board).
3. Pauses on the final file (silencedetect −35 dB): 12.37–13.94, 29.15–30.68, 74.47–76.06, 143.16–144.50; close hold 150.89–155.07.
4. Settled ring frames inspected (`states-map.jpg`): the right row each time, complete row inside the ring, banner edge to edge.
5. Same Tool walk keyframes inspected (`preview/same-tool/`): full board, the two photo panels, full board; every window inside the photo.
6. Tail (small.en): "…how you use the tool." 140.68–142.66 → "Don't just use AI. Work with it." 144.42–146.74 → "AI doesn't replace your
   thinking. It multiplies it." 147.92–150.68. Seam profile 143.9–148.4: floor holds at −60 to −70 dB into each onset, no cliff.
7. Corner mark: 509 frames paper-cloned, 1290 inpainted, 0 declined. `corner-check.jpg`: clean on paper and boards; on two drawn scenes
   (around output 0:15 and 0:25) the inpaint leaves a small smear where the mark sat over ink strokes, bottom-right 230×70 px. Same
   treatment as earlier ships; David to eye-test.
8. Standard close from output frame 4329; `last-frame.jpg` is the close board (copy from CLOSE_BOARDS[openerworkwith]).

**Not auditioned by ear.** David should listen to 144.3–151.1: the two donor lines under the close board (different roll, level-matched),
the breath between them, and the join from roll 2's "…how you use the tool." through the pause into the first donor line.

Left undone: the opening refrain remains roll 2's paraphrase (no verbatim source exists for "Don't just ask. Aim." / "Don't just copy.
Check."; the donor buried them too). Optional later graft of the donor's "Don't just use AI, work with it" over roll 2's third opening
sentence (5.3–8.2) was offered and not requested.
