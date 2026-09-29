# Hallucination: live-video evaluation — 2026-09-29

**Recommendation: targeted narration repair, with visual pacing improvements. Preserve the lesson and its worked examples.** This is a transcript-and-frame evaluation, not an end-to-end audiovisual sign-off. No video, lesson, or public site was changed.

## Verified source

- Public course: https://besmarterthanthetool.com/
- Public video: https://besmarterthanthetool.com/course-assets/hallucination/hallucination.mp4?v=20260921ship21
- Public and local video SHA-256: `1c7189c1aedafb057d1740e60d469a55209c3350ad3de504dc363f3bcf44c253`.
- Local file: `course-assets/hallucination/hallucination.mp4`; 4:40.40, 1280×720, 30 fps, 8,412 frames. The 5 min watch label is appropriate.
- The public `HallucinationSection` is identical to the local section. Both source snapshots are saved beside this report.
- Read the full current lesson, upload Markdown, complete retained finished-video transcript, current board assets, and September 29 production standards. Inspected six newly decoded contact sheets spanning the entire public-identical file at four-second intervals.
- Historical provenance: v12 is the September 21 illustration-only update to v11; v11/v10/v9 share the narration. The retained v9 finished-file transcript and raw-roll word timings therefore apply before the closing edits. Transcript read in full: `video-audit/hallucination-comparison-2026-09-21/build-v9/verification/hallucination-v9/transcript.txt`. Word timings: `video-audit/hallucination-comparison-2026-09-21/hallucination-1/words.json`.

## Findings, in priority order

### 1. Correct the grammar guarantee at 1:56–2:08

At approximately 1:56.46–2:01.50 the transcript says: **“The token prediction process ensures the grammar and syntax are always correct.”** The following sentence doubles down: **“The output sounds structurally perfect, even when the underlying facts are completely invented.”**

Token prediction does not guarantee grammatical correctness. The lesson's actual point is that plausible wording does not establish truth. It already teaches that correctly immediately before this passage, at approximately 1:47–1:56. The added guarantee is unnecessary and wrong. As a concrete counterexample to the guarantee, the [GrammarGPT authors](https://arxiv.org/abs/2307.13923) describe prompting a language model to generate ungrammatical sentences; token prediction can produce such output.

**Proposed repair:** remove both sentences, approximately 1:56.35–2:07.93, joining “…is a factual truth” to “People often use the term hallucination…”. All essential mechanism teaching remains. Local silence detection finds quiet intervals at 1:56.097–1:56.635 and 2:07.633–2:08.251, so these provisional cut points lie inside measured gaps. The join has not been auditioned; these are planning points, not approved frame-accurate edit decisions.

### 2. Remove the unsupported frequency claim at 0:48–0:51

“A hallucination **rarely** makes up the entire response” turns the page's correct statement—“does not have to make up the whole answer”—into an unsupported general claim about frequency. Hallucinations can be isolated details or extensive fabrications. The useful explanation is the next sentence about mixing fabricated details with real facts.

**Proposed repair:** remove the frequency sentence and assess the opening of the following sentence (“Instead, it embeds a fabricated detail…”). A possible local cut would join the definition to “It embeds…”, preserving the complete explanation at 0:51.86–0:56.90. This requires listening to the sentence attack and cadence before accepting the edit. No replacement voice or verified donor is claimed. No raw `Prompts/hallucination*.mp4` source currently exists in the workspace; the finished video is the available repair source.

### 3. Break up the longest board walks

The original build manifest gives these runs, consistent with the new sampled frames:

| Visual | Live interval | Unbroken duration |
|---|---|---:|
| Nothing Sounds Wrong | 0:10.53–0:39.83 | 29.30 s |
| Why Hallucinations Happen | 1:11.77–1:56.57 | 44.80 s |
| Real Text. Wrong Meaning. — first walk | 2:28.23–2:55.93 | 27.70 s |
| Check the Claim | 3:12.17–3:59.47 | **47.30 s** |
| Real Text. Wrong Meaning. — application | 4:03.17–4:29.50 | 26.33 s |

