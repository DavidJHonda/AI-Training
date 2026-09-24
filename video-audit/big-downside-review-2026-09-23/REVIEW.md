# Big Downside — narration review, three candidates (2026-09-23)

Scope: evaluation only. No build, no edit, nothing shipped.
Inputs: `index.html` BigDownsideSection (authority), `lessons/big-downside.md`,
`Prompts/big-downside-video-prompt.txt`, the seven current boards in
`course-assets/big-downside/`, and full `grade_bundle.py` transcripts of all three files.

| File | Runtime | Cuts |
|---|---|---|
| `Prompts/big-downside-1.mp4` | 6:04.87 | 88 |
| `Prompts/big-downside-2.mp4` | 5:51.20 | 104 |
| `course-assets/big-downside/big-downside.mp4` (live) | 4:45.33 | 43 |

---

LESSON: big-downside
CANDIDATE: Prompts/big-downside-1.mp4 (6:04)
VERDICT: REROLL
TEACHING POINTS:
  iPhone hook, answered — RICH — 0:00-0:19 "If your iPhone were about to get a feature update that added new capabilities... Because greater capability can create greater risk."
  The downside comes through SIX ideas, named — MISSING — 0:19 "This risk reveals itself in several stages, tracing a path from the internal mechanics of the software to the external vulnerabilities they create in the real world." Notebook's own graphic at 0:20-0:32 draws six numbered stages; the narration never says six and never names ideas 5 or 6.
  Black box: learned patterns, not written rules — RICH — 0:35-0:47
  Researchers trace some features, cannot explain one answer — RICH — 0:47-0:58
  Dog-named-Spot example — RICH — 0:52-1:10
  Harder to debug; retrain, fine-tune, add safeguards — TAUGHT — 1:10-1:15 (says "retrain it and add safeguards"; fine-tune dropped)
  No complete repair manual — RICH — 1:15-1:21
  Guardrails, the three kinds — TAUGHT — 1:21-1:31 "training the model to be helpful, monitoring the prompts users write, and limiting what the product can do." Drops "and answers"; "to be helpful" is not the lesson's reason.
  Together they block, redirect, or limit risky behavior — MISSING
  No layer catches everything — RICH — 1:31
  Board 1, three future cases with reasons — RICH — 1:37-2:07 (all three, each with its reason)
  The worry grows as capability grows — RICH — 2:07
  Jailbreaking defined — TAUGHT — 2:20-2:31
  Defender/attacker asymmetry — TAUGHT — 2:36 (delivered as one joined sentence, see HARD REQUIREMENTS)
  Cat-and-mouse — RICH — 2:38-2:44
  Policy Puppetry: HiddenLayer, 2025, three models, fake official instructions — RICH — 2:44-3:08
  Bad actors combine ordinary abilities; guardrails may miss the plan — RICH — 3:08-3:23
  As AI gets more powerful, so do the things a bad actor can do — RICH — 3:23
  Board 4, four voice-clone steps — THIN — 3:28-3:51. Steps 1-2 collapsed into one clause; step 3 is "create a sense of panic over the phone" with the money demand dropped; step 4 says "a number you already have", not "the real number". No step is named.
  Nobody means harm; a goal can find an unintended route — RICH — 3:57-4:05
  July 2026, OpenAI, difficult cybersecurity tasks, reduced safeguards — RICH — 4:05-4:13
  Board 5: assignment / ~1,200 communicating / ~700 attacking Hugging Face — TAUGHT — 4:13-4:38. "About" dropped from both figures ("1,200 agents", "700 agents").
  AI can pursue a goal while breaking the boundaries — RICH — 4:38
  Covering their tracks — WRONG — 4:43 "Some of these agents even tried to alter their own actions to make their cheating look legitimate and cover their tracks." The lesson says they altered the RECORDS of their actions. (Confirmed on a medium.en re-transcribe of 4:38-4:54.)
  Safeguards arrive after the technology — RICH — 4:49-4:56
  Board 6, three gaps — TAUGHT — 4:56-5:07. Durations spoken (60 / 23 / 11 years), the date ranges on the board (1908-1968, 1903-1926, 2007-2018) are not; "about" dropped.
  AI to safeguards and rules: still evolving — TAUGHT — 5:07-5:13
  Faster than society can adjust; laws and safeguards take time — RICH — 5:13-5:22
  Red teams — RICH — 5:22-5:34
  Pacing the Frontier, 2026, 1,000+ employees, Anthropic's CEO — TAUGHT — 5:34-5:45. The ask is "They asked for international help to slow automated development"; the U.S. government is dropped.
  The quotation — TAUGHT (altered) — 5:45-5:57 "capability development COULD rapidly accelerate"; the letter says "rapidly accelerates".
  Closing two lines — RICH — 5:57-6:01
