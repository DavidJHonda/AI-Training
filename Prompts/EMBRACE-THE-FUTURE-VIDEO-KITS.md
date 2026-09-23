# Embrace the Future Video Kits

> **Method note (2026-09-21):** per-lesson entries below dated before 2026-09-20 describe the previous preparation method (Scene/Takeaway labels, withheld face boards with "reserved" narration, prompts without a verbatim list, beat spine, or VOICE block). Rebuild a lesson's Markdown and prompt to the "Prepare a new lesson" procedure in `Prompts/README.md`, add it to `Prompts/upload-sets.json`, and run the sync before rolling it. Entries that say they are on the 2026-09-20 recipe are current.

Prep updated 2026-09-18. This guide covers source preparation, not the status of existing videos. No video was generated, edited, or deployed in this pass.

Use current Markdown in `lessons/`, canonical JPGs in each `course-assets/` lesson folder, and the matching prompt and upload checklist in `Prompts/`. Markdown contains the spoken teaching in lesson order; it is not a script for reading production labels. Upload selected JPGs separately. There are no upload JPG copies in `lessons/` or `illustrations/`.

## Current source sets

All paths below are repository-relative. Each named prompt and checklist is in `Prompts/`.

### opener-embrace


**Opener video v4 SHIPPED 2026-09-22** (cache key 20260922ship5, pill 3 min, 2:47): the live narration with the What Everyone's Saying card recaptured from the page at the Work opener's scale (full view, gold line rings, the live's paired-quote states) and the map-introduction sentence replaced by the Understand opener's "This roadmap shows what we'll explore in this section." (audio-only graft, +0.4 dB); the map now arrives on that line. Review: `video-audit/opener-embrace-repair-2026-09-18/` (Build v4 section).
- Markdown: `lessons/Opener-Embrace.md`
- Prompt: `opener-embrace-video-prompt.txt`
- Upload checklist: `opener-embrace-upload-files.txt`
- Canonical folder: `course-assets/embrace-the-future-opener/`
- Boards in lesson order:
  - `embrace-the-future-opener-voices.jpg` — upload
  - `embrace-the-future-opener-edge-of-the-map.jpg` — upload
  - `embrace-the-future-opener-section-map.jpg` — upload
  - `embrace-the-future-opener-close.jpg` — upload

### loudest-voices

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `loudest-voices.mp4` is v5, shipped
2026-09-18 under the old method (best-of of rolls 1 and 2; both rolls since deleted). Evaluated
2026-09-23 against the current system: **REROLL** — narration misses "None of them has a simple,
one-sided view", never speaks the banner, paraphrases the habits line, narrates board furniture
("as the bottom right panel notes"); pictures hold the boards 46/56/79 s and carry two invented charts.
Record: `video-audit/loudest-voices-evaluation-2026-09-23/REVIEW.md`. Reroll pending David's approval
of the beat spine below.

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

**Kit rebuilt 2026-09-23 on the 2026-09-20 recipe.** Live `pace-of-change.mp4` is v2, shipped
2026-09-18 under the old method (roll 2 base, AGI beat from the earlier course video, closing lines
from roll 1; both rolls since deleted). Evaluated 2026-09-23 against the current system: **narration
KEEP, pictures REROLL** — every point RICH/TAUGHT and the closing lines exact, but the four boards are
held 77/45/85 s and every Notebook span is an invented chart, a release timeline, a chapter card or a
restatement of the future-ideas boards, so Edit Spec 8b has nothing to break the holds with. Plan: roll
on this kit; if the live narration still wins beat by beat, use the new roll's drawings under the live
audio (8b, other rolls of the same lesson). Record:
`video-audit/pace-of-change-evaluation-2026-09-23/REVIEW.md`. Reroll pending David's approval of the
beat spine below.

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

- Markdown: `lessons/big-downside.md`
- Prompt: `big-downside-video-prompt.txt`
- Upload checklist: `big-downside-upload-files.txt`
- Canonical folder: `course-assets/big-downside/`
- Boards in lesson order:
  - `big-downside-safety-guardrails.jpg` — upload
  - `big-downside-jailbreak.jpg` — post-production only; reserve narration
  - `big-downside-policy-puppetry.jpg` — upload
  - `big-downside-voice-cloning.jpg` — upload
  - `big-downside-goal-test.jpg` — upload
  - `big-downside-safety-timeline.jpg` — upload
  - `big-downside-close.jpg` — upload

### big-upside

- Markdown: `lessons/big-upside.md`
- Prompt: `big-upside-video-prompt.txt`
- Upload checklist: `big-upside-upload-files.txt`
- Canonical folder: `course-assets/big-upside/`
- Boards in lesson order:
  - `big-upside-protein.jpg` — post-production only; reserve narration
  - `big-upside-hassabis-timeline.jpg` — upload
  - `big-upside-scientific-discovery.jpg` — upload
  - `big-upside-practical-help.jpg` — upload
  - `big-upside-close.jpg` — upload

### rise-of-agents

- Markdown: `lessons/rise-of-agents.md`
- Prompt: `rise-of-agents-video-prompt.txt`
- Upload checklist: `rise-of-agents-upload-files.txt`
- Canonical folder: `course-assets/rise-of-agents/`
- Boards in lesson order:
  - `rise-of-agents-gps.jpg` — post-production only; reserve narration
  - `rise-of-agents-chatbot-vs-agent.jpg` — upload
  - `rise-of-agents-agent-loop.jpg` — upload
  - `rise-of-agents-rogue.jpg` — upload
  - `rise-of-agents-close.jpg` — upload

### work-changes

- Markdown: `lessons/work-changes.md`
- Prompt: `work-changes-video-prompt.txt`
- Upload checklist: `work-changes-upload-files.txt`
- Canonical folder: `course-assets/work-changes/`
- Boards in lesson order:
  - `work-changes-four-shapes-of-ai-work.jpg` — upload
  - `work-changes-assignment.jpg` — post-production only; reserve narration
  - `work-changes-automation-and-augmentation.jpg` — upload
  - `work-changes-productivity-and-possibilities.jpg` — upload
  - `work-changes-close.jpg` — upload

### data-centers

- Markdown: `lessons/data-centers.md`
- Prompt: `data-centers-video-prompt.txt`
- Upload checklist: `data-centers-upload-files.txt`
- Canonical folder: `course-assets/data-centers/`
- Boards in lesson order:
  - `data-centers-data-center.jpg` — upload
  - `data-centers-physical-footprint.jpg` — upload
  - `data-centers-meeting-demand.jpg` — upload
  - `data-centers-close.jpg` — upload

Scene plan (2026-09-18, revised): assumed model calculation → compute for millions of people → warehouse scale → four community effects → three responses to demand → personal perspective → exact close. The page, Markdown, and prompt share the approved opening. No Hit Send board is used. Review highlighting before video edits: whole-card highlights on the community and demand boards, and no highlight on the warehouse illustration or close.

### unexpected-results

- Markdown: `lessons/unexpected-results.md`
- Prompt: `unexpected-results-video-prompt.txt`
- Upload checklist: `unexpected-results-upload-files.txt`
- Canonical folder: `course-assets/unexpected-results/`
- Boards in lesson order:
  - `unexpected-results-plans.jpg` — upload
  - `unexpected-results-close.jpg` — upload

## Changed teaching and scene directions

- Opener: show the navy “What Everyone’s Saying” board with its four quotes, then the existing map illustration and three-part section map. The added opening-board label does not renumber the existing Board 1 and Board 2 references.
- Loudest Voices and Pace of Change: superseded 2026-09-23 by their rebuilt kit entries above (the guardrails now live in each prompt).
- Big Downside: preserve the revised cyberattack account: reduced safeguards, about 1,200 communicating agents versus about 700 attacking, and attempted record alteration. Cards remain Assignment → Agents Joined Forces → Attack Spread. Keep the incident narration continuous. Research links are verification-only.
- Big Upside: teach proteins once, then Hassabis’s timeline once, then the two three-card boards. The timeline IS on the current lesson and IS uploaded. Preserve all six examples, scientific qualifications, quotation, personal encouragement, and closing lines. The prompt is under 500 words without dropping these requirements.
- Rise of Agents: 30 points, 50 clips. Narrate review and approval BEFORE publishing. Explain that an agent loop may stop, fail, or need help. Preserve the four-step loop and both rogue-agent stories.
- Work Changes: keep the full before/after assignment and the automate/augment connection. Speak “in one study” and “certain tasks” with the productivity percentages.
- Data Centers (lesson and prep revised 2026-09-18): the approved opening assumes one trillion weights per generated token, roughly two calculations per weight, and 1,000 generated tokens (around 750 words), yielding about two quadrillion calculations. Preserve the assumption within the explanation, without a separate caveat paragraph. The retired fixed training total and 2,000-word chat claim stay removed. Use the warehouse illustration, community-impact board, Meeting the Demand board, and close. Use “U.S. data centers” for the electricity figures and distinguish additional supply from efficiency. The separate electricity qualifier and nuclear-project examples were removed from both page and narration source.
- Unexpected Results: retain the rat story and four outcomes. Add the general explanation that extra road space can attract more driving, without treating it as proof of the entire Houston travel-time change. The supporting research citation is verification-only.

## Prep versus current page

The original batch pass updated prep materials only. Data Centers subsequently received the approved page and board update described above. The prep still clarifies statements present in page prose or board wording for Rise of Agents’ unconditional loop and publishing shorthand (the Pace of Change release generalization was reverted to the page sentence on 2026-09-23 under the Markdown-matches-the-page rule; see its entry). Narration should use the corrected Markdown; do not restore these older statements from screenshots. These page/board differences remain for a separate lesson edit, not a silent source reversion.

## Production handoff

Follow `Prompts/README.md`, `scripts/video/README.md`, `scripts/video/EDIT-SPEC.md`, and `scripts/video/NARRATION-REVIEW.md`.

- Each prompt stands alone and is under 500 words. Paste it in customization; do not upload it as lesson content.
- Use drawn scenes rather than stock photos for generated visuals, printed labels, no extra chapter/lesson-number cards, and unchanged, complete supplied boards.
- Visible-face exclusions are explicit in each checklist. Keep their narration and insert the canonical image in editing. Never recreate the faces.
- Speak the exact two closing lines. No narration follows them. The standard course closing visual is inserted in editing.
- The watermarking toggle does not take effect (the build removes the mark). Save each raw roll under the next unused name.
- Review changed scene directions before generation. During evaluation, present the proposed box-highlighting plan before edits, under the shared specs. Full-card versus subsection highlighting depends on the spoken explanation; source preparation does not preapprove timings or zooms.
- Use natural transitions. Decide pauses selectively during editing; do not automatically add one second at each idea or board.
- Check actual narration after the roll. These sources do not establish a KEEP/REPAIR/REROLL verdict or a shipping status for an existing video.
