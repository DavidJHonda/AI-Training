# How an LLM Works — v9 Review Handoff

## Status

Ready for owner review. This is a review build only; it has not been copied into the live course or deployed.

- Candidate: `/Users/davidobrien/Developer/AI-Training/Prompts/how-an-llm-works-v9.mp4`
- Format: 1280×720, 30 fps, 3:29.00, H.264/AAC mono
- Render SHA-256: `d360ad68fcf57f23e38a44559a0d0cecf38bf0ff74f84a870bf5fb6648a5fb2d`
- Build script: `/Users/davidobrien/Developer/AI-Training/scripts/video/build_how_an_llm_works_v9_review.py`
- Machine-readable manifest: `edit-manifest.json`

## Editorial construction

This is a full production repair assembled around the complete narration from `Prompts/llm-short-2.mp4`. The portrait Notebook video was not used as the final presentation. The finished video is landscape and combines the existing lesson boards with selected landscape Notebook drawings from `Prompts/how-an-llm-works-reroll-2.mp4`.

The narration runs continuously from source frame 0 through frame 6150 (0:00–3:25). There are no narration cuts, grafts, or added pauses. A four-second matched-room-tone close hold follows the natural narration tail.

Notebook visual spans:

- Output 0:53.30–1:01.28 from reroll source 1:34.00–1:41.98: learned structural patterns.
- Output 1:09.26–1:15.92 from reroll source 2:56.00–2:57.93, then held: completed next-token probability drawing.
- Output 2:58.72–3:03.70 from reroll source 2:58.00–3:02.98: predictive text.
- Output 3:15.80–3:19.70 from reroll source 3:13.50–3:17.40: autoregressive loop.

Board treatment:

- “What’s an LLM?” — compact, full-board treatment with timed emphasis.
- “Two Ideas Behind Every Answer” — compact overview plus section callbacks.
- “How Training Works” — compact.
- “How AI Learns Patterns” — compact, held through the broader-pattern explanation.
- “Same Word. Different Odds.” — dense; full view, left example, right example, then pullback.
- “One Word at a Time” — compact, intercut with the predictive-text and loop drawings.
- Standard close — starts at 3:19.70 and settles for the final hold.

## Verification

- Complete timestamped transcript generated: 40 segments across 3:29.
- Transition guard: PASS at all 18 declared visual boundaries; 0 failures.
- Probability drawing begins on the completed diagram rather than a blank panel.
- Silence scan found only natural speech gaps; no unintended inserted pause was detected.
- Corner-mark cleanup: 705 frames cloned, 0 frames inpainted, 0 declined cases.
- Source protection: the narration donor, reroll visual donor, lesson Markdown, and all seven canonical board JPGs match their recorded pre-build SHA-256 hashes.
- Output metadata: 6270 frames, 1280×720, 30 fps, 209.00 seconds.

## Required human check before shipping

This environment supported complete transcript, frame-state, contact-sheet, transition, metadata, and silence analysis, but not a literal real-time end-to-end listening/watch pass. Before replacing the live video, listen once from beginning to end for voice quality and prosody. Pay particular attention around 1:54.48: both ASR passes render the intended phrase as “The patterns built,” but a human should confirm it sounds natural and unambiguous.

The live lesson, `index.html`, canonical boards, donor videos, and course video remain unchanged.
