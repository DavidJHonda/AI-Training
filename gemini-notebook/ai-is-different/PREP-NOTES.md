# AI is Different: reroll preparation

Updated November 2, 2026 from the current lesson page and its four boards.
Status: complete reroll materials prepared and validated; generation has not started.

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
| Data setup | Traditional software usually expects a specific structure; AI can help interpret information without organizing it first. Preserve the qualifiers. | Lesson body before the playlist board |
| Same playlist comparison | Traditional Software / Structured Data is on the left; AI / Unstructured Data is on the right. Read the songs, artists, and order. Explain the first/last arrows and why the crossed-out Shake It Off is excluded. | Same Playlist. Different Formats., final version without bottom captions |
| Why AI can interpret the notes | Training supplied patterns in handwriting, language, arrows, and crossed-out words. Keep this explanation after the comparison. | Supporting drawing or the notes |
| Downside | Learned patterns make responses harder to predict and inspect; AI can miss a crossed-out song. | Playlist example |
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
exact prompt are in `scripts/video/assets/ai-is-different/playlist/`. The final board
is 1600×747, with software labels above the data labels and no bottom captions.
The older Rules vs. Patterns,
Structured vs. Unstructured Data, and Kryptonite upload variants are historical
assets, excluded from the active registry and upload folder. They are not sources
for this reroll.

## Narration review priorities

- Preserve the approved page wording and sequence: Rules vs. Patterns and cooking
  come before the playlist comparison.
- Include both password outcomes, all cooking-card teaching, both data definitions,
  the playlist interpretation and learned-pattern explanation, the downside, and closing.
- Verify the required sentences in the prompt at their lesson positions.
- Explain the playlist comparison aloud. Merely displaying the new board is not
  enough. Match its three song/artist pairs, first/last annotations, and exclusion.
- Keep the introduction as orientation and develop the two differences in order.
  Keep the training explanation after the board rather than repeating it before.
- Preserve “usually” and “can help.” AI can also use structured data; do not turn
  the comparison into a claim that it requires unstructured input.
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

## Existing video and reuse

The installed video is the October 9 v15 edit, 230.53 seconds (about 3:51), served
with cache key `20261009ship1`. Its SHA-256 is
`8ed63f95cf3bd166103544c01489d6f238e2ad14b3c55e0726096b51c3a14444`.
It is byte-identical to `Prompts/ai-is-different-v15.mp4`.

The November 2 comparison recommends a complete reroll: the existing video lacks
the new introductory framing, puts the playlist before cooking, and teaches data
through the retired GPA and campus-photo examples. The six original roll
transcripts contain no walkthrough of the new same-playlist board. Existing
narration about learned patterns remains useful but cannot supply that comparison.

Potential editing donors, subject to review with the new narration:

| Current-video range | Reusable material |
| --- | --- |
| 0:00–0:54 | Password setup and rule-flowchart treatment |
| 0:59–1:46 | Handwritten-playlist visuals and learned-pattern explanation |
| 1:57–2:45 | Cooking analogy and supporting kitchen imagery |
| 3:47–3:50 | Exact closing lines and canonical closing board |

This is a source-reuse inventory, not a verified splice plan. The previous review
used complete transcripts, matching encoded-audio hashes, and sampled frames;
no end-to-end listening or motion review was performed. Judge the returned roll's
complete narration first, then review any donor motion and audio joins in context.

Save the new raw roll as `Prompts/ai-is-different-reroll.mp4`, currently unused;
if it becomes occupied, choose the next unused `-reroll-N` name. Preparation does
not alter the installed MP4, its reference, or its displayed runtime.
