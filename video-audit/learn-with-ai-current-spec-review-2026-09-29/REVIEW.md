# Learn with AI — current-spec evaluation, September 29, 2026

**Recommendation: retain the shipped narration and make a targeted visual refresh. The live video does not fully meet today's production treatment.** The clearest opportunities are the 64-second and 56-second uninterrupted board runs, readable nonsense in the chat drawing, and the opening's apparent 3.5× learning-benefit claim. Preserve useful Notebook animation and the owner's expressly requested text-focused zooms.

This is an evaluation and proposed plan. No video, lesson, production asset, or tracker entry was changed. **This was a transcript and sampled-frame review, not end-to-end audiovisual playback.** Audio quality, natural pacing, and the complete animations remain unverified; this is not a shipping certificate.

## Exact live version

- Public page: <https://besmarterthanthetool.com/>. Its `studying` entry serves `course-assets/learn-with-ai/learn-with-ai.mp4?v=20260925ship14`.
- The public MP4 was streamed through SHA-256 without retaining a duplicate. Both public and local files hash to `61997998071f511fab088e0e7243efcc148917476c89646fed6066f7dc4793f1`, matching the September 25 v9 manifest.
- Fresh full sequential decode: **6,583 frames, 30 fps, 1280×720, 3:39.433**. The site's “4 min” label is appropriate.
- The public `StudyingWithAISection` matches the local page exactly. Teaching authority: this section, its three board images and close. Upload Markdown and generation prompt were also read.
- Standards: current `EDIT-SPEC.md`, `NARRATION-REVIEW.md`, and video README. Section 5's explicit fixed **4 px at 720p** rule governs new work despite residual 5 px checklist wording.
- All four current board hashes match their shipped build/sync manifests. The middle board includes the September 21 cast refresh.
- The complete prior v8 transcript was read and mapped onto v9's documented one-second silence deletion. See `transcript-mapped-v9.txt`. Approximate speech timestamps below are that mapping, not newly measured word onsets.

## Findings

| Priority | Evidence | Assessment and proposed action |
|---|---|---|
| Visual pacing | **0:55.333–1:59.400: 64.067 s**, Which Study Tool for the Job? **2:34.067–3:29.833: 55.767 s**, Your Four Moves for Gemini Notebook. Four Moves flows directly into the 9.6-second close, making the final continuous board sequence **65.367 s**. | Both boards remain actively taught; this is not dead narration. Section 8b calls for relevant supporting drawings around the approximately 20-second mark. Insert short, meaningful cutaways while retaining all explanations and the full quiz prompt. Section 8d now permits custom illustrations where surviving source drawings are insufficient. |
| Potentially misleading learning claim | **About 0:19–0:27**, the student → tablet → Study Efficiency animation reveals “Input 1 Hour Study” and **“3.5× Learning Output,”** with “High-retention active recall” below it. Confirmed at full resolution at 0:20 and in half-second reveal samples. | The animation usefully explains making study time count. The multiplier reads as a specific result a student can expect from AI, stronger than the narrated general benefit. Recommend changing only the result label to **“Practice, feedback, understanding”**, preserving the student, tablet, arrows, reveal, and timing. This is an editorial judgment about the claim conveyed, not a blanket ban on illustrative numbers. Exact affected frames and patch behavior need mapping before a build. |
| Distracting generated text | **About 0:49.6–0:55.333**, the notebook/chat drawing contains readable nonsense, including “Hi, watch, is bikey?” and “What is the one your right?” Confirmed at 0:52. | Retain the notebook and chat metaphor. Replace only bubble interiors with simple nonverbal text strokes, or short relevant study dialogue if it can be patched cleanly. No need to replace the entire drawing. |
| Old ring widths | Settled Focus/Exploration sections measure roughly **6 px**; middle-board cards roughly **6–7 px**; Four Moves purple/blue/amber cards roughly **6.5–7 px**. | Current target is 4 px, but section 5 explicitly grandfathers old shipped videos. **Do not rebuild for this alone.** Use 4 px on any board span rebuilt for the cutaways. Automated detections of 12–16 px in Four Moves include colored illustration edges and are not reliable ring measurements. |

