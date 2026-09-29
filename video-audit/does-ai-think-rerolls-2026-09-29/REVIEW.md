# Does AI Think? — three-candidate evaluation, September 29, 2026

**Use Candidate 2 as the base, with Candidate 3's clean closing narration. Do not request another generation yet.** Candidate 2 is the most faithful, complete explanation and preserves the five comparisons as separate beats. It needs narration cleanup before it can earn KEEP: it actually speaks a pause instruction during the close. Candidate 3 supplies the correct two closing lines without that interruption. Candidate 1 offers no essential teaching improvement worth choosing it as the base.

**Verification limit:** all three complete transcripts were read against the current page and upload Markdown. Full-duration four-second contact sheets and additional sequentially extracted detail frames were inspected. Selected wording was cross-checked with a second ASR model. No audio was heard and no animation was watched in continuous playback with sound. The REPAIR recommendations below are provisional editorial assessments, not certified feasible joins or shipping passes. An audition preview is provided; voice continuity and cadence remain to be heard. ASR agreement does not replace listening.

## Sources

| Candidate | Exact file | Duration, rounded | SHA-256 prefix |
|---|---|---|---|
| 1 | `Prompts/does-ai-think-1.mp4` | 3:45 | `9e11a6192e39` |
| 2 | `Prompts/does-ai-think-2mp4.mp4` | 3:40 | `3e2e5dfce476` |
| 3 | `Prompts/does-ai-think-3.mp4` | 3:13 | `9b85c612b297` |

All are 1280 × 720 at 30 fps. Full identities and differing audio/container versus video durations are recorded in `identity.json`. Candidate 2's unusual filename is unchanged.

Authorities: current `index.html` rendered lesson, both canonical boards and close, `lessons/does-ai-think.md`, and `gemini-notebook/does-ai-think/PROMPT.txt`. Generation materials have moved out of Prompts since preparation; the current prompt was found in its new location. Applied current `NARRATION-REVIEW.md` and today's updated `EDIT-SPEC.md`, including retaining useful independent animations and illustrative numerical examples. Tracker not accessed or changed. No source video, lesson, generation material, or published file was changed.

## Teaching comparison and best-of selection

Each cell rates the teaching and gives an actual transcript excerpt with its source timestamp. Related sentences in a single cell constitute one coherent beat; full text remains in each candidate's `transcript.txt`. Times are approximate unless word timing is specifically given below.

