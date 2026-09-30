# Make Your Move — current local video evaluation, September 30, 2026

Candidate: `course-assets/make-your-move/make-your-move.mp4`, approximately **5:01.53**. The `makeyourmove` entry in `index.html` references this file with `v=20260925notecut`. This evaluates the local file, not a verified public deployment. Source SHA-256 is recorded in `source.json`.

**Recommendation: keep the teaching; prioritize a targeted visual polish pass if revisiting this video.** The basketball hook, six career examples, four transferable skills, and four practical actions form a coherent lesson for high-school students. The actions are particularly strong: talk to someone doing the work, learn enough to catch AI's mistakes, produce something real, and accept responsibility for a result.

**Narration verdict: KEEP on transcript evidence, with listening verification outstanding.** All 20 essential teaching points below are RICH or TAUGHT, and both required closing lines are present. No material narration cut or graft is required. Wording qualifications and optional tightening are listed separately from this verdict.

**Review limitation:** this is a transcript, sampled-frame, and technical evaluation. I have not listened to the audio or watched continuous playback with sound. Voice quality, audible seams, and animation timing remain unverified; this report is not a completed ship checklist. The current lesson page, Markdown, and all five current board assets were inspected. The separate interactive lab remains on the page for both reading and video routes; it is not treated as narration that the video must recite.

## Findings, in priority order

1. **The career sequence is the main engagement weakness.** The first board runs approximately **0:50–1:46 (56 seconds)**; the second **1:50–2:38 (47 seconds)**. Narration continues teaching throughout, so these are not empty holds, but six consecutive AI/help–human/responsibility lists create the most repetitive stretch. The four-second strategy drawing between the boards helps only briefly. Preserve all six examples; improve visual variation before cutting teaching.
2. **The existing cutaways in the second half are useful.** The conversation at **4:00–4:06**, keyboard and notes at **4:15–4:20**, and volunteer scene at **4:40–4:45** make the advice concrete. Keep them. The earlier September 24 review proposed removing several such scenes; that proposal should not be carried forward under the September 29 Edit Spec, which explicitly preserves useful supporting scenes, including during a board topic.
3. **Career wording is stronger than the lesson.** The boards consistently say “AI may help”; narration uses “AI can handle,” “AI excels,” and “AI generates.” Most concerning is **about 1:18**, “the human tasks remain untouched.” In context it introduces relationships, motivation, adaptation, and community, so the intended human-responsibility distinction reaches the viewer. Still, “untouched” can imply those tasks will not change. Prefer “People still own…” in a future narration revision. The electrician example adds “live wires,” and the transition at **1:47** calls the next group “physical and trades work,” although it includes design and entrepreneurship. These are wording cautions, not reasons to discard the whole roll.
4. **The opening can be tighter.** The core hook and AI connection are complete by **0:28**. “Theory and practice can only take you so far. It is time to step onto the court and put those skills to work in the real world” repeats the invitation to act through about **0:35.6**. Optional cut: remove that extension and its “YOUR NEXT MOVE” intertitle. Preserve the basketball setup. Exact word boundaries and the resulting join need an audible check before editing; this is not a verified splice plan.
5. **Audio headroom needs attention on a future render.** The decoded file measures **−17.2 LUFS integrated**, **4.4 LU loudness range**, and approximately **+0.1 dBTP**. Seven decoded samples exceed full scale; the largest is at **1:28.78**. This is a measurable overshoot, not proof of audible distortion. Audition that sentence, then use modest peak control/headroom if rebuilding. Full decode completed without reported decoding errors; no black interval was reported by the scan.

The September 25 removal of the Nate and Luke note is present and agrees with the current lesson. That note is no longer required. The new join at **0:35.80** has a measured quiet interval **35.617–35.927 seconds (0.311 seconds)**; it is shorter than the surrounding major section gaps. Its flow needs listening before deciding whether to lengthen it. Do not automatically add a pause.

The completed current-file board scan (`board-spans.txt`, half-second sampling) measures the career runs at **56.5 and 47.5 seconds**, confirming the main pacing finding. The skills board's separate runs are **6, 18, and 14 seconds**; the actions board's are **8, 8.5, and 19.5 seconds**. Those later sections already have the visual breaks the career section lacks. The longest unbroken board run is therefore **56.5 seconds**.

