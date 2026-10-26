# Unexpected Results v6 — approved combined edit

The user approved the prior best-of plan on October 23, 2026: roll 1’s story and close, roll 3’s texting, and the retained cane-toad and AI takeaway sections. The prior plan also includes roll 3’s two-sentence acknowledgment of informed forecasts. Scope: full production pass; review candidate only.

## Audio timeline

| Output | Source | Source interval | Beat |
|---|---|---|---|
| 0:00.00–0:09.90 | 1 | 0:00.00–0:09.90 | opening |
| 0:09.90–1:57.97 | 1 | 0:38.10–2:26.17 | hanoi |
| 1:57.97–2:03.37 | 1 | 2:31.30–2:36.70 | examples-intro |
| 2:03.37–2:23.57 | 3 | 2:35.93–2:56.13 | texting |
| 2:23.57–2:32.03 | v4 | 1:51.80–2:00.27 | cane-toads |
| 2:32.03–2:38.00 | 1 | 3:31.30–3:37.27 | ai-handoff |
| 2:38.00–2:47.73 | 3 | 3:26.90–3:36.63 | informed-forecasts |
| 2:47.73–3:14.27 | v4 | 2:10.60–2:37.13 | ai-takeaway |
| 3:14.27–3:22.93 | 1 | 4:23.83–4:32.50 | close |
| 3:22.93–3:24.93 | 1 | matched room tone | close-hold |

Source file identities and SHA-256 hashes are in `edit-manifest.json`. `planned-narration.txt` holds the full selected text from source ASR; it is not a transcript of the output.

## Implementation decisions within the approved plan

- Cut at quiet waveform intervals, retaining complete words and natural breathing room. All nonzero cut endpoints measure below −48 dBFS in a 20 ms window. Five-millisecond edge fades; no inserted pauses between teaching beats.
- Match sources by measured integrated loudness: raw roll 1 story −19.64 LUFS, roll 3 texting −20.37 LUFS, older AI takeaway −14.65 LUFS. Apply +0.7 dB to roll 3 and −5.0 dB to v4; keep roll 1 unchanged. No time stretching.
- Preserve the rat-story animation. Sequence frames show that the first rat loses its tail at source 1:27, moves alive to the next step, and produces offspring before a tailed offspring starts the next cycle. The prior single-frame concern at 1:33 does not justify removing this useful animation. Continuous audiovisual playback remains unperformed.
- Replace the entire unsupported population-chart scene, source roll 1 frames 3882–4076 (2:09.40–2:15.90), with the preceding mountain-of-tails illustration. Preserve the rest of the story’s original picture and timing.
- Cover the five source frames before the first rat illustration at the opening story cut. This prevents a flash of the discarded forecasting illustration.
- Use the exact current two-card board, stationary full view. Unmarked introduction; 4 px purple and teal whole-card rings at the spoken example onsets. Retain the phone/toad split illustration from source roll 1 3:22.30–3:29.30 as the seven-second break.
- Use coherent roll 1 AI illustrations under the donor audio. Remove the diagnostic-network diagram, the toad-covered continent, the old board rendering, and generated closing/outro. No new imagery required.
- Canonical closing asset, standard 48-frame hold / 150-frame push to 1.2× / settled hold, with the complete roll 1 closing sentence and two seconds of matched room tone afterward.
- Clean the Notebook corner mark in kept native frames using the shared paper-clone/glyph-inpaint routine. Render raw picture once; the older finished v4 supplies audio only because its original raw narration is unavailable.

## Remaining listening verification

The environment supplies ASR and frame/numeric checks but no direct audio audition. Do not certify pronunciation, voice continuity, or seamless joins from those checks. The completed candidate and join review reel are for that review; installation/shipping is separate.
