# Does AI Think? — three-reroll evaluation, 2026-10-24

**Recommendation: use does-ai-think-4.mp4 as the base, with three whole-beat audio grafts and one narration cut. No fourth generation is recommended from the available evidence.** None of these raw versions earns KEEP as delivered. Version 4 is the most complete and the closest to the lesson; version 6 supplies a better word-choice explanation and the exact opening qualifier; version 5 supplies a clean useful-work conclusion.

This is a content evaluation and proposed full production plan, not a completed repair or shipping approval. No source video, installed video, lesson, board, or prep material was modified.

## Evidence and limits

Authority: the current `DoesAIThinkSection` in `index.html`, the current canonical Chinese Room and three-row comparison JPGs, the two closing lines, `lessons/does-ai-think.md`, and the current generation prompt. The lesson was read completely and both boards inspected, including 1280 × 720 full-view previews. `current-lesson.txt` and `lesson-source-identity.json` retain the evaluated source snapshot and hashes. `identity.json` records the exact three raw files, durations, frame counts, hashes, and candidate scene transitions.

Complete timestamped transcripts for all three files were produced with local faster-whisper base.en and read end to end. They are in `first-pass/`. A second model, small.en, checked the consequential qualifiers, errors, omitted Chinese reply, endings, and potential donors; see `passage-checks.json` and `audio-checks/`. Both models agree on the principal issues below. The initial full medium.en pass was stopped before it produced a complete transcript; it is not evidence for this review.

**Listening limitation:** no direct audio listening occurred. Transcripts cannot certify delivery, speaker compatibility, pronunciation, breaths, or seamless joins. All REPAIR verdicts below are provisional editorial judgments; the named audio exists and its wording has been checked, but donor joins have not been auditioned and are not verified repairs. Word times describe spoken content, not final frame-accurate splice boundaries.

**Visual limitation:** all 16 contact sheets were inspected, covering each file at four-second intervals with sequential decode. These establish sampled visual content, not end-to-end playback or animation quality in motion. Exact transition boundaries and retained animations need contextual playback before the build is locked. Detailed observations are in `VISUAL-NOTES.md`.

| File in Prompts | Duration | Editorial verdict | Role |
|---|---:|---|---|
| does-ai-think-4.mp4 | 3:36.27 | REPAIR, provisional | Recommended base; complete Chinese example, three rows, exact uncertainty pair and close |
| does-ai-think-5.mp4 | 4:24.73 | REPAIR, extensive and provisional | Useful-work donor; too many altered requirements and stronger philosophical claims for the base |
| does-ai-think-6.mp4 | 3:24.70 | REPAIR, provisional | Opening-qualifier and word-choice donor; missing spoken reply and added claims prevent KEEP |

## Teaching-point comparison and best-of selections

Times below are source-file times. Quotes reproduce the ASR text, with punctuation normalized for readability; they are not claims of direct hearing. RICH and TAUGHT both pass. The better beat is selected for teaching quality, not runtime or pictures.