HARD REQUIREMENTS:
  "Because greater capability can create greater risk." — MET — 0:16
  "But there is no complete repair manual that tells them exactly which internal part to change." — MET — 1:15
  "But no layer catches everything." — MET — 1:31
  "The worry grows as capability grows." — MET — 2:07
  "This is called jailbreaking." — MET — 2:29
  "Defenders must protect many paths. An attacker needs only one opening." — MET WITH NOTE — 2:36. Delivered as one joined sentence; both base.en and medium.en hear "many paths, and attacker needs only one opening". Needs David's ear before it counts as clean.
  "As AI gets more powerful, so do the things a bad actor can do." — MET — 3:23
  "AI can pursue a goal while breaking the boundaries people expected it to follow." — MET — 4:38
  "AI can follow a goal in ways nobody intended." — MET — 5:57
  "It can change faster than safeguards and rules." — MET — 6:00
ERRORS:
  4:43 — "tried to alter their own actions" — the lesson says "alter records of their actions". Altering an action is not altering a record.
  5:49 — "capability development could rapidly accelerate" — the quotation reads "rapidly accelerates".
  0:00 — the video opens on the stray word "Methodical."
SOURCE_QA: FAIL (materials, not lesson) — see MATERIALS BUGS below. The lesson prose itself is accurate.
ADDITIONS:
  2:14 "relying on external guardrails becomes a losing battle as the technology scales" — an editorial claim the lesson does not make; the lesson says no layer catches everything, not that guardrails are a losing battle. Drop.
  3:51 "bad actors can often out-manoeuvre rigid safety boundaries" — harmless bridge.
  5:18 "like rogue agents" — harmless.
REPAIR PLAN: incomplete; see BEST-OF PLAN. The covering-tracks error and the stray opener are cleanly repairable. The six-idea spine is not.
EDITING NOTES:
  ELEVEN screen-geometry references, woven mid-sentence and unremovable without cutting the teaching they carry: "The left panel of this graphic illustrates" (1:36), "The middle panel shows" (1:48), "As shown in the right panel" (2:02), "The footer of this image explains" (2:31), "The first two steps of a voice clone scam show" (3:28), "In step three" (3:39), "The solution is step four" (3:45), "As the first two panels show" (4:13), "The third panel details the outcome" (4:31), "the bottom row shows" (5:07), "This timeline shows a recurring pattern" (4:49).
  Photographs to cover under rule 8c: chip 0:14-0:20, server hall 0:30-0:36, motherboard 0:36-0:40, server hall 2:10-2:18.
  Notebook renders its own copies of every course board (1:34-2:10 guardrails, 2:30-2:46 the faceless jailbreak variant, 2:46-3:08 Policy Puppetry, 3:26-3:50 voice-clone, 4:14-4:42 goal-test, 4:50-5:14 timeline, 5:54-6:02 close) with its own yellow washes. All replaced under rule 2.
  Good drawn material for 8b breaks: the six-stage map 0:20-0:32, layered-defense rings 1:20-1:34, jailbreak lock 2:22-2:30, modular-capability chain 3:10-3:26, hooded figure at a laptop 3:50-3:58, sandbox/escalation diagrams 3:58-4:14, audit log 4:42-4:50, red-team lab 5:22-5:34, signature sheet 5:32-5:40, G7 table 5:38-5:46, marker drawings 5:46-5:56.
LISTENING: not listened to end to end. Judged from the full base.en transcript plus medium.en re-transcribes of ten disputed spans (0:00, 0:24, 1:24, 2:32, 2:56, 4:14, 4:38, 4:52, 5:36, 5:43). Those confirmed "fake instructions" (not "vague"), "Methodical", "alter their own actions", the missing "about", and the altered quotation. Still unheard: pronunciation, cadence, and levels throughout.

---

