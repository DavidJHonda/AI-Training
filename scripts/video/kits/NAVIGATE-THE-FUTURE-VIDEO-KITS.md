# Navigate the Future Video Kits

> November 16 lesson revision. Loudest Voices goes from the experts to What’s in Your Hands? Where Will AI Land? follows Big Upside, opens with Hanoi, and teaches the four scenarios on one board. Use the current Markdown, prompts, and upload sets for these two lessons.

> Further shortening approved 2026-10-27: Remove the Magellan detour and repeated commentary about filling blank spaces with hopes/fears and preparing for uncertain trajectories. Retain what sailors unexpectedly found, both views, the permanence qualification, section map, and close. Current lesson and prompt supersede historical instructions below.

> Current opener revision (2026-10-27): the opening blue declaration board is retired. Start directly with the revised lesson narration; retain the analogy, section map, and close. Essential points are folded into prose. This supersedes opening-board, creed, and opening-quote requirements below. Consult `gemini-notebook/upload-sets.json` for current preparation status and uploads. The existing MP4 still awaits revision.

Prep status is controlled by `gemini-notebook/upload-sets.json`. Any lesson listed in
`needs_preparation` requires a fresh kit; older “materials ready” or upload directions
below describe historical work and do not authorize reuse.

> **Method note (2026-09-21):** per-lesson entries below dated before 2026-09-20 describe the previous preparation method (Scene/Takeaway labels, withheld face boards with "reserved" narration, prompts without a verbatim list, beat spine, or VOICE block). Rebuild a lesson's Markdown and prompt to the "Prepare a new lesson" procedure in `scripts/video/PREPARATION.md`, add it to `gemini-notebook/upload-sets.json`, and run the sync before rolling it. Entries that say they are on the 2026-09-20 recipe are current; as of 2026-09-23 every entry below does.

Prep rebuilt 2026-09-23: all nine lessons are now on the 2026-09-20 recipe and in `gemini-notebook/upload-sets.json`. This guide covers source preparation, not the status of existing videos. No video was generated, edited, or deployed in this pass.

Use current Markdown in `lessons/`, canonical JPGs in each `course-assets/` lesson folder, and the matching prompt and upload instructions in `gemini-notebook/<slug>/`. Markdown contains the spoken teaching in lesson order; it is not a script for reading production labels. Upload selected JPGs separately. There are no upload JPG copies in `lessons/` or `illustrations/`.

## Current source sets

All paths below are repository-relative. Prep files live under `gemini-notebook/`.

### opener-navigate

**v6 shipped locally 2026-10-22 on David’s approval; queued for batch deployment.**
Runtime 3:17.3, cache key `20261022v6`. Removes the Doubter and the three-types lead-in;
the canonical voices board replaces the three-person illustration. Written lesson and prep agree.
Record: `video-audit/remove-doubter-2026-10-22/NAVIGATE-SHIP.md`.