| Teaching point | Version 4 | Version 5 | Version 6 | Best-of selection |
|---|---|---|---|---|
| Human-like replies create the question | **RICH**, 0:00–0:24: “It explains complex topics, tells jokes, and even says sorry…”; “Does AI actually think?” | **RICH**, 0:00–0:37: “It explains complex topics, it makes jokes…”; “Does AI actually think?” Longer and more embellished. | **RICH**, 0:00–0:39: “break down a complex poem, land a halfway decent joke…”; “is it actually thinking?” Adds the feeling of a “conscious mind.” | Keep 4: direct and closest to the lesson’s voice. |
| Sentence completion, poem and conversation show capability | **TAUGHT**, 0:24–0:32: “finish your sentence, write working code, and explain a poem”; conversation established in opening | **RICH**, 0:38–0:48: “finish your sentence…poem…hold a sustained conversation for hours” | **TAUGHT**, 0:00–0:18 and 0:34–0:39: natural responses, poem, jokes, coherent sentences; does not repeat sentence-completion example literally | Keep 4; no missing essential capability explanation. |
| Sounding human does not establish human-like understanding | **TAUGHT**, 0:33.20–0:37.64: “But sounding like a person doesn’t tell you whether it understands the way a person does.” Meaning preserved, required word “things” missing. | **TAUGHT**, 0:48.30–0:55.76: “producing a string of words that sounds human does not actually tell us whether the machine grasps the meaning…” Required sentence paraphrased. | **TAUGHT**, 0:39.66–0:44.16: “But sounding like a person doesn’t tell you whether it understands things the way a person does.” | Take complete sentence from 6 to meet the literal prompt requirement. |
| Chinese Room: person cannot read Chinese, follows symbol rules | **RICH**, 0:43.54–1:03.16: “does not know a single word of Chinese”; “giant rule book”; “match the symbols” | **RICH**, 1:07.90–1:38.60: cannot speak/read Chinese; exhaustive rulebook; matching visual shapes | **TAUGHT**, 0:52.30–1:02.80: person cannot speak/read Chinese; massive rulebook; steps then explain its use | Keep 4. Version 5 has more detail but repeats the setup at greater length without necessary new teaching. |
| Step 1: incoming note asks “How are you?” | **RICH**, 1:07.94–1:13.80: note under door; “The text asks, how are you?” | **RICH**, 1:42.42–1:48.78: “note that translates to, how are you?” | **RICH**, 1:04.80–1:10.22: note under door; “It asks, how are you?” | Keep 4. |
| Step 2: whole-phrase lookup without reading | **RICH**, 1:14.44–1:22.10: “They can’t read it, so they look up the entire phrase on a giant chart on the wall.” | **RICH**, 1:49.28–1:57.28: “look up the entire phrase on a giant reference…” Last noun uncertain in ASR, not needed as donor. | **TAUGHT**, 1:10.68–1:18.74: “take those unfamiliar shapes and visually match them on a giant look-up chart”; less explicit about whole phrase | Keep 4. |
| Step 3: matching reply “I’m fine, thank you!” returned | **RICH**, 1:22.10–1:32.46: “Write out the matching reply, meaning I’m fine, thank you, and slide it back…” | **RICH**, 1:58.04–2:06.92: “slide back a note that says, I’m fine, thank you.” | **MISSING worked answer**, 1:19.38–1:25.68: “select the exact matching set of symbols for the reply, and slide it back out.” Correct operation, but never speaks the actual reply. Second ASR confirms omission. | Keep 4. A visible reply on version 6’s board does not replace spoken teaching. |
| Outside fluency does not establish the person’s understanding | **RICH**, 1:33.60–1:39.70: “To anyone outside, it looks like fluent Chinese conversation”; “A convincing answer doesn’t prove understanding.” | **RICH**, 2:06.92–2:20.06: fluent native-speaker impression versus “zero comprehension”; takeaway paraphrased with “simply does not” | **RICH**, 1:25.68–1:35.56: exact outside line; “person inside comprehends nothing”; exact takeaway | Keep 4. The person’s non-understanding is part of the hypothetical; it does not itself establish a claim about LLMs. |
| Producing an answer and understanding it are not necessarily the same | **TAUGHT**, 1:40.80–1:46.88: exact distinction | **WRONG qualifier / required distinction missing**, 2:41.46–2:54.08: “underlying reality remains identical to the thought experiment”; fluent paragraph “gives us no evidence” | **TAUGHT**, 1:36.82–1:43.60: exact cautious distinction, although later claims undermine it | Keep 4. |
| Analogy limit: an LLM uses patterns learned in training, not literal rulebook | **TAUGHT**, 1:48.06–1:54.14: exact two sentences; followed by a problematic addition | **THIN / misleading**, 2:25.90–2:40.68: denies physical rulebook, then “relies on petabytes of training data” and “scans vast webs of text patterns”; shifts toward consulting data and invents scale | **TAUGHT**, 1:49.38–1:59.42: literal-rulebook limit and exact learned-pattern explanation; followed by a wrong optimal-sequence claim | Keep 4’s 1:48.06–1:54.14. |
| Fluency alone is insufficient evidence; preserve bridge into comparison | **TAUGHT**, 2:07.14–2:14.14: “an articulate output alone is not proof of internal comprehension.” Earlier 1:54.92–2:06.04 overclaims the mechanism. | **WRONG strength**, 2:45.82–2:54.08: “gives us no evidence” after claiming identical underlying reality | **WRONG strength**, 2:04.92–2:09.76: “simply an invalid metric for judging true comprehension” | Keep 4’s cautious bridge; cut its earlier extra mechanism passage. |
| Exactly three comparisons in current order | **TAUGHT**, 2:15.20–3:00.54: Experience and meaning → Word choice → Uncertainty | **TAUGHT**, 2:54.64–3:55.60: explicitly “three distinct areas,” same rows | **TAUGHT**, 2:10.70–2:53.36: same three rows, no obsolete separate beauty section | All match the structural change. Keep 4’s introduction. |
| Experience and meaning: lived experience versus learned patterns and input | **RICH**, 2:19.74–2:33.66: “things you have actually lived through”; words connected to “physical and emotional realities”; AI uses “learned data patterns and whatever information you tell it in the prompt” | **RICH**, 3:02.32–3:19.04: lifetime of experience; words tied to lived events; patterns learned in training and prompt | **TAUGHT, wording uncertain**, 2:19.16–2:30.08: human side closely matches source; both ASRs produce “AI solely uses learned patterns in what you tell it in a prompt.” Direct listening is needed to distinguish “in” from “and.” | Keep 4. Version 6’s more literal human side does not justify importing ambiguity into the AI side. |
| Word choice: intent versus predicting next word and repeating | **WRONG overstatement**, 2:34.70–2:46.84: “next most likely word” adds an always-top-choice implication absent from the lesson | **WRONG overstatement**, 3:20.00–3:33.14: “most probable next word…until the sentence is finished” | **RICH**, 2:30.86–2:39.20: “select words to express what you want to say”; “AI algorithmically predicts the next word, then repeats.” | Take complete word-choice beat from 6. Keeps the repeat loop without the top-choice claim. |
| Uncertainty: people can notice uncertainty; AI can sound certain when wrong | **TAUGHT**, 2:46.84–2:56.30: “You can notice when you are unsure”; “AI can sound certain even when it is wrong.” | **WRONG addition**, 3:36.46–3:48.74: “possess the self-awareness”; “Because an AI lacks a mind to be self-aware…” Replaces the qualified comparison with a philosophical explanation. | **TAUGHT**, 2:40.06–2:46.64: both required clauses present, “can” retained | Keep 4; no need to graft adequate teaching. |
| Similar-looking answers can arise from different processes | **TAUGHT**, 2:57.04–3:00.54: exact required sentence | **TAUGHT meaning / hard line missed**, 3:50.90–3:55.60: “can be produced by vastly different underlying processes” | **TAUGHT**, 2:47.18–2:53.36: extra setup then “but similar looking answers can come from very different processes” | Keep 4’s direct standalone takeaway. |
| AI is still useful and can do impressive work | **TAUGHT usefulness, WRONG added claim**, 3:01.60–3:15.88: “useless just because it lacks human comprehension”; impressive tasks; mechanics “look nothing like a human brain” | **RICH**, 3:56.54–4:06.88: “Pointing this out does not mean artificial intelligence is useless”; “summarize legal documents, write complex code, and do highly impressive valuable work…” | **TAUGHT usefulness, WRONG added claim**, 2:54.34–3:08.80: “Acknowledging this lack of understanding”; impressive work; “utility and cognition” | Take 5’s complete two-sentence useful-work beat. Accurate examples support the point and avoid assertion of absent understanding. |
| Final human-sounding output is not enough to establish understanding | **TAUGHT**, 3:18.68–3:26.08: output sounding like a person is “never enough evidence…understands the world the way you do” | **TAUGHT**, 4:11.30–4:21.16: convincing answer is not enough to prove understanding | **TAUGHT**, 3:09.82–3:14.88: human-sounding output is “never enough to prove…grasps the material” | Keep 4 after the useful-work donor. |
| Exact two-line close, last spoken words | **TAUGHT / MET**, 3:26.80–3:32.46: “Sounds human. Works differently.” “A convincing answer doesn’t prove understanding.” | **MISSING exact close**, 4:07.50–4:21.16: “But it sounds human, while working entirely differently…” then a longer paraphrase | **TAUGHT / MET**, 3:15.52–3:20.92: exact two-line close | Keep 4. |

