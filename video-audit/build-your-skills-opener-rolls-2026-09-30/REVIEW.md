# Build Your Skills Three Version Evaluation

**Recommendation: keep the current course video for now. None of these three new versions meets the current narration requirements, and combining them cannot supply all the missing lines.** Version 2 is the strongest new source for teaching coverage, version 3 offers the fullest bike example, and version 1 has useful explanatory diagrams. Those strengths do not make a complete replacement.

This review covers `Prompts/opener-build-1.mp4`, `opener-build-2.mp4`, and `opener-build-3.mp4`, uploaded September 30. They are distinct from the older `build-your-skills-opener-1.mp4` and `-2.mp4`. Full hashes, durations, and video properties are in `sources.json`. All are 1280 × 720 at 30 fps.

| Version | Runtime | Narration verdict | Main finding |
|---|---|---|---|
| 1 | 3:51.37 | REROLL | Omits honesty, weakens the last roadmap row, paraphrases the required lines, answers the reflection question, and adds a coda after the close |
| 2 | 3:46.17 | REROLL | Best coverage of honesty, privacy, human skills, and the bike analogy; still omits the spoken title, paraphrases required lines, and compresses the last roadmap row |
| 3 | 3:14.60 | REROLL | Fullest bike story and clearest reflection paraphrase; omits honesty, reduces privacy to security, and drops the concrete making-something-real part of the roadmap |

The verdicts follow `scripts/video/NARRATION-REVIEW.md`. Runtime and visual defects do not determine them. The failure is not merely that these versions are longer: they use that extra time for expansion while still missing required teaching or wording.

## What the new generations changed

All three explain the creed instead of speaking its four short sentences. None speaks the map title “Build Your Skills.” None gives the exact AI/human-skills bridge or the exact first-person reflection question. Their language also returns to the register the revised prompt explicitly tried to avoid: “permanent cognitive foundation” in version 1, “unique human differential” in version 2, and “permanent cognitive skills” in version 3.

This is evidence that the outputs did not follow those instructions; it does not establish which customization text or settings were supplied to the generator. The updated materials already contain the missing lines. Another prompt-only revision is not a verified remedy.

The new openings are materially longer than the existing video's opening. Version 2 spends approximately a minute reaching the refrain, with the creed continuously visible for 49.37 seconds. Version 1's creed holds for 39.13 seconds. Version 3 breaks its creed with a compass diagram, but still takes about 39 seconds to reach the refrain. The current local version reaches it in approximately 15 seconds.

## Evidence and limits

The current `OpenerSkillsSection` in `index.html`, `lessons/Opener-Build.md`, and the revised `gemini-notebook/build-your-skills-opener/PROMPT.txt` were read. The three canonical board hashes match the images inspected earlier in this task. No new lesson-source inconsistency was found.

Fresh base.en transcripts were produced for all three complete videos, with sequential scene scans and 15 contact sheets sampled every four seconds. The complete medium.en second pass was read for all three versions and confirms the material omissions and paraphrases; its timestamped segment and word records are retained in `verified-transcripts/`. The first-pass version 2 “Thank you” extends past the actual file duration and is absent from medium.en; it is a transcription artifact, not a counted closing defect. A transcript is not an audition: voice, performance, music balance, pronunciation, edit joins, and continuous animation were not heard or watched in real time. Visual findings below are from sampled frames. No candidate is certified for shipping.

`COMPARISON.md` contains the teaching-point comparison with ratings, quoted excerpts, source timestamps, and editorial choices. The per-version blocks below cover the same complete point set. Times are approximate source times, not an approved edit list; final cuts must be located within actual silence and auditioned.

## Version 1

The added explanations do not compensate for the missing honesty point or unresolved exact lines.

