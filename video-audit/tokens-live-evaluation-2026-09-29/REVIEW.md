# Tokens — live evaluation, September 29, 2026

## Result and evidence boundary

**Provisional narration verdict: REROLL under the course's replacement-for-reading standard.** The core explanation is strong, but the complete retained transcript does not explicitly teach two important lesson points: a token can be a whole word, and training and chat use the same tokens and IDs. No alternate Tokens audio source is currently available in `Prompts/` to establish a feasible graft. Recovering an existing donor could change this to REPAIR; a full regeneration is not required by the visual defects alone.

This is a transcript-and-frame evaluation, **not an end-to-end audiovisual certification**. No audio was heard, and continuous animation/playback was not observed. Pronunciation, prosody, splice naturalness, and mobile playback remain unverified. The verdict is provisional pending that listening check; it must not be represented as completed shipping QA.

## Exact live version

- Public page: https://besmarterthanthetool.com
- Public video: https://besmarterthanthetool.com/course-assets/tokens/tokens.mp4?v=20260927ship1
- The public page references that cache key and displays “5 min.” Actual retained runtime: **4:31.90**.
- Fresh public video stream SHA-256: `d1b7a9e0a5dabb90ec3bbb241518fc5727bab84be6f2bbd3327170b6812a1f16`.
- Local `course-assets/tokens/tokens.mp4` has the identical SHA-256. Thus fresh local frame inspection applies to the exact public bytes.
- Read the current public lesson source, local lesson Markdown, complete v9 timestamped transcript, v9 edit record, and current narration/edit rules. Extracted fresh frames every six seconds plus selected problem/boundary times. Also inspected retained encoded-state contact sheets for this exact version.
- This supersedes using the September 27 review of the older **5:05** video as an evaluation of today's site.

## Teaching coverage

| Lesson point | Assessment | Evidence in current transcript |
|---|---|---|
| Words in/out despite mathematical processing | RICH | 0:00–0:34; Avengers exchange gives a concrete hook. |
| A numbered dictionary of whole words cannot cover new slang, typos, emojis, and code | RICH | 0:35–0:58; million-word dictionary limitation is explained. |
| Tokens are reusable text pieces | RICH | 0:58–1:53; unbelievable and repeated un piece explain why reuse works. |
| A token may be a whole word or part of one | THIN | Pieces and subword examples are taught; no explicit whole-word case or statement in the transcript. The model's vocabulary is not exclusively word fragments. |
| Vocabulary means the model's collection of tokens | TAUGHT | 1:09–1:13. |
| Engineers choose splitting rules; a program builds vocabulary from text | TAUGHT | 1:54–2:04. Choosing vocabulary size is compressed, but the central construction process survives. |
| Token IDs identify pieces rather than their meanings | RICH | 2:15–2:23, then cat comparison at 3:01–3:25. |
| Same tokens and IDs during training and chat | MISSING | Explicit in public lesson and upload Markdown; absent from the full v9 transcript. This connects the vocabulary established before model training to its later use. |
| Text → tokenizer → lookup of IDs | RICH | 2:24–3:01; explains each stage and reads the three unbelievable IDs. |
| Concrete split examples | TAUGHT/RICH | Unbelievable earlier; basketball at 3:29–3:34; spaces/symbols at 3:35–3:51; URL count at 3:54–3:59. Removing repeated examples is acceptable compression. |
| IDs converted back into readable answer | TAUGHT | 3:59–4:19. “Mathematical process simply runs in reverse” is loose shorthand, but the following explanation correctly identifies decoding IDs into text; it does not explicitly say the neural network itself runs backward. |
| Both closing lines | MET | 4:21–4:27: “Words become numbers.” / “That lets AI work with your language using math.” |

The lesson arc is coherent: why a word dictionary fails → reusable pieces → vocabulary and IDs → send-time lookup → IDs are not meaning → concrete splits → readable output. Preserve that structure. The cat comparison and space-plus-symbol example are particularly useful.

## Material findings

