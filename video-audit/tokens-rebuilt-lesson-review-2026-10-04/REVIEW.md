# Tokens: repair or reroll after the lesson rebuild

LESSON: tokens

CANDIDATE: `course-assets/tokens/tokens.mp4`, identical to `Prompts/tokens-v11.mp4`, 3:31.23 / 6,337 frames / 30 fps. Page cache key: `20260929ship1`.

VERDICT: **REROLL for the rebuilt lesson.** Editing can recover much of the existing teaching, but the checked source inventory does not supply the new everyday-computing opening or the complete unusual/unmatchable examples. A repair using existing narration alone is incomplete. Recommend a fresh full lesson roll as the new narration base, retaining existing rolls as possible donors.

This is a content and repair-feasibility decision, not a completed audiovisual QA pass. The complete timestamped transcript and every-four-second visual samples were reviewed. Direct audio listening, continuous end-to-end playback, and contextual donor-join audition were not performed. No source video, lesson, or generation prompt was changed by this review; no generation was started.

## Verified sources

- Read the current `TokenSection` in `index.html`, `lessons/tokens.md`, and current `gemini-notebook/tokens/PROMPT.txt`.
- Current file SHA-256: `cd3083318c7f5c2e2f987013d1ea60fb1b9b971fe67fb5ee6f292b05f9fcb0a5`, matching the locally shipped v11 record and retained v11 candidate.
- Reused the complete `video-audit/tokens-build-2026-09-29-v10/final-transcript/tokens-v10b.txt`. Fresh extraction confirms the current file, v10c, and the transcribed second render have identical copied AAC payloads: `95459a38cfabf75f811c7dfc167872571267381d50395a5567984229f8cdfa9c`.
- Checked complete September 29 transcripts for `Prompts/tokens-1.mp4`, `tokens-2.mp4`, and `tokens-3.mp4`; all three video hashes match that comparison's source inventory.
- Checked the actual edited v9 transcript at `video-audit/tokens-repair-2026-09-27-v9/audio-check/edited.txt`; the retained `Prompts/tokens-v9.mp4` matches its historical live hash. The older September 16 and September 22 transcript records likewise supply no everyday email/phone explanation or complete new word splits. Those historical records are not claimed as newly auditioned donors.
- Fresh evidence: `sources.json`, five full-length contact sheets in `sheets/`, and frames at 0:57–0:59 in `early-ids/`.
- The current six-file generation bundle passes the lesson-specific sync check.

## Teaching points in the rebuilt lesson's order

Times below refer to current v11. Quotes are transcript-derived, not direct-listening claims.

