# Be Curious reroll preparation

Updated November 4, 2026. Preparation only; no new video has been generated, installed, or published. The previous Curious & Flexible video remains on disk and is disabled in the lesson. The stable `curious-and-flexible` source and registry paths now describe the lesson titled **Be Curious**.

## Lesson arc

A familiar basketball play stops working, prompting curiosity; the same habit supports learning throughout life, and four practical benefits lead into four ways to stay curious as AI changes.

1. The basketball captain's play worked all season until another team learned to stop it.
2. Say “Before you find a better play, you need to be curious.” **before** the three questions about opponents, openings, and watching the play again.
3. Curiosity reaches beyond basketball. Taking an interest, asking questions, and exploring possibilities supports lifelong learning. There is always more to discover.
4. **Why Be Curious:** teach It’s Your Armor, It Kills Boredom, It Helps You Grow, and Learn as You Live, with every question and instruction from the current board.
5. **As AI Changes:** models, tools, and ways of working keep appearing. You do not need to chase every feature; pay attention to changes that could matter to you.
6. **Be AI Curious:** teach Use AI Regularly, Check What Changed, Follow One Reliable Source, and Compare with Others, with all examples and qualifiers.
7. Close with “Curiosity keeps you growing.” followed by “Keep asking questions. Keep learning as you live.” End there.

The first board explains why curiosity matters throughout life. The second applies that habit to AI. Neither is a recap of the other. The prose bridges stay outside the board teaching sections. The boards are four parallel cards, read left to right across the top row, then the bottom row; there are no process arrows or causal diagrams to invent.

## Current wording and source handling

Authority: `BeCuriousSection` and `CLOSE_BOARDS.becurious` in `index.html`, plus the three current canonical JPGs. `lessons/curious-and-flexible.md` is the narration source. It preserves the revised opening order, “Curiosity reaches far beyond basketball,” “try to change what you think,” the shortened benefit copy, current board titles, merged AI transition, and new close.

The narration source ends at the closing message. The Follow Your Curiosity lab, including its new Open ChatGPT first step, remains in the live page and is deliberately excluded from the upload text. No page copy or interaction changes are part of this preparation. Do not restore the deleted assignment sentence, the simple-habits transition, the Be Flexible board, any flexibility teaching, or “Stay curious.” as the closing message.

Four short quotations are required verbatim in the prompt and occur as standalone lines in the source, allowing for Markdown emphasis. The remaining teaching should retain the source's language, full meaning, questions, and qualifiers. “Why be curious?” and “Be AI curious.” are brief spoken versions of the board titles. The basketball and other curiosity questions model inquiry; they are not quizzes. Preserve them without inventing answers or asking the viewer to pause. This follows the approved lesson instead of the general preparation guide's immediate-answer convention.

Do not imply that curious people are immune to manipulation, that students must choose a career now, or that keeping up with AI requires constant monitoring or many sources.

## Upload handling

Upload only the four files in `upload/`:

- `curious-and-flexible.md`
- `be-curious-why-faceless.jpg`
- `be-curious-ai-faceless.jpg`
- `curious-and-flexible-close.jpg`

Paste `PROMPT.txt` into the video customization field. Do not upload it, these notes, the README, or the asset manifest.

The two teaching boards show photographic people with visible faces. Under the preparation guide, their upload versions are text-only layouts with the same titles, card copy, colors, order, and canvas dimensions. They are rendered from the current board definitions by `scripts/video/prepare_be_curious_reroll.py`. The source manifest records their hashes and the canonical board hashes. No photographic asset is edited by this renderer.

In the finished edit, replace the upload versions with the current canonical Dallas Stars boards:

- Why Be Curious: `course-assets/curious-and-flexible/curious-and-flexible-stay-curious.jpg` (1600 × 1461).
- Be AI Curious: `course-assets/curious-and-flexible/be-curious-ai-habits.jpg` (1600 × 1379).
- Close: `course-assets/curious-and-flexible/curious-and-flexible-close.jpg` (1656 × 597), uploaded directly.

The prompt's restriction on photographic imagery applies to Notebook-generated scenes. It does not replace the approved photographic boards used in the final edit. Use relevant drawn scenes around the prose; assess their teaching value during the later narration and visual review. Do not infer a footage selection or approved edit from this preparation.

## Generation and review handoff

Save the next raw roll as `Prompts/be-curious-reroll.mp4`, or the next unused numbered reroll name. Preserve existing raw rolls and the previous video. Review the complete timestamped narration against the source before selecting a base or planning cuts, highlights, and pauses.

Rebuild and check the bundle with:

```sh
.video-venv/bin/python3 scripts/video/prepare_be_curious_reroll.py
.video-venv/bin/python3 scripts/video/sync_gemini_notebook.py --lesson curious-and-flexible
.video-venv/bin/python3 scripts/video/sync_gemini_notebook.py --lesson curious-and-flexible --check
```

The prompt contains 478 words and the four required blocks. Verify the four verbatim lines, complete eight-card teaching, upload filenames and dimensions, source hashes, and exclusion of the lab before generation. Sync verifies the assembled bundle; it does not certify narration from a video that has not yet been generated.