The rings and camera walk help, but the Check the Claim sequence spends almost a minute on one three-column board while the narration works through a specific study. It would teach more concretely if the student could also see the invented study or the claim being checked. The Why board is another clear candidate for supporting scenes under the September 23/29 version of Edit Spec 8b. These are engagement findings, separate from narration accuracy. Retain the useful pizza close-ups; they show the mechanism being explained.

### 4. Secondary wording and visual polish

- At 1:29–1:37, “which word is mathematically most likely to follow the previous one” is a compressed description. Tokens need not be whole words; prediction uses context, and generation need not always choose the top-probability token. Prefer the page's “predicting which token is likely to come next” in future narration. The sequence does explicitly name tokens, so this is less severe than the grammar guarantee.
- “Logical friction,” “mechanical failure,” and repeated “this graphic/diagram” framing are more formal than necessary for 16-year-olds. They do not erase the explanations. Avoid cutting good teaching solely to simplify the register.
- The monitor illustration at roughly 1:57–2:08 contains pseudo-text inside its magnifier. Removing the unnecessary grammar passage also removes most of this distracting span.
- The fake academic document around 0:57–1:06 is contextualized as a hallucination blueprint, not presented as authentic evidence. Do not reject it merely because the displayed paper is invented: invention is what this scene explains. Any reuse needs a closer label/motion check.

## Narration coverage

**Verdict: REPAIR recommended, provisional pending listening and edit-feasibility checks.** This file does not earn KEEP because of the factual addition above. A reroll is not currently justified by missing essential content; local cuts appear sufficient, but no unlistened join is certified as a feasible finished repair.

| Essential teaching point | Assessment | Evidence in live timeline |
|---|---|---|
| Student's music/chemistry question | RICH | 0:00–0:10; relatable setup |
| Invented 2022 Stanford study, 1,200 students, 18%, 60 dB | RICH | 0:16–0:28; numbers explained |
| Credible details are not evidence; no study/paper/source | RICH | 0:28–0:41; invention explicitly revealed |
| Hallucination definition | TAUGHT | 0:41–0:48; invented factual claim that sounds true |
| Real facts can conceal an invented detail | RICH, with unsupported added qualifier | 0:48–0:57; retain explanation, remove “rarely” claim |
| AI imitates the form of research findings | RICH | 0:57–1:11; percentages, sample sizes, academic tone |
| Training text includes mistakes, jokes, lies | TAUGHT | 1:20–1:29 |
| Generates one token at a time | TAUGHT, simplified wording | 1:29–1:37; see wording note above |
| Training to be helpful can encourage answers without verified data | TAUGHT | 1:37–1:47 |
| Probable wording does not establish factual truth | RICH, followed by WRONG addition | 1:47–1:56 correct; 1:56–2:08 adds grammar guarantee |
| Not every wrong answer is an invented source | RICH | 2:08–2:16 and 2:44–2:55 |
| Glue-on-pizza case; one-eighth cup; real sarcastic Reddit source | RICH | 2:16–2:44 |
| Invented study versus misinterpreted real text | RICH | 2:44–2:55; distinction spoken |
| Notice questionable claims without doubting every sentence | TAUGHT | 2:55–3:12 |
| Notice the claim / Find the source / Check the match | RICH | 3:12–3:21, then applied |
| Apply checking to Stanford; prestige isn't proof | RICH | 3:21–3:49 |
| Failure to find a source doesn't itself prove falsehood | RICH | 3:49–4:03; unverified numbers must not be repeated as established facts |
| Apply checking to pizza; real text must support the claim | RICH | 4:03–4:29 |
| Both closing lines, in order | MET in transcript and sampled close | Approximately 4:30–4:37 |

The arc works: persuasive false answer → why fluent text can be wrong → different source failure → a repeatable checking method → both examples revisited → concise takeaway. The worked applications are a strength, not expendable repetition. The Dino Game LAB remains a separate page activity, consistent with the watch strip saying both routes end at the LAB; no omission verdict for not narrating the click-by-click lab.