| Teaching point | Candidate 1 | Candidate 2 | Candidate 3 | Selection |
|---|---|---|---|---|
| Human-like explanations, jokes, apologies | RICH, 0:00–0:10: “It explains complex topics, throws in a joke, and even says sorry” | RICH, 0:00–0:17: “It explains complex topics, it cracks jokes, and it even says sorry” | RICH, 0:00–0:12: “It explains complex topics, it cracks jokes, and it even says sorry” | 2; equivalent teaching |
| Why it feels like someone is inside | TAUGHT, 0:10–0:16: “someone sitting on the other side of the screen” | TAUGHT, 0:17–0:21: “hard not to feel like someone is in there” | TAUGHT, 0:12–0:17: “hard not to feel like someone is in there” | 2 |
| Ask whether it thinks/understands like a person | TAUGHT, 0:18–0:27: “does it actually think?” | TAUGHT, 0:21–0:32: “Does this AI actually think?” followed by the understanding question | TAUGHT, 0:19–0:25: “is it actually understanding the world the way you do?” | 2; both questions explicit |
| Fluency examples: sentence, poem, conversation | RICH, 0:27–0:34: “finish your sentence, break down the meaning of a 19th century poem” | RICH, 0:34–0:41: “finish your sentence, explain a dense poem, and carry on a long conversation” | MISSING as this specific list; explanation/joke/apology examples remain at 0:06–0:12 | 2; 3's omission compresses the examples, rather than eliminating all evidence of fluency |
| Sounding human does not establish understanding | TAUGHT, 0:34–0:39: “But sounding human doesn't tell you whether it understands” | TAUGHT, 0:41–0:46: “But sounding like a person doesn't tell you whether it understands things the way a person does” | TAUGHT, 0:25–0:29: “Sounding like a person doesn't tell you whether it understands” | 2, exact required wording |
| Chinese Room setup: person has no Chinese | RICH, 0:40–0:58: “doesn't know a single word of Chinese”; giant rulebook explained | RICH, 0:46–1:03: “This person does not know a single word of Chinese”; chart/rulebook explained in steps | RICH, 0:29–0:39: “doesn't know a single word of Chinese” | 2; setup and steps form a coherent whole |
| Incoming note asks “How are you?” | RICH, 0:58–1:03: “It asks, how are you?” | RICH, 1:03–1:10: “It asks, how are you?” | RICH, 0:39–0:46: “It asks, how are you?” | 2 |
| Person cannot read; whole-phrase lookup | RICH, 1:03–1:11: “look up the exact sequence of symbols” | RICH, 1:10–1:22: “look up the entire phrase on a giant reference chart” | RICH, 0:46–0:53: “look up the entire phrase on a giant reference chart” | 2; complete and clear |
| Matching reply returned under door | RICH, 1:11–1:18: “I'm fine, thank you, and slide it back” | RICH, 1:22–1:33: “I'm fine, thank you”; then the reply is returned | RICH, 0:53–1:02: “I'm fine, thank you, and slide it back” | 2; 3 is tighter but not substantively richer |
| Outside impression versus inside limitation | RICH, 1:18–1:27: “fluent Chinese conversation, yet the person inside is just mechanically matching shapes” | TAUGHT, 1:33–1:37: “To anyone outside, it looks like fluent Chinese conversation” after explaining unreadable symbols | TAUGHT, 1:02–1:06: same required sentence | 1 has a useful extra contrast, but 2 already teaches it through the steps and preserves the required sentence; no graft needed |
| First board takeaway | TAUGHT in meaning, 1:27–1:34: “Producing a convincing answer does not prove that the person inside actually understands Chinese” | TAUGHT, 1:39.56–1:41.96: “a convincing answer doesn't prove understanding” | TAUGHT, 1:06–1:09: exact takeaway | 2, required words present |
| Producing versus understanding: qualified distinction | TAUGHT but qualification lost, 1:37–1:41: “are two different things” | TAUGHT, 1:43–1:50: “aren't necessarily the same thing” | TAUGHT, 1:09–1:15: “aren't necessarily the same thing” | 2; 1 does not meet the protected passage |
| Not a literal rulebook; patterns learned in training | RICH, 1:42–2:01: “does not use an actual static rule book or a simple lookup table”; statistical patterns explained | RICH, 1:50–2:08: “An LLM doesn't follow a literal rule book. It uses patterns learned during training to predict its response” | TAUGHT, 1:15–1:27: same required explanation | 2; stronger source fidelity. 1's “most logical next word” is a less precise substitution |
| Bridge back to limits of fluency | TAUGHT, 2:01–2:11: “a highly fluent answer still does not guarantee actual comprehension” | TAUGHT through the qualified distinction and explicit rulebook limit; returns to insufficient evidence at 3:22 | WRONG as stated, 1:27.94–1:38.20: “rather than actual comprehension” assumes the conclusion the lesson does not establish | 2; do not import 3's bridge |
| Orient to five comparisons | TAUGHT, 2:11–2:18: “across five specific areas” | TAUGHT, 2:08–2:16: “five specific differences” | TAUGHT, 1:38–1:44: “across five specific areas” | 2 |
| Meaning, both sides | TAUGHT, 2:18–2:27: “things you care about in your life”; “patterns it learned along with the text” | TAUGHT, 2:16–2:24: “what they actually mean in your life”; “learned patterns and the prompts” | TAUGHT, 1:44–1:54: “daily life”; “learned mathematical patterns” and prompt | 2; 1 adds warmth, not missing teaching |
| Experience, both sides and data modalities | TAUGHT, 2:27–2:39: “physical and emotional events”; “text, audio, and image data” | TAUGHT, 2:24–2:33: lived experience, then exact “text, images, audio, and other data” sentence | TAUGHT, 1:55–2:06: same complete AI sentence | 2; protected wording preserved |
| Word choice, both sides and repetition | RICH, 2:39–2:50: “express your internal thoughts”; “repeats that calculation over and over” | TAUGHT, 2:33–2:43: “choose words to express an internal desire to speak”; “predicts the next word in a sequence then repeats” | TAUGHT, 2:06–2:21: human side, then beauty, then AI word-choice side | 2; 3 interleaves two comparisons and is harder to track |
| Beauty, both sides | TAUGHT, 2:50–3:02: “personal visceral reaction”; “patterns of how humans write about art” | TAUGHT, 2:43–2:53: “personal emotional response”; “regurgitating learned structural patterns” | TAUGHT, 2:12–2:26: “painting or a song”; “retrieving patterns of text written by humans” | 2 for continuity; none offers a clean substantive improvement. Loaded vocabulary is a voice weakness across all three |
| Uncertainty, both sides | WRONG overclaim, 3:08–3:14: “AI is designed to sound highly confident” | TAUGHT, 2:53–3:03: “You inherently notice”; AI “can sound absolutely certain even when it is completely wrong” | TAUGHT, 2:26–2:37: “You notice when you feel unsure”; AI can sound certain when wrong | 3 has cleaner human wording, but 2's practical contrast is adequately taught; optional donor, not required |
| Comparison takeaway | TAUGHT in meaning but exact line missed, 3:14–3:20: “generated by completely different processes” | TAUGHT, 3:05.56–3:09.22: “Similar looking answers can come from very different processes” | TAUGHT, 2:40.76–2:43.76: same exact words | 2; its required qualifier “can” is preserved |
| AI remains useful and impressive | TAUGHT, 3:20–3:30: “complex, valuable work alongside you” | RICH, 3:10–3:22: “analytical work” and organizing information | RICH, 2:44–2:54: “generating code or drafting essays” | 2. 3's familiar examples are useful but do not warrant another seam; neither addition contradicts the lesson |
| Return to insufficient evidence | TAUGHT, 3:30–3:36: “output alone is never enough evidence” | TAUGHT, 3:22–3:29: “not enough evidence to prove it understands” | TAUGHT, 2:54–3:01: “not a reliable metric” | 2 |
| Two exact closing lines, no interruption | TAUGHT in meaning; required wording missed, 3:36–3:42: “It sounds human, but it works differently”; adds “simply” to final line | Required words present but interrupted, 3:28–3:37: “As this final graphic states” and “Slight pause for emphasis” | TAUGHT, 3:04.24–3:09.04: “Sounds human. Works differently. A convincing answer doesn't prove understanding” | **TAKE 3's two complete closing sentences**, excluding its preceding summary introduction |

