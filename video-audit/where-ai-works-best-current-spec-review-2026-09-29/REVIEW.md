# Where AI Works Best — current-spec evaluation, September 29, 2026

**Recommendation: targeted repair.** The current edit preserves the lesson's main teaching arc, all nine required lines, the current boards, and useful supporting drawings. It does not fully satisfy the current production and complete-example requirements: the translation example is absent, and four highlight runs measure 5 px instead of 4 px. A complete listening/motion review remains outstanding; this report is not a new shipping certification.

## File and scope

- Evaluated the local course file `course-assets/where-ai-works-best/where-ai-works-best.mp4`, referenced by `index.html:1112` with cache key `20260927ship4`.
- 3:52.033; 1280×720; 30 fps; 6,961 frames; 22,927,071 bytes.
- SHA-256 `89f85d327a9fa48b855b89055f66120b036e14a839ea943233a9828ed6ef225d`. It matches both `Prompts/where-ai-works-best-v7.mp4` and the September 27 build manifest exactly.
- Evaluation only. No video, lesson, canonical asset, generation prompt, or shared spec was modified. Public deployment and the Video Tracker were not queried; no new claim about public status is made.
- Authorities: current `index.html` lesson (`WhatItDoesBestSection`, starting at line 8803), `lessons/where-ai-works-best.md`, current generation prompt, and the September 29 versions of `scripts/video/README.md`, `NARRATION-REVIEW.md`, and `EDIT-SPEC.md`. The September 26 approved plan and September 27 build report supply historical context, not substitute verification.

## Findings

### 1. Restore the missing translation example (1:12–1:24)

The page and upload source list four Reshape examples; the generation prompt explicitly requires all four. The fresh encoded-file transcript contains study notes, a voice memo, and technical instructions, but never “translate a message into another language.” The visible board contains that fourth example; that does not make it spoken teaching.

This is a completeness defect, not an inaccurate explanation of reshaping. A plausible existing donor is roll 1, **1:15.68–1:28.36**:

> For example, take messy notes and have AI organize them into a clean study guide. Turn a scattered voice memo into a strict to-do list, translate a message, or rewrite technical instructions into plain English.

Use the complete examples beat, not a cut-out phrase. Its source hash still matches the September 26 transcript's build record. That wording restores the translation example, although “into another language” is compressed. Donor audio and the proposed joins have **not** been auditioned, so this is an identified repair candidate, not a verified clean graft.

### 2. Four highlight runs exceed the current fixed width

Fresh `ring_stroke.py` measurements reproduce the previously reported defect:

| Sampled output interval | Highlight | Measured | Required |
|---|---|---:|---:|
| 1:30.00–1:35.00 | Explore Possibilities — WHY IT FITS AI | 5 px | 4 px |
| 2:36.00–2:42.00 | Work Through Problems — WHY IT FITS AI | 5 px | 4 px |
| 2:42.50–2:50.50 | Work Through Problems — WHAT IT DOES | 5 px | 4 px |
| 3:02.00–3:05.00 | Work Through Problems — returning WHAT IT DOES | 5 px | 4 px |

Intervals are 0.5-second measurement samples, not exact edit boundaries. Other detected course highlights measure 4 px. The scanner's gold detections on Explore are the board illustration, not extra course rings.

Apply Edit Spec §5's fixed 4 px at 720p. This rule predates v7's September 27 build, so the exception for videos built under earlier standards does not explain these widths. README's shipping bullet and Edit Spec §10 still contain stale “5 px” wording; §5 explicitly owns and supersedes that width rule. This review did not edit those documents.

### 3. Listening remains an open verification requirement

The prior build explicitly reported that nothing had been heard by ear. The retained concerns remain:

- 1:24–1:26: statement versus question cadence on “Your material.”
- About 1:31.23: the mid-sentence removal of “millions of,” joining “from” to “ideas.”
- Donor seams around 0:13–0:16, 0:56–1:00, 1:55–1:59, 2:35–2:43, 3:08, and 3:27.
- 3:42–end: close entry, both closing statements, and the final hold.

