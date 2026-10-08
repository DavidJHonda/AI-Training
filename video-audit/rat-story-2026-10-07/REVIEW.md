# Rat Story companion video

Status: installed in the local lesson for review; not committed or published.

Approved scope: add an optional video after The Great Hanoi Rat Quiz, replace
archival photographs with matching original illustrations, soften the ending,
and connect the story to Unexpected Results. The existing lesson overview and
quiz remain intact. This is a supplementary story, not a standard overview edit.

Source: `Prompts/rat story.mp4`. Output:
`course-assets/unexpected-results/rat-story/rat-story.mp4` (4:28, 1280×720, 30 fps).
Source and output hashes are in `edit-manifest.json`.

## Visual edits

The source contains three archival-photo spans, including a Bettmann-marked
shot in addition to the two Getty-marked shots. All are fully replaced:

| Source/output frames | Seconds | Replacement | Camera |
| --- | --- | --- | --- |
| 264–482 | 8.800–16.100 | Original Hanoi street illustration | Centered 2% push |
| 1057–1234 | 35.233–41.167 | Original Hanoi street illustration | Centered 2% push |
| 4799–5019 | 159.967–167.333 | Original market illustration | Centered 2% push |
| 7656–8039 | 255.200–268.000 | AI connection text card | Full frame, no rings or zoom |

Illustrations were made with built-in image_gen. The two exact prompts and
style-reference provenance are saved beside the media in `generation-prompts.json`.
The text card is rendered by the build script with the course font. Other source
visuals and timings before the new ending remain unchanged.

## Narration treatment

Retained audio ends after: “Every mechanical gear of the plan functioned exactly
as designed.” The cut is at 255.200 seconds, inside the measured quiet interval
before the next sentence. The source's “ruthlessly optimize” and “weaponize”
passage and Notebook outro are removed. A 30 ms fade lies entirely in the quiet
tail. There are no other narration cuts or inserted pauses.

No recording of the proposed bridge in the original voice was available. The
bridge is therefore a 12.8-second **unvoiced** closing card, repeated as accessible
page text: “That’s why predicting AI’s effects takes more than understanding the
technology. We also have to watch what people do with it.” This adaptation was
reported in chat; do not describe the bridge as newly recorded narration.

## Verification

- Full decode passed; 8,040 frames, 30 fps, 268 seconds.
- Source/output decoded narration correlation through 255.1 seconds: 0.999928.
- Closing-card audio is silent. ASR timing and waveform inspection put the cut
  before the next word, preserving the complete final retained sentence.
- All seven declared visual boundaries passed `transition_guard.py`. Inspected
  the encoded first/last frames of each replacement and the literal final frame.
- Browser verified position after all quiz questions, desktop/390/320 px layout,
  poster-to-player behavior, video metadata/controls, and no JavaScript errors.
- JavaScript parsing and diff whitespace checks passed.
- End-to-end listening has **not** been performed. Waveform and ASR checks do not
  replace that review; the final audio still needs a listening pass before a
  release is described as fully reviewed.

Build: `.video-venv/bin/python scripts/video/build_rat_story_companion.py`.
See `edit-manifest.json`, `qa.json`, and `transitions/transition-guard.json` for
machine-readable evidence. No overview, PDF, or deployment was changed.
