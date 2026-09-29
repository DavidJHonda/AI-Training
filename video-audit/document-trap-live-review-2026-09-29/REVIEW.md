# Document Trap — public-video review, September 29, 2026

Scope: evaluation only. No lesson, video, prompt, tracker, or deployment changes.

The public page references `course-assets/document-trap/document-trap.mp4?v=20260921ship7`, displayed as 4 min. The served bytes, local canonical MP4, and stitched-v1 manifest's `render_sha256` all match: `3451967266e89b0543cdcd567f7c8c50b5843d9a8cacf4c745b316215de5329c`. This establishes that the retained stitched-v1 transcript belongs to this exact video, rather than an earlier version. Runtime is 226 seconds (3:46), 30 fps, 6,780 video frames according to container metadata. The public HTML is saved beside this report.

**Assessment: strong lesson structure, but not a KEEP as written.** Preserve the hook, worked example, four applied moves, and close. Correct the overconfident description of retrieval and the RAG graphic's promise of truth. These are specific defects rather than a reason to discard the whole visual treatment.

**Verification limit:** this is a retained-transcript and fresh sampled-frame evaluation, not an end-to-end audiovisual certification. Five fresh sequentially decoded contact sheets cover the actual public-matching file at four-second intervals. Motion, voice continuity, pronunciation, and joins were not personally heard/watched in real time. Do not treat earlier reviews' listening or transition results as new checks in this review. Timestamped wording comes from `video-audit/document-trap-stitch-2026-09-21/document-trap-v1/transcript.txt`, whose build timeline agrees with the current frames and public cache key. Fresh transcription did not complete and was stopped after repeated numerical warnings; wording is therefore not independently re-transcribed in this review. The automatic ORB board-span measurement was also stopped before completion; board durations below use the manifest and sampled visual confirmation, not a completed new feature-match measurement.

## Findings, in priority order

