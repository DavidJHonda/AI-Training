# Beyond the Average (whybother; formerly Does School Matter?) v5: review candidate (2026-09-14 PM, EDIT-SPEC build)

**Candidate:** `videos/beyond-the-average-v5.mp4` (2:51.4, 5143 frames, 30 fps). v5 = v4 with the closing audio carried to 202.0 (v4 ended
it at 201.5 and clipped the last word; "average" runs to 201.68 at −45 dB, David 2026-09-14). v4 = v3 with a third cut, David's note on v3 ("1:22 to
1:34. It feels like we can delete this video."): source 100.9–113.17, "School forces you to learn the foundational mechanics of how things
work. Instead of receiving a finished summary, you investigate the individual pieces to understand why they fit together. It provides a
sandbox for active practice." Notebook's busy foundational-mechanics diagram (four boxes, WHY hub, testing frame), drawn for that
passage, goes with it. The narration now runs "School provides the structured time and space required to develop those assets." →
pause → "You write essays, solve difficult math equations, build physical objects, and navigate the complexities of collaborating with
real people.", and the picture resumes on Notebook's own cut to the pen writing an essay. The lesson's "Learn how things work" line is
now unspoken by the video (accepted 2026-09-14). v3 answered David's note on v2 ("We are showing the
illustration from :55 to 1:23. That's too long."): the Same Tool board now holds only under roll 2's grafted line (0:55.3–1:04.9, 9.6 s);
when roll 1 resumes at "In a future where everyone has the same software…" (1:04.9) the picture is roll 1's own synced diagrams, kept
from the frame it resumes on: "The New Average" two-student stacks (fully drawn), morphing on Notebook's own animation into "The
Differentiation Gap" with the value-delta arrow under the question "what specifically takes you beyond the new average and makes you
more valuable than the tool?", dissolving to "Where Real Value Is Built / School: structured time & space" whose four cards draw in
under "That extra value comes from the internal knowledge and skills you build…" and sit fully drawn under "School provides the
structured time and space required to develop those assets." (1:04.9–1:21.7, to the first cut). No new audio; the sound is v2's.
Note for David: Notebook's diagram labels the two students "relying solely on tool" vs "using tool as foundation" (small type); that is
the picture of what you add on top of the same output, not the one-student-beats-the-other narration that v1 cut. v2 answered David's two notes on v1: (1) 0:55–1:16 was
roll 1 saying one student beats the other ("One of these students takes the work further… build something superior on top of it"), not
the lesson's framing; roll 1's 53.3–72.75 is replaced by roll 2's line under the board, "The difference is what you add. AI provides raw
material, but your unique subject knowledge and practiced problem-solving take the work further." (roll 2 55.10–64.3, −0.95 dB),
and the board holds still, full, banner visible (no camera walk); (2) the tall What to Start Building Today board's banner sat on the
frame's bottom edge and the opening push clipped it; `editspec_build.compose` now gives tall boards a 4% stage margin above and below,
and dense boards open static (no push on a full board). v1–v4 superseded. Named for the lesson's new title (David retitled the
lesson 2026-09-14; the page's `whybother` entry and its board assets still carry the old slug, to be re-slugged at ship).
**Live video and lesson unchanged** (`videos/does-school-matter.mp4`, `lessons/does-school-matter.md`, both board assets hash-verified).
**Build:** `scripts/video/build_beyond_the_average_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration status:** roll 1 of the second pair (`video-audit/does-school-matter-comparison-2026-09-14b/REVIEW.md`): every beat taught,
Board 2 read in full, close verbatim; its one hard-requirement miss, the Same Tool board line "The tool may be the same. What you
bring to it is yours.", is unspoken in all four rolls and accepted as the board's own text (the board is on screen while roll 2's line, "The difference
is what you add… take the work further", carries its meaning).

## Base, audio

- Base: `Prompts/does-school-matter-1.mp4` (3:25). One graft (roll 2's line above, under the Same Tool board). Three cuts approved by David 2026-09-14:
  1. 89.55–101.0: "Education is a process designed to build the human differentiators that an algorithm cannot replace. It shifts the
     focus away from simply finding the right answer and toward the capacity to improve upon it." (David: the second sentence can't
     stand alone; both go.) Extended in v4 through 113.17: "School forces you to learn the foundational mechanics… It provides a sandbox
     for active practice." The pause into "You write essays…" sits here; the picture resumes on Notebook's cut (1:53.17) to the pen.
  2. 126.9–132.0: "You develop a level of specialized expertise that a generalized AI lacks." No pause; the microscope drawing
     continues across the cut.
- Four one-second pauses (source seams): 13.8 (hook → "Imagine your future dream job"), 53.3 (→ "Consider two students"), the first
  cut, and 194.0 (before the closing lines, which the roll speaks verbatim).

## Boards (page assets)

| Board | Output frames | Arrives | Treatment | Leaves |
| --- | --- | --- | --- | --- |
| Same Tool. Different Advantage. (`illustrations/does-school-matter-same-tool-v1.jpg`, faces; not uploaded) | 1659–1947 | after the pause at 53.3, with roll 2's "The difference is what you add…" | full board, still, banner visible | as roll 1 resumes at "In a future where everyone has the same software…" (72.75); Notebook's New Average → Differentiation Gap → Where Real Value Is Built diagrams carry roll 1 to the first cut (89.55) |
| What to Start Building Today (`illustrations/does-school-matter-future-v3.jpg`, 2x2, dense; canvas with a 4% vertical margin) | 3172–4753 | "This roadmap shows the four specific pillars" (141.34); Notebook's cut to its render (141.97) inside the leg | dive per card as named: Deep Subject Knowledge 148.88 (purple), Strong Skills 157.84 (blue), AI Fluency 168.40 (teal), People Skills 178.24 (amber); pull back 187.6; banner at "By focusing on these four pillars, school helps you build what takes you beyond the new average" (188.16) | 194.0, then the pause and the close |

Notebook spans kept: 0–53.3 (laptop thinker, phone with code, classroom, developer and coworker diagram, data center, hand writing
"AI Generated"), 113.17–141.3 (pen writing an essay, calculus page, the meeting, microscope, "Smarter than the tool"
card; the brain-and-page and foundational-mechanics diagrams left with the cuts), 72.75–89.55 (the New Average / Differentiation Gap /
Where Real Value Is Built diagrams, roll 1's own drawings for these lines).
Notebook's 53.6–72.75 drawings (the New Average diagram building) sit under the board and roll 2's line. Longest unbroken
board run: What to Start Building Today, 52.7 s (Notebook drew nothing inside it); Same Tool 9.6 s. No photographs.

## Verification (ship checklist)

Run on the 21:47 render (v5).

1. Decoded frames 5143 = plan; audio 171.435 s (one AAC frame over plan). Each leg decoded its span exactly.
2. `transition_guard.py` passed all 6 declared boundaries (1659, 1947, 2481, 2893, 3172, 4783); `boundary-pairs.jpg` inspected: 2481 is
   Notebook's pen drawing, first frame after its cut; 1946 is
   the full board, 1947 the fully drawn New Average diagram; a frame strip of 1947–2451 shows the three diagram states arriving on
   Notebook's own morphs, none entered blank or mid-draw.
3. Pauses on the final file (silencedetect −35 dB): 13.48–15.15, 54.07–55.67, 81.55–82.77, 158.37–159.66; close hold 167.11–171.43 (speech runs to 167.11 at −45 dB; the word is whole).
4. Settled ring frames inspected (`states-future.jpg`): the board opens full with the banner clear of the frame edge, each dive lands on
   the named card, banner edge to edge at the end; `states-same-tool.jpg`: full board, still.
4b. Protected files (live video, lesson text, roll 2, both boards) hash-verified unchanged after the render.
5. Joins re-transcribed on the final file: "…find a way to take it further." 53.64 → pause → "The difference is what you add. AI provides
   raw material, but your unique subject knowledge and practiced problem-solving take the work further." 55.70–64.0 → "In a future where
   everyone has the same software…" 65.06; "…develop those assets." 80.90 → pause → "You write essays, solve difficult math equations…"
   82.66; "…go deep into it." 95.96 → "Technology will change…" 96.80; close verbatim 158.50–167.11. Floors into each onset −50 dB or lower, no cliff.
6. Corner mark: 1625 frames paper-cloned, 1169 inpainted, 0 declined; `corner-check.jpg` clean.
7. Standard close from output frame 4783; `last-frame.jpg` is the close board (copy from CLOSE_BOARDS[whybother]).

**Not auditioned by ear.** David should listen to 53.5–66 (roll 2's line in and out under the board), 80.5–83.5 (the extended cut 1, the
pause, and "You write essays"), and 95.5–97 (cut 2).
**At ship:** move to `videos/beyond-the-average.mp4`, point the `whybother` entry at it with a new cache key, duration pill 3 min (2:51),
and re-slug the two board illustrations and the kit files to `beyond-the-average-*` per the naming rule (David's call on timing).
Live video unchanged until then.