## Per-candidate verdicts

### Candidate 1 — REPAIR, provisional; not selected

**Teaching points:** Candidate 1 column above. Coverage is broad, with a good inside/outside Chinese Room contrast. It repeatedly paraphrases protected wording. It loses “aren't necessarily,” substitutes “most logical” for likely next-word prediction, and asserts that AI is designed to sound confident rather than that it can sound confident when wrong.

**Hard requirements:** the outside-observer line, qualified distinction, literal-rulebook passage, exact experience line, both board takeaways, and both close lines are paraphrased. The first fluency sentence is also shortened. Meaning is often adequate, but this is not a KEEP under the current exact-line requirements.

**Errors/additions:** “designed to sound highly confident” (3:08) is an unsupported design-purpose claim. “Most logical next word” (1:58) conflates likelihood with logical correctness. “Retrieving the patterns” and “visceral” add unnecessary language. The inside/outside contrast at 1:18–1:27 is useful.

**Repair route:** Candidate 2 supplies the protected opening qualification (0:40.88–0:46.48), Chinese Room block and analogy explanation (approximately 1:00–2:08), and comparison block (2:08–3:09.9); Candidate 3 supplies the clean close (3:04.24–3:09.04). Replacing so much of 1 is less sensible than starting from 2. Donors are textually identified; no joins have been auditioned.

