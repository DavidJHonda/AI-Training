# Vector Space video preparation

Updated October 6, 2026 after reviewing raw versions 4, 5, and 6. This revision prepares the next roll; it does not generate narration, render a video, or publish anything. The installed video and all existing rolls are preserved.

## Teaching progression

A token’s updated numbers need not exactly match another token’s starting numbers → city coordinates show how distance still finds a match → seven drink ratings extend that reasoning beyond two dimensions → the same idea connects high-dimensional positions to meaning → the restored IT/CAT illustration shows context changing a position.

The current page in `index.html` is the teaching authority. `lessons/vector-space.md` is now a spoken source, replacing its former activity implementation notes. It preserves the approved opening, current coordinates, all five drink vectors, both mystery answers, revised distance paragraph, position/meaning callback, restored illustration, and closing lines. Spoken “Let’s add” language adapts the approved activities for video. No course page prose was changed during preparation.

## What to use

- Upload all nine files in `upload/`: the narration Markdown, six map reference JPGs, the canonical context illustration, and the canonical close.
- Paste `PROMPT.txt` into the video customization field. Do not upload it as a source.
- Use `STORYBOARD.md` and `reveal-cues.json` for the edit. These are production documents, not sources to narrate.
- `reference-frames/` contains all 16 exact map states at 1280 × 720, without prompt cards, buttons, counters, footer keys, or explanatory body copy.
- `cities-sequence-review.jpg` and `drinks-sequence-review.jpg` show the full progression for review; they are not upload boards.
- Save the next raw roll as `Prompts/vector-space-7.mp4`, or the next unused numbered raw-roll name if that becomes occupied. No existing roll or candidate should be overwritten.

The six upload map JPGs show the established cities/drinks and the two answer states for each. They are reference images to anchor the narration and labels. They must not be held onscreen from the start of an example, because that would reveal answers early. The production sequence uses all eight states per map. The new prompt explicitly distinguishes reference boards from staged reveals.

## Visual treatment

Use the live lesson’s geographic outline, neighborhood shapes, colors, marker positions, names, and coordinates/vectors. Keep the pale blue outer border and white map panel. Fill the 16:9 frame with the map section. The instruction card and controls belong to the lesson; the video narration takes their place. Keep earlier markers and labels visible while adding each new item.

The two mystery positions on the city map are separate question/reveal pairs. The drinks follow the same structure. Mystery A and Mystery B remain the short labels on the diagram; narration says Mystery Drink A and Mystery Drink B. Hot coffee’s name and vector remain above its circle. Mystery B’s straight label connector appears with its diamond; it is distinct from the short answer connection to hot coffee.

The narrator asks all four closest-match questions and speaks each answer next, with no spoken timing directions. The generation prompt deliberately leaves timing to the editor. For these four questions, the user approved a brief pause before the answer in the finished edit. This supersedes the older generic “no pause-and-guess” instruction for these four moments. Do not tell the viewer to pause the player. At edit review, measure the natural gap in the roll and propose about 1.5–2 seconds total between question and answer, adding only the missing time. Do not apply a blanket pause to other scenes or publish guessed timestamps.

Use the restored canonical context illustration intact. It shows starting and updated positions at once. Highlight the starting numbers, the update path, and the updated numbers/IT beside CAT as the narration reaches each. Do not revive the discarded context interactivity. Follow the current Edit Spec for highlight styling and full-board framing; this prep packet specifies content cues, not final encoded timings.

## Source and upload choices

The older cities, closest-cities, taste-table, neighborhoods, and single-mystery JPGs are excluded from the active upload bundle. They do not match the revised lesson’s coordinates and full reveal sequence. They remain on disk for existing videos.

The six replacement JPGs are captures of the lesson’s shared SVG components in the video-only preview layout, not generated approximations. The context illustration and close are the exact canonical JPGs used by the live page. Neither includes human faces; the context map’s animal faces do not require a faceless variant under the existing Vector Space upload decision. Generated supporting scenes still follow the no-photo instruction. No post-only board substitutes are required.