1. **1:04.7–1:14.2: a conditional process becomes a universal rule.** “A short file easily fits in full” and “With a long file, the system has to search…” replace the page's careful “may fit” and “may search.” A viewer learns that document length alone determines the ingestion method. Restore the actual lesson wording: “A short file may fit there in full. With a long file, the system may search for the parts that seem most relevant and add those passages instead.” This is also explicitly required by the current generation prompt. Direct file input and retrieval are distinct supported approaches; see [OpenAI's file-input documentation](https://developers.openai.com/api/docs/guides/file-inputs).
2. **Around 1:54–2:02: the RAG diagram ends in “Ground Truth Output.”** That label implies retrieval makes an answer true. It weakens the very reason this lesson teaches verification. Keep the useful web/database-to-model diagram, but replace the output label with “Answer.” This can be a targeted visual correction; replacing the entire scene is unnecessary.
3. **3:04.5–3:13.7: “you force the system… [to] uncover the verified six foul tournament exception.”** The example does need a six-foul payoff, and it supplies one. However, “force” makes the four moves sound like a guarantee. Prefer the source's example-specific result: “In this example, the tournament rule allows six fouls.” Keep the following warning about checking quotations. Similarly, 2:07.5–2:11.6 says the AI “misses it too,” where the page says “may miss it too.”
4. **Around 2:12–2:16: the handwritten note is largely pseudo-text.** It adds little to the important “sounds complete / missing passage” distinction. Optional polish: replace only this short insert with a clear incomplete-answer example or a useful existing drawing. It does not justify rebuilding the surrounding graphics.
5. **1:14.3–1:43.3: the process board runs 29 seconds without a cutaway.** It remains relevant: split, search, load, and the takeaway are being explained. Under the current >20-second guidance, a future full pass should include a short, relevant process illustration; there is no need to shorten the teaching or add an arbitrary pause. The current file's 1:00–1:14 context-window scene may provide suitable material, but its motion and reuse need review before choosing exact edit points.

## Narration against the current lesson

Provisional rubric verdict: **REROLL for replacement narration**, because an essential qualification is wrong and there is no verified, available donor that corrects it. This is not an instruction to throw away the current video's useful narration and visuals. Recovering a complete correct donor and auditioning its joins could make this a REPAIR. The known raw `Prompts/document-trap-*.mp4` files were not present in this workspace or the checked Downloads paths; retained transcripts alone are not usable audio donors.

| Essential teaching point | Assessment | Evidence on current timeline |
|---|---|---|
| Tournament next week; upload the league's 200-page rulebook; ask the foul question | RICH | 0:00–0:16.7; concrete question and five-foul answer |
| Remember last year's player; check original; five regular-season versus six tournament fouls | RICH | 0:17.9–0:38.6; exception and failure explained |
| Incomplete rather than made-up answer; uploaded does not mean fully read | RICH | 0:38.6–1:00.1; both ideas spoken |
| Document text must reach the context window to ground the answer | TAUGHT | 1:00.1–1:04.7 |
| Short files may fit; long files may use retrieval | WRONG | 1:04.7–1:14.2; qualifications hardened |
| Split: smaller pieces; Search: keywords and meaning; Load: selected pieces into context | RICH | 1:14.2–1:40.8; all three explained |
| Connect the process back to the missed tournament exception | RICH | 1:40.8–1:52.4 |
| Full RAG term; same approach can retrieve from web/database | TAUGHT | 1:52.4–2:01.9 |
| Retrieval's benefit and failure risk | TAUGHT, qualification defect | 2:01.9–2:16.3; benefit clear, “misses it too” overly definite |
| Name the Section, with explanation | RICH | 2:21.8–2:26.5 plus 2:39.5–2:42.7 |
| Ask One Thing, with explanation | RICH | 2:26.5–2:30.8 plus 2:42.7–2:48.1 |
| Apply the tournament/personal-foul/quote-and-exceptions prompt | RICH | 2:30.8–2:39.5 |
| Share What Matters: paste the exact relevant passage | RICH | 2:48.1–2:57.0; not merely a named tactic |
| Ask for the Quote and compare with original | RICH | 2:57–3:04.5 |
| Return to the six-foul result | TAUGHT, overclaim in lead-in | 3:04.5–3:13.7; result present, “force” should be corrected |
| Quote is useful because it can be checked | RICH | 3:13.7–3:17.9 |
| Transfer to leases, employment contracts, insurance, financial-aid letters | TAUGHT | 3:17.9–3:31.4 |
| Uploading and asking is a starting point; both closing lines | TAUGHT | 3:31.4–3:41.2 |

Arc: the story establishes the failure, the mechanism explains it, the moves address it, the worked example resolves it, and the ending transfers the habit. No missing major bridge. The pasted-passage and quote example is a useful elaboration beyond the public prose, supported by the current upload lesson.

SOURCE_QA: no material correction to the lesson source identified. Its conditional wording is precisely what needs restoring in the video. Five/six are this fictional league's rules, not a claim about all basketball.

## Required wording

The full term “Retrieval-Augmented Generation” and both closing lines are present. The foul question, five-foul answer, search takeaway, full tournament question, and quotation-checking line are present.

The current prompt's exact-word requirements still differ at four lines: “it was **just** incomplete”; “**The** document trap…”; “doesn't mean **the** AI…”; and the six-foul result is expressed as uncovering an exception rather than the required “In this example…” sentence. The first three preserve the meaning and are secondary to the substantive qualification problem, but a strict exact-word audit must record them. The earlier stitched review already disclosed these differences; they are not newly introduced defects.

## Proposed visual treatment if a repair proceeds

Timing below refers to the current edit; it is provisional if narration changes. No build authorized or started. No new pause proposed: listening is required before deciding whether any gap needs changing.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| An Incomplete Answer | Unmarked image; takeaway banner when spoken | Full view first; existing tray/exception detail walk, then full view | 0:38.73–1:00.10, 21.37 s | Existing photographic detail walk teaches selected pages versus omitted exception. It is an intentional exception to complete-card zoom framing; retain only if approved as such, rather than treating it as a new default. |
| Split, Search, Load | Whole Split column, Search column, Load column, then full takeaway banner | Compact full view; no card dive | 1:14.27–1:43.27, 29 s; propose a brief context-loading insert inside this run, exact timing pending motion review | Current cards are readable and emphasis follows the explanation. Break the long run without cutting teaching. |
| Four Moves for Better Retrieval | Whole named card at each spoken onset; no sentence-level sub-rings | Full-view arrival then complete-card zoom | 2:16.10–2:30.63 (14.53 s); targeted-question/search drawing until 2:47.90; board until 3:04.17 (16.27 s); quote-verification scene until 3:13.53; full board until 3:17.67 (4.13 s) | Good existing interleaving. Preserve full cards, including image, title, and description. |
| Closing message | Unmarked | Preserve current standard hold/push/settle, subject to frame-level check | 3:31.27–3:46 | Correct text and settled close appear in end samples. Last-frame and exact-motion certification not performed. |

The longest board run supported by the build manifest and fresh frame sequence is 29 seconds. The prior ring-width rule is grandfathered by Edit Spec section 5; stroke thickness alone is not a reason to rebuild this shipped video. Use the current fixed 4 px at 720p on any newly rendered board treatment.

Useful supporting scenes to preserve, subject to motion review: 0:00–0:38.73 rulebook/upload/five-versus-six story; 1:00.10–1:14.27 selected passages entering context; 1:43.27–1:52.4 omitted exception; approximately 1:54–2:02 RAG diagram with its output label corrected; approximately 2:02–2:11 complete/incomplete retrieval comparison; 2:30.63–2:47.90 targeted prompt and isolated tournament passage; 3:04.17–3:13.53 pasted passage and matching quote; 3:17.67–3:31.27 transfer to other documents. Invented section/page identifiers function as illustrative props; no consequential factual attribution was identified.

## Remaining verification

An eventual repair needs real-time review of the entire encoded result, listening around each graft, exact correction spans, pause measurements only where a pause is proposed, and transition/last-frame checks. No claim is made here that clips are aurally seamless or that every animation is effective in motion. Tracker status was not consulted or changed.