**Source QA:** the substantive page teaching and generation Markdown agree. [Google's May 2024 account](https://blog.google/products-and-platforms/products/search/ai-overviews-update-may-2024/) supports the pizza example's mechanism: sarcastic forum content was interpreted as useful advice. The useful distinction is invented evidence versus mishandled evidence; avoid presenting the lesson's narrower use of “hallucination” as a universal research taxonomy. No material source correction is required for the identified grammar problem, which was added by the video.

## Proposed visual plan, separate from narration verdict

These are proposals, not edits. Times use the current live timeline and would shift after narration cuts. Additional supporting scenes must be selected and previewed before a full visual rebuild; the table does not pretend an uninspected donor exists.

| Board | Highlight sequence | Camera | Time / proposed break | Reason or exception |
|---|---|---|---|---|
| Nothing Sounds Wrong | AI speech bubble, then entire gold reveal banner | Full view; no conversation dive | Current 29.3 s. Consider a brief paper/source illustration during the credibility explanation, then return for the reveal | Preserve the question/answer reading and clear fake-study reveal. No approved cutaway yet |
| Why Hallucinations Happen | Full-height columns in spoken order: training text → tokens → helpfulness → probable ≠ true | Establish whole board; retain complete-column framing and uniform camera window | Current 44.8 s. Proposed supporting scene between early and late points; choose a genuinely relevant depiction of prediction or missing evidence first | Current tall columns gain only modest size from the pan. No decorative filler or unverified donor |
| Real Text. Wrong Meaning. | Unmarked | Preserve full establish, joke-card focus, machine/output focus, return | Current 27.7 s + 26.3 s. Retain these useful illustration walks provisionally | They explain the actual source-to-wrong-advice transformation; not a static three-column board |
| Check the Claim | Whole-height columns at named steps; repeat as applied to Stanford | Full view, compact; restrained push only | Current 47.3 s. Candidate break during ~3:23–3:30 using the existing hallucination-blueprint scene from ~0:57–1:06; another during ~3:49–3:59 using the existing UNVERIFIED ≠ FACT scene from ~3:59.5–4:03.2 | Makes the worked example visible. Reuse would split the long board into shorter intervals without changing its narration; check labels, motion, timing, and return framing first |
| Closing message | None | Preserve standard hold/push/settle if motion check confirms it | Current 4:29.50–4:40.40 | Exact current closing message visible; final spoken words match |

Retain provisionally: study/music opening (0:00–0:06), disintegrating paper/laptop (0:40–0:49), fabricated-detail paper (0:51–0:57), hallucination blueprint (0:57–1:06), perceptual eyes (1:06–1:11), crossed-out “ALL ERRORS = INVENTIONS” (2:08–2:17), pizza search/advice (2:17–2:28), TRUTH/FALSEHOOD comparison (2:56–3:12), and UNVERIFIED ≠ FACT (3:59–4:03). They support identifiable teaching beats. Sampled stills establish their content but do not certify animation timing.

**Pauses:** no new pauses proposed from a transcript-only pacing judgment. Preserve existing gaps until a listening review identifies a specific comprehension problem. Measured silence at the proposed grammar cut is for safe editing, not a reason to insert additional silence.

**Rings:** existing v12 predates the fixed 4 px-at-720p rule. The current spec expressly says not to rebuild old releases solely for the earlier stroke rule. If board spans are rebuilt, apply the current fixed stroke after camera cropping and retain full-height column boundaries. No ring-width failure is claimed from thumbnail appearance.

## Verification limits

- Public page and entire streamed MP4 hash verified; no claim based merely on a filename or old ship note.
- Complete transcript reviewed; newly generated four-second contact sheets inspected end to end, plus full-size current board JPGs.
- Fresh full-file transcription and ORB board matching were started but did not produce results during the review and were interrupted. No new ASR or ORB pass is claimed. Quoted narration comes from the retained finished-file transcript; exact board boundaries come from the build manifest, corroborated visually by fresh frame samples. The fresh sequential frame extraction completed successfully.
- No real-time end-to-end watch/listen, subjective voice/pause evaluation, frame-by-frame transition inspection, or audition of proposed joins was completed. No animation is certified solely from stills.
- No new candidate was built. No KEEP/ready-to-ship assertion, deployment, tracker status change, or publication.
- Video Tracker was not accessed; this report makes no claim about its workflow status.

## Build follow-up

David approved the targeted repair. [v14 build and verification](../hallucination-v14-2026-09-29/REVIEW.md) is now ready for audiovisual review; no site changes or publication.