## Hard requirements

These are literal prompt requirements, separate from meaning-level coverage. Punctuation, capitalization, and “rulebook” versus “rule book” in ASR are not spoken differences.

| Required wording or behavior | Version 4 | Version 5 | Version 6 |
|---|---|---|---|
| “But sounding like a person doesn’t tell you whether it understands things the way a person does.” | MISSED: omits “things” at 0:33 | MISSED: paraphrase at 0:48 | MET at 0:39 |
| “To anyone outside, it looks like fluent Chinese conversation.” | MET at 1:33 | MISSED literal line at 2:06, meaning taught | MET at 1:25 |
| “The Chinese Room illustrates a distinction: producing an answer and understanding it aren’t necessarily the same thing.” | MET at 1:40 | MISSED; later claim is stronger | MET at 1:36 |
| “An LLM doesn’t follow a literal rulebook. It uses patterns learned during training to predict its response.” | MET at 1:48 | MISSED: altered mechanism wording | MET at 1:52 |
| “You can notice when you are unsure.” | MET at 2:50 | MISSED at 3:36 | MET within introduction at 2:40 |
| “AI can sound certain even when it is wrong.” | MET at 2:53 | MISSED at 3:41 | MET at 2:44 |
| “Similar-looking answers can come from very different processes.” | MET at 2:57 | MISSED exact words at 3:50 | MET after “but” at 2:50 |
| “A convincing answer doesn’t prove understanding” after Chinese Room | MET at 1:37 | MISSED exact words at 2:17 | MET at 1:33 |
| Exact final two lines, nothing spoken afterward | MET at 3:26–3:32 | MISSED at 4:07–4:21 | MET at 3:15–3:20 |
| Chinese question AND matching reply spoken | MET at 1:12 / 1:27 | MET at 1:42 / 2:02 | MISSED reply; only question at 1:09 |
| Three rows, correct order, no separate Beauty / five-part structure | MET | MET | MET |
| No narration of lab or group activity | MET | MET | MET |

