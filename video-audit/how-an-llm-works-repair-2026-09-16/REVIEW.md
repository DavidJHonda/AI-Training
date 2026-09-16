# How an LLM Works v6: review candidate (2026-09-16; board refresh + Learn Once callbacks + the 2:44 flash)

**Candidate:** `Prompts/how-an-llm-works-v6.mp4` (4:22.90, 7887 frames, 30 fps). v6 = v5 (the URL-bearing boards and the canonical close
in the shipped v4 assembly) plus David's two notes on v5 (2026-09-16):

1. **Learn Once callbacks.** "The Learn Once. Answer Every Word. box shows the sections… we don't refer back to it." At each of the four
   section entries the Learn Once board returns with that step ringed, from 0.2 s before the boundary pause, through the pause, and 1.5 s
   into the section's intro sentence (2.7 s in all), then the section's own board or drawing follows. No narration changes.
   - 01 Training (purple): output 1:25.4–1:28.1, into "We can see how the AI teaches itself…"; the How Training Works board then arrives
     1.5 s later than in v5 (its first ring, Read, is at 3:01 source, unaffected).
   - 02 Patterns (purple): 2:10.9–2:13.6, into "If I say peanut butter and blank…"; the Patterns board arrives 1.5 s later, its first ring
     popping as it arrives.
   - 03 Probability (amber): 2:43.9–2:46.6, into "This chart illustrates the model's internal decision-making process"; six silent roll 2
     frames (170.38–170.95 is silence) carry the ring up before the pause, so this boundary is 0.2 s longer than in v5. The odds-chart
     drawing then starts on Notebook's own cut (5128) and runs 1.5 s behind the audio, clamped at the span's end.
   - 04 Prediction (amber): 3:32.8–3:35.5, into "Probability handles one word at a time."; the autoregressive drawings start on 218.8 and
     run 1.5 s behind the audio, clamped at the span's end.
   Rings reuse v4's exact row rectangles for the Learn Once board (the number bubble, title, and description as one component).
2. **The 2:44 flash.** The roll 1 graft's picture ran 12 frames past roll 2's scene cut (4852) into the math-and-grammar drawing, and the
   pause held it. `graft()` now takes `video_end`; the pattern-architecture card holds from 4852 through the graft's end and the pause.

**Live video unchanged.** **Build:** `scripts/video/build_how_an_llm_works_2_review.py`. **Manifest:** `edit-manifest.json` here.
Sources as in v5 (roll 2 base, roll 1 graft line, the four course-assets boards, the canonical close; all hash-verified).

## Verification (Edit Spec section 10)

1. Decoded frames 7887 = plan (v5 7881 + the six silent frames); audio 262.912 s; each leg decoded its span exactly.
2. `transition_guard.py` passed all 12 declared boundaries (1126, 1438, 2562, 2643, 3927, 4008, 4596, 4918, 4999, 6384, 6465, 7581);
   `boundary-pairs.jpg` inspected: each callback's first frame is the ringed Learn Once board, each section's first frame after it is
   its own board or Notebook's drawing on its own cut. Frame strips across all four callbacks and the old flash region inspected: the
   pattern-architecture card holds to the pause, no math-and-grammar frames.
3. Pauses on the final file (silencedetect −35 dB): 36.07–37.66, 85.33–86.93, 130.80–132.41, 152.63–153.54 (v4's, unchanged),
   163.76–165.15, 212.64–214.24, 251.48–252.86; close hold 258.48–262.91. The four callback seams re-transcribed clean: "…every single
   answer it generates." → "We can see how the AI teaches itself…"; "…patterns it needs to function." → "If I say, peanut butter and
   blank…"; "…commonly misspell words." → "This chart illustrates…"; "…on the surrounding context." → "Probability handles one word at a time."
4. Ring states inspected (`states-map-1..4.jpg`, `states-2-learn-once.jpg`, `states-3-training.jpg`, `states-4-patterns.jpg`): the
   callback ring traces the whole step row in the board's own accent; every other ring as v4.
5. Density and full-view opens unchanged; the callbacks are returns to a board already seen whole.
6. Not auditioned by ear: the audio is v4's except the six silent frames before the Probability callback; nothing to listen for.
7. Nothing left undone in scope. Spoken callbacks ("step two") remain a reroll item if David wants them later.

**At ship:** move to `course-assets/how-an-llm-works/how-an-llm-works.mp4`, new cache key on the `aihistory` entry (currently
`20260913ship1`), duration pill unchanged (4 min).