| Teaching point | Coverage | Current evidence and implication |
|---|---|---|
| Computers process numbers; everyday email, texting, and phone text are represented as numbers | MISSING as the new foundation | 0:00–0:07.90 opens “Math is the magic that powers AI” and says AI operates using numbers. It does not establish the everyday-computing concept the user restored. |
| Full Avengers chat exchange | RICH | 0:08.68–0:25.88 contains the question, Endgame explanation, Infinity War alternative, and words-in/words-out observation. |
| Ask both conversion questions at the opening | THIN | 0:26.52–0:29.42 asks how input words become numbers. The second question is not raised here, although the answer-to-text process is taught later. |
| Whole-word numbering and why it fails | RICH | 0:29.42–0:52.42 covers every language, new words/names/slang, typos, emojis/code, and the million-word limitation. |
| Reusable chunks called tokens; building-block analogy | TAUGHT | 0:53.44–1:01.42 teaches reusable pieces and building blocks. The approved new literal wording is absent, but the concept is present. |
| Unbelievable becomes un / belie / vable | TAUGHT, with pronunciation unverified | 1:08.84–1:15 approximately. Base ASR collapses the spoken chunks into a word; the retained contextual medium-English alignment separates three chunks around 1:13.62–1:15.83. Do not infer correct pronunciation from ASR alone. |
| Unusual becomes un / usual; unmatchable becomes un / match / able | MISSING complete breakdowns | 1:19.88–1:23.32 says “The piece un starts unbelievable, unmatchable, and unusual.” This explains their shared prefix, but never names the remaining chunks of the two new examples. |
| Reuse across words | RICH | 1:15.46–1:31.70 explains reuse and avoiding a new vocabulary entry for every new word. |
| Basketball → basket / ball, two tokens | TAUGHT | 2:34.80–2:38.92. The spoken “example two” is stale: this is now row 4. |
| I ♥ AI; leading spaces; three tokens | RICH | 2:39.76–2:56.08 explains the actual pieces, SP, and spaces attached to following chunks. Spoken “example four” is now row 6. |
| Web address: eight tokens, without reading fragments | TAUGHT | 2:56.84–3:03.98. Spoken “example five” is now row 7. |
| Whole words or parts, then vocabulary definition after examples | TAUGHT, misplaced | 1:02.20–1:07.68 teaches both before the examples; move them after the new examples block. |
| Engineers/program analyze text to build vocabulary | TAUGHT | 1:32.66–1:39.92. Existing wording includes engineers deciding the split rules. |
| Each chunk gets a token ID; an identifier rather than meaning | TAUGHT | 1:40.96–1:47.14 names IDs and their address role. The cat explanation at 2:16.62–2:31.18 supplies the meaning distinction. |
| Read cat versus start with ID 4719 | RICH | 2:16.62–2:31.18 explicitly says “the word cat,” supplies the correct ID, and distinguishes ID from meaning. The old visual title needs replacement. |
| Hit Send: text → chunks → ID lookup, with correct worked IDs | RICH, misplaced | 1:51.52–2:14.12 supplies all three steps, 359 / 32898 / 24694, and the summary. It should now follow cat as the final process recap. |
| Reply IDs convert to text pieces and join into readable words | RICH | 3:04.78–3:20.20. This is worth preserving as donor material. |
| Exact two-line close | TAUGHT / MET | 3:21.00–3:25.02 contains both current closing lines. |

## Hard requirements and removed content

- “Computers only process numbers.” — MISSED.
- New “Instead, AI uses reusable chunks of text called tokens…” wording — MISSED verbatim; concept taught.
- Combined whole-word/vocabulary passage — MISSED as an exact combined passage; both concepts taught separately at 1:02–1:08. These wording differences alone are not the reason for recommending a reroll.
- “A token ID identifies the token. Meaning comes later.” — MET at 2:28.10–2:31.18.
- “Tokenization turns text into token IDs the model can use.” — MET at 2:11.00–2:14.12.
- Both closing lines — MET at 3:21.00–3:25.02.
- The model-size narration was already cut in v10 and is absent from v11. Do not propose cutting an aside that is no longer present.
- The removed training/chat sentence remains at 1:48.00–1:51.52 and would need a cut.
- The examples board still prints numeric IDs and the tokenizer source line. Both are intentionally absent from the rebuilt board.
- The supporting drawing at 0:58 also shows numeric token IDs before their introduction, plus a vocabulary-size label. Replacing only the later examples board would leave this earlier violation of the new progression.

ERRORS: No new spoken numerical error established in v11. The 2/4/5 example references are incorrect against the rebuilt 4/6/7 row numbering. Token-piece pronunciation remains unverified.

SOURCE_QA: PASS for this editorial comparison; no material inconsistency found between the rebuilt page, Markdown, and current bundle. This is not a fresh technical fact audit.

ADDITIONS: The reusable-vocabulary explanation is useful but must not pull the definition ahead of the examples again. Training/chat consistency is deliberately removed by the owner. Existing incidental vocabulary-size graphics are also unnecessary.

## Existing-donor feasibility

The current video is already a hybrid of roll 1, roll 2, and v9. Multiple candidate filenames therefore do not imply independent narration coverage.

