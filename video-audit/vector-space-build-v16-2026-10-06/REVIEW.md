# Vector Space v16 build review

Built a **4:44.87 review candidate** from raw version 8, with the two approved narration passages from raw version 9. The cities and drinks now appear progressively from the current lesson maps. Each mystery answer remains hidden until the narrator gives the answer. The final context scene uses the canonical illustration, and the video ends on the canonical close.

[Watch v16](/Users/davidobrien/Developer/AI-Training/Prompts/vector-space-v16.mp4). This is a review candidate, not a KEEP or shipping certification. Direct listening and real-time motion review remain pending. The installed video, raw source videos, and canonical Vector Space assets were preserved. No lesson edits, installation, commit, tracker update, or publication were made by this build.

## Narration repairs

Version 9 supplies the complete embedding definition and the correct Pepsi coordinates, ending in Citrus 10. Version 8 supplies every other passage. Whole-sentence cuts remove the five repeated recaps identified in the approved evaluation and the inaccurate added claim after the close. All three city coordinate pairs, both mystery coordinate pairs, five drink vectors, four questions and answers, the training sentence, and separate IT/CAT explanation remain.

| Donor passage | Output span | Original donor span |
| --- | --- | --- |
| Complete embedding opening | 0:00.00–0:10.17 | Raw 9 0:00.00–0:10.17 |
| Pepsi with correct Citrus 10 | 1:51.17–2:03.20 | Raw 9 2:00.30–2:12.33 |

The donor gain is −0.815 dB, matched using active speech RMS. Audio is 48 kHz with 5 ms edges into measured source room tone. Peak assembled PCM is 28,312, below 32,767. Cut edges sit inside measured quiet intervals; no word-level splices or synthesized narration were used.

Listen particularly around **0:10**, **1:51**, and **2:03** for voice continuity and clean breath/word boundaries. Also listen to the four question-to-answer pauses and the final two sentences. Transcripts and silence measurements cannot certify those qualities.

## Visual treatment

| Section | Output time |
| --- | --- |
| Opening | 0:00.00–0:22.27 |
| Relationships | 0:22.27–0:31.40 |
| Cities | 0:31.40–1:25.40 |
| Drinks | 1:25.40–3:38.93 |
| Scale | 3:38.93–3:54.50 |
| Sentence | 3:54.50–4:06.23 |
| Context | 4:06.23–4:35.33 |
| Close | 4:35.33–4:44.87 |

- The opening reuses the previously approved IT and number-row drawing, with the lesson’s illustrative .12/−.34 and .41/.06 values. It replaces generated nonsense token text and is retimed to the new narration.
- The animals/vehicles relationship animation is retained from raw 8, source 0:22.50–0:28.17, slowed to fit the opening explanation. Its header and proximity label are corrected to preserve the lesson’s qualified claim.
- Sixteen states were freshly captured from the current shared lesson components. All maps stay at a fixed full-panel view. New points, labels, vectors, and answers fade in over 15 frames; previously shown locations stay fixed. Prompt cards, controls, counters, and vector-order keys are omitted for video.
- The scale sequence retains raw 8’s axes, concept neighborhoods, contextual bank position, and many-axis drawing, source 3:55.50–4:11.07. The invented dimension count and readable sample vector are replaced by “Thousands of dimensions” and “Values learned during training.” The absolute “Distance = Meaning” heading becomes “Positions and relationships.” The corrected panel covers its entire incoming transition.
- The exact CAT/IT sentence precedes the complete canonical “How Context Changes IT’s Position” illustration. This compact board stays at full view with both IT positions visible. Fixed 4 px outlines guide attention to starting numbers, updates, updated numbers, distinct IT/CAT, and the complete takeaway banner. The source JPG is unchanged.
- The close uses the canonical asset through `make_close_board.py`: 48-frame full view, 150-frame push to 1.2×, then settled hold. No outro or added spoken claim follows it.

The longest continuous map sequence is **133.53 seconds** for drinks, with staged additions and two learner comparisons; cities run **54 seconds**. These are the user-approved progressive-interactivity adaptation, intentionally preserving the accumulated objects. The static context board runs **29.10 seconds** after the sentence scene. The next two illustration breaks are the 9.13-second opening relationships animation and the 15.57-second scale sequence. There are no added decorative cutaways.

## Verification

All **8,546 planned frames** decoded at 1280 × 720 and 30 fps, with no black frames. **All 43 declared transition boundaries passed** the short visual-island check. The four encoded comparison gaps are **1.749, 1.763, 1.743, and 1.741 seconds**, each within one frame of the 1.75-second target. All four answer reveals were compared against their unanswered and answered reference states. Protected source and installed-video hashes are unchanged.

The complete edited WAV was transcribed with base.en. The encoded AAC was independently transcribed with small.en: **17 of 17 required passages match**, all five full drink vectors are present, Pepsi ends in Citrus 10, and the final inaccurate extra sentence is absent. One ASR renders “vector” as “factor” in the Mystery B comparison; the other renders “vector.” The raw source narration is unchanged there; direct listening must resolve that ASR disagreement.

The visual revision from internal v15 to v16 changes only the dimension-panel transition. Their extracted AAC streams are byte-identical, so the encoded transcript applies to the delivered v16. See [audio equivalence](audio-equivalence.json), [required passages](required-passages.json), and [encoded transcript](../vector-space-build-v15-2026-10-06/encoded-transcript/vector-space-v15.txt).

Final frame counts, measured comparison pauses, revealed-state comparisons, and transition results are recorded in [QA data](qa.json) and [transition guard](transitions/transition-guard.json). The [edit manifest](edit-manifest.json) records exact input/output frame ranges, source hashes, protected-file checks, and visual cues. Each frame was sequentially decoded; targeted stills and transition strips were inspected. This does not constitute real-time playback or audio audition.

Internal v15 is superseded because frame inspection caught the original dimension label faintly appearing during its incoming dissolve. V16 extends the repair over that full transition and preserves every other scene and the complete audio.
