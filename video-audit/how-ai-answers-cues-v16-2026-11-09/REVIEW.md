# How AI Answers v16 review

Candidate: `/Users/davidobrien/Developer/AI-Training/Prompts/how-ai-answers-v16.mp4`

SHA-256: `e35f9458102fc45683db32f87200f59dae61d37789bbdaf43c88350d3d066f2d`

Duration: 2:50.033, 5,101 frames at 30 fps. Review candidate only; canonical course video and lesson files unchanged.

## Requested changes

- Removed the unspoken banner highlight at v15 55.233-56.133 seconds. The banner remains visible and unoutlined. The two narrated card highlights remain.
- Inserted 0.600 seconds of matched source room tone at v15 68.400 seconds, inside measured quiet before the question reprise. The encoded gap below -40dB is 68.08-69.09 seconds, or 1.01 seconds total. The preceding loop drawing holds through the pause; the question board appears immediately before the question is spoken. Original PCM is sample-identical on both sides of the inserted tone.
- Added blue, fixed 4px row outlines on the spoken choices You, A, Great, Spot, Max, and Buddy. Each outline covers the choice and its percentage. Existing purple selection outlines and token flights remain. Word onsets were checked against the retained medium.en word timings and the v15 encoded transcript.

## Verification

Full encoded audio/video decode passed. All 46 declared boundaries passed the transition guard. Inspected the six encoded choice states, unhighlighted banner, pause frames, and question re-entry. Compared 44 encoded reference samples and 107 retained-picture samples; maximum retained-image difference 0.0423/255. Encoded/reference PCM correlation 0.99983497, SNR 34.77dB. All protected source, lesson and canonical asset hashes passed. No narration words were added, removed, regenerated, or retimed relative to their accompanying visuals; subsequent content shifts by the inserted 0.6 seconds.

Perceptual listening and uninterrupted playback were not performed. The inserted pause needs listening review; `pause-context.wav` and the review player's pause button provide context. No shipping, installation, commit, or publication was performed.

## Conceptual assessment, not applied in this build

The screenshot omits the visual connection between the earlier words and the numbers at the final token. A viewer can infer that the punctuation symbol itself supplies the answer. Emphasize the updated representation: information from the preceding words changes the final token's numbers through the layers; the model uses those updated numbers to score next-token possibilities. Suggested visual sequence: whole question -> updated numbers at the final token -> next-token choices. Arrows from preceding tokens would make the missing relationship explicit.

Technical reference: [Stanford Speech and Language Processing, language modeling head](https://web.stanford.edu/~jurafsky/slp3/ed3bookfeb3_2024.pdf). Its description identifies the final layer's output at the last token as the input for next-word prediction. This is an illustrative decoder-only explanation; the board's question mark is the selected example, not a requirement of real chat formatting.

## Reproduction

```sh
.video-venv/bin/python scripts/video/build_how_ai_answers_v16.py
.video-venv/bin/python scripts/video/qa_how_ai_answers_v16.py
```

Reconstructed retained picture and audio from the verified original source through the accepted v15 treatment. Final build, cue timings, pause measurements, source hashes and checks are recorded in `edit-manifest.json` and `qa.json`.
