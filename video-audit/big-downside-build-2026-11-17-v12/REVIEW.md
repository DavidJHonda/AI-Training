# Big Downside — version 5 production edit

Built 2026-11-17 under the user's approval to use uploaded version 5 as the base, repair narration from the identified donors, and apply the proposed visuals.

Candidate: `Prompts/big-downside-v12.mp4`. Duration **4:42.667**, 8,480 frames, 1280×720 at 30 fps, H.264/AAC, 45,507,670 bytes. SHA-256: `c4e6fc06bbf86b276cc07184788ed402858459cd1b4ac23ee08b45b37e552a63`.

**Superseded by v13 before handoff.** The encoded course-board outlines measured thinner than the shared renderer standard; v13 retains the same narration and visual timing while correcting the outlines. Direct review of v13 governs the delivered candidate.

**Not certified ready to ship.** Direct listening and an end-to-end motion watch have not been performed. Transcript, sampled frames, every-frame transition strips, and signal measurements are separate evidence and do not certify pronunciation, cadence, or voice continuity. Meaning-preserving paraphrases are accepted throughout.

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

## Verification

- All 8,480 frames decoded; audio and video both measure 282.667 seconds.
- Encoded audio correlates 0.99998589 with the planned assembly. Peak is −1.209 dBFS, with zero clipped samples.
- Every audio seam is declared. The immediate 20 ms regions are quiet (worst measured side approximately −63 dBFS); no abrupt high-amplitude sample jump was detected. These measurements do not replace listening.
- Transition guard passed all 22 checked boundaries. Every frame in the ±12-frame strips was inspected through the six review grids. No stale-picture island was found.
- All six encoded contact sheets were inspected, sampling every four seconds across the entire video. Full-size previews were also checked for labels, board legibility, highlight placement, and the closing frame.
- Original uploads, canonical board assets, and lesson Markdown hashes are unchanged. No course installation or publishing occurred.
- Complete exported-file transcript reviewed: all 695 words retain the intended teaching, including all three donor passages. ASR warnings did not prevent a complete transcript.
- Ring measurement found 2–3 px solid cores on several course-board outlines. Superseded by v13 using the shared course renderer; this v12 measurement is not a pass.

## Listening handoff

`narration-join-reel.mp4` is a **42-second local reel** with three seconds before and four seconds after each of the six boundaries around the three donor passages. Each excerpt labels its location in the full candidate. `audio-joins/` also contains all twelve edit seams as individual WAV excerpts.

Remaining review: listen for voice continuity, cadence, pronunciation, and natural joins at **0:54.067, 1:16.067, 3:02.400, 3:17.533, 4:20.833, and 4:32.067**, then watch/listen to the complete candidate. This is not a request to upload or regenerate anything.
