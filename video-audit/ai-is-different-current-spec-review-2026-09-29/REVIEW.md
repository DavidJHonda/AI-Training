# AI Is Different — live video against September 29 specifications

Reviewed September 29, 2026. Evaluation only; no lesson, asset, video, or deployment changed.

## Recommendation

Keep the existing production as the base. The strongest repair is the under-explained **Deepfakes** beat at **3:54.42–3:56.00**. A complete explanation survives in the previous shipped version. Board highlighting can also be brought closer to the current whole-card-then-section guidance. Preserve the useful Notebook scenes, the approved narration cuts, and the approved long Rules vs. Patterns run.

**Narration disposition: provisional REPAIR recommendation, not a certified REPAIR verdict.** The current explanation is THIN; donor wording is verified by fresh transcription, but the proposed joins have not been auditioned. The spec requires that listening before a repair source is verified. There is no basis for ordering a full reroll while this existing donor remains available.

**Review limit:** full applicable transcript and current lesson read; entire video decoded and inspected in two-second visual samples, with selected 720p frames and boundary summaries examined. No real-time end-to-end audiovisual playback or listening occurred. This is a substantive content/visual audit, not whole-file shipping certification. Animation judgments below are provisional because sampled sequences do not substitute for watching motion with narration.

## Verified live identity

- Public lesson: https://besmarterthanthetool.com
- Public `LESSON_VIDEOS.aivscode`: `course-assets/ai-is-different/ai-is-different.mp4?v=20260927ship1`, displayed as 5 min.
- Public stream, local canonical MP4, and v11 manifest match SHA-256 **75684df8c2e06aefe873c59ef8fbfed93d342c389edfc271b9876662f9cc305e**.
- Fresh sequential decode: **8,328 frames, 30 fps, 1280×720, 4:37.600**.
- Git commit `5b0b7b35` explicitly records shipping v11 with owner approval. The September 27 v11 REVIEW still says “not shipped”; it is stale, not evidence of the current release state.
- Standards: current `scripts/video/EDIT-SPEC.md`, `NARRATION-REVIEW.md`, and `README.md`. Section 5's explicit fixed **4 px at 720p** rule takes precedence over residual “5 px” wording in the general checklists.

## Narration against the current lesson

| Essential teaching | Assessment | Output evidence |
|---|---|---|
| Superpowers arise from a different foundation | TAUGHT | 0:00–0:10.80. Adds “completely”; previously considered for removal and deliberately retained because the isolated splice was unsuitable. |
| Programmers write rules; IF-THEN-ELSE; both password outcomes | RICH | 0:15.70–0:40.16. Both branches and repeatable result explained. |
| Training learns numerical patterns before use | RICH | 0:41.54–1:02.76. Training and patterns remain one learning process. |
| Probability scores next words; selection and repetition build an answer | RICH | 1:03.48–1:19.28. “Prediction” is not named, but its complete operation is explained. The arrow from learning to answering is carried in speech. |
| Cookbook robot versus experienced chef; new situations | RICH | 1:19.82–1:41.92. Fixed recipe contrasted with learning patterns of flavor and heat to make a novel dish. |
| PS5 question, preset-list rule, repeated Spider-Man 2, variable AI recommendations | RICH | 1:45.88–2:13.62. Names Spider-Man 2, NHL 26, and God of War Ragnarök. AI-side first Spider-Man answer is not separately repeated; the approved plan expressly retained this compression. |
| Structured GPA rows/columns versus receipt/text-message data | RICH | 2:14.80–2:34.14. Both categories and concrete examples explained. |
| Actual lesson developed from crossed-out legal-pad notes to a first draft | RICH | 2:34.90–2:47.52. Correctly says “This lesson started,” not a hypothetical lesson plan. |
| Expected fields/file types/commands versus organizing and transforming messy information | RICH | 2:48.16–3:08.86. Notes, PDFs, audio, summaries, and drafts spoken. |
| App-dependent inputs/outputs | TAUGHT | 3:09.76–3:13.76. Pictures/table/image list is not spoken; owner removed that repeated graft in v11. Do not restore it automatically. |
| Choose ordinary software for exact consistent jobs and AI for messy open-ended jobs | RICH | 3:14.56–3:27.42. GPA example and contrast both spoken. |
| Superman/Kryptonite analogy before the risks | TAUGHT | 3:28.66–3:37.22. |
| Learned behavior is harder to predict, inspect, and lock down | TAUGHT | 3:38.04–3:43.74. The longer page sentence about even builders being unable to fully predict behavior is compressed into this central limitation. |
| Scams that scale | RICH | 3:47.78–3:54.06. Fake identities and convincing messages generated in seconds. Code is omitted, but mechanism and harm remain. |
| Deepfakes: convincing fake media can target and humiliate people | **THIN** | **3:54.42–3:56.00: “or deepfakes that target victims.”** It names the threat without explaining what is faked or the humiliating harm. The board supplies that missing meaning, which the narration spec explicitly says is insufficient. The earlier reroll review rated this too generously. |
| Confident but wrong, including medical/safety consequences | RICH | 3:56.84–4:04.22. Explains hallucination and confident false answers. |
| Safety training plus app guardrails; both kinds of failure | RICH | 4:05.00–4:24.72. Both layers, missed danger, and blocked harmless requests. |
| Both closing lines | MET | 4:28.26–4:33.20, verbatim and in order, no sign-off afterward. |

