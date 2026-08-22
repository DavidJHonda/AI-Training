# Video repair pilot

## Shipped outputs

- `videos/fake-trap.mp4`
- `videos/layers.mp4`

The approved v3 pilots were promoted byte for byte to the canonical lesson
filenames on 2026-08-22. The prior tracked versions remain recoverable through
Git history, and the versioned pilot files remain available for comparison.

## Treatments

### Fake Trap

- Kept both current boards fully visible.
- Highlighted Money, Power, Fame, and Cruelty in narration order.
- Expanded the Fame and Cruelty outlines to include their complete panels.
- Replaced the confirmed 0.12-second stray syllable after "Fame" with matched
  room tone without changing the video stream or track duration. A fresh
  transcript reads: "Fame, to gain followers through viral lies. And cruelty..."
- Highlighted Source, Context, and Corroboration in narration order.
- Rebuilt the close from `CLOSE_BOARDS[faketrap]`.
- Used the standard close move: 48-frame prehold, 150-frame push to 1.2x,
  then a same-size settle through the remaining narration.

### Layers

- Kept the two lighter three-column boards fully visible and highlighted each
  component in narration order.
- Highlighted the main sentence only while the narrator reads it.
- Used a zoom-and-pan treatment for the dense "What happens inside every
  layer" board, including a final pullback to show the complete vector rail.
- Extended the current "dozens of layers" board through frame 4133, then cut
  directly to the neural-network animation at frame 4134. This removes the
  15-frame flash of the retired board at 2:17.
- Rebuilt the close from `CLOSE_BOARDS[layers]` with the same fixed endpoint as
  Fake Trap.

## Edit-integrity results

Both pilots pass:

- exact decoded frame count;
- nominal frame cadence;
- bit-identical source audio;
- no changed frames outside authorized visual spans;
- no one-to-five-frame source islands inside replacements.

Boundary contact strips and machine-readable reports are in:

- `video-audit/pilot/splice/fake-trap/`
- `video-audit/pilot/splice/layers/`

## Audio review

The visual repairs retain the original audio bit for bit. The audio-gap audit
flagged no blip candidates in Fake Trap and two candidates in Layers. Isolated
waveforms and spectrograms show that both Layers flags contain the onset of the
following spoken word inside the transcript-reported gap. Both are marked
`KEEP`; silencing them would damage narration. Natural breath and room-tone
candidates remain untouched.
