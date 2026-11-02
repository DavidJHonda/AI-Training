# AI is Different: reroll preparation

Updated November 2, 2026 from the current lesson page and its four boards.
Status: source materials prepared; no new video generated or installed.

## Lesson progression

Start with the approved introductory framing, teach written rules and learned
patterns through the password and cooking analogy, then compare the same playlist
in structured and unstructured formats.

| Beat | Teaching and transition | Visual source |
| --- | --- | --- |
| Introduction | Two differences: learned patterns and flexible handling of unstructured data. | Lesson introduction |
| Spotify password | Matching the password requires written instructions. Walk both outcomes. | Password-rule board |
| Rules vs. Patterns | AI learns from examples and uses patterns to answer you; people still write its code. | Short lesson paragraph |
| Cooking analogy | Compare recipe steps with learned relationships. | Cooking comparison |
| Structured and unstructured data | Traditional Software appears above Structured Data on the left; AI appears above Unstructured Data on the right. The same three songs appear in table fields and handwritten notes. Surrounding prose introduces the formats and explains the patterns learned during training. | Same Playlist. Different Formats. |
| Downside | AI can miss a crossed-out song. Check its interpretation. | Playlist board |
| Closing | “Different jobs need different tools.” Then “Choose the tool that fits the work.” | Current closing board |

## Upload handling

Upload all five files in `upload/`: the Markdown, password board, text-only cooking
board, playlist comparison, and current closing board. Paste `PROMPT.txt` into the customization field;
do not upload the prompt or these notes. The generated `README.txt` gives the exact
list and raw-roll save path. Never overwrite an existing roll.

The cooking illustration includes a robot face. Under the shared preparation rule,
its upload variant omits both artwork panels but preserves the 1600×920 canvas,
title, card text, takeaway lines, and text positions. The full illustrated canonical
board replaces it in the edit. Rebuild the upload variant with:

```sh
node scripts/video/render_ai_is_different_cooking.cjs --upload-variant
```

The password, new playlist comparison, and closing boards are uploaded directly.
The playlist board is byte-identical on the page and in preparation. Its renderer
is `scripts/video/render_ai_is_different_playlist.cjs`; its ImageGen source and
exact prompt are in `scripts/video/assets/ai-is-different/playlist/`. The older Rules vs. Patterns,
Structured vs. Unstructured Data, and Kryptonite upload variants are historical
assets, excluded from the active registry and upload folder. They are not sources
for this reroll.

## Narration review priorities

- Preserve the approved page wording and sequence: Rules vs. Patterns and cooking
  come before the playlist comparison.
- Include both password outcomes, all cooking-card teaching, both data definitions,
  the playlist interpretation and learned-pattern explanation, the downside, and closing.
- Verify the required sentences in the prompt at their lesson positions.
- Do not restore GPA, campus photos, next-word mechanics, PS5 recommendations,
  receipt or legal-pad examples, Superman/Kryptonite, scams, deepfakes, or guardrails.
- Do not imply AI has no code or always gives different answers.
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