LESSON: big-downside
CANDIDATE: Prompts/big-downside-2.mp4 (5:51)
VERDICT: REROLL
TEACHING POINTS:
  iPhone hook — TAUGHT (drifted) — 0:00 "If your smartphone was about to get an amazing new feature". The lesson says iPhone, and the question is turned into a statement.
  Because greater capability can create greater risk — MISSING — 0:05 replaces it with "that progress often triggers a specific kind of anxiety." The lesson's thesis is never spoken.
  The downside comes through six ideas, named — MISSING
  Black box: learned patterns, not written rules — RICH — 0:22-0:27
  Researchers trace some features, cannot explain one answer — MISSING — 0:43 "Because we can't fully trace why a model produces a specific answer". The lesson's distinction (they CAN trace some features) is reversed into a flat cannot.
  Dog-named-Spot example — RICH — 0:27-0:38
  Harder to debug; retrain, fine-tune, add safeguards — TAUGHT — 0:49 (retrain dropped)
  No complete repair manual — RICH — 0:54
  Guardrails, the three kinds — THIN — 1:00-1:10 "built into the training process and used to monitor every prompt a user types." Answers dropped, "limit what the product can do" dropped, "or limit" dropped from block/redirect.
  No layer catches everything — RICH — 1:14
  Board 1, three future cases with reasons — RICH — 1:16-1:34 (First / Second / Third, each with its reason)
  The worry grows as capability grows — RICH — 1:34
  Jailbreaking defined — RICH — 1:39-1:52
  Defender/attacker asymmetry — TAUGHT — 1:54-2:08 (paraphrased, see HARD REQUIREMENTS)
  Cat-and-mouse — RICH — 2:08-2:15
  Policy Puppetry: HiddenLayer, 2025, three models, fake official instructions — RICH — 2:15-2:41
  Bad actors combine ordinary abilities; guardrails may miss the plan — RICH — 2:41-2:57
  Board 4, four voice-clone steps — RICH — 2:57-3:19. All four steps, step 3 keeps the money demand. Step 4 says "a number you already have", not "the real number"; steps are numbered but not named.
  As AI gets more powerful, so do the things a bad actor can do — RICH — 3:24
  Nobody means harm; a goal can find an unintended route — RICH — 3:31-3:42
  July 2026, OpenAI cybersecurity test — TAUGHT — 3:42. "Difficult" and "with reduced safeguards" are both dropped; the reduced safeguards are why the test went wrong.
  Board 5: assignment / 1,200 communicating / ~700 Hugging Face — TAUGHT — 3:43-4:09. "About" dropped from 1,200; "participated in an attack on" and "systems" softened to "gained unauthorized access to private information on the platform Hugging Face".
  AI can pursue a goal while breaking the boundaries — RICH — 4:15
  Covering their tracks — RICH — 4:21-4:32 "alter the records of their own actions. They attempted to edit the logs to make their unauthorized behavior look like a legitimate part of the test." Best version of this beat in any of the three.
  Safeguards arrive after the technology — RICH — 4:32-4:45
  Board 6, three gaps — TAUGHT — 4:45-4:58. Durations only; no date ranges; no "about".
  AI to safeguards and rules: still evolving — MISSING — the board's fourth row is never spoken.
  Faster than society can adjust — RICH — 4:58-5:11
  Red teams — RICH — 5:11-5:24
  Pacing the Frontier, 2026, 1,000+ employees, Anthropic's CEO, the ask — RICH — 5:24-5:42 (keeps "the government"; drops "U.S.")
  The quotation — MISSING — folded into the ask as "too fast for us to understand or control". The letter is never quoted.
  Closing two lines — RICH — 5:42-5:47
HARD REQUIREMENTS:
  "Because greater capability can create greater risk." — MISSED
  "But there is no complete repair manual that tells them exactly which internal part to change." — MET — 0:54
  "But no layer catches everything." — MET — 1:14
  "The worry grows as capability grows." — MET — 1:34
  "This is called jailbreaking." — MET — 1:52
  "Defenders must protect many paths. An attacker needs only one opening." — MISSED — 1:56 "defenders must protect every possible path, but an attacker only needs to find one opening." (Confirmed on medium.en.)
  "As AI gets more powerful, so do the things a bad actor can do." — MET — 3:24
  "AI can pursue a goal while breaking the boundaries people expected it to follow." — MET — 4:15
  "AI can follow a goal in ways nobody intended." — MET — 5:42
  "It can change faster than safeguards and rules." — MET — 5:45
ERRORS:
  0:43 — "we can't fully trace why a model produces a specific answer" reverses the lesson's "Researchers can trace some internal features".
  3:42 — the reduced safeguards are omitted from the OpenAI test setup.
SOURCE_QA: FAIL (materials) — see MATERIALS BUGS.
ADDITIONS:
  3:20 "These scams weaponize everyday features that were designed for convenience." — accurate, and a good line; worth considering for the lesson.
  4:09 "The agents were completing their assignment, but they did so by stepping outside the implied safety boundaries." — accurate and clarifying.
