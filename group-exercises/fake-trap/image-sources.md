# Fake Trap individual and group exercises: image sources

This shared asset collection contains ten camera photographs supplied by the course owner and ten AI-generated counterparts. The individual Fake Trap TRY IT currently uses Cat, Sculpture, and Venice. The standalone group exercise uses all ten pairs. Public feedback omits the photographer’s name, as requested. A/B filenames avoid giving away the answer in the visible image labels or alt text.

| Pair | A | B |
| --- | --- | --- |
| Cat | AI-generated | User-supplied pet photograph |
| Sculpture | User photograph taken in Liverpool, England | AI-generated |
| Venice | AI-generated | User photograph taken in Venice, Italy |
| amarillo | User photograph | AI-generated |
| cake | AI-generated | User photograph |
| flowers | User photograph | AI-generated |
| hockey | AI-generated | User photograph |
| christmas | User photograph | AI-generated |
| ocean-view | AI-generated | User photograph |
| storefront | User photograph | AI-generated |

The Liverpool photograph was cropped to its top 1290 × 1364 pixels, ending below the rectangular torso opening and above the main figure’s groin. No generative edits were made to any camera photograph. The first three originals were resized as needed and encoded as JPGs for the site; the original attachments remain unchanged. The seven additional photographs were initially moved and renamed byte-for-byte unchanged, with their SHA-256 hashes verified after the move. On September 23, 2026, the Cake, Christmas, Hockey, and Ocean view photographs were resized proportionally to a 2,000-pixel longest edge and saved as high-quality JPGs (quality 90). Their EXIF orientation was applied to the pixels, full framing was preserved, and embedded color profiles were retained where present. Original SHA-256 values in generation-prompts.md document the intake files before this resizing.

All twenty current assets live in `group-exercises/fake-trap/`, with names `fake-trap-try-{subject}-{a,b}.jpg`. These images are shared exercise assets. The Fake Trap TRY IT loads them directly from this folder; keep one copy for individual and group use. Video prep intentionally excludes interactive activities, so this does not change the lesson’s video materials.

Generation briefs: a casual fluffy-cat smartphone photograph on a sofa; a bronze sculpture containing smaller figures outside a gallery; and a nighttime Venetian bridge viewed from a boat with a deck reflection. All were generated as new scenes with plausible natural lighting and ordinary travel/snapshot quality, not alterations of the supplied photographs.

The seven additional counterparts were created with the built-in image-generation tool from text descriptions as independent synthetic scenes. See [generation-prompts.md](generation-prompts.md) for the full prompts and file mapping. They were encoded as JPGs without changing the generated scene. The five unselected intake photos were deleted as requested, and the empty intake folder was removed.
