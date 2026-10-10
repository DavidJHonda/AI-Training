# Big Downside v8 — Roll 2 visual pass

**Superseded by v9 during visual QA.** V8 passed frame-count, audio equality, board-reference and unaffected-picture checks, but its new route sequence returned to the old execution-button picture for 20 frames before the server scene. V9 extends the route's final state through those frames. Use v9 for review.

User approval: “Build it please,” following the six-scene Roll 2 visual shortlist. This is a visual-only revision of v7, with the same narration and 4:10.47 runtime. It is a review candidate; no installation, commit, or publishing is included.

Candidate: `Prompts/big-downside-v8.mp4` (1280×720, 30 fps, 7,514 frames).

## Changed pictures

Times are output locations, with end times exclusive. All donor footage is from `Prompts/big-downside-2.mp4`. Retiming affects pictures only. Each selected sequence reaches its intended final state.

| Output | Roll 2 source | Treatment and teaching purpose |
|---|---|---|
| 0:22.80–0:31.67 | 0:30.20–0:41.50 | Rules are crossed out and become a learned network. A timing anchor aligns the network with “Instead.” |
| 0:31.67–0:36.37 | 0:41.50–0:45.50 | Dog on a chat screen during the Spot example, then return to the existing incomplete-explanation imagery. |
| 1:24.17–1:33.63 | 1:46.70–1:58.37 | Requests hit the guardrail; a later request passes through and reaches the model before the jailbreak board arrives. |
| 2:02.30–2:05.67 | 2:46.60–2:51.23 | The ordinary-looking voice request appears during “Every individual request might look harmless on its own.” Return to the existing combined-harm diagram for “but the sum…” |
| 2:33.73–2:42.40 | 3:04.83–3:15.97 | The complete agent-goal animation shows a boundary, an unauthorized detour, and the goal reached. Replaces the vacuum/execution-button portion during unintended goal pursuit. |
| 2:57.13–3:01.47 | 3:11.63–3:15.97 | During the incident's communication sentence, the route reminder now reaches the goal. V7's excerpt stopped before this payoff. |
| 3:53.27–4:01.80 | 4:47.37–4:52.37 | Testing and updating loop continues through the continuous-testing sentence. The source animation is slowed to fill the existing narration. |

The source sequence selected for the learning-network animation has two timing anchors; other inserts map their complete source span uniformly onto the listed output span. Exact frame mappings are in `edit-manifest.json` and `build_big_downside_v8.py`.

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

Build: `.video-venv/bin/python scripts/video/build_big_downside_v8.py`

QA: `.video-venv/bin/python scripts/video/qa_big_downside_v8.py`

`qa.json` confirms 7,514 decoded frames and exact AAC-payload and decoded-PCM equality with v7. Sixteen board samples and 98 unaffected-picture samples passed. The transition detector's two flags at frames 5032 and 5789 repeat v7's native animation-step and fade flags; decoded strips show no intervening graphic. All new boundaries passed automatic detection, but contextual visual inspection found the 20-frame execution-button return described above. Engine-corner cleanup is applied to every retained Notebook frame using the shared helper. No new images, speech, pauses, or factual labels are generated.

## Inherited limitations

This visual revision does not certify the narration as ready to ship. V7's remaining omissions persist: screening outgoing harmful answers, explicitly calling the number already known, and concrete spoken permissions examples. Four required wording entries remain paraphrased. Its illustrative capability chart and the donor-audio joins retain their earlier review qualifications.

Direct listening and real-time end-to-end motion perception are not available to this agent. Encoded-frame inspection, source timing, and audio equality checks do not substitute for them. The candidate and contextual comparisons are provided for playback review.