## Per-roll verdicts and repair routes

### Version 4 — REPAIR, provisional; recommended base

**Errors/material additions:** 1:54.92–2:06.04 expands the mechanism into “built entirely to calculate the next most probable word, rather than to comprehend your prompt.” This both adds a top-word restriction and turns a cautious evidence distinction into an asserted purpose/understanding contrast. 2:41.44–2:46.84 repeats “most likely word.” 3:01.60–3:15.88 asserts a lack of human comprehension and that the internal mechanics look “nothing like a human brain.” These go beyond the current lesson and its explicit prompt guardrails. The omitted “things” at 0:33 is a literal-prompt miss, not a substantive teaching error; the available complete donor can restore it without word splicing.

**Source QA: PASS.** The current lesson is coherent; no material source correction was identified. The failed qualifiers are generator additions. The current three-row board is correct.

**Useful additions:** physical/emotional context is a clear expression of lived experience; working code is a reasonable capability example. Preserve them. The extra mechanism exposition and categorical conclusion are not useful additions.

**Repair plan:** the three grafts and one cut in the selected edit plan below resolve the identified failures at the transcript level. Listening and seam verification remain outstanding.

**Editing notes:** canonical board inserts and standard close; replace overclaiming/jargon-heavy explanatory graphics; retain relevant drawings; corner mark/end slate cleanup. Details below and in `VISUAL-NOTES.md`.

