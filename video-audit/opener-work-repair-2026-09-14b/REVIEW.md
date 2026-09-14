# Work With AI opener v3: review candidate (2026-09-14 PM, EDIT-SPEC build from roll 4)

**Candidate:** `videos/opener-work-v3.mp4` (2:51.6, 5149 frames, 30 fps). Supersedes the v2 candidate (roll 2 + donor, built 12:36).
**Live video and lesson unchanged** (`videos/opener-work.mp4`, `lessons/Opener-Work.md`, the three boards and the donor roll
hash-verified after the render). **Build:** `scripts/video/build_opener_work_4_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration status:** roll 4 was REROLL on the verbatim refrain and close (`video-audit/opener-work-comparison-2026-09-14b/REVIEW.md`),
the fifth roll to decline them; David's call 2026-09-14 ("Yes. Build it."): stop rolling, build from roll 4 with the donor close and the two
cuts below. The refrain stays roll 4's paraphrase, spoken over the refrain board with each line ringed as it is paraphrased.

## Base, donor, audio

- Base: `Prompts/opener-work-4.mp4` (3:08). Two cuts, approved: 24.45–35.0 ("Real utility requires you to take the lead. The model needs
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
| What Makes AI Use Good? (`lessons/opener-work-1-refrain.jpg`, compact, still) | 0–577 | frame 0, replacing Notebook's render of the same card | gold rings per line at the paraphrase: "Don't just ask. Aim." at "You aim your requests" 6.12; "Don't just copy. Check." at "you verify the output" 7.48; "Don't just use AI. Work with it." at "you treat it as a collaboration" 9.12; the closing line at "The final line captures the central goal" 11.00 | Notebook's cut (18.23) to blank canvas |
| Same Tool. Different Results. (faces; not uploaded) | 1410–1779 | Notebook's cut 55.53, "The hardware in their hands never changed" | camera walk: full → the two photo panels at "The same principle applies to AI" (57.44) → full at "…is what turns a confusing response into a sharp, professional result" (62.36); Notebook's title card, phones-and-sandwich and blurry-vs-crisp drawings stay before it | Notebook's cut (66.83) to its map render, replaced |
| Work With AI section map (compact, still), two legs | 1779–4080, 4282–4796 | "To build those mechanics, we use a three-part roadmap" (66.90) | Know What It's For at "Step one is knowing what it's for" 72.70 (purple); Use It Well at "use it well" 105.06 (blue); Think Before You Trust at 134.70 (teal); break to Notebook's VERIFY ACCURACY card 143.53–150.27 under "independently verify the factual accuracy…"; back ringed; banner at "As the bottom of our roadmap shows" 161.78 | the cut after "…how you apply the tool." (167.4) |

Longest unbroken board run: the map's first leg, 76.7 s (66.9–143.5). The only Notebook drawings inside the map span are its invented
small-print diagrams (system architectures, tool selection, tool mismatch, model perception, precision aim, evaluation) and the VERIFY
ACCURACY card; the card is used, the diagrams are not. Notebook spans kept: 18.2–24.45 (engine-core diagram), 35.0–55.5 (title card,
phones and sandwich, blurry vs crisp). No photographs.

## Verification (ship checklist)

Run on the 18:44 render.

1. Decoded frames 5149 = plan; audio 171.648 s (one AAC frame over plan). Each leg decoded its span exactly.
2. `transition_guard.py` passed all 7 declared boundaries (577, 1410, 1779, 4080, 4282, 4796, 4826); `boundary-pairs.jpg` inspected.
3. Pauses on the final file (silencedetect −35 dB): 17.86–19.35, 25.32–26.69, 57.84–59.39, 159.70–161.06; close hold 167.46–171.65.
4. Settled ring frames inspected (`states-refrain.jpg`, `states-map.jpg`, `states-map-b.jpg`): the right line or row each time, complete
   inside the ring; banner edge to edge. Same Tool walk keyframes inspected (`preview/same-tool/`).
5. Joins re-transcribed on the final file: "…which AI scales up and amplifies." 17.12 → "You've seen the tool's capabilities" 19.24;
   "…how you actually operate it." 24.92 → "Here's…" 26.60; "…a sharp, professional result." 57.26 → "To build those mechanics" 59.26;
   "…how you apply the tool." 159.14 → "Don't just use AI. Work with it." 161.08 → "AI doesn't replace your thinking. It multiplies it."
   167.24 end. Floors into each onset −60 dB or lower, no cliff.
6. Corner mark: 825 frames paper-cloned, 180 inpainted, 0 declined; `corner-check.jpg` clean.
7. Standard close from output frame 4796; `last-frame.jpg` is the close board (copy from CLOSE_BOARDS[openerworkwith]).

**Not auditioned by ear.** David should listen to 24.5–27 (the cut), 159–167.5 (the donor's two lines under the close board), and the
refrain paraphrase over the board (0–17). Live video unchanged until David ships.
