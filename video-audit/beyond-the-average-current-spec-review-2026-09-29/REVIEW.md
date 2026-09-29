# Beyond the Average — current-spec evaluation, 2026-09-29

> **Notebook-graphics recommendations superseded later on September 29:** See [reassessment against the revised section 8](NOTEBOOK-GRAPHICS-REASSESSMENT.md). The blanket recommendations to replace the percentage animation, alternate skill diagrams, and changing tool labels are withdrawn. Earlier measurements and source identity remain applicable; use the reassessment's narrower visual plan.

**Recommendation: retain the approved narration and refresh selected visuals. The live video does not fully match today's production treatment. No reroll is recommended on the evidence reviewed.**

This is an evaluation, not a build or publication. No course content, video, asset, or tracker row was changed. Narration KEEP is conditional on the two documented owner exceptions below and on the limits of transcript-based review; this is not an end-to-end listening or shipping certification.

## Exact live identity and authority

- Public page read today: https://besmarterthanthetool.com. Its `LESSON_VIDEOS.whybother` points to `course-assets/beyond-the-average/beyond-the-average.mp4?v=20260921ship12`, matching the local page.
- Public MP4 streamed through SHA-256, without retaining another video copy. Remote and local SHA-256 both: `b50c3baa71e04088adb40898b73758acab11f3f2f0a34645c767ac82416c453a`.
- This also matches the shipped illustration-sync manifest of 2026-09-21. The complete 2026-09-25 transcript therefore remains applicable to the exact reviewed file, not merely a similarly named candidate.
- Fresh sequential decode: **4,984 frames, 30 fps, 1280×720, 2:46.133**. The website's rounded “3 min” label is appropriate.
- Current standards: `scripts/video/EDIT-SPEC.md` as read on 2026-09-29, `NARRATION-REVIEW.md`, and the shared README. Section 5's explicit current 4 px at 720p rule takes precedence over residual 5 px wording in the checklists.
- Current teaching authority: `index.html`, WhyBother lesson, and its canonical Same Tool, Future, and Close assets. Upload Markdown and video prompt were also read.

## Findings, in priority order

| Finding | Live evidence | Assessment / recommended treatment |
|---|---|---|
| Unsupported numerical claims in the opening diagram | At **0:38**, “~99% Identical”; at **0:42**, “Performance Floor (0% Differentiation).” See `frames/01140.jpg` and `frames/01260.jpg`. | These figures are absent from the lesson and unsupported. They give invented precision to the shared-starting-point example. Replace the affected drawing states with a simple drawn same-tool/shared-starting-point illustration, without percentages. Preserve narration and duration. Exact first/last affected frames must be measured before a build; these timestamps are confirmed examples, not claimed edit boundaries. |
| Long uninterrupted board sequence | **1:40.433–2:34.133: 53.700 seconds** on What to Start Building Today. The close immediately follows, making **65.700 seconds** of continuous course boards to the end. Fresh half-second ORB sampling reports approximately 54 seconds for the main board. | Section 8b calls for supporting drawings when a single board exceeds about 20 seconds. This board is actively taught, so the issue is visual variety, not dead time or excess narration. Break it with relevant illustrations while keeping each item and its instruction visible long enough to read. Today's section 8d supplies a custom-illustration option; lack of a surviving donor roll no longer prevents a proposal. |
| Competing skill taxonomies and invented product labels | Around **1:12–1:17**, “Where Real Value Is Built” substitutes Critical Problem Solving / AI Fluency & Inquiry / Human Collaboration. At **1:31–1:40**, “Internalized Knowledge & Practiced Skills” substitutes Problem Solving / Critical Analysis / Human & AI Fluency, with invented changing product names underneath. See `frames/02220.jpg` and `frames/02820.jpg`. | These Notebook diagrams visually restate the lesson with different category names just before the canonical four-card board. They add unnecessary competing lists. Replace them with drawn scenes supporting school practice and enduring knowledge, with little or no text. They are not exact copies of a course board, but are weak supporting visuals under sections 8/8d. |
| Close uses the old visual treatment | **2:34.133–2:46.133**. Correct wording and final-frame placement, but the encoded background is approximately RGB **245,244,249**, whereas the current canonical JPG background is **255,255,255**. | Current section 7 requires the canonical white JPG. On a visual refresh, use `make_close_board.py --lesson whybother`; preserve its copy and proportions. The legacy helper explicitly says existing finished videos are not rebuilt solely for this migration, so this is an update to include in a broader refresh, not grounds for an emergency republish. |
| Legacy thick rings | Main-board samples measure approximately **6–7 solid pixels**, generally 6.5 px on settled cards; takeaway ring about 6 px. | Today's target is fixed **4 px at 720p**, drawn after the crop. Section 5 explicitly grandfathers older shipped videos: **do not rebuild for this alone**. Apply 4 px when rebuilding this board for the cutaways. The detected 2 px gold box at 0:42 is Notebook artwork, not a course highlight. |

