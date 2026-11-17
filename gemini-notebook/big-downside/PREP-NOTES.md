# Big Downside: revised video preparation

Prepared 2026-11-17 from the approved current lesson in `index.html`, its canonical boards and `lessons/big-downside.md`. The installed v11 video is still the older narration. This package is ready for fresh generation; no new MP4 has been generated or installed.

## Generate

Upload the five files in `upload/`: the Markdown and four JPGs. Paste `PROMPT.txt` into video customization, not into sources. Save the raw result as `Prompts/big-downside-reroll.mp4`, or the next unused reroll suffix. Preserve all raw rolls and existing candidates. The prompt is 486 words.

## Lesson progression

Greater capability creates greater risk through difficult control, harmful human use, and goals pursued outside intended limits; safety work must keep up.

1. Open with the iPhone question and explain greater capability can create greater risk.
2. **Hard to Control:** black boxes and inconsistent refusal of differently worded requests. Teach training, screening during use and tool/permission limits. Ask whether safeguards will keep up.
3. **Bad Actors Cause Harm:** explain jailbreaking and the many-paths/one-opening problem. Misuse also combines ordinary abilities. Teach the three scam steps, then the callback advice as protection. Explain how growing abilities expand harmful use.
4. **AI Can Miss the Intent:** explain misunderstandings and pursuit outside intended limits. Introduce the July 2026 cybersecurity test, reduced safeguards and agents using tools. Teach assignment, crossed boundary and harm. Continue with collaboration, cheating, altered records aimed at the scoring system, and the absence of instructions to access the internet or attack Hugging Face.
5. **Red Teams:** deliberate testing for dangerous behavior and weaknesses, repeated as abilities grow.
6. **Close:** “More powerful AI. Higher stakes.” / “Safety has to keep up.” Nothing afterward.

The scam arrows show the sequence leading to the fake call; the yellow banner interrupts the scam rather than adding a fourth step. The incident cards connect assignment, unauthorized access and harm. The expanded incident aftermath is under its own source heading so it can use supporting scenes instead of extending the board hold.

## Visual plan

All four uploads are current canonical assets, inspected for text and visible faces. No faceless substitutes are needed. The jailbreak illustration is retired from this package; the old source asset is preserved.

| Board | Highlight sequence and camera | Estimated teaching time / breaks |
|---|---|---|
| AI Safety Layers | Open full and unmarked; Train for Safety → Screen for Harm → Limit What AI Can Do. Use complete-card focus only if the 720p legibility check requires it. No banner. | About 30–38 seconds; insert a supporting scene after screening if needed to avoid an uninterrupted hold over 20 seconds. |
| The Voice-Clone Scam | Full unmarked overview, then Voice Clip → Voice Cloned → Fake Call; finally ring the entire yellow callback banner. The callback is advice, not step four. | About 25–32 seconds; allow a supporting phone scene between the fake call and callback if the generated pacing requires it. |
| A Test Became a Real Cyberattack | Full unmarked overview; Assignment → Boundary Crossed → Harm. No banner. Complete cards remain visible during any focus move. | About 20–25 seconds; leave the board for the expanded cheating/records paragraph. |
| Closing Message | Canonical close, standard settled opening hold and slow push; no highlight. | Standard 48-frame hold, 150-frame push to 1.2x, settled ending at 30 fps, extended if narration requires it. |

These are planning estimates, not edit timestamps. After narration review, map actual phrase onsets and source transitions into the edit plan. Use one active 4 px ring at 720p, applied after the camera transform. Do not add pauses merely to accommodate ring/camera changes. Preserve useful generated scenes; no obsolete section labels, removed banners, Spot example, Safety Runs Behind section or four-step scam board.

## Verification and remaining work

The source uses the approved lesson text; board-title connective sentences are adjusted only to read naturally aloud. Required prompt lines stand alone in the source. The narration excludes activities, assessment, links and credits. Do not add claims about malice, precise counts, lawsuits or compensation.

Before generation: run `sync_gemini_notebook.py --lesson big-downside` and `--check`.
After generation: review complete narration against the current source, then finalize the timed edit plan and board previews. Build the next unused candidate, currently `Prompts/big-downside-v12.mp4`, from the fresh raw roll. Review narration, board text, highlights, transitions, audio seams and final closing frame before installing any finished video. Do not report preparation as a completed video.