**Previous release: v5.** Kit rebuilt 2026-09-23 on the 2026-09-20 recipe; v5 was
shipped 2026-09-24 on David's approval (cache key 20260924ship1, pill 3 min, 3:25.6): roll 4, the first
roll on this kit, which met all eleven verbatim lines and says "worrier". Two narration cuts ("Look at
this board..." and "To understand this debate, look at this vintage map."), no grafts; four photograph
spans covered with roll 1 drawings; canonical voices card (gold ring per quote), edge-of-the-map
illustration (the live's camera) and section map (broken once by a roll 3 drawing); standard close.
Build: `scripts/video/build_opener_navigate_v5.py`. Record: `video-audit/opener-navigate-v5-2026-09-24/REVIEW.md`.
Replaces v4 (shipped 2026-09-22), which misattributed the four quotes to camps.

**Rolls 1-4 evaluated 2026-09-23** in `video-audit/opener-navigate-evaluation-2026-09-23/REVIEW.md`:
rolls 1 and 2 (old materials) REPAIR, roll 3 REROLL, roll 4 REPAIR and shipped as v5. Rolls 1 and 3
are the donors for v5's drawings.

- Markdown: `lessons/Opener-Navigate.md` (rewritten 2026-09-23: the four quotes and the section map
  rows split onto their own lines; the What Everyone's Saying card and the map illustration are now
  boards of their own, with the page prose that used to sit inside them moved out under `##` headings
  (`## WHERE DOES ALL THIS LAND?`, `## THE EDGE OF THE MAP`, `## WHAT THE SAILORS ACTUALLY FOUND`),
  so neither board holds through a paragraph; the map lead-in is David's fixed sentence, "This road
  map shows what we'll explore in this section, Navigate the Future."; the board's banner line closes
  the map beat)
- Prompt: `gemini-notebook/navigate-the-future-opener/PROMPT.txt` (498 words, four blocks; carries the Worrier pronunciation note added 2026-09-23 after the roll evaluation)
- Registry: `gemini-notebook/upload-sets.json` → `gemini-notebook/navigate-the-future-opener/` (synced
  2026-09-23; registry slug is `navigate-the-future-opener`, matching the asset folder)
- Canonical folder: `course-assets/navigate-the-future-opener/`
- Boards in lesson order (no faces; all upload):
  - `navigate-the-future-opener-voices.jpg` — upload
  - `navigate-the-future-opener-edge-of-the-map.jpg` — upload (the two figures stand with their backs
    to the camera; no face is visible, so the canonical illustration uploads as-is)
  - `navigate-the-future-opener-section-map.jpg` — upload
  - `navigate-the-future-opener-close.jpg` — upload

**Beat spine**

1. Open on the voices card: "What everyone's saying", the four quotes in order, then "Who's right?
   Nobody knows."
2. Board gone: you already know how to use AI and understand the engine underneath; the goal is Be
   Smarter Than the Tool; done.
3. The two perspectives by their labels: the AI Optimist and the AI Worrier. "Here's the honest part: nobody knows." / "Not them, not us, not the people building AI."
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

**Current full-lesson reroll.** The added voice at 1:41–1:54 in the v16 review cut interrupted the transition. Generate the entire lesson with the same two hosts throughout. When reviewing a roll, listen from the final expert admission into the first hands example. One familiar host should carry the thought from “None of them has a simple, one-sided view” through “That’s where to put your energy.” Use the continuous passage from the roll for the edit.

Upload the lesson Markdown and the three boards in `gemini-notebook/loudest-voices/upload/`. Paste the adjacent `PROMPT.txt` into the video customization box.

1. Open with the competing opinions about AI. Introduce Dario Amodei and Geoffrey Hinton and quote what each predicts and what each admits.
2. Hold the experts board as the host explains where the two views overlap and why a ten-year forecast is a bet.
3. Reveal the hands board on “What’s actually in your hands?” Teach the five pairs, then the two-line close. The historical examples belong in *Where Will AI Land?*

**Historical releases**

**v12 shipped locally 2026-10-22 on David’s approval; queued for batch deployment.**
Runtime 4:36.733, cache key `20261022v12`, pill 5 min. Two-expert board; Doubter removed;
earlier board entrance; redundant highest-levels sentence cut; Hinton flash repaired;
In Your Hands comparison and the current close appended.
Record: `video-audit/loudest-voices-cut-v12-2026-10-22/SHIP.md`.

**Historical release: v7, shipped 2026-09-24** (David's approval; 3:49, cache key `20260924ship1`, pill 4 min). v7 is roll 1 of the
rebuilt kit, re-edited to apply David's three notes on v6 (built by
`scripts/video/build_loudest_voices_v7.py`; roll review in
`video-audit/loudest-voices-rolls-2026-09-23/REVIEW.md`, build record in its `build-v7/`).
The earlier v5 (shipped 2026-09-18, a best-of of the old-method rolls) was graded **REROLL** on
2026-09-23: `video-audit/loudest-voices-evaluation-2026-09-23/REVIEW.md`.

### pace-of-change

**2026-11-03 lesson revision:** The current page and upload kit replace the two future-ideas boards with `pace-of-change-three-future-ideas.jpg`, a canonical EE-3FB board for RSI, AGI, and ASI. Rebuild with `.video-venv/bin/python scripts/video/render_pace_future_ideas.py`. No status or takeaway banners. The older boards remain source artwork and historical video dependencies. The revised lesson is now installed locally as v12; the build history below describes earlier versions.

The November 16 local course video (v14, 3:42.233) includes the dog image comparison at 0:27.700–0:40.467, the high school reader at 0:54.200–1:03.067, and a date-free model release animation at 1:28.567–1:33.133. The audio matches v12 byte for byte. Cache key `20261116ship14`.

**Local release 2026-11-03:** v12 (3:42.233), cache key `20261103ship12`, pill 4 min. Roll 1 base, two roll 2 narration passages, current canonical boards, and supporting drawings. Approved by the owner after technical verification and disclosure that direct listening/continuous playback remain unperformed. Shipped locally; queued for batch deployment. Review: `video-audit/pace-of-change-build-2026-11-03-v12/REVIEW.md`.

**Local release 2026-09-30:** v10 (4:22.40), cache key `20260930ship10`, pill 4 min.
Approved source wording correction, three supporting visuals, final-board framing repair, and
removal of the four-idea preview while preserving the conceptual-map transition. Installed locally;
pending batch deployment. Review: `video-audit/pace-of-change-build-2026-09-30-v10/REVIEW.md`.
The v8 production notes below describe the prior source.

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

**Current reroll package, 2026-11-03:** `gemini-notebook/pace-of-change/PREP-NOTES.md` records the current beat spine, generation instructions, and review requirements. Upload the five files in `gemini-notebook/pace-of-change/upload/` and paste the current `PROMPT.txt` into customization. Save as `Prompts/pace-of-change-reroll.mp4` (or the next unused suffix). The three-roll evaluation and v12 build are complete; this package is retained for future regeneration.

Current boards, in order:
- `pace-of-change-three-years.jpg`
- `pace-of-change-what-speeds-it-up.jpg`
- `pace-of-change-three-future-ideas.jpg`
- `pace-of-change-close.jpg`

The beat spine is: opening hook; four 2023/2026 comparisons; the AI-company race; Why So Fast?; the AI-builds-AI bridge; RSI, AGI, and ASI as three parallel future ideas; the two closing lines. No Automated AI Research card, old status labels, comparison banners, or deleted speed claim. All boards have no visible faces. The current prompt requires four verbatim lines: today's “no,” AI already helping people build better AI, and the two closing lines. Historical v8/v10 notes above describe superseded versions; v12 follows the current lesson.

### big-downside

**Reroll materials ready, 2026-10-09.** The finalized three-idea lesson replaces the six-idea teaching in the existing video. Use `gemini-notebook/big-downside/PREP-NOTES.md`, `PROMPT.txt`, and the six files in its `upload/` folder. The current prompt is 470 words. The jailbreak upload is text-only and retains all teaching text; restore the canonical illustration during editing. Save the next raw generation as `Prompts/big-downside-reroll.mp4`. The package includes the latest safety wording, “They didn’t,” the cheating banner, attempted record concealment, Safety Runs Behind, and the clean two-line close. No video generation or edit has been performed for this revision.

#### Historical production record: earlier six-idea lesson

The records below preserve earlier work. They are not upload instructions for the current reroll.

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
- Prompt: `gemini-notebook/big-downside/PROMPT.txt` (496 words, four blocks)
- Registry: `gemini-notebook/upload-sets.json` → `gemini-notebook/big-downside/` (synced 2026-09-24)
- Canonical folder: `course-assets/big-downside/`
- Boards in lesson order:
  - `big-downside-safety-guardrails.jpg` — upload
  - `big-downside-jailbreak.jpg` — **post-only (faces)**; uploads as
    `gemini-notebook/big-downside/assets/big-downside-jailbreak-faceless.jpg`, the same 1387x1134 board with the photo panel
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

**Final reroll preparation, 2026-11-03:** Use `gemini-notebook/big-upside/PREP-NOTES.md` and `PROMPT.txt`; these supersede earlier generation directions below. Six uploads: current Markdown plus five canonical boards. The 451-word prompt covers the finalized four-example lesson, why protein shapes matter before AlphaFold, the amber cancer board, and the shortened ending. The five-step Find One More Upside lab is page-only. Required narration passages stand alone in the source. Save as `Prompts/big-upside-reroll.mp4` or the next unused reroll name. No new generation or installation has occurred.

**v8 review candidate built 2026-10-23:** `Prompts/big-upside-v8.mp4`, 3:19.567, removes three extra applications and uses the single Helping People Live Better board. AlphaFold, Hassabis, and the closing are retained; the doctor’s judgment sentence now follows Finding Cancer. Review: `video-audit/big-upside-three-examples-v8-2026-10-23/REVIEW.md`. Visual/mechanical checks completed; audio joins still need listening. Not installed or published.

**Current lesson and preparation updated 2026-11-03:** Four benefits, with AlphaFold as the main example. The Demis acknowledgment has been removed. Cancer detection, reading aloud, and flood warnings each have a dedicated section and single-scene editorial board, using the established dimensional object style. The lab is now Find One More Upside: open ChatGPT, start a new chat, enter an interest to personalize the prompt, find a real example, and check its source. V12 now implements this rewrite and is installed locally at cache key `20261103ship12` (3:32.500), commit `50784bfb`, awaiting the authorized batch push. Review and listening limitations: `video-audit/big-upside-build-2026-11-03-v12/REVIEW.md`.

Current upload order: `big-upside-protein.jpg`, `big-upside-cancer.jpg`, `big-upside-reading.jpg`, `big-upside-flood.jpg`, `big-upside-close.jpg`, plus `big-upside.md`. The canonical text, prompt, and registry are the source of truth; the generated bundle is synchronized. Built-in imagegen source art and exact prompts: `output/imagegen/big-upside-four-benefits-2026-11-03/`. Board renderer: `scripts/video/render_big_upside_benefits.py`.

Current beat spine: giant calculator and benefits today; protein shapes and research starting points; AI flags and doctors review; phone reading and everyday access; early flood information and preparation; the four human benefits; the two closing lines. Do not restore the childhood story, quote, timeline, or Nobel encouragement. Distinguish predictions from experimentally established structures, retain human medical decisions, and avoid promising reliable warnings in every case.

**Consistency pass, 2026-11-03:** All four teaching boards now share the same 1600×662 layout: illustration left, two teaching points right. The protein board removes its separate shape panel and gold band; shape explains function in the introductory prose. Cancer art is a neutral abstract scan, without recognizable anatomy. Board titles are A New Scale for Science, Helping Doctors Find Cancer, Reading Everyday Information, and Earlier Flood Warnings. The prose and prompt avoid repeating the board captions. Replacement art and prompts are recorded in `output/imagegen/big-upside-four-benefits-2026-11-03/prompts-v2.json`.

**Copy and color pass, 2026-11-03:** The science board now labels “AlphaFold AI.” The cancer illustration and teaching labels use the course’s amber palette, leaving teal for reading. Flood-warning prose is one paragraph. The summary ends with “These are making a difference in people's lives.” and leads directly to the closing board; the redundant question-and-answer ending is removed. Amber source art and prompt are recorded in `output/imagegen/big-upside-four-benefits-2026-11-03/prompts-v3.json`.

**Historical production records follow.** Their board lists and narration instructions are superseded by the current prompt and registry.

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
- Prompt: `gemini-notebook/big-upside/PROMPT.txt`
- Upload registry: `gemini-notebook/upload-sets.json`; synced bundle: `gemini-notebook/big-upside/`
- Upload boards, in order: `big-upside-protein.jpg`, `big-upside-hassabis-timeline.jpg`,
  `big-upside-examples.jpg`, `big-upside-close.jpg`.
  All are canonical JPGs in `course-assets/big-upside/`; no face variants or post-only boards.

**Beat spine**

1. Giant calculator and fifty-year scientific challenge.
2. Proteins do essential jobs; shape matters. Experiments versus predictions, clearly
   distinguished, and the free resource for research. Roughly 40–50 seconds; no mechanics.
3. Who helped make that happen? Demis, chess and games, studying the brain, DeepMind,
   AlphaFold, free release, Nobel recognition. Tell the story without a roll call of dates.
4. Reach: three million users, over 190 countries, shared 2024 Nobel Prize and quotation.
5. Three examples on one board: Finding Cancer, Reading Aloud, and Flood Warnings.
   Explain each benefit briefly and speak the takeaway once. Doctors retain medical decisions.
6. Answer what good AI does for society, then turn Demis's story toward students using
   their strengths to help people.
7. Two closing lines, with nothing after them.

**Required verbatim lines:** the eleven in the prompt, including the full attributed
Hassabis quotation and the exact experiment/prediction distinction. Read the quotation
in full, word for word; do not paraphrase or omit it. Do not imply laboratory confirmation of all AlphaFold outputs,
automatic medical decisions, approved antibiotic treatment, or guaranteed warnings.

### ai-agents

**Current reroll.** Use the four files in `gemini-notebook/ai-agents/upload/` and paste `gemini-notebook/ai-agents/PROMPT.txt` into the customization box. The source is the saved opening in `lessons/ai-agents.md`.

1. Open with the definition and how the authors used coding agents to build the course. Show the agents editing and testing, then the authors reviewing the lesson.
2. Show **Agents Today** with Coding, Research, Customer Service, and Office Work in card order. For Customer Service, include phone calls, online chat, and the package-tracking example.
3. Move to a drawn scene for the busywork paragraph. Leave the question about workers open.
4. Show **How an Agent Works** with Goal, Plan, Act, Check and the return to Plan. Speak the footer exactly, including the options to finish, retry, or ask for help.
5. Cut directly to the closing board for the two closing lines. The basketball exercise and discussion are on-page activities.

All three JPGs are the current course images. Save the raw roll as `Prompts/ai-agents-reroll.mp4`, using the next unused numbered name if needed.

**Earlier production history**

**Correction approved 2026-09-30:** remove the withdrawn Gemini file-deletion case from lesson, board,
and narration. PocketOS remains the single real case. The original reporter found the Gemini files:
https://github.com/google-gemini/gemini-cli/issues/4586#issuecomment-3125818690.
The v6 review build also corrects the PocketOS animation labels while preserving its drawings.
`scripts/video/build_ai_agents_v6.py`; review in `video-audit/ai-agents-repair-2026-09-30-v6/`.
The raw rolls and pre-v4 donor named in the historical records below no longer exist locally;
v6 uses the hash-verified finished v4. The former v4 source is retained in Git history; v7 supersedes it locally after owner approval.

**Lesson layout updated 2026-09-30 after v6:** the Rogue Agents board removes the inner title,
moves the April 2026 · PocketOS pill above the right-hand paragraph, and puts the agent's quote
in the standard gold takeaway banner. The canonical board and upload kit include this layout;
v7 incorporates it and also removes the universal review-first sentence and its imagery.
Build: `scripts/video/build_ai_agents_v7.py`; review: `video-audit/ai-agents-repair-2026-09-30-v7/`.
The sentence is also removed from the current lesson and generation prompt. v7 is shipped locally on owner approval (20260930ship1, 2:50.40, pill 3 min), queued for batch deployment.

**Historical v4 production record (superseded locally by v7):** `ai-agents.mp4` was **v4, shipped
2026-09-24** on David's approval (cache key 20260924ship1, pill 3 min, 3:07.8): roll 2 base with the old
live video's intro and loop narration, roll 2's everywhere line and roll 1's example line and loop banner, section-level
rings. Build: `scripts/video/build_ai_agents_v4.py`. Record: `video-audit/ai-agents-v4-2026-09-24/REVIEW.md`.
The replaced live video (commit 6cccc758) is kept as `Prompts/ai-agents-live-pre-v4.mp4`, the donor
the v3/v4 builds read.

**Rolls 1-2 and the live video evaluated 2026-09-24** in
`video-audit/ai-agents-evaluation-2026-09-24/REVIEW.md`: roll 1 REPAIR (8/8 verbatim, but drops
the analogy's mistake clause; donor only), roll 2 REPAIR and proposed base (7/8; the loop banner comes
from roll 1 @118.78-130.98 under the loop board), live REROLL (3/8, superseded). Edit plan was awaiting
David's approval (since given, below).
**v2 review candidate built 2026-09-24** on David's approval (both grafts + cut 1; optional "it's
autonomous" cut not taken): `Prompts/ai-agents-v2.mp4` (2:58.4), build
`scripts/video/build_ai_agents_v2.py`, record `video-audit/ai-agents-v2-2026-09-24/REVIEW.md`.
8/8 verbatim lines on the output transcript; transition guard 17/17. Not shipped; joins await David's ear.
**v3 review candidate built 2026-09-24** from David's notes on v2: the live video's intro (0:00-0:38)
replaces v2's opening, section-level rings wherever a card section is spoken (after the live video),
and the live video's loop narration under What an Agent Does (two live sentences omitted, roll 1's banner
line kept): `Prompts/ai-agents-v3.mp4` (3:00.0), build `scripts/video/build_ai_agents_v3.py`,
record `video-audit/ai-agents-v3-2026-09-24/REVIEW.md`. 7/8 verbatim lines (the live intro says
"A chatbot answers, but an agent acts."); transition guard 17/17. Not shipped.
**v4 review candidate built 2026-09-24**: v3 plus the analogy-to-example transition David flagged
(roll 2 "This distinction is exactly why AI agents are suddenly everywhere. They actually do the work."
over its Completed Tasks drawing, then roll 1 "Let's look at a concrete example."):
`Prompts/ai-agents-v4.mp4` (3:07.8), build `scripts/video/build_ai_agents_v4.py`, record
`video-audit/ai-agents-v4-2026-09-24/REVIEW.md`. Transition guard 19/19. **Shipped 2026-09-24.**

### work-changes

**Full reroll prepared November 20, 2026.** The current lesson and boards supersede
all earlier Work Changes generation directions. The resulting version-3-based
v10 is now installed; see the release record below.

**Three uploads reviewed November 20:** `Prompts/work-changes-1.mp4`, `-2.mp4`,
and `-3.mp4`. Content and sampled-frame evaluation recommends version 3, retaining
its narration and repairing the visuals. Full comparison and proposed board plan:
`video-audit/work-changes-three-rolls-2026-11-20/REVIEW.md`. Listening and continuous
motion were not verified in that evaluation. The approved build is recorded below.

**Approved visual edit built:** `Prompts/work-changes-v9.mp4` (4:28.37), using
version 3's unchanged audio. Canonical boards restored, review-checking cutaway
and version-2 school scene inserted, diagram labels simplified, timer removed,
and closing delayed to its narration. Review/build record:
`video-audit/work-changes-v9-2026-11-20/REVIEW.md`. Frame/audio identity checks and
19 scene-splice checks pass. Full playback review remains; not installed or shipped.

**Latest owner-directed revision:** `Prompts/work-changes-v10.mp4` (4:12.90).
Removes the repeated career-preparation sentence and the repeated immediate-learning
sentence, zooms to the assignment banner, and replaces the training-ground and
school shots with purpose-generated photographic scenes. Build and QA record:
`video-audit/work-changes-v10-2026-11-20/REVIEW.md`. All 18 scene-splice checks pass;
the two audio joins still need perceptual listening. David authorized shipping
and pushing after that limitation was disclosed. Installed November 20 at
`course-assets/work-changes/work-changes.mp4`, cache key `20261120ship1`, pill 4 min.
Full continuous playback is not claimed. Public verification is recorded after
the authorized push.

- Page teaching and lab: `lessons/work-changes.md`, matching `index.html`.
- Narration source: `lessons/work-changes-video.md`, derived by
  `scripts/video/prepare_work_changes.py`. It ends at the closing lines, excludes
  the lab, and uses David’s approved spoken time-savings passage.
- Prompt: `gemini-notebook/work-changes/PROMPT.txt`, eight meaning requirements; natural paraphrases are accepted.
- Registry: `gemini-notebook/upload-sets.json`; upload only the four files in
  `gemini-notebook/work-changes/upload/`.
- Save the raw roll as `Prompts/work-changes-reroll.mp4`, or the next unused suffix.
- Refresh/check commands and review criteria: `gemini-notebook/work-changes/PREP.md`.

**Current visual sequence**

1. Your First Assignment: upload the 1600x1506
   `gemini-notebook/work-changes/assets/work-changes-assignment-faceless.jpg`.
   Both photo panels are omitted, while the scenario, titles, purpose lines,
   Before AI / With AI comparisons, spacing, and banner remain intact.
   In the edit, replace it with the exact canonical
   `course-assets/work-changes/work-changes-assignment-short.jpg`.
2. Two Ways AI Changes Work: upload the current
   `course-assets/work-changes/work-changes-automation-and-augmentation.jpg`.
3. Closing: upload `course-assets/work-changes/work-changes-close.jpg`.

The retired Four AI Strengths at Work and How Work Is Changing boards are not
sources for this reroll. The old `work-changes-assignment.jpg` is not the current
assignment board.

**Lesson progression and beat spine**

The lesson moves from changing tasks, through one concrete assignment and the
concepts automate/augment, to the learning opportunities that automation can remove
and what students can do about that now.

1. Finishing school, starting a career, and what changing jobs might mean for you.
   Familiar titles can contain different daily tasks. Recall AI’s useful tasks and
   the value of what you know.
2. Manager’s complete 500-review assignment. Walk Routine Work, then Judgment &
   Decisions. For each, speak the purpose and both Before AI / With AI descriptions.
   Include spot-checking, evaluating suggestions, and presenting your recommendation.
3. Same assignment, same responsibility, different way of working. Leave the board
   for the approved time-savings explanation: no invented hours, weeks, or minutes.
   Preserve the point that more knowledge improves your work.
4. Introduce automate and augment. Explain both with the review-project examples.
   Finish with the name-on-it / own-the-outcome line.
5. A New Problem: routine work has been a training ground. Reading reviews helps
   you learn how customers think, what they care about, and how they describe the
   product. AI can make you productive before it makes you knowledgeable.
6. You might be asked to investigate and recommend before understanding the field
   well enough to judge AI’s suggestions.
7. What can you do? Spend some saved time learning. Read a sample and note your
   observations before AI’s summary, then compare. What can you do today? Learn,
   learn more, and use school.
8. Close with these ideas: “AI is changing the work you’ll do.” Then “Now it’s on you to LEARN.”

**Review priorities**

David’s November 20 clarification: the marked lines need to make the point, not
match verbatim. Judge all eight by meaning, including the closing.

Teach every current board sentence. Keep human judgment in both stages. No
week-to-minutes promise, guaranteed job survival, retired statistics, extra boards,
or lab narration. The comparison and learning response are required teaching,
not optional closing commentary. Exact wording and contractions are not pass/fail requirements. Production labels and
filenames are not spoken. The generated photo-panel-free board is a reference;
use the current page board during editing. Follow the shared Edit Spec for camera
and highlights after the new narration has been reviewed.

**Historical record:** the September 25 v3 build and earlier reroll findings are
recorded in `video-audit/work-changes-v3-2026-09-25/REVIEW.md` and
`video-audit/work-changes-review-2026-09-24/REVIEW.md`. Those timing and teaching
plans are historical, not instructions for the November 20 reroll.

### where-ai-lives

**Full reroll prepared November 19, 2026.** Use the five files in `gemini-notebook/where-ai-lives/upload/` and paste its sibling `PROMPT.txt` into video customization. Save the raw roll as `Prompts/where-ai-lives-reroll.mp4` (use the next unused suffix for another take).

The opening follows a spreadsheet from the learner’s laptop to the cloud. The calculations behind an AI reply lead to the server hall and then to the people who live nearby. The previous video uses a different math example and closing. Its production record is in `video-audit/where-ai-lives-lesson-update-2026-10-09/`.

- Markdown: Board 2's sentences, "The scale varies by facility." and the who-pays sentence now each
  stand alone on their own line (wording unchanged).
- Prompt: six Board 2 sentences and the scale line join the verbatim list (fourteen lines); the
  spine demands every Board 2 sentence, forbids "daily" for water, says token not word, and says
  "Teach each point once"; "massive", "sheer" and "environment" join the avoid list; drawn scenes
  carry no people or faces and no numbers the Markdown lacks. 497 words.
- **Rolls 3 and 4 (revised kit) evaluated 2026-09-24**, same REVIEW.md: roll 3 REPAIR (first roll
  to teach Board 2 fully; cut two bridges, graft roll 1's exact close at 4:32.08–4:36.84), awaiting
  David's approval; roll 4 REROLL (Board 2 compressed again).
- **v3 candidate built 2026-09-24** on David's approval: `Prompts/where-ai-lives-v3.mp4` (3:43.1), from roll 3 with the
  two cuts and roll 1's close. Build `scripts/video/build_where_ai_lives_v3.py`; record
  `video-audit/where-ai-lives-v3-2026-09-24/REVIEW.md`. Awaiting David's listening (close seam 3:33.8) and review; not shipped.
- **v4 candidate built 2026-09-24**: `Prompts/where-ai-lives-v4.mp4`, v3 with David's updated neighbors-board illustrations
  (asset replaced in place; upload folder re-synced). Record `video-audit/where-ai-lives-v4-2026-09-24/REVIEW.md`. **Shipped 2026-09-24 on David's approval**
  as live `course-assets/where-ai-lives/where-ai-lives.mp4` (cache key 20260924ship1, pill 4 min, 3:43.1, sha256 239d5a26ee58…).
- Fallback if the reroll also fails Board 2: roll 1 with the duplicate cut (2:18.92 → 3:17.40) plus
  live-video grafts for electricity, water and jobs (timestamps in the review).

- Markdown: `lessons/where-ai-lives.md`
- Prompt: `gemini-notebook/where-ai-lives/PROMPT.txt`
- Upload registry: `gemini-notebook/upload-sets.json`
- Canonical folder: `course-assets/where-ai-lives/`
- Boards in lesson order (no faces; all upload):
  - `where-ai-lives-math.jpg` — upload
  - `where-ai-lives-data-center.jpg` — upload (photograph of a server hall; the one distant figure walks
    away from the camera, so no face is visible)
  - `where-ai-lives-physical-footprint.jpg` — upload
  - `where-ai-lives-close.jpg` — upload

**Beat spine**

1. Follow a spreadsheet from Excel on a hard drive to Google Sheets on a phone. Define the cloud, then ask why March expenses jumped to introduce the math behind a reply.
2. Teach all three panels as estimates for the same example model. One output token takes about 100 billion calculations. At 100 output tokens (roughly 75 English words), the estimate reaches 10 trillion. At 1,000 output tokens across the conversation (roughly 750 words), it reaches 100 trillion.
3. Define compute, scale from one question to millions of people, and ask “Where does all that math happen?”
4. Define a data center and its servers, explain what GPUs do, and mention Nvidia. Introduce the scale of large facilities. Show the server hall and use the person in the aisle to explain what the racks hold. Go directly to the question about neighbors.
5. Living Near a Data Center: the projection of about 12% of U.S. electricity by 2030 and the effect on bills,
   fresh water to replace evaporation even with reuse, fans running around the clock, and fewer jobs after construction.
6. Follow the neighbors board with the short paragraph on additional electricity, water reuse and chip efficiency.
7. Go straight to the closing board and speak its two lines.

**Required verbatim lines:** the ten in the prompt (the per-token estimate, the compute definition, six neighbors-board sentences, and the two closing lines).

**Banned words:** leverage, framework, utilize, sustainability, carbon, emissions, environmental,
staggering; no screen/board-position references; no forecasts beyond the lesson; no town or company beyond
the Markdown; never tell anyone to use AI less. Highlighting call for the edit stands from 2026-09-18:
whole-card highlights on the neighbors board, none on the warehouse photograph or the
close. The retired fixed training total, the 2,000-word chat claim, the separate electricity qualifier
and the nuclear-project examples stay removed; no Hit Send board is used.

### where-will-ai-land

**Full reroll refreshed November 17, 2026.** Progression: Hanoi makes the gap between expected and actual results concrete; four examples broaden that idea; the AI comparison explains why neither camp can know exactly where AI will land; the close gives a reason to stay curious.

**Notebook sources and handoff**

- Upload the three files in `gemini-notebook/where-will-ai-land/upload/`: current narration Markdown, Beyond the Plan, and the two-line close. Both JPGs are canonical course boards with no visible faces; no faceless variants are needed.
- Paste `gemini-notebook/where-will-ai-land/PROMPT.txt` into video customization. Do not upload this kit or the prompt as sources.
- Save the raw roll as `Prompts/where-will-ai-land-reroll.mp4`, using the next unused suffix for subsequent takes. Never overwrite a raw roll or the installed video.

**Beat spine**

1. Open directly with “In 1902, Hanoi had a problem.” No AI introduction, title card, or Hanoi’s Rat Bounty kicker. Explain the sewer problem, payment for tails, and officials’ one-tail/one-dead-rat assumption.
2. Let thousands of tails arrive before revealing living tailless rats. Explain clipping, release, and continued breeding. Give the dead-rat/live-rat contrast room to land, then rat farms, stopped payments, a pile of tails, and more rats.
3. Use “In these four stories, compare what people expected with what happened next.” The board is **Beyond the Plan**, in this order: **Text Messaging, GPS, Cane Toads, Wider Highways**. Teach each original purpose followed by its **Unexpected Result**, using the current board’s separate paragraphs and labels.
4. SMS: early one-way network messages to subscribers became everyday communication, helped by young people. GPS: military positioning/navigation grew into rides, deliveries, and timing that supports phone networks, banks, and power grids. Cane toads: barely controlled sugarcane pests, poisoned native animals, and spread across the country. Highways: $2.8 billion spent to ease congestion; rush-hour trips grew 30%–55% longer between 2011 and 2014; more road space encouraged more driving. The dates are both after the expansion, not a preconstruction/postconstruction comparison.
5. Only after all four stories, deliver **The Future of AI** comparison from the source. Optimists and Worriers could be wrong; the results could be very different from expectations. Continue with the possibility that AI’s biggest effect, good or bad, is still unimagined, then “That uncertainty gives us a reason to keep paying attention.”
6. End on the close: “Some of the biggest results are the ones nobody predicted.” / “That’s the best reason to stay curious.” Nothing follows.

**Reroll review and production continuity**

- Judge complete meaning and natural narration joins. Faithful paraphrases of wording targets are acceptable under David’s instruction; do not reject a take solely for a wording change that preserves the point.
- Use one consistent Notebook narrator. Do not add an external synthetic voice or restore older mismatched narration. The approved `where-will-ai-land-5` 0:54–1:13 one-tail/tailless-rat reveal remains a possible edit source if needed; it is not an upload source or an automatic graft. Audition any proposed join before using it.
- Keep the purpose/result contrasts audible without the screen. “It helps” is a natural spoken connective for GPS’s printed “Helps”; do not change the printed board to force a verbatim read.
- Reveal tailless rats at the correct moment and show the pile of tails near the story’s end. Give the transition into four examples and the later AI comparison a complete sentence and natural cadence.
- Keep Online Shopping, Flying Cars, “Its creators…” in SMS, farm machinery in GPS, the deleted AI question, and the deleted practical-advice paragraph out. “Safety Runs Behind” remains with Big Downside.
- This is preparation for a new roll. The installed v10 does not reflect these lesson revisions; do not describe it as updated by syncing this bundle.

**Verification sources (not uploaded or narrated)**

- SMS early applications and two-way design: Friedhelm Hillebrand et al., *Short Message Service (SMS): The Creation of Personal Global Text Messaging* (2010), https://www.academia.edu/17311526/Friedhelm_Hillebrand_Short_Message_Service_SMS_The_Creation_of_Personal_Global_Text_Messaging
- GPS timing applications: https://archive.gps.gov/applications/timing/
- Katy Freeway project and $2.8 billion cost: https://www.fhwa.dot.gov/ipd/project_profiles/tx_katy_freeway.aspx
- 2011–2014 travel-time comparison: https://cityobservatory.org/reducing-congestion-katy-didnt/
- Road capacity and driving: https://www.nber.org/papers/w15376

## Changed teaching and scene directions

**Superseded 2026-09-23.** All nine lessons now have rebuilt kit entries above, on the 2026-09-20
recipe, and each one's teaching requirements and guardrails live in its own Markdown, prompt and beat
spine. The 2026-09-18 bullets that used to sit here are history, not instructions. Wider Highways was removed on 2026-10-23 and restored with revised wording on 2026-11-17; the current lesson entry above governs.

## Prep versus current page

Under the current recipe the Markdown matches the page: nothing is added to the narration that the
page and its boards do not teach, and a guardrail belongs in the prompt rather than in the narration.
Where a kit would once have clarified a page statement in the narration, the clarification now sits in
the prompt as a negative and the page question is written down in that lesson's entry. Research links,
source records and citations are verification-only and are never narrated. The hidden `md-source` divs
in `index.html` are stale; the board images and the visible page are the sources.

## Production handoff

Follow `scripts/video/PREPARATION.md`, `scripts/video/README.md`, `scripts/video/EDIT-SPEC.md`, and `scripts/video/NARRATION-REVIEW.md`.

- Each prompt stands alone and is under 500 words. Paste it in customization; do not upload it as lesson content.
- Use drawn scenes rather than stock photos for generated visuals, printed labels, no extra chapter/lesson-number cards, and unchanged, complete supplied boards.
- Boards with visible faces are never uploaded. Each one has a faceless upload variant in `gemini-notebook/<slug>/assets/`, named in its kit entry and recorded in the registry as the `covers` of the canonical board; the canonical board replaces it in the edit. Any teaching that lives only inside a removed photo is spoken from the Markdown. Never recreate the faces.
- Speak the exact two closing lines. No narration follows them. The standard course closing visual is inserted in editing.
- The watermarking toggle does not take effect (the build removes the mark). Save each raw roll under the next unused name.
- Review changed scene directions before generation. During evaluation, present the proposed box-highlighting plan before edits, under the shared specs. Full-card versus subsection highlighting depends on the spoken explanation; source preparation does not preapprove timings or zooms.
- Use natural transitions. Decide pauses selectively during editing; do not automatically add one second at each idea or board.
- Check actual narration after the roll. These sources do not establish a KEEP/REPAIR/REROLL verdict or a shipping status for an existing video.