**Editing notes:** sampled visuals include useful chat bubbles and a prediction sequence. “GENERATION / COGNITION” with a crossed-out brain around 1:34–1:42 and “STATISTICAL MATH ≠ TRUE AWARENESS” around 2:03–2:10 risk reinforcing the stronger conclusion rather than the lesson's evidential caution. These need targeted treatment if used. Raw course-board runs are about 54 s and 69 s. Recreated boards, engine mark, and outro need normal production work. Numerical prediction examples are not rejected solely for using illustrative values.

**SOURCE_QA:** page and upload source align. **LISTENING:** none; selected wording checked with base.en and medium.en.

### Candidate 2 — REPAIR, provisional; recommended base

**Teaching points:** Candidate 2 column above. Complete lesson, coherent sequence, separate word-choice and beauty explanations, correct qualified Chinese Room distinction, and required takeaways. It improves materially on the live video's “shares nothing in common” assertion.

**Hard requirements:** all protected passages are textually present, including the experience line and both closing lines. The required clean ending is not met because the narrator speaks production commentary between the closing lines. Sentence punctuation and pauses are not independently established by transcription.

**Required repair:** replace its close with the two clean sentences from Candidate 3, as specified below. The earlier phrases “As the takeaway at the bottom of the board shows” (1:37) and “Looking at the takeaway at the bottom makes the conclusion clear” (3:03) are cumbersome but coherent references to the screen; unlike the spoken pause instruction, they are not blockers and need not be cut automatically.

**Uncertain wording:** both ASR passes render “without dropping the threat” at approximately 0:39–0:40, where “thread” is likely intended. This may be a pronunciation or transcription issue. Listen to that phrase before deciding; do not classify it as a confirmed error from ASR alone. If actually misspoken, dropping the optional “without dropping the …” clause leaves a complete fluency example. Exact trim requires audio boundary inspection.

**Voice polish:** “regurgitating” (2:48) violates the requested plain voice; “You inherently notice” (2:55) is less careful than “You can notice.” The practical comparisons still reach the viewer. Candidate 3's uncertainty beat is a cleaner optional donor, but the proposed minimum repair avoids another unnecessary graft. No verified material factual error beyond the unresolved pronunciation issue is established in 2's core teaching.

**Additions:** analytical work and organizing information at 3:13–3:22 make usefulness concrete and can remain. **SOURCE_QA:** page/upload alignment passes. **LISTENING:** none; second ASR confirms protected phrases and spoken pause instruction. Not ready for shipping.

### Candidate 3 — REPAIR, provisional; useful donor

**Teaching points:** Candidate 3 column above. Concise, preserves the Chinese Room steps and most exact passages, and supplies the strongest usable close. It omits the separate sentence/poem/conversation list and combines word choice and beauty in a human-human/AI-AI sequence. All five comparisons are still explained, so that combination is a clarity weakness, not missing teaching.

**Material issue:** 1:27.94–1:38.20 says the software strings together words “rather than actual comprehension,” then treats that as the reason for the lesson's conclusion. The source only says fluency alone cannot establish understanding. Delete that overclaim; the exact learned-pattern sentence ends at 1:27.18, and the following five-way comparison is a coherent next step.

**Hard requirements:** all protected passages except the initial “But sounding…” are present in the transcripts; the initial sentence drops “But,” without changing its meaning. Strict restoration can use Candidate 2's 0:40.88–0:46.48 sentence. Both closing lines are clean once the preceding “This final summary makes it clear” is excluded.

**Repair route if choosing 3:** replace the opening fluency passage with Candidate 2's examples and qualification (approximately 0:33.84–0:46.48); remove 3's 1:27.94–1:38.20 overclaim; optionally use 2's sequential word-choice/beauty block (2:33.04–2:52.76) instead of 3's interleaved 2:06–2:26. Keep 3's own exact closing lines. These are identified sources, not auditioned joins. Choosing 2 needs less substantive repair.

**Additions:** code and essay examples are relevant. The rhetorical question at 2:37 is answered immediately by the correct takeaway, so it is not an unanswered activity request. **Editing notes:** canonical board replacement, house emphasis, and removal of the engine outro remain normal production work. **SOURCE_QA:** page/upload alignment passes. **LISTENING:** none; medium.en confirms the problematic bridge and clean close.