The “Differentiation Gap” at **1:00.6–about 1:09** is a secondary editorial concern: Student A/B labels and “superior solution” make it feel like a student-ranking graphic. It was explicitly retained in the approved September edit, so do not label it a newly discovered unauthorized change. A future visual pass could replace it with an illustration of a person improving a shared draft; this is optional unless included in the agreed scope.

## What holds up

- **Same Tool. Different Advantage.** is the current September 21 page asset, full, still, and unmarked for **0:50.700–1:00.600 (9.900 s)**. It supports one whole-board idea. No ring or camera walk is needed.
- **What to Start Building Today** uses the current page asset. It opens complete and unmarked at frame 3013, then stays full view for roughly **7.6 seconds** before the first item. At 720p its body text benefits from dense treatment. The settled views preserve each complete active card, including illustration, heading, and bottom text. Cropping inactive neighbors during a dense dive is not a defect.
- Highlight order and accent colors agree with the teaching: Deep Subject Knowledge (purple), Strong Skills (blue), AI Fluency (teal), People Skills (amber), then the violet takeaway. Existing recorded item onsets are approximately 1:48.0, 1:57.1, 2:07.7, 2:17.5; current half-second ring sampling is consistent with them. This review does not claim a fresh word-level audio alignment audit.
- Closing copy matches both required lines, and the close is the literal final frame. Fresh measurements show the pill grows **725 → 869 pixels (1.199×)**, consistent with the prescribed 48-frame opening hold, 150-frame push to 1.2×, and settled hold. The visual asset/background, not the motion, needs updating.
- Drawn people are allowed under the current spec. The Same Tool course image is a canonical page asset and is covered by the course-board exemption to the Notebook photo ban. No additional stock photograph or visible engine corner mark was found in the sampled frames. This is a sampled observation, not an every-frame certificate.
- Fresh transition guard passed all **eight** declared legacy boundaries: 1505, 1521, 1530, 1818, 2322, 2734, 3013, 4624. Four major board/edited-pause strips were inspected at larger size; all eight were inspected in the overview. No brief stale visual was identified in those checks.

## Narration review

**VERDICT: KEEP, preserving the documented owner exceptions.** This is a content judgment from the full applicable transcript and current lesson, not a claim that I auditioned the video. The September 14 review records acceptance of the unspoken Same Tool banner and the removal of the “Learn how things work” passage; later shipped revisions preserve those decisions.

| Essential teaching, in lesson order | Assessment | Transcript evidence |
|---|---|---|
| Why attend school if AI can answer and produce work? | RICH | 0:00–0:13: drafts, code, complex questions, years of classes. |
| Dream job, coworker, same job and same AI | RICH | 0:15–0:30: concrete adjacent-desk scenario. |
| Similar prompts produce a shared starting point: the new average | TAUGHT | 0:32–0:43: similar questions/answers and baseline output. “Identical” is stronger than the page's qualified “often … similar”; within the explicit same-tool scenario it carries the intended idea, but use the page's more careful wording in any future reroll. |
| What you contribute takes the work further | RICH | 0:50–1:00: “AI provides raw material,” subject knowledge and practiced problem solving. |
| Same Tool banner's underlying meaning | TAUGHT, verbatim exception | The prior sentence teaches it. “The tool may be the same. What you bring to it is yours.” is not spoken verbatim; accepted September 14. |
| What sets you apart, and school as a place to build it | TAUGHT | 1:00–1:17: question followed by internal knowledge, practiced skills, and structured school time. “More valuable than the tool” is a wording drift from the page's “What makes you more valuable?”; no new cut proposed. |
| Learn how things work | MISSING phrase, accepted cut | Specifically removed at the owner's request September 14. Do not reverse that decision through an automatic reroll recommendation. |
| Practice writing, problem solving, making, working with people | RICH | 1:17–1:25: essays, math equations, physical objects, collaboration. |
| Find an interest and go deep | RICH | 1:26–1:31: find a specific subject and study deeply. |
| Knowledge and practiced skills remain yours as tools change; meaning of Be Smarter Than the Tool | RICH | 1:31–1:40: both relationship and course phrase are spoken. |
| Deep Subject Knowledge and its instruction | RICH | 1:48–1:56: field you care about; become the person others turn to. |
| Strong Skills and its instruction | TAUGHT | 1:57–2:07: practice writing, building, analyzing; turn knowledge into work you are proud of. Problem solving was already explained earlier. |
| AI Fluency and its instruction | RICH | 2:07–2:17: work with systems, challenge outputs, go beyond the average. |
| People Skills and its instruction | RICH | 2:17–2:27: listening, communicating, earning trust, team ideas into action. |
| School builds what takes you beyond the new average | RICH | 2:27–2:33: required takeaway spoken verbatim after a brief lead-in. |
| Both closing lines, in order, with no sign-off | RICH | 2:34–2:42 in the segment transcript: “The opportunity to learn is already in front of you.” / “Use it to build the knowledge and skills that take you beyond the new average.” |