The lesson arc is intact: foundation → mechanisms → familiar comparison → messy data → tool choice → risk → safeguards → trade-off. No material factual contradiction was identified in the reviewed narration. “Hallucinate” is a useful addition and is immediately explained. Source QA: no material contradiction identified within the lesson; this was not an external factual research exercise.

Other required lines: “Written rules…,” “Learn patterns first…,” “Rules repeat… / Patterns build…,” “Trained behavior…,” training safety, and app safety layer are present. The app qualifier is a clause with “While”; the mess takeaway adds “and.” These preserve meaning. The retained “completely” and previously approved omissions are documented release decisions, not fresh reasons to reroll.

## Existing donor and proposed repair

Recovered read-only from Git: `d88a1399:course-assets/ai-is-different/ai-is-different.mp4` (previous shipped v9), SHA-256 **c7a9dbb804a30673aca2df73c4cd6b1f36256518ef68b624f08c880c9657ce66**. This matches the September 21 illustration-sync record. Temporary recovery: `/private/tmp/ai-is-different-v9-donor-20260929.mp4`. No old working file was overwritten.

Fresh word-timestamp transcription confirms **4:24.76–4:33.74**:

> There is also the issue of deepfakes. The system can use its patterns to create convincing fake media that can be used to target or humiliate individuals.

Proposed replacement: current **3:54.42–3:56.00**, “or deepfakes that target victims,” with that complete donor beat, under the current canonical Deepfakes card. Keep the preceding scams sentence through “in seconds,” then the donor sentences, then “Even without malicious intent, AI can hallucinate.” This carries the missing explanation without restoring unrelated old narration.

Approximate boundaries to audition: current 3:54.2–3:56.4; donor 4:24.3–4:34.2. These are search windows, not approved frame-exact cuts. Fresh ASR finds the previous donor sentence ending 4:23.86 and the next beginning 4:34.66, leaving usable gaps around the target. The proposed replacement adds roughly 7–8 seconds. Voice, cadence, level matching, breaths, and contextual joins remain unverified. `deepfake-donor-context.wav` and `deepfake-donor-transcript.json` preserve the evidence.

## Visual findings under the new rules

**Current assets:** all five teaching-board hashes match the v11 manifest and current canonical JPGs. The close visually matches the canonical white closing image. Boards open complete and unmarked: approximately 4.37 s for Rules, 4.00 s for Two Ideas, 2.13 s for Rules vs. Patterns, 3.43 s for Structured, and 3.43 s for Kryptonite before their first rings.

**Highlighting:** Two Ideas goes straight into Training and Patterns subsection rings without first introducing the complete Learn First card; its answering side does the same. Structured keeps whole-card rings while the narration separately teaches “The idea” and “Input & Output.” Those are the clearest opportunities to conform to current section 1b. Preserve the compact camera for Two Ideas. Keep whole-card rings on the brief Kryptonite examples rather than inventing sentence-level rings.

**Camera:** the tall comparison and Structured cards remain complete in their settled active-card views. At about 1:48–1:50 the question-focused camera crops the lower portions of both comparison cards. The active question box itself remains whole, and the manifest uses a uniform dive width; therefore this is optional camera polish, not a demonstrated violation of the complete-active-card rule. Prefer the full board through the question, then dive to the complete Normal Software card. This refines the preliminary observation made during review.

**Ring width:** 194 detected samples: 152 round to 4 px, 42 to 5 px. Several green/amber/teal spans read 5 px. Color thresholds, artwork edges, and antialiasing affect this measurement; it does not establish a zoom-scaled-stroke defect. Do not rebuild the entire video solely on these readings. Use the current fixed-width renderer on any rebuilt boards and inspect those output rings. No rings visibly clip the active card in inspected settled states.

**Board duration:** longest unbroken teaching board is **Rules vs. Patterns, 1:45.533–2:14.800 = 29.267 s**. This exceeds the approximate 20-second guideline but is an explicit owner decision in v11 after removal of a faulty cutaway. Preserve that exception. Kryptonite is **20.667 s**, a previously accepted continuous three-risk explanation. Two Ideas is split into 12.833 and 14.167 s runs; Structured into 14.633, 5.667, and 4.200 s. No minute-long chain of teaching boards remains. Automated ORB matching falsely labels two Notebook spans as the close; use the visually verified timeline, not those false positives.

**Close:** starts 4:25.300; literal final frame is the canonical close. The hash-matched manifest specifies the required 48-frame hold, 150-frame push to 1.2×, and settled hold. Sampled frames show that progression. No new close design is needed.

**Transitions:** fresh transition guard passes all **33 declared boundaries**, decoding all 8,328 frames. Boundary summaries inspected; no stale visual island identified there. This does not certify audio or every-frame graphic correctness.

