# Does AI Think? — current lesson comparison, October 23, 2026

Recommendation: pursue a targeted narration/board repair before requesting a reroll. A visual-only board replacement is insufficient. The installed video still explicitly announces five comparisons, walks Meaning and Experience separately, and teaches Beauty. The current lesson retains three rows: Experience and meaning, Word choice, Uncertainty. All three rows' essential explanations are present in the existing narration; no missing core explanation has been identified that requires a new generation.

This is a transcript-grounded editorial recommendation, not a completed listening review or a certified repair. The proposed cuts have not been auditioned. Under NARRATION-REVIEW.md, a formal feasible-REPAIR verdict and later KEEP/ship verdict remain pending listening and candidate review. Lack of audio perception is not evidence that a reroll is required.

## Exact source and review limits

CANDIDATE: `course-assets/does-ai-think/does-ai-think.mp4`, installed v10, 3:36.20, 6,486 frames, 1280×720, 30 fps. Current index cache key: `20260929ship-doesaithink-v10`.

SHA-256: `098b77a5b70fbc9ba6bce99e6b2b2f345343792a34688c1a2d6245a29df3771f`.

Fresh checks confirm the installed file is byte-identical to approved v10. Every AAC packet and its timestamps match v9, whose complete encoded transcript was read for this evaluation and copied here as `transcript.txt`. Thus this is the transcript of the installed audio, despite the original transcript's v9 heading. Segment timestamps are approximate speech boundaries, not frame-accurate cut instructions.

Read the current DoesAIThinkSection in index.html, both canonical lesson boards, lessons/does-ai-think.md, and the current generation prompt. Inspected all five fresh whole-file contact sheets, sampled every four seconds. This is not continuous playback or listening. The public server's file was not independently fetched; “installed” refers to the canonical course file referenced by the local page. No course content or video was edited.

## Teaching points, in lesson order

| Teaching point | Assessment | Installed narration evidence |
| --- | --- | --- |
| Human-like replies, explanations, jokes, apologies create the impression of someone inside | RICH | 0:00–0:21: examples and the felt impression are explained. |
| Ask whether AI understands the way a human does | TAUGHT | 0:21–0:32: the central question is explicit. |
| Sentence completion, poetry and conversation show capability, not proof of understanding | RICH | 0:33–0:46: all three examples, followed by the lesson's explicit caution. |
| Chinese Room setup: someone who cannot read Chinese | RICH | 0:46–1:00: room, person and absence of Chinese knowledge. |
| Incoming note and “How are you?” | RICH | 1:02–1:10: both the action and exact example. |
| Whole-phrase lookup despite inability to read | RICH | 1:10–1:21: unreadable note, entire phrase and chart. |
| Matching reply “I'm fine, thank you!” and returning it | RICH | 1:21–1:33: rulebook, reply and return through the door. |
| Outside observer sees fluent Chinese conversation | TAUGHT | 1:33–1:37: explicit outside perspective. |
| Convincing answer does not prove understanding | TAUGHT | 1:37–1:43: exact takeaway. |
| Producing and understanding are not necessarily the same | TAUGHT | 1:43–1:50: qualification “aren't necessarily” preserved. |
| LLM analogy limit: learned patterns, not a literal rulebook | RICH | 1:49–2:08: contrasts paper chart with training and explicitly states both required sentences. |
| Experience and meaning: lived events and personal meaning | TAUGHT, split across old rows | 2:17–2:20: “You connect words to what they actually mean in your life.” 2:25–2:28: “You draw on real things you have lived through.” |
| Experience and meaning: AI uses learned patterns and user input | TAUGHT | 2:20–2:24: “AI simply uses learned patterns and the prompts you feed it.” 2:28–2:33 adds training-data modalities. |
| Word choice: expressive intent versus repeated next-word prediction | TAUGHT | 2:34–2:42: both sides explained, including repetition. “Internal desire to speak” is more abstract than the lesson's plain wording, but the distinction is present. |
| Uncertainty: a person can recognize uncertainty | TAUGHT with wording concern | 2:54–2:57: “You inherently notice when you are unsure about something.” Stronger wording than the lesson's “You can notice”; it should not imply people always recognize their uncertainty. |
| Uncertainty: confident AI answers can be wrong | TAUGHT | 2:57–3:02: explicitly compares apparent certainty and wrong answers. |
| Similar-looking answers can come from different processes | TAUGHT | 3:06–3:09: exact comparison takeaway. |
| AI can still do impressive work | TAUGHT | 3:09–3:21: not dumb/useless; analytical work and organizing information. |
| Human-like output alone is insufficient evidence of human-like understanding | TAUGHT | 3:21–3:28: restated before the close. |
| Two closing lines in order | TAUGHT | 3:28–3:33: “Sounds human. Works differently.” then “A convincing answer doesn't prove understanding.” |

The Twenty Questions lab and Spot What's Wrong group activity remain page activities. The current video-generation instructions explicitly exclude lab narration; their absence is not a missing video teaching point.

## Hard requirements and source QA

All currently required verbatim passages appear in the matched transcript, disregarding punctuation/ASR spacing: sounding-like-a-person caution (0:40–0:46), outside-observer line (1:33–1:37), producing/understanding qualification (1:43–1:50), literal-rulebook/training pair (2:00–2:08), comparison takeaway (3:06–3:09), and both closing lines (3:28–3:33). The convincing-answer line also appears after the Chinese Room. The question and reply examples are both spoken.

SOURCE_QA: no material discrepancy found between the current page, revised canonical board, upload Markdown and prompt for the three-row lesson. Generation materials already request all three rows in order. The old five-row video, not the preparation bundle, is stale. No new philosophical claim is inferred from the thought experiment.