**Listening:** no direct listening or end-to-end playback; no verified audio joins.

### Version 5 — REPAIR, extensive and provisional; donor only

**Errors/material additions:** 2:31–2:40 gives an unrequested “petabytes” scale and frames the response as scanning vast text patterns. 2:41–2:54 says the underlying reality is “identical” to the thought experiment and that fluency provides “no evidence,” which is stronger than “alone is insufficient.” 3:26–3:33 adds most-probable-next-word selection. 3:41–3:48 asserts that AI lacks a mind and derives its certainty from absent self-awareness. Most required literal passages and both exact closing lines are paraphrased. Do not select this as the base merely because it is longest.

**Source QA: PASS.** **Useful addition:** the two-sentence useful-work beat at 3:56.54–4:06.88 gives concrete examples without asserting a lack of understanding. Use that donor.

**Repair route if retaining this version:** replace 0:48.30–0:55.76 with version 6’s 0:39.66–0:44.16 qualifier; replace its 2:06.92–2:20.06 outside/takeaway with version 4’s 1:33.60–1:39.70; replace its 2:21.06–2:54.08 analogy transition with version 4’s 1:40.80–1:54.14 plus 2:07.14–2:14.14; replace its comparison block 2:54.64–3:55.60 with version 4’s introduction/first row, version 6’s word-choice beat, and version 4’s uncertainty/takeaway as selected above; replace 4:07.50–4:21.16 with version 4’s 3:18.68–3:32.46 qualification and exact close. These identified complete beats avoid another generation but amount to rebuilding much of version 5. All joins would need audition; this is not the recommended assembly.

**Editing notes:** useful door, manual, lookup, chat and server drawings; long Chinese Room and comparison holds need cutaways. The quoted claims cannot be fixed with visual replacement alone.

**Listening:** no direct listening; no verified audio joins.

### Version 6 — REPAIR, provisional; two selected donor beats

**Errors/material additions:** the matching reply is never spoken, despite being shown. At 2:00.22–2:04.04 it says an LLM “calculates the mathematically optimal sequence of text,” overstating the next-word mechanism. At 2:04.92–2:09.76 it calls fluency “simply an invalid metric,” rather than insufficient evidence on its own. At 2:54.34 it starts “Acknowledging this lack of understanding,” asserting what the lesson deliberately does not conclude. The first comparison’s AI wording is ambiguous in both transcriptions (“patterns in what you tell it”); do not use it as a donor without listening.

**Source QA: PASS.** **Useful beats:** exact opening qualifier, literal human-side comparison wording, correct word-choice loop, cautious uncertainty pair, exact close. Select only the qualifier and whole word-choice beat; other adequate material already exists in the base.

**Repair route if retaining this version:** replace the worked steps at 1:04.80–1:25.68 with version 4’s complete 1:07.94–1:32.46 example, including both Chinese phrases; replace 2:00.22–2:09.76 with version 4’s 2:07.14–2:14.14 cautious fluency bridge; replace the ambiguous first-row beat 2:19.16–2:30.08 with version 4’s 2:19.74–2:33.66 complete first row; replace 2:54.34–3:08.80 with version 5’s 3:56.54–4:06.88 useful-work beat. Preserve its own exact close. These are identified donor routes, not auditioned repairs; using version 4 requires fewer substantive replacements.

**Editing notes:** categorical “OUTPUT ≠ UNDERSTANDING,” consciousness definitions and TOOL ≠ MIND graphics overstate the lesson even where the spoken line is cautious. Correct or replace them. Keep useful drawn setup/server/lookup scenes only after checking motion and narration together.

**Listening:** no direct listening; no verified audio joins.

## Selected production proposal: version 4 base

Scope: a full production pass on the new raw version, using the current canonical boards and the established highlighting interaction. This plan is proposed for review; prior approval of the old v11 repair does not determine new donor timings. A finished candidate must receive fresh narration and whole-file QA before installation.

### Narration: three whole-beat grafts and one cut

