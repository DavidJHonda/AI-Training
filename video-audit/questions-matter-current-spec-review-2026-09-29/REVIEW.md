# Questions Matter — live video against current specs

Reviewed 2026-09-29. Evaluation only; no video, lesson, or production setting changed.

**Recommendation: keep the narration and make a targeted visual repair to the opening.** The clearest current-spec issue is the first board's uninterrupted 32.8-second appearance. There is also a short establishment of the value board that can be improved by bringing it in during its spoken introduction. The later thick rings are a legacy treatment expressly grandfathered by Edit Spec §5; they are not, by themselves, a reason to rebuild this shipped video.

**Review limit:** this is a complete transcript review, sampled visual inspection across the whole file, and encoded-file measurement. I did not hear the audio or watch real-time audiovisual playback. The narration content supports KEEP; a final whole-file KEEP/ship certification remains conditional on listening and playback. In particular, animation effectiveness and audio seams have not been certified.

## Exact live file and authority

- Public page checked: https://besmarterthanthetool.com/
- Its `LESSON_VIDEOS.questionsvaluable` serves [questions-matter.mp4?v=20260926ship8](https://besmarterthanthetool.com/course-assets/questions-matter/questions-matter.mp4?v=20260926ship8), displayed as 4 min.
- Public file and local `course-assets/questions-matter/questions-matter.mp4` have the same SHA-256: `2c4fe76bbeb84aee589be758a27d29309945e44605df694d91de61c8d62dc039`.
- 23,698,941 bytes; 1280×720; 30 fps; 6,674 decoded frames; 222.467 seconds (3:42.47).
- Standards: current `scripts/video/README.md`, `EDIT-SPEC.md`, and `NARRATION-REVIEW.md`, including the September 29 instruction to preserve effective Notebook visuals.
- Teaching authority: `QuestionsValuableSection` in current `index.html`, its canonical boards and closing copy; checked against `lessons/questions-matter.md` and the public lesson source. The LAB remains an activity, not an omitted narration requirement.
- Sources and previous edits were traced through the September 16 v5 and September 26 v8 manifests. Prior reviews were background only; the measurements and transcripts below were generated from the current file.

## Findings

| Priority | Time | Finding and recommended action |
|---|---|---|
| Main visual repair | **0:12.40–0:45.20** | **32.8 seconds continuously on “How Answers Got Easier and Faster.”** Edit Spec §8b calls for a supporting scene when one board exceeds about 20 seconds. Narration is usefully walking Library → Search → AI, so this is a visual-variety issue, not dead narration. Add relevant library and search inserts while preserving all spoken teaching. |
| Small timing repair | **1:00.28–1:03.43** | “It just changes where our value lives” is spoken at 1:00.28–1:02.28, while the previous board remains. The value board arrives at 1:03.07 and its first ring appears 11 frames later, at 1:03.43. Bring the unmarked value board in around 1:00.27, giving about 3.17 seconds before the existing Pre-AI ring. This follows §3's introduction-first treatment without adding silence. The rule does allow early rings when a board lacks an introduction; this video has a usable introduction. |
| Grandfathered difference | **2:04–3:23, board appearances only** | Later card rings measure roughly **6–7 px**, versus today's fixed **4 px at 720p**. §5 explicitly says videos shipped under earlier stroke rules are not rebuilt solely for that change. Preserve these in an opening-only repair; normalize if those boards are rebuilt for another reason. |
| Optional framing polish | **Examples at 2:28 and 2:58** | Dense-board dives clip the top of the overall board heading. The complete active card, illustration, card title, weak question, and better question remain visible. This does not violate the complete-card requirement; a slightly smaller crop could preserve the heading if these spans are revisited. |

The adjacent Answers → Value run at **0:49.93–1:13.27 is 23.33 seconds**, but consists of separate 13.13- and 10.20-second board appearances. It does **not** exceed §8b's approximately 60-second rule for a run of multiple boards. The old review's treatment of this as another >20-second problem was too broad. No additional cutaway is required there.

The first two boards measure predominantly 4 px with the current detector; teal reads 5 px. The earlier build record also documents OpenCV rasterization/threshold differences. Do not interpret those readings as proof of a perfectly literal four-pixel stroke. The detector's 9–10 px gold detections in the later board are illustrated artwork, not an extra highlight ring.

## Narration review

**Content verdict: KEEP, provisional on listening. No identified essential omission, factual contradiction, or necessary narration edit. No reroll indicated.** Timestamps below use the fresh VAD-enabled transcript. They are speech estimates, not frame-accurate edit boundaries.

| Essential teaching point | Assessment | Current-file evidence |
|---|---|---|
| Useful AI help starts with knowing what to ask | TAUGHT | 0:00–0:07, “to actually get useful help … you have to know what to ask.” |
| Easier answers free time for better questions | TAUGHT | 0:08–0:18, less time chasing facts, more time framing the question. |
| Library: travel, catalog, books, handwritten notes; half a Saturday | RICH | 0:19–0:31, all steps and time comparison spoken. |
| Search: queries, tabs, source judgment, copying; an hour or two | RICH | 0:32–0:43, all steps and time comparison spoken. |
| AI: open app, ask, receive answer in seconds | RICH | 0:44–0:50. |
| Half a day → hour → seconds; cheap answers do not reduce human value | RICH | 0:51–1:02; explicitly explains that value shifts. |
| Pre-AI: locating a good answer required knowing where to look and what to trust | TAUGHT | 1:03–1:10; harmless compression of “what mattered.” |
| With AI: deciding which questions to ask and whether output solves the problem | RICH | 1:11–1:19; both human judgments retained. |
| Mid-lesson takeaway | TAUGHT | 1:22–1:25, “Answers got cheap. Questions didn't.” |
| Questioning is an old human skill; Socrates tests assumptions | RICH | 1:25–1:38. |
| Scientific method starts with a testable question | TAUGHT | 1:39–1:44. |
| Hour-to-save-world / 55 minutes finding the question | TAUGHT | 1:44–1:51, no unsupported named attribution added. |
| Four qualities are useful independently of AI | TAUGHT | 1:51–1:58. |
| Open-Minded: no predetermined answer; leading questions seek backup | RICH | 2:05–2:12. |
| Homework weak/better question pair | RICH | 2:14–2:22, both questions spoken. |
| Specific: enough detail for an answer that fits | TAUGHT | 2:23–2:28. |
| Sports → basketball point guard, losing ball against pressure, useful drills | RICH | 2:29–2:40, both questions and all constraints spoken. |
| On Target: solve the actual problem; first question may miss it | RICH | 2:55–3:01. |
| Energy drink → first-period tiredness, causes and changes | RICH | 3:02–3:15, full comparison spoken. |
| Open-Ended: invite explanation, beyond yes/no, room for surprise | RICH | 3:16–3:22. |
| Debate team → benefits and what joining displaces | RICH | 3:23–3:32, both questions spoken. |
| Both closing lines, in order | TAUGHT / MET | 3:33–3:38, “Answers got cheap. Questions didn't.” and “Frame the problem. Ask the next better question.” |

The grandparents/parents/you research-assignment framing is omitted, but the actual three-era comparison is fully taught. That omission does not lose essential understanding. The additions about examining assumptions and avoiding generic advice/confirmation improve the explanation. “The modern reality is actually quite simple” at 1:18.90–1:21.88 is optional filler, not a required cut.

Source QA: no material issue identified. The Markdown contains the essential teaching shown on the page. No narration of board numbers, source-file instructions, or the LAB appeared in the transcript.

ASR caution: the initial non-VAD transcript omitted the mid-video “Answers got cheap” and rendered “Invite an explanation” as “Write an explanation.” The second, VAD-enabled pass recovered both, agreeing with the older transcript. Those discrepancies are not evidence of a spoken defect. The full 617-word VAD transcript was read. Audio itself was not heard.

## Board and camera plan for a possible repair

Proposed scope: **narrow visual repair to the first two boards, preserving narration, duration, existing pauses, and the second half.** No build performed. Proposed insert endpoints should be checked against the chosen visual and exact encoded frames before assembly.

| Board (exact title) | Highlight sequence | Camera | On screen / supporting breaks | Reason |
|---|---|---|---|---|
| How Answers Got Easier and Faster | Whole Library → Search → AI cards; then Half a Saturday → An hour or two → Seconds panels; full takeaway banner | Keep compact full view | Current 0:12.40–0:45.20 and 0:49.93–1:03.07. Propose library insert 0:24.60–0:30.60 and search insert 0:36.50–0:42.67. Preserve existing brain/robot insert 0:45.20–0:49.93. End second board appearance around 1:00.27 for the value introduction. | With these inserts, longest first-board appearance becomes about 12.2 seconds. Return roughly one second before Search and AI item onsets. |
| It Changes Where Value Lives | Whole Pre-AI → With AI cards; takeaway banner | Keep compact full view | Propose first arrival 1:00.27 instead of 1:03.07; keep break at 1:13.27–1:17.10 and final appearance to 1:25.63. First appearance becomes about 13 seconds; last remains 8.53 seconds. | Establish during “changes where our value lives.” Preserve the brain/question drawing. |
| Four Qualities of a Good Question | Open-Minded whole card; Specific whole card | Preserve full opening and complete-card dives | 1:58.93–2:12.73 (13.8 s), 2:21.97–2:28.77 (6.8 s); examples continue in supporting diagrams | Brief explanations support whole-card outlines; no need to add section rings or replace useful example scenes. |
| Four Qualities of a Good Question, Continued | On Target whole card; Open-Ended whole card | Preserve full opening and complete-card dives | 2:49.10–3:02.00 (12.9 s), 3:14.70–3:23.23 (8.53 s); diagrams between/after | Same treatment; no >20-second single-board hold. |
| Answers got cheap. Questions didn’t. | Unmarked close | Preserve 48-frame hold, 150-frame push to 1.2×, settled hold | 3:33.13–3:42.47; literal final frame | Already matches prescribed close motion and copy. |

There is no verified surviving library/search donor scene. The earlier repair record identifies only an older roll, and its available useful scenes are already used. Under current §8d, propose purpose-generated photographic-looking high-school students: (1) locating books and taking handwritten research notes in a library; (2) evaluating search results across browser tabs and collecting useful material. These should demonstrate the narrated work, with minimal text. No reroll is needed merely to obtain these images. No new images were generated for this evaluation.

No narration changes or new pauses proposed. Preserve the existing 0:08 breath repair and the closing gap. Subjective pacing needs listening; no automatic silence minimum applies.

## Supporting scenes to preserve

These placements are identified from the current encoded cuts and build provenance; recommendation is based on visual samples plus transcript, not a real-time motion review.

| Current time | Scene and teaching purpose |
|---|---|
| 0:00–0:07.83 | Inquiry → AI engine → output; frames the role of the question. |
| 0:07.83–0:12.40 | Abacus → book → computer, question marks; changing answer-finding tools. |
| 0:45.20–0:49.93 | Brain and robot; human prompt / machine response. |
| 1:13.27–1:17.10 | Brain → question mark; choosing the question. |
| 1:25.63–1:39.33 | Drawn Socratic discussion; questions test assumptions. |
| 1:39.33–1:50.80 | Scientific-method sequence; questioning precedes testing/conclusions. |
| 1:50.80–1:58.93 | Criteria title; transition to the four qualities. |
| 2:12.73–2:21.97 | Leading question versus evidence-seeking inquiry. |
| 2:28.77–2:40.30 | Basketball role, situation, objective; makes specificity concrete. The athlete is visibly drawn, not a stock photograph. |
| 2:40.30–2:49.10 | Human filter / AI system; connects specificity and open-mindedness. |
| 3:02.00–3:14.70 | Symptom versus root-cause target; explains on-target questioning. |
| 3:23.23–3:33.13 | Yes/no dead end versus branching debate considerations; explains open-ended questions. |

No sampled supporting scene warrants replacement merely for its drawn style. No Notebook corner mark, unknown-source photograph, or obvious nonsensical text was found in the inspected samples. That is not an every-frame certification.

## Checks and remaining limits

- Public/local byte identity verified (`live-verification.json`).
- Full sequential decode: 6,674 frames; dimensions, duration, and frame rate match the v8 record.
- Fresh board matching every 0.5 seconds confirms all four teaching assets and current close. Exact span endpoints above are supported by scene cuts/manifests; the sampler can round outward by 0.5 seconds.
- Ring stroke measured every 0.5 seconds; results in `ring-stroke.txt`. Full-size frame samples confirm complete active cards and the visible title crop described above.
- Contact sheets across the entire runtime and selected full-size frames inspected.
- Fresh transition guard: **21/21 declared splice boundaries passed**. Manually inspected full strips at 0:07.83, 1:03.07, and 3:33.13; remaining 18 strips were not manually inspected. Automated results alone do not certify all transitions.
- Close measured directly from the encoded frames: dark pill width holds at 720 px, grows to 864 px (1.2×), and remains 864 px through final frame 6673. Timing agrees with the prescribed 48/150/settled sequence (`close-measurement.json`).
- Direct audio listening and whole-file real-time viewing not performed. In particular, listen through the 0:07.83 breath edit, inherited graft joins around 0:19 and 1:03–1:26, and the close transition. No new audio defect is asserted from ASR alone.
- Video Tracker was not accessed or changed; no workflow status is inferred from it.

The review recommends repair; it does not authorize or perform a build, local shipping, or deployment.
