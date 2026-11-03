# Big Upside: reroll preparation

Prepared November 3, 2026 for the finalized four-example lesson. V12 is now installed locally at `course-assets/big-upside/big-upside.mp4?v=20261103ship12` (3:32.500), committed as `50784bfb`, and awaiting the authorized batch push. It combines roll 1 narration with the complete roll 3 testing caveat, roll 2 supporting scenes, current boards, and the approved menu donor. See `video-audit/big-upside-build-2026-11-03-v12/REVIEW.md` for checks and listening limitations. The generation instructions below remain available for future rerolls.

## Generate

Upload all six files in `upload/`: `big-upside.md` and the five canonical JPGs. Paste `PROMPT.txt` into the video customization box. Do not upload these notes, the prompt, README, manifests, earlier lesson text, or old boards.

Save the raw result as `Prompts/big-upside-reroll.mp4`, unused at preparation time. If occupied, use the next unused `-reroll-N.mp4` name. Preserve all existing videos and candidates.

## Lesson progression

AI’s present-day value becomes concrete through four benefits: a starting point for science, support for doctors, access to everyday information, and time to prepare for floods.

1. Open with the giant calculator and benefits already happening.
2. Explain proteins’ jobs and how shape affects function. Put the sentence about understanding disease and finding medicines **before** “Figuring out their shapes…” Then introduce AlphaFold and the scale comparison: about 200,000 structures determined through experiments versus over 200 million predictions shared free. Explain that predictions still require research and testing. Do not restore “AlphaFold gives them a head start on that work.”
3. Teach cancer detection: difficult-to-spot signs in breast scans, the Swedish trial of over 100,000 women, AI flagging patterns, and doctors retaining review and care decisions.
4. Teach everyday access: menus, food labels, and signs can be difficult to access for someone who is blind; a phone camera and AI can read text aloud and describe photos.
5. Teach flood warnings: time matters; AI helps provide free warnings even where river-measuring equipment is absent; warnings days ahead give people time to prepare and move to safety. The opening two sentences are one paragraph in the lesson.
6. Bring together the four human benefits. Say “These are making a difference in people's lives.” Go directly to the two closing lines: “The big upside is happening today.” and “AI is already accelerating work that protects and improves lives.” Nothing afterward.

Do not reintroduce Demis Hassabis, the Nobel acknowledgment, biography, timeline, user counts, or the deleted “So the next time…” / “For starters…” ending. Cover the board teaching once; do not repeat the same explanation as a separate caption read.

## Boards and editing handoff

| Order | Canonical board | Treatment |
| --- | --- | --- |
| 1 | `big-upside-protein.jpg` | A New Scale for Science; purple; label reads “AlphaFold AI.” |
| 2 | `big-upside-cancer.jpg` | Helping Doctors Find Cancer; amber; abstract grayscale scan. |
| 3 | `big-upside-reading.jpg` | Reading Everyday Information; teal. |
| 4 | `big-upside-flood.jpg` | Earlier Flood Warnings; blue. |
| 5 | `big-upside-close.jpg` | Standard two-line closing message. |

All four teaching boards share the 1600×662 illustration-left/two-points-right layout. Use the established polished dimensional object style. The cancer illustration has no recognizable anatomy and is conceptual, not patient evidence. None of the upload boards has visible faces; no faceless variants or post-only stand-ins are needed. Canonical images and upload copies are identical.

Review the new narration against the current Markdown first. Check the eight required verbatim passages, the why-before-AlphaFold sequence, experimental versus predicted structures, all four examples, human medical decisions, and the clean ending. Then measure fresh board timings and plan the visual edit; old biography and combined-example board timings do not fit this lesson. Preserve useful generated scenes and apply the shared editing rules to canonical replacements, highlights, and watermark removal.

## On-page lab, excluded from video narration

The current lab is **Find One More Upside**, replacing Explore a Protein Shape. Its five steps are Open ChatGPT, Start a new chat, Pick something you care about, Find a real example, and Check the source. The interest field fills the copyable prompt automatically. It has no excluded topics and no “Name the benefit” step. These instructions stay on the course page; the video and upload Markdown end with the closing message.

## Preparation checks

`PROMPT.txt` has the four required blocks and 451 words. Its eight required passages appear on standalone lines in the narration source, in lesson order. Source teaching matches the current page and boards. Run `scripts/video/sync_gemini_notebook.py --lesson big-upside --check` before generation. The source record is `docs/research/big-upside-four-benefits-sources.md`; do not upload it.