The narrator introduces each dimension alongside its number. The visual keeps the compact vector beneath each drink’s name, with no “Vector order” footer. Sweetness, bitterness, fizz, heat, caffeine, darkness, and citrus always retain that order. The seven displayed characteristics describe this illustrative drink example; do not claim AI dimensions are these named human attributes.

## Narration review priorities

1. The opening must state both the no-exact-match question and its answer before the first map.
2. Dallas is 32.78 N, 96.80 W; Mountain View is 37 N, 122 W; New York City is 41 N, 74 W. Compare only those three cities. The new positions map to Mountain View and New York City, respectively.
3. Include all three named drinks, both neighborhoods, and both mystery drinks. Mystery A’s first six values match both Coke and Pepsi; citrus distinguishes the two. Mystery B is closest to hot coffee across its seven ratings.
4. Preserve the revised bridge: a vector need not match another exactly; its position in vector space helps represent its meaning. Do not turn that into a nearest-word lookup mechanism.
5. Preserve the IT/CAT sentence and distinguish the separate IT token from its connection to CAT. Map movement is an illustration of changed numbers.
6. End with the exact two current closing lines and nothing after them. Do not narrate the 2048 game, button labels, filenames, board numbers, headings, or production notes.

## Changes for the next roll

The [comparison of versions 4, 5, and 6](../../video-audit/vector-space-comparison-2026-10-06/REVIEW.md) favors version 6’s teaching sequence, version 5’s opening, and version 4’s numerical comparisons. The new roll should teach the complete source in its existing order; do not ask the generator to imitate an earlier roll or upload the review as narration.

- The customization prompt now explicitly prioritizes complete spoken teaching over a short runtime. All seven named dimension/value pairs must be read for Coke, Pepsi, hot coffee, and both mystery drinks. Keep both neighborhoods and the explicit citrus gaps of 1 and 8.
- Four existing source sentences join the required verbatim list: the simplified seven-dimensional drawing caveat, values learned during training, the updated vector not needing an exact match, and IT remaining a separate token. The prompt retains all 13 previously required passages, including the vector-space conclusion and position/meaning callback. These 17 passages appear as standalone paragraphs in the source; only paragraph breaks changed in the narration Markdown.
- Timing instructions stay out of the narration source and out of the generator’s voice directions. Ask the comparison question and give its answer next. The editor measures the recorded gap and adds only any missing silence. Do not upload the storyboard, this note, or the cue JSON.
- Guard against the errors in the reviewed rolls: physical token movement, meaning determined entirely by neighbors, invented drink vectors or dimension counts, and answer rings shown before the answer. Keep the complete context illustration and show IT as distinct from CAT.
- Visual failures alone do not require another roll. The existing staged maps remain the production assets. Judge the next recording’s spoken teaching first, then finalize visual cue timings against that recording.

Replace the previous Vector Space source files in the generation notebook with the nine refreshed files from `upload/`, and replace the customization text with the current `PROMPT.txt`. Avoid duplicate old source versions. Keep every previous raw video for comparison and possible donors. The next raw output is `Prompts/vector-space-7.mp4`; that filename is currently unused.

## Capture and timing handoff

Run `node scripts/video/preview_vector_space.cjs` after a relevant source change. A deterministic reference state is available at `previews/vector-space-maps.html?capture=1&scene=cities&step=3` (or `scene=drinks`, steps 0–7). The existing controlled `window.setVectorScene(kind, step)` interface remains available to production tooling. Capture mode uses a 1280 × 720 canvas and suppresses reveal animation for clean state images; build paced appearances from these states or enable the lesson’s reveal treatment in the actual render. Preview capture for `scene=context` now uses the restored illustration.

The older `capture_vector_space.cjs` and v14 renderer predate the current step counts and restored context illustration. Do not run them unchanged for this new build. `reveal-cues.json` is the current state inventory. A future production pass must update capture/render timing against the new narration; this preparation does not claim those legacy scripts are current.

Validation results and source hashes are recorded in `VALIDATION.json`. Narration length is an estimate until recorded audio exists. The draft still has roughly 900 spoken words, approximately 6–7 minutes with four short comparison pauses, depending on delivery. This is an estimate, not a target to force on the generator. Complete teaching takes priority over the previous video’s three-minute label. No audio/video sync or final pacing QA is possible before a new roll exists.
