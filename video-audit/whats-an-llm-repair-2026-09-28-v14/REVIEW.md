# Superseded by v15

V14 was an intermediate review render. Frame-by-frame inspection found the
prediction banner ring appearing for only two frames (8296–8297) immediately
before the new drawing cutaway. V15 starts the drawing at frame 8296 to remove
that flash. Do not publish v14.

The other checks passed: 9,114 decoded frames, unchanged AAC payload, and no
automatic transition-guard failures. This is why manual strip inspection remains
necessary even after the guard passes.

Audio investigation is retained here: `audio-41-50.wav` and
`audio-waveform.png`. The corrected owner-reported location is about 44.5 s,
within the sentence “To see where those patterns come from, we have to look at
the training process.” No audio edit occurs there in the prior build plan.
Decoded audio from 42–46.5 s correlates 0.999998 with the pre-shortening backup,
so the September 25 shortening did not materially change this phrase. This does
not establish that it sounds correct. No literal listening was performed and no
speculative audio filter or word splice was applied.