1. **Missing spoken completeness points.** Add the whole-word possibility and the shared training/chat vocabulary. Suggested intended content: “A token can be a whole word or just part of one” near 1:01, and “The model uses those same tokens and IDs during training and when you chat” before the send-time walkthrough at 2:24. These are proposed script lines, not existing or auditioned audio. Only the identical v9 candidate survives in `Prompts/`; no repair donor is established.
2. **Building Blocks framing, approximately 1:14–1:48.** Fresh frames confirm the large interior-machine crop and subsequent reuse-row crop remain in v9. They make individual text larger, but lose the complete illustrated card and separate the pieces from the reuse relationship. Recommend a complete-board view under the current complete-card framing rule. This is a visual repair, independent of the narration verdict.
3. **Long board exposure.** Building Blocks lasts 50.20 seconds. Send → Cat → Splits is still a continuous 95.60-second board sequence, from 2:23.97 to 3:59.57. The examples cut improved this by 33.37 seconds. These durations are review triggers, not automatic failures: narration continues explaining the displayed content. A useful same-topic supporting scene could help, but no suitable alternate scene is verified. Do not insert decorative filler or cut essential explanation merely to meet a duration threshold.
4. **Vocabulary-size wording, 2:06–2:15.** The corrected picture names GPT-4o/o200k_base and Gemini 1.5 Pro/Flash, but the narration and lesson use broader brand-wide wording. Prefer explicitly model-specific examples in the next revision. OpenAI's official tokenizer source maps models to different encodings: https://github.com/openai/tiktoken/blob/main/tiktoken/model.py . Google's token guide defines vocabulary but does not establish a universal Gemini vocabulary size: https://ai.google.dev/gemini-api/docs/tokens . This review has not independently established the stated Gemini count or Claude-publication claim. Do not label those numbers disproved; they remain incompletely verified and overly broad in wording.

## Proposed visual treatment

Times below are the current output, not a newly approved edit timeline. No build or source modification was performed.

| Board | Current span / duration | Highlight and camera recommendation | Break / reason |
|---|---|---|---|
| You Use Words. AI Uses Numbers. | 0:10.30–0:32.50 / 22.20s | Preserve full view and question → answer bubble outlines. | Complete exchange serves the hook. |
| Building Blocks for Language | 1:04.90–1:55.10 / 50.20s | Full unmarked opening; preserve complete board through split/reuse explanation; retain takeaway outline. Remove interior-photo and reuse-row dives. | No verified supporting donor. Preserve the visual relationship; check full-frame readability before finalizing treatment. |
| What Happens When You Hit Send | 2:23.97–3:01.67 / 37.70s | Preserve full view, Start With Text → Split Into Tokens → Look Up Token IDs → takeaway rings. | Each stage supports spoken process; no justified filler break. |
| Humans See a Cat. AI Starts With a Token ID. | 3:01.67–3:26.60 / 24.93s | Preserve full view; human card → token-ID card → takeaway. | Strong distinction, suitable bridge to Embeddings. |
| How AI Splits Text Into Tokens | 3:26.60–3:59.57 / 32.97s | Preserve full opening, then complete basketball → spaces/symbols → URL rows, with consistent row framing. | Shortened version teaches useful variety without repeating all five rows. Numbering 2, 4, 5 matches the visible board. |
| Words become numbers. / That lets AI work with your language using math. | 4:21.13–4:31.90 / 10.77s | Preserve canonical close and existing motion, subject to actual playback check. | Fresh final-frame sample confirms correct ending card. |

Preserve potentially useful independent Notebook scenes: word-to-number dictionary at approximately 0:35–0:44, evolving slang/code collage at 0:46–0:52, reusable-pieces scene near 0:58–1:04, corpus-to-vocabulary process near 1:55–2:04, ID mapping at 2:15–2:24, and return-to-text sequence at 3:59–4:21. Their still states support the teaching; motion/reveal quality was not certified. Keep the vocabulary chart's animation if its model-specific factual wording is resolved; count-up intermediate values are not factual errors.

## Audio and source checks still open

- Audition 1:22–1:25 and 2:41–2:48 for token-piece and tokenizer-name pronunciation. ASR spellings such as “claw” and “Clods” are not evidence of narrator mistakes.
- Audition existing joins at 3:29.50, 3:34.20, and 3:59.37. Retained signal checks cannot prove audible naturalness.
- No new pause is proposed without listening and measured need.
- Exact example IDs were not recomputed in this evaluation. Existing board/source attribution remains in place.
- No tracker workflow status was verified or changed. No site, lesson, production video, Git commit, or deployment was changed.