The earlier board-arrival problems are fixed: Which Study Tool arrives with “As you can see here,” and Four Moves with “To get the most…”. Do not repeat the September 25 pre-v9 report's obsolete findings.

The study-tool dives crop away the top illustration, contrary to the generic complete-card rule, **but this is the owner's explicit September 25 instruction**. Preserve that exception. The text and its section rings remain readable. Four Moves retains complete active cards, including their illustrations and bottom text.

## What holds up

- The boards use the current assets and open complete and unmarked. Study-tool opening is about 6.9 seconds before the first ring; middle board about 3 seconds; Four Moves roughly 5.5 seconds. The earlier arrival added context rather than a new pause.
- Study-tool sections follow Focus then Exploration, their explanations, best uses, catches, and takeaway. Four Moves follows the four spoken moves and pulls back for the takeaway. The compact middle board remains full view with one whole-card outline per side.
- **How Gemini Notebook Works:** 2:06.067–2:28.367, **22.3 s**, followed by the files-to-study-tools drawing until 2:34.067. This is close to the approximate 20-second guidance and already has a relevant handoff. Preserve it rather than forcing another interruption.
- **Standard close:** 3:29.833–3:39.433, literal final frame, current canonical JPG, correct copy and white-stage treatment. Fresh geometry measures the pill at 721 pixels during the initial 48-frame hold and 865 pixels after the 150-frame push (**1.200×**), followed by a settled hold. No close replacement needed.
- No additional Notebook stock photograph or engine corner mark was found in the sampled frames. The photos in the canonical study board are expressly allowed by the course-board exception. Illustrated people are allowed.
- Fresh transition guard: 11 of 12 checked boundaries pass automatically. The one flag at the Focus dive is consecutive changes during a continuous zoom; its every-frame strip shows progressive zoom, not a stale inserted picture. All strips were inspected in an overview and the flagged strip separately. This does not certify audio joins.

## Narration

**Editorial verdict: KEEP the existing shipped narration, carrying forward its documented paraphrase treatment. This is not a clean verbatim pass against today's generation prompt.** The September build deliberately highlighted two banners under paraphrases, and the September 25 review retained that treatment. Their meanings are taught. No new narration cut, graft, or full reroll is recommended for this visual refresh.

