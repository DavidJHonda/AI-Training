# Engagement Trap review candidate

Status: built for owner review, not shipped.

Candidate: `Prompts/engagement-trap-patched.mp4`

Source: `Prompts/engagement-trap.mp4`

Runtime: 4:02.167, 7,265 frames at 30 fps, 1280 x 720.

## Approved narration cuts

| Source time | Removed | New cut location |
|---|---|---|
| 0:58.300–1:14.400 | Repeated narration of the two timelines before the board walkthrough | 0:58.300 |
| 1:45.100–1:57.933 | Application-objective definition and academic-content-as-bait wording | 1:29.000 |
| 3:56.833–4:06.067 | Blanket maximizing-interaction / entirely-different-goals claim | 3:27.900 |

Keep the positive example of accepting useful additional practice. Keep all other approved narration. Preserve complete words at the measured quiet shoulders, with only 3 ms edge ramps at the cuts. No synthesized narration, added teaching pause, or ripple deletion of isolated breaths.

## Current assets and output locations

- 0:16.700–0:40.233: exact comparison board, then complete AI speech-bubble highlight. Covers the formula's Notebook highlight as well as the inappropriate warning and equation graphics.
- 0:58.300–1:16.733: exact comparison board, establish full, then frame both complete outcome boxes together and highlight blue left / amber right in narration order.
- 2:00.433–2:37.233: exact infinite-scroll board, both columns visible, blue / amber full-card highlights, then full-width takeaway highlight.
- 3:07.200–3:12.533: clean native phone-and-paper-ribbon footage with a restrained push, replacing the unsupported numerical chart.
- 3:31.633–3:54.600: current Nate and Luke stop illustration, full title and takeaway banner visible throughout.
- 3:54.600–4:02.167: exact current close with the established standard move and final hold. No Notebook outro.

## Verification

The recipe writes `manifest.json`, including every output-timeline boundary and each measured highlight's geometry, camera, and locked accent source.

`transitions/transition-guard.json` is the current machine-check result; its referenced every-frame strips are the authoritative boundary evidence. The initial audit caught a four-frame source graphic at the history cut and a six-frame source graphic at the final narration cut. Short destination-shot bridges now replace those remnants without changing audio timing. Old `audio-cut-2` and `audio-cut-3` strips in the directory are superseded by the current `to-bridge-*` / `from-bridge-*` strips.

Full-resolution settled highlight frames and the literal final frame are in `qa/`. Highlights follow actual bubble, card, and banner boundaries. No ring crosses target text or clips against the frame. Native board annotations are replaced by constant-weight course rings.

Audio checks: the three cut locations have quiet shoulders and sample-step magnitudes below 0.00002. The cut-reel transcription confirms the complete joins: “next hour. This breakdown…”, “engagement trap. To see why…”, and “good use of your time. Passively complying…”. Individual cut WAVs are available for listening. These checks are not a claim of a full human listening review.

The source and live-video hashes are checked by the builder. Neither the live video nor `index.html` is modified. No videos deleted and no commit made.

Recipe: `scripts/video/build_engagement_trap_review.py`.