## Proposed best-of edit

**BASE:** `Prompts/does-ai-think-2mp4.mp4`.  
**GRAFTS:** one required closing block from `Prompts/does-ai-think-3.mp4`, under the canonical close. No mid-lesson grafts proposed. The table above explains where optional richer wording was considered but does not warrant an additional seam.

- Keep Candidate 2 through “…the world the way we do.” Its final word ends at approximately **3:27.86**; provisional cut at **3:28.20**, within the gap before “As this final graphic states” starts at 3:28.52.
- Remove Candidate 2's complete closing block, including the spoken pause instruction and engine outro.
- Insert Candidate 3 **3:04.00–3:09.40**, including handles around the two sentences. Word onsets/ends from medium.en: **3:04.24–3:05.94**, “Sounds human. Works differently”; **3:06.74–3:09.04**, “A convincing answer doesn't prove understanding.” Exclude “This final summary makes it clear” at 3:02.02–3:03.52.
- Textual bridge: 2's conclusion → 3's two-line takeaway. No missing referent or repeated introduction. A voice/level/cadence audition is still required before certifying the graft.
- Audio-only preview: `audio-previews/proposed-2-to-3-close-context.wav`, with Candidate 2 from 3:09.50 through the proposed cut, then the donor. Join occurs 18.70 s into this preview. Original close and isolated donor are alongside it. This is an evaluation preview, not a video build; 5 ms edge fades are confined to the handles, with no added pause or loudness matching. Preview plan is recorded in JSON.
- The speech-gap estimate at the join is about **0.58 s** from ASR word boundaries, not a measured silence or an auditioned pacing decision. No extra pauses are proposed. Standard close motion may require a silent settled hold after narration; finalize in the production plan.

## Visual plan for Candidate 2

These placements use Candidate 2's source timeline, which stays unchanged until the close if no other audio edits are approved. Approximate cutaway times are proposals, not frame-final edit boundaries. Review motion with narration before retaining or replacing each animation. No candidate is penalized in its narration verdict for raw board crops, highlights, or marks.

| Board | Highlighting sequence | Camera | On screen / breaks | Purpose or exception |
|---|---|---|---|---|
| The Chinese Room | Full unmarked introduction; preserve the previously approved camera-only emphasis on complete step callouts, chart, and outside impression; full view for the takeaway | Dense: full view, complete callout zooms/pans, chart detail, then pullback. Do not copy Notebook's blurred dives or red annotations | Raw recreation **1:00.00–1:50.17**, 50.17 s. Proposed board windows about **1:00–1:06**, **1:09.5–1:25.7**, **1:32–1:50.17** (about 40.4 s total; longest 18.2 s), separated by the note/door drawing and person-inside-room drawing | Door drawing from 2's 0:46.23–0:50.80 supports the incoming note; room drawing from 0:52.97–1:00 supports the internal rule-following while the reply is returned. Return before the next callout/outside-observer sentence. Confirm source motion and exact handles; no new illustration needed for this initial proposal |
| When You Think. What AI Does. | One paired-row outline at Meaning **2:16.32**, Experience **2:24.04**, Word choice **2:33.04**, Beauty **2:42.52**, Uncertainty **2:52.76**; banner on the spoken takeaway at about **3:05.56** | Dense: full unmarked view from **2:07.97**, uniform complete-row dive/pan, full pullback for takeaway. Fixed 4 px on-screen strokes at 720p | Raw run **2:07.97–3:09.90**, 61.93 s. Proposed cutaways around **2:20.5–2:23.0**, **2:38.7–2:41.5**, **2:58–3:01.5**; approximately 53.1 s of board, longest uninterrupted stretch about 16.5 s if all fit | Re-time the base's learned-pattern/input sequence for the AI side of Meaning; use 1's independent next-word prediction sequence around 2:33–2:40 for Word choice. For confident-but-wrong, no clearly adequate existing scene identified: propose a purpose-generated realistic student checking a confident answer against source material under current 8d. Keep text minimal; do not replace a good animation with a still merely for polish. Final cutaway selection is provisional until motion review |
| Sounds human. Works differently. | Unmarked | Current canonical JPG, 48-frame hold, 150-frame push to 1.2×, settled final hold | Begins at the final graft boundary; duration depends on spoken close plus necessary visual settle | Candidate 3 supplies audio only; no Notebook closing recreation or engine outro remains |