| Teaching point, in lesson order | Assessment | Evidence on the current timeline |
|---|---|---|
| Too much schoolwork alongside family and sports | RICH | 0:00–0:13: history quiz, Friday essay, algebra, family, sports. |
| Cannot add four hours; make existing hours more effective | TAUGHT | 0:13–0:22: “We cannot add four more hours to your day…” The original joke is flattened, but its meaning survives. |
| AI as a useful learning tool, not just a way to finish | TAUGHT | Opening's “more effective,” patient-tutor explanation, later active testing and strengthening memory. |
| 1 a.m., never sighs, meets you where stuck | RICH | Approximately 0:27–0:38; all three benefits explained. |
| Choose based on existing materials versus something new | RICH | 0:40–0:55: complete guiding question and bridge to choosing a tool. |
| Focus / Exploration distinction | TAUGHT | 0:55–1:02 introduces both categories before the detail. |
| Focus is Gemini Notebook, grounded in your materials | RICH | 1:02–1:13: provided sources, study aids, focused exam preparation. “Only” and “strictly limited” are stronger than the page's language; preserve the existing edit, prefer the page's qualified wording in future generation. |
| Focus best use | RICH | 1:14–1:21: class notes, screenshots, study guides, webpage, YouTube video. |
| Focus catch | TAUGHT | 1:22–1:28: cannot reliably fill a missing key concept. |
| Exploration tools and broad training | TAUGHT | 1:28–1:39: ChatGPT, Claude, Gemini, massive data, generating explanations. “Or quiz you” is omitted, but the tool distinction remains clear. |
| Exploration best use | RICH | 1:40–1:46: no class materials, another explanation, extra practice. |
| Exploration catch | TAUGHT | 1:46–1:53: hallucination and explaining differently from the teacher. The explicit “expects it on the exam” clause is omitted. |
| Match tool to learning need | TAUGHT | 1:53–1:58: “choosing the tool that matches how you need to learn.” |
| Why Notebook for class-based study | RICH | 1:59–2:08: primary tool, grounded in the teacher's exact sources. |
| Upload materials | TAUGHT | 2:09–2:16: PDFs, slide decks, images, articles, YouTube links; notes appear elsewhere in the narration. |
| Get study tools | TAUGHT, incomplete enumeration | 2:17–2:25: quizzes, flashcards, study guides, audio overviews, mind maps. **Video overviews are not spoken**. The functional explanation is intact, but this does not satisfy a literal read-every-output instruction. |
| Turn materials into needed study tools | TAUGHT meaning; not verbatim | 2:25–2:33: “This pipeline takes a chaotic folder of raw class materials…” |
| One Subject per Notebook | RICH | 2:39–2:49: includes the history/math example and reason for separating subjects. |
| Give It the Full Picture | TAUGHT | 2:50–2:56: all materials, notes, slides, videos. |
| Quiz Yourself Blind | RICH | 2:57–3:10: names the move and reads the complete ten-question prompt. |
| Trace It Back | RICH | 3:10–3:21: click citation, return to original material, verify. |
| Strengthen learning rather than skip it | RICH meaning; not banner wording | 3:21–3:28: active testing and strengthening memory; reinforced by the first closing line. |
| Both closing lines, in order | TAUGHT, verbatim in transcript | 3:29.8–3:35.1: “Use AI to learn, not to skip the learning.” / “Feed it your materials. Trace it back.” No sign-off. |

**Hard requirements:** the exact quiz prompt and both closing lines are present in the complete transcript. Two banner lines are not spoken as written: “Turn your class materials into the study tools you need” and “Use AI to strengthen the learning, not skip it.” The first banner is near-verbatim (“choosing” rather than “Choose”). These discrepancies must remain visible in the review; the video's prior shipping does not make them verbatim. If requiring a fresh-generation exact-copy pass, those lines and the omitted video-overview item need new narration. No surviving `Prompts/learn-with-ai*.mp4` donor exists, so there is no verified audio repair to propose.

The arc is coherent: lack of time → patient tutor → which tool → why grounded sources → inputs/outputs → four habits → learn rather than skip. Some phrasing is more formal than the lesson (“dictates,” “constraint,” “pipeline,” “actionable,” “execute”). That is a voice weakness, not lost core teaching. The active-testing explanation and explicit reason to follow citations are useful additions.

**Source QA:** no contradiction between the core page and upload lesson found. The hidden accessible page text additionally says “It does not know what you did not give it.” The board and Markdown use the following missing-concept explanation instead, which teaches the same limitation. This is a copy-alignment difference, not a missing essential concept or reason to alter the board in this review. No product-capability fact-check outside the supplied course sources was undertaken.

## Proposed visual-only plan — not built

Preserve audio, duration, the approved pause removal, useful source drawings, and the expressly requested study-card text crop. Times below are current output times; proposed cutaway seams remain provisional until checked against exact words and camera states. No pause additions or narration changes are proposed.

