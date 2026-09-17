# Work With AI opener v5: review candidate (2026-09-14 PM, EDIT-SPEC build from roll 4)

**Candidate:** `Prompts/work-with-ai-opener-v5.mp4` (2:44.9, 4946 frames, 30 fps). v5 = v4 with one more cut (David: "Is that claim too strong? It's not
how we teach it."): 143.35–150.1, "This requires you to independently verify the factual accuracy of any claims or data the AI
provides." The course teaches question it, verify it when it matters, decide; roll 4 made verification a blanket rule. Notebook's VERIFY
ACCURACY card, drawn for that line, goes with it; "…rather than accepting it as an objective truth." now runs into "Finally, you have to
decide if the output meets the quality threshold…" with the evaluation diagram arriving on Notebook's cut. v4 (20:22) answered David's two notes on v3:
(1) the five frames of Notebook's engine diagram that flashed after the first cut's pause are gone (the picture resumes on Notebook's
cut to the Same Tool title card); (2) the section map no longer covers Notebook's diagrams for 1:00–2:40. The map now alternates with
Notebook's own diagrams exactly on Notebook's cuts, our board where Notebook showed its board render, Notebook's diagrams where it
showed those: board 66.8–75.1 (intro, Know What It's For), diagrams 75.1–102.2 (system architectures, logic patterns, tool selection,
tool mismatch), board 102.2–114.6 (Use It Well), diagrams 114.6–130.8 (model perception, precision aim), board 130.8–143.5 (Think
Before You Trust), diagrams 150.1–161.7 (evaluation and verification; the VERIFY ACCURACY card left with the cut), board 161.7–167.4 (banner). Longest board
run is now 12.7 s. v3 superseded; v2 (roll 2 + donor) superseded earlier.
**Live video and lesson unchanged** (`course-assets/work-with-ai-opener/work-with-ai-opener.mp4`, `lessons/Opener-Work.md`, the three boards and the donor roll
hash-verified after the render). **Build:** `scripts/video/build_opener_work_4_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration status:** roll 4 was REROLL on the verbatim refrain and close (`video-audit/opener-work-comparison-2026-09-14b/REVIEW.md`),
the fifth roll to decline them; David's call 2026-09-14 ("Yes. Build it."): stop rolling, build from roll 4 with the donor close and the two
cuts below. The refrain stays roll 4's paraphrase, spoken over the refrain board with each line ringed as it is paraphrased.

## Base, donor, audio

- Base: `Prompts/opener-work-4.mp4` (3:08). Three cuts, approved: 143.35–150.1 (above); 24.45–35.0 ("Real utility requires you to take the lead. The model needs
  your specific intent and direction to produce anything of value, because the software cannot define the why of the work for you.",
  invented; the pause into "Here's the reality most people miss" sits at the cut) and 167.4–188 (the paraphrased close, "This banner
  sets the standard… allows your thinking to reach much further than it could alone", replaced by the donor lines).
- Donor `Prompts/close-opener-work.mp4`, +1.0 dB (roll 4 −16.8 dBFS, donor −17.8): "Don't just use AI, work with it." (frames 990–1080)
  and "AI doesn't replace your thinking, it multiplies it." (1971–2069), a 15-frame breath between them. "AI doesn't" for the page's
  "It doesn't", as accepted for v2.
- Four one-second pauses (source seams): 18.1 (refrain → "You've seen the tool's capabilities"), 24.45/35.0 (the cut → "Here's the reality
  most people miss"), 66.6 (camera story → "To build those mechanics, we use a three-part roadmap"), and before the closing lines.

## Boards (page assets)

| Board | Output frames | Arrives | Rings (spoken onset, source s) | Leaves |
| --- | --- | --- | --- | --- |
| What Makes AI Use Good? (`lessons/work-with-ai-opener-refrain.jpg`, compact, still) | 0–577 | frame 0, replacing Notebook's render of the same card | gold rings per line at the paraphrase: "Don't just ask. Aim." at "You aim your requests" 6.12; "Don't just copy. Check." at "you verify the output" 7.48; "Don't just use AI. Work with it." at "you treat it as a collaboration" 9.12; the closing line at "The final line captures the central goal" 11.00 | Notebook's cut (18.23) to blank canvas |
| Same Tool. Different Results. (faces; not uploaded) | 1410–1779 | Notebook's cut 55.53, "The hardware in their hands never changed" | camera walk: full → the two photo panels at "The same principle applies to AI" (57.44) → full at "…is what turns a confusing response into a sharp, professional result" (62.36); Notebook's title card, phones-and-sandwich and blurry-vs-crisp drawings stay before it | Notebook's cut (66.83) to its map render, replaced |
| Work With AI section map (compact, still), four legs | 1779–2027, 2841–3213, 3698–4080, 4626–4796 | "To build those mechanics, we use a three-part roadmap" (66.90) | Know What It's For at "Step one is knowing what it's for" 72.70 (purple); Use It Well at "use it well" 105.06 (blue); Think Before You Trust at 134.70 (teal); cut after "…objective truth." (143.35) and Notebook's evaluation diagram from its cut (150.27) under "Finally, you have to decide…"; banner at "As the bottom of our roadmap shows" 161.78 | the cut after "…how you apply the tool." (167.4) |

Longest unbroken board run: 12.7 s (Think Before You Trust). Notebook's diagrams inside the map section are all used, on their own cuts. Notebook spans kept: 18.2–24.45 (engine-core diagram), 35.0–55.5 (title card,
phones and sandwich, blurry vs crisp). No photographs.

## Verification (ship checklist)

Run on the 20:33 render (v5).

1. Decoded frames 4946 = plan; audio 164.885 s (one AAC frame over plan). Each leg decoded its span exactly.
2. `transition_guard.py` passed all 12 declared boundaries (577, 794, 1410, 1779, 2027, 2841, 3213, 3698, 4074, 4423, 4593, 4623);
   `boundary-pairs.jpg` inspected: every first frame after a seam is the destination.
3. Pauses on the final file (silencedetect −35 dB): 17.86–19.35, 25.32–26.69, 57.84–59.39, 152.94–154.29; close hold 160.69–164.89.
4. Settled ring frames inspected (`states-refrain.jpg`, `states-map-1..4.jpg`); Same Tool walk keyframes inspected.
5. Joins re-transcribed on the final file: the three v3/v4 joins unchanged; the new cut reads "…rather than accepting it as an objective
   truth." 134.90 → "Finally, you have to decide if the output meets the quality threshold…" 135.96, floor −68 dB in the gap, no cliff.
   Close: "…how you apply the tool." → "Don't just use AI. Work with it." → "AI doesn't replace your thinking. It multiplies it."
6. Corner mark: 2271 frames paper-cloned, 180 inpainted, 0 declined; `corner-check.jpg` clean.
7. Standard close from output frame 4593; `last-frame.jpg` is the close board.

**Not auditioned by ear.** David should listen to 24.5–27 (the first cut), 134.5–136.5 (the new cut), 152–161 (the donor's two lines), and
0–17 (the paraphrased refrain over the board). Live video unchanged until David ships.
