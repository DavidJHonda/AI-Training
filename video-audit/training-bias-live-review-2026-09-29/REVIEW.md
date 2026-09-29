# Training Bias — live evaluation, September 29, 2026

**Recommendation: keep the narration; make a targeted visual pacing pass if revising this video. No reroll recommended.** The content recommendation is provisional pending listening. This review uses the complete timestamped transcript, fresh sampled frames across the entire encoded file, and live browser playback checks. It is not an end-to-end audiovisual sign-off: audio was not auditioned and continuous motion was not watched throughout.

## Exact version and scope

- Public video: https://besmarterthanthetool.com/course-assets/training-bias/training-bias.mp4?v=20260921ship22
- **4:21.00, 1280×720, 30 fps.** Public and local MP4 SHA-256: `0423a1b5f34337d130fbb1ff9392fa45ffab98d09426b47da68c8b99bc9917cd`; 25,555,256 bytes. This is the September 21 v7 illustration-sync release, based on roll 6 narration.
- Public MP4 and all six public JPGs match local files byte for byte. The TrainingBiasSection source and following local component text checked against the public HTML also match. See `public-verification.json` and `public-index.html`.
- Live lesson opened successfully, its WATCH control expanded, and video playback advanced. The displayed “4 min” is a reasonable rounded duration.
- Evaluation only. No video, board, lesson, website reference, tracker, release commit, or deployment changed. Tracker workflow status was not reviewed.
- Governing references: `scripts/video/README.md`, `NARRATION-REVIEW.md`, and `EDIT-SPEC.md` as of September 29. The current public lesson is the teaching authority; `lessons/training-bias.md` supplies the additional generation requirements.

## Teaching verdict

**KEEP, provisionally on content.** The lesson has a coherent progression: a memorable failure → the data mechanism → real consequences → questions students can use → stale information → current-source checks → retrieval and its limits. The opening does not read the page's first paragraph, but the essential “every individual fact can be right while the picture is distorted” distinction is taught explicitly at 1:38–1:52.

Timestamps below locate the spoken beats; segment ASR boundaries are approximate, not splice points.

| Teaching point | Assessment | Transcript evidence |
|---|---|---|
| Cow recognition works in familiar settings but fails on a beach | RICH | 0:00–0:22: familiar photos versus the same model encountering an unusual background. |
| Grass is the learned shortcut rather than the animal | RICH | 0:22–0:34: “green grass equals cow”; background instead of the animal. |
| A narrow slice becomes the model's whole picture | RICH | 0:46–0:56 explains the relationship between training distribution and worldview. |
| Skewed means distorted; stale means old | TAUGHT | 0:36–0:46 explicitly distinguishes the two traps before their detailed treatment. |
| Defaults | RICH | 1:02–1:11: frequent cases become the standard answer. |
| Blind spots | RICH | 1:11–1:18: rare cases contribute little learning. |
| Wrong patterns | RICH | 1:18–1:28: a secondary detail predicts the training answer and substitutes for the concept. |
| Demographic performance gaps and wrongful arrests | TAUGHT | 1:28–1:38 explains why this matters beyond cow photographs. |
| Correct individual facts do not establish a representative answer | RICH | 1:38–1:44 explicitly states this distinction. |
| Look for sameness; a default is not the world | RICH | 1:44–1:52 supplies the student's diagnostic clue. |
| Ask what's missing | TAUGHT | Approximately 2:02–2:05: “What's missing from this answer?” |
| Ask for exceptions | TAUGHT | Approximately 2:08–2:13: “Show me examples that don't fit the pattern you just gave.” |
| Remove the famous | TAUGHT | Approximately 2:15–2:20: “Answer again, leaving out the most famous examples.” |
| The model may have a broader picture but not lead with it | TAUGHT | 2:20–2:29 connects the questions to breaking the default. |
| Training stops; later events are absent from that training | TAUGHT | 2:29–2:39, followed by the separate retrieval mechanism later. |
| Cooper Flagg example: a correct fact was challenged, then corrected after web search | TAUGHT | 2:39–3:02 walks the four chat turns. The draft year and first-overall detail are visible rather than read aloud; the spoken example preserves the relevant error and correction. |
| The AI's self-explanation does not establish the cause | RICH | 3:02–3:12: “not evidence of the root cause”; cannot distinguish stale information from hallucination or another error. This qualification is essential and present. |
| When the date matters, verify against a current source | TAUGHT | 3:12–3:21 explicitly gives the practical response. |
| Retrieval-Augmented Generation named in full | MET in transcript | 3:25–3:30; acronym pronunciation still needs listening (see below). |
| Retrieve → add to context → generate | RICH | 3:30–3:49 explains each stage and their relationship. |
| Retrieval does not update training data or weights | RICH | 3:49–3:59: material enters active context for this response. |
| More to read does not guarantee truth | RICH | 3:59–4:11 covers both source reliability and interpretation. |
| Both closing lines, in order | MET in transcript | Approximately 4:11–4:17: “AI repeats the shape of its data. Ask what's missing. Check what's changed.” |