The existing contextual audition clips are in `../where-ai-works-best-v7-2026-09-27/audition/`. Fresh ASR confirms the intended words but cannot establish cadence, clicks, breath quality, or voice continuity. ASR punctuation also differs between runs; it does not establish whether the close is spoken as two statements.

### Previously accepted omission: the explicit transfer sentence

“It learned patterns it can apply to new problems” is still not spoken at 2:36–2:42. The September 26 plan explicitly disclosed that no roll supplied it, and the September 27 approved build retained that omission. This is an existing approved exception, not a newly discovered failure or authorization to reroll.

The broader relationship is conveyed by the examples-of-problem-solving training explanation, its immediate application to the student's task, and the later statement that all four strengths arise from training exposure. That makes the overall mechanism TAUGHT in compressed form. The exact transfer sentence remains MISSING as a sentence; do not claim the highlighted printed words supplied it. A future generation should speak it explicitly. The explicit “suggest what to try next” subclause is likewise compressed into breaking the task into steps and comparing approaches.

## Narration review

**LESSON:** where-ai-works-best  
**CANDIDATE:** current local course MP4 (3:52)  
**VERDICT:** provisional REPAIR recommendation for the required missing example; a formal audition-verified REPAIR/KEEP determination remains incomplete. Visual defects do not determine this narration recommendation.

Timestamps below follow the fresh small.en transcription of the encoded course file; speech boundaries are approximate.

| Teaching point, in lesson order | Assessment | Evidence |
|---|---|---|
| AI attempts many tasks; “can try” differs from “built for” | TAUGHT | 0:00–0:13: essay, schedule, code, image; explicit distinction |
| Course code A+, lesson drafts C− | RICH | 0:14–0:24: both grades and their different tasks |
| Missed intent, wrong order, weak flow | RICH | 0:25–0:30: all three faults spoken |
| Button/page testing differs from judging a good lesson | RICH | 0:31–0:41: concrete button and page tests versus ideas that make sense |
| Humans decided what worked and what to change | TAUGHT | 0:41–0:45: “rely on our own judgment” |
| Story takeaway and bridge to four strengths | TAUGHT | 0:46–0:56: exact takeaway, then four shapes of work |
| Reshape: name, learned forms, preserve meaning | RICH | 0:57–1:12: patterns, existing material, changed format, original meaning |
| Reshape: study guide, voice memo, plain instructions | TAUGHT | 1:12–1:24: three clear applications |
| Reshape: translate a message | MISSING | Never spoken; identified roll 1 donor above |
| Reshape takeaway | TAUGHT | 1:24–1:26: required words; cadence unverified |
| Explore: name, recombination, options, react and choose | RICH | 1:27–1:45: new options, variations, student chooses what to develop |
| Explore examples | TAUGHT | 1:45–1:54: essay, club, story, event ideas; “event ideas” broadens fundraiser harmlessly |
| Explore takeaway | TAUGHT | 1:55–1:58: both required clauses |
| Find: name, related concepts, question-matched details | TAUGHT | 2:00–2:09: substantial text, related concepts, query |
| Find: documents, summaries, requested specifics | TAUGHT | 2:10–2:16: summaries or requested data points |
| Find examples and takeaway | RICH | 2:16–2:32: textbook, scholarship, articles, handbook; exact takeaway |
| Problems: name and examples seen during training | TAUGHT | 2:32–2:42: required training sentence intact |
| Apply learned patterns to new problems | TAUGHT overall, compressed | 2:36–3:08 and 3:09–3:32 establish the relationship; explicit sentence absent as discussed above |
| Problems: goal, known facts, obstacle, steps, approaches | TAUGHT | 2:42–2:51: all inputs and the principal actions |
| Problems: four examples | RICH | 2:52–3:01: budgeted trip, code, colleges, experiment |
| Student makes final choice; Problems takeaway | TAUGHT | 3:02–3:07: “doesn't make the final choice,” then exact takeaway |
| Vast exposure, greater than a human lifetime | RICH | 3:09–3:26: causal bridge, lifetime comparison, six kinds of material |
| Familiarity with common formats; helps get started | TAUGHT | 3:23–3:31: common human formats and getting a task started |
| No guarantee of accuracy or fit; human judgment | RICH | 3:32–3:42: verbatim qualifier in the correct context, then judgment and accuracy |
| Both closing lines, no speech afterward | TAUGHT as words | 3:43–3:47; statement cadence still requires listening |

