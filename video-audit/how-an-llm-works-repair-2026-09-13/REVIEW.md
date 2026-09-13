# How an LLM Works v4 (2026-09-13) — candidate review kit

Source: Prompts/how-an-llm-works-2.mp4 (roll 2, REPAIR under NARRATION-REVIEW; comparison in
video-audit/how-an-llm-works-comparison-2026-09-13/REVIEW.md). Candidate: videos/how-an-llm-works-v4.mp4 (v3 superseded: roll 2's garbled "architecture" sentence at 2:30-2:42 source is replaced, sound only, by roll 1's "Over billions of examples, the system picks up more than just simple phrases. It learns how humans structure explanations, solve problems, and even commonly misspell words." under roll 2's own pattern-engine and math-and-grammar drawings; v2 superseded: it cut to Notebook's pattern-engine drawing during its fade-in from blank paper; the patterns board now holds through that second).
Build: scripts/video/build_how_an_llm_works_2_review.py. Live file videos/how-an-llm-works.mp4 untouched.

## Edit
- Two narration cuts (in measured silence): 2:41.5–2:50.93 ("matching and retrieving… not demonstrating genuine
  comprehension"; "retrieving" contradicted the lesson), resuming on Notebook's chart cut; 4:16.5–4:26.4 ("An LLM is not
  magic…"), which was Notebook narrating a STALE close-board copy it had been given (lessons/how-an-llm-works-5-close.jpg
  carried an old close; every Start Smarter and Embrace close copy was regenerated from the page the same day).
- Six room-tone pauses at new ideas: into how it turns words into an answer (0:36), into training (1:25), into patterns
  (2:09), into probability (the first cut), into prediction (3:39), before the close (the second cut). None inside a board.
- Board 1, What's an LLM (compact, still): the lesson opens on it; Large / Language / Model ringed blue / teal / purple
  as spoken; banner ringed at "the apps you interact with… the LLM is the underlying engine".
- Board 2, Learn Once. Answer Every Word (compact, still): from Notebook's own board cut with the intro "the LLM operates in
  two distinct phases"; 01 Training and 02 Patterns ringed purple, 03 Probability and 04 Prediction amber, banner ringed at
  "The model learns its patterns once…".
- Board 3, How Training Works (compact strip, still): from "We can see how the AI teaches itself…"; Read / Guess / Check /
  Adjust ringed at "Step one" through "Step four"; banner ringed at "repeats this exact read, guess, check, and adjust cycle".
- Board 4, How AI Learns Patterns (compact, still): from "If I say peanut butter and blank…"; One Familiar Pattern ringed
  at once, Patterns Are Everywhere at "The AI absorbs all of our common structural patterns"; leaves at Notebook's own cut
  to its pattern-engine drawing.
- Notebook spans kept (8b): core-processing engine drawing 0:37–0:47; pattern engine and math-and-grammar drawings
  2:30–2:41; the animated odds chart 2:51–3:30 (bars grow to the page's exact numbers, 41/27/16/5 and 54/16/9/2; the
  intermediate values are the animation, not errors); network drawing 3:30–3:39; autoregressive and phone-loop drawings
  3:39–4:16. No photographs. Longest unbroken board run: 45s (learn-once into training, separated by a pause). No interleaving needed.
- Standard close from the second cut. Gemini corner mark cleaned on every kept source frame; corner-check.jpg.

## Ship checklist
- transition_guard: all boundaries pass (transitions/). Frame count decoded = manifest total.
- Board states: states-*.jpg. Output contact sheets and transcript: bundle/how-an-llm-works-v4/.

## Listen (David's ear)
- The audio graft (output ~2:33 to ~2:44, roll 1's voice under roll 2's drawings), the two cut seams (~2:43 and ~4:14); "for" at ~3:47 (the transcript hears "four").

## Shipped
2026-09-13: v4 approved ("ship it"); copied to videos/how-an-llm-works.mp4, cache key 20260913ship1, candidate deleted, both rolls kept. Receipt: shipping-receipt.json. The 16 regenerated close-board copies (Start Smarter + Embrace) ship in the same commit.