```text
LESSON: build-your-skills-opener
CANDIDATE: Prompts/opener-build-1.mp4
VERDICT: REROLL
TEACHING POINTS:
  Hook: what makes you valuable? — TAUGHT — 0:10–0:18: what makes you valuable?
  Your choices — TAUGHT — 0:21–0:24: You decide the strategic direction. You make the choices
  Your questions — TAUGHT — 0:24–0:29: you frame the specific questions required to get a useful result
  Your judgment — TAUGHT — 0:29–0:34: you have to evaluate it. That requires independent judgment
  Your skills — TAUGHT — 0:34–0:39: practiced skills to refine raw output into a finished product
  Smarter Than the Tool refrain — TAUGHT — 0:39–0:49: the operator must always remain smarter than the tool
  Final skill-building section and lasting value — THIN — 2:03–2:12: a permanent cognitive foundation… after… software is replaced
  Learn to ride, outgrow and change bikes — RICH — 1:10–1:29: Eventually, you outgrew that first bike. You moved on to a different model
  Balance stays when equipment changes — RICH — 1:29–1:35: The machine itself was temporary… balance stayed with you
  Balance transfers to skating and basketball — TAUGHT — 1:35–1:41: different physical activities, like ice skating or playing basketball
  Skill stays whether serious cyclist or casual rider — THIN — 1:25–1:35: or you stopped cycling altogether… balance stayed with you
  Nobody can give you balance; practice builds it — TAUGHT — 1:53–2:03: Nobody can install those enduring abilities… build them through practice
  Bridge: both AI and human skills, human skills most important — THIN — 1:41–1:53: AI skills… buttons… human skills like creative thinking, which endure
  Introduce roadmap, then speak Build Your Skills — MISSING — 2:12–2:17: This roadmap outlines exactly how we will build those enduring skills
  Row 1: Use AI With Skill and Care — TAUGHT — 2:17–2:20: using AI with skill and care
  Choose what changes the answer — TAUGHT — 2:20–2:22: choosing inputs deliberately
  Improve ideas through conversation — TAUGHT — 2:22–2:27: actively improving ideas through conversation
  Use AI honestly — MISSING — 2:17–2:27: No spoken honesty point
  Protect what you share — TAUGHT — 2:22–2:27: protecting shared data
  Row 2: Skills That Grow in Value — TAUGHT — 2:36–2:40: skills that grow in value over time
  People skills help you work with others — RICH — 2:40–2:56: communicate clearly and collaborate with other people
  Creative thinking finds better angles — TAUGHT — 2:43–2:46: finding the creative angle to solve problems
  Row 3: stay flexible and keep learning as AI changes — TAUGHT — 2:56–3:02: staying flexible… adapt as AI changes
  Turn interests into action by building skills and something real — THIN — 2:59–3:04: turning abstract interests into tangible actions
  Takeaway: Build the skills you keep when the tool changes — TAUGHT — 3:04–3:11: capabilities you retain after a software update
  Reflection: same tool, what do I bring? — TAUGHT — 3:21–3:35: same automated tools… what exactly do you bring to the table?
  Leave question open; this section builds the answer — THIN — 3:35–3:40: The answer lies in recognizing the difference between what you use and what you own
  Close with the two exact lines and nothing after — TAUGHT — 3:40–3:48: The tool is rented. The skills are yours to keep. Let the software do the heavy lifting…
HARD REQUIREMENTS:
  Creed: four standalone exact sentences — MISSED; explanatory sentences replace the refrain.
  “And you'll always be Smarter Than the Tool.” — MISSED as exact wording; meaning is taught.
  Explicit final skill-building section — MISSED; lasting skills are described without that orientation.
  Exact AI/human-skills bridge — MISSED.
  Fixed roadmap introduction and spoken Build Your Skills title — MISSED; title is never said.
  Three map rows verbatim with complete explanations — MISSED; see individual coverage above.
  First-person reflection question verbatim — MISSED.
  Bike analogy and practice — taught, with practice deferred to the later human-skills discussion rather than explicitly finishing the balance story.
  Takeaway verbatim — MISSED; “Focus your time and energy entirely on capabilities you retain after a software update.”
  Keep reflection question open — MISSED; “The answer lies in recognizing the difference between what you use and what you own.”
  Exact two closing lines — PRESENT consecutively, but final-position requirement MISSED: “Let the software do the heavy lifting, but ensure you keep the mental gains” follows them.
ERRORS / CONTENT CAUTIONS: The “focus… entirely” takeaway is stronger than the lesson, which teaches both current AI skills and enduring human skills. “Routine technical tasks become fully automated” is an added absolute claim, not needed for the opener. Do not retain those formulations in a replacement.
SOURCE_QA: PASS; current page, board wording, and Markdown agree on required teaching.
ADDITIONS: The distinction between delegating work and acquiring a skill (0:59–1:10) is useful but expands this short opener. The tool-versus-balance diagram sequence may be useful visual material.
REPAIR PLAN: No verified complete repair. Other new rolls and the current local video can supply isolated stronger beats, but none supplies the missing complete exact creed, title, and reflection question. No synthetic word splices proposed.
EDITING NOTES: Creed 0:09.73–0:48.87; map appearances 2:12.43–2:27.17, 2:36.30–2:46.23, and 2:56.33–3:11.07. The interleaved map is more varied than a continuous hold. The coda could be cut, but that does not resolve the missing title/creed/question.
LISTENING: Transcript and sampled-frame review only; no direct audio audition or motion certification.
```

