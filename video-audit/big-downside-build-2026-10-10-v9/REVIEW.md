# Big Downside v9 — Roll 2 visual pass

User approval: “Build it please,” following the six-scene Roll 2 visual shortlist. This is a visual-only revision of v7, with the same narration and 4:10.47 runtime. It is a review candidate; no installation, commit, or publishing is included.

Candidate: `Prompts/big-downside-v9.mp4` (1280×720, 30 fps, 7,514 frames).

## Changed pictures

Times are output locations, with end times exclusive. All donor footage is from `Prompts/big-downside-2.mp4`. Retiming affects pictures only. Each selected sequence reaches its intended final state.

| Output | Roll 2 source | Treatment and teaching purpose |
|---|---|---|
| 0:22.80–0:31.67 | 0:30.20–0:41.50 | Rules are crossed out and become a learned network. A timing anchor aligns the network with “Instead.” |
| 0:31.67–0:36.37 | 0:41.50–0:45.50 | Dog on a chat screen during the Spot example, then return to the existing incomplete-explanation imagery. |
| 1:24.17–1:33.63 | 1:46.70–1:58.37 | Requests hit the guardrail; a later request passes through and reaches the model before the jailbreak board arrives. |
| 2:02.30–2:05.67 | 2:46.60–2:51.23 | The ordinary-looking voice request appears during “Every individual request might look harmless on its own.” Return to the existing combined-harm diagram for “but the sum…” |
| 2:33.73–2:43.07 | 3:04.83–3:15.97 | The complete agent-goal animation shows a boundary, an unauthorized detour, and the goal reached. Replaces the vacuum/execution-button portion during unintended goal pursuit. Holds the final state for the last 20 frames, then cuts directly to the restricted-server scene. |
| 2:57.13–3:01.47 | 3:11.63–3:15.97 | During the incident's communication sentence, the route reminder now reaches the goal. V7's excerpt stopped before this payoff. |
| 3:53.27–4:01.80 | 4:47.37–4:52.37 | Testing and updating loop continues through the continuous-testing sentence. The source animation is slowed to fill the existing narration. |

The learning-network sequence uses an anchor at “Instead.” The wrong-route sequence holds its completed state for the last 20 frames. Other inserts map their complete source span uniformly onto the listed output span. Exact frame mappings are in `edit-manifest.json` and `build_big_downside_v9.py`.

## Boards and close

All four canonical boards, full-view framing, highlighting coordinates and spoken onsets are inherited from v7. All canonical JPG hashes were checked before rendering. No course-board recreation is introduced by the donor scenes.

| Board | Output spans | Treatment |
|---|---|---|
| Layers of Protection | 0:50.97–1:11.77 | Unchanged full view; Safety Training → Screen for Harm → Limit What AI Can Do → takeaway. |
| Why Jailbreaks Keep Appearing | 1:33.63–1:49.53 | Unchanged full view; defenders' sign → attacker's sign → takeaway. |
| The Voice-Clone Scam | 2:08.73–2:24.03 | Unchanged full view and four step outlines. |
| A Test Became a Real Cyberattack | 2:47.73–2:57.13; 3:01.47–3:12.97; 3:16.97–3:20.73 | Unchanged board timing and outlines. The intervening route excerpt now completes. |
| Closing Message | 4:01.80–4:10.47 | Same canonical white asset, 48-frame hold and 150-frame push to 1.2×; 62-frame settled tail. Arrives after the testing sentence. |

Longest continuous teaching-board run remains **20.80 seconds**. No new relevant protection-layer drawing was approved for that run. The voice-board 1.47-second unmarked opening retains v7's spoken-onset exception.

## Build and verification

Pictures are rebuilt from the original source rolls and v7's canonical board rendering instructions, avoiding an additional video compression generation for unchanged shots. The earlier v6 donor remains part of v7's already assembled audio. The complete v7 AAC stream is copied without re-encoding.

Build: `.video-venv/bin/python scripts/video/build_big_downside_v9.py`

QA: `.video-venv/bin/python scripts/video/qa_big_downside_v9.py`

Verification of the encoded v9 candidate is complete within the perception limits below:

- Full sequential decode: **7,514 frames, 1280×720, 30 fps, 250.4667 seconds**.
- **Exact AAC-payload and decoded-PCM equality with v7.** No narration, timing, levels, or pauses changed.
- Sixteen sampled board frames match their original render references within the declared tolerance. Ninety-eight samples of unaffected pictures match v7 within compression tolerance.
- All protected file hashes remained unchanged during this build, including the existing modified `index.html`, source rolls, v7 candidate, canonical boards, lesson Markdown, and installed course video. The Big Downside section signature also matches.
- All newly introduced boundaries pass the transition detector. The final route exit at frame **4892** was inspected: the completed route cuts directly to the server, with no intervening execution-button picture.
- The full-file transition detector still flags two inherited boundaries, **5032** and **5789**, and reports exit status 1. Their v9 strips were inspected: 5031 is a normal server-animation motion step immediately before the board cut; the audit-log drawing at 5789 has a native fade-in. Neither inspected strip contains a stale intermediate graphic. The unmodified detector report remains in `transitions/transition-guard.json`; these are manual adjudications, not an automatic pass.
- Engine-corner cleanup used 2,935 paper-clone frames and 2,019 glyph-inpaint frames. No cleanup frame was left untreated. No new images, speech, pauses, or factual labels were generated.
- Before/after excerpts below each decoded to their expected frame count. Their audio is for review; the full candidate retains v7's original AAC stream exactly.

Candidate SHA-256: `5a99c0cefde7c5910a654c456cf105d9e2e164cb4a4bbe2ce7b17dd53488a1b2`.

## Contextual before/after comparisons

Each excerpt shows v7 on the left and v9 on the right, with the shared narration and surrounding context.

- [Guardrail bypass — 1:22.00–1:35.70](/Users/davidobrien/Developer/AI-Training/video-audit/big-downside-build-2026-10-10-v9/compare-guardrail.mp4)
- [Complete wrong route — 2:31.70–2:44.40](/Users/davidobrien/Developer/AI-Training/video-audit/big-downside-build-2026-10-10-v9/compare-wrong-route.mp4)
- [Testing cycle and close — 3:51.30–4:04.50](/Users/davidobrien/Developer/AI-Training/video-audit/big-downside-build-2026-10-10-v9/compare-testing-cycle.mp4)

![Wrong-route comparison poster](/Users/davidobrien/Developer/AI-Training/video-audit/big-downside-build-2026-10-10-v9/compare-wrong-route.jpg)

## Inherited limitations

This visual revision does not certify the narration as ready to ship. V7's remaining omissions persist: screening outgoing harmful answers, explicitly calling the number already known, and concrete spoken permissions examples. Four required wording entries remain paraphrased. Its illustrative capability chart and the donor-audio joins retain their earlier review qualifications.

Direct listening and real-time end-to-end motion perception are not available to this agent. Encoded-frame inspection, source timing, and audio equality checks do not substitute for them. The candidate and contextual comparisons are provided for playback review.