The lesson arc is intact: school question → common AI baseline → personal contribution → school practice → four things to build → action. Formal vocabulary (“assets,” “pillars,” “navigate the complexities,” “strategically”) is less natural than the page's voice, but does not remove essential teaching. No narration graft, cut, or reroll is proposed. “AI provides raw material” is a useful addition.

**Source QA: PASS for the core lesson and boards.** The interactive Can You Catch It? exercise stays on the page; the upload prompt expressly excludes narrating the activity. The core lesson Markdown and current page agree. No new source-material changes were made.

## Proposed visual-only plan — not built

This supplies the section 1b board plan alongside the evaluation. Keep audio, runtime, and approved narration omissions. Target times below are output times; cutaway seams need final frame mapping before rendering. All replacement illustrations are proposals, not claimed existing assets or verified donors.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| Same Tool. Different Advantage. | Unmarked | Full board, still | Preserve 0:50.700–1:00.600, 9.9 s | Already suitable; whole-board idea, no individual-item teaching. |
| What to Start Building Today | Preserve full unmarked opening; then one whole-card ring at each named item; violet full-width takeaway ring. Fixed 4 px at 720p on rebuilt spans. | Dense; full view first, uniform complete-card dives, return wide for takeaway. Return from a cutaway to a still board view about one second before the next item's onset. | Preserve total topic span 1:40.433–2:34.133. Proposed drawing breaks: **1:52–1:56.1**, **2:03–2:06.6**, **2:12–2:16.5**, **2:22–2:26.3**. About **37.2 s** total board exposure; longest individual board segment about **11.6 s**. Final board+close run about **19.8 s**. | Preserve all teaching and readable instructions while meeting the approximately 20-second visual-variety target. Exact return/camera behavior gets previewed before encoding. |
| The opportunity to learn is already in front of you. | Unmarked | Current canonical white JPG; 48-frame hold, 150-frame push to 1.2×, settled hold | Preserve 2:34.133–2:46.133, 12 s | Correct current asset treatment without changing the successful ending. |

Supporting illustration proposals:

- Opening diagram's affected percentage states, approximately 0:37–0:43: a drawn shared AI starting point on two desks, without numbers or ranking. Preserve earlier useful diagram animation where possible.
- Approximately 1:12–1:17: a drawn student using school time to practice a project, replacing the alternate category list.
- Approximately 1:31–1:40.433: a drawn student retaining a notebook and built project as the tool beside them changes; no imaginary product names or alternate four-part taxonomy.
- 1:52–1:56.1, Deep Subject Knowledge: reuse a clean part of this video's microscope drawing from approximately 1:26–1:31, or a custom drawn student studying a subject if repetition looks poor.
- 2:03–2:06.6, Strong Skills: reuse the brief drawn bridge-model construction scene from approximately 1:21–1:22.4 with restrained motion, or a custom drawing of a student testing a model. Verify exact clean source frames before selecting reuse.
- 2:12–2:16.5, AI Fluency: custom drawing of a student checking an AI draft against a source; minimal text, no invented claims.
- 2:22–2:26.3, People Skills: reuse the clean meeting-table drawing from approximately 1:22.4–1:26.3, or a custom team discussion if repeat exposure feels weak.

Using this video's existing drawings is a legitimate option under current section 8b; the September 25 report's claim that reusing a still-narrated drawing necessarily required an exception was too restrictive. Custom illustration fallback follows new section 8d. Neither option requires new audio or pause padding.

**Narration changes: none. Selective pause additions: none proposed.** Preserve the explicitly approved 1:17 pause removal. No fresh auditory pacing judgment is claimed.

## Verification limits and evidence

Fresh work: public reference and video-hash verification; full sequential decode; board matching every 0.5 seconds; ring measurement every 0.5 seconds; visual contact-sheet review every 2 seconds across the runtime; detailed frame inspection of the numerical claims, board states, alternate skill list, and final frame; close geometry measurements; eight-boundary transition guard. Current page text, all three board assets, generation prompt, upload Markdown, and the complete applicable transcript were read.

**Not performed: real-time end-to-end audiovisual playback, listening to words/joins/cadence, every-frame inspection of all graphics, a new ASR run, or a fresh word-level onset audit.** Audio was not exposed for listening in this workflow. Consequently this report does not certify audio quality or full shipping readiness. The pre-existing joins around 0:50–1:01, 1:17, and 1:31 should be auditioned during a future candidate review. The tracker was not accessed; no workflow status is inferred from it.

The pristine generation rolls are not present in the current Prompts directory. If proceeding, use the hash-pinned shipped file as the disclosed source, preserve/copy its audio, and avoid stacking multiple lossy repair passes. Source reuse frames must be bound to this hash, not to a replaceable live filename alone.

Evidence: `verification.json`, `board-spans.txt/json`, `ring-stroke.txt/json`, `close-motion.json`, `contact-1.jpg` through `contact-4.jpg`, `frames/`, and `guard/transition-guard.md`. Applicable transcript: `../beyond-the-average-live-review-2026-09-25/beyond-the-average/transcript.txt`. Owner exceptions and shipped lineage: September 14 repair review, September 16 v6/v7 reviews, September 21 illustration-sync manifest.
