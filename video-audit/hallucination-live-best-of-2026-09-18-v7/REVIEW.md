# Hallucination live best-of review candidate

## Recommendation

**KEEP as the review candidate. Do not ship until a human has auditioned the six listed edit boundaries.**

The candidate now carries the strongest instructional combination from the live video and both alternates: the live edit remains the picture and narration spine, Hallucination-2 supplies the corrected real-fact distinction and canonical close, and Hallucination-1 supplies the missing verification caution. The current lesson boards remain in use.

Candidate: `Prompts/hallucination-v7.mp4`

- SHA-256: `ba7d115eacfd31e55cef8edb532c74b7ea5bce11b3cee6617e4a2f7e5e30ce8f`
- Runtime: 4:00.667
- Video: 1280x720, 30 fps, 7,220 frames
- Status: review candidate only; live video and lesson materials were not changed

## Narration findings

The complete timestamped transcript contains the lesson's essential teaching accurately and in the intended sequence: a plausible fabricated Stanford study, why prediction can produce confident falsehoods, the pizza-glue example of a real source misread in context, the distinction between fabrication and misinterpretation, and the three-step verification method.

Three approved narration repairs are present:

1. **0:39.667-0:45.433** — Hallucination-2: “So it attaches an invented detail to a fact that is real, making the error much harder to spot.” This replaces the live edit's incorrect sentence.
2. **3:14.600-3:22.300** — Hallucination-1: “Failing to find a source doesn't automatically prove a claim false, but it means the claim remains unverified and shouldn't be trusted.” This is inserted before “If you do find the source document...”
3. **3:50.067-3:56.867** — Hallucination-2: “Hallucinations sound like every other AI answer. When something doesn't add up, trace the claim to its source.” This replaces the live close.

The retained subject-change pause is 1.236 seconds at 1:47.755-1:48.990. No new one-second pauses were added. The verification insertion has a 0.728-second pause before the next sentence, which is appropriate rather than rushed.

The final candidate's automatic transcript has 636 words and contains all three approved passages. A higher-accuracy transcript of the identical spoken program before the final room-tone-only refinement also preserves the two closing sentences as separate sentences.

## Visual and production notes

- All current boards are used: “Nothing Sounds Wrong,” “Why Hallucinations Happen,” “Real Text. Wrong Meaning.,” “Check the Claim,” and the canonical close.
- The verification caveat remains visually under **Find the Source**; **Check the Match** is not highlighted until the narration moves to contextual support.
- All settled highlight states were inspected at full 1280x720 resolution. Text, rings, crops, and recap states are clean.
- All six declared visual transitions passed the automated stale-frame/island guard and were also inspected in every-frame strips.
- The full-video contact-sheet pass is clean. The canonical settled close is the literal final frame.
- Gemini corner-mark cleanup completed on retained Notebook spans: 1,141 clone frames, 1 inpaint frame, 0 declined frames.

## Audio boundary checks

The pre-encode WAV and decoded AAC output were measured at every narration boundary. The decoded candidate has no material sample discontinuity:

| Boundary | Output time | Decoded sample step | 20 ms RMS |
| --- | ---: | ---: | ---: |
| live -> real-fact graft | 0:39.667 | 0.0000000 | -47.22 dBFS |
| real-fact graft -> live | 0:45.433 | 0.0000305 | -53.20 dBFS |
| live -> caution graft | 3:14.600 | 0.0000000 | -62.35 dBFS |
| caution graft -> live | 3:22.300 | 0.0000000 | -63.18 dBFS |
| live -> exact close | 3:50.067 | 0.0000305 | -59.25 dBFS |
| exact close -> quiet hold | 3:56.867 | 0.0000305 | -78.52 dBFS |

Peak after AAC decode is 0.699677, with no clipping in the delivered encode. Silence detection finds the intended 4.053-second quiet closing hold from 3:56.630 through the end.

## Required human audition before shipping

This environment could inspect waveforms, decoded samples, transcripts, timing, and frames, but it could not play and perceptually judge the audio. A human should listen across **0:39.667, 0:45.433, 3:14.600, 3:22.300, 3:50.067, and 3:56.867** for voice-color changes, cadence, and any perceptible edit texture. This is the only remaining sign-off item.

## Provenance and preservation

Protected inputs were hash-checked before and after the build and are unchanged: the live MP4, Hallucination-1, Hallucination-2, the lesson Markdown, and all five board assets. `index.html` and the live course video were not modified. Earlier v5 and v6 renders are retained as superseded audit iterations; v7 replaces them because it uses sample-continuous joins and verified quiet post-word room tone for the settled close.

Detailed source ranges, gain matching, board timing, protected hashes, and render metadata are recorded in `edit-manifest.json`.