**Notebook treatment:** retain the existing drawings and illustrative numbers. No sampled evidence justifies replacing them with new photographic stills. The new photographic preference governs new custom imagery, not removal of useful existing drawings. Canonical board photography is permitted. No unknown-source stock photograph or engine corner mark was found in the inspected samples; the hash-matched build records zero declined mark-cleanup frames. This is not an every-frame mark certificate.

## Proposed board plan — no build performed

Times are current output positions; downstream timing must be remapped if the donor is accepted.

| Board | Highlight sequence | Camera | Exposure / breaks | Treatment |
|---|---|---|---|---|
| Rules Look Like This | Password → IF → THEN → ELSE → takeaway | Compact, full board | 0:23.100–0:41.367; 18.267 s | Preserve. |
| Two Ideas Behind Every Answer | Introduce whole Learn First card, then Training/Patterns as explained; whole Answer One Word at a Time card at its spoken introduction, then Probability/Prediction; takeaway | Compact, full board | 0:50.167–1:03.000 and 1:05.567–1:19.733; retain 1:03.000–1:05.567 response-building drawing | Whole-card introductions would be brief; preview without adding pauses. |
| Rules vs. Patterns | Question → Normal Software whole card → repeated-answer section → AI Software whole card → named answer rows → takeaway | Full view through question; uniform complete-card dives thereafter | 1:45.533–2:14.800; 29.267 s, owner-approved exception | Question camera change optional; keep approved uninterrupted run. |
| Structured vs. Unstructured Data | Whole Normal Software card → Input & Output when explained; whole AI Software card → Input & Output when explained; app qualifier → takeaway | Preserve dense complete-card views and full-view opening | 2:47.933–3:02.567, 3:08.967–3:14.633, 3:24.367–3:28.567; retain both data drawings and tool-choice drawing | Add section emphasis for distinct narrated parts, not each sentence. Some AI input/output narration is already under drawings; do not remove those drawings to show a ring. |
| AI’s Kryptonite | Whole Scams card → whole Deepfakes card → whole Confident but Wrong card | Compact, full board | Currently 3:44.500–4:05.167; donor adds ~7–8 s | If grafting, propose a ~4 s supporting insert within the longer Deepfakes explanation, returning ~1 s before Confident but Wrong. New asset proposal: realistic student discovering a convincingly fabricated image of them, showing the distinction between real student and fabricated media without explicit or humiliating content. This is an unbuilt proposal requiring final timing and preview; retain other useful animations. |
| AI’s foundation gives it new superpowers. | Unmarked | Canonical white close; 48-frame hold, 150-frame 1.2× push, settle | Current 4:25.300–4:37.600; shift intact if audio length changes | Preserve. |

Supporting visuals to retain (output times):

- 0:00–0:11.567: output/foundation diagrams introduce rules versus learned patterns.
- 0:11.567–0:23.100: calculator and code monitor make ordinary software concrete.
- 0:41.367–0:50.167: rule-code contrast and next-word sequence bridge to learning/answering.
- 1:03.000–1:05.567: learned-patterns/response diagram connects the two phases.
- 1:19.733–1:43.233: cookbook robot, chef, and pattern-to-novel-dish sequence teach the analogy. “10,000+ dishes” is illustrative within that analogy, not grounds for automatic deletion.
- 1:43.233–1:45.533: controller/phone introduces the PS5 comparison.
- 2:14.800–2:34.500: GPA table, receipt, and copied text illustrate data organization. Supporting-scene emphasis is allowed.
- 2:34.500–2:47.933: marked-up notes and organizing-to-draft sequence support the legal-pad story. The project-proposal example is an added illustration, not a canonical-board recreation.
- 3:02.567–3:08.967: varied input forms and input→AI→outputs diagrams show transformation.
- 3:14.633–3:24.367: calculator/notes tool-choice drawing, including existing room tone.
- 3:28.567–3:44.500: backpack/Kryptonite and behavior diagrams connect capability to control difficulty.
- 4:05.167–4:25.300: safety-training and runtime-guardrail sequences illustrate both safety approaches and failures.

**Selective pauses:** no new pauses proposed without listening. Preserve the existing additions after “Patterns build a fresh one” and before Kryptonite; transcript gaps are about 1.18 and 1.24 s. Those are ASR gaps, not fresh acoustic silence measurements. Do not add silence to accommodate ring or camera changes.

## Remaining verification

Before a future build/ship decision: audition the donor and contextual joins; approve the final combined narration/board plan; inspect retained animations in real-time motion with narration; verify all changed rings/onsets and final close motion; measure any altered gaps acoustically; listen end to end. Existing graft joins at about 1:20, 1:54, 2:35, the 3:09 cut, and the 3:24 cut deserve listening. No such listening is claimed here. Tracker not accessed or changed.

Evidence is beside this report: `verification.json`, `contact-0.jpg` through `contact-5.jpg`, selected full-size `frames/`, `current-assets.jpg`, `board-spans.txt/json`, `ring-stroke.txt/json`, `guard/`, and donor transcript/audio. Applicable full transcript: `../ai-is-different-v11-2026-09-27/transcript/ai-is-different-v11.txt`.
