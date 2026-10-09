# Embeddings v13: approved lesson visuals in the video

Scope: narrow visual update requested after the owner approved the new guided
comparison and removed the student-ID banner. Carry that same treatment into a
review candidate. Preserve narration, timing, pauses, useful supporting animations,
and all unaffected visuals. No new audio or publication.

Source: `Prompts/embeddings-v12.mp4`, SHA-256
`b6fcc8211b27ea97ab25b6dedc94eba7c692bb94ff773071aa2e7aa730e19806`.
The installed lesson video matches this file. Raw generations are not present;
this update reencodes the existing finished source once, copying its AAC stream.

| Board / component | Highlighting | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| An ID Identifies You. It Doesn’t Describe You. | Unmarked; obsolete banner highlight removed | Complete image with the lesson's bottom crop, centered in 16:9 | 18.367–34.633 seconds | Same banner-free title and photograph as the page |
| Drink ratings by dimension, replacing Meaning Becomes an Ordered Row of Numbers | Headings first; reveal Coke, then Coffee at their narration. Outline the named value, then a full row / position / value with concise term labels | Full table, no zoom or pan | 64.333–86.300, 95.900–106.500; retain the mystery-drink animation at 86.300–95.900 | Learner-controlled live states become narration-controlled reveals, with no buttons or instruction card |
| Drink ratings by dimension, replacing One New Dimension Separates Similar Meanings | Move Coffee above the colas as the updated table is introduced; add Pepsi; compare the first six values. Reveal the Citrus heading and empty tiles, then each rating as spoken | Full table, no zoom or pan | 106.500–116.300, 122.800–137.200; retain matching-can animation at 116.300–122.800 | Keep Coke and Pepsi adjacent and separate adding a dimension from filling its values |

The first table's video order is Coke, Coffee, Pepsi because existing narration
explicitly says “first row for Coke” and “Moving down to the next row, coffee”.
At “This updated table” the order changes to Coffee, Coke, Pepsi, matching the
approved final lesson layout. This video-specific staging preserves the approved
narration and avoids a contradictory row reference. Shared colors, data, geometry,
and lesson render function are captured directly from `index.html`.

Preserved supporting scenes: the taste-rating introduction at 49.167–64.333,
the mystery can reveal at 86.300–95.900, the paired-can comparison at
116.300–122.800, and the animated dimension explanation after 137.200.
Longest changed continuous table run: 21.967 seconds, containing successive
row and value reveals rather than an unchanging static hold.

No narration cuts, grafts, synthesis, or added pauses. Existing wording defines
vector, dimension, and value correctly, while the new labels emphasize those
terms. Complete video remains 7,997 frames at 30 fps (4:26.567).

V14 review repair: the original ten-frame mystery dissolve at frames 2589–2599
contained the retired static board. Re-render that short opening directly from
the existing animation code; retain the remainder. Rebuild from v12, preserving
all narration and timing. This is a necessary join repair within the replaced
board's outgoing transition, not a new animation or an audio change.