| Missing or changed beat | Checked donor evidence | Feasibility |
|---|---|---|
| Everyday-computing foundation before AI | Roll 3, 0:25.08–0:27.58: “Behind the screen, the model can only process numbers.” Roll 1/2 and v9 use the math/AI premise. Earlier September 16 transcript says “It runs on math. It only processes numbers.” | Closest lines remain AI-specific. None supplies the email/text/phone explanation or the intended bridge from ordinary computers to AI. No complete donor. |
| New unusual/unmatchable breakdowns | Roll 1, 1:19.70–1:23.16; roll 2, 1:17.00–1:20.98; roll 3, 1:13.18–1:21.22; v9, 1:37.44–1:48.52 all explain shared un/reuse. | None actually narrates un + usual or un + match + able. No complete donor. |
| Move examples before vocabulary, then cat before Send | Existing current spans listed above | Structurally editable, but still requires new missing narration and coherent new joins. Not a complete repair by itself. |
| Stale numbered example references | Roll 1 has unnumbered basketball at 3:02.56–3:06.24 and URL count at 3:25.80–3:28.72. Its spaces passage is less explicit than current v11. | Potential donors for two individual references; no joins auditioned. Could alternatively cut introductory number phrases if cadence permits. This is extra repair work, not a verified assembled solution. |
| The input/output question pair | v9 has a later output question at 3:59.62–4:05.26 | Conceptually available as a separate donor; moving it into the opening needs reference/cadence review. It does not solve the missing everyday-computing foundation. |

REPAIR PLAN: No complete existing-audio-only plan. Generating a short supplemental roll for the missing material is technically an option, but it would still leave substantial reordering, row-reference repairs, new board replacement, and multiple unauditioned joins. A new full lesson roll is the recommended base; old rolls remain optional donors for omissions or stronger explanations after comparison.

## Provisional production plan after a new roll

This is not a build authorization or timed edit plan. Narration onsets, scene cuts, active spans, existing pauses, and target gaps must be measured from the new selected roll before editing. No added pauses are proposed now.

| Board | Proposed highlighting | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| You Use Words. AI Uses Numbers. | Question bubble, then answer bubble | Full board; no chat dive | New-roll timings pending; board accompanies the complete exchange | Preserve the familiar chat illustration. |
| What Tokens Look Like | First three complete rows in order; shared un comparison when spoken; then basketball, symbols, URL row | Full unmarked establishing view; complete-row zoom/pan if needed for readability | New-roll timings pending; definition follows the examples | Use current chunks-only board. Do not narrate ChatGPT or URL fragments, display IDs, or restore a tokenizer-source explanation. |
| You See a Word. AI Starts With a Number. | Human card, AI card, then takeaway | Full view if legible; preserve complete cards | After vocabulary and IDs; new-roll timings pending | Use the current title and keep the written-word-versus-number distinction explicit. |
| What Happens When You Hit Send | Three complete columns in order, then summary | Full board; outlines span complete columns in their shared white stage | Final teaching board, after cat; new-roll timings pending | It is now the process recap. Return-to-text narration follows. |
| Words become numbers. | Standard close treatment | Canonical close motion | Literal final image; new-roll cadence/tail pending | Preserve both closing lines. |

Potential supporting-scene donors, subject to real-time motion/listening review:

- Current v11 around 0:26–0:53: whole-word lookup and unfamiliar-input failure. Teaching purpose still fits; numeric labels belong to the explicitly hypothetical approach. Do not assume animation quality from the sampled frames.
- Around 1:36–1:40: text-corpus/vocabulary construction. The “Pre-Training: Industrial Corpus Analysis” label is unnecessarily technical and would need treatment if retained.
- Around 3:05–3:20: IDs returning to chunks and a word. Teaching purpose remains useful; audition and inspect movement before choosing it.
- The old Building Blocks board at roughly 0:59–1:15 and brief return near 1:24 is superseded by the current examples board. Its replacement is a content decision, not a reason to discard good narration elsewhere.

## New generation requirements

Use the current six-file upload folder and prompt. The new roll must carry the ordinary-computing opening, both chat-conversion questions, whole-word limitation, chunks-only examples including both new breakdowns, vocabulary/IDs after those examples, cat, Send, readable reply, and exact close. Avoid the removed model-size aside, training/chat aside, tokenizer-name attribution, old row numbers, and premature IDs in supporting drawings.

LISTENING: None performed directly. All verbal findings above are based on matched full transcripts and documented contextual ASR. The content gaps support the reroll decision independently of splice-quality uncertainty. Continuous playback, pronunciation, pacing, and any proposed donor joins still require listening review.
