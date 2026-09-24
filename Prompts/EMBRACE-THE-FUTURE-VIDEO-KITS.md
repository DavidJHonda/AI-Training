# Embrace the Future Video Kits

> **Method note (2026-09-21):** per-lesson entries below dated before 2026-09-20 describe the previous preparation method (Scene/Takeaway labels, withheld face boards with "reserved" narration, prompts without a verbatim list, beat spine, or VOICE block). Rebuild a lesson's Markdown and prompt to the "Prepare a new lesson" procedure in `Prompts/README.md`, add it to `Prompts/upload-sets.json`, and run the sync before rolling it. Entries that say they are on the 2026-09-20 recipe are current; as of 2026-09-23 every entry below does.

Prep rebuilt 2026-09-23: all nine lessons are now on the 2026-09-20 recipe and in `Prompts/upload-sets.json`. This guide covers source preparation, not the status of existing videos. No video was generated, edited, or deployed in this pass.

Use current Markdown in `lessons/`, canonical JPGs in each `course-assets/` lesson folder, and the matching prompt and upload checklist in `Prompts/`. Markdown contains the spoken teaching in lesson order; it is not a script for reading production labels. Upload selected JPGs separately. There are no upload JPG copies in `lessons/` or `illustrations/`.

## Current source sets

All paths below are repository-relative. Each named prompt and checklist is in `Prompts/`.