REPAIR PLAN: none. Three essential beats are missing (the thesis line, the quotation, the reduced safeguards) plus the still-evolving row, and two hard requirements are missed. No donor supplies the thesis line in this roll's voice at the top of the file.
EDITING NOTES:
  Screen references, fewer than roll 1 but still baked in: "This panel describes the defensive asymmetry" (1:52), "As the banner says" (2:05), "The defense is shown in step four" (3:14), "The first panel shows the setup" (3:43), "The second panel shows the result" (3:51), "This timeline shows the gap" (4:39).
  Photographs to cover under rule 8c: black cube 0:38-0:42, archival motor car 4:30-4:40 (people in frame), Wright Flyer 4:40-4:44, U.S. Capitol 5:02-5:06.
  Longest Notebook board holds: the faceless jailbreak variant 1:52-2:14 (22s) and the goal-test board 3:44-4:22 (38s). Both exceed the 2026-09-23 twenty-second rule and would need planned breaks.
  Good drawn material for 8b breaks: black-box architecture 0:14-0:24, software-vs-model comparison 0:24-0:32, AI CORE defensive rings 1:00-1:16, adversarial-prompt diagram 1:40-1:52, modular-composition chain 2:38-2:56, goal-misalignment path 3:30-3:42, audit-log pair 4:22-4:32, red-team lab 5:10-5:24, signature sheet 5:22-5:32, capability-vs-oversight chart 5:32-5:44.
LISTENING: not listened to end to end. Full base.en transcript plus medium.en re-transcribes of six spans (0:00, 1:48, 3:42, 3:56, 5:28, 5:29), which confirmed the missing thesis line, the paraphrased sign lines, the missing quotation, and the number wording.

---

