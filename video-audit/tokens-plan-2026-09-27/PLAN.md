# Tokens — proposed narrow repair

**Overall recommendation: REPAIR the vocabulary-chart label and update highlights in the repair. Preserve the existing narration, graphics, animations, pauses, and purposeful board camera moves. No established reason for a reroll.** Plan only; no lesson, prep, video, or publication changes.

The current published reference is `course-assets/tokens/tokens.mp4?v=20260922ship6`, 5:05.27, 9,158 frames at 30fps. Fresh sequential decoding completed. SHA-256 `48f170a1ed6794de08903ca578570dab9186d80ac605896bc9718c7e9433aa1f` matches the retained production manifest and the prior same-day published/local comparison. All five teaching-board hashes still match that manifest. No new public download was performed.

## Teaching and narration

Read the current TokenSection in index.html, current lessons/tokens.md, current prompt, complete published-file transcript, prior production review, Narration Review, and current Edit Spec. Narration assessment is transcript-based, with the limitations below; it is not an end-to-end listening certification.

| Point | Current time | Assessment |
|---|---|---|
| Math operates on numbers while you use words; Avengers exchange | 0:00–0:30.66 | RICH: question and full answer read. |
| Why assigning one permanent number to every word breaks down | 0:32.46–1:04.08 | RICH: slang, typos, emojis, code, million-word dictionary, reusable pieces. |
| Tokens and vocabulary; unbelievable and reuse of un | 1:04.82–1:53.32 | RICH: three pieces and reuse in unbelievable, unmatchable and unusual. A whole-word token is demonstrated later by cat, although the earlier definition does not explicitly repeat “a whole word or part of one.” |
| Vocabulary construction before use; token ID as address rather than meaning | 1:54.90–2:23.24 | TAUGHT. The page's sentence explicitly saying the same vocabulary/IDs are used during training and chatting is not spoken. This is a minor missing reinforcement, not an established material misunderstanding demanding a new generation. Vocabulary-size claims are generalized by product in both lesson and narration; model-specific wording would be more precise in future materials. |
| Three Send steps; unbelievable IDs 359, 32898, 24694 | 2:24.08–3:00.90 | RICH. |
| Human understanding versus cat ID 4719 | 3:01.70–3:25.00 | RICH; ID is identified as a structural tag, not meaning. |
| Five worked splits and their counts; spaces/SP; eight-piece URL | 3:26.56–4:32.36 | RICH in example coverage. ASR merges some URL fragments in transcription; spoken separation is unverified, not an established error. |
| IDs return to text | 4:32.80–4:52.76 | TAUGHT. |
| Two closing lines | 4:56.76–5:00.40 | Both wording sequences present. Cadence not independently auditioned. |

The seven required prompt passages' words are present in the transcript, with some combined punctuation in ASR. ASR punctuation cannot certify or disprove separate-sentence cadence. Keep the previously accepted delivery rather than reroll over transcript spellings. The prior September 22 review records David accepting the Claude line and specifically authorizing the removal of the redundant bridge before the examples; do not restore that bridge.

Specific listening checks remain: 1:22–1:25 (un/belie/vable), 2:41–2:48 (cl100k_base), 4:14–4:23 (URL chunks). No verified pronunciation error or complete alternative audio donor has been established. A local search found no surviving Tokens MP4 raw rolls or candidate donors under Prompts/video-audit, despite older documentation naming them.

## Concrete repair

**Around 2:06–2:15, vocabulary-size demonstration:** the left card's subtitle reads `GPT-4o / cl100k / o200k` above `200,000`. This mixes two different tokenizers. OpenAI's official mapping assigns GPT-4o to o200k_base and GPT-4 to cl100k_base: https://github.com/openai/tiktoken/blob/main/tiktoken/model.py . Change only that subtitle to `GPT-4o • o200k_base`; preserve the original chart, numerical count-up animation, narration, and adjacent demonstrations. The count-up's intermediate values are animation, not errors. Mark the display as model examples if needed to make its existing version labels clearer; do not introduce new statistics or claim these are permanent brand-wide vocabulary sizes.

**Highlights throughout the five teaching boards:** existing rings are roughly 6–7px in retained sampling; some detector hits inside cat artwork are false positives. Older widths are grandfathered, so this alone is not grounds for a rebuild. In the authorized chart repair, rebuild outlines at the current fixed 4px/720p after camera transforms, preserving their whole-bubble/card/row targets and spoken timing. Do not change canonical JPGs.

No narration cuts, grafts, reorder, or new pauses proposed. Preserve original illustrations and motion, including descriptive demonstrations. A drawing that differs from the canonical example is not automatically a defect.

## Board plan and continuous durations