ERRORS / EXCESS: at 2:08–2:16, “five specific differences” is now a direct mismatch with the board. At 2:42–2:52, Beauty is obsolete content; “can only describe beauty by regurgitating learned structural patterns” also overstates the lesson's careful comparison and uses an unnecessarily dismissive verb. The uncertainty wording concern above is pre-existing, not caused by the board update.

ADDITIONS: the extra training-data modalities at 2:28–2:33 and examples of useful analytical work at 3:13–3:21 are compatible explanatory additions. The Beauty detour no longer belongs in the comparison. No essential current teaching depends on keeping it.

## Proposed narrow repair — not yet built or auditioned

Use installed v10 as the timing reference; use its pristine raw base `Prompts/does-ai-think-2mp4.mp4` and existing v10 build mapping when constructing an approved edit. All body speech through the close graft is already available. No synthetic narration or new recording is presumed.

| Source time, approximately | Exact spoken material | Proposed treatment |
| --- | --- | --- |
| 2:08.12–2:17.56 | “This side-by-side chart breaks down five specific differences between what happens when a human thinks and what an AI actually does. First is meaning.” | Remove the obsolete five-part introduction and first label. Introduce the current board visually during the preceding learned-patterns explanation, so it has a full-view opening before the first comparison. |
| 2:17.56–2:24.08 | “You connect words to what they actually mean in your life. AI simply uses learned patterns and the prompts you feed it.” | Retain under Experience and meaning. |
| 2:24.08–2:25.92 | “Second is experience.” | Remove the separate numbered-row label. |
| 2:25.92–2:33.00 | “You draw on real things you have lived through. AI works with patterns learned from text, images, audio, and other data.” | Retain under the same combined first row; no second highlight state. This preserves the current audio's meaning-first order within the combined topic. Reordering those sentences is optional, not necessary to preserve the lesson. |
| 2:33.00–2:34.92 | “Third is word choice.” | Remove the obsolete numbered label; the following full explanation clearly identifies word choice. |
| 2:34.92–2:42.84 | “You actively choose words to express an internal desire to speak. AI merely predicts the next word in a sequence then repeats.” | Retain under Word choice. |
| 2:42.84–2:52.76 | “Fourth is beauty. You have a genuine personal emotional response to art or music. AI can only describe beauty by regurgitating learned structural patterns.” | Remove the whole obsolete comparison. |
| 2:52.76 onward | “Finally, uncertainty” through the comparison takeaway and closing teaching | Retain. “Finally” remains correct for the third/final row. Check the human uncertainty wording during listening before deciding whether it needs a separate donor repair. |

These broad transcript cuts would remove roughly 23 seconds, making the result around 3:13; final duration depends on measured silent handles. They are not approved sample-accurate splice points. Before building, locate the actual word ends and silence, and audition the joins in context. Do not cut mechanically at segment timestamps or visual cuts. No extra pauses are proposed.

Potential optional uncertainty donor: `Prompts/does-ai-think-3.mp4`, approximately 2:28–2:31, “You notice when you feel unsure about an answer.” That is a complete existing sentence, with less emphatic wording. It has not been auditioned against v10 and is not a verified graft. Roll 1's next-word paragraph says “most probable” and its uncertainty paragraph says AI is “designed to sound highly confident”; importing whole alternate passages would introduce unnecessary issues. Do not reroll or graft merely to replace “inherently” without first listening and judging the exact delivery.

## Proposed board and camera treatment

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
| --- | --- | --- | --- | --- |
| When You Think. What AI Does. | Experience and meaning for both retained old explanations, then Word choice, then Uncertainty, then takeaway; one outline across both columns of the active row | Full unmarked opening, then uniform complete-row framing if the current three-row board remains too small at full view; pull back for takeaway. Fixed 4 px outline at 720p. | Approximately 40 seconds of comparison narration after the proposed cuts. Retain relevant existing learned-network, prediction and checking-an-answer cutaways; map them to the shortened timeline before setting exact windows. | Three rows replace five. The new asset is 1600×1310; old row coordinates and camera crops cannot be reused. Preview legibility before finalizing the dive. |
| The Chinese Room | Preserve approved camera-only walk | Preserve | Existing opening and continuous 1:09.50–1:50.17 board treatment retained, including the owner's prior long-board exception | No current content mismatch identified. |
| Sounds human. Works differently. | Preserve unmarked canonical close | Preserve existing hold/push/settle | Existing 8-second close shifted earlier only by approved cuts | Exact required lines already present; no new closing graft needed. |

Supporting scenes to retain, subject to motion/listening confirmation: opening chat and examples (0:00–0:40.70), Chinese Room setup (0:46.23–1:00), incoming-note cutaway (1:06–1:09.50), rulebook-to-learned-network explanation (1:50.17–2:07.97), learned-network insert (2:20.50–2:23), prediction example (2:38.70–2:41.50), student checking an answer (2:58–3:01.50), useful-work animation (3:09.90–about 3:22), and final comparison with its previously corrected footer (about 3:22–3:28.20). These serve identifiable teaching purposes in the sampled frames; motion was not watched. No replacement of them is proposed merely because a new still could be inserted.

LISTENING: none performed in this session; no available tool provided audio perception. The old 0:39 “thread/threat” transcription ambiguity and closing-graft listening limitation remain unresolved. The recommendation concerns alignment with the revised lesson. It does not certify narration delivery, audio joins, continuous motion, or readiness to ship.

If the proposed cuts cannot be made naturally, a reroll should teach only the three current comparisons, retain all Chinese Room examples and qualifiers, say “can notice” for uncertainty, avoid the discarded Beauty claim, and preserve both closing lines. The current prompt already provides that direction. A new generation is not yet justified by a missing essential explanation.
