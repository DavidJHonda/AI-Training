# Where AI Works Best v2: review candidate (2026-09-14, EDIT-SPEC build)

**Candidate:** `videos/where-ai-works-best-v2.mp4` (4:52.8, 8783 frames, 30 fps). **Live video and lesson unchanged**
(`videos/where-ai-works-best.mp4`, `lessons/where-ai-works-best.md`, all five board assets hash-verified after the render).
**Build:** `scripts/video/build_where_ai_works_best_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration verdict:** roll 1 REPAIR under NARRATION-REVIEW (`video-audit/where-ai-works-best-comparison-2026-09-14/REVIEW.md`);
this edit performs that repair, so the candidate's narration is KEEP once the graft is heard.

## Base, donor, audio

- Base: `Prompts/where-ai-works-best-1.mp4`. No narration cut. Roll 1's engine close card and Gemini end card removed.
- One audio-only graft (needs listening): roll 1's paraphrase "Just because it can try a task doesn't mean it was built for it."
  (source 279.48–282.60) replaced by roll 2's "Can try is not built for." (`Prompts/where-ai-works-best-2.mp4` 193.56–195.35,
  donor span frames 5798–5865 = 193.27–195.50, inside its silences; roll 2's digital-zero tail after 195.56 excluded).
  Donor gain +1.7 dB (roll 1 speech −17.0 dBFS, roll 2 −18.7 dBFS). A 6-frame room-tone breath sits between "others." and "Can".
  Output: "AI does some things better than others." 284.10–285.64, "Can try is not built for." 286.86–288.28 (small.en re-listen).
  Seam energy profile 285.8–287.2: floor holds at −56 to −69 dB with no cliff, "Can" onset at 286.80.
- Seven one-second pauses at idea boundaries, measured on the final file with silencedetect (−35 dB):
  11.45–12.94 (into the course story), 61.78–63.21 (into Reshape), 104.30–105.82 (into Explore), 144.93–146.62 (into Find),
  191.11–192.59 (into Problems), 236.35–237.79 (into vast exposure), 278.80–280.18 (before the closing lines). Close hold 288.67–292.78.
  No pause inside any board.

## Boards (all compact; page assets byte-identical to `lessons/`)

| Board | Output frames | Arrives at | Rings (spoken onset, source s) | Leaves at |
| --- | --- | --- | --- | --- |
| AI Helped Us Build This Course (`illustrations/where-ai-works-best.jpg`) | 378–1645 | "We saw this distinction clearly when building this very course" (11.72) | none (owner request 2026-09-14: a camera walk instead). Establish the full board with a slight push, then 16:9 windows inside the photograph: the CODE A+ monitor at "When we asked the AI to code the page layouts" (15.26), the LESSON DRAFT C− easel at "But when we asked it to write the first drafts" (21.46), the marked-up draft on the desk at "The code worked, but the text was a mess" (26.92), the two of them at work at "This highlights the gap" (37.76), pull back to the full board at "Because AI struggles… relies on human judgment" (46.90) and hold it to the end. Windows are clamped to the photo rect so no board margin enters a dived frame | Notebook's own cut to the four-shapes drawing (53.83), kept as the hand-off |

**Opener (owner request 2026-09-14):** Notebook's three-card "AI Task Ingestion" graphic finishes drawing at source frame 159 (5.3 s); from
there the engine runs a blue wipe and a glitchy dissolve into "Execution Gap". The candidate holds frame 159 from 5.3 s until the
illustration arrives (output 12.6 s), so the wipe and dissolve never show. (David asked for "the graphic at 7 seconds"; at 7.0 s the
same three cards are already under the blue wash, so the hold starts on the last clean frame of that graphic instead.)
| Reshape Your Material (blue #1652f0) | 1888–3134 | "Let's look at this graphic detailing our first strength" (61.12) | why 65.76, what 74.42, rows 1/2/4 at 84.70/88.90/93.08, banner 96.72 | narration boundary 102.45 |
| Explore Possibilities (amber #a9760c) | 3164–4353 | "Our second strength, as outlined in this next graphic" (102.76) | why 107.76, what 117.48, rows 1/2/4 at 128.66/131.96/134.24, banner 136.86 | 142.10 |
| Find What Matters (purple #4f2fc4) | 4383–5738 | "The third core strength is finding what matters, shown here as a funnel" (142.60) | why 148.26, what 157.24, rows 1/2/3 at 170.96/174.36/178.54, banner 183.10 | 187.25 |
| Work Through Problems (teal #0e8f86) | 5768–7095 | "Our fourth and final strength… represented by these interlocking blocks" (187.52) | why 193.16, what 205.78, rows 1/2/4 at 217.12/221.16/222.68, banner 227.38 | 231.50 (audio); picture resumes at source 6952, the first frame of Notebook's Core Capabilities → Vast Exposure scene (blank canvas, then the draw-in). The first render resumed at 6945 and showed the finished "Optimal Path" diagram for 8 frames before Notebook's own cut to blank, an orphan beat caught on the guard strip; fixed with `video_from=6952, video_end=8194` (the hands illustration's last frame holds 7 frames before the close) |

Density: compact for all five (card body reads at full view on the 1280×720 frame; state sheets `states-*.jpg`). Full-view open:
Board 1 whole span; strengths 4.8 / 5.3 / 6.2 / 5.9 s before the first ring. Ring geometry is the section boundary (label + text)
16 px inside the card rails for why-it-fits; label + paragraph above the divider for what-it-does; the bullet row including its dot
for examples; the banner ring traces the gold banner edge to edge. Colors are each board's locked pill accent; banners neutral purple.
Rings are drawn post-crop at 5 px (`ken_burns_path.py`); Notebook's yellow example washes, arrows and corner brackets never appear.

**Longest unbroken board run (rule 8b):** Reshape → Problems, 1888–7095 = 173.6 s with no Notebook scene between. The roll's only
drawings inside that stretch are the takeaway diagrams (Raw Material → Useful Form at 96.6, the possibilities tree at 137.0) and they
animate in from a blank canvas over the takeaway lines, so none could be re-timed under an intro or item without showing a blank or
half-drawn frame; the stock photograph at 3:04 (highlighted page) is covered by the Find board. Notebook spans kept: 0–11.6 (Execution
Gap graphics), 53.8–60.9 (four-shapes drawing), 231.5–272.9 (Optimal Path, Core Capabilities/Vast Exposure, form-vs-fact diagrams,
hands-on-tablet illustration). No photographs ship: the 0:48 pen and 4:28 hands are drawn illustrations. David can pull any of it back.

## Verification (ship checklist)

Run three times: on the first render (which surfaced the Problems-exit orphan beat), on the rebuilt file (11:27, handed over), and
on the 12:05 rebuild that added the opener hold and the illustration camera walk after David's notes. The numbers below hold for
the 12:05 file. Opener hold verified by decode: max frame-to-frame delta 0.24 across output frames 160–377 (a static frame),
`opener-walk-sheet.jpg` shows the hold, the walk's five windows, and the full-board ending. Guard strip at f7125: last board frame → blank
canvas, the Core Capabilities draw-in following; at f8397: hands illustration → close board directly.

1. Decoded frame count 8783 = plan; audio 292.779 s vs 292.767 planned (one AAC frame of padding). Each leg decoded its span exactly.
2. `transition_guard.py` passed all 8 declared boundaries (378, 1645, 1888, 3164, 4383, 5768, 7125, 8397); `boundary-pairs.jpg`
   shows the last frame before and first frame after each: every first frame is already the destination (board, drawing, or close).
3. Pauses measured above.
4. Settled ring frames inspected (`state-*-NNNN.jpg`, `states-*.jpg`): correct section each time, complete text inside, nothing clipped.
5. Density and full-view open confirmed by frame (`state-*-0000.jpg`).
6. Corner mark: 1398 frames paper-cloned, 405 inpainted, 0 declined; `corner-check.jpg` samples every 300th kept frame, no mark.
7. Standard close from output frame 8397: 48-frame hold, 150-frame push to 1.2×, settle; `last-frame.jpg` is the close board.
   Copy taken from CLOSE_BOARDS[whatitdoesbest] by `make_close_board.py`.

**Not auditioned by ear.** Transcripts and the energy profile do not certify the splice. David should listen to:
- 285.6–288.4: "…better than others." → breath → "Can try is not built for." (roll 2 voice under roll 1's).
- The seven pause seams listed above (room tone tiled from the roll's own floor).
- 236.3–238.0: leaving the Problems board onto the engine diagram under "The reason AI is so capable…".

Left undone: none within scope. Optional follow-up if David wants the four takeaway lines verbatim: roll 2 speaks them at 1:30.5, 1:48.2,
2:04.8, 2:20.0, each a mid-video graft (four more seams); not built.