**Hard requirements:** all three exact prompts, the full RAG term, the self-explanation caveat, the context-versus-weights distinction, and both closing lines are present in the transcript. The LAB remains an activity below the video; it is not a missing spoken lesson section.

**Source QA:** no material contradiction identified between the current page, upload lesson, and transcribed teaching. This is not a new independent research audit of every historical claim. No narration cut, move, or graft is recommended. “Force the AI to reveal the missing context” around 1:57 is stronger language than necessary; “help reveal what is missing” would be gentler wording in a future generation, but is not a reason to replace this narration.

## Visual findings

1. **Highest priority: RAG at approximately 3:49–3:59.** The Generate card remains outlined after its explanation ends, while the narrator teaches that retrieval changes context rather than weights. This is the clearest mismatch between the active visual and the spoken idea. Introduce a relevant context/weights visual at this change of subject. Preserve the existing 3:59–4:11 animation, which progressively brings retrieved information into the active context and then marks an unreliable source. Do not replace that useful animation with a still merely for stylistic uniformity.
2. **Questions board, 1:52.27–2:28.60 (36.33 seconds).** Its three prompt highlights are helpful and readable. The extended introduction and nine-second takeaway make the overall hold feel like a slide presentation. Preserve the actual prompts on screen while spoken; use a relevant drawing under some of the setup or late takeaway. The earlier build record says it covered a raw-roll latent-space drawing here. That raw MP4 is no longer present locally, so restoring that drawing is not currently an available repair. A brief callback to the existing default-versus-reality scene is the available option to preview.
3. **Mechanisms board, 0:55.67–1:27.60 (31.93 seconds).** The rings correctly follow Defaults, Blind Spots, and Wrong Patterns; the duration is largely productive teaching. A short supporting example after an initial card explanation would improve variety without shortening the explanation. This is lower priority than the RAG mismatch.
4. **Chat board, 2:38.47–3:02.33 (23.87 seconds).** Preserve its continuous four-turn walkthrough. The text is comparatively small, but narration explains each turn and the rings identify the active bubble. Interrupting the exchange solely to meet a duration target would make the sequence harder to follow. The course's AI-chat rule calls for full-board framing, so do not dive into a single bubble.
5. **Keep the cow sequence and the canonical illustration walk.** They make the shortcut visible before the abstract explanation. The narrow 0:21.90–0:33.73 camera walk is a previously approved illustration treatment, not a cropped instructional card needing a redesign.
6. **Keep the supporting diagrams that explain relationships.** The skewed/stale fork, data/worldview progression, facial-analysis/error sequence, accurate-but-unrepresentative facts, knowledge cutoff, self-explanation versus cause, and final retrieval animation all serve the lesson. Some fine labels are small or technical; optional typography cleanup should be targeted, not a blanket replacement of effective motion.

The exact build boundaries give the longest continuous canonical-board run as **38.00 seconds** (RAG, 3:21.27–3:59.27). The other long holds are listed above. These boundaries match the fresh sequential scene-cut results and inspected frames. The slower ORB board-span scan was stopped before completion; it is not claimed as additional evidence.

## Proposed visual-only plan

These are proposals, not changes already made or approved. Preserve audio, total runtime, and existing pauses. Timing-dependent donor choices must be checked in motion before a build. The table keeps the useful highlighted walkthroughs and concentrates changes on their setup, supporting examples, and narration that has moved beyond the card.