## Narration assessment

The teaching-point assessment below uses approximate current-video timestamps. Each career is judged on whether it teaches both AI assistance and human responsibility; omitted alternatives in an example list are recorded without treating every alternative as a separate essential concept.

The current file was freshly transcribed using faster-whisper `base.en`; all 93 segments in `make-your-move/transcript.txt` were read in full. Its wording agrees with the retained September 24 transcript after the note removal. ASR timestamps are coarse, and some segments extend into measured silence; they are evidence for teaching coverage, not edit boundaries. Seven contact sheets sample the entire runtime at four-second intervals. Additional 1280×720 frames were inspected for career and skills framing, and the literal last decoded frame at 301.466667 seconds shows the closing board.

| Teaching point | Assessment | Evidence / qualification |
|---|---|---|
| Basketball fundamentals, practice, improvement | RICH | 0:00–0:09: team with friends, fundamentals, drills, and improvement. |
| Move from practice to participation | RICH | 0:09–0:16: “Are we joining a league or just practicing forever?” |
| Apply the AI understanding and skills already learned | RICH | 0:16–0:28: models, skills, and deciding what to do with them. |
| Jobs consist of tasks affected differently | RICH | 0:36–0:52: a job is “a collection of distinct tasks”; not every task is affected the same way. |
| Doctor | RICH | 0:53–1:12: records, research, and patterns versus examination, context, explanation, and responsibility. “Uncertainty” is not named separately. |
| Teacher | TAUGHT | 1:13–1:30: plans/practice versus knowing students, motivation, adaptation, and community. Reviewing student work is omitted; “untouched” is too absolute. |
| Lawyer | TAUGHT | 1:30–1:46: case search and drafts versus advice, strategy, persuasion, and liability. Document summaries omitted; “persuade a jury” narrows “persuade others.” |
| Electrician | TAUGHT | 1:50–2:05: manuals and possible causes versus safety, real-world diagnosis, and adaptation. Work planning omitted. |
| Graphic designer | RICH | 2:05–2:20: drafts and variations versus purpose, audience, taste, and final direction. |
| Entrepreneur | TAUGHT | 2:20–2:36: research, plans, organization versus choosing problems, risk, customers, and leadership. Comparing options omitted; ownership of decisions is conveyed through responsibility. |
| Why transferable skills follow the examples | TAUGHT | 2:38–2:50: human responsibility leads to capabilities usable across careers. Increasing AI task coverage is established by the preceding examples rather than repeated. |
| Work well with people | RICH | 2:50–3:00: listening, explanation, collaboration, trust, and leadership. |
| Critical thinking and judgment | RICH | 3:01–3:14: deciding what matters, evaluating information, trade-offs, and responsibility; more generated content gives a reason for the skill. |
| Create and solve problems | RICH | 3:15–3:27: new angles, combining ideas, testing possibilities, and improvement. |
| Stay curious and flexible | RICH | 3:28–3:40: continued learning, tools, approaches, and changing methods. |
| Act without deciding an entire future | RICH | 3:41–3:55: actions work for students with a career in mind and those still exploring. |
| Learn from people in the field | RICH | 3:55–4:06: ask about a normal week, change, and student misunderstandings. |
| Build real depth | RICH | 4:07–4:20: class, practice, feedback, and enough knowledge to spot AI's errors and missed nuances. |
| Make something real | TAUGHT | 4:21–4:33: projects, events, business, problem solving, and tangible proof. Research omitted as one possible project type. |
| Step into responsibility | TAUGHT | 4:33–4:44: clubs, volunteering, leadership, and delivering a result for others. Organizing something is not listed separately. |

**Hard requirements:** both closing lines appear in the narration: “You know how to be smarter than the tool,” around **4:51–4:53**, and “Keep learning. Keep building. Make your move,” around **4:54–4:57**. The first follows a longer lead-in, as in the previous review. The measured quiet tail begins at **4:56.94** and lasts approximately **4.61 seconds**.

**Source QA:** the current page's core lesson and current Markdown agree in meaning. Five active board assets support the career, skills, actions, and closing sections. The retained note JPG is not referenced by this lesson and is not a missing video scene. No material contradiction was identified in the teaching source. Workflow tracker status was not checked or changed.