### opener-embrace

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `embrace-the-future-opener.mp4` is **v5**,
shipped 2026-09-24 on David's approval (cache key 20260924ship1, pill 3 min, 3:25.6): roll 4, the first
roll on this kit, which met all eleven verbatim lines and says "worrier". Two narration cuts ("Look at
this board..." and "To understand this debate, look at this vintage map."), no grafts; four photograph
spans covered with roll 1 drawings; canonical voices card (gold ring per quote), edge-of-the-map
illustration (the live's camera) and section map (broken once by a roll 3 drawing); standard close.
Build: `scripts/video/build_opener_embrace_v5.py`. Record: `video-audit/opener-embrace-v5-2026-09-24/REVIEW.md`.
Replaces v4 (shipped 2026-09-22), which misattributed the four quotes to camps.

**Rolls 1-4 evaluated 2026-09-23** in `video-audit/opener-embrace-evaluation-2026-09-23/REVIEW.md`:
rolls 1 and 2 (old materials) REPAIR, roll 3 REROLL, roll 4 REPAIR and shipped as v5. Rolls 1 and 3
are the donors for v5's drawings.

- Markdown: `lessons/Opener-Embrace.md` (rewritten 2026-09-23: the four quotes and the section map
  rows split onto their own lines; the What Everyone's Saying card and the map illustration are now
  boards of their own, with the page prose that used to sit inside them moved out under `##` headings
  (`## WHERE DOES ALL THIS LAND?`, `## THE EDGE OF THE MAP`, `## WHAT THE SAILORS ACTUALLY FOUND`),
  so neither board holds through a paragraph; the map lead-in is David's fixed sentence, "This road
  map shows what we'll explore in this section, Embrace the Future."; the board's banner line closes
  the map beat)
- Prompt: `opener-embrace-video-prompt.txt` (498 words, four blocks; carries the Worrier pronunciation note added 2026-09-23 after the roll evaluation)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/embrace-the-future-opener/` (synced
  2026-09-23; registry slug is `embrace-the-future-opener`, matching the asset folder)
- Canonical folder: `course-assets/embrace-the-future-opener/`
- Boards in lesson order (no faces; all upload):
  - `embrace-the-future-opener-voices.jpg` — upload
  - `embrace-the-future-opener-edge-of-the-map.jpg` — upload (the two figures stand with their backs
    to the camera; no face is visible, so the canonical illustration uploads as-is)
  - `embrace-the-future-opener-section-map.jpg` — upload
  - `embrace-the-future-opener-close.jpg` — upload

**Beat spine**

1. Open on the voices card: "What everyone's saying", the four quotes in order, then "Who's right?
   Nobody knows."
2. Board gone: you already know how to use AI and understand the engine underneath; the goal is Be
   Smarter Than the Tool; done.
3. The three people by their labels: the AI Optimist, the AI Worrier, the Doubter who rolls their eyes
   at both. "Here's the honest part: nobody knows." / "Not them, not us, not the people building AI."
4. Drawn scene: the mapmakers who filled unknown waters with sea monsters and serpents.
5. The map illustration, three lines only: the ocean comparison, what the Worriers fill the unknown
   with, what the Optimists see in the same unknown.
6. Board gone: what the sailors actually found; Magellan, his crew, his death before the voyage ended;
   the section takes both views seriously; AI is here to stay, with both qualifiers.
7. Section map: the fixed lead-in sentence, then all three parts with their full descriptions, then
   "Take both views of the map seriously."
8. Close on the two lines with nothing after.

**Required verbatim lines:** the eleven in the prompt (the four quotes, the who's-right line, the two
honest-part lines, the map lead-in, the banner, and the two closing lines).

**Banned words:** leverage, framework, utilize, discourse, revolution, journey, transformative; no
screen/board-position references; no predicting which side turns out right; no lesson previewed beyond
what the map says.

### loudest-voices

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `loudest-voices.mp4` is **v7, shipped
2026-09-24** (David's approval; 3:49, cache key `20260924ship1`, pill 4 min). v7 is roll 1 of the
rebuilt kit, re-edited to apply David's three notes on v6 (built by
`scripts/video/build_loudest_voices_v7.py`; roll review in
`video-audit/loudest-voices-rolls-2026-09-23/REVIEW.md`, build record in its `build-v7/`).
The earlier v5 (shipped 2026-09-18, a best-of of the old-method rolls) was graded **REROLL** on
2026-09-23: `video-audit/loudest-voices-evaluation-2026-09-23/REVIEW.md`.

- Markdown: `lessons/loudest-voices.md` (rewritten 2026-09-23: board titles carried as spoken
  sentences; the page prose after Board 1 moved under `## THE TELL`; the required lines split onto
  their own lines; the verification-only sources line removed from the narration base, its guardrail
  now in the prompt)
- Prompt: `loudest-voices-video-prompt.txt` (492 words, four blocks)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/loudest-voices/` (synced 2026-09-23)
- Canonical folder: `course-assets/loudest-voices/`
- Boards in lesson order (no faces; all upload):
  - `loudest-voices-experts.jpg` — upload
  - `loudest-voices-missed-predictions.jpg` — upload
  - `loudest-voices-close.jpg` — upload

**Beat spine**

1. Hook over a drawn scene: opinions everywhere; who do you believe? Answer: the people who make AI
   for a living. "Same field. Same evidence. Very different bets."
2. Even the Experts Don't Know: Amodei the Optimist, Hinton the Worrier, LeCun the Doubter, in board
   order; each with his background, then his SAYS and BUT ADMITS quotations read word for word.
3. The tell (over a drawn scene, board gone): "None of them has a simple, one-sided view." Optimist
   sees danger / Worrier sees benefits / Doubter acknowledges risks; the people who know AI best still
   don't know where it's going. "Where AI will be in ten years is a bet."
4. This Has Happened Before: Stoll 1995, Ballmer 2007, Metcalfe 1996, Ford 1940, each with person,
   year, prediction, outcome; banner "The future is hard to predict because people change the result."
5. Why were they wrong: "A technology becomes the future only when people change their habits around
   it. Machines improve fast. Habits change at human speed."
6. Close on the two lines with nothing after.

**Required verbatim lines:** the six in the prompt (the three-beat bets line, the one-sided line, the
banner, the three habits sentences as one line, and the two closing lines). The six expert quotations
are demanded word for word in the beat spine rather than the verbatim list, to keep the list short.

**Banned words:** exponential, neural network, stakeholders, leverage, framework, utilize, narrative,
paradigm; no screen/panel/board-position references; no invented numbers or charts; no source citations;
the Right or Wrong? activity is not narrated.

### pace-of-change

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `pace-of-change.mp4` is **v8, shipped
2026-09-24** (David's approval; 4:52, cache key `20260924ship1`, pill 5 min). v8 is roll 4 of 2026-09-24
with four narration cuts (the two 2026-as-a-projection lines, "autonomous agent", the compounding
exponential loop); canonical Board 1 for 7.6 s, then roll 4's own animated 2023-vs-2026 build, which
David liked; race-beat drawings from rolls 1-4; canonical Boards 2-4 (roll 4's versions carry invented
statistics and draw the four ideas as a roadmap and a timeline); roll 4's forked spectrum under "not a
guaranteed timeline"; standard close. Build: `scripts/video/build_pace_of_change_v8.py`. Record:
`video-audit/pace-of-change-rerolls-2026-09-24/REVIEW.md` (roll 3/4 evaluation, v6, v7, v8). Known
gap: Boards 3 and 4 still run about 90 s back to back.

History: v2 (shipped 2026-09-18) was graded narration KEEP / pictures REROLL on 2026-09-23
(`video-audit/pace-of-change-evaluation-2026-09-23/REVIEW.md`). Rolls 1 and 2 of 2026-09-23
(`video-audit/pace-of-change-comparison-2026-09-23/REVIEW.md`) gave review builds v4/v5 on roll 1;
the race-beat reroll (rolls 3 and 4 of 2026-09-24) gave v6 (v5 re-pictured), then v7/v8 on roll 4.

- Markdown: `lessons/pace-of-change.md` (rewritten 2026-09-23: board titles carried as spoken
  sentences; the race paragraph moved out of Board 1 under `## A RACE TO DOMINATE`; the slow-down beat
  under `## READ THAT THIRD ONE AGAIN`; the required lines split onto their own lines; Board 4 now
  carries both tags and the ASI card's "Nobody knows whether it is possible."; the Markdown-only
  two-groups sentence and the "Now switch…" connective removed, their guardrail now in the prompt).
  **Page-match call (David's 9/21 rule, Markdown = the page):** the race paragraph now reads the page's
  "Each new ChatGPT, Claude, or Gemini release is a new, stronger LLM replacing the one before it."
  instead of the 9/18 generalization "not every release improves every task"; the prompt still forbids
  claiming every release improves every task. If the page sentence should soften, fix the page first.
- Prompt: `pace-of-change-video-prompt.txt` (493 words, four blocks)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/pace-of-change/` (synced 2026-09-23)
- Canonical folder: `course-assets/pace-of-change/`
- Boards in lesson order (no faces; all upload):
  - `pace-of-change-three-years.jpg` — upload
  - `pace-of-change-what-speeds-it-up.jpg` — upload
  - `pace-of-change-could-ai-improve-itself.jpg` — upload
  - `pace-of-change-how-far-can-ai-go.jpg` — upload
  - `pace-of-change-close.jpg` — upload

**Beat spine**

1. Hook: the argument is louder because the technology is advancing at blazing speeds.
2. ChatGPT: 2023 vs. 2026: all four rows, both years each, in order (answering, images, context
   window, doing).
3. The race (over a drawn scene, board gone): new models every couple of months, each release a new,
   stronger LLM; "A limitation can disappear quickly, so today's 'no' is not necessarily permanent."
4. Why So Fast?: three concepts by name with their explanations; then "Slow down and read that third
   one again." and "AI is already helping people build better AI."
5. Four future ideas (drawn scene): four ideas, one happening in limited form, three not demonstrated;
   ideas to understand, never steps in order.
6. Could AI Improve Itself?: automated AI research (limited form) and self-improving AI (not
   demonstrated); banner "One is human-directed. The other would be a self-reinforcing loop."
7. How Far Can AI Go?: AGI (no agreed finish line; no accepted definition or test), ASI (hypothetical;
   nobody knows whether it is possible); banner "Nobody knows whether AI will reach either milestone."
8. Close on the two lines with nothing after.

**Required verbatim lines:** the six in the prompt (the today's-"no" line, the AI-builds-AI line, the
two banners, the two closing lines).

**Banned words:** ultimate, trajectory, theoretical, exponential, stakeholders, leverage, framework,
utilize, paradigm; no screen/tag/board-position references; no product names, release dates, charts or
timelines beyond the Markdown; no redrawn board diagrams; the lab is not narrated.

### big-downside

**Live `big-downside.mp4` is v3, shipped 2026-09-24** (David's approval; 5:38, cache key `20260924ship1`,
pill 6 min). Rolls 3 and 4 (2026-09-24, on the fixed materials below) were reviewed in
`video-audit/big-downside-review-2026-09-24/REVIEW.md`: roll 3 is the base (six-idea frame, no positional screen
references), and roll 4 is a donor. v3 is roll 3 with roll 4's jailbreak section and Pacing the Frontier request,
and roll 1's guardrail kinds, trace-some-features line, goal line and Anthropic's-CEO sentence. It uses canonical
boards, has the 1908 car photograph covered, and ends on the standard close. Build: `scripts/video/build_big_downside_v2.py`;
record: `video-audit/big-downside-v2-2026-09-24/REVIEW.md` (v2 flashed six frames of an old slide at 5:10; v3 fixes it).
Keep rolls 1-4: they hold the donor audio and drawings.

**Kit rebuilt 2026-09-23; materials fixed 2026-09-23 after the first two rolls.** Rolls 1 and 2 and
the live video were all reviewed against the current page
(`video-audit/big-downside-review-2026-09-23/REVIEW.md`); all three are REROLL. The live video is
teaching the pre-rewrite OpenAI incident (a single model escaping a sandbox) and must be replaced
whatever happens next. Both new rolls missed the six-idea spine and narrated board geometry
seventeen times between them, which blocks the 2026-09-23 hold rule. Fixes applied before the reroll:

- The prompt never actually banned screen references (it only forbade the phrase "this board shows").
  VOICE now carries an explicit ban on panel/left/middle/right/row/footer/banner/graphic/image and on
  "as shown" and "the first panel", with the rule stated positively: teach each point as a fact about
  the world, not a thing on a picture.
- The upload Markdown had dropped the page's own Roman numerals from the six idea headings, so the
  engine had no signal which six of its eleven `##` headings were the ideas. Headings are now
  `## I - The Black Box` through `## VI - Safety Runs Behind`, matching the page's SectionKickers, and
  the prompt points at them ("the Markdown's six numbered headings").
- Three lines promoted into REQUIRED VERBATIM AUDIO, now thirteen: "The downside becomes clear through
  six ideas.", the altered-records line (roll 1 said agents altered "their own actions"), and the
  Pacing the Frontier quotation (roll 1 changed "accelerates" to "could accelerate", roll 2 dropped it).
- "Say 'about' wherever the Markdown does" added; all three rolls said "1,200 agents" flat.
- The photograph ban now says "of any kind, archival included" - roll 2 used an archival motor car with
  people in frame, a Wright Flyer, and the U.S. Capitol.
- Source conflict settled: `index.html`'s hidden md-source said "An attacker needs to find only one
  opening"; the board art and the Markdown say "An attacker needs only one opening." The page now
  matches the board. The Markdown's "whether guardrails will work" is now the page's "if".

Prompt is 499 words, four blocks, within the recipe's limit.

- Markdown: `lessons/big-downside.md` (rewritten 2026-09-23: the six ideas now run as prose sections
  with their boards beneath them; each board carries only what is printed on it, so the page prose
  that used to sit inside a board section moved out under `##` headings; the required lines split onto
  their own lines; the hidden `md-source` divs in `index.html` were ignored in favour of the board
  images themselves, and the boards' own wording is what the Markdown speaks)
- Prompt: `big-downside-video-prompt.txt` (496 words, four blocks)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/big-downside/` (synced 2026-09-23)
- Canonical folder: `course-assets/big-downside/`
- Boards in lesson order:
  - `big-downside-safety-guardrails.jpg` — upload
  - `big-downside-jailbreak.jpg` — **post-only (faces)**; uploads as
    `Prompts/big-downside-jailbreak-faceless.jpg`, the same 1387x1134 board with the photo panel
    filled in the board's lavender. The two sign lines ("Defenders must protect many paths." / "An
    attacker needs only one opening.") live only in that photo, so the Markdown speaks them as
    sentences and the prompt demands them verbatim. The canonical board replaces the variant in the edit.
  - `big-downside-policy-puppetry.jpg` — upload
  - `big-downside-voice-cloning.jpg` — upload
  - `big-downside-goal-test.jpg` — upload
  - `big-downside-safety-timeline.jpg` — upload
  - `big-downside-close.jpg` — upload

**Beat spine**

1. Hook: the iPhone question, answered — "Because greater capability can create greater risk." The
   downside comes through six ideas.
2. The Black Box: learned patterns rather than written rules, researchers can trace some features but
   cannot explain one answer, the dog-named-Spot example, no complete repair manual.
3. Guardrails: the three kinds, "But no layer catches everything.", then the board's three future
   cases with their reasons and "The worry grows as capability grows."
4. Jailbreaking: "This is called jailbreaking.", the defender-attacker asymmetry and cat-and-mouse,
   then Policy Puppetry (HiddenLayer, 2025, Claude/ChatGPT/Gemini, fake official instructions).
5. Bad Actors: ordinary abilities combined, guardrails may miss the plan, then all four voice-clone
   steps, ending on calling back on the real number. "As AI gets more powerful, so do the things a bad
   actor can do."
6. AI Follows the Goal: July 2026, OpenAI, reduced safeguards; assignment, ~1,200 agents
   communicating, ~700 attacking Hugging Face, the boundary line, then the altered records.
7. Safety Runs Behind: all three historical gaps with their years, AI still evolving, then why the gap
   matters now.
8. What the AI companies are doing: red teams, the 2026 "Pacing the Frontier" statement and its ask,
   then the quotation.
9. Close on the two lines with nothing after.

**Required verbatim lines:** the thirteen in the prompt (the capability/risk line, the six-ideas line,
the repair-manual line, the no-layer line, the two banners, the jailbreaking definition, the sign
lines, the bad-actor line, the altered-records line, the Pacing the Frontier quotation, and the two
closing lines).

**Save the next roll as** `Prompts/big-downside-5.mp4` (1-4 are the 2026-09-23/24 rolls; keep them).

**Banned words:** leverage, framework, utilize, mitigate, adversary, exponential, robust; no
screen/board-position references; no softened numbers; no invented incidents; never explain how a
jailbreak is performed.

### big-upside

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe; lesson rewritten 2026-09-24.** Live `big-upside.mp4` is v5 (below).

**Rolls 1-2 and the live file evaluated 2026-09-24** in
`video-audit/big-upside-review-2026-09-24/REVIEW.md`: roll 1 REPAIR (meets all eight verbatim
lines; recommended base), roll 2 REROLL (donor for the verbatim Hassabis quotation), live REPLACE
(no protein board, three of eight required lines).
**v2 review candidate built 2026-09-24** (`Prompts/big-upside-v2.mp4`, 4:56.2): roll 1 with five cuts
and roll 2's quotation grafted, canonical boards, photographs covered with live-video drawings, standard
close. Not listened to; not shipped. Build: `scripts/video/build_big_upside_v2.py`. Record:
`video-audit/big-upside-v2-2026-09-24/REVIEW.md`.
**v3 built 2026-09-24** (`Prompts/big-upside-v3.mp4`, 4:50.9): v2 plus David's cut of "The sequence of
those acids determines the folding, and that final shape determines the function." Record:
`video-audit/big-upside-v3-2026-09-24/REVIEW.md`.
**Lesson rewritten 2026-09-24; rolls 3-6 on the new materials.** Rolls 3-4 gave each example card one sentence
(`video-audit/big-upside-review-2026-09-24b/`); the Markdown and prompt were revised to make the card sentences
verbatim, and roll 6 met all 19 lines (`video-audit/big-upside-review-2026-09-24c/`). **v4 built 2026-09-24**
(`Prompts/big-upside-v4.mp4`, 4:17.3): roll 6 with six cuts and roll 3's question line grafted; closing photographs
covered with rolls 3-4 drawings. Not listened to; not shipped. Build: `scripts/video/build_big_upside_v4.py`.
Record: `video-audit/big-upside-v4-2026-09-24/REVIEW.md`. v2/v3 predate the lesson rewrite.
**v5 built 2026-09-24** (`Prompts/big-upside-v5.mp4`): v4 with the dissolve flash at 4:06 removed (two donor
tails trimmed). Record: `video-audit/big-upside-v5-2026-09-24/REVIEW.md`.
**Live `big-upside.mp4` is v5**, shipped 2026-09-24 on David's approval (cache key 20260924ship1, pill 4 min, 4:17.3).
Not listened to end to end before shipping; the joins listed in the v4 record are still unauditioned.

**Lesson simplified 2026-09-24:** protein teaching now covers essential jobs, shape,
and scale: about 200,000 experimentally determined structures versus over 200 million
AlphaFold predictions, shared freely. Removed the bead-chain mechanics, amino-acid
count, atoms comparison, and near-lab-accuracy detour. The new board replaces the old
protein illustration in place. The obsolete faceless upload crop was removed.

An explicit bridge introduces Demis as the person who helped make this achievement
possible. David approved telling his journey as a short story, rather than reciting
every timeline date. The timeline board stays; the Markdown and prompt specify its
concise narration. The six examples now form two boards: Helping People Stay Healthy (cancer
screening, urgent scan alerts, antibiotic research) and Helping People in Everyday
Life (reading aloud, flood warnings, targeted spraying). Repeated prose beneath
them stays removed. New art replaces the materials and weather illustrations. Card wording was shortened with David’s approval; the antibiotic finding remains explicitly a lab result, and the spraying example now states the environmental benefit upfront. Existing rolls and v3 predate these changes; no video was edited.

- Markdown: `lessons/big-upside.md`
- Prompt: `Prompts/big-upside-video-prompt.txt` (495 words)
- Upload registry: `Prompts/upload-sets.json`; synced bundle: `gemini-notebook/big-upside/`
- Upload boards, in order: `big-upside-protein.jpg`, `big-upside-hassabis-timeline.jpg`,
  `big-upside-scientific-discovery.jpg`, `big-upside-practical-help.jpg`, `big-upside-close.jpg`.
  All are canonical JPGs in `course-assets/big-upside/`; no face variants or post-only boards.

**Beat spine**

1. Giant calculator and fifty-year scientific challenge.
2. Proteins do essential jobs; shape matters. Experiments versus predictions, clearly
   distinguished, and the free resource for research. Roughly 40–50 seconds; no mechanics.
3. Who helped make that happen? Demis, chess and games, studying the brain, DeepMind,
   AlphaFold, free release, Nobel recognition. Tell the story without a roll call of dates.
4. Reach: three million users, over 190 countries, shared 2024 Nobel Prize and quotation.
5. Patterns used for health and daily life; six examples with problem, AI contribution,
   benefit, and both banners. Doctors retain medical decisions; antibiotics remain lab research.
6. Answer what good AI does for society, then turn Demis's story toward students using
   their strengths to help people.
7. Two closing lines, with nothing after them.

**Required verbatim lines:** the eleven in the prompt, including the full attributed
Hassabis quotation and the exact experiment/prediction distinction. Read the quotation
in full, word for word; do not paraphrase or omit it. Do not imply laboratory confirmation of all AlphaFold outputs,
automatic medical decisions, approved antibiotic treatment, or guaranteed warnings.

### rise-of-agents

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `rise-of-agents.mp4` is **v4, shipped
2026-09-24** on David's approval (cache key 20260924ship1, pill 3 min, 3:07.8): roll 2 base with the old
live video's intro and loop narration, roll 2's everywhere line and roll 1's example line and loop banner, section-level
rings. Build: `scripts/video/build_rise_of_agents_v4.py`. Record: `video-audit/rise-of-agents-v4-2026-09-24/REVIEW.md`.
The replaced live video (commit 6cccc758) is kept as `Prompts/rise-of-agents-live-pre-v4.mp4`, the donor
the v3/v4 builds read.

**Rolls 1-2 and the live video evaluated 2026-09-24** in
`video-audit/rise-of-agents-evaluation-2026-09-24/REVIEW.md`: roll 1 REPAIR (8/8 verbatim, but drops
the analogy's mistake clause; donor only), roll 2 REPAIR and proposed base (7/8; the loop banner comes
from roll 1 @118.78-130.98 under the loop board), live REROLL (3/8, superseded). Edit plan was awaiting
David's approval (since given, below).
**v2 review candidate built 2026-09-24** on David's approval (both grafts + cut 1; optional "it's
autonomous" cut not taken): `Prompts/rise-of-agents-v2.mp4` (2:58.4), build
`scripts/video/build_rise_of_agents_v2.py`, record `video-audit/rise-of-agents-v2-2026-09-24/REVIEW.md`.
8/8 verbatim lines on the output transcript; transition guard 17/17. Not shipped; joins await David's ear.
**v3 review candidate built 2026-09-24** from David's notes on v2: the live video's intro (0:00-0:38)
replaces v2's opening, section-level rings wherever a card section is spoken (after the live video),
and the live video's loop narration under What an Agent Does (two live sentences omitted, roll 1's banner
line kept): `Prompts/rise-of-agents-v3.mp4` (3:00.0), build `scripts/video/build_rise_of_agents_v3.py`,
record `video-audit/rise-of-agents-v3-2026-09-24/REVIEW.md`. 7/8 verbatim lines (the live intro says
"A chatbot answers, but an agent acts."); transition guard 17/17. Not shipped.
**v4 review candidate built 2026-09-24**: v3 plus the analogy-to-example transition David flagged
(roll 2 "This distinction is exactly why AI agents are suddenly everywhere. They actually do the work."
over its Completed Tasks drawing, then roll 1 "Let's look at a concrete example."):
`Prompts/rise-of-agents-v4.mp4` (3:07.8), build `scripts/video/build_rise_of_agents_v4.py`, record
`video-audit/rise-of-agents-v4-2026-09-24/REVIEW.md`. Transition guard 19/19. **Shipped 2026-09-24.**

- Markdown: `lessons/rise-of-agents.md` (rewritten 2026-09-23: the comparison board's six labelled
  rows are written out as sentences; review and approval are narrated before publishing; "An agent is
  not a new kind of AI." split onto its own line so the prompt can demand it verbatim; both rogue-agent
  quotations carried with their speakers)
- Prompt: `rise-of-agents-video-prompt.txt` (494 words, four blocks)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/rise-of-agents/` (synced 2026-09-23)
- Canonical folder: `course-assets/rise-of-agents/`
- Boards in lesson order:
  - `rise-of-agents-gps.jpg` — **post-only (faces)**; uploads as
    `Prompts/rise-of-agents-gps-faceless.jpg`, the same 1408x1117 board with the two car photos filled
    in the board's lavender. Both card texts stay on the variant. The canonical board replaces it in
    the edit.
  - `rise-of-agents-chatbot-vs-agent.jpg` — upload
  - `rise-of-agents-agent-loop.jpg` — upload
  - `rise-of-agents-rogue.jpg` — upload
  - `rise-of-agents-close.jpg` — upload

**Beat spine**

1. "What's an agent?" then the analogy board: GPS is like ChatGPT, self-driving is like an agent, each
   with its full explanation including "You may not catch a mistake until later."
2. Agents are everywhere because they do the work.
3. Comparison board: the scenario (30 points, Friday's game, a friend's phone, 50 clips); everything
   you do with a chatbot and the one thing AI does; everything the agent does and what you still own.
4. Board gone: an agent runs on the same kind of LLM; what changes is what happens after you type.
5. The loop board: Goal, Plan, Act, Check with their descriptions, "Not done? Go again.", and "An
   agent loops until the goal is met. You set the goal and judge the result."
6. Your name on the finished product: the review responsibility in full, "Agents are good. But not
   perfect."
7. Rogue agents: April 2026 PocketOS (permissions error, master key, live database and backups in nine
   seconds, its quotation); 2025 Gemini (project files wiped, the apology, its quotation).
8. The rule: "AI should not send, spend, submit, delete, or post without you reviewing first." Then the
   rule of thumb, including starting with ChatGPT.
9. Close on the two lines with nothing after.

**Required verbatim lines:** the eight in the prompt (the chatbot/agent line, the not-a-new-kind line,
the loop banner, the review-responsibility line, the good-but-not-perfect line, the never-without-review
rule, and the two closing lines).

**Banned words:** leverage, framework, utilize, autonomous, orchestrate, workflow, seamless, deploy; no
screen/board-position references; never promise an agent always finishes; never suggest working around
a block, a limit or a permission; the Be the Agent activity is not narrated.

### work-changes

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `work-changes.mp4` shipped under the old
method; no evaluation of it against the current system has been run, and no roll on this kit yet.

- Markdown: `lessons/work-changes.md` (rewritten 2026-09-23: the assignment board's full before/after
  lists are written out as sentences, including all five first-pass steps on both sides, both results,
  and the manager's words verbatim; "in one study" and "certain tasks" stay attached to the 25% and 40%
  figures; the required lines split onto their own lines)
- Prompt: `work-changes-video-prompt.txt` (484 words, four blocks)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/work-changes/` (synced 2026-09-23)
- Canonical folder: `course-assets/work-changes/`
- Boards in lesson order:
  - `work-changes-four-shapes-of-ai-work.jpg` — upload
  - `work-changes-assignment.jpg` — **post-only (faces)**; uploads as
    `Prompts/work-changes-assignment-faceless.jpg`, the same 1203x1308 board with both photo panels
    filled white. Every list item and both results stay on the variant. The canonical board replaces it
    in the edit.
  - `work-changes-automation-and-augmentation.jpg` — upload
  - `work-changes-productivity-and-possibilities.jpg` — upload
  - `work-changes-close.jpg` — upload

**Beat spine**

1. Hook: finishing school, starting a career; all four job titles; what those jobs look like is already
   changing.
2. Four AI Strengths at Work: all four by name with their descriptions.
3. What sets you apart, asked and answered immediately: "It's what you already know."
4. The assignment board: the manager's words verbatim; the old job with its five first-pass steps,
   three follow-on steps and its result; the new job with the same five done by AI in minutes, the four
   steps you start with, and its result.
5. Board gone: the busy work was AI's strengths in action; improving AI's work took what you already
   know. "AI doesn't just help you work faster. It can help you focus on what's really important."
6. Automate and augment, each with its example from the reviews job, then "The work still has your name
   on it. You own the outcome."
7. What Changes with AI: all three by name, with "in one study", "certain tasks", 25% faster, 40%
   higher quality spoken together.
8. The part that matters: entry-level work, "AI can make you productive before it makes you
   knowledgeable.", being asked to check work you haven't learned yet, and the answer — learn, learn
   more, school.
9. Close on the two lines with nothing after.

**Required verbatim lines:** the seven in the prompt (the what-you-already-know line, the manager's
assignment, the focus line, the name-on-it banner, the productive-before-knowledgeable line, and the two
closing lines).

**Banned words:** leverage, framework, utilize, disrupt, upskill, synergy, workforce, transformation; no
screen/board-position references; no statistic beyond the Markdown; no predicting job losses; the LAB is
not narrated.

### data-centers

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `data-centers.mp4` shipped under the old
method; no evaluation of it against the current system has been run, and no roll on this kit yet.

- Markdown: `lessons/data-centers.md` (rewritten 2026-09-23: the approved 2026-09-18 opening is kept
  word for word as an assumption inside the explanation — one trillion weights per generated token,
  roughly two calculations per weight, 1,000 tokens or around 750 words, about two quadrillion
  calculations — with no separate caveat paragraph; the Scene labels are gone; each board carries only
  its printed text, with the page prose moved out under `##` headings; "U.S. data centers" stays
  attached to the electricity figures, and additional supply stays distinct from efficiency)
- Prompt: `data-centers-video-prompt.txt` (499 words, four blocks)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/data-centers/` (synced 2026-09-23)
- Canonical folder: `course-assets/data-centers/`
- Boards in lesson order (no faces; all upload):
  - `data-centers-data-center.jpg` — upload (photograph of a server hall; the one distant figure walks
    away from the camera, so no face is visible)
  - `data-centers-physical-footprint.jpg` — upload
  - `data-centers-meeting-demand.jpg` — upload
  - `data-centers-close.jpg` — upload

**Beat spine**

1. Hook: type a question, hit send, and an enormous amount of math runs behind the chat.
2. The assumed calculation in order, then "The ability to run that math is called compute."; serving
   millions of people; why companies build more data centers.
3. A warehouse of thousands of GPUs running around the clock; the hall itself on the photograph.
4. Board gone: several football fields, as much electricity as a small city, scale varies by facility,
   "When you hit send in ChatGPT, a data center answers.", "Somebody pays for all that arithmetic.",
   and who else it affects.
5. What a Data Center Means for Its Neighbors: all four effects with their numbers (4.4% in 2023, the
   Berkeley Lab projection of 6.7–12% by 2028, household bills; about a million gallons on a hot day
   with recycling and reuse; fans 24 hours a day and lawsuits over lost sleep; 100 to 200 permanent
   workers, about a big supermarket's staff).
6. Meeting the Demand: all three responses by name, then the banner; then "More efficient tasks do not
   automatically mean a smaller total footprint." with its condition.
7. The footprint, honestly: one request is a small part, every technology has a footprint, who pays it
   in dollars, watts, water and quiet, and the no-guilt line with its reason.
8. Close on the two lines with nothing after.

**Required verbatim lines:** the seven in the prompt (the compute definition, the hit-send line, the
somebody-pays line, the demand banner, the no-guilt line, and the two closing lines).

**Banned words:** leverage, framework, utilize, sustainability, carbon, emissions, environmental,
staggering; no screen/board-position references; no predicted future totals; no town or company beyond
the Markdown; never tell anyone to use AI less. Highlighting call for the edit stands from 2026-09-18:
whole-card highlights on the neighbours and demand boards, none on the warehouse photograph or the
close. The retired fixed training total, the 2,000-word chat claim, the separate electricity qualifier
and the nuclear-project examples stay removed; no Hit Send board is used.

### unexpected-results

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe. v2 SHIPPED 2026-09-24** (David: "Ship it"): roll 2 base, roll 1's
"The new space quickly fills back up with new drivers." in place of roll 2's "incentive" sentence, and the old live
video's Text Messaging and GPS explanations under the board (David: they felt much stronger), after roll 2's own GPS
sentence. Build `scripts/video/build_unexpected_results_v2.py`; records `video-audit/unexpected-results-review-2026-09-24/`
(both rolls and the old live video), `-v1-2026-09-24/`, `-v2-2026-09-24/`. The v1/v2 builds read donor drawings and
audio from the pre-ship live file; restore it from the parent of the ship commit before rebuilding.
Page question: the live SMS/GPS explanations (why each turned out better than planned) are not on the page yet.

- Markdown: `lessons/unexpected-results.md` (rewritten 2026-09-23: the board's four cards are written
  out as sentences; the tailless-rat question is answered in the next sentence rather than left for the
  viewer; "A dead rat pays once. A live rat pays forever." and the moral split onto their own lines)
- Prompt: `unexpected-results-video-prompt.txt` (497 words, four blocks)
- Registry: `Prompts/upload-sets.json` → `gemini-notebook/unexpected-results/` (synced 2026-09-23)
- Canonical folder: `course-assets/unexpected-results/`
- Boards in lesson order (no faces; all upload):
  - `unexpected-results-plans.jpg` — upload
  - `unexpected-results-close.jpg` — upload

**Page gap, David's call 2026-09-23:** the induced-demand explanation is IN the narration. The
Markdown now carries it as prose after the board, under `## WHY MORE LANES CAN MEAN MORE TRAFFIC`:
an easier road attracts more driving, some of the new space fills back up, that alone does not explain
the whole Houston number, and it is why "just add lanes" does not always end congestion. The lesson
page does not say this yet, so this is the one place in the section where the Markdown runs ahead of
`index.html`. Add it to the Wider Highways beat on the page when the section next gets an editorial
pass, or the video will teach something a reader cannot find.

**Beat spine**

1. Hook: Worriers and Optimists, and results nobody predicted. "The best way to see it is a true story
   about rats."
2. Hanoi, 1902: too many rats in the new sewers, pay for a tail, tails by the thousands, then tailless
   rats — answered immediately: rats live a full rat life without tails and keep breeding, so hunters
   clipped and released. "A dead rat pays once. A live rat pays forever."
3. Rat farms, and the ending: a mountain of tails, more rats than at the start.
4. The moral: the payment system worked exactly as designed, "But the real goal was fewer rats, and the
   program encouraged people to keep rats alive."
5. Four plans, two better and two worse: Text Messaging, GPS, Cane Toads, Wider Highways, each with its
   full result including $2.8 billion, the Katy Freeway, 2014 and 51% longer.
6. The general road pattern (board gone): an easier road attracts more driving, some of the new space
   fills back up; that alone does not explain the Houston number; it is why adding lanes does not
   always end congestion. General only, never offered as proof of the Houston figure.
7. Point it at AI: both sides are predicting, every prediction smart and informed, and the most
   important thing AI does may be something nobody has thought of yet.
8. "That's not a reason to fear the future. It's the reason to walk into it curious, with your eyes
   open." Then the three things you need to do.
9. Close on the two lines with nothing after.

**Required verbatim lines:** the six in the prompt (the rats hook, the pays-once line, the moral, the
curious line, and the two closing lines). The board title was dropped from the list to make room for the
road-pattern beat; it is still spoken from the board.

**Banned words:** leverage, framework, utilize, incentive, perverse, unintended consequences, induced
demand; no screen/board-position references; never say which AI camp is right; no prediction about what
AI will do; no example beyond the Markdown; the Rat Quiz is not narrated.

## Changed teaching and scene directions

**Superseded 2026-09-23.** All nine lessons now have rebuilt kit entries above, on the 2026-09-20
recipe, and each one's teaching requirements and guardrails live in its own Markdown, prompt and beat
spine. The 2026-09-18 bullets that used to sit here are history, not instructions. The page
questions they raised are recorded in their own entries: the Pace of Change release sentence, and the
Wider Highways induced-demand explanation, which David directed into the narration on 2026-09-23 and
which the page still needs.

## Prep versus current page

Under the current recipe the Markdown matches the page: nothing is added to the narration that the
page and its boards do not teach, and a guardrail belongs in the prompt rather than in the narration.
Where a kit would once have clarified a page statement in the narration, the clarification now sits in
the prompt as a negative and the page question is written down in that lesson's entry. Research links,
source records and citations are verification-only and are never narrated. The hidden `md-source` divs
in `index.html` are stale; the board images and the visible page are the sources.

## Production handoff

Follow `Prompts/README.md`, `scripts/video/README.md`, `scripts/video/EDIT-SPEC.md`, and `scripts/video/NARRATION-REVIEW.md`.

- Each prompt stands alone and is under 500 words. Paste it in customization; do not upload it as lesson content.
- Use drawn scenes rather than stock photos for generated visuals, printed labels, no extra chapter/lesson-number cards, and unchanged, complete supplied boards.
- Boards with visible faces are never uploaded. Each one has a faceless upload variant in `Prompts/`, named in its kit entry and recorded in the registry as the `covers` of the canonical board; the canonical board replaces it in the edit. Any teaching that lives only inside a removed photo is spoken from the Markdown. Never recreate the faces.
- Speak the exact two closing lines. No narration follows them. The standard course closing visual is inserted in editing.
- The watermarking toggle does not take effect (the build removes the mark). Save each raw roll under the next unused name.
- Review changed scene directions before generation. During evaluation, present the proposed box-highlighting plan before edits, under the shared specs. Full-card versus subsection highlighting depends on the spoken explanation; source preparation does not preapprove timings or zooms.
- Use natural transitions. Decide pauses selectively during editing; do not automatically add one second at each idea or board.
- Check actual narration after the roll. These sources do not establish a KEEP/REPAIR/REROLL verdict or a shipping status for an existing video.