## Version 2

Best overall raw source for meaning, but not a complete or approved base.

```text
LESSON: build-your-skills-opener
CANDIDATE: Prompts/opener-build-2.mp4
VERDICT: REROLL
TEACHING POINTS:
  Hook: what makes you valuable? — TAUGHT — 0:00–0:12: what exactly do you bring to the table?
  Your choices — RICH — 0:16–0:23: your choices. You are the one who decides which problems are actually worth solving
  Your questions — RICH — 0:24–0:33: your questions… You have to know what to ask to get a useful result
  Your judgment — RICH — 0:33–0:41: your judgment… determine if it is accurate, ethical, and ready to be used
  Your skills — TAUGHT — 0:41–0:51: your skills… shape it into a finished real-world product
  Smarter Than the Tool refrain — TAUGHT — 0:56–1:01: which means you will always be smarter than the tool
  Final skill-building section and lasting value — THIN — 1:02–1:14: this next phase of learning… building internal capabilities that last
  Learn to ride, outgrow and change bikes — TAUGHT — 1:15–1:24: you outgrew that specific frame… and you moved on
  Balance stays when equipment changes — RICH — 1:21–1:25; 1:36–1:41: you retained… Balance… environment changed… capability remained
  Balance transfers to skating and basketball — RICH — 1:25–1:36: a sharp, fast turn on roller skates… steady when driving to the net
  Skill stays whether serious cyclist or casual rider — TAUGHT — 1:36–1:41: environment changed completely, but the internal capability remained
  Nobody can give you balance; practice builds it — RICH — 1:41–1:48: Nobody could simply hand you that sense of balance… repeated effort and practice
  Bridge: both AI and human skills, human skills most important — TAUGHT — 1:56–2:09: specific mechanics for operating AI… most valuable capabilities… foundational human skills
  Introduce roadmap, then speak Build Your Skills — MISSING — 2:09–2:16: This roadmap outlines exactly how we will construct those permanent skills over three distinct phases
  Row 1: Use AI With Skill and Care — TAUGHT — 2:16–2:20: use AI with skill and care
  Choose what changes the answer — TAUGHT — 2:20–2:24: deliberately choosing your inputs
  Improve ideas through conversation — TAUGHT — 2:20–2:27: refining early ideas through back and forth conversation
  Use AI honestly — TAUGHT — 2:27–2:34: ethical boundaries… be transparent about your tool use
  Protect what you share — TAUGHT — 2:30–2:34: protect sensitive data
  Row 2: Skills That Grow in Value — TAUGHT — 2:34–2:39: interpersonal traits that grow in value over time
  People skills help you work with others — TAUGHT — 2:39–2:44: communication skills required to collaborate with human teams
  Creative thinking finds better angles — TAUGHT — 2:44–2:48: creative thinking necessary to find better angles on tough problems
  Row 3: stay flexible and keep learning as AI changes — THIN — 2:48–2:59: continuous adaptation… take everything you have learned… creating something real
  Turn interests into action by building skills and something real — THIN — 2:52–2:59: turn your theoretical knowledge into tangible action by creating something real
  Takeaway: Build the skills you keep when the tool changes — TAUGHT — 3:02–3:05: to build the skills you keep when the tool changes
  Reflection: same tool, what do I bring? — TAUGHT — 3:11–3:19: same automated baseline… what is your unique human differential?
  Leave question open; this section builds the answer — TAUGHT — 3:19–3:25: Every exercise and module ahead… construct your own answer
  Close with the two exact lines and nothing after — TAUGHT — 3:33–3:43: The tool is rented, but the critical thinking… The skills are yours to keep.
HARD REQUIREMENTS:
  Creed: four standalone exact sentences — MISSED; explanatory sentences replace the refrain.
  “And you'll always be Smarter Than the Tool.” — MISSED as exact wording; meaning is taught.
  Explicit final skill-building section — MISSED; lasting skills are described without that orientation.
  Exact AI/human-skills bridge — MISSED.
  Fixed roadmap introduction and spoken Build Your Skills title — MISSED; title is never said.
  Three map rows verbatim with complete explanations — MISSED; see individual coverage above.
  First-person reflection question verbatim — MISSED.
  Bike analogy, transfer, and practice — MET in substance.
  Priority of human skills — MET in substance at 1:56–2:09.
  Takeaway — target words present at approximately 3:02–3:05, introduced by “to” inside a longer sentence; standalone exact delivery MISSED.
  Keep reflection question open — MET; it defers the answer to upcoming learning.
  Closing lines — both PRESENT, but additional commentary separates them; clean two-line ending MISSED.
ERRORS / CONTENT CAUTIONS: No clear factual contradiction with the lesson identified. Material omissions are the final-section orientation and complete row-three explanation. Do not mistake its privacy teaching for the missing explicit keep-learning/AI-changes and personal-interests connection.
SOURCE_QA: PASS; current page, board wording, and Markdown agree on required teaching.
ADDITIONS: The choices explanation asks which problems are worth solving; judgment includes accuracy and ethics. These are useful explanations, but the creed does not need to become a minute-long mini-lesson.
REPAIR PLAN: No verified complete repair. Other new rolls and the current local video can supply isolated stronger beats, but none supplies the missing complete exact creed, title, and reflection question. No synthetic word splices proposed.
EDITING NOTES: Creed 0:12.43–1:01.80, 49.37 seconds. Map 2:09.60–3:05.47, 55.87 seconds. Replace Notebook underlines/washes with canonical boards and course rings in any future build. The early bike/skating sequence is usable visual material pending motion review.
LISTENING: Transcript and sampled-frame review only; no direct audio audition or motion certification.
```

