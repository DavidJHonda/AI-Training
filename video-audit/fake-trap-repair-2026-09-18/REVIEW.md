# Fake Trap repair build — 2026-09-18

## Result

- Review candidate: `Prompts/fake-trap-v1.mp4`
- Duration: 4:26.633 (7,999 frames at 30 fps)
- SHA-256: `2c86325848f7024d64c44926bc6ab5168b5afdbeaac22841fa49174d1e096d5b`
- Base: `Prompts/fake-trap-2.mp4`
- Narration donor: `Prompts/fake-trap-1.mp4`
- Live visual donor: `course-assets/fake-trap/fake-trap.mp4`, the exact live path read from `LESSON_VIDEOS`
- Build script: `scripts/video/build_fake_trap_v1.py`
- Status: rendered and technically verified; perceptual listening remains a human checkpoint (see Limitations).

The build does not modify the live video, either raw candidate, `index.html`, the lesson Markdown, the board JPGs, or the tracker. Protected-file hashes were checked after rendering and all remained unchanged.

## Narration edit map

### Complete four-motive explanation

- Donor: `Prompts/fake-trap-1.mp4`, frames 2604–3544 (1:26.800–1:58.133).
- Destination: replaces candidate 2's thin list after its introduction; output 1:14.700–1:46.033.
- Visual: canonical `fake-trap-reasons.jpg` board.
- Gain: +0.8 dB, based on the measured candidate mix difference.
- Join feasibility: the whole teaching beat begins and ends in low-level gaps. Sample jumps at the output joins are 0.00165 and 0.00208 full scale; no click-sized discontinuity was measured.
- Complete inserted passage, verified from the rendered transcript:

  > First is money. Generating outrage leads to increased clicks, which translates directly to financial profit. Second is power. Manipulating public belief is a deliberate tactic to influence how people vote, protest, and spend their money. Third is fame. Viral content generates followers. The material does not actually need to be true in order to spread rapidly across platforms. Fourth is cruelty. Some fakes are designed entirely to humiliate a targeted individual, a tactic seen frequently in school environments.

This donor passage is retained as one continuous passage; it is not assembled item by item.

### Unsupported detector claim removed

- Removed from `Prompts/fake-trap-2.mp4`: frames 3314–3540 (1:50.467–1:58.000), the complete sentence:

  > Because software cannot reliably grade other software, the responsibility for finding the truth falls on human investigation.

- Destination edit: output boundary 2:11.467, from “It is not definitive proof” directly into “Fakes travel quickly when they spike your emotions.”
- The cut is on source scene boundaries and low-level audio. The measured sample jump is 0.00308 full scale.
- The rendered transcript contains no version of the removed claim.

### Conclusion reordered before the hard close

- Moved same-file donor: `Prompts/fake-trap-2.mp4`, frames 7219–7475 (4:00.633–4:09.167).
- Destination: output 4:05.467–4:14.000, after the Take It Down/no-fault guidance and before the close.
- Passage:

  > Your eyes still work perfectly for reading, judging, and enjoying the fiction you choose to watch. They just stopped working as a lie detector in the digital age.

- The hard close then runs at output 4:14.000–4:22.633:

  > So, always remember the ultimate rule. Seeing or hearing isn't proof anymore. Check the source, not the pixels.

- A four-second settled close hold follows. No scene or narration appears after the hard close.
- The moved conclusion and close are from the same source voice. Their measured join is low-level, with a 0.00208 full-scale sample jump.

No automatic one-second teaching pauses were added. Natural source and donor gaps were preserved.

## Visual and production changes

These are implemented treatments, not proposals:

- 0:13.333–0:33.500 — `fake-trap-comparison.jpg`: full board, complete Before AI card, complete AI Era card, then full-board takeaway banner.
- 0:46.967–0:56.567 — candidate 1's drawn harmless-hockey-joke sequence replaces candidate 2's photo-real trophy imagery while candidate 2's narration remains.
- 1:05.033–1:46.033 — `fake-trap-reasons.jpg`: full board and takeaway banner, then complete-card camera/highlight sequence for Money, Power, Fame, and Cruelty.
- 2:20.233–2:24.767 — `fake-trap-follow-the-source.jpg`: compact full board, deliberately unmarked.
- 2:24.767–3:14.933 — `fake-trap-checks.jpg`: full board with complete-card rings for Source, Context, and Corroboration, followed by the takeaway banner.
- 3:49.833–3:57.833 — live video's neutral platform-report/NCMEC diagram replaces candidate 2's large displayed CyberTipline URL. Its final frame is held for 21 frames to cover the full source span.
- 4:14.000 onward — standard close is final and remains settled through the tail.

The build uses no corner mark. Corner cleanup reports 1,194 cloned frames, 2,830 inpainted frames, and zero declined frames.

## Verification

- Full video decode: pass, 7,999/7,999 frames.
- Output timing: pass, exactly 30 fps and 266.633 seconds.
- Rendered audio transcription: 736 timestamped words; all four motives are present, the unsupported detector sentence is absent, and the moved conclusion precedes the close.
- Corrected video audio matches the first full verification encode byte-for-byte after decoding (`MD5 a57facd273aa4fef61b699b08a0ead88`).
- Six four-second contact sheets reviewed across the entire video. The compact source board was confirmed at 2:24 after correcting an internal board-name collision.
- Sixteen every-frame transition strips reviewed. Fifteen pass the automatic stale-island gate. The single automatic failure at frame 2241 is a false positive: it is the continuous camera move into the Money card at an audio-only donor boundary, not an intervening stale visual. Manual strip review confirms a continuous board move followed by a stable Money view.
- All actual source/board/donor transitions show a single intended cut or the source's intended reveal; no one-to-six-frame stale visual island was found.
- Board state sheets confirm legible full views and complete-card highlights. The standard close remains unchanged and final.

## Limitations and human checkpoint

This environment provided frame-accurate visual inspection, full decode, timestamped speech recognition, silence detection, and sample-level seam measurements, but it did not provide perceptual audio playback to the reviewer. A human should listen to the following joins before approval:

- 1:14.700 — candidate 2 introduction into candidate 1's four-motive passage; check the subtle voice/delivery change.
- 1:46.033 — candidate 1 passage back into candidate 2's detector passage.
- 2:11.467 — unsupported detector sentence removal.
- 4:05.467 — Take It Down/no-fault guidance into the moved conclusion.
- 4:14.000 — moved conclusion into the hard close.

The cross-candidate motive graft may have a detectable delivery/generation shift even though its loudness was adjusted and its joins are technically clean. If that shift is distracting in listening, do not deploy this candidate without revisiting the donor choice or rerolling that complete beat.

The superseded first encode was retained, not deleted, at `video-audit/fake-trap-repair-2026-09-18/fake-trap-v1-superseded-board-name-collision.mp4`. It is audit-only and should not be used; it omitted the compact source board because `source` is a reserved visual name in the renderer.
