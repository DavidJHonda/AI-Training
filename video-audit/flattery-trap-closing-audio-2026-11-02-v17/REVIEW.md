# Flattery Trap v17 — closing onset repair

User hears an off-sounding closing splice and a short blip. Analysis found a sharp waveform attack at output 232.70054 seconds, inherited from archived standalone v13 at source 255.70054. The adjacent quiet interval and inserted one-second pause contain no comparable transient. This is a plausible cause of the reported blip; perceptual listening has not been performed.

Repair: matched source ambience plus a 27ms raised-cosine onset at “Useful.” Total modified interval: 232.685–232.725 (40ms). No word cut, new speech, timing change, or picture change. Original edited PCM is used as the audio source to avoid another decode generation; every video packet is copied from v16.

Checks passed: bit-identical video elementary stream; 7264 frames at 30fps; unchanged 4:02.133 runtime; all planned PCM outside the 40ms interval identical; both closing lines confirmed by ASR on the encoded tail; encoded audio matches planned PCM. The encoded sample-to-sample jump at the onset fell from 0.12832 to 0.00287 (33.0dB reduction). This quantifies the transient reduction, not a perceptual sign-off.

Candidate: Prompts/flattery-trap-v17.mp4. Twelve-second before/after previews are before.mp4 and after.mp4 in this folder. Listening review is needed to decide whether the repair resolves the sound the user noticed. No installation, commit, or publication.