## Version 3

The shorter runtime does not make it more complete. The bike story is its strongest passage.

```text
LESSON: build-your-skills-opener
CANDIDATE: Prompts/opener-build-3.mp4
VERDICT: REROLL
TEACHING POINTS:
  Hook: what makes you valuable? — TAUGHT — 0:00–0:11: What exactly makes you valuable?
  Your choices — TAUGHT — 0:14–0:19: the specific choices you make
  Your questions — TAUGHT — 0:19–0:21: the unique questions you decide to ask
  Your judgment — TAUGHT — 0:25–0:29: your critical judgment to evaluate the results
  Your skills — TAUGHT — 0:29–0:32: your developed skills to actually put them to use
  Smarter Than the Tool refrain — TAUGHT — 0:36–0:39: You will always be smarter than the tool
  Final skill-building section and lasting value — THIN — 0:39–0:50: a specific phase of your learning journey… skills you will retain permanently
  Learn to ride, outgrow and change bikes — RICH — 0:50–1:00: you outgrew it… a larger bike with different mechanics
  Balance stays when equipment changes — RICH — 1:00–1:12: a physical sense of balance… long after the original equipment has been left behind
  Balance transfers to skating and basketball — RICH — 1:12–1:27: skates… stabilize itself… stop and pivot on a basketball court
  Skill stays whether serious cyclist or casual rider — RICH — 1:27–1:36: competing in serious races or just riding your bike for fun… belonged completely to you
  Nobody can give you balance; practice builds it — RICH — 1:36–1:44: No one could simply hand you that balance… earn it through your own deliberate practice
  Bridge: both AI and human skills, human skills most important — THIN — 1:44–1:57: both the technical methods of using AI and the permanent cognitive skills
  Introduce roadmap, then speak Build Your Skills — MISSING — 1:57–2:02: This graphic outlines the three steps we will take
  Row 1: Use AI With Skill and Care — TAUGHT — 2:02–2:06: use AI with skill and care
  Choose what changes the answer — TAUGHT — 2:06–2:09: construct prompts that change the output
  Improve ideas through conversation — TAUGHT — 2:09–2:11: iterate ideas through conversation
  Use AI honestly — MISSING — 2:11–2:14: use these platforms securely
  Protect what you share — THIN — 2:11–2:14: use these platforms securely
  Row 2: Skills That Grow in Value — TAUGHT — 2:14–2:18: skills that appreciate in value over time
  People skills help you work with others — TAUGHT — 2:18–2:22: collaborating effectively with your peers
  Creative thinking finds better angles — TAUGHT — 2:22–2:26: creative thinking… a stronger angle
  Row 3: stay flexible and keep learning as AI changes — TAUGHT — 2:26–2:33: maintaining flexibility… stay adaptable as the software updates
  Turn interests into action by building skills and something real — THIN — 2:33–2:37: translate your personal interests into tangible action
  Takeaway: Build the skills you keep when the tool changes — TAUGHT — 2:37–2:44: capabilities that stay with you when the software inevitably changes
  Reflection: same tool, what do I bring? — TAUGHT — 2:44–2:51: If everyone has access to the exact same tool, what do you bring that it doesn’t?
  Leave question open; this section builds the answer — TAUGHT — 2:51–2:59: The steps ahead are designed to help you answer that question
  Close with the two exact lines and nothing after — TAUGHT — 3:03–3:12: The tool is rented, but the judgment… the skills are yours to keep.
HARD REQUIREMENTS:
  Creed: four standalone exact sentences — MISSED; explanatory sentences replace the refrain.
  “And you'll always be Smarter Than the Tool.” — MISSED as exact wording; meaning is taught.
  Explicit final skill-building section — MISSED; lasting skills are described without that orientation.
  Exact AI/human-skills bridge — MISSED.
  Fixed roadmap introduction and spoken Build Your Skills title — MISSED; title is never said.
  Three map rows verbatim with complete explanations — MISSED; see individual coverage above.
  First-person reflection question verbatim — MISSED.
  Bike story, transfer, serious/casual branch, and practice — MET in substance.
  Human skills explicitly most important — MISSED; the narration says both kinds, without the priority.
  Takeaway verbatim — MISSED; only a paraphrase is spoken.
  Keep reflection question open — MET; the following steps help build the answer.
  Closing lines — target words PRESENT but interrupted by elaboration; clean two-line ending MISSED.
ERRORS / CONTENT CAUTIONS: No major factual contradiction established. “Learned center of gravity” is awkward wording for learned balance/control and is not a reason to prefer this narration over version 2. Security does not supply the absent honesty teaching.
SOURCE_QA: PASS; current page, board wording, and Markdown agree on required teaching.
ADDITIONS: The serious-racing versus casual-riding branch preserves an original lesson detail omitted or compressed by the other versions. The compass adds an explanation of choice and questions but is not required by the opener.
REPAIR PLAN: No verified complete repair. Other new rolls and the current local video can supply isolated stronger beats, but none supplies the missing complete exact creed, title, and reflection question. No synthetic word splices proposed.
EDITING NOTES: Map 1:57.47–2:43.97, 46.50 seconds. The stepped-paper illustration near 0:39 carries production-direction labels. The closing card is cropped by the generated camera movement, then replaced by the engine outro; use the canonical standard close in any future edit.
LISTENING: Transcript and sampled-frame review only; no direct audio audition or motion certification.
```