**Hard requirements:** the five board takeaways, verbatim many-examples sentence, accuracy/fit qualifier, and both closing lines are present as words. All four strength names appear. No invented training count remains in the transcript. The all-four-Reshape-examples instruction is MISSED. No title-card narration, pause/guess request, spoken URL, or interactive exercise narration appears.

**ERRORS:** no material factual contradiction found in the transcript. “AI fits this perfectly” and “exact data points” are stronger phrasing than the source, but the accuracy/fit qualifier is explicit later; these are not separate reroll grounds.

**SOURCE_QA:** no material contradiction found between the current page's instructional text and the upload Markdown. The interactive quiz is intentionally outside the video prompt's scope. The absent translation and transfer wording are not missing source-material problems.

**ADDITIONS:** “Because the system is ultimately predictive” is consistent with the course and connects the accuracy qualifier to human judgment. Retain it. Generalized event ideas and compressed lists of training material do not lose a separate essential concept.

## Production checks and retained scenes

- **Identity and decode:** fresh full sequential decode produced all 6,961 expected frames. The course file equals the reviewed v7 candidate and original build hash.
- **Current assets:** five teaching-board hashes match the protected build inputs; fresh feature matching identifies all six current JPGs, including the close. Full-size frame inspection confirms current text, complete boards, and readable full-view treatment.
- **Openings:** unmarked full view lasts 2.33 s (course story), 3.30 s (Reshape), 3.30 s (Explore), 4.00 s (Find), and 3.53 s (Problems). First-frame, pre-ring, and first-ring images are retained in this folder.
- **Board duration:** longest single-board appearance is 19.0 s. The longest continuous run across adjacent boards is **22.23 s**, 2:28.77–2:51.00 (Find takeaway into Problems). The earlier report's “longest continuous board run 19 s” conflated these measurements. Both satisfy §8b: no individual hold exceeds about 20 s and no adjacent-board run approaches 60 s. See `board-spans.txt` and `exact-board-runs.txt`.
- **Transition scan:** fresh automated `transition_guard.py` passes all 26 declared boundaries. Strips are retained in `transitions/`; every strip was not manually inspected in this review. This is not an audio-splice pass.
- **Close:** literal final frame inspected and matches the course close. Manifest specifies 48 frames held, 150-frame push to 1.2×, 79-frame settled hold; sampled frames show the expected progression. Continuous playback was not performed.
- **Notebook cleanup:** sampled retained scenes show drawings and diagrams with no visible engine corner mark or stock-photo intrusion. Historical build record reports 3,424 cloned frames, 63 inpainted frames, zero declined. This review does not claim every mark-cleaned frame was newly inspected.
- **Pauses:** prior record reports a 1.02 s gap before the close after adding 12 room-tone frames. It was not freshly measured or auditioned. No new pauses are recommended from transcript evidence.

Retain these supporting sequences, subject to the outstanding motion/listening review:

| Current output span | Scene and teaching purpose |
|---|---|
| 0:00–0:13.43 | Task map: demonstrates the breadth of things AI will attempt |
| 0:24.60–0:40.97 | Intent/order/flow, button tests, marked-up draft: illustrates the code-versus-lesson distinction |
| 0:49.23–0:56.33 | Code/structured-information graphic and four-strength map: bridges to the taxonomy |
| 1:11.87–1:23.87 | Notes/study guide, to-do list, instructions: tangible examples of reshaping |
| 1:44.93–1:54.87 | Essay/club/story/event option map: makes divergent options visible |
| 2:16.27–2:28.77 | Textbook, scholarship, articles, handbook: shows filtering for relevant information |
| 2:51.00–3:01.53 | Trip, code, college comparison, experiment: makes problem-solving examples concrete |
| 3:08.03–3:26.93 | Training inputs and recurring formats: explains the common reason for the four strengths |
| 3:26.93–3:42.80 | Draft quality and human judgment: distinguishes fluent output from trustworthy results |

