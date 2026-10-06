# Tokens v13 — review candidate

Built 2026-10-04 from the approved roll-4 repair plan, with the complete roll-6 conversion sentence. Candidate: `Prompts/tokens-v13.mp4`. Duration 3:58.633; 7,159 frames at 30 fps, 1280×720. No installation, commit, or publishing performed.

## Implemented edit

The narration opens with computers processing numbers, follows the full Avengers exchange and both conversion questions, explains the whole-word limitation, then introduces reusable chunks. It preserves the complete examples, vocabulary/ID definition before the cat board, the Send steps and worked IDs, the return to words, and both closing lines. Removed excess whole-word logistics, the later logistics aside, the backward network aside, and the leaked “Deliberate final tone” instruction. The Send summary now follows its worked example.

Roll 6 supplies the complete opening conversion sentence. Its gain is +1.2875 dB; joins use 5 ms room-tone ramps. No teaching pauses or narration speed changes were added. Closing room tone supplies the standard hold/push/settle.

| Output seconds | Source seconds | Beat |
|---|---|---|
| 0.000–8.733 | Roll 4: 0.000–8.733 | Opening everyday text |
| 8.733–13.667 | Roll 6: 6.233–11.167 | Exact conversion sentence |
| 13.667–68.467 | Roll 4: 13.533–68.333 | Chat, both questions, whole-word limitation |
| 68.467–182.933 | Roll 4: 82.267–196.733 | Chunks, complete examples, vocabulary, cat |
| 182.933–204.333 | Roll 4: 202.700–224.100 | Send: three steps |
| 204.333–214.400 | Roll 4: 227.733–237.800 | Send: worked IDs |
| 214.400–218.033 | Roll 4: 224.100–227.733 | Send: summary moved after IDs |
| 218.033–228.033 | Roll 4: 237.800–247.800 | Reply IDs to readable text |
| 228.033–234.333 | Roll 4: 252.700–259.000 | Exact close |

## Visual treatment

All five canonical course JPGs are used. Chat, cat, and Send use full views with narration-timed section rings. The examples board opens unmarked, then pans over complete rows with a shared-un comparison. Token IDs are absent from that examples board. Course rings remain fixed at 4 px. The close holds 48 frames, pushes to 1.2× over 150 frames, then settles for 120 frames.

Useful source illustrations remain: phone/processor, hypothetical dictionary, failed lookups, building blocks, finite-chunk recombination, corpus/program/vocabulary, address, and reply decoding. Targeted foreground extraction reduces the recurring wallpaper. Simple question, vocabulary, and ID diagrams replace confusing source material. Faint source animation/morphing artifacts remain in retained generated illustrations; they have not been assessed during continuous playback.

Longest continuous course-board run is cat plus Send, 59.33 seconds. The dense examples board runs 49.73 seconds with whole-row movement. No filler breaks inserted.

V12 was an intermediate candidate. Encoded inspection caught an incorrect building-block donor range and an extra sentence appearing at the end of the reply animation. V13 corrects output frames 2054–2265 using roll 4 frames 2263–2388, and output 6541–6840 using roll 6 frames 6180–6474. V13 inherits the assembled AAC audio bit for bit from v12.

## Verification

- Fully decoded all 7,159 frames at the expected dimensions and rate.
- Transition guard: all 20 boundaries passed; every-frame strips inspected in overview sheets, including both corrected legs.
- Canonical board/ring states inspected. Final samples checked against canonical render and parent encoded frames. V13 is a second visual encode, with maximum parent-sample mean pixel difference 2.447/255; the per-generation limit is 3/255.
- AAC payload matches v12 exactly: `3023314481e22f67c00bb266442367790c63d77a50ce7ebab6012cbf750ac296`.
- Decoded/reference PCM correlation: 0.999984; clipped samples: 0.
- Candidate SHA-256: `09529f7d738a38e2a21eeb654b4b3b5d220e16288a8fcb7b853c5a7f4a78c8b5`.
- Live Tokens MP4, lesson, page, and canonical JPG hashes match the build's protected-file snapshot. Existing unrelated workspace changes preserved. `git diff --check` passed.

## Narration review limitation

The complete final small.en transcript was read against the lesson. It contains the required arc, all worked examples and numbers, explicit space handling, token-ID/meaning distinction, Send sequence, reverse conversion, and closing lines. The transcript is copied here because v13 has identical audio. It is raw ASR, not a corrected script.

**Direct listening and end-to-end playback with sound were not performed. This is a review candidate, not a certified KEEP or shipping verdict.** ASR renders “vable” as “vol,” “belie” as “believe” in one place, the URL adjective as “desperate,” and “the animal” as “be animal.” Those are listening checkpoints, not proven narration errors. Audition 1:17–1:21, 2:01–2:05, 2:46–2:48, and 3:24–3:34, plus the opening donor join at 0:08.73/0:13.67 and other joins saved under `encoded-check/join-clips/`. Continuous playback is also needed to judge animation and pacing. No claim of direct hearing is made.