| Board | Highlight sequence | Camera | Current span and proposed breaks | Reason / exception |
|---|---|---|---|---|
| Wrong Pattern. Wrong Answer. | Unmarked illustration | Preserve whole opening → machine → beach-card walk | 0:21.90–0:33.73; preserve all 11.83 s | Short, concrete, previously approved illustration treatment. |
| How Skewed Data Distorts the Picture | Whole Defaults card → whole Blind Spots card → whole Wrong Patterns card at spoken onsets | Full compact view; no dives | Current 31.93 s. Candidate break around 1:06–1:10 using the existing data-distribution drawing; return before Blind Spots at 1:11.22. Candidate cow/shortcut callback around 1:23–1:27 after Wrong Patterns is established. | Preserve each complete explanation. Donor selection/re-timing provisional until motion review; do not introduce a numerical claim or imply rare cases are the default. |
| Three Questions That Reveal Bias | Whole prompt cards, one at a time; brief takeaway-banner outline | Full compact view | Current 36.33 s. Extend relevant sameness/missing-context drawing under setup until about 1:57.7; establish the full board for about 3 s before the first card. After all prompts and a short banner hold, consider a callback to the existing default-versus-reality drawing around 2:23–2:28.6. | Reduces a long static setup and takeaway while keeping all verbatim prompts visible. Preview the repeated drawing for continuity and redundancy before committing; the covered raw-roll scene is unavailable. |
| Stale Information in Real Life | Each complete speech bubble in conversation order | Full compact view throughout | Preserve 2:38.47–3:02.33, 23.87 s | Deliberate exception: one coherent conversation, continuously walked. No added pause and no bubble zoom. |
| How RAG Works | Whole Retrieve → Add to Context → Generate cards; stop Generate emphasis when that beat ends | Full compact view; no dives | Current 38.00 s. Consider a relevant retrieval illustration under the 3:21–3:27 setup, then full board roughly 3:27–3:49. Replace 3:49–3:59 with a diagram distinguishing active context from unchanged weights; preserve the existing 3:59–4:11 reveal. | Strongest improvement. First inspect whether the existing animation can supply an appropriate earlier state without spoiling/repeating its later reveal. If not, propose one simple context/weights diagram; no new asset has been generated. |
| Closing message | Unmarked | Preserve canonical close and its existing motion | 4:11.67–4:21.00 | Both lines appear, followed by a settled hold. No additional outro. |

**Rings:** the September 21 video predates the fixed-4-pixel-at-720p rule. That rule explicitly grandfathers older releases; stroke alone does not justify a rebuild. Any newly rendered board span should use the current fixed-width renderer, measured card edges, locked colors, and full-board opening. Unchanged spans retain their approved treatment.

**Pauses and narration:** no proposed cuts, grafts, new silence, or rearrangement. No listening evidence currently supports a pause change. If a later listening pass identifies a rushed transition, measure the existing gap and propose a specific total gap before editing.

## Verification and limitations

- Public/local identity and all public board hashes verified directly.
- Fresh sequentially extracted contact sheets inspected across 0:00–4:20, including all boards, retained drawings, and close; see `visual-sheets/`.
- Live browser playback advanced from the opening to the closing card; normal-size board readability was spot-checked. This is not continuous end-to-end viewing or listening.
- Fresh transcript of this exact MP4 read in full against the current lesson (`training-bias/transcript.txt`). Sequential scene decoding completed all 7,830 frames. **Audio not auditioned.** The fresh transcript reads “RAG” at both occurrences; older transcriptions disagreed between “REG” and “RAG.” Listening is still needed to settle pronunciation. Fresh ASR also garbles the beginning of the current-source instruction around 3:15, while the earlier transcript reads “Whenever a specific date matters”; this is another targeted listening check, not a confirmed narration defect.
- Raw generations under `Prompts/training-bias*.mp4` are absent from the current workspace. Any visual repair would use the verified finished video and current board assets unless pristine source media is recovered; disclose that extra encoding generation in a build. No new splice or ship QA was necessary for this evaluation. Boundary-by-boundary transition inspection and end-to-end listening would still be required for a rebuilt candidate. Existing build records are context, not a new verification pass.
- Automated ORB board matching and the full-file ring-width scan were stopped before completion because of extended runtime during concurrent video work. No measured ring-width pass is claimed. The source manifest, fresh scene boundaries, and inspected current frames establish the board timings above; existing stroke treatment is grandfathered under the current spec.
- No KEEP decision here certifies final audio quality. The recommendation is to preserve the current teaching while addressing the focused visual opportunities above.
