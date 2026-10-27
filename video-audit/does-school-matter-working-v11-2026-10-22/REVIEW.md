# Does School Matter? — working v11

Built 2026-10-22 on the owner's approval of the review's proposed edits and short ending pickup. Review candidate only; the installed lesson, video, and asset files are unchanged.

## Result

`Prompts/does-school-matter-v11.mp4`: 2:07.800, 3,834 frames, 30 fps, 1280 × 720. The video preserves the opening argument, replaces the four-card board with the current Knowledge-and-Skills board, retains those two explanations, and places the people-skills sentence within Skills. The four-pillar introduction, AI Fluency passage, “Finally” introduction, four-pillar recap, and obsolete closing are removed.

It intentionally ends after “helping a team turn ideas into action.” The new board takeaway and current closing are pending the approved short reroll. This is ready for working-cut review, not shipping.

## Sources and exact edit

Stable source: `Prompts/does-school-matter-v10.mp4`, SHA-256 `646b062e8b2f59d62a241e47f606c6765f1f71a698cc49d6e205b129e93d41a9`. This is the same file as the installed video at review time. The pristine raw generation is unavailable, so this is one additional encode from the finished v10.

The manifest records source, asset and protected-file hashes, candidate hash, geometry, boundaries, and scope. All frame ranges below are half-open at 30 fps.

| Source frames | Output frames | Treatment |
| --- | --- | --- |
| 0–3028 | 0–3028 | Retain through the sentence ending “smarter than the tool,” including its tail and natural gap. Replace the old board from its first source frame, 3013. |
| 3230–3820 | 3028–3618 | Retain “First is deep subject knowledge” through “work you are proud of.” |
| 4202–4418 | 3618–3834 | Retain “Focus on listening” through “ideas into action,” including its complete tail. |

Both joins are in measured silence. Five-millisecond audio edge ramps occur within those gaps; no new pauses or gain changes were introduced. Encoded speech gaps are 0.383 seconds at 1:40.780–1:41.164 and 0.360 seconds at 2:00.377–2:00.737. The video cuts occur at 1:40.933 and 2:00.600 respectively.

## Board treatment

| Board | Highlighting | Camera | On screen / breaks |
| --- | --- | --- | --- |
| What School Helps You Build | Complete Knowledge card in purple, then complete Skills card in blue, continuing through the people-skills passage. Unmarked opening and final tail. Fixed four-pixel outlines. | Compact; full view throughout. Canonical 1600 × 876 JPG centered on a 1600 × 900 white canvas, scaled to 1280 × 720. | Begins at 1:40.433. Existing microscope cutaway at 1:45.267–1:49.367, model-building cutaway at 1:57.200–1:59.867, teamwork cutaway at 2:02.533–2:06.833. Longest continuous board run: 7.833 seconds. |

The board has no retained introductory sentence, so the first item begins within two seconds. It opens complete and unmarked; the Knowledge ring starts at the spoken item's onset (1:41.167), using the Edit Spec's no-introduction exception. No zoom or extra pause is introduced. All useful existing cutaway motion is preserved. Their original positions within each retained passage are unchanged.

## Checks

- Decoded all 3,834 encoded frames; exact planned frame count, continuous presentation timestamps, 30 fps.
- Compared every encoded frame against its retained source frame or replacement board state. Maximum mean absolute pixel error: 2.852/255, consistent with the expected encode.
- All nine declared board/cutaway/edit boundaries passed `transition_guard.py`; the boundary strips were visually inspected. No obsolete-board flash appears in these transitions.
- Inspected full-resolution encoded Knowledge and Skills ring states and the full-board canvas. Complete cards, readable text, correct accent colors, and unclipped fixed-width outlines.
- Encoded audio correlation against the edited PCM: 0.999989. Both cut gaps measured in the encoded output.
- Read the complete fresh small.en transcript of this exact candidate. It retains the intended narration and omits the removed categories, four-pillar framing, and old ending.
- Protected installed video, source candidate, lesson Markdown, index, current board, and current closing hashes remain unchanged.
- Review page opened successfully in the in-app browser.

No independent direct audio audition or end-to-end playback review was performed. Please listen to the cuts around 1:41 and 2:01. The pending reroll will also need a voice-continuity check when grafted. Technical checks and transcription do not certify audible joins.

## Ending pickup

Prepared kit: `gemini-notebook/does-school-matter/ending-2026-10-22/`.

Upload the Markdown and exact current closing JPG from its `upload/` folder. Paste `PROMPT.txt` into the video customization field. The prompt is 357 words, uses the four required blocks, and requests only:

> School is where you get to build what you bring to the work.
>
> The opportunity to learn is already in front of you.
>
> Choose something you want to get better at. Start there.

The board is deliberately omitted from this tiny generation to avoid re-narrating its cards. Its canonical image will carry the first line in the final edit. The full lesson and standard kit registry were not altered.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_does_school_matter_working_v11.py` (refuses to overwrite the candidate).

QA: `.video-venv/bin/python scripts/video/qa_does_school_matter_working_v11.py`.

Transcript: `.video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/does-school-matter-v11.mp4 --output-dir video-audit/does-school-matter-working-v11-2026-10-22/transcripts --model small.en`.

No installation, commit, push, or deployment was requested or performed.