| Board | Current interval | Continuous duration | Planned highlights/camera |
|---|---|---:|---|
| You Use Words. AI Uses Numbers. | 0:10.30–0:32.50 | 22.20s | KEEP full-view conversation; question bubble then complete answer bubble; 4px outlines. |
| Building Blocks for Language | 1:04.90–1:55.10 | 50.20s | KEEP full opening, machine/token close-up, move to complete reuse row, return to full view/banner. Banner outline only; do not ring the photograph. |
| What Happens When You Hit Send | 2:23.97–3:01.67 | 37.70s | KEEP full-board framing, three complete step targets followed by takeaway; 4px. |
| Humans See a Cat. AI Starts With a Token ID. | 3:01.67–3:26.60 | 24.93s | KEEP full view, complete human card then complete ID card then banner; 4px. |
| How AI Splits Text Into Tokens | 3:26.60–4:32.93 | 66.33s | KEEP full opening and uniform complete-row zoom/pan for each of five examples, then pullback; 4px. |
| Words become numbers. / That lets AI work with your language using math. | 4:54.50–5:05.27 | 10.77s | KEEP existing standard close unchanged. |

The longest continuous single teaching board is **66.33s**. The Send → Cat → Splits chain is **128.97s**, including all movements and pauses. Camera moves do not reset either count.

These are genuine pacing exceptions, not hidden by the row changes. My recommendation is to keep them for this narrow repair: the narration is actively teaching the corresponding components/examples, and replacing their visuals risks hiding what the viewer needs to follow. No convincing same-lesson drawing donor has been established for cutting into those calculations. Do not insert unrelated stills to meet an arbitrary duration target. A separately approved pacing rewrite could shorten the teaching; it is not required to correct the chart label.

### Revision to the earlier section audit

The earlier recommendation to remove the Building Blocks photo dive was too broad. Fresh full-resolution frames show the complete word and all three token tiles during the split explanation (1:23), then the complete reuse row during its explanation (1:38). The board opens complete first and returns to full view. This is a purposeful illustration tour, not evidence that the teaching is hidden throughout 1:14–1:47. Preserve it. The full board is the current canonical asset; its people/photo imagery is not a newly inserted stock-photo scene.

## Verification completed and limitations

Completed now: fresh 9,158-frame sequential decode; source/manfiest identity; all five current teaching-board hash matches; current page, Markdown, prompt and complete transcript review; canonical-board sheet and both overview sheets inspected; fresh selected full-resolution frames including 1:23, 1:38, 2:12.50 and 4:14 inspected; official tokenizer/model mapping checked. Evidence is in source-checks.json and frame-*.jpg.

Retained rather than repeated: fourteen-boundary transition guard passed for this exact hash; four-second highlight sampling; same-day published/local byte comparison. No observed new transition defect is asserted, and no fresh exhaustive transition-strip inspection was performed for this plan.

Not completed: end-to-end real-time watching/listening, warmth/prosody and pronunciation, audible joins/pauses, mobile playback/readability, exhaustive encoded-ring scan, or independent re-encoding of every token example. The local Python environment lacks tiktoken, so a new local token-ID computation could not run. No fresh independent verification of the Gemini/Claude vocabulary-size claims was completed. No tracker access/update or publication. The original generation files are unavailable locally. These limits are not presented as passes.

Build only after David approves the scope; compare the eventual candidate against this plan and verify the restored/original footage remains intact.

## Approved scope amendment — three narrated examples

David asked whether narrating all five split examples was useful and approved building the recommendation to narrate three: basketball (one word, two tokens), I ♥ AI (spaces and symbols), and the URL (eight tokens, without reciting its fragments). Keep every row on the canonical board. Unbelievable is already explained earlier; ChatGPT adds less new teaching here. This approval supersedes the original no-narration-cuts proposal above. The chart-label repair and 4px highlights remain in scope. No publication authorized.

The available recording supports the shorter sequence without new speech or a donor voice. Retain spoken example numbers 2, 4, and 5 because those still match the visible board. Source cuts, selected in quiet gaps: 3:29.50–3:36.17, 3:40.87–3:49.13, and 4:14.30–4:32.73. The last removes the URL fragment recital plus the redundant tokenizer recap, leading directly to the return-to-words explanation. Use 5ms anti-click ramps at the three joins; add no silence.

The examples board opens full and unmarked for three seconds, then uses the existing uniform complete-row zoom for basketball, spaces/symbols, and the URL. The omitted examples receive no narrated dive. Final examples-board span is 3:26.60–3:59.57 (32.97s); total candidate is 4:31.90. Zooms and pans remain inside these continuous counts. See ../tokens-repair-2026-09-27-v9/REVIEW.md for the finished-file verification and limitations.