The comparison's third cutaway is a proposed new asset, not generated or approved. Without it, the final board run would be about 28.4 s; record that exception rather than invent decorative filler. New custom supporting photography follows today's updated preference for realistic high-school-age students. Existing effective drawings remain eligible to keep.

### Supporting scenes to retain or review

| Candidate 2 source span | Teaching purpose and recommendation |
|---|---|
| 0:00–0:07.73 | Student typing into chat: retain after mark cleanup. Directly supports the opening action |
| 0:07.73–0:16.30 | Explanations/jokes/apology sequence: retain subject to motion review. Its illustrative punchline number is not automatically a factual error; a numerical-cleanup pass is not proposed solely because the example is invented |
| 0:16.30–0:21.27 | Student responding to the laptop: retain; supports the feeling that someone is there |
| 0:21.27–0:26.30 | Question-mark chip: retain; frames the lesson question |
| 0:26.30–0:40.70 | Human/model question and sentence/poem/conversation sequence: inspect timing and readability in playback. The example completion probability illustrates prediction; it is not a claimed benchmark. Do not flatten this sequence by default |
| 0:40.70–0:46.23 | Output/comprehension drawing: potentially useful distinction; retain if the complete reveal with cautious narration reads as two concepts, not proof that understanding is absent |
| 0:46.23–1:00.00 | Door/note, plaque, and room cutaway drawings: keep the relevant setup images and reuse the door/room for board breaks. Plaque is optional polish if it contributes nothing; do not remove merely for consistency |
| 1:50.17–2:07.97 | **Priority retain:** rulebook → learned network → input → next-word output sequence. Sequential frames at 1:53, 1:56, 1:59, 2:02, 2:05, 2:07.8 show the teaching progression. “The sky is…” and illustrative probabilities support the explicit rulebook limitation and learned prediction. No automatic probability removal; motion and narration still require audition |
| 3:09.90–3:13.43 | Files/gears: keep; organizes information under the usefulness conclusion |
| Approximately 3:13.43–3:21.9 | “Analytical Structuring” animation: keep provisionally; shows organization while narration describes analytical work. Small jargon labels may need a targeted readability treatment if playback makes them distracting, not wholesale replacement by default |
| Approximately 3:21.9–3:28.40 | Human/model comparison under the final caution: review completed labels and motion. Prefer a targeted label adjustment if it turns insufficient evidence into a categorical no-understanding claim |

**Standard cleanup:** replace actual course-board recreations with exact current JPGs, restore the photo panel in the comparison, apply house camera/highlights, remove the engine mark from retained Notebook scenes, and use the canonical close as the final frame. Reviewed samples did not reveal unknown-source stock photos outside course boards; this is not exhaustive every-frame clearance.

**Content corrections versus polish:** the spoken pause instruction and 3's comprehension overclaim are substantive edit issues. Board replacement and mark/outro removal are production standards. Trimming references to “the bottom of the board,” changing adequate but formal words, or replacing a relevant animation merely for visual consistency are optional, not reasons to reroll.

## Checks and remaining work

- Completed: source hashes, full transcripts for all three, source/lesson comparison, all contact sheets, selected full-resolution/sequential detail frames, selected second-model word timestamps, and an audio-only closing-join preview.
- Not completed: listening, continuous video review, pronunciation check at 2's 0:39, voice matching and join audition, exact silence measurements, all-frame mark/photo clearance, final cutaway-motion selection, or an encoded production candidate.
- Next production step: audition the two highlighted audio issues and the proposed closing join, finalize the board/cutaway plan, then build if authorized. No new generation is recommended on the evidence currently available.

Evidence files: `identity.json`; each candidate's `transcript.txt`, `scenes.txt`, `holds.txt`, `sheets/`, and `details/`; `verification-medium.json`; and `audio-previews/`. Raw candidates are preserved unchanged.