| Board | Highlighting | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| Which Study Tool for the Job? | Full unmarked opening; Focus title/description/best use/catch, then Exploration equivalents, then full-width violet takeaway. Preserve sequence; rebuilt outlines fixed at 4 px. | Preserve approved dense text-focused dives and pan; pull back for takeaway. | Keep topic span 0:55.333–1:59.400. Proposed drawings **1:16–1:21**, **1:36–1:39**, **1:49–1:52**. About 53.1 s total board exposure; longest uninterrupted piece about 20.7 s. | Notes/files under Focus examples; alternate explanation under Exploration mechanism; teacher approach versus alternative approach under its catch. Return to settled board views before the next section ring. |
| How Gemini Notebook Works | Whole-card Upload, whole-card Get, violet banner; no additional subdivisions. | Compact, full view. | Preserve 2:06.067–2:28.367 and existing files drawing through 2:34.067. | Appropriate short board run with a meaningful visual handoff. No rebuild solely for legacy stroke. |
| Your Four Moves for Gemini Notebook | Whole-card outlines in spoken order, then violet banner; fixed 4 px when rebuilt. | Full unmarked opening, complete-card dives/pans, pull back. | Keep topic span 2:34.067–3:29.833. Proposed breaks **2:52.5–2:56.1**, **3:15.7–3:19.8**. About 48.1 s board exposure; longest piece about 19.6 s; final board-plus-close piece about 19.6 s. | Full-picture drawing under materials list; citation-to-source drawing under tracing back. Keep the complete blind-quiz prompt visible throughout its reading. |
| Use AI to learn, not to skip the learning. | Unmarked. | Preserve canonical close and existing hold/push/hold. | 3:29.833–3:39.433, 9.6 s. | Already suitable. |

Supporting visuals to retain, subject to motion/playback verification:

- **0:00–about 0:17:** workload diagram and 24-hour/four-more-hours illustration. The illustrative 28-hour demand and stress-capacity label express the hook; no blanket numerical cleanup proposed.
- **About 0:17–0:27:** student/tablet/result animation. Patch the specific result label described above while retaining motion.
- **About 0:27–0:39.9:** late-night tutor comparison and repeated-explanation sequence. Retain their teaching purpose; the human tutor's depicted hours are a scenario, not grounds to reject the whole scene.
- **About 0:39.9–0:49.6:** tablet desk, materials, and search sketches support the learning-choice question. The materials sketch is a candidate reuse source for the 1:16–1:21 break; confirm clean source frames before using it.
- **About 0:49.6–0:55.333:** notebook/chat illustration, with targeted bubble-text repair.
- **1:59.400–2:06.067:** animated teacher-materials/source-grounding diagram. Its illustrative textbook, notes, and study-guide labels support the narration. Do not replace it solely because it is an independent Notebook graphic. The old review's blanket rejection of invented mock labels is not today's section 8 policy.
- **2:28.367–2:34.067:** files-to-study-tools drawing. Retain; consider reusing a clean part at 2:52.5–2:56.1 only if the near repetition remains effective. Otherwise propose a distinct drawing of assembling notes, slides, and video into one subject notebook.
- **New illustrations proposed, not existing assets:** a different explanation of one problem for 1:36–1:39; two routes to the same problem with the teacher's route visibly identified for 1:49–1:52; a citation returning to a highlighted source passage for 3:15.7–3:19.8. Minimal text, no invented claims; match the existing drawn style. These show relationships rather than duplicate the course boards.

## Verification limits and evidence

Fresh checks: public reference and SHA-256; current live lesson comparison; full sequential decode; current board identities; half-second board matching and ring sampling; five contact sheets across the complete runtime; full-size problematic frames and final frame; half-second opening reveal samples; every-frame close geometry; twelve-boundary transition guard with strip inspection.

**Not performed:** end-to-end audiovisual playback, listening to words/joins/cadence, complete motion review, a fresh ASR transcription, every-frame watermark/photo inspection, or a fresh word-level highlight alignment audit. The existing audio grafts near 1:14/1:28/1:53 and 2:50/2:57, plus the removed pause near 0:22, remain listening checkpoints for a future candidate. The tracker was not accessed, and no workflow status is inferred.

Evidence files: `verification.json`, `transcript-mapped-v9.txt`, `board-spans.txt/json`, `ring-stroke.txt/json`, `close-motion.json`, `current-boards.jpg`, `opening-reveal.jpg`, `sheets/`, `frames/`, and `guard/transition-guard.md`. Exact board boundaries above come from the matching shipped manifests and inspected boundary strips; half-second ORB results are rounded corroboration.

If proceeding to a build, use the hash-pinned live file as the disclosed source: pristine rolls no longer exist. Preserve its audio and perform a single visual assembly, rather than stacking repair encodes.