## Best of plan

**BASE: version 2 only as a provisional source if narration replacement is pursued. No complete assembly recommended from the available audio.** It has the strongest human-skills bridge and explicit honesty/privacy teaching. Keep its concise bike example rather than adding a longer graft simply for more words. Version 3's 1:27–1:36 serious/casual branch is richer, but not grafted: it is an optional detail, and joins/voice continuity have not been auditioned.

The full beat comparison is in `COMPARISON.md`. Material differences:

- **Honesty/privacy:** take version 2's 2:27–2:34 explanation if a donor is needed. Version 1 lacks honesty; version 3 says only “securely.”
- **Balance transfer:** versions 2 and 3 both give concrete skating/basketball examples; version 2 is more economical. Version 3 preserves the serious/casual branch. Version 1's animated transfer diagram may help visually, independently of which narration is selected.
- **AI/human priority:** version 2 at 1:56–2:09 is clearest in meaning, but still not the requested exact line.
- **Row three:** none of the new versions supplies the complete required row. The current local v5 has a fuller keep-learning/projects passage at approximately 1:52–2:09, but it also paraphrases the exact row. A graft would improve substance without fixing all requirements.
- **Question:** version 3 at 2:44–2:51 has the clearest paraphrase. It still says “If… what do you bring” instead of the two exact sentences with “What do I bring.”
- **Close:** version 1 has the cleanest consecutive pair at approximately 3:40–3:44, followed by a removable coda. The current local v5 also has the correct close at approximately 2:36–2:39. These are potential donors, not auditioned grafts.

Both transcription passes render version 1 at 1:43.58–1:48.18 as “buttons to push on today’s intervals.” That phrase needs listening before labeling it a mispronunciation or an ASR error; it is not used as a reason for the verdict.