These are independent supporting diagrams, not substituted course-board recreations. Their illustrative trip budget and experiment chart are not statistical claims; today's §8 does not require removing them merely for containing numbers. No custom photographic replacements are justified by this evaluation. The existing painted-out exposure banner need not be restored just because the newer rule allows useful illustrative numbers.

## Proposed edit plan (not built)

Scope: narrow repair of the missing example and oversized outlines, preserving the accepted teaching and supporting scenes elsewhere. Existing times below locate the current material; subsequent output times will shift if the donor examples beat is longer. Preserve approved framing and treatment unless the named repair requires a change.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| AI Helped Us Build This Course | Preserve A+ → C−; returning whole illustration → takeaway | Full board, stationary | 11.17 s, drawings, 8.27 s | Already readable and within hold limits |
| Reshape Your Material | Preserve WHY → WHAT; on donor return highlight the complete EXAMPLES section, then takeaway | Full board, stationary | Current 15.53 s; donor study-guide/to-do drawings; return for “translate a message, or rewrite technical instructions…” (~4.6 s), then takeaway | Restore complete spoken example set without a brief flashing cutaway; exact return and ring onset require donor audition |
| Explore Possibilities | Preserve WHY → WHAT → returning takeaway; render WHY at 4 px | Full board, stationary | 18.37 s; 9.93 s drawing break; 3.47 s takeaway | Correct width; retain options diagram |
| Find What Matters | Preserve WHY → WHAT → returning takeaway | Full board, stationary | 17.93 s; 12.50 s drawing break; 3.23 s takeaway | Already compliant in sampled visual checks |
| Work Through Problems | Preserve WHY → WHAT; drawing break; returning WHAT → takeaway; render teal outlines at 4 px | Full board, stationary | 19.0 s; 10.53 s drawing break; 6.50 s return | Correct three oversized runs; preserve approved compressed transfer explanation |
| AI does some things better than others. / “Can try” is not “built for.” | Unmarked standard close | 48-frame hold, 150-frame push, settled hold | Current 9.23 s | Preserve asset and motion; audition both statements |

**Narration proposal:** replace current examples beat at output 1:11.87–1:23.87 with roll 1's complete examples speech at approximately 1:15.68–1:28.36. Use silence-based endpoints established from the source audio, match levels, and audition the preceding “preserving your original meaning” and following “Your material. A more useful form.” together. Keep the study-guide/to-do drawings; return to the canonical EXAMPLES section for the translation/instructions sentence instead of inventing a new picture. This changes one beat and its necessary visual timing; it is not authorization to perform the edit.

**Selective pauses:** none proposed. Preserve natural gaps and the previously approved closing pause. Do not add silence for highlight changes.

**Highlight onset detail:** the previous build intentionally places several returning takeaway rings on the return frame, about 0.2–0.3 s ahead of the reported spoken onset. This is a documented deviation from §5's exact-onset wording. During any affected rebuild, an unmarked return until the target begins is the straightforward strict-spec treatment; do not flash the previous section's ring. Exact onset work needs audio inspection, not ASR timestamps alone.

## What was actually inspected

Read the complete current page lesson, Markdown, current prompt, full fresh timestamped transcript, and relevant prior plan/build records. Decoded the entire file; inspected 78 frames sampled every three seconds across its complete duration, full-size board/ring frames, opening/ring boundary frames, and the literal final frame. Ran fresh board matching, ring measurements, and automated transition checks. Read the existing donor transcript and verified all three donor hashes still match their build inputs.

**Nothing was heard by ear, and the movie was not watched in real-time motion.** The sampled sequences support visual/content findings, but do not certify animation timing, every transient label, every splice, or cadence. No audio-capable listening/video-analysis tool was exposed in this session. The required end-to-end audiovisual review and donor-join audition remain incomplete. Accordingly this is an evidence-backed repair recommendation with explicit verification limits, not an unconditional KEEP or shipping approval.