Times specify speech intervals; build boundaries must be placed in adjacent natural gaps after listening and waveform inspection. Do not make the edits directly at ASR word boundaries.

| Change | Base version 4 speech | Replacement / resulting connection | Why and placement |
|---|---|---|---|
| Graft 1 | 0:33.20–0:37.64, “But sounding like a person…understands the way a person does.” | **Version 6, 0:39.66–0:44.16:** “But sounding like a person doesn’t tell you whether it understands things the way a person does.” | Restore the exact required sentence. Whole sentence, nearly identical duration (4.44 versus 4.50 s). Under the base’s relevant fluency/understanding drawing, not a course board; retain scene coherence and check voice match. |
| Cut 1 | 1:54.92–2:06.04, “Because the system is built entirely to calculate the next most probable word, rather than to comprehend your prompt, its conversational fluency is simply a byproduct of mathematical pattern matching.” | Join “It uses patterns learned during training to predict its response” (ends 1:54.14) to “Knowing how this predictive mechanism operates…an articulate output alone is not proof…” (starts 2:07.14). | Removes the unsupported mechanism claim while keeping the explanation and its connection to the takeaway. Remove associated overclaiming diagram span; no new silence proposed. |
| Graft 2 | 2:34.70–2:46.84, entire “Second, consider word choice…” beat ending “repeats that cycle.” | **Version 6, 2:30.86–2:39.20:** “For word choice, you actively select words to express what you want to say. AI algorithmically predicts the next word, then repeats.” | Complete two-sided row, under the canonical comparison. Retain base first row before it and “Finally, look at uncertainty” after it. Removes always-most-likely wording. |
| Graft 3 | 3:01.60–3:18.34, from “None of this means…” through the two overclaims and “But as this final graphic states,” | **Version 5, 3:56.54–4:06.88:** “Pointing this out does not mean artificial intelligence is useless. These tools can summarize legal documents, write complex code, and do highly impressive valuable work at massive scale.” Then base 3:18.68: “Generating an output that sounds like a person is never enough evidence…” | Two complete donor sentences, followed by the base’s complete final qualification. Removes categorical claims without chopping dependent clauses. Use matching useful-work drawings from version 5, whose corresponding scene block starts near 3:56.67; confirm exact cuts and extend/re-time the first drawing over the small offset. This is the second Notebook-scene graft exception; source/target durations and animation must be fitted coherently. |

**Grafts: three; one under a course board and two under Notebook supporting scenes.** The opening sentence differs by only about 0.06 s; the useful-work graft can carry its own matching drawing sequence. These are feasible visual approaches, not confirmation of audio compatibility. All six donor entry/exit joins plus the mechanism cut need direct listening in context. If a voice or cadence mismatch prevents a clean graft, resolve that before building; do not assume identical Notebook voices.

The remaining narration, including complete Chinese Room example, first comparison, exact uncertainty pair, takeaway, final qualification and two-line close, stays from version 4. No shortening based solely on duration is proposed. The philosophical additions are the reason for the cuts.

### Board highlighting and camera plan

Table times refer to the base source or donor speech, before timeline changes. Board timings and sampled source scenes are provisional until exact cuts are decoded and the selected audio joins are reviewed. All boards first appear complete and unmarked; outlines are 4 px at 720p, without fills. Current fonts, wording and layout remain unchanged.

