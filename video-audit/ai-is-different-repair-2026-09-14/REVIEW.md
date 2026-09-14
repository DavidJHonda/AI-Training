# AI Is Different v5: review candidate (2026-09-14, EDIT-SPEC build, first build under the beat-by-beat rule)

**Candidate:** `videos/ai-is-different-v5.mp4` (5:33.2, 9996 frames, 30 fps). v5 = v4 with one visual fix (David, "4:06. There's a flash
of a graphic"): after the pause that follows "normal software wins.", the picture now resumes at Notebook's own cut to blank canvas
(source 7460) instead of at the audio seam, so its pattern-recognition diagram no longer shows for 8 frames; the finished
rule-vs-probabilistic diagram holds its last frame for 8 frames before the Kryptonite board. v4 = v3 plus the best-of graft: roll 2's Kryptonite stories
and banner line (roll 2 162.40–200.40, +1.1 dB) replace roll 1's thin version (265.5–281.1) under the AI's Kryptonite board, whose rings
follow roll 2's onsets; roll 1's intro "This graphic outlines severe risks from this lack of control." stays, with a 0.3 s breath before
the graft. Plan: `video-audit/ai-is-different-comparison-2026-09-14/REVIEW.md`, "Best-of plan". v2 (13:24, 5:26.3) was reviewed by
David; v3 (13:59, 5:11.5) applied his four notes: (1) the Rules vs. Patterns ask rings no longer cut into the labels and values (rows now start 12 px left of the text);
(2) the Structured board rings the AI card's photo, the two of them at the glowing box, from "When writing this very lesson" (207.20)
through the legal-pad story; (3) cut "AI is the necessary tool for messy, open-ended jobs where writing strict rules is impossible."
(242.04–247.32, already covered) with the cut landing after "normal software wins." and before the narrator's inhale; (4) the inserted
pause into guardrails is gone (the roll's own 0.76 s gap stays), and both summary sentences after "harmless one." are cut (302.66–313.22),
so the close board arrives at the trough after "one." (302.55) with a one-second pause and then the donor lines. The v2 details below
are updated where they changed. **Live video and lesson unchanged** (`videos/ai-is-different.mp4`,
`lessons/ai-is-different.md`, the five board assets and the donor roll hash-verified after the render).
**Build:** `scripts/video/build_ai_is_different_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration status:** roll 1 was REROLL under `video-audit/ai-is-different-comparison-2026-09-14/REVIEW.md` for the unspoken close and two
missing beats. David's call 2026-09-14: build roll 1 with the donor close ("The donor was only for the Closing Message… Maybe we just
need the roll?"). The two beats stay unspoken and are accepted: the Superman-and-Kryptonite setup ("A human can hold Kryptonite… AI has
its own Kryptonite. It's not fatal, but you need to be aware of it.") and "That difference shows up everywhere: how each one solves a
problem, how it reaches an answer, how it fails, and whether you can even trace why." The word superpowers is spoken only in the close.

## Base, donor, audio

- Base: `Prompts/ai-is-different-1.mp4` (5:17). Two narration cuts (David, on v2): "AI is the necessary tool for messy, open-ended jobs
  where writing strict rules is impossible." (241.0–248.4 source, the cut after "wins." at 241.0 and before the inhale; the Kryptonite
  pause follows) and everything after "…a completely harmless one." (302.55–313.22: "The architecture that allows AI to understand our
  world also makes its behavior unpredictable." and "These new capabilities are fundamentally linked to the risks we've just seen.").
- Donor `Prompts/close-ai-is-different.mp4`: "AI's foundation gives it new superpowers. Those superpowers come with kryptonite."
  38.40–43.13, both lines in one breath; span frames 1146–1308 (38.20–43.60) between −67 / −66 dB troughs. Gain −0.75 dB (roll 1 speech
  −18.2 dBFS, donor −17.5). The donor's other requested lines (Kryptonite paragraph, "no one can fully predict") were not spoken by it.
- Seven one-second pauses at idea boundaries (source seams): 13.5 (hook → how standard software is created), 54.45 (→ AI is based on
  patterns), 127.7 (→ the practical test), 176.9 (→ structured vs unstructured), 226.1 (→ the right tool), 241.0/248.4 (the cut, → AI's
  Kryptonite), and before the closing lines. None inside a board. No pause into guardrails (David: the roll's own gap is enough).

## Boards (page assets, byte-identical to `lessons/`)

| Board | Output frames | Arrives | Rings (spoken onset, source s) | Leaves |
| --- | --- | --- | --- | --- |
| Rules Look Like This (compact) | 871–1702 | Notebook's own cut into its render (28.03), "This flowchart shows…" | User enters password 31.54 (neutral), IF 35.80 (blue), THEN 37.12 (green), ELSE 39.78 (red), banner 44.34 "Because a programmer wrote every single step… same result every time" | Notebook's cut to the IF-THEN-ELSE X (54.73); the audio pause sits at 54.45 inside the leg |
| Learn Once. Answer Every Word. (compact) | 1906–2974 | Notebook's cut (61.53), "This infographic illustrates the new process" | 01 Training 68.54, 02 Patterns 73.48 (purple), Patterns power every answer 80.82 (neutral), 03 Probability 86.10, 04 Prediction 90.56 (amber); banner not spoken, not ringed | Notebook's cut to the cookbook robot (97.13) |
| Rules vs. Patterns (faces; not uploaded; dense) | 4020–5437 | "Let's ask a computer to recommend the best game for a new PS5" (131.06), over Notebook's list drawing and its invented engine diagrams | question card 132.34; Normal Software card 137.98 and its three asks 143.22 / 146.70 / 149.72 (blue); AI Software card 152.80 and its asks 155.40 / 159.22 / 165.36 (purple); pull back 168.0; banner 168.88 "Rules force the computer to repeat…" | Notebook's cut to the keyboard monitor (177.23); pause at 176.9 inside the leg |
| Structured vs. Unstructured Data (faces; not uploaded; dense) | 5865–6943 | "AI, however, does not need neat rows and columns" (191.70), over Notebook's invented vector and legal-pad diagrams | AI Software: the idea 191.70, input and output 197.74, its photo (the two of them at the glowing box) 207.20 through the legal-pad story (purple); pull back 221.9; banner 222.68 "Being able to process a mess is a powerful ability" | Notebook's cut to brain vs calculator (226.43); pause at 226.1 inside the leg |
| AI's Kryptonite (compact, no push) | 7816–9068 | Notebook's cut (261.93), roll 1's "This graphic outlines severe risks from this lack of control." | roll 2 audio from 264.3 output: Scams That Scale at "One risk is the ability to scale scams" (blue), Deepfakes at "There is also the issue of deep fakes" (purple), Confident but Wrong at "We also see instances where the model is confident but wrong" (teal), banner at "These errors happen because trained behavior is much harder to predict or lock down" | roll 1 resumes in its own quiet before "To defend against these threats" with the phone drawing start-cloned (282.0–282.5), then Notebook's phone scene |

Kept Notebook scenes: opening standard-vs-AI diagrams, code monitor, IF-THEN-ELSE card, the crossed-out IF-THEN-ELSE, cookbook robot,
pasta plates, chef brain, plated dish, explicit-instructions arrow, next-state diagram, PS5 controller, RIGID/DYNAMIC (10 frames), keyboard
monitor, GPA spreadsheet, brain vs calculator, rule-based and pattern-recognition diagrams, rule-vs-probabilistic diagram (draws in
from blank after its cut), phone guardrails, guardrail diagrams. Longest unbroken board run: Rules vs. Patterns, 47 s. No photographs.
Not used: Notebook's spreadsheet-drawing-to-board transition text cards, receipt/vector diagram, legal-pad diagrams, torn-notes drawing
(all under the Structured board), and its "Deterministic Execution" diagram (under the Rules banner line).

## Verification (ship checklist)

Run on the 14:48 render (v5); numbers unchanged from v4 except the added seam.

1. Decoded frames 9996 = plan; audio 333.205 s vs 333.200 planned (one AAC frame of padding). Each leg decoded its span exactly.
2. `transition_guard.py` passed all 13 declared boundaries (871, 1702, 1906, 2974, 4020, 5437, 5865, 6943, 7410, 7816, 9068, 9684, 9714);
   the new 7410 strip: pause-held rule-based diagram → blank canvas (Notebook's own scene start) → draw-in;
   `boundary-pairs.jpg` inspected: the first frame after each seam is already the destination (the graft end lands on the start-cloned
   phone drawing, the close on the app board).
3. Pauses on the final file (silencedetect −35 dB): 13.27–15.15, 55.25–56.81, 129.55–130.93, 179.58–181.17, 229.98–231.36,
   246.00–247.37 (after "normal software wins."), 322.70–323.99 (before the closing lines); close hold 328.78–333.21. No inserted
   pause into guardrails. The added breath before the graft measures 0.5 s quiet (263.96–264.48), under the pause threshold by design.
4. Settled ring frames inspected (`states-*.jpg`): rules boxes; Learn Once items; the question card, both software cards and their ask
   rows clear of the text; the AI card paragraphs and its photo; the three Kryptonite cards and the banner at roll 2's onsets.
5. Density confirmed by frame: rules, learn, kryptonite compact (kryptonite held still, no push, because it spans the graft); rvp and
   structured dense, each opening on the complete unmarked board.
6. Joins re-listened (small.en on the final file): "…from this lack of control." 263.44 → "One risk is the ability to scale scams" 264.60;
   "…than a simple written rule." 301.44 → "To defend against these threats" 302.82; "…a completely harmless one." 322.32 → "AI's
   foundation gives it new superpowers." 323.96 → "Those superpowers come with Kryptonite." 328.18 end. Seam profiles at all three:
   floor −60 to −68 dB into each onset, no cliff; roll 2 at +1.1 dB sits within 0.3 dB of roll 1's speech level.
7. Corner mark: 3181 frames paper-cloned, 767 inpainted, 0 declined; `corner-check.jpg` clean on every sampled Notebook frame.
8. Standard close from output frame 9684 (the cut after "harmless one."), 48-frame hold, push to 1.2×, settle; `last-frame.jpg` is the
   close board (copy from CLOSE_BOARDS[aivscode]).

**Not auditioned by ear.** David should listen to 263–265 (roll 1 into roll 2 under the Kryptonite board), 301–303.5 (roll 2 back
into roll 1 before "To defend"), 245.5–248 (the cut after "wins."), and 322–329 (the close). Left undone: none within scope; the two
accepted missing beats (Superman/Kryptonite setup, "the difference shows up everywhere") remain unspoken in both rolls. Live video and
lesson unchanged.
