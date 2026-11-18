# Big Downside — revised video from uploaded version 5

Built 2026-11-17 under the approved narration and visual plan. **Current review candidate: `Prompts/big-downside-v13.mp4`.**

Duration **4:42.667**, 8,480 frames, 1280×720 at 30 fps, H.264/AAC, 45,500,453 bytes. SHA-256: `0d2b879e8b9111b40fc5afcaa60c4da16180cec82e0cef6cbc1f88e09105bf0a`.

**Ready for owner review, with direct listening and an end-to-end motion watch still outstanding.** The build and technical checks are complete; no shipping certification is claimed. Meaning-preserving paraphrases pass. All requested narration repairs and visual updates are implemented. Version 13 supersedes v12 solely to use the shared course-board outline renderer; its audio is exactly identical after decoding.

## Narration changes

Version 5 supplies the main narrative. Three complete passages come from the other local uploads:

| Output span | Source | Repair |
|---|---|---|
| 0:54.067–1:16.067 | Version 6, 1:17.233–1:39.233 | Explains training, incoming/outgoing screening, and human approval for important actions. |
| 3:02.400–3:17.533 | Version 6, 4:10.300–4:25.433 | Establishes the cybersecurity test, software tools, restricted environment, and reduced safeguards. |
| 4:20.833–4:32.067 | Version 4, 4:14.867–4:26.100 | Explains renewed safety testing as capabilities grow, replacing the claim that all earlier safeguards become obsolete. |

Removed the invented internal refusal mechanism, external-only safety framing, temporary-dam metaphor, mathematical aside, macro-level lead-in, and highest-tier ranking. Kept the meaningful refusal/rewording example, ordinary-capability misuse, complete scam sequence and callback, intended-limits explanation, incident aftermath, red teams, and the approved close. No extra pauses were inserted between teaching beats; cut points fall inside existing gaps. Donor gains are −0.8 dB for version 6 and +0.3 dB for version 4, with 5 ms fades into source room tone.

## Visual changes

All three teaching boards use the exact current canonical JPGs, at full readable view, with one 4 px outline at a time. Board introductions are unmarked. No card dives or new banners were added.

| Board | Output spans | Treatment |
|---|---|---|
| AI Safety Layers | 0:50.933–1:16.067 | Train for Safety → Screen for Harm → Limit What AI Can Do. One concise three-card walk. |
| The Voice-Clone Scam | 1:54.733–2:11.600; 2:18.600–2:38.133 | Voice Clip → Voice Cloned → Fake Call → callback banner. The second step is visible before cutting to the preserved voice-generation/fake-call scenes. Both board shots stay under 20 seconds. |
| A Test Became a Real Cyberattack | 3:17.533–3:39.033 | Assignment → Boundary Crossed → Harm, followed by the no-human-direction and collaboration/scoring scenes. |
| Closing Message | 4:32.067–end | Current closing artwork; 48-frame initial hold, 150-frame push, 120-frame settled hold. Literal final frame checked. |

Retained useful software/network, jailbreaking, ordinary-capability, voice-generation, growing-reach, limits, sandbox/tools, collaboration/scoring, red-team, and continuing-testing graphics. Replaced the unsupported refusal-path diagram with a simple request/response comparison. Corrected section titles and the incident month. Removed the breaking dam, obsolete-guards/99% sequence, and the invented agent-count label. Cleaned the Notebook corner mark on retained source frames. Full source hashes and exact output/source frames are in `edit-manifest.json`.

## Verification of the delivered v13 file

- All 8,480 frames decode. Video and audio both measure 282.667 seconds.
- Audio is byte-identical, after PCM decoding, to v12's completely reviewed 695-word exported-file transcript. All essential teaching and all three replacement passages are present. Transcript evidence: `../big-downside-build-2026-11-17-v12/render-transcript/big-downside-v12.txt`; identity evidence: `audio-identity-to-v12.json`. No transcription result is presented as direct listening.
- Encoded audio correlation to the assembly is 0.99998589; peak -1.209 dBFS, with 0 clipped samples. All twelve seams fall in quiet gaps, with 5 ms room-tone fades. Signal checks do not certify how the voices sound together.
- Transition guard passes all 22 edited boundaries. Every frame in the ±12-frame boundary strips and the complete four-second-sampled contact sheets were visually inspected on this export. No stale-picture island was found.
- Course-board outlines use the same `ken_burns_path.draw_ring` and `ring_px(720)` as the established course renderer. The encoded board-only measurement has 133 samples, median 4.0 px, range 4.0–5.0 px at the tool's solid-color threshold. This threshold varies with anti-aliasing and compression; the requested drawing width is a fixed 4 px. Unrelated colored shapes in supporting scenes are excluded from this summary. All ten ring targets also passed a short encoded calibration before the full build.
- Current canonical boards remain complete and legible. Highlights follow the named cards and callback banner. The canonical closing message is the literal final frame, with the standard 48/150/120-frame hold/push/settled timing.
- Source videos, canonical board JPGs, and lesson Markdown hashes are unchanged. No installation or publishing occurred.

## Listening handoff

`narration-join-reel.mp4` is a **42-second local reel** containing three seconds before and four seconds after each cross-roll boundary. Each excerpt labels its timestamp in the full candidate. `audio-joins/` holds all twelve edit seams individually.

The six donor joins are at **0:54.067, 1:16.067, 3:02.400, 3:17.533, 4:20.833, and 4:32.067**. They still need direct listening for voice continuity, cadence, pronunciation, and natural pacing. The complete candidate also needs an end-to-end watch/listen before it can be called ready to ship.

## Reproduction

Builder: `scripts/video/build_big_downside_v13.py`, using the v12 timeline/visual renderer plus the shared course ring implementation. `edit-manifest.json` records exact source/output spans, gains, asset hashes, and final hash. `verify_export.py` checks the actual export and makes the six-join reel. Existing numbered candidates are never overwritten.