**GRAFTS: zero approved or verified.** A best-of assembly still lacks the required creed, spoken title, exact bridge/map wording, and reflection question. It is therefore not a complete REPAIR plan.

## Proposed production treatment

No build is proposed until narration is resolved. This provisional board plan uses version 2 to locate the topics; durations must be re-established against the selected narration. Prior approval of full-row highlights remains the design preference, not approval of a new audio edit.

| Board | Highlight sequence | Camera | Current version 2 span and future treatment | Reason |
|---|---|---|---|---|
| What Makes You Valuable? | Unmarked opening, then gold outline around each exact creed line and the final refrain at its spoken onset | Full board | Currently 0:12.43–1:01.80. A corrected opening should start on the board and leave after the short creed, without the explanatory expansion | Restore the intended brief refrain; no filler pause or camera move |
| Build Your Skills | Unmarked fixed introduction and title; full row 1, row 2, row 3, then banner; one outline at a time | Full board; compact text, no need for a dive | Currently 2:09.60–3:05.47. Shorten narration first. If a long hold remains, consider the same roll's collaboration drawing near 2:04 under row two, and project-planning scene near 3:20 under row three, subject to full-resolution/source-span inspection | Keep all row teaching and David's full-row emphasis; drawings are supporting candidates, not verified inserts |
| The tool is rented. / The skills are yours to keep. | Unmarked | Canonical close; 48-frame hold, 150-frame push to 1.2×, settled final hold | Current close topic begins about 3:25.87. Correct narration must end with the two lines only; remove engine outro in production | Standard cleanup; none of the raw closes certifies the final course treatment |

Use exact current canonical JPGs and fixed 4 px rings at 720p on any rebuilt boards. No new pauses proposed: no listening evidence justifies additional silence. The retained `silences.txt` files are measurement aids, not listening approval or an edit decision.

## Supporting visuals to retain or inspect

These scene recommendations are based on sampled frames; no animation was certified in motion.

- **Version 1, approximately 1:10–1:41:** the diagrams separate bike/equipment from internal balance and then connect that skill to skating and basketball. This is useful explanatory material. Preserve coherent reveals if auditioned in a future build; do not replace it merely because it is a diagram.
- **Version 1, approximately 0:49–1:10:** human-intent and skill-acquisition/delegation diagrams help explain the added narration, but that detour is optional and overlong for this opener. The photorealistic computer/wooden-figure scenes at the opening and around 0:59 and 1:53 require replacement under the Notebook imagery rule if those spans are used. Do not infer that they are licensed photographs from their appearance.
- **Version 2, approximately 1:15–1:41:** cycling, skating, and basketball drawings support the full analogy. Some ancillary scenes contain drafting labels or dense annotations (old bike near 1:24, shoes around 1:44). Prefer targeted label removal over discarding an otherwise useful drawing.
- **Version 2, approximately 2:00–2:09:** chat, human collaboration, and closing-laptop drawings distinguish the temporary interface from lasting human ability. The collaboration scene is a plausible map interleave; inspect the full animation before using it.
- **Version 2, approximately 3:11–3:25:** equal-tool screens and planning work support the reflection. The planning scene mixes rendered/realistic objects and drawn hands; classify its full-resolution appearance before treating it as compliant Notebook imagery.
- **Version 3, approximately 0:11–0:22:** compass sequence connects choices and questions to project direction. It explains an added idea; retaining it depends on whether that expanded opening is kept.
- **Version 3, approximately 0:50–1:44:** bike stages, skating, basketball, serious/casual cycling, and practice imagery preserve the analogy's sequence. Some labels are too technical (“Permanent Equilibrium,” “Invariant Axis Control”); clean labels while preserving useful motion. The source must be watched to establish exact safe donor boundaries.
- **Version 3, around 0:39:** remove illustration instructions around the staircase. Around 2:52, the photorealistic pencil/notebook scene needs replacement if used. Replace the cropped closing graphic and engine outro with the canonical close.

## Next step

Preserve these rolls as potential donors. Do not replace the current video with one of them or spend a full production pass assembling a still-incomplete hybrid. Before another generation, verify that the current customization prompt and exactly the four staged source files were used. If the generator continues replacing required sentences, a controlled narration recording is a more dependable route than further visual editing; that would be a separate proposed action, not work performed here.

No lesson, prompt, canonical image, current video, tracker, or deployment was changed by this evaluation.
