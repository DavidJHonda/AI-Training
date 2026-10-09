# AI is Different: reroll preparation

Prepared October 9, 2026 from the current lesson page and its three boards.
Status: source materials prepared; no new video generated or installed.

## Lesson progression

Start with why a password needs an exact rule, introduce the messy playlist that
cannot be handled by anticipating every scribble, and explain how learned patterns
provide flexibility while making responses less predictable.

| Beat | Teaching and transition | Visual source |
| --- | --- | --- |
| Spotify password | Answer the opening questions immediately. Connect matching the password to written instructions, calculators, and spreadsheet formulas. Walk both outcomes in the flowchart. | Password-rule board |
| Handwritten playlist | Cross-outs, arrows, abbreviations, and jokes create an interpretation problem. A separate instruction for every mark is impractical. | Drawn playlist notes |
| Learned patterns | Training provides patterns that help interpret the notes. AI is still software; people write its code without writing each answer. | Supporting drawing |
| Cooking analogy | Compare following specified recipe steps with using learned relationships. Teach both cards and their bottom lines. | Cooking comparison |
| Structured and unstructured data | Define consistent fields through GPA rows and columns. Contrast a college photo with signs and clues for identifying dorms. | Spreadsheet and campus drawings |
| Downside | Connect flexibility to harder prediction and inspection. Return to the crossed-out song and wrong dorm name. | Reuse the playlist and campus examples |
| Closing | “Different jobs need different tools.” Then “Choose the tool that fits the work.” | Current closing board |

## Upload handling

Upload all four files in `upload/`: the Markdown, password board, text-only cooking
board, and current closing board. Paste `PROMPT.txt` into the customization field;
do not upload the prompt or these notes. The generated `README.txt` gives the exact
list and raw-roll save path. Never overwrite an existing roll.

The cooking illustration includes a robot face. Under the shared preparation rule,
its upload variant omits both artwork panels but preserves the 1600×920 canvas,
title, card text, takeaway lines, and text positions. The full illustrated canonical
board replaces it in the edit. Rebuild the upload variant with:

```sh
node scripts/video/render_ai_is_different_cooking.cjs --upload-variant
```

The password and closing boards are uploaded directly. The older Rules vs. Patterns,
Structured vs. Unstructured Data, and Kryptonite upload variants are historical
assets, excluded from the active registry and upload folder. They are not sources
for this reroll.

## Narration review priorities

- Preserve the approved page wording and sequence, especially the playlist story
  before the cooking analogy and the explicit statement that AI is still software.
- Include both password outcomes, all cooking-card teaching, both data definitions,
  the visible-signs explanation, both mistake examples, and the current closing.
- Verify the seven required sentences in the prompt at their lesson positions.
- Do not restore next-word mechanics, PS5 recommendations, receipt or legal-pad
  examples, Superman/Kryptonite, scams, deepfakes, or guardrail explanations.
- Keep the analogy from becoming a claim that AI has no code or always gives
  different answers. Do not promise that every campus photo identifies a building.
- The LAB and Group Exercise remain on the page and are not narrated.
- Judge teaching coverage before runtime. Perform listening and visual review of
  the generated roll; source checks alone do not evaluate a future video.

## Source maintenance

The live page remains the content authority. `lessons/ai-is-different.md` is the
narration source: it retains the lesson teaching, with spoken board content and
standalone required lines, and ends at the closing. The on-page LAB and Group
Exercise are unchanged by preparation.

After source changes, run:

```sh
.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson ai-is-different
.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson ai-is-different --check
```

The installed September 29 video is still the previous lesson version. This prep
does not change the MP4, its lesson reference, or its displayed runtime.
