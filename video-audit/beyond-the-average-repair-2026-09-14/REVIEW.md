# Beyond the Average (whybother; formerly Does School Matter?) v1: review candidate (2026-09-14 PM, EDIT-SPEC build)

**Candidate:** `videos/beyond-the-average-v1.mp4` (3:12.9, 5788 frames, 30 fps), named for the lesson's new title (David retitled the
lesson 2026-09-14; the page's `whybother` entry and its board assets still carry the old slug, to be re-slugged at ship).
**Live video and lesson unchanged** (`videos/does-school-matter.mp4`, `lessons/does-school-matter.md`, both board assets hash-verified).
**Build:** `scripts/video/build_beyond_the_average_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration status:** roll 1 of the second pair (`video-audit/does-school-matter-comparison-2026-09-14b/REVIEW.md`): every beat taught,
Board 2 read in full, close verbatim; its one hard-requirement miss, the Same Tool board line "The tool may be the same. What you
bring to it is yours.", is unspoken in all four rolls and accepted as the board's own text (the board is on screen while roll 1 says
"One of these students takes the work further by applying their own knowledge and practiced skills to that baseline").

## Base, audio

- Base: `Prompts/does-school-matter-1.mp4` (3:25). No grafts. Two cuts approved by David 2026-09-14:
  1. 89.55–101.0: "Education is a process designed to build the human differentiators that an algorithm cannot replace. It shifts the
     focus away from simply finding the right answer and toward the capacity to improve upon it." (David: the second sentence can't
     stand alone; both go.) The pause into "School forces you to learn the foundational mechanics of how things work" sits here.
  2. 126.9–132.0: "You develop a level of specialized expertise that a generalized AI lacks." No pause; the microscope drawing
     continues across the cut.
- Four one-second pauses (source seams): 13.8 (hook → "Imagine your future dream job"), 53.3 (→ "Consider two students"), the first
  cut, and 194.0 (before the closing lines, which the roll speaks verbatim).

## Boards (page assets)

| Board | Output frames | Arrives | Treatment | Leaves |
| --- | --- | --- | --- | --- |
| Same Tool. Different Advantage. (`illustrations/does-school-matter-same-tool-v1.jpg`, faces; not uploaded) | 1659–2746 | "Consider two students starting with the same AI-generated answer" (53.62), over the last 9 frames of Notebook's hand-writing drawing and its "New Average" diagram | camera walk: full, dive to the second student with his bridge model and laptop at "One of these students takes the work further" (62.32), back to full at "In a future where everyone has the same software" (72.82); ends full with the banner visible through "…develop those assets." | the first cut (89.55) |
| What to Start Building Today (`illustrations/does-school-matter-future-v3.jpg`, 2x2, dense) | 3832–5413 | "This roadmap shows the four specific pillars" (141.34); Notebook's cut to its render (141.97) inside the leg | dive per card as named: Deep Subject Knowledge 148.88 (purple), Strong Skills 157.84 (blue), AI Fluency 168.40 (teal), People Skills 178.24 (amber); pull back 187.6; banner at "By focusing on these four pillars, school helps you build what takes you beyond the new average" (188.16) | 194.0, then the pause and the close |

Notebook spans kept: 0–53.3 (laptop thinker, phone with code, classroom, developer and coworker diagram, data center, hand writing
"AI Generated"), 101.0–141.3 (brain and marked-up page, engine diagrams, calculus page, the meeting, microscope, "Smarter than the tool"
card). Notebook's "New Average" and "Where real value is built" diagrams (53.6–89.4) sit under the Same Tool board. Longest unbroken
board run: What to Start Building Today, 52.7 s (Notebook drew nothing inside it). No photographs.

## Verification (ship checklist)

Run on the 20:52 render.

1. Decoded frames 5788 = plan; audio 192.939 s (one AAC frame over plan). Each leg decoded its span exactly.
2. `transition_guard.py` passed all 5 declared boundaries (1659, 2776, 3553, 3832, 5443); `boundary-pairs.jpg` inspected.
3. Pauses on the final file (silencedetect −35 dB): 13.48–15.15, 54.07–55.63, 91.39–92.53, 180.37–181.66; close hold 188.92–192.94.
4. Settled ring frames inspected (`states-future.jpg`): each dive lands on the named card, banner edge to edge. Same Tool walk
   keyframes inspected (`preview/same-tool/`): full, the second student, full.
5. Joins re-transcribed on the final file: "…required to develop those assets." 90.72 → pause → "School forces you to learn the
   foundational mechanics of how things work." 92.44; "…and you go deep into it." 117.96 → "Technology will change, but internalized
   knowledge and practiced skills belong to you permanently." 119.00; "…beyond the new average." 179.64 → pause → "The opportunity to
   learn is already in front of you. Use it to build the knowledge and skills that take you beyond the new average." 181.58–188.52.
6. Corner mark: 1486 frames paper-cloned, 1169 inpainted, 0 declined; `corner-check.jpg` clean.
7. Standard close from output frame 5443 (Notebook's own close render arrives 4 frames later, covered); `last-frame.jpg` is the close
   board (copy from CLOSE_BOARDS[whybother]).

**Not auditioned by ear.** David should listen to 90.5–93 (cut 1 and the pause) and 117.5–119.5 (cut 2, inside the microscope scene).
**At ship:** move to `videos/beyond-the-average.mp4`, point the `whybother` entry at it with a new cache key, set the duration pill to
3 min (3:13), and, per the asset-naming rule, re-slug the two board illustrations and the kit files to `beyond-the-average-*` (David's call
on timing). Live video unchanged until then.
