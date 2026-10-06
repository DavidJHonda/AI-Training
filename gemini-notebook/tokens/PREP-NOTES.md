# Tokens reroll preparation — October 4, 2026

Full-lesson reroll materials updated at David’s request after the [rebuilt-lesson video review](../../video-audit/tokens-rebuilt-lesson-review-2026-10-04/REVIEW.md). The current v11 and retained rolls do not supply the everyday-computing opening or complete unusual/unmatchable breakdowns; existing narration alone cannot complete the repair. The lesson page, Markdown, and upload sources follow the approved revised sequence. No new roll has been generated or installed.

## Generation handoff

Upload all six files in `gemini-notebook/tokens/upload/`: `tokens.md` and the five current JPGs. Paste `gemini-notebook/tokens/PROMPT.txt` into the video customization field separately. Do not upload these notes, the review, the prompt, old videos, or the retired Building Blocks board. None of the selected boards needs a human-face substitute; `post_only` is empty.

Save the new raw roll as `Prompts/tokens-reroll.mp4`, or the next unused `tokens-reroll-N.mp4`. Preserve the existing raw rolls and candidates as possible donors. The current course video remains v11 at `course-assets/tokens/tokens.mp4`, cache key `20260929ship1`; its timestamps are not a template for the new roll. Local preparation status does not update the Video Tracker.

## Teaching progression

Computers process numbers, including everyday text → the chat raises both conversion questions → numbering every whole word falls short → reusable chunks and concrete examples → vocabulary and token IDs → the written word cat versus its ID → the three Send steps → reply IDs become readable text.

## Boards and narration

Use four teaching boards plus the close: chat, What Tokens Look Like, You See a Word. AI Starts With a Number., What Happens When You Hit Send, close. The examples replace the separate Building Blocks board. The upload bundle contains six files: Markdown plus five JPGs. No faceless substitute or post-only board is needed.

The examples board has seven rows, showing chunks and token counts only. Numeric IDs and the tokenizer-attribution line are omitted from this board and its narration. Token IDs are introduced afterward; tokenizer provenance is retained only in these verification notes. Explain unbelievable, unusual, and unmatchable together to establish reuse; then basketball, spaces/symbols, and the web address’s eight-token count. Keep ChatGPT visible without a separate spoken walkthrough. Do not read the URL or its fragments. Speak numeric IDs only for unbelievable during Send and cat during its comparison. SP denotes a leading space, not literal inserted text.

The whole-word qualification and vocabulary definition follow the examples. Vocabulary construction and IDs precede the cat board. Omit model vocabulary sizes and the former training/chat sentence. Explain the return to readable text after Send and preserve the exact closing lines.

The Markdown separates the post-chat questions and vocabulary prose from the preceding boards’ Teaching content. Those headings are organizational, not spoken chapter titles. The everyday conversion sentence stands alone, and the prompt now requires it and both conversion questions verbatim, alongside the seven existing required passages. The new examples explicitly say two and three tokens. No lesson-page wording or board artwork changed during this preparation.

## Review the new roll

- Confirm the opening establishes ordinary computers processing numbers using email, texting, and phone use, then bridges to AI. Both conversion questions must follow the complete chat.
- Listen for all pieces of unbelievable, unusual, and unmatchable, their counts, and reuse of un. Merely naming the words or saying they share a prefix is incomplete. Check pronunciation directly; transcript matching alone is insufficient.
- Confirm the chunks-only examples precede vocabulary and IDs. Check supporting animations as well as boards for premature token IDs. Generic numbers in the opening or hypothetical whole-word scheme are appropriate; they must not be presented as already-explained token IDs.
- Name examples without row numbers. Keep ChatGPT visible without a spoken walkthrough; explain SP and eight URL tokens without reading URL fragments.
- Confirm the written word cat becomes ID 4719, rather than suggesting the pictured animal is tokenized. Then teach Send as the recap, with un = 359, belie = 32898, vable = 24694, followed by the readable reply and exact close.
- Check all nine required passages in spoken audio. Omit model vocabulary sizes, training/chat consistency, and tokenizer-source attribution from narration and supporting visuals. The current v11 already omits spoken model sizes but still contains some obsolete visuals and the training/chat sentence.

Evaluate complete teaching before visual polish under `scripts/video/NARRATION-REVIEW.md`. The review’s five-board highlighting and camera plan is provisional: measure new narration onsets, board spans, transitions, and pauses from the selected roll before proposing an edit. No new timed build plan or pause additions are authorized by this preparation.

## Verification

The new examples were checked with OpenAI tiktoken 0.14.0 using cl100k_base:

- unbelievable: un (359), belie (32898), vable (24694).
- unusual: un (359), usual (81324).
- unmatchable: un (359), match (6481), able (481).

The cat board title was updated using built-in imagegen; its artwork and teaching remain. The examples board is generated from the repository’s editable renderer. Page and upload copies must match byte for byte. Run the lesson-specific sync check before generating.

Review any new roll against this revised order. Previous video timestamps, crop plans, and board numbers are historical and do not apply to the new sequence.
