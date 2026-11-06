# Learn with AI v15 — narrow pacing repair

Owner review of v14, November 6: questioned 1:46–2:00 and preferred keeping the boards over the repeated laptop drawing at 2:21 and 2:57. Apply only these three changes; preserve v14 and rebuild from its pristine raw sources.

## Changes relative to v14

1. Remove 1:45.600–2:00.200 (438 frames / 14.600 seconds). This removes two added sentences: “Deciding upfront whether you need to drill facts for a test or break down a tough new theory makes a significant difference. It stops you from studying irrelevant information and keeps you actively engaged instead of passively letting the AI do the work.” The current lesson already distinguishes the two tools on the preceding board; neither sentence is required. Keep “Check your class materials. Ask your teacher if something doesn't line up.” and join directly to “Let's focus entirely on the study tool track.” The boundaries sit in measured quiet portions of the source, outside both complete sentences. No added pause.
2. Replace the repeated materials drawing at old 2:21.000–2:25.000 with the existing How Gemini Notebook Works board. Preserve its full framing and active You Upload outline. New output span: 2:06.400–2:10.400, frames 3792–3912 exclusive. The audio is unchanged.
3. Replace the repeated materials drawing at old 2:55.600–2:59.600 (including the owner's 2:57 observation) with the existing Four Moves board, retaining the complete Give It the Full Picture card and its outline. New output span: 2:41.000–2:45.000, frames 4830–4950 exclusive. The audio is unchanged.

The longer board holds are intentional under the owner's preference for these specific passages. How It Works runs 24.033 seconds continuously; Four Moves runs 42.267 seconds continuously, including its introduction and four changing card views, before the citation diagram. No new supporting illustration is needed. The first board's longest run remains 19.300 seconds.

## Build and checks

Target: `Prompts/learn-with-ai-v15.mp4`, 6,948 frames / 3:51.600. Builder: `scripts/video/build_learn_with_ai_v15.py`. The donor, speech-level adjustment, highlights, canonical assets, and standard close retain the v14 treatment, rebased by 438 frames after the cut.

Pre-encode PCM comparison confirms that the v15 assembly equals the v14 assembly with exactly the selected interval removed, except for the 8 ms boundary ramps at the new join. The two visual-only changes cause no audio change. See `audio-preservation.json`.

Finished-file verification will decode every frame, check timing and audio correlation, freshly transcribe the encoded MP4, inspect the new join, inspect both retained-board spans and their endpoints, and check the final frame. Direct listening and full-speed audiovisual playback are not available and will not be reported as passed. This build does not authorize installation, commit, or deployment.
