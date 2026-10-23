# Doubter removal — review candidates, 2026-10-22

**Superseded for Loudest Voices by v11:** David found the independent three-voice branching diagram near 0:22 that this review missed. The [opening repair](../loudest-voices-opening-v11-2026-10-22/REVIEW.md) brings our board in at 0:19.9. Opener v6 is unchanged.

David authorized removing the Doubter from Loudest Voices and the Embrace the Future opener, updating the board and videos, and fixing the flash at 1:14. Both candidates are built. Installed videos are unchanged; no commit or push was made.

## Results

| Candidate | Runtime | Changes |
|---|---|---|
| `Prompts/loudest-voices-v10.mp4` | 4:41.933 (8,458 frames) | Two-expert board, LeCun narration and synthesis line removed, Hinton flash repaired; retains the approved In Your Hands ending. |
| `Prompts/embrace-the-future-opener-v6.mp4` | 3:17.300 (5,919 frames) | Removes the three-types lead-in and Doubter sentence; replaces the three-person illustration with the canonical opening quotes board. |

The page and Markdown now omit the Doubter. The experts board retains the original Amodei and Hinton quotations, artwork, standard typography and footer credit, in two equal-width cards. Video prep bundles have been synchronized and checked.

## Source edits

All ranges are half-open, at 30 fps; exact mappings and source hashes are in each candidate's manifest.

- Loudest Voices v8: remove frames 2751–3612 (91.700–120.400 seconds) and 3823–3884 (127.433–129.467 seconds). Cut through measured silence, preserving the full word “benefits.”
- The flash was a ten-frame return to Hinton's biography at source frames 2224–2233. The quotation view now starts at 2224 and remains stable; audio is unchanged there.
- Preserve the prior v9 assembly's source selections: Loudest Voices through frame 6488; In Your Hands v6 frames 1074–3477, then its closing audio at 5019–5508 under the current canonical Loudest Voices close.
- Opener v5: remove frames 1062–1209 (35.400–40.300 seconds) and 1429–1531 (47.633–51.033 seconds). Replace every retained frame of the old archetypes scene, through source frame 1539; the question-mark scene begins at 1540.
- No new narration, added pauses, or loudness changes. Five-millisecond fades sit only at quiet cut handles. Each output has one additional H264/AAC encode from the surviving finished sources; raw generation masters are unavailable.

## Board treatment

- **Even the Experts Don’t Know:** full two-card comparison first; retain the previously approved complete-card context at left and readable native section at right. Follow identity, SAYS, BUT ADMITS for each expert, then return to both cards for the synthesis. Four-pixel outlines use the existing card accents. Independent Google illustration is retained.
- **What Everyone’s Saying:** returns at full view during the revised opener passage, with the two positive quotations highlighted for Optimist and the two negative quotations for Worrier. The complete board was already established at the video opening. Hold the Worrier state across the removed sentence to the existing question-mark scene, avoiding a new brief intermediate state.
- All unaffected scenes retain their source timing and framing. The closing board retains the 48-frame hold, 150-frame push to 1.2×, and settled hold.

## Verification

- Compared all 14,377 encoded frames against the selected source frames or expected native board rendering. Correct 1280×720, 30 fps, continuous presentation timestamps.
- Transition guard passed all 21 changed boundaries with a 12-frame island threshold (including the old ten-frame defect). Reviewed the every-frame strips and board/contact-sheet frames; no leaked Doubter or biography-return frames found.
- Audio matches the intended sample-aligned edit: correlations 0.999808 and 0.999774. All six joins have quiet handles and negligible sample steps. Peaks remain below clipping.
- Fresh transcripts omit the Doubter, LeCun, and “three types of people.” Read both transcripts, including the new joins. ASR spells Worrier as “warrior” and misspells some names; no narration was synthesized or changed to match those errors.
- Both browser players load the expected durations and 720p dimensions without media errors.
- Source hashes and installed videos verified unchanged. Prep checks and `git diff --check` pass.

**Listening remains outstanding.** Frame inspection, transcription, and PCM checks do not establish audible cadence or continuity between the Loudest Voices and In Your Hands source voices. Use the review page's jump buttons for the changed passages and the retained donor/closing joins. These are review candidates, not a whole-file shipping approval.
