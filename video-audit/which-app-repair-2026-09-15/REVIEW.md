# Your Home Base (modelselection; retitled from Which App? 2026-09-15) v1: review candidate (2026-09-15, EDIT-SPEC best-of build from roll 1 + roll 2)

**Candidate:** `Prompts/your-home-base-v1.mp4` (renamed from which-app-v1 at the retitle) (3:49.5, 6885 frames, 30 fps). Roll 1 is the base; roll 2 donates the Gemini card and Board 3's
columns, per David 2026-09-15 ("Agree with delete of 'Warning tone'. And, using the Gemini narration from Roll 2. And, use the Board 3
from Roll 2."). Comparison and plan: `video-audit/which-app-comparison-2026-09-15/REVIEW.md`.
**Live video and lesson unchanged** (`course-assets/your-home-base/your-home-base.mp4`, formerly which-app.mp4, hash-verified; `lessons/which-app.md` is mid-edit for the attribution boards and
was not protected). **Build:** `scripts/video/build_which_app_review.py`. **Manifest:** `edit-manifest.json` here.
**Narration status:** roll 1 REPAIR (the leak and the filler cut here; Gemini's name and question now roll 2's, as written). Every hard
requirement met: three apps with companies, In-N-Out and McDonald's as written, each app by board name with its question as written,
any of the three can do the job, Claude requires 18, ChatGPT home base with one-deeply-beats-dabbling, the power move, Board 3 in full,
the close verbatim as the last words. Board 2's own lines ("Three workstations… Pick one and learn it deeply.") are unspoken before the
close in both rolls; the board carries them and the close speaks them.

## Base, donor, audio

- Base: `Prompts/which-app-1.mp4` (3:37). Two cuts: 2:54.6–2:56.0 "Warning tone." (a stage direction spoken aloud; silences 174.37–174.81 /
  175.68–176.23) and 1:16.1–1:19.2 "Each app brings a specific mission to your workflow." (filler with a banned word; 75.95–76.46 / 78.94–79.61,
  under Board 1). Roll 1's "Then there is Gemini." (1:55.8–1:56.6) and "Google designed Gemini to answer a practical question. How do we put AI
  inside the digital environment people already inhabit?" (2:02.7–2:09.7) are replaced by the grafts; its "ChatGPT handled ideas and
  improvements, brainstorming," leads into the Board 3 graft (roll 2's "brainstorming TRY ITs and LABs" transcribes as "triads"; not used).
- Donor: `Prompts/which-app-2.mp4`, +1.2 dB (roll 1 −17.09 dBFS median speech, roll 2 −18.31). Three audio-only grafts, all under our boards:
  1. 2:19.0–2:24.6 "Gemini takes a different approach. It acts as the AI assistant built directly into Google." → then roll 1's own "Its main
     advantage shows up when your work connects to the Google tools you already use on a daily basis." (1:57.1–2:02.4) →
  2. 2:32.0–2:38.7 "Google's guiding question focuses on integration. How do we put AI inside the tools people already use?" → roll 1 resumes
     at "Each app has distinct strengths…" (2:10.25).
  3. 4:29.9–4:48.9 "reviewing lessons, writing code, and helping edit videos. Claude handled building and design. We relied on it for writing
     code with Claude Code and styling pages with Claude Design. Finally, Gemini managed information and videos. We used it for finding current
     information and creating lesson videos with Gemini Notebook."
- Six one-second pauses (source seams): 21.4 (the hook question → the burger place), 46.6 (→ "The big three AI apps work the same way"),
  72.95 (→ "This board breaks down…"), 137.85 (overlap → "Because of this overlap…", under Board 1), 155.5 (→ "For this course, ChatGPT is
  your designated home base"), 185.5 (→ "This graphic shows how we used the big three"), and before the closing lines.

## Boards (page assets)

| Board | Output frames | Arrives | Rings / treatment | Leaves |
| --- | --- | --- | --- | --- |
| The Big Three, Side by Side (`illustrations/which-app-big-three-v2.jpg`, compact, two legs) | 2278–4362 | "This board breaks down the big three side by side" (source 72.95, 7 frames before Notebook's render cut 73.17) | green ring on the ChatGPT column at "We can think of ChatGPT as the anything box" 79.56; purple on Claude at "Claude acts as the thinking partner" 98.64; blue on Gemini at the grafted "Gemini takes a different approach", held through its question; bare for "Each app has distinct strengths… any of the three tools will do the job for most tasks" | 141.85, for Notebook's finished "Big Three AI models" cards (blank at Notebook's own cut 137.97, complete by 141.3) |
| Pick a Home Base. Learn It Deeply. (`illustrations/which-app-pick-home-base-v2.jpg`, faces; not uploaded; camera walk, no rings) | 4801–5167 | "For this course, ChatGPT is your designated home base" 155.5, over Notebook's stand-in diagram | walk to the ChatGPT desk and lightbox at "Learn it deeply, its settings, its features, its quirks" 158.84; back to full at "Knowing one app thoroughly beats shallow dabbling in all three" 162.28; full through "Later, you can try a specific strategy." | 167.7, for Notebook's primary-model / secondary-verifier diagram from its labelled state (5040) under "Ask a second app the exact same question"; its arrows, bullets, disagreement flag and "consensus does not equal truth" draw with the lines |
| How We Used the Big Three (`illustrations/which-app-how-we-used-big-three-v2.jpg`, compact) | 5689–6558 | "This graphic shows how we used the big three" 185.5 (0.7 s before Notebook's render cut 186.23) | green ring on ChatGPT at "ChatGPT handled ideas and improvements" 190.64; purple on Claude at the grafted "Claude handled building and design"; blue on Gemini at the grafted "Finally, Gemini managed information and videos" | the pause and the close |

Notebook spans kept: 0–72.95 (person at laptop, Big Three ecosystem cards, THE IMPACT card, burger philosophies diagram, shared-patterns
chips, three monitors, peeled UI), 141.85–155.5 (Big Three AI models cards, age 18 badge on Claude), 167.7–185.5 (verifier diagram).
Longest unbroken board run: Big Three, 69 s (its narration is the board's own three columns; Notebook drew nothing else inside it).
No photographs beyond the two-student board.

## Verification (ship checklist)

Run on the 10:14 render.

1. Decoded frames 6885 = plan; audio 229.504 s (one AAC frame over plan). Each leg decoded its span exactly.
2. `transition_guard.py` passed all 7 declared boundaries (2278, 3624, 4362, 4801, 5167, 5689, 6558); `boundary-pairs.jpg` inspected: the
   board's first frame on each arrival, Notebook's finished cards at 4362, its labelled verifier boxes at 5167, the close board at 6558.
3. Pauses on the final file (silencedetect −35 dB): 21.10–22.74, 47.34–48.87, 74.74–76.22, 140.20–141.55, 158.85–160.20, 188.49–190.31,
   217.56–218.92; close hold 224.74–229.50.
4. Ring frames inspected on the output (`wa-out-strip`): each column ringed at its onset, the Gemini ring carried across the two legs, the
   board bare under the overlap sentence; the camera walk lands on the ChatGPT desk and lightbox and returns to the full board.
5. Joins re-transcribed on the final file (small.en): "…core philosophy." → pause → "This board breaks down the big three, side by side." →
   "We can think of ChatGPT as the anything…" (the filler gone); "…we can actually trust." → "Gemini takes a different approach. It acts as the
   AI assistant built directly into Google." → "Its main advantage shows up when your work connects to the Google tools you already use on a
   daily basis." → "Google's guiding question focuses on integration. How do we put AI inside the tools people already use?" → "Each app has
   distinct strengths…"; "…a completely different approach to the problem." → "If the two apps disagree…" ("Warning tone." gone); "ChatGPT
   handled ideas and improvements, brainstorming, reviewing lessons, writing code, and helping edit videos. Claude handled building and
   design… with Gemini Notebook." → pause → "Pick a home base. Learn it deeply. The skills transfer. The app is just where you practice
   them." Floors into each onset −47 dB or lower.
6. Corner mark: 2777 frames paper-cloned, 312 inpainted, 0 declined; `corner-check.jpg` clean.
7. Standard close from output frame 6558; `last-frame.jpg` is the close board (copy from CLOSE_BOARDS[modelselection]).

**Not auditioned by ear.** David should listen to 1:53–2:13 (the Gemini grafts in and out; roll 2's voice level against roll 1's), 2:57–2:59
(the "Warning tone." cut), 3:17–3:20 ("brainstorming, reviewing lessons": roll 1 into roll 2 mid-list), and 3:21–3:37 (roll 2's three
"Claude" mentions).
**At ship:** move to `course-assets/your-home-base/your-home-base.mp4`, new cache key on the `modelselection` entry, duration pill 4 min (3:50). Board illustrations and kit files still carry the which-app slug (re-slug after the attribution pass lands). Live video unchanged until then.
