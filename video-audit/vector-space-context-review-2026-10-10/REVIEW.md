# Vector Space: revised-sentence donor comparison

Date: 2026-10-10. Scope: narrow repair of the approved live video after lesson edits. This is a transcript/still-frame donor comparison and proposed plan, not a full-roll teaching verdict or shipping certification.

## Recommendation

Keep the live v18 edit as the base. Replace only its spoken example sentence and matching sentence graphic. Try roll 11 as the donor, with roll 12 as an alternative if its voice fits better. Do not substitute an entire new closing section.

The current lesson in `index.html` reads: “The tired CAT sat on the mat during the May rainstorm. IT soon fell asleep.” Its essential explanation is that layers update IT’s numbers to carry information about CAT, and changing the numbers changes the position. The existing live explanation already teaches these relationships without using later words as clues to update the earlier IT position. The lesson’s new Layers bridge need not be inserted verbatim: the live introduction already connects context to position.

## Evidence and source identity

`sources.json` records hashes, durations, dimensions, frame rates, and audio rates. The live SHA-256 is `cd895007b43e295a86f7aaea199014cec17e17bd332bf6ceaac08506e87ac805`. Installed source: `course-assets/vector-space/vector-space.mp4`, page tag `20261008ship-vector-space-v18`, duration 256.633333 seconds.

All four files were transcribed with offline faster-whisper small.en, including word timestamps. Complete transcripts are in `transcripts/`. Tail stills were inspected in `tail-contact.jpg`; this is not real-time motion review. Quotes below are ASR-derived, not certified by direct listening. Timing differences of a few tenths of a second across ASR runs are expected.

## Comparison of the changed teaching beat

| Source | Sentence, ASR timestamps | Assessment for this repair |
|---|---|---|
| Live | 212.94–217.28: “The cat sat on the mat during the May rainstorm because it was tired.” | Old example; replace. |
| Roll 10 | 184.28–188.54: “the tiled cat sat on the mat during the May rainstorm. It soon fell asleep.” | ASR renders “tiled”; tired/tiled needs listening verification. Do not select over clearer transcript alternatives yet. |
| Roll 11 | 221.24–225.26: “The tired cat sat on the mat during the May rainstorm. It soon fell asleep.” | Exact revised wording in transcript. First proposed donor; voice match remains unverified. |
| Roll 12 | 221.00–225.22: “The tired cat sat on the mat during the May rainstorm. It soon fell asleep.” | Exact revised wording in transcript. Equal content alternative; no claim that 11 sounds better. |

The existing live continuation at 218.00–227.42 says: “On its own, it could refer to many things. As the layers process the sentence, they update its numbers to carry information connecting it to cat.” At 228.20–246.60 it walks the starting coordinates, updated coordinates, separate token, and connection to CAT. These explanations remain compatible with the revised example. Preserve them.

Broader donor passages are unnecessary. Roll 10 adds “context physically moves a word” (179.58–182.46); roll 11 adds “the system physically changes the token’s position” (237.20–241.76); roll 12 adds “two absolute rules for how models comprehend language” (264.80–268.78) and an extra outro. These are reasons to limit the graft, not full-roll verdicts.

## Proposed narration edit and audition

- Live removal window: 212.333333–217.466667, in the gaps around the old example (5.133334 seconds).
- Roll 11 insertion window: 220.766667–225.700000 (4.933333 seconds), containing both complete revised sentences.
- Provisional timing delta: −0.200000 seconds. Final boundaries depend on listening/waveform verification; retain natural spacing and do not time-stretch speech merely to match the old duration.
- Preserve the live “Consider the sentence” introduction and resume at “On its own…” afterward.
- No additional teaching pauses. Preserve other audio/visual timing relative to the retained speech. If necessary, match donor level only after measuring it; do not process the whole soundtrack.

`sentence-donor-11-audition.wav` is an exploratory, unlevelled audio preview joining live 206.266667–212.333333, donor 220.766667–225.700000, and live 217.466667–227.700000. It is not a candidate video. Direct listening has not been completed; the seam and pronunciation are not yet a verified REPAIR source.

## Proposed picture plan

| Board / scene | Highlighting | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| Existing sentence graphic (no displayed title) | Preserve purple CAT and IT emphasis; change the text to the revised two-sentence example | Static full frame | Approximately 206.27–217.80 in proposed output, replacing the existing 206.27–218.00 card | Correct the displayed example. `proposed-sentence-card.png` previews the same typography/style. No added ring or pause. |
| How Context Changes IT’s Position | Preserve approved starting-numbers → layers → updated-numbers → IT → conclusion emphasis | Preserve existing framing | Existing live 218.00–247.10 shifts to approximately 217.80–246.90; same duration and no new breaks | Canonical board contains no obsolete example sentence. Retained narration and highlights remain synchronized by shifting together. |

Preserve all earlier city/drink/scale scenes and the existing close. No new Notebook illustrations are proposed. Prior build provenance is `video-audit/vector-space-build-v18-2026-10-08/`; use its source assembly for an eventual candidate where practical to avoid cumulative lossy encoding.

## Status and next step

No live file, page entry, lesson, or candidate video changed. Existing unrelated edits to `index.html` were left untouched. No tracker entry, commit, or push performed.

Present this narrow plan and audition for approval before the first candidate build, per `scripts/video/EDIT-SPEC.md` section 1b: “Present this with proposed narration changes and selective pauses as ONE edit plan for David’s approval before the first build.” Analysis and audition previews are explicitly permitted. A candidate would still need audio seam listening, encoded frame verification, and the applicable whole-file ship checks before shipping.
