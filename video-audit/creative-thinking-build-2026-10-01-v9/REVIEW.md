# Creative Thinking v9 — October reroll build

Built from the newly uploaded **roll 2**, following the October 1 comparison and the user’s “build it please” approval. The review candidate is `Prompts/creative-thinking-v9.mp4`: **3:08.13, 1280×720, 30 fps, 5,644 frames**. It is now installed and committed locally; batch deployment is pending.

## What changed

- Removed two complete redundant passages from roll 2: source **2:05.30–2:13.30** and **3:03.80–3:17.80**. These remove the repeated competitive-advantage statement and the exaggerated/repeated summary. All profession examples, four full habit instructions, seven required lines, and the two-line close remain.
- Retained roll 2’s voice throughout. No donor audio, added instructional pauses, or broad audio cleanup. Source PCM is preserved outside the two deletions, their 5 ms shoulders, and the closing room-tone tail.
- Replaced both Notebook teaching boards with the current canonical JPGs. Both open whole and unmarked, then zoom to complete cards with a single accent-colored outline. Rings use the shared `ring_px(720) = 4` setting after cropping.
- Replaced the Jobs/computer photographs with existing drawn technologist, hardware, and home-computer scenes from rolls 3 and 1.
- Added three supporting cutaways under unchanged narration: engineer/workshop, a path around an obstacle, and a wall of varied ideas. The longest uninterrupted board run is **24.2 seconds**, the explicit exception recorded in the approved plan. The practice board’s longest run is **20.7 seconds**.
- Kept the useful opening diagrams, performance comparison, AI/student illustrations, and the full “Not a Magic Gift” → daily-practice reveal. Repaired three malformed note labels in the student’s planning drawing using tracked overlays while retaining its source camera motion.
- Reused the expanding-options and star-selection drawings under the concise options/judgment bridge.
- Applied engine-corner cleanup to every retained/donor Notebook frame. Replaced the engine ending with the canonical close: 48-frame hold, 150-frame push to 1.2×, 30-frame settled hold; the canonical close is the literal final frame.

The internal v8 preview exposed an overly early excerpt for the what-if cutaway. V9 uses roll 2 frames **1740–1842** (0:58.00–1:01.40), which show the useful path around the obstacle. This visual-only refinement preserves v8’s audio and duration.

## Timeline for review

All ranges are half-open and use the delivered output timeline.

| Output | Treatment |
|---|---|
| 0:28.97–0:34.77 | Roll 3 drawn technologist, source frames 920–1095 |
| 0:34.77–0:40.27 | Roll 1 drawn hardware, source frames 1202–1344 |
| 0:40.27–0:44.73 | Roll 1 drawn home computer, source frames 1344–1553 |
| 1:01.00–1:25.20 | Canonical professions board: lawyer → entrepreneur → engineer |
| 1:25.20–1:28.60 | Roll 1 workshop, source frames 1740–1842 |
| 1:28.60–1:36.60 | Professions board returns for doctor |
| 1:52.60–1:58.77 | Existing student drawing with tracked label repair |
| **2:05.30** | First narration splice: daily practice → four-habit introduction |
| 2:05.30–2:26.00 | Canonical practice board: first habit → what-if |
| 2:26.00–2:31.80 | Alternate-path cutaway |
| 2:31.80–2:39.00 | Practice board: what-if → connect unrelated things |
| 2:39.00–2:43.10 | Idea-wall cutaway from roll 2 source frames 5740–5863 |
| 2:43.10–2:55.80 | Practice board returns for step away, then pulls back |
| **2:55.80** | Second narration splice: attention moves elsewhere → habits widen options |
| 2:55.80–2:58.20 | Option-network excerpt, roll 2 source frames 5580–5660 |
| 2:58.20–3:00.53 | Star selection, roll 2 source frames 5970–6079 |
| 3:00.53–3:08.13 | Canonical close, including short tail after final speech |

## Verification and limits

The retained teaching was checked against the full candidate transcript and the original beat-by-beat comparison. A base-model ASR pass incorrectly transcribed “isn't a magic gift” as “is a magic gift.” A targeted medium.en pass recovered **“That human advantage isn't a magic gift”**; the underlying retained PCM is unchanged. The supplemental result is recorded separately so the disagreement is visible.

Narration is **provisionally KEEP on transcript evidence**, with the approved excess removed and all essential points still RICH or TAUGHT. This is not a listening sign-off. Neither the complete audio nor its two joins has been auditioned, and the video has not been watched in real time end to end. Sequential decoded frames, contact sheets, and boundary evidence are the visual review method.

The listening points are **2:05.30** and **2:55.80**. Short context WAVs were generated during QA and reclaimed after local shipping; their source intervals and measurements remain recorded. Waveform checks place both cuts in low-level gaps; those measurements do not establish natural cadence or rule out perceptual artifacts.

Final encoded checks and source identities are recorded in `edit-manifest.json`, `qa/verification.json`, `qa/transitions/transition-guard.json`, and `qa/ring-stroke.txt`:

- Full decode: **5,644 frames, 30 fps, 188.133 seconds**; 1280×720.
- Transition guard: **19 boundaries passed, zero flagged stale-frame islands**. Boundary overview frames were inspected; the corrected cutaway’s every-frame entry/exit strips were inspected separately.
- Eight settled card states were inspected at full resolution in the encoded candidate. All active cards retain their complete illustration, heading, and text. Both board openings are unmarked full views.
- The highlight renderer uses the fixed shared 4 px setting independently of zoom. Color-threshold measurements read 4–5 solid pixels depending on color/rasterization. The lone 11.5 px gold detection is an illustration edge, confirmed by its saved crop, not an added highlight.
- Close: initial pill width 720 px, final width 864 px, exactly **1.2×**, with the prescribed hold/push/settle and the canonical final frame.
- Every retained/donor Notebook frame passed corner cleanup; zero declined frames.
- PCM is identical to the retained source outside the declared deletions and 5 ms join shoulders. V9’s encoded AAC stream is **identical to the fully transcribed v8 audio**, verified by SHA-256; see `audio-identity.json`.
- The two join neighborhoods measure approximately −59.5 and −69.6 dBFS in the assembled PCM. Encoded low-level gap measurements are in `qa/encoded-gap-measurements.json`.
- Source-video, lesson-Markdown, and canonical-board hashes remain unchanged.

Candidate SHA-256: `8b80e0df353698764e6f832fc1d7bd03f65221270ccf1878be53e2bc2748d172`.

**Status: shipped locally; queued for batch deployment.** User authorized shipping with “ship it” after the listening limitation was disclosed. This records authorization, not a claim that independent listening or end-to-end playback occurred.

Local commit: `27bef486987126b3581b3fcb7c416cba5a11aaed`. The installed and committed MP4 both match the approved v9 SHA-256. Only the canonical MP4 and Creative Thinking’s cache key (`20261001ship9`) were committed. The displayed runtime remains the accurate rounded “3 min.” Tracker was not accessed or modified; no push or deployment occurred. Regenerable audio/canvas scratch was reclaimed; raw generations, candidates, manifests, transcripts, and frame evidence remain.

## Reproduction

```sh
.video-venv/bin/python scripts/video/build_creative_thinking_v9.py
.video-venv/bin/python scripts/video/qa_creative_thinking_v9.py
```

The build refuses to overwrite a candidate. V9 imports the documented v8 builder and changes only the selected cutaway source interval. No shared renderer, live video, lesson reference, or tracker was changed by this build. Concurrent unrelated workspace changes were left alone.
