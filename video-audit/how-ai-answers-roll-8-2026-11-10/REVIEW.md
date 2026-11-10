# How AI Answers: roll 8 narration insert

Source: `Prompts/how-ai-answers-8.mp4`, 43.458 seconds. This is a donor for the new familiar-continuation example, not a replacement for the full lesson. The raw video is unchanged.

## Teaching assessment

The complete small.en transcript and a second medium.en transcription both show all required teaching for this insert:

| Point | Finding | Source time |
| --- | --- | --- |
| Compare peanut butter and / salt and | TAUGHT; both phrases are spoken. The recording uses “and” between the phrases rather than the on-page “or.” | 0:04.02–0:06.64 |
| Same final word, different contextualized vector | RICH; explicitly identifies and and explains that its updated vector reflects different preceding words. | 0:08.74–0:13.98 |
| Learned patterns support likely continuations | RICH after removing an intrusive section label; training, high probability, jelly, and pepper are all present. | 0:15.16–0:29.02 |
| Prediction depends on the context reflected in the numbers | TAUGHT, with the lesson wording intact after the filler introduction. | 0:31.14–0:33.98 |

No missing concept or material conceptual error was identified in these transcripts. Verdict for the donor: repair by trimming the extra framing and section-label speech. Final audio suitability remains provisional because direct listening and voice-continuity review have not been performed. This is not a final KEEP certification or an auditioned full-video graft.

## Removed material in the listening preview

Approximate spoken ranges; sample-accurate retained ranges are in trim-plan.json.

- 0:00–0:03.38: “Okay, let’s dive right into context and AI predictions.” The insert belongs inside an existing explanation.
- Approximately 0:07.3–0:08.50: “The context setup.” Both recognizers identify this extraneous label.
- Approximately 0:14.88–0:15.00: “Right.” Retain “So using patterns learned during training…” to avoid an unnecessary tight cut between so and using.
- Approximately 0:18.70–0:20.06: “AI probability predictions.” Both recognizers identify this label. Retain “An AI would likely give…” as a complete continuation.
- Approximately 0:30.12–0:30.96: “At the end of the day.” The sentence can begin with “The prediction…”
- After approximately 0:34.12: the speculative closing question about hidden contexts and the remaining tail. It introduces an unrelated idea and interrupts the lesson's progression.

The spoken “and” joining the two examples is retained. Replacing it with or would require another recorded word and an unnecessary micro-splice. On-screen formatting can clearly separate the two phrases, as on the page.

## Prepared artifacts

- `example-trim-preview.wav`: 23.49 seconds, five retained source spans, no synthetic speech or playback-speed changes. Five-millisecond edge ramps limit discontinuities at cuts.
- `example-in-context-preview.wav`: roll 4 from 1:32.45–1:39.26, then the trimmed insert, then roll 4 from 1:39.26–1:52.70. The new passage therefore follows the first-token explanation and precedes “It adds the chosen token to the context…” and the dog-name demonstration. Insert gain is approximately +0.63 dB to match active-speech RMS in the surrounding source; this does not certify voice or cadence continuity.
- `trim-check/example-trim-preview.txt`: transcription of the actual trimmed audio. It retains the comparison, the vector/context explanation, learned patterns, both likely completions, and the final context sentence. None of the deleted labels or framing is transcribed.
- `build-trim-preview.py`: reproducible preview recipe; `source.json` records the raw source hash.

No on-page teaching, upload materials, installed video, or full review candidate was modified. The 40-second roll-7 motion proof remains unchanged. The proposed full assembly now needs this single narration insert in addition to the roll-4 audio spine.

## Picture for the insert

Use the previously proposed simple comparison: Peanut butter **and** / Salt **and**, then reveal jelly / pepper with the corresponding spoken words. Emphasize the shared and while its contextualized vector is explained. Preserve the qualification that these are likely continuations; add no percentages. The complete pair should remain visible during the closing context sentence. No additional vector schematic or new technical terms are needed.

Listening status: neither the raw voice delivery nor either preview's joins were directly auditioned. The previews are provided specifically for that review; automatic transcription is evidence of retained wording, not evidence of natural delivery.