| Board | Highlighting sequence | Camera | Planned on-screen time / breaks | Reason or exception |
|---|---|---|---|---|
| **The Chinese Room** | Start around base 1:04.13, unmarked; step 1 at 1:07.94; step 2 at 1:14.44; step 3 at 1:22.10; outside-impression panel at 1:33.60; gold takeaway at 1:37.58. One complete panel at a time. | Full view for at least two seconds; then established complete-step camera walk. Keep the phrase/reply illustration with each active card. Pull back for takeaway. | Topic leg about 36.6 s, through 1:40.70. Proposed cutaways at base 1:17.5–1:21.1 to its own rulebook drawing (source approximately 0:51.57–0:55.17), and 1:29.6–1:32.6 to its own outgoing-note drawing (source approximately 0:58.13–1:01.13). About 30 s total board exposure; longest proposed uninterrupted run about 13.4 s. | Source crop/washes are replaced with the canonical JPG. The drawings explain lookup and return, while breaking a long hold. Return before the next panel’s spoken onset. |
| **When You Think. What AI Does.** | Base introduction around 2:15.20; Experience and meaning at 2:19.74; donor word-choice onset at version 6 2:30.86 after graft; base uncertainty at 2:46.84; exact takeaway at 2:57.04. Outline each complete row across both columns, not isolated words. | Clean full-board opening, then complete-row zoom/pan only enough to improve reading, with a consistent camera window. Pull back for gold banner. Preview the first long row before locking framing. | About 42 s after replacing the 12.14 s word-choice beat with the 8.34 s donor. Propose two three-second drawing breaks roughly 15–18 s and 32–35 s after this leg begins, placed after row emphasis has been established and returned before the next target. Use version 5’s student-at-laptop drawing near 0:00–0:04 for input, and version 4’s question-mark drawing near 0:15.23–0:19.8 for uncertainty. Roughly 36 s board exposure; maximum planned continuous run about 15 s. | Replaces the face-free blank photo area, yellow washes and cropped rows. The three-row board gets the same established interaction. Cutaway positions must follow final audio timing rather than the old v10/v11 coordinates. |
| **Sounds human. Works differently. / A convincing answer doesn’t prove understanding.** | Unmarked canonical close; exact spoken lines retained from base 3:26.80–3:32.46. | Standard 48-frame hold, 150-frame push to 1.2×, then settled hold at 30 fps; extra time goes into hold. | Start on closing line, retain enough final hold to finish motion; end on the canonical board. Remove branded end slate starting near source 3:33.27. | Preserve the lesson’s exact closing wording and standard appearance. |

The proposed 15-second maximum board run is a plan target, not a measured finished-file result. Recalculate after final cuts; no build exists yet.

### Retain, correct, replace

- **Retain candidates:** version 4’s opening conversational drawings; Chinese Room door/room/book/note drawings at roughly 0:38.6–1:04.1; its producing-versus-understanding drawing at 1:40.7–1:47.9 if contextual playback supports the cautious narration. Retain the nonliteral-rulebook / learned-pattern explanation scene at 1:48–1:54 only after checking labels and timing in motion. Preserve useful motion, rather than replacing every scene with a still.
- **Content corrections:** remove or correct diagrams that add absent semantic-comprehension modules, conscious-grounding assertions, “nothing like” conclusions or verified-output guarantees. The new useful-work donor can use version 5’s corresponding computer/server drawings around 3:56.67–4:07.7 instead of version 4’s jargon-heavy utility/internal-mechanics graphics. Any remaining unsupported labels need targeted repair.
- **Standard cleanup:** all actual course-board recreations become the current canonical JPGs; apply established outlines; replace close; remove corner mark and branded end slate. No new stock photos were positively identified outside course-board imagery in the sampled frames, but that is not a whole-file clearance.
- **Optional polish:** simplify unrelated formula/jargon visuals in the opening if they distract in playback. Their mere presence does not make narration fail. Illustrative probability graphics are assessed for what they teach, not automatically treated as empirical claims; the problematic wording identified above still needs audio repair.
- **New custom illustrations:** none proposed at this stage; relevant drawings exist across the three rolls. Confirm their animation quality and exact source spans before relying on them.

### Pauses and verification

No extra pauses are proposed from a transcript-only review. Preserve natural source gaps and check the seven join boundaries in context; do not insert a standard second for each board or row. If listening reveals a comprehension or cadence problem, measure the actual gap and specify a targeted adjustment before the build.

A repaired candidate must be re-transcribed for full teaching coverage, listened to end to end, and visually reviewed in motion. Verify canonical board framing, every ring, all transition seams, longest unbroken board run, mark cleanup, exact closing lines and final frame. The current recommendation does not certify those future checks.