**Additions worth retaining:** the career-as-tasks explanation counters an all-or-nothing view of professions; the increased-volume-of-content explanation strengthens critical thinking; “errors and nuances” gives a good reason to build depth. The opening's final eight seconds add less teaching value.

## Proposed board and camera plan

This is an evaluation proposal, not an executed edit. Timings refer to the current file and would shift if the optional opening trim were adopted. Preserve narration unless a separate wording repair is planned with verified donor audio.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| How AI Might Change Careers (1 of 2) | Doctor → Teacher → Lawyer. On a rebuild, introduce each whole card, then highlight “AI may help” and “People still own” as those two sections are explained. | Full board; avoid a slight zoom that clips the heading while barely enlarging the tall cards. | Current 0:50–1:46. The unbroken run is the priority for added visual variety. | Preserve every example. No new supporting asset or verified donor has yet been selected; do not pretend this is a finalized cutaway build plan. |
| How AI Might Change Careers (2 of 2) | Electrician → Graphic Designer → Entrepreneur; same whole-card introduction and two-section progression. | Full board, readable text and complete cards. | Current 1:50–2:38; keep strategy drawing immediately before it. | Same long-hold issue; a relevant work-in-progress cutaway would help, subject to asset selection. |
| Four Skills to Build | Work Well with People → Critical Thinking and Judgment → Create and Solve Problems → Stay Curious and Flexible. Whole-card rings suffice for these short explanations. | Full view, then complete active-card zooms, then pull back. | Approximately 2:47–3:41; preserve supporting people-skills sequence around 2:53–3:00 and creative-thinking sequence around 3:18–3:27. | Dense 2×2 board benefits materially from the card zooms. Keep useful introductory drawings at 2:38–2:47 under Edit Spec 8b. |
| Moves to Make | Learn from People in the Field → Build Real Depth → Make Something Real → Step into Responsibility. | Full view, then complete-card zooms. | Approximately 3:52–4:45, interrupted by conversation 4:00–4:06, keyboard/notes 4:15–4:20, volunteering 4:40–4:45. | The illustrations reinforce real action. Preserve city/foundation introduction around 3:41–3:52. |
| Closing board: You know how to be smarter than the tool. / Keep learning. Keep building. Make your move. | Unmarked. | Preserve the existing hold/push/settled framing unless a motion check reveals a problem. | Approximately 4:45–5:01.53. | Both lines are legible in sampled frames. Tail gives the call to action time to land. |

Apply the current fixed 4-pixel on-screen ring standard at 720p to any rebuilt span. Do not rebuild unchanged spans solely because they predate that rule.

The completed ring scan (`ring-stroke.txt`) reads approximately **6–7 solid pixels** for the stable career outlines, consistent with their visibly heavy appearance in the full-resolution frame. Larger automatic detections inside the blue/amber illustrations are not reliable outline measurements and are not being reported as ring defects. The existing small career zoom also crops the board heading while preserving the active card; staying at full view would avoid that crop without sacrificing much text size.

## Supporting scenes to preserve

- **0:00–0:28:** basketball practice, decision, and learned-skills sequence; establishes the hook and connects it to AI. Retention is provisional for motion quality because only sampled states were inspected.
- **0:36–0:50:** career monolith followed by distinct task tiles; useful visual representation of the central distinction.
- **1:46–1:50:** people at a strategy board; breaks the career lists and illustrates real-world collaboration.
- **2:38–2:47:** clipboard and team meeting; supports developing capabilities and responsibility.
- **2:53–3:00:** active-listening/clear-explanation sequence; expands the people-skills card.
- **3:18–3:27:** new angles, combining ideas, and testing options; unfolds the creative-thinking process.
- **3:41–3:52:** city on a foundation; supports practical steps built on learned skills.
- **4:00–4:06:** conversation; directly supports talking with someone in the field.
- **4:15–4:20:** keyboard and notes; supports serious learning and feedback.
- **4:40–4:45:** donation drive; concrete responsibility for other people.

No new pause is proposed without listening. Preserve the existing major section gaps; the 0:35.80 note-removal join is the one specific place to audition for breathing room. The opening trim, if chosen, must preserve a natural transition into the careers explanation.

No video, lesson, source asset, or tracker entry was changed during this evaluation.
