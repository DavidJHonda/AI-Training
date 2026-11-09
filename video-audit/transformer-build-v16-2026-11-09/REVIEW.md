# Transformer v16 — review candidate

Built November 9, 2026 following “Build it please.” The candidate is
[transformer-v16.mp4](../../Prompts/transformer-v16.mp4), **4:26.93**, 1280×720,
30 fps, H.264/AAC. This is a full production review candidate, not installed,
committed, or published. The installed video, current lesson, canonical boards,
and raw generations are unchanged by this build.

## What changed

Roll 6 supplies the foundation. Roll 5 supplies the fuller opening questions,
the human-reading/earlier-AI bridge, and the transition from reading to updating
numbers. The opening uses the proposed safe alternative: retain roll 6’s “Two
problems,” then begin roll 5 at “Let’s look at the left side, problem one.” The
uncertain “lays out/leaves out” phrase is excluded.

The exact qualified earlier-AI line comes from raw roll 2. The return to the
examples repeats roll 6’s complete LIGHT and IT sentences and meanings before
its clue explanations. The false sentence claiming simultaneous processing loses
the sequence is removed, along with that drawing. No extra instructional pauses
or speech stretching were added. Donor gain adjustments are +0.42 dB for roll 2
and −0.12 dB for roll 5; 5-ms ramps occur in measured quiet gaps.

All six instructional boards use the current canonical JPGs. The two tall
example boards establish the full view, move to complete cards, and return for
the takeaway. Compact boards remain whole. Highlights follow the narration and
use the shared fixed 4-pixel outline renderer. No extra outline surrounds the
already-emphasized IT token. The canonical close ends the file, with the standard
48-frame hold, 150-frame push to 1.2×, and 46-frame settled hold.

## Output timeline and listening locations

| Output | Passage / source |
| --- | --- |
| 0:00–0:21.87 | Roll 6 tokens, embeddings, whole-word convention, “Two problems” |
| 0:21.87–1:22.73 | Roll 5 examples, questions, surrounding words, earlier-AI bridge |
| 1:22.73–1:33.27 | Roll 6 full tired-cat reading and distance |
| 1:33.27–1:38.07 | Roll 2 exact “Earlier AI often struggled … especially in longer passages” |
| 1:38.07–2:07.37 | Roll 6 history and parallel processing |
| 2:07.37–2:16.90 | Roll 5 “There’s more to reading …” and number-update bridge |
| 2:16.90–2:45.37 | Roll 6 mechanisms and return setup |
| 2:45.37–2:51.70 | Roll 6 opening LIGHT examples reused |
| 2:51.70–3:04.37 | Roll 6 LIGHT clues and pronoun setup |
| 3:04.37–3:14.17 | Roll 6 opening IT examples reused |
| 3:14.17–3:40.37 | Roll 6 pronoun clues, conclusion, sarcasm/idioms |
| 3:40.37–4:26.93 | Roll 6 correct order bridge, position explanation, close |

Listen particularly across **0:21.87, 1:22.73, 1:33.27, 1:38.07, 2:07.37,
2:16.90, 2:45.37, 2:51.70, 3:04.37, 3:14.17, and 3:40.37**. Every assembly
seam lies in a detected quiet interval; measured total intervals range from
0.28 to 0.89 seconds (`join-gaps.json`). This verifies cut placement, not cadence,
voice compatibility, or natural pacing.

## Supporting illustrations and board duration

- 0:00–0:20.77: roll 6 phone, token pieces, numbers, and whole-word drawing.
- 1:09.43–1:14.57: roll 5 eyes/book/CAT/MILK drawing for human interpretation.
- 1:14.57–1:22.73: roll 5 sequential-processing diagram for earlier AI.
- 1:38.17–1:47.60: roll 5 paper-title drawing, picture retimed to roll 6 speech.
- 1:47.60–1:51.47: roll 6 ChatGPT/T reveal; specialist architecture stack covered.
- 2:07.37–2:16.90: roll 5 CAT-to-IT number update. Its early attention heading
  is removed; the actual mechanism is introduced on the next board.
- 3:25.00–3:40.37: roll 5 familiar sarcasm/idiom drawing, picture slowed to
  accompany the intact roll 6 explanation. Misleading technical arrows are removed.

The longest single board span is **48.67 seconds** for the opening examples;
the return runs 44.20 seconds, and word order 38.43 seconds. No additional
relevant illustration was planned inside these worked examples, so the edit uses
the approved card/section progression rather than decorative filler. The longest
continuous run of adjacent boards is 68.10 seconds (mechanisms plus return).
These are deliberate review points for pacing, not claims that the usual
20-second illustration preference has been met everywhere.

## Verification and remaining review

- Exact candidate SHA-256: `cd9029d8c283c221dffcdadf2f7c2d59ad1f1d8c627a41d605192515a0d0e3a9`.
- Decoded **8,008 frames**, matching the planned duration. Both streams decode.
- All **20 declared boundaries pass transition_guard**; every-frame boundary
  contact strips inspected, with no stale board or sequence-loss frames observed.
- Fresh transcript from the encoded candidate confirms the selected passages,
  complete repeated examples, qualified earlier-AI line, removed false claim,
  and both closing lines. ASR spelling variants are not treated as listening facts.
- All 171 prepared board states compared with corresponding encoded frames;
  maximum mean channel difference 2.88/255. Encoded overview sheets, boundary
  strips, supporting scene samples, and close inspected. Continuous audiovisual
  playback and every settled state at full resolution remain unperformed.
- Fixed-width renderer verified; targeted contrast measurements of 44 ring
  states give effective median width 4.21 px (compression edges included).
  The general color detector also counts thin baked-in token borders, so its
  unfiltered 2–4 px histogram is not the added-ring width measurement.
- Encoded audio correlates 0.999987 with assembled PCM. This confirms timing and
  transfer, not perceptual audio quality. No direct listening has been performed.
- Corner cleanup applied to all 2,168 retained drawing frames: 1,835 paper clones
  and 333 glyph-only inpaints, with no declined frames.
- Source, installed-video, lesson, and board hashes remain unchanged.

One known script deviation remains at **2:37.40–2:40.18**: the intact narration
says “The surrounding words help update each token’s numbers,” omitting “AI.”
The board shows the approved full sentence. Its meaning is preserved; this is
not an exact-script pass. Spoken position numbers are present, but the narrator
does not explicitly say DOG=1, BITES=2, MAN=3; the board supplies the mapping.

**Status: built and technically checked for owner review.** Cross-roll voice
continuity, all audio joins, pacing, and continuous animation review remain open.
This is not a KEEP/ready-to-ship certification.

Build: `scripts/video/build_transformer_v16.py`. Technical QA:
`scripts/video/qa_transformer_v16.py`. Exact source identities, source/output
frames, board hashes, ring timing, camera paths, and visual repairs are in
`edit-manifest.json`.