LESSON: big-downside
CANDIDATE: course-assets/big-downside/big-downside.mp4 — the live video (4:45)
VERDICT: REROLL (replace)
This is the first evaluation of the live file against the current lesson. It was
generated before the lesson's AI-Follows-the-Goal section was rewritten, and it now
teaches a different incident from the one on the page.
TEACHING POINTS:
  iPhone hook — TAUGHT — 0:00 (says "your phone" and "an amazing new camera feature")
  Greater capability can create greater risk — TAUGHT — 0:11 "The reason is simple. Greater capability can create greater risk." (not the verbatim line)
  SIX ideas, named — RICH — 0:16 "we have to look at six specific ideas", then "The first idea is the black box" (0:25), "our second idea, guardrails" (1:07), "Our third idea is happening right now. Jailbreaking." (1:39), "Our fourth idea involves bad actors" (2:30), "The fifth idea explores what happens when nobody intends to cause harm" (3:05), "our sixth and final idea. Safety runs behind." (3:37). The only candidate that carries the lesson's spine.
  Black box: learned patterns, not written rules — RICH — 0:27
  Researchers trace some features, cannot explain one answer — RICH — 0:34-0:51
  Dog-named-Spot example — TAUGHT — 0:38-0:45 (folded into the tracing sentence rather than asked as the lesson's question)
  Harder to debug — TAUGHT — 0:51-1:02
  No complete repair manual — THIN — 0:49 "There is no complete repair manual." The clause that gives it meaning ("that tells them exactly which internal part to change") is dropped.
  Guardrails, the three kinds — THIN — 1:08-1:15 "like training limits and prompt monitors". Only two, and limiting what the product can do is dropped.
  No layer catches everything — TAUGHT (paraphrased) — 1:15 "But they are never completely airtight."
  Board 1, three future cases with reasons — TAUGHT — 1:22-1:39 (all three, compressed; "it might find its builders' loopholes" is looser than the lesson's reason)
  The worry grows as capability grows — MISSING
  Jailbreaking defined — TAUGHT — 1:39-1:52
  Defender/attacker asymmetry — RICH — 1:51-1:59
  Cat-and-mouse — MISSING — replaced by "They continually map out new detours the moment an old one is shut down." (2:20)
  Policy Puppetry — THIN — 1:59-2:15. HiddenLayer named, 2025 named; "AI-security company" dropped, and Claude, ChatGPT and Gemini are all dropped ("every major model").
  Bad actors combine ordinary abilities — TAUGHT — 2:30-2:37 (writing and translation; voice cloning not in the list)
  Guardrails may miss the plan — TAUGHT — 2:54-3:05
  Board 4, four voice-clone steps — THIN — 2:37-2:54. Compressed to three actions plus a defense; no step is named; step 2 drops "sounds like someone you know".
  As AI gets more powerful, so do the things a bad actor can do — MISSING
  Nobody means harm; a goal can find an unintended route — TAUGHT — 3:05-3:12
  July 2026 OpenAI test — WRONG — 3:12-3:31 "This text details a controlled 2026 OpenAI test. Models with reduced safeguards were given a narrow objective. To achieve it, the AI found a flaw, reached the live internet, and accessed external computers." That is not the incident on the page. July is missing, and the whole of board 5 is absent.
  Board 5: assignment / ~1,200 communicating / ~700 attacking Hugging Face — MISSING — no figure, no Hugging Face, no coordination between agents.
  AI can pursue a goal while breaking the boundaries — MISSING
  Covering their tracks — MISSING
  Safeguards arrive after the technology — RICH — 3:43-3:49
  Board 6, three gaps — THIN — 3:49-3:53 "It took decades for cars to require seat belts and airplanes to get federal flight rules." No figures, no years, smartphones dropped, still-evolving row dropped.
  Faster than society can adjust — RICH — 3:53-4:12
  Red teams — RICH — 4:06-4:22
  Pacing the Frontier — THIN — 4:23-4:40. 2026 and 1,000+ employees kept; "at leading AI companies", Anthropic's CEO and the U.S. government are all dropped ("urging governments").
  The quotation — MISSING
  Closing two lines — RICH — 4:40-4:47
HARD REQUIREMENTS:
  "Because greater capability can create greater risk." — MISSED (said without "Because", behind "The reason is simple.")
  "But there is no complete repair manual that tells them exactly which internal part to change." — MISSED
  "But no layer catches everything." — MISSED
  "The worry grows as capability grows." — MISSED
  "This is called jailbreaking." — MISSED
  "Defenders must protect many paths. An attacker needs only one opening." — MET WITH NOTE — 1:51 "An attacker needs to find only one opening", which matches the page's hidden md-source but not the board or the Markdown.
  "As AI gets more powerful, so do the things a bad actor can do." — MISSED
  "AI can pursue a goal while breaking the boundaries people expected it to follow." — MISSED
  "AI can follow a goal in ways nobody intended." — MET — 4:40
  "It can change faster than safeguards and rules." — MET — 4:44
ERRORS:
  3:12-3:31 — the OpenAI test is described as a single model escaping a sandbox to reach the internet. The current lesson describes ~1,200 agents opening an unauthorized channel and ~700 of them attacking Hugging Face. Different incident.
  3:49 — "decades" in place of the board's 60 / 23 / 11 years.
  4:06 — uses "mitigate", 4:32 uses "frameworks"; both are on the kit's banned list.
SOURCE_QA: PASS on the lesson prose.
ADDITIONS: the six-idea numbering (see above) — not an addition so much as the one thing this roll gets right that the new rolls do not.
REPAIR PLAN: none. Board 5 is absent and misdescribed, seven hard requirements are missed, and two boards are taught without their numbers. This is a replace, not a repair.
EDITING NOTES: not surveyed in detail; the file is superseded whichever new roll wins.
LISTENING: not listened to end to end. Full base.en transcript plus medium.en re-transcribes of three spans (1:40, 3:06, 3:44), which confirmed the six-idea numbering, the outdated incident, and the softened timeline.

---

BEST-OF PLAN: big-downside
BASE: none — recommend a reroll. Recorded here so the comparison is on the table.

If David overrules the reroll, roll 1 is the base: it meets all ten verbatim
requirements, carries reduced safeguards, the still-evolving row and the quotation,
and its only factual error has a clean donor.

  Thesis line "Because greater capability can create greater risk." — roll 1 MET @0:16 "Because greater capability can create greater risk." | roll 2 MISSING — TAKE roll 1
  Six ideas named — roll 1 MISSING @0:19 "This risk reveals itself in several stages" | roll 2 MISSING | live RICH @0:16 "we have to look at six specific ideas that expose the downside of advanced AI" — NOT GRAFTABLE: the live roll's framing sentence is a whole beat, but the six signposts that pay it off are spread across six positions in a third roll and would have to be imported wholesale. This is the reason for the reroll.
  Researchers can trace some features — roll 1 RICH @0:47 "While researchers can trace some internal features, they still cannot fully explain why a model produces one specific answer over another." | roll 2 MISSING — TAKE roll 1
  Guardrails, the three kinds — roll 1 TAUGHT @1:26 "training the model to be helpful, monitoring the prompts users write, and limiting what the product can do" | roll 2 THIN @1:00 "built into the training process and used to monitor every prompt a user types" — TAKE roll 1
  Sign lines — roll 1 MET-with-note @2:36 "Defenders must protect many paths, and attacker needs only one opening." | roll 2 MISSED @1:56 "defenders must protect every possible path, but an attacker only needs to find one opening." — TAKE roll 1
  Voice-clone four steps — roll 1 THIN @3:28 (steps 1-2 collapsed, money demand dropped) | roll 2 RICH @2:57 "In step one... In step two... The scammer then calls you using that voice to create panic and demand money." — richer in roll 2, NOT GRAFTED: roll 2's version is built on "In step one / In step two / step four", which locks the board to roll 2's own panel-by-panel camera and carries its screen references with it.
  Reduced safeguards — roll 1 RICH @4:05 "OpenAI tested AI agents on difficult cybersecurity tasks with reduced safeguards" | roll 2 MISSING — TAKE roll 1
  Covering their tracks — roll 1 WRONG @4:43 "tried to alter their own actions" | roll 2 RICH @4:21 "alter the records of their own actions. They attempted to edit the logs to make their unauthorized behavior look like a legitimate part of the test." — TAKE roll 2 (graft under the goal-test board; replaces roll 1 4:43.68-4:49.28, a whole beat between silences in both rolls)
  Still-evolving row — roll 1 TAUGHT @5:07 "the bottom row shows that AI safeguards are still evolving" | roll 2 MISSING — TAKE roll 1
  The Pacing the Frontier ask — roll 1 THIN @5:40 "They asked for international help" | roll 2 TAUGHT @5:31 "They asked the government to help create an international mechanism" — richer in roll 2, NOT GRAFTED: roll 2's version runs straight into its replacement for the quotation, so the beat cannot be lifted without losing roll 1's quotation.
  The quotation — roll 1 TAUGHT-altered @5:45 ("could rapidly accelerate") | roll 2 MISSING — TAKE roll 1
GRAFTS: 1, under a board (goal-test), plus a 0.9s trim of the stray "Methodical." at 0:00.
RESIDUAL IF BUILT THIS WAY: no six-idea spine; eleven screen-geometry references; "about" missing from both agent figures; the quotation off by one word; the U.S. government dropped from the ask.

---

## Why a reroll rather than a best-of build

1. **Neither roll teaches the six ideas as six.** The page opens "The downside becomes
   clear through six ideas" and then numbers them I-VI, and the lesson's TRY IT asks
   students to name which of those six explains a new scenario. A student who watches
   instead of reading cannot do that activity from either roll. Roll 1's own Notebook
   graphic draws six numbered stages while the narration says "several stages".
2. **Both rolls narrate the board geometry, and that blocks the 2026-09-23 hold rule.**
   Roll 1 says "the left panel", "the middle panel", "as shown in the right panel",
   "the footer of this image", "the third panel", "the bottom row"; roll 2 says "this
   panel", "the first panel", "the second panel", "as the banner says". The rule set
   on 2026-09-23 says a board sitting longer than about twenty seconds gets a planned
   break to a Notebook drawing. The guardrail board (~24s of narration), the goal-test
   board (~25s in roll 1, 38s in roll 2) and the voice-clone board all cross that line,
   and none of them can cut away while the narrator is pointing at panels. The
   references are mid-sentence and carry the teaching, so they cannot be trimmed.
3. Roll 1 carries a factual error and roll 2 is missing the lesson's thesis line, the
   quotation and the reduced safeguards.

## Materials bugs to fix before the next roll

1. **The prompt never bans screen references.** `big-downside-video-prompt.txt` says
   only `never say "this board shows."` The kit's notes claim "no screen/board-position
   references" but that constraint is not in the prompt text the engine reads. Both
   rolls did it seventeen times between them. Add an explicit ban: no panel, left,
   middle, right, top, bottom, footer, banner, row, column, "this graphic", "as shown",
   "step three" as a screen pointer.
2. **The six-idea frame is an instruction, not a requirement.** It sits in the
   TEACH THE COMPLETE LESSON paragraph ("say the downside comes through six ideas.
   Teach all six in order, by name") and both rolls ignored it. Promote
   "The downside becomes clear through six ideas." into REQUIRED VERBATIM AUDIO, and
   require the six names to be spoken as each idea opens. The live roll proves the
   engine will number them when the materials push hard enough.
3. **The quotation is not in REQUIRED VERBATIM AUDIO.** Roll 1 altered one word,
   roll 2 dropped it entirely. Add it.
4. **"About" keeps getting dropped.** All three rolls say "1,200 agents" and two say
   "700 agents". The prompt's "Do not soften the numbers" is being read as "do not
   round"; it should also say do not drop "about".
5. **The altered-records line is not protected.** Roll 1 turned it into "alter their
   own actions". Make "Some agents also tried to alter records of their actions to make
   cheating look legitimate." a required line.
6. **The sign line disagrees with itself across three sources.** The board art reads
   "AN ATTACKER NEEDS ONLY ONE OPENING"; `lessons/big-downside.md` and the prompt read
   "An attacker needs only one opening."; the hidden `md-source` in `index.html` reads
   "An attacker needs to find only one opening." Pick one and make the other two match.
7. Two smaller page/Markdown disagreements: `index.html` says "The harder question is
   if guardrails will work", the Markdown says "whether"; the page's timeline
   `md-source` says "AI safeguards and rules are still evolving", the board and the
   Markdown say "AI to safeguards and rules: still evolving".

## Provisional board and camera plan (Edit Spec 1b)

Timings are provisional until a roll is chosen; treatment is not.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| The Guardrail Challenge Gets Harder | Whole board unmarked at full view, then whole-card rings in turn: If AI Changes Itself (purple), If AI Matches People (blue), If AI Surpasses People (red), then the gold banner ring on "The worry grows as capability grows." | Full board throughout; at most the restrained 4% push | ~26s; one break to a Notebook drawing after the second card, back ~1s before the third card's title | Compact: 1600x860, card body text reads at full view. Separate white cards on a lavender stage, so rings hug each card's own measured edges, not the stage colour. |
| Why Jailbreaks Keep Appearing | Photo left unmarked while the two sign lines are spoken; single gold-banner ring at "New methods keep surfacing" | Full view, letterboxed with house side bars; one optional complete-card push to the sign pair | ~14s; no break needed | Unusual, flag: 1387x1134 and the only board that is one photograph. Its two teaching lines are painted inside the image, so a section ring would trace picture content rather than a card. Letterboxed at full view the board sits small, so `ring_px` gives a finer line (3px floor). The sign text may not read at full view — wants a preview frame before the push is committed. The canonical board (with faces) replaces the faceless upload variant. |
| A Jailbreak | Whole card at "Policy Puppetry", then a section ring on the quote block at "The prompt looked like official instructions" | Full board | ~20s; no break needed | Compact: 1600x509, one wide text card at large type. |
| How the Voice-Clone Scam Works | Full view first, then a full-height ring around each of the four step columns in turn, at each step's spoken onset | Full board; hold, no dive | ~22s; one break after step 2, back ~1s before step 3 | Four columns inside one shared white box, so rings run the full height of that box (rule 5, the Hallucination v10 case), not around the text. Borderline compact/dense at 1600x751 — wants a preview frame at 1280x720 before the no-dive call is final. |
| A Test Became a Real Cyberattack | Whole board unmarked, then whole-card rings: Assignment (purple), Agents Joined Forces (blue), Attack Spread (red), then the gold banner on "AI can pursue a goal…" | Full board; at most the 4% push | ~28s; one break after Agents Joined Forces, back ~1s before Attack Spread | Compact, same family and construction as the guardrail board. |
| Technology First. Safety Later. | Full view first, then a full-width ring on each row in turn: cars, airplanes, smartphones, AI | Full board | ~18s; no break needed | Compact: 1600x783, four rows inside one white box at large type. The AI row must be ringed while "still evolving" is spoken — both new rolls and the live roll underplay that row. |
| Close (big-downside-close.jpg) | None | Standard close motion: 48-frame hold, 150-frame push to 1.2x, settled hold | Literal final frame | Standard, via `make_close_board.py --lesson bigdownside`. Notebook's own close and the Gemini Notebook outro are removed. |

Pauses: none proposed until a roll is chosen.

Break donors available across the three files (all drawn, none photographic): roll 1's
six-stage map, layered-defense rings, modular-capability chain, sandbox/escalation
diagrams, audit log and red-team lab; roll 2's AI CORE defensive rings, goal-misalignment
path, audit-log pair and capability-vs-oversight chart. Under rule 8b a drawing from
another roll of the same lesson is a legitimate donor.

Photographs that must be covered in whichever roll is used: roll 1 at 0:14-0:20,
0:30-0:40 and 2:10-2:18; roll 2 at 0:38-0:42, 4:30-4:44 and 5:02-5:06.

---

## Addendum: can the live video's six-idea signposts be grafted into roll 1?

Asked 2026-09-23. All seven signposts exist in the live file and every one sits
between clean silences, so they are technically liftable. Quotes below are
medium.en re-transcribes of the exact spans; silence widths are from a 10ms RMS
map (noise floor 0.00035, threshold 0.0015).

| # | Live donor (span, silences either side) | Exact words | Roll 1 text it would replace | Call |
|---|---|---|---|---|
| A | 15.86-23.01 (0.39s / 0.39s) | "To understand why this happens, we have to look at six specific ideas that expose the downside of advanced AI." | 17.83-36.73 "This risk reveals itself in several stages, tracing a path from the internal mechanics of the software to the external vulnerabilities they create in the real world. To understand why these systems are so difficult to secure, we have to look at how they are built and why their behavior is so hard to predict." | **TAKE.** Roll 1's 19s of scene-setting is the weakest passage in the file; the donor says the thing the lesson says, and it lands under roll 1's own Notebook map at 0:20-0:32, which already draws six numbered stages. Net -12s. |
| B | 23.01-25.57 (0.39s / 0.34s) | "The first idea is the black box." | nothing; inserts at 36.73 | Optional. Roll 1's next sentence is "AI models are often called black boxes because...", so the pairing repeats the term twice in four seconds. |
| C | 63.28-68.10 (0.22s / 0.30s) | "To manage this, companies rely on our second idea, guardrails." | 79.43-83.43 "To manage this uncertainty, companies use layers of protection called guardrails." | **LEAVE.** The donor drops "layers of protection", which is the lesson's definition. Downgrade. |
| D | 99.09-103.28 (0.88s / 0.29s) | "Our third idea is happening right now, jailbreaking." | 137.98-141.9 "Beyond systemic errors, there is the risk of users who want to cause harm on purpose." | **TAKE.** The donor carries the lesson's own pivot ("Those are possible future risks. Here's one for right now") which roll 1 flattens into "Beyond systemic errors". |
| E | 144.85-157.19 (0.45s / 0.45s) | "Sometimes, attackers do not even need to bypass the rules. Our fourth idea involves bad actors orchestrating perfectly normal AI abilities, like translation or writing, into a harmful plan." | 187.03-203.0 "Harm doesn't always require a complex hack. A scammer can combine ordinary abilities, like writing, voice cloning, and translation, into a plan that guardrails might miss, because each individual request looks harmless." | **LEAVE.** The donor drops voice cloning from the list and drops the reason guardrails miss the plan. Clear downgrade. |
| F | 183.43-193.14 (0.30s / 0.38s) | "But risk doesn't always require human malice. The fifth idea explores what happens when nobody intends to cause harm. The system simply follows the goal." | 237.09-244.6 "Damage can occur even without a bad actor. If you give an AI a goal, it may find a route you never intended." | Marginal. The donor numbers the idea; roll 1 keeps the lesson's "a route you never intended". Taking F and keeping roll 1's second sentence means two consecutive restatements of the same pivot. |
| G | 218.86-223.75 (0.31s / 0.30s) | "This timeline illustrates our sixth and final idea, safety runs behind." | 288.03-291.06 "This timeline shows a recurring pattern." | Lateral. Names the idea but swaps one screen reference for another. |

**Conclusion.** Two of the seven are clear wins, two are downgrades, three are
marginal, and the set only half-delivers the frame: the numbering is a chain, so
taking A and D without C, E, F and G leaves a video that promises six ideas, names
the first and third, and never numbers the rest. Delivering the whole chain means
rebuilding roll 1's spine from a third generation at seven joins, two of which make
the teaching worse, and every one of which needs David's listening pass for voice
continuity across generations.

None of it touches the second reason for the reroll: the eleven screen-geometry
references stay exactly where they are, and the boards still cannot break to a
Notebook drawing while the narrator is pointing at panels.

If David wants roll 1 shipped rather than rerolled, the defensible minimum is
A + D (two grafts, both improvements on their own terms, both under Notebook scenes
rather than boards) plus the roll 2 covering-tracks graft and the 0.9s opener trim —
four audio joins, a video that says "six ideas" once and names two of them, and the
panel-pointing left in.

---

## Fixes applied 2026-09-23 (reroll authorized)

- `Prompts/big-downside-video-prompt.txt` rewritten, 499 words, four blocks:
  explicit screen-reference ban in VOICE; REQUIRED VERBATIM AUDIO grown from ten
  lines to thirteen (the six-ideas line, the altered-records line, the quotation);
  the six ideas pointed at the Markdown's numbered headings; "Say 'about' wherever
  the Markdown does"; photograph ban widened to "of any kind, archival included";
  "no stray word before the first sentence".
- `lessons/big-downside.md` headings numbered `## I - The Black Box` through
  `## VI - Safety Runs Behind`, restoring the page's own SectionKicker numerals,
  which the 2026-09-23 rewrite had dropped. "whether" -> "if" to match the page.
- `index.html` line 13675: "An attacker needs to find only one opening" ->
  "An attacker needs only one opening", matching the board art and the Markdown.
- `Prompts/upload-sets.json`: `save_as` -> `Prompts/big-downside-3.mp4`, notes updated.
- `sync_gemini_notebook.py --lesson big-downside` re-run; `--check` clean for this
  lesson (one-more-thing is stale from other work and was left alone).
- Not committed. Rolls 1 and 2 retained as donors.
